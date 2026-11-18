---
id: hua2026passive
title: "From Passive Delegates to Strategic Negotiators: Reinforcing Social Reasoning in Small Language Models with SocialRL"
authors: [Wenyue Hua, Zachary Huang, Tyler Payne, Safoora Yousefi, Saleema Amershi, Asli Celikyilmaz]
year: 2026
arxiv: "2608.13787"
venue: arXiv preprint (v1, 13 Aug 2026)
code: null
read: full
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

Read all 25 pages (main text pp. 1–22, references pp. 22–25; there is no appendix) on 2026-11-15.
Microsoft Research, AI Frontiers. No code or data link appears in the paper. Turns alternate
(free-form messages plus structured proposals), so `turn_protocol: strict`; the interface also
supports simultaneous moves and N players, but every reported experiment is 2-party.

## Question
Can a small model (4B) be post-trained to act as a strategic *delegate* — protect its principal's
private information, anchor, concede selectively, walk away — instead of the friendly, agreeable,
leaky behaviour of assistant models? Does training in one negotiation/coordination domain transfer
to the others, and can the per-domain specialists be merged into one model? Does explicit
theory-of-mind supervision help? (pp. 1–3)

## Setup
- **Infrastructure (SocialRL)**: event-based, agent-agnostic environment interface
  (`decide(context, actions) → action`; observation vs notification events; per-agent filtered
  channels; stale/invalid/timeout actions logged, not fatal) and an OpenAI-compatible rollout proxy
  that records exact model inputs/outputs + log-probs per session and writes a Parquet buffer for
  PPO (veRL/phitrain) or distillation (§3, pp. 4–7). Werewolf/Avalon are named as supported but not
  used.
- **Six 2-party domains** (Table 1, p. 8): Deal-or-No-Deal (3-item allocation, values sum to 10),
  CaSiNo (3 resources × 3 units, priorities 5/4/3, max 36), Craigslist (single-issue price, buyer
  analysed), Job Interview (5-issue contract, ~10^4 outcomes), Calendar and Marketplace (both from
  Microsoft's SocialReasoning-Bench; Calendar = choose a meeting slot against a requestor with
  opposed preferences; Marketplace = buyer with private reservation price, ZOPA guaranteed).
  All are **mixed-motive bargaining or preference-conflict coordination between a principal's
  agent and a counterpart**; there is no pure cooperation, zero-sum game, hidden-role/deception
  game or persuasion/resistance task.
- **Reward: rules only, terminal, in [0, 1]** (§4.2, pp. 8–10). DnD/CaSiNo: utility passed through a
  sigmoid centred on the envy-free Pareto-optimal reference for that role (Eq. 2, 5, T = 0.2);
  Job Interview: same transform centred on the egalitarian (max-min) deal (Eq. 3–5);
  Craigslist/Marketplace: share of the price corridor captured (Eq. 6–8); Calendar: principal's
  slot value normalised over mutually free slots (Eq. 10). No deal/timeout = 0 (or the env's
  walk-away payoff). No LLM judge anywhere in scoring.
- **Model**: Qwen3-4B-Instruct-2507 only. PPO with a Qwen3-1.7B critic (30 critic warm-up steps,
  actor lr 2e-6, batch 144, ≤200 steps); Craigslist and Marketplace get an SFT warm start before
  PPO; the other four PPO from base (pp. 10–11). SFT data source for the warm start is not stated.
- **Counterparts are not specified.** Evaluation is "10 scenarios × 3 opponents × 5 trials (150
  games per environment)" on held-out scenarios (Table 5 caption, p. 14), but the paper never says
  who the 3 opponents or the training counterparts are (fixed LLM? which?). No self-play, no
  population, no human opponents.
