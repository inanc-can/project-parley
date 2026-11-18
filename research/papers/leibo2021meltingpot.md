---
id: leibo2021meltingpot
title: "Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot"
authors: [Joel Z. Leibo, Edgar Duéñez-Guzmán, Alexander Sasha Vezhnevets, John P. Agapiou, Peter Sunehag, Raphael Koster, Jayd Matyas, Charles Beattie, Igor Mordatch, Thore Graepel]
year: 2021
venue: ICML 2021 (PMLR 139)
arxiv: "2107.06857"
code: code/melting-pot
read: full
relevance: medium
topics: [eval-methodology]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 33 pages (main text pp. 1–9, appendices A–F pp. 10–29, references pp. 29–33) on
2026-11-15. Metadata checked with `scripts/arxiv.py` (it suggests the key `leibo2021scalable`;
the existing key is kept). The heatmaps in Figs. 4–5 (pp. 8–9) do not survive text extraction;
numbers below come from the raw-score table (App. F, pp. 27–29). This is a **pre-LLM multi-agent RL
benchmark**: agents act from 88×88 pixels in 2D grid worlds and there is no language at all.
The later Melting Pot 2.0 tech report (Agapiou et al., arXiv 2211.13746) is a separate paper.

## Question
How can multi-agent RL be evaluated on **generalisation to unfamiliar co-players**, the way
supervised learning is evaluated on held-out test data, without hand-building each test
environment? The answer proposed: use pre-trained agents as the test set (pp. 1–2).

## Setup
- **Central equation**: Substrate + Background Population = Scenario (p. 2). A *substrate* is the
  game (a partially observable general-sum Markov game; agents are not told the rules, p. 3). A
  *background population* is a set of pre-trained "bots". A *scenario* combines them and is **used
  only for testing, never for training** (p. 2).
- **What is evaluated is a training algorithm** (a "multi-agent population learning algorithm",
  MAPLA), not one agent: the algorithm gets unlimited access to the substrate, produces a population,
  and agents sampled from it are tested zero-shot (no test-time learning) with bots they have never
  met (pp. 2, 4). Policies are sampled independently, so a fixed division of labour cannot be
  imposed; the design "deliberately penalizes heterogeneous specialization" (p. 4).
- **Three kinds of test** (pp. 3–4): *resident mode* (focal agents are the majority, a few unfamiliar
  visitors join: is the group's cooperation robust?), *visitor mode* (one or a few focal agents join
  a majority of bots: can they read and follow the local convention?), and *universalization* (all
  players are copies of one focal policy: "what if everyone behaved like you?").
- **Metric**: focal per-capita return (mean reward of focal players only), min-max normalised per
  scenario to 0 (worst) – 1 (best) (pp. 3, 8). Secondary metrics: background per-capita return
  (do the focal agents harm others?) and background positive-income equality, 1 − Gini (p. 4;
  App. A, p. 10). Elo is computed separately for competitive substrates and the rest (p. 8).
- **Suite**: 21 substrates (one training run per substrate, p. 7) covering competitive, pure common
  interest, team and mixed-motive games: social dilemmas (Clean Up, Commons Harvest ×3, Prisoner's
  Dilemma / Chicken / Stag Hunt "in the Matrix"), coordination (Pure / Rationalizable Coordination,
  Bach or Stravinsky, Collaborative Cooking ×2, Chemistry ×2), competition (Running with Scissors ×2,
  Capture the Flag, King of the Hill), territory (Territory ×2) and Allelopathic Harvest (pp. 4–6;
  App. B). 2 to 16 players, most around 8 (p. 2); episodes 1,000 steps (p. 11). The paper says
  "over 80" / "∼85" scenarios (pp. 1, 9); App. E lists 82 numbered scenarios plus 17
  universalization tests (pp. 16–26).
- **Bots** (pp. 6–7): RL agents trained on pseudo-rewards from substrate events (e.g. pure-rock
  players, grim-trigger reciprocators, free riders, "good partners" that guard one entrance), some
  chained by a scripted "if this event, run that behaviour" controller ("puppet", p. 16). Each bot
  is checked in 10–30 episodes and rejected if it does not show the intended behaviour (p. 7).
  Communication/language games, turn-based games and physics games were left out (p. 2, fn. 1).
- **Baselines** (p. 7): A3C, V-MPO and OPRE, each also in a "prosocial" variant trained on the group's
  per-capita return; N agents per substrate, 10⁹ steps each; no hyper-parameter tuning (p. 16).
  An *exploiter* (A3C trained directly on the test scenario) and a *random* agent give rough upper
  and lower bounds.

## Findings
- **Overall** (p. 8): V-MPO best on average, then OPRE, then A3C; similar on mixed-motive games,
  V-MPO ahead on competitive ones such as King of the Hill (SC 1: V-MPO 627.8 vs −895 to −990 for the
  others and −991.1 for the exploiter; p. 28).
- **Training score does not predict test score**: prosocial OPRE and A3C reach about the same
  self-play score as their selfish versions in Bach or Stravinsky (A3C 10.8 vs 10.2) but collapse
  when visiting a population of Bach fans (8.3 vs 1.9) (p. 9; p. 27); in Stag Hunt SC 1 A3C scores
  28.6 vs 6.6 for prosocial A3C (p. 29). They learned only cooperation in self-play and are
  exploitable by defectors at test time (p. 9).
