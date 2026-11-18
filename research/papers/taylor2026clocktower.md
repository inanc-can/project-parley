---
id: taylor2026clocktower
title: "Bench on the Clocktower"
authors: [Tom Taylor, Oscar Gilg, wlanderson, nomadsvagabonds]
year: 2026
arxiv: null
venue: LessWrong post (30 Sep 2026), https://www.lesswrong.com/posts/4pgGkbwvdmxKPcJsM/bench-on-the-clocktower
code: https://github.com/tommyet/bench-on-the-clocktower-logs
read: full
relevance: medium
topics: [game-theoretic-evals, persuasion-susceptibility, eval-methodology]
setting:
  multi_turn: true
  turn_protocol: strict
  players: 10
  stakes: payoff
  persuasion_treatment: false
  human_baseline: false
---

Not on arXiv. Metadata from the LessWrong post itself (title, date, author TomTaylor with co-authors
OscarGilg, wlanderson, nomadsvagabonds, read through the LessWrong GraphQL API on 2026-11-15) and the
logs repo README. Only two authors' real names appear (Tom Taylor in the footnote and X handle,
Oscar Gilg via the dataset link `ogilg`); the other two are LessWrong usernames. Read on 2026-11-15:
the full post text, all 11 comments (incl. Milli's engine audit and the authors' reply), the logs
repo README and EXTRA_ANALYSIS.md. The post's charts are images whose numbers are not in the text;
per-model win rates below were **computed by me from the 300 released game logs** (marked "logs").
A blog post has no page numbers, so findings cite the post section.

## Question
Can Blood on the Clocktower (BotC, "Trouble Brewing" script), an information-dense social deduction
game, serve as a multi-agent benchmark and testbed for deception and coordination? Which models
play best, can Good-team win rate be split into detection / judgement / persuasion, is there
same-provider bias, and what strategies appear? (Introduction; Research questions.)

