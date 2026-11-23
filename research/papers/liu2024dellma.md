---
id: liu2024dellma
title: "DeLLMa: Decision Making Under Uncertainty with Large Language Models"
authors: [Ollie Liu, Deqing Fu, Dani Yogatama, Willie Neiswanger]
year: 2024
arxiv: "2402.02392"
venue: arXiv preprint (v3, 11 Oct 2024)
code: https://dellma.github.io/ (project site)
read: partial
relevance: high
topics: [uncertainty-calibration, game-theoretic-evals]
setting:
  multi_turn: false
  turn_protocol:
  players: 1
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read: main text (§§1–5, limitations) in full and App. C.4 (failure cases). Other appendix pages
(prompts, extra plots, API costs) not read. Results in Figs. 2 and 4 are plots; only values printed
in tables are quoted. Studied 2026-11-20.

## Question
When an LLM must choose an action whose payoff depends on unknown future states (what to plant,
which stock to buy), does it weigh the uncertainty properly? If not, does a scaffold built on
classical decision theory help? (§1)

## Setup
- Scaffold in four steps: list unknown factors; forecast each factor's values with verbal
  likelihoods mapped to numbers; elicit a utility function by having the LLM rank sampled
  (state, action) pairs and fitting a Bradley–Terry model; choose the action with the highest
  expected utility, computed outside the LLM (§3).
- Two tasks, 120 decision problems each: Agriculture (pick a fruit from 7, context = USDA
  September 2021 report and statistics, utility = price × yield next year) and Stocks (pick one of
  7 tickers for December 2023 from 24 monthly prices) (§4.1–4.2).
- Baselines: zero-shot, self-consistency, a three-step chain of thought (unknown factors, their
  likelihoods, decision). Backbones GPT-4 (1106), Claude 3, Gemini 1.5; also o1-preview zero-shot
  (§4).

## Findings
- **Plain prompting fails as the choice grows**: with larger action sets, zero-shot,
  self-consistency and CoT often do **worse than random** (§4.1, Fig. 2).
- **The failure is following the mood of the text, not weighing scenarios**: e.g. GPT-4 assumes a
  high grapefruit price lasts because last year had extreme weather; CoT names alternative
  scenarios but doesn't use them systematically. Neither sampling, imagining alternatives, nor
  *giving the model a posterior belief* in the prompt substantially fixes it (§4.1, App. C.4).
- **The forecasts themselves are fairly calibrated**: ECE 0.062 (GPT-4), 0.142 (Claude 3), 0.064
  (Gemini 1.5) (Table 1). So the problem is not the probabilities but using them to decide.
- **Computing the expected utility outside the model helps**: up to 40% higher accuracy than
  baselines (abstract), consistent across the three model families (Fig. 2); it beats zero-shot
  o1-preview by a wide margin at similar cost per problem ($0.09–0.37 vs $0.21) (Table 3, §4.3).
- More samples and more overlap between ranking batches raise accuracy roughly linearly (Fig. 3).
- The LLM's rankings of outcomes agree with the authors' 65–70% of the time, close to their own
  inter-annotator agreement of 77.5% (Table 4).

## Limitations
- Small discrete state and action spaces; one-shot choices, no other agents or dialogue
  (limitations section).
- Utility comparisons judged against the authors' own annotations; independence between factors
  assumed for simplicity (§3.2).

## Relevance to Parley
- **The clearest outside evidence for the TERMS-Bench pattern** ([[zhang2026terms]]): models can
  produce reasonable probabilities, yet don't turn them into good decisions, and putting a
  posterior in the prompt doesn't help. Here it holds in a single-agent setting with no opponent,
  so the weakness is general, not specific to negotiation.
- Suggests a fix by construction: let the model forecast and rank, and do the expected-utility
  arithmetic outside it. For a training study ([[gap]]), the question becomes whether training can
  install that step *inside* the model, and whether it then transfers.

## Ideas to borrow
- Split a decision into forecast, utility and maximisation, and score each step separately, to
  locate where a failure happens (same logic as the oracle ladder).
- Compare against random choice as the action set grows; failure shows up with size.
