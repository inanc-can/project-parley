"""Rooms: two people co-author one game, then each privately sets up a seat.

Pure logic (no HTTP) so it can be tested directly. Errors carry an HTTP status.
"""

import os
import secrets
import statistics
from typing import Any

from pydantic import BaseModel, Field

from parley.core.spec import Alternating, GameSpec, JudgeOnlyScoring, Role
from parley.matches.runner import EpisodeRecord, MatchConfig
from parley.matches.seats import LLMSeat, Seat, TeamSeat

# OpenRouter models across families (needs OPENROUTER_API_KEY). Until 2026-10-17 the defaults
# were on Featherless; OpenRouter has no Hermes-3-8B or Qwen2.5-14B, so Llama-3.1-8B (Hermes 3's
# base model) and Qwen2.5-7B stand in. Featherless still works through PARLEY_MODELS.
DEFAULT_MODELS = [
    "openrouter/mistralai/mistral-nemo",
    "openrouter/qwen/qwen-2.5-7b-instruct",
    "openrouter/meta-llama/llama-3.1-8b-instruct",
    "openrouter/microsoft/phi-4",
    "openrouter/qwen/qwen-2.5-72b-instruct",
]


def allowed_models_from_env() -> list[str]:
    raw = os.environ.get("PARLEY_MODELS", "")
    return [m.strip() for m in raw.split(",") if m.strip()] or DEFAULT_MODELS


class RoomError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status, self.message = status, message


class Participant(BaseModel):
    token: str
    name: str
    seat: Seat | None = None
    ready: bool = False
    reveal: bool = True  # show my setup to the others after a match
    owner: str | None = None  # token of the person controlling this seat, if it isn't its own


class RoomSettings(BaseModel):
    allowed_models: list[str] = Field(default_factory=allowed_models_from_env)
    judge_model: str | None = None
    parallel: int = 4


class Room(BaseModel):
    id: str
    host_token: str
    participants: list[Participant] = Field(default_factory=list)
    spec: GameSpec
    version: int = 1
    edited_by: str | None = None  # who saved the current version
    agreed: list[str] = Field(default_factory=list)  # tokens that agreed to `version`
    locked: bool = False
    settings: RoomSettings = Field(default_factory=RoomSettings)
    match_ids: list[str] = Field(default_factory=list)

    # --- helpers ---
    def participant(self, token: str | None) -> Participant:
        for p in self.participants:
            if p.token == token:
                return p
        raise RoomError(403, "you are not in this room")

    def acting(self, token: str | None, seat_of: str | None) -> Participant:
        """The participant `token` acts as: itself, or a seat it took with `assign_self`."""
        me = self.participant(token)
        if seat_of is None or seat_of == me.name:
            return me
        for p in self.participants:
            if p.name == seat_of and p.owner == token:
                return p
        raise RoomError(403, f"you don't control the seat {seat_of!r}")

    def owned_by(self, token: str | None) -> list[Participant]:
        return [p for p in self.participants if p.owner is not None and p.owner == token]

    def is_host(self, token: str | None) -> bool:
        return token == self.host_token

    def capacity(self) -> int:
        return len(self.spec.roles)


def blank_spec() -> GameSpec:
    return GameSpec(
        title="Untitled game",
        shared_context="",
        roles=[Role(name="side_a"), Role(name="side_b")],
        scoring=JudgeOnlyScoring(),
        protocol=Alternating(max_messages=12),
        runs=5,
    )


def create_room(host_name: str) -> tuple[Room, str]:
    token = secrets.token_urlsafe(16)
    settings = RoomSettings()
    settings.judge_model = settings.allowed_models[0] if settings.allowed_models else None
    room = Room(id=secrets.token_hex(4), host_token=token, spec=blank_spec(), settings=settings)
    room.participants.append(Participant(token=token, name=_clean_name(host_name)))
    return room, token


def _clean_name(name: str) -> str:
    name = name.strip()[:40]
    if not name:
        raise RoomError(422, "a display name is required")
    return name


def join(room: Room, name: str) -> str:
    name = _clean_name(name)
    if any(p.name.lower() == name.lower() for p in room.participants):
        raise RoomError(409, f"the name {name!r} is taken in this room")
    if len(room.participants) >= room.capacity():
        raise RoomError(409, "this room is full")
    token = secrets.token_urlsafe(16)
    room.participants.append(Participant(token=token, name=name))
    return token


def assign_self(room: Room, token: str) -> str:
    """Take an open seat yourself, so one person can run agents against each other."""
    me = room.participant(token)
    if len(room.participants) >= room.capacity():
        raise RoomError(409, "there is no open seat")
    n = 2
    while any(p.name.lower() == f"{me.name} {n}".lower() for p in room.participants):
        n += 1
    name = f"{me.name} {n}"
    room.participants.append(Participant(token=secrets.token_urlsafe(16), name=name, owner=token))
    if token in room.agreed:  # you already agreed for yourself, so for this seat too
        room.agreed.append(room.participants[-1].token)
        _lock_if_all_agreed(room)
    return name


def release_seat(room: Room, token: str, seat_of: str) -> None:
    seat = room.acting(token, seat_of)
    if seat.owner is None:
        raise RoomError(409, "you can only release a seat you took with Assign me")
    room.participants.remove(seat)
    room.agreed = [t for t in room.agreed if t != seat.token]
    room.locked = False  # the room is no longer full
    for p in room.participants:
        p.ready = False


def update_game(room: Room, token: str, spec: GameSpec) -> None:
    me = room.participant(token)
    if room.locked:
        raise RoomError(409, "the game is locked; unlock it to edit")
    if len(spec.roles) < len(room.participants):
        raise RoomError(
            422, f"{len(room.participants)} people are in the room; keep at least that many roles"
        )
    room.spec, room.version, room.agreed = spec, room.version + 1, []
    room.edited_by = me.name


