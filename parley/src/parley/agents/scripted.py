"""Deterministic agents: baselines for experiments and the backbone of tests."""

from typing import Any

from parley.core.agent import RoleView
from parley.core.scoring import role_payoff
from parley.core.types import Action, Turn


class ThresholdAgent:
    """Accepts any offer worth at least `min_payoff` to it; otherwise proposes.

    Proposals are made in order (the last one repeats), so a falling list is a conceder.
    If it may not offer (e.g. an ultimatum responder), it rejects instead.
    """

    def __init__(self, proposals: list[dict[str, Any]], min_payoff: float):
        self.proposals = proposals
        self.min_payoff = min_payoff
        self._next = 0

    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        offer = view.standing_offer
        if offer and offer.role != view.role:
            value = role_payoff(view.scoring, view.role, view.private_values, offer.terms)
            if value is not None and value >= self.min_payoff and "accept" in view.allowed_actions:
                return Turn(role=view.role, message="Deal.", action=Action(type="accept"))
        if "offer" in view.allowed_actions and self.proposals:
            terms = self.proposals[min(self._next, len(self.proposals) - 1)]
            self._next += 1
            return Turn(
                role=view.role,
                message=f"I propose {terms}.",
                action=Action(type="offer", terms=terms),
            )
        if offer and "reject" in view.allowed_actions:
            return Turn(role=view.role, message="No.", action=Action(type="reject"))
        return Turn(role=view.role, message="...")


class WalkAwayAgent:
    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        return Turn(role=view.role, message="I'm out.", action=Action(type="walk_away"))


class SilentAgent:
    """Talks but never acts; useful to hit message limits."""

    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        return Turn(role=view.role, message="Hmm.")


class MatrixStrategy:
    """Simultaneous-move strategies: always_cooperate, always_defect, tit_for_tat, grim_trigger."""

    def __init__(self, strategy: str, cooperate: str = "cooperate", defect: str = "defect"):
        if strategy not in ("always_cooperate", "always_defect", "tit_for_tat", "grim_trigger"):
            raise ValueError(f"unknown strategy {strategy!r}")
        self.strategy, self.C, self.D = strategy, cooperate, defect

    def _choose(self, view: RoleView) -> str:
        others = [m for rnd in view.move_history for r, m in rnd.items() if r != view.role]
        match self.strategy:
            case "always_cooperate":
                return self.C
            case "always_defect":
                return self.D
            case "tit_for_tat":
                return others[-1] if others else self.C
            case _:  # grim_trigger
                return self.D if self.D in others else self.C

    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        if view.phase == "talk":
            return Turn(role=view.role, message="Let's both cooperate.")
        return Turn(role=view.role, message="", action=Action(type=self._choose(view)))
