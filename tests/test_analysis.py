import pytest

pytest.importorskip("pandas")

from parley.analysis import bootstrap_ci, compare, load_episodes  # noqa: E402
from parley.llm.client import LLMClient  # noqa: E402
from parley.matches.runner import MatchConfig, run_match  # noqa: E402
from parley.matches.seats import ScriptedSeat  # noqa: E402
from parley.storage import Store  # noqa: E402
from parley.templates import iterated_prisoners_dilemma  # noqa: E402


async def test_export_loads_and_compares(tmp_path):
    cfg = MatchConfig(
        spec=iterated_prisoners_dilemma(rounds=3),
        seats={"A": ScriptedSeat(name="tit_for_tat"), "B": ScriptedSeat(name="always_defect")},
        runs=4,
    )
    store = Store(tmp_path / "db.sqlite")
    store.create_match("m", cfg)
    for r in await run_match(cfg, LLMClient(), "m"):
        store.save_episode(r)
    store.export_jsonl("m", tmp_path / "m.jsonl")

    df = load_episodes(tmp_path / "m.jsonl")
    assert len(df) == 4 * 2  # episodes × roles
    table = compare(df, "model").set_index("model")
    assert table.loc["tit_for_tat", "mean"] == 2  # (0,5) + 2×(1,1)
    assert table.loc["always_defect", "mean"] == 7


def test_bootstrap_ci_brackets_the_mean():
    est, lo, hi = bootstrap_ci([1, 2, 3, 4, 5])
    assert est == 3 and lo <= 3 <= hi
