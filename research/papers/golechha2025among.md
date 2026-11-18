---
id: golechha2025among
title: "Among Us: A Sandbox for Measuring and Detecting Agentic Deception"
authors: [Satvik Golechha, Adrià Garriga-Alonso]
year: 2025
arxiv: "2504.04072"
venue: NeurIPS 2025 (arXiv v3, 10 Feb 2026)
code: https://github.com/7vik/AmongUs
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 24 pages (main text pp. 1–9, appendices A–J pp. 14–24; references skimmed) on 2026-11-15.
MATS / FAR AI. Players act one after another in each phase (`turn_protocol: strict`); 7 players
per game. The code link comes from the PDF's hyperlink ("available here", p. 2).

## Question
Can a text version of Among Us elicit **open-ended, goal-directed deception** (the model works out
for itself that it should deceive, given only the rules), and can it measure deception and
detection as separate, unbounded capabilities? Do activation probes and SAE features trained on
simple honesty datasets detect this deception out of distribution? (pp. 1–2)

## Setup
- **Game** (builds on AmongAgents, Chi et al. 2024): 5 crewmates + 2 impostors on the Skeld map;
  task phase (move, complete/fake task, kill, vent, call meeting, check cameras) alternating with
  meeting phase (3 discussion rounds, then a vote to eject). Crew wins by finishing tasks or
  ejecting both impostors; impostors win when they reach parity or at the 50-step limit (§2.1–2.3,
  pp. 2–3). Prompts give only the rules and map, no examples or personas; each step the agent
  writes [Condensed Memory], [Thinking Process], [Action] (App. B pp. 14–15).
- **Experiment 1**: 400 games, Llama-3.3-70B vs Phi-4-15B randomly assigned to roles (§3.1 p. 4).
- **Experiment 2**: 2,054 games with 7 players drawn from **18 OpenRouter models** (April 2025):
  Claude 3.7 Sonnet (+thinking), Claude 3.5 Sonnet, Claude 3 Opus, DeepSeek-R1, R1-distill-Llama-
  70B, DeepSeek-V3-0324, Grok-3-beta, o3, Gemini 2.5 Pro preview, Gemini 2.0 Flash, Llama-3.3-70B,
  Llama-4-Maverick, Qwen3-235B-A22B, Qwen-2.5-7B, Gemma-3-4B, Phi-4, Mistral-Small-3.1-24B
  (Fig. 2 p. 3; §3.3 p. 6).
- **Metrics**: "Deception Elo" (rating as impostor, updated against the average crewmate rating)
  and "Detection Elo" (as crewmate); K = 32, start 1500, sequential updates, 1,000-sample bootstrap
  CIs; plus win rate (§3.2 p. 5). Win/loss is rule-decided.
- **LLM judge** (GPT-4o-mini) scores every step 1–10 for awareness, lying, deception, planning;
  used only to label data for probes, binarised (§3.1 p. 5; App. D prompt pp. 18–19).
- **Detection methods**: logistic-regression probes on Phi-4 layer 20 residual stream (last 10
  tokens), trained on TruthfulQA, DishonestQA ("pretend you're dishonest" system prompt), RepEng,
  or Among Us data; SAE features (Goodfire API, Llama-3.3-70B) for detection and steering (§4
  pp. 6–8).
- **Cost**: 2,054 games ≈ $2,000 OpenRouter; 400 games $100; judge $2; probes ~$400 GPU; SAEs $30
  (App. I p. 20).

## Findings
- **Deception vs detection**: frontier reasoning models (Claude 3.7 Sonnet thinking, DeepSeek-R1,
  Grok-3) have the highest Deception Elo (≈1,800–1,850 by plot reading) and win rates (≈50–60%);
  Qwen-2.5-7B and Claude 3 Opus lowest (≈1,580–1,600) (Fig. 2 p. 3). On Detection Elo, small and
  non-reasoning models are comparable to frontier ones; most reasoning ("RL") models lie above the
  slope-1 line in deception-vs-detection (Fig. 5 p. 5; §3.3 p. 6). Against release date, deception
  rises (quadratic fit) and detection does not (Fig. 16 p. 24). No statistical test of the RL vs
  non-RL difference is given.
- **Size and role**: in 400 Llama-3.3 vs Phi-4 games, Llama-3.3 wins more as impostor, Phi-4 more
  as crewmate (Fig. 3 p. 4).
- **Judge labels**: GPT-4o-mini scores are poorly calibrated (few scores 3–7) but separate binary
  labels; crewmates almost never lie, impostors sometimes tell the truth to build trust (Fig. 4
  p. 5).
- **Probes generalise OOD**: RepEng-trained probe on Among Us AUROC 0.94 (lying) and 0.99
  (deception) (§4.2 p. 7; Fig. 10b p. 21: 0.941 / 0.996); on-distribution Among Us probe 0.863 /
  1.000 (Fig. 10a). On "speak" actions alone the probe scores 0.984 from the action text only, but
  across all actions (77% non-speech) action-only AUROC is **0.653**, rising to 0.948 with the
  thinking text (Fig. 6 p. 6). Probes do not transfer to TruthfulQA, which the authors attribute to
  unintentional vs intentional falsehood (App. A p. 14; Table 2 p. 16). Most of the 40 layers work
  for RepEng probes (Fig. 9 p. 18).
