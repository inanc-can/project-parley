"""Room assistant: a chat agent that manages a room for the person talking to it.

It acts with that person's token, so it can do exactly what they could do in the UI: edit and
agree to the game, take or release seats, set up their agents, mark them ready, start matches
and read results. It never sees other people's private seats.

Any model works: instead of provider tool calling (unreliable on open models) the assistant
replies with one JSON object, {"message": ..., "actions": [{"tool": ..., "args": {...}}]}. The
actions run, their results go back to it, and it replies again until it sends no actions.
"""

import json
import logging
import os
import re
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from parley.agents.parsing import extract_json
from parley.api import rooms as R
from parley.core.spec import GameSpec, SurplusScoring
from parley.llm.client import LLMClient
from parley.matches.seats import LLMSeat, ScriptedSeat
from parley.templates import TEMPLATES

log = logging.getLogger("parley.assistant")

DEFAULT_MODEL = "openrouter/qwen/qwen-2.5-72b-instruct"
# Answers instead when the main model is rate limited (on Featherless a 72B model takes the whole
# concurrency plan while a match runs). Override with PARLEY_ASSISTANT_FALLBACK_MODEL.
FALLBACK_MODEL = "openrouter/microsoft/phi-4"
MAX_STEPS = 6


def assistant_model() -> str:
    return os.environ.get("PARLEY_ASSISTANT_MODEL", "").strip() or DEFAULT_MODEL


def fallback_model() -> str:
    return os.environ.get("PARLEY_ASSISTANT_FALLBACK_MODEL", "").strip() or FALLBACK_MODEL


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


@dataclass
class RoomOps:
    """What the assistant can touch, bound to one room and one person's token."""

    room_id: str
    token: str | None
    load: Callable[[], R.Room]
    mutate: Callable[[Callable[[R.Room], Any]], Awaitable[Any]]
    start_match: Callable[[int | None], Awaitable[dict[str, Any]]]
    match_summary: Callable[[str], dict[str, Any]]


TOOLS = """\
- room_state {} — the game, players, your seats and what blocks starting (also given below).
- use_template {"name": one of %(templates)s} — replace the game with a template.
- edit_game {"changes": {...}} — merge top-level fields into the game spec (title,
  shared_context, roles, runs, protocol, ...). Send whole values: "roles" replaces all roles.
- agree_game {} — agree to the current game version (also for seats you took yourself); this
  locks the game once everyone agreed. There is no separate lock tool. Finish all game edits
  (template, runs, ...) before agreeing.
- unlock_game {} — unlock the game to edit it again (clears everyone's ready).
- assign_me {} — take the open seat yourself to run your own agents against each other.
- release_seat {"seat": name} — give back a seat you took with assign_me.
- set_agent {"seat": name or null for your own, "model": one of the allowed models,
  "strategy": instructions, "temperature": 0-2} — set up an LLM agent.
  Or {"seat": ..., "scripted": one of %(scripted)s} for a fixed baseline strategy.
- set_ready {"seat": name or null, "ready": true/false} — needs a locked game and a saved agent.
- start_match {"runs": number or null} — start a match (everyone must be ready).
- match_results {"match_id": id or null for the latest} — summary of a finished match.
"""

SCRIPTED = ["tit_for_tat", "always_cooperate", "always_defect", "grim_trigger", "walk_away"]

SYSTEM = """\
You are the Parley assistant. Parley is a research platform where LLM agents negotiate and play
games. You manage one room for the person you are talking to, acting as them.

A room has one shared game (the spec both players agree to) and one seat per role. Each seat
holds an agent: a model plus private strategy instructions. Flow: write or pick the game ->
everyone agrees (the game locks) -> each agent is set up and marked ready -> start a match,
which plays the game several times with roles swapped -> read the results.

Tools:
%(tools)s
Seats are not roles. A seat belongs to a player and is named after them: your own seat is
"seat": null, and a seat you took with assign_me has its own name (e.g. "Ada 2"). Roles (e.g.
seller, buyer) come from the game and every agent plays each role in turn, so never pass a role
name as a seat. "My agent" means your own seat; "my second agent" / "the other side" means the
seat you took.

Templates are complete, tested games: keep their roles, briefs and values. With edit_game change
only what the person asked for (e.g. just "runs"); never rewrite roles unless asked to.

Reply with exactly one JSON object and nothing else:
{"message": "what you say to the person", "actions": [{"tool": "...", "args": {...}}]}
Only actions change the room: never say you changed, set up or started something unless the
action for it is in "actions" (or a tool result already shows it). Actions run in order and you
then see their results and reply again. When you are done, or
need the person to decide something, reply with "actions": []. Keep messages short and say what
you changed. Do not invent players, models or results: use the room state and tool results.
"""


