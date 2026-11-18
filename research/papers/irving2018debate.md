---
id: irving2018debate
title: "AI safety via debate"
authors: [Geoffrey Irving, Paul Christiano, Dario Amodei]
year: 2018
arxiv: "1805.00899"
venue: arXiv preprint (v2, 22 Oct 2018)
code: null
read: full
relevance: low
topics: [judges, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 24 pages (pp. 1–22 text, pp. 23–24 references) on 2026-11-15. OpenAI. This is an
**AI-safety method paper** (a proposal for training aligned agents), not a benchmark of social
skill or negotiation. Stakes are a zero-sum win/loss decided by the judge.

## Question
Can a zero-sum debate between two agents, judged by a human, supervise AI systems on questions too
hard for the human to judge directly? (abstract, pp. 1–2)

## Setup
- **Game** (§2, p. 3): both agents see a question, state answers, alternate short statements up to
  a limit; the judge decides who "gave the most true, useful information". Zero sum; trained by
  self-play. At test time only the answers are needed.
- **Central claim**, stated as an empirical hypothesis, not proven: "it is harder to lie than to
  refute a lie" (p. 3). If true, the authors *hope* all Nash equilibria are honest.
- **Theory** (§2.2, pp. 5–6): with a polynomial-time judge and optimal play, debate with n rounds
  reaches Σn P, and with polynomially many rounds PSPACE (Theorem 1), vs NP for direct judging;
  explicitly "analogies only" (p. 6).
- **One experiment** (§3.1, pp. 8–10): sparse MNIST. A CNN judge is pre-trained to classify from 6
  (or 4) random nonzero pixels; two agents (pure MCTS, 10k rollouts per move, no learning) each
  claim a digit, one forced honest and one liar, and alternately reveal pixels. No natural language,
  no LLMs, no human judges.
- A human cat-vs-dog one-pixel debate website (debate-game.openai.com) was played only informally
  (§3.2, p. 11).

## Findings
- **MNIST** (Table 2, p. 8; p. 10): judge accuracy from random pixels 59.4% (6 px) and 48.2% (4 px);
  honest-player win rate with precommitted lies 88.9% (6 px) and 85.2% (4 px); without precommit
  74.4% and 59.7%. Precommit is "crucial" (p. 10). Without averaging over 3 seeds, 87.7% / 83.8%.
- Successful lies concentrate on claiming 8 or 9 (e.g. 5 → 8, 4 → 9), likely because only nonzero
  pixels can be revealed (Fig. 3, p. 9). The game has a second-mover advantage (p. 9).
- Informal human play: "extremely difficult to lie" when players know the game (p. 11); no
  numbers.
- The rest (§§4–7) is argument: admitting ignorance (p. 12), judge belief bias and remedies
  (pp. 14–15), stability of self-play, mind-hacking risk, stochastic simulation failure (p. 18),
  symmetry fixes (p. 19), and near-equivalence with amplification (pp. 20–21).

## Limitations
- Only a toy image experiment with a fixed classifier judge and planning (not trained) debaters;
  natural-language debate is "proposal only" (p. 22).
- Honesty-at-equilibrium rests on an unproven empirical claim; the authors list many ways it could
  fail (§5).
- No social-skill measurement, no negotiation, no LLMs.

## Relevance to Parley
- Background for the [[judges]] topic: the setup where a weaker judge reads an adversarial
  transcript is the same shape as Parley's judge LLM, and the paper names the judge failure
  modes (belief bias, not following long debates, being swayed by one emotional point, p. 13–15)
  that a judge-reliability study should test.
- Debate is a zero-sum persuasion game whose judge must *resist* the liar, which links it to
  [[persuasion-susceptibility]]. Multi-agent debate later appears as a downstream test of
  game-trained LLMs in [[yuan2025marshal]].

## Ideas to borrow
- Forced honest vs liar roles with sides randomized, so "honest win rate" measures whether the
  judge can be fooled (pp. 7–8, 11).
- Precommit: making the arguer state its claim before play sharply reduces successful lies
  (Table 2) — a cheap control for any judged game.
- Measure judge convergence by asking the judge's opinion after each statement (§5.7, p. 17).

## Map fields
- Skills measured: not a benchmark (the method is a persuade-the-judge game; the experiment
  measures whether a fixed judge is fooled by a liar).
- Scoring: not a benchmark (judge decides; a CNN classifier in the experiment, humans proposed).
- Agents: 2 (n-agent variant discussed, §6.3).
- Opponents: not a benchmark (MCTS agents in MNIST; humans informally).
- Tests: not a benchmark.
- Training evaluated: none (MCTS planning; self-play RL proposed only).
- Transfer between skills measured: no.
- Models tested: none (no LLMs; MNIST CNN judge + MCTS debaters).
- Code released: none (prototype website debate-game.openai.com only).
