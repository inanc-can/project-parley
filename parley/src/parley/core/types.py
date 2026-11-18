"""Records produced while an episode is played."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class Action(BaseModel):
    """A formal move attached to a message: offer, accept, reject, walk_away, or a game move."""

    type: str
    terms: dict[str, Any] = Field(default_factory=dict)


class Turn(BaseModel):
    """One message in the dialogue, plus the optional formal action it carries."""

    role: str
    message: str = ""
    action: Action | None = None
    reasoning: str | None = None  # private; never shown to the other side
    follow_up: bool = False  # natural turn-taking: the speaker asked to speak again right away
    deliberation: list[dict[str, Any]] | None = None  # TeamAgent internals
    raw_output: str | None = None
    retries: int = 0
    tokens: dict[str, int] = Field(default_factory=dict)
    round: int | None = None
    phase: Literal["talk", "move"] | None = None


# "silence": every role passed in a row. "limit": the message cap was hit (shown to the agents
# or not; the spec says which). "error": every attempt at the episode failed (provider errors);
# EpisodeRecord.error says why.
EndReason = Literal[
    "accept", "walk_away", "reject", "silence", "limit", "rounds_complete", "forfeit", "error"
]


class Deal(BaseModel):
    terms: dict[str, Any]
    source: Literal["formal", "judge_extracted"] = "formal"
    confidence: float | None = None


class Outcome(BaseModel):
    end_reason: EndReason
    deal: Deal | None = None
    payoffs: dict[str, float] = Field(default_factory=dict)
    forfeited_by: str | None = None
    # The forfeiting role's rejected replies, oldest first: {"error": why, "output": raw text}.
    forfeit_attempts: list[dict[str, str]] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)
    judge: dict[str, Any] | None = None
