---
id: bozdag2025persuade
title: "Persuade Me if You Can: A Framework for Evaluating Persuasion Effectiveness and Susceptibility Among Large Language Models"
authors: [Nimet Beyza Bozdag, Shuhaib Mehri, Gokhan Tur, Dilek Hakkani-Tür]
year: 2025
arxiv: "2503.01829"
venue: CAIS '26 (ACM Conference on AI and Agentic Systems), per the v4 PDF (27 May 2026)
code: https://beyzabozdag.github.io/PMIYC/
read: full
relevance: high
topics: [persuasion-susceptibility, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: opinion
  persuasion_treatment: false
  human_baseline: false
---

## Question
How persuasive are LLMs at convincing *other LLMs*, and how easily are they persuaded, in multi-turn
agent-to-agent conversation? Does this depend on single- vs multi-turn, subjective vs
misinformation claims, and model family/size? (pp. 1–2)

## Setup
- **PMIYC** (UIUC). Persuader (ER) is told to make the Persuadee (EE) "completely support" a claim;
  the Persuadee is told to be "sensible" and may change its stance. Code adapted from
  [[bianchi2024negotiationarena]] (pp. 3, 25; prompts Figs. 32–36, pp. 24–25).
- Strict alternation, Persuadee speaks first. After every message the Persuadee self-reports
  agreement on a 1–5 Likert scale; the Persuader also self-ranks, hidden from the other side. Early
  stop if Persuadee hits 5; always a final-decision prompt that restates the claim (Alg. 1, p. 3;
  App. B, p. 11).
- Single-turn t = 3 (one argument); multi-turn t = 9 (four Persuader turns) (pp. 5–6). Persuadee's
  opening message and score are fixed per claim across Persuaders for fairness (p. 4).
- Metric: **normalized change in agreement (NCA)** in [−1, 1], scaled by the room left to move up
  (5 − s₀) or down (s₀ − 1). Effectiveness = mean NCA as Persuader; susceptibility = mean NCA as
  Persuadee (Eq. 1, p. 4).
- Claims: 961 subjective (Durmus et al. + Perspectrum) and 817 misinformation (TruthfulQA question
  + first incorrect answer) (pp. 4–5; topic breakdown Table 2, p. 11).
- Models: GPT-4o-mini, GPT-4o, GPT-4.1(-mini), o4-mini, Claude 3 Opus, Claude 2, Claude 3 Haiku,
  Llama-3.1-8B, Llama-3.3-70B, Qwen-3-32B (thinking off). Full round-robin, **one run per
  pair × claim** (pp. 4, 6).
- Validity checks: initial-stance consistency over 5 repeats (Table 1, p. 6); 12 human annotators
  on 125 conversations (p. 7, App. G); action-based MCQs (p. 8, App. D.2); GPT-4o judge (App. D.1);
  utterances labelled with the [[zeng2024johnny]] 40-technique taxonomy by GPT-4o-mini (App. F).

## Findings
- **Multi-turn raises persuasion**: e.g. GPT-4o persuading GPT-4o 0.40 → 0.64 NCA from single- to
  multi-turn; susceptibility generally rises over turns (p. 6). Influence peaks at the first and
  second persuasive attempts (Fig. 7, p. 7).
- **Single-turn ranking matches human data** from Durmus et al.: Claude 3 Opus 0.56 > Claude 3
  Haiku 0.43 > Claude 2 0.24 effectiveness (p. 6).
- **Persuasiveness is stable across domains, susceptibility is not** (Figs. 5–6, p. 5). o4-mini (the
  only reasoning model) is both the most effective Persuader and the least susceptible; its
  misinformation susceptibility is below 0. GPT-family and Qwen-32B show >50% more resistance to
  misinformation than the rest (p. 6). Abstract: Llama-70B ≈ GPT-4o in persuasiveness, both ~30%
  above Claude 3 Haiku; GPT-4o >50% more resistant to misinformation than Llama-70B (p. 1).
  Claude 3 Haiku is the most susceptible multi-turn Persuadee (p. 6).
- Variance check (only Llama-70B vs itself, 3 runs): NCA 0.71/0.70/0.71 (SD 0.005) subjective,
  0.65/0.65/0.63 (SD 0.010) misinformation (p. 6). Initial stances are stable except Llama-8B
  (avg SD 0.49, match rate 16%) (Table 1, p. 6).
- **Stated vs real stance**: weaker Persuaders get pulled to the Persuadee's side; the Persuadee then
  "agrees" with the drifted position, and its agreement collapses when the final prompt restates
  the original claim (p. 7, example Fig. 31, p. 23). Claude 3 Haiku's stance adherence falls to
  ~45% (subjective) and < 10% (misinformation) by turn 4 (Fig. 9, p. 8); utterance-level 65% vs
  94–98% for most models (App. F.2, p. 15).
- **Self-reports are a decent proxy**: humans match the model's 3-way stance 76% of the time,
  κ = 0.63, mean abs. difference 0.51 points (p. 7). GPT-4o judge matches 0.95 (subjective) and
  0.87 (misinformation) (App. D.1, p. 12). Action-based MCQ agrees with self-report > 90% in most
  cells; in misinformation 64–78% of cases pick the false answer *and* report support ≥ 4
  ("genuine persuasion") (p. 8; Table 3, p. 12: GPP 64.0% GPT-4o to 77.7% GPT-4o-mini; opinion
  match only 69.1% for Llama-70B in misinformation).
- **LLMs can't judge persuasiveness directly**: picking the more persuasive of two human-rated
  arguments, GPT-4o 54.6%, GPT-4o-mini 51.6%, Llama-3-70B 49.3%; a trained Llama-8B reward model
  47.2% (App. E, p. 12).
- Persuaders are more effective when they themselves agree with the claim (Fig. 8, p. 8).
- **Tactic use when free-running** ([[zeng2024johnny]] taxonomy): information-based techniques
  (Evidence-based Persuasion, Logical Appeal) are 65–97% of utterances; o4-mini uses
  Evidence-based Persuasion in 83% (subjective) / 84% (misinformation) of utterances; Claude 3 Haiku
  uses Alliance Building 13% in misinformation; Deception, Social Sabotage and Threats are
  "virtually absent" (perhaps missed by the judge) (pp. 8, 16; Figs. 10, 20–21).
- Generation success > 96% (subjective) and 99% (misinformation); refusals and format failures are
  the losses, most often Claude 3 Haiku as Persuader (App. B.0.1, p. 11).

## Limitations
- **Stakes are opinions**: a Likert self-report on debate claims or trivia, no resource, no
  principal, no cost to conceding. The Persuadee is told to be open-minded, so "susceptibility" on
  subjective claims is partly instructed behaviour, not a failure.
- **Tactics are observed, not manipulated**: technique labels come post hoc from one GPT-4o-mini
  judge on a 50-claim sample against one Persuadee (App. F, p. 13). No causal tactic effect.
- One run per pair × claim; variance shown only for one pair (p. 6). No significance tests on the
  heatmaps.
- Mostly older models (Claude 3, GPT-4o era); the only reasoning model is o4-mini.
- Strict turn protocol by design; authors flag natural turn-taking as future work (App. B, p. 11).
- The self-report scale can be gamed by claim drift (the Haiku case); the final restated-claim
  prompt is what catches it.

## Relevance to Parley
- **Pre-empts the generic version of [[gap]]**: "multi-turn agent-to-agent persuasion
  susceptibility, measured per model" exists, with a round-robin design and a published normalised
  metric. The claim has to sit on what PMIYC lacks: a principal with a limit, money outcomes, and
  tactics as controlled treatments.
- **Supports tactics as treatments**: left free, LLM persuaders almost only argue with evidence and
  logic and never use authority, scarcity, threats or deception (p. 16). So a study of *which
  tactics* break agents can't rely on free-running persuaders: it needs scripted tactic seats, as
  [[gap]] proposes.
- **Supports measuring actions, not stated agreement**: stated agreement drifts and reverses at the
  final prompt (p. 7), and action-based MCQs disagree with self-reports in up to ~31% of
  misinformation cases (Table 3, p. 12). A deal price is a cleaner outcome than a Likert stance.
- **Judges**: LLMs are at chance on judging persuasiveness (p. 12): another reason to score by
  outcome (money), as in [[li2026whose]]'s judge-fragility warning.
- vs [[sadab2026receiver]]: both find the *target* matters a lot (o4-mini resists almost
  everything; Haiku gives in). Sadab adds money and a variance decomposition (holder ~47%, wording
  ~2%); PMIYC adds a domain split (factual resistance vs subjective openness). Together: rank agents
  by resistance, and expect small tactic effects unless tactics are strong and deliberate.
- vs [[micelibarone2026used]]: both observe credulity to unverifiable claims, but PMIYC's is about
  trivia, not counterparty claims that move a price.
- Built on [[bianchi2024negotiationarena]]'s code, so its harness is close to a negotiation
  platform; the persuasion and negotiation lines already share tooling.

## Ideas to borrow
- NCA normalisation (scale change by room left) for any "how far did the agent move" metric, e.g.
  concession as a fraction of the distance to the reservation value.
- Fixed opening for the target across all persuaders, so persuader comparisons are fair.
- Final-decision prompt that restates the original terms, to catch drift (in Parley: restate the
  principal's limit before the binding accept).
- Effectiveness/susceptibility as two separate per-model scores from one round-robin.
- Post-hoc tactic labelling with the [[zeng2024johnny]] taxonomy as a manipulation check: confirm a
  scripted tactic seat really used the assigned tactic.
- Domain split as a control: a condition where giving in is *correct* (like their subjective claims)
  so resistance can't be won by refusing everything.

## Map fields
- Skills measured: persuading (effectiveness), resisting persuasion (susceptibility), other: misinformation claims vs subjective claims
- Scoring: mixed (persuadee's self-reported 1–5 agreement; human annotators and a GPT-4o judge as validity checks)
- Agents: 2
- Opponents: LLM (full round robin)
- Tests: both (persuasion effectiveness; susceptibility as persuadee)
- Training evaluated: none
- Transfer between skills measured: no
- Models tested: GPT-4o-mini, GPT-4o, GPT-4.1, GPT-4.1-mini, o4-mini, Claude 3 Opus, Claude 2, Claude 3 Haiku, Llama-3.1-8B, Llama-3.3-70B, Qwen-3-32B
- Code released: https://beyzabozdag.github.io/PMIYC/
