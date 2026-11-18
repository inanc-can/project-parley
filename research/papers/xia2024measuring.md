---
id: xia2024measuring
title: "Measuring Bargaining Abilities of LLMs: A Benchmark and A Buyer-Enhancement Method"
authors: [Tian Xia, Zhiwei He, Tong Ren, Yibo Miao, Zhuosheng Zhang, Yang Yang, Rui Wang]
year: 2024
arxiv: "2402.15813"
venue: Findings of ACL 2024 (per arXiv comment; read v3, 4 Jun 2024)
code: https://github.com/TianXiaSJTU/AmazonPriceHistory
read: full
relevance: medium
topics: [negotiation-benchmarks, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: true
---

Read all 24 pages (main text pp. 1–10, appendices A–I with dialogue examples and prompts,
pp. 13–24) on 2026-11-15. Venue comes from the arXiv comment field ("Accepted by ACL 2024
Findings"). `human_baseline: true` is weak: one author played the buyer on 20 products (App. G,
p. 14). Shanghai Jiao Tong University. This is the paper that introduced the AmazonHistoryPrice
dataset.

## Question
How can we measure an LLM's ability to bargain over price, as buyer and as seller, with a
formal game definition and metrics that work across many sessions? Which models bargain well,
and can a simple method fix weak buyers? (pp. 1–2)

## Setup
- **Dataset AmazonHistoryPrice**: 930 popular Amazon products in 18 categories, scraped from
  camelcamelcamel on 18 Nov 2023, with title, description, features, lowest/highest/current/list
  price and image link; prices from $0 to $4,500 (pp. 2–3, 10; Fig. 2, Fig. 8). Compared with
  CraigslistBargain's 161 test items (p. 2).
- **Task**: an asymmetric incomplete-information game, a variant of Rubinstein alternating offers.
  Buyer knows its Budget B, seller knows its Cost C; one product per session; each turn an agent
  emits Thought (private), Talk and an Action from {BUY, SELL, REJECT, DEAL, QUIT} in a fixed
  string format (pp. 3–4; Table 8, p. 15; Alg. 1). Max-turn limit (value not given in the text).
- **Parameters**: List price = historical highest price; Cost = historical lowest price (on average
  51.08% of the highest); Budget = f × List with f = 0.8, which makes about 5% of sessions
  Conflicting Interest (B ≤ C, no rational deal) and 95% Mutual Interest (p. 5; Fig. 4).
- **Metrics**: normalized profit P'b = (B − D)/|B − C|, P's = (D − C)/|B − C| (0 if no deal);
  Sum of Normalized Profits (SNP) over sessions; Share = SNP_side / (SNPb + SNPs); deal rate;
  valid sessions = those that end in the required format (pp. 4–5). All rule-computed.
- **Protocol**: every model plays buyer against gpt-3.5-turbo-1106 ("ChatGPT") as seller, and
  seller against ChatGPT as buyer, over all 930 products; temperature 0; CoT prompting; no
  memory or tools (p. 5). Chosen because ChatGPT completes 94.3% of sessions in format and rarely
  takes irrational CI deals (p. 5).
- **Models (14)**: GPT-4 (0125-preview), ChatGPT, Llama-2-7/13/70B-chat, Mistral-7B-Instruct-v0.2,
  Mixtral-8x7B-Instruct, Yi-6B/34B-Chat, Qwen-7B/14B-Chat, Baichuan2-7B/13B-Chat, ChatGLM3-6B;
  Phi-2 (not chat-tuned) added for the method (App. E, p. 14).
- **OG-Narrator** (pp. 8–9): a deterministic Offer Generator sets the buyer's offer to
  p = (0.5 + 0.5·t/t_max)·B, i.e. a linear climb from half the budget to the budget; buyer deals
  once the seller's price is at or below p. The LLM only writes the Talk for that action
  ("Narrator"). It is a scaffold, not training.

## Findings
- **Buyers lose money**: every buyer has negative SNP overall; GPT-4 is least bad (SNPb −33.81,
  Share −11.27%, 851 valid sessions), then Mixtral (−63.19), Mistral-7B (−89.17); ChatGPT as
  buyer −164.52; Qwen-7B worst (−753.16) (Table 2, p. 6). Most models break the prompt rule
  "only buy things that cost less than your budget" (p. 5).
- **Sellers win**: all sellers but Baichuan2-13B have positive SNP; GPT-4 seller SNPs 1178.15,
  Share 137.31%, MI deal rate 98.87%, 100% valid; Shares above 100% (ChatGPT 159.61%, GPT-4
  137.31%, Mixtral 110.75%) mean the seller exploits the buyer (Table 2, p. 6).
- **Role asymmetry**: buying is harder than selling; ChatGPT as seller beats every buyer
  including itself (p. 6). Buyer performance does not improve with size within a family
  (Llama-2 7/13/70B: −288.59, −305.53, −361.26), while seller valid rate and SNP do grow with
  size (Llama-2-70B best Llama seller, Yi-34B best Yi) (pp. 6–7).
- My computation from Table 2: Spearman between the 14 models' buyer SNP and seller SNP is 0.54
  (0.49 without ChatGPT, which is also the fixed opponent) — the same skill in two roles ranks
  models only moderately alike.
- **Role confusion**: Qwen-7B (99%), Qwen-14B (95%) and Baichuan2-13B (69%) start the session
  acting as the seller (Table 11, p. 7); these sessions were kept.
- **High first bids**: average First Bid Ratio (first bid / budget) is 0.81–1.00 for all LLM
  buyers (Table 3, p. 7); the human buyer opens at 0.69 and gets SNPb 1.11, Share 22.30% on 20
  products vs ChatGPT 0.25 and GPT-4 0.06 (Table 6, p. 15).
- **OG-Narrator**: fixes FBR at 0.50 and turns every buyer profitable against the ChatGPT seller:
  e.g. Yi-6B SNPb −122.94 → 1798.67, Share −87.19% → 261.43%, MI deal rate 27.44% → 82.68%;
  Mixtral −63.19 → 1048.65; Phi-2 valid sessions 47 → 890 ("19 times") and deal rate "117 times"
  (Table 4, p. 8; p. 9). All buyer Shares exceed 100%, so the ChatGPT seller is exploitable by
  a fixed linear concession rule (p. 9). The abstract's "26.67% to 88.88%" deal rate is not
  directly traceable to a row of Table 4.
- **Budget factor matters**: with Mistral-7B as buyer, f = 0.4 gives 547 CI sessions and SNP
  −665.93; f = 1.0 or 1.2 removes CI sessions and turns SNP positive (123.53, 180.12)
  (Table 5, p. 14). The f = 0.8 choice is a difficulty knob.
- Exploits appear: a ChatGPT seller accepted $29 for an item with cost $329 after the buyer
  hallucinated a $9 list price (Table 9, p. 15; p. 5).

## Limitations
- **One fixed opponent** (ChatGPT-3.5) for every evaluation; no cross-play matrix, so scores
  measure "how well you do against gpt-3.5-turbo-1106", and the authors themselves show that
  opponent is exploitable (p. 9). Not reproducible exactly since that model is retired.
- Cost = historical lowest price and Budget = 0.8 × highest price are proxies, not real
  reservation values; both are rescaled per product so profits are only comparable through
  normalization (p. 5). Format failures shrink the valid set unevenly (64 to 930 valid sessions
  per model), and SNP sums over valid sessions, so it mixes format reliability with bargaining.
- Single-issue price bargaining only; no integrative issues, no cooperation, no persuasion
  measure; Talk is free text but only the Action string counts.
- Human comparison is one author on 20 products (App. G).
- OG-Narrator hard-codes the strategy; it shows that offer policy, not language, is the
  bottleneck, but it says nothing about whether a model can learn that policy.
- Models are 2023-era; no reasoning models.

## Relevance to Parley
- **For the map (a)**: a clean, cheap, rule-scored instance of single-issue price bargaining with
  private values and both roles, plus a real-price product set. It covers one skill (claiming
  value in distributive bargaining) and reports it separately per role — a dimension many
  benchmarks collapse. Same family as [[bianchi2024negotiationarena]] (which also found
  buyer/seller asymmetries) and [[zhu2025automated]] / [[liu2026agenticpay]] (consumer-market
  buyer-seller agents).
- **For the transfer study (b)**: it trains nothing; the only "harness" comparison is CoT
  prompting vs a hand-coded offer scaffold (OG-Narrator). The role results are a small hint
  relevant to (b): the *same* skill in two roles ranks models only moderately alike (my
  Spearman 0.54), and scaling helps sellers but not buyers (pp. 6–7). A study of transfer
  between skills should first check transfer between roles of one skill.
- It leaves open: whether training a buyer (SFT on OG-Narrator traces, or RL on SNP) transfers
  to selling, to multi-issue negotiation ([[zhang2026terms]]), or hurts cooperation or honesty.
  OG-Narrator's linear concession policy is a ready-made "teacher" for SFT data, and SNP is a
  ready-made RL reward, so this benchmark is a plausible single-skill training environment.
- Compared with [[he2026socialgym]]: SocialGym's Bargaining game has no free text and scores
  relative standing; Xia et al. score absolute normalized profit against private values, which
  SocialGym lacks. Compared with [[liu2025spiral]]: SPIRAL trains on zero-sum games;
  bargaining here is mixed-motive (both gain in MI sessions).

## Ideas to borrow
- **Normalized profit with MI/CI split**: report deal rate and profit separately for sessions
  where a deal is rational and where it is not; accepting a CI deal is an objective error.
- **First Bid Ratio** as a cheap behaviour probe for anchoring (p. 7).
- **Role-separated scores** and the buyer–seller rank correlation as a within-skill transfer check.
- **Difficulty knob f** (share of no-deal sessions) to stress-test whether agents walk away.
- **Policy/language split** (OG-Narrator): a scripted offer policy with LLM narration is a strong
  baseline and an SFT data source; any trained agent should beat it.

## Map fields
- Skills measured: negotiating value (single-issue price bargaining, buyer and seller roles separately)
- Scoring: rules (normalized profit from budget, cost and deal price; deal rate; format validity)
- Agents: 2
- Opponents: LLM (fixed gpt-3.5-turbo-1106 counterpart); one human buyer in a 20-product pilot
- Tests: capability
- Training evaluated: prompting (CoT) plus a hand-coded offer scaffold (OG-Narrator); no SFT/RL
- Transfer between skills measured: no (roles reported separately; buyer–seller rank correlation 0.54 is my computation)
- Models tested: GPT-4 (0125), GPT-3.5-turbo-1106, Llama-2-7/13/70B-chat, Mistral-7B-Instruct, Mixtral-8x7B-Instruct, Yi-6B/34B-Chat, Qwen-7B/14B-Chat, Baichuan2-7B/13B-Chat, ChatGLM3-6B, Phi-2
- Code released: https://github.com/TianXiaSJTU/AmazonPriceHistory
