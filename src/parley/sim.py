"""`parley sim`: set up a match step by step in the terminal, watch it live, see a summary.

The wizard only builds a MatchConfig; running and storing is shared with `parley run`.
"""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

import questionary
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from parley.api.rooms import allowed_models_from_env, match_summary
from parley.core.spec import GameSpec, JudgeOnlyScoring, MatrixScoring
from parley.llm.client import LLMClient
from parley.matches.runner import EpisodeRecord, MatchConfig, run_match
from parley.matches.seats import LLMSeat, ScriptedSeat, Seat, TeamSeat
from parley.storage import Store
from parley.templates import TEMPLATES

LAST_SIM = Path(".parley/last_sim.json")
OTHER = "Other (type a LiteLLM model id)…"
FROM_FILE = "A game from a JSON file…"
MATRIX_BASELINES = ["tit_for_tat", "always_cooperate", "always_defect", "grim_trigger"]
BARGAINING_BASELINES = ["walk_away", "silent"]

console = Console(highlight=False)


def short(model: str) -> str:
    """openrouter/qwen/qwen-2.5-7b-instruct -> qwen-2.5-7b-instruct"""
    return model.rsplit("/", 1)[-1]


def seat_label(seat: Seat) -> str:
    if isinstance(seat, LLMSeat):
        return short(seat.model)
    if isinstance(seat, TeamSeat):
        return f"team {short(seat.proposer_model)}+{short(seat.critic_model)}"
    return seat.name


# --- the wizard ----------------------------------------------------------------------


def _ask(question: questionary.Question) -> Any:
    """Ask, treating Ctrl-C / Esc as "stop the wizard"."""
    answer = question.ask()
    if answer is None:
        raise KeyboardInterrupt
    return answer


def _number(text: str, default: float, minimum: float, maximum: float | None = None) -> float:
    def ok(v: str) -> bool | str:
        try:
            x = float(v)
        except ValueError:
            return "Enter a number"
        if x < minimum or (maximum is not None and x > maximum):
            return (
                f"Between {minimum} and {maximum}" if maximum is not None else f"At least {minimum}"
            )
        return True

    return float(_ask(questionary.text(text, default=f"{default:g}", validate=ok)))


def _pick_model(text: str, models: list[str], default: str | None = None) -> str:
    choices = [questionary.Choice(short(m), value=m) for m in models] + [OTHER]
    model = _ask(questionary.select(text, choices=choices, default=default))
    if model == OTHER:
        model = _ask(
            questionary.text(
                "Model id (e.g. openrouter/<org>/<model>, anthropic/<model>):",
                validate=lambda v: bool(v.strip()) or "Required",
            )
        ).strip()
    return model


def _pick_game() -> GameSpec:
    templates = {name: make() for name, make in TEMPLATES.items()}
    choices = [questionary.Choice(spec.title, value=name) for name, spec in templates.items()]
    name = _ask(questionary.select("Game:", choices=[*choices, FROM_FILE]))
    if name != FROM_FILE:
        return templates[name]
    path = Path(
        _ask(questionary.path("File (a game spec, or a match config from `parley template`):"))
    ).expanduser()
    data = json.loads(path.read_text())
    return GameSpec.model_validate(data.get("spec", data))


def _pick_seat(seat_id: str, spec: GameSpec, models: list[str]) -> Seat:
    console.print(f"\n[bold]Seat {seat_id}[/bold]")
    baselines = (
        MATRIX_BASELINES if isinstance(spec.scoring, MatrixScoring) else BARGAINING_BASELINES
    )
    kind = _ask(
        questionary.select(
            "Agent:",
            choices=[
                questionary.Choice("Single LLM", value="llm"),
                questionary.Choice("Team: proposer + critic", value="team"),
                questionary.Choice(f"Scripted baseline ({', '.join(baselines)})", value="scripted"),
            ],
        )
    )
    if kind == "scripted":
        return ScriptedSeat(name=_ask(questionary.select("Baseline:", choices=baselines)))
    if kind == "team":
        proposer = _pick_model("Proposer model:", models)
        critic = _pick_model("Critic model:", models, default=proposer)
    else:
        model = _pick_model("Model:", models)
    strategy = _ask(
        questionary.text("Strategy instructions (Enter for none):", multiline=False)
    ).strip()
    temperature = _number("Temperature:", 0.7, 0, 2)
    if kind == "team":
        return TeamSeat(
            proposer_model=proposer, critic_model=critic, strategy=strategy, temperature=temperature
        )
    return LLMSeat(model=model, strategy=strategy, temperature=temperature)


def wizard() -> tuple[MatchConfig, bool]:
    """Ask for everything a match needs. Returns the config and whether to show turns live."""
    models = allowed_models_from_env()
    console.print("[bold]Parley simulation[/bold]  [dim]Ctrl-C to quit[/dim]\n")
    spec = _pick_game()
    console.print(f"[dim]{escape(spec.shared_context)}[/dim]")
    seats = {sid: _pick_seat(sid, spec, models) for sid in ("A", "B")}

    console.print()
    runs = int(_number("Runs (roles swap every run):", spec.runs, 1))
    needs_judge = isinstance(spec.scoring, JudgeOnlyScoring)
    judge_model = None
    if needs_judge or _ask(questionary.confirm("Use the judge LLM (rubric scores)?", default=True)):
        if needs_judge:
            console.print("[dim]This game is scored by the judge only.[/dim]")
        judge_model = _pick_model("Judge model:", models)
    parallel = int(_number("Episodes played at once:", 2, 1, 16))
    live = _ask(questionary.confirm("Show conversations live?", default=True))

    cfg = MatchConfig(spec=spec, seats=seats, runs=runs, judge_model=judge_model, parallel=parallel)
    console.print(
        f"\n{spec.title}: A = {seat_label(seats['A'])}, B = {seat_label(seats['B'])}, "
        f"{runs} runs, judge {short(judge_model) if judge_model else 'off'}"
    )
    if not _ask(questionary.confirm("Start?", default=True)):
        raise KeyboardInterrupt
    return cfg, live