- **Maximising collective reward often makes policies less robust** than maximising individual
  reward (p. 2); prosocial agents underperform overall (p. 9) — **but** in Clean Up only the
  prosocial agents learn anything (self-play: 0.0 for all selfish agents vs 36.9 / 72.8 / 188.6
  prosocial; visiting altruists SC 0: A3C 91.5 vs prosocial A3C 380.3, random 69.1; p. 27). The
  paper's conclusion: agents must "contingently balance selfishness and prosociality" (p. 9).
- **Universalization catches over-specialisation**: OPRE in Chemistry: Metabolic Cycles scores 237.9
  in self-play but 1.5 when every player is a copy of one OPRE agent (p. 9; p. 27).
- **Hard substrates stay unsolved**: no agent beats random in self-play on Collaborative Cooking
  (all 0.0; p. 28); in Arena Running with Scissors and Capture the Flag agents are far below the
  exploiter (e.g. Arena RWS SC 2: exploiter 0.60 vs best MAPLA 0.06; p. 27).
- **Exploiters are not a true upper bound** (pp. 8–9): they fail against strong bots (King of the
  Hill) and in games needing cooperation (Commons Harvest: Closed SC 2: exploiter 0.0 vs V-MPO 81.2;
  p. 28).
- **Secondary metrics** (App. A, p. 10): prosocial agents usually raise the background population's
  return without raising inequality; exception Chicken in the Matrix, where they raise background
  return a lot at a mild cost in equality.

## Limitations
- Not language: pixel-based RL in grid worlds, and the paper explicitly excludes communication
  (p. 2, fn. 1). Any use for LLMs is by analogy.
- Policies cannot move between substrates (observation/action spaces differ, p. 3), so it measures
  generalisation to new **co-players within one game**, not transfer between skills or games.
- Bots are only as good as current RL: the authors could not train bots that truly "understand"
  trust, so they built "good partners" by shaping rewards (Commons Harvest: Partnership, p. 21).
- The ranking depends on how scenarios are weighted; the authors call their evaluation "only a
  simple evaluation" (p. 8). Single training runs, no seeds or confidence intervals reported.
- Min-max normalisation uses the worst and best agent in the pool, so scores are relative to the
  agents tested.
- No humans as co-players.

## Relevance to Parley
- **The reference design for held-out co-players.** An LLM benchmark of social skills that compares
  training methods (prompting vs SFT vs RL vs multi-agent training) has exactly Melting Pot's
  problem: a method trained against its own copies or a fixed opponent can look good in training
  and fail with strangers. Melting Pot's answer carries over directly: (1) evaluate the *training
  method*, not one checkpoint; (2) keep a population of co-players that no method ever trains
  against; (3) test in resident mode (does a group trained together survive a few odd partners?),
  visitor mode (can one agent adapt to a group's convention?) and universalization (what happens
  if everyone uses this policy?); (4) report harm to the background population, not just own score.
- The overfitting it shows (prosocial agents exploitable at test time, specialists failing
  universalization) is the RL version of what [[yuan2025marshal]] finds for LLM self-play: training
  against a fixed opponent raises the training-game score and loses breadth. [[liu2025spiral]] trains
  LLMs in self-play; a held-out opponent population of the Melting Pot kind would test whether
  such gains survive unfamiliar partners.
- [[zhang2026terms]] uses scripted negotiation opponents with known private types; Melting Pot's
  bots are the same idea with learned, behaviour-targeted co-players, and its quality-control step
  (reject a bot that does not show its intended behaviour) is a check TERMS-style opponents need too.
- [[he2026socialgym]] uses LLM-vs-LLM round-robin Elo among the evaluated models only, so the
  "opponents" are not held out; Melting Pot shows why a fixed, separate test population makes
  scores comparable across papers.

## Ideas to borrow
- **Substrate + background population = scenario** as the unit of a Parley test: a negotiation game
  plus a fixed pool of held-out opponents (scripted types, frozen LLM agents with set personas,
  human-like imitation models) that training never touches.
- **Resident / visitor / universalization modes** for multi-party Parley games, and a
  **self-play vs held-out gap** as the overfitting measure for every training method.
- **Background welfare and equality** (1 − Gini) as secondary metrics, to see whether a trained
  negotiator wins by hurting the other side.
- **Bot quality control**: run each opponent persona a few times and drop it if it does not behave as
  specified.
- **Exploiter and random anchors** per scenario to normalise scores, keeping in mind that the
  exploiter is not always the ceiling.
- Its social-dilemma categories (conflicting vs corresponding interests, Fig. 2, p. 6) as names
  for behavioural measures.

## Map fields
- Skills measured: cooperating, competing, deceiving-detecting (feinting in Running with Scissors,
  Chicken, Prisoner's Dilemma scenarios), other (coordination on conventions, reciprocity, resource
  sharing, teamwork).
- Scoring: rules (environment reward, focal per-capita return).
- Agents: many (2–16 per substrate, mostly about 8).
- Opponents: learned agents (pre-trained RL bots, some with a scripted high-level controller).
- What it tests: capability.
- Training evaluated: multi-agent (MARL: A3C, V-MPO, OPRE, each selfish vs prosocial reward).
- Transfer measured: yes, to unseen co-players within a substrate; no transfer between substrates
  or skills.
- Models tested: A3C, V-MPO, OPRE (+ prosocial variants), plus exploiter and random baselines.
- Code released: https://github.com/deepmind/meltingpot
