---
id: oh2026merit
title: "MERIT Feedback Elicits Better Bargaining in LLM Negotiators"
authors: [Jihwan Oh, Murad Aghazada, Yooju Shin, Se-Young Yun, Taehyeon Kim]
year: 2026
arxiv: "2602.10467"
venue: arXiv preprint (v4, 9 Mar 2026)
code: null
read: full
relevance: medium
topics: [negotiation-benchmarks, eval-methodology, judges]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 22 pages (main text pp. 1–9, references pp. 9–11, appendices A–G pp. 12–22) on 2026-11-15.
KAIST AI, Amazon AGI, LG AI Research. The paper names three things: the benchmark **AgoraBench**,
the metric **MERIT**, and the prompting method **ICL-MF** (once called "ICL-UF", Table 18 p. 19).
No code or dataset link is given in the paper; the human-preference data is "released" (p. 1) and
the scenario prompts "will be shared as data" (p. 14), but no URL. `human_baseline: false`: humans
judge pairs of LLM dialogues, they never negotiate.

## Question
Can buyer-side LLM bargaining be evaluated with a metric that matches what humans prefer (not
profit alone), across economically distinct market conditions, and does feeding that metric back
to the model (as a prompt or as SFT data) make it a better buyer? (pp. 1–2)

## Setup
- **AgoraBench** (§3, pp. 3–4): buyer vs seller, Thought–Talk–Action (ReAct) turns, actions BUY,
  SELL, REJECT, DEAL, QUIT, following the AmazonHistoryPrice framework of Xia et al. 2024. The
  seller's initial ask always exceeds the buyer's willingness to pay (WTP); seller cost is hidden
  from the buyer, buyer WTP hidden from the seller (App. A pp. 12–14).
- **Nine market regimes**: Vanilla (single only) plus Deceptive, Monopoly, Installment, Negative
  seller perception, each as Single product and Multi product (4 substitutes, one "desired"); all
  except Vanilla sit on a deception layer where both sides are told "You can be deceptive or
  cunning" (Tables 7–8, pp. 13–14). Nine product categories (camera, smartphone, shoes, bicycle,
  drone, soccer ball, bag, wine, cup) (Table 9, p. 15).
- **MERIT** (§4, pp. 4–5): buyer score = α·CS + β·NP + γ·AR, with consumer surplus CS =
  (WTP − deal)/(WTP − cost), negotiation power NP = (initial − deal)/(initial − cost), acquisition
  ratio AR = cosine similarity (text-embedding-ada-002) between acquired and desired item. No deal
  scores 0 (p. 13). Weights fitted by Bradley–Terry on MTurk pairwise choices, scaled to sum 3:
  α′ = 1.0139, β′ = 0.8812, γ′ = 1.1049 (p. 5; App. C p. 17). Max score 3.
- **Human preference data** (§3.2, §4.2; App. C pp. 14–17): 180 MTurk workers, 20 per product,
  each picks the better of 20 dialogue pairs (10 same-product, 10 different-product), attention
  check ≥ 7/10; paid $1.45, median time 26.1 min, i.e. an effective **$3.33/h** (p. 15). IRB
  exemption.
- **Evaluation protocol**: 10 runs per model–opponent pair per market and item; item means
  averaged per market (p. 13). Temperature 1 for all models (p. 22).
- **Behaviour study** (§5, Table 2 p. 6): five buyers (gpt-4o, gpt-4o-mini, gpt-3.5-turbo,
  gemini-1.5-pro, gemini-1.5-flash) with ReAct, across the nine regimes.
- **ICL-MF** (§6, App. B pp. 14–16): the MERIT formula is put in the system prompt as a "private
  reward function", with instructions to estimate the seller's cost and keep the deal alive.
  Baselines: ReAct and OG-Narrator (linear price schedule from 50% to 100% of budget). Buyers:
  the five above vs a gemini-1.5-pro seller; and GPT-5.1, DeepSeek-v3.2, Sonnet 4.5, Gemini-3-
  Flash, gpt-oss-120b, gpt-oss-20b (+ reasoning modes of GPT-5.1 and DeepSeek-v3.2) vs a
  DeepSeek-v3.2 seller (Table 4, p. 7).
