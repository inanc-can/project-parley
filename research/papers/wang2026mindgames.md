---
id: wang2026mindgames
title: "MINDGAMES: A Live Arena for Evaluating Social and Strategic Reasoning in Multi-Agent LLMs"
authors: [Kevin Wang, Anna Thöni, Benjamin Kempinski, Bobby Cheng, Jianzhu Yao, Benjamin Finch, Leon Guertler, Viraj Nadkarni, Yihan Jiang, Aliaksei Korshuk, Alexander Buyantuev, Ilya Makarov, Siyuan Wu, Yu-Chi Cheng, Yan-Ru Ju, Ti-Rong Wu, I-Hsuan Chu, Yu-Yu Yang, I-Chen Wu, Yitian Huang, Qinlu Cao, Yiheng Sun, Yuhong Dai, Hongkun Yao, Jingxuan Fu, Jiwei Zhang, Hao Liao, Mossimo Ebeling, Govind Arun, Sadhvik Bathini, Mihir S Arya, Avinash Anish, Aditya Ranjan, Kirtana Sunil Phatnani, Paval KS, Vrushali Mehta, Aravind S, Nikhil Arora, Tanya Upadhyay, Amol Bandagale, Yuan Lu, ChunEn Hsiao, YuTing Lin, Arvin Chung, Jerry John Thomas, Mathieu Laurière, Leshem Choshen, Yoram Bachrach, Pramod Viswanath, Maria Polukarov, Cheston Tan, Tal Kachman, Atlas Wang]
year: 2026
arxiv: "2605.29512"
venue: arXiv preprint (v1, 28 May 2026); report of the NeurIPS 2025 MindGames competition
code: https://github.com/mind-games-challenge/mindgames-starter-kit
read: full
relevance: high
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: null
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 48 pages (main text pp. 1–20, contributors p. 24, appendices A–J pp. 25–48) on
2026-11-15; figures (TrueSkill time series, similarity matrices, role boxplots) only as far as their
captions and text describe them. Turn protocol differs by game (Blotto and IPD decisions
simultaneous, Codenames sequential, Mafia day/night phases), so `turn_protocol` is left empty;
2 to 6 players per game. Dataset: https://huggingface.co/datasets/mindgameschallenge/MGC2025.

## Question
Can a live, multi-game arena on TextArena measure LLM agents' social and strategic reasoning
(opponent modelling, trust/betrayal, cooperative signalling, deception), and what do the first
competition's 944 agents show about what works and about what the leaderboard actually measures?
(pp. 1–3)

## Setup
- **Four games** chosen along information structure × incentive alignment (§3.2 pp. 5–6; Fig. 1
  p. 2): **Colonel Blotto** (2 players, zero-sum, no talk, up to 9 rounds, 20 units over 3 fields);
  **3-player Iterated Prisoner's Dilemma** (free chat then private C/D per opponent, 5–10 rounds,
  pairwise payoffs 3/1/5/0); **Codenames** (2v2, spymaster one-word clue + operative guesses);
  **Secret Mafia** (6 players, 2 Mafia, Doctor, Detective, 2 Villagers, day talk + vote).
- **Scoring is terminal reward only**, ±1 (§3.4 p. 7). Note IPD: +1 goes "to the player(s) with
  the highest total score and −1 to all others" (p. 7) — so the mixed-motive game is scored as
  relative standing, which makes defection the winning line.
- **Invalid actions** handled per game (App. C Table 8 p. 38): IPD silently replaces invalid moves
  with `[cooperate]`; Blotto and Mafia allow one retry, then forfeit/elimination; Codenames illegal
  clue = immediate loss; Mafia Doctor/Detective errors silently corrected.
- **Tracks/divisions** (§3.3 p. 6): Generalization Track (aggregate over Blotto, IPD, Codenames) and
  Social Deduction Track (Mafia), each with Efficient (open-weight ≤9B) and Unlimited divisions.
  Stage I open ladder (Jul–Oct 2025), Stage II frozen submissions, reset ratings, minimum 30
  games per Generalization game and 50 Mafia games (App. I p. 46).
- **Rating**: TrueSkill (μ=25, σ=25/3), with cumulative reward reported alongside (p. 6).
- **Scale**: 944 submitted agents from 76 teams; 29,571 games, 94,132 player trajectories, 243M
  tokens (Table 2 p. 5) released CC-BY-4.0 with turn-level observations, actions, rewards (§3.5).
- **Participants' methods** (App. A pp. 25–33) span RL (In2AI: RLOO on Qwen3-8B, no KL, opponent
  curriculum gpt-oss-120B → GPT-5/Gemini 2.5 Pro/Grok-4/Qwen3-235B), SFT (RLGaming Llama-3.1-8B
  LoRA on rule-based + PPO + GPT traces; Odyssean No-CoT SFT → CoT-SFT from Qwen3-235B → GRPO),
  code-augmented prompting (STARS PAL + constrained decoding), multi-agent scaffolds (Phoebus
  status/action agents; Revac reviewer/action + social alignment graph + tone selector), and a
  6.8M-parameter graph-attention policy distilled from LLM teachers (Team GB).
