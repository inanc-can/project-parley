---
id: lyu2026gift
title: "GIFT: Games as Informal Training for Generalizable LLMs"
authors: [Nuoyan Lyu, Bingbing Xu, Xueyun Tian, Weihao Meng, Yige Yuan, Yang Zhang, Zhiyong Huang, Tat-Seng Chua, Huawei Shen]
year: 2026
arxiv: "2601.05633"
venue: arXiv preprint (v2, 3 Jun 2026)
code: https://anonymous.4open.science/r/GIFT-LLM
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 21 pages (main text pp. 1–9, appendices A–F pp. 11–21) on 2026-11-15. Players: Matrix
Games are single-turn 2-player, TicTacToe 2-player, Who's the Spy 4-player; `many` is the maximum.
**Arithmetic caveat**: the 7B "Formal (Math)" row in Table 2 (p. 6) lists Avg 42.00, but its four
columns average 52.51; the 1.5B base row lists 27.10 but averages 21.70. The abstract's headline
"42.00% → 57.39% for 7B" (p. 2) rests on the 42.00 entry; with the corrected value the gain over
math-only is +4.9 and over the untrained base model (53.36) only +4.0. All other Avg cells I checked
match their columns.

## Question
Does adding RL on games ("informal learning") to RL on math ("formal learning") improve general
abilities beyond math-only RL, and does training subtasks in sequence (Coordinated Subtask Training,
CST) integrate heterogeneous RL signals better than mixing them in one batch? (pp. 1–2)

## Setup
- ICT/CAS, UCAS, UW, NUS. RL with GRPO via RAGEN/StarPO* (DAPO, no KL, top-25% variance trajectory
  filter), 250 rollout-update iterations, group size 16, reward 1 win / 0 loss / 0.5 TicTacToe draw,
  format penalty −0.1 (App. B.3 p. 17).
- **Models trained**: Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct (p. 6).
- **Tasks**: Math (MathLv3-5 from SimpleRL-Zoo) as "formal"; three games as "informal" (Table 5,
  p. 12; App. A pp. 11–14):
  - *Matrix Games* (single turn): 9 classic 2×2/3×3 games (Prisoner's Dilemma, Battle of the Sexes,
    Chicken, Stag Hunt, Radio Station, IESDS, Duopoly, "GAME", weakly dominated game), payoffs randomly
    negated and offset ±100. **Success = choosing a Nash-equilibrium action** (App. C.2 p. 17) — so in
    the Prisoner's Dilemma the rewarded move is defection; no cooperation is rewarded.
  - *TicTacToe* vs Qwen3-14B (max 5 turns); success = three in a row.
  - *Who's the Spy* (Undercover): 4 players, 3 civilians + 1 spy, two description rounds then a vote;
    trained model's role and order random; other three seats Qwen3-14B.
- **Settings**: single-task RL on each task; multi-task F + I1 (Math + Matrix), F + I2 (+ TicTacToe),
  F + I3 (+ Spy), each with *mixed* batches or *CST* (cyclic per-task updates; block τ = 4 for 1.5B,
  1 for 7B) (pp. 4–6). CST is motivated by a second-order (Reptile-style) expansion showing that
  sequential updates add a term that increases pairwise gradient inner products (Eq. 3–4 p. 5;
  App. A.4 pp. 14–16).
- **Evaluation** (p. 6; App. C pp. 17–18): MATH500; Matrix (NE rate); TicTacToe and Spy win rate over
  100 games **vs Gemini-2.5-Flash** (a different opponent than in training); "general abilities" Avg =
  mean of MMLU, MMLU-Pro, CommonGen (GPT-4o pairwise judge vs human reference, win-or-tie) and
  SocialIQA. One run per cell, no seeds, no CIs.

