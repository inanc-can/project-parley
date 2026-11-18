"""HTTP API for the web app. Participants authenticate with the token they got on joining
(header X-Parley-Token). The SSE stream takes it as ?token=: EventSource can't set headers."""

import asyncio
import base64
import json
import uuid
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from pydantic_core import to_jsonable_python
from sse_starlette.sse import EventSourceResponse

from parley import files as F
from parley import research as RS
from parley.agents.live import LiveTurns
from parley.agents.parsing import render_rules, render_state
from parley.api import assistant as A
from parley.api import rooms as R
from parley.api.events import MatchEvents
from parley.core.baselines import reference_solutions
from parley.core.spec import GameSpec, SharedFile
from parley.core.types import Action, Turn
from parley.llm.cache import Cache
from parley.llm.client import LLMClient
from parley.matches.runner import run_match
from parley.matches.seats import LiveSeat, Seat
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
    seat_of: str | None = None  # a seat you took with "Assign me"; default is your own


class ReadyBody(BaseModel):
    ready: bool
    seat_of: str | None = None


class SeatOfBody(BaseModel):
    seat_of: str


class StartBody(BaseModel):
    runs: int | None = None


class TalkBody(BaseModel):
    goal: str
    name: str
    client: str = ""  # e.g. "claude-code", "grok-cli"


class JoinTalkBody(BaseModel):
    name: str
    client: str = ""


class TurnBody(BaseModel):
    """A live agent's turn: what it says, and at most one formal action."""

    message: str = ""
    action: Action | str | None = None  # an object, or just its type ("accept", "pass", ...)
    follow_up: bool = False
    reasoning: str | None = None  # private: kept in the record, never shown to the other side
    seat_of: str | None = None


class ChatBody(BaseModel):
    messages: list[A.ChatMessage]


class FileBody(BaseModel):
    name: str
    mime: str = ""
    data: str  # base64


class SummaryBody(BaseModel):
    files: list[SharedFile]
    context: str = ""


class ResearchBody(BaseModel):
    topic: str
    context: str = ""


