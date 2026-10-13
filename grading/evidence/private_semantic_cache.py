"""Private, version-addressed cache for score-neutral semantic proposals.

Caller supplies a location outside the public repository. JSON payloads may
contain answer excerpts and must never be committed or uploaded as artifacts.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
from typing import Any


class PrivateSemanticCache:
    def __init__(self, path: str | Path, *, repository_root: str | Path):
        target = Path(path).expanduser()
        root = Path(repository_root).resolve()
        if not target.is_absolute() or target.resolve().is_relative_to(root):
            raise ValueError("semantic cache must be outside the repository")
        if target.is_symlink():
            raise ValueError("semantic cache must not be a symlink")
        if not target.parent.is_dir():
            raise ValueError("semantic cache parent must already exist")
        if target.exists() and (not target.is_file() or target.stat().st_mode & 0o077):
            raise ValueError("existing semantic cache is not private")
        old_mask = os.umask(0o077)
        try:
            self._db = sqlite3.connect(str(target))
            self._db.execute("PRAGMA journal_mode=DELETE")
            self._db.execute("PRAGMA synchronous=FULL")
            self._db.execute("CREATE TABLE IF NOT EXISTS responses ("
                             "request_hash TEXT PRIMARY KEY, response_json TEXT NOT NULL)")
            self._db.commit()
        finally:
            os.umask(old_mask)
        if target.stat().st_mode & 0o077:
            self._db.close()
            raise ValueError("semantic cache permissions are too broad")

    def get(self, request_hash: str) -> dict[str, Any] | None:
        row = self._db.execute(
            "SELECT response_json FROM responses WHERE request_hash=?", (request_hash,),
        ).fetchone()
        return json.loads(row[0]) if row else None

    def __setitem__(self, request_hash: str, response: dict[str, Any]) -> None:
        raw = json.dumps(response, ensure_ascii=False, sort_keys=True, allow_nan=False)
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO responses(request_hash,response_json) VALUES(?,?)",
                (request_hash, raw),
            )

    def close(self) -> None:
        self._db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
