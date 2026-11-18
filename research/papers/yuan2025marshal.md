---
id: yuan2025marshal
title: "MARSHAL: Incentivizing Multi-Agent Reasoning via Self-Play with Strategic LLMs"
authors: [Huining Yuan, Zelai Xu, Zheyue Tan, Xiangmin Yi, Mo Guang, Kaiwen Long, Haojia Hui, Boxun Li, Xinlei Chen, Bo Zhao, Xiao-Ping Zhang, Chao Yu, Yu Wang]
year: 2025
arxiv: "2510.15414"
venue: ICLR 2026 (arXiv v3, 12 Feb 2026)
code: https://github.com/thu-nics/MARSHAL
read: full
relevance: high
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Requested as "MARS: Reinforcing Multi-Agent Reasoning of LLMs through Self-Play in Strategic
Games" (presumably an earlier version's title, not checked); arXiv metadata and the v3 PDF
(28 pages, read in full) title it MARSHAL.

## Question
Can multi-turn self-play RL on a mix of **cooperative and competitive** two-player games give an
LLM strategic skills that carry over to held-out games and to LLM multi-agent systems (debate,
AutoGen) on reasoning benchmarks? Does a generalist trained on all games beat per-game
specialists? (pp. 1–2, 5)

## Setup
- **Games** (OpenSpiel + VS-Bench, actions only, no free-text talk between players) (pp. 5, 15):
  - competitive, perfect information: train **Tic-Tac-Toe**, held-out **Connect Four**;
  - competitive, imperfect information: train **Kuhn Poker**, held-out **Leduc Hold'em**;
  - **cooperative**, imperfect information: train **Mini Hanabi** (2 colours, 2 ranks), held-out
    **Simple Hanabi** (3 colours, 5-card hands) (p. 5; App. I p. 22).
  No negotiation or persuasion game; Hanabi "hints" are structured reveal actions.
- **Rewards**: win/loss/draw ±1 (Tic-Tac-Toe, scaled ×2), chips (Kuhn, max 2), shared +1 per card
  played (Hanabi, max 4); format reward +0.05 / −10 (game ends); linear length penalty above 11
  tokens up to 2,048, α = 0.5 (p. 5; ablation of α in Table 13, p. 20).
