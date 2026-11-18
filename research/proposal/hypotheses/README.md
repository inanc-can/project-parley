# Hypotheses: concede vs disclose (draft, 2026-11-01)

Made with the `hypothesis-generation` skill from [[gap]] and the 2026-10-24 direction
(`proposal/drafts/2026-10-24-agent-deliberation.md`). All entries are **candidates**, not findings.
No Parley data exists yet and no source note is `read: full`, so nothing here is supported.

## Question
For frozen target agents buying or selling with a private reservation value: does a persuasion or
extraction adversary, compared with a neutral one, change (a) money conceded past the limit and
(b) how much of the limit the transcript gives away? Do defences reduce these without costing the
principal deals?

## Candidates and how to tell them apart

| | Candidate | Its rival | What separates them |
|---|---|---|---|
| H1 | Persuasive content raises concession | H2: volume and persistence of asks; H3: the limit fades over long talks | **Placebo-persistent adversary** (same length, turns and number of asks, no persuasion principle). H1: persuasion above placebo. H2: placebo close to persuasion. H3: concessions start late in every condition |
| H4 | Extraction raises disclosure | H5: the offers alone reveal the limit | **Offers-only estimator**. H4: the full transcript adds information over the offers, more so under extraction. H5: it adds little |
| H6 | Forced restatement of the limit protects the principal | H7: the defence only makes the agent rigid | **Principal surplus including no-deal**, plus a **sham defence** (same note step, no restatement). H6: surplus up, deal rate unchanged. H7: deal rate down, surplus flat |

Positive control: an authorised-concession brief and planted disclosures that the measures must
recover. Comprehension probe before each talk: the target restates its limit.

## Confirmatory analyses (Holm-corrected as one family)
- A1: persuasion vs placebo, per tactic family.
- A2: extraction vs neutral on verbal disclosure.
- A3: defence vs none on principal surplus.

Each is computed within model, paired by scenario, with cluster-bootstrap intervals. Onset timing
(A4) is exploratory. Pilot data is exploratory and its scenarios are not reused. Sample size is not
set yet; use the statistical-power skill after the pilot.

## Decisions for the owner before the record can be frozen
1. **AI-use policy**: check your university's rules on AI-assisted research design, then set
   `ai_use.local_policy_checked`. This is the only validator error left.
2. **Dual use**: whether to publish adversary prompts that work against deployed shopping agents.
3. **Data governance**: provider and model terms for adversarial prompts and published transcripts.
4. **Your own rivals**: add yours before freezing; Claude drafted these, which risks anchoring.
5. **Read the sources**: start with The Automated but Risky Game (A2A-NT) and AgentLeak. No
   challenging source is in the ledger yet.

After 1–3, run `generate_preregistration_scaffold.py record.json -o preregistration.md`.

## Files
- `record.json`: full record. It is the source; the next three files are generated from it.
- `prediction-matrix.csv`, `falsification-controls.json`, `operationalization.json`.
- `evidence-ledger.csv`, `search-boundary.json`: sources, which are existing notes and the draft
  only. No systematic search has been done and novelty is not assessed.

Validator status: matrix, controls, measurements and ledger are valid pending human review. The
record is blocked only by item 1.

The skill asks for this citation if it materially shapes a manuscript: Kassis et al. (2026),
Scientific Agent Skills, arXiv:2609.00065. Check the record on arXiv before citing.
