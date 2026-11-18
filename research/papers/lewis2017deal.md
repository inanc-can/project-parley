---
id: lewis2017deal
title: "Deal or No Deal? End-to-End Learning for Negotiation Dialogues"
authors: [Mike Lewis, Denis Yarats, Yann N. Dauphin, Devi Parikh, Dhruv Batra]
year: 2017
venue: EMNLP 2017
arxiv: "1706.05125"
code: code/deal-or-no-deal
read: full
relevance: medium
topics: [negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 11 pages (arXiv v1, main text pp. 1–9, references pp. 9–11) on 2026-11-15. Metadata
checked with `scripts/arxiv.py`. The venue comes from the paper itself: it thanks "the anonymous
EMNLP reviewers" (p. 9). The code is the paper's repo, facebookresearch/end-to-end-negotiator
(p. 1, footnote 1), pinned as `code/deal-or-no-deal`. This is a **pre-LLM** paper: the agents are
small GRU sequence-to-sequence models trained from scratch.

## Question
Can one neural model learn to negotiate in free natural language end to end, with no annotated
dialogue states, by imitating human dialogues? And does it negotiate better if it is trained
(RL) or decodes (rollout planning) to maximise its own reward instead of likelihood? (pp. 1–2)

## Setup
- **Task** (multi-issue bargaining, after DeVault et al. 2015) (p. 2): two agents see the same pool
  of 5–7 items of 3 types (books, hats, balls) and each gets a private random value function.
  Constraints: each agent's items are worth 10 in total; every item is worth something to at least
  one agent; some items are worth something to both, so both cannot get the maximum. Agents take
  turns sending messages or selecting that a deal is reached; then **each agent separately writes
  down the deal**, and if the two versions differ both get 0. After 10 turns they may end with no
  deal, worth 0 to both.
- **Data** (pp. 2–3): Amazon Mechanical Turk, US workers only, $0.15 per dialogue plus a $0.05 bonus
  for a maximum score. 5,808 dialogues on 2,236 scenarios; 252 scenarios (526 dialogues) held out as
  the test set. Human–human statistics (Table 2, p. 7): 6.6 turns per dialogue, 7.6 words per turn,
  80.1% agreed, average score 6.0/10, 76.9% of deals Pareto-optimal.
- **Model** (pp. 3–4, 6): GRU seq2seq conditioned on the agent's goals; it predicts **both** sides'
  words (so it can serve as a model of the partner), plus an attention classifier that outputs the
  final split. Small: 64-dim goal and 256-dim word embeddings, 128-unit dialogue GRU, no
  pre-training.
- **Four systems** (p. 6): LIKELIHOOD (supervised imitation), RL (REINFORCE fine-tuning on the deal
  score, discount 0.95, one supervised update after every 4 RL updates, 4,086 simulated dialogues),
  ROLLOUTS (supervised model + decoding that samples 10 candidate turns and simulates 5 complete
  continuations of each to estimate expected reward), and RL + ROLLOUTS.
- **"Self-play" here is not two learning agents**: the RL agent practises against a *fixed* copy of
  the supervised model, because updating both agents made their language drift away from English
  (p. 4).
- **Evaluation** (p. 6): on held-out scenarios, against the LIKELIHOOD model and against MTurk
  humans. Humans were told they were talking to other humans, and "few appeared to realize" they
  were not (p. 6). Metrics: score out of 10 (all dialogues, no-deal = 0, and agreed only),
  agreement rate, Pareto optimality of agreed deals.

## Findings
- **Against the LIKELIHOOD model** (Table 1, p. 7): score (all) LIKELIHOOD 5.4 vs 5.5, RL 7.1 vs 4.2,
  ROLLOUTS 7.3 vs 5.1, RL + ROLLOUTS 8.3 vs 4.2; agreement 87.9 → 94.4%; Pareto-optimal deals
  49.6 → 74.8%.
- **Against humans** (Table 1, p. 7): score (all) LIKELIHOOD 4.7 vs 5.8, RL 4.3 vs 5.0, ROLLOUTS
  5.2 vs 5.4, RL + ROLLOUTS 4.6 vs 4.2. Agreement **falls** from 76.5% (LIKELIHOOD) to 67.3% (RL) and
  57.2% (RL + ROLLOUTS); score on agreed deals rises from 6.2 to 8.0; Pareto-optimal deals rise from
  66.2 to 82.4%. RL + ROLLOUTS is the only system that beats its human partner on score (all).
- So the claim that RL agents "outperform their supervised counterparts in negotiations with
  humans" (p. 1) holds on **agreed deals only** (6.4 vs 6.2): on score (all), RL alone scores *less*
  than LIKELIHOOD (4.3 vs 4.7), and so does RL + ROLLOUTS (4.6). The best absolute score against
  humans is ROLLOUTS (5.2) (Table 1, p. 7). The paper says "significantly" but reports no test, no
  confidence intervals and no number of human dialogues per system.
- **Goal-based agents negotiate harder and lose deals** (p. 7): RL + ROLLOUTS dialogues with humans
  last 7.2 turns vs 5.3 for LIKELIHOOD; people often walked away with 0 rather than give in to an
  uncompromising partner; the models tend to repeat the same demand every turn, which works far
  better against the LIKELIHOOD model than against humans. The training partner does not model
  human walk-aways.
- **Imitation makes soft negotiators**: models trained only to imitate humans are "overly willing to
  compromise" (p. 1); LIKELIHOOD has the most human-like language (test perplexity 5.47 vs 5.86 for
  RL; Table 3, p. 7).
