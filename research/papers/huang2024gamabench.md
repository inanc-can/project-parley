---
id: huang2024gamabench
title: "How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments"
authors: [Jen-tse Huang, Eric John Li, Man Ho Lam, Tian Liang, Wenxuan Wang, Youliang Yuan, Wenxiang Jiao, Xing Wang, Zhaopeng Tu, Michael R. Lyu]
year: 2024
venue: ICLR 2025
arxiv: "2403.11807"
code: https://github.com/CUHK-ARISE/GAMABench
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 43 pages of arXiv v7 (6 Mar 2025, header "Published as a conference paper at ICLR 2025")
on 2026-11-15, as extracted text: main text pp. 1–11 and appendices A–M pp. 16–43. The plots
(Figs. 1–12) were not looked at as images, so numbers come from tables and prose. The arXiv script
suggests the citekey `huang2024decision`; the existing id is kept. The benchmark is called
GAMA(γ)-Bench, and the repo is the local submodule `code/gama-bench`. 6 of the 8 games are
simultaneous; Battle Royale and the Pirate Game are sequential. `human_baseline: false` because no
humans played; the paper only quotes published human means for one game (p. 9).

## Question
How good are LLMs at decisions in **multi-player, multi-round** classic games? How robust is
performance to sampling, temperature and prompt wording? Do CoT or persona prompts help? Do models
generalize when game parameters change, i.e. beyond memorized textbook settings? (pp. 1–3, 8)

## Setup
- **8 games in 3 categories** (§2 pp. 3–5):
  - *Cooperative*, where the NE is said to align with social welfare: (1) Guess 2/3 of the Average
    (0–100), (2) El Farol Bar (capacity 60%), (3) Divide the Dollar (G = 100).
  - *Betraying*, where the NE lowers welfare: (4) Public Goods (R = 2, 20 tokens), (5) Diner's
    Dilemma (prices 20/10, utilities 20/15), (6) Sealed-Bid Auction (valuations 0–200).
  - *Sequential*: (7) Battle Royale (hit rates 35–80%), (8) Pirate Game (G = 100).
- **Protocol**: 10 agents, **all copies of the same model**, temperature 1, 20 rounds for the
  simultaneous games, 5 runs (p. 5). **No communication**: each agent sees the rules and the
  history of results and answers in JSON (`{"chosen number": ...}`) (App. C pp. 20–25). Agents are
  told the total number of rounds (p. 37). Prompts were written by GPT-4 from game descriptions
  and checked by hand (App. C.1 p. 20).
- **Scoring**: a raw score per game measures distance to the NE/"optimal" action, rescaled to
  0–100 (higher is better) and averaged into an Overall score (§3 pp. 5–8; App. E p. 29, Eq. 1).
  Several choices matter for interpretation:
  - El Farol is scored only in the Implicit-information variant (p. 5, fn. 3), and the auction only
    in First-Price (p. 7, fn. 4).
  - Betraying games reward the *selfish* action: contributing 0 to the public pot, ordering the
    costly dish (pp. 6–7).
  - The auction score is the mean shading (v − b)/v, so a lower bid always scores higher, whether
    or not the agent wins (p. 7).
  - Battle Royale scores only "targets the player with the highest hit rate". The paper itself
    notes that deliberately missing can be optimal (p. 7).
  - The Pirate Game combines the L1 distance of proposals from Stewart's optimal split (96 to
    the proposer, 1 each to ranks 3, 5, 7, 9) with voter accuracy (pp. 7–8).
- **RQs**: robustness (5 runs; temperatures 0–1; 5 prompt templates rephrased by GPT-4),
  reasoning prompts (CoT; personas: cooperative, selfish, mathematician), generalizability
  (sweeps of game parameters, Table 8), leaderboard (§4 pp. 8–10).
- **Models (13)**: GPT-3.5-turbo 0613/1106/0125, GPT-4-turbo-0125, GPT-4o-0806, Gemini-1.0-Pro,
  Gemini-1.5-Pro, LLaMA-3.1 8B/70B/405B, Mixtral 8x7B/8x22B, Qwen-2-72B (p. 3). GPT-3.5 (0125) is
  the case study; full robustness appendices also cover LLaMA-3.1-70B, Gemini-1.5-Pro and GPT-4o
  (Apps. K–M pp. 38–43).
- Extras: fixed-strategy co-players (App. G pp. 36–37), a CipherChat jailbreak on GPT-4o
  (App. H p. 37), and a literature table of 16 earlier game-theory LLM papers (Table 3 p. 19).