- **Baselines**: base 4B; GPT-4.1, GPT-5.1, GPT-5.2, GPT-5.5 (single mean, no variance) (Table 2).
- **Unification** (§5.3): cascade RL (sequential PPO per domain, 200 steps each, checkpoint picked
  every 20 steps by mean over domains seen so far) under transfer-aware, random and anti-transfer
  orders; and multi-teacher on-policy distillation (MOPD: reverse KL to the domain specialist,
  top-32 logits, lr 1e-5, gap-closed sampling curriculum). Both start from the Craigslist-SFT
  checkpoint (p. 12).
- **ToM study** (§5.4): INFER → ACT → ANTICIPATE scaffold; prompt-only vs SFT on actions vs SFT on
  GPT-5.2 traces with the ToM steps ("ExpToM"), per-env or mixed over the 4 negotiation domains.
- **Variance**: one training run per configuration; ± values are std across 3–5 *evaluation*
  re-runs (footnote p. 11 says 5; Table 3 caption says 3; Table 5 transfer-aware says 2). No
  training seeds, no significance tests. **Compute** (GPUs, hours) not reported.

## Findings
- **Specialists reach GPT range** (Table 2, p. 11): base 4B avg 0.389 → domain-trained 0.619
  (DnD 0.656, CaSiNo 0.503, Craigslist 0.583, Job 0.594, Calendar 0.540, Marketplace 0.838) vs
  GPT-4.1 0.625, GPT-5.1 0.619, GPT-5.2 0.613. **GPT-5.5 is clearly better at 0.708** (Craigslist
  0.746, Marketplace 0.985). Calendar specialist (0.540) is below all GPTs (0.573–0.702).
- **Transfer matrix** (Table 3, p. 12; deltas vs base computed from the table): strongest is the
  price pair, Craigslist→Marketplace +0.317 and Marketplace→Craigslist +0.184. Calendar is a
  destructive donor (Craigslist −0.151, Job −0.168; out-transfer −0.060). Job Interview is the
  broad donor (+0.026). Full matrix in the overlap section below.
- **Cascade order matters** (Table 5, p. 14): transfer-aware 0.627 ± 0.004 vs random 0.578 ± 0.008
  (text says 0.584) vs anti-transfer 0.562 ± 0.010. Calendar ends at 0.742, above its own specialist
  (0.540), and rises *after* CaSiNo/DnD stages with no Calendar updates (0.621 → 0.733 → 0.758,
  Table 4, p. 14). Craigslist dips during allocation stages (0.614 → 0.489) then recovers.
- **MOPD** (Tables 6–7, pp. 16–17): 60 steps, Avg-6 0.597 ± 0.015, 92.6% mean gap closure (84.5%
  clipped); beats its teachers on DnD (0.664 vs 0.656) and Calendar (0.564 vs 0.540). Dropping the
  saturated CaSiNo teacher helps.
- **ToM** (Table 8, p. 18): ToM *prompt* hurts the base model (avg 0.454 → 0.353; Job 0.476 →
  0.221). ExpToM SFT 0.546 per-env / 0.525 mixed vs action SFT 0.500 / 0.495; GPT-5.2 0.567.
  Next-action prediction rises ~30 pp after training; base preference inference 0.618 vs
  next-action ~54%. Next-action accuracy correlates with utility, preference inference "shows
  little" relationship (p. 17–18) — no coefficients or n given.
- **Behaviour** (§6, pp. 18–21): Craigslist buyer opens below target 3% → 71% (SFT) → 78% (PPO);
  base buyer states its private target in 52.7% of messages → 1.0% after SFT; Marketplace base
  reveals its reservation price in 62% of openings → "essentially disappears" after PPO; opening
  0.956 → 0.361 of reservation. Calendar: meetings scheduled 92% → 74%, max-utility slots 16% →
  38%. Reject actions 0–3% → ~14% (DnD) and ~20% (Job). SFT alone *raised* CaSiNo over-concession
  17.3% → 29.4%; PPO lowered it to 13.6%. Commitment language 3% → 23% (Craigslist), 2% → 43% (Job).
