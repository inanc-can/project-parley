---
id: he2026socialgym
title: "SocialGym: Evaluating LLM Social Intelligence through Verifiable Multi-Agent Games"
authors: [Keyu He, Xuhui Zhou, Maarten Sap]
year: 2026
arxiv: "2608.09128"
venue: arXiv preprint (v2, 9 Nov 2026)
code: https://github.com/Keyu-He/Social_Gym_Spartan
read: full
relevance: high
topics: [game-theoretic-evals, negotiation-benchmarks, eval-methodology, judges, persuasion-susceptibility]
setting:
  multi_turn: true
  turn_protocol: strict
  players: many
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Read all 31 pages (main text pp. 1–10 and appendices A–N, pp. 13–31) on 2026-11-15. The arXiv v2
title is the one above; the paper's method is called SPaRTan (the repo name keeps "Spartan").
Turns follow a per-phase FSM scheduler that is round-robin, random or simultaneous, so
`turn_protocol: strict` is approximate; players range from 2 to 6 per game.

## Question
Can a suite of social games with **rule-decided outcomes** (no LLM judge) measure LLM social
intelligence across many kinds of interaction (cooperation, coordination, negotiation, bluffing,
hidden-role deduction, coalitions) and on every side of a game? Do rankings agree across game
families? And can an inference-time method (a playbook written from self-play) improve play?
(pp. 1–2)