- **Algorithm**: GRPO with two changes: (1) **turn-level advantage**, "sum then normalize": Monte
  Carlo return from each turn minus the group mean (= GAE with γ = λ = 1 and a batch-mean baseline);
  (2) **agent-specific normalization**: advantages computed separately per player role (analogous
  to SPIRAL's RAE). One shared policy plays both roles; each game is its own group (pp. 3–4).
- **Models**: **Qwen3-4B** (main; a reasoning model with `<think>`), Qwen3-8B generalist in the
  appendix (App. E, p. 16). Specialists = one per training game; generalist = all three at once
  (p. 5).
- **Compute and framework**: **ROLL** (vLLM rollouts + Megatron-LM training); one server with
  **8 H100**; **200 steps**, batch 128 trajectories (specialists) / 384 (generalist, 128 per game);
  Adam, lr 1e-6 cosine, KL coefficient 0.2, PPO clip 0.2, 1 PPO epoch, max response 4,096 tokens
  (App. B–C, pp. 15–16). **No wall-clock or GPU-hours are reported.** Sampling temperature is 0.6 in
  the text but 0.5 in Table 5, and Table 5 lists λ = 0.95 while the method says λ = 1 (pp. 4, 15–16).
- **Eval**: 1,000 games per game against MCTS (100/1,000 sims Tic-Tac-Toe; 10/100 Connect Four),
  exact Nash (Kuhn) or CFR-approximated Nash (Leduc), as first and second mover; Hanabi in
  self-play. Scores normalized between worst observed and optimum (App. D p. 15). Downstream:
  MATH500, GSM8K, AQUA-RAT, AIME24, AMC23, MMLU-STEM, GPQA-Diamond, single-agent and inside
  **MAD** (competitive debate) and **AutoGen** (cooperative) via MASLab, zero-shot (pp. 6, 16).
  Baseline: SPIRAL trained on the same base (p. 5). **Single run per model, no seeds or CIs.**

## Findings
Game scores are normalized returns (%) from Fig. 3 (p. 6), first / second mover.
- **Specialist vs generalist on the specialist's own game (training games)**: Tic-Tac-Toe
  75.3 / 32.1 specialist vs 77.2 / 29.1 generalist; Kuhn 79.0 / 22.5 vs 76.2 / **3.9** (generalist
  second mover = base 3.9); Mini Hanabi 55.5 vs 54.3. Base Qwen3-4B: 70.2 / 18.6, 62.3 / 3.9, 30.0
  (Fig. 3, p. 6).
- **Held-out games**: Connect Four specialist (Tic-Tac-Toe) 30.6 / 14.8 vs generalist 28.9 / 11.0
  (base 26.9 / 4.4; SPIRAL 30.9 / 8.3); Leduc specialist (Kuhn) 63.9 / 55.1 vs generalist
  61.7 / 47.4 (base 47.7 / 28.7; SPIRAL 24.5 / 27.3); Simple Hanabi specialist 33.9 vs generalist
  **36.8** (base and SPIRAL 13.9) (Fig. 3, p. 6). So the generalist is slightly *below* the matched
  specialist on 5 of 6 games and above only on Simple Hanabi; it is the best on *average*. The
  headline "+28.7% on Leduc" is measured against SPIRAL, not the base (base gap ≈ 16 points); the
  "+22.9% on Simple Hanabi" is against both (p. 6).
- **Cross-category transfer of specialists** (Tables 3–4, p. 9): Tic-Tac-Toe specialist on Mini
  Hanabi 50.48 (base 30.0), and its Hanabi score rises smoothly during training (Fig. 4, p. 6);
  Kuhn specialist on Mini Hanabi 44.98. **Negative transfer**: Hanabi specialist as Tic-Tac-Toe
  second mover 7.35 (base 18.6) and Leduc first mover 37.36 (base 47.7).
- **Competitive-only vs mixed games** (MARSHAL algorithm, average of both seats, Table 8, p. 18):
  Tic-Tac-Toe+Kuhn gives TTT 48.80, Kuhn **47.55**, Mini Hanabi **24.48**, Connect Four 17.90,
  Leduc **29.98**, Simple Hanabi **11.48**; adding Mini Hanabi gives 53.13, 40.05, 54.33, 19.98,
  54.56, 36.75. Against base averages (≈44.4, 33.1, 30.0, 15.7, 38.2, 13.9 from Fig. 3)
  competitive-only training **falls below the untrained model** on Mini Hanabi, Simple Hanabi and
  Leduc (interference), while adding the cooperative game helps five games but **costs 7.5 points on
  Kuhn**.
- **Multi-agent systems** (Table 1, p. 7; averages over 7 benchmarks): single-agent base 60.74,
  SPIRAL **63.75**, TTT 63.54, Kuhn 61.38, Hanabi 62.05, generalist 62.79 (generalist *drops* on
  GPQA 39.39 → 34.85 and AIME 36.7 → 33.3). **MAD**: base 72.45, SPIRAL 73.41, TTT 75.01, Kuhn 74.54,
  Hanabi 73.70, **generalist 75.96** (+3.51; GPQA +7.57). **AutoGen**: base 79.14, SPIRAL 80.05,
  TTT 80.15, Kuhn 81.54, Hanabi 81.54, **generalist 82.15** (+3.01; AIME +10.0, i.e. 3 of 30
  problems). Competitive-only training: MAD 75.24 (≈ full), AutoGen 80.34 vs 82.15 (Tables 9–10,
  p. 18). Authors read this as "competitive games help debate, cooperative games help AutoGen" (p. 7).
- **Fixed-opponent training overfits in games** (Table 3, p. 9): Tic-Tac-Toe vs MCTS improves its
  own game (88.00 / 41.95 vs 75.30 / 32.10) but falls on Mini Hanabi (34.93 vs 50.48) and Simple
  Hanabi (12.22 vs 29.75); Kuhn vs Nash collapses to 0.00 on every other game (raw return −1 = loss
  every game) and is also worse on Kuhn itself (76.19 / 15.64 vs 79.04 / 22.49).
- **But in the appendix tables the "bad" variants score higher in MAD**: averaging Table 17
  (p. 28), fixed-opponent TTT 78.5 and Kuhn 78.3, no-turn-level TTT 79.4 and Kuhn 80.2, all above
  the full generalist's 75.96; in AutoGen (Table 18, p. 28) the same variants fall to 72–75,
  below the base 79.14. The paper does not discuss this; it suggests MAS scores are noisy or
  framework-specific (my computation from the tables).
- **Ablations** (Table 4, p. 9): removing turn-level advantage or role normalization lowers most
  held-out scores (e.g. Kuhn specialist Leduc 63.94 / 62.10 → 32.26 / 31.23) but sometimes *raises*
  the training game (Kuhn 79.04 → 92.49 first mover), i.e. better on the target, worse at transfer.
  Role normalization matters most where roles' returns differ (Tic-Tac-Toe, Kuhn), little in
  cooperative Hanabi (Fig. 6, p. 9). SPIRAL's RAE on the same games: Mini Hanabi 24.93, Simple
  Hanabi 5.53, Leduc 6.11 (Table 8, p. 18). MT-GRPO is worse on 5/6 games (Table 11, p. 19).
- **Failure modes** (GPQA in MAD, taxonomy of Cemri et al.): inter-agent misalignment falls
  55.2 → 43.7% (−11.5), mainly task derailment and ignoring the other agent's input; the text says
  system-design failures fall ~7 points, which the extracted figure labels do not clearly confirm
  (Fig. 5, p. 8).
  Reasoning-pattern claims (role awareness, intent recognition) rest on hand-picked traces (Table 2,
  p. 8).
- **8B** generalist: Leduc 7.26 → 53.89, Simple Hanabi 4.55 → 37.27; MAD 82.49 → 85.09, AutoGen
  79.68 → 83.58 (Tables 6–7, pp. 16–17). No 8B specialists.

## Limitations
- One run per configuration, no seeds or confidence intervals; many downstream gaps are 1–3
  points on benchmarks where one AIME problem is 3.3 points and one AMC problem 2.5.
- Ablated and fixed-opponent models beat the full method in MAD (Table 17, p. 28), undercutting
  the claim that MAS gains come from the proposed design; not discussed.
- Normalized game scores use "worst observed" as the floor, so they depend on which models are in
  the comparison (App. D p. 15); the "28.7%" headline uses SPIRAL as reference.
- Only three training games, one cooperative; two-player only; no natural-language communication,
  negotiation, persuasion or mixed-motive games; no humans (p. 10).
- Generalist uses 3× the batch (384 vs 128) at equal steps, so it sees 3× the trajectories; breadth
  and data volume are confounded (App. B p. 15).
- Hyperparameter inconsistencies (temperature, λ) between text and table (pp. 4, 15–16); no
  compute time reported.

## Relevance to Parley
- **On the student's hypothesis (broad social/strategic training beats narrow training, even on the
  narrow target): mixed, leaning against the strong form.** On its own game the matched specialist
  beats the generalist in 5 of 6 games, sometimes by a lot (Kuhn second mover 22.5 vs 3.9), and the
  generalist wins only on held-out Simple Hanabi (36.8 vs 33.9) (Fig. 3, p. 6). Same pattern as
  [[liu2025spiral]], where the multi-game model lost to the negotiation specialist (33.2 vs 39.1%).
