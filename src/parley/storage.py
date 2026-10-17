"""SQLite storage for matches and episodes, with JSONL export for analysis."""

import json
import sqlite3
import threading
from datetime import UTC, datetime
from functools import wraps
from pathlib import Path

from parley.matches.runner import EpisodeRecord, MatchConfig

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches (
    id TEXT PRIMARY KEY, room_id TEXT, config TEXT NOT NULL,
    status TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS episodes (
    match_id TEXT NOT NULL, idx INTEGER NOT NULL, record TEXT NOT NULL,
    PRIMARY KEY (match_id, idx)
);
CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY, data TEXT NOT NULL, created_at TEXT NOT NULL
);
"""


def _locked(method):
    @wraps(method)
    def inner(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return inner


class Store:
    # One connection is shared by the API's worker threads; sqlite3 objects aren't safe to
    # use from two threads at once, so every method takes the lock.
    def __init__(self, path: str | Path = ".parley/parley.sqlite"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    @_locked
    def create_match(self, match_id: str, cfg: MatchConfig, room_id: str | None = None) -> None:
        self.db.execute(
            "INSERT INTO matches VALUES (?, ?, ?, 'running', ?)",
            (match_id, room_id, cfg.model_dump_json(), datetime.now(UTC).isoformat()),
        )
        self.db.commit()

    @_locked
    def set_status(self, match_id: str, status: str) -> None:
        self.db.execute("UPDATE matches SET status = ? WHERE id = ?", (status, match_id))
        self.db.commit()

    @_locked
    def mark_interrupted(self) -> int:
        """Matches left 'running' by a stopped server; their finished episodes are kept."""
        n = self.db.execute("UPDATE matches SET status = 'interrupted' WHERE status = 'running'")
        self.db.commit()
        return n.rowcount

    @_locked
    def save_episode(self, record: EpisodeRecord) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO episodes VALUES (?, ?, ?)",
            (record.match_id, record.index, record.model_dump_json()),
        )
        self.db.commit()

    @_locked
    def matches(self, room_id: str | None = None) -> list[dict]:
        q = "SELECT id, room_id, status, created_at, config FROM matches"
        rows = (
            self.db.execute(q + " WHERE room_id = ? ORDER BY created_at DESC", (room_id,))
            if room_id
            else self.db.execute(q + " ORDER BY created_at DESC")
        )
        return [{**dict(r), "config": MatchConfig.model_validate_json(r["config"])} for r in rows]

    @_locked
    def episodes(self, match_id: str) -> list[EpisodeRecord]:
        rows = self.db.execute(
            "SELECT record FROM episodes WHERE match_id = ? ORDER BY idx", (match_id,)
        )
        return [EpisodeRecord.model_validate_json(r["record"]) for r in rows]

    # Rooms are small documents; the API owns their shape (parley.api.rooms.Room).
    @_locked
    def save_room(self, room_id: str, data: str) -> None:
        self.db.execute(
            "INSERT INTO rooms VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET data = excluded.data",
            (room_id, data, datetime.now(UTC).isoformat()),
        )
        self.db.commit()

    @_locked
    def load_room(self, room_id: str) -> str | None:
        row = self.db.execute("SELECT data FROM rooms WHERE id = ?", (room_id,)).fetchone()
        return row["data"] if row else None

    @_locked
    def export_jsonl(self, match_id: str, path: str | Path) -> int:
        records = self.episodes(match_id)
        with open(path, "w") as f:
            for r in records:
                f.write(json.dumps(r.model_dump(mode="json")) + "\n")
        return len(records)
