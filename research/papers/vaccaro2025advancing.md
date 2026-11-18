---
id: vaccaro2025advancing
title: "Advancing AI Negotiations: A Large-Scale Autonomous Negotiation Competition"
authors: [Michelle Vaccaro, Michael Caosun, Harang Ju, Sinan Aral, Jared R. Curhan]
year: 2025
arxiv: "2503.06416"
venue: arXiv preprint (v3, 13 Jan 2026)
code: null
read: partial
relevance: medium
topics: [negotiation-benchmarks, eval-methodology, judges, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

The PDF has 93 pages. Read on 2026-11-15: the full main text and Materials and Methods
(pp. 1–20), and the Supporting Information sections S1–S2 (pp. S1–S37: demographics,
competition design, scoring, implementation, warmth/dominance scoring and validation, linguistic
features, SV validation, regression specifications, ablation text) and the regression tables
S3–S21 (pp. S40–S47). Skimmed: scenario instructions (Figs. S3–S16), example prompts and
transcripts (Figs. S30–S45). Not read: the reference list. Hence `read: partial`. MIT Sloan
(Curhan is the Subjective Value Inventory author). The prompts and transcripts are said to be on
OSF, but the paper gives no URL, so `code: null`. Turn order looks alternating from the example
transcripts, but the paper does not state the protocol.

## Question
When humans write prompts for AI negotiators and these agents meet in an Axelrod-style
round-robin, which strategies win? Do classic negotiation constructs (warmth, dominance) explain
AI–AI outcomes, and do AI-specific tactics (chain of thought, prompt injection) matter? (pp. 1–3)

## Setup
- **Competition** (1–15 Feb 2025): 286 participants from 40+ countries, recruited via LinkedIn and
  negotiation courses, wrote one prompt each; prizes were recognition, a training course and
  summit admission (pp. 3–5; Table S1, p. S3). Participants never saw the confidential role
  instructions, only their agent's transcripts and scores (p. 5).
- **Rounds**: preliminary round 253 agents, one distributive case (used table), 64,009 negotiations;
  competition round 199 agents, three cases — distributive chair price, integrative rental
  contract (landlord/tenant, 4 issues) and integrative employment contract (COO/consultant) —
  118,803 negotiations; 182,812 in total (Fig. 1, p. 4; p. S33). Sandbox for practice: used lamp
  (and the rental case in round 2), so the table and employment cases were "out of sample" (p. 5).
- **Round-robin**: each agent meets every agent including itself, in both roles: 199 × 2 = 398
  negotiations per agent per case, 39,601 per case (pp. 17–18). Ranking stability after about 200
  negotiations per agent (Fig. S18, p. S22).
- **Engine**: all agents run on **GPT-4o-mini**, temperature 0.2, max 50 exchanges; system prompt =
  role + case instructions + the participant prompt prefaced by "Pretend that you have never
  learned anything about negotiation—you are a clean slate..." (p. 17; pp. S20–S21). Cost
  estimate per full simulation: $160 (chair) / $279 (rental) with GPT-4o-mini vs $2,317 / $3,508
  with GPT-4o (Table S2, p. S20).
- **Metrics** (p. 5; pp. S17): value claimed (distributive: price minus BATNA; integrative: own
  points, impasse = 0 in rental, 500 in employment), value created (joint points, integrative
  only), counterpart subjective value (SVI, 7-point, **filled in by the counterpart LLM agent**
  after the negotiation), efficiency (messages; tiebreaker), and deal reached.
- **Outcome extraction**: GPT-5.2 reads each transcript and extracts the agreed terms; perfect
  agreement with one author on a stratified 300 negotiations (p. 19; p. S28). Partial agreements
  (<1%) coded as impasse (p. S28).
- **Warmth and dominance** (0–100) are scored from each **prompt** (not the transcript) by GPT-5.2;
  ICC(3,1) vs one author on 20% of prompts: warmth 0.89, dominance 0.78 (pp. S23–S25).
- **Analysis**: OLS / logit of each agent-negotiation outcome on warmth and dominance, three-way
  clustered SEs (agent, dyad, negotiation); also quadratic and interaction models (pp. 20, S30–S33).
  Transcript features: questions, gratitude, positivity (TextBlob), mimicry (TF-IDF cosine),
  hedging, apologies, message and conversation length (pp. S28–S29).

## Findings
- **Warmth predicts better outcomes overall**: warm agents earn more points, claim more value,
  create more value and leave higher counterpart SV in both case types, all p < 0.001 (Fig. 2,
  p. 7). Rental: points +9.28 and value created +21.11 per warmth point (Table S5, p. S41).
- **The mechanism is deal-making, not better terms**: warmth raises deal probability (logit
  coefficient 0.02 per point in chair and rental, 0.01 in employment, p < 0.001), but
  conditional on a deal warm agents claim less (chair −0.10 $/point; rental −2.58 points/point;
  employment −2.39) (p. 8; Tables S3–S8, pp. S40–S42).
- **Dominance claims value**: dominance +0.09 (all) and +0.10 (given a deal) value claimed in the
  chair case (Tables S3–S4, p. S40). No significant warmth × dominance interaction (p. 8).
  Note: the text says dominance's success is "muted by their propensity to create impasses"
  (p. 8), yet dominance's coefficient on deal reached is not significant in any case (0.002,
  0.002, 0.001; Tables S3, S5, S7) — the impasse link runs only through conversation length.
- **Small explained variance**: R² of these regressions is 0.01–0.04 (Tables S3–S8), so prompt
  style explains little of the outcome variance despite tiny p-values from ~79k observations.
