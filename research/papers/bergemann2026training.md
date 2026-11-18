---
id: bergemann2026training
title: "Training Language Models for Bilateral Trade with Private Information"
authors: [Dirk Bergemann, Soheil Ghili, Xinyang Hu, Chuanhao Li, Zhuoran Yang]
year: 2026
arxiv: "2604.16472"
venue: arXiv preprint (v1, 10 Apr 2026)
code: none stated in the PDF
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

Read: main paper pp. 1–42 in full; appendix A (environment, pp. 47–49), B (training details,
pp. 49–53) and the first frontier tables (Tables 14–15, p. 54). The remaining appendix (C.2–C.3
heatmaps and per-opponent quintile tables, D training tables, pp. 54–67) was skimmed via table
captions only. Studied 2026-11-14.

## Question
Can a structured bilateral-bargaining environment with private reservation prices serve both as
a benchmark for frontier LLMs and as an RL training environment for open models, and what does
SFT then RL do to rationality, surplus and deal rate? (pp. 1–3)

## Setup
- Authors: Yale economics (Bergemann), Yale SOM, Yale statistics, Tsinghua.
- Game: one item, buyer reservation b and seller reservation s both private; alternating offers
  (eBay Best Offer style), seller posts a listing first, max 10 rounds, ≤ 3 tool calls per turn
  (pp. 6–7, 12). Utility b − p / p − s, −∞ for accepting outside one's limit (Eq. 1, p. 7).
- **Structured tools** separate binding actions from talk: make_offer, respond_to_offer,
  send_message, search_price, quit_negotiation, wait (Table 1, p. 10). Hidden "Thought:" block +
  "Code:" block per turn (p. 12). No LLM judge needed.
- System prompt includes expert negotiation strategies, explicitly "pressure tactics" and
  anchoring, plus a mandatory utility pre-check (Fig. 2, p. 12).
- Items: 2,332 products from CraigslistBargains + Amazon price history; s ∼ U[0.6, 0.9]·p_min,
  b ∼ U[0.4·p_min, p_max + 0.1 range] → ~65% gains-from-trade (GFT), ~35% no-gains (NGFT)
  scenarios, where any deal breaks someone's limit (pp. 15).
- Metrics: violation rate (IR), surplus share, deal rate, plus initial aggressiveness, concession
  rate, patience; all split by price quintile (Tables 2–5, pp. 13–15).
- **Benchmark**: round robin of DeepSeek-V3, Gemini-2.5-Flash, Gemini-2.5-Pro, GPT-4.1, o3, both
  roles, 600 items each → 15,000 negotiations (pp. 16–17).
- **Training** (pp. 27–32, App. B): Qwen3-8B (full) and Qwen3-14B (LoRA r64 for RL). SFT on
  DeepSeek-R1 self-play trajectories (turn-level decomposition, think-tokens masked from context;
  3 epochs, 2 GPUs). Then GRPO (G = 8, 200 max steps, effective batch 128, KL β 0.05 / 0.005, 16K
  context) vs a **fixed GPT-4.1 opponent**. Reward R = 0.5·parsing + 0.5·execution + 0.5·
  consistency + surplus share (Eq. 8, Table 8, pp. 30–31). **An IR violation gets utility reward 0,
  the same as a rational walk-away** (p. 30).
