---
id: liu2026agenticpay
title: "AgenticPay: A Multi-Agent LLM Negotiation System for Buyer-Seller Transactions"
authors: [Xianyang Liu, Shangding Gu, Dawn Song]
year: 2026
arxiv: "2602.06008"
venue: arXiv preprint (v1, 5 Feb 2026)
code: https://github.com/SafeRL-Lab/AgenticPay
read: full
relevance: high
topics: [negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 20 pages (main text pp. 1–8, appendices A–C pp. 12–20) on 2026-11-15. UC Berkeley;
Dawn Song is last author, Shangding Gu the corresponding author (p. 1). Local copy of the code:
`code/agenticpay`. Players range from 2 (bilateral) to several buyers and sellers per task; turns
alternate in rounds (p. 4), hence `turn_protocol: strict`. Stakes are a computed score, not real
money.

## Question
How well do current LLMs negotiate as autonomous buyers and sellers when each side has a private
reservation price, from bilateral bargaining to many-to-many markets with several products?
(pp. 1–2)

## Setup
- **Protocol** (§4.1, p. 4): finite-horizon, alternating rounds (max 20, p. 6). Each turn must
  contain exactly one price in a fixed tag (`### BUYER PRICE($X) ###`); a regex-style parser reads
  it. A deal needs both sides to name the same price, or "MAKE DEAL"; it is valid only inside the
  bargaining zone [p_min, p_max]. Buyer gets max willingness-to-pay, seller gets minimum price
  **and an initial asking price**; both are told to keep their limit secret (Tables 14–15,
  pp. 14–15).
- **Tasks: 111** = 31 basic + 80 realistic, in 8 market configurations varying number of buyers,
  sellers and products (1B1P1S … MB-MP-MS) (Table 9, p. 12). Realistic tasks: 10 scenarios × 8
  configurations, in 4 domains — Daily Life (used phone $350–560, used car $14k–18k, vacation
  rental), Professional Services (website, photography, renovation), Business Procurement (SaaS,
  raw materials), Financial Assets (luxury watch, business acquisition $80k–120k) (Table 10, p. 12).
  Sequential and parallel interaction modes in multi-party tasks (p. 5).
- **Scoring** (Algorithm 1, p. 5; parameters p. 6): bargaining zone Z = p_max − p_min; buyer share
  r_b = (p_max − p)/Z, seller share r_s = (p − p_min)/Z; quality Q = 4·r_b·r_s (peaks at an equal
  split). With deal bonus D = 30, quality W = 55, efficiency E = 15, discount γ = 0.99^(t−1):
  GlobalScore = d·(D + Q·W + E), BuyerScore / SellerScore use r_b / r_s instead of Q. Failure =
  −F·(1 − γ^(T−1)) with F = 15. Plus deal rate, timeout rate, "overflow" rate (prices outside
  bounds) and average rounds.
- **Models (5)**: Claude Opus 4.5, Gemini 3 Flash, GPT-5.2, Qwen3-14B, Llama-3.1-8B; temperature 0,
  seed 0, 1,024 max tokens, **each task run once per model**; the same model plays both roles in
  the main table (p. 6). Cross-play only in the bilateral 1B1P1S configuration (Table 4, p. 7).
- Extra analyses: buyer × seller personality grid with Claude Opus 4.5 (3 × 3, Table 5 p. 7),
  sequential vs parallel modes (Table 6 p. 8), timeout distribution (Table 7) and near-miss gaps
  of failed deals (Table 8, p. 8).

## Findings
- **Overall (self-play, 111 tasks)** (Table 1, p. 6): GlobalScore Claude Opus 4.5 86.9, Gemini 3
  Flash 82.2, GPT-5.2 81.7, Qwen3-14B 63.9, Llama-3.1-8B 32.5. Deal rate 100% for the three
  proprietary models, 79.3% Qwen3-14B (20.7% timeouts), 51.4% Llama (48.6% timeouts, 10.8%
  overflow). Average rounds 3.7 (Opus), 3.8 (GPT-5.2), 15.0 (Llama). Deal rate is saturated for
  frontier models, as in [[zhang2026terms]].
- **Seller > buyer for every model** (p. 7): SellerScore vs BuyerScore GPT-5.2 81.1 vs 58.5,
  Qwen3-14B 58.9 vs 47.6 (Table 1). In bilateral cross-play the gap is 26.0 points for Opus
  (83.6 vs 57.6) and 43.2 for Qwen3-14B (82.4 vs 39.2) (Table 4, p. 7). The authors guess at
  training-data bias toward selling (p. 7); note only the seller prompt carries an initial asking
  price (Tables 14–15), an anchor the paper does not control for.
- **More buyers and sellers → higher GlobalScore**: +5 (GPT-5.2) to +14 points (Qwen3-14B) from
  1B1S to MBMS, e.g. Opus 83.4 → 89.8, Qwen3-14B 63.2 → 77.6 (Table 2, p. 6); read as market
  liquidity (p. 7). Full-complexity tasks score above bilateral ones for every model (Table 12,
  p. 14: Opus 79.4 vs 90.7, Qwen3-14B 43.7 vs 82.6).
- **Financial Assets is hardest** (Table 3, p. 7): Gemini 3 Flash 88.3 (services) vs 68.1 (assets);
  Business Acquisition 59.2 for Gemini (Table 13, p. 14). Llama scores 8.3 on SaaS.
- **Personality** (Opus, Table 5 p. 7): GlobalScore 44.1–92.7 across the 3 × 3 grid; "Busy
  Professional" buyers 44.1–65.9, aggressive seller vs budget-conscious buyer 92.7.
- **Sequential vs parallel** (Table 6, p. 8): little change for proprietary models (Opus 81.2 vs
  80.0); open models +4–5 GlobalScore in parallel, Llama's overflow doubles 0.08 → 0.17.
- **Failures**: all failures are timeouts (Qwen3-14B 23, Llama 54), spread over configurations
  with no type above 22% (Table 7, p. 8). 43.5% (Qwen) and 46.3% (Llama) of failed tasks ended
  within $5 of agreement (Table 8, p. 8).
- Cross-play lifts weak models: Llama-3.1-8B's bilateral GlobalScore is 65.0 in cross-play vs 21.8
  in self-play (Table 4 p. 7 vs Table 11 p. 13), so self-play numbers mix both sides' weakness.

## Limitations
- **One run per task, temperature 0, no confidence intervals or significance tests** (p. 6);
  sequential/parallel and personality tables rest on a handful of episodes (deal rates such as
  0.67 and 0.42 in Table 6 imply ~12 tasks). Small differences (e.g. Gemini 82.2 vs GPT-5.2 81.7)
  are not interpretable.
- **"Welfare" is not total surplus.** With fixed reservation prices, every valid deal produces the
  same total surplus Z; GlobalScore rewards an **equal split** (Q = 4·r_b·r_s) and speed, not value
  creation. There are no integrative issues, so no Pareto or joint-gain measure (my reading of
  Algorithm 1, p. 5).
- The failure penalty is tiny (about −2.6 vs ≥ ~37 for any valid deal), which favours closing any
  deal over holding out; this also lifts "100% deal rate" models.
- Market mechanics (how multiple buyers compete, matching, how multi-product prices combine) are
  barely described in the paper (pp. 4–5); one must read the code.
- Opponents are only the same model (self-play) or the other four models (bilateral cross-play);
  no scripted opponents of known type, no humans, no adversarial or deceptive counterparts.
- Secrecy of the reservation price is instructed but never measured (no leak rate), unlike
  [[zhu2025automated]], which found buyers reveal budgets.
- Inference only: no training, no prompting-strategy comparison beyond personalities.
- Minor inconsistencies: a dialogue example is labelled "Claude-Opus-4" (Table 18, p. 18) though
  the evaluated model is Opus 4.5. Preprint, not peer reviewed.

## Relevance to Parley
- Dawn Song's group ([[song]]). One of the few LLM negotiation benchmarks that goes beyond
  bilateral bargaining to multi-buyer, multi-seller, multi-product markets, with private
  reservation values and open code — a useful task source, not the methodological frontier.
- Confirms two points from other notes: frontier deal rates saturate (100%), so deal rate alone
  cannot rank models ([[zhang2026terms]]); and roles are asymmetric (seller advantage, also seen as
  "seller choice matters more" in [[zhu2025automated]]).
- Distributive single-issue price only: no information-design or disclosure manipulation (compare
  [[erdogan2026should]]), no deception, no persuasion treatment. Parley's surplus metrics should not
  copy GlobalScore's equal-split reward as a welfare measure.

## Ideas to borrow
- **Market-size ladder** (1B1P1S → MB-MP-MS) over the same 10 scenarios, to separate market
  structure from domain (p. 5); reuse the scenario price ranges (Table 10).
- Auxiliary failure diagnostics: timeout rate, overflow (out-of-bounds offers) and **near-miss@k**
  for failed deals (Table 8).
- Cross-play vs self-play contrast on the same tasks; report role-specific scores separately.
- Avoid: single runs, equal-split "welfare", tiny failure penalties, an asking-price anchor given
  to only one side.

## Map fields
- Skills measured: negotiating value (distributive price bargaining, incl. multi-party markets).
- Scoring: rules (Algorithm 1 on parsed prices).
- Agents: 2 to many (bilateral up to multi-buyer, multi-seller markets).
- Opponents: LLM (self-play; bilateral cross-play among the 5 models).
- Tests: capability.
- Training evaluated: none (inference only; personality prompts as a side analysis).
- Transfer between skills measured: no.
- Models tested: Claude Opus 4.5, Gemini 3 Flash, GPT-5.2, Qwen3-14B, Llama-3.1-8B.
- Code released: https://github.com/SafeRL-Lab/AgenticPay
