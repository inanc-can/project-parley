# Project Parley

Two folders, each its own git repo with its own CLAUDE.md:

- `parley/` — the software: the platform where LLM agents negotiate and play games
  (Python API + Next.js app). Run commands from inside it (`make test`, `make dev`).
- `parley-mcp/` — a free open-source MCP tool where a developer's coding agents message each other
  and reach written agreements. Built by OpenCode from `parley-mcp/docs/PLAN.md`; it doesn't depend on `parley/`.
- `research/` — the knowledge base: paper notes, possible hosts, the research question
  (`research/proposal/gap.md`) and the proposal. Never imported by the software.

Start a session inside the folder you are working on; start here only for work that spans both
(e.g. turning a research finding into an experiment in Parley).
