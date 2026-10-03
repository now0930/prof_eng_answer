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
                    question_id TEXT NOT NULL,
                    topic_id TEXT NOT NULL,
                    attempted_at TEXT NOT NULL,
                    score REAL NOT NULL CHECK(score >= 0 AND score <= 25),
                    diagnosis_json TEXT NOT NULL,
                    review_status TEXT NOT NULL,
                    last_reviewed_at TEXT,
                    next_review_at TEXT
                )"""
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_training_history_due ON training_history(next_review_at, review_status)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_training_history_topic ON training_history(topic_id, attempted_at)")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "attempt_id": row["attempt_id"],
            "question_id": row["question_id"],
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
                   (attempt_id, question_id, topic_id, attempted_at, score, diagnosis_json,
                    review_status, last_reviewed_at, next_review_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    values["attempt_id"], values["question_id"], values["topic_id"],
                    values["attempted_at"], values["score"],
                    json.dumps(values["diagnosis"], ensure_ascii=False, sort_keys=True),
                    values["review_status"], values["last_reviewed_at"], values["next_review_at"],
                ),
            )
        return values

    def list_attempts(self, *, topic_id: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM training_history"
        parameters: tuple[Any, ...] = ()
        if topic_id is not None:
            query += " WHERE topic_id = ?"
            parameters = (topic_id,)
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
