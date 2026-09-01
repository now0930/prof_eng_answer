from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import bot
from grade_output_summarizer import summarize_grade_for_telegram
from logic_check_evaluator import evaluate_logic_checks
from question_type_coverage_adapter import (
    attach_question_type_coverage_feedback,
)
from sil_relation_integrity import SIL_TARGET_TOPIC_ID
from verdict_consistency import enforce_final_decision_consistency


FIXTURE = REPO / "calibration" / (
    "sil_target_operations_overgrading_regression.json"
)


def fixture() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def fatal_grade() -> dict[str, object]:
    data = fixture()
    statuses = data["expected"]["original"]["demand_status"]
    rows = [
        {
            "requirement_id": requirement_id,
            "requirement": requirement_id,
            "status": status,
            "mentioned": status != "missing",
            "evidence": "fixture" if status != "missing" else "",
            "is_core": True,
        }
        for requirement_id, status in statuses.items()
    ]
    logic = evaluate_logic_checks(
        data["original_answer"],
        {"logic_check_topic_id": SIL_TARGET_TOPIC_ID},
    )
    grade = {
        "total_score": 13.52,
        "max_score": 25.0,
        "score_range": "13.0~14.0",
        "confidence": "high",
        "grade_confidence": "high",
        "confidence_level": "high",
        "official_pass_score": 15.0,
        "practical_target_score": 17.5,
        "high_score_target": 20.0,
        "official_pass_met": True,
        "practical_target_met": True,
        "high_score_met": True,
        "verdict": "strong",
        "summary": (
            "SIL 결정 방법론과 최신 이슈 연계가 매우 우수하며 "
            "핵심 관계식과 PFH/PFD 설명이 정확합니다."
        ),
        "overall_comment": "요구사항 충족률 100%, 전체 판정 strong",
        "rater_summary": "핵심 Fact가 정확하여 3인 모두 합격 판정",
        "rater_results": [
            {
                "rater_name": "교수",
                "total_score": 18.0,
                "max_score": 25.0,
                "official_pass_score": 15.0,
                "practical_target_score": 17.5,
                "high_score_target": 20.0,
                "official_pass_met": True,
                "practical_target_met": True,
                "high_score_met": True,
            }
        ],
        "logic_check_evaluation": logic,
        "question_type_coverage": {
            "question_type": "IMPLEMENTATION_EVALUATION",
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {
                "requirements": rows,
            },
        },
        "general_evidence_contract": {
            "defects": [],
        },
    }
    return attach_question_type_coverage_feedback(grade)


def test_final_json_caps_confidence_and_removes_false_praise() -> None:
    result = enforce_final_decision_consistency(fatal_grade())

    assert result["confidence"] == "medium"
    assert result["grade_confidence"] == "medium"
    assert result["confidence_level"] == "medium"
    assert result["confidence_ceiling"] == "medium"
    assert result["passing_score_allowed"] is False
    assert result["strong_verdict_allowed"] is False
    assert result["requirements_full_credit_allowed"] is False
    assert result["verdict"] == "검증된 핵심 기술 오류 보완 필요"
    assert "매우 우수" not in result["summary"]
    assert "정확합니다" not in result["summary"]
    coverage = result["question_type_coverage_summary"]
    assert coverage["overall_coverage"] == "weak"
    assert coverage["correctness_coverage_percent"] == 25.0
    assert coverage["full_credit_allowed"] is False


def test_compact_telegram_overrides_llm_strong_claims() -> None:
    malicious_summary = json.dumps(
        {
            "headline": "strong",
            "overall": "요구사항 100% 충족, 핵심 Fact가 정확합니다.",
            "key_reasons": ["SIL 관계식이 정확하고 우수함"],
            "section_basis": ["D/E만 보완하면 됨"],
            "improvements": ["IEC 표준만 추가"],
        },
        ensure_ascii=False,
    )
    text = summarize_grade_for_telegram(
        fatal_grade(),
        call_ollama_fn=lambda _prompt: malicious_summary,
    )

    assert text is not None
    assert "신뢰도: medium" in text
    assert "판정: 검증된 핵심 기술 오류 보완 필요" in text
    assert "목표 PFDavg" in text
    assert "전체 판정 strong" not in text
    assert "100% 충족" not in text
    assert "관계식이 정확하고 우수" not in text


def test_deterministic_telegram_shows_separate_coverage_metrics() -> None:
    with patch.dict(
        os.environ,
        {"GRADE_OUTPUT_LLM_SUMMARY": "0"},
    ):
        text = bot.format_result(fatal_grade())

    assert "신뢰도: medium" in text
    assert "공식 합격선: 15점 (미달)" in text
    assert "실전 목표선: 17.5점 (미달)" in text
    assert "고득점 기준: 20점 (미달)" in text
    assert "요구사항 언급률: 87.5%" in text
    assert "요구사항 정확 충족률: 25.0%" in text
    assert "오답 3" in text
    assert "전체 판정: weak" in text
    assert "요구사항 충족률: 100%" not in text
    assert "전체 판정: strong" not in text
    assert "공식 15점: 달성" not in text
    assert "실전 17.5점: 달성" not in text
    assert "핵심 Fact가 정확하여" not in text


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} SIL output checks")


if __name__ == "__main__":
    main()