def create_app(store: Store | None = None, client: LLMClient | None = None) -> FastAPI:
    load_dotenv()
    store = store or Store()
    client = client or LLMClient(cache=Cache())
    store.mark_interrupted()  # matches this process didn't start can't still be running
    live: dict[str, MatchEvents] = {}
    turns = LiveTurns()  # mailboxes of live seats (outside agents answering through /turn)
    background: set[asyncio.Task] = set()  # running talks (keeps their tasks referenced)
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

    # --- shared files: converted here; they join the game when the draft is saved ---
    @app.post("/api/rooms/{room_id}/files")
    async def add_file(room_id: str, body: FileBody, x_parley_token: Token = None):
        load(room_id).participant(x_parley_token)
        try:
            data = base64.b64decode(body.data, validate=True)
        except ValueError:
            raise HTTPException(400, "the file data isn't valid base64") from None
        try:
            return await F.to_shared_file(body.name, body.mime, data, client)
        except F.FileError as e:
            raise HTTPException(400, str(e)) from None
        except Exception as e:  # the vision model failed
            raise HTTPException(502, f"couldn't describe {body.name}: {e}") from None

    @app.post("/api/rooms/{room_id}/files/summary")
    async def summarise_files(room_id: str, body: SummaryBody, x_parley_token: Token = None):
        load(room_id).participant(x_parley_token)
        try:
            return {"text": await F.summarise(body.files, body.context, client)}
        except F.FileError as e:
            raise HTTPException(400, str(e)) from None
        except Exception as e:
            raise HTTPException(502, f"the summary failed: {e}") from None

    @app.post("/api/rooms/{room_id}/research")
    async def research(room_id: str, body: ResearchBody, x_parley_token: Token = None):
        load(room_id).participant(x_parley_token)
        try:
            return {"text": await RS.research(body.topic, body.context, client)}
        except RS.ResearchError as e:
            raise HTTPException(400, str(e)) from None
        except Exception as e:
            raise HTTPException(502, f"the research failed: {e}") from None

    @app.post("/api/rooms/{room_id}/game/agree")
    async def agree(room_id: str, body: VersionBody, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.agree(r, x_parley_token, body.version))

    @app.post("/api/rooms/{room_id}/game/unlock")
    async def unlock(room_id: str, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.unlock(r, x_parley_token))

    @app.put("/api/rooms/{room_id}/seat")
    async def put_seat(room_id: str, body: SeatBody, x_parley_token: Token = None):
        return await mutate(
            room_id, lambda r: R.set_seat(r, x_parley_token, body.seat, body.reveal, body.seat_of)
        )

    @app.post("/api/rooms/{room_id}/ready")
    async def ready(room_id: str, body: ReadyBody, x_parley_token: Token = None):
        return await mutate(
            room_id, lambda r: R.set_ready(r, x_parley_token, body.ready, body.seat_of)
        )

    @app.post("/api/rooms/{room_id}/seats/assign")
    async def assign_self(room_id: str, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: {"name": R.assign_self(r, x_parley_token)})

    @app.post("/api/rooms/{room_id}/seats/release")
    async def release_seat(room_id: str, body: SeatOfBody, x_parley_token: Token = None):
        return await mutate(room_id, lambda r: R.release_seat(r, x_parley_token, body.seat_of))

    @app.put("/api/rooms/{room_id}/settings")
    async def put_settings(room_id: str, settings: R.RoomSettings, x_parley_token: Token = None):
        def apply(r: R.Room):
            if not r.is_host(x_parley_token):
                raise R.RoomError(403, "only the host can change settings")
            r.settings = settings

        return await mutate(room_id, apply)

    # --- matches ---
    def running(match_id: str) -> bool:
        return match_id in live and not live[match_id].done

    async def launch(
        room_id: str, token: str | None, runs: int | None, tasks: BackgroundTasks | None
    ):
        """Start a match in the background; the endpoint and the assistant both use this.
        Without `tasks` it runs as its own asyncio task, not tied to the request: a talk between
        live agents waits on their later requests."""
        match_id = uuid.uuid4().hex[:12]

        def prepare(r: R.Room):
            r.participant(token)
            cfg = R.match_config(r, runs)
            if R.has_live_seat(r) and any(running(m) for m in r.match_ids):
                raise R.RoomError(409, "this talk is already running")
            r.match_ids.append(match_id)
            # Open the live seats' mailboxes now, so whoever sees the new match id finds them.
            for sid, seat in cfg.seats.items():
                if isinstance(seat, LiveSeat):
                    turns.box(match_id, sid)
            return {"match_id": match_id, "cfg": cfg}

        prepared = await mutate(room_id, prepare)
        cfg = prepared.pop("cfg")
        store.create_match(match_id, cfg, room_id)
        events = live[match_id] = MatchEvents()

        async def run():
            try:
                await run_match(cfg, client, match_id, events.push, store.save_episode, turns)
                store.set_status(match_id, "done")
            except Exception as e:  # surface to viewers instead of dying silently
                message = f"{type(e).__name__}: {e}"
                store.set_status(match_id, "failed")
                await turns.end(match_id, {"end_reason": "error", "error": message})
                await events.push({"type": "error", "message": message})
            finally:
                turns.drop(match_id)

        if tasks is None:
            task = asyncio.create_task(run())
            background.add(task)
            task.add_done_callback(background.discard)
        else:
            tasks.add_task(run)
        return prepared

    async def start_if_ready(room_id: str, token: str) -> str | None:
        """Start the talk once everyone is in and ready (the second agent to join starts it)."""
        try:
            return (await launch(room_id, token, None, None))["match_id"]
        except R.RoomError:  # not ready yet, or already running
            return None

    # --- talks: outside agents (Claude Code, Grok CLI, ...) take live seats ---
    @app.post("/api/talks")
    def open_talk(body: TalkBody):
        room, token = R.open_talk(body.goal, body.name, body.client)
        save(room)
        return {"room_id": room.id, "token": token}

    @app.post("/api/rooms/{room_id}/talk/join")
    async def join_talk(room_id: str, body: JoinTalkBody):
        joined = await mutate(room_id, lambda r: {"token": R.join_talk(r, body.name, body.client)})
        token = joined["token"]
        return {"token": token, "match_id": await start_if_ready(room_id, token)}

    def live_box(room: R.Room, seat: str):
        """The mailbox of `seat` in the room's latest match, while that match runs."""
        return turns.get(room.match_ids[-1], seat) if room.match_ids else None

    def last_outcome(match_id: str) -> dict[str, Any]:
        """How a finished match ended, from the store (its mailboxes are gone by then)."""
        episodes = store.episodes(match_id)
        return episodes[-1].outcome.model_dump() if episodes else {"end_reason": "error"}

    @app.get("/api/rooms/{room_id}/turn")
    async def wait_turn(
        room_id: str, wait: float = 50, seat_of: str | None = None, x_parley_token: Token = None
    ):
        """Long poll for a live seat: returns as soon as it is this seat's turn or the talk is
        over, else after `wait` seconds with status "waiting" (call again). A talk that is ready
        but not running yet (say, agreed again after an edit) is started here."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + max(0.0, min(wait, 120))
        while True:
            room = load(room_id)
            seat = room.acting(x_parley_token, seat_of)
            box = live_box(room, seat.name)
            if box:
                await box.wait(max(0.0, deadline - loop.time()))
                if p := box.open_turn:
                    v, feedback = p.view, p.feedback
                    prompt = render_rules(v, json_reply=False) + "\n\n"
                    prompt += render_state(v, json_reply=False)
                    if feedback:
                        prompt += f"\n\nYour previous turn was refused: {feedback}\nTry again."
                    return {
                        "status": "your_turn",
                        "role": v.role,
                        "prompt": prompt,
                        "feedback": feedback,
                        "allowed_actions": v.allowed_actions,
                        "can_follow_up": v.can_follow_up,
                        "standing_offer": v.standing_offer,
                        "transcript": v.transcript,
                    }
                if box.outcome:
                    return {"status": "ended", "outcome": box.outcome}
                return {"status": "waiting", "detail": "the other side is speaking; call again"}
            if room.match_ids and not running(room.match_ids[-1]):
                return {"status": "ended", "outcome": last_outcome(room.match_ids[-1])}
            if not room.match_ids and await start_if_ready(room_id, x_parley_token):
                continue
            if loop.time() >= deadline:
                problems = R.start_problems(room)
                return {"status": "not_started", "detail": "; ".join(problems) or "starting"}
            await asyncio.sleep(1)

    @app.post("/api/rooms/{room_id}/turn")
    async def send_turn(room_id: str, body: TurnBody, x_parley_token: Token = None):
        # async: answering resolves an asyncio future, which only the event loop's thread may do
        room = load(room_id)
        seat = room.acting(x_parley_token, body.seat_of)
        box = live_box(room, seat.name)
        pending = box.open_turn if box else None
        if pending is None:
            raise HTTPException(409, "it isn't your turn; wait for it first")
        action = Action(type=body.action) if isinstance(body.action, str) else body.action
        turn = Turn(
            role=pending.view.role,
            message=body.message,
            action=action,
            follow_up=body.follow_up,
            reasoning=body.reasoning,
            raw_output=body.model_dump_json(exclude={"seat_of"}),
        )
        if not box.answer(turn):
            raise HTTPException(409, "it isn't your turn; wait for it first")
        return {"ok": True}

    @app.post("/api/rooms/{room_id}/matches")
    async def start(
        room_id: str, body: StartBody, tasks: BackgroundTasks, x_parley_token: Token = None
    ):
        return await launch(room_id, x_parley_token, body.runs, tasks)

    # --- assistant ---
    def assistant_ops(room_id: str, token: str | None, tasks: BackgroundTasks) -> A.RoomOps:
        load(room_id).participant(token)  # only people in the room
        return A.RoomOps(
            room_id=room_id,
            token=token,
            load=lambda: load(room_id),
            mutate=lambda fn: mutate(room_id, fn),
            start_match=lambda runs: launch(room_id, token, runs, tasks),
            match_summary=lambda match_id: R.match_summary(store.episodes(match_id)),
        )

    @app.post("/api/rooms/{room_id}/assistant")
    async def assistant(
        room_id: str, body: ChatBody, tasks: BackgroundTasks, x_parley_token: Token = None
    ):
        ops = assistant_ops(room_id, x_parley_token, tasks)
        try:
            steps = await A.chat(ops, body.messages, client)
        except Exception as e:  # provider down or over its limits: say so instead of a bare 500
            raise HTTPException(502, f"The assistant model didn't answer: {str(e)[:300]}") from e
        return {"steps": steps, "model": A.assistant_model()}

    @app.post("/api/rooms/{room_id}/assistant/stream")
    async def assistant_stream(
        room_id: str, body: ChatBody, tasks: BackgroundTasks, x_parley_token: Token = None
    ):
        """The same answer as /assistant, as newline-delimited JSON events while it happens."""
        ops = assistant_ops(room_id, x_parley_token, tasks)

        async def gen():
            try:
                async for e in A.chat_events(ops, body.messages, client):
                    yield json.dumps(e, default=to_jsonable_python) + "\n"
            except Exception as e:  # provider down or over its limits: tell the chat
                msg = f"The assistant model didn't answer: {str(e)[:300]}"
                yield json.dumps({"type": "error", "message": msg}) + "\n"

        # no-transform: Next's proxy would otherwise gzip and hold back the stream.
        headers = {"Cache-Control": "no-cache, no-transform"}
        return StreamingResponse(gen(), media_type="application/x-ndjson", headers=headers)

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
        mine = {me.name} | {p.name for p in room.owned_by(x_parley_token)}
        return {
            "summary": R.match_summary(records),
            "episodes": [R.visible_episode(rec, mine, revealed) for rec in records],
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

        # no-transform stops proxies (including Next's rewrite) from gzipping the stream,
        # which holds events back until the match ends.
        return EventSourceResponse(gen(), headers={"Cache-Control": "no-cache, no-transform"})

    return app
