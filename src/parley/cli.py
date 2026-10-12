"""Command line: run matches, export results, serve the web app."""

import asyncio
import json
import uuid
from pathlib import Path

import typer
from dotenv import load_dotenv

from parley.llm.cache import Cache
from parley.llm.client import LLMClient
from parley.matches.runner import MatchConfig, run_match
from parley.matches.seats import ScriptedSeat
from parley.storage import Store
from parley.templates import TEMPLATES

app = typer.Typer(no_args_is_help=True, help="Parley: AI agents negotiating and playing games.")


@app.command()
def template(name: str = typer.Argument(..., help=f"one of {sorted(TEMPLATES)}")):
    """Print a match config for a template, with placeholder seats, to edit and run."""
    spec = TEMPLATES[name]()
    cfg = MatchConfig(
        spec=spec,
        seats={"A": ScriptedSeat(name="silent"), "B": ScriptedSeat(name="silent")},
    )
    typer.echo(cfg.model_dump_json(indent=2))


@app.command()
def run(
    config: Path,
    db: Path = Path(".parley/parley.sqlite"),
    no_cache: bool = False,
):
    """Run a match from a JSON config and store every episode."""
    load_dotenv()
    cfg = MatchConfig.model_validate_json(config.read_text())
    store = Store(db)
    client = LLMClient(cache=None if no_cache else Cache())
    match_id = uuid.uuid4().hex[:12]
    store.create_match(match_id, cfg)

    async def on_event(e):
        if e["type"] == "episode_end":
            o = e["outcome"]
            typer.echo(f"episode {e['index']}: {o['end_reason']:<16} payoffs {o['payoffs']}")

    try:
        records = asyncio.run(run_match(cfg, client, match_id, on_event))
    except BaseException:
        store.set_status(match_id, "failed")
        raise
    for r in records:
        store.save_episode(r)
    store.set_status(match_id, "done")
    typer.echo(f"match {match_id}: {len(records)} episodes stored in {db}")


@app.command()
def export(match_id: str, out: Path | None = None, db: Path = Path(".parley/parley.sqlite")):
    """Write a match's episodes as JSONL (one record per line)."""
    out = out or Path(f"{match_id}.jsonl")
    n = Store(db).export_jsonl(match_id, out)
    typer.echo(f"wrote {n} episodes to {out}")


@app.command()
def matches(db: Path = Path(".parley/parley.sqlite")):
    """List stored matches."""
    for m in Store(db).matches():
        typer.echo(f"{m['id']}  {m['status']:<8} {m['created_at'][:19]}  {m['config'].spec.title}")


@app.command()
def baselines(name: str):
    """Show the reference solutions of a template."""
    from parley.core.baselines import reference_solutions

    typer.echo(json.dumps(reference_solutions(TEMPLATES[name]()), indent=2))


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """Start the API server (the Next.js frontend runs separately: `cd frontend && pnpm dev`).
    Use --host 0.0.0.0 so others on your network can join."""
    import uvicorn

    uvicorn.run("parley.api.app:create_app", factory=True, host=host, port=port, reload=reload)
