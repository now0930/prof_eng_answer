"""The Bot must report a successful secondary history write as success."""

from __future__ import annotations

import json

import bot
import study.learning_runtime as learning_runtime
import study.training_history as training_history


def test_completed_grade_logs_saved_history_without_queue_field(monkeypatch, tmp_path):
    session_id = "synthetic-learning-session"
    messages = []
    snapshot = {"history_status": "saved", "attempt_id": "synthetic-attempt"}
    saved = []

    monkeypatch.setattr(bot, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(bot, "DATA_DIR", tmp_path)
    monkeypatch.setattr(bot, "get_active_session", lambda _chat, _state: session_id)
    monkeypatch.setattr(bot, "load_meta", lambda _sid: {"images": []})
    monkeypatch.setattr(bot, "save_meta", lambda _sid, _meta: None)
    monkeypatch.setattr(bot, "load_rubric", lambda: {})
    monkeypatch.setattr(bot, "get_chat_provider", lambda _chat: "auto")
    monkeypatch.setattr(bot, "log", messages.append)
    monkeypatch.setattr(bot, "normalize_grade_submission", lambda _raw: {
        "normalized_text": "문제: 합성 질문\n답안: 합성 답안",
        "question_text": "합성 질문",
        "answer_text": "합성 답안",
        "question_answer_boundary": {"manual_review_required": False},
    })
    grade = {
        "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
        "topic_id": "synthetic_topic",
        "total_score": 12.0,
    }
    monkeypatch.setattr(bot, "run_agent_pipeline", lambda **_kwargs: ({}, grade))
    monkeypatch.setattr(bot, "reconcile_grade_score", lambda **kwargs: kwargs["parsed"])
    monkeypatch.setattr(bot, "_finalize_grade_before_bot_persistence", lambda value: value)
    monkeypatch.setattr(bot, "attach_submission_normalization", lambda value, _evidence: value)
    monkeypatch.setattr(training_history, "TrainingHistoryStore", lambda _path: object())
    monkeypatch.setattr(learning_runtime, "record_completed_grade", lambda *args, **kwargs: saved.append(kwargs) or snapshot)

    returned_sid, _, _ = bot.grade_answer(123, "합성 제출", {})

    assert returned_sid == session_id
    assert len(saved) == 1
    assert json.loads((tmp_path / session_id / "grade.json").read_text())["total_score"] == 12.0
    assert any("learning history saved" in message for message in messages)
    assert not any("learning history write failed" in message for message in messages)
