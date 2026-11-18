---
id: smith2025evaluating
title: "Evaluating Generalization Capabilities of LLM-Based Agents in Mixed-Motive Scenarios Using Concordia"
authors: [Chandler Smith, Marwa Abdulhai, Manfred Diaz, Marko Tesic, Rakshit S. Trivedi, Alexander Sasha Vezhnevets, Lewis Hammond, Jesse Clifton, Minsuk Chang, Edgar A. Duéñez-Guzmán, John P. Agapiou, Jayd Matyas, Danny Karmon, Akash Kundu, Aliaksei Korshuk, Ananya Ananya, Arrasy Rahman, Avinaash Anand Kulandaivel, Bain McHale, Beining Zhang, Buyantuev Alexander, Carlos Saith Rodriguez Rojas, Caroline Wang, Chetan Talele, Chenao Liu, Chichen Lin, Diana Riazi, Di Yang Shi, Emanuel Tewolde, Elizaveta Tennant, Fangwei Zhong, Fuyang Cui, Gang Zhao, Gema Parreño Piqueras, Hyeonggeun Yun, Ilya Makarov, Jiaxun Cui, Jebish Purbey, Jim Dilkes, Jord Nguyen, Lingyun Xiao, Luis Felipe Giraldo, Manuela Chacon-Chamorro, Manuel Sebastian Rios Beltran, Marta Emili García Segura, Mengmeng Wang, Mogtaba Alim, Nicanor Quijano, Nico Schiavone, Olivia Macmillan-Scott, Oswaldo Peña, Peter Stone, Ram Mohan Rao Kadiyala, Rolando Fernandez, Ruben Manrique, Sunjia Lu, Sheila A. McIlraith, Shamika Dhuri, Shuqing Shi, Siddhant Gupta, Sneheel Sarangi, Sriram Ganapathi Subramanian, Taehun Cha, Toryn Q. Klassen, Wenming Tu, Weijian Fan, Wu Ruiyang, Xue Feng, Yali Du, Yang Liu, Yiding Wang, Yipeng Kang, Yoonchang Sung, Yuxuan Chen, Zhaowei Zhang, Zhihan Wang, Zhiqiang Wu, Ziang Chen, Zilong Zheng, Zixia Jia, Ziyan Wang, Dylan Hadfield-Menell, Natasha Jaques, Tim Baarslag, Jose Hernandez-Orallo, Joel Z. Leibo]
year: 2025
arxiv: "2512.03318"
venue: NeurIPS 2025 Datasets and Benchmarks Track (per the PDF footer; not checked on DBLP); arXiv v1, 3 Dec 2025
code: https://github.com/google-deepmind/concordia
read: full
relevance: high
topics: [game-theoretic-evals, negotiation-benchmarks, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: null
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 37 pages (main text pp. 1–10, checklist pp. 15–18, appendix pp. 19–37) on 2026-11-15.
Figures 2–8 (posterior plots, per-scenario means, ability profiles, Likert ratings) are images;
I only have what the text says about them. Actions are free text resolved by an LLM game master,
so there is no fixed turn protocol (`turn_protocol` empty). Contest code: Concordia v1.8.9.
Co-author [[hadfield-menell]] is on the people list.

## Question
Can LLM agents **cooperate zero-shot in new mixed-motive situations with unfamiliar partners**,
i.e. find and use opportunities for mutual gain, and can a Melting-Pot-style protocol (held-out
scenarios × background populations) measure that for language agents? (pp. 1–2, 4)

## Setup
- **Protocol** (§3 pp. 4–5): a scenario = substrate (rules, a POSG without rewards) + background
  population ρ + mode. **Resident** mode: focal agent is the majority, ρ a minority (tests
  stability and resistance to invasion). **Visitor** mode: focal agent is a minority among ρ (tests
  adapting to local norms). Background strategies modelled on human patterns (naive altruism,
  stubbornness, conditional cooperation). Scenarios are "cooperation-eliciting": an agent does well
  only if it finds mutual gains.
- **Five substrates** (Table 1 p. 7): *Reality Show* (PD / Chicken / Stag Hunt mini-games with talk
  phases), *Pub Coordination* (choose pubs with friends, closures, persuasion), *Haggling* (2–4
  fruit merchants bargain over prices), *Labor Collective Action* (strike vs work, organizer, boss),
  *State Formation* (two village elders negotiate an alliance against raiders). Each tagged in
  advance with demands (negotiation, persuasion, discouraging antisocial behaviour, calculation,
  coordination, hidden information, social networks, convention following; Table 13 p. 37).
- **Veil of ignorance** (§4.1 pp. 5–6): development phase on public scenarios with feedback;
  evaluation on **14 held-out scenarios** (p. 10) with held-out background players and, in
  evaluation, the top-5 submissions as co-players (p. 7); some held-out populations were not
  cooperative, to test not being exploited.
- **Fixed LLM**: every agent uses Gemma-2-9B-it; participants submit only the scaffold (memory,
  calculation, prompts) around it, with a cap on LLM calls per step (pp. 6, 22).
- **Scoring**: an LLM game master resolves free-text actions; "each environment was equipped with
  a language model-based reward model" scoring GM outcomes (p. 21). §3.2 describes the score as
  based on the share of agents playing jointly cooperative strategies (p. 5). Raw scores min–max
  normalized per scenario to [0,1] (p. 8).
- **Ranking**: Elo over all agents, then the top six in a cross-play round; also Iterative Maximal
  Lotteries, Copeland, Ranked Pairs and "evaluation without aggregation" (pp. 8, 22–24).
- **Analyses**: hierarchical Beta regression of score on tags (LKJ prior); mixed-effects model vs a
  "rational agent" baseline; Measurement Layouts (Bayesian capability profiles from tag demands),
  vs linear regression and XGBoost; LLM-based qualitative summaries and 10 Likert traits; survey of
  20 teams (pp. 8–9, 25, 34).
- **Scale**: 197 participants, 878 submissions, 25 final teams (p. 21); contest Sep–Nov 2024.

## Findings
- **Low absolute scores**: mean normalized score 0.426 ± 0.005 (SE) (p. 8); strongly
  scenario-dependent — one scenario near 0.9, most well below (p. 8; Fig. 3).
- **Few agents beat a simple baseline**: only five agents significantly above the rational agent;
  most are similar or worse (p. 8; Fig. 2). Evaluation Elo spans only 1412–1588, with
  `rational_agent` 16th of 26 at 1477 (Table 3 p. 23).
- **Cooperative demands lower scores**: persuasion, convention following, negotiation,
  discouraging antisocial behaviour and coordination each reduce expected score by 10–20
  percentage points (p. 8). Persuasion ability separates top agents from the rational baseline;
  weak sanctioning ("discouraging antisocial behaviour") marks the worst (p. 9; Fig. 6).
- **Rankings depend on aggregation and on co-players**: `in2ai_megamind` is 1st by evaluation Elo
  (1588) and by IML and Copeland, but in final top-six cross-play it is 6th of 6 agents by Elo at
  1433, below `rational_agent` (1459); `taehun_cgcal` (4th by Elo, 8th by Ranked Pairs, 13th by
  evaluation without aggregation) wins the cross-play at 1561 (Tables 3–8 pp. 23–29). Mid-ranks
  reshuffle across methods; top and bottom stable (p. 24).
- **Overfitting to development scenarios**: several teams scored much higher in development than
  evaluation (p. 10).
- **Demand tags predict performance**: Measurement Layout ≈ linear regression < XGBoost on
  held-out R², all better than a constant baseline on average but worse for some agents (pp. 25,
  28; Fig. 7). Profiles shown only for agents with test R² ≥ 0.35 (p. 25).
- **Failure modes**: distraction from task goals, selfish choices, losing goal alignment,
  dialogue–action mismatches (pp. 9, 35); Likert ratings (LLM-assigned) correlate with returns
  (p. 9).
- Survey (n=20): self-rated proficiency with open-source codebases correlates −0.95 with final rank
  (lower rank = better); trying alternative ideas: average rank 10.4 vs 22.0 (p. 34).

## Limitations
- **One model** (Gemma-2-9B-it) for every agent (p. 10): measures scaffolds, not models; says
  nothing about frontier models or about training.
- **LLM-adjudicated outcomes**: GM and reward model are LLMs (p. 21); no judge-agreement check is
  reported. The score definition in §3.2 (share of cooperative strategies) and the appendix (LLM
  reward model, "highly contextual") are not reconciled.
- Elo differences are small (176 points end to end) and the authors say Elo "can be sensitive to
  noise" (p. 8); no CIs on Elo; final cross-play has only six agents.
- 14 held-out scenarios from five substrates, text only (p. 10); participants reported a
  mid-contest change of the evaluation model (p. 35).
- Results in figures cannot be checked numerically from the text (tag coefficients, per-scenario
  means). LLM used for Likert and policy-adherence ratings is not named.
- Cooperation is the scored target, so capability and cooperative propensity are not separated;
  no humans.

## Relevance to Parley
- For the **map (a)**: the clearest **generalization protocol** among the notes — held-out
  scenarios plus held-out co-player populations, resident/visitor modes, pre-registered demand
  tags. It is the language-agent version of [[leibo2021meltingpot]], from the same group. Covers
  cooperation, negotiation (Haggling, State Formation), persuasion and sanctioning in open-ended
  natural language; scores mutual gain rather than who won, unlike [[he2026socialgym]] and
  [[wang2026mindgames]].
- For the **transfer study (b)**: it measures generalization of a *fixed* agent across scenarios,
  not whether *training* one skill moves others. But it gives the evaluation design a transfer
  study needs: train on development substrates, test on held-out substrates and populations, and
  explain results through demand tags (Measurement Layouts). The dev-vs-eval drop (p. 10) is
  exactly the over-specialization a training study would measure. With the LLM fixed, all variation
  comes from scaffolds — a clean "prompting/scaffolding harness" arm; adding SFT/RL arms on the same
  base model would turn it into the student's comparison.
- The `in2ai_megamind` reversal (1st by evaluation Elo, below the rational agent in top-six
  cross-play) shows rankings depend on the co-player population; the same team won the MINDGAMES
  Generalization track with an RL-trained model ([[wang2026mindgames]]).
- Compared with [[abdelnabi2023cooperation]]: both put LLMs in multi-party negotiation with
  cooperative and selfish incentives; Concordia adds held-out scenarios and background populations.
- Compared with [[zhang2026terms]]: TERMS uses scripted opponents with known types for attribution;
  Concordia's background populations play the same role at the population level (naive altruist,
  stubborn, conditional cooperator).
