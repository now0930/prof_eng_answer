from __future__ import annotations

import copy
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from study.learning_runtime import (
    _review_candidates,
    complete_topic_review,
    create_daily_review_queue,
    record_completed_grade,
)
from study.master_topic_pack import load_master_topic_pack
from study.training_history import TrainingAttempt, TrainingHistoryStore


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
        assert all(item["status"] == "pending" for item in output["queue"]["items"])
        assert len(history.list_attempts(learner_id="telegram-chat-100")) == 1
        assert history.list_attempts(learner_id="telegram-chat-100")[0]["question_text"] == "Define the topic and give an application."
        assert len(history.list_attempts(learner_id="another-chat")) == 0
        assert (base / "session-1" / "learning_history.json").is_file()

        # Reopening the queue on the same local date must not replenish it.
        same_day_queue, _ = create_daily_review_queue(
            history,
            learner_id="telegram-chat-100",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T23:00:00+09:00",
        )
        assert same_day_queue == output["queue"]

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


def test_unattempted_topic_completion_survives_until_due() -> None:
    with tempfile.TemporaryDirectory(prefix="learning-runtime-new-topic-") as directory:
        history = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        first_queue, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-03T10:00:00+09:00",
        )
        topic_id = first_queue["items"][0]["topic_id"]
        reviewed = complete_topic_review(
            history,
            learner_id="new-learner",
            topic_id=topic_id,
            reviewed_at="2026-10-03T10:30:00+09:00",
        )
        assert reviewed["next_review_at"].startswith("2026-11-02")
        history.complete_daily_queue_item("new-learner", "2026-10-03", topic_id)
        assert history.list_attempts(learner_id="new-learner") == []
        tomorrow, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-10-04T10:00:00+09:00",
        )
        assert all(item["topic_id"] != topic_id for item in tomorrow["items"])
        due, _ = create_daily_review_queue(
            history,
            learner_id="new-learner",
            master_directory=ROOT / "master_topic_packs",
            generated_at="2026-11-03T10:00:00+09:00",
        )
        assert any(
            item["topic_id"] == topic_id and item["reason"] == "long_unreviewed_topic"
            for item in due["items"]
        )


def test_source_change_is_acknowledged_after_review() -> None:
    master = copy.deepcopy(load_master_topic_pack(sorted((ROOT / "master_topic_packs").glob("*.json"))[0]))
    topic_id = master["topic_id"]
    master["sources"].append({"updated_at": "2026-10-01T10:00:00+09:00"})
    attempt = {
        "topic_id": topic_id,
        "question_id": "q1",
        "question_text": "Explain this topic.",
        "attempted_at": "2026-09-01T10:00:00+09:00",
        "last_reviewed_at": "2026-10-02T10:00:00+09:00",
        "next_review_at": "2026-11-01T10:00:00+09:00",
        "score": 18.0,
    }
    before = _review_candidates(
        [attempt], {topic_id: master}, {}, now=datetime.fromisoformat("2026-10-03T10:00:00+09:00"),
        repository_root=ROOT,
    )
    assert not any(item["reason"] == "recently_changed_topic" for item in before)
    master["sources"][0]["updated_at"] = "2026-10-03T09:00:00+09:00"
    after = _review_candidates(
        [attempt], {topic_id: master}, {}, now=datetime.fromisoformat("2026-10-03T10:00:00+09:00"),
        repository_root=ROOT,
    )
    assert any(item["reason"] == "recently_changed_topic" for item in after)


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"LEARNING_RUNTIME_TESTS={len(tests)}_PASS")
