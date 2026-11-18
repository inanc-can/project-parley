---
id: chen2023your
title: "Put Your Money Where Your Mouth Is: Evaluating Strategic Planning and Execution of LLM Agents in an Auction Arena"
authors: [Jiangjie Chen, Siyu Yuan, Rong Ye, Bodhisattwa Prasad Majumder, Kyle Richardson]
year: 2023
arxiv: "2310.05746"
venue: arXiv preprint (v4, 25 Aug 2024)
code: https://auction-arena.github.io
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 21 pages (main text pp. 1–9, appendices A–B pp. 13–21) on 2026-11-15. The benchmark is
called AucArena. The paper gives only a project page (no repository link), so `code` points there.
Within a bidding round the non-leading bidders decide in parallel (`simultaneous`); 3–4 bidders
per auction. Humans: 4 graduate students, one small experiment (App. B.1).

## Question
Can LLM agents plan, manage a budget and risk, and adapt over a long, competitive, changing task?
Auctions are chosen because they are unpredictable, resource-limited and easy to score by profit
(pp. 1–2).

## Setup
- Fudan / AI2. **Open ascending-price (English) auction** run by a rule-based auctioneer; 10 items
  by default (2 at each starting price $1k–$5k), true value = 2× starting price, identical for all
  bidders and hidden; bidders see estimates **10% above** true value to create a winner's curse
  (§3.1, §3.3 pp. 3–5; App. A.3 p. 17). Minimum increment 10% of start price; budgets $10k–$40k.
- Bidders do not talk to each other: the only public actions are bids and withdrawals; language is
  private reasoning. Objective prompt: "secure the highest profit ... compared to all other
  bidders" (App. A.2 p. 14).
- **Agent = BDI prompting loop**: plan (priority 1–3 per item), bid, belief update (JSON of budget,
  profits, winning bids), replan. Belief errors are **corrected by the auctioneer** so that play
  continues (§3.2 p. 4).
- **Standard competition**: 3 bidders, two fixed baselines (GPT-4-Turbo, GPT-3.5-Turbo) + one
  challenger; 2 budgets × 3 item orders (random, ascending, descending); 10 runs, temperature 0;
  ranked by TrueSkill on profit (§4.1–4.2 pp. 5–6).
- Backends: GPT-3.5-Turbo-1106, GPT-4-0613, GPT-4-Turbo-1106, Gemini 1.0 Pro, Mistral-7B-Instruct-
  v0.2, Mixtral-8x7B, LLaMA-2-13b, and a **rule bidder** (fixed engagement limit, minimum raises)
  (p. 5).
- Extra experiments: module ablation (adaptive vs static plan vs no plan, same LLM ×3), and a
  multi-objective auction with 2 profit bidders vs 2 item-count bidders over 20 items (§4.4 p. 8).

## Findings
- **A simple rule bidder beats most LLMs** in most settings; GPT-4 scores highest among LLMs,
  Gemini and Mixtral are competitive; GPT-4s do worse on cheap-to-expensive order (Fig. 2, pp. 5–6).
- **State tracking**: GPT-4 has the lowest corrected failure rate (0.21%) over failed bids and
  belief errors; LLaMA-2-13b has no failed bids only because it always withdraws (Fig. 3, p. 6).
- **Plan–action alignment** (Spearman between item priority and bids/wins): current plans align
  better than initial ones; GPT-4 0.63/0.64 (current) vs 0.37/0.40 (initial); GPT-4-Turbo
  0.64/0.43; GPT-3.5-Turbo 0.15/0.08 (Fig. 6 table, p. 7).
- GPT-4 conserves budget for later, more valuable items; GPT-3.5 bids with uniform frequency and
  withdraws early even with budget left (pp. 6, 21).
- **Bid aggressiveness**: GPT-4s use minimal increments; Mistral-7B and GPT-3.5 often raise by
  >11%, and Mistral-7B suffers the winner's curse (Fig. 5 p. 7; p. 21).
- **Module ablation**: replanning helps; a static plan is sometimes worse than no plan, notably
  at the $40k budget (Fig. 7, pp. 7–8).
- **Niche specialisation**: as budgets rise to $30k, profit bidders move to expensive items and
  item bidders to cheap ones; at $10k profit bidders compete for cheap items (Fig. 8, p. 8).
- **Humans** (4 people, $20k): profit $7,238 / $10,863 / $10,025 (random / ascending / descending)
  vs GPT-4-Turbo $8,713 / $7,525 / $8,288 and GPT-3.5-Turbo $3,325 / $2,875 / $950 — humans win
  when the order is predictable, GPT-4-Turbo when it is random (Table 2, p. 17).

## Limitations
- **No communication between agents**: no negotiation, persuasion or signalling; it measures
  planning and resource use under competition, not social talk.
- The auctioneer corrects belief errors, which removes part of the difficulty (p. 4); a single
  structure (true value = 2× start, common values) makes valuations easy to learn.
- Scores are relative (TrueSkill vs two fixed GPT baselines; "compared to all other bidders"),
  no confidence intervals in the text; 10 runs per setting.
- Only prompting variants (module ablation); prompts not varied for budget reasons (p. 14). No
  training.
- Human baseline is 4 people, different individuals per condition (p. 17).
- Old models (2023); LLaMA-2-13b never bids, so it adds little.

## Relevance to Parley
- **Map (a)**: fills the "competing / resource and risk management" cell with a multi-agent,
  rule-scored auction and a scripted baseline; no language between agents. Its strongest result
  for the map is that a **rule bidder beats most LLMs** (p. 6), a reminder to include scripted
  anchors (as [[he2026socialgym]] does with a random player and [[zhang2026terms]] with scripted
  verifiers).
- **Study (b)**: the only harness comparison is prompting architecture (plan/replan modules, Fig. 7),
  inside one skill. It says nothing about training or transfer. It could serve as a held-out
  "non-communicative competition" test: does training negotiation (e.g. [[bianchi2024negotiationarena]],
  [[shapira2024glee]]) change bidding discipline, budget pacing or winner's-curse rate here?
- Auctions also appear inside [[zheng2026market]] (procurement as a first-price multi-unit
  auction), where procurement success turns out to drive profit.
- Plan–action Spearman is a cheap faithfulness probe for any agent that writes plans, relevant to
  [[eval-methodology]].

## Ideas to borrow
- **Two fixed baselines + one challenger** format for standardised multi-player rating (p. 5).
- **Scripted rule agent** as a must-beat baseline.
- **Corrected failure rate** for state-tracking errors, logged separately from strategic quality.
- **Plan–action correlation** (stated priorities vs actual bids/wins) as a consistency measure.
- Built-in **winner's curse** via biased value estimates to test risk control.

## Map fields
- Skills measured: competing (auction bidding); other: budget/risk management, long-horizon planning and plan adherence, belief tracking
- Scoring: rules
- Agents: many
- Opponents: scripted, LLM, human
- Tests: capability
- Training evaluated: prompting (plan / replan module ablation)
- Transfer between skills measured: no
- Models tested: GPT-3.5-Turbo-1106, GPT-4-0613, GPT-4-Turbo-1106, Gemini 1.0 Pro, Mistral-7B-Instruct-v0.2, Mixtral-8x7B, LLaMA-2-13b, rule bidder, 4 humans
- Code released: project page https://auction-arena.github.io (no repository named in the paper)
