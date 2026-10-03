"""SQLite persistence for learner attempts and review state."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4


REVIEW_STATUSES = {"new", "scheduled", "due", "completed", "skipped"}


class TrainingHistoryError(ValueError):
    pass


def _timestamp(value: str | None, field: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        raise TrainingHistoryError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TrainingHistoryError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise TrainingHistoryError(f"{field} must include a timezone")
    return parsed.isoformat()


@dataclass(frozen=True)
class TrainingAttempt:
    question_id: str
    topic_id: str
    attempted_at: str
    score: float
    diagnosis: dict[str, Any]
    learner_id: str = "default"
    question_text: str = ""
    session_id: str = ""
    review_status: str = "new"
    last_reviewed_at: str | None = None
    next_review_at: str | None = None
    attempt_id: str | None = None

    def validated(self) -> "TrainingAttempt":
        if not isinstance(self.question_id, str) or not self.question_id.strip():
            raise TrainingHistoryError("question_id is required")
        if not isinstance(self.topic_id, str) or len(self.topic_id.strip()) < 8:
            raise TrainingHistoryError("topic_id is required")
        attempted_at = _timestamp(self.attempted_at, "attempted_at")
        if isinstance(self.score, bool) or not isinstance(self.score, (int, float)) or not 0 <= self.score <= 25:
            raise TrainingHistoryError("score must be between 0 and 25")
        if not isinstance(self.diagnosis, dict):
            raise TrainingHistoryError("diagnosis must be an object")
        if not isinstance(self.learner_id, str) or not self.learner_id.strip():
            raise TrainingHistoryError("learner_id is required")
        if not isinstance(self.question_text, str) or not isinstance(self.session_id, str):
            raise TrainingHistoryError("question_text and session_id must be strings")
        if self.review_status not in REVIEW_STATUSES:
            raise TrainingHistoryError("review_status is invalid")
        last_reviewed = _timestamp(self.last_reviewed_at, "last_reviewed_at", nullable=True)
        next_review = _timestamp(self.next_review_at, "next_review_at", nullable=True)
        attempt_id = self.attempt_id or str(uuid4())
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            raise TrainingHistoryError("attempt_id must be a non-empty string")
        return TrainingAttempt(
            question_id=self.question_id.strip(),
            topic_id=self.topic_id.strip(),
            attempted_at=attempted_at or "",
            score=float(self.score),
            diagnosis=self.diagnosis,
            learner_id=self.learner_id.strip(),
            question_text=self.question_text.strip(),
            session_id=self.session_id.strip(),
            review_status=self.review_status,
            last_reviewed_at=last_reviewed,
            next_review_at=next_review,
            attempt_id=attempt_id,
        )


class TrainingHistoryStore:
    """Small local store; the database path is supplied by the caller."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS training_history (
                    attempt_id TEXT PRIMARY KEY,
                    learner_id TEXT NOT NULL DEFAULT 'default',
                    question_id TEXT NOT NULL,
                    question_text TEXT NOT NULL DEFAULT '',
                    session_id TEXT NOT NULL DEFAULT '',
                    topic_id TEXT NOT NULL,
                    attempted_at TEXT NOT NULL,
                    score REAL NOT NULL CHECK(score >= 0 AND score <= 25),
                    diagnosis_json TEXT NOT NULL,
                    review_status TEXT NOT NULL,
                    last_reviewed_at TEXT,
                    next_review_at TEXT
                )"""
            )
            columns = {row["name"] for row in connection.execute("PRAGMA table_info(training_history)")}
            if "learner_id" not in columns:
                connection.execute("ALTER TABLE training_history ADD COLUMN learner_id TEXT NOT NULL DEFAULT 'default'")
            if "question_text" not in columns:
                connection.execute("ALTER TABLE training_history ADD COLUMN question_text TEXT NOT NULL DEFAULT ''")
            if "session_id" not in columns:
                connection.execute("ALTER TABLE training_history ADD COLUMN session_id TEXT NOT NULL DEFAULT ''")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_training_history_due ON training_history(next_review_at, review_status)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_training_history_learner_topic_v1 ON training_history(learner_id, topic_id, attempted_at)")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS daily_review_queues (
                    learner_id TEXT NOT NULL,
                    queue_date TEXT NOT NULL,
                    queue_json TEXT NOT NULL,
                    PRIMARY KEY (learner_id, queue_date)
                )"""
            )
            connection.execute(
                """CREATE TABLE IF NOT EXISTS unattempted_topic_reviews (
                    learner_id TEXT NOT NULL,
                    topic_id TEXT NOT NULL,
                    last_reviewed_at TEXT NOT NULL,
                    next_review_at TEXT NOT NULL,
                    PRIMARY KEY (learner_id, topic_id)
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "attempt_id": row["attempt_id"],
            "learner_id": row["learner_id"],
            "question_id": row["question_id"],
            "question_text": row["question_text"],
            "session_id": row["session_id"],
            "topic_id": row["topic_id"],
            "attempted_at": row["attempted_at"],
            "score": row["score"],
            "diagnosis": json.loads(row["diagnosis_json"]),
            "review_status": row["review_status"],
            "last_reviewed_at": row["last_reviewed_at"],
            "next_review_at": row["next_review_at"],
        }

    def save(self, attempt: TrainingAttempt) -> dict[str, Any]:
        record = attempt.validated()
        values = asdict(record)
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO training_history
                   (attempt_id, learner_id, question_id, question_text, session_id, topic_id, attempted_at, score, diagnosis_json,
                    review_status, last_reviewed_at, next_review_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    values["attempt_id"], values["learner_id"], values["question_id"],
                    values["question_text"], values["session_id"], values["topic_id"],
                    values["attempted_at"], values["score"],
                    json.dumps(values["diagnosis"], ensure_ascii=False, sort_keys=True),
                    values["review_status"], values["last_reviewed_at"], values["next_review_at"],
                ),
            )
        return values

    def list_attempts(self, *, learner_id: str = "default", topic_id: str | None = None) -> list[dict[str, Any]]:
        if not isinstance(learner_id, str) or not learner_id.strip():
            raise TrainingHistoryError("learner_id is required")
        query = "SELECT * FROM training_history"
        clauses = ["learner_id = ?"]
        parameters: tuple[Any, ...] = (learner_id.strip(),)
        if topic_id is not None:
            clauses.append("topic_id = ?")
            parameters += (topic_id,)
        query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY attempted_at, attempt_id"
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update_review(
        self,
        attempt_id: str,
        *,
        review_status: str,
        last_reviewed_at: str | None,
        next_review_at: str | None,
    ) -> dict[str, Any]:
        if review_status not in REVIEW_STATUSES:
            raise TrainingHistoryError("review_status is invalid")
        last_reviewed = _timestamp(last_reviewed_at, "last_reviewed_at", nullable=True)
        next_review = _timestamp(next_review_at, "next_review_at", nullable=True)
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE training_history SET review_status = ?, last_reviewed_at = ?, next_review_at = ? WHERE attempt_id = ?",
                (review_status, last_reviewed, next_review, attempt_id),
            )
            if cursor.rowcount != 1:
                raise TrainingHistoryError("attempt_id was not found")
            row = connection.execute("SELECT * FROM training_history WHERE attempt_id = ?", (attempt_id,)).fetchone()
        return self._row_to_dict(row)

    def review_latest_for_topic(
        self,
        learner_id: str,
        topic_id: str,
        *,
        last_reviewed_at: str,
        next_review_at: str,
    ) -> dict[str, Any]:
        last_reviewed = _timestamp(last_reviewed_at, "last_reviewed_at")
        next_review = _timestamp(next_review_at, "next_review_at")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT attempt_id FROM training_history WHERE learner_id = ? AND topic_id = ? ORDER BY attempted_at DESC, attempt_id DESC LIMIT 1",
                (learner_id, topic_id),
            ).fetchone()
            if row is None:
                raise TrainingHistoryError("no attempt exists for this learner and topic")
            connection.execute(
                "UPDATE training_history SET review_status = ?, last_reviewed_at = ?, next_review_at = ? WHERE attempt_id = ?",
                ("scheduled", last_reviewed, next_review, row["attempt_id"]),
            )
            updated = connection.execute(
                "SELECT * FROM training_history WHERE attempt_id = ?",
                (row["attempt_id"],),
            ).fetchone()
        return self._row_to_dict(updated)

    def list_unattempted_topic_reviews(self, learner_id: str) -> dict[str, dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT topic_id, last_reviewed_at, next_review_at FROM unattempted_topic_reviews WHERE learner_id = ?",
                (learner_id,),
            ).fetchall()
        return {
            row["topic_id"]: {
                "last_reviewed_at": row["last_reviewed_at"],
                "next_review_at": row["next_review_at"],
            }
            for row in rows
        }

    def schedule_unattempted_topic_review(
        self,
        learner_id: str,
        topic_id: str,
        *,
        last_reviewed_at: str,
        next_review_at: str,
    ) -> dict[str, str]:
        if not learner_id.strip() or not topic_id.strip():
            raise TrainingHistoryError("learner_id and topic_id are required")
        last_reviewed = _timestamp(last_reviewed_at, "last_reviewed_at")
        next_review = _timestamp(next_review_at, "next_review_at")
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO unattempted_topic_reviews
                   (learner_id, topic_id, last_reviewed_at, next_review_at)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT (learner_id, topic_id) DO UPDATE SET
                     last_reviewed_at = excluded.last_reviewed_at,
                     next_review_at = excluded.next_review_at""",
                (learner_id, topic_id, last_reviewed, next_review),
            )
        return {
            "learner_id": learner_id,
            "topic_id": topic_id,
            "last_reviewed_at": last_reviewed or "",
            "next_review_at": next_review or "",
        }

    def get_daily_queue(self, learner_id: str, queue_date: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT queue_json FROM daily_review_queues WHERE learner_id = ? AND queue_date = ?",
                (learner_id, queue_date),
            ).fetchone()
        return json.loads(row["queue_json"]) if row else None

    def save_daily_queue(self, learner_id: str, queue_date: str, queue: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps(queue, ensure_ascii=False, sort_keys=True)
        with self._connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO daily_review_queues (learner_id, queue_date, queue_json) VALUES (?, ?, ?)",
                (learner_id, queue_date, payload),
            )
            row = connection.execute(
                "SELECT queue_json FROM daily_review_queues WHERE learner_id = ? AND queue_date = ?",
                (learner_id, queue_date),
            ).fetchone()
        return json.loads(row["queue_json"])

    def complete_daily_queue_item(self, learner_id: str, queue_date: str, topic_id: str) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT queue_json FROM daily_review_queues WHERE learner_id = ? AND queue_date = ?",
                (learner_id, queue_date),
            ).fetchone()
            if row is None:
                raise TrainingHistoryError("no daily review queue exists")
            queue = json.loads(row["queue_json"])
            match = next((item for item in queue["items"] if item["topic_id"] == topic_id), None)
            if match is None:
                raise TrainingHistoryError("topic is not in today's review queue")
            match["status"] = "completed"
            connection.execute(
                "UPDATE daily_review_queues SET queue_json = ? WHERE learner_id = ? AND queue_date = ?",
                (json.dumps(queue, ensure_ascii=False, sort_keys=True), learner_id, queue_date),
            )
        return queue
