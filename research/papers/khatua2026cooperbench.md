---
id: khatua2026cooperbench
title: "CooperBench: Why Coding Agents Cannot be Your Teammates Yet"
authors: [Arpandeep Khatua, Hao Zhu, Peter Tran, Arya Prabhudesai, Frederic Sadrieh, Johann K. Lieberwirth, Xinkai Yu, Yicheng Fu, Michael J. Ryan, Jiaxin Pei, Diyi Yang]
year: 2026
arxiv: "2601.13295"
read: full
relevance: high
topics: [agent-coordination, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: natural
  players: 2
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

## Question
Can two coding agents, each given its own feature on the same repository, coordinate by chat
well enough that their merged patches pass both features' tests? Does the chat help, and how do
they fail?

## Setup
- 652 tasks from 34 feature pools (199 features) over 12 open-source repos in Python, TypeScript,
  Go and Rust; pools hold 2–12 features that are jointly compatible (a gold patch implements all
  of them) but touch overlapping code. 77.3% of tasks have conflicting gold solutions (p. 4).
  Features are small: 52.3 changed lines and 1.4 files on average (p. 22).
- Each agent sees only its own feature, works in its own container (OpenHands v0.54), and can
  send free-text messages at any time through an SQL-backed tool; incoming messages are added to
  the next step's prompt. No turn-taking; 100-action cap (pp. 4, 6).
- Scoring: `git merge-file` the two patches; if that fails, a union merge, then a fine-tuned
  Qwen2.5-Coder-0.5B resolver for trivial conflicts; then run both test sets (pp. 4–5, 22–23).
- Baselines: **Solo** (one agent does both features) and **no comm** (chat tool removed).
  Models: GPT-5, Claude Sonnet 4.5, MiniMax-M2, Qwen3-Coder-30B-A3B, Qwen3-30B-A3B-Instruct.
- Failure analysis: symptom taxonomy applied by GPT-5 as judge (96% agreement with humans on 50
  traces, p. 29); root causes coded by hand on 50 failed traces (p. 10).

## Findings
- **Curse of coordination:** two agents do worse than one doing both features. GPT-5 0.48 Solo
  vs 0.28 Coop; Claude 0.47 vs 0.26; MiniMax 0.36 vs 0.14; Qwen Coder 0.22 vs 0.13 (bar labels
  in Fig. 4, p. 7; the text rounds the leaders to "only 25%", p. 3). Pooled retention
  (Coop AUC / Solo AUC) is 0.59; MiniMax retains only 0.46, while the weakest coder (Qwen
  Instruct) retains the most, 0.68: coding skill does not predict coordination (pp. 24–25).
- The gap is largest on mid-difficulty tasks (p. 7–8).
- More agents is worse: 68.6% with 2, 46.5% with 3, 30.0% with 4 agents (46 tasks, p. 8).
- **Chat does not raise success** (with vs without comm not significant; final merge success
  17.14% vs 17.64% averaged, Table 6, p. 27). It does cut naive merge conflicts, and costs up to
  ~20% of steps (Claude 20.0%, GPT-5 16.3%; p. 8–9).
- What good chat looks like (p. 9): a Plan message in the first turn nearly halves conflicts
  (29.4% vs 51.5%); Plan:Question ratio 2.04 in conflict-free runs vs 1.31; successful runs name
  more line numbers (32.6 vs 22.5) and file paths (13.1 vs 10.0).
- **Spatial vs semantic coordination** (p. 9, App. I): agents agree on *where* to edit, not
  *what* to implement. Case study: 10 messages and 3,000+ words on line ranges, and a wrong
  default value (`case_sensitive=True` vs `False`) that one sentence would have caught (p. 31–33).
- Failure symptoms (Table 1, p. 11): work overlap 33.2%, divergent architecture 29.7%,
  repetition 14.7%, unresponsiveness 8.7%, unverifiable claims 4.3%, broken commitment 3.7%.
- Root causes (Table 2, p. 12): **expectation** 42% (partner's plan was heard but not acted on),
  **commitment** 32% (promised change missing, no checkable contract), **communication** 26%
  (unanswered questions, vague or repeated messages).
- "Trust paradox" (hypothesis, p. 13): models trained to verify before trusting cannot verify a
  partner's branch, so they fail to update on the partner's claims.
- Rare successful behaviours (p. 13–14): role division with mutual confirmation, resource
  division by line ranges, and negotiation where one agent offers mutually exclusive, fully
  specified options ("option (1) or (2)?") and the other picks.
- Prompt optimization gave only marginal gains (App. D, p. 13, 25–27).

## Limitations
- One framework (OpenHands) and one chat tool; the authors do not compare scaffolds or
  protocols, so "chat doesn't help" is about this free-text channel, not communication in general.
- Agents cannot see each other's branches by design; real teams share a repo and can check.
- Features are small and synthetic around one real PR per pool; no human-team baseline (the
  "humans get better with teammates" contrast is asserted, not measured).
- Root causes come from 50 hand-coded traces; symptom shares from an LLM judge.
- Single agent framework per model, no repeated seeds reported; error bars are Wilson CIs over
  task sets. A 2026 preprint: check for a peer-reviewed version before citing.

## Relevance to Parley
- **Direct evidence for parley-mcp.** Its future-work list asks for "lightweight protocols for
  verifiable commitments" (p. 16) — that is what parley-mcp's written agreements and file claims
  are. Its failure counts give parley-mcp a concrete target: claims address work overlap
  (33.2%), written, accepted agreements address broken and unverifiable commitments.
- A ready-made evaluation: CooperBench's Solo / Coop / no-comm design could measure whether a
  parley-mcp channel closes the coordination gap, against the paper's own free-text tool.
- For the negotiation study: the successful "negotiation" pattern (offer complete, mutually
  exclusive options) and the unresponsiveness failures are behaviours Parley can measure in its
  own talks. Not evidence for or against the persuasion claim in [[gap]].
- Diyi Yang's SALT lab ([[yang]]) with Hao Zhu (Sotopia): a concrete paper to cite in outreach.

## Ideas to borrow
- **Solo vs Coop retention** (Coop AUC / Solo AUC over difficulty buckets) as a normalized cost
  of coordination, with Wilson CIs and counts summed across models (App. C).
- A no-comm ablation to show a channel actually changes outcomes, not just traffic.
- Message speech-act coding (Plan / Question / Update / Answer / Ack) and the first-turn-plan
  and specificity (line numbers, file paths) predictors.
- Precision-first LLM judge for chat failures that must quote evidence and may return no label
  (App. F); validate on 50 traces against humans.
- Require agreements to be semantic, not just spatial: values, defaults and interfaces, not
  only line ranges (App. I's one missing sentence).
- Code and data: https://cooperbench.com.
