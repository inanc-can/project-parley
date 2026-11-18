---
id: liu2026instructing
title: "Instructing LLMs to Negotiate using Reinforcement Learning with Verifiable Rewards"
authors: [Shuze Daniel Liu, Claire Chen, Jiabao Sean Xiao, Lei Lei, Yuheng Zhang, Yisong Yue, David Simchi-Levi]
year: 2026
arxiv: "2604.09855"
venue: arXiv preprint (v1, 10 Apr 2026)
code: not stated
read: full
relevance: high
topics: [negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: true
  human_baseline: false
---

## Question
Can RL with verifiable rewards (surplus + budget adherence) teach an LLM buyer to negotiate, and
what strategies emerge? (pp. 1–2)

## Setup
- Buyer agent vs a "regulated" LLM seller (Qwen3-30B-A3B-Instruct) whose cost constraint is
  enforced by the environment, so the buyer can't exploit hallucinated concessions (p. 4).
- AmazonHistoryPrice (Xia et al. 2024): 930 products, 802 train / 128 test; buyer budget B and
  seller cost C per item; includes infeasible cases (B < C) (pp. 5, 15).
- Structured output: hidden reasoning, dialogue, action tag ([BUY]/[DEAL]/[REJECT]/[QUIT]) (p. 4).
- **Reward** = (B − P_final)/|B − C| clipped to [−1, 1]; 0 for no deal; −1 for proposing above budget
  or bad format (pp. 4–5).
- **Training**: GRPO on Qwen3-30B-A3B-Instruct via Thinking Machines' Tinker service (compute from
  a Tinker research grant); 60 iterations × 64 products × 8 rollouts = 512 episodes per iteration;
  max 6 turns; KL penalty 0; LR 3e-5 (App. A.2, p. 14; p. 10).
- Evaluation: 128 test items × 4 rollouts vs default seller, vs unseen GPT-5.4-high seller, and vs
  three adversarial seller personas (begging, insulting, unyielding) (pp. 8–10, App. C.3).

## Findings
- **Four training phases**: aggressive lowballing → deadlock (deal rate collapses) → rational
  concession → "advanced persuasion" with ~90% deal rate (pp. 6–7).
- Budget overshoot driven to ~0 within a few iterations by the −1 penalty (p. 7).
- Held-out: trained 30B reward 0.766 vs GPT-5.4-high 0.402, Kimi-K2-Thinking 0.342; bargained
  ratio 0.839 vs 0.438; untrained base 0.013 with 10.35% budget overshoot (Table 1, p. 8).
- Vs unseen GPT-5.4-high seller: 0.408 vs 0.182 for GPT-5.4-high as buyer (Table 2, p. 9).
- **Robustness to manipulative personas** (Table 3, p. 10): begging 0.695 vs 0.380 (GPT-5.4-high);
  insulting 0.499 vs 0.126; unyielding 0.117 vs −0.001. Frontier models show "artificial empathy"
  against begging. Untrained base under insulting persona overshoots budget 18.95%, Llama-3.3-70B
  36.91% (App. D.3).

## Limitations
- One seller model in training (same family as the buyer); persona robustness is a side
  evaluation, not a training target; only three crude personas.
- The trained buyer's "persuasion" includes pressure lines ("I can go no higher") that may be
  bluffs; honesty isn't measured.
- No seeds/variance across training runs reported; code not stated.
- Gains vs frontier models partly reflect frontier models' tendency to close deals near budget.

## Relevance to Parley
- **Best existing evidence on RL feasibility and cost for a negotiation thesis**: 30B MoE model,
  60 GRPO iterations, ~30k episodes, run on a rented training service (Tinker). Use as the
  reference point for compute planning.
- **Closest to the "defence" extension of [[gap]]**: RL with a money reward already makes a buyer
  robust to begging/insulting/stubborn sellers. A persuasion-defence thesis must go beyond this:
  deliberate tactics (authority, scarcity, false evidence, information extraction), loyalty to a
  principal's limit, and comparing prompting vs fine-tuning vs RL on the same tactics.
- Author David Simchi-Levi ([[simchi-levi]]).

## Ideas to borrow
- Reward (B − P)/|B − C| with a −1 penalty for violating the principal's limit; include infeasible
  episodes so walking away is learned.
- Environment-enforced constraints on the opponent so the policy can't exploit hallucinations.
- Track first-offer ratio, deal ratio and overshoot during training to see strategy phases.
- Persona prompts as a cheap adversarial test set.
