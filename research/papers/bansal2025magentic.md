---
id: bansal2025magentic
title: "Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets"
authors: [Gagan Bansal, Wenyue Hua, Zezhou Huang, Adam Fourney, Amanda Swearngin, Will Epperson, Tyler Payne, Jake M. Hofman, Brendan Lucier, Chinmay Singh, Markus Mobius, Akshay Nambi, Archana Yadav, Kevin Gao, David M. Rothschild, Aleksandrs Slivkins, Daniel G. Goldstein, Hussein Mozannar, Nicole Immorlica, Maya Murad, Matthew Vogel, Subbarao Kambhampati, Eric Horvitz, Saleema Amershi]
year: 2025
arxiv: "2510.25779"
venue: arXiv preprint (v1, 27 Oct 2025)
code: https://github.com/microsoft/multi-agent-marketplace
read: full
relevance: medium
topics: [negotiation-benchmarks, persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: natural
  players: many
  stakes: payoff
  persuasion_treatment: true
  human_baseline: false
---

Read all 19 pages on 2026-11-15. Microsoft (with Arizona State). Most results are only in
figures (Figs. 4–9); the numbers below are those stated in the text. Agents act asynchronously
through a REST API, so `turn_protocol: natural` is approximate. Sonnet-4, Sonnet-4.5 and
Qwen3-4B-2507 appear in the results but not in the model list on p. 8.

## Question
How do LLM agents behave in a two-sided market where Assistant agents (for consumers) search,
talk to and pay Service agents (for businesses)? Do they reach good welfare, how does search
quality and the number of options affect them, can businesses manipulate them, and what biases
do they show? (pp. 1–2, 6)

## Setup
- **Environment** (§3, pp. 4–6): HTTP/REST server with three endpoints (register, protocol
  discovery, action); five actions — search, send text, send order proposal (items + prices),
  send payment (accepts a proposal), receive. Assistants search, message and pay; Services reply
  with text and proposals (Table 1, p. 7; Fig. 2–3). Services keep private catalogs; assistants
  do not know who can serve them or prices; services do not know budgets (p. 4).
- **Data** (§4.1, pp. 7–8): fully synthetic; two domains, Mexican restaurants and contractors.
  Each customer wants 1–3 items and 1–2 amenities with target prices; K candidate businesses per
  customer, only some satisfy all constraints. Scales: small (33 customers, 99 businesses) and
  medium (100, 300); results shown for 100–300.
- **Metric** (§4.2, p. 8): all-or-nothing fit; consumer utility U = V × Fit − Price, with V = 2 ×
  average price of the desired items; consumer welfare = sum of utilities. Rule-computed.
- **Conditions** (Table 2, p. 9): baselines Random-with-items, Cheapest-with-items-and-prices,
  Random-with-items-and-amenities, Optimal; agentic Perfect search (top 3 matching businesses
  given) and Lexical search (agent writes queries, paginated lists of 10).
- **Experiments**: welfare (§5.1), consideration set size 3 → 100 results (§5.2), six
  manipulation strategies embedded in business descriptions — authority, social proof, loss
  aversion, basic and strong prompt injection, plus control (Table 3, p. 12; §5.3), and position
  and proposal-order bias with three identical businesses (§5.4).
- **Models**: GPT-4o, GPT-4.1, GPT-5, Gemini-2.5-Flash, GPT-OSS-20b, Qwen3-14b (YaRN to 131k
  context) (p. 8), plus Sonnet-4/4.5 and Qwen3-4B-2507 in the results. 5 runs each, mean ± SD.
  ReAct-style agents (p. 10). The text does not say which model runs the Service agents.

## Findings
- **Welfare**: under Lexical search, Sonnet-4, Sonnet-4.5, GPT-5, GPT-4.1, GPT-4o and
  Gemini-2.5-Flash beat two of three baselines (random among item matches; cheapest without
  amenity info); under Perfect search GPT-4.1 and Gemini-2.5-Flash come "very close to the
  optimal" and beat random among full matches (pp. 9–10; Fig. 4). Open models drop sharply under
  lexical search; Qwen3-14b is poor in both, with premature termination, role confusion and
  over-buying (p. 10).
- **More options, lower welfare**: going from 3 to 100 search results lowers welfare by 4.3%
  for GPT-4o, 44% for GPT-5 (minimal reasoning) and 65.4% for Sonnet-4 (Mexican 100–300)
  (p. 11; Fig. 5). Most models contact only a few businesses whatever the set size; only
  Gemini-2.5-Flash contacts all, and contacting more does not help (p. 11; Fig. 6).
- **Manipulation**: GPT-4.1, Sonnet-4.5 and Gemini-2.5-Flash keep mean payments to the
  manipulating business under 1.0 of 3.0; Sonnet-4.5 shows "virtually no susceptibility";
  Gemini-2.5-Flash rises to 1.6 under strong prompt injection (restaurants) (p. 12; Fig. 7).
  GPT-4o, GPT-OSS-20B and Qwen3-4B-2507 are vulnerable to injection (often all payments
  redirected) and to authority and social-proof claims (p. 13).
- **Position bias** is small for frontier models; Qwen3-4B picks the third-listed business
  57.1% (restaurants) and 66.7% (contractors) of the time (p. 13; Fig. 8).
- **First-proposal bias is universal**: first proposals are selected 60–100% of the time,
  third ones near 0 — a 10–30× advantage for answering first; GPT-4o and Sonnet-4.5 reach 100%
  first-proposal selection in some conditions; even GPT-4.1 (contractors) picks first 60% vs
  third 13.3% (pp. 13–14; Fig. 9).

## Limitations
- **Little negotiation**: prices come from catalogs and the paper reports no haggling results;
  "negotiation" here is inquiry plus accepting an order proposal. Persuasion is one-way (static
  text in business descriptions), not conversational.
- Synthetic data in two domains; static one-shot markets with no learning or repeated play
  (p. 14).
- Most numbers are in figures only; Service-agent model and prompts are not described in the text;
  model list and result models differ.
- Welfare is consumer welfare only; business profit and market-level efficiency beyond the
  consumer side are not reported.
- No training; no humans; ReAct-style baselines only.

## Relevance to Parley
- **For the map (a)**: a many-agent, rule-scored market benchmark that covers a skill the
  dyadic negotiation benchmarks do not: **delegated search and choice under competition** —
  discovery, comparison, and resisting manipulation at scale. Its manipulation grid (authority,
  social proof, loss aversion, injection) is a clean [[persuasion-susceptibility]] probe with a
  payoff-based outcome (payments to the manipulator), unlike the judge-based measures in
  [[jose2026agents]]. It extends the consumer-market line of [[zhu2025automated]] and
  [[liu2026agenticpay]] from pairs to 100 × 300 markets.
- **For the transfer study (b)**: nothing is trained; models differ in architecture and
  vendor, so the paper cannot say whether e.g. negotiation training would change manipulation
  resistance. It does supply two **propensity-like** measures that a training study could track
  as possible side effects: first-proposal satisficing and manipulation-driven payments. A
  hypothesis for (b): training an agent to close deals (e.g. RL on deal rate as in
  [[liu2025spiral]]-style self-play) may worsen first-proposal bias; training on persuasion
  ([[sadab2026receiver]]) may change susceptibility.
- Compared with [[he2026socialgym]] and [[leibo2021meltingpot]]: also many agents, but with an
  economic welfare metric and an optimal benchmark instead of Elo; welfare relative to "Optimal"
  is the kind of absolute score SocialGym lacks. Compared with [[vaccaro2025advancing]]: both
  report prompt injection between agents; here it is a planned treatment with a control.

## Ideas to borrow
- **Welfare vs Optimal plus information-limited baselines** (Table 2): locate whether a failure
  is in search, information, or decision.
- **Consideration-set sweep** as a stress test: more options should not reduce welfare.
- **Proposal-order and position bias probes** with identical offers in rotated order.
- **Manipulation grid with payment outcome** (Table 3) as a reusable susceptibility test.
- Protocol discovery endpoint (actions added without breaking agents) as a design for Parley's
  own environment.

## Map fields
- Skills measured: other (delegated search, comparison and purchase choice in a two-sided market), resisting persuasion (authority, social proof, loss aversion, prompt injection), negotiating value (only light inquiry and order proposals)
- Scoring: rules (consumer utility/welfare, payments to manipulators, selection rates)
- Agents: many (100 customers × 300 businesses; 33 × 99)
- Opponents: LLM (Service agents; model not stated in the text); manipulation via fixed text
- Tests: both (capability: welfare; propensity-like: first-proposal and position bias, susceptibility)
- Training evaluated: none
- Transfer between skills measured: no
- Models tested: GPT-4o, GPT-4.1, GPT-5, Gemini-2.5-Flash, GPT-OSS-20b, Qwen3-14b; also Sonnet-4, Sonnet-4.5, Qwen3-4B-2507 in results
- Code released: https://github.com/microsoft/multi-agent-marketplace
