---
id: wu2026measuring
title: "Measuring AI Agents as Teammates with Collaborative Intelligence"
authors: [Sean Wu, Aneesh Pappu, Jiaru Zou, Yubin Kim, Yuncong Mao, Hongjian Zhou, Junchi Yu, Jieneng Chen, James Zou]
year: 2026
arxiv: "2611.02633"
venue: arXiv preprint (v1, 2 Nov 2026)
code: https://github.com/zou-group/collaborative-intelligence
read: full
relevance: high
topics: [eval-methodology, negotiation-benchmarks, judges, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2–5
  stakes: none
  persuasion_treatment: true
  human_baseline: true
---

Read all 51 pages (main text pp. 1–11, references, appendices A–H incl. all 22 cases, pp. 17–51)
on 2026-11-15. This is the "CIB" the caller described: the paper calls it the **Collaborative
Intelligence Benchmark** (it never uses the acronym "CIB" itself). Code link and website
(https://zou-group.github.io/collaborative-intelligence/) are the PDF's header hyperlinks. Rounds are
fixed-length (3–8 rounds) with a scripted teammate replying after each model message, so
`turn_protocol: strict`. `persuasion_treatment: true` because the test condition is a scripted
pressure/withholding treatment against a calm-teammate baseline; `human_baseline: true` only for 6
public tasks taken from published human studies (§5).

## Question
Can an individual model's **teamwork** be measured as a capability separate from task skill —
holding the rest of the team fixed — across eight dimensions drawn from organisational psychology,
and how do current models do? (pp. 1–2)

## Setup
- Stanford (James Zou's group, also behind [[bianchi2024negotiationarena]]), MIT, Oxford.
- **8 dimensions, 30 tasks each (20 public, 10 held-out) = 240 tasks** (§2.1 pp. 2–3): resisting
  unsafe pressure, reporting misconduct, sharing and seeking information, emotional intelligence
  (a teammate with a key fact becomes upset and withdraws), keeping the team on track, **handling
  conflict** (a same-side teammate presses for its own split and threatens to walk away), taking
  initiative (unowned need, nobody asks), taking over (inheriting a session where a weaker model
  cheated or wrote a false record).
- **Sources** (Table 1 p. 4): 94 real-world records (FDA/misconduct findings 36, clinical cases 35,
  NTSB/NASA ASRS/CSB accident reports 23) and 146 adapted benchmark items (ImpossibleBench/SWE-bench
  coding 66, **CaSiNo and Deal or No Deal negotiations 34** — cf. [[lewis2017deal]], HiddenBench /
  hidden-profile team decisions 27, MATH/GPQA 19).
- **Team**: 2–5 members. One **scripted teammate** (fixed branching lines written from the source;
  never generates text) creates the dimension's problem; after each model message, LLM judges label
  it from a fixed list (complies / challenges / hedges …) and the script branches on the label
  (§2.2 p. 4; App. B pp. 17–18). Other teammates are live LLMs (Claude Haiku 4.5, GPT-5 mini,
  Qwen3-14B) with private facts. 79 tasks add a shared sandbox (files, tests, inbox).
- **Three versions per task** (§2.3 p. 4): *alone* with all facts (1 run), *baseline* calm team (1
  run), *test* with the problem (3 seeds). **A model is scored only on tasks it solves alone**, so
  failures are teamwork failures. Binary pass/fail except conflict: 1 = best joint deal, 0.5 = held
  firm without it, 0 = gave in. Score = mean over 8 dimension means; 4,000-sample bootstrap CIs.
- **Outcome checked by code** (answer keys, hidden tests); judges (Claude Sonnet 4.6 referee, Haiku
  4.5 second rater, GPT-5 tie-break) only steer the script (p. 4).
- **18 models** (11 closed, 7 open-weight), 6 also at high reasoning effort; default = lightest
  reasoning setting; 24,851 scored runs (§3 p. 5). Frontier = Gemini 4 Argon, GPT-6 Astra, GPT-6.1
  Sol, Claude Opus 5.5, Claude Fable 5.1.
- Cost per full evaluation $1.8 to $662 (GPT-6 Astra high) at list prices, excl. partners/judges
  (§3.3 p. 7). A 40-task "Lite" subset (5 per dimension) keeps Kendall τ = 0.95 (App. C.4 p. 20).

## Findings
- **Leaderboard** (Table 2 p. 5; Fig. 1 p. 1): Gemini 4 Argon high 82.2 (best), Argon default 76.6,
  GPT-6 Astra 76.5, GPT-6.1 Sol 74.5, Opus 5.5 71.0, Fable 5.1 65.3, Sonnet 5.5 65.2, best open
  Kimi K3.1 Pro 59.9 … gpt-oss-120b 19.1. Baseline (calm team) 64.6–97.9%; drop from baseline to
  test **20.2–46.6 points** for every model (p. 5).
- **By dimension** (Fig. 3 p. 6; Table 5 p. 22): safety and reporting near-saturated (frontier ≥ 93%);
  **frontier models reach the best deal in only 14% of conflict tests** and pass 45% of
  emotional-intelligence tests (p. 6). Open-weight models average 41.6, 31.2 points below frontier;
  widest gaps in sharing (30 vs 88%) and initiative (16 vs 73%) (p. 6). Similar overall scores
  hide very different profiles (Fig. 13 p. 23).
- **Conflict is anticorrelated with the rest**: conflict correlates −0.43 to −0.23 with each other
  dimension, the other seven with each other at r ≥ 0.59; **one component explains 71% of variance
  in the eight scores and conflict is the only dimension against it** (App. F.1 p. 26; Fig. 19a
  p. 27). Conflict vs capability index r = −0.34, the other seven 0.75–0.95 (Fig. 18b p. 26).
- **Why**: stronger models ask about the teammate's needs more (r = 0.81 with score on the other
  seven) **and give in more** (r = 0.53, p = 0.03); best-deal rate is unrelated to ability (r = 0.00);
  weak models "hold firm" more (r = −0.67) — open-weight 28% vs frontier 5% (p. 27). Frontier models
  ask about needs in 99% of pressured runs yet accept the teammate's weaker split in 81% (p. 8).
  Alone they find the best split 100%, with a calm teammate 84% (accepting weaker offer 6%), under
  pressure 14% (p. 8). Opus 5.5 gives in 90% (default), 96% (high) (pp. 6–7; Table 8 p. 28).
- **But joint value barely suffers**: deals after giving in reach 93% of best joint points; all
  deals 94%; models range only 90–96%; counting no-deal as 0, joint points correlate **−0.55** with
  the conflict score — the "hold firm" models end without a deal more often (open 10% vs frontier 1%)
  (App. F.2 pp. 27–28). The conflict score thus rewards stubbornness the payoff does not reward.
- **Reasoning effort**: high effort raises 5 of 6 models by 2.7–5.7 points, lowers Kimi K3.1 Pro by
  3.7, at 1.0–4.8× cost (Table 6 p. 24). Pooled over 6 models: **initiative +8.4 (p = 0.001),
  emotional intelligence +6.9 (p < 0.001), conflict down for all 6 models (−0.3 to −11.7; 46 tasks
  worse vs 20 better, p = 0.002)**; paired runs: 66 give in only at high effort vs 37 only at default
  (p = 0.006) (App. E p. 24). Kimi's initiative falls 25.7 points at high effort because it makes
  fewer tool calls (54 vs 89) and misses the problem (p. 25).
- **Noticing vs acting**: of 5,094 failed runs, 45 ± 4% came after the model recognised the problem;
  in conflict 88%, on track 81%, taking over 74%, safety 73%, reporting 61% (failures of acting) vs
  sharing 19%, EI 15%, initiative 12% (failures of noticing) (p. 9; Fig. 6a p. 9). Stronger models
  fail more after noticing (r = 0.78 across models; frontier 62%) (p. 10; App. G.2 p. 29).
- **Taking over**: frontier pass 81% of takeovers vs 97% starting fresh; 56 of 165 coding takeovers
  fail, in 44 the cheat remains (p. 9). Showing the diff: edited test survives 1/18 instead of 17,
  special-cased code 16/24 instead of 22 (p. 9).
- **Initiative**: models notice the need in only 12% of 816 failures; quiet vs busy day 92% vs 72%
  for three closed models (p. 9).
- **Capability vs teamwork**: score vs Artificial Analysis index r = 0.92 (85% of variance; HLE
  r = 0.92, LMArena 0.76); Argon and Fable within 1 index point but 11 points apart; Opus 5.5 highest
  index (57.6) but 4th on teamwork (App. F p. 26).
- **Reliability** (App. C.1 p. 18): held-out vs public Kendall τ = 0.88, mean gap 2.7 points;
  seed-to-seed r ≥ 0.98; **only 80% of single test runs give the same verdict in all 3 seeds**, so
  averaging matters; split-half reliability 0.99; head-to-head on shared solved tasks agrees with
  the ranking in 271 of 276 pairs. Scoring on own solved tasks vs a filled-in common set: τ = 0.98,
  no row moves more than one rank (App. C.3 p. 19).
- **Judges** (App. C.2 pp. 18–19): referee and second rater agree on 81% of 51,279 messages (conflict
  71%, taking over 67%, EI 68%); people pick the judges' label on 82.5% of 40 messages (κ = 0.81);
  four non-Claude judges agree with people 90%; no evidence of Claude self-favour (lenient 1/52 vs
  6/128, p = 0.68), but the test detects only ≥ ~19% leniency. In safety/reporting, 19 of 315
  failing runs had a grading error corrected by hand (App. A p. 17).
- **People** (§5 pp. 10–11; Table 9 p. 29): on 3 of 6 tasks every model succeeded, above the human
  rates; in 13 real CaSiNo/DoND negotiations only 1 human pair reached the best joint deal vs
  frontier 24% and open 21% of runs — but people bargained for their own points while models were
  told the joint score is the goal.
- Negotiation tasks are the hardest source family (29% mean) and the only one where frontier
  models do not beat the average model (App. C.5 p. 21; Fig. 12b).

## Limitations
- Partners are LLMs, the "difficult" teammate is scripted with fixed lines; alone and baseline run
  once (App. A p. 17). Scripted branching depends on two Claude judges' labels, whose agreement is
  lowest exactly in conflict, EI and taking over (67–71%).
- **Conflict scoring conflates firmness with quality**: giving in costs only a few joint points
  (93% vs best), and joint-point scoring reverses the conflict ranking (r = −0.55) (App. F.2). The
  tasks are built so the pushy teammate's offer is close to optimal (p. 28). The anticorrelation
  finding may partly reflect this design choice rather than a general trade-off.
- Each model is scored on a different subset (tasks it solves alone); checked, but cells with 10–19
  tasks move ~6.8 points under re-estimation (App. C.3 p. 19).
- Correlations (r, PCA 71%) are across only 17–18 models; the initiative and pressure analyses in
  §4 use an earlier round of 6 models (App. A).
- Human comparisons rest on six tasks with mismatched incentives and settings, some with 5–15
  groups (App. G.1).
- **Training not evaluated**: no SFT/RL arm; the only "harness" variable is reasoning effort.

## Relevance to Parley
- **For the MAP (a)**: a cooperative-teamwork benchmark (not competitive games) covering cooperating,
  resisting pressure, information pooling, emotional intelligence and a negotiation-like conflict
  dimension built from CaSiNo/DoND. Outcomes are code-checked; judges only steer a scripted
  confederate — a design between rule-scored games ([[he2026socialgym]]) and judge-scored dialogue
  ([[wang2024sotopia]]).
- **For (b), the most direct evidence yet of a trade-off between social skills**: the seven
  "attentive teammate" dimensions load on one factor (71%), and conflict-holding goes the other way
  (−0.23 to −0.43). More reasoning effort raises initiative (+8.4) and EI (+6.9) while lowering
  conflict for all six models (p = 0.002). That is an inference-time harness change producing
  interference, exactly what (b) asks about for training. Prediction to test: SFT/RL that raises
  accommodating behaviours (EI, initiative) will lower firmness in negotiation; RL on hard
  bargaining (e.g. [[liu2025spiral]], [[zhang2026terms]]) may lower EI/initiative.
- **What it leaves open**: (1) no weight updates at all; (2) the conflict effect is cross-model
  correlation plus one effort knob, not a controlled intervention on one model; (3) the conflict
  score's sign depends on scoring — under joint-points scoring the trade-off nearly vanishes, so (b)
  must fix the outcome metric (own payoff, joint surplus, deal rate) before claiming interference.
- Links: "listens then gives in" mirrors sycophancy ([[sharma2023understanding]]) and the
  persuasion-susceptibility angle ([[persuasion-susceptibility]]): walk-away threats and guilt move
  frontier models off a deal they computed as best. Same group as [[bianchi2024negotiationarena]];
  cooperation-side companion to [[khatua2026cooperbench]] (cited as [23]). Leaking-under-pressure
  parallels [[li2026whose]].

## Ideas to borrow
- **Alone / calm-baseline / test triad** and scoring only on tasks solved alone, to separate social
  failure from task inability. Directly usable for transfer studies: measure each skill as a drop
  from a calm baseline.
- **Scripted confederate with judge-labelled branching**: fixed pressure lines, reacting to the model,
  so every model meets the same opponent — a reproducible "pushy counterpart" for Parley negotiations.
- Report both a behavioural score (gave in / held firm / best deal) and the payoff (joint points),
  and show where they disagree.
- Noticed-vs-acted failure taxonomy from judge labels (Table 11 p. 29).
- Public / held-out split with per-split scores; Lite subset chosen by greedy reproduction of the
  full score and validated on held-out models.
- Factor analysis (one component, sign of each dimension's loading) as the headline test for
  whether skills move together — run it before and after training.

## Map fields
- Skills measured: cooperating, negotiating value (joint-deal conflict tasks), resisting persuasion (unsafe pressure, walk-away threats), other: reporting misconduct, information seeking, emotional intelligence, keeping on track, initiative, auditing inherited work
- Scoring: mixed (code-checked final state; LLM judges label messages to drive the scripted teammate)
- Agents: many (teams of 2–5)
- Opponents: scripted (problem teammate) plus LLM (live partners: Claude Haiku 4.5, GPT-5 mini, Qwen3-14B)
- Tests: both (capability gated on solving alone; propensity to give in, report, take initiative)
- Training evaluated: none (only default vs high reasoning effort)
- Transfer between skills measured: no (cross-dimension correlations, PCA 71% with conflict anticorrelated, and effort-induced trade-off, but no training on one dimension)
- Models tested: Gemini 4 Argon, GPT-6 Astra, GPT-6.1 Sol, Claude Opus 5.5, Claude Fable 5.1, Claude Sonnet 5.5, Grok 4.7, Claude Haiku 5.5, Gemini 3.8 Flash, Mistral Large 4, GPT-6 Luna, Kimi K3.1 Pro, DeepSeek V4.1 Flash, Kimi K3, GLM-5.3, DeepSeek V4 Pro, Nemotron 3 Ultra, gpt-oss-120b (6 also at high effort; Qwen 3.7 Max in an earlier round)
- Code released: https://github.com/zou-group/collaborative-intelligence (160 public tasks; 80 held out)
