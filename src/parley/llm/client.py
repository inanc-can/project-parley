"""Thin wrapper over LiteLLM: any provider by model string, with caching and token counts.

Model strings follow LiteLLM, e.g. "featherless_ai/meta-llama/Llama-3.3-70B-Instruct"
(needs FEATHERLESS_AI_API_KEY), "anthropic/claude-sonnet-5-5", "ollama/llama3".
"""

import asyncio
import hashlib
import json
from typing import Any

from pydantic import BaseModel, Field

from parley.llm.cache import Cache


class LLMResponse(BaseModel):
    text: str
    model: str
    tokens: dict[str, int] = Field(default_factory=dict)
    cached: bool = False


class LLMClient:
    def __init__(self, cache: Cache | None = None, concurrency: int = 4, num_retries: int = 3):
        self.cache, self.num_retries = cache, num_retries
        self._sem = asyncio.Semaphore(concurrency)

    async def complete(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        seed: int = 0,
    ) -> LLMResponse:
        """`seed` is part of the cache key, so repeated episodes get distinct samples
        while rerunning the same episode is reproducible."""
        request = dict(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
        )
        key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
        if self.cache and (hit := self.cache.get(key)):
            return LLMResponse(**hit, cached=True)

        async with self._sem:
            resp = await self._call(model, messages, temperature, max_tokens)
        if self.cache:
            self.cache.set(key, resp.model_dump(exclude={"cached"}))
        return resp

    async def _call(self, model, messages, temperature, max_tokens) -> LLMResponse:
        import litellm  # slow import; only needed for live calls

        # num_retries covers transient failures (rate limits, timeouts); permanent ones
        # such as a gated or unknown model still raise and stop the match.
        r: Any = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            num_retries=self.num_retries,
        )
        usage = getattr(r, "usage", None)
        return LLMResponse(
            text=r.choices[0].message.content or "",
            model=model,
            tokens={
                "prompt": getattr(usage, "prompt_tokens", 0) or 0,
                "completion": getattr(usage, "completion_tokens", 0) or 0,
            },
        )
