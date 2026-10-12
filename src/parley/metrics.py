"""Per-episode metrics, including distance from game-theoretic reference solutions."""

from typing import Any

from parley.core.spec import GameSpec, MatrixScoring, SurplusScoring, ValuationsScoring
from parley.core.types import Outcome, Turn


def episode_metrics(
    spec: GameSpec, turns: list[Turn], outcome: Outcome, refs: dict[str, Any]
) -> dict[str, float]:
    m: dict[str, float] = {
        "messages": len(turns),
        "retries": sum(t.retries for t in turns),
        "tokens": sum(sum(t.tokens.values()) for t in turns),
        "deal": float(outcome.deal is not None),
    }
    s = spec.scoring
    if isinstance(s, SurplusScoring) and outcome.deal and refs.get("max_joint_surplus"):
        # Share of the available surplus each role captured (0.5 each = Nash split).
        for role, p in outcome.payoffs.items():
            m[f"surplus_share.{role}"] = p / refs["max_joint_surplus"]
    if isinstance(s, ValuationsScoring) and outcome.deal:
        welfare = sum(outcome.payoffs.values())
        m["welfare_ratio"] = welfare / sum(refs["max_welfare"]["payoffs"].values())
        frontier = [pt["payoffs"] for pt in refs["pareto_frontier"]]
        m["pareto_optimal"] = float(outcome.payoffs in frontier)
    if isinstance(s, MatrixScoring):
        moves = [t for t in turns if t.phase == "move" and t.action]
        cooperate = spec.protocol.moves[0]
        for role in spec.role_names():
            mine = [t.action.type for t in moves if t.role == role]
            if mine:
                m[f"cooperation_rate.{role}"] = mine.count(cooperate) / len(mine)
        rounds = {}
        for t in moves:
            rounds.setdefault(t.round, []).append(t.action.type)
        if rounds:
            m["mutual_cooperation_rate"] = sum(
                all(a == cooperate for a in acts) for acts in rounds.values()
            ) / len(rounds)
    if outcome.deal and outcome.deal.source == "judge_extracted":
        m["judge_extracted"] = 1.0
    return m
