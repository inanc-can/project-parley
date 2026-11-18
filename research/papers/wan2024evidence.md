---
id: wan2024evidence
title: "What Evidence Do Language Models Find Convincing?"
authors: [Alexander Wan, Eric Wallace, Dan Klein]
year: 2024
arxiv: "2402.11782"
venue: arXiv preprint (v2, 9 Aug 2024)
code: https://github.com/AlexWan0/rag-convincingness
read: full
relevance: low
topics: [persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: false
  turn_protocol:
  players: 1
  stakes: opinion
  persuasion_treatment: true
  human_baseline: false
---

## Question
When a retrieval-augmented LLM sees conflicting real web evidence on a contested yes/no question,
which features of a document make the model side with it, and do they match what humans find
credible? (pp. 1–2)

## Setup
- **ConflictingQA**: GPT-4-generated contested yes/no questions stratified over 191 categories
  (e.g. "is aspartame linked to cancer?"); evidence from Google Search top-20 for affirmative and
  negative rephrasings, text only (no URL, date, visuals), best 512-token window by TAS-B
  similarity (pp. 3–4, 11). For LLaMA-2 Chat: 238 questions, 2,208 paragraphs (Table 2, p. 4).
- Stance labels from a GPT-4 + Claude Instant ensemble (kept only when they agree), then filtered
  again so the tested model reads each paragraph's stance correctly alone (pp. 4, 12).
- **Measure**: give the model one Yes and one No paragraph, "use only the information in the above
  text", read Yes/No (log-probs for open models). A paragraph's **win-rate** is how often the answer
  matches its stance against ≥ 5 opposing paragraphs, both orders (pp. 4–5, 15).
- Models: LLaMA-2 Chat 13B, Vicuna 1.5 13B, WizardLM 1.2 13B, GPT-4, Claude v1 Instant (p. 5).
- Two analyses: (1) correlate win-rate with readability, unique tokens, sentiment, perplexity,
  n-gram overlap, question–paragraph embedding similarity, on a dataset balanced per answer
  (pp. 5–6); (2) counterfactual edits by Claude Instant to the Yes paragraph: style edits (add
  science references, more info, contact info; rewrite more confident / technical / objective)
  vs relevance edits (question prefix, keyword stuffing, add one stance sentence, rewrite for
  relevance), against a control suffix "Thanks for reading!" (pp. 6, 15–17).

## Findings
- **Relevance dominates**: question–paragraph embedding similarity correlates strongly with
  win-rate for every model except GPT-4; n-gram overlap weaker but positive; readability and
  unique-token count show no relation; perplexity and sentiment small and model-dependent
  (Fig. 4, p. 6; Figs. 5–8, pp. 13–14).
- **Counterfactuals**: relevance edits raise win-rate substantially, while human-credibility style
  edits (scientific references, neutral tone, confidence, technical language) are neutral or
  negative vs control (Fig. 2, p. 2; p. 6). Prefixing "The following text is about the question:
  [question]" alone substantially improves win-rate (p. 1). Exact effect sizes appear only as a
  bar chart (axis −0.4 to +0.4 mean win-rate change); the text gives no numbers.
- **Stated vs revealed credibility differ**: asked to rate a paragraph's credibility 1–5 alone, the
  model's ratings barely track its actual win-rate (Fig. 3, p. 5), so self-report can't replace
  behavioural measurement (pp. 4–5, 11).
- Real conflicts are often underspecified rather than contradictory (old- vs new-world coral
  snakes, date dependence) (Table 4, p. 7).

## Limitations
- Single turn, two paragraphs, binary answer, no stakes and no adversary that adapts (p. 7).
- Relevance and style edits are made by an LLM and change different amounts of text; only the Yes
  paragraph is perturbed (p. 6). Counterfactual figure doesn't state which model(s) it pools.
- GPT-4 statistics rest on 38 balanced samples (Fig. 6, p. 14); 2023-era models.
- "Use only the information in the text" removes priors, so it measures evidence weighing, not
  resistance to being argued out of a position.
- No human baseline collected; the human comparison is to prior HCI literature (p. 6).

## Relevance to Parley
- Background, not a negotiation paper. For [[gap]] it is **context that narrows the tactic list**:
  in a single-turn evidence setting, appeals humans find credible (scientific references, authority,
  confident or objective tone) did *not* move models, while surface relevance did. That predicts
  small effects for classic Cialdini-style tactics such as authority, consistent with
  [[sakhawat2026areg]] (authority appeals correlate negatively with extraction, ρ = −0.157, p. 6)
  and [[sadab2026receiver]] (framing ≈ 0% of variance).
- It doesn't speak to delegated agents, principals or money, so it neither strengthens nor weakens
  the claim directly. It adds one candidate "tactic" to test in Parley: claims phrased to restate
  the agent's own task or question (relevance mimicry) rather than appeals to credibility.
- Methodological point for Parley: revealed behaviour (what the agent concedes) and stated
  judgement (what it says it finds convincing) can diverge (p. 5), so measure outcomes, not self-reports.
  Compare [[li2026whose]] and [[zhang2026terms]], which also measure behaviour.
- Contrast with [[micelibarone2026used]]: there uninformed agents are credulous to unverifiable
  claims; here models weigh claims by topical fit, not by verifiability cues.

## Ideas to borrow
- Win-rate against a pool of opposing items, both orders, as a robust "convincingness" score.
- A control perturbation ("Thanks for reading!") to separate "any edit" from the targeted change.
- Counterfactual edits that hold content fixed and change one feature, as a template for scripted
  tactic variants of the same offer.
- Check stated vs revealed: ask the agent how convincing a message was and compare with its
  concession.
