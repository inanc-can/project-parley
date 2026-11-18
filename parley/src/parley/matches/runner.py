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
    # Tries per episode before it is recorded as failed. With the LLM cache on, a retry
    # replays the calls that succeeded and only repeats the one that failed.
    episode_attempts: int = Field(3, ge=1)


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
    attempts: int = 1
    error: str | None = None  # set when every attempt failed (outcome.end_reason == "error")


Event = dict[str, Any]
OnEvent = Callable[[Event], Awaitable[None]] | None
OnRecord = Callable[["EpisodeRecord"], None] | None


def is_setup_error(e: Exception) -> bool:
    """Bad key, gated or unknown model: these fail every episode the same way, so they stop
    the match instead of being retried."""
    import litellm  # slow import; only reached once a call has failed

    return isinstance(
        e, litellm.AuthenticationError | litellm.NotFoundError | litellm.PermissionDeniedError
    )


def assignment_for(spec: GameSpec, seat_ids: list[str], index: int, swap: bool) -> dict[str, str]:
    roles = spec.role_names()
    if len(seat_ids) != len(roles):
        raise ValueError(f"{len(roles)} roles need {len(roles)} seats, got {len(seat_ids)}")
    shift = index % len(roles) if swap else 0
    order = seat_ids[shift:] + seat_ids[:shift]
    return dict(zip(roles, order, strict=True))


async def run_match(
    cfg: MatchConfig,
    client: LLMClient,
    match_id: str | None = None,
    on_event: OnEvent = None,
    on_record: OnRecord = None,
) -> list[EpisodeRecord]:
    """Play every episode. A failing episode is retried, then recorded as failed; the others
    carry on. on_record gets each record as soon as its episode finishes."""
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

            async def on_turn(turn: Turn):
                public = turn.model_dump(include={"role", "message", "action", "round", "phase"})
                await emit({"type": "turn", "index": index, "turn": public})

            error = None
            for attempt in range(1, cfg.episode_attempts + 1):
                agents = {
                    role: build_agent(cfg.seats[sid], client, seed)
                    for role, sid in assignment.items()
                }
                start = {"type": "episode_start", "index": index, "assignment": assignment}
                await emit({**start, "attempt": attempt})
                try:
                    turns, outcome = await run_episode(spec, agents, on_turn)
                    error = None
                    break
                except Exception as e:  # provider errors that outlived the client's retries
                    if is_setup_error(e):
                        raise
                    error = f"{type(e).__name__}: {e}"
                    retry = {"type": "episode_retry", "index": index, "attempt": attempt}
                    await emit({**retry, "error": error})
            if error:
                turns, outcome = [], Outcome(end_reason="error")
            else:
                if judge:
                    try:
                        judgment = await judge.assess(spec, turns, outcome)
                    except Exception as e:  # keep the episode; its judgment is just missing
                        judgment = {"error": f"judge failed: {type(e).__name__}: {e}"}
                    outcome = apply_judgment(spec, outcome, judgment)
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
                attempts=attempt,
                error=error,
            )
            if on_record:
                on_record(record)
            end = {"type": "episode_end", "index": index, "outcome": outcome.model_dump()}
            await emit({**end, "error": error})
            return record

    await emit({"type": "match_start", "match_id": match_id, "runs": runs})
    records = await asyncio.gather(*(one(i) for i in range(runs)))
    await emit({"type": "match_end", "match_id": match_id})
    return list(records)
