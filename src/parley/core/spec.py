"""GameSpec: the shared, co-authored definition of a game."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, model_validator


class Role(BaseModel):
    name: str
    private_brief: str = ""  # shown only to this role's agent
    private_values: dict[str, float] = Field(default_factory=dict)  # e.g. {"reservation": 8000}


class DealField(BaseModel):
    name: str
    type: Literal["number", "integer"] = "number"
    min: float | None = None
    max: float | None = None
    description: str = ""


# --- Scoring ---------------------------------------------------------------


class SurplusScoring(BaseModel):
    """Payoff is linear in one deal field, measured from the role's `reservation` value.

    direction "up": payoff = value - reservation (a seller); "down": reservation - value (a buyer).
    No deal pays private_values["no_deal"] (default 0).
    """

    kind: Literal["surplus"] = "surplus"
    field: str
    direction: dict[str, Literal["up", "down"]]


class ValuationsScoring(BaseModel):
    """Items are split; terms give how many of each item `allocation_role` receives.

    Each role values items through private_values[item]; the other role gets the remainder.
    """

    kind: Literal["valuations"] = "valuations"
    items: dict[str, int]  # item -> total count
    allocation_role: str


class MatrixScoring(BaseModel):
    """Per-round payoffs from simultaneous moves, summed over rounds (e.g. the prisoner's dilemma).

    Keys are the moves joined with "," in role order; values are payoffs in role order.
    """

    kind: Literal["matrix"] = "matrix"
    payoffs: dict[str, tuple[float, ...]]


class JudgeOnlyScoring(BaseModel):
    kind: Literal["judge_only"] = "judge_only"


Scoring = Annotated[
    SurplusScoring | ValuationsScoring | MatrixScoring | JudgeOnlyScoring,
    Field(discriminator="kind"),
]


# --- Protocols -------------------------------------------------------------


class Conversation(BaseModel):
    """One continuous conversation; any message may carry an offer, accept, reject or walk-away.

    "natural" turn-taking: a turn may also pass (stay silent) or ask to follow up (speak again
    right away, at most `max_follow_ups` times in a row). Ends on accept, walk away, (optionally)
    reject, everyone passing in a row ("silence"), or `max_messages` ("limit"). With
    `show_limit` False the cap is a safety net the agents are not told about.
    "strict": roles alternate, one message each, and the cap is shown (the classic setup).
    """

    kind: Literal["conversation"] = "conversation"
    turn_taking: Literal["natural", "strict"] = "natural"
    max_messages: int = 40  # every turn counts, passes included
    show_limit: bool = False  # tell agents how many messages are left
    max_follow_ups: int = 2  # natural only
    first: int = 0  # index into roles
    reject_ends: bool = False  # ultimatum-style: a rejection ends the game with no deal


def strict_alternation(max_messages: int = 20, **kw) -> Conversation:
    """The classic alternating-offers preset: strict turns and a visible message limit."""
    return Conversation(turn_taking="strict", show_limit=True, max_messages=max_messages, **kw)


class SimultaneousRounds(BaseModel):
    """Each round: a short alternating talk phase, then every role moves at once."""

    kind: Literal["simultaneous_rounds"] = "simultaneous_rounds"
    rounds: int = 10
    talk_messages: int = 2  # messages per round before moving; 0 = no talk
    moves: list[str] = Field(default_factory=lambda: ["cooperate", "defect"])
    show_horizon: bool = True  # tell players how many rounds there are


Protocol = Annotated[Conversation | SimultaneousRounds, Field(discriminator="kind")]

CONVERSATION_ACTIONS = ["offer", "accept", "reject", "walk_away"]
PASS = "pass"  # natural turn-taking: stay silent this turn (not a formal decision)


class SharedFile(BaseModel):
    """A file added to the shared context, kept as the text every agent reads. Images and other
    non-text files hold a description written when they were added."""

    name: str
    mime: str = ""
    sha256: str = ""  # of the original bytes, so a study can tell which file was used
    text: str


class GameSpec(BaseModel):
    title: str
    shared_context: str
    files: list[SharedFile] = Field(default_factory=list)
    roles: list[Role]
    deal_fields: list[DealField] = Field(default_factory=list)
    scoring: Scoring
    protocol: Protocol = Field(default_factory=Conversation)
    # role name -> allowed action types; None means every action the protocol offers
    allowed_actions: dict[str, list[str]] | None = None
    runs: int = 1
    judge_rubric: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _upgrade_protocol(cls, data: Any) -> Any:
        """Specs saved before 2026-10-18 use {"kind": "alternating"}: the strict preset."""
        if isinstance(data, dict):
            p = data.get("protocol")
            if isinstance(p, dict) and p.get("kind") == "alternating":
                data = {
                    **data,
                    "protocol": {
                        **p,
                        "kind": "conversation",
                        "turn_taking": "strict",
                        "show_limit": True,
                    },
                }
        return data

    @model_validator(mode="after")
    def _check(self) -> "GameSpec":
        names = [r.name for r in self.roles]
        if len(set(names)) != len(names):
            raise ValueError("role names must be unique")
        if len(names) < 2:
            raise ValueError("a game needs at least two roles")
        s = self.scoring
        if isinstance(s, SurplusScoring):
            if s.field not in {f.name for f in self.deal_fields}:
                raise ValueError(f"scoring field {s.field!r} is not a deal field")
            if set(s.direction) != set(names):
                raise ValueError("surplus scoring needs a direction for every role")
        if isinstance(s, ValuationsScoring) and s.allocation_role not in names:
            raise ValueError(f"unknown allocation role {s.allocation_role!r}")
        if isinstance(s, MatrixScoring) and not isinstance(self.protocol, SimultaneousRounds):
            raise ValueError("matrix scoring needs the simultaneous_rounds protocol")
        return self

    def full_context(self) -> str:
        """The shared context followed by the text of every shared file."""
        parts = [self.shared_context]
        if self.files:
            parts.append("## Shared files (every player has these)")
            parts += [f"### {f.name}\n{f.text}" for f in self.files]
        return "\n\n".join(p for p in parts if p)

    def role(self, name: str) -> Role:
        return next(r for r in self.roles if r.name == name)

    def role_names(self) -> list[str]:
        return [r.name for r in self.roles]

    def actions_for(self, role: str) -> list[str]:
        p = self.protocol
        base = CONVERSATION_ACTIONS if isinstance(p, Conversation) else list(p.moves)
        if self.allowed_actions and role in self.allowed_actions:
            base = [a for a in base if a in self.allowed_actions[role]]
        if isinstance(p, Conversation) and p.turn_taking == "natural":
            base = [*base, PASS]  # silence is always allowed; it is not a decision
        return base