- For [[judges]]: outcomes here are themselves decided by an LLM game master and reward model, a
  step further than judging transcripts; a reason for Parley to keep outcomes rule-decided where
  possible.

## Ideas to borrow
- **Resident vs visitor** populations: test a trained agent both as the majority (does it resist
  exploiters?) and as a minority (does it adapt to local conventions?).
- **Development/held-out split of scenarios and co-players**, with the held-out set hidden from
  whoever tunes the agent — needed to tell transfer from overfitting.
- **Pre-registered demand tags** per scenario and a regression of score on tags (or Measurement
  Layouts) to get per-skill ability profiles; compare profiles before and after training on one
  skill.
- A **rational/self-interested baseline agent** as the reference to beat.
- Report several aggregation rules (Elo, maximal lotteries, Copeland, ranked pairs) and show where
  rankings disagree.
- Fix the base model across arms so that differences come only from the harness.

## Map fields
- Skills measured: cooperating, negotiating value (Haggling, State Formation), persuading, other: discouraging antisocial behaviour (sanctioning), coordination, convention following
- Scoring: LLM judge (LLM game master resolves actions; an LLM-based reward model scores outcomes, p. 21), normalized per scenario
- Agents: many
- Opponents: LLM (organizer-written background agents with fixed strategy profiles; top-5 submissions as co-players in evaluation)
- Tests: capability (cooperative skill; cooperation is the rewarded target, so propensity is not separated)
- Training evaluated: prompting (scaffolds around a fixed Gemma-2-9B-it; no weight updates)
- Transfer between skills measured: no (zero-shot generalization of fixed agents to held-out scenarios and co-players)
- Models tested: Gemma-2-9B-it only (26 scaffolded agents incl. a rational baseline)
- Code released: https://github.com/google-deepmind/concordia (v1.8.9; agent implementations supplied as a zip, p. 16)
