# Project Parley

Research and software on LLM agents that negotiate, cooperate and play games.

| Folder | What it is |
|---|---|
| `parley/` | The platform where LLM agents negotiate and play games (Python API + Next.js app). |
| `parley-mcp/` | Submodule: an open-source MCP tool where coding agents message each other and reach written agreements ([repo](https://github.com/inanc-can/parley-mcp)). |
| `research/` | Knowledge base: paper notes, benchmark map fields, possible hosts, the working research question. Paper PDFs are not included. |
| `parley-test/` | Early test scaffold. |
| `plans/` | Design notes. |

Clone with submodules: `git clone --recurse-submodules https://github.com/inanc-can/project-parley`.

Third-party code in `research/code/` is linked as submodules and keeps its own licenses. Five skills in
`research/.claude/skills/` come from K-Dense-AI/scientific-agent-skills (MIT); see `SOURCES.md` there.

License: MIT (see LICENSE), except where a file or submodule states otherwise.
