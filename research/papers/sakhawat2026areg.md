---
id: sakhawat2026areg
title: "AREG: Adversarial Resource Extraction Game for Evaluating Persuasion and Resistance in Large Language Models"
authors: [Adib Sakhawat, Fardeen Sadab]
year: 2026
arxiv: "2602.16639"
venue: arXiv preprint (v1, 18 Feb 2026)
code: none stated in the PDF
read: full
relevance: medium
topics: [persuasion-susceptibility, game-theoretic-evals, judges]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: money
  persuasion_treatment: false
  human_baseline: false
---

## Question
Is an LLM's ability to persuade related to its ability to resist persuasion, when both are
measured by money actually handed over in a zero-sum game? (pp. 1–2)

## Setup
- The original AREG paper; [[sadab2026receiver]] reuses the game at larger scale.
- Two roles. **Culprit** (persuader): "friendly, enthusiastic salesperson or fundraiser", told no
  pressure, threats or deception; it can't see the victim's budget. **Victim**: a "savvy consumer"
  who just won $100 in a lottery and should "prioritize keeping your winnings". Both at T = 0.7
  (pp. 3, 14–15).
- Strict alternation, at most 10 turns; the game ends when the budget hits $0 (p. 3).
- **Arbiter** (Grok 4.1 Fast, T = 0) reads each victim reply and extracts only *new, unconditional*
  cash handovers ("Here is $20"); promises, conditionals and restatements count $0; it outputs
  JSON with amount, type (donation/investment/purchase), confidence (pp. 3–4, 14–15).
- 8 models (GPT-5.2, Llama 4 Maverick, DeepSeek V3.2, Grok 4.1 Fast, Llama 3.3 70B, Gemini 2.5
  Flash, Qwen3 Next 80B, Mixtral 8×7B) via OpenRouter, Jan 2026. Round robin, both roles, 5
  rounds: 280 games, 2,781 arbiter verdicts (pp. 4–5, 10).
- Score: extraction ratio S = (100 − B_final)/100, fed into separate "linear Elo" ratings for
  persuasion (C-Elo) and resistance (V-Elo), K = 24, start 1500 (p. 4).
- Linguistic markers (verification requests, refusals, reciprocity, authority…) correlated with
  outcomes; how markers were coded isn't described (p. 6).

## Findings
- **Resistance beats persuasion for every model**: V-Elo > C-Elo, mean spread +216. GPT-5.2 is
  the best defender (V-Elo 1694, $0 lost in 65.7% of games); Mixtral the worst (1502, 5.7%)
  (Table 1, p. 5).
- **Persuading and resisting are weakly related**: Spearman ρ = 0.33, p = 0.42 (n = 8). Pearson
  r = 0.634 on the same data (Table 4, p. 11), so "dissociated" rests on 8 points. Top persuader
  DeepSeek V3.2 is 5th at resisting; top defender GPT-5.2 is 5th at persuading (p. 5).
- **Early window**: 57.5% of commitments happen in turns 1–3; with nothing by turn 5, the chance of
  any later extraction is < 4% (p. 6). Per-turn success peaks at 20.4% in turns 2–3 and falls to
  3.6% in turns 6–10 (Table 5, p. 11). First commitment size correlates with total extraction,
  ρ = 0.808 (p. 8).
- **Foot-in-the-door works**: culprits getting ≥ 3 separate commitments extract 61.4% on average vs
  22.2% for a single ask (2.8×, p < 10⁻⁸) (p. 6). Observational, not a manipulated treatment.
- **Defence by procedure, not refusal**: verification requests correlate with resisting
  (ρ = +0.377, p < 0.001), delay +0.182; explicit refusal −0.135 and mentioning one's budget
  −0.156 correlate with *losing* (Table 2, p. 6). Persuader side: reciprocity +0.213, authority
  appeals −0.157 (p. 6).
- **Victim matters more than attacker, by eye**: per-victim mean loss ranges from 4.1% (GPT-5.2)
  to 37.1% (Mixtral); DeepSeek is the strongest extractor against 7 of 8 victims (Table 6, p. 12);
  best single cell 65% (DeepSeek vs Mixtral), GPT-5.2 never loses > 10% on average (Table 7, p. 12).
