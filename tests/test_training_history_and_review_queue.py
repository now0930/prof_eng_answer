from __future__ import annotations

import sys
import sqlite3
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from study.review_queue import ReviewQueueError, build_review_queue
from study.training_history import TrainingAttempt, TrainingHistoryError, TrainingHistoryStore
from study.learning_runtime import resolve_review_topic


def test_training_history_persists_attempt_and_review_state() -> None:
    with tempfile.TemporaryDirectory(prefix="training-history-") as directory:
        store = TrainingHistoryStore(Path(directory) / "learning.sqlite3")
        saved = store.save(TrainingAttempt(
            question_id="exam-2026-01-q2",
            topic_id="control_valve_authority_rangeability_gain_installed_performance",
            attempted_at="2026-10-03T09:00:00+09:00",
            score=16.5,
            diagnosis={"format": ["conclusion missing"], "content": ["rangeability partial"]},
        ))
        assert saved["review_status"] == "new"
        assert saved["attempt_id"]
        updated = store.update_review(
            saved["attempt_id"],
            review_status="scheduled",
            last_reviewed_at="2026-10-03T09:30:00+09:00",
            next_review_at="2026-10-06T09:00:00+09:00",
        )
        assert updated["review_status"] == "scheduled"
        assert updated["next_review_at"].startswith("2026-10-06")
        assert store.list_attempts(topic_id=saved["topic_id"])[0]["diagnosis"]["format"] == ["conclusion missing"]


def test_training_history_rejects_naive_time_and_out_of_range_score() -> None:
    for kwargs in (
        {"attempted_at": "2026-10-03T09:00:00", "score": 12},
        {"attempted_at": "2026-10-03T09:00:00+09:00", "score": 26},
    ):
        try:
            TrainingAttempt(
                question_id="q1",
                topic_id="valid_topic_id",
                diagnosis={},
                **kwargs,
            ).validated()
        except TrainingHistoryError:
            pass
        else:
            raise AssertionError("invalid training attempt was accepted")


def test_history_isolated_by_learner_and_latest_review_updates_schedule() -> None:
    with tempfile.TemporaryDirectory(prefix="training-history-learners-") as directory:
        store = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        attempt = TrainingAttempt(
            learner_id="chat-100",
            question_id="question-1",
            topic_id="valid_topic_id",
            attempted_at="2026-10-01T09:00:00+09:00",
            score=12,
            diagnosis={"content": ["needs work"]},
        )
        store.save(attempt)
        assert len(store.list_attempts(learner_id="chat-100")) == 1
        assert store.list_attempts(learner_id="chat-200") == []
        reviewed = store.review_latest_for_topic(
            "chat-100",
            "valid_topic_id",
            last_reviewed_at="2026-10-03T09:00:00+09:00",
            next_review_at="2026-11-02T09:00:00+09:00",
        )
        assert reviewed["review_status"] == "scheduled"
        assert reviewed["last_reviewed_at"].startswith("2026-10-03")


def test_training_history_migrates_pre_learner_columns() -> None:
    with tempfile.TemporaryDirectory(prefix="training-history-migration-") as directory:
        database = Path(directory) / "history.sqlite3"
        connection = sqlite3.connect(database)
        connection.execute(
            """CREATE TABLE training_history (
                attempt_id TEXT PRIMARY KEY,
                question_id TEXT NOT NULL,
                topic_id TEXT NOT NULL,
                attempted_at TEXT NOT NULL,
                score REAL NOT NULL,
                diagnosis_json TEXT NOT NULL,
                review_status TEXT NOT NULL,
                last_reviewed_at TEXT,
                next_review_at TEXT
            )"""
        )
        connection.execute(
            "INSERT INTO training_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("old-attempt", "old-question", "valid_topic_id", "2026-10-01T09:00:00+09:00", 10, "{}", "new", None, None),
        )
        connection.commit()
        connection.close()

        store = TrainingHistoryStore(database)
        old_row = store.list_attempts()[0]
        assert old_row["learner_id"] == "default"
        assert old_row["question_text"] == ""
        assert old_row["session_id"] == ""
        saved = store.save(TrainingAttempt(
            learner_id="chat-1",
            question_id="new-question",
            topic_id="valid_topic_id",
            attempted_at="2026-10-03T09:00:00+09:00",
            score=17,
            diagnosis={},
        ))
        assert saved["learner_id"] == "chat-1"


def test_review_queue_selects_weakness_and_retention_slots() -> None:
    queue = build_review_queue([
        {"topic_id": "topic_weak_01", "reason": "weak_topic", "question_id": "q-weak"},
        {"topic_id": "topic_old_01", "reason": "long_unreviewed_topic", "question_id": "q-old"},
        {"topic_id": "topic_new_01", "reason": "new_topic", "question_id": "q-new"},
    ], generated_at="2026-10-03T10:00:00+09:00")
    assert queue["daily_target"] == 2
    assert len(queue["items"]) == 2
    assert [item["slot"] for item in queue["items"]] == ["weakness", "retention"]
    assert {item["reason"] for item in queue["items"]} == {"weak_topic", "long_unreviewed_topic"}


def test_review_queue_deduplicates_topic_and_rejects_bad_contract() -> None:
    queue = build_review_queue([
        {"topic_id": "same_topic_01", "reason": "weak_topic", "question_id": "q1"},
        {"topic_id": "same_topic_01", "reason": "new_topic", "question_id": "q2"},
    ], generated_at="2026-10-03T10:00:00+09:00")
    assert len(queue["items"]) == 1
    try:
        build_review_queue([], generated_at="2026-10-03T10:00:00", daily_target=3)
    except ReviewQueueError:
        pass
    else:
        raise AssertionError("invalid queue target was accepted")


def test_manual_review_topic_resolution_is_date_independent() -> None:
    topics = sorted((ROOT / "master_topic_packs").glob("*.json"))
    topic_id = topics[0].stem
    import json
    master = json.loads(topics[0].read_text(encoding="utf-8"))
    selected_by_id, id_matches = resolve_review_topic(ROOT / "master_topic_packs", topic_id)
    selected_by_title, title_matches = resolve_review_topic(
        ROOT / "master_topic_packs", master["title_ko"]
    )
    ambiguous, candidates = resolve_review_topic(ROOT / "master_topic_packs", "제어")
    assert selected_by_id["topic_id"] == topic_id and len(id_matches) == 1
    assert selected_by_title["topic_id"] == topic_id and len(title_matches) == 1
    assert ambiguous is None and len(candidates) > 1


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"TRAINING_HISTORY_QUEUE_TESTS={len(tests)}_PASS")
