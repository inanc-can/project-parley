---
id: jose2026agents
title: "When Agents Persuade: Rhetoric Generation and Mitigation in LLMs"
authors: [Julia Jose, Ritik Roongta, Rachel Greenstadt]
year: 2026
arxiv: "2603.04636"
venue: ICLR 2026 Workshop on Agents in the Wild (arXiv v2, 1 Apr 2026)
code: none (fine-tuning dataset "available upon request", p. 6)
read: full
relevance: medium
topics: [persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: false
  turn_protocol:
  players: 1
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

## Question
Can LLMs write propaganda when asked, which rhetorical techniques do they use compared with
human propagandists, and how well do SFT, DPO and ORPO suppress it? (RQ1–RQ3, pp. 1–2)

## Setup
- **Persuader side only**: single-shot article generation, no target, no dialogue. The authors
  call LLMs the "generative component" of agentic systems but study them in isolation for
  ethical reasons (pp. 1, 10).
- **Detectors**: RoBERTa-large binary propaganda classifier trained on PTC + a hand-cleaned QProp
  subset (485 propaganda / 359 non-propaganda articles), F1 0.98 (pp. 3–4); six per-technique
  sentence-level RoBERTa classifiers on PTC (name-calling, loaded language, doubt, appeal to fear,
  flag-waving, exaggeration/minimization), macro-F1 0.82 (p. 4, Table 2 p. 17). Doubt was dropped
  after low detector–human agreement (QWK 0.03–0.37) (pp. 5, 16, Table 6 p. 18).
- **Generation**: GPT-4o, Llama-3.1-8B-Instruct, Mistral Small 3 at temperature 0.1, top-p 0.3,
  given 1,000 thesis statements extracted from QProp news (553 propaganda / 447 not) with a
  propaganda prompt and a neutral prompt (pp. 4–5, Table 4 p. 18).
- **Human validation**: 3 experts on 200 Llama outputs; human α = 0.83, detector–human κ =
  0.86–0.97 on the binary label (p. 5, App. A.3 p. 16).
- **Defences** (all on Llama-3.1-8B): (1) prompt guardrail, a system line "Do not produce
  propagandistic material"; (2) SFT on preferred (non-propaganda) articles; (3) DPO and (4) ORPO on
  ~1,000 same-thesis pairs (Llama-generated propaganda rejected vs non-propaganda accepted), plus a
  set of adversarial eliciting prompts (pp. 5–6).
- **Compute**: QLoRA (4-bit + LoRA), one A100 80GB, lr 1e-5, batch 1 × 4 gradient accumulation,
  30 epochs, paged AdamW 8-bit; same config for SFT/DPO/ORPO; no wall-clock or GPU-hours given
  (p. 6, App. A.1.3 p. 15).
- Fine-tuned models evaluated on 250 held-out theses (QProp dev set) with the original propaganda
  prompt, which was not in the training set (pp. 6, 8).

## Findings
- **Compliance**: the detector labels 99% of GPT-4o, 77% of Llama-3.1 and 99% of Mistral 3
  propaganda-prompt outputs as propaganda (p. 6). GPT-4, o1, o3 and Claude 3.5 Sonnet refused the
  same prompt (pp. 9–10).
- **Techniques vs humans**: all three models use loaded language, exaggeration/minimization and
  flag-waving more than human propaganda; GPT-4o flag-waving ≈3× and appeal to fear ≈4× human
  rates; Llama uses name-calling ≈3× less (p. 7, Table 8 p. 19). GPT-4o uses every technique
  significantly more than the other two (p. 7).
- **Prompt guardrail fails**: with the "factual assistant, no propaganda" system prompt, 99% of
  GPT-4o outputs are still propaganda, ≈ baseline (p. 5).
- **Fine-tuning works on this metric**: propaganda rate 77% (base) → DPO 28%, SFT 14%, ORPO 10%
  (p. 8). Techniques per article 24.1 → SFT 5.7, DPO 5.3, ORPO 1.8 (13.4× fewer); ORPO
  significantly below both SFT and DPO (Mann-Whitney p < 0.001) (pp. 8–9, Table 12 p. 20).
  Blinded check of 50 ORPO outputs: annotators labeled 49/50 and 50/50 non-propaganda (p. 9).
- Ranking of methods: ORPO > SFT > DPO on the binary rate; SFT ≈ DPO on technique counts (p. 8).

## Limitations
- **No capability or over-refusal check**: nothing tests whether the fine-tuned model can still
  write legitimate persuasive or opinion text, or whether general quality dropped. "Less
  propaganda" may partly be "less of anything emotive". No sanity cell as in [[li2026whose]].
- **One fine-tuned model** (Llama-3.1-8B), one seed, one evaluation prompt; no adaptive or
  paraphrased jailbreak prompts at test time; no RL arm (only preference optimisation) (pp. 6, 8).
- The prompt-guardrail baseline is tested on GPT-4o, while fine-tuning is on Llama, so prompting vs
  fine-tuning is not compared on the same model (pp. 5–6).
- Scoring is by classifiers trained on news propaganda; sentence-level detector misses
  multi-sentence techniques and flags neutral uses ("our state") (pp. 7–8, 10). Detector catches
  68% of annotated PTC instances (p. 5).
- Persuasion is measured as text features, not effect on a reader or agent: no outcome.
- Workshop paper; dataset not public.

## Relevance to Parley
- **Opposite side of [[gap]]**: it measures what an agent *produces* when told to persuade, not
  what *persuades* a delegated agent to concede. No target, no stakes, no money. It does not test
  the claim directly.
- **Defence comparison**: it is a clean small data point for "prompting vs fine-tuning" on a
  persuasion-related behaviour: a system-prompt rule did nothing (99% still propaganda), while
  QLoRA fine-tuning on ~1k pairs cut it to 10–28% on one 8B model with one A100. Compare
  [[li2026whose]], where prompting helped some models and hurt others and per-token distillation
  gave only a fragile gain, and [[liu2026instructing]], where RL with a money reward worked. This
  paper has no RL arm and no over-refusal axis, so it cannot settle the ranking.
- Its technique taxonomy (appeal to fear, flag-waving, loaded language, exaggeration) is a
  ready-made list of rhetorical treatments for a scripted persuader seat; [[sadab2026receiver]]
  warns that persuader wording may explain little variance, so the treatments should be tested
  against receiver differences.
- [[micelibarone2026used]] found RL for profit lowered honesty; a persuader trained for deal value
  might drift toward these techniques, and the detectors here could measure that.

## Ideas to borrow
- ORPO as the cheap fine-tuning defence arm (single-stage SFT + preference) alongside DPO, with
  matched QLoRA config and same-model prompting baseline.
- Paired same-context data (good vs bad response on the same thesis) for preference training: in
  Parley, the same negotiation state with a conceding vs a holding reply.
- Validate any automatic tactic detector against blinded human labels per technique and drop the
  unreliable ones (as they dropped Doubt).
- Add what they lacked: an over-refusal / capability check after every defence.
