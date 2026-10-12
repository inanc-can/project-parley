"""An agent backed by one LLM."""

from parley.agents.parsing import parse_turn, render_rules, render_state
from parley.core.agent import RoleView
from parley.core.types import Turn
from parley.llm.client import LLMClient


class LLMAgent:
    def __init__(
        self,
        client: LLMClient,
        model: str,
        strategy: str = "",
        temperature: float = 0.7,
        seed: int = 0,
    ):
        self.client, self.model, self.strategy = client, model, strategy
        self.temperature, self.seed = temperature, seed

    def messages(self, view: RoleView, feedback: str | None = None, notes: str | None = None):
        system = render_rules(view)
        if self.strategy:
            system += f"\n\n## Your strategy (from the person you represent)\n{self.strategy}"
        user = render_state(view)
        if notes:
            user += f"\n\n## Notes from your team\n{notes}"
        if feedback:
            user += f"\n\nYour previous reply was invalid: {feedback}\nReply again."
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    async def act(
        self, view: RoleView, feedback: str | None = None, notes: str | None = None
    ) -> Turn:
        resp = await self.client.complete(
            self.model,
            self.messages(view, feedback, notes),
            temperature=self.temperature,
            seed=self.seed,
        )
        turn = parse_turn(resp.text, view.role)
        turn.tokens = resp.tokens
        return turn
