from parley.llm.client import LLMClient
from parley.matches.runner import MatchConfig, assignment_for, run_match
from parley.matches.seats import ScriptedSeat
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
