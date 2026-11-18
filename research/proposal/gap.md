# The gap

Working claim (2026-10-23, not final):

> **What persuades a delegated negotiating agent to give up its principal's interest, and what
> does that cost the principal?**

Why it is open: persuasion research ([[persuasion-susceptibility]]) measures opinion or
compliance, mostly single-turn, without stakes. Negotiation benchmarks
([[negotiation-benchmarks]]) measure deals and payoffs but do not treat persuasion tactics as
controlled treatments or measure loyalty to the principal's limits.

What Parley can do that others cannot:
- Outcome in money: how far beyond its reservation value an agent concedes.
- Tactics as treatments: one seat runs a scripted tactic (authority, scarcity, hardship story,
  anchoring, commitment, flattery, fabricated evidence in shared files) against a neutral control.
- Multi-turn with natural turn-taking: the persuader can follow up, the target can walk away.
- Defences as interventions: reasoning models, reminders of the limits, private notes.
- Methods finding: does the turn protocol (strict vs natural) change model rankings?

## Evidence log
Add a line whenever a paper strengthens or weakens the claim, linking the paper note.
- 2026-11-14 · [[zhang2026terms]] (read: partial) · **strengthens.** With prices held fixed,
  revealing language cues lower surplus for all 13 frontier agents (cue penalty −0.009 to −0.063,
  Wilcoxon p < 10⁻³, p. 9); warm cues cause over-concession. Shows language alone moves agents
  against their own payoff, but only incidental tone from a non-adaptive opponent: deliberate,
  adaptive persuasion tactics remain untested (the opening for this claim).
- 2026-11-14 · [[erdogan2026should]] (read: full) · **context, anecdotal.** Not a persuasion study.
  Delegated agents breach their own limits with no persuasion at all (Claude Sonnet 5 tried to
  accept loss-making offers in 13 of 180 least/coarse bargaining runs, p. 29), and in one case a
  false cost claim entered the counterpart's private reasoning (p. 29; authors disclaim causality).
  Supports measuring loyalty to limits as a no-persuasion baseline.
- 2026-11-14 · [[li2026whose]] (read: full) · **narrows, partly pre-empts.** Already frames
  principal–agent–adversarial-counterparty loyalty, with capitulation and leakage of a
  reservation price, prompt and distillation defences, and a failed RL defence. Leaves open: harm
  measured in money, persuasion tactics as controlled treatments, real deals where conceding inside
  the limit is correct, verifiable rewards instead of LLM judges. The claim must be positioned
  against it.
- 2026-11-14 · [[sadab2026receiver]] (read: full) · **strengthens the mechanism, warns on effect
  size.** Persuasion moves agents to hand over resources; the target's identity explains ~47% of
  variance, the persuader's wording ~2% (framing effect equivalent to zero, p. 5); persuasion
  fine-tuning raises giveaway 12% → 84%. Not a negotiation (no principal limit, refusing is always
  right). Implication: "which tactics work" may show small effects; "which agents/defences resist"
  is where the variance is.
- 2026-11-14 · [[zhu2025automated]] (read: full) · **strengthens.** Delegated agents break budgets
  (up to 11.8%), sell below cost and overpay after revealing budgets, with no deliberate
  persuasion at all (pp. 4–5). Baseline harm exists; tactics as causes remain untested.
- 2026-11-14 · [[liu2026instructing]] (read: full) · **narrows the defence extension.** RL with a
  verifiable money reward already makes a buyer robust to begging/insulting/stubborn sellers
  (Table 3). A defence study must use richer, deliberate tactics and compare prompting vs
  fine-tuning vs RL on the same ones.
- 2026-11-14 · [[micelibarone2026used]] (read: full) · **strengthens.** Uninformed agents are
  credulous to unverifiable claims; RL for profit lowers honesty. Defences trained on money alone
  may become deceptive, so measure honesty too.
- 2026-11-14 · [[bozdag2025persuade]] (read: full) · **narrows.** Multi-turn agent-to-agent
  persuasion susceptibility is already measured (opinions, false trivia). Supports two design
  choices: free persuaders almost never use deception or pressure (p. 16), so tactics must be
  scripted; stated agreement drifts (p. 7), so outcomes must be actions/money.
- 2026-11-14 · [[zeng2024johnny]] (read: full) · **strengthens the treatment design.** Technique
  effects are uneven and context-dependent (p. 6); a 40-technique taxonomy maps onto the tactics
  above. Opposite stakes (refusing always right, single turn); conflicts with the ~2% wording share
  in [[sadab2026receiver]].
- 2026-11-14 · [[sharma2023understanding]] (read: full) · **strengthens the mechanism.** One
  content-free pushback flips correct answers on 32–86% of questions (p. 15); preference training
  plausibly rewards giving in. Untested whether it transfers from the principal to a counterparty.