def agree(room: Room, token: str, version: int) -> None:
    room.participant(token)
    if version != room.version:
        raise RoomError(409, f"the game changed (now version {room.version}); review it again")
    for t in [token] + [p.token for p in room.owned_by(token)]:  # your seats agree with you
        if t not in room.agreed:
            room.agreed.append(t)
    _lock_if_all_agreed(room)


def _lock_if_all_agreed(room: Room) -> None:
    everyone = {p.token for p in room.participants}
    if len(room.participants) == room.capacity() and everyone <= set(room.agreed):
        room.locked = True


def unlock(room: Room, token: str) -> None:
    room.participant(token)
    room.locked, room.agreed = False, []
    for p in room.participants:
        p.ready = False


def set_seat(room: Room, token: str, seat: Seat, reveal: bool, seat_of: str | None = None) -> None:
    me = room.acting(token, seat_of)
    models = []
    if isinstance(seat, LLMSeat):
        models = [seat.model]
    elif isinstance(seat, TeamSeat):
        models = [m for m in (seat.proposer_model, seat.critic_model, seat.decider_model) if m]
    for m in models:
        if m not in room.settings.allowed_models:
            raise RoomError(422, f"model {m!r} is not allowed by the host")
    me.seat, me.reveal, me.ready = seat, reveal, False


def set_ready(room: Room, token: str, ready: bool, seat_of: str | None = None) -> None:
    me = room.acting(token, seat_of)
    if ready and not room.locked:
        raise RoomError(409, "agree on the game first")
    if ready and me.seat is None:
        raise RoomError(409, "set up your seat first")
    me.ready = ready


def start_problems(room: Room) -> list[str]:
    problems = []
    if not room.locked:
        problems.append("the game is not locked")
    if len(room.participants) < room.capacity():
        problems.append(f"waiting for {room.capacity() - len(room.participants)} more person(s)")
    problems += [f"{p.name} is not ready" for p in room.participants if not p.ready]
    if isinstance(room.spec.scoring, JudgeOnlyScoring) and not room.settings.judge_model:
        problems.append("this game is scored by the judge only, but no judge model is set")
    return problems


def match_config(room: Room, runs: int | None) -> MatchConfig:
    if problems := start_problems(room):
        raise RoomError(409, "; ".join(problems))
    return MatchConfig(
        spec=room.spec,
        seats={p.name: p.seat for p in room.participants},
        runs=runs,
        judge_model=room.settings.judge_model,  # rubric scores for every game
        parallel=room.settings.parallel,
    )


# --- What each person may see -------------------------------------------------


def room_view(room: Room, token: str) -> dict[str, Any]:
    me = room.participant(token)
    return {
        "id": room.id,
        "me": {
            "name": me.name,
            "is_host": room.is_host(token),
            "seat": me.seat,
            "ready": me.ready,
            "reveal": me.reveal,
        },
        # Seats this person took with "Assign me": they see and edit these like their own.
        "controlled": [
            {"name": p.name, "seat": p.seat, "ready": p.ready, "reveal": p.reveal}
            for p in room.owned_by(token)
        ],
        "participants": [
            {
                "name": p.name,
                "ready": p.ready,
                "has_seat": p.seat is not None,
                "agreed": p.token in room.agreed,
                "is_host": room.is_host(p.token),
                "owner": next((o.name for o in room.participants if o.token == p.owner), None),
            }
            for p in room.participants
        ],
        "capacity": room.capacity(),
        "game": {
            "version": room.version,
            "spec": room.spec,
            "locked": room.locked,
            "edited_by": room.edited_by,
        },
        "settings": room.settings,
        "can_start": not start_problems(room),
        "start_problems": start_problems(room),
        "match_ids": room.match_ids,
    }


def visible_episode(record: EpisodeRecord, mine: set[str], revealed: set[str]) -> dict[str, Any]:
    """Hide the private reasoning and setup of seats that are neither the viewer's (`mine`: their
    own seat plus any they took with "Assign me") nor revealed."""
    data = record.model_dump(mode="json")
    can_see = revealed | mine
    for t in data["turns"]:
        if record.assignment[t["role"]] not in can_see:
            t["reasoning"] = t["deliberation"] = t["raw_output"] = None
    data["seats"] = {sid: (s if sid in can_see else None) for sid, s in data["seats"].items()}
    if data["outcome"].get("judge"):
        data["outcome"]["judge"].pop("raw_output", None)
    return data


def match_summary(records: list[EpisodeRecord]) -> dict[str, Any]:
    """Per-seat averages across roles, plus overall deal rate and mean metrics.
    Failed episodes count in end_reasons and failed, but not in any average."""
    if not records:
        return {}
    played = [r for r in records if r.error is None]
    seats: dict[str, list[float]] = {}
    for r in played:
        for role, payoff in r.outcome.payoffs.items():
            seats.setdefault(r.assignment[role], []).append(payoff)
    metric_keys = {k for r in played for k in r.outcome.metrics}
    metrics = {
        k: statistics.fmean(r.outcome.metrics[k] for r in played if k in r.outcome.metrics)
        for k in sorted(metric_keys)
    }
    ends: dict[str, int] = {}
    for r in records:
        ends[r.outcome.end_reason] = ends.get(r.outcome.end_reason, 0) + 1
    return {
        "episodes": len(records),
        "failed": len(records) - len(played),
        "mean_payoff_by_seat": {s: statistics.fmean(v) for s, v in seats.items()},
        "end_reasons": ends,
        "metrics": metrics,
        "reference": records[0].reference,
    }
