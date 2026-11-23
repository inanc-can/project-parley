---
id: lin2022teaching
title: "Teaching Models to Express Their Uncertainty in Words"
authors: [Stephanie Lin, Jacob Hilton, Owain Evans]
year: 2022
arxiv: "2205.14334"
venue: arXiv preprint (v2, 13 Jun 2022)
code: none stated
read: partial
relevance: medium
topics: [uncertainty-calibration]
setting:
  multi_turn: false
  turn_protocol:
  players: 1
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

Read: main text pp. 1–10 in full and App. A (task table). Appendices B–C (training details,
extra experiments) not read. Studied 2026-11-20.

## Question
Can a language model learn to say how likely its own answer is to be correct, in words ("61%",
"medium confidence"), and does that stay calibrated on new kinds of questions? (pp. 1–2)

## Setup
- GPT-3 175B (davinci); smaller models were too weak at arithmetic for the test to mean anything
  (p. 5).
- CalibratedMath: 21 programmatically generated arithmetic tasks split by difficulty (p. 4,
  Table 3). Train on Add-subtract (~10k items); evaluate under shift on Multi-answer (several
  correct answers, new concepts, easier: median accuracy 65% vs 21%) and Multiply-divide (pp. 4–5).
- Supervised fine-tuning: the label is GPT-3's empirical accuracy on that sub-task, given as a
  number or one of five words (p. 5). Compared with the zero-shot answer logit, a fine-tuned
  "indirect logit" (probability of "True"), and a constant baseline (p. 6).
- Metrics: MSE (Brier) and MAD calibration error (p. 5).

## Findings
- **Verbalized probability generalizes under shift**: on Multi-answer, MSE 22.0 vs 37.4 (answer
  logit), 33.7 (indirect logit), 34.1 (constant) (Table 1, p. 6). On Multiply-divide it only
  matches the constant baseline; the indirect logit is best there (p. 6).
- **It is underconfident under shift**: the evaluation answers are more often right than the
  training ones, and the model doesn't fully adjust (p. 6).
- **50 examples in context almost match fine-tuning on ~10k** (Fig. 6, p. 7).
- **Not just logits or simple heuristics**: a logistic regression on hand-made difficulty features
  does worse; a linear probe on GPT-3 embeddings separates right from wrong answers, suggesting
  the uncertainty was already represented from pretraining and fine-tuning surfaces it
  (Table 2, Fig. 7, pp. 8–9).
- The model only outputs probability tokens it saw in training (footnote 7, p. 6).

## Limitations
- Arithmetic only, one model, small shift in format (p. 9). Supervised labels are per sub-task,
  so an easy item in a hard sub-task gets a low label (p. 5).
- The authors propose RL with a proper scoring rule as the more principled training (pp. 5, 9);
  not done here.

## Relevance to Parley
- Shows uncertainty about one's own answers can be **trained** and partly carries to new tasks:
  a small transfer result for an uncertainty skill. What's untested is uncertainty about *another
  agent* and using it to act ([[zhang2026terms]]).
- Supports the reading that the representation exists from pretraining and training mainly
  exposes it, which is relevant to whether "acting on likelihoods" can be trained cheaply.

## Ideas to borrow
- Train on one family of situations, evaluate calibration on a shifted family with a different
  base rate: a clean transfer test design.
- Constant baseline fitted on training data, to show the model beats "always say the base rate".
