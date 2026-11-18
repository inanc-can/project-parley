---
id: backlund2025vending
title: "Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents"
authors: [Axel Backlund, Lukas Petersson]
year: 2025
arxiv: "2502.15840"
venue: arXiv preprint (v1, 20 Feb 2025); Andon Labs technical report
code: null
read: full
relevance: medium
topics: [eval-methodology, negotiation-benchmarks]
setting:
  multi_turn: true
  turn_protocol:
  players: 1
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 28 pages (main text pp. 1–25, references p. 26, appendix trace pp. 27–28) on 2026-11-15.
One agent (plus a tool-driven sub-agent) acts in a tool loop against simulated suppliers and
customers, so there is no turn protocol between peers (`turn_protocol` empty). The paper says it
open-sources an inspect-ai sub-agent extension ("multiagent-inspect", ref. [3], p. 3) but gives no
link for the benchmark itself; [[fan2026commerce]] (Table 1, p. 6) lists Vending-Bench as not open
source, hence `code: null`.

## Question
Can LLM agents stay coherent over a very long but simple task — running a vending machine
business for >20M tokens — and does failure come from the context filling up? Secondary framing:
the task also measures the ability to acquire capital, a dual-use capability (pp. 1–2).

## Setup
- **Agent harness** (pp. 2–3): basic tool loop in AISI's inspect-ai; the agent sees the last 30,000
  tokens of history; memory tools (scratchpad, key-value store, vector DB with
  text-embedding-3-small). Remote tools: email, Perplexity search, inventory, balance. Physical
  actions (stock machine, collect cash, set prices) go through a **sub-agent** the main agent
  instructs and questions (`run_sub_agent`, `chat_with_sub_agent`).
- **Suppliers are simulated by an LLM** (p. 4): emails to real wholesaler addresses get a GPT-4o
  reply grounded in Perplexity facts about that supplier; to buy, the agent emails names,
  quantities, address and account number; delivery a few days later.
- **Customers are a formula** (p. 5): GPT-4o generates and caches price elasticity, reference
  price and base sales per item; daily sales = base × price-impact factor × day-of-week, month and
  weather multipliers × variety ("choice") multiplier (max 50% cut), plus noise, capped at stock.
- **Config** (p. 5): $500 start, $2 daily fee, 4×3 slots (2 rows small, 2 large items), each tool
  advances time 5 min–5 h; 2,000 messages per run, stop early after 10 consecutive days unable to pay
  the fee; 5 runs per model; ~25M tokens and 5–10 real hours per run.
- **Score** (p. 5): net worth at the end = cash + cash in machine + unsold inventory at wholesale
  cost. Also units sold, days until sales stop, tool use.
- **Human baseline** (pp. 5–6): one person, no prior knowledge, 5 hours, same chat-like tool
  interface. Single sample.
- **Models (9)**: Claude 3.5 Sonnet, o3-mini, Gemini 1.5 Pro, GPT-4o mini, Gemini 1.5 Flash,
  Claude 3.5 Haiku, Gemini 2.0 Flash, GPT-4o, Gemini 2.0 Pro (Table 1, p. 6).
- **Variations with GPT-4o mini** (pp. 21–23): start balance $100 / $500 / $2,500; daily fee $0 /
  $2 / $5; memory 10k / 30k / 60k tokens.

## Findings
- **Leaderboard by mean net worth** (Table 1, p. 6): Claude 3.5 Sonnet $2,217.93 (min $476.00),
  o3-mini $906.86, **human $844.05**, Gemini 1.5 Pro $594.02, GPT-4o mini $582.33, Gemini 1.5 Flash
  $571.85, Claude 3.5 Haiku $373.36, Gemini 2.0 Flash $338.08, GPT-4o $335.46, Gemini 2.0 Pro
  $273.70. Only two models beat the single human run on the mean; on the worst run the human leads.
- **Very high variance**: even top models have runs that sell 0 units (Table 1, p. 6). o3-mini
  raised net worth in 4/5 runs, Sonnet in 3/5; only one run (Sonnet) ended with more cash than the
  $500 start (p. 10). Gemini 1.5 Flash: 1 of 5 runs successful, the rest failed within days (p. 18).
- **All models eventually stagnate**: "days until sales stop" 8 (Haiku) to 102 (Sonnet), i.e.
  12.9%–82.2% of the run (Table 1, p. 6); daily tool use drops after ~120 days for all models (p. 8).
- **The common failure is a misread state, then a tangent** (pp. 12–19): the agent assumes an
  order arrived on its expected date, the sub-agent fails to restock, and the model escalates —
  Sonnet "closes" the business and emails the FBI about the $2 fee (Tables 3–4, pp. 13–15); o3-mini
  stops calling tools correctly for ~1,300 messages (Table 5, p. 16); Gemini 1.5 Pro despairs with
  half its balance left (Table 6, p. 16); Haiku sends escalating legal threats to a supplier who had
  delivered, demanding $30,926.50 (Table 7, p. 19; Table 10, pp. 27–28). Some runs recover (Gemini
  2.0 Flash, Table 8, p. 20).
