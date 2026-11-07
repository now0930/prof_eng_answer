"""Question-scoped review must not modify finalized scores or leak answers."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import bot
from study.learning_runtime import review_material_for_topic
from study.master_topic_pack import load_master_topic_pack, project_grading, project_training
from study.review_model_answer import load_review_model_answer, matches_question
from study.review_presentation import review_model_answer_messages
from study.training_history import TrainingAttempt, TrainingHistoryStore


ROOT = Path(__file__).resolve().parents[1]
TOPIC = "control_valve_cavitation_flashing_choked_flow_damage_prevention"


def test_model_answer_is_question_scoped_and_score_neutral():
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{TOPIC}.json")
    grading = project_grading(ROOT, master)
    answer = load_review_model_answer(ROOT, TOPIC)
    assert answer and answer["review_status"] == "llm_reviewed_human_pending"
    assert project_training(ROOT, master)["review_model_answer"] == answer
    assert project_grading(ROOT, master) == grading
    assert "review_model_answer" not in grading
    assert matches_question(answer, "OCR 앞글\n문제 " + answer["question"])
    assert not matches_question(answer, "제어밸브의 유량특성을 설명하시오")
    assert load_review_model_answer(ROOT, "../data") is None


def test_two_finalized_attempts_are_compared_without_private_answer_text():
    answer = load_review_model_answer(ROOT, TOPIC)
    with TemporaryDirectory() as directory:
        base = Path(directory)
        store = TrainingHistoryStore(base / "history.sqlite3")
        sessions = base / "sessions"
        for number, score, status in ((1, 10.65, "MISSING"), (2, 17.83, "SATISFIED")):
            sid = f"synthetic_{number}"
            grade = {"topic_id": TOPIC, "total_score": score,
                     "requirements": [{"requirement_id": "cavitation_classification", "status": status}]}
            session = sessions / sid
            session.mkdir(parents=True)
            (session / "grade.json").write_text(json.dumps(grade), encoding="utf-8")
            store.save(TrainingAttempt(
                learner_id="42", question_id=f"q{number}", topic_id=TOPIC,
                attempted_at=f"2026-11-07T0{number}:00:00+09:00", score=score,
                diagnosis={}, question_text=("OCR 앞글 문제 " if number == 1 else "문제 ") + answer["question"],
                session_id=sid))
        material = review_material_for_topic(store, learner_id="42", topic_id=TOPIC,
                                            master_directory=ROOT / "master_topic_packs",
                                            sessions_directory=sessions)
        assert material["matched_question"]
        messages = review_model_answer_messages(material["training"], material["question_review_attempts"])
        combined = "\n".join(messages)
        assert "10.65/25" in combined and "17.83/25" in combined
        assert "MISSING" in combined and "SATISFIED" in combined
        assert "OCR 앞글" not in combined
        assert all(len(message.encode("utf-16-le")) // 2 <= 3000 for message in messages)
        assert [a["score"] for a in store.list_attempts(learner_id="42")] == [10.65, 17.83]


def test_unrelated_question_is_not_matched():
    with TemporaryDirectory() as directory:
        store = TrainingHistoryStore(Path(directory) / "history.sqlite3")
        store.save(TrainingAttempt(learner_id="42", question_id="other", topic_id=TOPIC,
                                   attempted_at="2026-11-07T01:00:00+09:00", score=12,
                                   diagnosis={}, question_text="다른 제어밸브 문항", session_id="other"))
        material = review_material_for_topic(store, learner_id="42", topic_id=TOPIC,
                                            master_directory=ROOT / "master_topic_packs")
        assert not material["matched_question"]
        assert material["question_review_attempts"] == []


def test_telegram_review_and_done_use_study_answer_without_changing_grade():
    messages = []
    with TemporaryDirectory() as directory:
        base = Path(directory)
        answer = load_review_model_answer(ROOT, TOPIC)
        history = TrainingHistoryStore(base / "history.sqlite3")
        history.save(TrainingAttempt(learner_id="42", question_id="q", topic_id=TOPIC,
                                     attempted_at="2026-11-07T01:00:00+09:00", score=10.65,
                                     diagnosis={"requirement_statuses": [
                                         {"requirement_id": "cavitation_classification", "status": "PARTIAL"}]},
                                     question_text=answer["question"], session_id="synthetic"))
        with patch.object(bot, "BASE_DIR", ROOT), patch.object(bot, "DATA_DIR", base), \
             patch.object(bot, "SESSIONS_DIR", base / "sessions"), \
             patch.dict(os.environ, {"TRAINING_HISTORY_DB": str(base / "history.sqlite3")}), \
             patch.object(bot, "send_message", side_effect=lambda _id, msg: messages.append(msg)):
            bot.handle_text({"text": f"/review {TOPIC}"}, 42, {})
            rendered = "\n".join(messages)
            assert "학습용 모범답안" in rendered
            assert "10.65/25" in rendered
            assert "발생 원리와 차이: PARTIAL" in rendered
            messages.clear()
            bot.handle_text({"text": f"/review done {TOPIC}"}, 42, {})
            assert "복습 완료" in "\n".join(messages)
        assert history.list_attempts(learner_id="42")[0]["score"] == 10.65
