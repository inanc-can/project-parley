"""Command line: run matches, export results, serve the web app."""

import json
import sys
from pathlib import Path

import typer
from dotenv import load_dotenv

from parley.llm.cache import Cache
from parley.llm.client import LLMClient
from parley.matches.runner import MatchConfig
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
    show_turns: bool = typer.Option(False, "--show-turns", help="print every message live"),
):
    """Run a match from a JSON config (from `parley template` or `parley sim`); store it."""
    from parley.sim import LivePrinter, print_summary, run_and_store

    load_dotenv()
    cfg = MatchConfig.model_validate_json(config.read_text())
    client = LLMClient(cache=None if no_cache else Cache())
    match_id, records = run_and_store(cfg, client, Store(db), LivePrinter(cfg, show_turns))
    print_summary(cfg, records)
    typer.echo(f"\nmatch {match_id} stored in {db} · parley export {match_id}")


@app.command()
def sim(db: Path = Path(".parley/parley.sqlite"), no_cache: bool = False):
    """Set up a match step by step, watch it live, and get a summary (interactive)."""
    from parley.sim import LAST_SIM, LivePrinter, print_summary, run_and_store, wizard

    if not sys.stdin.isatty():
        typer.echo("parley sim asks questions, so it needs a terminal. To script a match, use")
        typer.echo("`parley template <game> > match.json`, edit it, then `parley run match.json`.")
        raise typer.Exit(1)
    load_dotenv()
    try:
        cfg, live = wizard()
    except KeyboardInterrupt:
        typer.echo("\nCancelled.")
        raise typer.Exit(1) from None
    LAST_SIM.parent.mkdir(parents=True, exist_ok=True)
    LAST_SIM.write_text(cfg.model_dump_json(indent=2))
    client = LLMClient(cache=None if no_cache else Cache())
    try:
        match_id, records = run_and_store(cfg, client, Store(db), LivePrinter(cfg, live))
    except KeyboardInterrupt:
        typer.echo("\nStopped. Finished episodes are saved; the match is marked interrupted.")
        raise typer.Exit(130) from None
    print_summary(cfg, records)
    typer.echo(f"\nmatch {match_id} stored in {db} · parley export {match_id}")
    typer.echo(f"setup saved to {LAST_SIM} · rerun it: parley run {LAST_SIM}")


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


@app.command("mcp")
def mcp_server(
    client: str = typer.Option("", help='who is calling, kept in the record, e.g. "claude-code"'),
    url: str = typer.Option("", help="the Parley API (default $PARLEY_URL or localhost:8000)"),
    http_port: int | None = typer.Option(None, help="serve streamable HTTP on this port instead"),
    path: str = typer.Option("/mcp", help="the HTTP endpoint's path; make it hard to guess"),
    sessions: str = typer.Option("", help="token file (default ~/.parley/agent-talks.json)"),
):
    """Run the MCP server that lets an agent take a seat in a Parley talk. stdio for local
    agents (`claude mcp add parley -- uv run parley mcp`); --http-port for hosted ones such as
    a grok.com custom connector, behind a tunnel."""
    import os

    from parley.mcp_server import main

    if client:
        os.environ["PARLEY_CLIENT"] = client
    if url:
        os.environ["PARLEY_URL"] = url
    main(http_port, path, Path(sessions).expanduser() if sessions else None)
