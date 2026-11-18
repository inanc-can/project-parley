"""On-disk response cache (SQLite) so reruns cost nothing and are reproducible."""

import json
import sqlite3
from pathlib import Path
from typing import Any


class Cache:
    def __init__(self, path: str | Path = ".parley/cache.sqlite"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute("CREATE TABLE IF NOT EXISTS responses (key TEXT PRIMARY KEY, value TEXT)")

    def get(self, key: str) -> dict[str, Any] | None:
        row = self._db.execute("SELECT value FROM responses WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def set(self, key: str, value: dict[str, Any]) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO responses (key, value) VALUES (?, ?)", (key, json.dumps(value))
        )
        self._db.commit()
