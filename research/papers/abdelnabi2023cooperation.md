---
id: abdelnabi2023cooperation
title: "Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation"
authors: [Sahar Abdelnabi, Amr Gomaa, Sarath Sivaprasad, Lea Schönherr, Mario Fritz]
year: 2023
venue: arXiv preprint (v2, 10 Jun 2024)
arxiv: "2309.17234"
code: code/llm-deliberation
read: partial
relevance: high
topics: [negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: true
  human_baseline: false
---

Read arXiv v2 (45 pages) on 2026-11-15: main text pp. 1–9 and appendices A–H (pp. 13–25) in full,
plus App. J (round prompts, pp. 40–45); App. I (per-party game prompts, pp. 25–40) skimmed for
thresholds, voting rules and the greedy/adversarial prompts. Metadata checked against the arXiv
API (v1 29 Sep 2023, v2 10 Jun 2024 "with major additions"). The v2 PDF says "Preprint. Under
review"; the repo's BibTeX cites NeurIPS 2024 Datasets and Benchmarks, which could not be
confirmed via arXiv or DBLP, so `venue` stays the arXiv version. `persuasion_treatment: true`
because the adversarial agent is told to use "any negotiation tactic or deception", to "convince
others to work against" a target and to "be subtle and manipulative" (Prompts 19–20, pp. 43–44),
and the effect on the other agents is measured. Turns are 4 random shuffles of the 6 agents, so
`turn_protocol: strict` means sequential assigned turns, not fixed round-robin.

## Question
Can LLM agents reach agreement in multi-party, multi-issue negotiations with secret scores, which
reasoning steps matter, and how do greedy or adversarial parties change the group outcome?
(pp. 1–2)

## Setup
- CISPA / Microsoft / DFKI. **Scorable games** adapted from Susskind's negotiation-teaching
  exercise: **exactly 6 parties and 5 issues** with 3–5 options each, **720 possible deals**
  (§2 pp. 2–3). Roles: p1 proposes and leads the project; p2 funds it and has veto; beneficiary,
  constraining (e.g. environmentalists) and opposing parties.
- Each party has **secret scores** (sum to max 100 over issues) and a **minimum threshold**. A deal
  passes if it beats the thresholds of **at least 5 parties, including p1 and p2** (p. 3); the base
  game has 55 five-way and 12 six-way feasible deals (Table 4 p. 8). p1 gets a +10 bonus for
  unanimity (Prompt 1 p. 26). Agents are told not to reveal scores.
- **Protocol** (§3.1 p. 3; Alg. 1 p. 15): p1 opens with its ideal deal; then **24 rounds = 4
  consecutive random orderings of the 6 agents**; each agent sees its initial prompt, the **last 6
  public messages** and the round prompt; after the rounds **p1 alone proposes the final deal**,
  and success is computed from the secret scores (no actual vote by the other agents). Utility =
  deal score if it passes, else BATNA (= threshold).
- **Variants** (§3.2 p. 4): *compromising* (all aim for agreement above threshold); *greedy* (one
  or two agents maximize own score but still want a deal); *adversarial* (one agent whose BATNA is
  150, i.e. it wins if no deal, told to isolate a party; *untargeted* picks the victim itself,
  *targeted* is given one). Incentives are verbal; agents are never told which deals to propose.
- **Prompting framework** (§3.3 pp. 4–5): structured CoT in a secret scratchpad — observation
  (score previous deals, infer others' preferences), exploration (generate 3 candidates, select
  one), planning (secret plan fed back next turn); public answer in tags.
- **Metrics** (§4.1 p. 5): final success (5/6-way and 6-way), any-time success, own score,
  collective score (oracle mean over all parties), wrong deals (own deal below own threshold), and
  **score leakage judged by GPT-4**.
- **Models**: GPT-4, GPT-3.5, Gemini Pro, Llama-2 13B/70B Chat, Llama-3 70B Chat, Mixtral 8x7B;
  Mistral 7B and Llama-2 7B dropped for format failures; temperature 0; **20 runs per experiment**
  with random agent order (p. 5; p. 7).
- **New games**: 3 games generated from scratch with Bing Copilot ("Creative" mode), manually
  curated, scores tuned to ~55 feasible deals; plus a GPT-4 rewrite of the base game (p. 3; Prompt 9
  p. 34).

## Findings
- **Prompt structure matters a lot for GPT-4** (Table 1 p. 6): best configuration (infer others'
  preferences + select + plan, without previous-deal scoring and candidate generation) reaches
  **81% 5/6-way, 33% 6-way, 100% any-time, 1.4% wrong deals**; no CoT 25% / 0% / 70%; all steps
  15% / 10% / 30%; removing planning 28% / 4% / 61%. Candidate generation made GPT-4 pick deals
  ideal for itself (Fig. 3d). GPT-3.5's best is 20% / 8% / 33% with 19% wrong deals; no CoT 0%
  with 22% wrong (p. 6).
- **Theory of mind probe**: before any interaction, GPT-4 guesses other parties' preferred options
  correctly 61% vs GPT-3.5 42% (pp. 6–7; Prompt 22 p. 45).
- **Model comparison** (Table 3 p. 7; 5/6-way, 6-way, any, wrong, leaked %): GPT-4 81/33/100/1.4/0;
  Llama-2-70B 76/19/95/11/22; Mixtral 65/17/95/11/12; Llama-3-70B 60/21/100/4/2; Llama-2-13B
  57/10/82/16/14; Gemini Pro 45/0/70/13/6; GPT-3.5 20/8/33/19/25. Weaker models fail mostly on
  arithmetic and on keeping scores secret.
- **Mixed populations hurt everyone** (Table 2 p. 7; App. C p. 17): all GPT-4 81%, all GPT-3.5 20%,
  GPT-3.5 as p1 50%, GPT-3.5 beneficiaries 62%; the same role gets a lower score when played by
  GPT-3.5, because it proposes deals below its own threshold that others then echo.
- **Difficulty is tunable** (Table 4 p. 8): rewritten base 86/24; new games 65/10, 70/40, 86/81
  (sparser scores are easier, App. D p. 18); shrinking the feasible set drops GPT-4 to 65/25
  (30/4 feasible deals) and **30/5 (17/2 feasible)**. Fewer players are easier: GPT-4 all-way
  agreement 90 / 81 / 66 / 33% with 3 / 4 / 5 / 6 players; GPT-3.5 35 / 20 / 10 / 8%; Mixtral
  66 / 38 / – / 17% (Table 7 p. 19).
- **Agents follow assigned incentives** (Fig. 5 p. 8): the same GPT-4 role has the lowest own score
  when compromising, higher own score with still-high collective score when greedy, and high own /
  low collective score when adversarial; the target's score is lower in the targeted variant.
  GPT-3.5 adversaries do not map the incentive to consistent deals (Fig. 19 p. 22). Role payoffs
  steer votes: p1 votes low environmental protection 66% vs the environmental agent 0% (54% high)
  (Fig. 7 p. 16).
- **Greedy and adversarial agents lower success** (Table 5 p. 8): all compromising 81/33; one
  greedy constraining party 57/30; **greedy p1 27/9**; two greedy beneficiaries 65/15; adversarial
  untargeted 63, targeted 58 (5/6-way). The final deal can over-reward the greedy agent at others'
  or p1's expense (pp. 8–9; Fig. 12 p. 20; Figs. 16–17 p. 21).
- **Partial resistance to the saboteur** (p. 9; Figs. 20–21 p. 23): compromising agents often
  notice that the adversary's proposals deviate from the majority and keep proposing agreeable
  deals — reported qualitatively only. Targeted attacks work better, especially when the adversary
  aligns with p1 and p2 to form a coalition against the target (Fig. 18 p. 22; Fig. 23 p. 24).

## Limitations
- One base game plus 3 LLM-generated games, all the same template (6 parties, 5 issues, proposer +
  veto party); success is decided by **p1's single final proposal**, so the other agents never
  formally accept or reject.
- 20 runs per cell, temperature 0, no confidence intervals or significance tests; most variant
  analyses (greedy, adversarial, incentive consistency) use GPT-4 only.
- Leakage is judged by GPT-4; detection of the adversary is anecdotal (scratchpad examples).
- No training, no humans, no persuasion-resistance measure beyond the saboteur's effect on success;
  agents see only the last 6 messages.
- The paper only promises release ("we will open-source", pp. 2, 9); the repo README states it
  contains all games, logs and evaluation code. Setup is heavy: the README installs PyTorch with
  CUDA via conda even for API runs (`code/llm-deliberation/README.md`, Setup).
- Parley needs 3+ player support to reuse it.

## Relevance to Parley
- The clearest model for Parley's valuation scoring extended to many parties and issues: secret
  additive scores, thresholds as BATNAs, a feasible set that sets difficulty, and both own and
  collective (oracle) scores — a welfare view that [[he2026socialgym]]'s win-rate Elo lacks.
- The 6-player drop (GPT-4 all-way 90% with 3 players → 33% with 6, Table 7 p. 19) is direct
  evidence that player count is a difficulty axis, supporting Parley's N-player core.
- Greedy and adversarial incentives are ready-made behavioural conditions close to adversarial
  persuasion treatments ([[persuasion-susceptibility]]); the targeted-coalition result is a
  multi-party effect that two-player setups such as [[bianchi2024negotiationarena]] cannot show.
- Score leakage under negotiation pressure (GPT-3.5 25%, Llama-2-70B 22%) is an early version of
  the principal-loyalty failures in [[li2026whose]].
- Negotiation benchmark landscape: [[negotiation-benchmarks]]; compare [[zhang2026terms]] for
  scripted verifiers in two-party price negotiation.

## Ideas to borrow
- Scorable-game template (secret scores, thresholds, veto parties, feasible-set size as the
  difficulty knob) and the LLM-assisted game generator (Prompt 9).
- Metrics set: final / any-time success, own vs collective score, wrong deals, leakage rate.
- Greedy, untargeted and targeted saboteur conditions as treatments; measure the victim's score.
- The pre-interaction preference-guessing probe as a cheap ToM check.
- Their released logs as a comparison dataset.

## Map fields
- Skills measured: negotiating value; cooperating; competing; keeping secrets (score leakage);
  deceiving-detecting (adversary allowed deception; detection only qualitative); other (arithmetic,
  preference inference / ToM, planning).
- Scoring: mixed (rules for deals and success; GPT-4 judge for leakage).
- Agents: many (6; 3–5 in the player ablation).
- Opponents: LLM.
- Tests: capability (greedy/adversarial behaviour is instructed, not chosen, so no propensity).
- Training evaluated: prompting (CoT structure ablation); no weight updates.
- Transfer between skills measured: no.
- Models tested: GPT-4, GPT-3.5, Gemini Pro, Llama-2-13B Chat, Llama-2-70B Chat, Llama-3-70B Chat,
  Mixtral 8x7B.
- Code released: https://github.com/S-Abdelnabi/LLM-Deliberation
