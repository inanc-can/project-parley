"""Load exported episodes into a DataFrame and compare conditions with bootstrap CIs.

Needs the `analysis` extra: `uv sync --extra analysis`.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd


def load_episodes(*paths: str | Path) -> pd.DataFrame:
    """One row per (episode, role): who played it, their payoff, the outcome and metrics."""
    rows = []
    for path in paths:
        for line in Path(path).read_text().splitlines():
            ep = json.loads(line)
            out = ep["outcome"]
            for role, seat in ep["assignment"].items():
                cfg = ep["seats"].get(seat) or {}
                rows.append(
                    {
                        "match_id": ep["match_id"],
                        "episode": ep["index"],
                        "game": ep["spec"]["title"],
                        "role": role,
                        "seat": seat,
                        "agent_kind": cfg.get("kind"),
                        "model": cfg.get("model") or cfg.get("proposer_model") or cfg.get("name"),
                        "strategy_sha256": cfg.get("strategy_sha256"),
                        "payoff": out["payoffs"].get(role),
                        "end_reason": out["end_reason"],
                        "deal": out["deal"] is not None,
                        "deal_source": (out["deal"] or {}).get("source"),
                        **{f"m.{k}": v for k, v in out["metrics"].items()},
                    }
                )
    return pd.DataFrame(rows)


def bootstrap_ci(
    values, stat=np.mean, n: int = 10_000, level: float = 0.95, seed: int = 0
) -> tuple[float, float, float]:
    """(estimate, low, high) by percentile bootstrap."""
    x = np.asarray(values, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    rng = np.random.default_rng(seed)
    boots = np.array([stat(rng.choice(x, size=len(x), replace=True)) for _ in range(n)])
    alpha = (1 - level) / 2
    return (float(stat(x)), float(np.quantile(boots, alpha)), float(np.quantile(boots, 1 - alpha)))


def compare(df: pd.DataFrame, by: str | list[str], value: str = "payoff") -> pd.DataFrame:
    """Mean of `value` per group with a 95% bootstrap CI."""
    out = []
    for key, g in df.groupby(by):
        est, lo, hi = bootstrap_ci(g[value])
        out.append(
            {
                **dict(
                    zip(
                        [by] if isinstance(by, str) else by,
                        key if isinstance(key, tuple) else (key,),
                        strict=True,
                    )
                ),
                "n": len(g),
                "mean": est,
                "ci_low": lo,
                "ci_high": hi,
            }
        )
    return pd.DataFrame(out)