## Findings
Transfer is the core of this paper; numbers are base → trained unless noted (Tables 1–2, p. 6).
- **Game → other games, 1.5B**: Matrix training lifts TicTacToe 1 → 34 and Spy 2 → 14; TicTacToe
  training lifts Matrix 7 → 32 and Spy 2 → 21; Spy training lifts Matrix 7 → 21 but **TicTacToe
  1 → 0**. The 1.5B base model scores near zero on all games (Spy 2, TicTacToe 1) and below chance
  on 3-way SocialIQA (27.64), so much of the 1.5B "transfer" is likely learning to answer in format.
- **Game → other games, 7B (base already competent)**: Matrix training **hurts TicTacToe 40 → 23**;
  TicTacToe training helps Matrix 40 → 57 and Spy 25 → 33; Spy training leaves Matrix 43 and
  TicTacToe 38 (≈ base).
- **Game → math**: 1.5B: Matrix 17.2 → 19.2, TicTacToe 22.4, Spy 19.2 MATH500 (math RL: 43.2). 7B:
  Matrix 54.6 → 58.2 (≈ math RL 58.4), Spy 55.6, but **TicTacToe 54.6 → 49.8** (negative).
- **Game → general benchmarks, 7B**: general Avg base 53.36 → Matrix 55.02, TicTacToe 56.26, Spy
  53.95; MMLU-Pro 40.17 → 44.51 (Matrix), 46.35 (TicTacToe). **Spy training does not raise SocialIQA**
  (75.44 → 74.92) even though it is the social game; it raises CommonGen at 1.5B (7.79 → 20.85).
