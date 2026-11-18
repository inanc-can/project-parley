---
id: zhu2025automated
title: "The Automated but Risky Game: Modeling and Benchmarking Agent-to-Agent Negotiations and Transactions in Consumer Markets"
authors: [Shenzhe Zhu, Jiao Sun, Yi Nian, Tobin South, Alex Pentland, Jiaxin Pei]
year: 2025
arxiv: "2506.00073"
venue: arXiv preprint (v4, 20 Sep 2025)
code: https://github.com/ShenzheZhu/A2A-NT
read: full
relevance: high
topics: [negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

## Question
When both consumers and merchants delegate negotiation to LLM agents, do model differences
produce unequal deals, and what risks to the principals arise? (p. 1)

## Setup
- Buyer agent with a user budget β vs seller agent knowing the wholesale cost; both see retail
  price. Buyer opens; up to 30 rounds; GPT-4o extracts prices and judges accept/reject/continue
  (pp. 2–3, App. E).
- 100 real products (vehicles, electronics, real estate); retail prices collected, wholesale
  costs **estimated by GPT-4o** (p. 3, App. C).
- Five budget levels from 0.8 × wholesale (infeasible) to 1.2 × retail (Table 1, p. 3); 50
  products × 5 budgets; nine models in all buyer–seller pairings incl. self-play (p. 3).
- Metrics: price reduction rate, relative profit, deal rate; risk metrics: out-of-budget rate,
  out-of-wholesale rate, overpayment rate, deadlock rate (pp. 3–4, App. D).
- Mitigation: an online multi-armed bandit over 96 prompt variants for Qwen2.5-7B (pp. 6–7, App. G).

## Findings
- Capability gaps: o3 strongest overall; GPT-3.5 weakest; most sellers earn ~9.6× GPT-3.5's
  profit, GPT-4.1 13.3×, DeepSeek-R1 12× (p. 3). Negotiation score correlates with MMLU at
  r = 0.93, with parameter count only r = 0.53 (p. 4).
- **Principal-limit violations:** out-of-budget acceptance 11.76% (Qwen2.5-7B), 6.25% (GPT-3.5),
  2.98% (o4-mini), 0.36% (GPT-4o-mini); below-wholesale up to 7.91% overall and ~18.5% for
  Qwen2.5-7B at low budgets; even o4-mini sometimes sells below cost under extreme price pressure
  (Fig. 5–6, pp. 4–5).
- **Overpayment above retail** happens at high budgets, often after the seller asks for the
  budget and the buyer reveals it despite instructions; the seller anchors to it (p. 5).
- Early settlement: higher budgets → less bargaining, ~9% gap in price reduction (p. 6).
- Strong vs weak pairing: weak sellers earn 6.9–14.1% less, weak buyers pay 1.1–2.1% more
  (Table 3, p. 13). Seller choice matters more than buyer choice (14.9% vs 2.6% range) (p. 13).
- Bandit prompt search cut out-of-budget from 18.4% to 1.3% but didn't reduce overpayment
  (8.1 → 8.3%) or deadlocks (4.0%) (Table 2, p. 7).

## Limitations
- Wholesale costs are LLM-estimated; judge and price extraction by GPT-4o (pp. 3, 11).
- No deliberate persuasion or tactics; violations come from ordinary bargaining pressure.
- Older models (GPT-3.5, Qwen2.5); one prompt per role, deliberately untuned (p. 11).
- The mitigation is preliminary and only for one model (p. 7).

## Relevance to Parley
- Closest prior work on delegated agents losing their principal's money ([[gap]]): budgets broken,
  costs undercut, budgets revealed then exploited. It shows the harm exists without anyone trying
  to persuade; it doesn't treat persuasion tactics as causes. Pentland and Pei ([[pentland]])
  are authors.
- The "reveal budget → seller anchors → overpay" chain is a natural persuasion mechanism to test
  as a controlled treatment (information extraction then exploitation).

## Ideas to borrow
- Budget levels including infeasible ones (budget below cost) to test refusal.
- Risk metrics in money terms: out-of-budget, below-cost, overpayment, deadlock.
- Strong-vs-weak pairings to show who bears the loss.
- Bandit search over prompt components as a cheap defence baseline.
