import json

import pytest

from parley.agents.llm import LLMAgent
from parley.agents.parsing import extract_json, parse_turn
from parley.agents.scripted import SilentAgent
from parley.agents.team import Critic, TeamAgent
from parley.core.agent import TurnError
from parley.core.engine import run_episode
from parley.core.spec import Alternating
from parley.judge import Judge, apply_judgment
from parley.llm.cache import Cache
from parley.llm.client import LLMClient, LLMResponse
from parley.templates import buy_sell, iterated_prisoners_dilemma


class FakeClient(LLMClient):
    """Returns queued replies instead of calling a provider; records prompts."""

    def __init__(self, *replies, cache=None):
        super().__init__(cache=cache)
        self.replies, self.prompts = list(replies), []

    async def _call(self, model, messages, temperature, max_tokens):
        self.prompts.append(messages)
        text = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        return LLMResponse(text=text, model=model, tokens={"prompt": 10, "completion": 5})


def reply(message="", action=None, reasoning="thinking"):
    return json.dumps({"reasoning": reasoning, "message": message, "action": action})


def test_extract_json_tolerates_fences_and_prose():
    assert extract_json('Sure!\n```json\n{"message": "hi"}\n```') == {"message": "hi"}
    assert extract_json('{bad} then {"a": 1}') == {"a": 1}


def test_extract_json_repairs_an_object_closed_too_early():
    text = '{"reasoning": "too high"},  "message": "No.", "action": {"type": "walk_away"}}'
    turn = parse_turn(text, "buyer")
    assert (turn.reasoning, turn.message, turn.action.type) == ("too high", "No.", "walk_away")
    with pytest.raises(TurnError, match='no "message"'):
        parse_turn('{"reasoning": "hmm"}', "buyer")


async def test_reprompts_are_fresh_samples_even_with_the_cache(tmp_path):
    client = FakeClient("nope", reply("Deal?"), cache=Cache(tmp_path / "c.sqlite"))
    turns, _ = await run_episode(
        buy_sell(), {"seller": LLMAgent(client, "m"), "buyer": SilentAgent()}
    )
    assert turns[0].message == "Deal?" and turns[0].retries == 1
    assert "(attempt 2 of 4)" in client.prompts[1][-1]["content"]


def test_parse_turn_rejects_an_empty_reply():
    with pytest.raises(TurnError, match="empty"):
        parse_turn(reply(message="  "), "seller")
    assert parse_turn(reply(action="accept"), "seller").action.type == "accept"


def test_parse_turn_accepts_bare_action_string():
    t = parse_turn('{"message": "no", "action": "reject"}', "buyer")
    assert t.action.type == "reject" and t.role == "buyer"


async def test_llm_agent_makes_offer_and_sees_private_brief():
    client = FakeClient(reply("I ask 10,500.", {"type": "offer", "terms": {"price": 10500}}))
    spec = buy_sell().model_copy(update={"protocol": Alternating(max_messages=1)})
    turns, _ = await run_episode(
        spec, {"seller": LLMAgent(client, "m", strategy="Anchor high."), "buyer": SilentAgent()}
    )
    assert turns[0].action.terms == {"price": 10500}
    assert turns[0].reasoning == "thinking" and turns[0].tokens["prompt"] == 10
    system = client.prompts[0][0]["content"]
    assert "8,000" in system and "Anchor high." in system
    assert "9,500" not in system  # the buyer's private limit is not leaked


async def test_malformed_output_is_retried_with_feedback():
    client = FakeClient(
        "I'd like 10k please", reply("10k", {"type": "offer", "terms": {"price": 10000}})
    )
    spec = buy_sell().model_copy(update={"protocol": Alternating(max_messages=1)})
    turns, _ = await run_episode(spec, {"seller": LLMAgent(client, "m"), "buyer": SilentAgent()})
    assert turns[0].retries == 1
    assert "not a JSON object" in client.prompts[1][1]["content"]


async def test_hopeless_llm_forfeits():
    client = FakeClient("nope")
    _, out = await run_episode(
        buy_sell(), {"seller": LLMAgent(client, "m"), "buyer": SilentAgent()}
    )
    assert out.end_reason == "forfeit" and out.forfeited_by == "seller"
    assert [f["output"] for f in out.forfeit_attempts] == ["nope"] * 4  # first try + 3 re-prompts
    assert "not a JSON object" in out.forfeit_attempts[0]["error"]


async def test_ipd_move_phase():
    client = FakeClient(reply("let's cooperate"), reply("agreed"), reply("", {"type": "cooperate"}))
    spec = iterated_prisoners_dilemma(rounds=1, talk_messages=2)
    agent = LLMAgent(client, "m")
    _, out = await run_episode(spec, {"player_a": agent, "player_b": agent})
    assert out.payoffs == {"player_a": 3, "player_b": 3}


async def test_team_agent_logs_deliberation():
    client = FakeClient(
        reply("10k", {"type": "offer", "terms": {"price": 10000}}),  # proposer draft
        "- too low, ask more",  # critic
        reply("11k", {"type": "offer", "terms": {"price": 11000}}),  # decider
    )
    team = TeamAgent(LLMAgent(client, "big"), Critic(client, "small"))
    spec = buy_sell().model_copy(update={"protocol": Alternating(max_messages=1)})
    turns, _ = await run_episode(spec, {"seller": team, "buyer": SilentAgent()})
    t = turns[0]
    assert t.action.terms == {"price": 11000}
    assert [d["step"] for d in t.deliberation] == ["proposer", "critic", "decider"]
    assert t.deliberation[1]["text"] == "- too low, ask more"
    assert t.tokens == {"prompt": 30, "completion": 15}
    assert "too low" in client.prompts[2][1]["content"]  # decider saw the critique


async def test_cache_makes_reruns_free_but_seeds_distinct(tmp_path):
    cache = Cache(tmp_path / "c.sqlite")
    client = FakeClient("a", cache=cache)
    msgs = [{"role": "user", "content": "hi"}]
    await client.complete("m", msgs, seed=1)
    again = await client.complete("m", msgs, seed=1)
    other = await client.complete("m", msgs, seed=2)
    assert again.cached and not other.cached and len(client.prompts) == 2


async def test_judge_extracts_words_only_deal():
    spec = buy_sell()
    from parley.core.types import Outcome, Turn

    turns = [
        Turn(role="buyer", message="ok, 9,100 works"),
        Turn(role="seller", message="great, done"),
    ]
    limit = Outcome(end_reason="limit", payoffs={"seller": 0, "buyer": 0})
    judgment_json = json.dumps(
        {
            "deal_reached": True,
            "deal_terms": {"price": 9100},
            "confidence": 0.86,
            "rubric": {"seller": {"honesty": 4}},
            "summary": "s",
            "evidence": ["ok, 9,100 works"],
        }
    )
    judge = Judge(FakeClient(judgment_json), "judge-model")
    judgment = await judge.assess(spec, turns, limit)
    out = apply_judgment(spec, limit, judgment)
    assert out.deal.source == "judge_extracted" and out.deal.confidence == 0.86
    assert out.payoffs == {"seller": 1100, "buyer": 400}

    walked = Outcome(end_reason="walk_away", payoffs={"seller": 0, "buyer": 0})
    assert apply_judgment(spec, walked, judgment).deal is None  # a formal walk-away stands
