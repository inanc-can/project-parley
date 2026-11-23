---
id: qiu2025bayesian
title: "Bayesian Teaching Enables Probabilistic Reasoning in Large Language Models"
authors: [Linlu Qiu, Fei Sha, Kelsey Allen, Yoon Kim, Tal Linzen, Sjoerd van Steenkiste]
year: 2025
arxiv: "2503.17523"
venue: arXiv preprint (v3, 15 Jan 2026)
code: data at https://zenodo.org/records/17677329
read: partial
relevance: high
topics: [uncertainty-calibration]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: none
  persuasion_treatment: false
  human_baseline: true
---

Read: main text (§§1–4, discussion) in full and the statistical-test supplement (G). Other
supplements (prompt variants, priors, noise, human-study details, verbalized beliefs) only
skimmed. Results are mostly plots; quoted numbers come from the text and Supplement G. Studied
2026-11-20.

## Question
When an LLM must infer someone's hidden preferences from their choices over several rounds, does
it update its beliefs the way Bayes' rule says it should? If not, can it be taught to, and does
the skill carry over to other tasks? (§1)

## Setup
- Flight recommendation: 5 rounds, 3 flights per round (departure time, duration, stops, price);
  a simulated user with one of 624 hidden preference profiles picks one; the assistant must
  predict the pick and is told the right answer after each round. Accuracy is tested on 100 fresh
  option sets after each round (§2).
- Upper bound: a **Bayesian Assistant** that keeps a probability over all 624 profiles and updates
  it exactly (§2.1).
- Models: Gemini 1.5 Pro, GPT-4.1 Mini, Gemma 2 9B/27B, Llama 3 8B/70B, Qwen 2.5 7B/32B; humans
  acting as the assistant for 48 users (§2.2).
- Training: supervised fine-tuning of Gemma 2 9B, Llama 3 8B and Qwen 2.5 7B on interactions with
  either an **oracle** (always the right answer) or the **Bayesian Assistant** (its best guesses,
  often wrong early on) (§3). DPO and LoRA give similar results (App. C.2).
- Transfer tests: flights with 2–8 features, a hotel task, and web shopping with real products
  (§3.2); 500 human users choosing flights (§3.3).

## Findings
- **LLMs barely update**: all models fall well short of the Bayesian Assistant and most improve
  little after round 1; performance plateaus after one interaction (Fig. 2, §2.2).
- **Prompting doesn't fix it**: chain of thought, numerical formats, 30 rounds instead of 5, and
  base (non-instruction) models all fail to help (App. C.1, §2.2).
- Humans improve over rounds (p = 0.002) but also fall short of the Bayesian standard (§2.2).
- **Training on the Bayesian model's guesses works, and beats training on correct answers**:
  flight accuracy from 37.0% (original) to +24.0% with oracle teaching and +38.5% with Bayesian
  teaching (Supp. G). Fine-tuned 7–9B models beat the larger models and humans (§3.1). Bayesian-
  tuned models agree with the Bayesian Assistant ~80% of the time (Fig. 4).
- **It transfers**: hotel task +16.7% (oracle) vs +29.4% (Bayesian) from 36.7%; web shopping +7.1%
  vs +18.6% from 54.0% (Supp. G). Also to unseen numbers of features (Fig. 5a). A gap remains to
  models trained on shopping directly (Fig. 5c).
- **Stated beliefs get better too**: recommendations derived from the fine-tuned models' stated
  beliefs ("on a scale of 1–5, what is my preference for price?") are more accurate than the
  originals' (§3.1, App. B).
- With real human users, original models do well from round 1 because people's preferences are
  predictable (cheap flights), but they still don't improve over rounds; fine-tuned models do
  (Fig. 6, §3.3).

## Limitations
- The user only reveals choices; no strategic behaviour, no bluffing, no conflict of interest.
- Small models fine-tuned; larger models only evaluated (§3).
- Preference space small enough for exact Bayes in training; transfer targets are still
  recommendation tasks.

## Relevance to Parley
- **Direct evidence that belief updating about another party can be trained and transfers**
  across tasks. That is the skill missing in [[zhang2026terms]] (flat belief error over rounds)
  and [[liu2024dellma]] (probabilities not used).
- A **teaching signal that encodes uncertainty** (the Bayesian model's educated guesses) beats the
  right answers. For a negotiation training study ([[gap]]), distilling from an oracle that acts on
  the posterior (like the TERMS-Bench DP oracle) may be better than training on outcomes alone.
- Open for Parley: does this transfer to an *adversarial* counterpart who hides or misstates
  preferences? Nobody has tested it.

## Ideas to borrow
- Normative upper bound computed exactly in a small, controlled task, then transfer to tasks where
  no such bound exists.
- Compare oracle teaching vs normative-model teaching as two training conditions.
- Ask for stated beliefs and turn them into actions with a fixed rule, to check whether the
  beliefs or the action step is the problem.
