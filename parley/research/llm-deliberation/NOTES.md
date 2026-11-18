# LLM-Deliberation

**Paper:** Abdelnabi et al., NeurIPS 2024 D&B — *Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation* (arXiv 2309.17234) — `paper.pdf`

Code: `code/` (git submodule, pinned commit; `git submodule update --init` to fetch).

## What it is
Multi-party, multi-issue "scoreable games": six or more stakeholders with private scores over issue options negotiate toward a deal that must pass thresholds. Includes cooperative, greedy and adversarial (saboteur) variants, all experiment logs, and evaluation code.

## Useful for Parley
- The clearest model for Parley's valuations scoring extended to many parties and issues.
- Saboteur/greedy variants: ready-made behavioural conditions.
- Their released logs are a dataset to compare Parley results against.

## Caveats
- Heavy setup (PyTorch/conda listed even for API runs).
- Round-robin multi-party format; needs 3+ player support in Parley first.
