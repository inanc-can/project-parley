---
id: xie2026bench
title: "M3-BENCH: Process-Aware Evaluation of LLM Agents' Social Behaviors in Mixed-Motive Games"
authors: [Sixiong Xie, Zhuofan Shi, Haiyang Shen, Yun Ma, Xiang Jing]
year: 2026
arxiv: "2601.08462"
venue: arXiv preprint (v2, 2 Apr 2026)
code: https://github.com/FredericVAN/PKU_M3Bench
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: null
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 46 pages (main text pp. 1–9, appendices A–M pp. 12–46) on 2026-11-15. Peking University.
Level 1 games are one-shot; levels 2–4 are repeated or episodic. Turn order varies by game
(simultaneous matrix moves, alternating offers, day/night phases), so `turn_protocol` is left
empty. 2 to 9 players. The Silent vs Comm toggle is a communication treatment, not a persuasion
treatment.

## Question
Does evaluating LLM agents in mixed-motive games on **what they do, think and say** (behaviour,
stated rationale, dialogue), rather than outcomes alone, reveal differences that outcome-only
benchmarks miss? (pp. 1–2)

## Setup
- **24 classic games in 4 levels**, 6 each (Table 4 p. 18; App. F pp. 19–22):
  - *L1 one-shot dyadic*: PD, Stag Hunt, Hawk–Dove, Battle of the Sexes, Ultimatum (pie 10),
    Inspection game.
  - *L2 repeated dyadic*: repeated PD (T=10), gift-exchange contract, loan & default, deposit
    contract, mutual insurance with claim fraud, alternating-offer bargaining (pie 10, K=5, δ=0.95).
  - *L3 group*: public goods (N=5), volunteer's dilemma, minority game, common-pool resource,
    rule voting + contribution with sanctions, networked trust game.
  - *L4 private information / language*: sealed-bid auction with collusion channel, committee
    voting + lobbying with private signals, hidden traitor, hidden informant, Werewolf (7–9),
    Kuhn/Leduc poker.
- **Silent vs Comm**: same game with and without free-form messages each round (p. 6).
- **Three views** per episode (§3.3 pp. 4–5):
  - **BTA** (behaviour): rule-based indicators per task, normalized to [0,1] and averaged
    (App. I Table 10 pp. 29–32). Directions are **normative**: e.g. cooperation +1, Hawk rate −1,
    collusion index −1, payoff efficiency = welfare/max welfare.
  - **RPA** (reasoning): LLM judge scores the agent's ≤120-token stated rationale on 8 dimensions
    (prosocial, self-interest, reciprocity, punishment, forgiveness, horizon, deception intent,
    opponent modelling) (App. G–H pp. 23–26).
  - **CCA** (communication): LLM judge labels each message with one of 15 pragmatic acts
    (propose, promise, threat, deception, info withhold, …) and scores clarity, credibility,
    persuasiveness, consistency with actions (App. B.1, H.3). Taxonomy κ=0.82 between two coders
    on pilot data (p. 13).
  - **Judge**: Claude Opus 4.5 at temperature 0, 5 calls per record, median/majority (p. 28).
  - **Cross-view consistency σ**: SD of the three module scores per dimension; lower = more
    coherent (Eq. 4 p. 13).
  - Optional "portrait" layer maps evidence onto Big Five and Social Exchange Theory, explicitly
    not psychometric (p. 5; Tables 13–14).
- **Agents**: 11 LLMs in three groups — closed (GPT-5.1, Claude Opus 4.5, Gemini-3 Pro, Grok-4.1),
  open-weight (gpt-oss-120b, DeepSeek-V3.2, Kimi-K2-Thinking, Mistral Large 3), reasoning (GPT-5
  pro, Gemini-3 Deep Think, DeepSeek-V3.2-Speciale) — plus rule-based TFT, GTFT, ALL_D, RAND and
  **50 human crowdworkers** (Alibaba Cloud, CNY 25/h, each played all 24 tasks in both conditions)
  (pp. 5–6; Table 3 p. 14; Table 11 pp. 34–35).
- **Protocol**: one zero-shot template telling the agent to "maximize your own total payoff"
  (p. 24); each target model paired with all opponent types in the pool, 50 episodes per pairing
  and condition (p. 6). Default task score = equal-weight mean of BTA, RPA, CCA (p. 6; App. K).

## Findings
- **Level averages** (Table 1 p. 6, BTA/RPA/CCA ×100), L4: GPT-5.1 86.2/85.8/83.7; Claude Opus 4.5
  85.5/84.7/86.8; GPT-5 pro 82.2/92.0/66.8; DeepSeek-V3.2-Speciale 78.2/94.0/58.0; Kimi-K2-Thinking
  74.3/81.0/63.2; Human 80.7/77.5/84.7. Spread grows from L1 to L4 (p. 7).
- **"Overthink–undercommunicate"**: reasoning models top RPA but trail on CCA. Repeated PD with
  Comm: DS-V3.2-Speciale BTA 92/RPA 97/CCA 72, σ=0.108, gap 25; GPT-5 pro 94/96/79, σ=0.074
  (Table 20 p. 46). Kuhn poker: Speciale 85/94/50, σ=0.190, gap 44; GPT-5 pro 88/92/60, σ=0.138
  (Table 21 p. 46).
- **Humans vs LLMs**: top LLMs beat humans on scores, and the paper says humans are "markedly"
  more consistent across views (p. 7). The tables support this only in part: in Kuhn poker humans
  have the lowest σ (0.016), but in repeated PD Claude Opus 4.5 (0.012) is more consistent than
  humans (0.029) and GPT-5.1 is similar (0.033) (Tables 20–21 p. 46).
