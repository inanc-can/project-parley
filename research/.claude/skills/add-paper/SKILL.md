---
name: add-paper
description: Read a paper in full and add it to the knowledge base (note, topics, people, gap). Use when the user says /add-paper <arXiv id or title> or asks to add a paper.
---

# Add a paper

1. **Metadata:** `uv run scripts/arxiv.py <id> --pdf <citekey>`. Use its `id` as the citekey
   unless a clearer one exists (`surname + year + distinctive word`, e.g. `davidson2024agency`).
   For papers not on arXiv, take metadata from DBLP or the publisher page, never from memory.
2. **Read the whole PDF** in `pdfs/` (Read tool with `pages`, 20 at a time). If you cannot read
   it all, set `read: partial` and say which parts.
3. **Write `papers/<citekey>.md`** with the frontmatter from step 1 plus `venue`, `code`,
   `read`, `relevance`, `topics` and `setting` (copy the field names from an existing note), and
   the sections Question, Setup, Findings (numbers with page references), Limitations,
   Relevance to Parley, Ideas to borrow.
4. **Link it:** add a bullet to each topic in `topics:` (create the topic page if new); if an
   author is in `people/`, add the paper there.
5. **Test the claim:** add a line to the evidence log in `proposal/gap.md` if the paper
   strengthens or weakens it, and tell the user.
6. Remove the paper from `inbox.md`, run `uv run scripts/build.py`, and fix any error.
7. Reply with a five-line summary: what it found, how it bears on the gap, what to borrow.