- **Deception appears without being designed** (p. 7; Fig. 7, p. 8): "numerous cases" of the model
  feigning interest in an item worth 0 to it and later conceding it. Evidence is example dialogues
  only, with no count or rate.
- 76% of LIKELIHOOD messages in self-play are copied verbatim from the training data (p. 7).
  RL + ROLLOUTS often starts a message with "Deal"/"I agree" and then makes a counter-offer, which
  frustrated humans (p. 8).

## Limitations
- Pre-LLM: small GRU models with no pre-training; the paper's strategies and failure modes are
  those of reward hacking against a weak, fixed partner, not those of current LLMs.
- One task with tiny action space (3 item types, ≤7 items), symmetric values summing to 10.
  It generalises only to held-out *scenarios* of the same task; transfer to other negotiation
  domains is named as future work (p. 9).
- Human evaluation: no significance tests or sample sizes per condition; participants were deceived
  about talking to a machine; MTurk pay is $0.15 per dialogue, so human stakes are small.
- The human–human statistics (Table 2) are over the whole dataset, while model results are on
  held-out scenarios, so the two are not exactly comparable.
- The deception finding is anecdotal.
- Old PyTorch code: use it for the data and the task definition, not to run.

## Relevance to Parley
- Parley's multi-issue trade template follows this setup, so the 5,808 human dialogues are a
  **human baseline** for that game (agreement 80.1%, score 6.0/10, 76.9% Pareto-optimal; Table 2,
  p. 7), but only if Parley keeps the same constraints (3 types, 5–7 items, values summing to 10,
  10-turn walk-away, separate deal write-down).
- It is the original evidence for a trade-off that newer LLM work keeps finding: optimising for own
  score raises the value of deals won but lowers how often a deal is reached with humans. Parley
  should always report agreement rate, score on agreed deals, score over all dialogues and joint
  efficiency together, as [[zhang2026terms]] argues for LLM negotiators.
- Its RL against a fixed partner is the early version of what [[liu2025spiral]] and
  [[yuan2025marshal]] do with LLM self-play; MARSHAL also finds that fixed-opponent training
  overfits. Lewis et al. show the same overfitting toward the training partner (larger gains against
  LIKELIHOOD than against humans, p. 7).
- Among LLM benchmarks ([[bianchi2024negotiationarena]], [[abdelnabi2023cooperation]]), this paper
  is the source of a human–human dataset for the item-splitting game. [[he2026socialgym]]'s bargaining game uses structured offers with no free text, so it
  cannot reuse these dialogues.

## Ideas to borrow
- The **separate deal write-down** (both agents state the deal; mismatch = 0) as a cheap, rule-based
  check that an agreement was really reached and understood.
- Report the four numbers together: score (all), score (agreed), agreement rate, Pareto optimality.
- Use humans or a human-like imitation model as **held-out partners** for any RL-trained Parley
  agent, since gains against the training partner overstate gains against people.
- Count tactics such as feigned interest in zero-value items with a rule (asks for an item worth 0
  to oneself, then concedes it) instead of reporting examples.

## Map fields
- Skills measured: negotiating value (deceiving appears only as anecdotes).
- Scoring: rules (points from the private value functions, agreement check), plus perplexity for
  language quality.
- Agents: 2.
- Opponents: learned agents (the fixed supervised LIKELIHOOD model) and human (MTurk).
- What it tests: capability.
- Training evaluated: SFT (supervised imitation) and RL (REINFORCE against a fixed partner), plus
  planning at decoding time (rollouts).
- Transfer measured: no (only held-out scenarios of the same task).
- Models tested: GRU seq2seq models trained from scratch (LIKELIHOOD, RL, ROLLOUTS, RL + ROLLOUTS).
- Code released: https://github.com/facebookresearch/end-to-end-negotiator
