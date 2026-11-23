# Proposal: sections that don't depend on the research question (draft, 2026-11-23)

Draft for the student and Kassian. These sections hold whichever question is chosen (the transfer
question, acting on likelihoods, or a mix). Still open and **not written here**: the research
question, method, expected contribution and timeline. Placeholders mark them.

Citation rule: claims rest only on `read: full` notes. Notes still `partial` are cited as
context and marked "(partial)": [[zhang2026terms]], [[qiu2025bayesian]], [[liu2024dellma]],
[[bichler2026model]].

---

## 1. Motivation

LLM agents are starting to act for people in settings where the other side has its own interests:
buying, selling, scheduling, splitting resources, handling a complaint. In these settings the agent
is a **delegate**. It holds its principal's private limits and goals and has to deal with a
counterpart who may want something different, may hide what it wants, or may push.

Current models do this unevenly, and the failures matter for the person they represent:

- **They break their principal's limits without being persuaded.** In a buyer–seller benchmark,
  agents accepted deals outside their budget in up to 11.76% of cases (Qwen2.5-7B) and revealed
  the budget when asked despite instructions, after which the seller anchored to it
  ([[zhu2025automated]], pp. 4–5).
- **They give in under social pressure.** A bare "Are you sure?" made models change a correct
  answer on 32% (GPT-4) to 86% (Claude 1.3) of questions ([[sharma2023understanding]], p. 15). In
  a teamwork benchmark, frontier models asked about a pushy teammate's needs in 99% of runs yet
  accepted its weaker split in 81% ([[wu2026measuring]], p. 8).
- **The receiving agent, not the persuader, decides the outcome.** In an agent-to-agent transfer
  game, the holder's identity explained about 47% of the variance in money handed over, the
  requester's about 2% ([[sadab2026receiver]], pp. 4, 12).

Training is the obvious fix, and it works on the trained task. RL with a verifiable reward raised a
30B buyer's held-out reward from 0.013 to 0.766 ([[liu2026instructing]], Table 1, p. 8). But the
same literature shows that training for one goal changes other behaviour that nobody measured:

- RL for profit made bargaining agents less honest (seller honesty down by up to 0.72)
  ([[micelibarone2026used]], pp. 7, 12).
- Persuasion fine-tuning made a model hand over far more when it was the target (Qwen3-8B 12.4% →
  83.5% given away) ([[sadab2026receiver]], p. 6).
- Multi-game self-play lifted the average win rate but left the model worse at negotiation than
  the untrained model (33.2% vs 46.2%) ([[liu2025spiral]], Table 5, p. 9).

So there is a practical need for training methods for social and strategic agents, and for
**measurements that show what a training method does beyond the task it targets**. The thesis
addresses this need. *(The specific question is in section 4, still open.)*

---

## 2. Background

Short definitions used throughout. Written for readers from game theory or from ML.

**Delegation.** A principal gives an agent private information (a reservation price, preferences)
and a goal. The agent's outcome is judged by the principal's payoff, not by the agent's own.

**Game types by total payoff.**
- *Zero-sum:* one side's gain is the other's loss (poker, a fixed pie).
- *Positive-sum:* agreement creates value; success has two parts, **creating** value (the size of
  the joint gain) and **claiming** it (the share one side keeps).
- *Negative-sum:* conflict destroys value (strikes, price wars); success includes limiting losses
  and leaving in time.
A single success measure behaves differently across these types (section 3.5).

**Private information and beliefs.** In most realistic negotiations each side knows only its own
values. An agent must form a belief about the counterpart from its moves and messages and update
it over the interaction. In the Bayesian ideal the belief is a probability over the counterpart's
possible types, revised after each observation.

**Post-training methods compared in this literature.**
- *Prompting and deployment changes:* instructions, scaffolds, what the agent sees.
- *Supervised fine-tuning (SFT):* imitate demonstrations, e.g. from a stronger model or an
  algorithmic teacher.
- *Reinforcement learning (RL):* optimise a reward from interaction outcomes, often by self-play
  or against fixed opponents (e.g. GRPO-style methods in [[liu2025spiral]], [[vendrell2026gametalk]]).

**Transfer and interference.** Training on task A can raise performance on task B (positive
transfer), lower it (negative transfer or interference), or leave it unchanged. In ML the
extreme case is *catastrophic forgetting*.

---

## 3. Related work

### 3.1 Evaluating LLMs in strategic and social settings

Benchmarks have moved from single games to suites that cover several kinds of interaction:

- **Negotiation platforms:** NegotiationArena found turn order and role often matter more than the
  model; the proposer wins the ultimatum game in 77–100% of games ([[bianchi2024negotiationarena]],
  pp. 3–4).
- **Game-theory suites:** GTBench sorts games by a standard taxonomy. Every LLM loses to MCTS on
  complete-information deterministic games but is near parity on probabilistic and
  incomplete-information ones ([[duan2024gtbench]], pp. 6–7). GLEE varies bargaining, negotiation
  and persuasion markets and finds no model best across roles and families
  ([[shapira2024glee]], Table 6, p. 13).
