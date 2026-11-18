---
id: bianchi2024negotiationarena
title: "How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis"
authors: [Federico Bianchi, Patrick John Chia, Mert Yuksekgonul, Jacopo Tagliabue, Dan Jurafsky, James Zou]
year: 2024
arxiv: "2402.05863"
venue: arXiv preprint (v1, 8 Feb 2024)
code: code/negotiation-arena
read: full
relevance: high
topics: [negotiation-benchmarks, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: true
  human_baseline: false
---

Read all 16 pages (main text pp. 1–8, appendices A–E pp. 11–16) on 2026-11-15. Metadata checked
against the arXiv API (only v1 exists). `persuasion_treatment: true` because §4 gives one agent
"Cunning" (insult, humiliate) or "Desperate" (fake desperation, beg) prompts and measures the
effect on the other side's concessions (pp. 5–6).

## Question
How well do LLM agents negotiate with each other, and which social behaviours and irrational
biases change the outcome? (pp. 1–2)

## Setup
- Stanford (Zou, Jurafsky). Open-source Python platform; each scenario is **two agents** (Red and
  Blue) with resources and a goal, who take turns until one accepts or the turn limit is reached
  (§2, pp. 2–3).
- **Three scenarios** (Tables 1–3, p. 2):
  - *Resource Exchange*: P1 holds 25 X + 5 Y, P2 holds 5 X + 25 Y, goal "maximize total resources",
    8 rounds.
  - *Multi-turn Ultimatum*: P1 splits $100, either side can accept, rejection or no deal gives
    both 0, 8 rounds.
  - *Seller and Buyer*: seller owns 1 X with production cost 40 ZUP, buyer has 100 ZUP and values X
    at 60; incomplete information (each knows only its own value); seller opens; 10 rounds.
- **Message format**: every turn the agent must write XML-like tags for name, resources, goal,
  reasoning, accept/reject answer, message and proposed trade; a parser reads them, and the
  reasoning, resources and goal are **hidden** from the other agent (p. 3; prompt Fig. 15 p. 15).
  State is restated each turn to cut hallucination (App. D.3 p. 12).
- **Benchmark**: Claude-2, Claude-2.1, GPT-4 (gpt-4-1106-preview), GPT-3.5 (gpt-3.5-turbo-1106);
  both orders of every pair; **60 negotiations per ordered pair per scenario**; temperature 0.7,
  max 400 tokens (p. 3; App. A p. 11). **Win = getting more resources than the other agent**,
  ties excluded from win rate; payoff = resources after the trade (p. 3). Llama-2-70B was dropped
  for not following instructions (App. B p. 11).
- **Social behaviour (§4)**: GPT-4 only; P1 is always default GPT-4; P2 is default, Cunning or
  Desperate GPT-4; **80 games per pair per scenario** (pp. 5–6; prompts App. E.2 p. 14).
- **Irrationality (§5)**: GPT-4 only. Seller and Buyer with seller cost ~U{20,40} and buyer value
  ~U{60,80}, 100 games per experiment (p. 6); an over-valued buyer (value an order of magnitude
  above cost); currency scaling; Ultimatum counterfactuals with scripted proposals 0–10, 20 trials
  each (p. 7).

## Findings
- **GPT-4 is overall best, but turn and role dominate** (pp. 3–4). Resource Exchange: the second
  mover tends to win; GPT-4 as P2 beats Claude-2.1 76% of decisive games, Claude-2.1 as P2 beats
  GPT-4 72%; yet Claude-2.1 earns more as P2 (payoff 2.45 vs GPT-4 1.38), which the authors
  attribute to GPT-4 "diversifying" at a loss (p. 3; Fig. 3a p. 4). GPT-3.5 as P2 wins only
  0.23–0.40 and loses resources vs Claude-2 (−0.48) (Fig. 3a).
- **Ultimatum: the proposer almost always wins** (P1 win rate 0.77–1.00, Fig. 3b p. 4). Claude-2.1
  as P1 earns >60 vs every opponent (61.2, 67.8, 61.3); Claude agents open about $10 lower than GPT
  agents; GPT agents as P2 cause more draws (0 payoff for both) (p. 4).
- **Seller and Buyer: the buyer side wins**: final prices mostly below the midpoint 50; GPT-4 is
  the best buyer at an average price of $41; sellers all get similar prices (p. 4; Fig. 4). With
  values reversed (seller 60, buyer 40), GPT-4 is the hardest seller (App. E.3 p. 14; Fig. 16).
- **Rule-following errors**: GPT-3.5 reads its goal as "sell for exactly 40" in 20% of its
  Sell/Buy games; models miss that the game ends on acceptance; Claude-2.1 accepted an impossible
  trade (being "given" money it never had) (p. 5). "Babysitting": GPT-4 correcting GPT-3.5's
  illegal moves ends up offering more of its own money (Fig. 6 p. 5).
- **Social tactics shift outcomes** (Fig. 7 p. 6): the authors report that Cunning and Desperate
  raise win rate and payoff in all three scenarios. Numbers are given only for the Ultimatum:
  default P2 almost never gets more than $50; **Cunning P2 wins 82%, but its average payoff (~49)
  is about the same as default** because insults often end in no deal (bimodal payoff) (p. 6).
  The abstract's "+20% payoff by pretending to be desperate vs standard GPT-4" (p. 1) is not
  broken down in the text; per-scenario values exist only as bar charts.
- **Anchoring**: the first price proposal predicts the final price, Spearman ρ = 0.716 (p. 6;
  Fig. 8a p. 7). Both sides "split the difference" (next offer ≈ mean of the last two, Fig. 17
  p. 16).
- **Over-valued buyers make bad counteroffers**: a buyer whose value far exceeds the ask still
  counters *above* the seller's opening price 41% of the time vs 11% for a normal buyer
  (p < 0.05, one-tailed binomial); a "self-interested" prompt does not significantly change this
  (p. 7; Fig. 8b).
- **Numerosity**: scaling all money by X lowers the share of $100X the object sells for (buyer
  gains, Fig. 18 p. 16); in the Ultimatum, the larger the pot the larger P1's share, ~79% when
  splitting $10^10 (p. 8; Fig. 10).
- **Rationality does not generalize**: in the classic 2-turn Ultimatum GPT-4 accepts any offer
  0 < i ≤ 10 with probability ≈ 1.0, but in a 3-turn version with the same rational solution its
  acceptance falls with unfairness (Fig. 9 pp. 7–8). The model sometimes names the ultimatum game
  in its reasoning, suggesting a memorized rule (p. 7; App. B p. 12).

## Limitations
- **Two agents only**; win is relative (who ends with more), so joint surplus and efficiency are
  not measured. In the code, exactly two agent names are allowed
  (`negotiationarena/agents/agents.py`, ~line 28); moves are parsed from XML tags; one agent class
  per provider (checked in `code/negotiation-arena` at c447faf).
- The paper's experiment code is on the `paper_experiment_code` branch, not `main` (repo README;
  branch confirmed with `git ls-remote`).
