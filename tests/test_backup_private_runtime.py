"""Synthetic tests for private runtime backup; no real secrets or provider calls."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

import pytest

from scripts.backup_private_runtime import backup


def test_backup_private_runtime_copies_sessions_config_and_consistent_wal_sqlite():
    with TemporaryDirectory() as folder:
        home = Path(folder)
        repo = home / "hermes/workspace/prof_eng_answer"
        data = repo / "data"
        data.mkdir(parents=True)
        (data / "state.json").write_text('{"last_update_id":42,"chats":{}}', encoding="utf-8")
        session = data / "sessions" / "private-test"
        session.mkdir(parents=True)
        (session / "answer.txt").write_text("synthetic-private-answer", encoding="utf-8")
        env = home / "hermes/.env"
        env.write_text("TELEGRAM_TOKEN=TEST_ONLY_NOT_REAL\n", encoding="utf-8")

        db_path = data / "training_history.sqlite3"
        connection = sqlite3.connect(db_path)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("CREATE TABLE history (value TEXT NOT NULL)")
            connection.execute("INSERT INTO history VALUES ('committed-in-wal')")
            connection.commit()
            # Keep the writer connection open while backup takes its snapshot.
            dest = backup(repo, home / "private_backups"/"prof_eng_answer", home)
        finally:
            connection.close()

        manifest = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["status"] == "OK"
        assert manifest["state_json_valid"] is True
        assert len(manifest["sqlite_databases"]) == 1
        snapshot = dest / manifest["sqlite_databases"][0]["backup"]
        with sqlite3.connect(snapshot) as copied:
            assert copied.execute("SELECT value FROM history").fetchone()[0] == "committed-in-wal"
            assert copied.execute("PRAGMA journal_mode").fetchone()[0] == "delete"
        assert manifest["sqlite_databases"][0]["quick_check"] == "ok"
        assert (dest / "runtime/data/sessions/private-test/answer.txt").read_text(
            encoding="utf-8"
        ) == "synthetic-private-answer"
        assert (dest / "config/hermes.env").read_text(encoding="utf-8").startswith("TELEGRAM_TOKEN=")
        assert not (dest / "runtime/data/training_history.sqlite3-wal").exists()
        assert not (dest / "runtime/data/training_history.sqlite3-shm").exists()
        for item in dest.rglob("*"):
            assert item.stat().st_mode & 0o077 == 0


def test_backup_must_be_outside_repository():
    with TemporaryDirectory() as folder:
        repo = Path(folder) / "prof_eng_answer"
        (repo / "data").mkdir(parents=True)
        with pytest.raises(RuntimeError, match="outside the project"):
            backup(repo, repo / "backup", Path(folder))