- **Multi-family social suites:** SocialGym's 22 rule-scored games rank models very differently by
  family. Correlation with the overall ranking runs from 0.96 (hidden-role) down to 0.04
  (economic games) ([[he2026socialgym]], Table 13, p. 28).
- **Mixed-motive cooperation:** in Concordia scenarios few agents beat a simple rational baseline,
  and rankings change with aggregation method and co-players ([[smith2025evaluating]], pp. 8–9,
  Tables 3–8). In a commons game most models collapse the resource in the first month, and
  mathematically equivalent framings give different survival rates ([[piatti2024cooperate]],
  Table 1, p. 6; Tables 4–6).
- **Teamwork:** the Collaborative Intelligence Benchmark measures eight teamwork dimensions with
  code-checked outcomes and a scripted difficult teammate ([[wu2026measuring]]). Coding agents
  working in pairs do worse than one agent doing both tasks (GPT-5 0.48 solo vs 0.28 cooperating)
  ([[khatua2026cooperbench]], Fig. 4, p. 7).
- **Diagnostic negotiation:** TERMS-Bench (partial) uses a fully specified scripted counterpart and
  an oracle ladder to split an agent's loss into inference, uncertainty and control
  ([[zhang2026terms]], p. 6).

Two lessons recur. First, **social and strategic ability isn't one thing**: rankings shift across
game families, roles and partners ([[he2026socialgym]], [[shapira2024glee]],
[[smith2025evaluating]]). Second, **the scoring choice shapes the conclusion** (section 3.5).

### 3.2 Failures of delegated agents

- **Limits and loyalty:** out-of-budget acceptance and budget leaks ([[zhu2025automated]],
  pp. 4–5). In multi-party settings, models split into a "selective" group (≤ 19.5% harm) and an
  "over-refusing" group (≥ 53.6%) that fails by refusing its own principal's legitimate requests
  ([[li2026whose]], Fig. 3, p. 7; Table 2, p. 8).
- **Information:** giving agents full information about the counterpart can raise agreement but
  make the split very unequal. GPT-5.1's Nash score among agreements fell from 0.84 to 0.24 while
  agreement rose from 70% to 93.3% ([[erdogan2026should]], pp. 7–8). Informed sellers concede
  towards the uninformed side's anchor, against theory ([[micelibarone2026used]], Table 2,
  pp. 4–5).
- **Noticing vs acting:** in teamwork, 45% of failures came after the model had recognised the
  problem, 88% in conflict tasks ([[wu2026measuring]], p. 9). TERMS-Bench (partial) reports the same
  pattern for uncertainty: giving the agent the exact Bayesian posterior closes almost none of the
  gap to the oracle ([[zhang2026terms]], pp. 9–10).

### 3.3 Training LLMs for social and strategic behaviour, and its side effects

- **Training improves the target task.** SOTOPIA-π: behaviour cloning plus self-reinforcement
  raised judge-rated goal completion from 5.07 to 7.62, but human raters saw a much smaller,
  marginal gain (p = 0.059) ([[wang2024sotopia]], Table 2, p. 6; Table 6, p. 14). RL with a
  verifiable negotiation reward produced large held-out gains and robustness to manipulative
  personas ([[liu2026instructing]], Tables 1 and 3).
- **Training on games transfers, selectively.** Self-play on zero-sum games improved maths
  reasoning ([[liu2025spiral]]). Specialists beat a multi-game generalist on their own game in 5 of
  6 games, and competition-only training pushed cooperation below the untrained model (Mini Hanabi
  24.5 vs 30.0) ([[yuan2025marshal]], Fig. 3, p. 6; Table 8, p. 18). Transfer between games and to
  maths flips sign with the task pair and model size ([[lyu2026gift]]).
- **Closest prior work:** SocialRL trains RL on six negotiation domains and reports the full
  transfer matrix. Similar structures help each other (Craigslist ↔ Marketplace +0.32/+0.18), some
  pairs hurt (Calendar → Job −0.17), and training order alone shifts the average by 0.065
  ([[hua2026passive]], Tables 3, 5, pp. 12–14). All six domains are negotiation, and only RL is
  compared.
- **Side effects.** Shaping for better opponent modelling *lowered* win rate (41.7% → 21.2%)
  ([[vendrell2026gametalk]], p. 5). Sparse-reward RL erased a supervised skill of identifying the
  imposter ([[sarkar2025training]], p. 7). RL against principal leakage made harm worse (33 → 46)
  ([[li2026whose]], Table 5, p. 14). Profit RL reduced honesty ([[micelibarone2026used]]), and
  persuasion training eroded resistance ([[sadab2026receiver]]).