## Findings
- **Leaderboard (Overall, mean ± sd over 5 runs)**: Gemini-1.5-Pro 69.8±1.6, GPT-4o 66.7±4.7,
  LLaMA-3.1-70B 65.9±3.3, GPT-4-turbo 62.4±2.7, Mixtral-8x22B 62.4±2.2, LLaMA-3.1-405B 61.8±4.7,
  Qwen-2-72B 56.7±3.4, LLaMA-3.1-8B 56.0±3.1, Gemini-1.0-Pro 45.7±3.4, GPT-3.5 1106/0125/0613
  45.1/44.4/42.7, Mixtral-8x7B 43.4±2.2 (Table 1 p. 2). LLaMA-3.1-405B scores below the 70B model
  because it stays home in El Farol (20.5 vs 59.7) (p. 10).
- **Per-game profiles disagree strongly**: GPT-4-turbo gets 98.1 on Divide the Dollar but 0.9 on
  Diner's Dilemma and 23.0 on El Farol. Mixtral-8x7B gets 1.2 on Divide the Dollar but 76.4 on
  Diner's Dilemma. GPT-3.5-0613 is *best* on Diner's Dilemma among the closed models (67.0)
  (Table 1 p. 2). The Overall score hides near-opposite profiles.
- **GPT-3.5 (0125) behaviour** (Overall 45.9 in the default run, p. 5): it starts at ~50 in Guess
  2/3 and then moves down (65.4). It cooperates spontaneously without communication: it
  contributes to the public pot despite a −80% return (41.2), and mostly orders the cheap dish in
  Diner's Dilemma, so it scores **4.0** there (p. 6). It rarely targets the strongest shooter (20.0)
  and never misses on purpose (p. 7). It proposes non-optimal pirate splits and votes wrongly
  (80.6) (pp. 7–8). Its decisions follow the last round's outcome more than equilibrium reasoning
  (p. 5).
- **Robustness**: across 5 runs GPT-3.5 gets 44.4±2.1; Public Goods (±8.1), Battle Royale (±11.0)
  and the Pirate Game (±7.7) are the noisy games (Table 4 p. 30). Over temperatures 0–1 the
  Overall moves 36.7–45.9 (sd 3.4), but Guess 2/3 rises from 48.0 to 65.4 (Table 5 p. 31). Prompt
  wording matters a lot: Diner's Dilemma ranges 0.0–57.0 across 5 templates (sd 23.7), Pirate
  ±14.7, Public Goods ±11.5 (Table 6 p. 32). The same pattern holds for stronger models, e.g.
  GPT-4o Battle Royale 10.0–89.5 across templates (Table 20 p. 43) and El Farol 41.7–95.0 across
  runs (Table 18 p. 42).
- **CoT raises GPT-3.5 from 45.9 to 57.9**, close to GPT-4-turbo's 62.4. Most of the gain comes
  from Diner's Dilemma (4.0 → 82.5) and Public Goods (41.2 → 56.1): **CoT makes the model
  free-ride**, which these games score as correct. The auction drops (14.6 → 5.3) (Table 7 p. 33;
  pp. 8–9). Personas: cooperative 43.7, selfish 37.8, mathematician 46.5 (Table 7).
- **Generalizability**: GPT-3.5 holds up under new parameters in Guess 2/3, Divide the Dollar,
  Diner's, Auction and Pirate, but not in El Farol (it goes ~50% of the time whatever the capacity)
  or Public Goods (contributions barely change even at R = 0) (p. 9; Table 8 p. 34). Stronger
  models break at the edge cases: in Guess-R with R = 1 (target equals the average), Gemini-1.5-Pro
  gets 5.3 and GPT-4o 22.7, against ~90–99 elsewhere (Tables 17 p. 41, 21 p. 43).
- **Human comparison (Guess-R only)**: GPT-3.5's means for R = 1/2, 2/3, 4/3 are 34.59, 34.59,
  74.92, against human means of 27.05, 36.73, 60.12 (Nagel 1995) and 36.2 (Rubinstein 2007, 2,423
  subjects). The model looks more like humans than like the NE (p. 9).
- **Fixed-strategy co-players**: against one player who always bids 91 in Divide the Dollar, the
  other agents lower their bids. Against a persistent free-rider in Public Goods, the other agents
  *raise* their contributions to make up for it (App. G p. 36). GPT-4o picks 0 at once when told
  the others play the NE, converges to 0 when told they are "smart", and plays randomly instead of
  ~33 when told they are random (p. 37).