def _state(room: R.Room, token: str | None) -> dict[str, Any]:
    view = R.room_view(room, token)
    return {
        "you": view["me"]["name"],
        "your_seat": view["me"]["seat"],
        "your_ready": view["me"]["ready"],
        "seats_you_took": view["controlled"],
        "players": view["participants"],
        "open_seats": view["capacity"] - len(view["participants"]),
        "game": {"version": view["game"]["version"], "locked": view["game"]["locked"]},
        "spec": room.spec.model_dump(mode="json"),
        "allowed_models": room.settings.allowed_models,
        "can_start": view["can_start"],
        "start_problems": view["start_problems"],
        "match_ids": room.match_ids,
    }


async def _run_tool(ops: RoomOps, tool: str, args: dict[str, Any]) -> Any:
    t = ops.token
    seat_of = args.get("seat") or None
    match tool:
        case "room_state":
            return _state(ops.load(), t)
        case "use_template":
            if args.get("name") not in TEMPLATES:
                raise ValueError(f"unknown template; pick one of {sorted(TEMPLATES)}")
            spec = TEMPLATES[args["name"]]()
            await ops.mutate(lambda r: R.update_game(r, t, spec))
            return f"game is now the {args['name']} template ({spec.title})"
        case "edit_game":
            changes = args.get("changes") or {}

            def edit(r: R.Room):
                spec = GameSpec.model_validate({**r.spec.model_dump(mode="json"), **changes})
                # Surplus scoring reads each role's reservation and silently uses 0 without it,
                # which a rewrite of the roles easily drops.
                if isinstance(spec.scoring, SurplusScoring):
                    missing = [x.name for x in spec.roles if "reservation" not in x.private_values]
                    if missing:
                        raise ValueError(
                            f"roles {missing} have no private_values.reservation, which this "
                            "game's scoring needs; keep the roles' values or leave roles out"
                        )
                R.update_game(r, t, spec)
                return f"game updated to version {r.version}"

            return await ops.mutate(edit)
        case "agree_game":
            await ops.mutate(lambda r: R.agree(r, t, r.version))
            return "locked" if ops.load().locked else "agreed; waiting for the others"
        case "unlock_game":
            await ops.mutate(lambda r: R.unlock(r, t))
            return "unlocked"
        case "assign_me":
            return {"seat": await ops.mutate(lambda r: R.assign_self(r, t))}
        case "release_seat":
            await ops.mutate(lambda r: R.release_seat(r, t, args["seat"]))
            return "released"
        case "set_agent":
            if args.get("scripted"):
                seat = ScriptedSeat(name=args["scripted"])
            else:
                seat = LLMSeat(
                    model=args["model"],
                    strategy=args.get("strategy", ""),
                    temperature=float(args.get("temperature", 0.7)),
                )
            reveal = ops.load().acting(t, seat_of).reveal  # keep the person's reveal choice
            await ops.mutate(lambda r: R.set_seat(r, t, seat, reveal, seat_of))
            return "agent saved (not ready yet)"
        case "set_ready":
            ready = bool(args.get("ready", True))
            await ops.mutate(lambda r: R.set_ready(r, t, ready, seat_of))
            return "ready" if ready else "not ready"
        case "start_match":
            started = await ops.start_match(args.get("runs"))
            return {"match_id": started["match_id"], "note": "running; results when it finishes"}
        case "match_results":
            room = ops.load()
            match_id = args.get("match_id") or (room.match_ids[-1] if room.match_ids else None)
            if not match_id or match_id not in room.match_ids:
                raise ValueError("no such match in this room")
            return ops.match_summary(match_id) or "no finished episodes yet"
    raise ValueError(f"unknown tool {tool!r}")


FORMAT_REMINDER = (
    "(Your last reply was not the required JSON object, so nothing ran. Reply again with exactly "
    'one JSON object {"message": ..., "actions": [...]} and put every change you mean to make '
    'into "actions".)'
)


def parse_reply(text: str) -> dict[str, Any] | None:
    """The reply's JSON object, or None if it has none we can use. When the object carries no
    message (some models write prose, then a bare {"actions": []}), the prose before it is used."""
    try:
        obj = extract_json(text)
    except Exception:
        return None
    if "message" not in obj and "actions" not in obj:
        return None
    if not obj.get("message"):
        prose = re.sub(r"```(?:json)?", "", text[: text.find("{")]).strip()
        obj = {**obj, "message": prose}
    return obj


