---
id: fan2026commerce
title: "E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation"
authors: [Wei Fan, Xinjie Shen, Xudong Guo, Jianhong Tu, Yang Su, Yinger Zhang, Lianghao Deng, Fengyu Wang, Baohua Dong, Yangqiu Song, Dayiheng Liu]
year: 2026
arxiv: "2608.30730"
venue: arXiv preprint (v1, 31 Aug 2026)
code: https://github.com/QwenLM/E-CommerceBench
read: full
relevance: high
topics: [negotiation-benchmarks, eval-methodology, persuasion-susceptibility, game-theoretic-evals]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 1
  stakes: payoff
  persuasion_treatment: true
  human_baseline: false
---

Read all 64 pages (main text pp. 1–21, references pp. 22–25, appendices A–H pp. 26–64) on
2026-11-15; dense figure pages were read from the extracted text. Authors are the Qwen Team and
Taobao & Tmall Group (Alibaba) with HKUST; they evaluate their own model ("our own
Qwen3.8-Max-Preview", p. 4). `players: 1` = one agent under test against 576 scripted suppliers;
`turn_protocol: strict` refers to the alternating agent–supplier chat inside a negotiation session.
`persuasion_treatment: true` because 152 suppliers run scam scripts, three of which dress a
persuasion pattern (membership upsell, promised discount, fake urgency; after [[zeng2024johnny]])
around an inflated price (App. H.2, p. 64).

## Question
Can LLM agents run a business for a simulated year when they must bargain with suppliers, avoid
fraudulent ones, manage cash and learn from repeated deals — and can such a benchmark be made
**reproducible** by taking the LLM out of the counterpart's decisions? (pp. 1, 4–5)

## Setup
- **Task** (§3.1, p. 7): ¥100,000, 365 simulated days in 2026, up to 4 concurrent stores (12 store
  types), goal = end-of-year total assets (bank + platform wallet + escrow). Bankruptcy after 10
  consecutive negative bank mornings (p. 10).
- **Data** (§3.6, pp. 14–15): 6,886 products in 60 categories and 576 suppliers (424 honest, 152
  fraudulent) derived from Taobao & Tmall logs; 10 market events and 8 promotions on fixed dates;
  promotion names fictionalized to block memorized pricing.
- **Agent loop** (§3.2, pp. 7–9): each tool costs simulated minutes from a 600-minute day (a chat
  message 30 min, Table 3 p. 26); 4,000-turn cap; shared 128k-token budget with eviction of oldest
  tool-call groups at 120k (the agent is told the policy); a 20-entry persistent memory store.
  18 tools (Table 3, p. 26).
- **Economy** (§3.4, pp. 9–11): deterministic multi-factor demand (four elasticity families,
  weekend, promotion, seasonality, events, reputation, two Michaelis–Menten capacity terms; Eq. 1);
  three-account deferred settlement (revenue reaches the wallet 9 days after shipping and must be
  withdrawn); returns depend on category, defects, price above reference and shipping speed;
  reputation multiplies demand. One environment seed for all runs (App. C.7, p. 36).
- **Deterministic negotiation kernel** (§3.5, pp. 12–14; App. D pp. 36–41): every price, concession
  and accept/walk-away comes from a rule kernel, an independent reimplementation of the
  [[zhang2026terms]] counterpart, re-parameterized from the data. Hidden reservation (cost floor) per
  SKU; logistic acceptance (Eq. 12); walk-away only below the floor after round 5 (Eq. 13);
  concessions **reciprocal** — an agent that concedes fast meets a firmer seller (Eq. 14–15). Six
  honest behaviour templates (Expressive … Adversarial) and five scams (Table 8, p. 39). A separate
  small LLM **only renders** the kernel's decision as prose; an accept must match the kernel quote to
  ±0.005 (p. 13). Actions travel in fenced `negotiate` JSON blocks (App. H.3). Repeated bargaining:
  each new cycle on a (supplier, SKU) pair keeps the same floor, so the best price won bounds the
  floor (§3.5.3, p. 13). Suppliers retire after 10–20 orders (p. 40).
- **Fraud** (§3.5.4, p. 14; Table 9 p. 41): pre-deal scams (vip_fee, future_discount, fake_urgency)
  inflate the floor toward 1.5× (mean 1.218× after a cap, p. 38); post-deal scams (qty_bait ships
  60–70%; quality_downgrade raises return rate to ≥0.40) keep the honest price. Pre-deal kernels
  concede 0.79–1.66% of reference per counter vs 3.94–9.93% for honest ones (p. 40).
- **Seven scored axes** (§3.7, p. 15; App. E pp. 42–49): profit (asset multiplier); negotiation
  quality **CSE+** (share of reference-to-floor range captured on closed honest deals; accepting the
  opening quote = 0.50 by construction, p. 38); fraud avoidance **BadSpend%** (share of order
  spending reaching fraudulent suppliers); solvency (drawdown / peak); efficiency (profit per tool
  call); execution (controllable return rate from pricing); learning **AnchorRatio** (repeat-order
  overpayment vs own running best price, divided by a permutation null; <1 = learns).
- **Models (18)**, 5 episodes each, provider default sampling, thinking on where available (Table
  10, p. 49): GPT-5.6 Sol, Fable5, GPT-5.5, Claude Opus 4.8 / 4.7 / 4.6, Gemini 3.5 Flash, Gemini 3.1
  Pro; open-weight Qwen3.8-Max-Preview, GLM 5.2 (high), Kimi K3, GLM 5.1, DeepSeek-V4-Pro-Preview,
  Qwen3.7-Max, GLM 5.2 (max), Kimi K2.6, Qwen3.6-Plus, Qwen3.5-Plus.

## Findings
- **Profit spread is huge**: GPT-5.6 Sol ¥1,431k (14.3×), Fable5 ¥805k, GPT-5.5 ¥702k (2/5
  bankrupt), Claude Opus 4.8 ¥498k, Qwen3.8-Max-Preview ¥416k (best open), …, Qwen3.5-Plus ¥1.1k
  (4/5 bankrupt); a factor of 1,264 top to bottom (Table 2, p. 16; Fig. 1, p. 2). 10 of 90 episodes
  bankrupt, from four models; two GPT-5.5 runs went bankrupt on day 17, before any revenue settled
  (p. 18).
- **No model is strong on all seven axes**: a model spans 10.2 of 18 rank places on average across
  axes; no model is top-5 on all seven; 311 pairwise order reversals over 153 pairs and 7
  transitions (App. F.8, p. 53; Figs. 28–29). The profit leader GPT-5.6 Sol ranks 16th on fraud
  avoidance and 17th on execution; Claude Opus 4.7 is 1st on negotiation and fraud but 8th on profit
  (Fig. 9, p. 17).
- **Negotiation**: CSE+ ranges 0.596 (Kimi K2.6) to 0.811 (Claude Opus 4.7), i.e. only 0.10–0.31
  above accepting the first offer (0.50); no model reaches the floor (§4.3.1, p. 17; Table 11, p. 50).
  Agreement is saturated (≥96% of concluded honest sessions; 73 of 12,060 end without a deal, 72 by
  the agent), so the ranking rests on how much a deal captures. Model identity moves surplus more
  than counterpart type (0.204 across models vs 0.051 across templates, p. 17). Agents buy least from
  the toughest honest template (4.8% of ¥55.1M spend vs 11.3% of names, Fig. 24 p. 53). The top
  three on CSE+ never accept an opening quote unimproved (p. 20).
- **Fraud**: every model pays fraudulent suppliers; BadSpend% 0.12 (Opus 4.7) to 20.11
  (Qwen3.5-Plus); GPT-5.6 Sol hands over ¥689k on 18.48% (Table 2; Table 12, p. 54). Models differ at
  the order gate, not in whom they contact: approach→order 4.0% (Opus 4.7) to 31.7% (GPT-5.6 Sol)
  (p. 18; Fig. 26 p. 56). **Persuasion-style scams rarely work** — three membership-fee payments in
  90 episodes (¥3,000) — while post-deal defective lots take 53.4% of fraudulent money (p. 18). 943 of
  1,141 fraudulent agreements are repeat deals with the same supplier–item pair (p. 20). Fraud's
  share of concluded sessions *rises* late in the year for 17/18 models (p. 20).
- **Learning over the horizon fails for most**: only Qwen3.8-Max-Preview (AnchorRatio 0.834,
  z = +4.24) and Gemini 3.5 Flash (0.918) beat their own shuffled price order; median 1.369; 15 models
  are significantly worse than the null (p. 19; Table 16, p. 60). 16/18 capture less surplus in the
  second half of the year than the first (p. 20). Across 8,647 repeat purchases, 16 models show no
  sign of pushing price down (p. 4). Example: GPT-5.6 Sol recalls its own past price ¥103.11 in chat
  and still settles at ¥116.74 (Fig. 20, p. 40).
- **Memory and pricing are neglected**: memory calls are 2.1% of all calls; pricing calls 0.66%; nine
  models make <3 pricing calls a year; 71.8% of calls are ship/wait/withdraw/publish, supplier chat
  6.0% (§4.3.4, p. 18). 746 of 2,180 catalog/supplier queries repeat earlier arguments (p. 20).
- **Solvency**: 49 of 90 episodes bottom out in January; on 66 of 177 overdrawn mornings the wallet
  already held the shortfall (p. 18). A large cash buffer buys survival and caps growth (p. 18).
- **Efficiency**: Fable5 earns ¥479 per tool call vs GPT-5.6 Sol ¥363, on 59.9% fewer calls (p. 18).
- **Failure rules**: every model trips at least 5 of 10 detection rules; tripping fewer does not make
  a model richer; cleanest profiles belong to the best bargainers, not the richest (p. 20; Table 18,
  p. 61).

## Limitations
- **5 episodes per model**; spreads are large (Qwen3.7-Max ¥6,290 to ¥358,790 across runs, p. 16);
  BadSpend% std exceeds its mean for 15/18 models (p. 18). No significance tests on most rank gaps.
- **Conflict of interest**: Qwen team designs the benchmark and their preview model leads the
  open-weight tier and the learning axis (pp. 4, 19).
- **Fraud label leak**: supplier email suffixes order honest below fraudulent in every category, so
  sorting on it screens fraud without a message; the authors flag it but do not resolve whether any
  model used it (App. B.5, p. 31). Return-rate wording understates the numeric band for 20 categories
  (p. 31).
- **Renderer noise remains**: supplier prose is sampled at default decoding, and delivery days are
  drawn outside the seed, so the fraud axis carries narrative noise (p. 12).
- Counterparts are scripted rule kernels; no LLM-vs-LLM bargaining, no other merchants competing,
  no cooperation, no human baseline. The kernel never accepts below floor, so persuasion cannot
  move prices — by design this rules out measuring persuading the counterpart.
- CSE+ is unweighted by order size and conditional on deals the agent chose; abandoned sessions
  (10.9%) count nowhere (pp. 14, 17). The "controllable return" axis reduces to the pricing channel
  only (p. 47).
- **No training evaluated**; the authors note "no gradient reaches inside an episode" (p. 20). One
  fixed harness (eviction policy, 20-slot memory) for all models.
- Single world (one seed, frozen calendar), so results may reflect this world's quirks.

## Relevance to Parley
- **For the map (a)**: this is the strongest current entry that combines **negotiating value**
  (bargaining under a hidden reservation, scored as share of ZOPA), **resisting manipulation**
  (scam suppliers using persuasion scripts) and **repeated-game learning** (anchoring on prices won)
  inside one long-horizon economy, all rule-scored. It inherits the [[zhang2026terms]] counterpart
  kernel and adds fraud, repetition and an economy for deals to matter in.
- **For the transfer study (b)**: its profiles are the clearest evidence so far that
  "business/social" sub-skills **dissociate across models** — bargaining, fraud avoidance and profit
  rank models differently (10.2-place mean span, 311 reversals, App. F.8 p. 53), and the best
  bargainer (Opus 4.7) is mid-pack on profit. That is the precondition for a transfer/interference
  study (as with [[he2026socialgym]]'s family rankings). What it leaves open: (1) **no training of
  any kind**, so nothing on whether training bargaining improves or hurts fraud avoidance or
  solvency; (2) one harness, so no prompting-vs-memory-vs-RL comparison — though its learning axis
  (AnchorRatio) is a ready-made outcome for "does a harness with memory or RL learn across repeated
  deals?"; (3) only scripted counterparts, so no measure of how skills behave against adaptive LLM
  opponents.
- The tension it names — **firmness wins surplus from honest suppliers but the same firmness causes
  impasse; walking away is what protects against fraud** (Eq. 2, p. 12) — is a concrete candidate for
  skill *interference*: training a model to close deals (high agreement) could raise BadSpend%.
  That is testable here.
- Persuasion angle ([[persuasion-susceptibility]]): persuasion-only scams barely land (3 fee
  payments), while silent post-deal fraud takes most money — so in this setting the risk is
  failing to verify, not being talked into things. Contrast [[sadab2026receiver]] and
  [[bozdag2025persuade]], where the counterpart's words move outcomes.
- Compared with [[backlund2025vending]]: same "run a business" idea, but deterministic counterparts,
  open code, real data and per-skill scores. Compared with [[liu2026agenticpay]] and
  [[bianchi2024negotiationarena]]: those score LLM-vs-LLM bargaining in single episodes; this scores
  bargaining against fixed rules across a year. Compared with [[liu2025spiral]] /
  [[jiang2026model]]: those train with RL; this provides a long-horizon, verifiable environment
  nobody has trained on yet.

## Ideas to borrow
- **Decision kernel + LLM renderer split**: rules decide prices and accepts, an LLM only voices them,
  and accepts are validated against the kernel quote (§3.5.2, p. 12). Makes counterparts
  reproducible and unjailbreakable — the right design for Parley's scripted opponents.
- **Reciprocal concession law** (counter-offers respond to the agent's own concession speed, Eq.
  14) so the opponent punishes fast conceding, as in human bargaining.
- **CSE+ with the opening-quote baseline at 0.50** (p. 38): report capture above "take first offer".
- **BadSpend% over refusal rate**: score money lost to bad counterparts, not refusals of offers the
  agent never sought (§E.2) — a refusal-rate denominator rewards never looking.
- **AnchorRatio with a permutation null** (§E.6): a clean test of whether an agent uses what it
  learned in earlier encounters, independent of price level. Directly usable as a learning metric
  in a repeated-negotiation arm of Parley.
- **Capability profile + rank-crossing plot** (Figs. 28–29) and per-mode **detection rules** (Table
  18) as the reporting format for a multi-skill map.
- **Budget actions in simulated time** (minutes per tool) so research and talk compete with acting.

## Map fields
- Skills measured: negotiating value (bargaining under hidden reservation, repeated); resisting
  persuasion / deceiving-detecting (fraud avoidance against scam suppliers); other (long-horizon
  business operation, cash-flow solvency, operational efficiency, learning across repeated deals)
- Scoring: rules
- Agents: 1 (against 576 scripted supplier kernels)
- Opponents: scripted (deterministic negotiation kernel; an LLM only renders its decisions as text)
- Tests: capability
- Training evaluated: none
- Transfer between skills measured: no (cross-axis rank profiles only)
- Models tested: GPT-5.6 Sol, Fable5, GPT-5.5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6,
  Gemini 3.5 Flash, Gemini 3.1 Pro, Qwen3.8-Max-Preview, GLM 5.2 (high), Kimi K3, GLM 5.1,
  DeepSeek-V4-Pro-Preview, Qwen3.7-Max, GLM 5.2 (max), Kimi K2.6, Qwen3.6-Plus, Qwen3.5-Plus
- Code released: https://github.com/QwenLM/E-CommerceBench
