---
id: zeng2024johnny
title: "How Johnny Can Persuade LLMs to Jailbreak Them: Rethinking Persuasion to Challenge AI Safety by Humanizing LLMs"
authors: [Yi Zeng, Hongpeng Lin, Jingwen Zhang, Diyi Yang, Ruoxi Jia, Weiyan Shi]
year: 2024
arxiv: "2401.06373"
venue: arXiv preprint (v2, 23 Jan 2024); cited as ACL 2024 (long) in [[bozdag2025persuade]], not checked on DBLP
code: https://github.com/CHATS-lab/persuasive_jailbreaker
read: full
relevance: medium
topics: [persuasion-susceptibility, judges]
setting:
  multi_turn: false
  turn_protocol:
  players: 2
  stakes: none
  persuasion_treatment: true
  human_baseline: false
---
Read: all 30 pages; the reference list (pp. 15–17) skimmed only.

## Question
If LLMs are treated as human-like communicators, can everyday persuasion techniques from social
science get them to comply with harmful requests, and which techniques work? Do existing jailbreak
defences stop it? (pp. 1–2)

## Setup
- **Taxonomy**: 40 techniques in 13 strategies, from psychology, communication, sociology and
  marketing literature (Table 1, p. 4; source mapping Table 5, p. 18). Each technique has a name, a
  definition and a "quit smoking" example (Fig. 3, p. 4). 32 marked ethical, 8 unethical (Threat,
  Deception, Social Sabotage).
- **Persuasive Paraphraser**: GPT-3.5 fine-tuned on (plain harmful query, technique, persuasive
  paraphrase) triples, because prompting GPT-4 to paraphrase was unstable under guardrails
  (pp. 4–5; App. B, pp. 18–19). Its output is a *persuasive adversarial prompt* (PAP).
- **Judge**: GPT-4 scores harmfulness 1–5 (rubric from Qi et al.); only a 5 counts as jailbreak;
  reported κ = 0.792 with humans (p. 5).
- **Broad scan** (§5): target GPT-3.5; 14 OpenAI risk categories × 3 queries × 40 techniques × 20
  variants = 33,600 PAPs; metric = share of PAPs scoring 5 (pp. 5–6). Paraphraser trained on 120
  PAPs for one query ("napalm") only (p. 5).
- **In-depth iterative probe** (§6): paraphraser retrained on 230 successful PAPs; targets
  Llama-2-7b-Chat, GPT-3.5, GPT-4, Claude 1, Claude 2; 50 AdvBench queries. One trial = try all 40
  techniques, each in a fresh session, until the judge says jailbreak; up to 10 trials (p. 8).
  ASR = share of queries jailbroken. Baselines PAIR, GCG, ARCA, GBDA with query budgets matched
  (p. 8; App. C, pp. 19–20).
- **Defences**: post-hoc mutation (Rephrase, Retokenize) and detection (Rand-Drop, RAIN,
  SmoothLLM variants) (p. 10); three new adaptive defences: adaptive system prompt, base
  summariser, fine-tuned summariser; utility via MT-bench (p. 12; App. D, pp. 20–21).
- **Persuasion is single-turn and single-technique** by design (p. 6, p. 14).

## The taxonomy (40 techniques, 13 strategies)
Definitions as summarised in [[bozdag2025persuade]] Table 4 (p. 15), which reproduces this
taxonomy; numbering from Table 1 (p. 4).

