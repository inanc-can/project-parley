---
id: duan2024gtbench
title: "GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations"
authors: [Jinhao Duan, Renming Zhang, James Diffenderfer, Bhavya Kailkhura, Lichao Sun, Elias Stengel-Eskin, Mohit Bansal, Tianlong Chen, Kaidi Xu]
year: 2024
arxiv: "2402.12348"
venue: arXiv preprint (v2, 10 Jun 2024)
code: https://github.com/jinhaoduan/GTBench
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 29 pages of arXiv v2 (main text pp. 1–10, appendix pp. A15–A29) on 2026-11-15, as
extracted text. The leaderboard screenshots (Figs. A8–A9) and the bar charts (Figs. 2–4, A6) were
not looked at as images, so numbers come from tables and prose only. The v2 PDF says "Preprint. Under
review." The GAMA-Bench paper ([[huang2024gamabench]], p. 11) cites it as NeurIPS 2024 (vol. 37) with
"capabilities" in place of "limitations" in the title; that venue was not checked against DBLP.
The repo is the local submodule `code/gtbench`. Most games alternate turns, but the Iterated
Prisoner's Dilemma and Blind Auction are simultaneous, so `turn_protocol: strict` is approximate.

## Question
Where does LLM strategic reasoning break down when games are sorted by a standard game-theory
taxonomy? How do LLMs compare with conventional solvers (MCTS, Tit-for-Tat), and with each other?
Do code pretraining, model size or reasoning prompts (CoT, SC-CoT, ToT) help? (pp. 1–3)

## Setup
- **10 two-player games, all built on OpenSpiel** (Table 1 p. 4; App. A1 p. A15): Tic-Tac-Toe,
  Connect-4, Breakthrough (board cut to 3×8), Nim (piles 1-3-5-7), Kuhn Poker, Liar's Dice (1 die
  each), Blind Auction (first-price sealed bid), Negotiation (Deal-or-No-Deal item split, from
  [[lewis2017deal]]), Pig, Iterated Prisoner's Dilemma (App. A2 pp. A15–A17).
- **Taxonomy on three axes**: complete vs incomplete information, dynamic vs static,
  probabilistic vs deterministic; plus "preferred ability" tags: board strategy, bids,
  collaboration, bluff, math (Table 1 p. 4; App. A2.2 p. A17).
- **Every action is a structured token from a legal-move list** (e.g. `<C2R2>`, `<Bet>`,
  `<pile:x, take:y>`). Even in Negotiation the "utterance" is a numeric claim `<Utterance: [a,b,c]>`
  that "does not mean your real intent" (App. A5.4 p. A22). **There is no free-text dialogue**.
- **Opponents**: MCTS with 1,000 simulations for most games, Tit-for-Tat for the IPD, and a Random
  agent as a sanity check. The Random agent is left out for Negotiation and the IPD (p. 5; p. 7).
- **LLM agents** = backbone × reasoning: Prompt, CoT, SC-CoT (5 paths, majority vote), ToT
  (3 candidates for generation and for voting) (p. 5; App. A5.5 pp. A22–A23).
- **Models**: GPT-3.5-turbo-1106, GPT-4-0613, Llama-3-70b-Instruct, Llama-2-70b-chat,
  CodeLlama-34b-Instruct, Mistral-7b-Orca, Deepseek-LLM-67b/7b-chat, Deepseek-Coder-6.7b-instruct
  (p. 6; Table 2 p. 7). Temperature 0.2, 1,024 max tokens. 50 valid matches per pairing, each side
  first in 25 of them (p. 6).
- **Metrics**: Normalized Relative Advantage NRA ∈ [−1, 1], which compares summed scores (win = 1,
  draw = 0.5 in zero-sum games, reward in non-zero-sum games) (p. 4). Elo for zero-sum games uses
  K = 20 from a start of 1,500 (App. A7 p. A24). Regret is reported for Blind Auction and the IPD
  (App. A10 p. A27), and Pareto efficiency for Negotiation and the IPD (p. 9).
- **LLM-vs-LLM**: every agent plays GPT-3.5-turbo with the Prompt agent as a common opponent; the
  full NRA matrix is in Fig. A6 (p. A18), and Elo is in Table 6 (p. 8).
- Sanity check: every LLM agent has a ≥90% completion rate. A match counts only if every move is
  legal, so illegal-move matches are thrown out and re-run, not scored as losses (App. A5.6 p. A23;
  Table A7).