- **Case study**: Kimi-K2-Thinking cooperates in rounds 1–9 of a 10-round PD and defects in round
  10; its judged self-interest rises 34 → 63 → 94 across stages while commitment strength falls
  79 → 55 → 22 (Table 2 p. 12; App. E p. 17: cooperation 80%, commitment–action consistency 55/100).
- **Robustness (reported without detail)**: alternative fusion weights give Kendall τ 0.85–0.93
  with the default ranking, top 3 unchanged (pp. 13–14); first-30 vs 50-episode ranking τ >0.95
  (p. 14); judge vs 3 expert raters on 200 episodes "strong agreement", judge swap and prompt
  paraphrase keep findings, "no statistically significant" provider favouritism — no numbers
  given (App. C.4 p. 14).
- Rule baselines on BTA: TFT 79 vs ALL_D 61 on one-shot PD; ALL_D near 35–50 everywhere
  (Tables 15–18 pp. 44–45), showing BTA rewards prosocial play, not payoff.

## Limitations
- **BTA is not payoff.** Indicators reward cooperation, fairness, non-collusion and conceding
  (Table 10 pp. 29–32) while the agent is told to maximize its own payoff (p. 24). So the main
  score mixes capability with prosocial propensity, and which one a high score means is unclear.
- **Two of three views are judged by an LLM**, and the judge (Claude Opus 4.5) is also one of the
  judged models; Claude tops CCA in several columns (Table 1). Judge robustness is asserted
  without numbers (App. C.4). RPA scores stated rationales, not hidden reasoning (p. 8).
- **Reporting gaps**: no confidence intervals in the result tables (bootstrap only "recommended",
  App. K.8); "held-out transfer prediction" and "process-risk flagging" are listed as analyses
  (p. 7) but I found no results for them; App. J's σ validation is written as a protocol
  ("examples; adapt to your tasks", p. 36) without AUROC values.
- **Model identity oddities**: Gemini-3 Pro and Gemini-3 Deep Think both map to
  `gemini-3.1-pro-preview`, Grok-4.1 to `grok-4` (Table 3 p. 14).
- Unclear who plays whom: "all opponent types in the evaluation pool" (p. 6) is not broken down by
  LLM vs scripted vs human opponent, and per-opponent results are not shown.
- Humans paid by the hour, no performance bonus (p. 34); human RPA implies humans wrote
  rationales, but the procedure is not described.
- No training of any kind.

## Relevance to Parley
- For the **map (a)**: the broadest classic-game catalogue among the notes (24 games covering
  social preferences, repeated reciprocity, collective action, auctions/collusion, lobbying,
  hidden roles, bluffing), with a Silent/Comm toggle and a human baseline. Its distinctive idea is
  scoring **talk–act consistency** (promises vs actions) alongside behaviour.
- For the **transfer study (b)**: covers many directions in one harness but trains nothing and
  reports no cross-skill correlation. Two things are usable: (1) the per-skill indicator library
  (Table 10) as a menu of rule-based measures; (2) talk–act consistency as an outcome that
  training could hurt — e.g. does RL for payoff increase endgame defection and broken commitments
  (the Kimi case, p. 12)? Training-induced changes in σ would be a new measure.
- Treat its numbers with caution (see Limitations); I would not cite its model rankings in the
  proposal without the released data.
- Compared with [[he2026socialgym]]: SocialGym is rule-scored with reliability checks and no
  judge in the main score; M3-Bench leans on an LLM judge for two thirds of its score and has no
  reliability numbers. SocialGym ranks who wins; M3-Bench rewards prosocial behaviour.
- Compared with [[huang2024gamabench]] and [[duan2024gtbench]]: similar classic-game coverage but
  adds communication, process views and humans.
- Compared with [[wang2024sotopia]] and the [[judges]] topic: another case where a judge scores
  open-ended social behaviour; useful as a warning about self-judging (judge model in the pool).
- Kuhn poker scored against Nash bluff rate 1/3 (Table 10 note b, p. 32) is a clean
  solver-referenced measure, like [[zhang2026terms]]'s known-optimum checks.

## Ideas to borrow
- **Silent vs Comm** on the same game to isolate what talk adds.
- **Commitment–action consistency**: extract promises from dialogue, check them against later
  actions with rules (App. K.2 p. 38: `cta = 1 − violated/|commitments|`). Endgame defection rate
  in known-horizon repeated games as a propensity probe.
- Solver-referenced indicators (Nash bluff frequency, welfare/max welfare) to give scores an
  absolute anchor.
- Report each view separately and their disagreement rather than one fused score.
- Do not let a judged model act as judge; report judge agreement with numbers.
- Keep rule-based payoff and prosocial indicators as separate columns so capability and
  propensity can be read apart.

## Map fields
- Skills measured: cooperating, competing, negotiating value (ultimatum, alternating offers, loan, gift exchange), persuading (lobbying, Werewolf), deceiving-detecting (traitor, informant, Werewolf, poker), other: commitment keeping / talk–act consistency, norm enforcement, collusion
- Scoring: mixed (rule-based BTA + LLM-judge RPA and CCA, equal weights)
- Agents: many (2–9)
- Opponents: scripted (TFT, GTFT, ALL_D, RAND) / LLM; human baseline as a separate population
- Tests: both (BTA's normative directions reward prosocial choices; payoff efficiency and Nash references measure skill)
- Training evaluated: none (zero-shot prompting only)
- Transfer between skills measured: no
- Models tested: GPT-5.1, Claude Opus 4.5, Gemini-3 Pro, Grok-4.1, gpt-oss-120b, DeepSeek-V3.2, Kimi-K2-Thinking, Mistral Large 3, GPT-5 pro, Gemini-3 Deep Think, DeepSeek-V3.2-Speciale; 50 humans; 4 rule-based baselines
- Code released: https://github.com/FredericVAN/PKU_M3Bench