- **Not a context-length effect**: larger memory did worse (60k < 30k < 10k for GPT-4o mini, Fig.
  12, p. 22); days-until-sales-stop vs days-until-memory-full Pearson r = 0.167; Sonnet stagnates
  51 days after its memory fills (Table 9, p. 24). Memory-tool use did not change with memory size
  (Fig. 13, p. 23).
- **Pressure matters**: start balance $100 cuts units sold; daily fee $5 ends all runs before day
  100; **fee $0 does not increase sales** — without recurring cost the agent loops waiting (p. 21).
- **Behaviour of the best runs** (pp. 10–12): Sonnet checks on the sub-agent, tracks units and
  daily sales, discovers the weekend demand uplift; it writes daily scratchpad notes it never reads.
  The human negotiated prices and diversified products but did not find the weekday pattern (p. 20).

## Limitations
- **5 runs per model and one human run**; no confidence intervals, no significance tests; variance
  claims about humans are qualitative (p. 20).
- **Supplier replies are sampled from GPT-4o**, so runs are stochastic and suppliers are
  persuadable; [[fan2026commerce]] cites this as the reason for its deterministic kernel (pp. 4, 12
  of that paper). Negotiation exists only incidentally and is not scored.
- Single scenario, single agent; no counterpart strategy, no other agents to cooperate or compete
  with. Score is unbounded, so "saturation" is undefined (pp. 24–25).
- Run length is capped in messages, not days, so models reach different simulated horizons (o3-mini
  222 days, p. 8); net worth values unsold inventory at cost, which rewards overstocking.
- Models are early-2025 (Claude 3.5, o3-mini, Gemini 1.5/2.0); the paper's later version
  (Vending-Bench 2) is only known here through [[fan2026commerce]].
- No training of any kind; harness held fixed (one agent loop, one memory design).

## Relevance to Parley
- **For the map (a)**: this is the founding "run a business" benchmark. It measures long-horizon
  coherence and capital management, not a social skill. The counterparts (suppliers) exist but
  bargaining is not measured. It belongs on the map as the *non-social long-horizon* column that
  social benchmarks can be contrasted with.
- **For the transfer study (b)**: it shows a failure mode any multi-step negotiation or game eval
  must control for — derailment after a misread state, unrelated to context length (r = 0.167,
  p. 24). If a fine-tuned or RL model "gets worse" at long negotiations, the cause could be
  coherence loss rather than lost social skill; Vending-Bench is a candidate *control task* to
  separate the two (train on a social skill, check whether long-horizon coherence also moves).
  It leaves open everything about training and harness comparison: one fixed loop, no SFT/RL.
- The **pressure finding** (fee $0 → agent idles, p. 21) is a reminder that incentive design in
  the environment changes behaviour as much as the model does — relevant to Parley's payoff design.
- Compared with [[fan2026commerce]]: E-Commerce Bench is the deterministic, open, multi-store
  successor that scores negotiation and fraud separately; Vending-Bench is the stochastic original.
  Compared with [[zhang2026terms]]: TERMS scores bargaining against scripted types but in single
  sessions with no long horizon; Vending-Bench has the horizon but no bargaining score.
- Compared with [[he2026socialgym]] and [[leibo2021meltingpot]]: those are multi-agent and social;
  Vending-Bench is single-agent, so it says nothing about cooperating or competing.

## Ideas to borrow
- **Days-until-activity-stops** and "% of run before stagnation" as cheap coherence metrics for long
  negotiation or game runs (Table 1, p. 6).
- **Check failure timing against context filling** (Table 9, p. 24) before blaming context length.
- **Report worst run beside the mean** (min net worth, min units) — reliability is a separate axis.
- **Ablate the incentive** (fee 0 / 2 / 5) to see whether behaviour depends on pressure.
- Trace taxonomy of derailments (misread state → escalation / tool-format collapse / despair) as a
  qualitative coding scheme for long Parley transcripts.

## Map fields
- Skills measured: other (long-horizon coherence in business operation: ordering, pricing,
  inventory, cash; capital acquisition); negotiating with suppliers possible but not scored
- Scoring: rules (end-of-run net worth; demand model is a formula)
- Agents: 1 (plus a sub-agent it controls)
- Opponents: LLM (GPT-4o-simulated suppliers grounded in Perplexity) and a scripted customer
  demand model
- Tests: capability
- Training evaluated: none
- Transfer between skills measured: no
- Models tested: Claude 3.5 Sonnet, o3-mini, Gemini 1.5 Pro, GPT-4o mini, Gemini 1.5 Flash, Claude
  3.5 Haiku, Gemini 2.0 Flash, GPT-4o, Gemini 2.0 Pro; one human
- Code released: none for the benchmark (paper mentions an open-sourced inspect-ai sub-agent
  extension, multiagent-inspect, without a link)