- **Weak form (one method improves many directions): supported on average, with clear trade-offs.**
  The generalist is the best-*average* agent and best in both MAS (75.96 MAD, 82.15 AutoGen,
  Table 1, p. 7). But adding the cooperative game cost 7.5 points on Kuhn, competitive-only
  training pushed cooperative games *below* the untrained model (Mini Hanabi 24.48 vs 30.0,
  Table 8, p. 18), and the Hanabi specialist got worse at some competitive seats. That is measurable
  **interference between social directions** (competition ↔ cooperation), exactly what the planned
  benchmark should quantify.
- **Direction-specific transfer**: competitive training helps the competitive MAS (debate),
  cooperative training is needed for the cooperative one (AutoGen 80.34 vs 82.15 without Hanabi,
  Table 10, p. 18). This supports treating cooperation and competition as distinct axes in a
  transfer/interference matrix, though the effect sizes are small and single-seed.
- **Overfitting to opponents**: fixed-opponent RL wins more on the training game but loses breadth
  or collapses entirely (Kuhn → 0 elsewhere, Table 3, p. 9), matching SPIRAL. For a harness
  comparison (prompting / fine-tuning / RL / multi-agent), "who you train against" must be a factor.
- Compared to [[wang2024sotopia]] (broad social training with no narrow control), MARSHAL has the
  specialist-vs-generalist control the student needs, but on board/card games rather than
  language-based social tasks. Neither [[sadab2026receiver]] nor [[li2026whose]] is addressed:
  there is no persuasion, principal or reservation price; the li2026whose finding that RL could not
  improve both loyalty and helpfulness is a negotiation-side counterpart of the Kuhn/Hanabi
  trade-off here.
- **Feasibility**: 4B, 200 steps, one 8×H100 node, open code (ROLL + OpenSpiel), so a master's
  thesis could reproduce the specialist/generalist matrix and add a negotiation and a persuasion
  game, if hours on such a node are available (time not reported).

## Ideas to borrow
- **Full train-game × test-game matrix** with specialists, generalist, competitive-only and base
  rows, reporting both seats separately; it exposes interference that averages hide.
- Pair each training game with a **harder held-out variant** of the same family (Mini → Simple
  Hanabi, Kuhn → Leduc) as a cheap near-transfer test.
- Score against **fixed reference opponents** (MCTS / Nash) rather than only self-play win rate.
- Evaluate transfer inside **both a competitive and a cooperative multi-agent framework**; the
  split showed direction-specific gains.
- Control for data volume (equal trajectories) when comparing generalist and specialist, and run
  seeds; MARSHAL did neither.
- Turn-level "sum then normalize" advantages with per-role baselines for multi-turn self-play.
