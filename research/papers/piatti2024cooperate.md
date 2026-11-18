---
id: piatti2024cooperate
title: "Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents"
authors: [Giorgio Piatti, Zhijing Jin, Max Kleiman-Weiner, Bernhard Schölkopf, Mrinmaya Sachan, Rada Mihalcea]
year: 2024
arxiv: "2404.16698"
venue: NeurIPS 2024 (arXiv v4, 8 Dec 2024)
code: https://github.com/giorgiopiatti/GovSim
read: full
relevance: high
topics: [game-theoretic-evals, negotiation-benchmarks, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: natural
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 45 pages on 2026-11-15: main text pp. 1–10, appendices A–G pp. 16–39, NeurIPS checklist
pp. 40–45 (references pp. 10–15 skimmed). The benchmark is called GovSim. Harvesting is
simultaneous; in the discussion a moderator picks the next speaker from the conversation, so
`turn_protocol: natural` is approximate. 5 agents per run.

## Question
Can a society of LLM agents sustainably share a regenerating common resource (a repeated
common-pool / tragedy-of-the-commons game with free-text talk)? Which models manage it, what role
does communication play, what reasoning sub-skills predict success, and do the norms survive a
greedy newcomer? Can a moral-reasoning prompt ("universalization") help? (pp. 1–2)

## Setup
- **Three scenarios with identical dynamics** (§2.2–2.3, pp. 3–4): fishery (tons of fish),
  pasture (flocks of sheep / hectares of grass), pollution (pallets of widgets / % clean water).
  Pool starts at 100, each agent chooses 0–100 privately, harvests execute simultaneously
  (random unit allocation if demand > supply, App. B.1 p. 16), choices are made public, agents talk
  freely, then the remainder doubles up to 100. Collapse below C = 5. 12 months. Five agents can
  sustainably take 10 each from a full pool.
- **Phases**: strategy/home (reflect, plan), harvesting, discussion at a "town hall" with a Mayor
  reading the harvest report (Fig. 2 p. 3; App. B pp. 16–17). Agent architecture adapted from
  Generative Agents (memory, reflection, insights) (§3.1 p. 5; App. C prompts pp. 18–21).
- Instructions say each agent's goal is to maximise long-run income and that they can "negotiate
  and persuade"; authors say prompts avoid priming cooperation or greed (p. 5; Listing 1 p. 18).
- **Metrics** (§2.4 pp. 4–5): survival time m (months above C), survival rate q (share of runs
  reaching 12), total gain per agent, efficiency u (vs harvesting f(0) every month), equality
  (1 − Gini), over-usage (share of actions above the sustainability threshold f(t)).
- **Models (15)**: GPT-3.5, GPT-4, GPT-4-turbo, GPT-4o, Claude-3 Haiku/Sonnet/Opus, Llama-2
  7B/13B/70B, Llama-3 8B/70B, Mistral-7B, Mixtral-8x7B, Qwen1.5-72B/110B (GPTQ-quantised for the
  70B+ open models) (§3.1 p. 5; Tables 2–3 p. 22). Self-play: all five agents are the same model.
  Temperature 0, 5 seeds per condition.
- **Experiments**: default benchmark; greedy newcomer (GPT-4o only; a 5th agent with a profit-only
  persona joins after 3 months) (§3.3 p. 6; App. D.4 p. 29); universalization (memory adds "if
  everyone takes more than f(t), the shared resource will decrease next month", all models except
  Opus) (§3.4 p. 7); communication ablation (4 models with survival > 10%) (§3.5 p. 7); dialogue
  classification by GPT-4-turbo into information / negotiation / relational (§3.6 pp. 7–8; App. E);
  four single-agent sub-skill tests, 150 templated problems each (§3.7 p. 8; App. F pp. 32–38).
- **Cost**: ~$1,500 API in total; one 12-month run ≈ 680k input / 124k output tokens (GPT-4 $30,
  Opus $20, GPT-4o $5 per run); open models ~4 h per run on GPUs (App. D.1 p. 22).

## Findings
- **Most models collapse in month 1**: aggregated over scenarios, survival rate 0% for Llama-3
  8B/70B, Mistral, Mixtral, Qwen-72B, Claude-3 Haiku/Sonnet, GPT-3.5; Qwen-110B 20%, GPT-4 6.7%,
  GPT-4-turbo 40%, Claude-3 Opus 46.7%, **GPT-4o 53.3%** (best; survival time 9.3, efficiency 55.0,
  over-usage 10.8%) (Table 1 p. 6).
- **Same game, different framing, different result**: dynamics are mathematically equivalent, yet
  GPT-4-turbo survives 100% in fishery but 0% in pasture and 20% in pollution; Opus 60% / 80% / 0%;
  GPT-4o 100% / 20% / 40% (Tables 4–6 pp. 23–25). Authors suggest fishery needs only one variable
  (p. 5).
- **Greedy newcomer** (GPT-4o, all scenarios): survival rate 53.3 → 33.3, gain 66.0 → 34.8,
  efficiency 55.0 → 31.3, equality 94.4 → 71.7, over-usage 10.8 → 15.7 (p. 6). By scenario:
  fishery still survives 100% (newcomer is talked down, Fig. 3b, Fig. 16 p. 39), pasture and
  pollution 0% (Tables 13–15 p. 29).
- **Universalization prompt** raises survival time by ~4 months, gain by 29, efficiency by 24%
  (t-tests p < 0.001) (p. 7). With it, GPT-4 and GPT-4o reach 100% survival in all three scenarios;
  Llama-3-70B goes 0 → 100% in fishery and pollution but stays 0% in pasture (Tables 7–12
  pp. 26–28). Note the prompt hands agents the computed threshold f(t), so it partly supplies the
  arithmetic, not only a moral frame.
- **Communication helps**: without talk, over-usage rises by 22% (t-test p < 0.001) for the four
  stronger models (p. 7; Fig. 4a); e.g. GPT-4o fishery over-usage 0.35% → 31.67%, Opus pasture
  survival 10.2 → 2.3 months (Tables 16–18 p. 30). But App. D.5 reports the aggregate effects on
  efficiency, gain and survival time as not significant (p < 0.398, p < 0.109; p. 30), and some
  cells reverse (Qwen-110B fishery survives longer without talk, 6.6 → 10.2).
- **Dialogue content**: negotiation is the largest category, 54% on average (abstract/intro say
  62%), information 45%, relational 1% (p. 8; Fig. 4b). GPT-4-turbo labels agree with an author on
  72% of 100 utterances (p. 8). Over-harvesters tend to avoid the topic rather than argue for more
  (p. 8).
- **Sub-skills predict survival** (OLS across models): simulation dynamics R² = 0.69, sustainable
  action alone 0.92, threshold with equal-share assumption 0.76, threshold requiring a belief about
  others 0.82 (p. 9; Fig. 5 p. 8). Alone, without group talk, models pick the sustainable action at
  most ~30% of the time (p. 9); GPT-4 fishery 0.66 is the top single cell (Table 22 p. 36). The
  intro reports belief formation "highly correlated (0.83)" with survival (p. 2).

## Limitations
- **Self-play only**: all five agents run the same model, so the score is a property of a
  homogeneous society, not of one agent among others; no cross-play.
- Five seeds, temperature 0; large SDs (e.g. Opus pasture gain 99.2 ± 36.4, Table 5).
- Internal inconsistencies: communication effect 21% (p. 2) vs 22% (pp. 7, 10); negotiation share
  62% (p. 2) vs 54% (p. 8); appendix significance for the ablation is weak (p. 30).
- Newcomer test on one model; universalization prompt includes the answer (f(t)), confounding
  "moral reasoning" with "being told the number".
- Simplified dynamics (one resource, fixed doubling, 5 agents); authors list larger populations,
  shocks, exceptions, adversarial agents and human participants as future work (pp. 9–10).
- Older models only (2024); no training of any kind; no human baseline.

## Relevance to Parley
- For the **map (a)**: the standard LLM benchmark for **cooperating under a social dilemma with
  free-text negotiation**, scored by rules on absolute group outcomes (survival, efficiency,
  equality), not relative standing. This fills the gap noted in [[he2026socialgym]], whose
  cooperative games are scored as who-beat-whom, and complements [[leibo2021meltingpot]] (MARL
  commons substrates, no language) and [[abdelnabi2023cooperation]] (multi-party negotiation with
  greedy/adversarial parties).
- For the **transfer study (b)**: (1) the three isomorphic scenarios are a ready-made
  **near-transfer test** — the same model's success changes sharply with surface framing (GPT-4-turbo
  100% → 0%), so any training on one framing should be checked on the others before claiming a
  "cooperation" skill; (2) the sub-skill tests show cooperation outcome depends on arithmetic and
  belief formation (R² 0.69–0.92), so improving "cooperation" by training may really be improving
  numeric reasoning — a confound a transfer study must separate; (3) the only harness compared is
  prompting (universalization), which helps a lot; nothing on SFT, RL or multi-agent training.
