"""The `parley sim` wizard, driven with keystrokes, and the printer and summary it uses."""

from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from parley import sim
from parley.llm.client import LLMClient
from parley.matches.seats import ScriptedSeat
from parley.storage import Store
from parley.templates import buy_sell

DOWN, ENTER, BACKSPACE = "\x1b[B", "\r", "\x7f"


def answer(*keys: str):
    """Feed one keystroke string per prompt, in order."""
    with create_pipe_input() as inp:
        for k in keys:
            inp.send_text(k)
        with create_app_session(input=inp, output=DummyOutput()):
            return sim.wizard()


def test_wizard_builds_a_match_and_it_runs(tmp_path, capsys):
    cfg, live = answer(
        DOWN + ENTER,  # game: Iterated prisoner's dilemma
        DOWN + DOWN + ENTER,  # seat A: scripted baseline
        ENTER,  # tit_for_tat
        DOWN + DOWN + ENTER,  # seat B: scripted baseline
        DOWN + DOWN + ENTER,  # always_defect
        BACKSPACE * 5 + "2" + ENTER,  # runs
        "n",  # no judge
        ENTER,  # episodes at once: default
        "y",  # show turns live
        "y",  # start
    )
    assert cfg.spec.title == "Iterated prisoner's dilemma"
    assert cfg.seats == {
        "A": ScriptedSeat(name="tit_for_tat"),
        "B": ScriptedSeat(name="always_defect"),
    }
    assert (cfg.runs, cfg.judge_model, cfg.parallel, live) == (2, None, 2, True)

    store = Store(tmp_path / "db.sqlite")
    match_id, records = sim.run_and_store(cfg, LLMClient(), store, sim.LivePrinter(cfg))
    sim.print_summary(cfg, records)
    out = capsys.readouterr().out
    assert store.matches()[0]["status"] == "done" and len(store.episodes(match_id)) == 2
    assert "player_a (A · tit_for_tat)" in out and "rounds_complete" in out
    assert "summary" in out and "always_defect" in out
    assert "[cooperate]" in out and "[defect]" in out  # actions survive Rich markup


async def test_printer_shows_brackets_in_model_text(capsys):
    cfg = sim.MatchConfig(
        spec=buy_sell(), seats={"A": ScriptedSeat(name="silent"), "B": ScriptedSeat(name="silent")}
    )
    printer = sim.LivePrinter(cfg)
    await printer(
        {"type": "episode_start", "index": 0, "assignment": {"seller": "A", "buyer": "B"}}
    )
    turn = {
        "role": "seller",
        "message": "[bold] $9,000 [/x]",
        "action": {"type": "offer", "terms": {"price": 9000}},
    }
    await printer({"type": "turn", "index": 0, "turn": turn})
    out = capsys.readouterr().out
    assert "[bold] $9,000 [/x]" in out and "[offer price=9000]" in out