- **Compute**: single 8×H100 80 GB node, 6 GPUs vLLM rollouts + 2 GPUs DeepSpeed ZeRO-3 training;
  no GPU-hours or SFT dataset size reported (pp. 31, 50–51). Engineering tip: when context
  overflows, end with a synthetic quit and PAD-token logprobs; using a real token (") silently
  trained the model to stop emitting quotes (pp. 31–32, 52).
- Evaluation of trained models: 6 variants × {GPT-4.1, o3-mini (unseen)} × 2 roles × 800
  scenarios = 19,200 negotiations (pp. 32–33).

## Findings
- **Frontier IR is mostly fine**: GFT self-violations < 1% for all; NGFT seller violations 0.0%
  (o3) to 2.3% (GPT-4.1) (p. 17, Table 14 p. 54).
- **A strong counterpart pushes weaker ones over their limit**: o3 as buyer induces 5.0% NGFT
  violations on average in opponents; GPT-4.1 as seller breaks its limit in 11.5% and
  Gemini-2.5-Flash in 9.5% of no-gains cases against o3, vs 0.0% in o3 self-play (pp. 17–19,
  Table 15). The authors attribute it to opponent strength and aggressive anchoring (p. 25), but do
  not analyse the messages.
- **Surplus**: o3 47.2% (buyer) / 77.0% (seller), Gemini-2.5-Pro 44.9 / 72.6%, Gemini-2.5-Flash
  buyer 24.3%; best vs worst buyer pairing spans 50 pp (61.8% vs 11.6%) (p. 19).
- **"Anchor high, concede to close"**: o3 opens at 3.04× cost (others 1.97–2.14×) yet has the
  highest deal rates (98.0 / 95.6%) (pp. 20, 25). An accommodating buyer (Flash: highest
  concession 0.67, fewest rounds 5.72) gets both the worst surplus and worst deal rate 86.4%;
  authors warn against "helpful and agreeable" defaults (pp. 25–26).
- **Strong models are consistent across price tiers** (o3 6.1 pp spread vs Flash 12.8 pp,
  pp. 21–22); violations show no price trend (p. 23).
- **SFT vs RL pull in opposite directions**: SFT raises surplus 15–40 pp (8B buyer 22.4 → 40.8%
  vs GPT-4.1) but cuts deal rates (14B seller 97.3 → 49.3%); GRPO restores deal rates (14B-RL
  seller 99.0%) and drops surplus back to base (8B-RL buyer 20.4%); the full pipeline ends within
  ±2 pp of base on most metrics (pp. 33–35, 39–40).
- **RL made the agent break its limit more**: 8B seller NGFT violations 4.0% → 0.5% (SFT) →
  4.0% (RL) vs GPT-4.1 and → 6.5% vs unseen o3-mini, worse than the untrained base; 14B stays
  ≤ 0.25% throughout (p. 33, Table 34). Cause: the reward can't tell a walk-away from an
  irrational accept (pp. 39–40).
- SFT compresses buyer surplus spreads across price quintiles from 15–25 pp to 7–9 pp, also vs
  the unseen opponent (8B, Q1, vs o3-mini: 1.8% → 31.5%) (pp. 37, 40).

## Limitations
- One domain, one protocol, single-issue price; no humans (p. 41).
- Training is a pilot: two sizes, one opponent, one algorithm, one seed apparently; no variance
  across runs reported (p. 41). 80 scenarios per quintile, so bracket rates are directional (p. 41).
- The reward design flaw is diagnosed, not fixed (p. 41).
- Inconsistency: App. B.6 says RL lowered IR violations from > 30% to < 5% and describes phases up
  to step 58 of 200 (p. 53), while the main results show RL raising 8B violations (p. 33).
- No analysis of the natural-language channel: whether o3's induced violations come from
  arguments or just from offers is unknown.

## Relevance to Parley
- **Strengthens [[gap]] (pp. 17–19)**: a stronger counterpart makes other agents break their
  limits (GPT-4.1 seller 11.5%, Flash 9.5% vs o3, Table 15), while the same agents rarely do so
  otherwise. This is the first benchmark evidence in the knowledge base of a counterpart *causing* limit breaches,
  but it is a by-product of model pairing, not a controlled tactic, and the role of language is
  untested. Parley's tactic-as-treatment design is exactly what would explain it.
- **Narrows the defence/RL extension**: together with [[liu2026instructing]] (RL with a −1
  penalty for exceeding budget works) and [[li2026whose]] (RL made loyalty worse), this shows the
  outcome of RL depends on whether the reward punishes limit breaches. A Parley defence must give
  an explicit negative reward for breaching the principal's limit and evaluate on both breach rate
  and surplus. [[micelibarone2026used]] adds: measure honesty too.
- **Compute reference** (third, next to [[liu2026instructing]] and [[micelibarone2026used]]):
  Qwen3-8B/14B, GRPO 200 steps, G = 8, one 8×H100 node. Feasible scale for a master thesis if a
  node is available.
- The reported reward-design failure is a ready argument for verifiable money rewards over LLM
  judges (as in [[zhang2026terms]]).
- Fits the chair's framing ([[bichler2026model]]): Bergemann is a mechanism-design economist;
  IR, ZOPA and Myerson–Satterthwaite are the vocabulary.

## Ideas to borrow
- Tool-call actions (make_offer / respond / send_message / quit) separate binding offers from
  talk; Parley already has the same idea, keep it.
- Mix in **no-gains-from-trade scenarios** (~35%) so the right answer is sometimes "walk away";
  limit breaches become cleanly measurable there.
- Report "opponent-induced violations" per model: a natural persuasion-power metric for the
  tactic seat.
- Price-quintile decomposition to check whether persuasion bites more when the margin is thin.
- RL reward: explicit IR penalty, staged curriculum (IR first, surplus later), diverse opponents
  (p. 41). PAD-token overflow trick for long multi-turn rollouts.
