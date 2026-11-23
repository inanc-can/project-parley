---
id: zhang2026terms
title: "TERMS-Bench: Diagnosing LLM Negotiation Agents Beyond Deal Rate"
authors: [Erica Zhang, Fangzhao Zhang, Aneesh Pappu, Batu El, Jose Blanchet, Susan Athey, Jiashuo Liu, James Zou]
year: 2026
arxiv: "2605.13909"
read: partial
relevance: high
topics: [negotiation-benchmarks, eval-methodology, game-theoretic-evals]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read: main paper pp. 1–13 in full; from the appendix only E (oracle interventions, pp. 40–42),
C.5.4 (voice layer), H.1.5 (agent interface), H.5.2 (example traces, pp. 66–67) and the bankroll
supplier modes (J, pp. 75–76). The other ~60 appendix pages are unread. Studied 2026-11-10/14.

## Question
Deal rate and LLM-vs-LLM play can't say *why* a negotiation agent fails, because the opponent's
preferences are unknown and vary. Can a fully specified opponent act as the verifier, so that
failures can be attributed to the agent?

## Setup
- Bilateral single-price negotiation, up to K alternating-offer rounds (v2 of arXiv
  2605.13909, 13 Jun 2026; Stanford, equal advising Liu and Zou). The agent sends
  Offer/Accept/Reject + price + message, and reports a belief about the opponent's type each
  round (pp. 4, 8).
- **Scripted counterpart:** private type = reservation price, urgency, stance (conciliatory /
  neutral / aggressive). Acceptance, walk-away and concessions come from fixed stochastic
  formulas of that type (Eqs. 5–9, pp. 6–7). After the move is fixed, latent cues (sentiment;
  concede/hold/pressure) go to a voice LLM (GPT-5.2) that writes the message and can't change
  the price (pp. 7–8, App. C.5.4).
- The agent knows only its own reservation price. The evaluator sees everything (p. 4).
- Three regimes: overlap, urgency-shift, no-deal (p. 7).
- **Six counterpart families** on two axes (p. 5): driven by latent type vs by the agent's recent
  behaviour; cues revealing vs muted → CANDID, TACITURN, EXPRESSIVE, STRATEGIC, plus STOCHASTIC
  and ADVERSARIAL. Family is hidden from the agent.
- 1,800 seeded episodes per agent, identical across agents; 13 LLMs via OpenRouter at
  temperature 0, reasoning effort xhigh where available, one rollout per episode; three
  fixed-concession baselines (p. 8).
- Metrics (Table 1, p. 5): surplus efficiency SE+ (= agreement rate × conditional surplus),
  agreement rate on feasible episodes, false agreement on no-deal episodes, belief error on the
  type, critical violation rate, %Oracle.
- **Oracle ladder** (Eq. 4, p. 6; App. E): base → given the exact Bayesian posterior summary →
  given the true type → dynamic-programming oracle (which acts on the posterior, not the true
  type). Gaps = inference + uncertainty + control.
- Extensions: Amazon price data (831 products, 14 categories) with the counterpart unchanged
  (§4.3); commerce mode with unit economics, and bankroll mode chaining 50 periods with a cash
  ledger and bankruptcy (§4.4).

## Findings
- **Deal rate is saturated, value isn't.** All LLMs but GPT-4o-mini close 93.4–99.9% of feasible
  deals; SE+ ranges 0.522 (Doubao, 99.9% agreement) to 0.694 (Claude Opus 4.6). GPT-4o-mini
  0.189, below the simplest fixed baseline (0.273) (Table 2, p. 8; F1, p. 9).
- No-deal discipline: false agreement 0 for all but Qwen3.6-Plus (0.17%); critical violations
  up to 2.06% (Qwen), 1.50% (Grok 4.20), 1.33% (GLM-5.1) (Table 2, p. 8).
- **Cue penalty:** every LLM earns less against cue-revealing families than cue-muted ones,
  −0.009 to −0.063 SE+; 9 of 13 CIs exclude zero, Wilcoxon p < 10⁻³. Warm cues → over-concession,
  pressure cues → brittle play. ADVERSARIAL is the lowest-surplus family for most agents;
  STOCHASTIC stays competitive (F2, p. 9).
- **Information–action gap** (F3, pp. 9–10): the posterior intervention closes 1% of the oracle
  gap for Claude Opus 4.7 and −6% for GPT-4o-mini; belief error is flat or rising over 10 rounds
  for every frontier model; inference penalty (type-driven minus reactive families) is negative
  for 10 of 13 (Wilcoxon p = 0.007, but no single CI excludes zero).