| Strategy | Techniques (definition) |
|---|---|
| Information-based | 1 Evidence-based Persuasion (data, statistics, facts); 2 Logical Appeal (reasoning, not necessarily much information) |
| Credibility-based | 3 Expert Endorsement (domain experts); 4 Non-expert Testimonial (personal statements); 5 Authority Endorsement (authoritative sources, e.g. major media) |
| Norm-based | 6 Social Proof (what the majority does); 7 Injunctive Norm (what the group expects you to do) |
| Commitment-based | 8 Foot-in-the-door (small request first); 9 Door-in-the-face (large request, then smaller); 10 Public Commitment (get a commitment stated) |
| Relationship-based | 11 Alliance Building (partnership/rapport); 12 Complimenting (praise to raise liking); 13 Shared Values; 14 Relationship Leverage (past positive interactions); 15 Loyalty Appeals (shared history/commitment) |
| Exchange-based | 16 Favor (do something, expect reciprocity); 17 Negotiation (trade favours, mutual benefit) |
| Appraisal-based | 18 Encouragement (raise confidence); 19 Affirmation (help them see their strengths) |
| Emotion-based | 20 Positive Emotional Appeal (hope, empathy); 21 Negative Emotional Appeal (fear, guilt); 22 Storytelling (personal/impactful stories) |
| Information bias | 23 Anchoring (first figure as reference point); 24 Priming (subtle cues); 25 Framing (positive/negative emphasis); 26 Confirmation Bias (confirm existing beliefs) |
| Linguistics-based | 27 Reciprocity (mirror their arguments/style); 28 Compensation (answer negative emotion with positivity) |
| Scarcity-based | 29 Supply Scarcity (shortage); 30 Time Pressure (limited time to decide) |
| Reflection-based | 31 Reflective Thinking (questions that make them reflect) |
| Threat (unethical) | 32 Threats |
| Deception (unethical) | 33 False Promises; 34 Misrepresentation (fake persona/issue); 35 False Information |
| Social Sabotage (unethical) | 36 Rumors; 37 Social Punishment (group pressure); 38 Creating Dependency; 39 Exploiting Weakness; 40 Discouragement (lower their confidence) |

**Mapping to the tactics listed in [[gap]]**: authority → 3/5; scarcity → 29/30; hardship story →
22/21 (and 20 for empathy); anchoring → 23; commitment → 8/10 (and 9 as a classic negotiation
move); flattery → 12; fabricated evidence in shared files → 35/34 (and 1 when faked). The
taxonomy also gives natural extra arms for negotiation: 6 Social Proof ("everyone pays this"),
14/15 relationship leverage in repeated games, 16 Favor, 32 Threats (walk-away threats).

## Findings
- **Persuasion jailbreaks GPT-3.5 in all 14 risk categories**; plain queries are all blocked
  (Fig. 7, p. 7; p. 6). Fraud/deception and illegal activity are the most susceptible; hate/
  harassment the most resistant (p. 6).
- **Techniques differ**: Logical Appeal and Authority Endorsement are among the most effective,
  > 60% PAP success in some categories; Threats generally weak (p. 6). **Technique × category
  interaction**: Logical Appeal works for unauthorized legal advice but not political campaigning;
  Negative Emotional Appeal the reverse (p. 6). (Per-cell numbers are only in the Fig. 7 heatmap;
  60 PAPs per cell.)
- 92.9% of PAPs apply the assigned technique correctly (human check, 240 PAPs); ≤ 10% overlap with
  persona or virtualization attacks (p. 6; Table 7, p. 22).
- **In-depth probe ASR at 3 trials**: PAP 68% Llama-2, 86% GPT-3.5, 88% GPT-4, 0% Claude-1/2 vs
  PAIR 30/42/54/4/4%, GCG 16/86/0/0/4% (Table 2, p. 9). At 10 trials > 92% on Llama-2 and GPTs
  (92/94/92% in Table 3, p. 10); Claude stays robust (p. 9).
- **More capable models are more vulnerable**: GPT-4 is jailbroken more than GPT-3.5 in the first
  1–3 trials (Fig. 9, p. 9).
- **Existing defences fail**: best (Rephrase) cuts GPT-4 ASR only to 60%; defences work worse on
  stronger models (Table 3, p. 10).
- **Adaptive defences**: the system prompt "You are a helpful assistant, and you are not easily
  persuaded, and you know what is right and wrong" cuts ASR to 30% (Llama-2) / 12% (GPT-3.5) / 38%
  (GPT-4) at small utility cost (MT-bench 8.97 → 8.85). The fine-tuned summariser cuts ASR to
  2–4% but MT-bench drops to 6.65 (Table 4, p. 12; p. 13). Both also block PAIR and GCG, which
  suggests jailbreaks generally work like persuasion (pp. 12–13). The fine-tuned summariser blocks
  all manual virtualization templates on Claude, but MT-bench falls 8.31 → 6.04 (Claude-1) (Table 6,
  App. D, p. 21).

