"""A seat played by an agent outside Parley (Claude Code, Grok CLI, ...) through the API.

The engine calls LiveAgent.act as for any agent; the view waits in the seat's Mailbox until the
outside agent fetches it (GET /turn) and answers (POST /turn). Everything lives in memory in the
API process, like the match event log."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from parley.core.agent import RoleView
from parley.core.types import Action, Turn

TURN_TIMEOUT = 15 * 60  # seconds an outside agent has to answer before it walks away


@dataclass
class Pending:
    view: RoleView
    feedback: str | None  # why the previous reply was rejected
    reply: asyncio.Future = field(repr=False)


class Mailbox:
    """One live seat in one match: the turn waiting for an answer, and the outcome at the end."""

    def __init__(self):
        self.pending: Pending | None = None
        self.outcome: dict[str, Any] | None = None  # set when the episode ends
        self._cond = asyncio.Condition()

    async def _set(self, **kw) -> None:
        async with self._cond:
            for k, v in kw.items():
                setattr(self, k, v)
            self._cond.notify_all()

    @property
    def open_turn(self) -> Pending | None:
        """The turn still waiting for an answer: an answered one stays `pending` until the
        engine picks the answer up, and must not be handed out again."""
        p = self.pending
        return p if p is not None and not p.reply.done() else None

    async def wait(self, timeout: float) -> None:
        """Return when a turn is open or the talk is over, or after `timeout` seconds."""
        async with self._cond:
            try:
                await asyncio.wait_for(
                    self._cond.wait_for(lambda: self.open_turn or self.outcome), timeout
                )
            except TimeoutError:
                pass

    def answer(self, turn: Turn) -> bool:
        """Hand the outside agent's turn to the engine; False if no turn is open. Call it on
        the event loop's thread: the reply is an asyncio future."""
        p = self.open_turn
        if p is None:
            return False
        p.reply.set_result(turn)
        return True


class LiveTurns:
    """Mailboxes by (match id, seat id)."""

    def __init__(self):
        self._boxes: dict[tuple[str, str], Mailbox] = {}

    def box(self, match_id: str, seat_id: str) -> Mailbox:
        return self._boxes.setdefault((match_id, seat_id), Mailbox())

    def get(self, match_id: str, seat_id: str) -> Mailbox | None:
        return self._boxes.get((match_id, seat_id))

    async def end(self, match_id: str, outcome: dict[str, Any]) -> None:
        for (mid, _), b in list(self._boxes.items()):
            if mid == match_id:
                await b._set(pending=None, outcome=outcome)

    def drop(self, match_id: str) -> None:
        """Forget a finished match's mailboxes; its outcome is in the store from then on."""
        for key in [k for k in self._boxes if k[0] == match_id]:
            del self._boxes[key]


class LiveAgent:
    def __init__(
        self,
        box: Mailbox,
        timeout: float = TURN_TIMEOUT,
        on_pending: Callable[[str], Awaitable[None]] | None = None,
    ):
        self.box, self.timeout, self.on_pending = box, timeout, on_pending

    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        reply = asyncio.get_running_loop().create_future()
        await self.box._set(pending=Pending(view, feedback, reply))
        if self.on_pending:
            await self.on_pending(view.role)
        try:
            return await asyncio.wait_for(reply, self.timeout)
        except TimeoutError:
            return Turn(
                role=view.role,
                message="(timed out)",
                action=Action(type="walk_away"),
                reasoning="the live agent did not answer in time",
            )
        finally:
            await self.box._set(pending=None)
