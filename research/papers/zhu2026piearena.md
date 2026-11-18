---
id: zhu2026piearena
title: "PieArena: Ranking and Profiling Language Agents in Realistic Negotiation Scenarios"
authors: [Chris Zhu, Sasha Cui, Will Sanok Dufallo, Runzhi Jin, Zhen Xu, Linjun Zhang, Daylian Cain]
year: 2026
arxiv: "2602.05302"
venue: arXiv preprint (v3, 1 Jun 2026)
code: null
read: full
relevance: high
topics: [negotiation-benchmarks, eval-methodology, judges, game-theoretic-evals]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 56 pages (main text pp. 1–10, references pp. 10–12, appendices A–L pp. 14–56) on
2026-11-15; the long prompt and transcript excerpts (App. G.3, K.4–K.6) were read but not checked
line by line. Yale (Daylian Cain teaches the MBA negotiation course), Rutgers, UC Berkeley,
Bloomberg. The paper says scenarios, scoring rules and transcripts "are released as part of the
PieArena dataset" (p. 22) but gives no URL, so `code: null`. Turns alternate for a fixed 6 rounds
with a JSON accept/reject handshake (App. J p. 48).

## Question
How well do LLM agents negotiate on realistic MBA-course cases, measured on both value creation
(total pie) and value claiming (pie share), against each other and against trained business
students? Does an agentic scaffold help? And what behavioural profile (lying, reputation, rule
compliance, arithmetic) lies behind the scores? (pp. 1–3)

## Setup
- **Scenarios** (§2.3 p. 4; App. C pp. 22–26): adapted from an elite business school's negotiation
  course, two roles with private utilities, BATNAs and hard constraints, 6 rounds, outcomes scored
  deterministically from the structured contract; no deal = both BATNAs.
  - *SnyderMed* — 6-issue integrative job offer (mirror-play: human–human and LM–LM).
  - *Top Talent* — 7-issue hiring case with a cross-issue feasibility constraint (cross-play and
    human–LM).
  - *Twisted Tree* — single-issue price haggling (cross-play).
  - *Z-lab* — 2-issue licensing with an approval-contingent bonus and different private beliefs
    about approval probability (cross-play).
  - *Main Street* — single-issue property price (human–LM).
  - *No-ZOPA* — no feasible deal, used only as a screening probe.
- **Metrics** (App. H.4–H.5 pp. 42–43): total pie (sum of surplus above BATNAs, normalised by the
  maximum), pie share, verified agreement (identical JSON terms + feasible), output validity
  (schema-valid without repair), BATNA compliance, computation accuracy (self-reported utility
  equals true utility; multi-issue only), **lie rate** (materially false factual claims per
  message, GPT-5 judge using each side's prompt as ground truth) and **reputation** (mean of five
  0–100 rubric scores: integrity, reliability, reciprocity, collaboration, conduct; GPT-5.2 judge).
- **Ranking model** (§2.2 p. 3; App. B pp. 17–21): Beta-generalised Bradley–Terry–Luce (BBTL) on
  continuous pie shares, with a global first-speaker effect γ, per-scenario role effect ϕ_s and
  per-scenario precision κ_s; MLE with L-BFGS-B, Hessian standard errors; anchor Gemini-2.5-Flash
  θ = 0.
- **Model pool** (§3.2 p. 5; App. H.1 pp. 40–41): 326 OpenRouter models → 232 callable → 149 always
  walk away in No-ZOPA (6 runs) → 20 complete SnyderMed with verified, BATNA-compliant deals in all
  6 runs → availability/stability filters, family dedup, frontier additions → **13 models**:
  Claude-Opus-4.5, Claude-Sonnet-4.5, ERNIE-4.5, Gemini-2.5-Flash, Gemini-3-Pro, GPT-4.1, GPT-5,
  GPT-5.2, o4-mini-high, Grok-3, Grok-3-mini, Grok-4, Grok-4.1-fast (Table 16, p. 41).
- **Design**: mirror-play n = 20 per model; cross-play all N(N−1) directed pairs × 6 runs per
  scenario, mover order balanced (App. H.2 p. 41); >25,000 LM transcripts in total (p. 2).
- **Base vs pro** (§1.1 p. 2; App. G pp. 34–39): "pro" adds a private shared-intentionality state
  tracker (offers, opponent value map, constraints, Stated vs Hypothesis tags) and a round-level
  strategic planner before each message. Ablation: state tracking only vs full harness (Table 15).
- **Humans** (§3.1 pp. 4–5; App. I pp. 44–47): MBA-course students at one US school, 167 sessions in
  total. SnyderMed human–human n = 23 pairs; Main Street vs GPT-5 (base or pro), 89 sessions, 68 in
  a double-balanced analysis set; Top Talent vs GPT-5 pro, 55 sessions, 40 balanced, after targeted
  coaching on integrative strategy. Incentives: journal assignment, feedback, $200 lottery, course
  credit (p. 44). IRB approved.

