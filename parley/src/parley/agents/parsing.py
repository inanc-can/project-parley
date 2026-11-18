"""Rendering a RoleView as a prompt, and parsing the model's JSON turn."""

import json
from typing import Any

from parley.core.agent import RoleView, TurnError
from parley.core.spec import PASS, SimultaneousRounds
from parley.core.types import Action, Turn

ACTION_HELP = {
    "offer": 'propose terms: {"type": "offer", "terms": {...every deal field...}}',
    "accept": 'accept the other side\'s standing offer: {"type": "accept"}',
    "reject": 'reject the other side\'s standing offer: {"type": "reject"}',
    "walk_away": 'walk away: end the conversation with no deal: {"type": "walk_away"}',
    PASS: 'stay silent this turn (leave "message" empty): {"type": "pass"}',
}


def render_rules(view: RoleView) -> str:
    lines = [
        f"# Game: {view.title}",
        view.shared_context,
        "",
        f"Players: {', '.join(view.roles)}. You are **{view.role}**.",
    ]
    if view.private_brief:
        lines += ["", "## Your private brief (the other side cannot see this)", view.private_brief]
    if view.private_values:
        vals = ", ".join(f"{k} = {v:g}" for k, v in view.private_values.items())
        lines.append(f"Your private values: {vals}")
    if view.deal_fields:
        lines += ["", "## Deal terms"]
        for f in view.deal_fields:
            bounds = "".join(
                [
                    f", min {f.min:g}" if f.min is not None else "",
                    f", max {f.max:g}" if f.max is not None else "",
                ]
            )
            desc = f": {f.description}" if f.description else ""
            lines.append(f"- {f.name} ({f.type}{bounds}){desc}")
    p = view.protocol
    lines += ["", "## How a turn works"]
    if isinstance(p, SimultaneousRounds):
        horizon = f"{p.rounds} rounds" if view.total_rounds else "an unknown number of rounds"
        lines.append(
            f"The game lasts {horizon}. Each round has a talk phase (messages only) and then a "
            f"move phase where everyone picks one of {p.moves} at the same time."
        )
    elif p.turn_taking == "strict":
        lines.append(
            "Players take turns sending messages. A message may carry one formal action. "
            "Only formal actions count: a deal exists only when someone formally accepts "
            "a standing offer."
        )
    else:
        limit = f" It lasts at most {p.max_messages} turns." if p.show_limit else ""
        lines.append(
            "This is a conversation, as between people. On your turn you may say something, "
            "stay silent (pass), or say something and keep the floor to add more right after. "
            "Any message may carry one formal action, at any point in the conversation. "
            "Only formal actions count: a deal exists only when someone formally accepts "
            "a standing offer. The conversation ends when an offer is accepted, someone walks "
            f"away, or everyone stays silent in a row.{limit}"
        )
    natural = getattr(p, "turn_taking", None) == "natural"
    lines += [
        "",
        "## Reply format",
        "Reply with one JSON object and nothing else:",
        '{"reasoning": "<private thinking, never shown to anyone>",',
        ' "message": "<what you say to the other side>",',
        ' "action": null or an action object'
        + (
            ',\n "follow_up": false or true to speak again right after this message}'
            if natural
            else "}"
        ),
    ]
    return "\n".join(lines)


def render_state(view: RoleView) -> str:
    lines = ["## Conversation so far"]
    if not view.transcript:
        lines.append("(nothing yet — you speak first)")
    for t in view.transcript:
        where = f"[round {t.round} {t.phase}] " if t.round else ""
        if t.action and t.action.type == PASS:
            lines.append(f"{where}{t.role}: (stays silent)")
            continue
        act = f"  ACTION: {json.dumps(t.action.model_dump())}" if t.action else ""
        lines.append(f"{where}{t.role}: {t.message}{act}")
    if view.move_history:
        lines += ["", "## Moves in finished rounds"]
        for i, moves in enumerate(view.move_history, 1):
            lines.append(f"round {i}: " + ", ".join(f"{r}={m}" for r, m in moves.items()))

    lines += ["", "## Your turn"]
    if view.round:
        total = f" of {view.total_rounds}" if view.total_rounds else ""
        lines.append(f"Round {view.round}{total}, {view.phase} phase.")
    if view.standing_offer:
        offer = view.standing_offer
        lines.append(f"Standing offer from {offer.role}: {json.dumps(offer.terms)}")
    if view.messages_left is not None:
        lines.append(
            f"Messages left in the whole negotiation (including this one): {view.messages_left}"
        )
    if not view.allowed_actions:
        lines.append('Talk phase: "action" must be null.')
    elif view.must_act:
        opts = ", ".join(f'{{"type": "{m}"}}' for m in view.allowed_actions)
        lines.append(f'You must choose a move now. "action" must be one of: {opts}')
    else:
        lines.append("Allowed actions (or null for just talking):")
        lines += [f"- {ACTION_HELP.get(a, a)}" for a in view.allowed_actions]
    if view.can_follow_up:
        lines.append('To add another message right after this one, set "follow_up": true.')
    elif PASS in view.allowed_actions:
        lines.append("You cannot keep the floor this time: the other side speaks next.")
    return "\n".join(lines)


def extract_json(text: str) -> dict[str, Any]:
    """Return the first JSON object in `text` (tolerates code fences and surrounding prose).

    Also repairs an object closed too early, `{"reasoning": "..."}, "message": "..."}`,
    which some open models write: the keys after the stray brace are merged in."""
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                obj, end = decoder.raw_decode(text, i)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                rest = text[end:].lstrip()
                if rest.startswith(","):
                    try:
                        more, _ = decoder.raw_decode("{" + rest[1:])
                    except json.JSONDecodeError:
                        more = None
                    if isinstance(more, dict):
                        obj = {**obj, **{k: v for k, v in more.items() if k not in obj}}
                return obj
    raise TurnError("reply was not a JSON object. Reply with exactly one JSON object.")


def parse_turn(text: str, role: str, allow_empty: bool = False) -> Turn:
    """`allow_empty`: an empty reply is a valid turn (natural turn-taking reads it as a pass)."""
    data = extract_json(text)
    if "message" not in data and data.get("action") in (None, ""):
        raise TurnError('the JSON object has no "message" key. Put every key in one object.')
    message = data.get("message", "")
    if not isinstance(message, str):
        raise TurnError('"message" must be a string')
    reasoning = data.get("reasoning")
    action = data.get("action")
    if action in (None, "", "null", "none"):
        parsed = None
    elif isinstance(action, str):
        parsed = Action(type=action)
    elif isinstance(action, dict) and isinstance(action.get("type"), str):
        terms = action.get("terms") or {}
        if not isinstance(terms, dict):
            raise TurnError('"terms" must be an object')
        parsed = Action(type=action["type"], terms=terms)
    else:
        raise TurnError('"action" must be null or an object with a "type"')
    if not message.strip() and parsed is None and not allow_empty:
        raise TurnError('the reply was empty. Write a "message", or take an "action".')
    return Turn(
        role=role,
        message=message,
        action=parsed,
        reasoning=reasoning if isinstance(reasoning, str) else None,
        follow_up=data.get("follow_up") is True,
        raw_output=text,
    )
