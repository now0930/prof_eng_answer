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
