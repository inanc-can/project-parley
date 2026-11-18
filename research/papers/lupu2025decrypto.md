---
id: lupu2025decrypto
title: "The Decrypto Benchmark for Multi-Agent Reasoning and Theory of Mind"
authors: [Andrei Lupu, Timon Willi, Jakob Foerster]
year: 2025
arxiv: "2506.20664"
venue: arXiv preprint (v1, 25 Jun 2025)
code: https://github.com/facebookresearch/decrypto
read: partial
relevance: medium
topics: [game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 3
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read on 2026-11-15: main text pp. 1–10 and appendices A–H and K in full (limitations, baselines,
experimental details, prompt robustness, RSA formalism, human study); the verbatim prompt listings
(App. I–J, pp. 22–27) and failure/perspective-taking transcripts (App. L–M, pp. 34–41) only
skimmed, hence `partial` (41 pages). Figure 3/4 numbers taken from the extracted figure text.
Two teams, three roles (Encoder, Decoder vs Interceptor); turns are a fixed sequence (hint → two
independent guesses → reveal), so `turn_protocol: strict` fits.

## Question
Can a word-association game built on the board game Decrypto serve as an interactive,
hard-to-saturate benchmark for multi-agent reasoning (cooperation, competition, ad-hoc and
human-AI coordination) and for theory of mind (ToM), while removing confounds such as
tokenisation, maths, spatial reasoning, long contexts and text renderings of embodied scenes?
(pp. 1–3)

## Setup
- **Game** (§2 pp. 2–3): Alice (Encoder) and Bob (Decoder) share 4 secret keywords; each turn
  Alice gets a 3-digit code (digits 1–4, no repeats, each of 24 codes at most once) and gives 3
  public hints; Bob and Eve (Interceptor) guess independently; all guesses, the code and the hint
  history are then public. Eve wins on 2 intercepts or 2 miscommunications; Alice/Bob win by
  surviving 8 turns. 680 curated keywords (>8.8 billion keyword combinations); hints open-ended.
- **Why ToM is needed**: an RSA (Rational Speech Act) formalisation shows Bob must model Alice's
  model of Eve (second-order ToM) whenever intercepts matter (App. H pp. 19–21, eq. 10), and that
  Alice's interception risk grows with the KL divergence between her model of Eve and the true Eve
  (eq. 21).
- **Settings** (§3.1 p. 4): *competition* (A plays Alice+Bob, B plays Eve, teams swapped);
  *ad-hoc coordination* (Eve fixed, Alice and Bob different models); *human-AI coordination*.
- **Metrics**: miscommunications, intercepts, and **average game length** (preferred over win
  rate because Eve wins most LLM games) (p. 4). A Hessian-determinant metric of outcome
  sensitivity to players/prompts is announced (p. 2) but its definition is not in the text I read.
- **Generalist vs specialist agents** (§4.1 p. 5): generalists play out of the box with the
  environment's prompt (no prompt engineering, no fine-tuning); specialists include rule-based
  agents, RL-trained agents and engineered prompts. Robustness: 625 prompt variants per model
  (App. G p. 17).
- **Baselines** (§4.1, App. E): GloVe and Word2Vec agents; Alice samples hints from the top-K most
  similar nouns (5,696-noun corpus) that are closer to the intended keyword than any other; Bob
  picks the most similar keyword; Eve solves an assignment against mean hint-history embeddings.
  K=16 used throughout.
- **ToM experiments** (§3.2 pp. 4–5; App. D): a Smarties-task variant for Eve (prompt A: guess
  keywords; B: after reveal, what did *you* think; C: what would a *second interceptor* think) →
  representational change (RC) and false belief (FB), each with a Weak pass (answer ≠ true
  keywords) and a Strong pass (answer = own earlier answer); a Three-Mountain variant for Alice
  (predict Eve's guess) → perspective taking (PT). Each experiment needed only new prompts and
  ~15 lines of code.
- **Models** (§5 p. 7; Table 1): Llama-3.1-8B/70B-Instruct, DeepSeek-R1-Distill-Qwen-32B, GPT-4o,
  plus DeepSeek-R1, Claude 3.7 Sonnet (extended thinking), o1 (high) and ExploreToM-8B (Llama-3.1-8B
  fine-tuned on ToM data by Sclar et al.) in the human and ToM studies. Temperature 0.6 for games,
  0 for ToM; 32 games × 3 seeds per cell; up to 10 re-prompts for format (App. F pp. 16–17).
- **Humans**: 10 games by novice human Alice/Bob teams vs Llama-3.1-70B as Eve, played on the same
  CLI and prompts; games continued for all 8 turns for replay (§4.2 p. 6; App. K).
- **Cost**: ~$0.10 per role per episode for Claude 3.7; a full 32-episode × 3-seed all-Claude run
  ~$30; the full matrix scales as n³ in models (App. A p. 14; App. F.3 p. 17).

## Findings
- **Baselines beat LLMs**: at K=16 the embedding baselines outperform all LLM agents in self-play
  and competition, but cross-play with a different embedding or with an LLM collapses; for K>128
  most cross-play games end in miscommunication (Fig. 2 p. 6; Fig. 3 p. 7). Example: GloVe-Alice's
  50th-nearest word to "fire" is "oil", which is outside Word2Vec's top 1,000 (p. 7).
- **Coordination** (Fig. 3 top, Eve = Llama-70B): baseline→LLM miscommunication rates 0.48–0.67 vs
  0.00–0.08 baseline–baseline and 0.00–0.04 LLM–LLM; among LLMs the decoder model drives
  miscommunications (Llama-8B worst). **No self-play/cross-play gap** among LLMs (p. 8).
- **Competition is skewed to Eve**: intercept rates mostly 0.71–1.00 (Fig. 3 bottom p. 7); LLM
  teams rarely survive 32 games (Fig. 7 p. 18). Novice humans win 33% even against the strongest
  Eves (p. 8). DeepSeek-R1-Distill-32B is the best LLM in LLM-only play.
- **Human games** (Table 1 p. 8): as Eve against humans, DeepSeek-R1 (15.0 intercepts, human win
  rate 20%) and Claude 3.7 (14.0, 20%) are strongest; as Bob with a human Alice, every model is
  worse than human decoders (human 11 miscommunications, 40% win, 6.9 turns vs Claude 3.7 12.67,
  16.7%, 6.57; GPT-4o 17.33, 3.3%; Llama-8B/ExploreToM 20, 0%). **ExploreToM-8B (ToM fine-tuned)
  is worse than its base Llama-3.1-8B** in both roles (p. 8) — a data point that ToM-dataset SFT
  does not transfer to interactive ToM.
- **ToM** (Fig. 4 p. 9): most models pass Weak RC and Weak FB at high rates, but **all score ≤10% on
  Strong RC/FB** (poor self-consistency even at temperature 0). In PT, all models except
  Llama-3.1-70B predict Eve will intercept on nearly every turn, while the real rate is ~52%, even
  on turn 1 when Eve can only guess at random; o1 still does so when told Eve "does *NOT* know the
  secret keywords" (p. 9; Listings 14–16 pp. 39–41). **Llama-3.1-70B beats Claude 3.7 and o1 on all
  three ToM tasks**; authors hypothesise RL on verifiable tasks pushes models to always give a
  definite answer (p. 40).
- **Prompt robustness**: across 625 prompt combinations, model size is the main predictor of game
  length for Llama-8B/70B (Fig. 8 p. 18).

## Limitations
- Few models, few seeds; GPT-4o is the only closed model in the main matrix (p. 7). The human study
  is 10 games with human Alice/Bob only, no human Eve (App. A p. 14).
- ToM coverage is narrow by design: RC, FB, PT; no intent or emotion inference (App. A–B).
- One game, one skill family: cooperative signalling against an eavesdropper. No negotiation,
  persuasion, free dialogue or mixed-motive payoffs (authors exclude free-form dialogue on purpose,
  p. 9).
- No training is run; MARL fine-tuning is named as future work (pp. 10, 14).
- The Hessian-determinant metric is mentioned in the intro and Table 1 caption without a definition
  in the text read.

## Relevance to Parley
- **For the map (a)**: a clean, rule-scored entry for *cooperative communication under an
  adversarial listener* plus interactive ToM probes; 3 agents, LLM/baseline/human opponents,
  capability only. It covers what [[he2026socialgym]] files under ToM/deception (Chameleon,
  Codenames-like clue games) with a much tighter design and a human anchor.
- **For the transfer study (b)**: Decrypto is a good *held-out probe* rather than a training target.
  It is cheap, short (≤8 turns), dense in signal, and the RC/FB/PT probes measure ToM separately
  from win/loss. Two results bear directly on (b): (1) ExploreToM-8B, fine-tuned on static ToM data,
  is *worse* than its base model in play (Table 1) — skill-specific SFT can fail to transfer or even
  hurt; (2) newer reasoning (RL-trained) models regress on perspective taking (Fig. 4) — a hint that
  RL on one kind of task can damage a social skill, which is the interference question. It leaves
  open whether training on any social game (negotiation, deception) moves Decrypto ToM scores.
- Compared with [[liu2025spiral]] and [[yuan2025marshal]] (self-play RL on games, then held-out
  tests): neither tests interactive ToM; Decrypto could be the held-out ToM probe in such a design.
  Compared with [[duan2024gtbench]] / [[huang2024gamabench]]: those are game-theoretic and mostly
  non-linguistic; Decrypto is linguistic but not about payoffs.
- Cross-play matters: embedding agents perfect in self-play fail in cross-play (Fig. 2), the same
  warning [[leibo2021meltingpot]] makes for MARL — a trained agent should be tested against unseen
  partners, not only itself.

## Ideas to borrow
- **Generalist vs specialist reporting rule** (§4.1): state whether prompts are part of the agent;
  useful to keep prompting vs fine-tuning vs RL arms comparable in (b).
- **Probe prompts inserted mid-game and kept out of context** (App. F.1) to measure ToM without
  changing play — a template for propensity/skill probes in Parley talks.
- **Weak vs Strong pass** split (consistency with one's own earlier answer).
- **Perspective-taking check**: ask the speaker to predict the other side's inference and compare
  with the true rate; in negotiation, ask an agent to predict what the counterpart believes about
  its reservation value.
- **Rule-based agents with a tunable difficulty knob** (K) as fixed, cheap opponents.
- Use game length rather than win rate when one side dominates.

## Map fields
- Skills measured: cooperating (ad-hoc and human-AI coordination), competing (interception), keeping secrets (hints hidden from the interceptor), other: theory of mind (representational change, false belief, perspective taking), pragmatic communication
- Scoring: rules
- Agents: many (3: two-person team vs interceptor)
- Opponents: scripted (GloVe/Word2Vec baselines), LLM, human
- Tests: capability
- Training evaluated: none (only an existing ToM-SFT model, ExploreToM-8B, compared with its base)
- Transfer between skills measured: no
- Models tested: Llama-3.1-8B/70B-Instruct, DeepSeek-R1-Distill-Qwen-32B, GPT-4o, DeepSeek-R1, Claude 3.7 Sonnet (extended thinking), o1 (high), ExploreToM-8B
- Code released: https://github.com/facebookresearch/decrypto (code, configs, human game data)