- **Learned dishonesty, flagged in passing**: trained Craigslist buyers cite market comparables the
  environment never provided — "fabricated", "learned bluffing", treated as a limitation (p. 19).

## Limitations
- One base model (4B), one training run per arm, variance only over evaluation re-runs, 10 held-out
  scenarios per domain; many matrix cells differ by less than 0.03, inside plausible run-to-run
  training variance that is never measured.
- Opponents unnamed and fixed; no cross-play against varied or adaptive counterparts, so "transfer"
  may partly be transfer of exploits of one counterpart's style.
- Donor arms are not matched: Craigslist and Marketplace donors had SFT+PPO, the rest PPO only
  (Table 3 †); the Craigslist donor's large out-transfer is confounded with SFT data.
- Text/table inconsistencies (avg 0.615 vs 0.619, random cascade 0.584 vs 0.578, baseline std
  differs between Tables 2 and 3, ToM-section base scores differ from Table 2, Table 10 caption
  lists columns that are missing); the abstract's "73–122% gap closed" is not computed in the body.
- No evaluation outside the six domains: no general-capability, helpfulness, honesty or safety
  checks after training, although training visibly increases fabrication and firmness.
- Only the principal's side is trained in asymmetric domains (Marketplace buyer); behaviour metrics
  (politeness, firmness, leakage) have no stated measurement method.

## Overlap with the student's question
The student's question: does training one social skill transfer to or hurt the others, across
harnesses (prompting, fine-tuning, RL, multi-agent) and across directions (negotiating value,
cooperating, competing, persuading, resisting persuasion, deceiving/detecting, keeping secrets)?

**1. Tasks — all one direction.** The six domains are all *2-party mixed-motive negotiation over
private values* (Table 1, p. 8): two allocation games (DnD, CaSiNo), two single-issue price games
(Craigslist, Marketplace), one multi-issue contract (Job Interview), one slot-coordination game
whose requestor is built "in opposition to the principal's preferences" (Calendar, p. 10). Calendar
is called coordination but is scored as value-claiming for the principal, not joint success.
There is **no** pure cooperation task (no joint-reward or team game), no zero-sum competitive game,
no deception/detection or hidden-role game, no persuasion or resistance-to-persuasion task, and no
explicit secret-keeping task (leakage appears only as a behavioural side-measure, p. 19–20). In
the student's taxonomy this is *negotiating value*, with keeping secrets measured incidentally.
The transfer matrix is therefore **within-direction transfer across negotiation structures**, not
transfer between social skills.

**2. Transfer matrix** (Table 3, p. 12; rows = donor, delta vs base 4B on each off-diagonal
recipient, computed from the table; in-domain gain on the diagonal):

| Donor ↓ / recipient → | DnD | CaSiNo | Craigslist | Job | Calendar | Mktplace | Out-transfer |
|---|---|---|---|---|---|---|---|
| base score | 0.583 | 0.476 | 0.318 | 0.479 | 0.301 | 0.174 | — |
| DnD | **+0.073** | +0.015 | −0.036 | +0.002 | +0.069 | −0.024 | +0.005 |
| CaSiNo | +0.014 | **+0.027** | −0.009 | −0.016 | +0.030 | −0.006 | +0.003 |
| Craigslist (SFT+PPO) | −0.019 | +0.018 | **+0.265** | −0.032 | −0.035 | +0.317 | +0.050 |
| Job Interview | +0.027 | +0.035 | +0.010 | **+0.115** | +0.072 | −0.013 | +0.026 |
| Calendar | +0.024 | −0.002 | −0.151 | −0.168 | **+0.239** | −0.002 | −0.060 |
| Marketplace (SFT+PPO) | −0.025 | −0.012 | +0.184 | −0.108 | −0.033 | **+0.664** | +0.001 |

