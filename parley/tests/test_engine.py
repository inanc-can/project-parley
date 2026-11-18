import pytest

from parley.agents.parsing import render_rules
from parley.agents.scripted import MatrixStrategy, SilentAgent, ThresholdAgent, WalkAwayAgent
from parley.core.engine import MAX_RETRIES, run_episode
from parley.core.scoring import InvalidTerms, deal_payoffs, validate_terms
from parley.core.spec import (
    Conversation,
    DealField,
    GameSpec,
    MatrixScoring,
    Role,
    SharedFile,
    SimultaneousRounds,
    SurplusScoring,
    ValuationsScoring,
    strict_alternation,
)
from parley.core.types import Action, Turn


def car_sale(**kw) -> GameSpec:
    return GameSpec(
        title="Used car",
        shared_context="A 2015 Civic is for sale.",
        roles=[
            Role(name="seller", private_values={"reservation": 8000}),
            Role(name="buyer", private_values={"reservation": 9500}),
        ],
        deal_fields=[DealField(name="price", min=0, max=50000)],
        scoring=SurplusScoring(field="price", direction={"seller": "up", "buyer": "down"}),
        **kw,
    )


def prices(*ps):
    return [{"price": p} for p in ps]


async def test_bargaining_reaches_deal():
    turns, out = await run_episode(
        car_sale(),
        {
            "seller": ThresholdAgent(prices(10500, 9800, 9300), min_payoff=1000),
            "buyer": ThresholdAgent(prices(8500, 8800, 9000), min_payoff=200),
        },
    )
    assert out.end_reason == "accept"
    assert out.deal.terms == {"price": 9300}
    assert out.payoffs == {"seller": 1300, "buyer": 200}
    assert [t.role for t in turns] == ["seller", "buyer"] * 3


async def test_walk_away_pays_no_deal_value():
    spec = car_sale()
    spec.roles[0].private_values["no_deal"] = 500
    _, out = await run_episode(spec, {"seller": WalkAwayAgent(), "buyer": SilentAgent()})
    assert out.end_reason == "walk_away"
    assert out.payoffs == {"seller": 500, "buyer": 0}


async def test_message_limit():
    turns, out = await run_episode(
        car_sale(protocol=strict_alternation(4)),
        {"seller": SilentAgent(), "buyer": SilentAgent()},
    )
    assert out.end_reason == "limit" and len(turns) == 4


class Scripted:
    """Plays back a fixed list of turns, recording the feedback it gets."""

    def __init__(self, *turns):
        self.turns, self.feedback = list(turns), []

    async def act(self, view, feedback=None):
        self.feedback.append(feedback)
        return self.turns.pop(0) if len(self.turns) > 1 else self.turns[0]


async def test_invalid_action_is_reprompted_with_feedback():
    bad = Turn(role="seller", action=Action(type="accept"))  # nothing to accept yet
    good = Turn(role="seller", message="10k", action=Action(type="offer", terms={"price": 10000}))
    seller = Scripted(bad, good)
    turns, out = await run_episode(
        car_sale(protocol=strict_alternation(2)),
        {"seller": seller, "buyer": SilentAgent()},
    )
    assert turns[0].retries == 1
    assert "no offer" in seller.feedback[1]


async def test_hopeless_agent_forfeits():
    bad = Turn(role="seller", action=Action(type="offer", terms={"price": -5}))
    seller = Scripted(bad)
    turns, out = await run_episode(car_sale(), {"seller": seller, "buyer": SilentAgent()})
    assert out.end_reason == "forfeit" and out.forfeited_by == "seller"
    assert len(seller.feedback) == MAX_RETRIES + 1 and turns == []


def test_validate_terms():
    spec = car_sale()
    with pytest.raises(InvalidTerms, match="missing"):
        validate_terms(spec.deal_fields, spec.scoring, {})
    with pytest.raises(InvalidTerms, match="unknown"):
        validate_terms(spec.deal_fields, spec.scoring, {"price": 1, "car": 2})
    with pytest.raises(InvalidTerms, match="number"):
        validate_terms(spec.deal_fields, spec.scoring, {"price": "9000"})


async def test_ultimatum_rejection_ends_game():
    spec = GameSpec(
        title="Ultimatum",
        shared_context="Split 100.",
        roles=[Role(name="proposer"), Role(name="responder", private_values={"reservation": 100})],
        deal_fields=[DealField(name="proposer_share", type="integer", min=0, max=100)],
        scoring=SurplusScoring(
            field="proposer_share", direction={"proposer": "up", "responder": "down"}
        ),
        protocol=strict_alternation(2, reject_ends=True),
        allowed_actions={"proposer": ["offer"], "responder": ["accept", "reject"]},
    )
    greedy = ThresholdAgent([{"proposer_share": 70}], min_payoff=0)
    _, out = await run_episode(spec, {"proposer": greedy, "responder": ThresholdAgent([], 40)})
    assert out.end_reason == "reject" and out.payoffs == {"proposer": 0, "responder": 0}

    fair = ThresholdAgent([{"proposer_share": 55}], min_payoff=0)
    _, out = await run_episode(spec, {"proposer": fair, "responder": ThresholdAgent([], 40)})
    assert out.payoffs == {"proposer": 55, "responder": 45}


PD = MatrixScoring(
    payoffs={
        "cooperate,cooperate": (3, 3),
        "cooperate,defect": (0, 5),
        "defect,cooperate": (5, 0),
        "defect,defect": (1, 1),
    }
)


