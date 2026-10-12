"""HTTP API for the web app. Participants authenticate with the token they got on joining
(header X-Parley-Token). The SSE stream takes it as ?token=: EventSource can't set headers."""

import asyncio
import json
import uuid
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from parley.api import rooms as R
from parley.api.events import MatchEvents
from parley.core.baselines import reference_solutions
from parley.core.spec import GameSpec
from parley.llm.cache import Cache
from parley.llm.client import LLMClient
from parley.matches.runner import run_match
from parley.matches.seats import Seat
from parley.storage import Store
from parley.templates import TEMPLATES

Token = Annotated[str | None, Header(alias="X-Parley-Token")]


class NameBody(BaseModel):
    name: str


class VersionBody(BaseModel):
    version: int


class SeatBody(BaseModel):
    seat: Seat
    reveal: bool = True


class ReadyBody(BaseModel):
    ready: bool


class StartBody(BaseModel):
    runs: int | None = None


def create_app(store: Store | None = None, client: LLMClient | None = None) -> FastAPI:
    load_dotenv()
    store = store or Store()
    client = client or LLMClient(cache=Cache())
    live: dict[str, MatchEvents] = {}
    lock = asyncio.Lock()  # serialises room read-modify-write

    app = FastAPI(title="Parley")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(R.RoomError)
    async def _room_error(_: Request, e: R.RoomError):
        return JSONResponse({"detail": e.message}, status_code=e.status)

    def load(room_id: str) -> R.Room:
        data = store.load_room(room_id)
        if data is None:
            raise HTTPException(404, "no such room")
        return R.Room.model_validate_json(data)

    def save(room: R.Room) -> None:
        store.save_room(room.id, room.model_dump_json())

    async def mutate(room_id: str, fn) -> dict[str, Any]:
        async with lock:
            room = load(room_id)
            result = fn(room)
            save(room)
        return result if result is not None else {"ok": True}

    # --- catalogue ---
    @app.get("/api/templates")
    def templates():
        return {name: make() for name, make in TEMPLATES.items()}

    @app.post("/api/reference")
    def reference(spec: GameSpec):
        return reference_solutions(spec)

    # --- rooms ---
    @app.post("/api/rooms")
    def create(body: NameBody):
        room, token = R.create_room(body.name)
        save(room)
        return {"room_id": room.id, "token": token}

    @app.post("/api/rooms/{room_id}/join")
    async def join(room_id: str, body: NameBody):
        return await mutate(room_id, lambda r: {"token": R.join(r, body.name)})

    @app.get("/api/rooms/{room_id}")
    def get_room(room_id: str, x_parley_token: Token = None):
        room = load(room_id)
        view = R.room_view(room, x_parley_token)
        view["running"] = [m for m in room.match_ids if m in live and not live[m].done]
        return view

    @app.put("/api/rooms/{room_id}/game")
    async def put_game(room_id: str, spec: GameSpec, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.update_game(r, x_parley_token, spec))

    @app.post("/api/rooms/{room_id}/game/agree")
    async def agree(room_id: str, body: VersionBody, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.agree(r, x_parley_token, body.version))

    @app.post("/api/rooms/{room_id}/game/unlock")
    async def unlock(room_id: str, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.unlock(r, x_parley_token))

    @app.put("/api/rooms/{room_id}/seat")
    async def put_seat(room_id: str, body: SeatBody, x_parley_token: Token = None):
        return await mutate(
            room_id, lambda r: R.set_seat(r, x_parley_token, body.seat, body.reveal)
        )

    @app.post("/api/rooms/{room_id}/ready")
    async def ready(room_id: str, body: ReadyBody, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.set_ready(r, x_parley_token, body.ready))

    @app.put("/api/rooms/{room_id}/settings")
    async def put_settings(room_id: str, settings: R.RoomSettings, x_parley_token: Token = None):
        def apply(r: R.Room):
            if not r.is_host(x_parley_token):
                raise R.RoomError(403, "only the host can change settings")
            r.settings = settings

        return await mutate(room_id, apply)

    # --- matches ---
    @app.post("/api/rooms/{room_id}/matches")
    async def start(
        room_id: str, body: StartBody, tasks: BackgroundTasks, x_parley_token: Token = None
    ):
        match_id = uuid.uuid4().hex[:12]

        def prepare(r: R.Room):
            r.participant(x_parley_token)
            cfg = R.match_config(r, body.runs)
            r.match_ids.append(match_id)
            return {"match_id": match_id, "cfg": cfg}

        prepared = await mutate(room_id, prepare)
        cfg = prepared.pop("cfg")
        store.create_match(match_id, cfg, room_id)
        events = live[match_id] = MatchEvents()

        async def run():
            try:
                records = await run_match(cfg, client, match_id, events.push)
                for rec in records:
                    store.save_episode(rec)
                store.set_status(match_id, "done")
            except Exception as e:  # surface to viewers instead of dying silently
                store.set_status(match_id, "failed")
                await events.push({"type": "error", "message": f"{type(e).__name__}: {e}"})

        tasks.add_task(run)
        return prepared

    @app.get("/api/rooms/{room_id}/matches")
    def list_matches(room_id: str, x_parley_token: Token = None):
        load(room_id).participant(x_parley_token)
        return [
            {
                "id": m["id"],
                "status": m["status"],
                "created_at": m["created_at"],
                "title": m["config"].spec.title,
                "runs": m["config"].runs or m["config"].spec.runs,
            }
            for m in store.matches(room_id)
        ]

    @app.get("/api/rooms/{room_id}/matches/{match_id}")
    def get_match(room_id: str, match_id: str, x_parley_token: Token = None):
        room = load(room_id)
        me = room.participant(x_parley_token)
        if match_id not in room.match_ids:
            raise HTTPException(404, "no such match in this room")
        records = store.episodes(match_id)
        revealed = {p.name for p in room.participants if p.reveal}
        return {
            "summary": R.match_summary(records),
            "episodes": [R.visible_episode(rec, me.name, revealed) for rec in records],
            "status": next(
                (m["status"] for m in store.matches(room_id) if m["id"] == match_id), None
            ),
        }

    @app.get("/api/rooms/{room_id}/matches/{match_id}/stream")
    async def stream(room_id: str, match_id: str, token: str):
        room = load(room_id)
        room.participant(token)
        if match_id not in live:
            raise HTTPException(404, "match is not running (see its results instead)")

        async def gen():
            async for e in live[match_id].stream():
                yield {"event": e["type"], "data": json.dumps(e)}

        return EventSourceResponse(gen())

    return app