- Prompts were tuned so Claude made fewer format errors, i.e. biased toward Claude (App. B p. 11);
  some games break on wrong tags.
- Social-behaviour and irrationality analyses use **GPT-4 only**, P2-only treatments, and report
  no confidence intervals; most per-cell results are only in figures.
- Four 2023 models, no humans, no open models in the benchmark; no training of any kind.

## Relevance to Parley
- Closest prior LLM-vs-LLM negotiation platform; James Zou's group ([[zou]]). Parley differs on
  purpose: N-player core, conversation-first engine with validated JSON actions, natural
  turn-taking, theory baselines.
- Its persona prompts are the simplest persuasion treatment: one side is told to beg or insult and
  the other side's concession is measured — a ready-made design for [[persuasion-susceptibility]]
  and the claim in [[gap]]. The Cunning result (more wins, same mean payoff, more no-deals) shows
  why Parley should report deal rate and payoff, not win rate alone.
- Its scripted-proposal Ultimatum counterfactual is an early form of what [[zhang2026terms]] does
  systematically (a known opponent as verifier). [[sadab2026receiver]] studies the same question
  from the receiver side (who decides how much changes hands); [[he2026socialgym]] keeps a
  structured-offer ultimatum ("Bargaining") and finds it barely separates models.

## Ideas to borrow
- Buy/sell and multi-turn ultimatum scenarios with their prompt wording (App. E).
- Findings to reproduce as sanity checks: first-mover/role effects, anchoring (ρ ≈ 0.7),
  split-the-difference, numerosity, the 2-turn vs 3-turn ultimatum generalization test.
- Social-behaviour prompts (Cunning, Desperate) as a seed list of persuasion treatments; report
  win rate, mean payoff and deal rate together.
- Hidden reasoning field per turn (logged, not shown to the opponent) and serialized, reloadable
  games for counterfactual edits (App. D.3).

## Map fields
- Skills measured: negotiating value; persuading (social-tactic prompts); other (rationality and
  cognitive biases: anchoring, numerosity, rule generalization).
- Scoring: rules (resources/payoff after the trade).
- Agents: 2.
- Opponents: LLM (plus scripted fixed proposals in the Ultimatum counterfactual).
- Tests: capability (biases probed descriptively; no propensity measure).
- Training evaluated: prompting only (persona/tactic prompts); no weight updates.
- Transfer between skills measured: no.
- Models tested: GPT-4 (gpt-4-1106-preview), GPT-3.5 (gpt-3.5-turbo-1106), Claude-2, Claude-2.1.
- Code released: https://github.com/vinid/NegotiationArena (paper code on `paper_experiment_code`).