- **Jailbreak**: CipherChat barely changes GPT-4o (Public Goods 90.91 → 88.55, Diner's 10.7 → 7.5),
  and its Dark Triad scores fall (Machiavellianism 4.6 → 3.5) (App. H p. 37; Table 9).

## Limitations
- **Self-play only**: all 10 agents are the same model; the authors list mixed-model games as
  future work (p. 37). So the score is how a population of identical copies behaves, not how one
  model does against others.
- **The score mixes capability with propensity**: in Betraying games, the cooperative choice is
  scored as error. GPT-3.5's 4.0 on Diner's Dilemma, and CoT's 78.5-point "improvement" there,
  measure willingness to defect, not reasoning (pp. 6, 9). GPT-4's low El Farol and Diner's scores
  are explained as risk aversion (p. 10). The paper calls the Betraying category a test of
  "propensity" (p. 2) but scores it as ability.
- **Several scores are proxies that can be gamed**: the auction score rewards bidding low no
  matter the outcome, and Battle Royale rewards a single heuristic the paper itself says is not
  always optimal (p. 7). In identical-copy play, the cooperative-category NE scores reward
  coordination that the copies can reach by symmetry.
- **No communication** of any kind, so nothing is measured about negotiation talk, persuasion or
  deception.
- Agents know the horizon (20 rounds), which allows end-game defection; the authors set this
  aside (p. 37).
- Prompt sensitivity is large (Diner's 0–57 across templates) and model rankings depend on
  per-game swings, yet the leaderboard reports one template.
- The GPT-3.5 (0125) aggregate appears as 45.9 (default run, p. 5) and 44.4 (5-run mean,
  Table 1). Cite which one you use. Only v7 was read, so earlier arXiv versions may differ in
  models and scores.

## Relevance to Parley
- **Multi-player social dilemmas with parameter sweeps** are a direct template for 3+-player
  Parley games. Changing parameters (Table 8) is a cheap guard against memorized textbook answers.
- **Main lesson for Parley's metrics: a "distance to NE" score is not neutral.** Here it penalizes
  cooperation, and the CoT gain is mostly a shift toward defection. Parley should report
  **welfare/joint payoff and individual payoff separately**, as GTBench's Pareto plots do
  ([[duan2024gtbench]]), and treat cooperation rate as a propensity, not an ability score. This is
  the capability/propensity gap also flagged for [[he2026socialgym]].
- **Per-game profiles diverge** (GPT-4-turbo 98 vs 1 across games; Mixtral-8x7B the reverse), the
  same multi-direction point as [[he2026socialgym]]'s family rankings. But here the divergence is
  partly built in by scoring that rewards opposite dispositions.
- Prompting moves behaviour a lot (CoT, personas, wording), but nothing is trained. Whether
  training changes cooperative vs selfish dispositions, and whether that carries over between
  categories, is open. [[liu2025spiral]] and [[yuan2025marshal]] train on zero-sum games only.
- The free-rider result (agents compensate instead of punishing, App. G) is a cheap probe of
  exploitability. It relates to Parley's [[persuasion-susceptibility]] angle: being exploitable
  by a fixed strategy, without any talk.
- Compare [[leibo2021meltingpot]] (test against held-out co-players) vs GAMA (self-play copies
  only): Parley should mix models in a game.

## Ideas to borrow
- **Parameter sweeps per game** (R, G, capacity, price/utility tuples) to test generalization and
  contamination.
- **Robustness triad** reported per game: run-to-run sd, temperature sweep, paraphrased prompt
  templates. Prompt sd turned out to be the biggest source of variance.
- **Fixed-strategy plants** (dominant bidder, persistent free-rider, "others play NE") inside an
  LLM population, to probe exploitability and belief updating.
- **Published human baselines** where they exist (Nagel, Rubinstein) next to the NE.
- Versioned leaderboard in the repo (`leadboard.md`), with each score tied to a paper version.

## Map fields
- Skills measured: cooperating (Guess 2/3, El Farol, Divide the Dollar), competing (Public Goods, Diner's Dilemma and Sealed-Bid Auction scored for self-interest; Battle Royale), negotiating value (Pirate Game propose/vote, no talk), other (equilibrium / K-level reasoning, mixed strategies)
- Scoring: rules (distance to NE / optimal action, rescaled 0–100)
- Agents: many (10 per game)
- Opponents: LLM (9 copies of the same model); scripted fixed-strategy co-players in App. G
- What about the model it tests: both (scored as capability, but Betraying-game scores largely reflect propensity to cooperate or defect)
- Training evaluated: prompting (CoT, personas, prompt paraphrases, temperature; CipherChat jailbreak)
- Transfer between skills measured: no (generalization is across parameters of the same game)
- Models tested: GPT-3.5-turbo 0613/1106/0125, GPT-4-turbo-0125, GPT-4o-0806, Gemini-1.0-Pro, Gemini-1.5-Pro, LLaMA-3.1 8B/70B/405B, Mixtral 8x7B/8x22B, Qwen-2-72B
- Code released: https://github.com/CUHK-ARISE/GAMABench
