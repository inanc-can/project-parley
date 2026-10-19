"""What an agent sees (RoleView) and what it must implement (Agent)."""

from typing import Any, Literal, Protocol

from pydantic import BaseModel

from parley.core.spec import DealField, Scoring
from parley.core.spec import Protocol as GameProtocol
from parley.core.types import Action, Turn


class PublicTurn(BaseModel):
    """A turn as the other players see it: no private reasoning or deliberation."""

    role: str
    message: str
    action: Action | None = None
    round: int | None = None
    phase: Literal["talk", "move"] | None = None


class StandingOffer(BaseModel):
    role: str
    terms: dict[str, Any]


class RoleView(BaseModel):
    """Everything one role's agent may know at the moment it must speak."""

    title: str
    role: str
    roles: list[str]
    shared_context: str
    private_brief: str
    private_values: dict[str, float]
    deal_fields: list[DealField]
    scoring: Scoring
    protocol: GameProtocol
    allowed_actions: list[str]  # empty in a talk phase
    must_act: bool  # an action is required this turn (simultaneous move)
    transcript: list[PublicTurn]
    standing_offer: StandingOffer | None = None
    messages_left: int | None = None  # None when the limit is hidden
    can_follow_up: bool = False  # natural turn-taking: may ask to speak again right away
    round: int | None = None
    total_rounds: int | None = None  # None when the horizon is hidden
    phase: Literal["talk", "move"] | None = None
    move_history: list[dict[str, str]] = []  # revealed moves of finished rounds


class TurnError(Exception):
    """The agent could not produce a usable turn (e.g. unparseable model output)."""

    raw_output: str | None = None  # the reply that failed, when the agent has one


class Agent(Protocol):
    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        """Return this role's next turn. `feedback` says why the last attempt was invalid."""
        ...