- **SFT** (§6.1 p. 8; App. F p. 22): LoRA (r 16, attention projections only) on gpt-oss-20b, trained
  on human-preferred buyer turns (reasoning, utterance, action; seller thoughts removed) from the
  **Deceptive regime with GPT/Gemini opponents only**, evaluated on all nine regimes vs an unseen
  DeepSeek-v3.2 seller ("dual out-of-distribution shift", p. 8). Dataset size not reported.
- **LLM judge** (§6.2, pp. 8–9; Table 10 p. 15): gemma-3-27b-it picks the dialogue "more favorable
  in buyer perspective" from ICL-MF vs baseline pairs in random order.

## Findings
- **MERIT matches human choices better than profit**: ROC AUC 0.80 vs 0.68 for a profit-only
  metric (Fig. 3, p. 5). Whether the AUC is on held-out pairs is not stated.
- **Baseline buyers (ReAct, Table 2 p. 6)**: average MERIT gemini-1.5-pro 1.381 (deal 80.3%),
  gpt-3.5-turbo 1.257 (88.5%), gpt-4o 1.247 (83.9%), gpt-4o-mini 1.240 (79.0%),
  gemini-1.5-flash 1.044 (69.6%). No consistent size–performance trend outside Gemini (p. 21).
- **Market effects** (pp. 6, 21): allowing deception raises buyer MERIT by +0.10 and deal rate by
  +10.62 pp vs vanilla; monopoly lowers deal rate by 3.34% (single) and 8.80% (multi) and MERIT by
  ~0.10/0.13; installments raise single-item deal rates at worse prices; negative seller perception
  lowers deal rates. Authors read such directional shifts as a test of "market compatibility".
- **Anchoring and first mover** (Table 3, p. 6): a $550 vs $520 seller anchor raises the final
  price (gemini-1.5-pro 444.6 vs 432.1); a buyer first offer lowers it further (422.6).
- **Irrational concessions**: gpt-4o-mini offers $480 → $475 → $450 → back to $480 (Table 20,
  p. 20), non-monotone concessions atypical for humans.
- **ICL-MF vs baselines** (Table 4, p. 7): vs gemini-1.5-pro seller, average single-product MERIT
  ReAct 1.160 (76.7% deals), OG-Narrator 1.060 (42.6%), ICL-MF **1.576 (99.2%)**; multi-product
  1.360 / 1.414 / 1.576 (99.6%). Vs DeepSeek-v3.2 seller: single 1.582 / 0.997 / 1.747, multi
  1.541 / 1.114 / 1.789. Exceptions: Sonnet 4.5 single (OG-Narrator 1.856 > ICL-MF 1.778) and
  Gemini-3-Flash single (2.116 > 1.995). Deal rates near 100% suggest ICL-MF mostly prevents
  walk-aways.
- **Raw outcomes** (Table 19, p. 19): GPT-5.1 buyer profit per attempt ReAct 22.5, ICL-MF 30.7;
  Sonnet 4.5 ReAct 6.1, OG-Narrator 40.6, ICL-MF 19.6 — so on profit alone ICL-MF is not always
  best.
- **Opponent-aware reasoning (OAR)**: 25.6% of ICL-MF buyer-thought sentences mention seller cost,
  profit or next move vs 2.1% for ReAct (Table 18, p. 19). Adding an explicit OAR prompt to ReAct
  closes most of the gap (gpt-4o single 1.120 → 1.636 vs ICL-MF 1.606) (Table 17, p. 18), so much
  of the gain is "think about the opponent's cost", not the metric itself.
- **SFT** (Table 6, p. 8): gpt-oss-20b vs DeepSeek-v3.2 single MERIT ReAct 1.325 (89.3%), ICL-MF
  1.413 (91.3%), SFT 1.332 (89.6%); multi 0.986 (65.3%), 1.410 (86.6%), **1.459 (93.1%)**. SFT
  helps only in multi-product.
- **LLM judge** prefers ICL-MF over OG-Narrator in ≥84.7% of pairs on average (94.4% deceptive,
  71.3% installment) and over ReAct in 70–83.3% (Fig. 5, p. 8).
- **Same-family pairs** reach higher deal rates (gpt-4o in 4 of 5 markets; both Gemini models in
  all markets) (App. E p. 19; Fig. 11).

## Limitations
- **Buyer-only**: the seller side has no metric (p. 9), and every reported run uses one fixed
  seller model per table; no cross-play matrix, no rating of sellers.
