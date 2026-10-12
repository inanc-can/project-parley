# Deal or No Deal (FAIR end-to-end negotiator)

**Paper:** Lewis et al., 2017 — *Deal or No Deal? End-to-End Learning for Negotiation Dialogues* (arXiv 1706.05125); also Yarats & Lewis, ICML 2018 — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
The classic item-split negotiation: two people divide books, hats and balls with private values. Includes a dataset of 5,808 human–human dialogues (2,236 scenarios) and PyTorch models trained by supervised learning, RL self-play and rollout planning.

## Useful for Parley
- Parley's multi-issue trade template follows this setup, so its human dialogues and scores are a **human baseline** for that game.
- RL self-play: the reference point for future RL agents in Parley.

## Caveats
- Pre-LLM code (old PyTorch); use it for the data and the ideas, not to run.