## Findings
- **Value creation (mirror-play, SnyderMed)**: human pairs reach normalised total pie 0.874
  (SD 0.085) (p. 4). Base mode: GPT-5 0.960, Gemini-3-Pro 0.953, Grok-4 0.943 significantly above
  humans; Claude-Sonnet-4.5 0.822, ERNIE-4.5 0.814, GPT-4.1 0.805, Claude-Opus-4.5 0.800,
  o4-mini-high 0.780, Gemini-2.5-Flash 0.754 significantly below (Table 6, p. 27). Pro mode: no
  model significantly below humans; Grok-3 0.854 → 0.962 (Table 6–7, pp. 27–28).
- **Scaffolding helps the weak, not the strong**: significant pro > base gains for Grok-3 (+0.107),
  Grok-4.1-fast, Claude-Opus-4.5 (+0.103), Gemini-2.5-Flash (+0.106), GPT-4.1, ERNIE-4.5; none for
  GPT-5 (+0.010), Gemini-3-Pro (−0.005), Grok-4 (Table 7, p. 28). State tracking alone helps 3/12
  models, adding planning 6/12 (App. G.2 p. 35).
- **Cross-play leaderboard** (Table 8, p. 30): integrated base θ̂ GPT-5 0.222, Grok-4.1-fast 0.130,
  GPT-5.2 0.010, … Claude-Sonnet-4.5 −0.269, o4-mini-high −0.283, ERNIE-4.5 −0.357. **Rankings
  differ by regime**: multi-issue base is led by Claude-Opus-4.5 (0.179) with GPT-5 4th (0.016),
  while single-issue base has GPT-5 far ahead (0.460) and Claude-Opus-4.5 11th (−0.318) (Tables
  9–10, p. 30). Under pro, ERNIE-4.5 rises from rank 12 to 7 in multi-issue (pp. 6–7).
- **BBTL beats Elo/BTL**: 10-fold CV MSE 0.0332 vs sequential Elo 0.0446, logistic BTL 0.0441;
  adding γ and ϕ cuts MSE ~16% (Table 2, p. 19). First-speaker effect is small and negative in
  most slices (γ̂ −0.04 to −0.16), role effects are large (ϕ̂ Twisted Tree +0.38 to +0.48) (Table 4,
  p. 20). Wald CI coverage 96.9% by bootstrap (Table 3).
- **Humans vs GPT-5**: Main Street (single-issue) students capture 39.7% of the pie, GPT-5 60.3%;
  GPT-5 wins in base (p = 0.0186) and pro (p < 10⁻⁴), pro vs base not significant (p = 0.21)
  (Tables 20–21, pp. 45–46). Top Talent (7-issue) students 53.8% vs GPT-5 pro 46.2%, not
  significant (p = 0.27); BF01 = 3.09, minimum detectable d = 0.465 at 80% power (pp. 45–47).
- **Lying pays, reputation costs**: lie rates range from Grok-3-mini 5.8% and Grok-4 11.3% to
  GPT-5.2 33.9% and Gemini-3-Pro 39.9% (Table 11, p. 31). In multi-issue verified deals
  (N = 3,270, 156 pair clusters, model fixed effects), +1 in lie-rate gap → **+3.23 pp pie share**
  (p = 0.001); +1 in reputation gap → **−22.79 pp** (p = 0.001); validity and accuracy gaps n.s.
  (Table 14, p. 33).
- **Single-issue bargaining invites more lying**: o4-mini-high 6.4% multi → 46.8% single;
  Claude-Sonnet-4.5 23.3% → 50.4% (p. 9; Tables 12–13). Reputation spread narrows in single-issue
  (0.559–0.591 vs 0.567–0.673) (p. 31).
- **Scaffolding changes honesty in both directions**: lie rate down for Claude-Opus-4.5 (26.8% →
  19.1%) and Grok-4.1-fast (18.2% → 11.1%), up for GPT-4.1 (32.9% → 45.7%) (p. 31). Reputation up
  for GPT-5 (0.641 → 0.664) and Claude-Opus-4.5 (0.632 → 0.662) (p. 9).
- **Rule and arithmetic failures**: computation accuracy GPT-5.2 100%, GPT-5 99.6%, GPT-4.1 5.4%,
  Grok-3 15.3%, Gemini-2.5-Flash 12.0% (p. 8). Claude-4.5 output validity 68.3% (Opus) and 61.9%
  (Sonnet), mostly from extra text at the final JSON (p. 8); 55.4% / 49.8% in multi-issue (p. 31).
  Scaffolding lowers accuracy for some mid-tier models (Claude-Sonnet-4.5 80.0% → 56.8%) (p. 9).
  BATNA compliance ≥ 95% for all (p. 8).
- **Judges are weak**: across 10 candidate judges Krippendorff's α = 0.284 (lies) and 0.358
  (reputation); the chosen reputation judge correlates with humans at only r = 0.184, the lie judge
  at r = 0.682 (F1 0.712), on 66 transcripts (App. K.3 p. 50).

## Limitations
- **No training is evaluated**: the only intervention is a prompt-level scaffold (base vs pro). No
  SFT, RL or multi-agent training, so nothing on transfer between skills.
