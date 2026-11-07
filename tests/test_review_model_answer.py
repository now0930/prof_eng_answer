"""Regression: optional /review model answer never alters grading authority."""

from __future__ import annotations

import copy
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import bot
from study.master_topic_pack import load_master_topic_pack, project_grading, project_training
from study.review_model_answer import load_review_model_answer
from study.review_presentation import review_model_answer_messages

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "control_valve_cavitation_flashing_choked_flow_damage_prevention"


def test_argon_study_answer_is_score_neutral():
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{TOPIC}.json")
    grading_before = project_grading(ROOT, master)
    training = project_training(ROOT, master)
    example = training["review_model_answer"]
    assert example["topic_id"] == TOPIC
    assert example["score_effect"] == "none"
    assert example["review_status"] == "llm_reviewed_human_pending"
    assert len(example["sections"]) >= 4
    assert project_grading(ROOT, master) == grading_before
    assert "review_model_answer" not in grading_before["sources"]

    snapshot = copy.deepcopy(training)
    messages = review_model_answer_messages(training)
    rendered = "\n".join(messages)
    assert "학습용 모범답안" in rendered
    assert "사람 검토 대기" in rendered
    assert "Vena Contracta" in rendered
    assert "플래싱" in rendered
    assert "초크" in rendered
    assert all(len(message.encode("utf-16-le")) // 2 <= 3000 for message in messages)
    assert training == snapshot


def test_review_answer_missing_for_other_topics_and_bad_path():
    assert load_review_model_answer(ROOT, "../data") is None
    assert load_review_model_answer(ROOT, "nyquist_stability_criterion_gain_phase_margin") is None
    assert review_model_answer_messages({}) == []
    assert review_model_answer_messages({"review_model_answer": {"score_effect": "grading"}}) == []


def test_manual_telegram_review_displays_answer_and_preserves_review_done():
    messages = []
    with TemporaryDirectory(prefix="review-model-answer-") as directory:
        data = Path(directory)
        with patch.object(bot, "BASE_DIR", ROOT), \
             patch.object(bot, "DATA_DIR", data), \
             patch.dict(os.environ, {"TRAINING_HISTORY_DB": str(data / "history.sqlite3")}), \
             patch.object(bot, "send_message", side_effect=lambda _id, message: messages.append(message)):
            bot.handle_text({"text": f"/review {TOPIC}"}, 8675309, {})
            output = "\n".join(messages)
            assert "요청 주제 복습" in output
            assert "학습용 모범답안" in output
            assert "최저 압력" in output
            assert "복습 후 /review done " + TOPIC in output

            messages.clear()
            bot.handle_text({"text": f"/review done {TOPIC}"}, 8675309, {})
            assert "복습 완료" in "\n".join(messages)