- **MERIT is not neutral between methods**: ICL-MF is told the exact formula it is then scored on.
  The OAR ablation and Table 19 show part of the gain is generic opponent modelling and deal-
  keeping rather than better bargaining.
- **AR via embedding similarity** is a proxy for preference (a Film Camera scores 0.57 against a
  DSLR, Table 9 p. 15); it rewards buying something semantically close, not what the buyer values.
- Small samples: 10 dialogues per product per condition, standard deviations reported but no
  significance tests; SFT data size, epochs and seeds beyond 42 are not given.
- MTurk annotators paid ~$3.33/h, judging LLM dialogues, not negotiating themselves; no human
  negotiation baseline.
- The "deception layer" instructs both sides to be deceptive; there is no measure of when models
  deceive unprompted, nor of lying itself (risk noted on p. 12).
- Only one skill (single-buyer price bargaining with substitutes); no code link.

## Relevance to Parley
- **Map entry**: a price-bargaining benchmark with economically motivated market variants and a
  human-fitted outcome metric. It covers *value claiming* for a buyer under deception, monopoly,
  installments and reputation shocks. It does not cover value creation (no multi-issue trade-offs
  beyond substitutes), multi-party play, persuasion resistance or propensity.
- **For the transfer study (b)**: it is one of few negotiation papers that compares prompting and
  SFT on the same eval (Table 6), and the SFT arm already tests a small *within-negotiation*
  transfer (trained on Deceptive regime + GPT/Gemini opponents, tested on all nine regimes +
  DeepSeek seller). Result: SFT ≈ ReAct on single-product (+0.007) but +0.47 on multi-product. It
  does not test transfer to any other social skill, and has no RL arm. A thesis could reuse the
  nine regimes as "near-transfer" test conditions and add far-transfer tests (cooperation,
  persuasion resistance) to see whether bargaining SFT helps or hurts them.
- Compare [[zhang2026terms]]: both diagnose bargaining beyond deal rate; TERMS uses scripted
  opponents with known types, MERIT uses a single LLM seller and a human-fitted scalar. Compare
  [[zhu2026piearena]]: PieArena scores pie share relative to BATNAs and covers multi-issue value
  creation; MERIT's CS/NP are buyer-only cousins of pie share.
- The deception finding (deception raises buyer MERIT) parallels PieArena's lie-rate → pie-share
  link (+3.23 pp) and [[bianchi2024negotiationarena]]'s observation that tactics like feigned
  desperation pay off. For [[judges]]: the gemma judge agrees with MERIT, but it is shown both
  outcomes, so this is weak evidence of judge validity.
- [[davidson2024evaluating]] already noted cooperative bargaining as the hardest case; MERIT avoids
  it entirely by scoring only the buyer.

## Ideas to borrow
- **Fit outcome-metric weights to human pairwise choices** with Bradley–Terry (p. 17) — a cheap way
  to justify any composite score in the map.
- **Market-condition shifts as a coherence test**: does a model's deal rate and surplus move in
  the economically expected direction under monopoly, reputation shocks, substitutes (p. 7)?
  Usable as a "near-transfer" battery.
- **Count opponent-aware reasoning sentences** in private thoughts (Table 18) as a process measure
  next to outcomes.
- **Report raw outcomes next to the composite** (deal rate, price on deals, profit per attempt,
  Table 19) so a method that wins by over-conceding is visible.
- Avoid: telling the treated model the exact evaluation formula, and paying annotators below
  minimum wage.

## Map fields
- Skills measured: negotiating value (buyer-side price bargaining with substitutes, under permitted deception)
- Scoring: mixed (rule-based MERIT with weights fitted to human preferences; LLM judge as secondary check)
- Agents: 2
- Opponents: LLM (one fixed seller model per experiment: gemini-1.5-pro or DeepSeek-v3.2)
- Tests: capability
- Training evaluated: prompting, SFT
- Transfer between skills measured: no (only across market regimes and opponents within bargaining)
- Models tested: gpt-4o, gpt-4o-mini, gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro, GPT-5.1 (± reasoning), DeepSeek-v3.2 (± reasoning), Claude Sonnet 4.5, Gemini-3-Flash, gpt-oss-120b, gpt-oss-20b (SFT base)
- Code released: none (no link in the paper)
