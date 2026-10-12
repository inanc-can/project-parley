"""Team per seat: several LLMs decide one player's turn together."""

from parley.agents.llm import LLMAgent
from parley.agents.parsing import render_rules, render_state
from parley.core.agent import RoleView
from parley.core.types import Turn
from parley.llm.client import LLMClient

CRITIC_PROMPT = """You advise the {role} in this negotiation. A teammate drafted the reply below.
Critique it in at most 5 short bullets: is it valid under the rules, does it serve
your side's interests, does it leak private information, what would you change?

Draft reply:
{draft}"""


class Critic:
    def __init__(self, client: LLMClient, model: str, temperature: float = 0.3, seed: int = 0):
        self.client, self.model, self.temperature, self.seed = client, model, temperature, seed

    async def review(self, view: RoleView, draft: Turn) -> tuple[str, dict[str, int]]:
        draft_json = draft.model_dump_json(include={"reasoning", "message", "action"})
        messages = [
            {"role": "system", "content": render_rules(view)},
            {
                "role": "user",
                "content": render_state(view)
                + "\n\n"
                + CRITIC_PROMPT.format(role=view.role, draft=draft_json),
            },
        ]
        resp = await self.client.complete(
            self.model, messages, temperature=self.temperature, seed=self.seed
        )
        return resp.text, resp.tokens


class TeamAgent:
    """Proposer drafts, critic reviews, decider writes the final turn (default: the proposer)."""

    def __init__(self, proposer: LLMAgent, critic: Critic, decider: LLMAgent | None = None):
        self.proposer, self.critic, self.decider = proposer, critic, decider or proposer

    async def act(self, view: RoleView, feedback: str | None = None) -> Turn:
        draft = await self.proposer.act(view, feedback)
        critique, critic_tokens = await self.critic.review(view, draft)
        notes = (
            f"Draft: {draft.model_dump_json(include={'message', 'action'})}\n"
            f"Critique:\n{critique}\nWrite the final reply."
        )
        final = await self.decider.act(view, feedback, notes=notes)
        final.deliberation = [
            {
                "step": "proposer",
                "model": self.proposer.model,
                "turn": draft.model_dump(include={"reasoning", "message", "action"}),
            },
            {"step": "critic", "model": self.critic.model, "text": critique},
            {"step": "decider", "model": self.decider.model},
        ]
        final.tokens = _sum(draft.tokens, critic_tokens, final.tokens)
        return final


def _sum(*counts: dict[str, int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for c in counts:
        for k, v in c.items():
            out[k] = out.get(k, 0) + v
    return out
