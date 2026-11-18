---
id: liu2025spiral
title: "SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning"
authors: [Bo Liu, Leon Guertler, Simon Yu, Zichen Liu, Penghui Qi, Daniel Balcells, Mickel Liu, Cheston Tan, Weiyan Shi, Min Lin, Wee Sun Lee, Natasha Jaques]
year: 2025
arxiv: "2506.24119"
venue: ICLR 2026 (arXiv v3, 2 Mar 2026)
code: https://github.com/spiral-rl/spiral
read: full
relevance: high
topics: [game-theoretic-evals, negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

## Question
Can an LLM learn general reasoning, without curated problem-answer data, by playing multi-turn
two-player zero-sum games against itself with online RL? Does training on several games beat one
game, and does it beat imitation (SFT) or fixed opponents? (pp. 1–3)

## Setup
- **Training games** (TextArena, Guertler et al.): TicTacToe (spatial), Kuhn Poker (probabilistic,
  hidden info), **Simple Negotiation** (trade 5 resources with private, differing values over
  10 turns, free text plus `[Offer]`/`[Accept]`/`[Deny]`) (p. 6; Fig. 7, p. 18; App. G p. 28).
  Every game is scored as win/lose/draw {+1, 0, −1}, zero-sum, reward only at the end (p. 5), so
  the negotiation game rewards beating the opponent, not the value created by the trade.
- **OOD games**: Snake, Pig Dice, **Truth and Deception** (one player persuades the other to pick
  a false fact over 6 turns; the "communication" OOD test for the negotiation specialist), plus
  Liar's Dice and Connect Four in the observation figure (Fig. 8, p. 19; App. G p. 28).
- **One shared policy plays both roles** (role given in the system prompt); fully online, full-
  parameter updates (p. 5).
- **Algorithm**: REINFORCE with **Role-conditioned Advantage Estimation (RAE)**: a separate EMA
  baseline b_{G,p} per game and role (decay 0.95), advantage = R − b_{G,p}; no length
  normalization (Eq. 2–3, p. 5). The hyperparameter table also lists PPO-style policy clipping 0.2
  and 2 inner proximal epochs; KL coefficient 0; lr 1e-6 constant; batch 128; max response 8,192
  tokens; temperature 1.0 (Table 6, pp. 19–20).
- **Models** (4B–8B): Qwen3-4B-Base, Qwen3-8B-Base, Octothinker-8B-Base, Llama-3.1-8B-Instruct,
  DeepSeek-R1-Distill-Qwen-7B; Qwen3-4B-Instruct-2507 in the appendix (p. 6; App. E.8 p. 24).
- **Compute and framework**: 400 steps × 128 samples on **8 H100**; ~25 h (Qwen3-4B), 28 h
  (Qwen3-8B), 16 h (Llama-8B, Octothinker-8B) per run, i.e. roughly 130–225 H100-hours per run
  (pp. 6, 16, 18). Built on Oat (actor-learner) + vLLM + TextArena (pp. 5–6).
- **Baselines**: SFT on 25k (and 52k) winning trajectories from Qwen3-32B self-play; RL against
  fixed opponents (random, Mistral-Small-3, Gemini-2.0-Flash-Lite) (pp. 6, 8, 23).
- **Eval**: 8 benchmarks zero-shot (MATH500, AIME24/25, OlympiadBench, AMC23, Minerva, GPQA-D,
  MMLU-Pro; base model few-shot) and win rates in games vs Gemini-2.0-Flash (pp. 6, 19–20).

## Findings
- **Math/general transfer**: Qwen3-4B-Base 34.0 → 44.5 average (+10.5) with multi-game SPIRAL;
  Qwen3-8B-Base 39.5 → 49.6; Octothinker-8B 25.8 → 33.8; Llama-3.1-8B-Instruct 23.9 → 25.9;
  DeepSeek-Distill-7B 60.4 → 61.8. SFT-Multi: 39.7, 46.1, 27.0, 25.0, 58.3 (Table 1, p. 7). Doubling
  SFT data to 52k changes nothing (39.7) (Table 9, p. 23). Three seeds on Qwen3-4B: 44.5 ± 0.5 vs
  SFT 39.6 ± 0.4 (Table 10, p. 23).
- **Single vs multi-game on benchmarks (Qwen3-4B, single seed each)**: TicTacToe 41.3, Kuhn 43.4,
  **Negotiation 40.0** (weakest), TicTacToe+Kuhn 41.3 (*below* Kuhn alone), all three 44.5
  (Table 9, p. 23). So multi-game is best, but only +1.1 over the best single game, and adding a
  game does not always help. The appendix text quotes different ranges (single 40.0–41.4, multi
  42.3–42.7) that do not match the table (p. 22).
- **Single vs multi-game in games** (vs Gemini-2.0-Flash, Table 5, p. 9): multi-game average 59.5%
  vs best specialist 52.9% (TicTacToe), 52.7% (Kuhn), 48.6% (Negotiation). **But on Simple
  Negotiation itself the multi-game model (33.2%) loses to the negotiation specialist (39.1%)**;
  multi-game wins on Kuhn (53.9 vs 48.5) and the OOD games. The untrained *instruct* model averages
  57.6%, almost as high, and beats every model on Simple Negotiation (46.2%).
- **Specialists transfer to "similar" OOD games** in head-to-head play: TicTacToe → Snake 56.0%,
  Poker → Pig Dice 91.7%, Negotiation → Truth and Deception 55.8%; but the negotiation specialist
  gets **1.1% on Pig Dice** (negative transfer outside its skill) (Table 4, p. 9). Against Gemini,
  Truth and Deception is near ceiling for everyone (base 49.6%, instruct 75.5%, multi 84.0%).
- **Harder variants** (Table 8, p. 22): 8-resource Negotiation (OOD) 31.0% for SPIRAL vs 8.7% SFT
  and 5.5% base; OOD average 36.1 vs 18.4 (SFT).
- **Self-play beats fixed opponents**: RL against fixed Mistral/Gemini on Kuhn *lowers* math scores
  (29.6, 33.4 vs base 34.0) (Table 9, p. 23); Gemini-trained win rate climbs 0% → 62.5% (exploiting
  one opponent) while self-play stays at 50–52% vs its past self (Table 3, Fig. 5, p. 8).
- **RAE prevents "thinking collapse"**: without it, reasoning traces shrink from ~2,000 characters
  to near zero within 100–200 steps (outputs like `\boxed{bet}`), general reasoning drops 44 → 40%
  and math 35 → 12%; with RAE 40 → 47% (Fig. 6, p. 9; Fig. 9, p. 20).
- **Mechanism (LLM-judged)**: GPT-4.1 classifies 290 Kuhn games and 46,792 math solutions;
  case-by-case analysis 72% (games) → 71% (math), pattern recognition 35 → 45%, expected value
  78 → 28% (Fig. 4, p. 7; App. F pp. 24–27).
- **Combines with RLVR**: Math RLVR alone 46.0; SPIRAL → RLVR 46.5; RLVR → SPIRAL 47.9 (Table 12,
  p. 24; text says 48.1). On Qwen3-4B-Instruct SPIRAL 75.9 vs base 74.1, SFT 71.9 (Table 13, p. 24).

## Limitations
- All games are reduced to **win/lose zero-sum**; the negotiation game's possible joint gains are
  not rewarded or measured (no deal rate, no surplus, no Pareto efficiency).
- Single-game vs multi-game comparisons are single-seed; the gaps (1–4 points) are within the
  range a seed could move on some benchmarks (only the main row has 3 seeds) (pp. 22–23).
- Small numeric inconsistencies between text and tables (pp. 22–24); mechanism analysis relies on
  GPT-4.1 classification with only spot checks (p. 26).
- Only 4B–8B models, 400 steps; gains plateau with longer training (p. 16). LLM opponents only;
  no humans. Authors acknowledge academic-benchmark focus and reward-hacking risk (pp. 16–17).
- Negotiation is the weakest single game for math transfer and the multi-game model is worse at
  it than the specialist, which the paper does not discuss.

## Relevance to Parley
- **Most direct evidence so far on the student's hypothesis** (broad social/strategic training
  beats one setting, or improves many directions at once). It **partly supports** it: multi-game
  training gives the best benchmark average (44.5 vs 40.0–43.4 single-game, Table 9, p. 23) and the
  best game average (59.5 vs ≤ 52.9%, Table 5, p. 9), i.e. one method improves many directions
  rather than trading them off, unlike [[li2026whose]] where RL could not cross the
  leak/over-refusal frontier and [[micelibarone2026used]] where RL for profit cost honesty.