- **Different bottlenecks** (F4, p. 10): GPT-4o-mini is control-limited (98% of its gap); Claude
  Opus 4.7 (130%) and Grok 4.20 (82%) are uncertainty-limited; Claude Opus 4.6 mixed (18/53/29).
- **Stable fingerprints** (F5, p. 10; pp. 65–67): five styles (anchor-and-hold, mid/balanced,
  anchor-and-concede, accepter, refuser); no agent changes style across families. Firmness in
  deals and respecting one's own limit in no-deal episodes are independent (GLM-5.1 firm but
  breaches; Doubao soft but exits cleanly).
- Example traces (pp. 66–67): Claude Opus 4.6 opens 88, concedes to 83 then 79, accepted, ≈0.89
  of surplus; GPT-4o-mini opens 90, rejects after one counter, no deal although one was feasible.
  The GPT-5.4 "accepter" example reports ≈0.0 surplus at a close equal to the buyer's reservation,
  which looks inconsistent with the stated reservations (would be ≈1.0 for a seller); unresolved.
- **Amazon data** (F6, p. 11): rank correlation with synthetic SE+ ρ = 0.90 over 11 models;
  stronger models gain, weaker lose; cue penalty shrinks for all 11 (p = 0.001), inference
  penalty grows for 10 of 11 (p = 0.002).
- **Money** (F7–F8, p. 12): over 192 commerce scenarios Claude Opus 4.6 leaves 29% of feasible
  profit unrealized vs 50% for the best fixed baseline and 80% for GPT-4o-mini. Bankroll from
  $100: five models end at $380–443 with no ruin; Grok 4.20 $110 (1 of 4 sessions ruined);
  GPT-4o-mini $21 (half ruined). Spread ~21× vs ~14× in SE+.

## Limitations
- **The counterpart never adapts or persuades.** Its type is fixed. In bankroll POOL mode the
  agent carries beliefs about 5 recurring suppliers, but suppliers learn nothing about the agent
  (p. 76). Exploitation of the agent over time is untested by design.
- Single scalar price, two parties; multi-issue and human studies are named as next steps (p. 13).
- The oracle is optimal only relative to the simulator, not to human negotiation (p. 6).
- Conclusions about language rest on cues voiced by one LLM (GPT-5.2), with three postures and
  three sentiments.
- One rollout per seeded episode at temperature 0; CIs are over episodes.
- A 2026 preprint; check for a peer-reviewed version before citing.

## Relevance to Parley
- **Evidence for [[gap]]:** language cues alone, with prices held fixed, make every frontier agent
  concede more (cue penalty). That's the controlled effect the persuasion claim needs, in its
  weakest form: incidental tone, not deliberate tactics.
- **Its limit is Parley's opening:** no adaptive or deliberately persuasive opponent. A tactic
  delivered on purpose, followed up and adapted to the agent is what [[gap]] studies and
  TERMS-Bench can't.
- Directly relevant to [[zou]] (equal-advising author) and to the NegotiationArena line
  ([[bianchi2024negotiationarena]]); a must-cite in any outreach to his lab.
- Possible environment for training or comparison (prompting / fine-tuning / RL), since it gives
  a verifiable reward. Whether the code supports training is unchecked
  (https://github.com/Terms-bench).

## Ideas to borrow
- Separate the economic move from its wording, so tone can be manipulated with outcomes held
  fixed (voice layer can't change price). This is how to make tactics clean treatments in Parley.
- Paired counterpart families that differ in one parameter, compared with Wilcoxon tests across
  models.
- Elicit a belief about the opponent every round and score it against ground truth.
- Oracle ladder (base → posterior → revealed → oracle) to split losses into inference,
  uncertainty and control.
- Report agreement separately on feasible and infeasible episodes; SE+ = agreement × conditional
  surplus.
- Bankroll mode as a compounding-loss stress test.

## Map fields
- Skills measured: negotiating value (bilateral single-price bargaining), other: belief inference about the counterpart's hidden type (reported every round), acting under uncertainty, walk-away discipline on no-deal episodes
- Scoring: rules (surplus efficiency, agreement and false agreement, belief error against the true type; oracle ladder)
- Agents: 2
- Opponents: scripted (six counterpart families; an LLM only voices moves already fixed by formulas)
- Tests: capability
- Training evaluated: none (oracle information given in the prompt as a diagnostic, no training)
- Transfer between skills measured: no
- Models tested: 13 LLMs incl. Claude Opus 4.6 and 4.7, GPT-5.4, GPT-4o-mini, Grok 4.20, GLM-5.1, Qwen3.6-Plus, Doubao (full list not in the note); three fixed-concession baselines
- Code released: https://github.com/Terms-bench
