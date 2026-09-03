from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading_agents import _stage17e5_finalize_pipeline_result
from verified_correctness_score_cap import apply_verified_correctness_score_cap
from verdict_consistency import enforce_final_score_status_narrative_consistency


QUESTION_TYPES = (
    "IMPLEMENTATION_EVALUATION",
    "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION",
    "PRINCIPLE_INTERPRETATION",
)


def _grade(total: float = 21.0, question_type: str = QUESTION_TYPES[0]) -> dict:
    return {
        "total_score": total,
        "final_total_score": total,
        "score": total,
        "final_score": total,
        "question_type": question_type,
        "canonical_evaluation_ledger": {
            "rows": [
                {"requirement_id": "core-1", "is_core": True, "status": "correct"},
                {"requirement_id": "noncore-1", "is_core": False, "status": "correct"},
            ],
        },
    }


def test_fatal_cap_is_question_type_neutral() -> None:
    for question_type in QUESTION_TYPES:
        grade = _grade(question_type=question_type)
        grade["logic_check_evaluation"] = {
            "findings": [{"rule_id": "fatal-rule", "severity": "fatal"}],
        }
        result = apply_verified_correctness_score_cap(grade)
        assert result["total_score"] == 14.5
        assert result["final_total_score"] == 14.5
        assert result["verified_correctness_score_cap"]["fatal_count"] == 1
        assert result["verified_correctness_score_cap"]["score_effect"] == "hard_cap"


def test_major_cap_requires_verified_core_linkage() -> None:
    grade = _grade()
    grade["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "major-core",
            "defect_type": "correctness_error",
            "severity": "major",
            "requirement_id": "core-1",
        }],
    }
    result = apply_verified_correctness_score_cap(grade)
    assert result["total_score"] == 17.4
    assert result["verified_correctness_score_cap"]["major_core_count"] == 1

    noncore = _grade()
    noncore["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "major-noncore",
            "defect_type": "correctness_error",
            "severity": "major",
            "requirement_id": "noncore-1",
        }],
    }
    unchanged = apply_verified_correctness_score_cap(noncore)
    assert unchanged["total_score"] == 21.0
    assert unchanged["verified_correctness_score_cap"]["policy_applicable"] is False


def test_unverified_or_noncorrectness_hints_never_trigger_cap() -> None:
    grade = _grade()
    grade["semantic_fact_check"] = {
        "severity": "fatal", "comment": "model-only assertion",
    }
    grade["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "style-only",
            "defect_type": "style_gap",
            "severity": "fatal",
        }],
    }
    result = apply_verified_correctness_score_cap(grade)
    assert result["total_score"] == 21.0
    assert result["verified_correctness_score_cap"]["policy_applicable"] is False


def test_applicable_but_already_low_score_is_not_reported_as_applied_cap() -> None:
    grade = _grade(total=13.0)
    grade["logic_check_evaluation"] = {
        "findings": [{"rule_id": "fatal-rule", "severity": "fatal"}],
    }
    result = apply_verified_correctness_score_cap(grade)
    assert result["total_score"] == 13.0
    assert result["verified_correctness_score_cap"]["score_effect"] == "none"
    assert result.get("applied_caps") in (None, [])


def test_legacy_applied_cap_history_is_preserved_across_policy_upgrade() -> None:
    grade = _grade(total=14.5)
    grade["logic_check_evaluation"] = {
        "findings": [{"rule_id": "fatal-rule", "severity": "fatal"}],
    }
    grade["verified_correctness_score_cap"] = {
        "version": "verified_correctness_score_cap_v1",
        "cap": 14.5,
        "source_ids": ["logic_check_evaluation.findings:fatal-rule"],
        "score_effect": "hard_cap",
        "original_total_score": 18.2,
    }
    result = apply_verified_correctness_score_cap(grade)
    assert result["verified_correctness_score_cap"]["score_effect"] == "hard_cap"
    assert result["verified_correctness_score_cap"]["preserved_prior_application"] is True
    assert result["applied_caps"][0]["type"] == "verified_correctness_score_cap"


def test_final_boundary_synchronizes_thresholds_after_fatal_cap() -> None:
    grade = _grade()
    grade["logic_check_evaluation"] = {
        "fatal_error_detected": True,
    }
    result = _stage17e5_finalize_pipeline_result(
        grade,
        {"question_text": "일반 문제", "question_answer_boundary": {}},
    )
    assert result["total_score"] == 14.5
    assert result["official_pass_met"] is False
    assert result["practical_target_met"] is False
    assert result["high_score_met"] is False


def test_unresolved_ledger_rewrites_global_accuracy_praise() -> None:
    result = enforce_final_score_status_narrative_consistency({
        "total_score": 14.0,
        "summary": "핵심 개념과 요구사항에 정확히 응답했습니다.",
        "canonical_evaluation_ledger": {
            "summary": {"status_counts": {"partial": 1, "correct": 3}},
        },
    })
    assert "정확히 응답" not in result["summary"]
    assert result["final_consistency_evaluation"]["conflict_sources"]


def test_formatter_reports_an_applied_verified_cap() -> None:
    from grade_output_summarizer import _build_payload, _normalise_summary, _render

    grade = _grade()
    grade["logic_check_evaluation"] = {
        "findings": [{"rule_id": "fatal-rule", "severity": "fatal"}],
        "fatal_error_detected": True,
    }
    grade = apply_verified_correctness_score_cap(grade)
    payload = _build_payload(grade)
    rendered = _render(_normalise_summary(None, payload), payload)
    assert "예상 점수대: 14.5점 cap 적용" in rendered
    assert "점수 상한이 적용되었습니다." in rendered
    assert "추가적인 수치 cap은 적용되지 않았습니다." not in rendered


def main() -> None:
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"VERIFIED_CORRECTNESS_SCORE_CAP_TESTS={len(tests)}_PASS")


if __name__ == "__main__":
    main()