- *Helps*: Craigslist↔Marketplace (+0.317 / +0.184); DnD↔CaSiNo (+0.015 / +0.014); Job Interview
  helps 4 of 5; Calendar as a *recipient* gains from DnD (+0.069), Job (+0.072), CaSiNo (+0.030).
- *Hurts (negative transfer, yes)*: Calendar → Craigslist −0.151 and → Job −0.168; **Marketplace →
  Job −0.108** (in the table but not discussed in the text); Craigslist → Calendar −0.035, → Job
  −0.032; DnD → Craigslist −0.036. 13 of 30 off-diagonal cells are negative, but most are below
  0.04 and within the reported eval std plus unmeasured training variance.
- *Measurement*: rule-computed normalised utility only (§4.2), against the same 3 unnamed opponents
  on 10 held-out scenarios; out-transfer = mean off-diagonal delta. No judge. Baselines are the base
  4B and four GPT models (no variance for GPTs). Uncertainty: std over 3 (Table 3 caption) or 5
  (footnote p. 11) eval re-runs of a single trained checkpoint; **no training seeds, no CIs, no
  tests**. Donors are not matched (two had an SFT warm start).
- *Second-order evidence*: cascade order changes the final model by 0.065 Avg-6 (0.627 vs 0.562,
  Table 5) and stage-wise tables show forgetting and recovery (Table 4) — interference is real and
  path-dependent within negotiation.

**3. Training methods compared**: prompting (ToM scaffold prompt only, hurts: −0.101 avg, Table 8);
SFT on actions (source unclear for the Craigslist/Marketplace warm start; GPT-5.2 demos in §5.4);
SFT on ToM traces distilled from GPT-5.2; single-domain PPO; cascade RL (3 orders); multi-teacher
on-policy distillation (2 curricula × with/without CaSiNo). **No multi-agent/self-play training**
(fixed counterparts), no DPO/GRPO, no comparison of harnesses *on transfer*: the transfer matrix is
RL-only (SFT+PPO for two donors); the SFT/ToM study reports only in-domain and mixed scores on 4
domains, not a cross-domain matrix. One model size (Qwen3-4B-Instruct-2507, critic Qwen3-1.7B).
Compute: PPO ≤200 steps/domain at batch 144, MOPD 60 steps; GPU hours not reported.

**4. What it does NOT cover that the student's question adds**:
- *Other social directions*: cooperation with joint reward, zero-sum competition, persuading,
  resisting persuasion, deception and its detection, explicit secret keeping. The core question —
  does training negotiation change cooperation or susceptibility to persuasion? — is untested.
- *Propensities*: the paper's own trajectories show training raises fabrication ("learned
  bluffing", p. 19) and drops leakage (52.7% → 1.0%, 62% → ~0), i.e. training negotiation shifted
  honesty and secrecy propensities, but neither is measured systematically or as a transfer target.
  No check that the hard-bargaining delegate stays honest or helpful elsewhere.
- *Harness comparison on transfer*: prompting vs SFT vs RL vs multi-agent training are never
  compared on the same off-domain matrix.
- *Multi-agent setups*: no self-play, population or cross-play training; no N > 2 games despite the
  infrastructure supporting them; opponents fixed and unnamed.
- *Rigor*: training seeds, CIs, matched donor budgets, several model sizes/families.
- *Verifiable scoring* is present (rules, no judge) — that part the student can borrow, not add.

**5. Verdict: narrows the question, does not pre-empt it.** It is the first full donor × recipient
transfer matrix under RL for LLM social-interaction tasks I have seen, and it answers a *narrow
sub-question* ("does RL on one negotiation structure transfer to other negotiation structures?"):
yes when structure matches (price↔price), sometimes harmful otherwise (Calendar, Marketplace →
Job) (Table 3 p. 12; Table 5 p. 14). It leaves the student's question — transfer and interference
*between different social directions*, compared across harnesses, with propensities — largely open
(all six domains are negotiation, p. 8; no cooperation/deception/persuasion tasks; no harness
comparison on transfer; single runs). The student must cite it as the closest prior work and
position against it: "Hua et al. show structure-dependent transfer *within* negotiation under RL;
we ask whether it holds *across* social directions and harnesses, and whether it moves honesty."
Its finding that structural similarity predicts transfer gives the student a testable hypothesis
for the cross-direction case.

