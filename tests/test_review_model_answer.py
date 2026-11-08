"""Regression: PR #18 study answer uses v2 provenance and cannot change grading."""

from __future__ import annotations

import copy
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import bot
from study.master_topic_pack import (
    load_master_topic_pack, project_grading, project_training,
)
from study.review_model_answer import load_review_model_answer, matches_question
from study.review_presentation import review_model_answer_messages

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "control_valve_cavitation_flashing_choked_flow_damage_prevention"


def test_review_model_answer_v2_is_provenance_bound_and_score_neutral():
    master = load_master_topic_pack(ROOT / "master_topic_packs" / f"{TOPIC}.json")
    grading_before = copy.deepcopy(project_grading(ROOT, master))
    training = project_training(ROOT, master)
    answer = training["review_model_answer"]

    assert answer["schema_version"] == "review-model-answer-v2"
    assert answer["topic_id"] == TOPIC
    assert answer["score_effect"] == "none"
    assert answer["review_status"] == "llm_reviewed_human_pending"
    assert len(answer["sections"]) >= 3
    assert answer["sources"]
    assert all(source["url"].startswith("https://") for source in answer["sources"])
    assert project_grading(ROOT, master) == grading_before
    assert "review_model_answer" not in grading_before["sources"]

    snapshot = copy.deepcopy(training)
    messages = review_model_answer_messages(training)
    rendered = "\n".join(messages)
    assert "학습용 모범답안" in rendered
    assert "사람 검토 대기" in rendered
    assert "베나 콘트랙타" in rendered
    assert "플래싱" in rendered
    assert "점수 영향 없음" in rendered
    assert all(len(message.encode("utf-16-le")) // 2 <= 3000 for message in messages)
    assert training == snapshot


def test_review_is_question_scoped_and_invalid_files_fail_closed():
    answer = load_review_model_answer(ROOT, TOPIC)
    assert answer is not None
    assert matches_question(answer, answer["question"])
    assert matches_question(answer, "문제: " + answer["question"] + " 답안: 베나 콘트랙타")
    assert not matches_question(answer, "계장 접지와 차폐의 설치 방법을 설명하시오.")
    assert load_review_model_answer(ROOT, "../data") is None
    assert load_review_model_answer(ROOT, "nyquist_stability_criterion_gain_phase_margin") is None
    assert review_model_answer_messages({}) == []
    assert review_model_answer_messages({"review_model_answer": {"score_effect": "grading"}}) == []


def test_telegram_review_reads_v2_without_mutating_grade_or_done_behavior():
    messages = []
    with TemporaryDirectory(prefix="review-model-answer-v2-") as directory:
        data = Path(directory)
        with patch.object(bot, "BASE_DIR", ROOT), \
             patch.object(bot, "DATA_DIR", data), \
             patch.dict(os.environ, {"TRAINING_HISTORY_DB": str(data / "history.sqlite3")}), \
             patch.object(bot, "send_message", side_effect=lambda _id, message: messages.append(message)):
            bot.handle_text({"text": f"/review {TOPIC}"}, 8675309, {})
            output = "\n".join(messages)
            assert "요청 주제 복습" in output
            assert "학습용 모범답안" in output
            assert "베나 콘트랙타" in output
            assert "검토 상태" in output
            assert "복습 후 /review done " + TOPIC in output

            messages.clear()
            bot.handle_text({"text": f"/review done {TOPIC}"}, 8675309, {})
            assert "복습 완료" in "\n".join(messages)
