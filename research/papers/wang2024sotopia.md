---
id: wang2024sotopia
title: "SOTOPIA-$π$: Interactive Learning of Socially Intelligent Language Agents"
authors: [Ruiyi Wang, Haofei Yu, Wenxin Zhang, Zhengyang Qi, Maarten Sap, Graham Neubig, Yonatan Bisk, Hao Zhu]
year: 2024
arxiv: "2403.08715"
venue: arXiv preprint (v3, 25 Apr 2024)
code: https://pi.sotopia.world
read: full
relevance: high
topics: [negotiation-benchmarks, eval-methodology, judges, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 2
  stakes: none
  persuasion_treatment: false
  human_baseline: false
---

## Question
Can a 7B model become more socially intelligent by learning from its own and an expert's
interactions, filtered by GPT-4 ratings? Is the GPT-4 rating a usable stand-in for human
judgement when you train on it? And what does this training do to safety and general knowledge?
(RQ1–3, p. 2)

## Setup
- CMU LTI. Hao Zhu is the overall project lead, Neubig and Bisk co-advise, Sap gave feedback on
  the write-up (p. 26). Diyi Yang ([[yang]]) is **not** an author. She is cited as co-author of
  NormBank (one of the three task sources) and of Stable Alignment, which the authors call the
  closest prior work (pp. 2, 12). Hao Zhu also co-wrote [[khatua2026cooperbench]] with her lab.
- **Environment: SOTOPIA** (Zhou et al. 2024). Two characters, each with a profile and a private
  social goal. They take turns, and each turn is speak, non-verbal, physical action, none or
  leave (pp. 2–3, 16). SOTOPIA-EVAL scores 7 dimensions: believability BEL [0,10], relationship
  REL [-5,5], knowledge KNO [0,10], secret SEC [-10,0], social rules SOC [-10,0], financial/material
  FIN [-5,5], goal GOAL [0,10]. "Overall" is their mean (p. 3, fn. 1).
- **Step 1, task generation.** GPT-4-turbo writes scenarios plus two goals from keywords sampled
  from Social Chemistry, Social IQa and NormBank: 510 prompts, 462 usable tasks. The tasks are not
  filtered by hand, and the 40 SOTOPIA character profiles are reused (pp. 3–4, 15). Topics are
  "negotiation, collaboration, and competition" (p. 5). The examples are mostly mixed-motive
  persuasion between friends (road trip, apology) (pp. 14–15). Persuasion for Good and
  Deal-or-No-Deal were left out as sources (p. 14). The training tasks are guaranteed not to
  overlap with the evaluation tasks (p. 4).
- **Step 2, data.** 100 tasks per round, 10 character pairs per task (p. 5).
  - Behaviour cloning (BC): GPT-4 vs GPT-4 episodes. Keep the top 2 per task per agent, plus
    lower ranks that beat both the local and the global mean goal score (p. 15).
  - Self-reinforcement (SR): the model plays itself, and the top 20% of its episodes per task by
    GPT-4 goal score are kept. This is offline ReST/RAFT-style training without iterations, and
    it replaces ReST's threshold filtering, which "did not work well for multiple tasks" (pp. 3, 15).
- **Step 3, update.** Supervised fine-tuning on the kept turns. The filter uses **only the GOAL
  score**, since GOAL has the highest GPT-4–human correlation in SOTOPIA (p. 4). Arms: BC, SR,
  BC then SR, and SR then BC.
- **Model and compute.** Mistral-7B-Instruct-v0.1, QLoRA (r 8, α 16), 4× A6000, 20 epochs, lr 5e-5.
  The BC checkpoint is taken at epoch 20 and the SR one at epoch 5 (p. 17). Expert gpt-4-0613,
  partner gpt-3.5-turbo-0613 (p. 16).
- **Evaluation.** The trained agent plays a fixed GPT-3.5 partner on all 90 SOTOPIA tasks (180
  episodes) and on the 14 "hard" tasks (140 episodes), both judged by GPT-4 (Table 5, p. 13).
  Humans rate 28 hard-task episodes per model: Prolific, 30 qualified annotators plus 4 internal,
  2 annotators per episode, blind to which side is the target model. About 20% of datapoints were
  re-annotated after disagreement filtering (pp. 17–22). There is also a safety case study (one
  "injure a third person" task, 9 episodes per model) and MMLU (pp. 6–7).

## Findings
- **Goal completion (GPT-4 judge, all tasks):** base 5.07 → SR 5.83, BC 7.27, BC+SR 7.62, GPT-4
  expert 7.62. Overall 2.33 → 3.44 vs expert 3.31 (Table 2, p. 6).
- **Order matters:** on hard-28, BC then SR reaches GOAL 5.71, while SR then BC reaches only 3.92,
  worse than SR alone (Table 5, p. 13). Learning from the expert beats learning from oneself (p. 5).
- **Judge overestimates trained models.** On hard tasks the GPT-4-minus-human GOAL gap grows from
  0.36 (base) to 1.42 (BC+SR) (Fig. 4, p. 5). Humans put BC+SR at 4.29 against GPT-4 at 5.25. By
  GPT-4's rating the two are nearly tied (5.71 vs 5.89) (pp. 5–6). The human GOAL gain over base
  is only marginal (t = 2.07, p = 0.059), and BC+SR vs GPT-4 is not significant on any dimension
  (Table 6, p. 14). Judge–human Pearson r on GOAL falls from 0.86 (GPT-4 agent, SR) to 0.73 (BC) and
  0.58 (BC+SR) (Table 7, p. 23).
- **Other dimensions, human-rated, BC+SR minus base, hard tasks:** BEL +2.05, REL +1.91, SOC +1.11
  (all significant), overall +0.91 (significant). KNO −0.14, SEC 0.00, FIN +0.09 are not
  significant (Table 1, p. 6; t-tests in Table 6, p. 14). Training on GOAL alone produced **no
  measured cost on secret-keeping or social rules**. SEC sits near 0 for every model, so it barely
  separates models (Table 5, p. 13).
- **The partner benefits too:** when the target model improves, the fixed GPT-3.5 partner's
  human-rated GOAL also rises, from 2.98 (vs base) to 5.55 (vs BC+SR) (Table 9, p. 23). The
  authors read this as more agreements that satisfy both sides. The trained model is not winning
  at the partner's expense.
- **Safety case study:** BC+SR as would-be injurer has 100% engagement (base 22%) and a 44% injury
  rate (base and SR 100%, same as GPT-4's 44%), with 0.9 toxic words against 3.6 for base. As the
  peacekeeper it reaches 100% prevention (base 11%) and offers 2.9 alternatives (GPT-4 1.2)
  (Table 3, p. 7). BC alone and SR alone are **more** toxic than base (7.5 and 5.5) and still
  injure 100% of the time, so the safety gain shows up only in the combined arm.
- **General knowledge:** MMLU base 49.21, SR 43.46, BC 47.48, BC+SR 48.57 (Table 4, p. 7). The
  paper says this is "not subject to catastrophic forgetting", but SR alone lost ~6 points.
- **Annotator agreement:** Randolph's κ is 0.60 for GOAL and 0.58 for BEL, and 0.94–0.99 for SOC
  and SEC, because those almost always score 0 (Table 8, p. 23).
- **Secrets, qualitative:** the BC model mostly avoids the secret entirely. When it does reveal
  it, it does so explicitly. GPT-4 disguises it ("a friend of mine") (App. E, p. 25).

## Limitations
- **No single-skill arm.** Every arm trains on the same mix of negotiation, collaboration and
  competition tasks. There is no negotiation-only or persuasion-only training to compare against,
  so the paper says nothing about breadth vs specialisation.
- Results are not split by task type (negotiation vs cooperation vs competition), so transfer
  between social skills can't be read off.
- Stakes are judge-rated Likert goals, never money or verifiable payoff. The FIN dimension is
  also judge-rated.
- Trained and selected on the GPT-4 judge's GOAL score, then evaluated mostly by the same judge.
  The paper itself shows this inflates the scores (p. 5). Human evaluation covers only 28
  episodes per model, on the hard subset only (p. 13).
- One fixed, weak partner (GPT-3.5). No adversarial counterparty, no test of resisting
  persuasion, and the agent is never on the receiving end of a manipulator.
- The safety evidence is one scenario with 9 episodes per model, hand-labelled (p. 6). Offline,
  single round of SR, one 7B model, one seed. No variance across training runs is reported.
- "Held-out" here means new SOTOPIA tasks from the same generator family and character pool. It
  is not out-of-distribution transfer.

## Relevance to Parley
- **The student's hypothesis:** training on a broad set of social skills makes an agent better,
  including at negotiation, than training on negotiation alone. The weaker version: there is a
  training method that improves many social directions at once instead of trading one for
  another.
  - *Strong version:* **neutral, untested.** SOTOPIA-π trains only on a broad mix ("negotiation,
    collaboration, and competition", p. 5). It has no negotiation-only control and doesn't break
    results down by task type. So it shows broad training helps on a broad test set, which
    is the baseline the hypothesis has to beat, not evidence for it. The missing ablation
    (broad vs negotiation-only, scored on held-out negotiations with a money outcome) is exactly
    the gap.
  - *Weak version:* **mild support, with caveats.** Optimising one judge score (GOAL) also raised
    believability, relationship and social rules under human rating, with no significant loss on
    secrets, knowledge or financial benefit (Table 1, p. 6). It also improved the partner's
    outcome (Table 9, p. 23). Three caveats: (a) it holds only for BC then SR; the single arms
    were more toxic and SR lost MMLU (pp. 7, 13). (b) The human-rated GOAL gain is only marginal
    (p = 0.059). (c) SEC barely varies, so "no cost to secret-keeping" is weak evidence. None of
    this tests resistance to persuasion, which is where the trade-offs elsewhere show up.
- **Contrast with the trade-off papers.** [[li2026whose]] finds every mechanism (prompting,
  distillation, RL) moves along a leak/over-refusal frontier. [[sadab2026receiver]] finds
  persuasion fine-tuning eroded the holder's resistance (12.4% → 83.5% given away). SOTOPIA-π
  reports no trade-off, but it never puts its agent on the defending side against a manipulative
  counterparty, and its "secret" dimension is near-constant. The absence of a trade-off here may
  just mean the trade-off was never measured.
- **Against [[bozdag2025persuade]]:** that paper measures persuader and persuadee separately.
  SOTOPIA-π trains only the persuading or goal-seeking side, so its "more persuasive" finding
  (Table 3, p. 7) says nothing about susceptibility.
- **Against [[liu2026instructing]] and [[bergemann2026training]]:** those train negotiation alone
  with verifiable money rewards (RLVR/GRPO, SFT then RL). SOTOPIA-π trains broad social skills
  with a judge reward and offline filtered SFT. The student's comparison sits between the two:
  broad versus negotiation-only training, scored on the verifiable negotiation outcome those
  papers use. Both camps find SFT/BC first, then self-improvement, works best (BC+SR here,
  p. 13).
- **Judge warning for any Parley training loop:** optimising against an LLM judge widened the
  judge–human gap from 0.36 to 1.42 and dropped the judge–human r to 0.58 (pp. 5, 23). This is
  a concrete argument for verifiable (money) rewards in Parley, as in [[li2026whose]]'s judge
  fragility.

## Ideas to borrow
- The BC-then-SR pipeline as a cheap baseline: GPT-4-quality episodes, then the model's own top
  20% per task. Run it once on a broad social mix and once on negotiation only, with matched
  token counts. That is the student's ablation.
- Score the **partner's** outcome as well as the agent's (Table 9) to tell joint-value creation
  apart from extraction.
- Report the per-dimension change with significance (Table 1/6 style) to show whether gains on
  one axis cost another. Add a resistance/susceptibility axis that SOTOPIA lacks.
- Track judge–human correlation separately **per trained arm** (Table 7), not just once for the
  benchmark. Optimisation pressure is what breaks it.
- Generate held-out tasks from disjoint seed prompts (p. 15), plus a check on general ability
  (MMLU) for forgetting.
