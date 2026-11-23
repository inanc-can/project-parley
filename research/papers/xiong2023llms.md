---
id: xiong2023llms
title: "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs"
authors: [Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi]
year: 2023
arxiv: "2306.13063"
venue: ICLR 2024 (stated on the PDF, arXiv v2, 17 Mar 2024)
code: https://github.com/MiaoXiong2320/llm-uncertainty
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

Read: main text pp. 1–10 in full. Appendices (pp. 14–29: white-box comparison, extra results,
prompts) not read. Page numbers are approximate (from the extracted text). Studied 2026-11-20.

## Question
For black-box LLMs (no token probabilities), which ways of asking for confidence give scores that
are calibrated and that separate right from wrong answers? (pp. 1–2)

## Setup
- Framework of three parts: prompt (vanilla, chain of thought, self-probing in a separate chat,
  multi-step confidence, top-K guesses), sampling (repeat, paraphrase, misleading hint) and
  aggregation (consistency, Avg-Conf, Pair-Rank) (pp. 3–5, Fig. 1, Table 1).
- Models: Vicuna 13B, GPT-3 175B, GPT-3.5-turbo, GPT-4, LLaMA 2 70B (p. 5).
- Eight datasets in five types: commonsense, arithmetic, symbolic, professional law, business
  ethics (p. 5).
- Metrics: ECE for calibration, AUROC and AUPRC for failure prediction (p. 6).

## Findings
- **Stated confidence is overconfident and human-like**: values cluster at 80–100% in multiples
  of 5, accuracy in each bin far below the stated level (Fig. 2, p. 6). GPT-3, GPT-3.5 and Vicuna
  average ECE above 0.377 (p. 7).
- **Scale helps but not enough**: ECE falls and AUROC rises from GPT-3 to GPT-4 (~22% AUROC gain),
  yet GPT-4's average AUROC is only 62.7%, close to chance at 50% (Table 2, p. 7).
- **Low ECE can be empty**: GPT-4 with chain of thought on GSM8K reaches ECE 0.064 by saying 100%
  for everything at 93.6% accuracy; it can't tell its right answers from wrong ones (p. 8).
- **Agreement across samples beats stated confidence for spotting errors**: 5 samples plus
  consistency raise GSM8K AUROC from 54.8% to 92.7% on GPT-3.5 (Table 3, p. 8).
- Human-inspired prompts reduce overconfidence, with smaller gains for GPT-4; no prompt wins
  everywhere (Fig. 3, p. 7). Best ECE 0.028 with Pair-Rank (p. 9).
- White-box methods beat black-box ones only narrowly (AUROC 0.605 vs 0.522) (p. 9).
- Professional-knowledge tasks (law) stay hard for all methods (p. 9).

## Limitations
- Question answering with one correct answer only; no open-ended tasks or decisions (p. 9).
- Prompting and sampling only, no training.

## Relevance to Parley
- Two different things get called "calibration": matching the average (ECE) and telling right
  from wrong (AUROC). The second is what an agent needs to decide when to trust its own read of a
  situation, and it is the weak one. Relevant to belief scoring in [[zhang2026terms]]-style setups.
- Overconfidence that imitates human talk ("90%") is a warning for any study that asks agents for
  stated beliefs: stated numbers may be style, not belief.

## Ideas to borrow
- Score elicited beliefs on both ECE and AUROC; flag "same confidence for everything".
- Use agreement across several samples as a cheap uncertainty signal, compared with the stated
  number.
