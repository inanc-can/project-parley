---
id: sarkar2025training
title: "Training Language Models for Social Deduction with Multi-Agent Reinforcement Learning"
authors: [Bidipta Sarkar, Warren Xia, C. Karen Liu, Dorsa Sadigh]
year: 2025
arxiv: "2502.06060"
venue: AAMAS 2025 (Detroit), per the paper's p. 1; arXiv v1, 9 Feb 2025
code: https://socialdeductionllm.github.io/
read: full
relevance: medium
topics: [game-theoretic-evals, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 14 pages (main text pp. 1–8, references pp. 9–10, appendices A–F pp. 11–14) on
2026-11-15. Venue taken from the ACM reference block on p. 1 (arXiv metadata gives none).
Win rates in Figs. 3–4 are bar charts without printed values; numbers below are those stated in
the text. Players: 5 in training (4 crewmates + 1 imposter), 4–6 at evaluation; discussion order
is a random cycle over living players twice, so `turn_protocol: strict`.

## Question
Can small LLMs learn to *discuss* productively in a social deduction game without any human
demonstrations, by decomposing communication into **listening** (inferring the hidden role from
observations and messages) and **speaking** (sending messages that move teammates' beliefs toward
the truth), trained with multi-agent RL? (pp. 1–2)

## Setup
- Stanford (Sadigh, Liu). Own text-only **Among Us** environment: W×H grid of rooms; crewmates do
  tasks (blind while doing them), one imposter kills; reporting a body starts a discussion (each
  living player speaks twice, ≤20 tokens, random order), then a plurality vote ejects one player
  (pp. 4–5; App. A p. 11). Crewmates win (+1) by finishing all tasks or ejecting the imposter;
  imposter wins (−1 to crew) when imposters ≥ crewmates (p. 4).
- Before discussion and after every message the environment **surveys each crewmate's vote
  distribution** (no effect on the game) — used for training signals (p. 4; App. A p. 11).
- Base model: **RWKV** (recurrent, linear attention) chosen because trajectories reach tens of
  thousands of tokens per player; **1.5B** used for ablations after a scaling check of 169M–7B
  (p. 4; App. B Table 1 p. 12: imposter-prediction accuracy after listening training 0.60 → 0.65
  from 169M to 7B, vs 0.15–0.22 for original RWKV).
- **Training arms** compared (pp. 5–6):
  - *RL*: independent PPO on sparse game reward + task rewards, with a KL penalty to the base
    model (λ_NL = 0.05) (Eq. 1).
  - *L (listening only)*: supervised loss −log π(true imposter | history) at each survey step, on
    rollouts with random gameplay actions (Eq. 4).
  - *RL + L*: both (Eq. 3).
  - *RL + L + S*: adds a **speaking reward** = change in the sum of living crewmates' belief in
    the true imposter after the speaker's message (Eqs. 5–7).
  - All add a world-modelling loss (predict next observation, λ_WM = 1) for stability (Eq. 9).
  - Baselines: base RWKV 1.5B and RWKV 7B, no training.
- **Multi-agent setup**: iterated self-play where crewmates and imposters train against earlier
  versions of each other; imposters keep the RL loss and get the *inverted* speaking reward
  (reward for misleading) (Eq. 8). One crewmate is always frozen to the listening policy π_L
  (N-agent ad hoc teamwork) to prevent private conventions (p. 6).
- **Training distribution**: layouts 1×3, 2×2, 2×3; 3–5 tasks per crewmate; always 4 crewmates +
  1 imposter (p. 6).
- **Evaluation**: "base" environment (2×2 grid, 4 tasks, 5 players) with imposter and one crewmate
  fixed to π_L (Fig. 3 p. 6); variations in layout (2×1, 1×3, 2×2, 2×3, 3×2), tasks (2–6) and
  players (4–6), several outside training (Fig. 4 p. 7); exploitability curves across 3 self-play
  iterations (Fig. 5 p. 8). Three seeds, min/max error bars.
- **Compute**: single A40 (48 GB) per run; every model trains within 48 h; lr 3e-4, batch of 30
  environments (App. E pp. 13–14). Code under GPL v3, built on CleanRL PPO (p. 14).

## Findings
- **Base models fail**: RWKV 1.5B and 7B both win under 20% in the base environment (p. 6).
- **RL alone helps** and beats the untrained 7B, but cannot learn to identify the imposter; even
  warm-started from π_L, RL "quickly loses the ability to identify imposters", voting for anyone
  with equal probability (p. 7) — sparse-reward RL erased a skill learned by supervision.
- **Listening is the big lever**: π_L alone is a strong baseline; RL + L raises win rates
  "dramatically"; adding the speaking reward gives a further but **relatively small** gain (p. 7).
  Full RL + L + S has **twice the win rate of RL-only** and over **three times** that of base
  models more than four times larger (pp. 3, 7). Speaking improves partly as a side effect of
  better listening (coherent suspicion-sharing appears even without S) (p. 7).
- **Unseen configurations**: method ranking persists across layouts, task counts and player
  counts; no significant deviation from trend in out-of-distribution settings (2×1, 3×2 layouts;
  2 or 6 tasks; 4 or 6 players). More tasks lowers all win rates; more crewmates raises them
  (p. 7; Fig. 4).
- **Robust to adaptive imposters**: across self-play iterations crewmate win rate converges to
  **0.51–0.56** (by seed) against adversarially trained imposters; crewmates trained only against
  the base imposter are already strong (large jump in the lower bound from iteration 0 to 1)
  (p. 7; Fig. 5 p. 8).
- **Emergent behaviour**: crewmates accuse directly and cite observation-like evidence ("Player
  Green is leaving Room (0,1)"); naming a player makes others more likely to vote for them. They
  also **make up evidence** — stating whatever is most convincing — and imposters learn to
  counter-accuse and mimic crewmate speech, which sometimes works (pp. 7–8; App. C pp. 12–13).
- **Failure modes** (p. 8): (i) KL weight too low → language degenerates into random tokens
  within a few iterations; (ii) training all crewmates together → degenerate conventions (all stay
  silent and vote out whoever speaks; wait in the start room and eject whoever leaves) — fixed by a
  frozen crewmate; (iii) RL raises action-token probability so models emit action tokens in
  discussion — fixed by the world-modelling loss.

## Limitations
- **One game, one side measured**: only Among Us, and results are reported for crewmates; the
  imposter is trained only as an adversary. "Unseen" means unseen *configurations* (layout, tasks,
  player count) of the same game, not unseen games or other social skills.
- The listening signal needs a ground-truth hidden answer (who the imposter is); authors note the
  scene-prediction target is task-dependent (p. 8).
- Small, old base model (RWKV 1.5B); discussion messages are ≤20 tokens and still crude (App. C).
- No human players, no frontier LLM opponents; win rates only shown in charts, three seeds.
- Truthfulness is not optimized and the crewmates lie; the authors flag this as potentially
  dangerous outside the sandbox (p. 8; App. D p. 13).

## Relevance to Parley
- **A clean multi-agent RL harness for a social skill**, with ablations that separate
  sub-skills: supervised *listening* (detecting deception), RL *speaking* (persuading teammates),
  and sparse-reward RL. For study (b) it is evidence that the harness matters per sub-skill:
  supervision on the hidden answer drives most of the gain; RL on payoff alone *destroys* the
  listening skill (p. 7) — a within-game case of one objective eroding another.
- It covers deceiving/detecting and persuading in one hidden-role game, and tests robustness to
  configuration shift and to adaptively trained opponents (exploitability curves). It leaves open
  everything about **cross-skill transfer**: whether Among Us training changes negotiation,
  cooperation, or susceptibility to persuasion elsewhere.
- **Persuasion-by-fabrication** emerges from a belief-change reward: crewmates win by inventing
  convincing evidence (p. 7). For [[persuasion-susceptibility]], the speaking reward is literally
  "how much did my message move the listener's belief", so it trains persuasiveness, not
  truthfulness — and the same with [[vendrell2026gametalk]], where payoff training produced a
  cooperative-talk/undercutting deceiver. A transfer study should measure whether such training
  raises deception or fabrication in other games.
- Compared with [[he2026socialgym]] and [[taylor2026clocktower]]: those *evaluate* hidden-role
  games with prompted frontier models; this *trains* a small model on one. SocialGym's finding that
  deceiving and detecting rank models differently (side gaps) fits this paper's split of listening
  vs speaking as separable skills.
- Compared with [[liu2025spiral]]: both use multi-agent self-play RL, but SPIRAL tests transfer to
  general reasoning; this tests only within-game robustness.

## Ideas to borrow
- **Belief surveys between messages** (ask every listener for a distribution over the hidden
  answer) as a dense, rule-based signal of persuasion: usable as a measure (did the message move
  beliefs toward or away from the truth?) and as a reward.
- **Separate listening and speaking objectives** and ablate them (L, RL, RL+L, RL+L+S) — the same
  factorial layout can isolate which harness changes which skill.
- **Frozen partner** (one agent fixed to a reference policy) to block private conventions in
  multi-agent training (p. 6).
- **Exploitability curves** (win rate vs a best-response opponent per self-play iteration) to show
  a trained policy is not just exploiting a fixed opponent (Fig. 5).
- Hold out configurations (layout, team size) for a cheap generalization check before moving to
  cross-game tests.

## Map fields
- Skills measured: deceiving-detecting (identify the imposter), persuading (moving teammates' votes), cooperating (crewmate team coordination)
- Scoring: rules
- Agents: many (5 in training; 4–6 at evaluation)
- Opponents: learned agents (self-play imposters, frozen listening-policy crewmate)
- Tests: capability
- Training evaluated: SFT (supervised listening loss), RL (PPO), multi-agent (iterated self-play MARL)
- Transfer between skills measured: no (only held-out configurations of the same game)
- Models tested: RWKV 1.5B (trained); RWKV 169M–7B (scaling check); RWKV 7B untrained baseline
- Code released: https://socialdeductionllm.github.io/