- **MG-Ref**: frozen reference pool of top Stage II Efficient agents + deterministic factorial
  offline schedule, 198 games per new agent, references' ratings held fixed (§5.4 pp. 16–18;
  App. J pp. 47–48).

## Findings
- **Leaderboard validity differs by game.** Stage II games with ≥1 error: Blotto 8.5%, Codenames
  38.6%, IPD 0.0%, Mafia 50.3% (Table 4 p. 11); Stage I: 16.5%, 85.4%, 0.0%, 77.9% (Table 10 p. 39).
  IPD's 0% is partly an artifact of the auto-cooperate default (p. 12).
- **Error-survival confound in Mafia**: top two Efficient Mafia agents caused errors in 4/130 and
  10/132 games but witnessed opponent errors in 129/130 and 131/132; each had only 1 fully clean
  game (Table 5 p. 13). Terminated Mafia games end after <3 turns vs 8–12 expected (p. 13; Fig. 4
  p. 14). Proposed rule of thumb: error rate >~30% and median termination depth < half of expected
  length → read rank as robustness to opponent failure, not skill (p. 13).
- **Codenames mixes skill and rule following**: top-3 clean-game rates 39–45%, self-forfeit
  5.8–24.6% (p. 13); every recorded error is a fatal illegal clue (339 in Stage II, Table 4).
- **TrueSkill vs reward disagree**: Generalization TrueSkill compresses to ≈0..+50 while
  cumulative reward spans ≈−120..+170; in Mafia, Efficient agents gain TrueSkill at near-zero
  reward while Unlimited agents show the inverse (pp. 14–15; Fig. 5).
- **Per-game rankings diverge within one track**: In2AI (Efficient) is 1st on Blotto (36.8, win
  86.7%) and IPD (39.3, win 97.9%) but 3rd on Codenames (26.6); STARS is 2nd on Blotto but wins
  17.8% of IPD; RLG-8B wins 48.1% Blotto, 1.9% IPD, but is 1st on Codenames (Tables 12–14 pp.
  40–41). A single "Generalization" score hides this.
- **Training vs scaffolding by division** (self-reported designs, Table 3 p. 9): in Efficient,
  4 of 6 top entries fine-tune (1 RL, 3 SFT); in Unlimited, 5 of 6 use no task training (p. 9).
  In2AI's single RL-trained Qwen3-8B checkpoint ranks 1st in both Generalization divisions, ahead
  of prompted GPT-5 (p. 9) — one model trained jointly on three games, not per game.
- **Scaffolding without training hurts** (team-reported, own setups): RLGaming Mafia win rate base
  21.7% → +prompt 25.0% → +memory/deduction 16.7% → +SFT on gpt-oss-120B traces 45.0% (App. A.2.1
  p. 29); Tungsten's memory agent did worse than its thinking agent (p. 29).
- **Narrow training overfits to opponents**: RLGaming SFT agents overfit Blotto opponent patterns
  and IPD agents collapsed to all-defect; Codenames "least improvable via SFT" (App. A.1.3 p. 27).
  DeceptionNet abandoned self-play PPO because performance degraded from the imitation baseline
  (p. 32). Curation beat volume: score-5-only filtering kept 20% of data and produced stronger
  agents (p. 9).
- **Deception asymmetry**: Mafia side wins 88–96% across all RLGaming configurations while the
  Villager side rises 16% → 60% with structure (p. 31); Phoebus multi-agent scaffold 15.0% →
  70.0% (Villager 8.3% → 75.0%, Mafia 25% → 62.5%) (p. 30). Mafia role has positive role advantage,
  Codenames roles ≈0 (§5.3 pp. 15–16). Several teams report models reluctant to lie as Mafia (p. 10).
- **Leakage fixed architecturally**: private reasoning block with harness extracting only the
  public action prevents Mafia role leaks without fine-tuning (p. 12; App. A.2.2).
- **Behavioural similarity** (embeddings of responses): IPD all pairs >0.8; top Blotto agents
  cluster; Mafia top agents split into two styles at similar TrueSkill (§5.2 pp. 14–15).
- **Non-LLM policy viable**: 6.8M-parameter GNN reaches 78.4% Blotto win rate [77.36, 79.44] over
  1,000 games (team-reported, p. 28).

## Limitations
- Competition report, not a controlled study: training-vs-prompting conclusions come from
  heterogeneous team submissions with different models, budgets and self-reported ablations run in
  each team's own setup (App. A). No matched comparison of harnesses.
- **IPD is scored winner-take-all** (p. 7), so "cooperation" is not rewarded as such; together with
  the auto-cooperate default for invalid moves it measures relative standing, not joint gains.
  No welfare, surplus or deal measure anywhere.