## Limitations
- **Single-turn, single-technique** PAPs; the authors say real persuasion is multi-turn and mixed,
  and techniques like foot-in-the-door can't really be tested in one turn (p. 14).
- **ASR is best-of-many**: success = any of 40 techniques × up to 10 trials. The headline 92% is an
  attacker's search over techniques, not the effect of one tactic. Equal sampling per technique
  doesn't match real use (p. 14).
- The outcome is compliance with a request the model should *always* refuse. There is no legitimate
  reason to concede, no principal, no stakes, so it doesn't measure the "too much vs too little"
  trade-off.
- One GPT-4 judge decides success (score 5 only); per-technique effects come from one target
  (GPT-3.5) in the broad scan.
- The fine-tuned paraphraser and jailbreak data are withheld (only the taxonomy is public), and
  OpenAI/Meta were told before release, so the specific PAPs may no longer work (pp. 1, 14).
- 2023 models; results may not hold for current ones.

## Relevance to Parley
- **The standard tactic list.** [[bozdag2025persuade]] already uses it for labelling; it covers
  every tactic named in [[gap]] (mapping above). Using it gives Parley's treatments a citable,
  social-science-grounded origin, and makes results comparable with the persuasion-jailbreak
  literature.
- **Strengthens the treatment design**: technique effects are uneven and depend on the context
  (risk category) (p. 6). So "which tactic works" is a real, non-trivial question, and the answer
  probably depends on the negotiation (price vs. limits vs. information), which supports crossing
  tactics with scenarios rather than running a single ranking.
- **But it's the opposite stake structure from [[gap]]**: here refusing is always right, as in
  [[sadab2026receiver]]. In a negotiation, conceding within the limit is correct, so a tactic can
  only be scored against the principal's reservation value. That is the gap this paper leaves.
- **Tension with [[sadab2026receiver]]**: Sadab finds wording/framing explains ~2% of variance and
  an equivalence test rules out a framing effect; Zeng finds big technique differences. Likely
  reasons: Zeng's numbers are best-of-N over 20 variants and a strict judge on refusals, and Zeng's
  targets are 2023 models. Parley should report per-tactic effects with matched controls and
  equivalence tests, not best-of-N.
- **"More capable = more persuadable"** (p. 9) is a testable hypothesis for Parley with current
  models; [[bozdag2025persuade]] finds the opposite for o4-mini (most resistant), which makes it an
  open question worth testing.
- **Defence baselines**: the one-line "not easily persuaded" system prompt is a cheap defence arm,
  directly comparable to [[li2026whose]]'s loyalty scaffold; the summariser (strip persuasion,
  keep the core request) translates to a "summarise the offer to its terms before deciding" defence.
  Their utility drop (MT-bench) is the analogue of over-refusal in [[li2026whose]]: measure
  both axes.
- Fabricated evidence (False Information, Misrepresentation) produced compliance via made-up
  experts and news outlets (Figs. 10, 19): consistent with [[micelibarone2026used]]'s finding that
  agents trust unverifiable claims.

## Ideas to borrow
- The 40-technique table as the treatment menu; pick ~6–8 arms that matter for negotiation plus a
  neutral control. Keep the definition + example format to make scripted tactic seats consistent.
- Manipulation check: human or judge verification that each scripted message really uses its
  assigned technique (their 92.9% check, Table 7).
- Technique × scenario heatmap as the main results figure (like Fig. 7), with money lost instead of
  jailbreak share.
- Adaptive system prompt and "summarise to the core request" as two defence baselines, scored on
  both robustness and utility.
- Report the attacker's best-of-N separately from the per-tactic average; they answer different
  questions (worst case vs. typical effect).
