# Melting Pot

**Paper:** Leibo et al., ICML 2021 — *Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot* (arXiv 2107.06857); Melting Pot 2.0 tech report (arXiv 2211.13746) — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
DeepMind's suite for multi-agent RL: 50+ substrates (games) and 256+ test scenarios probing cooperation, competition, deception, reciprocity and trust, scored on generalisation to unfamiliar co-players.

## Useful for Parley
- The reference design for evaluating agents against held-out co-players: a future Parley tournament mode could follow it.
- Social-dilemma categories for naming behavioural measures.

## Caveats
- Grid-world environments for RL, not language. Relevant once Parley adds RL agents.
