# GTBench

**Paper:** Duan et al., 2024 — *GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations* (arXiv 2402.12348) — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
Ten games built on OpenSpiel (e.g. Tic-Tac-Toe, Connect-4, Kuhn poker, Nim, Liar's Dice, blind auction, negotiation, iterated prisoner's dilemma), covering complete vs. incomplete information and deterministic vs. probabilistic play. Supports LLM-vs-solver (MCTS) and LLM-vs-LLM, with several reasoning agents (prompt, CoT, ToT, …). Has a Hugging Face leaderboard.

## Useful for Parley
- LLM-vs-conventional-solver comparisons: a strong baseline idea beyond scripted agents.
- Its game taxonomy for choosing future Parley templates.
- Comparing reasoning-agent styles (CoT vs. plain) as an experimental factor.

## Caveats
- Mostly board/card games with a move interface; little free conversation.
- Uses LangChain for inference.
