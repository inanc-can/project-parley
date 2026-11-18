# Research context — read this first

A hand-off for any session (home or work laptop, any Claude account). It says where the research
stands, what has been decided, and how to work with me. Update the "Where I left off" section at
the end of a session. Last updated: 2026-11-18.

## The project in one paragraph
Master's thesis at TUM, Chair of Decision Sciences & Systems (Prof. Martin Bichler); PhD student
Kassian Köck co-writes the proposal (his work: deep RL, LLM agents in markets — see
`papers/bichler2026model.md`). The topic is LLM agents in social and strategic settings
(negotiation, cooperation, persuasion, games). `../parley/` is my platform where agents negotiate;
`papers/` holds the literature notes.

## The current question (my own words, 2026-11-15)
> **Does training one social skill transfer to or hurt the others?**

Behind it: I want a way to benchmark models *and harnesses* (prompting, fine-tuning, RL,
multi-agent) across several social directions, not negotiation alone.

Open decisions on the question (not settled yet):
1. Which 3–4 social skills (candidates: negotiating value, cooperating, competing, persuading,
   resisting persuasion, deceiving/detecting, keeping secrets).
2. Which training methods to compare.
3. Compared to what (untrained model, or a different training under the same budget).
4. "How much", not just "whether".

Direction under consideration (2026-11-16): make the core a **training study** (how to organise RL
or fine-tuning across social skills — single task, mixed, sequential, grouped by structural
similarity — so one skill improves without hurting others), using a light evaluation built from
existing environments (TextArena, SocialGym, TERMS-Bench-style negotiation), rather than building
a new benchmark from scratch. Not yet confirmed; the tie-breaker is whether I want to spend months
on RL runs.

## What the evidence says so far
Full log with page references: `proposal/gap.md`, section "Emerging direction".
- **Closest prior work: `hua2026passive` (SocialRL).** RL transfer matrix across six negotiation
  tasks: structurally similar tasks help each other, some pairs hurt. All six are negotiation,
  only RL is compared, single training runs. My question is still open across *different* social
  skills and *several* training methods.
- **Broad training lifts the average but can hurt specific skills:** `liu2025spiral` (multi-game
  model worse at negotiation), `yuan2025marshal` (specialists win on their own game; competition
  training hurt cooperation), `lyu2026gift` (transfer flips with task pair and model size).
- **Training one skill can wear down another or produce unrequested deception:**
  `sadab2026receiver`, `vendrell2026gametalk`, `sarkar2025training`, `micelibarone2026used`.
- **Skills trade off or diverge inside models:** `wu2026measuring` (CIB, Zou lab: conflict
  handling opposes the other 7 skills), `taylor2026clocktower`, `golechha2025among`,
  `he2026socialgym` (rankings barely carry across game families).
- **TERMS-Bench (`zhang2026terms`, read: partial):** precise finding — LLM negotiators struggle to
  turn *uncertain* information into better offers; strong models act well when told the truth.
- Human-learning parallel worth testing: negative transfer / interference, interleaving, comparing
  cases (analogical encoding, Loewenstein, Thompson & Gentner) — not yet in the knowledge base.

## Plans in progress
- **A map of benchmarks** for LLM social skills / game theory (for the proposal's related work).
  Every benchmark note ends with a "Map fields" block (skills, scoring, agents, opponents,
  capability vs propensity, training evaluated, transfer measured). Axes to be chosen after
  collecting; backlog of ~35 more candidates in `inbox.md` ("Map backlog").
- **Visiting researcher** at Stanford or Berkeley is a goal; hosts and routes in `people/`.
  Strongest link: James Zou's lab (TERMS-Bench, CIB, "Who Should Know What?" — `people/zou.md`).

## My criteria for choosing the direction (agreed 2026-11-14)
Filters: open (not already answered), measurable (verifiable score, ideally not an LLM judge),
feasible for one person in ~6 months, affordable (RL references: ~130–225 H100-hours per run in
`liu2025spiral`; grants possible). Ranked criteria: (1) fit for a Stanford/Berkeley visit,
(2) skills it builds (prompting, fine-tuning, RL), (3) what it leads to (a published paper, then a
research job or a US PhD).

## How to work with me
- **Context first**: say what problem an idea solves before the mechanics.
- **One idea at a time**, short. No long multi-section explanations of several ideas at once.
- **Feynman method**: when I learn a paper or concept, explain one idea, then ask me to explain it
  back and point to the specific gap. Don't re-explain everything.
- **Don't write my research question for me.** Help me sharpen my own wording; check it against
  the notes.
- Be literal and precise; say when something is uncertain or unverified.

## Rules of the knowledge base
See `CLAUDE.md` in this folder. Short version: metadata from arXiv/DBLP only; `read:` must be
honest (only `full` notes support claims); findings carry numbers and page references; run
`uv run scripts/build.py` after changing notes; add a line to `proposal/gap.md` when a paper bears
on the question.

## Where I left off (2026-11-18)
- Knowledge base: 59 notes, 51 read in full. Feynman walkthrough of the new papers paused at GIFT
  (`lyu2026gift`); next suggested: SPIRAL/MARSHAL, then CIB.
- Pending decision: training study (core) vs new benchmark — see "Direction under consideration".
- TERMS-Bench note should be finished (`read: partial`) before citing it in the proposal.
