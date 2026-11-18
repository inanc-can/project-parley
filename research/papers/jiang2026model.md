---
id: jiang2026model
title: "One Model, All Roles: Multi-Turn, Multi-Agent Self-Play Reinforcement Learning for Conversational Social Intelligence"
authors: [Bowen Jiang, Taiwei Shi, Ryo Kamoi, Yuan Yuan, Camillo J. Taylor, Longqi Yang, Pei Zhou, Sihao Chen]
year: 2026
arxiv: "2602.03109"
venue: arXiv preprint (v1, 3 Feb 2026)
code: none given in the paper
read: full
relevance: medium
topics: [game-theoretic-evals, negotiation-benchmarks, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: 2–9
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

## Question
Can one LLM learn conversational social intelligence (goal pursuit, empathy, persuasion,
compromise) by role-playing *every* participant of a multi-turn, multi-party conversation and being
trained with RL on end-of-episode rewards, with no human supervision of behaviour? Does training
on competitive goals also produce collaborative behaviour? (pp. 1–3)

## Setup
- **OMAR ("One Model, All Roles")**: GRPO's n rollouts per prompt are reinterpreted as the n
  participants of one conversation; the same policy writes every participant's turn, each with its
  own persona prompt, and the batch size equals the number of active participants (Fig. 1, p. 2;
  §3.1, p. 4). **All participants speak simultaneously each turn**; their utterances are
  concatenated into the shared history for the next turn (p. 4; listed as a limitation, p. 13).
- **Algorithm**: PPO with a critic, not GRPO, because rollouts of one conversation are not
  independent and group normalization is "ill-defined" (p. 4). **Hierarchical advantage
  estimation**: turn-level GAE on the value of each turn's last token, then that turn advantage is
  the pseudo-reward for token-level GAE within the turn (Fig. 2, §3.2, pp. 4–5). Turn decay 0.9.
- **Environment 1, SOTOPIA** (two-party role-play with private goals and secrets, usually
  opposing goals, e.g. buyer vs seller): ~3,200 train / 500 test samples, 0–2 human-written opening
  rounds kept, up to 5 turns per participant (pp. 5–6). Model **Qwen-2.5-7B**, SFT cold start,
  then RL, batch 16, lr 1e-7, **one epoch** (p. 6).
- **Reward in SOTOPIA is an LLM judge (GPT-5)**: the seven SOTOPIA dimensions (goal completion,
  believability, knowledge 0–10; secret, social rules −10–0; relationship, financial benefit −5–5)
  are scored per participant and *aggregated* into the reward (p. 6). So the "competitive" reward
  already contains relationship and social-rule terms.
- **Environment 2, Werewolf** (6 or 9 players, two teams, zero-sum): **Qwen-3-4B**, Werewolf data
  from Ye et al. 2025 (~3,200 / 500), same setup. **Verifiable reward**: winning side +1, losing
  side 0, players eliminated early get 75% of their side's reward (p. 9).
- **Anti-reward-hacking measures**: SFT cold start on expert trajectories; a GPT-5 per-utterance
  quality filter (natural, some reasoning, format, no degeneration) that zeroes the turn reward of
  failing turns; early stopping on hacking, filter failure or rising entropy (p. 10).
- **Compute and framework**: **8 H100**, **verl** + vLLM (pp. 5–6); arena evaluation uses 4 GPUs
  per model (p. 6). Wall-clock time and GPU-hours not reported.
- **Evaluation**: an "arena" of 100 conversations where the trained model and base Qwen-2.5-7B take
  opposite roles, judged by GPT-5 (p. 6). Comparison: SOTOPIA-RL (Yu et al. 2025a, same base model,
  single-turn utterance-level rewards from a reward model) in the same arena (p. 6). Five
  additional judge metrics (0–10), never used in training: compromise seeking, persuasion skill,
  strategic commitment, empathy expression, mutual benefit seeking (pp. 6–7).

## Findings
- **Trained SOTOPIA metrics, small gains** (normalized scores, trained / SOTOPIA-RL / base; Fig. 3
  top, p. 7): believability 0.712 / 0.696 / 0.651; goal 0.666 / 0.656 / 0.601; knowledge 0.623 /
  0.610 / 0.574; relationship 0.223 / 0.209 / 0.219; social rules −0.017 / −0.035 / −0.020;
  average 0.309 / 0.291 / 0.299. Secret and financial benefit omitted (all near zero). Note
  SOTOPIA-RL's average is *below* base, and relationship barely moves.
- **Untrained ("emergent") judge metrics** (Fig. 3 bottom, p. 7): mutual benefit seeking 0.771 /
  0.755 / 0.730; compromise seeking 0.737 / 0.727 / 0.668; empathy 0.687 / 0.684 / 0.677;
  strategic commitment 0.696 / 0.682 / 0.684; persuasion 0.573 / 0.555 / 0.555; average 0.695 /
  0.681 / 0.663. The text calls these "substantially larger" gains (p. 7); vs base the average gap
  is +0.032 (vs +0.010 on trained metrics), but vs SOTOPIA-RL it is only +0.014, and compromise
  seeking's big jump is mostly shared with SOTOPIA-RL (+0.059 vs +0.069 for OMAR).
- **"Competition elicits collaboration" (SOTOPIA)**: the claim rests on the rises in mutual-benefit
  and compromise seeking above, plus qualitative examples (Fig. 4, p. 8; text pp. 7–8). The authors
  themselves explain it as the agent seeking partial goal fulfilment "where the LLM-as-a-judge
  would give higher partial scores" (p. 8), i.e. the judge rewards compromise.
- **Werewolf**: werewolf-team win rate rises "from approximately 55% to 72%" with the trained model
  (p. 9); the opponent in that comparison is not specified. Behaviour rates (Table 1, p. 9) compare
  **surviving vs eliminated players**, not trained vs base: identity concealment 59 vs 35%, voting
  manipulation 43 vs 26%, intra-team collaboration 41 vs 32% (werewolves); protecting power roles
  32 vs 14%, recognizing deception 51 vs 34% (villagers). How behaviours were labelled (judge or
  human) and on how many games is not stated.
- **Reward hacking is the main failure**: without the three mitigations "training fails easily
  ... producing little meaningful results" (p. 10); worse in zero-sum games where someone always
  wins regardless of quality (pp. 10, 13). Small models degenerate (repeating instructions, mixing
  languages) (pp. 10–11).

## Limitations
- **No transfer or multi-task experiment**: SOTOPIA and Werewolf are trained separately, on
  different base models (7B vs 4B); no cross-evaluation (SOTOPIA-trained on Werewolf or vice versa),
  no mixed training.
- **No ablations**: no single-role vs all-roles comparison, no PPO-without-hierarchical-advantage
  run, no seeds, no error bars, no significance tests; the arena is 100 conversations (p. 6).
- **Almost everything is judged by GPT-5**: the training reward, the quality filter and all
  SOTOPIA metrics. Judge and reward share a model, so "emergent" metrics may reflect the judge's
  taste rather than new skill. No human evaluation.
- The SOTOPIA reward is not purely competitive (it includes relationship and social-rule terms), so
  collaborative behaviour is partly rewarded directly; in Werewolf the "collaboration" is
  within-team, which the zero-sum team reward directly incentivizes.
- Werewolf numbers are correlational (survivors vs eliminated) and the win-rate opponent is
  unclear. Simultaneous speaking is unlike real turn-taking; participant count is capped by batch
  size (p. 13). Scores in Fig. 3 are normalized without saying how.
- Financial benefit, the only money-like SOTOPIA dimension, shows no movement (p. 7).

## Relevance to Parley
- **On the student's hypothesis** (broad social/strategic training beats narrow, or one method
  improves many directions at once): this paper is **weak, indirect support for the weak form
  only**. One RL run on SOTOPIA lifts all five trained-and-reported dimensions and all five
  untrained judge dimensions a little, with no dimension getting worse vs base (Fig. 3, p. 7):
  no visible trade-off between e.g. persuasion and empathy, unlike [[li2026whose]] (could not
  cross the leak/over-refusal frontier) and [[micelibarone2026used]] (RL for profit cost honesty).
  But all these "directions" are scored by the same GPT-5 judge in one environment, so they may be
  one correlated judge preference rather than separate skills, and gains vs SOTOPIA-RL are
  0.01–0.02.
