"""Local end-to-end rehearsal with an actual private WordPress HTML bundle.

The public CI checkout lacks this private bundle and skips the rehearsal.
"""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bot
from study.learning_runtime import record_completed_grade
from study.training_history import TrainingHistoryStore

TOPIC = "second_order_lag_response_by_damping_ratio"
MASTER = ROOT / "master_topic_packs" / f"{TOPIC}.json"
BUNDLE = ROOT / "data" / "wordpress_topic_packs" / f"{TOPIC}.json"


def test_private_master_to_review() -> bool:
    if not BUNDLE.is_file():
        print("MASTER_VIEW_PRIVATE_E2E=SKIP_PRIVATE_BUNDLE_ABSENT")
        return False
    original_master = hashlib.sha256(MASTER.read_bytes()).hexdigest()
    original_bundle = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
    grade = {
        "topic_id": TOPIC,
        "final_total_score": 12.0,
        "verdict": "needs_correction",
        "weaknesses": ["근거 설명 부족"],
    }
    before_grade = copy.deepcopy(grade)
    user_id = 8675309
    with tempfile.TemporaryDirectory(prefix="master-view-e2e-") as temp:
        base = Path(temp)
        history = TrainingHistoryStore(base / "training_history.sqlite3")
        snapshot = record_completed_grade(
            history,
            learner_id=str(user_id),
            sid="private-e2e-session",
            grade=grade,
            submission_normalization={"question_text": "2차 시스템의 감쇠비별 응답을 설명하시오."},
            master_directory=ROOT / "master_topic_packs",
            session_directory=base / "session",
        )
        assert grade == before_grade
        attempts = history.list_attempts(learner_id=str(user_id), topic_id=TOPIC)
        assert len(attempts) == 1 and attempts[0]["score"] == 12.0
        feedback = attempts[0]["diagnosis"]["topic_guidance"]
        assert feedback["score_effect"] == "none"
        assert len(feedback["source_review_annotations"]) == 3
        assert "queue" not in snapshot
        messages = []
        with patch.object(bot, "BASE_DIR", ROOT), \
             patch.object(bot, "DATA_DIR", base), \
             patch.object(bot, "send_message", side_effect=lambda _id, message: messages.append(message)):
            bot.handle_text({"text": f"/review {TOPIC}"}, user_id, {})
            rendered = messages[-1]
            assert "요청 주제 복습" in rendered
            assert "2차" in rendered and "출처 원문 발췌" in rendered
            assert "검토 대기 (점수 영향 없음" in rendered
            assert "이전 진단 약점: 근거 설명 부족" in rendered
            bot.handle_text({"text": f"/review done {TOPIC}"}, user_id, {})
            assert "복습 완료" in messages[-1]
        reviewed = history.list_attempts(learner_id=str(user_id), topic_id=TOPIC)[0]
        assert reviewed["last_reviewed_at"] is not None
        assert reviewed["next_review_at"] is not None
        assert reviewed["score"] == 12.0
    assert hashlib.sha256(MASTER.read_bytes()).hexdigest() == original_master
    assert hashlib.sha256(BUNDLE.read_bytes()).hexdigest() == original_bundle
    print("MASTER_VIEW_PRIVATE_E2E=PASS")
    return True


if __name__ == "__main__":
    test_private_master_to_review()
