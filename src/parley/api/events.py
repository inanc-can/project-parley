"""In-memory event log per running match; any number of viewers can stream it from the start."""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

FINAL = {"match_end", "error"}


class MatchEvents:
    def __init__(self):
        self.events: list[dict[str, Any]] = []
        self._cond = asyncio.Condition()

    @property
    def done(self) -> bool:
        return bool(self.events) and self.events[-1]["type"] in FINAL

    async def push(self, event: dict[str, Any]) -> None:
        async with self._cond:
            self.events.append(event)
            self._cond.notify_all()

    async def stream(self) -> AsyncIterator[dict[str, Any]]:
        i = 0
        while True:
            async with self._cond:
                await self._cond.wait_for(lambda i=i: len(self.events) > i)
                batch = self.events[i:]
            i += len(batch)
            for e in batch:
                yield e
                if e["type"] in FINAL:
                    return
