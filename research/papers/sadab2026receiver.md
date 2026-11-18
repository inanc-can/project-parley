---
id: sadab2026receiver
title: "Receiver Decides Agent-to-Agent Negotiations"
authors: [Fardeen Sadab, Alif Hasnain, Afsana Shehrin, Md. Azam Hossain, Abu Raihan Mostofa Kamal]
year: 2026
arxiv: "2610.18424"
venue: arXiv preprint (v1, 13 Oct 2026)
code: transcripts, traces and analysis code released (no URL in the PDF)
read: full
relevance: high
topics: [persuasion-susceptibility, negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: money
  persuasion_treatment: true
  human_baseline: false
---

## Question
When one LLM agent asks another for money, which side decides how much changes hands: the
persuader or the holder? And can training move the holder's resistance? (pp. 1–2)

## Setup
- Game: AREG (Sakhawat & Sadab 2026, arXiv 2602.16639). A REQUESTER raises money for a cause
  (emotional appeal, urgency, logic allowed; threats, coercion, deception forbidden). A HOLDER has
  "won $100" and is told to prioritise keeping it. Up to 10 turns each (p. 2, App. C).
- Round robin of 15 agents (frontier, open-weight, small, plus two fine-tuned by the authors);
  every agent meets every other in both roles; 1,049 games (p. 3).
- Framing manipulation: requester advocates for one identifiable person vs a group in crisis
  (p. 3).
- Each reply carries a private reasoning trace. A judge model (grok-4.1-fast, also a player)
  extracts explicit USD commitments; 98.4% agreement between two readings; vs humans MAE $0.22 on
  random turns but much worse on hard cases (κ 0.408 pooled) (p. 3, App. A).
- Variance decomposition with crossed random effects (Social Relations Model) (p. 4).
- Interventions: QLoRA fine-tuning of Qwen3-8B on 8,000 persuasion dialogues containing almost no
  refusals; behaviour-cloning distillation of never-losing holders (grok) into Qwen3-4B
  (pp. 6–7, App. D–E).

## Findings
- **The holder decides.** Holder identity explains 46.7–47.2% of variance in the amount
  transferred, requester identity 1.9–2.1%, matchup 3.0%, framing 0.1% (pp. 4, 12). Removing
  extreme agents narrows it to 22.3% vs 4.3%, but the ratio CI still excludes 1 (p. 4).
- Framing changed the text (named protagonist 79.9% vs 43.5% of turns) but not the outcome:
  19.8% vs 22.0% extracted, equivalence test rules out |d| > 0.2 (p = 0.016) (p. 5).
- Outcomes are bimodal: holder gives nothing in 47% of games, everything in 11% (p. 5).
- **First turn predicts all:** turn-1 refusal rate ranks holders by total losses, ρ = −0.73
  (held-out −0.75); first concession ≤ $5 → gives everything in 4% of games, > $50 → 95%
  (pp. 5–6). About 20 single-turn probes recover the ranking (ρ = −0.74) (p. 17).
- Holder giveaways range 0.0% (grok-4.1-fast) to 83.5%; Claude Opus 4.6 gives 30.2%, GPT-5.4
  12.0% (Table 5, p. 13). Persuading and resisting are uncorrelated across agents (r = 0.14)
  (p. 7).
- **Persuasion fine-tuning erodes resistance:** Qwen3-8B as holder 12.4% → 83.5% given away
  (d = 2.31); turn-1 concession $4.71 → $29.78 (p. 6). A harmful-request benchmark wouldn't
  notice, since nothing asked is prohibited.
- **Distillation installs it:** 842 refusal turns cut a Qwen3-4B student's losses from 94.8% to
  1.0% (p. 7).

## Limitations
- One zero-sum game with a fictional endowment; requester can't deceive, use tools or evidence
  (p. 8).
- Holders are explicitly told to keep the money, so "holder decides" may partly measure
  instruction-following; a neutral prompt wasn't run (p. 8).
- **No principal, no reservation price, no deal**: it is donation resistance, not a negotiation
  where conceding is sometimes correct. Refusing everything is always optimal here.
- Fine-tuning: one backbone, one corpus, no control corpus with refusals; distillation one seed
  (p. 8). Judge is a single model that also plays.

## Relevance to Parley
- **Most direct prior work for [[gap]].** It already shows (a) persuasion moves agents to give up
  resources, (b) the target's identity matters far more than the persuader's, (c) training moves
  resistance both ways. A persuasion study must cite it and differ from it.
- **What it leaves open**, i.e. where [[gap]] still has room: a real negotiation with a principal
  and a reservation price, where the right answer is "concede to the limit, not beyond", not
  "refuse everything". Distillation to always-refuse would fail there (it would block good deals).
  Also: deliberate tactics as treatments (here only one framing contrast), deception/evidence.
- Its finding that requester wording barely matters is a warning: a "which tactics work" study
  may find small effects. Power the design accordingly.

## Ideas to borrow
- Round-robin + crossed random effects to split variance between persuader and target.
- Equivalence tests (TOST) to claim a null.
- First-turn refusal probe as a cheap robustness metric (~20 probes per agent).
- Persuasion fine-tuning as a stress test of defences; distillation from robust teachers as a
  defence baseline.