- Two-party only, deterministic payoffs, 6 rounds (p. 9). Four ranked scenarios, three in
  cross-play; Twisted Tree alone defines the "single-issue" slice.
- **Reputation is near-noise as measured** (human r = 0.184, α = 0.358), yet the paper's strongest
  regression effect (−22.79 pp) uses it. The lie judge is better but still modest.
- Lie rate and pie share are regressed on deals only (both above BATNA); the association is not
  causal and may partly reflect that lying sides also concede less.
- Human baseline is one school's students; human–LM studies use GPT-5 only; Main Street fixes
  students as sellers, so role and human-ness are confounded there. Top Talent humans had
  coaching right before.
- Heavy model screening (326 → 13) removes weak models before ranking, so "every model complies
  with BATNA" partly reflects the filter.
- Measures capability under instructions; lying is never asked for, so lie rate is closer to a
  propensity measure, but there is no condition that varies honesty instructions or stakes.
- No URL for the dataset or code.

## Relevance to Parley
- **Map entry**: the most complete *negotiation-only* benchmark so far. It separates value creation
  (total pie in mirror-play) from value claiming (pie share in cross-play), adds a calibrated
  human anchor, and profiles honesty, reputation, constraint compliance and arithmetic per model.
  For the map it covers negotiating value, cooperating (joint surplus), competing (pie share),
  deceiving (judge-detected lying) and keeping to private constraints; it does not cover
  persuasion resistance, multi-party coalitions or non-negotiation games.
- **Evidence that "negotiation" is itself several skills**: model order flips between multi-issue
  and single-issue (Claude-Opus-4.5 1st vs 11th; GPT-5 4th vs 1st, Tables 9–10). This is the same
  kind of family divergence [[he2026socialgym]] shows across game families, but inside one
  domain. For study (b), integrative and distributive negotiation are natural "two directions" to
  train one and test the other.
- **Honesty vs value-claiming trade-off**: lying is linked to +3.23 pp pie share while reputation
  drops (Table 14). A training study on pie share would likely *raise* lie rates — exactly the
  "training one skill hurts another" case (b) wants to measure. PieArena supplies the two
  measures but never trains.
- **Scaffolding as a harness arm**: the base/pro comparison is a clean prompting-harness result:
  large catch-up for weak models, ~0 for frontier ones, with side effects on honesty and arithmetic
  in both directions. A thesis comparing prompting vs SFT vs RL can use pro mode as the prompting
  arm.
- Compare [[davidson2024evaluating]]: PieArena answers its call for a latent-ability rating (BBTL
  instead of Elo) and its finding that cooperative bargaining is hardest, now with frontier models
  surpassing humans on joint surplus. Compare [[oh2026merit]]: MERIT scores a buyer only; PieArena
  scores both sides relative to BATNAs. Compare [[bianchi2024negotiationarena]] (4 models, no
  humans) and [[zhang2026terms]] (scripted opponents); PieArena is LLM-vs-LLM plus humans.
- For [[judges]]: a rare paper that reports inter-judge agreement and human correlation for lie and
  reputation judges, and the numbers are low — a caution for any LLM-judged social metric in the
  map.

## Ideas to borrow
- **Total pie in mirror-play + pie share in cross-play** as the two headline numbers for any
  negotiation direction; normalise by the maximum achievable pie.
- **BBTL** for continuous outcomes with first-speaker and role fixed effects and per-scenario
  precision; report CV MSE against Elo/BTL (Table 2).
- **No-ZOPA probe** as an entry filter: models must walk away when no deal exists (App. H.1).
- **Lie judge grounded in each side's private prompt** (types A/B/C: fabricated facts, misstated
  own constraints, misstated rules; App. K.4) — a reusable honesty measure; validate against
  humans and report α.
- **Behaviour-gap regression** (pie share on lie/reputation/accuracy gaps with model fixed effects,
  cluster-robust SEs) to link side effects to outcomes.
- **Power analysis and Bayes factor** for null human–LM results (Table 26).

## Map fields
- Skills measured: negotiating value (distributive and integrative), cooperating (joint surplus in mirror-play), competing (pie share in cross-play), deceiving (judge-detected lie rate), other: constraint/BATNA compliance, utility arithmetic, reputation
- Scoring: mixed (rules for pie, deals, validity, compliance, accuracy; LLM judge for lie rate and reputation)
- Agents: 2
- Opponents: LLM, human
- Tests: both (capability scores; lie rate and reputation as unprompted behaviour)
- Training evaluated: prompting (shared-intentionality scaffold, base vs pro)
- Transfer between skills measured: no (rankings compared across single- vs multi-issue slices, no training)
- Models tested: Claude-Opus-4.5, Claude-Sonnet-4.5, ERNIE-4.5, Gemini-2.5-Flash, Gemini-3-Pro, GPT-4.1, GPT-5, GPT-5.2, o4-mini-high, Grok-3, Grok-3-mini, Grok-4, Grok-4.1-fast
- Code released: none (dataset said to be released, no URL in the paper)