## Findings
- **Complete-information deterministic games are a wall**: against MCTS, *every* LLM agent with
  every reasoning method gets NRA = −1 on Tic-Tac-Toe, Connect-4, Breakthrough and Nim, i.e. it
  "can barely win even a single match". Against Random, all LLMs are clearly positive, and GPT-4
  with CoT is best (p. 6; Fig. 2).
- **Probabilistic and incomplete-information games are near parity**: against MCTS/TfT, NRA is
  close to 0 for Kuhn Poker, Blind Auction, Negotiation, Pig and the IPD. GPT-4 beats MCTS on Kuhn
  Poker. Liar's Dice is the exception (≈ −1), because two players with one die each is close to
  complete information (p. 7; Fig. 3).
- **Code pretraining helps** (avg NRA vs GPT-3.5-turbo/Prompt): CodeLlama-34b −0.01 vs
  Llama-2-70b-chat −0.20; Deepseek-Coder-6.7b −0.03 vs Deepseek-LLM-67b −0.05 and -7b −0.08;
  GPT-4 0.13 and Llama-3-70b 0.04 are the top two (Table 2 p. 7).
- **Reasoning prompts are a double-edged sword**: against GPT-3.5/Prompt, CoT is flat for GPT-4
  (0.13 → 0.13), slightly up for GPT-3.5 (0.00 → 0.02) and Llama-3-70b (0.04 → 0.07), and down for
  CodeLlama-34b (−0.01 → −0.09) and Llama-2-70b (−0.10 → −0.23) (Table 3 p. 7). Against Random,
  only Mistral-7b-Orca gains much from CoT (Fig. 4 p. 7). All five alternative CoT wordings tried on
  GPT-3.5 score below the plain Prompt agent (App. A8 pp. A24–A25; Fig. A7).
- **Open vs closed models**: Llama-2-70b and CodeLlama-34b fail on Breakthrough, the game with the
  largest state space. With Breakthrough removed, CodeLlama's avg NRA rises from −0.01 to 0.08,
  while Llama-3-70b holds up there (Table 4 p. 8).
- **Elo leaderboard (LLM vs LLM, 5 zero-sum games)**: GPT-4 1592, Llama-3-70b 1577, GPT-3.5 1514,
  CodeLlama-34b 1462, Llama-2-70b 1458, Mistral-7B 1393. Rankings change by game: CodeLlama is
  *first* on Tic-Tac-Toe (1590) but fifth on average, and Llama-3-70b leads on Kuhn Poker (1625) and
  Liar's Dice (1695) (Table 6 p. 8).
- **Error profile** (GPT-4 with CoT vs solvers, 157 hand-labelled turns from 50 matches): factual
  errors (a plan the chosen move cannot carry out) 45.1%, endgame misdetection 33.3%,
  overconfidence 15.7%, misinterpretation 9.8%, calculation 9.8% (Table 5 p. 8). Plans are
  reasonable, but moves don't match them (p. 8).
- **Game-theoretic properties** (vs GPT-3.5/Prompt): GPT-4 has the lowest regret in Blind Auction.
  In the IPD, CodeLlama has lower regret than GPT-4, because GPT-4 stays `<Silent>` (cooperates)
  more often; the authors guess this comes from alignment toward morality or system reward (p. 9;
  Fig. 5a). In Negotiation, Llama-2-70b and CodeLlama accept unfair splits, while GPT-4 and Mistral
  rarely reach agreement and hold out for Pareto improvements (p. 9; Fig. 5b). The repeated PD
  shows Pareto improvement over rounds, which the single-shot PD does not (Fig. 5c).
- **Temperature** (20 matches, 0.2 vs 0.4/0.6/0.8): higher temperature hurts in deterministic games
  (GPT-3.5 −0.10 → −0.34 at 0.8), and the effect in probabilistic games depends on the model
  (Table A8 p. A24).

## Limitations
- **No language interaction**: every move is a token from a legal-move list, and Negotiation's
  "utterance" is a numeric claim, so nothing tests persuasion, framing or dialogue. The authors
  say this is deliberate: verbal games "mask" reasoning gaps (p. 2).
- **Two players only**. No coalitions and no multi-party dynamics.
- **Regret is defined ad hoc**: in the IPD, regret = 0 whenever the player Testifies, so
  cooperating is counted as error even in the repeated game (App. A10.2 p. A27). Low regret
  therefore rewards defection, and GPT-4's "worse" IPD regret is a cooperation propensity, not
  a reasoning failure.
