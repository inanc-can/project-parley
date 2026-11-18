---
id: erdogan2026should
title: "Who Should Know What? Empirical Information Design for Multi-Agent LLM Economies"
authors: [Mete Erdogan, Mirac Suzgun, Aneesh Pappu, Guowei Xu, Batu El, Andrew A. Schoen, Furong Huang, John P. Dickerson, Mert Pilanci, James Zou]
year: 2026
arxiv: "2611.07667"
venue: arXiv preprint (v1, 5 Nov 2026)
code: https://github.com/meterdogan07/agent-information-design
read: full
relevance: medium
topics: [negotiation-benchmarks, game-theoretic-evals]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

## Question
When LLM agents trade or bargain for their principals, does giving them more precise information
about the other side raise collective outcomes, or does it make them demand more and destroy value?
"Empirical information design": vary only what each agent is told, holding models, markets,
instructions and rules fixed (pp. 1–3).

## Setup
- Ten models (GPT-5 mini, GPT-6 Luna, GPT-5.1, GPT-6 Sol, Gemini 3.7 Flash, Gemini 3.1 Pro,
  Claude Sonnet 5, Claude Opus 5.5, Grok 4.3, Grok 4.7), two instances of the same model per game;
  plus a mixed-model study of six pairs from four models (pp. 3, 9).
- Three games with known utilities (pp. 3–5):
  - **Multi-resource trade** (from NegotiationArena): public inventories, private per-unit values,
    up to 8 alternating messages, 90 markets split into extraction opportunity for A, for B, or
    equal (App. B.1).
  - **Single-good bargaining**: seller cost c, buyer value v, both from U[20,100]; 15 profitable
    pairs (thin/medium/large surplus), both starting roles, 2/4/6 messages; last message is
    accept/reject only (App. C.1).
  - **Double auction**: 3 buyers, 3 sellers, one sealed bid/ask each, midpoint pricing; 30 markets
    by number of efficient trades × margin of the last one (App. D.1).
- Disclosure levels: **least** (own values only), **coarse** (counterpart's ranking; in bargaining,
  "a profitable price exists"), **full** (counterpart's exact values). Ablations: one-sided
  disclosure, dialogue length, 2/6/10 resources, a welfare-maximizing mediator (pp. 4–5, 9–10).
- Measures (pp. 5–6): realized performance W (share of maximum total gains; in bargaining the
  normalized Nash product 4(v−p)(p−c)/(v−c)², zero for no deal); candidate quality Q (best feasible
  proposal made); realization gap L = Q − W; "extractive counteroffers" (raise own gain while
  lowering the other's and the total).
- Low reasoning effort, provider-default sampling, JSON actions with a private reasoning field in
  bargaining; CIs over markets, not repeated runs (App. F; p. 11).

## Findings
- **Trade, coarse → full** (p. 7): GPT-6 Sol 97.7% → 90.8% of maximum gains, GPT-5.1 97.2% → 88.4%;
  but GPT-6 Luna 68.9% → 79.0%, Claude Sonnet 5 72.1% → 85.6%. Full disclosure raises extractive
  counteroffers (GPT-6 Sol 0.63 → 1.50 per negotiation when B has the opportunity); for GPT-6 Sol
  B gains 11.1 points while A loses 22.5. Sonnet 5 and Grok 4.3 improve both sides' gains.
- **Bargaining** (pp. 7–8): full disclosure can raise agreement while making the split unequal:
  GPT-5.1 at 4 messages, agreement 70% → 93.3%, Nash score among agreements 0.84 → 0.24; Grok 4.7
  at 6 messages 80% → 100% agreement, 0.89 → 0.17, although its best proposal improved 0.79 → 0.97.
  Longer dialogue restores balance for several models (Claude Opus 5.5 0.24 → 0.92 from 2 to 6
  messages).
- **First mover + information** (p. 8): with 2 messages, full disclosure lifts GPT-5.1 sellers'
  share from 68.8% to 97.3% when they start, and cuts it from 27.4% to 0.4% when they respond.
  Grok 4.7 keeps 98.7% vs 17.4% even at 6 messages.
- **Auctions** (pp. 8–9): agents find the efficient pairs (Q > 0.99) but full disclosure makes
  sellers ask more and buyers bid less, so trades fail: Claude Opus 5.5 94.6% → 64.1%, Grok 4.7
  97.4% → 62.1%, Gemini 3.1 Pro 97% → 78% (abstract). Losses concentrate in wide-margin markets.
- **Complexity flips it** (p. 9): at 10 resources full beats coarse in Q for all ten models and in W
  for nine (GPT-5.1 63.8% → 80.4%). More dialogue helps least-information agents more (GPT-5.1
  +30.6 points vs +2.8 under full, 2 → 12 messages).
- **Mediator reverses the preference** (App. B.4, p. 20): a welfare-maximizing mediator does best
  with full information (near-optimal), while direct negotiation does best with coarse.
- Mixed-model pairs (p. 10, App. E.2): auctions worse under full for all six pairs (−4.9 to −14.6
  points); bargaining better under full for every pair in thin-surplus markets (+7.7 to +77.7).
- Behaviour (p. 10, App. E.3): Claude Sonnet 5 tried to accept loss-making offers in 13 of 180
  least/coarse bargaining runs (8 least, 5 coarse; none under full; p. 29), its own reasoning recommending rejection in 11;
  a safeguard blocked all. GPT-5.1 escalates demands in its final offer (13/17 under full vs 2/5
  coarse). One mixed-model case: the seller falsely claims an offer is below its cost, and the
  buyer's private reasoning adopts the claim; the authors say it doesn't establish persuasion.

## Limitations
- Stylized games with known utilities; real principals' preferences are uncertain (p. 11).
- Disclosure is truthful and given by the designer, not chosen strategically by agents (beyond
  chat); no deception treatment.
- CIs over markets only, no repeated runs per input (p. 11); low reasoning effort for all models.
- Effects differ by model with no single direction, so the general claim is "co-optimize model and
  information policy", not a law.
- Same-model self-play in the main study; mixed pairs only for four models.

## Relevance to Parley
- Same lab and partly same authors as [[zhang2026terms]] and [[bianchi2024negotiationarena]]
  ([[zou]]); shows the Zou lab's current focus is controlled economic experiments with LLM agents.
- For [[gap]]: not a persuasion study, but two relevant observations: delegated agents breach
  their own limits without any persuasion (Sonnet accept attempts), and a false cost claim entered
  the counterpart's reasoning. Both anecdotal; they motivate measuring loyalty to limits as a
  baseline before adding persuasion treatments.
- "Who should know what" is a design knob Parley can vary: what a delegate is told about its
  principal's limit, and what leaks to the other side.

## Ideas to borrow
- Candidate quality vs realized performance (Q, W, L = Q − W): separates finding a good deal from
  closing it.
- Count "extractive counteroffers" from true utilities.
- Normalized Nash product as a single score for agreement plus balance.
- Report by starting role; the first-mover effect interacts with information.
- Market construction with pre-registered groups (who has the extraction opportunity), labelled
  before any model run.
- Safeguard that blocks loss-making acceptances, and log the private reasoning to catch
  explanation/action contradictions.
