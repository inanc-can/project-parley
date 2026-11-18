# Where these skills come from

`add-paper` is ours. The rest were copied on 2026-11-01 and are not tracked upstream.

**lingzhi227/agent-research-skills** @ `9e6c085`. The repo has no license file.
literature-review, novelty-assessment, idea-generation, research-planning, data-analysis,
math-reasoning, paper-writing-section, related-work-writing, figure-generation, table-generation,
citation-management, backward-traceability, self-review, latex-formatting, paper-compilation,
paper-revision, rebuttal-writing

Local edits:
- `~/.claude/skills/` paths changed to `.claude/skills/` (run from `research/`).
- Steps that called the upstream deep-research / literature-search scripts (not installed) now
  point to the paper-search MCP tools and `papers/`.

**K-Dense-AI/scientific-agent-skills** @ `5f2bc03` (v2.72.0), MIT; each SKILL.md may carry its own license.
statistical-analysis, statistical-power, experimental-design, scientific-critical-thinking,
hypothesis-generation

Its scripts need Python 3.12+ with the scientific stack; run them with e.g.
`uv run --with statsmodels --with scipy --with numpy --with pandas --with matplotlib python <script>`.

Left out on purpose: overlaps (K-Dense scientific-writing / peer-review; lingzhi experiment-design,
which plans ML training runs) and ML-only or duplicate skills.

## Public repository
The 17 lingzhi227/agent-research-skills copies are not included in the public repository because that
repo has no license. Get them from https://github.com/lingzhi227/agent-research-skills.