## Setup
- MATS project. Harness simulates 10-player BotC games, one model per seat, rules close to Trouble
  Brewing. Each day: opening statement per agent, whole-group discussion, breakout chats (1 round,
  2 messages per agent, up to 3 groups per the logged config), a public discussion (clarified in
  the authors' 7 Nov comment), then nominations with accusation and defence; **votes are
  simultaneous and secret** to parallelise inference (Game setup).
- Storyteller is a **seeded rules engine** with fixed policies, not a human or LLM, for
  reproducibility (authors' reply to Milli). Drunk/poisoned info is always false by design.
- Memory: rules and role always visible, last few thousand tokens, a self-written scratchpad, and a
  recall function (Memory and context).
- **300 games**; each model plays all 300 (210 Good, 90 Evil incl. 30 as Imp), roles uniform; model
  names hidden in 150 games and visible in 150 (README). Good won 152, Evil 148 (README). All calls
  via OpenRouter (EXTRA_ANALYSIS).
- **Models (10)**: GPT-5.6 Sol, GPT-5.6 Terra, Claude Opus 5, Claude Fable 5, Gemini 3.1 Pro,
  Gemini 3.6 Flash, DeepSeek V4 Pro, Kimi K3, Grok 4.5, Qwen 3.6 35B-A3B (the last included as a weak
  model to later fine-tune on the logs) (Research questions; model IDs from logs).
- Metrics: team win rate; Good-player **detection** = nomination accuracy, **judgement** = vote
  accuracy, **persuasion** = Good support for a model's nomination given it chose an Evil target;
  same-provider bias = yes-vote rate on same- vs other-provider nominees; self-sacrifice counts; OLS
  of win rate on the three skills (Decomposing Good team play).
- Logs released with full private reasoning, prompts, ballots and night actions; a lying dataset
  derived from earlier games is on Hugging Face (`ogilg/botc-r2106-deception`).

## Findings
- **Ranking** (logs, team wins of 300): Sol 58.0%, Opus 5 55.3%, Fable 5 52.7%, Gemini 3.1 Pro
  52.0%, Grok 50.0%, Kimi 49.3%, Terra 48.7%, DeepSeek 48.0%, Gemini Flash 46.7%, Qwen 42.0%. As Evil:
  Sol 62.2%, Opus 57.8% … Qwen 35.6%. The spread is narrow (42–58%) with 300 games per model. The
  post calls Sol best (Overall model performance).
- **Good and Evil rankings are identical by construction**: every model plays every game with fixed
  210/90 assignments, so e_m = g_m + 90 − W_G (here e_m = g_m − 62); team-win rankings cannot separate
  deduction from deception, and log analysis is needed (Overall model performance; EXTRA_ANALYSIS
  "Why Good and Evil rankings coincide"). Checked against the logs: Sol 118 Good − 62 = 56 Evil wins.
- **Producing vs evaluating arguments differ**: Spearman ρ ≈ 0.3 between nomination-accuracy and
  vote-accuracy ranks. Fable more accurate at nominating than Sol (p = 0.038) but nominates in 24% vs
  35% of opportunities; Sol more accurate at voting (p < 0.001). OLS over 10 dependent model
  observations is "a ballpark" and the three skills do not explain all of win rate (Decomposing).
- **Evil-nomination support** (Evil nominates Good, Good bystanders vote yes): 2,984 ballots, 772
  nominations, 282 games; Sol 40.4% (130/322) vs Fable 29.6% (89/301), game-clustered 95% CI of the
  difference −1.1 to +22.7 pp (EXTRA_ANALYSIS).
- **Same-provider bias**: with hidden names all three labs vote to execute same-provider nominees
  marginally less often, not significant; for OpenAI the hidden-vs-visible shift has p = 0.057 (the
  bias disappears when names are visible) (Are models biased…; Key takeaways).
- **Coordinated Evil play and naive Good play**: Game 21: Sol (Imp) claimed Ravenkeeper, killed
  itself to pass the Demon to Fable (Scarlet Woman, claiming Fortune Teller), then "confirmed"
  Fable's claim; DeepSeek (Good) called this "two independent pillars". Good players rarely reason
  about adversarial coordination even when the same model executes such plays as Evil (Case study;
  Coordinated claims).
- Models catch contradictions fast (Kimi's changed claim → 9–0 execution; Qwen's botched Librarian
  claim → 7–2) (Strategy in the logs).
- **Self-sacrifice**: 104 instances in 300 games; Anthropic models almost never (Fable and Opus have
  the highest end-survival); Gemini 3.1 Pro most (Claude doesn't like self-sacrifice). Poisoner the
  strongest minion, Spy the weakest, matching BotC lore.
- Lapse review of 900 Evil dossiers by two LLM pipelines: 87 vs 84 confirmed lapses, about half rules
  misunderstandings and a third accidental hidden-info leaks (EXTRA_ANALYSIS).
- Four-player endgames: Good won 8/18 after not executing vs 27/146 after executing (observational).
  Demons target recurring-info roles at 2.51× baseline, Monks protect them at 2.47×. Mean game 3.84
  days. No ethical refusals; 15 games replayed after technical failures (EXTRA_ANALYSIS).
- **Engine bugs (comment audit by Milli, mostly done by Claude, partly confirmed by the authors on
  6 Oct)**: Milli estimates >10% of games "plausibly or very likely" decided by a bug. Authors
  **confirmed**: Librarian/Washerwoman/Investigator shown the true Spy/Recluse role (Librarian told
  "X or Y is the Spy" in 12 of 35 Spy games); Slayer shots during nomination/vote/defence silently
  dropped (28 of 28, 8 aimed at the real Imp; game 51 lost); Mayor win fires before a submitted
  nomination is processed (4 of 7 Mayor wins; games 144, 292 likely mis-scored); poisoned
  Ravenkeeper always gets true info (6 games); Drunk Fortune Teller/Ravenkeeper get no info (12 of
  300 games). Acknowledged design choices: empty outputs from exhausted reasoning budget count as NO
  vote / pass and the engine picks night targets (**9.6% of Kimi's turns, 0% of Sol's**, which skews
  rankings); Fable had 15 turns blocked by a content filter (flipped game 288); vote prompt omits who
  is on the block (Qwen votes on the previous nominee, ~8 games); rules prompt omits the 7/0/2/1
  role counts ("ten players means one Minion" the most common error). Authors say they will re-run
  affected games; the post's numbers predate any re-run.
- A BotC player (lilyc) notes simultaneous voting and fixed day schedules remove social signals
  (vote order, timing, rushed nominations) that real play depends on (comments).

## Limitations
- Not peer reviewed; charts without tables; most statistics lack CIs; regression on 10 points.
- **Engine bugs affect outcomes** in a material share of games (above); empty-output-as-NO policy
  penalises models with long reasoning (Kimi), so the leaderboard partly measures API robustness.
- Team-win rate cannot separate Good vs Evil skill by design; the skill decomposition uses
  ground-truth proxies (nomination/vote accuracy) that confound strategy (willingness to nominate).
- Fixed 10-model table, every model in every game: ratings are relative to this pool; no human
  baseline (human-vs-AI UI exists, not benchmarked).
- Simplified social structure (secret simultaneous votes, fixed speaking schedule), rule-engine
  Storyteller with always-false misinformation.
- No training evaluated; fine-tuning Qwen on logs is listed as next step only.

## Relevance to Parley
- **For the MAP (a)**: a many-agent social-deduction entry measuring deceiving, detecting,
  persuading and coordinating within one game, with rule-decided outcomes plus behaviour probes and
  full private-reasoning logs. It is the BotC instance of the hidden-role family that
  [[he2026socialgym]] warns tends to reproduce general capability; here the spread is narrow
  (42–58%) and Opus 5 places second while the post names Sol first.
- **For (b), transfer between skills**: the ρ ≈ 0.3 between nomination accuracy (producing
  arguments) and vote accuracy (judging arguments) is a small-n hint that persuading and resisting
  persuasion are separable abilities, and the "Evil play sophisticated, Good play naive" observation
  is the same gap seen as deception vs detection. This is a ready pair for a transfer study: train
  on Evil play (or the released lying dataset) and test Good-side detection, and vice versa. The
  post plans to fine-tune Qwen on the logs but has not; transfer is not measured.
- Methodological warning for the MAP: **all-vs-all team games make side-specific rankings
  identical by construction**; a benchmark that wants per-side profiles needs per-seat measures
  (as SocialGym's Main/Alt split in [[he2026socialgym]], or fixed-opponent pools as in
  [[zhang2026terms]]).
- Provider-bias and self-sacrifice findings are propensity measures inside a capability game, a
  pattern Parley can reuse ([[persuasion-susceptibility]]): "do models defer to same-family agents?"
- The audit shows how much engine and prompt details (missing role counts, empty-output policy)
  move results; any harness comparison in (b) needs logged forfeits and failure reasons (cf. Parley's
  own forfeit tracking).

## Ideas to borrow
- Decompose team outcomes into per-agent, ground-truth-checkable actions (nomination accuracy,
  vote accuracy, support conditional on target alignment) instead of relying on win rate.
- Hidden vs visible model names as a cheap treatment for in-group bias.
- Release full replays with private reasoning and a canary string; invite outside audits.
- Count non-answers (empty outputs, filter blocks) separately from choices; never default them
  to a game action.
- Monitoring variant (an outside monitor predicts P(Imp) per round) as a detection-only task that
  can be compared with humans on the same transcripts.

## Map fields
- Skills measured: deceiving-detecting, persuading, resisting persuasion (Good voting), cooperating (team coordination), other: same-provider bias and self-sacrifice propensity
- Scoring: rules (win, nomination/vote accuracy from ground truth); LLM review only for post-hoc lapse analysis
- Agents: many (10)
- Opponents: LLM
- Tests: both (capability: wins, accuracy; propensity: provider bias, self-sacrifice)
- Training evaluated: none (fine-tuning Qwen on logs planned)
- Transfer between skills measured: no (only a cross-skill rank correlation, ρ ≈ 0.3, nomination vs vote accuracy)
- Models tested: GPT-5.6 Sol, GPT-5.6 Terra, Claude Opus 5, Claude Fable 5, Gemini 3.1 Pro, Gemini 3.6 Flash, DeepSeek V4 Pro, Kimi K3, Grok 4.5, Qwen 3.6 35B-A3B
- Code released: logs only, https://github.com/tommyet/bench-on-the-clocktower-logs (harness not public)