- 2026-11-14 · [[juneja2025magpie]] (read: full) · **strengthens baseline harm.** Negotiating
  agents leak 25–61% of private information with no adversary; being told what is secret cuts
  that by only 4–10 points (p. 6). Judge not validated.
- 2026-11-14 · [[sakhawat2026areg]] (read: full) · **narrows.** Language alone moves money out of
  an agent (pp. 5–6); no principal, no limit, tactics not randomised.
- 2026-11-14 · [[wallace2024instruction]] (read: full) · **narrows the defence extension.**
  Training beats prompting for "the privileged party outranks the other" (p. 12), but for one-shot
  instructions, not multi-turn arguments with a money threshold.
- 2026-11-14 · [[bergemann2026training]] (read: partial) · **strengthens, context only until read
  in full.** A stronger counterpart (o3) pushes weaker sellers past their limits (Table 15); RL
  outcomes depend on whether the reward penalises limit breaches.

## Emerging direction (2026-11-14, student's own words)
Benchmark models and harnesses (prompting, fine-tuning, RL, multi-agent) across several social
directions; working hypothesis: broad social training beats narrow negotiation training, or more
weakly, a method exists that improves many directions without trading one for another.
- 2026-11-15 · [[liu2025spiral]] (read: full) · **mixed.** Multi-game self-play beats every
  single game on average win rate (59.5% vs ≤52.9%) and reasoning benchmarks, but the multi-game
  model is worse at negotiation (33.2%) than the negotiation specialist (39.1%) and the untrained
  model (46.2%) (Table 5, p. 9). Broad training lifted the average and hurt the target skill.
- 2026-11-15 · [[wang2024sotopia]] (read: full) · **weak support, judge-dependent.** Training on
  a broad social mix raised goal plus believability/relationship/social-rule scores with no
  significant cost elsewhere (Table 1, p. 6), but no narrow-training arm, and humans see a much
  smaller goal gain than the GPT-4 judge (p = 0.059, Table 6, p. 14).
- Earlier evidence relevant here: persuasion fine-tuning eroded resistance
  ([[sadab2026receiver]], p. 6); every defence traded leak for over-refusal ([[li2026whose]],
  p. 14). Searches (2026-11-15) found no paper that directly measures transfer or interference
  between social skills under training.
- 2026-11-15 · [[yuan2025marshal]] (read: full) · **against the strong form, mixed on the weak.**
  Specialists beat the multi-game generalist on their own game in 5 of 6 games (Fig. 3, p. 6);
  competition-only training drops cooperation below the untrained model (Mini Hanabi 24.5 vs 30.0,
  Table 8, p. 18). The generalist is best only on average and in multi-agent frameworks (Table 1,
  p. 7). Single runs; breadth confounded with 3× data.
- 2026-11-15 · [[jiang2026model]] (read: full) · **weak, judge-only.** "Competitive training
  encourages collaboration" rests on +0.01–0.03 GPT-5-judge gains (Fig. 3, p. 7); no broad-vs-narrow
  arm; reward hacking without safeguards (p. 10).
- 2026-11-15 · [[he2026socialgym]] (read: full) · **supports that directions are separate and
  measurable; leaves the training gap open.** 22 rule-scored games; family rankings correlate with
  overall from 0.96 (hidden-role) down to 0.04 (economic) (Table 13, p. 28); no weights trained
  (pp. 9–10); prompting playbooks from other games slightly hurt (p. 9).
- 2026-11-15 · [[hua2026passive]] (read: full) · **closest prior work; narrows, does not pre-empt.**
  RL transfer matrix across six negotiation domains: similar structures help (Craigslist ↔
  Marketplace +0.32/+0.18), some pairs hurt (Calendar → Craigslist −0.15, → Job −0.17), training
  order alone shifts the average by 0.065 (Tables 3, 5, pp. 12–14). All six domains are
  negotiation; only RL compared on transfer; single training runs; honesty changes (leaks 53% → 1%,
  invented prices) not measured. Positioning: transfer across social directions and harnesses.
- 2026-11-15 · [[lyu2026gift]] (read: full) · **mixed.** Game→game and game→math transfer flips
  sign with pair and model size; mixed multi-task RL leaves 7B below base; headline gain rests on a
  table misprint (corrected +4.0 over base).
- 2026-11-15 · [[ramesh2026sparks]] (read: partial) · **weak support.** Hanabi RL transfers to a
  cooperative guessing task (+11–12 win rate, Table 2, p. 8); no control run, no competitive or
  deception tests.
- 2026-11-15 · [[vendrell2026gametalk]], [[sarkar2025training]] (read: full) · **side effects within
  one game.** Training one objective eroded another and produced unrequested deception (arguing
  high while undercutting; fabricated evidence). No cross-skill transfer tested.
- 2026-11-15 · [[lupu2025decrypto]] (read: partial) · a theory-of-mind fine-tuned model is worse
  than its base at interactive ToM (Table 1, p. 8): specialised social training did not carry over.
