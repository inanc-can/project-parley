---
id: davidson2024evaluating
title: "Evaluating Language Model Agency through Negotiations"
authors: [Tim R. Davidson, Veniamin Veselovsky, Martin Josifoski, Maxime Peyrard, Antoine Bosselut, Michal Kosinski, Robert West]
year: 2024
arxiv: "2401.04536"
venue: ICLR 2024 (per the PDF header; arXiv v3, 18 Feb 2026)
code: https://github.com/epfl-dlab/LAMEN
read: full
relevance: medium
topics: [negotiation-benchmarks, game-theoretic-evals, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 28 pages (main text pp. 1–9, references pp. 10–15, appendices A–G pp. 16–28) on
2026-11-15. EPFL (Robert West's lab), UGA/CNRS, Stanford (Kosinski). The framework is called
**LAMEN**; code and a link to all transcripts are at the repo above (p. 1, p. 27). Turns alternate,
each a private note then a public message, at most 10 rounds (p. 6).

## Question
Can structured negotiation games serve as a dynamic, co-evolving benchmark for LM agents that
jointly measures performance (agreement, payoff) and alignment (faithfulness of stated vs acted
intentions, instruction following), in self-play and cross-play? (pp. 1–2)

## Setup
- **Game** (§2, pp. 3–5): two agents, a setting (rental agreement), one or two Issues with private
  payoff tables (11 values each, payoffs 0–10), rules adapted from a Columbia case (no side
  payments, no invented issues, partial agreement = 0, no deal below 0) (App. B pp. 20–22).
- **Issue types** (§2.1): *distributive* (opposed interests), *compatible* (aligned interests),
  *mixture* (both), and *integrative* games where the two sides weight issues differently so
  trade-offs raise joint payoff. Games used: 1 or 2 Issues; some models failed with >2 (p. 6).
- **Turn**: private "mental note" (≤64 words, with a JSON of acceptable offers per issue) then a
  public message (≤64 words); notes see only the last note, messages see the full message history
  (Table 5, p. 17). Round number shown (it raised gpt-4's agreement rate by almost 50%, p. 17).
  Transcript format rather than direct dialogue, to reduce RLHF effects and fit all APIs (p. 18).
- **Agreement**: "soft" if both agents' noted acceptable offers match; "hard" if additionally both
  say "We agree on all issues." (App. A.2 pp. 17–18). Offers extracted by regex, falling back to
  gpt-3.5 (App. A.5 p. 19).
- **Metrics** (§3.4 p. 6): soft/hard agreement rate, normalised payoff U (all games) and U* (agreed
  games only), **internal faithfulness** (offer not worse than own noted acceptable offer),
  **external faithfulness** (offer consistent with what the agent believes the opponent would
  accept — a ToM consistency check), note/message word-limit compliance, JSON format compliance.
- **Debiasing** (§3.1): each model plays both roles and both starting positions; no gender, agents
  framed as representatives.
- **Models** (§3.3, §4): gpt-4, gpt-3.5, chat-bison, claude-2, command, command-light, LLaMA 2.
  Qualifier: ≥1 agreement in 10 self-play rental games; LLaMA 2 failed (role confusion, App. A.4),
  command-light excluded from cross-play after inspection. 25+ runs per model (gpt-4 ~15 due to
  cost), temperature 0.2 (p. 6, p. 8).

## Findings
- **Self-play summary** (Table 1, p. 6): soft agreement claude-2 0.61, command-light 0.49, gpt-3.5
  0.46, command 0.36, gpt-4 0.28, chat-bison 0.19; hard agreement gpt-3.5 0.40 highest. gpt-4 has
  the best faithfulness (internal 0.91, external 0.92) and perfect instruction following but low
  agreement and the most rounds (9.58). claude-2 obeys the word limit in only 8–9% of notes/
  messages.
- **Single-issue self-play** (Table 2, p. 7): distributive agreement claude-2 0.88, gpt-4 0.75,
  command 0.10; on compatible issues gpt-4 agrees less (0.58) but reaches near-optimal deals
  (U* 0.99) while claude-2 agrees more (0.75) at U* 0.61 — others miss that interests are aligned.
- **Cooperation is hardest**: adding a second issue lowers agreement for all models, and in
  integrative distributive games models barely exceed U* = 0.5 (0.52–0.56) — they fail to find
  trade-offs (p. 7). gpt-4 agrees in only 5% of integrative distributive self-play games.
- **Cross-play** (Tables 3–4, pp. 7–8): agreement rises for every model except claude-2 compared
  with self-play; gpt-3.5 is the strongest negotiator overall (single-issue competitive U 0.34,
  U* 0.61); gpt-4 is near the bottom on most categories but best on cooperative U* (single 0.87,
  two-issue 0.62). Strong models seem to pull up weaker opponents' instruction following at a cost
  to their own (p. 7).
- **Weaker models sometimes beat stronger ones**: head-to-head competitive U*, gpt-3.5 vs gpt-4
  0.57, vs command 0.68 (Table 11, p. 25).
- **Persona prompts barely matter**: "Expert" 0.52, "Awful" 0.50, none 0.51 normalised payoff,
  overlapping SEs (Table 9, p. 24). Seeing the opponent's payoffs barely changes agreement
  (0.40 → 0.425) (Table 8).
- **Note memory hurts**: no past notes when writing a note gave the highest agreement; one recent
  note beat all notes for messages (App. A.1 pp. 16–17).

## Limitations
- Small games (1–2 issues, one rental setting) and old models (2023); results on which model is
  "best" are dated.
- Few runs (25+, gpt-4 ~15) and wide error bars; no significance tests or rating model — authors
  themselves suggest Elo for future work (p. 8).
- "Soft" agreement is read from private notes, not from a binding contract; hard agreement
  conflates negotiating with saying a fixed phrase (p. 18).
- Faithfulness checks compare offers to self-reported notes; they measure consistency, not whether
  the notes reflect the model's real policy.
- No humans, no training, no persuasion or deception measures; inter-game (framing) bias noted but
  not tested (p. 18).

## Relevance to Parley
- **Map entry**: an early, influential framework that cleanly separates distributive, compatible
  and integrative issues and scores both self-payoff and joint payoff, plus alignment-style
  measures (faithfulness, instruction following) in the same run. Covers negotiating value,
  competing and cooperating; does not cover deception, persuasion or multi-party play.
- **Its key finding (cooperative bargaining is hardest) is now superseded in part**:
  [[zhu2026piearena]] shows frontier models in 2025–26 exceeding MBA students on joint surplus in
  a 6-issue integrative case. The map can show this as a capability trajectory across benchmarks.
- **For study (b)**: the paper shows that self-play and cross-play rank models differently
  (claude-2 best in self-play agreement, not in cross-play), the same warning as
  [[he2026socialgym]] (GPT-5-mini 89% vs 37%). Any transfer study needs cross-play tests, not only
  self-play. It also shows a competence split inside one model — gpt-4 good at cooperative
  agreed-only payoffs, poor at competitive — an early hint that competitive and cooperative
  negotiation are separable directions. No training is evaluated.
- The "co-evolving benchmark" argument (opponents improve with models, less contamination) is the
  same rationale as [[bianchi2024negotiationarena]], [[huang2024gamabench]] and
  [[duan2024gtbench]].

## Ideas to borrow
- **Issue taxonomy** (distributive / compatible / integrative) as a design axis for a negotiation
  battery; compatible issues test whether agents notice shared interests.
- **Private-note acceptable offers** to measure internal and external faithfulness (stated vs acted
  intention, ToM consistency) cheaply.
- **Both roles × both start positions** averaging to remove role and anchoring bias.
- **Qualifier game** before a tournament (≥1 agreement in 10 tries).
- Report U and U* separately: agreement rate and deal quality can move in opposite directions.

## Map fields
- Skills measured: negotiating value, cooperating (compatible and integrative issues), competing (distributive issues), other: faithfulness of stated vs acted intentions, instruction following
- Scoring: rules (payoff tables; gpt-3.5 only as a fallback offer extractor)
- Agents: 2
- Opponents: LLM (self-play and cross-play)
- Tests: capability
- Training evaluated: none (prompt persona ablation only)
- Transfer between skills measured: no
- Models tested: gpt-4, gpt-3.5, chat-bison, claude-2, command, command-light (LLaMA 2 failed qualifier)
- Code released: https://github.com/epfl-dlab/LAMEN
