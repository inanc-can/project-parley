# Game-theoretic evaluations

Benchmarks that score LLM play against game-theoretic solutions.

- [[duan2024gtbench]]: ten OpenSpiel games, LLM vs solver.
- [[huang2024gamabench]]: eight multi-player games, distance to rational play.
- [[erdogan2026should]]: empirical information design; outcomes scored against known utilities
  (share of maximum gains, normalized Nash product).
- [[bichler2026model]]: LLM pricing agents in repeated Bertrand competition; the deployment
  interface, not the model, selects competitive vs high-price regimes (TUM DSS chair).
- [[liang2026agents]]: LLM bargaining against a Perfect Bayesian Equilibrium benchmark.
- [[bergemann2026training]]: bilateral trade with private information (Bergemann et al.).
- [[liu2025spiral]]: multi-game self-play RL; multi-game beats single-game on average but not on
  negotiation (Table 5).
- [[yuan2025marshal]]: MARSHAL (formerly MARS); self-play on competitive + cooperative games;
  specialists beat the generalist on their own game in 5 of 6; competition-only training hurts
  cooperation (Table 8).
- [[jiang2026model]]: OMAR; one policy plays all roles; SOTOPIA (judge-scored) and Werewolf.
- [[he2026socialgym]]: SocialGym; 22 rule-scored social games in 5 families; rankings barely
  carry across families (economic r = 0.04); no training evaluated.
- [[wang2026mindgames]]: MINDGAMES NeurIPS 2025 arena (Blotto, IPD, Codenames, Secret Mafia); many errors in Mafia.
- [[xie2026bench]]: M3-Bench; 24 games scored on behaviour, reasoning and messages; judge is also a player.
- [[smith2025evaluating]]: Concordia Contest; zero-shot cooperation on held-out mixed-motive scenarios.
- [[taylor2026clocktower]]: Bench on the Clocktower; 10-model social deduction; engine bugs affect >10% of games (estimate).
- [[lyu2026gift]]: GIFT; RL on games + math; transfer depends on pair and model size (headline number rests on a table misprint).
- [[ramesh2026sparks]]: Hanabi; RL transfers to a cooperative guessing task; SFT barely helps.
- [[sarkar2025training]]: Among Us social deduction trained with MARL (listening + speaking rewards).
- [[golechha2025among]]: Among Us deception sandbox; deception Elo vs detection Elo; activation probes.
- [[piatti2024cooperate]]: GovSim; common-pool resource collapse; wording swings results.
- [[lupu2025decrypto]]: Decrypto; interactive theory of mind; ToM fine-tuned model worse than base.
- [[guertler2025textarena]]: TextArena; 74-game Gym-style suite tagged by soft skill; used by SPIRAL and MINDGAMES.
