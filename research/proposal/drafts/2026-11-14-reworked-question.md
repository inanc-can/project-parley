# Reworked research question (draft, 2026-11-14)

Draft for the student, Kassian and possible hosts. Not final. Builds on [[gap]] and its
2026-11-14 evidence log. Notes marked (partial) are not `read: full`, so they give context only
and do not support claims: [[zhang2026terms]], [[bichler2026model]].

## 1. Candidate core questions

### A. Cheap talk with offers held fixed
**When a counterpart's offers are fixed, how much of its principal's money does a delegated
negotiating agent give up because of what the counterpart says, and which properties of the agent
and its deployment decide that loss?**

- New vs prior work: [[li2026whose]] bundles tactics into personas and scores binary harm with LLM
  judges (pp. 4–6), with judge agreement as low as κ = 0.08 (p. 15). Here the counterpart's price
  policy is scripted and identical across conditions, and only its messages vary. Any change in the
  outcome is caused by the words. [[sadab2026receiver]] finds the target explains ~47% of
  variance and the wording ~2% (pp. 4–5), but in a donation game where refusing is always right.
  Here a deal inside the limit is correct, so "refuse everything" loses money.
  [[zhu2025automated]] shows limit breaches with no persuasion (pp. 4–5).
  [[liu2026instructing]] tests only three crude personas (Table 3, p. 10).
- Primary outcome: principal surplus per episode (money), paired against the same agent's
  neutral-message control on the same seed. Secondary outcomes: limit breaches, false agreement on
  no-deal episodes, and deal rate on feasible episodes (the over-refusal check).
- Theory benchmark for the chair: messages not backed by offers are cheap talk, so a rational
  delegate's concessions should not move. The measured loss is the distance from that benchmark.
- Layers: **core** = targets × deployments (limit restated or not, raw vs summarized history,
  private note) × message conditions (neutral, length-matched placebo, three or four tactics
  including a false cost claim), plus a small symmetric LLM-vs-LLM slice to check that results
  hold there. **Ext 1** = prompt/deployment defence vs fine-tuning (distillation from a robust
  teacher) on an open 8B model, on the same money score. **Ext 2** = GRPO with the
  [[liu2026instructing]] reward (pp. 4–5) against persuading counterparts, tested on held-out
  tactics, with honesty measured ([[micelibarone2026used]], p. 7).

### B. Defence ladder
**Which defence (prompt/deployment change, fine-tuning, RL with a money reward) best keeps a
delegated agent's principal surplus against adaptive persuaders without losing good deals?**

- New vs prior work: [[li2026whose]] compares prompting, distillation and RL but on judge-scored
  binary harm, and its RL made harm worse (33 → 46, p. 14). [[liu2026instructing]] has RL
  robustness but no comparison with other defences. New here: all three defences on one money score.
- Primary outcome: principal surplus and deal rate on feasible episodes, against held-out tactics.
- Layers: **core** = prompt/deployment defences; **ext 1** = fine-tuning; **ext 2** = RL. The weak
  point: the contribution sits mostly in the extensions, which carry the compute risk.

### C. Concede vs disclose, priced in money
**How much principal money does a delegated agent lose by conceding past its limit compared with
disclosing the information behind that limit to an extracting counterpart?**

- New vs prior work: continues the 2026-10-24 draft. [[li2026whose]] counts leakage as a binary
  cell (Table 1, p. 4). [[zhu2025automated]] shows budget reveal followed by overpayment (p. 5).
  New: both paths priced in money.
- Primary outcome: concession past the limit, plus disclosure measured as the extra surplus an
  estimator-guided counterpart captures.
- Layers: **core** = measurement; **ext 1** = defences per path; **ext 2** = RL. Disclosure depends
  on an estimator, which is itself a model and may be noisy.

## 2. Scoring

