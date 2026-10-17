"""Thin wrapper over LiteLLM: any provider by model string, with caching and token counts.

Model strings follow LiteLLM, e.g. "featherless_ai/meta-llama/Llama-3.3-70B-Instruct"
(needs FEATHERLESS_AI_API_KEY), "anthropic/claude-sonnet-5-5", "ollama/llama3".
"""

import asyncio
import hashlib
import json
import random
from typing import Any

from pydantic import BaseModel, Field

from parley.llm.cache import Cache


class LLMResponse(BaseModel):
    text: str
    model: str
    tokens: dict[str, int] = Field(default_factory=dict)
    cached: bool = False


def is_transient(e: Exception) -> bool:
    """Provider hiccups worth waiting out: overload, rate limits, timeouts, dropped
    connections. Featherless also answers an overloaded model with a 200 whose body has an
    error object appended; LiteLLM reports that as an InternalServerError ("Extra data")."""
    import litellm

    return isinstance(
        e,
        litellm.InternalServerError
        | litellm.ServiceUnavailableError
        | litellm.RateLimitError
        | litellm.Timeout
        | litellm.APIConnectionError,
    )


class LLMClient:
    def __init__(
        self,
        cache: Cache | None = None,
        concurrency: int = 4,
        retry_delays: tuple[float, ...] = (2, 5, 10, 20),
    ):
        """retry_delays: seconds to wait before each retry of a transient failure."""
        self.cache, self.retry_delays = cache, retry_delays
        self._sem = asyncio.Semaphore(concurrency)

    async def complete(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        seed: int = 0,
        cache: bool = True,
        retry_delays: tuple[float, ...] | None = None,
    ) -> LLMResponse:
        """`seed` is part of the cache key, so repeated episodes get distinct samples
        while rerunning the same episode is reproducible. `cache=False` always asks the model
        (and stores nothing); `retry_delays` overrides the client's backoff for this call."""
        request = dict(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
        )
        key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
        use_cache = self.cache if cache else None
        if use_cache and (hit := use_cache.get(key)):
            return LLMResponse(**hit, cached=True)

        delays = self.retry_delays if retry_delays is None else retry_delays
        for delay in (*delays, None):
            try:
                async with self._sem:
                    resp = await self._call(model, messages, temperature, max_tokens)
                break
            except Exception as e:
                if delay is None or not is_transient(e):
                    raise
                await asyncio.sleep(delay * (0.75 + random.random() / 2))  # jitter
        if use_cache:
            use_cache.set(key, resp.model_dump(exclude={"cached"}))
        return resp

    async def _call(self, model, messages, temperature, max_tokens) -> LLMResponse:
        import litellm  # slow import; only needed for live calls

        # complete() retries transient failures with backoff; what still fails is retried
        # per episode by the match runner, except setup errors, which stop the match.
        r: Any = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            num_retries=0,
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
