# Evaluation methodology

How to build an eval that reviewers and labs trust: legible headline metric, variance, error
bars, held-out opponents, human baselines.

- [[leibo2021meltingpot]]: evaluation against held-out co-players.
- [[sharma2023understanding]]: content-free pushback as a control arm.
- [[bozdag2025persuade]]: stated agreement drifts; measure actions, not self-reports.
- [[he2026socialgym]]: per-family and per-side ratings, random-player anchor, split-half
  reliability; hidden-role games dominate overall scores.
- [[wang2024sotopia]]: judge-trained models look better to the judge than to humans; validate.
- [[li2026whose]]: two-axis reporting (betrayal vs over-refusal), sanity items, integrity gate
  for silent API failures.

In `inbox.md`: Vending-Bench (Andon Labs), BetterBench, "Adding Error Bars to Evals", HELM,
Chatbot Arena.
- [[wu2026measuring]]: only 80% of single runs agree across 3 seeds; held-out split; trade-off depends on scoring.
- [[smith2025evaluating]]: held-out scenarios and co-players; rankings depend on co-players.
- [[wang2026mindgames]]: leaderboard validity varies by game (error rates 0–50%).
