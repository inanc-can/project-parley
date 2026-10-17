"""The conversation engine: runs one episode of a GameSpec between agents."""

import asyncio
from collections.abc import Awaitable, Callable

from parley.core.agent import Agent, PublicTurn, RoleView, StandingOffer, TurnError
from parley.core.scoring import InvalidTerms, deal_payoffs, matrix_payoffs, validate_terms
from parley.core.spec import Alternating, GameSpec, SimultaneousRounds
from parley.core.types import Deal, Outcome, Turn

MAX_RETRIES = 3

OnTurn = Callable[[Turn], Awaitable[None]] | None


class InvalidTurn(ValueError):
    pass


async def run_episode(
    spec: GameSpec, agents: dict[str, Agent], on_turn: OnTurn = None
) -> tuple[list[Turn], Outcome]:
    """Play one episode. `agents` maps every role name to the agent playing it.
    `on_turn` is awaited with each turn as it happens (for live viewing)."""
    missing = set(spec.role_names()) - set(agents)
    if missing:
        raise ValueError(f"no agent for role(s) {sorted(missing)}")
    if isinstance(spec.protocol, Alternating):
        return await _alternating(spec, spec.protocol, agents, on_turn)
    return await _simultaneous(spec, spec.protocol, agents, on_turn)


def _view(spec: GameSpec, role: str, transcript: list[Turn], **kw) -> RoleView:
    r = spec.role(role)
    return RoleView(
        title=spec.title,
        role=role,
        roles=spec.role_names(),
        shared_context=spec.shared_context,
        private_brief=r.private_brief,
        private_values=r.private_values,
        deal_fields=spec.deal_fields,
        scoring=spec.scoring,
        protocol=spec.protocol,
        transcript=[
            PublicTurn(
                role=t.role, message=t.message, action=t.action, round=t.round, phase=t.phase
            )
            for t in transcript
        ],
        **kw,
    )


Failures = list[dict[str, str]]


async def _get_turn(
    agent: Agent, view: RoleView, validate: Callable[[Turn], Turn]
) -> tuple[Turn | None, Failures]:
    """Ask the agent for a turn, re-prompting with the error up to MAX_RETRIES times.
    Returns the turn (None if every reply was rejected) and the rejected replies."""
    feedback, failures = None, []
    for attempt in range(MAX_RETRIES + 1):
        turn = None
        try:
            turn = await agent.act(view, feedback)
            turn.role = view.role
            turn = validate(turn)
            turn.retries = attempt
            return turn, failures
        except (TurnError, InvalidTurn, InvalidTerms) as e:
            raw = getattr(e, "raw_output", None) or (turn.raw_output if turn else None)
            failures.append({"error": str(e), "output": raw or ""})
            # The attempt number keeps each re-prompt distinct, so a cached bad reply
            # isn't simply served again.
            feedback = f"{e} (attempt {attempt + 2} of {MAX_RETRIES + 1})"
    return None, failures


# --- Alternating -------------------------------------------------------------


async def _alternating(
    spec: GameSpec, p: Alternating, agents: dict[str, Agent], on_turn: OnTurn
) -> tuple[list[Turn], Outcome]:
    names = spec.role_names()
    transcript: list[Turn] = []
    standing: StandingOffer | None = None
    idx = p.first

    def no_deal(reason, **kw) -> Outcome:
        return Outcome(end_reason=reason, payoffs=deal_payoffs(spec, None), **kw)

    for n in range(p.max_messages):
        role = names[idx]
        allowed = spec.actions_for(role)

        def validate(turn: Turn, role=role, allowed=allowed, standing=standing) -> Turn:
            a = turn.action
            if a is None:
                return turn
            if a.type not in allowed:
                raise InvalidTurn(f"action {a.type!r} is not allowed; allowed: {allowed}")
            if a.type in ("accept", "reject"):
                if standing is None or standing.role == role:
                    raise InvalidTurn(f"there is no offer from another player to {a.type}")
                if a.type == "accept":
                    a.terms = dict(standing.terms)
            elif a.type == "offer":
                a.terms = validate_terms(spec.deal_fields, spec.scoring, a.terms)
            return turn

        view = _view(
            spec,
            role,
            transcript,
            allowed_actions=allowed,
            must_act=False,
            standing_offer=standing,
            messages_left=p.max_messages - n,
        )
        turn, failures = await _get_turn(agents[role], view, validate)
        if turn is None:
            return transcript, no_deal("forfeit", forfeited_by=role, forfeit_attempts=failures)
        transcript.append(turn)
        if on_turn:
            await on_turn(turn)

        a = turn.action
        if a is not None:
            if a.type == "accept":
                deal = Deal(terms=a.terms)
                return transcript, Outcome(
                    end_reason="accept", deal=deal, payoffs=deal_payoffs(spec, deal.terms)
                )
            if a.type == "walk_away":
                return transcript, no_deal("walk_away")
            if a.type == "reject":
                if p.reject_ends:
                    return transcript, no_deal("reject")
                standing = None
            if a.type == "offer":
                standing = StandingOffer(role=role, terms=a.terms)
        idx = (idx + 1) % len(names)

    return transcript, no_deal("limit")


# --- Simultaneous rounds -----------------------------------------------------


async def _simultaneous(
    spec: GameSpec, p: SimultaneousRounds, agents: dict[str, Agent], on_turn: OnTurn
) -> tuple[list[Turn], Outcome]:
    names = spec.role_names()
    transcript: list[Turn] = []
    history: list[dict[str, str]] = []
    total = p.rounds if p.show_horizon else None

    def silent(turn: Turn) -> Turn:
        if turn.action is not None:
            raise InvalidTurn("this is the talk phase: send a message only, no action")
        return turn

    def move(turn: Turn) -> Turn:
        a = turn.action
        if a is None or a.type not in p.moves:
            raise InvalidTurn(f"you must choose a move now, one of {p.moves}")
        a.terms = {}
        return turn

    def forfeit(role: str, failures: Failures) -> tuple[list[Turn], Outcome]:
        return transcript, Outcome(
            end_reason="forfeit",
            forfeited_by=role,
            forfeit_attempts=failures,
            payoffs=matrix_payoffs(spec, history) if history else dict.fromkeys(names, 0.0),
        )

    for rnd in range(1, p.rounds + 1):
        common = dict(round=rnd, total_rounds=total, move_history=list(history))
        for k in range(p.talk_messages):
            role = names[k % len(names)]
            view = _view(
                spec, role, transcript, allowed_actions=[], must_act=False, phase="talk", **common
            )
            turn, failures = await _get_turn(agents[role], view, silent)
            if turn is None:
                return forfeit(role, failures)
            turn.round, turn.phase = rnd, "talk"
            transcript.append(turn)
            if on_turn:
                await on_turn(turn)

        # Everyone moves at once, from the same transcript; moves are revealed afterwards.
        views = {
            role: _view(
                spec,
                role,
                transcript,
                allowed_actions=list(p.moves),
                must_act=True,
                phase="move",
                **common,
            )
            for role in names
        }
        results = await asyncio.gather(*(_get_turn(agents[r], views[r], move) for r in names))
        for role, (turn, failures) in zip(names, results, strict=True):
            if turn is None:
                return forfeit(role, failures)
        turns = [turn for turn, _ in results]
        for turn in turns:
            turn.round, turn.phase = rnd, "move"
            transcript.append(turn)
            if on_turn:
                await on_turn(turn)
        history.append({t.role: t.action.type for t in turns})

    return transcript, Outcome(end_reason="rounds_complete", payoffs=matrix_payoffs(spec, history))