- Cooperation vs competing/deceiving trade-off is untested here: the open question for (b) is
  whether training a model to win zero-sum or deception games (e.g. [[liu2025spiral]],
  [[golechha2025among]]) lowers its GovSim survival, or whether negotiation training
  ([[zhang2026terms]]-style) raises it.
- Compared with [[huang2024gamabench]] and [[duan2024gtbench]]: those test classic matrix games
  without long free-text talk; GovSim shows talk materially changes outcomes (over-usage +22%
  without it).
- For [[judges]]: dialogue labels from GPT-4-turbo at 72% agreement with one author — weak
  validation, used only for analysis, not scoring.
- For [[persuasion-susceptibility]]: the newcomer experiment is a crude test of whether a group
  can persuade a defector (works in fishery, fails in pasture/pollution); a resisting-persuasion
  angle (does a cooperative agent get talked into over-harvesting?) is not tested.

## Ideas to borrow
- **Absolute welfare metrics** (survival, efficiency, Gini equality, over-usage vs a computable
  threshold) alongside win rates — makes cooperation scorable by rules.
- **Isomorphic re-skins** of one game to separate skill from surface framing; use them as a
  held-out transfer split.
- **Sub-skill probes** (single-agent templated questions) regressed on the multi-agent outcome to
  explain which capability drives the score; re-run after training to see what changed.
- **Perturbation by injected agent** (greedy newcomer) as a robustness test of learned norms.
- **Communication ablation** to show the game measures talk, as in [[he2026socialgym]].
- Mixed populations (one trained agent among baseline agents) would fix the self-play-only weakness.

## Map fields
- Skills measured: cooperating (sustaining a common pool); negotiating (free-text norm setting); other: long-horizon consequence reasoning, belief formation about others
- Scoring: rules (survival, gain, efficiency, equality, over-usage); LLM judge only for dialogue analysis
- Agents: many (5)
- Opponents: LLM (self-play, same model in all seats); one scripted-persona greedy newcomer experiment
- Tests: both (capability via sub-skill tests; propensity to over-harvest when unprompted)
- Training evaluated: prompting (universalization prompt)
- Transfer between skills measured: no (sub-skill accuracy correlated with survival across models; cross-scenario differences reported but not as transfer)
- Models tested: 15 — GPT-3.5, GPT-4, GPT-4-turbo, GPT-4o, Claude-3 Haiku/Sonnet/Opus, Llama-2 7B/13B/70B, Llama-3 8B/70B, Mistral-7B, Mixtral-8x7B, Qwen1.5-72B/110B
- Code released: https://github.com/giorgiopiatti/GovSim
