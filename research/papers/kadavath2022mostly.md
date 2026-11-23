---
id: kadavath2022mostly
title: "Language Models (Mostly) Know What They Know"
authors: [Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, Scott Johnston, Sheer El-Showk, Andy Jones, Nelson Elhage, Tristan Hume, Anna Chen, Yuntao Bai, Sam Bowman, Stanislav Fort, Deep Ganguli, Danny Hernandez, Josh Jacobson, Jackson Kernion, Shauna Kravec, Liane Lovitt, Kamal Ndousse, Catherine Olsson, Sam Ringer, Dario Amodei, Tom Brown, Jack Clark, Nicholas Joseph, Ben Mann, Sam McCandlish, Chris Olah, Jared Kaplan]
year: 2022
arxiv: "2207.05221"
venue: arXiv preprint (Anthropic)
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

Read: main text (§§1–6, incl. discussion and limitations) in full. Appendices A–D (metric
details, extra results, dataset descriptions, ~18 pages) not read. Page numbers below are
section and figure references because the extracted text had no reliable page numbers. Studied
2026-11-20.

## Question
Do language models know what they know? Three steps: are their probabilities calibrated on
multiple-choice questions; can they judge whether their *own* sampled answers are correct
(P(True)); and can they be trained to predict, before answering, whether they will get a question
right (P(IK)), and does that carry over to new tasks? (§1)

## Setup
- Anthropic pretrained models of 800M, 3B, 12B and 52B parameters; a brief check of RLHF policies
  trained from them (§1.3, §3.3).
- Calibration on all BIG-Bench multiple-choice tasks, MMLU, TruthfulQA, LogiQA, QuALITY, with
  lettered options shown to the model (§2).
- Self-evaluation on TriviaQA, Lambada, arithmetic, GSM8k, Codex HumanEval and scraped Python
  function synthesis (§4).
- P(IK): a value head fine-tuned on TriviaQA, label = fraction of 30 samples at T = 1 that are
  correct; tested out of distribution (§5).

## Findings
- **Large models are well calibrated on multiple choice** when they see the options, and
  calibration improves with size and with few-shot prompting (Figs. 4–6, §2). No clear link
  between accuracy and calibration within BIG-Bench (Fig. 5).
- **"None of the above" breaks it**: replacing an option sharply lowers accuracy and calibration;
  even the 52B model avoids using it, also at 20-shot (Fig. 7, §3.1).
- **RLHF policies look badly miscalibrated**, but one temperature (T = 2.5) largely fixes it on
  three evaluations (Fig. 9, §3.3).
- **Self-evaluation works few-shot and improves with size**: answers the 52B model rates
  P(True) > 0.5 are far more often correct than average. Zero-shot P(True) is poorly calibrated
  and sits near 50% (Figs. 1, 10–11, §4). Showing the model five of its own samples before judging
  one ("brainstorming") helps on short answers, less on code and GSM8k (§4.2).
- **Verification improves faster than generation**: the gap between base accuracy and accuracy
  among P(True) > 0.5 answers grows with size (Fig. 11, §4).
- **P(IK) transfers partly**: trained only on TriviaQA, it separates answerable from unanswerable
  questions in arithmetic, code and Lambada (AUROC rises with size), but **calibration out of
  distribution is poor**, mostly underconfident; on Lambada it gives uniformly low scores.
  Training on all four tasks fixes much of this (Figs. 13–16, Table 1, §5.2).
- P(IK) rises when a relevant Wikipedia article is in context (18% → 78% in one example) and with
  correct hints more than with wrong or irrelevant ones, without training on this (Figs. 18–19,
  §5.3–5.4).
- Model-specific self-knowledge is weak: two 12B models give higher P(IK) to questions *they* got
  right, by only ~6% (Table 2, §5.5).

## Limitations
- Pure pretrained models; the authors expect RLHF models to be less calibrated (§6).
- Calibration is about factual questions; no decisions, no other agents.
- Does not address learned deception, which would undo honest self-evaluation (§6).
- Only five sampling datasets for generalization claims (§6).

## Relevance to Parley
- The strongest evidence that **self-knowledge transfers across tasks only partly**: training on
  one domain helps tell right from wrong elsewhere, but calibration doesn't carry. That is a
  transfer result for an uncertainty skill, the same shape as the question in [[gap]].
- Contrast with [[zhang2026terms]]: models can be well calibrated about *their own* answers
  given options, yet fail to act on a probability about *an opponent*. Knowing a probability and
  using it are separate skills.
- RLHF reshaping calibration is another training side effect ([[tian2023just]] replicates it).

## Ideas to borrow
- Train on one domain, test calibration on others, and report AUROC and calibration separately:
  transfer can show up in one and not the other.
- "Brainstorm alternatives before judging" as a cheap prompting baseline for belief reports.
