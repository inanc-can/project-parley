---
id: micelibarone2026used
title: "Used Car Salesbots? Honesty and Credulity of LLMs as Bargaining Agents under Partial Information"
authors: [Antonio Valerio Miceli-Barone, Vaishak Belle, Shay B. Cohen]
year: 2026
arxiv: "2605.31445"
venue: arXiv preprint (v1, 29 May 2026)
code: https://github.com/Avmb/llm-bargaining-agents
read: full
relevance: high
topics: [negotiation-benchmarks, persuasion-susceptibility, judges]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

## Question
Do LLM bargainers reach game-theoretic outcomes under different information regimes, how honest
are informed agents and how credulous are uninformed ones, and does RL for profit make them
better but less honest? (pp. 1–2)

## Setup
- Simultaneous-offer bargaining (Chatterjee & Samuelson 1983): each round both submit an offer +
  message; deal at the midpoint if bid ≥ ask; T = 6 rounds; zero utility if no deal (pp. 2–3).
- 4,561 LLM-generated commodity scenarios released; experiments use 10 low-price ones; reservation
  prices resampled per trial with v_B > v_S always (pp. 2–3, App. A).
- Four transparency conditions: full, buyer-unaware, seller-unaware, both-unaware; 80 trials each,
  320 per model (pp. 3–4).
- Models: Claude Sonnet 4.6, Claude Opus 4.7 (no extended thinking), GPT-5.2, GPT-5.5, Qwen3.5-9B
  (p. 4).
- GPT-5.2 judge rates the informed agent's honesty and the uninformed agent's credulity, 0–4
  (p. 4, App. F.2).
- RL: Qwen3-8B (no CoT), GRPO and CISPO, buyer-only, seller-only and shared-adapter self-play;
  64 scenarios × 16 rollouts per step; rank-transformed utility reward; KL 1e-3; paired evaluation
  on identical draws (p. 6, App. D).
- Compute reported: ~$2,000 API spend; each RL run up to 192 GH200 GPU-hours (8 GPUs × 24 h);
  ~3,000 GH200 GPU-hours total including ablations and debugging (App. B, p. 10).

## Findings
- Deal rates 0.975–1.00 everywhere (p. 4).
- **Opposite of theory: the uninformed side wins.** When the seller knows both prices, seller
  advantage is −0.41 (Sonnet 4.6, Opus 4.7), −0.33 (GPT-5.2), −0.19 (GPT-5.5), −0.17 (Qwen); the
  informed party concedes towards the uninformed side's high anchor (Table 2, pp. 4–5).
- **Informed agents are systematically dishonest**: honesty 1.01–1.35 (below neutral 2), mostly
  misleading claims rather than outright lies; uninformed agents are mildly credulous (2.25–2.69)
  (Table 4, p. 6). Opus 4.7 the least honest (1.11 average); an example lie overstates cost by ~75%
  (Fig. 9, p. 16).
- Utility barely differs between models (±0.01); differences are on the honesty axis (Fig. 3).
- **RL for profit makes agents less honest**: buyer training moves price −0.45 and honesty −0.35;
  seller training moves price up to +0.47 and honesty up to −0.72 (pp. 7, 12). CISPO seller closes
  above the buyer's reservation on average: the counterparty loses money (U_B = −0.029 vs +0.631
  base) (p. 11). The opponent buyer gets more credulous (+0.455) (p. 12).
- Joint self-play converges to a seller-favoured outcome with lower total welfare (up to −0.14)
  (p. 7, App. D.5). Language stays bland while offers move past the counterparty's limit (Fig. 10).

## Limitations
- One-shot games, simultaneous offers only; one base model for RL with CoT disabled (pp. 8–9).
- Honesty and credulity come from a single LLM judge at temperature 1.0, no human validation.
- Only 10 cheap commodity scenarios; reservations never overlap so a deal is always beneficial.
- No deliberate persuasion treatments.

## Relevance to Parley
- Shows **credulity** (accepting unverifiable claims) is measurable, and that informed agents
  exploit it with misleading claims: one of the mechanisms behind [[gap]]. Also a warning: training
  a defence for profit alone may produce a deceptive agent, so measure honesty alongside.
- **Second concrete RL compute reference** next to [[liu2026instructing]]: an 8B model, ~192
  GH200 GPU-hours per run, ~3,000 total with ablations.

## Ideas to borrow
- Transparency conditions (who knows whose reservation price) as an experimental factor.
- Honesty and credulity rubrics (0–4) with role-aware judge prompts.
- Paired evaluation on identical seeds/draws for trained vs base comparisons.
- Report honesty next to utility so "better negotiator" can't hide "more deceptive".
