---
id: liu2026paying
title: "Paying Less Generalization Tax: A Cross-Domain Generalization Study of RL Training for LLM Agents"
authors: [Zhihan Liu, Lin Guan, Yixin Nie, Kai Zhang, Zhuoqun Hao, Lin Chen, Asli Celikyilmaz, Zhaoran Wang, Na Zhang]
year: 2026
arxiv: "2601.18217"
venue: arXiv preprint (v1, 26 Jan 2026)
code: none linked in the paper
read: full
relevance: high
topics: [eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 1
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

Read all 22 pages (main text pp. 1–12, references pp. 13–15, appendices A–C pp. 16–22) on
2026-11-23. Meta Superintelligence Labs / FAIR, Northwestern. Single agent acting in text
environments (no other agents), so `players: 1`; turns alternate agent action / environment
observation, so `turn_protocol: strict`.

## Question
Generalist agents are post-trained on a narrow set of environments but deployed in broader,
unknown ones. Which properties of an RL training environment, and which modelling choices, best
*preserve* performance on domains never seen in training? (pp. 1–2) The authors stress
**cross-domain** generalization (different tools, states, goals), not held-out tasks in the same
domain, and frame the work as prevention: in their pilots, out-of-domain (OOD) scores fell while
in-domain scores rose during RL (p. 2).

## Setup
- Four text environments: WebShop (shopping), Sokoban (grid puzzle, coordinates as text), ALFWorld
  (household), SciWorld (lab tasks) (Table 1, p. 2; §4.1, p. 5).
- Train with GRPO on **one** environment, evaluate on the other three; 150 steps, success rate
  averaged over the last four checkpoints (steps 105–150), **3 seeds** (p. 5).
- Base model Llama-3.1-8B-Instruct. Two start points: Ckpt V1 = 20 RL steps on WebShop; Ckpt V2 =
  SFT warm-up ("mid-training") on SciWorld expert data plus self-generated ALFWorld/WebShop data,
  ratio 19:3:1 (§4.2, pp. 5–6; App. A.5, p. 17).
- Reward 10 for success, 0 for failure, −0.1 per invalid action; group size 8, KL coefficient 0.01,
  8 A100 GPUs (App. A, pp. 16–17).
- Two environment measures: **state information richness** = average characters per state;
  **planning complexity** = average trajectory length under Ckpt V2, failures counted as the
  50-step cap (p. 7).
- "OOD Ranking Score" = sum of a training domain's ranks across unseen domains, lower is better
  (Table 3, p. 6).
- Intervention: **state information augmentation**: insert goal-irrelevant text (distractor
  objects, ads, unreachable grid cells) into observations; reward and transitions unchanged; volume
  ε tuned upward until in-domain success drops; applied to 50% of trajectories for Ckpt V2 (§6,
  pp. 8–9; App. C, pp. 21–22).

## Findings
- **RL raises in-domain success and lowers OOD success** (Table 2, p. 6). E.g. Ckpt V1 trained on
  ALFWorld: +47.2 in-domain, WebShop 34.4 → 15.2. Ckpt V1 trained on WebShop: ALFWorld 25.8 → 10.8.
- **What predicts OOD robustness is structure, not realism or surface similarity.** Domains high
  on both richness and planning complexity preserve most: SciWorld (rank score 3) and Sokoban (5)
  vs WebShop (6) and ALFWorld (8) (Table 3, p. 6). The abstract grid puzzle Sokoban transfers
  better to realistic SciWorld than realistic ALFWorld does (p. 8).
- **Not just "learned less"**: training Sokoban and SciWorld longer, until their in-domain gain
  matches or exceeds ALFWorld/WebShop (Sokoban +68 after 300 steps), keeps their OOD rank (Table 4,
  p. 8).
- **Adding irrelevant information to the state improves OOD performance** with in-domain success
  roughly unchanged. Aggregate OOD change, Ckpt V1: WebShop +35.5%, Sokoban +42.5%; Ckpt V2:
  ALFWorld +7.0%, WebShop +33.4%, Sokoban +5.7% (Table 5, p. 9). For Ckpt V1 ALFWorld the table
  gives +32.6% while the text says +7.0% (p. 9), apparently a copy of the V2 value; the table is
  likely right.
- **SFT warm-up protects covered domains and hurts uncovered ones.** With warm-up, OOD drops on
  covered domains shrink (Sokoban-trained, WebShop eval: −56.4% → −11.2%), but the uncovered domain
  Sokoban suffers (WebShop-trained, Sokoban eval: +2.4% without warm-up → −36.2% with it) (Table 6,
  p. 10).
- **Step-by-step reasoning preserves OOD performance but doesn't help in-domain.** Disabling
  thinking: ALFWorld-trained Ckpt V2 on WebShop 30.5 → 1.0; OOD change −234.2% (ALFWorld), −216.5%
  (Sokoban), −216.9% (SciWorld) (Table 7, p. 11). In-domain can even rise without thinking (ALFWorld
  73.0 → 77.0, p. 11). Authors' reading: reactive policies learn brittle domain-specific shortcuts
  (p. 11). One exception: WebShop-trained Ckpt V1 does slightly better OOD without thinking
  (+16.9%, Table 7).

## Limitations
- Four environments, so the two "factors" rest on a correlation over four points; the authors call
  the evidence "indicative rather than conclusive" and the characterization "relatively ad hoc"
  (p. 8). Only richness is tested causally; planning complexity is not manipulated (p. 8).
- One model (Llama-3.1-8B-Instruct), one RL algorithm (GRPO), single-domain training only (no
  mixtures) (§4, §8).
- Richness is measured as character count, which works only because all four domains are compact
  (p. 7).
- Ckpt V1 and V2 differ in more than SFT warm-up (V1 also had 20 WebShop RL steps), so the warm-up
  comparison is not fully clean (§4.2).
- Single agent, no other parties: no social or strategic interaction. Rewards are binary task
  success.
- No variance or CIs reported in the tables despite 3 seeds.

## Relevance to Parley
- **The deployment argument for the motivation, stated by an industry lab:** generalist agents are
  post-trained narrowly and deployed broadly, and RL on one environment costs performance on others
  (the "generalization tax"). Same logic as [[fan2026commerce]] (one agent, many skills) and
  [[he2026socialgym]] (rankings shift across families), but for training. Their stated scope
  excludes multi-agent settings, so social and strategic transfer stays open ([[gap]]).
- **Structure over surface** matches the SocialRL finding that structurally similar negotiation
  tasks help each other ([[hua2026passive]]), and suggests a testable prediction for social skills:
  training environments with richer states and longer, contingent interactions should transfer
  better than short, simple ones, whatever their realism.
- **Three training-design variables to borrow for a transfer study**: state richness (and
  distractor augmentation), SFT warm-up coverage, and reasoning on/off. Each changed OOD results
  by large margins with in-domain scores nearly flat, so in-domain scores alone can't choose a
  training recipe.
- The SFT warm-up result is an interference result: consolidating some domains made an uncovered
  one more fragile. That's the trade-off structure the transfer question is about.

## Ideas to borrow
- Train on one domain, evaluate on all others, with 3 seeds and averaging over late checkpoints.
- An OOD summary (rank score, relative OOD change vs a baseline policy) next to in-domain change.
- Test "learned more → forgot more" by training longer until in-domain gains match, then compare OOD.
- Distractor augmentation as a cheap treatment: in negotiation, irrelevant chit-chat, ads or
  off-topic facts in the counterpart's messages, with offers and payoffs unchanged.
- Reasoning on/off as a factor in any RL arm.