- **MCTS acts as a ceiling, not a baseline**: in complete-information games, NRA = −1 for every
  model leaves no room to separate them (p. 6). Against MCTS in the other games, the authors give
  only a qualitative "close to 0" (p. 7).
- **Statistics are thin**: 50 matches per cell, no confidence intervals in the tables, and error
  bars only "over different reasoning methods" (Fig. 3). Matches with illegal moves are dropped and
  re-run, which hides instruction-following failures (App. A5.6).
- LLM-vs-LLM uses a single common opponent (GPT-3.5/Prompt), not a round robin. NRA against one
  anchor can reorder models in ways that do not carry over to other opponents.
- Models are old (GPT-4-0613, Llama-2/3), there are no reasoning models, nothing is trained, and
  prompt sensitivity is admitted in the Limitations (p. 9).
- The code uses LangChain (`requirements.txt`, `gamingbench/chat/chat.py` in `code/gtbench`). The
  paper does not mention it.

## Relevance to Parley
- **Evidence that "strategic reasoning" splits by game structure**: the same models go from
  parity (probabilistic games) to total failure (complete-information games, NRA −1) (pp. 6–7),
  and Elo rankings reorder by game (Table 6). This early, small version of the
  family-profile result in [[he2026socialgym]] (economic vs overall Spearman 0.04) is a
  precondition for any transfer or interference question: the skills are not one dimension.
- **Solver opponents**: the MCTS/TfT opponent gives a fixed, non-LLM reference that does not drift
  as models improve. For Parley, a solver or scripted opponent is a stable *anchor* (compare the
  random anchor in [[he2026socialgym]]). It only works as a *baseline* in games where it is not
  near-optimal; where it is, use it as a ceiling.
- **Its game set became the RL training set of later work**: [[liu2025spiral]] (TicTacToe, Kuhn
  Poker, simple negotiation via TextArena) and [[yuan2025marshal]] (Tic-Tac-Toe, Kuhn Poker → held-
  out Leduc) train on GTBench-type games and evaluate on games like these. GTBench itself trains
  nothing (Impact Statement, p. 10), so it shows where the gap was before self-play RL.
- **Negotiation here is a toy**: a structured Deal-or-No-Deal split with numeric "utterances". It
  says nothing about language-level bargaining as in [[abdelnabi2023cooperation]] or
  [[bianchi2024negotiationarena]].
- The IPD regret definition is a warning for Parley's metrics: a "rationality" score that counts
  cooperation as error mixes capability with propensity. [[huang2024gamabench]]'s Betraying
  games have the same problem.

## Ideas to borrow
- **The 3-axis taxonomy** (information × timing × chance) as a checklist when choosing Parley game
  templates, so a suite covers each cell.
- **Reasoning style as a factor** (Prompt / CoT / SC-CoT / ToT) crossed with model. CoT helping
  strong models and hurting weak ones (Table 3) is a cheap interaction worth replicating.
- **Error-profile coding** of a sample of turns (factual error, endgame misdetection,
  overconfidence, misinterpretation, calculation) to explain *why* a score is low (Table 5).
- **Solver/scripted anchor plus random floor** per game, so scores have fixed reference points.
- **Swap first mover** within each pairing (25/25) to cancel first-player advantage (p. 6).
- Report illegal-move rates instead of re-running failed matches.

## Map fields
- Skills measured: competing (zero-sum board/card games, bluffing in Kuhn Poker/Liar's Dice), cooperating (IPD), negotiating value (structured item split), other (board strategy, math, bidding)
- Scoring: rules (win/draw/payoff → NRA, Elo, regret); error profile hand-labelled by humans
- Agents: 2
- Opponents: solver (MCTS, Tit-for-Tat), scripted (Random), LLM (GPT-3.5/GPT-4 Prompt agent as common opponent)
- What about the model it tests: capability (IPD silence rate read as a side effect of alignment, p. 9)
- Training evaluated: prompting (Prompt / CoT / SC-CoT / ToT; five CoT wordings; temperature)
- Transfer between skills measured: no
- Models tested: GPT-4-0613, GPT-3.5-turbo-1106, Llama-3-70b-Instruct, Llama-2-70b-chat, CodeLlama-34b-Instruct, Mistral-7b-Orca, Deepseek-LLM-67b-chat, Deepseek-LLM-7b-chat, Deepseek-Coder-6.7b-instruct
- Code released: https://github.com/jinhaoduan/GTBench (leaderboard https://huggingface.co/spaces/GTBench/GTBench)