- **"Friendly jailbreak"**: told not to deceive, culprits still invent named people, charities and
  distress stories (manual review, no rate given) (p. 8). 94% of successful extractions use a
  donation frame (n = 188) (p. 13).
- Arbiter: confidence 1.0 on 96.1% of verdicts; a manual audit of 45 transcripts found zero errors
  (p. 5). No inter-judge or human agreement statistic.
- Shorter persuaders do better: culprit/victim length ratio ρ = −0.136, p = 0.023 (Table 10, p. 13).
  No relation of scale or price to either skill (p > 0.15) (p. 7).

## Limitations
- n = 8 models; the core "dissociation" claim is a non-significant correlation, i.e. absence of
  evidence, and the Pearson value is 0.63 (p. 11). No CIs on Elo; Elo depends on game order.
- Tactics aren't controlled: every strategy result is a correlation between coded markers and
  outcome, with the coding method unstated. Confounded by victim identity (better defenders may
  simply both verify more and lose less).
- One arbiter that is also a player (Grok), validated only by its own confidence and a 45-transcript
  audit (pp. 5, 9). [[sadab2026receiver]] later found much weaker human agreement on hard cases.
- Single scenario (lottery winner vs charity/sales), English only, Jan 2026 snapshot (pp. 9–10).
- Some internal inconsistencies in the appendix (e.g. turn-5 extraction probability "< 4%" on p. 6
  vs "< 10%" on p. 11; Table 8's turn 6–10 share 18.5% vs Table 5's 3.6%, which measure different
  things but aren't labelled clearly).
- No principal and no limit: refusing everything is always optimal for the victim, so it measures
  resistance, not loyalty within a real negotiation.

## Relevance to Parley
- Same game and author as [[sadab2026receiver]]; that note is the stronger, larger version (15
  agents, variance decomposition, framing manipulation, fine-tuning). Cite AREG for the game
  design and the original observations, Sadab for the effect sizes.
- **For [[gap]]**: it supports the mechanism (language alone moves money out of an agent, and the
  victim's identity dominates) but, like [[sadab2026receiver]], has no principal, no reservation
  value and no correct deal. It narrows the claim's novelty on "persuasion with money outcomes",
  leaving open: tactics as randomised treatments, a principal's limit, and costs measured against
  that limit. Compare [[li2026whose]] (principal and limits, but binary harm, no money) and
  [[zhu2025automated]] / [[zhang2026terms]] (money and limits, no deliberate persuasion).
- Its observational tactic findings become testable hypotheses for Parley: does foot-in-the-door
  (incremental asks) raise concessions beyond the limit when assigned at random? Does a
  "verify before conceding" defence prompt reduce them, compared with a "refuse" prompt? That
  is a prompting arm for the prompting / fine-tuning / RL comparison ([[liu2026instructing]]).
- Spontaneous fabrication by the persuader echoes [[micelibarone2026used]]: a scripted tactic seat
  in Parley needs an honesty check, or "tactic" effects will include lying.

## Ideas to borrow
- Arbiter that counts only new, unconditional commitments and the delta on increases; give it the
  running ledger so restatements aren't double counted.
- Separate offence and defence ratings per model; report both, not one "social" score.
- Turn-of-first-concession and first-concession size as early predictors (also in
  [[sadab2026receiver]]); cheap probes for screening agents.
- Code victim replies for verification vs refusal vs budget disclosure as process measures.
- Avoid: judge drawn from the player pool; Elo on n = 8 without CIs.

## Map fields
- Skills measured: persuading (extracting money as a salesperson), resisting persuasion (keeping lottery winnings)
- Scoring: mixed (an LLM arbiter extracts unconditional handovers; rules compute the extraction ratio and Elo)
- Agents: 2
- Opponents: LLM (round robin, both roles)
- Tests: capability
- Training evaluated: none
- Transfer between skills measured: no
- Models tested: GPT-5.2, Llama 4 Maverick, DeepSeek V3.2, Grok 4.1 Fast, Llama 3.3 70B, Gemini 2.5 Flash, Qwen3 Next 80B, Mixtral 8×7B
- Code released: none stated in the PDF
