# Research library

Related academic work, kept for reference. **Parley's code never imports from here.** Ideas
we reuse are re-implemented natively, with credit.

Each folder has the paper (`paper.pdf`), notes (`NOTES.md`) and, where available, the
code as a pinned git submodule in `code/`. Fetch the code with:

```sh
git submodule update --init --depth 1
```

| Project | Paper | Most useful for |
|---|---|---|
| [NegotiationArena](negotiation-arena/NOTES.md) | Bianchi et al., 2024 | Buy/sell and ultimatum scenarios and their prompt wording. |
| [GTBench](gtbench/NOTES.md) | Duan et al., 2024 | LLM-vs-conventional-solver comparisons: a strong baseline idea beyond scripted agents. |
| [GAMA-Bench](gama-bench/NOTES.md) | Huang et al., ICLR 2025 | Multi-player social dilemmas (public goods, diner's dilemma) for when Parley adds 3+ player games. |
| [LLM-Deliberation](llm-deliberation/NOTES.md) | Abdelnabi et al., NeurIPS 2024 D&B | The clearest model for Parley's valuations scoring extended to many parties and issues. |
| [AgenticPay](agenticpay/NOTES.md) | *AgenticPay: A Multi-Agent LLM Negotiation System for Buyer-Seller Transactions* (arXiv 2602.06008) | Task variety for buy/sell templates (multi-product, markets). |
| [Deal or No Deal (FAIR end-to-end negotiator)](deal-or-no-deal/NOTES.md) | Lewis et al., 2017 | Parley's multi-issue trade template follows this setup, so its human dialogues and scores are a **human baseline** for that game. |
| [Melting Pot](melting-pot/NOTES.md) | Leibo et al., ICML 2021 | The reference design for evaluating agents against held-out co-players: a future Parley tournament mode could follow it. |
| [AI Safety via Debate](ai-safety-via-debate/NOTES.md) | Irving, Christiano & Amodei, 2018 | The judge-reads-the-transcript setup mirrors Parley's judge LLM, so it can inform judge reliability studies. |

`baselines/` holds published human results that Parley compares agents against.

To add a project: `git submodule add --depth 1 <repo-url> research/<name>/code`, save the
paper as `research/<name>/paper.pdf`, and write a `NOTES.md` in the same shape.
