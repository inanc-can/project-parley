---
id: guertler2025textarena
title: "TextArena"
authors: [Leon Guertler, Bobby Cheng, Simon Yu, Bo Liu, Leshem Choshen, Cheston Tan]
year: 2025
arxiv: "2504.11442"
venue: arXiv preprint (v2, 24 May 2025)
code: https://github.com/LeonGuertler/TextArena
read: full
relevance: high
topics: [game-theoretic-evals, negotiation-benchmarks, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: null
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 13 pages (main text pp. 1–6, appendix A–B pp. 8–13) on 2026-11-15, including Figures 1–2
as images. It is a short system/resource paper: no experimental section, no tables of results;
the only model results are two figures. Turn order differs by game, so `turn_protocol` is left
empty; 1 to 15 players per game. Humans appear pooled as one "Humanity" player.

## Question
Can a large, extensible collection of competitive text games with a Gym-style interface and a live
TrueSkill leaderboard (models vs models vs humans) give a relative, non-saturating measure of LLM
skills, including social ones (negotiation, ToM, deception), and serve as an RL training source?
(pp. 1–3)

## Setup
- **Framework** (§2 p. 3): interface kept "as similar to OpenAI Gym (aka Gymnasium) … as possible",
  with stackable wrappers (e.g. `LLMObservationWrapper`); loop `env.reset` →
  `env.get_observation()` → `env.step(action)` → `env.close()` returns rewards; agents wrap
  OpenRouter etc.; `ta.make_online(...)` plays on the public server (App. B p. 12). MCP-compatible
  (acknowledgements p. 6).
- **Environments**: "57+" at submission, 74 at publication (footnote p. 2); Table 1 counts 16
  single-, 47 two- and 11 multi-player (p. 5), while the appendix tables list 16 / 43 / 12 = 71
  (Tables 2–3, pp. 11, 13). Games marked * are **not fully implemented yet**, including several of
  the social ones (BattleOfSexes, StagHunt, IntegrativeDistributiveNegotiation, MonopolyGame, Jaipur,
  DuopolisticCompetition, EscalationGame, Pit). Some are taken from GameBench, LAMEN and GTBench.
- **Skill tags** (§4 p. 4): each game is tagged with up to five of 10 soft skills with weights; a
  model's skill score is the weighted average of its per-game ratings (weights not given in the
  paper; the tables show binary marks).
- **Online evaluation** (§4 pp. 4–5): TrueSkill (μ=25, σ=25/3), chosen because it handles teams and
  varying player counts and converged faster than Elo "in our experiments" (no numbers). 283
  models evaluated online, 64 official hosted models; no rules on submissions.

### Games grouped by tagged skill (Tables 2–3; * = not fully implemented)
Social skills:
- **Persuasion (17)**: Blind Auction, Character Conclave, Codenames, Negotiation (multi), Poker,
  Two Rooms and a Boom, Diplomacy, SecretMafia, BattleOfSexes*, Debate,
  IntegrativeDistributiveNegotiation*, Jaipur*, LetterAuction, MonopolyGame*, ScenarioPlanning,
  SimpleBlindAuction, TruthAndDeception.
- **Bluffing (13)**: Liar's Dice, Poker, SecretMafia, DontSayIt, DuopolisticCompetition*,
  EscalationGame*, Jaipur*, KuhnPoker, LetterAuction, MonopolyGame*, SimpleBlindAuction,
  SimpleNegotiation, TruthAndDeception.