## Setup
- CMU (Sap's group, the SOTOPIA lab; Xuhui Zhou is the SOTOPIA first author). The engine extends
  the SOTOPIA loop to N agents with an FSM per game, LiteLLM backends, and public / team / private
  message visibility (§3.2 p. 4; App. F pp. 16–19).
- **22 games in 5 families** (Table 6, p. 23; Fig. 1, p. 2):
  - *Normal-form (6)*: Prisoner's Dilemma, Chicken, Battle of the Sexes (with pre-play talk),
    Stag Hunt (4 players), Minority Game (5), Rock-Paper-Scissors; iterated 5–12 rounds, no
    communication except BoS.
  - *Economic (4)*: Public Goods (4), Centipede, Bargaining (iterated ultimatum over 10 tokens,
    structured offers, **no free text**), Bohnanza (4-player free-form card trading).
  - *Bluffing (4)*: Liar's Dice, Skull, Coup, Sheriff of Nottingham (free-form bribes).
  - *Hidden-role deduction (6)*: Chameleon, Insider, Spyfall, Undercover, Resistance (Avalon-like),
    Werewolves (Seer, Witch); 4–6 players in two teams, free-form dialogue.
  - *Social strategy (2)*: Survivor (jury vote), Dead Last (elimination + 3-way prize split);
    6 players, alliances and persuasion.
  - Skill tags overlap: Strategic 8, Deception 10, ToM 11, Persuasion 5, Negotiation 5,
    Coordination 3, Probabilistic 2 games (Table 5, p. 17). Several commercial games are simplified
    (e.g. Sheriff reduced to an honest/smuggle choice, Dead Last needs a strict majority) (App. K
    pp. 22–23).
- **Verification**: every game ends with a rule-computed score per agent; no LLM judge in the
  primary score (§3, pp. 3–4; App. F p. 17). Four cooperation/coordination games (BoS, Stag Hunt,
  Public Goods, Centipede) are **reported as pairwise win rates, not Elo**, and the win rate is a
  within-episode score comparison, i.e. still relative standing, not joint success (App. C p. 14).
- **Tournament**: round-robin cross-play, no self-play; each model plays 54 episodes per game
  (56 Coup/Skull, 90 Dead Last), 4,588 episodes in total, ~3,700 pairwise outcomes per model; each
  cross-model pair in an episode is a battle (higher score wins, tie = 0.5); regularized
  Bradley–Terry Elo with 1,000-sample bootstrap CIs (§3.3–4, pp. 4–5; App. C p. 14). Ratings per
  game, per family, per skill tag, per structural axis and per side (majority "Main" vs minority
  "Alt") in hidden-role games.
- **Models (10)**: GPT-5-mini, GPT-4o, GPT-4o-mini, Gemma3-27B/12B/4B, Qwen3-32B, Qwen3-4B-Instruct-
  2507, Qwen2.5-3B, Qwen3-1.7B (Qwen3 thinking off); JSON action replies, unparsable reply = no
  action (App. B pp. 13–14). No frontier Claude/Gemini/large-reasoning models, no humans.
- **Extra analyses**: SOTOPIA-EVAL judge (Qwen3.8-27B) on every seat for agreement checks (App. D);
  six outside benchmarks (MMLU-Pro, GPQA, ToMBench, FANToM, ConfAIde, PrivacyLens) (§4.2); a
  uniformly random player as anchor (App. L.4); a discussion-removal experiment (App. L.5).
- **SPaRTan (Self-Play and Reflect-Transfer)**, training-free (§5 p. 8; App. H pp. 19–20): the
  model plays N=10 self-play games, reads all trajectories (with every role's hidden moves) and
  writes a first-person "strategy playbook" (1,062–1,511 words) that is prepended to its prompt.
  Variants 1→1 (playbook per target game), (n−1)→1 (from all other games, i.e. cross-game
  transfer), n→n (one pooled playbook), plus iterated rounds R2–R4. Baselines: generic game
  advice, everyday social advice, 2 winning trajectories in context, Self-Refine playbook (rules
  only), Reflexion (lesson after each loss) (App. I pp. 20–22).
- SPaRTan is evaluated **only for GPT-5-mini and Qwen3-32B, only on Werewolves, Spyfall and
  Resistance, only in self-play** (armed side vs the same model without text), 60 deals per game
  and side, paired with vanilla; metric ΔElo from win rates, paired-bootstrap CIs (p. 8).
- **Cost**: ~$630 API in total (tournament ~$170, SPaRTan ~$300); open models and judge on local
  GPUs (Table 16, p. 31).

## Findings
- **Overall leaderboard** (18 competitive games): GPT-5-mini 1122 (win 68.5%), GPT-4o 1066,
  GPT-4o-mini 1019, Gemma3-27B 1019, Qwen3-32B 1008, Gemma3-12B 997, Gemma3-4B 955, Qwen3-4B 953,
  Qwen2.5-3B 934, Qwen3-1.7B 922 (Fig. 2, p. 4). 38 of 45 pairs separated at 95% (App. E p. 15).
- **No model best everywhere**: Qwen3-1.7B (last overall) is first on Sheriff, Insider and the
  Minority Game (p. 5). In Sheriff, Qwen3-1.7B and Gemma3-4B rarely smuggle (2%, 6%) and inspect
  most bribed bags (84%, 64%) (Table 11, p. 27).
- **Rankings shift across families** — Spearman with the overall ranking: hidden-role 0.96, social
  strategy 0.85, normal-form 0.55, bluffing 0.47, **economic 0.04**; between families: hidden-role
  vs social strategy 0.88, economic vs others 0.02–0.31 (Fig. 4, p. 6; Table 13, p. 28). Split-half
  reliability: normal-form 0.89, economic 0.68, bluffing 0.90, hidden-role 0.94, social strategy
  0.55 — so the normal-form, bluffing and economic reorderings exceed what noise would allow (p. 28).
  Hidden-role games supply 43% of episodes and alone reproduce the overall ranking (Spearman 0.96,
  42 of 45 pairs) (App. E p. 15) — the overall score is largely a hidden-role score.
- **Negotiation is the most compressed skill**: the nine models below GPT-5-mini lie within 27 Elo
  on the Negotiation tag, no pair separated (p. 15; Table 5 p. 17: 976–1003 vs GPT-5-mini 1107). The
  two economic games separate only GPT-5-mini from the rest (p. 15).
- **Sides diverge**: in hidden-role games the minority-minus-majority Elo gap exceeds 100 in 37 of
  60 (model, game) cells, median 190 (App. M p. 29). Resistance: GPT-5-mini −220 (best Resistance
  1296, mid Spy 1076), Qwen2.5-3B +447 (Spy 1050, Resistance 603) (Fig. 3, p. 5). Deceiving and
  detecting are different abilities whose direction differs by model.
- **Cross-play vs self-play differ**: GPT-5-mini's Werewolves win 89% vs other models but 37% in
  self-play (App. M.2 p. 30; Table 15).
- **Structural axes**: Elo spread grows with horizon (SD 26 single-round, 53 fixed-round, 89
  open-ended); the six strongest models gain from complete info → hidden roles, the four ≤4B models
  lose (e.g. Qwen3-1.7B 959 → 857) (App. E p. 16).
- **Outside benchmarks**: overall and hidden-role Elo correlate with MMLU-Pro/GPQA/ToM benchmarks
  at 0.75–0.90; normal-form and economic Elo far less (economic 0.04–0.09 with MMLU-Pro/GPQA/
  ToMBench) (Fig. 5, p. 6). Rule-measured secret keeping correlates with FANToM (0.85, 0.91) and
  PrivacyLens (0.76, 0.65) more than MMLU-Pro/GPQA (0.34–0.51) (p. 6; Fig. 18 p. 29).
- **Judge agreement**: SOTOPIA-EVAL (Qwen3.8-27B) agrees with the rule outcome in 92.5% of 15,501
  within-episode pairs (81.0% without the goal dimension), model-level Spearman 0.98 with Elo
  (0.95 without goal) — but the judge sees the game outcome in the transcript (App. D p. 14).
- **Behaviour**: strong models keep the secret word out of clues but name it in discussion (GPT-5-
  mini 70%, GPT-4o 96% of Chameleon games); a caught Chameleon then guesses the word 63% vs 15%
  (p. 7). Nine of ten models are not reliably above chance at voting for hidden opponents in at
  least one hidden-role game; Qwen3-1.7B's Werewolf votes 16% vs 43% chance (p. 7; Tables 7–8,
  p. 24). Bargaining: GPT-5-mini accepts 81% of below-half offers (wins 56%), GPT-4o rejects 78%
  (wins 76%); accepting more below-half offers correlates with winning less (Spearman −0.57)
  (p. 26) — the score is relative standing, so absolute-payoff-maximizing looks like weakness.
  Bohnanza: 76% of swaps help neither player; trades vs coins Spearman 0.05 (p. 26). GPT-5-mini is
  most persuasive: 74% of others' votes follow its first call (p. 25).
- **Random anchor**: median model is +205 Elo above random in hidden-role, +99 economic, only +10
  normal-form; Gemma3-12B (−97) and Qwen2.5-3B (−68) fall below random on normal-form (p. 26).
- **Discussion matters**: removing discussion in Werewolves drops villager accuracy 53 → 40%
  (random 41%) and GPT-5-mini villager wins 96 → 30%; a private reasoning turn recovers little
  (22%); Dead Last agreed splits 40 → 2% (App. L.5 pp. 27–28; Fig. 17).
- **Prompting baselines don't help**: generic advice, Self-Refine and Reflexion change average Elo
  by −18 to +19 with CIs spanning zero, except GPT-5-mini's Self-Refine playbook at **−157**
  (bad advice: probe votes, Spies failing every shared mission → Spies win 2%) (pp. 8–9).
- **SPaRTan gains are narrow**: 1→1 playbook +51 Elo for GPT-5-mini (95% CI [16, 90]; alt +76,
  main +26), mostly from Werewolves (wolf win 37 → 67%), little in Spyfall/Resistance; Qwen3-32B
  +22 [−9, 55] (Fig. 7–8, p. 8). **Cross-game transfer fails**: (n−1)→1 −13 (GPT-5-mini) and −45
  (Qwen3-32B); pooled n→n −25 and −21, with the majority side losing 97 and 82 Elo (p. 9). Later
  reflection rounds R2–R4: 0 to +19, below R1 (p. 9; Fig. 14 p. 21).
- **Stability**: a random 20% of episodes reproduces the ranking at 0.94; early/late deals 0.88;
  model ratings move 8 Elo on average when refit vs different opponent groups (App. L.6 p. 28).
  94.9% of 155,971 calls usable as written (0.6% unusable for GPT-5-mini, 11.1% Qwen3-1.7B) (p. 28).

## Limitations
- **No training is evaluated**: authors say they "do not evaluate methods that update model
  weights" and leave RL on verifiable game outcomes to future work (pp. 9–10). So nothing here says
  whether training on one family transfers to or interferes with another.
- SPaRTan covers 2 models × 3 hidden-role games in self-play only (p. 10); the "transfer" variants
  are prompt-level transfer of written advice, not of learned skill.
- **Everything is scored as relative standing** (who beat whom within an episode). Cooperative
  games are win rates of score comparisons, "rather than the frequency of a jointly successful
  episode" (App. C p. 14); no joint surplus, deal rate, Pareto efficiency or welfare measure.
  Negative-sum situations exist only implicitly (Bargaining rejection, Dead Last no-split).
- Negotiation coverage is thin: Bargaining has no free text, Bohnanza and Sheriff are simplified;
  the negotiation tag barely separates models (p. 15). No price-negotiation with reservation
  values (unlike [[zhang2026terms]]).
- Measures **capability, not propensity**: no measure of whether a model *chooses* to deceive,
  leak or cooperate when it is not instructed by role; in-game deception does not count as a
  social-rule violation (Fig. 10, p. 15).
- Uneven family weights (hidden-role 43% of episodes) drive the overall score; economic and social
  strategy families have only 2 competitive games each and low reliability (0.68, 0.55) (p. 9).
- Small/mid models only (≤32B open, three OpenAI models); no humans; Elo is relative to this
  pool and the random anchor (p. 9). Correlations are across only 10 models.
- Several game rules were altered from the published versions (App. K).

## Relevance to Parley
- **Closest existing multi-direction benchmark** for the student's idea: one engine, 22 games,
  every side, rule-verified outcomes, family- and skill-tag profiles, open code, and cheap
  (~$170 for the full leaderboard, p. 31). It directly shows that **social "directions" are
  measurably distinct**: family rankings correlate 0.02–0.88, economic vs overall 0.04, above
  what split-half noise allows (Fig. 4 p. 6; Table 13 p. 28). That is the precondition for any
  transfer/interference study: if all families ranked models identically, there would be nothing
  to transfer between.
- **The gap it leaves is exactly the student's question**: (1) no weight updates of any kind — no
  SFT, no RL, no multi-agent training — so no evidence on whether training one direction moves the
  others (p. 10); (2) the only harness comparison is prompt-level, and there the cross-game
  playbooks *hurt* ((n−1)→1 −13/−45, n→n −25/−21, p. 9), a small hint of interference that a
  training study could test properly; (3) no propensity measures and no welfare/surplus scoring,
  so cooperation and negative-sum dynamics are seen only through who-beat-whom.
- Compared with [[liu2025spiral]]: SPIRAL trains (RL self-play) but on 3 zero-sum games; SocialGym
  evaluates 22 games but trains nothing. A thesis can sit between them: SPIRAL-style training on one
  SocialGym family, measured on all families. SPIRAL's negotiation specialist beating the
  multi-game model on negotiation is the kind of interference SocialGym's family profiles could
  reveal at scale.
- Compared with [[wang2024sotopia]] (same lab lineage): SocialGym replaces SOTOPIA's GPT-4 judge
  with rules, and shows the judge agrees 92.5% at the pair level when the outcome is visible
  (App. D) — useful evidence for the [[judges]] topic that judges track outcomes when outcomes
  exist, but not that they are reliable where no outcome exists.
- Compared with [[li2026whose]]: both find leaking under conversational pressure (strong models
  name the secret while justifying suspicions, p. 7), and both find prompting fixes do not reliably
  help. Li et al. trained (distillation) and hit a leak/over-refusal frontier; SocialGym leaves
  training open.
- Compared with [[zhang2026terms]]: TERMS uses scripted opponents with known types to attribute
  failures; SocialGym uses LLM-vs-LLM Elo, which makes negotiation hard to separate (27-Elo band).
  A benchmark covering negotiation should borrow TERMS-style verifiers for that direction.
- Clocktower-style social deduction benchmarks (Werewolf Arena, AvalonBench, Blood on the
  Clocktower evals): SocialGym folds six such games into one protocol and rates both sides;
  its finding that hidden-role games dominate and reproduce the overall ranking (0.96) warns that a
  multi-direction benchmark heavy on social deduction will mostly measure general capability.
- For Parley's persuasion angle ([[persuasion-susceptibility]]): the vote-call following (65% of
  others' votes go to the named player, chance 24%) is a cheap rule-based persuasion measure.

## Ideas to borrow
- **Family × side profile with split-half reliability**: report each direction's ranking, its
  Spearman with the others, and the reliability ceiling (ρ_overall vs √reliability) to show that
  differences are not noise (Table 13, p. 28). Use the same test on pre/post-training profiles.
- **Equal-weight family average** instead of pooling episodes, so one family cannot dominate.
- **Random-player anchor** per family to give relative Elo a floor (App. L.4).
- **Ablate communication** (discussion vs private reasoning vs none) to show a game actually
  measures talk (App. L.5).
- **Rule-based behaviour probes** (secret stated, vote on hidden opponent, kept vote calls, bribe
  inspection, trades that help) alongside win/loss — these are the hooks for propensity measures.
- **Paired-deal evaluation** (same seeds with and without a treatment, paired bootstrap ΔElo) for
  comparing harnesses cheaply (p. 8).
- Use the open engine (FSM + visibility config per game, no engine changes per game) as a base, and
  add what it lacks: absolute payoff/surplus scores, free-text negotiation with private values,
  propensity probes, and SFT/RL arms trained on one family and tested on all.