- **SAEs**: an "assistant should promote honesty" feature detects impostors at AUROC 0.967, "acts of
  deception" 0.851; a "contexts involving deception" feature is inverted (0.182) (Table 1 p. 8).
  **Steering with these features fails**: small amounts change nothing, large amounts make the
  model incoherent (§4.3 p. 8; App. F pp. 16–17).
- Authors note the deception label is "very correlated with the 'Impostor' label" (Fig. 6 caption,
  p. 6), so probes may partly detect role rather than deceptive intent (p. 9).

## Limitations
- **Capability, not propensity**: authors say the sandbox measures deceptive capability, "different
  from deception propensity" (p. 9); deception is required by the impostor role.
- One game, one fixed role split; models likely know Among Us from pretraining (p. 9).
- Elo numbers are reported in figures only, with no table; Fig. 2 and Fig. 5 show different
  Deception Elo ranges for the same 2,054 games (≈1,550–1,900 vs ≈1,350–1,650), not explained.
  Sequential Elo with K = 32 is order-dependent; bootstrap CIs mitigate this partly.
- "RL-trained" is a coarse label (reasoning models vs others) with no controlled comparison and no
  test; the claim rests on visual position relative to a line (Fig. 5).
- Probe ground truth comes from an uncalibrated GPT-4o-mini judge; probes are only tested on one
  model (Phi-4); no human baseline; no training of game-playing agents.
- Mixed-model 7-player games make each model's rating depend on the random mix of co-players.

## Relevance to Parley
- For the **map (a)**: a clean instance of measuring **deceiving and detecting as two separate
  scores from the same game**, by side. It covers deception/detection in a social-deduction setting
  with rule-decided outcomes; it does not cover negotiation, cooperation for surplus, or
  persuasion as a treatment.
- For the **transfer study (b)**: its main result is itself a skill-asymmetry claim — whatever
  frontier training did (RL for reasoning) raised deception more than detection (Fig. 5, Fig. 16).
  That is observational, across uncontrolled model families. A controlled version — train one side
  (e.g. RL as impostor) and measure the other side and other games — is exactly the open question.
  Same pattern as [[he2026socialgym]], where the minority-minus-majority side gap is often >100 Elo
  and its sign differs by model.
- Compared with [[he2026socialgym]] (hidden-role family, 6 games, both sides, 10 models) and
  [[taylor2026clocktower]] (BotC, detection/judgement/persuasion split): Among Us adds bigger
  frontier models and an interpretability arm, but only one game.
- Their stated broader-impact worry (training for deception is gain-of-function, p. 9) is relevant
  if the thesis trains a deception-heavy skill: one would want to measure whether deception
  transfers *out* of the game into negotiation honesty (e.g. misreporting values in
  [[zhang2026terms]]-style settings).
- For [[judges]]: the step-level LLM judge is uncalibrated but usable for binary labels; rule
  outcomes remain the primary score.

## Ideas to borrow
- **Side-specific Elo** (Deception Elo vs Detection Elo) and the deception-vs-detection scatter with
  a slope-1 line: a compact way to show a skill pair moving apart before/after training.
- **Release-date trend** of each skill as a cheap observational precursor to a training study.
- **Activation probes as a second measurement channel**: a probe trained on a generic honesty
  dataset, applied to game transcripts, could check whether training changes deceptive intent and
  not just behaviour (needs open weights).
- Report probe AUROC on action text alone vs with reasoning, to avoid crediting the probe for
  reading the role from the prompt.

## Map fields
- Skills measured: deceiving-detecting (impostor deception vs crewmate detection); other: lying/deception detection from activations (probes, SAEs)
- Scoring: mixed (rule-decided win/loss for Elo; GPT-4o-mini judge only for probe labels)
- Agents: many (7 per game)
- Opponents: LLM
- Tests: capability
- Training evaluated: none (probes are trained as detectors; SAE steering tried and fails; no agent training)
- Transfer between skills measured: no (deception vs detection compared observationally across models, not via training)
- Models tested: 18 (Claude 3.7 Sonnet ± thinking, Claude 3.5 Sonnet, Claude 3 Opus, DeepSeek-R1, R1-distill-Llama-70B, DeepSeek-V3, Grok-3-beta, o3, Gemini 2.5 Pro preview, Gemini 2.0 Flash, Llama-3.3-70B, Llama-4-Maverick, Qwen3-235B, Qwen-2.5-7B, Gemma-3-4B, Phi-4, Mistral-Small-3.1-24B); probes on Phi-4, SAEs on Llama-3.3-70B
- Code released: https://github.com/7vik/AmongUs
