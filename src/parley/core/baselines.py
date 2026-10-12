"""Game-theoretic reference solutions, derived from a spec's scoring and protocol.

They apply to user-written games too, whenever the scoring is structured.
"""

import itertools
import math
from typing import Any

from parley.core.scoring import deal_payoffs, role_payoff
from parley.core.spec import (
    Alternating,
    GameSpec,
    MatrixScoring,
    SimultaneousRounds,
    SurplusScoring,
    ValuationsScoring,
)


def reference_solutions(spec: GameSpec) -> dict[str, Any]:
    s = spec.scoring
    if isinstance(s, SurplusScoring):
        return _surplus(spec, s)
    if isinstance(s, ValuationsScoring):
        return _valuations(spec, s)
    if isinstance(s, MatrixScoring):
        return _matrix(spec, s)
    return {}


def is_ultimatum(spec: GameSpec) -> bool:
    p = spec.protocol
    return isinstance(p, Alternating) and p.reject_ends and p.max_messages == 2


def _surplus(spec: GameSpec, s: SurplusScoring) -> dict[str, Any]:
    up = next(r for r in spec.roles if s.direction[r.name] == "up")
    down = next(r for r in spec.roles if s.direction[r.name] == "down")
    lo = up.private_values.get("reservation", 0.0) + up.private_values.get("no_deal", 0.0)
    hi = down.private_values.get("reservation", 0.0) - down.private_values.get("no_deal", 0.0)
    out: dict[str, Any] = {
        "zopa": [lo, hi] if lo <= hi else None,  # prices both prefer to no deal
        "max_joint_surplus": max(hi - lo, 0.0),
    }
    if lo > hi:
        return out
    if is_ultimatum(spec):
        # Subgame-perfect equilibrium: the responder accepts any positive amount,
        # so the proposer keeps all but the smallest unit.
        field = next(f for f in spec.deal_fields if f.name == s.field)
        unit = 1 if field.type == "integer" else 0
        proposer = spec.roles[spec.protocol.first].name
        value = hi - unit if s.direction[proposer] == "up" else lo + unit
        out["spe"] = {"terms": {s.field: value}, "payoffs": deal_payoffs(spec, {s.field: value})}
    # Nash bargaining solution (symmetric, disagreement = no-deal values): split the surplus.
    mid = (lo + hi) / 2
    out["nash_bargaining"] = {
        "terms": {s.field: mid},
        "payoffs": deal_payoffs(spec, {s.field: mid}),
    }
    return out


def _valuations(spec: GameSpec, s: ValuationsScoring) -> dict[str, Any]:
    names = spec.role_names()
    items = list(s.items)
    points = []
    for combo in itertools.product(*(range(s.items[i] + 1) for i in items)):
        terms = dict(zip(items, combo, strict=True))
        points.append((terms, deal_payoffs(spec, terms)))

    def dominated(p, q):  # q dominates p
        return all(q[n] >= p[n] for n in names) and any(q[n] > p[n] for n in names)

    frontier = [(t, p) for t, p in points if not any(dominated(p, q) for _, q in points)]
    best_welfare = max(points, key=lambda tp: sum(tp[1].values()))
    disagree = {r.name: role_payoff(s, r.name, r.private_values, None) for r in spec.roles}
    feasible = [(t, p) for t, p in points if all(p[n] >= disagree[n] for n in names)]
    nash = max(
        feasible,
        key=lambda tp: math.prod(tp[1][n] - disagree[n] for n in names),
        default=None,
    )
    return {
        "pareto_frontier": [{"terms": t, "payoffs": p} for t, p in frontier],
        "max_welfare": {"terms": best_welfare[0], "payoffs": best_welfare[1]},
        "nash_bargaining": {"terms": nash[0], "payoffs": nash[1]} if nash else None,
        "no_deal": disagree,
    }


def _matrix(spec: GameSpec, s: MatrixScoring) -> dict[str, Any]:
    p = spec.protocol
    assert isinstance(p, SimultaneousRounds)
    names = spec.role_names()
    moves = p.moves

    # Pure-strategy Nash equilibria of the one-shot stage game.
    def pay(profile):
        return s.payoffs[",".join(profile)]

    stage_ne = []
    for profile in itertools.product(moves, repeat=len(names)):
        if all(
            pay(profile)[i] >= pay(profile[:i] + (m,) + profile[i + 1 :])[i]
            for i in range(len(names))
            for m in moves
        ):
            stage_ne.append(profile)
    welfare_best = max(itertools.product(moves, repeat=len(names)), key=lambda pr: sum(pay(pr)))

    def totals(profile):
        return {n: pay(profile)[i] * p.rounds for i, n in enumerate(names)}

    out: dict[str, Any] = {
        "stage_nash": [dict(zip(names, pr, strict=True)) for pr in stage_ne],
        "max_welfare_profile": dict(zip(names, welfare_best, strict=True)),
        "max_welfare_payoffs": totals(welfare_best),
    }
    if len(stage_ne) == 1:
        # With a unique stage equilibrium and a known horizon, backward induction says
        # play it every round (finite prisoner's dilemma: always defect).
        key = "spe_known_horizon" if p.show_horizon else "stage_nash_every_round"
        out[key] = {"profile": out["stage_nash"][0], "payoffs": totals(stage_ne[0])}
    return out
