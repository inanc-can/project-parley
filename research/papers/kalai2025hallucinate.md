---
id: kalai2025hallucinate
title: "Why Language Models Hallucinate"
authors: [Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, Edwin Zhang]
year: 2025
arxiv: "2509.04664"
venue: arXiv preprint (v1, 4 Sep 2025)
code: none (theory and a meta-evaluation)
read: partial
relevance: medium
topics: [uncertainty-calibration, eval-methodology]
setting:
  multi_turn: false
  turn_protocol:
  players: 1
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

Read: main text (§§1–6) in full, including the pretraining theory at the level of statements and
examples. Proofs and appendices (B–F, incl. the benchmark meta-evaluation details) not read.
Section numbers instead of pages. Studied 2026-11-20.

## Question
Why do language models state confident falsehoods instead of saying "I don't know", and why
doesn't post-training remove this? (§1)

## Setup
- Theory: reduce generation to a yes/no classification problem ("is this output valid?") and
  bound generation errors from below by its misclassification rate (§3).
- Socio-technical argument with a meta-evaluation of popular benchmarks and whether they give any
  credit for abstaining (§4, Table 2).

## Findings
- **Pretraining makes some errors unavoidable**: generative error rate ≳ 2 × the
  misclassification rate of "is it valid?" (§1.1). For arbitrary facts with no pattern (e.g.
  birthdays), the hallucination rate after pretraining is at least the share of facts that appear
  once in training ("singleton rate") (§3.3).
- **Calibration and errors go together**: cross-entropy pretraining yields calibrated base models,
  and a calibrated model must make errors; a model that never errs (always "I don't know") would
  be uncalibrated (§3.1). GPT-4's calibration on multiple choice is good before RL and worse after
  (Fig. 2, reprinted from the GPT-4 report).
- **Evaluations reward guessing**: under 0–1 grading, abstaining is never optimal for any belief
  about the answer (Observation 1, §4.1). Most leading benchmarks give no credit for "I don't
  know" (Table 2), so a model that always guesses beats an honest one; models stay in "test-taking
  mode" (§1.2, §4).
- **Proposed fix**: state an explicit confidence threshold in the instructions ("answer only if
  > t confident; mistakes cost t/(1−t) points, IDK 0") and add it to mainstream benchmarks, not
  just to special hallucination tests. The behaviour to aim for is "behavioral calibration":
  answer only when confidence exceeds the stated threshold (§4.2).

## Limitations
- Mostly theory and argument; the empirical part is a benchmark survey, no training experiment.
- Treats right/wrong/IDK as categories; ignores degrees of error and hedging (§5).
- Single factual questions; open-ended and interactive settings only discussed.

## Relevance to Parley
- A clean statement of **how the reward scheme shapes behaviour under uncertainty**: if only
  outcomes count, models learn to act confidently whatever they believe. A negotiation reward that
  pays only for deals may train the same thing, a training side effect in the sense of [[gap]].
- "Behavioral calibration" (act only when confident enough, given stated stakes) is close to what
  TERMS-Bench finds missing ([[zhang2026terms]]): using a probability to decide whether to push,
  probe or walk away.

## Ideas to borrow
- State the stakes and threshold explicitly in the task, then check whether behaviour changes
  across thresholds: a direct test of acting on uncertainty.
- Audit an evaluation for whether it ever rewards abstaining or hedging before using it as a
  training reward.
