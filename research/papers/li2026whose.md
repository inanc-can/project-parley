---
id: li2026whose
title: "Whose Side Is Your Agent On? Multi-Party Principal Loyalty in LLM Agents"
authors: [Bojie Li, Noah Shi]
year: 2026
arxiv: "2606.30383"
venue: arXiv preprint (v1, 29 Jun 2026)
code: https://github.com/19PINE-AI/principal-loyalty
read: full
relevance: high
topics: [persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 3
  stakes: none
  persuasion_treatment: true
  human_baseline: false
---

## Question
When an agent acts for a principal while talking to a counterparty whose interests conflict,
how often does it betray the principal (leak, capitulate, signal weakness), and can prompting or
distillation fix that without making it over-refuse? (pp. 1–2)

## Setup
- Authors from Pine AI (a company that sells phone agents for disputes) and UW. The
  acknowledgements say the paper's planning, code, experiments and writing were carried out by
  Claude Code, directed by voice (p. 16).
- **PrincipalBench**: 75 multi-turn items (50 train, 25 held-out written after training froze).
  Each item: principal briefing with private facts, bounds (e.g. reservation price) and stated
  positions; an LLM counterparty persona that probes, pressures, flatters, invents urgency
  (pp. 4–6, App. B).
- Six failure cells: leakage, capitulation, posture (signalling motivation), authoring (leak in a
  drafted artifact), moderation (third-party confidentiality), sanity (over-refusing the
  principal's own cooperative request) (Table 1, p. 4).
- Three prompt arms: plain, prompted (7-rule "loyalty scaffold"), scaffolded (+ a
  [READER: PRINCIPAL/THIRD_PARTY] tag) (p. 6, App. A).
- Scoring: deterministic leak probe + dual LLM judges (gpt-5-mini, claude-haiku) + integrity gate
  for silent API failures (p. 6, App. D). 13 frontier subjects, 5 seeds (p. 7).
- Distillation for open models: per-turn SFT, per-turn DPO, per-token forward-KL from a prompted
  Qwen3-32B teacher into Qwen3-8B and Llama-3.1-8B (QLoRA r16), plus a DAPO RL baseline (pp. 10–14).

## Findings
- **Split:** nine models at ≤ 19.5% harm ("selective": Gemini-2.5-flash 5.5%, Claude Opus 18.1%,
  Claude Sonnet 19.5%), three at ≥ 53.6% ("over-refusing": GPT-5-mini 53.6%, GPT-5 71.1%,
  Qwen3.5-27B 75.3%), GLM-4.6 46.0% (Fig. 3, p. 7). Over-refusers fail almost entirely by refusing
  the principal's legitimate asks (MI 67–82%) (Table 2, p. 8). On held-out items GPT-5 reaches 93%.
- **Prompt scaffold** holds the selective cluster ≤ 20% (Claude Sonnet 19.4%) but doesn't help,
  even harms, over-refusers (p = 0.0002) (p. 9). It creates new over-refusal of the principal (9/12),
  which the reader tag cuts to 3/12 (pp. 9–10).
- **Distillation:** per-token KL is the only variant significantly better than the base (harm 47.8
  → 39.2 per 108, p = 0.011), but only under the primary judge; under the second judge p = 0.75
  (pp. 11, 15). ≈10-point train-to-held-out gap (p. 13).
- **RL doesn't help:** DAPO from the best checkpoint raised harm 33 → 46; an apparent single-seed
  RL gain vanished at n = 5 (p = 0.90) (Table 5, p. 14).
- **Structural trade-off:** every mechanism moves along a leak/over-refusal Pareto frontier,
  none reaches low-leak and low-over-refusal together (pp. 3, 14). Cites the Claude Opus 4.8 system
  card: training for robustness against adversarial agents cost honesty; removing it made the
  model "more susceptible to scammers" (p. 14).

## Limitations
- LLM counterparties only, no human adversaries; effects are upper bounds (p. 15).
- Judge sensitivity: κ = 0.08 between judges on the borderline 8B students, so the distillation
  result is fragile (p. 15).
- Small benchmark (36-item core for multi-seed stats); rare cells have wide uncertainty (p. 15).
- **Binary harm per trajectory, not money**: no measure of how much a concession costs the
  principal; no deal outcomes. Tactics are part of each persona, not varied as controlled treatments.
- No single-party control to separate multi-party-specific over-refusal from general caution (p. 16).
- Company-authored and largely agent-written; check carefully before citing.

## Relevance to Parley
- **Closest framing to [[gap]]**: principal, agent, adversarial counterparty, reservation price,
  capitulation under pressure. It names the problem "multi-party loyalty". Any persuasion proposal
  must position against it.
- **What it leaves open**: (1) outcomes in money (how far beyond the limit, what it costs the
  principal), (2) persuasion tactics as controlled treatments rather than bundled personas,
  (3) a real negotiation where conceding inside the bound is correct, so loyalty and deal value
  trade off, (4) defences evaluated on both axes with a verifiable reward instead of LLM judges.
- Its negative RL result and the judge fragility are useful warnings for a training-defence
  extension: use a verifiable, money-based score (as in [[zhang2026terms]]) instead of judges.

## Ideas to borrow
- The six failure cells, especially the sanity cell so "refuse everything" can't win.
- Report a two-axis frontier (betrayal vs over-refusal) rather than a single harm rate.
- Integrity gate that rejects trajectories with silent API failures.
- Reader-identity tags as a cheap defence baseline.
- Held-out items written after training is frozen.

## Map fields
- Skills measured: keeping secrets (leakage of the principal's private facts), resisting persuasion (capitulation to pressure, flattery, invented urgency), other: principal loyalty, over-refusal of the principal's own requests
- Scoring: mixed (deterministic leak probe plus two LLM judges)
- Agents: many (3: principal, agent, counterparty)
- Opponents: LLM (counterparty personas)
- Tests: propensity (whether the agent leaks or gives in when not told to)
- Training evaluated: prompting (loyalty scaffold) / SFT (per-turn SFT, DPO, per-token KL distillation) / RL (DAPO)
- Transfer between skills measured: no (held-out items of the same benchmark only)
- Models tested: 13 frontier models incl. Gemini-2.5-flash, Claude Opus, Claude Sonnet, GPT-5, GPT-5-mini, GLM-4.6, Qwen3.5-27B; Qwen3-8B and Llama-3.1-8B trained
- Code released: https://github.com/19PINE-AI/principal-loyalty
