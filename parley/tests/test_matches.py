import json

import pytest

from parley.api.rooms import match_summary
from parley.llm.client import LLMClient, LLMResponse
from parley.matches.runner import MatchConfig, assignment_for, run_match
from parley.matches.seats import LLMSeat, ScriptedSeat
from parley.storage import Store
from parley.templates import buy_sell, iterated_prisoners_dilemma


def test_roles_rotate_between_runs():
    spec = buy_sell()
    assert assignment_for(spec, ["A", "B"], 0, True) == {"seller": "A", "buyer": "B"}
    assert assignment_for(spec, ["A", "B"], 1, True) == {"seller": "B", "buyer": "A"}
    assert assignment_for(spec, ["A", "B"], 1, False) == {"seller": "A", "buyer": "B"}


async def test_match_runs_stores_and_exports(tmp_path):
    cfg = MatchConfig(
        spec=iterated_prisoners_dilemma(rounds=4),
        seats={"A": ScriptedSeat(name="tit_for_tat"), "B": ScriptedSeat(name="always_defect")},
        runs=4,
    )
    events = []

    async def on_event(e):
        events.append(e)

    records = await run_match(cfg, LLMClient(), "m1", on_event)
    assert len(records) == 4
    r0, r1 = records[0], records[1]
    assert r0.assignment == {"player_a": "A", "player_b": "B"}
    assert r1.assignment == {"player_a": "B", "player_b": "A"}
    assert r0.outcome.payoffs == {"player_a": 3, "player_b": 8}  # (0,5) + 3×(1,1)
    assert r0.outcome.metrics["cooperation_rate.player_a"] == 0.25
    assert r0.reference["spe_known_horizon"]["payoffs"] == {"player_a": 4, "player_b": 4}
    assert r0.seed != r1.seed
    assert sum(e["type"] == "turn" for e in events) == 4 * 4 * (2 + 2)
    assert events[-1] == {"type": "match_end", "match_id": "m1"}

    store = Store(tmp_path / "db.sqlite")
    store.create_match("m1", cfg)
    for r in records:
        store.save_episode(r)
    store.set_status("m1", "done")
    assert store.matches()[0]["status"] == "done"
    assert [e.index for e in store.episodes("m1")] == [0, 1, 2, 3]
    assert store.export_jsonl("m1", tmp_path / "m1.jsonl") == 4
    assert len((tmp_path / "m1.jsonl").read_text().splitlines()) == 4


async def test_bargaining_surplus_share_metric():
    cfg = MatchConfig(
        spec=buy_sell(8000, 9500),
        seats={
            "A": ScriptedSeat(
                name="threshold", params={"proposals": [{"price": 9000}], "min_payoff": 500}
            ),
            "B": ScriptedSeat(
                name="threshold", params={"proposals": [{"price": 9000}], "min_payoff": 500}
            ),
        },
        runs=1,
    )
    [rec] = await run_match(cfg, LLMClient())
    assert rec.outcome.deal.terms == {"price": 9000}
    assert rec.outcome.metrics["surplus_share.seller"] == 1000 / 1500


class FlakyClient(LLMClient):
    """Raises `error` for the first `failures` calls, then walks away on every turn."""

    def __init__(self, failures: int, error: Exception | None = None):
        import litellm

        super().__init__(retry_delays=())  # exercise the runner's retries, not the client's
        self.failures, self.calls = failures, 0
        self.error = error or litellm.InternalServerError("Extra data", "featherless_ai", "m")

    async def _call(self, model, messages, temperature, max_tokens):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.error
        reply = {"message": "No thanks.", "action": {"type": "walk_away"}}
        return LLMResponse(text=json.dumps(reply), model=model)


def llm_match(runs: int) -> MatchConfig:
    seats = {"A": LLMSeat(model="m"), "B": LLMSeat(model="m")}
    return MatchConfig(spec=buy_sell(), seats=seats, runs=runs, parallel=1)


async def test_failed_episode_is_retried():
    events = []

    async def on_event(e):
        events.append(e)

    [record] = await run_match(llm_match(1), FlakyClient(failures=1), "m", on_event)
    assert record.attempts == 2 and record.error is None
    assert record.outcome.end_reason == "walk_away"
    assert [e["type"] for e in events if e["type"] != "turn"] == [
        "match_start",
        "episode_start",
        "episode_retry",
        "episode_start",
        "episode_end",
        "match_end",
    ]


async def test_episode_that_keeps_failing_is_recorded_and_the_match_goes_on(tmp_path):
    store = Store(tmp_path / "db.sqlite")
    store.create_match("m", llm_match(2))
    # 3 failed attempts sink episode 0; episode 1 then plays normally.
    records = await run_match(llm_match(2), FlakyClient(failures=3), "m", None, store.save_episode)
    assert [r.error is not None for r in records] == [True, False]
    assert records[0].outcome.end_reason == "error" and records[0].attempts == 3
    assert "Extra data" in records[0].error
    assert len(store.episodes("m")) == 2  # saved as each one ended
    assert store.mark_interrupted() == 1  # as on the next server start
    assert store.matches()[0]["status"] == "interrupted"
    summary = match_summary(records)
    assert summary["failed"] == 1 and summary["end_reasons"] == {"error": 1, "walk_away": 1}
    assert summary["mean_payoff_by_seat"] == {"A": 0, "B": 0}  # only the played episode


async def test_setup_errors_stop_the_match():
    import litellm

    bad_key = litellm.AuthenticationError("bad key", "featherless_ai", "m")
    with pytest.raises(litellm.AuthenticationError):
        await run_match(llm_match(2), FlakyClient(failures=99, error=bad_key), "m")


async def test_client_waits_out_transient_errors_but_not_setup_errors():
    import litellm

    client = FlakyClient(failures=2)
    client.retry_delays = (0, 0)
    resp = await client.complete("m", [{"role": "user", "content": "hi"}])
    assert client.calls == 3 and "walk_away" in resp.text

    bad_key = FlakyClient(failures=9, error=litellm.AuthenticationError("bad key", "x", "m"))
    bad_key.retry_delays = (0, 0)
    with pytest.raises(litellm.AuthenticationError):
        await bad_key.complete("m", [{"role": "user", "content": "hi"}])
    assert bad_key.calls == 1
