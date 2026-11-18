---
id: gajewska2026benchmarking
title: "Benchmarking Argumentative Behaviour of LLMs: A Study of Defences Against Character Attacks"
authors: [Ewelina Gajewska, Katarzyna Budzynska, Jaroslaw Chudziak]
year: 2026
arxiv: "2609.28673"
venue: arXiv preprint (v1, 23 Sep 2026)
code: https://osf.io/9ynx7
read: full
relevance: medium
topics: [persuasion-susceptibility, eval-methodology, judges]
setting:
  multi_turn: false
  turn_protocol:
  players: 2
  stakes: opinion
  persuasion_treatment: true
  human_baseline: true
---

Read all 12 pages (text pp. 1–11, references pp. 11–12) on 2026-11-15. Warsaw University of
Technology. The page header reads "April 2026" while arXiv v1 is dated 23 Sep 2026. Each LLM writes
**one reply** to one character attack taken from a real debate, so `multi_turn: false`; the attacker
is the human line from the corpus. `persuasion_treatment: true` = every response is elicited by an
ad hominem attack (the varied factor is persona grounding). The OSF link holds the prompts and the
annotated dataset (pp. 7–8). The corpus is called both "ElecDeb60to16-fallacy" and
"ElectToDeb60to16-fallacy" in the paper.

## Question
When an LLM is attacked on its character (ad hominem) in a political persuasion dialogue, which
defence does it choose, and does that match human debaters? RQ1: LLM vs human defence strategies.
RQ2: does grounding the LLM in the specific candidate's persona change this? (p. 2)

