---
id: bichler2026model
title: "How language model agents reshape price competition"
authors: [Martin Bichler, Philip Hierhager, Kassian Köck, Fabian Pieroth]
year: 2026
arxiv: "2610.21711"
venue: arXiv preprint (v1, 15 Oct 2026)
code: promised on publication
read: partial
relevance: medium
topics: [game-theoretic-evals]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read: main paper and Methods in full (pp. 1–33). Supplementary Notes 1–10 (pp. 34–87) unread.
TUM DSS chair; Kassian Köck co-writes the thesis proposal ([[gap]]).

## Question
In repeated Bertrand price competition, where standard learning algorithms converge to the
competitive (Nash) price, do LLM pricing agents select different price regimes, and what in their
deployment decides it? (pp. 1–6)

## Setup
- Homogeneous winner-takes-all Bertrand market (c = 0.10, ceiling 0.36, 21-price grid, T = 2,000)
  and a differentiated logit market (pp. 24–25).
- Standard learners as baselines and opponents: Exp3, BM-RM, UCB, PPO, FTRL, full-information
  regret matching, weighted fictitious play, coin betting; round robin for 10⁷ periods, 10 seeds
  (pp. 6–8, 28).
- LLM **deployments** D = (history, action space, output, interval, memory, prompt), coded
  output–history–interval: P-R-1 (point price every period from raw 100-period history incl. rival
  prices; Fish et al. reimplementation), P-S-1, D-S-1, D-S-25, D-S-50 (distribution over the grid
  from summarized history every 25/50 periods). Mostly Gemini 3 Flash at temperature 0.7; GPT-5.6
  Terra in a robustness block (pp. 27–28, Table 1).
- Protocol ablations from the P-R-1 control (5 runs per row); heterogeneous LLM markets as single
  300-period runs (pp. 15–19).
- DBBS ("downward-biased belief search"): a fitted surrogate of D-S-25's distribution updates,
  validated held-out (pp. 12–13, 31–32).

## Findings
- Standard learners mostly reach the competitive region (price index ≈ 0.05–0.10); UCB self-play
  the exception (0.93). Bandit learners need 10⁵–10⁷ periods; full-information learners ~10⁴
  (Fig. 1, pp. 7–8).
- **LLMs earn private advantages against standard learners**: D-S-25 takes 71–72% of industry
  profit vs Exp3/BM-RM/PPO/UCB over 2,000 periods, by undercutting (prices lower in 57–60% of late
  periods), not by keeping prices high (Fig. 2, p. 9). Against full-information learners the edge
  disappears (coin betting earns 71% against P-R-1) (p. 11).
- **Deployment selects the regime**: P-R-1 self-play holds high prices (index 0.88) even in the
  homogeneous market; D-S-25/D-S-50 self-play go to ~0.05 (Fig. 4a, p. 16).
- Ablations: changing only the output (point vs distribution) keeps prices high (0.97–1.05);
  hiding the rival price (0.56) or summarizing history (0.53) roughly halves them; both together
  0.31; full D-S-50 bundle 0.13 (Fig. 4b–c, p. 16). **What the LLM observes matters more than how
  it acts.**
- Decision traces: opponent-facing motifs (anchoring, avoiding price wars) in 94% of P-R-1 traces
  vs 34% of D-S-25; payoff-region motifs in 98% of D-S-25 vs 21% of P-R-1 (p. 11).
- **Anchor-and-harvest**: in mixed markets one agent holds a high anchor while another prices just
  below and takes most profit (e.g. D-S-1 66–71%) (Figs. 5–6, pp. 17–19). Welfare: consumers keep
  95% of surplus under D-S self-play but 15% under P-R-1 self-play (p. 23).
- Policy: auditing LLM pricing needs system-level tests across deployments, not prompt checks
  (pp. 23–24).

## Limitations
- Stylized Bertrand markets; mixed-deployment results are single runs (representative paths, not
  effects) (pp. 17, 24).
- Mostly one model (Gemini 3 Flash); decision traces are behavioural artefacts, not cognition.
- No equilibrium certification of the dynamic regimes; DBBS explains D-S-25 but not P-R-1 (p. 22).

## Relevance to Parley
- **Not about negotiation or persuasion**, but it is the chair's current framing of LLM agents:
  learning in games, deployment-induced learning rules, regime selection, welfare and regulation.
  A thesis proposal for this chair should speak this language (incentives, equilibria vs dynamics,
  welfare, auditing).
- Directly transferable lesson for [[gap]]: **the interface (what the agent observes, how history
  is shown) can matter more than the model**. In a persuasion study, "deployment" variables (does
  the agent see the principal's limit, a summary vs raw transcript, private notes) are natural
  defence treatments.
- Method fit: standard learners as baselines, held-out seeds, bootstrap over seeds, surrogate
  models of LLM behaviour.

## Ideas to borrow
- Name deployments with a compact code and ablate one component at a time.
- Use non-LLM learners as a benchmark class next to LLMs.
- Fit a small surrogate policy to LLM behaviour and validate it held-out (teacher-forced and
  free-running).
- Report welfare split (consumer vs producer), not only prices.