- Mafia leaderboard is error-dominated in this cycle (authors' own conclusion, p. 19); Codenames
  partly so.
- Only four games; one negotiation-like channel (IPD chat, Mafia debate); no bargaining with
  private values.
- Small Stage II pools ("relatively small", sparse matchmaking, p. 46); Unlimited division
  matchmaking differed from Efficient, so cross-division comparisons are qualitative (p. 8). Some
  games are missing from the public dataset (p. 40).
- No humans; no propensity measures; capability only.
- MG-Ref Mafia runs with five identities, below the 15-agent pool the authors think stable (p. 48).

## Relevance to Parley
- For the **map (a)**: a live multi-game arena with released trajectories and an offline reference
  protocol. Covers competing (Blotto), cooperative signalling (Codenames), talk-then-act social
  dilemma (IPD, but scored relatively) and deception/deduction (Mafia). Its main methodological
  contribution is a **validity audit**: per-game error rates, caused/witnessed/forfeit attribution
  and termination depth. Any map entry for a live-arena benchmark should carry these columns.
- For the **transfer study (b)**: this is the only paper among the notes where many independent
  teams applied **prompting, SFT, RL and multi-agent scaffolds** to the same games, and it reports
  harness patterns: RL/SFT wins at ≤9B, scaffolding wins at frontier scale, scaffolds need matched
  training, narrow training overfits to opponents (pp. 8–12). But it does not measure transfer:
  In2AI trained one checkpoint on all three Generalization games with no single-game ablation, and
  nobody tested whether Mafia training moves Codenames or IPD play. The per-game rank reversals
  (Tables 12–14) show the games measure different things — the precondition for a transfer study,
  as in [[he2026socialgym]].
- The RLGaming IPD collapse to all-defect under SFT (p. 27) is a concrete example of the
  interference the student wants to measure: training for winning in one game pushes play away
  from cooperation; here the winner-take-all IPD scoring rewards that, so the benchmark cannot tell
  it apart from improvement.
- Compared with [[he2026socialgym]]: both are rule-scored multi-game suites; SocialGym runs a
  controlled tournament of 10 fixed models with split-half reliability; MINDGAMES runs an open
  competition with many training approaches but uncontrolled designs and error-confounded games.
  Both score by relative standing, not joint outcome.
- Compared with [[smith2025evaluating]] (cited as [36]): same lineage of NeurIPS competitions with
  TrueSkill/Elo; Concordia scores mutual gain with held-out scenarios, MINDGAMES scores wins. The
  In2AI team (Korshuk, Buyantuev, Makarov) entered both: 1st in MINDGAMES Generalization, and
  `in2ai_megamind` 1st in Concordia's evaluation Elo but below the rational baseline in the final
  cross-play (see that note) — a hint that what wins one arena need not carry to another.
- Compared with [[liu2025spiral]] and [[yuan2025marshal]]: In2AI's recipe (RLOO, per-environment
  advantage normalization, curriculum over external opponents rather than self-play, p. 25) is a
  practical multi-game RL recipe to compare with self-play RL; DeceptionNet's failed self-play PPO
  (p. 32) is a counterpoint.
- The error-as-forfeit confound matches a known Parley problem: provider or format failures that
  look like strategic outcomes. Parley should log caused vs witnessed failures the same way.

## Ideas to borrow
- Report **Clean / Caused / Witnessed / Self-forfeit / Opp-forfeit** per agent and game, and the
  game-level error rate + median termination depth diagnostic (Table 5 p. 13; p. 13).
- Report **cumulative reward next to the rating**; treat metric choice as a design decision (p. 19).
- **Frozen reference pool with fixed ratings** and a deterministic seat/role-balanced schedule so
  new agents (e.g. post-training checkpoints) are scored against the same opponents (App. J).
- Never auto-correct invalid actions to a substantive move (IPD default `cooperate` inflates
  cooperation); log invalid strings instead (App. C).
- Score cooperative games on joint outcome, not winner-take-all, if the study is about whether
  training on competition erodes cooperation.
- Private-reasoning / public-action separation in the harness as a leakage control (p. 12).
- Use the released 29,571-game corpus as SFT/RL data for single-game training arms, then test on
  the other games — the transfer experiment the paper does not run.

## Map fields
- Skills measured: competing (Blotto), cooperating (Codenames signalling; IPD nominally, but scored winner-take-all), deceiving-detecting (Mafia), persuading (Mafia debate, IPD chat), other: rule adherence / opponent modelling
- Scoring: rules (terminal ±1 rewards, TrueSkill)
- Agents: many (2–6 per game)
- Opponents: learned agents / LLM (other submitted agents and organizer baselines in a live pool)
- Tests: capability
- Training evaluated: prompting / SFT / RL / multi-agent (by competing teams, uncontrolled; self-reported ablations)
- Transfer between skills measured: no (one RL checkpoint trained on all three Generalization games, no single-game ablation or cross-game test)
- Models tested: participant agents mainly on Qwen3-8B, Llama-3.1-8B, Phi-3-mini, GPT-5, GPT-5-mini, gpt-5-nano, gpt-oss-120b, Gemini 2.5, plus a 6.8M-parameter GNN policy
- Code released: https://github.com/mind-games-challenge/mindgames-starter-kit (dataset https://huggingface.co/datasets/mindgameschallenge/MGC2025)