| | A. Cheap talk, offers fixed | B. Defence ladder | C. Concede vs disclose |
|---|---|---|---|
| Open | pass: no study holds offers fixed and varies deliberate tactics (risk: the TERMS group may do it) | risk: li2026whose and liu2026instructing cover much of it | risk: li2026whose already measures leakage, though not in money |
| Measurable | pass: money from a scripted counterpart, no judge for the outcome | pass: money, if RL reward is reused | risk: disclosure needs an estimator |
| Feasible (6 months) | pass: core is API runs; ext 2 optional | risk: core result depends on training working | pass |
| Affordable | pass: estimate a few hundred to ~$1,500 API (uncertain, from a rough episode count) | risk: RL compute needs a grant | pass |
| Host fit | high: extends TERMS-Bench (Zou); A2A-NT money metrics (Pentland/Pei) | med: Simchi-Levi fits best (MIT, not on the list) | med: Pentland/Pei, Song |
| Skills | med in core, high with ext 1–2 | high | low–med |
| Leads to | high: clean causal result, publishable as null or effect | med: risk of looking incremental to li2026whose | med |

## 3. Recommendation: A

Why: it is the only candidate where the outcome is money with no judge in the loop, and the cause
is isolated by design. It answers the open point named in the TERMS-Bench limits (the counterpart
never persuades; [[zhang2026terms]], partial). It turns the [[sadab2026receiver]] warning into a
factor: if wording matters little, the agent and deployment factors carry the result. It speaks the
chair's language: cheap talk, a rational benchmark, deployment as the treatment
([[bichler2026model]], p. 16, partial), and auditing.

Main risk: message conditions move surplus very little once offers are fixed (as in
[[sadab2026receiver]], p. 5). Then the core becomes "deployment and model explain the loss, wording
does not". That result is still publishable with equivalence tests, but it is less striking.

Cheapest viability pilot (1–2 weeks):
- 2 targets (one open mid-size model, one frontier model), 1 deployment.
- 5 message conditions: neutral, length-matched placebo, false cost claim, hardship story,
  authority/deadline.
- About 100 paired seeds per cell. Scripted concession policy (TERMS-style; whether its code can
  be reused is unchecked, otherwise a simple formula in Parley).
- Positive control: a brief that authorizes conceding, which the measure must detect.
- Go if at least one tactic moves surplus below neutral, with a CI excluding zero in at least one
  model, and the deal rate on feasible episodes stays measurable. Otherwise shift the core to the
  deployment factor.

## 4. Provisional version for an email to a host

I am a master's student at TUM (Prof. Martin Bichler's chair) planning a six-month thesis on
delegated negotiating agents. TERMS-Bench showed that a scripted counterpart makes agent
failures measurable in money, and that tone alone lowers surplus. My question is the next step:
if the counterpart's offers are held fixed and only its messages change, how much of its
principal's money does an agent give up to deliberate persuasion, such as false cost claims,
deadlines or hardship stories? And what about the agent and its deployment (what it sees, whether
its limit is restated) decides that loss? Since unbacked messages are cheap talk, a rational agent
should lose nothing, which gives a clear benchmark. Optional later parts compare prompting,
fine-tuning and RL as defences on the same money score. I would value a short conversation about
whether this fits your group's work.

## 5. Open questions (student, Kassian or a host)

1. Kassian: is the cheap-talk framing acceptable as the chair's theoretical anchor, or does it
   need a market or welfare component (e.g. bankroll mode, several counterparts)?
2. Kassian: can the thesis be partly written during a visit, and what are the start and end dates?
3. Host (Zou group): is an adaptive or persuading TERMS counterpart already in progress? Can the
   TERMS code take a custom message layer?
4. Student: which target models, given the budget? Must an open model be in the core for ext 1–2?
5. Student/Kassian: may tactic prompts that work against deployed shopping agents be published
   (dual use)?
6. Student: a scripted counterpart is less realistic than symmetric agents. Is a small symmetric
   slice enough to defend the framing?
7. Funding: BlueDot or Tinker grant for ext 2, and when to apply.