- **Theory of Mind (34)**: all of the multi-player social games (Blind Auction, Character Conclave,
  Codenames, Liar's Dice, Negotiation, Poker, Two Rooms and a Boom, Diplomacy, SecretMafia), GuessWho,
  TwentyQuestions, and two-player AirLandAndSea*, BattleOfSexes*, Brass*, Debate, DontSayIt,
  DracoGame*, DuopolisticCompetition*, EscalationGame*, IntegrativeDistributiveNegotiation*,
  IteratedPrisonersDilemma, Jaipur*, KuhnPoker, MonopolyGame*, PrisonersDilemma, ScenarioPlanning,
  SimpleBlindAuction, SimpleNegotiation, SpiteAndMalice, StagHunt*, Stratego, Taboo, TriGame*,
  TruthAndDeception.
- **Adaptability (21)**: Character Conclave, Diplomacy, SecretMafia, GuessWho, Hangman, LogicPuzzle,
  AirLandAndSea*, Debate, DontSayIt, HotColdGame*, IntegrativeDistributiveNegotiation*,
  IteratedPrisonersDilemma, MonopolyGame*, PrisonersDilemma, SimpleNegotiation, SpellingBee,
  SpiteAndMalice, Stratego, Taboo, WaitGoGame*, WordChains.
- **Uncertainty Estimation (26)**: Blind Auction, Liar's Dice, Pit*, Poker, GuessTheNumber,
  GuessWho, Minesweeper, TwentyQuestions, AirLandAndSea*, Battleship, Brass*, EscalationGame*,
  HotColdGame*, IteratedPrisonersDilemma, Jaipur*, KuhnPoker, LetterAuction, MonopolyGame*,
  PigDice, PrisonersDilemma, SeaBattle*, SimpleBlindAuction, SpiteAndMalice, StagHunt*, Stratego,
  TruthAndDeception.
Non-social skills (counts; mostly puzzles and board games): Strategic Planning 43, Logical
Reasoning 43, Pattern Recognition 26, Memory Recall 18, Spatial Thinking 13 (e.g. Chess, Checkers,
ConnectFour, Othello, Tak, Sudoku, Wordle, Minesweeper, TowerOfHanoi, Snake, Surround).
Note: negotiation and cooperation are **not** tags of their own; negotiation games sit under
Persuasion/Bluffing/ToM, and the cooperation dilemmas (PD, IPD, StagHunt, BattleOfSexes) under
ToM/Uncertainty.

## Findings
- **Soft-skill radar** (Fig. 1 p. 1): Humanity above claude-3.5-sonnet, qwen-plus and gpt-4o on all
  10 skills, but each axis is normalised separately and no numbers are given.
- **Per-game TrueSkill** (Fig. 2 p. 2, "preliminary", read off the bars): Humanity first on
  DontSayIt (~34) and TicTacToe (~35.5), second on Poker behind claude-3.7-sonnet-thinking, third on
  Snake, mid-pack on SecretMafia (claude-3.7-sonnet first, ~38); models include o3, o3-mini,
  claude-3.7-sonnet (± thinking), grok-3-beta, gemini-2.5-pro-preview-03-25, deepseek-chat-v3-0324,
  gpt-4o-2024-11-20. Caption: results mix game skill with rule/format understanding; some reasoning
  models reveal their cards or roles.
- **Positioning** (Table 1 p. 5): only framework among 9 compared with all four of Gym API, online
  evaluation, model-vs-model and model-vs-human.
- No other quantitative results: no reliability, no per-skill validation, no rating CIs.

## Limitations
- A resource paper: no controlled experiments, no analysis of whether skill tags measure distinct
  abilities; tags are author-assigned and the aggregation weights are unpublished.
- Humans are pooled into one "Humanity" rating with unknown skill and sample size.
- Leaderboard is live and open: opponent pool, model versions and sample sizes change, so ratings
  are not reproducible snapshots.
- Many social games were unimplemented at the time (*), and the negotiation games are not described
  beyond one line each (no reservation values, surplus or welfare scoring mentioned).
- Terminal win/loss rewards make mixed-motive games relative-standing contests (the same issue
  [[wang2026mindgames]] reports for its IPD scoring).
- **RL training is claimed as a use but not done here**: listed as future direction (p. 6).

## Relevance to Parley
- **The ready multi-game training environment**: if the student needs one Gym-style API across
  many social games for (b), this is it. Already used for exactly that: [[liu2025spiral]] trained
  by self-play RL on TextArena's TicTacToe, Kuhn Poker and Simple Negotiation (Oat + vLLM +
  TextArena), and [[wang2026mindgames]] (the NeurIPS 2025 MindGames competition) is built on
  TextArena with Blotto, 3-player IPD, Codenames and SecretMafia, where teams used RL and SFT.
  So the plumbing for "train on game A, test on games B…Z" exists and has been exercised.
- **For the map (a)**: one row covering the widest game catalogue with a human anchor; but it is a
  catalogue, not a measurement study. Its skill profile (Fig. 1) is exactly the kind of
  "direction" vector the student would compare before and after training, yet the paper never
  checks that the directions are distinct — [[he2026socialgym]] does that (family Spearman
  0.02–0.88) and should be the reference for whether such profiles are meaningful.
- **What it leaves open for (b)**: no training results, no transfer or interference measures, no
  absolute payoff/surplus scores for negotiation or cooperation, no propensity measures. The skill
  tags overlap heavily (ToM in 34 games), so "train on Persuasion games, test on Bluffing games" would
  need a cleaner partition than the authors' tags.
- Compared with [[bianchi2024negotiationarena]] and [[zhang2026terms]]: those score negotiation
  with values and deal quality; TextArena's negotiation games only feed a win/loss TrueSkill.
  Compared with [[duan2024gtbench]] / [[huang2024gamabench]]: TextArena reuses several GTBench games
  (KuhnPoker, Nim, PigDice, Breakthrough, SimpleBlindAuction) inside a trainable API.

## Ideas to borrow
- Gym-style `reset/get_observation/step/close` loop with wrappers as the harness interface, so the
  same environment serves prompting, SFT data generation and RL.
- TrueSkill for mixed team/free-for-all games with varying player counts.
- Skill-tag weighted profiles, but validated (split-half reliability, between-tag correlation as in
  [[he2026socialgym]]) before use.
- A human-play UI on the same environments for a human anchor.

## Map fields
- Skills measured: negotiating value (SimpleNegotiation, Negotiation, IntegrativeDistributiveNegotiation*), cooperating (PD, IPD, StagHunt*, Codenames), competing, persuading, deceiving-detecting (bluffing, SecretMafia, TruthAndDeception), other: theory of mind, strategic planning, spatial, logic, memory, uncertainty estimation, adaptability (plus single-player puzzles)
- Scoring: rules (game outcomes → TrueSkill)
- Agents: 1 / 2 / many
- Opponents: LLM, human, learned agents (community-submitted models)
- Tests: capability
- Training evaluated: none (Gym-compatible API designed for RL; RL training listed as future work, p. 6)
- Transfer between skills measured: no
- Models tested: 283 models online (64 hosted); named in figures: claude-3.5-sonnet, qwen-plus, gpt-4o, o3, o3-mini, claude-3.7-sonnet (± thinking), grok-3-beta, gemini-2.5-pro-preview-03-25, deepseek-chat-v3-0324, gpt-4o-2024-11-20; plus "Humanity"
- Code released: https://github.com/LeonGuertler/TextArena
