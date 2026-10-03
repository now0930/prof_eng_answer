from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from review_queue import ReviewQueueError, build_review_queue
from training_history import TrainingAttempt, TrainingHistoryError, TrainingHistoryStore


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


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"TRAINING_HISTORY_QUEUE_TESTS={len(tests)}_PASS")
