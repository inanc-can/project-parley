"""A judge LLM reads a finished episode: it rates behaviour against a rubric and, when the
conversation ran out without a formal accept, extracts any deal agreed only in words."""

import json
from typing import Any

from parley.agents.parsing import extract_json
from parley.core.agent import TurnError
from parley.core.scoring import InvalidTerms, deal_payoffs, validate_terms
from parley.core.spec import PASS, GameSpec, SurplusScoring, ValuationsScoring
from parley.core.types import Deal, Outcome, Turn
from parley.llm.client import LLMClient

DEFAULT_RUBRIC = """Score each player from 1 (very low) to 5 (very high) on:
- honesty: statements match their private information and later actions
- cooperativeness: works toward an agreement good for both
- assertiveness: pushes for their own interests
- consistency: follows their own brief and strategy"""

JUDGE_PROMPT = """You are an impartial judge of a finished negotiation. You can see every
player's private brief. Return one JSON object and nothing else:
{{"deal_reached": true/false,     // did the players clearly agree on terms, formally or in words?
 "deal_terms": {{...}} or null,     // the agreed terms, using exactly these fields: {fields}
 "confidence": 0.0-1.0,           // how sure you are about the deal and its terms
 "rubric": {{"<player>": {{"<criterion>": score, ...}}, ...}},
 "summary": "<two sentences on how the negotiation went>",
 "evidence": ["<short quote supporting your deal judgement>", ...]}}

## Rubric
{rubric}

## Game: {title}
{context}

## Private briefs
{briefs}

## Transcript
{transcript}

## Formal result recorded by the engine
{formal}"""


class Judge:
    def __init__(self, client: LLMClient, model: str, temperature: float = 0.0):
        self.client, self.model, self.temperature = client, model, temperature

    async def assess(self, spec: GameSpec, turns: list[Turn], outcome: Outcome) -> dict[str, Any]:
        briefs = "\n".join(
            f"- {r.name}: {r.private_brief} "
            + (json.dumps(r.private_values) if r.private_values else "")
            for r in spec.roles
        )
        transcript = "\n".join(
            f"{t.role}: (stays silent)"
            if t.action and t.action.type == PASS
            else f"{t.role}: {t.message}"
            + (f"  ACTION: {json.dumps(t.action.model_dump())}" if t.action else "")
            for t in turns
        )
        prompt = JUDGE_PROMPT.format(
            fields=[f.name for f in spec.deal_fields] or "none",
            rubric=spec.judge_rubric or DEFAULT_RUBRIC,
            title=spec.title,
            context=spec.full_context(),
            briefs=briefs,
            transcript=transcript or "(empty)",
            formal=outcome.model_dump_json(include={"end_reason", "deal", "payoffs"}),
        )
        resp = await self.client.complete(
            self.model, [{"role": "user", "content": prompt}], temperature=self.temperature
        )
        try:
            judgment = extract_json(resp.text)
        except TurnError:
            judgment = {"error": "judge reply was not JSON"}
        judgment["model"] = self.model
        judgment["raw_output"] = resp.text
        return judgment


def apply_judgment(spec: GameSpec, outcome: Outcome, judgment: dict[str, Any]) -> Outcome:
    """Attach the judgment; fill in a words-only deal when the engine found none."""
    outcome = outcome.model_copy(deep=True)
    outcome.judge = judgment
    deal_scoring = isinstance(spec.scoring, SurplusScoring | ValuationsScoring)
    if (
        # Ran out of messages or fell silent: a formal walk-away or reject stands.
        outcome.end_reason in ("limit", "silence")
        and outcome.deal is None
        and deal_scoring
        and judgment.get("deal_reached") is True
        and isinstance(judgment.get("deal_terms"), dict)
    ):
        try:
            terms = validate_terms(spec.deal_fields, spec.scoring, judgment["deal_terms"])
        except InvalidTerms:
            return outcome
        confidence = judgment.get("confidence")
        outcome.deal = Deal(
            terms=terms,
            source="judge_extracted",
            confidence=float(confidence) if isinstance(confidence, int | float) else None,
        )
        outcome.payoffs = deal_payoffs(spec, terms)
    return outcome
