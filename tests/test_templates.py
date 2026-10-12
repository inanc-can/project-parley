from parley.agents.scripted import MatrixStrategy, ThresholdAgent
from parley.core.baselines import reference_solutions
from parley.core.engine import run_episode
from parley.templates import (
    TEMPLATES,
    buy_sell,
    iterated_prisoners_dilemma,
    multi_issue_trade,
    ultimatum,
)


def test_all_templates_build():
    for make in TEMPLATES.values():
        assert make().title


def test_ultimatum_spe_keeps_all_but_one():
    ref = reference_solutions(ultimatum(100))
    assert ref["spe"]["terms"] == {"proposer_share": 99}
    assert ref["spe"]["payoffs"] == {"proposer": 99, "responder": 1}
    assert ref["nash_bargaining"]["terms"] == {"proposer_share": 50}


def test_buy_sell_zopa_and_split():
    ref = reference_solutions(buy_sell(8000, 9500))
    assert ref["zopa"] == [8000, 9500]
    assert ref["max_joint_surplus"] == 1500
    assert ref["nash_bargaining"]["payoffs"] == {"seller": 750, "buyer": 750}
    assert "spe" not in ref


def test_no_zopa():
    ref = reference_solutions(buy_sell(9000, 8000))
    assert ref["zopa"] is None and ref["max_joint_surplus"] == 0


def test_ipd_backward_induction():
    ref = reference_solutions(iterated_prisoners_dilemma(rounds=10))
    assert ref["stage_nash"] == [{"player_a": "defect", "player_b": "defect"}]
    assert ref["spe_known_horizon"]["payoffs"] == {"player_a": 10, "player_b": 10}
    assert ref["max_welfare_payoffs"] == {"player_a": 30, "player_b": 30}


def test_trade_frontier_and_welfare():
    ref = reference_solutions(multi_issue_trade())
    # alex values hats (3) most, blair values books and the ball (2 each):
    # alex takes both hats, blair takes everything else.
    assert ref["max_welfare"]["terms"] == {"books": 0, "hats": 2, "balls": 0}
    assert ref["max_welfare"]["payoffs"] == {"alex": 6, "blair": 8}
    assert {
        "terms": {"books": 0, "hats": 2, "balls": 0},
        "payoffs": {"alex": 6, "blair": 8},
    } in ref["pareto_frontier"]


async def test_templates_play_with_scripted_agents():
    _, out = await run_episode(
        iterated_prisoners_dilemma(rounds=3),
        {"player_a": MatrixStrategy("tit_for_tat"), "player_b": MatrixStrategy("tit_for_tat")},
    )
    assert out.payoffs == {"player_a": 9, "player_b": 9}

    _, out = await run_episode(
        multi_issue_trade(),
        {
            "alex": ThresholdAgent([{"books": 0, "hats": 2, "balls": 0}], min_payoff=6),
            "blair": ThresholdAgent([{"books": 3, "hats": 0, "balls": 1}], min_payoff=8),
        },
    )
    assert out.end_reason == "accept" and out.payoffs == {"alex": 6, "blair": 8}