## Relevance to Parley
- **For the benchmark map (a)**: a training suite more than a benchmark — 6 classic negotiation
  datasets with rule rewards normalised to [0, 1]; useful as the "negotiating value" column, with
  a clean difficulty-aware reward (envy-free Pareto / egalitarian reference) that the student could
  reuse.
- **For the transfer study (b)**: closest prior work (see verdict). Compared with
  [[yuan2025marshal]]: MARSHAL found competition-only training drops cooperation (Mini Hanabi 24.5
  vs 30.0); SocialRL has no cooperation task to test that. Compared with [[liu2025spiral]] (zero-sum
  self-play) and [[jiang2026model]] (judge-scored self-play): SocialRL is rule-scored but not
  self-play. Compared with [[liu2026instructing]] and [[bergemann2026training]]: same "RL with
  verifiable economic rewards" line, now across six domains. [[he2026socialgym]] covers the
  directions SocialRL lacks but trains nothing — combining SocialGym-style breadth with SocialRL's
  donor × recipient design is the student's study.
- Uses [[lewis2017deal]] (DnD) and the Marketplace domain parallels [[zhu2025automated]]; cites
  [[zhang2026terms]], [[bianchi2024negotiationarena]], [[zhu2026piearena]], [[juneja2025magpie]].
- For the [[persuasion-susceptibility]] angle: base assistants "concede the principal's position at
  the first sign of resistance" (abstract) — trained resistance to concession is a negotiation-side
  analogue of persuasion resistance, but the paper never tests resistance to argument.
- Training increased fabrication: a direct example of a capability gain coming with an honesty
  cost, the kind of side effect Parley's study should measure.

## Ideas to borrow
- **Full donor × recipient matrix with out-transfer** (mean off-diagonal delta) as the headline
  table; add training seeds and CIs, which this paper lacks.
- **Transfer-aware curricula as a test**: if a matrix is real, ordering by it should beat
  random/anti orders (0.627 vs 0.578 vs 0.562) — a nice falsification check of a transfer matrix.
- **Difficulty-aware reward**: centre a sigmoid on a scenario's fair-efficient reference (Eq. 5) so
  rewards compare across scenarios.
- **SFT vs RL behaviour ladder**: report untrained → SFT → RL behaviour rates (leakage, anchoring,
  over-concession) to separate what imitation adds from what reward selects (§6).
- **Rollout proxy** at the OpenAI-API boundary so any harness can be trained without changes —
  relevant to Parley's own agent-agnostic design.
- Measure honesty/leakage as *side effects* on every trained arm, since this paper shows they move.

## Map fields
- Skills measured: negotiating value (allocation, price, multi-issue contract, preference-conflict scheduling); keeping secrets only as a side measure (leakage rates); other: theory of mind (preference inference, next-action prediction)
- Scoring: rules (normalised utility); behaviour rates by unstated method
- Agents: 2
- Opponents: LLM (3 unnamed fixed opponents; not specified)
- Tests: capability (propensity changes — leakage, fabrication — reported anecdotally)
- Training evaluated: prompting / SFT / RL (PPO, cascade RL, on-policy distillation); no multi-agent
- Transfer between skills measured: yes, but only across six negotiation domains, not across social directions
- Models tested: Qwen3-4B-Instruct-2507 (trained); GPT-4.1, GPT-5.1, GPT-5.2, GPT-5.5 (baselines); GPT-5.2 as ToM teacher
- Code released: none linked in the paper (v1)
