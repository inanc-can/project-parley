"""GameSpec: the shared, co-authored definition of a game."""

from typing import Annotated, Literal

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


class Alternating(BaseModel):
    """Roles speak in turn. Ends on accept, walk away, (optionally) reject, or the message limit."""

    kind: Literal["alternating"] = "alternating"
    max_messages: int = 20
    first: int = 0  # index into roles
    reject_ends: bool = False  # ultimatum-style: a rejection ends the game with no deal


class SimultaneousRounds(BaseModel):
    """Each round: a short alternating talk phase, then every role moves at once."""

    kind: Literal["simultaneous_rounds"] = "simultaneous_rounds"
    rounds: int = 10
    talk_messages: int = 2  # messages per round before moving; 0 = no talk
    moves: list[str] = Field(default_factory=lambda: ["cooperate", "defect"])
    show_horizon: bool = True  # tell players how many rounds there are


Protocol = Annotated[Alternating | SimultaneousRounds, Field(discriminator="kind")]

ALTERNATING_ACTIONS = ["offer", "accept", "reject", "walk_away"]


class GameSpec(BaseModel):
    title: str
    shared_context: str
    roles: list[Role]
    deal_fields: list[DealField] = Field(default_factory=list)
    scoring: Scoring
    protocol: Protocol = Field(default_factory=Alternating)
    # role name -> allowed action types; None means every action the protocol offers
    allowed_actions: dict[str, list[str]] | None = None
    runs: int = 1
    judge_rubric: str | None = None

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

    def role(self, name: str) -> Role:
        return next(r for r in self.roles if r.name == name)

    def role_names(self) -> list[str]:
        return [r.name for r in self.roles]

    def actions_for(self, role: str) -> list[str]:
        base = (
            ALTERNATING_ACTIONS
            if isinstance(self.protocol, Alternating)
            else list(self.protocol.moves)
        )
        if self.allowed_actions and role in self.allowed_actions:
            return [a for a in base if a in self.allowed_actions[role]]
        return base
