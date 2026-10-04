from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bot
from study.training_history import TrainingHistoryStore


def test_grade_answer_records_learning_history_after_grade_file() -> None:
    topic_id = "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration"
    user_id = 8675309
    sid = "20261003_120000_8675309"
    queue_date = datetime.now().astimezone().date().isoformat()
    with tempfile.TemporaryDirectory(prefix="bot-learning-integration-") as directory:
        base = Path(directory)
        sessions = base / "sessions"
        session_dir = sessions / sid
        session_dir.mkdir(parents=True)
        (session_dir / "meta.json").write_text(json.dumps({"session_id": sid, "chat_id": user_id, "images": [], "status": "created"}), encoding="utf-8")
        state = {"chats": {str(user_id): {"active_session": sid}}}
        final_grade = {
            "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
            "topic_id": topic_id,
            "final_total_score": 13.5,
            "total_score": 13.5,
            "breakdown": [{"item": "C", "score": 3.0, "max": 8.0}],
            "weaknesses": ["현장 검증 근거 부족"],
        }

        with (
            patch.object(bot, "BASE_DIR", ROOT),
            patch.object(bot, "DATA_DIR", base),
            patch.object(bot, "SESSIONS_DIR", sessions),
            patch.object(bot, "load_meta", side_effect=lambda _sid: json.loads((sessions / _sid / "meta.json").read_text(encoding="utf-8"))),
            patch.object(bot, "save_meta", side_effect=lambda _sid, meta: (sessions / _sid / "meta.json").write_text(json.dumps(meta), encoding="utf-8")),
            patch.object(bot, "load_rubric", return_value={}),
            patch.object(bot, "log", return_value=None),
            patch.object(bot, "run_agent_pipeline", return_value=("raw grade", final_grade.copy())),
            patch.object(bot, "reconcile_grade_score", side_effect=lambda **kwargs: kwargs["parsed"]),
            patch.object(bot, "_finalize_grade_before_bot_persistence", side_effect=lambda value: value),
            patch.object(bot, "send_message", side_effect=lambda _chat_id, text: messages.append(text)),
        ):
            messages = []
            returned_sid, _, returned_grade = bot.grade_answer(
                user_id,
                "/grade\n문제: 압전식 센서의 원리와 적용을 설명하시오.\n답안: 전하 발생 원리를 설명한다.",
                state,
            )
            bot.handle_text({"text": "/review"}, user_id, state)
            assert "오늘의 복습 Queue" in messages[-1]
            assert "문제:" in messages[-1]
            assert "학습 개요:" in messages[-1]
            assert "핵심 사실:" in messages[-1]
            assert "고득점 포인트:" in messages[-1]
            assert "이전 진단 약점: 현장 검증 근거 부족" in messages[-1]
            with patch("study.learning_runtime.review_material_for_topic", return_value={
                "training": {
                    "source_materials": [{"title": "연결된 HTML", "text": "검증된 View 원문"}],
                    "source_review_annotations": [{"status": "pending_review", "score_effect": "none",
                        "source_state": "stale", "quote": "기존 인용", "review_note": "나중에 판단"}],
                },
                "wordpress_topic_pack": {"sources": [{"source_type": "pdf",
                    "extracted_text": "UNLINKED_RAW_MUST_NOT_APPEAR"}]},
            }):
                bot.handle_text({"text": "/review"}, user_id, state)
                assert "검증된 View 원문" in messages[-1]
                assert "검토 대기" in messages[-1]
                assert "이전 원문 기준" in messages[-1]
                assert "UNLINKED_RAW_MUST_NOT_APPEAR" not in messages[-1]
            bot.handle_text({"text": f"/review done {topic_id}"}, user_id, state)
            assert "복습 완료" in messages[-1]
            new_topic = next(
                item["topic_id"] for item in TrainingHistoryStore(base / "training_history.sqlite3")
                .get_daily_queue(str(user_id), queue_date)["items"]
                if item["reason"] == "new_topic"
            )
            bot.handle_text({"text": f"/review done {new_topic}"}, user_id, state)
            assert "복습 완료" in messages[-1]

        assert returned_sid == sid
        assert returned_grade["final_total_score"] == 13.5
        saved_grade = json.loads((session_dir / "grade.json").read_text(encoding="utf-8"))
        assert saved_grade["final_total_score"] == 13.5
        learning = json.loads((session_dir / "learning_history.json").read_text(encoding="utf-8"))
        assert learning["history_status"] == "saved"
        rows = TrainingHistoryStore(base / "training_history.sqlite3").list_attempts(learner_id=str(user_id))
        assert len(rows) == 1
        assert rows[0]["topic_id"] == topic_id
        assert rows[0]["score"] == 13.5
        assert rows[0]["diagnosis"]["weaknesses"] == ["현장 검증 근거 부족"]
        assert rows[0]["session_id"] == sid
        daily_queue = TrainingHistoryStore(base / "training_history.sqlite3").get_daily_queue(
            str(user_id), queue_date
        )
        assert daily_queue is not None
        assert next(item for item in daily_queue["items"] if item["topic_id"] == topic_id)["status"] == "completed"
        assert all(item["status"] == "completed" for item in daily_queue["items"])
        assert len(rows) == 1



if __name__ == "__main__":
    test_grade_answer_records_learning_history_after_grade_file()
    print("BOT_LEARNING_HISTORY_INTEGRATION_TESTS=1_PASS")
