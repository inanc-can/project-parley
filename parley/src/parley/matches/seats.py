"""Seat setups: the private, per-person configuration of who plays."""

import hashlib
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from parley.agents import scripted
from parley.agents.live import LiveAgent, Mailbox
from parley.agents.llm import LLMAgent
from parley.agents.team import Critic, TeamAgent
from parley.core.agent import Agent
from parley.llm.client import LLMClient


class LLMSeat(BaseModel):
    kind: Literal["llm"] = "llm"
    model: str
    strategy: str = ""
    temperature: float = 0.7


class TeamSeat(BaseModel):
    kind: Literal["team"] = "team"
    proposer_model: str
    critic_model: str
    decider_model: str | None = None  # default: the proposer decides
    strategy: str = ""
    temperature: float = 0.7


class ScriptedSeat(BaseModel):
    """A deterministic baseline, e.g. {"name": "tit_for_tat"} or
    {"name": "threshold", "params": {"proposals": [...], "min_payoff": 1000}}."""

    kind: Literal["scripted"] = "scripted"
    name: str
    params: dict[str, Any] = Field(default_factory=dict)


class LiveSeat(BaseModel):
    """Played by an agent outside Parley (e.g. Claude Code) through the API's /turn endpoints.
    `client` is a free label such as "claude-code" or "grok-cli", kept in the record."""

    kind: Literal["live"] = "live"
    client: str = ""


Seat = Annotated[LLMSeat | TeamSeat | ScriptedSeat | LiveSeat, Field(discriminator="kind")]


def build_agent(
    seat: Seat,
    client: LLMClient,
    seed: int,
    mailbox: Mailbox | None = None,
    on_pending=None,
) -> Agent:
    """`mailbox` (and `on_pending`) are for live seats: where their turns wait for an answer."""
    if isinstance(seat, LiveSeat):
        if mailbox is None:
            raise ValueError("a live seat can only play in a room, through the API")
        return LiveAgent(mailbox, on_pending=on_pending)
    if isinstance(seat, LLMSeat):
        return LLMAgent(client, seat.model, seat.strategy, seat.temperature, seed)
    if isinstance(seat, TeamSeat):
        proposer = LLMAgent(client, seat.proposer_model, seat.strategy, seat.temperature, seed)
        decider = (
            LLMAgent(client, seat.decider_model, seat.strategy, seat.temperature, seed)
            if seat.decider_model
            else None
        )
        return TeamAgent(proposer, Critic(client, seat.critic_model, seed=seed), decider)
    match seat.name:
        case "threshold":
            return scripted.ThresholdAgent(**seat.params)
        case "walk_away":
            return scripted.WalkAwayAgent()
        case "silent":
            return scripted.SilentAgent()
        case _:
            return scripted.MatrixStrategy(seat.name, **seat.params)


def seat_fingerprint(seat: Seat) -> dict[str, Any]:
    """What a record stores about a seat: full config plus a hash of its strategy text."""
    data = seat.model_dump()
    text = data.get("strategy", "")
    data["strategy_sha256"] = hashlib.sha256(text.encode()).hexdigest()[:16]
    return data
