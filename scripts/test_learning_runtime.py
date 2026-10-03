from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from learning_runtime import (
    complete_topic_review,
    create_daily_review_queue,
    record_completed_grade,
)
from training_history import TrainingAttempt, TrainingHistoryStore


def test_grade_history_queue_and_completion_cycle() -> None:
    topics = sorted((ROOT / "master_topic_packs").glob("*.json"))
    assert len(topics) == 3
    master_one_topic = topics[0].stem
    attempted_at = "2026-10-03T10:00:00+09:00"
    with tempfile.TemporaryDirectory(prefix="learning-runtime-") as directory:
        base = Path(directory)
        history = TrainingHistoryStore(base / "history.sqlite3")
        output = record_completed_grade(
            history,
            learner_id="telegram-chat-100",
            sid="session-1",
            grade={"topic_id": master_one_topic, "final_total_score": 12.0, "breakdown": []},
            submission_normalization={"question_text": "Define the topic and give an application."},
            master_directory=ROOT / "master_topic_packs",
            session_directory=base / "session-1",
            attempted_at=attempted_at,
        )
        assert output["history_status"] == "saved"
        assert len(output["queue"]["items"]) == 2
        assert output["queue"]["items"][0]["reason"] == "weak_topic"
        assert output["queue"]["items"][1]["question_text"]
        assert len(history.list_attempts(learner_id="telegram-chat-100")) == 1
        assert history.list_attempts(learner_id="telegram-chat-100")[0]["question_text"] == "Define the topic and give an application."
        assert len(history.list_attempts(learner_id="another-chat")) == 0
        assert (base / "session-1" / "learning_history.json").is_file()

        completion_time = "2026-10-04T10:00:00+09:00"
        reviewed = complete_topic_review(
            history,
            learner_id="telegram-chat-100",
            topic_id=master_one_topic,
            reviewed_at=completion_time,
        )
        assert reviewed["review_status"] == "scheduled"
        assert reviewed["next_review_at"].startswith("2026-11-03")

        queue, _ = create_daily_review_queue(
            history,
            learner_id="telegram-chat-100",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-04T10:01:00+09:00",
        )
        assert all(item["topic_id"] != master_one_topic for item in queue["items"])


def test_review_queue_uses_due_history_and_keeps_learners_separate() -> None:
    topics = sorted((ROOT / "master_topic_packs").glob("*.json"))
    topic_id = topics[0].stem
    with tempfile.TemporaryDirectory(prefix="learning-runtime-due-") as directory:
        history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        history.save(TrainingAttempt(
            learner_id="alice",
            question_id="q-alice",
            topic_id=topic_id,
            attempted_at="2026-08-01T10:00:00+09:00",
            score=18,
            diagnosis={},
            review_status="scheduled",
            next_review_at="2026-09-01T10:00:00+09:00",
        ))
        queue_alice, _ = create_daily_review_queue(
            history,
            learner_id="alice",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        queue_bob, _ = create_daily_review_queue(
            history,
            learner_id="bob",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        assert any(item["reason"] == "long_unreviewed_topic" for item in queue_alice["items"])
        bob_topic = next(item for item in queue_bob["items"] if item["topic_id"] == topic_id)
        assert bob_topic["reason"] == "new_topic"


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"LEARNING_RUNTIME_TESTS={len(tests)}_PASS")
