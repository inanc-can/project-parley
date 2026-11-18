# NegotiationArena

**Paper:** Bianchi et al., 2024 — *How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis* (arXiv 2402.05863) — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
Two LLM agents play turn-based negotiation games (resource exchange, ultimatum, buy/sell) through free-text messages with XML-tagged fields that a parser reads. The paper studies win rates, payoffs and behavioural tactics such as pretending to be desperate or cunning.

## Useful for Parley
- Buy/sell and ultimatum scenarios and their prompt wording.
- Behavioural findings to try to reproduce: anchoring, the effect of personas, irrational concessions.

## Caveats
- Hard-codes exactly two agents (`negotiationarena/agents/agents.py:28`); agents are LLM chat histories; moves are parsed from XML tags with regexes; one agent class per provider.
- Parley differs on purpose: N-player core, conversation-first engine with validated JSON actions, team-per-seat, theory baselines.
- The paper's code is on the `paper_experiment_code` branch, not `main`.
- This local clone has a `.env.local`; keep it out of any commit.