## Setup
- **Theory** (§3, pp. 4–6): Walton's credibility function made binary — Accept(A) =
  LogicalStatus(A) × Ethos(X). An argument can be defended on the **logical layer** (rebuttal:
  counter-evidence; undercutter: cut the inference) or on the **ethotic layer** (counterattack the
  attacker's character, which sets Ethos(O) = 0 and so neutralizes the attack). Rebuttals and
  underminers are merged into "rebuttal" (footnote 2, p. 5). Builds on Budzynska & Reed's Ad Hominem
  Dialogue game.
- **Data** (§4.2, p. 7): all ad hominem exchanges in U.S. presidential debates 1960–2016 where X
  attacks Y and Y responds: **N = 97 exchanges**.
- **Conditions** (§4.1, pp. 6–7): (1) *Persona-grounded agent*: system prompt to play the specific
  candidate, with Wikipedia background; (2) *Generic agent*: same model as a generic debater;
  (3) *Human*: the candidate's actual reply. Temperature 0.5, **5 responses per context** per model.
- **Models (5)**: Gemini 2.5, Gemini 3.0 Pro, GPT 4.1 mini, GPT 5.1, Grok 4.1 reasoning (Table 1,
  p. 8).
- **Annotation** (§4.3, pp. 7–8): each response classified as rebuttal / undercutter / ethotic
  counterattack by one human expert plus two reasoning LLMs (GPT 5.1, Grok 4.1-reasoning; few-shot
  with definitions); majority vote with human oversight. Cohen's κ human–GPT 5.1 = 0.62,
  human–Grok 4.1 = 0.63 (p. 8).

## Findings
- **Humans** (Table 1, p. 8): rebuttal 59%, undercutter 9%, **ethotic counterattack 32%**.
- **Generic LLMs**: rebuttal 67% (±7), undercutter 18% (±9), counterattack **15% (±8)** — twice the
  human undercutter rate and half the counterattack rate (p. 8).
- **Persona LLMs**: rebuttal 76% (±9), undercutter 7% (±2), counterattack 17% (±9) — persona
  grounding cuts undercutters and slightly raises counterattacks, moving some models toward the human
  distribution (p. 8).
- **Model spread**: GPT 4.1 mini almost never counterattacks (3% generic, 2% persona; 91% rebuttal
  with persona); Gemini 3.0 Pro (24%, 26%) and Grok 4.1 reasoning (23%, 25%) come closest to humans
  (Table 1, p. 8).
- **Qualitative**: when models do counterattack they often turn overtly aggressive or toxic (e.g.
  Grok-persona insulting a third party), which the authors read as models conflating legitimate
  character contestation with hate speech (pp. 9–10).
- **Authors' interpretation**: safety fine-tuning (RLHF for harmlessness) restricts the strategic
  action space in mixed-motive persuasion; persona prompting shifts frequencies but "does not endow
  the model with genuine argumentative reasoning" (pp. 10–11).

## Limitations
- **Tiny and single-turn**: 97 contexts × 5 samples; one reply each, no follow-up, so there is no
  dialogue dynamics, escalation or reinstatement actually observed.
- **No outcome measure**: the paper scores *which* move is chosen, not whether it works — no
  audience, judge of persuasiveness or credibility rating. "Competence" is defined as matching the
  human move distribution.
- **No statistics**: no significance tests or CIs on the distribution differences; Table 1's
  denominator (97 contexts vs 485 samples per cell) is not stated.
- **The safety-tuning explanation is untested**: no base vs aligned model comparison; it is a
  conjecture.
- **Annotator overlap**: two of the three annotators (GPT 5.1, Grok 4.1) are also evaluated models;
  κ ≈ 0.62 is only "substantial".
- Human baseline is professional politicians in high-stakes televised debates, compared with LLMs
  answering a prompt; the human reply had full debate context, the LLM may not (prompt details are
  only on OSF).
- Model versions loosely named ("Gemini 2.5" without variant).

## Relevance to Parley
- **For the map (a)**: a niche entry for **persuasion / argument defence** — measures the
  *propensity* to choose a defence type under a character attack, against a human corpus baseline.
  It is not a game, has no payoff, and no adversary that adapts. Useful as an example of a
  move-taxonomy evaluation (what kind of move, not who won).
- **For the transfer study (b)**: its central claim is itself an interference hypothesis — that
  alignment training for harmlessness *suppresses* a strategically valid social move (ethotic
  counterattack: 15–17% vs human 32%, p. 8). That is the kind of cross-skill side effect (b) wants
  to measure, but the paper does not test it (no pre/post-alignment comparison, no training). A
  study could: take a base and an instruction-tuned model, or SFT/RL a model on negotiation or
  persuasion, and measure the move distribution here before and after. It covers only prompting
  (persona vs generic), which shifts frequencies a little.
- Compared with [[bozdag2025persuade]] and [[sadab2026receiver]]: those measure whether persuasion
  *works* on a model (susceptibility, money moved); this measures what a model does when its
  credibility is attacked, without measuring effect. Compared with [[zeng2024johnny]]: there,
  persuasion techniques are the attack on a model's safety; here, a rhetorical attack probes whether
  safety limits the model's own rhetoric.
- Compared with [[he2026socialgym]] and [[fan2026commerce]], which are rule-scored: this relies on
  hybrid human–LLM annotation (κ 0.62–0.63), a data point for the [[judges]] topic on using LLMs to
  label argument moves.
- Relation to sycophancy work ([[sharma2023understanding]]): over-polite logical defence and reluctance
  to counterattack may share a cause with sycophancy (preference training), but the paper does not
  connect them.

## Ideas to borrow
- **Move-type taxonomy with a human corpus baseline**: classify each agent turn into a small set of
  formal moves (here rebuttal / undercutter / counterattack) and compare distributions with real
  human dialogues. In Parley: classify negotiation turns (offer, concession, threat, appeal to
  fairness, credibility attack) and compare against human negotiation corpora.
- **Persona vs generic ablation** as a cheap prompting arm.
- **Two-layer model (logic × credibility)** as a way to code whether a turn targets the claim or the
  speaker — relevant for detecting manipulation in negotiation transcripts.
- Use it as a **side-effect probe** for (b): measure the move distribution before and after training
  a different skill.

## Map fields
- Skills measured: persuading (argumentative defence of one's position under a character attack);
  other (choice of argument move: rebuttal / undercutter / ethotic counterattack)
- Scoring: mixed (human expert + two LLM annotators, majority vote)
- Agents: 2 (human attacker line from corpus, LLM responder)
- Opponents: human (fixed attack lines from U.S. presidential debates; no live opponent)
- Tests: propensity (which defence the model chooses, compared with humans)
- Training evaluated: prompting (persona-grounded vs generic system prompt)
- Transfer between skills measured: no
- Models tested: Gemini 2.5, Gemini 3.0 Pro, GPT 4.1 mini, GPT 5.1, Grok 4.1 reasoning; human
  debaters from the corpus as baseline
- Code released: https://osf.io/9ynx7 (prompts and annotated dataset)