# --- running and printing ------------------------------------------------------------


class LivePrinter:
    """Prints match events. Episodes run in parallel, so every line names its episode."""

    def __init__(self, cfg: MatchConfig, show_turns: bool = True):
        self.cfg, self.show_turns = cfg, show_turns
        self.assignments: dict[int, dict[str, str]] = {}

    def who(self, index: int, role: str) -> str:
        sid = self.assignments.get(index, {}).get(role, "?")
        seat = self.cfg.seats.get(sid)
        return f"{role} ({sid}{' · ' + seat_label(seat) if seat else ''})"

    async def __call__(self, e: dict[str, Any]) -> None:
        tag = f"[dim]#{e.get('index', 0) + 1}[/dim]"
        match e["type"]:
            case "match_start":
                console.rule(f"{self.cfg.spec.title} · {e['runs']} runs")
            case "episode_start":
                self.assignments[e["index"]] = e["assignment"]
                if self.show_turns:
                    roles = ", ".join(f"{r}={s}" for r, s in e["assignment"].items())
                    again = f" (attempt {e['attempt']})" if e.get("attempt", 1) > 1 else ""
                    console.print(f"{tag} [bold]start[/bold] {roles}{again}")
            case "turn" if self.show_turns:
                t = e["turn"]
                action = ""
                if a := t.get("action"):
                    terms = " ".join(f"{k}={v:g}" for k, v in (a.get("terms") or {}).items())
                    action = escape(f"[{a['type']}{' ' + terms if terms else ''}]")
                    action = f"  [cyan]{action}[/cyan]"
                # Model text is printed as-is: brackets in it must not be read as markup.
                who, message = escape(self.who(e["index"], t["role"])), escape(t["message"])
                console.print(f"{tag} [bold]{who}[/bold]: {message}{action}")
            case "episode_retry":
                retry = f"attempt {e['attempt']} failed, retrying:"
                console.print(f"{tag} [yellow]{retry}[/yellow] {escape(e['error'][:200])}")
            case "episode_end":
                o = e["outcome"]
                if e.get("error"):
                    console.print(
                        f"{tag} [red]failed after every attempt:[/red] {escape(e['error'][:200])}"
                    )
                    return
                colour = "green" if o.get("deal") else "yellow"
                deal = ""
                if d := o.get("deal"):
                    deal = " · " + " ".join(f"{k}={v:g}" for k, v in d["terms"].items())
                    if d.get("source") == "judge_extracted":
                        deal += " (judge-extracted)"
                by = (
                    f" by {self.who(e['index'], o['forfeited_by'])}"
                    if o.get("forfeited_by")
                    else ""
                )
                pays = "  ".join(
                    f"{self.assignments[e['index']][r]} {p:+g}" for r, p in o["payoffs"].items()
                )
                console.print(f"{tag} [{colour}]{o['end_reason']}{by}[/{colour}]{deal}  {pays}")


def print_summary(cfg: MatchConfig, records: list[EpisodeRecord]) -> None:
    summary = match_summary(records)
    if not summary:
        console.print("No episodes finished.")
        return
    console.rule("summary")
    table = Table(box=None, pad_edge=False)
    table.add_column("seat")
    table.add_column("agent")
    table.add_column("mean payoff", justify="right")
    for sid, seat in cfg.seats.items():
        mean = summary["mean_payoff_by_seat"].get(sid)
        table.add_row(sid, seat_label(seat), "–" if mean is None else f"{mean:,.2f}")
    console.print(table)
    ends = ", ".join(f"{k} {v}" for k, v in summary["end_reasons"].items())
    failed = f" · {summary['failed']} failed (left out of averages)" if summary["failed"] else ""
    console.print(f"\nendings: {ends}{failed}")
    if summary["metrics"]:
        metrics = "  ".join(f"{k} {v:.2f}" for k, v in summary["metrics"].items())
        console.print(f"metrics: {metrics}")
    if ref := summary.get("reference"):
        console.print(f"theory:  {json.dumps(ref, separators=(', ', ': '))}", soft_wrap=True)


def run_and_store(
    cfg: MatchConfig, client: LLMClient, store: Store, on_event
) -> tuple[str, list[EpisodeRecord]]:
    """Run a match, saving each episode as it ends. Ctrl-C marks the match interrupted
    (finished episodes stay saved); other failures mark it failed."""
    match_id = uuid.uuid4().hex[:12]
    store.create_match(match_id, cfg)
    try:
        records = asyncio.run(run_match(cfg, client, match_id, on_event, store.save_episode))
    except KeyboardInterrupt:
        store.set_status(match_id, "interrupted")
        raise
    except BaseException:
        store.set_status(match_id, "failed")
        raise
    store.set_status(match_id, "done")
    return match_id, records
