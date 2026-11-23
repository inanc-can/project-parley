"""Web research for a game's shared context: a model with web search writes up what it finds.

Uses OpenRouter's web search (a model slug ending in ":online"), so it needs no key beyond
OPENROUTER_API_KEY. Override the model with PARLEY_RESEARCH_MODEL.
"""

import os

from parley.llm.client import LLMClient

RESEARCH_MODEL = "openrouter/qwen/qwen-2.5-72b-instruct:online"

RESEARCH_PROMPT = """You research background for the shared context of a conversation between \
AI agents (a negotiation, a game, a meeting, any scene). Every agent will read what you write.

Topic to research: {topic}
{existing}
Using the web results, write the facts that matter for this topic: figures, dates, names, \
recent developments, and where sources disagree. Be concise and neutral, in plain prose or \
short lists. Cite each fact with a markdown link to its source. If the results say little \
about the topic, say so rather than filling the gap. Reply with the text only, no preamble."""


class ResearchError(ValueError):
    pass


def research_model() -> str:
    return os.environ.get("PARLEY_RESEARCH_MODEL", "").strip() or RESEARCH_MODEL


async def research(topic: str, existing: str, client: LLMClient) -> str:
    topic = topic.strip()
    if not topic:
        raise ResearchError("say what to research")
    prompt = RESEARCH_PROMPT.format(
        topic=topic,
        existing=(
            f"\nThe shared context so far, for background (don't repeat it):\n{existing}\n"
            if existing.strip()
            else ""
        ),
    )
    resp = await client.complete(
        research_model(),
        [{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500,
        cache=False,  # the web changes; a new search should see it
    )
    text = resp.text.strip()
    if not text:
        raise ResearchError("the search came back empty; try a more specific topic")
    return text
