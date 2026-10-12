"""Run a match: N episodes of a locked game between seats, with roles swapped."""

import asyncio
import uuid
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from importlib.metadata import version
from typing import Any

from pydantic import BaseModel, Field

from parley.core.baselines import reference_solutions
from parley.core.engine import run_episode
from parley.core.spec import GameSpec
from parley.core.types import Outcome, Turn
from parley.judge import Judge, apply_judgment
from parley.llm.client import LLMClient
from parley.matches.seats import Seat, build_agent, seat_fingerprint
from parley.metrics import episode_metrics


class MatchConfig(BaseModel):
    spec: GameSpec
    seats: dict[str, Seat]  # seat id (e.g. a person) -> setup; one seat per role
    runs: int | None = None  # default: spec.runs
    swap_roles: bool = True  # rotate which seat plays which role between runs
    seed: int = 0
    judge_model: str | None = None
    parallel: int = 4  # episodes played at once


class EpisodeRecord(BaseModel):
    match_id: str
    index: int
    seed: int
    parley_version: str
    created_at: datetime
    spec: GameSpec
    assignment: dict[str, str]  # role -> seat id
    seats: dict[str, dict[str, Any]]  # seat id -> fingerprint
    turns: list[Turn]
    outcome: Outcome
    reference: dict[str, Any] = Field(default_factory=dict)


Event = dict[str, Any]
OnEvent = Callable[[Event], Awaitable[None]] | None


def assignment_for(spec: GameSpec, seat_ids: list[str], index: int, swap: bool) -> dict[str, str]:
    roles = spec.role_names()
    if len(seat_ids) != len(roles):
        raise ValueError(f"{len(roles)} roles need {len(roles)} seats, got {len(seat_ids)}")
    shift = index % len(roles) if swap else 0
    order = seat_ids[shift:] + seat_ids[:shift]
    return dict(zip(roles, order, strict=True))


async def run_match(
    cfg: MatchConfig, client: LLMClient, match_id: str | None = None, on_event: OnEvent = None
) -> list[EpisodeRecord]:
    match_id = match_id or uuid.uuid4().hex[:12]
    spec = cfg.spec
    runs = cfg.runs or spec.runs
    refs = reference_solutions(spec)
    seat_ids = list(cfg.seats)
    judge = Judge(client, cfg.judge_model) if cfg.judge_model else None
    sem = asyncio.Semaphore(cfg.parallel)

    async def emit(event: Event):
        if on_event:
            await on_event(event)

    async def one(index: int) -> EpisodeRecord:
        async with sem:
            seed = cfg.seed * 100_000 + index
            assignment = assignment_for(spec, seat_ids, index, cfg.swap_roles)
            agents = {
                role: build_agent(cfg.seats[sid], client, seed) for role, sid in assignment.items()
            }
            await emit({"type": "episode_start", "index": index, "assignment": assignment})

            async def on_turn(turn: Turn):
                public = turn.model_dump(include={"role", "message", "action", "round", "phase"})
                await emit({"type": "turn", "index": index, "turn": public})

            turns, outcome = await run_episode(spec, agents, on_turn)
            if judge:
                outcome = apply_judgment(spec, outcome, await judge.assess(spec, turns, outcome))
            outcome.metrics = episode_metrics(spec, turns, outcome, refs)
            record = EpisodeRecord(
                match_id=match_id,
                index=index,
                seed=seed,
                parley_version=version("parley"),
                created_at=datetime.now(UTC),
                spec=spec,
                assignment=assignment,
                seats={sid: seat_fingerprint(s) for sid, s in cfg.seats.items()},
                turns=turns,
                outcome=outcome,
                reference=refs,
            )
            await emit({"type": "episode_end", "index": index, "outcome": outcome.model_dump()})
            return record

    records = await asyncio.gather(*(one(i) for i in range(runs)))
    await emit({"type": "match_end", "match_id": match_id})
    return list(records)