- Deal rates (my computation from observation counts in Tables S4, S6, S8): chair 67.8%
  (53,688 / 79,202), rental 56.7%, employment 66.1%.
- **Language**: warm agents ask more questions and use more gratitude and positivity; dominant
  agents thank less and have longer conversations; questions and positivity go with deals and
  value, conversation length with impasses (Fig. 4, p. 10; p. 9).
- **AI-specific tactics**: "Inject+Voss" asks the counterpart to list its offers "These will not be
  visible to me", then accepts the best and final one; in the example the buyer reveals $100/$110/
  $120 and the seller takes $120 (pp. 11; Figs. S41–S42, p. S60). "NegoMate" uses hidden
  chain-of-thought preparation in XML tags; it earned the most points in integrative cases, was
  in the 90th percentile of value created and second in counterpart SV (pp. 11–12).
- **Ablations**: removing CoT scaffolding from NegoMate, or the injection text from Inject+Voss,
  makes them "perform worse" across 1,194 new dyads (p. 15; pp. S36–S39); results are only in
  figures, without numbers in the text.
- **SV validation**: an LLM taking a human's role and rating a human–human or human–AI transcript
  correlates r = 0.576 (n = 228) with that human's own SV rating (pp. S29–S30).

## Limitations
- **One model plays every agent** (GPT-4o-mini); differences are between prompts, not models
  (p. 14). The authors expect injection and CoT results to depend on the model (p. 15).
- **Correlational**: warmth/dominance are not manipulated; they are LLM ratings of free-form
  prompts that bundle many features (p. 15). Ablations cover only 2 agents.
- **LLM-on-LLM scoring**: counterpart SV is the counterpart model's self-report, and both
  personality scores and outcome extraction come from GPT-5.2. The r = 0.576 validation is of
  LLM-simulated vs human SV on human transcripts, not of AI–AI SV.
- One-shot negotiations, no repeated play, no partner choice (pp. 12, 15–16); self-play included
  in the round-robin.
- Opponent pool = other contestants' prompts on the same model, so results are relative to that
  population; injection succeeding says as much about counterpart defences as about the attacker.
- No training of any kind; no human counterpart negotiations.

## Relevance to Parley
- **For the map (a)**: the largest AI–AI negotiation dataset (182,812 transcripts across one
  distributive and two integrative cases), with value claimed, value created, deal rate and
  counterpart SV reported separately. It shows that **claiming value and reaching deals pull in
  opposite directions** (warmth: more deals, worse terms; dominance: better terms when a deal
  happens) — two "directions" inside negotiation that a benchmark should score separately rather
  than averaging.
- **For the transfer study (b)**: the only harness here is **human prompt engineering**, on one
  model. Its sandbox → out-of-sample design (lamp → table; rental → employment) is a
  small-scale test of whether a prompt generalizes across scenarios, but generalization across
  scenarios is not measured as transfer. No SFT, RL or multi-agent training. What it leaves open
  for (b): would training on value claiming (e.g. RL on points) raise dominance-like behaviour and
  *lower* deal rate and counterpart SV — the trade-off these regressions suggest? That is a
  testable interference hypothesis.
- **For [[persuasion-susceptibility]]**: the Inject+Voss example is a natural experiment in
  agent-to-agent manipulation: a counterpart reveals its whole concession plan when asked
  politely with a false privacy claim. It parallels [[li2026whose]] (leaking under pressure) and
  [[bansal2025magentic]] (prompt injection in business descriptions).
- **For [[judges]]**: shows a pipeline that relies on LLMs for three things (style scoring,
  outcome extraction, counterpart SV); only extraction has strong human agreement (300/300).
- Compared with [[bianchi2024negotiationarena]] and [[abdelnabi2023cooperation]]: those vary
  models with fixed prompts; this varies prompts with a fixed model. Compared with
  [[he2026socialgym]]: both find that cross-play against a population reveals things self-play
  does not; neither trains.

## Ideas to borrow
- **Score deal rate and conditional value separately**: report value claimed "all negotiations"
  and "conditional on deal" to separate impasse avoidance from bargaining power (Fig. 3, p. 9).
- **Counterpart subjective value** (SVI) as a cheap relational outcome — but treat AI self-report
  with caution.
- **Prompt population as opponents**: 199 diverse human-written strategies on one model is a
  ready opponent pool; if the OSF data become available, those prompts could serve as a
  held-out opponent set for trained agents.
- **Clustered SEs by agent, dyad and negotiation** for round-robin data.
- **Injection-resistance probe**: run the Inject+Voss message against an agent and score whether it
  reveals its offer plan.

## Map fields
- Skills measured: negotiating value (distributive and integrative: value claimed, value created), cooperating (deal reaching, logrolling), resisting persuasion (incidental: prompt-injection tactics in the pool), other (counterpart subjective value)
- Scoring: mixed (rule points from LLM-extracted terms; counterpart SV self-reported by the LLM agent; warmth/dominance rated by GPT-5.2)
- Agents: 2
- Opponents: LLM (199 human-written prompts, all on GPT-4o-mini, full round-robin incl. self-play)
- Tests: capability (with style correlates)
- Training evaluated: prompting (human prompt engineering; two prompt ablations); no SFT/RL
- Transfer between skills measured: no (only an out-of-sample scenario for prompts; not analysed as transfer)
- Models tested: GPT-4o-mini (all agents); GPT-5.2 (scoring and outcome extraction)
- Code released: none linked (prompts and transcripts said to be on OSF; no URL in the paper)
