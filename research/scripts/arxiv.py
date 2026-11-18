# /// script
# requires-python = ">=3.11"
# ///
"""Print a paper's frontmatter metadata from the arXiv API; optionally save its PDF.

    uv run scripts/arxiv.py 2401.04536            # metadata as YAML
    uv run scripts/arxiv.py 2401.04536 --pdf KEY  # also save pdfs/KEY.pdf

Metadata always comes from arXiv, never from memory: citations typed by hand drift.
"""

import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ATOM = {"a": "http://www.w3.org/2005/Atom"}
ROOT = Path(__file__).resolve().parent.parent


def fetch(arxiv_id: str) -> dict:
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(url, timeout=30) as response:
        entry = ET.fromstring(response.read()).find("a:entry", ATOM)
    if entry is None or entry.find("a:title", ATOM) is None:
        sys.exit(f"arXiv has no paper {arxiv_id}")
    authors = [a.findtext("a:name", "", ATOM) for a in entry.findall("a:author", ATOM)]
    title = re.sub(r"\s+", " ", entry.findtext("a:title", "", ATOM)).strip()
    year = entry.findtext("a:published", "", ATOM)[:4]
    surname = re.sub(r"[^a-z]", "", authors[0].split()[-1].lower())
    word = next(
        (w for w in re.findall(r"[a-z]+", title.lower()) if len(w) > 3 and w not in STOP), "paper"
    )
    return {"id": f"{surname}{year}{word}", "title": title, "authors": authors, "year": year}


STOP = {"with", "from", "that", "this", "what", "when", "towards", "large", "language", "models"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("arxiv_id")
    parser.add_argument("--pdf", metavar="KEY", help="save the PDF as pdfs/KEY.pdf")
    args = parser.parse_args()
    meta = fetch(args.arxiv_id)
    print(f"id: {meta['id']}")
    print(f'title: "{meta["title"]}"')
    print("authors:")
    for author in meta["authors"]:
        print(f"  - {author}")
    print(f"year: {meta['year']}")
    print(f'arxiv: "{args.arxiv_id}"')
    if args.pdf:
        target = ROOT / "pdfs" / f"{args.pdf}.pdf"
        target.parent.mkdir(exist_ok=True)
        urllib.request.urlretrieve(f"https://arxiv.org/pdf/{args.arxiv_id}", target)
        print(f"# saved {target.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
