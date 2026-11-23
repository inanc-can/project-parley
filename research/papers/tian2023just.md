---
id: tian2023just
title: "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback"
authors: [Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, Christopher D. Manning]
year: 2023
arxiv: "2305.14975"
venue: arXiv preprint (v2, 24 Oct 2023)
code: none stated
read: full
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

Read: all 10 pages (main text, appendix figures and prompt table). Studied 2026-11-20.

## Question
RLHF is suspected of making a model's token probabilities overconfident, and closed models don't
expose probabilities anyway. Can you get calibrated confidence from RLHF models simply by asking
them to state it, in numbers or words? (pp. 1–2)

## Setup
- Models: gpt-3.5-turbo, gpt-4, claude-1, claude-2, Llama-2-70b-chat (p. 2).
- Data: 1,000 TriviaQA and 1,000 SciQ validation questions, all 817 TruthfulQA questions;
  correctness judged by GPT-4/GPT-3.5 for semantic equivalence (p. 3, App. C).
- Metrics: ECE, ECE after temperature scaling (ECE-t), Brier score (BS-t), and AUC of selective
  accuracy vs coverage (p. 3).
- Methods: label probability estimated from 10 samples; "Is True" probability; verbalized
  numerical confidence in one stage or two stages, with top-1/2/4 guesses; chain of thought before
  the confidence; linguistic expressions ("almost certain" … "almost no chance") mapped to numbers
  from a 123-person survey or fitted on held-out data (pp. 3–4).

## Findings
- **RLHF worsens calibration of token probabilities**: Llama-2-70B base vs chat, higher ECE and
  lower AUC on all three datasets (Fig. 2, p. 2; replicates the GPT-4 report).
- **Stated confidence beats token probabilities**: gpt-3.5-turbo TriviaQA ECE 0.140 (label prob.)
  vs 0.050 (verbalized, top-2); SciQ 0.256 vs 0.065 (top-4); TruthfulQA 0.451 vs 0.203 (top-4)
  (Table 1, p. 3). gpt-4 TriviaQA 0.078 vs 0.024 (Table 2, p. 3). Often a ~50% relative cut in ECE
  (abstract).
- **Considering alternatives helps**: listing several candidate answers before giving
  confidences improves calibration, like "consider the opposite" in human psychology (p. 4).
- **Chain of thought does not improve stated calibration** (p. 4; App. Fig. 5).
- Models differ: Claude-1 verbalizes poorly despite good probabilities; Claude-2 verbalizes a bit
  better than gpt-3.5; Llama-2-70b-chat gains least and inconsistently (Tables 3–5, pp. 4–5).
- Models state lower confidence on TruthfulQA (adversarial misconceptions) than on trivia (App.
  Figs. 3–4).

## Limitations
- Short factual questions only; reasoning, long answers and decisions untested (p. 5).
- One- vs two-stage prompts sometimes give very different calibration: results are prompt-
  sensitive (p. 5).
- Correctness is judged by an LLM.

## Relevance to Parley
- Calibration here means *stating* how likely your own answer is correct. That is one step before
  the TERMS-Bench problem ([[zhang2026terms]]): there, models are handed a probability about the
  opponent and fail to *act* on it. This paper shows models can produce reasonable numbers; it says
  nothing about using numbers to choose actions.
- Evidence that post-training (RLHF) reshapes uncertainty handling, a training side effect of the
  kind the transfer question in [[gap]] is about.

## Ideas to borrow
- Elicit a stated probability with each belief report and score it with ECE/Brier; ask for several
  hypotheses first (top-k), which improved calibration.
- Report AUC (selective accuracy) alongside ECE: ECE alone rewards always saying 50%.