- **But it does not support the strong form for negotiation**: on Simple Negotiation the
  multi-game model (33.2%) is *worse* than the negotiation specialist (39.1%) and than the
  untrained instruct model (46.2%) (Table 5, p. 9). Broad training here trades some negotiation skill
  for breadth. Also the "broad set" is only three games, only one of them a negotiation, and none
  cooperative or persuasion-trained; the authors list cooperative games as future work (p. 10).
- **The reward is the gap**: SPIRAL negotiation is zero-sum win/lose, while Parley's negotiations
  (and [[liu2026instructing]], [[bergemann2026training]]) have integrative value and reservation
  prices. A thesis could test whether SPIRAL-style multi-game self-play still helps when one game is
  mixed-motive and scored on surplus, deal rate and honesty, not on winning.
- **Feasibility for a master's thesis**: a full run is 8 H100 × 16–28 h at 4–8B with open code
  (Oat + vLLM + TextArena). Several ablation runs are needed, so this needs a GPU allocation (e.g.
  at TUM), but it is not out of reach. RAE is a cheap, essential trick for shared-policy self-play.
- Market framing ([[bichler2026model]]): the fixed-opponent result (exploits one rival, loses
  generality) mirrors the point that what an agent trains against shapes the regime it learns.

## Ideas to borrow
- **Role-conditioned baselines** (per game × role EMA) for any shared-policy self-play in Parley.
- Report **specialists vs multi-game** in a full matrix (training games × held-out games), with
  seeds, to test "breadth vs trade-off" directly; include the untrained instruct model as a
  baseline, since it was competitive here.
- Watch response length as a **collapse alarm** during RL.
- Fixed-opponent vs self-play comparison as a control for "learned the game" vs "exploited one
  opponent".
- Held-out harder variants (8-resource negotiation) as a cheap generalization test.
