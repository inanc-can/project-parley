---
id: shapira2024glee
title: "GLEE: A Unified Framework and Benchmark for Language-based Economic Environments"
authors: [Eilam Shapira, Omer Madmon, Itamar Reinman, Samuel Joseph Amouyal, Roi Reichart, Moshe Tennenholtz]
year: 2024
arxiv: "2410.05254"
venue: arXiv preprint (v3, 2 Mar 2026)
code: https://github.com/eilamshapira/GLEE
read: full
relevance: high
topics: [negotiation-benchmarks, game-theoretic-evals, persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 37 pages (main text pp. 1–19, appendices A–C pp. 21–37) on 2026-11-15. The model-pair
heatmaps (Figs. 1–6) carry no printed cell values in the text layer, so findings below use the
tables. Turns alternate (Alice, Bob), so `turn_protocol: strict`. Humans were paid a bonus tied to
results (`stakes` would be `money` for the human games). Persuasion is one of the game families,
not a treatment applied to a target, so `persuasion_treatment: false`; the "messages allowed vs
structured" switch is the communication treatment.

## Question
Can bargaining, bilateral price negotiation and persuasion be put on one parameterised footing
(horizon, information, communication form) with shared outcome measures (self-gain, efficiency,
fairness), so LLM results become comparable across studies? How do market parameters and model
choice shape outcomes, and how do humans compare? (pp. 1–5, 11)

## Setup
- Technion / Tel Aviv (Reichart, Tennenholtz). Two-player, sequential, rule-scored games
  (§2, pp. 5–9):
  - *Bargaining* (Rubinstein alternating offers): split M with discount factors δA, δB; efficiency
    = discounted joint payoff, fairness = 1 − 4(p − ½)²; no deal counts as fair (1) and
    inefficient (0) (p. 6).
  - *Negotiation* (bilateral trade): seller value VA = M·FA, buyer VB = M·FB, alternating prices,
    no discounting; efficiency = 1 if trade happens exactly when VA ≤ p ≤ VB (or no trade when
    VA ≥ VB); fairness = closeness to the midpoint price (pp. 6–7).
  - *Persuasion* (repeated cheap talk): seller knows quality (high w.p. p), sends a message, buyer
    buys at price 1 or not; 20 rounds; long-living buyer or myopic buyers who see only summary
    statistics. Efficiency = share of high-quality rounds sold; fairness = share of low-quality
    rounds *not* sold, i.e. a buyer-protection measure (pp. 7–8). Theory: cheap talk only has a
    babbling equilibrium; with commitment (Bayesian persuasion) the seller lies with a fixed
    probability (p. 9).
- Degrees of freedom per family: complete vs incomplete information, finite vs "infinite"
  (unknown) horizon, free text vs structured messages, scale M ∈ {10², 10⁴, 10⁶}, plus δ / F / p /
  v values. **1,320 configurations** (384 bargaining, 576 negotiation, 360 persuasion) (Table 2,
  p. 10).
- **13 LLMs**, all 169 ordered pairs incl. self-play: Claude 3.5/3.7 Sonnet, Gemini 1.5 Flash/Pro,
  Gemini 2.0 Flash/Flash-Lite, GPT-4o, GPT-4o-mini, o3-mini, Grok 2, Llama 3.1-405B, Llama
  3.3-70B, Mistral Large (Table 3, p. 10). **80.1K games, 587K decisions, 230K messages** (Table 4,
  p. 11). One fixed prompt, JSON actions; no personas or prompt variants, for budget reasons
  (App. A.2 pp. 24–26).
- **Humans**: 3,405 mTurk players (after excluding 26.8% for failed attention checks), all against
  Gemini-1.5-Flash, in 195 configurations; $2,245 paid, bonus scaled with M (App. B pp. 27, 33–34).
- **Analysis**: one linear regression per family × metric on one-hot game parameters + player
  identities; effects reported relative to a default configuration and to Gemini-1.5-Flash, with
  95% CIs (§3 p. 11; App. C pp. 34–36). Linear models match XGBoost/CatBoost RMSE (Table 9, p. 37).

## Findings
- **Market parameters matter, and differently per family** (Table 5, p. 12): longer horizons help
  efficiency and fairness everywhere. Bargaining: incomplete info + messages + unknown horizon is
  best (+2.8 efficiency, +4.4 fairness pp, CI ±0.5/±0.6); complete information *hurts*, and only
  when messages are allowed. Negotiation: complete info + unknown horizon +17.4 efficiency (±1.7);
  messages change fairness slightly. Persuasion: free-text messages **lower** efficiency and
  fairness by up to −24.7 and −22.7 pp (±2.5) (pp. 12).
- Authors' reading: language helps where there is no ground truth (bargaining, negotiation) and
  hurts where there is (product quality in persuasion), and the info × language interaction
  means classic language-free theory may not carry over (p. 12).
- **No best model; rankings depend on role and family** (Table 6, p. 13): e.g. o3-mini is worst as
  bargaining Alice (−6.9) but strong as persuasion buyer (+24.2); Mistral Large is 11th of 13 as
  Alice in bargaining but the best persuasion buyer (+28.3) and the best opponent for Alice to
  face (p. 13). Claude 3.5/3.7 Sonnet are top in bargaining.
- **Meta-game**: if users pick the LLM to represent them, the pure Nash equilibria are Claude 3.5
  (Alice) vs Claude 3.7 (Bob) in bargaining, Gemini 2.0 Flash vs Gemini 1.5 Pro (or Llama-405B vs
  Grok 2) in negotiation, Gemini 1.5 Pro vs Mistral Large in persuasion (p. 13).
- No pair maximises both efficiency and fairness against all others; self-play neither raises nor
  lowers efficiency or fairness compared with cross-play (p. 13).
- **Humans are extreme**: persuasion self-gain +20.5 (seller) and +54.8 (buyer) above all LLMs,
  negotiation the lowest (−26.6 seller, −14.5 buyer), bargaining +6.6 as Alice but −17.1 as Bob
  (Table 6, p. 13). Anchoring: a human Bob's payoff tracks the LLM Alice's first offer (r = 0.63);
  an LLM Bob's tracks a human Alice's first offer only weakly (r = 0.18) (pp. 16–17).

## Limitations
- **Two players only**, short sequential games; the authors point to group settings as future
  work (pp. 17–18).
- **No training**: no SFT, RL or prompting variants; one fixed prompt (p. 25). The authors list
  training adaptive agents as a future use (p. 18).
- Averages depend on the arbitrary configuration grid; the authors warn that numbers are
  sensitive to the configuration distribution (p. 11).
- Model effects are regression coefficients relative to Gemini-1.5-Flash and to a default
  configuration, not absolute scores; the model-pair heatmaps print no values.
- Humans only played against one model (Gemini-1.5-Flash) and in 195 of 1,320 configurations;
  mTurk with heavy exclusion (26.8%) (pp. 27, 34).
- Models are 2024–early 2025 vintage; no reasoning-heavy frontier models beyond o3-mini.
- Fairness = 1 for no deal mixes "nothing happened" with "fair split" (p. 6).
- No per-family consistency analysis (e.g. rank correlations across families), although the data
  would allow it.

## Relevance to Parley
- **Map (a)**: the cleanest rule-scored, two-player *economic* benchmark with three named social
  directions (bargaining, price negotiation, persuasion) and **joint outcome measures**
  (efficiency, fairness) next to self-gain — exactly what [[he2026socialgym]] lacks (it scores
  only relative standing). Has a large human-vs-LLM baseline, unlike most entries on the map.
- **Study (b)**: it measures *within-family* and *within-role* rankings and shows they disagree
  (Table 6), which is the precondition for a transfer study, but it never trains anything and
  never tests whether improving one family moves another. Its 80K-game dataset with per-role
  outcomes is a ready source of SFT/RL data for one family (e.g. negotiation) that could then be
  scored on the other two families with GLEE's own metrics.
- The persuasion family directly measures **resisting persuasion** as a rule outcome: the buyer's
  "fairness" (not buying low quality) is a susceptibility score, linking to
  [[persuasion-susceptibility]] and [[sadab2026receiver]] (who trained the holder's resistance).
  GLEE finding that free text *lowers* buyer protection (−12 to −25 pp) is a concrete, cheap
  harm-of-language result.
- Compared with [[bianchi2024negotiationarena]] and [[liu2026agenticpay]]: similar bilateral
  negotiation with private values, but GLEE adds the bargaining and persuasion families and the
  information/horizon/language grid. Compared with [[huang2024gamabench]] and [[duan2024gtbench]]:
  GLEE has natural-language messages, which those lack (Table 1, p. 5). Compared with
  [[zhang2026terms]]: GLEE uses LLM-vs-LLM play with a regression to separate opponent effects,
  rather than scripted verifier opponents.
- RL self-play on games ([[liu2025spiral]], [[yuan2025marshal]]) never included bargaining /
  persuasion with fairness metrics; GLEE could be the held-out economic test set for such training.

## Ideas to borrow
- **Report efficiency and fairness alongside self-gain** for every negotiation-like direction, so
  "winning" and "making the pie bigger" are separable.
- **Language on/off as a treatment** (structured vs free text) inside the same game, to show what
  talk adds or costs per direction (Table 5).
- **Regression with player-identity and configuration dummies** to compare models that played
  different configuration subsets (p. 11), and the **meta-game Nash** over models (p. 13) as a
  deployment-style summary.
- Persuasion "fairness" = share of bad items not bought: a rule-based susceptibility measure.
- Human interface on oTree with attention checks and an end-of-game quiz (App. B).

## Map fields
- Skills measured: negotiating value (bargaining, price negotiation); persuading; resisting persuasion (buyer in cheap-talk persuasion); other: outcome efficiency and fairness
- Scoring: rules
- Agents: 2
- Opponents: LLM, human
- Tests: capability (self-gain), with efficiency/fairness outcome measures that partly reflect propensity
- Training evaluated: none
- Transfer between skills measured: no
- Models tested: Claude 3.5 Sonnet, Claude 3.7 Sonnet, Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, GPT-4o, GPT-4o-mini, o3-mini, Grok 2, Llama 3.1-405B, Llama 3.3-70B, Mistral Large (13) + 3,405 humans vs Gemini 1.5 Flash
- Code released: https://github.com/eilamshapira/GLEE (code and data)
