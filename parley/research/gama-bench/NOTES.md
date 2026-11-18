# GAMA-Bench

**Paper:** Huang et al., ICLR 2025 — *How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments* (arXiv 2403.11807) — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
Eight classic multi-player games: guessing (2/3 of the average), El Farol bar, divide the dollar, public goods, diner's dilemma, sealed-bid auction, battle royale, pirate game. Scores models on how rational their play is and keeps a leaderboard.

## Useful for Parley
- Multi-player social dilemmas (public goods, diner's dilemma) for when Parley adds 3+ player games.
- Its scoring of distance to rational play, close to Parley's distance-to-baseline metrics.

## Caveats
- Players act through numeric choices more than negotiation dialogue.
- The scoring scheme changed over versions (see their changelog); cite the version you compare against.
