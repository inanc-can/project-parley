# Parley Research — notes for Claude

Literature knowledge base for the Parley study (LLM agents negotiating; working question in
`proposal/gap.md`). The software lives in `../parley` and never imports from here.

**Read `CONTEXT.md` first** — current question, decisions, where I left off, how to work with me.
At the end of a session, update its "Where I left off" section.

## Layout
- `papers/<citekey>.md` — one note per paper: YAML frontmatter + fixed sections.
- `pdfs/<citekey>.pdf` — gitignored; re-fetch with `uv run scripts/arxiv.py <id> --pdf <citekey>`.
- `code/<name>` — related projects as pinned git submodules (`git submodule update --init`).
- `topics/` synthesis pages, `people/` possible hosts with outreach logs, `proposal/` the claim
  and drafts, `baselines/` published human results, `inbox.md` the reading queue.
- `generated/` (matrix, references.bib) is built by `uv run scripts/build.py`: never edit it.

## Rules
- **Metadata comes from arXiv or DBLP, never from memory**: `uv run scripts/arxiv.py <id>`.
- **`read:` must be honest**: `full` only after reading the whole PDF; `abstract` if only the
  abstract; `unverified` for notes of unknown origin. Only `full` notes support claims in the
  proposal.
- Findings carry numbers and page references, e.g. "agreement 0.28 in self-play (p. 6)".
- Link notes with `[[name]]` (a file name in papers/, topics/, people/ or proposal/).
- After any change to notes, run `uv run scripts/build.py`; it must pass before committing.
- When a paper strengthens or weakens the claim, add a line to `proposal/gap.md`.
- Answer questions from the notes and cite citekeys; say when a note is not `full`.

## Paper note sections
Question · Setup · Findings · Limitations · Relevance to Parley · Ideas to borrow.
Frontmatter fields and allowed values are checked by `scripts/build.py`.