- **It says nothing on the strong form**: no broad-vs-narrow comparison, no transfer between
  SOTOPIA and Werewolf, no single-role control. The "competitive training encourages collaborative
  behaviour" headline is mostly judge-scored and partly built into the reward (p. 6, p. 8); it is
  not a clean case of competition transferring to cooperation. Compare [[liu2025spiral]], which
  does run single vs multi-game and finds multi-game best on average but worse on negotiation.
- **Measurement lesson for the benchmark**: SOTOPIA-style judge rubrics ([[wang2024sotopia]]) as
  both reward and eval make "transfer" hard to separate from judge-gaming. A transfer/interference
  benchmark needs verifiable outcomes (deal value, surplus, win rate, leak) per direction, with the
  judge only as a secondary measure; Werewolf's win/loss is the only verifiable signal here.
- **Persuasion**: "persuasion skill" here is a judge score for the speaker, not resistance of the
  target. [[sadab2026receiver]] shows the receiver decides outcomes; OMAR never measures whether
  the trained model becomes easier or harder to persuade, which is exactly an interference
  direction worth measuring.
- **Harness axis**: it adds one more "RL, multi-agent self-play" point (PPO, 4–7B, 8 H100, verl)
  next to [[liu2025spiral]] (REINFORCE + RAE, Oat), useful as a template for the RL arm.

## Ideas to borrow
- **One model, all roles, n-party batches**: makes self-play for 3+ party negotiations (coalitions,
  mediator) cheap to set up; batch size = participants.
- **Hierarchical (turn → token) advantage** for long negotiations with end-only rewards.
- **Arena evaluation** (trained vs base on opposite sides) solves the zero-sum "everyone can't
  improve" problem; extend it to a cross-play matrix of harnesses (prompted, SFT, RL).
- **Turn-level quality filter** that zeroes reward for degenerate turns as a cheap anti-hacking
  guard; log the filter failure rate and entropy as stop signals.
- Held-out "emergent" metrics never used in training is a good design idea, but use verifiable
  ones (e.g. Pareto efficiency, honesty about reservation price) rather than the reward judge.
