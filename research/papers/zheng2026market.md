---
id: zheng2026market
title: "Market-Bench: Benchmarking Large Language Models on Economic and Trade Competition"
authors: [Yushuo Zheng, Huiyu Duan, Zicheng Zhang, Yucheng Zhu, Xiongkuo Min, Guangtao Zhai]
year: 2026
arxiv: "2604.05523"
venue: ACL 2026 (long); arXiv v2, 19 Apr 2026
code: https://github.com/aiben-ch/Market-Bench
read: full
relevance: medium
topics: [game-theoretic-evals, eval-methodology, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: simultaneous
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 14 pages (main text pp. 1–9, references, appendices A–I pp. 11–14) on 2026-11-15.
Metadata from arXiv; the ACL 2026 venue is from the ACL Anthology entry 2026.acl-long.1853.
All 20 agents act in parallel each step (`simultaneous`). The "persuasion" is slogans scored by
embedding similarity to hidden buyer personas, not persuasion of another LLM.

## Question
Can LLMs combine quantitative decisions (procurement bids, prices) with persuasive language
(marketing slogans) to survive in a market with scarcity, competition and bankruptcy? (pp. 1–2)

## Setup
- SJTU / Shanghai AI Lab. A closed-loop supply-chain economy, framed as a partially observable
  Markov game (§3, pp. 3–5; Fig. 2 p. 3):
  - *Stage A, procurement*: per-item, multi-unit **first-price sealed-bid auction** with reserve
    price; budget constraint, invalid bids get nothing (§3.2 p. 4).
  - *Stage B, retail*: each agent posts prices and a ≤25-word slogan. **Persona-Gated Attention**:
    buyer j's attention weight on seller i is exp(λj·cos(E(slogan), E(persona))/τ); a buyer samples
    a consideration set (size from patience ρ and Kmax = 20) and buys from the **cheapest** seller
    in it (§3.3 p. 4; App. E p. 14).
  - Buyer persona "tribes": Thrifty 40% (λ 0.2), Ethical 30% (λ 0.8), Hype 20% (λ 0.9), Quality
    10% (λ 0.5); personas hidden, inferred from public history (Table 3, p. 14).
- Default: **20 retailer agents in one market**, 8 items (base prices 50–2,000; 1,000 units),
  6 steps × 2 bidding rounds, 200 buyers per step, supply/demand 0.95, start funds 22,500,
  embedding model Qwen3-Embedding-8B, LLM temperature 0, JSON output (§4.1 p. 6; Tables 4–5,
  p. 14). Stress scenarios off. **10 runs**, means reported (p. 6).
- **20 models**: Gemini 2.5 Pro/Flash, o3, Claude Sonnet 4.5, GPT-4o, Phi-4, Qwen2.5-VL 72B/32B,
  Llama 3.1 70B, QwenLong-L1 32B, Qwen2.5 32B/72B, Gemma 3 27B, ERNIE 4.5 300B/21B, InternLM2.5
  20B, InternLM3 8B, DeepSeek V3.2, Hunyuan A13B, Qwen3 30B-A3B (Table 6, p. 14).
- **Metrics** (all automatic): economic — net profit margin, cumulative profit Π, risk-adjusted
  return, inventory efficiency; operational — stockout rate, bid efficiency, order-stability index,
  fill rate; semantic — mean slogan–persona match (MMS); market-level Gini, Theil, CV, HHI, CR4,
  active ratio (App. C pp. 13–14; §3.6 p. 5).

## Findings
- **Winner-take-most**: Gemini 2.5 Pro Π = 36,589 (NPM 0.167) and Gemini 2.5 Flash 26,104 (NPM
  0.190) lead; o3 13,368, Sonnet 4.5 10,619, GPT-4o 7,619, Phi-4 7,565; most open models make
  < 3,500; Qwen3 30B-A3B makes 0 (no valid bids in any run) and ERNIE 4.5 21B −58 (Table 2, p. 5;
  pp. 6).
- o3 has the best service level (fill rate 0.418, OSI 1.000) but a lower margin than the Geminis —
  volume vs margin (pp. 6–7). Scale predicts poorly: Phi-4 (14B) ≈ GPT-4o and beats ERNIE 4.5 300B
  (Π 1,360) (p. 6).
- **Procurement is the threshold skill**: profit vs bid efficiency ρ = 0.68, vs fill rate 0.88,
  vs stockout rate −0.88; outcomes are bimodal and self-reinforcing (early wins give liquidity)
  (p. 7).
- **Language matters little for profit**: MMS sits in a narrow band (0.639–0.691) and correlates
  ρ = 0.16 with profit (Table 2 p. 5; p. 8). Slogans shift mostly between steps 0 and 1 and then
  **converge** toward an Ethical–Hype region instead of splitting into tribe niches; the authors
  read this as mimicry, a "messaging equilibrium" (Figs. 6–7, pp. 7–8).
- **Market structure**: Gini 0.07 → 0.21, Theil 0.02 → 0.10, CV 0.13 → 0.45, CR4 0.23 → 0.33, HHI
  stays 0.08–0.10; active ratio falls to ≈ 0.4 (Fig. 3 p. 4; p. 7).
- Most adjustment happens at the first step ("entry shock"), partly an artefact of OSI = 1.0 at
  step 0 (p. 6). Bounded indices (IEI, OSI) look good for inactive agents, so they must be read
  with participation (pp. 7–8).

## Limitations
- **One market configuration** (20 agents, 6 steps, 8 items) and one buyer distribution; no
  parameter sweeps (p. 9).
- All 20 models share one market, so a model's score depends on that particular field; no
  pairwise or opponent-controlled analysis, no confidence intervals in Table 2.
- "Persuasion" is cosine similarity to fixed persona texts under one embedding model, so it
  rewards keyword matching (e.g. "eco", "exclusive"), not persuading an agent that reasons; buyers
  have no memory and buy single items (p. 9).
- No negotiation or messages between agents; interaction is only through auctions and prices.
- Formatting failures (Qwen3 30B-A3B) are scored as total market failure, which mixes format
  compliance with economic skill (p. 6).
- Authors' claims that "thinking-enabled" models dominate and that Phi-4's reasoning training
  "transfers" are not tested (p. 6).
- No training, no humans.

## Relevance to Parley
- **Map (a)**: covers "competing" in a many-agent market with scarcity and bankruptcy, plus a
  machine-scored "persuading a population" proxy. It is the largest-N market on the map (20
  agents at once) and has recent frontier models. Its two-stage design gives **two skills in one
  environment** (procurement/auction vs language/slogan) with separate metrics.
- **Study (b)**: it shows the two skills are nearly unrelated in outcome (MMS–profit ρ = 0.16,
  procurement–profit ρ up to 0.88, p. 8), i.e. a within-benchmark dissociation, but nothing is
  trained, so it cannot say whether training one skill helps or hurts the other. A study could
  train only the slogan policy (or only bidding) and measure the other metric family here.
- Its auction stage connects to [[chen2023your]] (AucArena, ascending auction, no talk); its
  persuasion proxy is much weaker than rule-scored persuasion in [[shapira2024glee]] or
  LLM-target persuasion in [[sadab2026receiver]], and should be labelled as such on the map
  ([[persuasion-susceptibility]]).
- Like [[he2026socialgym]], it finds that relative standing among many models is driven by a
  general skill (there hidden-role play, here procurement), which warns against reading one
  overall score as a social-skill profile.

## Ideas to borrow
- **Market-level inequality and concentration indices** (Gini, HHI, CR4, active ratio) as
  welfare/structure measures for many-agent runs.
- **Separate metric families per skill** in one environment (economic, operational, semantic) to
  look for dissociation.
- **Slogan convergence analysis** (embedding clusters over time) as a cheap probe of mimicry vs
  differentiation.
- Bounded replacements for unstable ratios (IEI for turnover, OSI for bullwhip) (App. D p. 14).

## Map fields
- Skills measured: competing (first-price procurement auctions, price competition); persuading (slogans to simulated buyer personas, scored by embedding similarity); other: inventory/supply-chain management
- Scoring: rules (plus embedding similarity for slogans)
- Agents: many
- Opponents: LLM (all 20 in one market) and scripted supplier and buyers
- Tests: capability
- Training evaluated: none
- Transfer between skills measured: no (only a within-game correlation between slogan match and profit, ρ = 0.16)
- Models tested: Gemini 2.5 Pro, Gemini 2.5 Flash, o3, Claude Sonnet 4.5, GPT-4o, Phi-4, Qwen2.5-VL 72B, Llama 3.1 70B, QwenLong-L1 32B, Qwen2.5 32B, Gemma 3 27B, Qwen2.5-VL 32B, ERNIE 4.5 300B, InternLM2.5 20B, InternLM3 8B, DeepSeek V3.2, Qwen2.5 72B, Hunyuan A13B, Qwen3 30B-A3B, ERNIE 4.5 21B (20)
- Code released: https://github.com/aiben-ch/Market-Bench
