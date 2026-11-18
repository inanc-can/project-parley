---
id: ramesh2026sparks
title: "Sparks of Cooperative Reasoning: LLMs as Strategic Hanabi Agents"
authors: [Mahesh Ramesh, Kaousheik Jayakumar, Aswinkumar Ramkumar, Pavan Thodima, Aniket Rege, Emmanouil-Vasileios Vlatakis-Gkaragkounis]
year: 2026
arxiv: "2601.18077"
venue: ICML 2026 (PMLR 306); arXiv v3, 8 Aug 2026
code: null
read: partial
relevance: medium
topics: [game-theoretic-evals, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read on 2026-11-15: main text pp. 1–10 in full, appendices A–H (pp. 17–33) in full; skimmed the
prompt listings (App. I, pp. 33–56) and the qualitative transcripts (App. J, pp. 57–75), hence
`read: partial` (75 pages in all). The paper says code, models and datasets are released "at this
url", but the hyperlink target is not in the extracted text, so `code: null` until the link is
checked on the arXiv page. Players: 2–5 per Hanabi game (all copies of one LLM except the
cross-play test); the human baseline is a score distribution from 80,699 BoardGameGeek games, not
humans playing with the models.

## Question
How well do current LLMs cooperate under hidden information in Hanabi across 2–5 players, how much
does context engineering (engine-supplied beliefs vs self-tracked memory) matter, and can a small
model be post-trained on LLM-generated Hanabi data — and does that training transfer outside
Hanabi? (pp. 1–2)

## Setup
- UW–Madison / UMD. Hanabi Learning Environment; each seat an independent instance of the same LLM,
  no orchestrator; 10 fixed seeds per player count (40 games per model per scaffold); a team that
  loses all lives keeps its score at that moment (p. 3; App. B.2 p. 18).
- **17 LLMs** (+ Qwen3-4B-Instruct-2507 as the training base): o3, o4-mini, GPT-4o, GPT-4.1, GPT-4.1
  mini, Gemini 2.5 Pro/Flash, Gemini 2.0 Flash, DeepSeek-R1/V3, Grok-3, Grok-3-mini, Qwen3-32B,
  Qwen3-235B-A22B, Llama-4 Maverick, Mistral Medium 3, Claude 3.7 Sonnet (Table 3, p. 18).
- **Three scaffolds**: *Watson* — minimal state plus what each player explicitly knows about own
  cards; *Sherlock* — adds engine-computed "could be" belief state, Hanabi strategy and a
  Bayesian step-by-step workflow; *Mycroft* — no engine deductions, the agent must write its own
  deduction scratchpad and read it next turn (pp. 3–6). Agents pick from legal moves and rate every
  candidate move in [−1, 1].
- **Datasets**: HanabiLogs (1,520 trajectories with reasoning traces) and HanabiRewards (560 games
  with per-move ratings, which are the playing LLM's own move ratings, described as LLM-as-judge)
  (Table 1 p. 2; §3.4 p. 5).
- **Training** of Qwen3-4B-Instruct-2507 (non-thinking): *SFT* with LoRA on o3 + Grok-3-mini Sherlock
  trajectories, 3 epochs (App. G p. 27); *RL* (GRPO via Prime-RL, LoRA r = 32, 16 rollouts, batch
  512) on ~6,000 o3 samples from Sherlock then continued on Mycroft, reward = o3's rating of the chosen
  move, no format or state-tracking reward (§5.2 p. 7; App. H.1 p. 31). Training data come from 20
  Sherlock + 20 Mycroft games per player count (160 games total) (p. 32). Fine-tuned models are
  evaluated on held-out seeds {4, 6, 8, 10, 12}, i.e. 5 games per player count (p. 19; Fig. 8).
- **Transfer evals** for the RL model only (Table 2, p. 8): Group Guessing Game (10 copies of the
  model propose integers that must sum to a hidden target with only "too high/low" group feedback;
  200 games × 50 rounds, Plain variant, run twice), EventQA (long-context temporal reasoning, BM25
  RAG, 6-way MCQ at 64K/128K/800K), IFBench strict (294 prompts), AIME 2025.

## Findings
- **Benchmark**: reasoning models score >13/25 even in Watson; non-reasoning <10 (p. 5). Best
  Sherlock scores: Grok-3-mini 18.0 (3p), 17.4 (4p); o3 best in Watson for 2–4p (p. 6; Fig. 5).
  Top LLMs reach about the lower quartile of 80,699 human BGG games, below the median (App. F,
  pp. 26–27); specialist RL agents score >23 (2p) and R3D2 ≥20 (p. 6).
- **Context helps reasoning models, hurts non-reasoning ones**: Sherlock vs Watson Gemini 2.5 Flash
  +4.4, Pro +2.9, o4-mini +0.6; but GPT-4.1 family −2.4, Grok-3 −3.9, Claude 3.7 Sonnet −4.1
  (pp. 5–6). On Grok-3-mini 5p seed 3: Watson 12.2, SPIN-Bench prompt 14.5, SPIN without deductions
  15.4, Sherlock 16.1 (Fig. 2, pp. 3–4).
- **Self-tracked state is weak**: Mycroft vs Sherlock drops o4-mini and Gemini 2.5 Pro ~3.7, Grok-3-
  mini ~2.1, o3 ~1.2 (p. 6). An o4-mini judge rates state tracking 0.252 (o4-mini) vs 0.459
  (Grok-3-mini) out of 1 (Table 4, p. 26).
- **Scores fall with more players** for most top models (p. 6), except in Mycroft where 2p is worst
  (p. 22).
- **Cross-play interpolates**: teams with one Grok-3-mini (Mycroft 14.9) among o4-minis (11.3) score
  between the two self-play levels; one strong seat of five adds ≈ 1.7 (p. 7, p. 9; Fig. 7). Only
  this one model pair was tested.
- **Sampling/ensembles**: Best-of-K helps weak prompts (Watson +1.5 at k = 5) but not Sherlock
  (+0.1); a 6-agent mixture adds +0.8–1.6 in 5p with high variance (App. E pp. 23–25).
- **SFT**: Qwen3-4B base 4.8 → 5.8 (Sherlock, ~+21%; IQM gap only 0.6) (Fig. 8a p. 8; p. 20); helps
  2–3p but makes the model overconfident in 4–5p (App. G.2 p. 27).
- **RL**: Sherlock 4.8 → 12.3 (+7.5, +156%), beats GPT-4.1 by +4.2; Mycroft 1.7 → 8.3 (+6.6,
  +388%); o4-mini 15.0 / 11.3 (pp. 7–8). MAPPO trained on 64K games per player count peaks at a
  6.39 average window (Table 5, p. 32) — but MAPPO starts from scratch and the 4B model distils o3's
  judgments, so this is not a like-for-like efficiency comparison.
- **Transfer after RL on Hanabi** (Table 2, p. 8; base → RL):
  - *Cooperative task (Group Guessing)*: 61.0 → 73.0 and 60.5 → 71.5 win rate (+12.0, +11.0).
  - *Temporal reasoning (EventQA)*: 64K 84.0 → 85.6, 128K 62.6 → 66.8, 800K 37.2 → 43.6 (+1.6, +4.2,
    +6.4).
  - *Instruction following (IFBench strict)*: Avg@10 30.9 ± 1.3 → 31.5 ± 1.1 (within noise),
    Pass@10 42.9 → 44.6.
  - *Math (AIME 2025)*: Avg@10 48.7 → 50.0; Pass@10 73.3 → 73.3 (unchanged).
  - **No negative transfer is reported** on these four; no social, competitive, negotiation or
    deception evaluation was run, and the SFT model's transfer was not tested.

## Limitations
- Small samples: 10 games per player count for the benchmark, 5 for fine-tuned models; IQM CIs in
  App. D but no tests on the transfer table except IFBench's ±.
- The RL reward is o3's own move rating (LLM judge), so "RL" is closer to distilling o3's
  preferences; the paper does not test reward quality against game outcome.
- Transfer evaluation: one checkpoint, one base model, no control arm (e.g. RL on a non-cooperative
  task with the same format and length), so the Group Guessing and EventQA gains could come from
  longer reasoning (Mycroft outputs grow to 5–7K tokens per turn, Table 6 p. 33) or structured-output
  training rather than cooperation. Group Guessing is self-play with 10 copies of the same model.
- Self-play for almost everything; cross-play only one model pair. No human–AI play.
- Scaffold effects are large and model-specific, so model rankings depend on prompt choice.

## Relevance to Parley
- **One of few papers that trains on a cooperative game and measures transfer**: Hanabi RL → a
  different cooperative task (+11–12 points), long-context temporal reasoning (+1.6 to +6.4), no
  loss on AIME math. That is a positive data point for (b): training one cooperative skill moved
  another cooperative task.
- **What it leaves open for (b)**: it never checks whether cooperative training changes competitive,
  negotiating, persuading or deceiving behaviour — the interference question. No prompting-vs-SFT-vs-
  RL transfer comparison (SFT transfer was not measured; SFT barely moved Hanabi). No propensity
  measures (does the trained model become more trusting / exploitable?).
- Complements [[lyu2026gift]] (RL on matrix games, TicTacToe and Who's the Spy with fixed opponents;
  finds both positive and negative transfer and multi-task interference) and [[liu2025spiral]] (RL
  self-play on zero-sum games → math). Together they cover cooperative, competitive and mixed games,
  but no paper here trains on negotiation and tests on cooperation/competition, which
  [[he2026socialgym]]-style family profiles could measure. Hanabi is pure common-interest, unlike the
  mixed-motive settings in [[leibo2021meltingpot]], [[bianchi2024negotiationarena]] or
  [[zhang2026terms]].
- For [[judges]]: rewards from an LLM's move ratings worked well enough to train on, and an LLM judge
  scores state tracking — both unvalidated against ground truth here.

## Ideas to borrow
- **Scaffold ladder** (minimal → engine beliefs → self-tracked memory) to separate reasoning about
  others from bookkeeping; report which a training gain comes from.
- **Held-out seeds** for fine-tuned models to avoid training-data leakage (App. B.2).
- **Cross-play interpolation test**: replace k of n seats with a stronger/weaker partner and check
  whether the team score interpolates — a cheap ad-hoc cooperation measure for trained models.
- Group Guessing Game as a cheap out-of-domain cooperative probe in a transfer battery.
- Add a control arm (same harness, non-social task) before attributing transfer to the social skill.

## Map fields
- Skills measured: cooperating (Hanabi; Group Guessing as transfer), other (theory of mind / belief-state tracking; temporal reasoning, instruction following, math as transfer)
- Scoring: mixed (game rules for Hanabi; LLM judge for move ratings/RL reward and state tracking)
- Agents: many (2–5 Hanabi seats; 10 in Group Guessing)
- Opponents: LLM (teammates are copies of the same LLM; one cross-play pair; MAPPO as a trained baseline)
- Tests: capability
- Training evaluated: prompting (scaffolds, Best-of-K, mixture of agents), SFT, RL
- Transfer between skills measured: yes (Hanabi RL → Group Guessing, EventQA, IFBench, AIME 2025)
- Models tested: o3, o4-mini, GPT-4o, GPT-4.1, GPT-4.1 mini, Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash, DeepSeek-R1, DeepSeek-V3, Grok-3, Grok-3-mini, Qwen3-32B, Qwen3-235B-A22B, Llama-4 Maverick, Mistral Medium 3, Claude 3.7 Sonnet; Qwen3-4B-Instruct-2507 (trained)
- Code released: stated as released ("at this url"), link not recoverable from the PDF text; check the arXiv page
