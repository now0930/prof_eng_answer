from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grade_submission_normalizer import (
    attach_submission_normalization,
    normalize_grade_submission,
)
from grading_agents import (
    _phase2_build_canonical_submission_text,
    _phase2_extract_submission_context,
    _phase3_extract_answer_text,
    _phase3_extract_question_text,
    _phase8_run_originality_evaluator,
)
from grading_identity import build_grading_identity


SIL_SUBMISSION = """/grade
🚨 [안전 무결성] SIL 결정 방법 및 실제 플랜트 운영 / 최신 산업 이슈 연계
📌 문제 정의
SIL 결정 방법을 설명
이를 실제 플랜트 운영 및 최신 산업 이슈와 연계하여 설명
🔹 1. 배경 (Background)
왜 SIL을 사용해야 하는가?
SIS는 위험을 저감한다.
끝."""


def _evidence(result: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in result.items()
        if key not in {"normalized_text", "answer_text"}
    }


def test_problem_definition_shape_separates_question_and_answer() -> None:
    result = normalize_grade_submission(SIL_SUBMISSION)
    boundary = result["question_answer_boundary"]

    assert "SIL 결정 방법을 설명" in result["question_text"]
    assert "왜 SIL을 사용" not in result["question_text"]
    assert result["answer_text"].startswith("🔹 1. 배경")
    assert boundary["status"] == "problem_definition_body_marker"
    assert boundary["question_answer_separated"] is True
    assert boundary["manual_review_required"] is False


def test_unknown_boundary_is_answer_only_and_fail_closed() -> None:
    source = "배경과 원리를 설명한다.\n현장 대책을 제안한다."
    result = normalize_grade_submission(source)
    boundary = result["question_answer_boundary"]

    assert result["question_text"] == ""
    assert result["answer_text"] == source
    assert boundary["status"] == "unknown_answer_only"
    assert boundary["question_answer_separated"] is False
    assert boundary["manual_review_required"] is True
    assert boundary["confidence_ceiling"] == "medium"


def test_legacy_leading_question_sentence_is_separated() -> None:
    source = (
        "PID 제어기의 튜닝 순서와 각 게인의 영향을 설명하시오.\n\n"
        "PID 튜닝은 P, I, D의 영향을 함께 확인한다."
    )
    result = normalize_grade_submission(source)

    assert result["question_text"].startswith("PID 제어기의 튜닝 순서")
    assert result["answer_text"].startswith("PID 튜닝은")
    assert result["question_answer_boundary"]["status"] == "leading_question_sentence"


def test_legacy_standalone_problem_marker_uses_first_body_heading() -> None:
    source = """## 문제
레이더 액위계의 FMCW와 펄스 방식을 비교하고 신뢰성 확보방안을 설명
## 1. 배경: Radar
레이더는 반사파로 거리를 측정한다.
"""
    result = normalize_grade_submission(source)

    assert result["question_text"].startswith("레이더 액위계")
    assert result["answer_text"].startswith("## 1. 배경")
    assert result["question_answer_boundary"]["status"] == (
        "standalone_question_marker_body_heading"
    )


def test_legacy_multiline_scope_before_body_heading_is_separated() -> None:
    source = """공압식 밸브의 불평형력과 마찰력 개념 설명.
Fail Safe 동작을 위한 Spring 설계 기준 제시
## 1. 배경
밸브에는 여러 힘이 작용한다.
"""
    result = normalize_grade_submission(source)

    assert "불평형력" in result["question_text"]
    assert "Spring 설계 기준" in result["question_text"]
    assert result["answer_text"].startswith("## 1. 배경")
    assert result["question_answer_boundary"]["status"] == (
        "leading_question_scope_body_heading"
    )


def test_legacy_serialized_pattern_before_body_heading_is_separated() -> None:
    source = """{'pattern': '가동부에 작용하는 힘을 설명하시오.', 'intent': '힘 평형'}

## 1. 개요
가동부 자유물체도를 작성한다.
"""
    result = normalize_grade_submission(source)

    assert result["question_text"] == "가동부에 작용하는 힘을 설명하시오."
    assert result["answer_text"].startswith("## 1. 개요")
    assert result["question_answer_boundary"]["status"] == (
        "serialized_question_pattern_body_heading"
    )


def test_legacy_answer_title_recovers_only_explicit_scope() -> None:
    source = """Telegram 길이에 맞춰 정리한 모범 답안입니다.

---

[답안] 밸브 불평형력, 마찰력 및 Fail-Safe 스프링 설계 기준

1. 개요
밸브는 힘의 평형으로 동작한다.
"""
    result = normalize_grade_submission(source)

    assert result["question_text"].startswith("밸브 불평형력")
    assert result["answer_text"].startswith("1. 개요")
    assert result["question_answer_boundary"]["status"] == (
        "answer_title_scope_body_heading"
    )
    assert result["question_answer_boundary"]["confidence"] == "medium"


def test_phase2_has_no_legacy_question_equals_answer_fallback() -> None:
    source = "배경과 원리를 설명한다.\n현장 대책을 제안한다."
    question, answer = _phase2_extract_submission_context(source)

    assert question == ""
    assert answer == source
    assert question != answer


def test_all_legacy_consumers_receive_the_same_canonical_envelope() -> None:
    question, answer = _phase2_extract_submission_context(SIL_SUBMISSION)
    canonical = _phase2_build_canonical_submission_text(question, answer)

    assert _phase3_extract_question_text(canonical).strip() == question.strip()
    assert _phase3_extract_answer_text(canonical).strip() == answer.strip()

    identity = build_grading_identity(question, answer).to_dict()
    assert identity["normalized_question"] == question.strip()
    assert identity["normalized_answer"] == answer.strip()
    assert identity["normalized_question"] != identity["normalized_answer"]


def test_unknown_boundary_caps_confidence_and_positive_verdicts() -> None:
    result = normalize_grade_submission("답안 본문만 존재한다.")
    grade = {
        "confidence": "high",
        "grade_confidence": "high",
        "confidence_level": "high",
        "strong_verdict_allowed": True,
        "requirements_full_credit_allowed": True,
        "question_type_locked": True,
        "question_type_status": "locked",
    }
    updated = attach_submission_normalization(grade, _evidence(result))

    assert updated["confidence"] == "medium"
    assert updated["grade_confidence"] == "medium"
    assert updated["confidence_level"] == "medium"
    assert updated["manual_review_required"] is True
    assert updated["strong_verdict_allowed"] is False
    assert updated["requirements_full_credit_allowed"] is False
    assert updated["question_type_locked"] is False
    assert updated["question_type_status"] == "provisional"


def test_confirmed_boundary_preserves_high_confidence() -> None:
    result = normalize_grade_submission(
        "문제: SIL 결정 방법을 설명하시오.\n답안:\n위험 저감량으로 결정한다."
    )
    grade = {
        "confidence": "high",
        "strong_verdict_allowed": True,
        "requirements_full_credit_allowed": True,
    }
    updated = attach_submission_normalization(grade, _evidence(result))

    assert updated["confidence"] == "high"
    assert updated["strong_verdict_allowed"] is True
    assert updated["requirements_full_credit_allowed"] is True
    assert "manual_review_required" not in updated


def test_originality_evaluator_keeps_public_input_text_contract() -> None:
    import inspect

    parameters = inspect.signature(
        _phase8_run_originality_evaluator
    ).parameters
    assert "input_text" in parameters
    assert "canonical_input_text" not in parameters


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} boundary regression checks")


if __name__ == "__main__":
    main()