async def test_ipd_tit_for_tat_vs_always_defect():
    spec = GameSpec(
        title="IPD",
        shared_context="Prisoner's dilemma.",
        roles=[Role(name="A"), Role(name="B")],
        scoring=PD,
        protocol=SimultaneousRounds(rounds=5, talk_messages=2),
    )
    turns, out = await run_episode(
        spec, {"A": MatrixStrategy("tit_for_tat"), "B": MatrixStrategy("always_defect")}
    )
    assert out.end_reason == "rounds_complete"
    assert out.payoffs == {"A": 4, "B": 9}  # (0,5) then 4 × (1,1)
    assert len(turns) == 5 * (2 + 2)


def test_valuations_payoffs():
    spec = GameSpec(
        title="Trade",
        shared_context="Split the items.",
        roles=[
            Role(name="A", private_values={"books": 1, "hats": 3}),
            Role(name="B", private_values={"books": 2, "hats": 1}),
        ],
        deal_fields=[
            DealField(name="books", type="integer"),
            DealField(name="hats", type="integer"),
        ],
        scoring=ValuationsScoring(items={"books": 3, "hats": 2}, allocation_role="A"),
    )
    # A gets 0 books, 2 hats; B gets 3 books, 0 hats
    assert deal_payoffs(spec, {"books": 0, "hats": 2}) == {"A": 6, "B": 6}


def test_spec_rejects_bad_scoring_field():
    with pytest.raises(ValueError, match="not a deal field"):
        car_sale().model_copy()  # valid
        GameSpec(
            title="x",
            shared_context="",
            roles=[Role(name="a"), Role(name="b")],
            scoring=SurplusScoring(field="price", direction={"a": "up", "b": "down"}),
        )


# --- Natural turn-taking -----------------------------------------------------


class Says:
    """Plays fresh copies of a script of turns (the last one repeats); records each view."""

    def __init__(self, *script: Turn):
        self.script, self.views, self.feedback = list(script), [], []

    async def act(self, view, feedback=None):
        self.views.append(view)
        self.feedback.append(feedback)
        turn = self.script.pop(0) if len(self.script) > 1 else self.script[0]
        return turn.model_copy(deep=True)


def silent():
    return Turn(role="", action=Action(type="pass"))


async def test_everyone_passing_in_a_row_ends_in_silence():
    seller = Says(Turn(role="", message="Make me an offer."), silent())
    turns, out = await run_episode(car_sale(), {"seller": seller, "buyer": Says(silent())})
    assert out.end_reason == "silence" and out.payoffs == {"seller": 0, "buyer": 0}
    assert [(t.role, t.action and t.action.type) for t in turns] == [
        ("seller", None),
        ("buyer", "pass"),
        ("seller", "pass"),
    ]


async def test_follow_ups_keep_the_floor_up_to_the_limit():
    seller = Says(Turn(role="", message="One more thing", follow_up=True))
    buyer = Says(Turn(role="", message="ok"))
    turns, _ = await run_episode(
        car_sale(protocol=Conversation(max_messages=7, max_follow_ups=2)),
        {"seller": seller, "buyer": buyer},
    )
    # The seller keeps the floor twice, then must yield.
    assert [t.role for t in turns] == ["seller"] * 3 + ["buyer"] + ["seller"] * 3
    assert [v.can_follow_up for v in seller.views[:3]] == [True, True, False]


async def test_hidden_limit_is_not_shown_but_still_ends_the_conversation():
    agents = {
        "seller": Says(Turn(role="", message="hm")),
        "buyer": Says(Turn(role="", message="hm")),
    }
    turns, out = await run_episode(car_sale(protocol=Conversation(max_messages=5)), agents)
    assert out.end_reason == "limit" and len(turns) == 5
    assert all(v.messages_left is None for v in agents["seller"].views)
    assert "at most" not in render_rules(agents["seller"].views[0])


async def test_a_pass_with_words_is_reprompted_and_an_empty_turn_is_a_pass():
    seller = Says(Turn(role="", message="hi", action=Action(type="pass")), Turn(role=""))
    turns, _ = await run_episode(
        car_sale(protocol=Conversation(max_messages=1)), {"seller": seller, "buyer": Says(silent())}
    )
    assert "pass means saying nothing" in seller.feedback[1]
    assert turns[0].action.type == "pass" and turns[0].retries == 1


async def test_deal_can_come_on_the_first_or_the_last_turn():
    offer = Turn(role="", message="10k?", action=Action(type="offer", terms={"price": 9000}))
    accept = Turn(role="", message="Deal.", action=Action(type="accept"))
    _, out = await run_episode(car_sale(), {"seller": Says(offer), "buyer": Says(accept)})
    assert out.end_reason == "accept" and out.deal.terms == {"price": 9000}


def test_pass_is_always_allowed_in_natural_turn_taking_only():
    spec = car_sale(allowed_actions={"seller": ["offer"]})
    assert spec.actions_for("seller") == ["offer", "pass"]
    strict = car_sale(protocol=strict_alternation(4))
    assert "pass" not in strict.actions_for("buyer")


def test_specs_saved_with_the_old_alternating_kind_load_as_strict():
    data = car_sale().model_dump()
    data["protocol"] = {"kind": "alternating", "max_messages": 6, "first": 1, "reject_ends": False}
    p = GameSpec.model_validate(data).protocol
    assert isinstance(p, Conversation)
    assert (p.turn_taking, p.show_limit, p.max_messages, p.first) == ("strict", True, 6, 1)


async def test_agents_read_the_shared_files_after_the_context():
    spec = car_sale(files=[SharedFile(name="report.md", text="Mileage: 120k km.")])
    seller = Says(silent())
    await run_episode(spec, {"seller": seller, "buyer": Says(silent())})
    rules = render_rules(seller.views[0])
    assert spec.shared_context in rules
    assert "## Shared files (every player has these)\n\n### report.md\nMileage: 120k km." in rules
