---
id: liang2026agents
title: "When LLM Agents Negotiate: Private Information and Dynamic Bargaining in Supply Chains"
authors: [Chen Liang, Fasheng Xu]
year: 2026
arxiv: "2608.07538"
venue: arXiv preprint (v1, 29 Jul 2026)
code: none stated in the PDF
read: partial
relevance: medium
topics: [negotiation-benchmarks, game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read: main paper pp. 1–31 in full (incl. limitations); from the online appendix only A (prompts,
pp. ec1–ec4), C.1 (example transcript), C.4–C.6 (disclosure and public–private divergence,
pp. ec19–ec22) and the section headings of B, D, E. The other ~35 appendix pages (detail tables,
robustness extensions, PBE derivation) are unread. Studied 2026-11-14.

## Question
When firms delegate procurement bargaining to LLM agents, do the agents create value, divide it
predictably and avoid loss-making contracts, measured against a Perfect Bayesian Equilibrium? And
which of the firm's choices (capability tier, provider, prompt configuration) move outcomes?
(pp. 1–5)

## Setup
- Two business-school authors (UConn), operations-management framing (vendor choice, guardrails).
- Game: Feng et al. (2015) supply-chain bargaining. Buyer privately knows its demand type
  (High µ = 80 / Low µ = 40); uninformed seller (cost c = 30, retail r = 60, prior 0.5). They
  alternate offers on a (quantity, total payment) contract, max 10 rounds, outside options 0
  (pp. 9–10). Each turn: public offer + message, private reasoning in JSON (pp. ec1–ec4).
- Prompts disclose all primitives (payoff formulas, discount factors, priors) but not the
  equilibrium strategy; both agents are told "You cannot accept if π < 0" (pp. 8–10, ec1).
- 2×2×4 factorial: buyer type × first proposer × patience (δB, δS) ∈ {(0.9,0.9), (0.7,0.9),
  (0.4,0.9), (0.9,0.4)}, 15 reps (Table 1, p. 9).
- Nine models, three providers × three tiers: GPT-5.2 / GPT-5-mini / GPT-4o-mini; Gemini-3-Pro /
  3-Flash / 2.5-Flash; Qwen3-Max / Qwen3-32B / Qwen2.5-14B. Temperature 1.0 (Table 2, pp. 9–10).
- 9,840 negotiations: self-play (2,160), cross-family flagship pairs (1,440), within-family
  cross-tier (480), plus extensions R1 numbers-only, R2 no discounting, R3 strategic patience,
  R4 reasoning effort, R5 retail price, R6 prior, R7 model size (Table 3, p. 13).
- Deal terms extracted by GPT-4o-mini with a rule-based fallback; a second extractor (Claude Sonnet
  4.6) on 300 cases agreed on deal status in 100% (p. 10, fn. 5). Benchmark = executable PBE,
  1.25 rounds on average (p. 12).

## Findings
- **Efficient but slow**: 98.9% agreement, 95.4% of first-best surplus undiscounted, but 2.98
  rounds vs 1.25 benchmark; discounted efficiency 66.2% vs 96.4% (Table 4, p. 14). Capability
  explains ~66% of explained efficiency variance (Shapley), patience 90% of buyer-share variance
  (Table 5, p. 19).
- **Breaking the principal's limit**: irrational (negative-profit) agreements in 0.0% flagship,
  0.6% mid-tier, 19.2% baseline; 97.1% involve a baseline model. GPT-4o-mini 36.2%, Qwen2.5-14B
  20.0%, reasoning baseline Gemini-2.5-Flash 2.9% (pp. 16–17, Fig. 2). Buyers 5.1% vs sellers 1.4%;
  79% of cases are revenue miscalculation, 21% cost miscalculation (p. 17). So in this setting the
  breaches look like arithmetic/constraint-checking failures, not persuasion.
- **Provider, not capability, decides who gets the surplus**: self-play buyer share OpenAI 40%,
  Google 50%, Qwen 70% (Qwen3-Max 91.4%) (Table 6, p. 20). Cross-family: Gemini-3-Pro gets 66.7%
  as buyer, Qwen3-Max keeps only 27.3% as seller; reversing roles swings 7–18 pp (pp. 22–23).
  Within a family the stronger model wins: GPT-5.2 seller profit $931 vs $680 (p. 19).
- **Compression toward 50/50**: when theory gives the buyer ~13%, LLM buyers get 40.2%; when it
  gives ~91%, they get 70.9% (p. 21).
- **Language does strategic work but is not the whole story**: removing messages (numbers only)
  lowers agreement 98.9 → 96.4% and efficiency 95.4 → 92.8%, shifts GPT-5-mini buyer share
  41.9 → 51.3%, but provider orderings persist (pp. 24–25).
- **Prompted patience is a lever**: tuning the agent's announced discount factor away from the
  principal's true one gains +74.8 payoff units on average for buyers (p. 27, Table 7 p. 28).
- **Public–private divergence (LLM-classified, Claude Haiku 4.5)**: fairness appeals paired with
  self-interested private reasoning in 56.5% of 13,023 turns, profit hiding 14.1%, false constraint
  9.4%, false finality 0.7% (Table EC.16, p. ec21). Outright deceptive type claims are rare
  (High-type 4.0%, Low-type 1.4%, Table EC.15, p. ec20). Authors call these exploratory, not
  validated deception rates (p. ec20).

## Limitations
- Self-play and LLM-vs-LLM only; no humans, no deliberate persuasion or adversarial counterparty.
- Patience is common knowledge; real urgency is usually hidden (p. 30).
- Role-specific prompts, so shares are "under a common prompting regime", not intrinsic biases
  (p. 30). No Anthropic models (p. 9).
- Process claims (heuristic substitution, mimicking) are descriptive, not mechanistic (p. 30);
  tactic labels come from one LLM classifier without human validation.
- Payoffs are abstract units, not real money; no compute/cost figures reported.

## Relevance to Parley
- **Context for [[gap]], neither strengthens nor weakens the persuasion claim directly.** It
  confirms delegated agents break an explicit "never accept negative profit" rule (19.2% for
  non-reasoning baselines, ~0% for reasoning models, p. 17) with no persuasion at all, the same
  baseline harm as [[zhu2025automated]] and [[erdogan2026should]]. But it narrows the claim in one
  way: for current reasoning models the no-pressure breach rate is ~0, so any limit breaches
  Parley finds with frontier models would be attributable to the counterpart's tactics rather than
  arithmetic, which makes the persuasion question cleaner.
- Unlike [[li2026whose]] it measures harm in payoff and has a theory benchmark, but there is no
  adversary and no tactic treatment. Unlike [[liu2026instructing]] and [[micelibarone2026used]]
  there is no training.
- The **provider-identity** result (who you face matters more than how strong you are) parallels
  [[sadab2026receiver]] (target identity explains most variance): persuasion resistance may also be
  a provider profile. Parley should cross providers, not just tiers.
- The public–private divergence coding (fairness mismatch, false constraint, false finality) is
  a ready taxonomy for tactics agents already use spontaneously, a natural source for scripted
  tactic treatments, and pairs with the honesty concern in [[micelibarone2026used]].
- Fits the chair's game-theory framing ([[bichler2026model]]): an equilibrium-referenced audit is
  the kind of baseline a TUM proposal should include.

## Ideas to borrow
- Equilibrium benchmark as the "rational" reference for concessions, so harm = deviation from it.
- Split outcomes into efficiency (created value), division (who captured it) and reliability
  (limit breaches), and decompose with Shapley R².
- Numbers-only control arm (R1) to isolate what the language channel does: directly usable to
  separate persuasion from offers.
- Public vs private reasoning fields in each turn, then code divergence (said fair, thought greedy).
- A second-family extractor to validate LLM parsing of deal terms.