def _rate_limited(e: Exception) -> bool:
    import litellm  # slow import; only reached after a live call failed

    return isinstance(e, litellm.RateLimitError)


async def _complete(client: LLMClient, model: str, prompt: list[dict[str, str]]) -> str:
    """Ask the assistant model (never cached: a regenerated answer must be new); when it is over
    the provider's concurrency limit, ask the smaller fallback model instead."""
    kwargs: dict[str, Any] = {
        "temperature": 0.2,
        "max_tokens": 1500,
        "cache": False,
        "json_mode": True,  # providers that support it then can't return malformed JSON
    }
    try:
        return (await client.complete(model, prompt, retry_delays=(2,), **kwargs)).text
    except Exception as e:
        if not _rate_limited(e) or model == fallback_model():
            raise
    return (await client.complete(fallback_model(), prompt, **kwargs)).text


async def chat_events(
    ops: RoomOps, history: list[ChatMessage], client: LLMClient, model: str | None = None
) -> AsyncIterator[dict[str, Any]]:
    """Answer the latest user message, yielding events as they happen so the UI can show the
    trace live: {"type": "thinking"} before each model call, {"type": "message", "text"},
    {"type": "action", "id", "tool", "args"} when an action starts and
    {"type": "result", "id", "ok", "result"} when it ends."""
    model = model or assistant_model()
    system = SYSTEM % {
        "tools": TOOLS % {"templates": sorted(TEMPLATES), "scripted": SCRIPTED},
    }
    messages: list[dict[str, str]] = [m.model_dump() for m in history[-20:]]
    n = 0  # action ids, unique within this answer

    reminded = False
    for _ in range(MAX_STEPS):
        # Fresh room state every step, so the assistant sees what its last actions changed.
        state = json.dumps(_state(ops.load(), ops.token), default=to_jsonable_python)
        prompt = [{"role": "system", "content": f"{system}\nRoom state now: {state}"}, *messages]
        yield {"type": "thinking"}
        text = await _complete(client, model, prompt)
        reply = parse_reply(text)
        if reply is None:  # keep a trace of what the model sent, to diagnose format failures
            log.warning("assistant reply was not usable JSON: %r", text[:2000])
        if reply is None and not reminded:  # prose only: it may claim changes it never made
            reminded = True
            messages += [
                {"role": "assistant", "content": text},
                {"role": "user", "content": FORMAT_REMINDER},
            ]
            continue
        reply = reply or {"message": text.strip(), "actions": []}  # still prose: just say it
        if message := str(reply.get("message") or ""):
            yield {"type": "message", "text": message}
        actions = reply.get("actions") or []
        done: list[dict[str, Any]] = []
        for a in actions if isinstance(actions, list) else []:
            tool, args = str(a.get("tool", "")), a.get("args") or {}
            n += 1
            yield {"type": "action", "id": n, "tool": tool, "args": args}
            try:
                ok, result = True, await _run_tool(ops, tool, args)
            except Exception as e:  # report back so the assistant can correct itself
                ok, result = False, (e.message if isinstance(e, R.RoomError) else str(e))[:500]
            done.append({"tool": tool, "args": args, "ok": ok, "result": result})
            yield {"type": "result", "id": n, "ok": ok, "result": result}
        messages.append({"role": "assistant", "content": text})
        if not done:
            break
        messages.append(
            {
                "role": "user",
                "content": "(Tool results: " + json.dumps(done, default=to_jsonable_python) + ")",
            }
        )


async def chat(
    ops: RoomOps, history: list[ChatMessage], client: LLMClient, model: str | None = None
) -> list[dict[str, Any]]:
    """`chat_events` collected into steps, one per model reply: {"message": str, "actions":
    [{"tool", "args", "ok", "result"}]}."""
    steps: list[dict[str, Any]] = []
    for_id: dict[int, dict[str, Any]] = {}
    async for e in chat_events(ops, history, client, model):
        if e["type"] == "thinking":
            steps.append({"message": "", "actions": []})
        elif e["type"] == "message":
            steps[-1]["message"] = e["text"]
        elif e["type"] == "action":
            for_id[e["id"]] = {"tool": e["tool"], "args": e["args"]}
            steps[-1]["actions"].append(for_id[e["id"]])
        elif e["type"] == "result":
            for_id[e["id"]].update(ok=e["ok"], result=e["result"])
    return [s for s in steps if s["message"] or s["actions"]]  # drop replies we re-prompted
