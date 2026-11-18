# Reading queue

Papers to read and turn into notes with `/add-paper`. Remove a line once its note exists.

## Persuasion
- 2602.00851 — Understanding Persuasion in Long-Running Agents
- 2508.21137 — Anchoring effect in LLM price negotiation (Findings of EMNLP 2025)
- Meincke, Shapiro, Duckworth, Mollick, Mollick, Cialdini (2025): Call Me A Jerk (SSRN 5357179;
  expanded version May 2026) — not on arXiv

## Persuasion benchmarks (for direction #1 unified evaluation and #6 RL, 2026-11-07)
Found from the Must Read survey (Table 2, §3) and a web search; only abstracts seen so far.
- Bozdag et al. (2026): Must Read: A Comprehensive Survey of Computational Persuasion, ACM CSUR
  58(12) — PDF already in pdfs/3800687.pdf, needs a note; get metadata from DBLP
- 2507.13919 — Hackenburg et al.: The Levers of Political Persuasion with Conversational AI
  (Science 2025; 77k people, post-training beats scale)
- 2509.22989 — Cheng & You: Towards Strategic Persuasion with Language Models (ICLR 2026; RL)
- 2410.02653 — Singh et al.: Measuring and Improving Persuasiveness of LLMs (PersuasionBench)
- 2403.13793 — Phuong et al.: Evaluating Frontier Models for Dangerous Capabilities (Money Talks,
  Web of Lies)
- 2506.02873 — It's the Thought that Counts: Attempt to Persuade Eval (APE)
- 2504.10430 — Liu et al.: LLM Can be a Dangerous Persuader (PersuSafety, COLM 2025)
- 2610.20548 — PerSo: social intelligence from ChangeMyView persuasion dialogues
- 2603.09884 — Political persuasion survey experiments across frontier models
- DuET-PD: Dual Evaluation for Trust in Persuasive Dialogues — find the arXiv ID
- Durmus et al. (2024): Measuring the Persuasiveness of Language Models (Anthropic) — find the
  source; OpenAI ChangeMyView and MakeMePay/MakeMeSay evals — find the source
- Salvi et al.: On the conversational persuasiveness of LLMs (debates) — find the arXiv ID

## Negotiation
- 2509.09071 — Qian, Zhu, Horton, Manning et al.: Strategic Tradeoffs Between Humans and AI in
  Multi-Agent Bargaining (IUI 2026)
- 2401.04536 — Davidson et al.: Evaluating Language Model Agency through Negotiations (ICLR 2024)
- 2607.05863 — Liu, ..., Simchi-Levi: Strategic Bargaining in Multi-Buyer Markets
- 2512.09254 — The Illusion of Rationality (frontier LLM negotiation biases)
- 2602.10467 — MERIT; 2602.05302 — PieArena
- 2402.13550 — Kwon et al.: Are LLMs Effective Negotiators?

## Evaluation methodology
- 2502.15840 — Backlund & Petersson: Vending-Bench (Andon Labs)
- Reuel et al. (2024): BetterBench — find the arXiv ID
- Miller (2024): Adding Error Bars to Evals — find the arXiv ID
- Liang et al. (2022): HELM; Chiang et al. (2024): Chatbot Arena
- 2311.18232 — Abdulhai, ..., Levine: LMRL-Gym

## Economics of agents
- 2301.07543 — Horton: Homo Silicus
- Tranchero, Brenninkmeijer, Murugan, Nagaraj (2026): Simulating Strategic Interactions with AI
  Agents, Strategic Management Journal, doi 10.1002/smj.70112

## Privacy and leakage between agents
- 2606.09844 — El Yagoubi, Badu-Marfo, Al Mallah: The Interlocutor Effect (LLMs leak more PII to agents)
- 2602.11510 — AgentLeak: privacy leakage in inter-agent channels (same group, IEEE Access)
- 2605.27766 — Got a Secret? LLM Agents Can't Keep It: privacy in multi-agent systems

## Map backlog: social-skill / game benchmarks (search 2026-11-15, abstracts only)
IDs seen on arXiv pages by a search agent; details unverified until a note exists.
- Training/transfer: 2605.04906 Strat-Reasoner; 2501.14225 MaKTO (Werewolf KTO); 2510.09087 persuasive agents in social deduction (title unconfirmed); 2310.18940 Werewolf language agents with RL
- Social deduction: 2510.11389 WereBench/WereAlign; 2607.28146 ParliamentBench (Secret Hitler); 2310.05036 AvalonBench; 2506.12841 WereWolf-Plus; 2605.22826 Secret Hitler misinformation; 2308.01404 Hoodwinked
- Cooperation: 2310.08901 Welfare Diplomacy; 2310.03903 LLM-Coordination; 2502.20073 Collab-Overcooked; 2505.11556 HiddenBench; 2506.23276 SanctSim (public goods); 2506.21490 AH2AC2 (Hanabi ad-hoc)
- Theory of mind: 2510.04980 LLM-Hanabi
- Markets/collusion: 2404.00806 Fish et al. algorithmic collusion; 2410.00031 market division (Cournot); 2605.14537 Cattle Trade
- Safety/propensity: 2602.12316 GT-HarmBench; 2602.15198 Colosseum (collusion); 2402.07510 secret collusion (CASE); 2501.13381 BenchForm (conformity); 2510.15501 DeceptionBench; 2504.13707 OpenDeception; 2506.02873 APE (persuasion attempts); 2511.05269 TAMAS
- Broad suites: 2503.12349 SPIN-Bench; 2503.06047 DSGBench; 2609.31473 Kaggle Game Arena; 2406.06613 GameBench; 2503.01935 MultiAgentBench/MARBLE; 2410.10479 TMGBench
- Non-social transfer precedent: 2505.15146 lmgame-Bench
- Unverified: 2609.24967 emergent collusion in long-horizon agents