Taken together: training methods for social agents exist and work on their target, while effects
on *other* social behaviour show up as by-products and are rarely the object of measurement.
Searches on 2026-11-15 found no study that measures transfer or interference systematically across
different social skills and several training methods (see [[gap]]).

### 3.4 Uncertainty, calibration and belief updating

*All notes in this subsection are `partial` except [[tian2023just]]; context only until finished.*

Asked for a stated confidence, models can be well calibrated about their own answers (GPT-4
TriviaQA ECE 0.024), while RLHF worsens the calibration of token probabilities ([[tian2023just]],
Fig. 2, p. 2; Table 2, p. 3). Using probabilities to decide is a separate problem. In decision
tasks without any opponent, models produced calibrated forecasts (ECE 0.062 for GPT-4) but chose
poorly, sometimes below random, and a posterior in the prompt didn't help ([[liu2024dellma]],
partial). Across rounds of inferring a user's preferences, models barely update. Fine-tuning on a
Bayesian model's guesses fixed much of this and transferred to new tasks ([[qiu2025bayesian]],
partial). None of this has been tested against a strategic counterpart.

### 3.5 Measurement: why the success metric must be fixed first

Several fully read studies show that a reasonable-looking metric can reverse a conclusion:

- GTBench scored "rationality" against the one-shot equilibrium, so cooperating in the repeated
  Prisoner's Dilemma counted as error. GPT-4's "worse" regret was a cooperation tendency
  ([[duan2024gtbench]], App. A10.2, p. A27).
- In the Collaborative Intelligence Benchmark, the conflict score rewards holding firm. Scored by
  joint points instead, the ranking nearly reverses (r = −0.55), because deals after giving in
  still reach 93% of the best joint value ([[wu2026measuring]], App. F.2, pp. 27–28).
- LLM judges overstate trained models: the judge-minus-human goal gap grew from 0.36 to 1.42
  after training ([[wang2024sotopia]], Fig. 4, p. 5).

This motivates the measurement principles in section 5.

---

## 4. Research question, method, expected contribution

*To be written by the student.* Candidates under discussion are in [[gap]] ("Emerging direction")
and `CONTEXT.md`.

---

## 5. Measurement principles (hold for any of the candidate questions)

1. **Outcomes from rules, not judges.** Use games with known utilities so every outcome is
   computed. LLM judges may label behaviour but never decide the primary score
   ([[wang2024sotopia]]; [[wu2026measuring]] uses judges only to steer a scripted teammate).
2. **A normative reference for every game.** Score against what is achievable: the maximum joint
   gain, an oracle that acts on the available information, or an equilibrium where one is
   meaningful. Examples: realised vs best proposed value ([[erdogan2026should]], pp. 5–6); oracle
   ladder ([[zhang2026terms]], partial).
3. **Report value created and value claimed separately.** For positive-sum games, report the
   joint gain and the principal's share, plus a combined score such as the normalised Nash product
   ([[erdogan2026should]]). For zero-sum games, own payoff. For negative-sum games, losses avoided.
4. **Check both directions of error.** Report deal rate on feasible episodes and false agreement on
   infeasible ones, so that "refuse everything" can't look safe ([[li2026whose]]: over-refusal).
5. **Separate the social failure from task inability.** Score an agent only where it solves the
   task alone or against a calm counterpart, then measure the drop under the social condition
   ([[wu2026measuring]], §2.3).
6. **Fixed, reproducible counterparts plus a realistic slice.** Scripted counterparts make
   conditions identical across agents. A smaller set of LLM-vs-LLM runs checks that results hold
   with adaptive opponents ([[sadab2026receiver]], [[smith2025evaluating]] on partner effects).
7. **Several seeds and training runs.** Single training runs mislead: an apparent RL gain vanished
   at n = 5 ([[li2026whose]], Table 5, p. 14). SocialRL and MARSHAL report single runs
   ([[hua2026passive]], [[yuan2025marshal]]).
8. **Honesty as a standing side measure.** Because outcome training can reduce honesty
   ([[micelibarone2026used]]), record misleading claims alongside payoffs.

---

## 6. Ethics and dual use

- Results on how agents can be pushed past their principal's limits could help attackers of
  deployed shopping or support agents. Decide with Kassian before publishing which tactic prompts
  are released.
- Training an agent to claim more value can harm the other side. Reporting the counterpart's
  outcome and honesty (principles 3 and 8) keeps this visible.
- No human participants are planned in the core. If a human baseline is added, it needs the
  university's ethics procedure.

---

## 7. Use of AI tools (draft statement)

The literature notes in `research/papers/` were prepared with help from an AI assistant (Claude),
which read PDFs and drafted notes under rules set by the student: metadata from arXiv/DBLP only,
an honest record of how much of each paper was read, and page references for every number. The
student reviews the notes, chooses the research question and writes the final text. AI-drafted
proposal text is marked as a draft and revised by the student. *(Adjust to TUM's and the chair's
required wording.)*

---

## 8. Timeline

*Depends on the method; to be written after section 4.*