- **Math → everything, negative at 7B**: math-only RL lowers MMLU 71.43 → 66.51, MMLU-Pro 40.17 →
  32.45, TicTacToe 40 → 31, Spy 25 → 18; general Avg 53.36 → 52.51 (table misprints 42.00). At 1.5B
  math-only RL is the best single task for general Avg (38.34) and gives the biggest SocialIQA jump
  (27.64 → 65.92, larger than Spy training's 60.70).
- **Mixing tasks can hurt**: 7B mixed F + I1 general Avg 51.00 and F + I3 mixed 52.99, both **below
  the untrained base (53.36)**; mixed F + I2 drops Spy to 9 (base 25). 1.5B mixed F + I1 33.53 <
  math-only 38.34 (p. 6). In 7B CST F + I3, TicTacToe (a trained task) ends at 36, below base 40.
- **CST vs mixed**: best general Avg 41.13 (1.5B, F + I2 CST) vs 38.49 mixed; 57.39 (7B, F + I3 CST)
  vs 52.99 mixed (+4.4) (p. 7). CST beats task-level advantage normalisation (TaskAdv, from AgentRL):
  1.5B F + I2 41.13 vs 38.24, and TaskAdv collapses MATH to 10.4 (Table 3, p. 7).
- **Informal alone is not enough**: 1.5B I2 (Matrix + TicTacToe, no math) CST 35.47 vs F + I2 CST
  41.13; MMLU 52.35 → 41.16 without math (Table 4, p. 8).
- **Opponent choice**: training TicTacToe vs Qwen3-14B gives 75% (vs Gemini) and Avg 35.00; training
  vs Gemini-2.5-Flash gives 46% and 29.57; Spy 33 vs 38 (Table 6, p. 19). Authors read this as "no
  clear evidence of broad negative transfer" but MATH falls 25.8 → 22.4 with the Qwen opponent.
- **Reference models** (Table 7, p. 20): general Avg GPT-4o 70.78, Gemini-3-Flash 61.82,
  DeepSeek-V3.2 74.49; Matrix NE rate GPT-4o 48, so the trained 1.5B (65) "beats" them on Matrix.

## Limitations
- One run per configuration, 100 evaluation games, no seeds or CIs; differences of 2–5 points are
  read as effects throughout (Tables 1–4). The Avg misprint inflates the headline claim.
- "Social" coverage is one 4-player word game against fixed LLM opponents, and the social transfer
  test is SocialIQA (multiple-choice), which Spy training does not move at 7B.
- Matrix reward = Nash action, so the "strategic" game teaches equilibrium play (defection in PD),
  not cooperation, welfare or negotiation; no free-text bargaining at all.
- Fixed opponents (Qwen3-14B train, Gemini eval); authors leave self-play and adaptive opponents to
  future work (p. 9). Only Qwen2.5 models.
- CommonGen scored by a GPT-4o judge; the gains there are the largest in the paper and the least
  verified.
- Case studies (Figs. 5, 7, 8) are single cherry-picked examples.

## Relevance to Parley
- **A direct, if noisy, transfer matrix**: 4 training tasks × 8 evaluations at two scales, including
  a cooperative/social game, a zero-sum game and normal-form games — the shape of study (b) wants.
  It shows **both positive and negative transfer depending on the pair and the scale**: Matrix →
  TicTacToe +33 at 1.5B but −17 at 7B; math RL helps 1.5B broadly but hurts 7B on MMLU-Pro (−7.7) and
  both games. That is evidence that transfer/interference between "skills" is real and
  scale-dependent, and that weak base models make transfer look larger (format learning).
- **Multi-task interference is the paper's motivation**: naive mixing pushed 7B general ability below
  the untrained base, and the fix (CST) is an optimisation trick, not a skill account. For (b), the
  harness question ("does joint training of several social skills interfere?") has a concrete
  baseline here: mixed vs sequential vs task-normalised RL.
- **What it leaves open for (b)**: no negotiation, persuasion, deception-detection or propensity
  measures; cooperation is never rewarded (NE in PD); no prompting or SFT arm to compare against RL;
  no multi-agent self-play training; social transfer only to SocialIQA. Compare [[liu2025spiral]]
  (RL self-play on zero-sum games, transfer to math) — GIFT is the same "games → general" story with
  fixed opponents and a multi-task twist; and [[ramesh2026sparks]] (cooperative Hanabi RL → group
  guessing, +12) which covers the cooperative side GIFT lacks. [[he2026socialgym]] shows the families
  GIFT would need for a real social profile; [[huang2024gamabench]] and [[duan2024gtbench]] cover the
  normal-form games GIFT trains on as evals.

## Ideas to borrow
- Report a **full train-task × eval-task matrix** (diagonal = in-domain, off-diagonal = transfer),
  at more than one model scale, and include the untrained base as a row (Tables 1–2).
- Include the **opponent as a variable**: training opponent ≠ evaluation opponent, and test
  sensitivity (Table 6).
- Compare **mixed vs sequential (CST) vs task-normalised** multi-task RL when training several social
  skills; CST is a cheap change to the update loop.
- Guard against format-learning artefacts: check the base model is above chance and parseable before
  attributing gains to transfer (1.5B SocialIQA 27.64 is below 3-way chance).
- Recompute summary columns from the tables (the 42.00 misprint).

## Map fields
- Skills measured: competing (TicTacToe), cooperating/deceiving-detecting (Who's the Spy), other (Nash-equilibrium choice in matrix games; math; MMLU; CommonGen; SocialIQA)
- Scoring: mixed (rules for games/math/MCQ; GPT-4o judge for CommonGen)
- Agents: many (2 in TicTacToe/matrix, 4 in Who's the Spy)
- Opponents: LLM (Qwen3-14B in training, Gemini-2.5-Flash in evaluation)
- Tests: capability
- Training evaluated: RL (single-task, mixed multi-task, CST, task-level advantage normalisation)
- Transfer between skills measured: yes (game ↔ game, game ↔ math, game → MMLU/MMLU-Pro/CommonGen/SocialIQA)
- Models tested: Qwen2.5-1.5B-Instruct, Qwen2.5-7B-Instruct (trained); GPT-4o, Gemini-3-Flash-Preview, DeepSeek-V3.2 (reference only)
- Code released: https://anonymous.4open.science/r/GIFT-LLM
