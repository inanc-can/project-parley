# Parley Research

Literature notes, possible hosts and the research proposal for the Parley study. The software is
in `../parley`.

```sh
uv run scripts/build.py                     # check notes, rebuild generated/
uv run scripts/arxiv.py 2401.04536          # paper metadata from arXiv
git submodule update --init --depth 1       # fetch related projects' code
```

In Claude Code, `/add-paper <arXiv id>` reads a paper in full and writes its note.

- [Literature matrix](generated/matrix.md)
- [The gap](proposal/gap.md)
- [Reading queue](inbox.md)
