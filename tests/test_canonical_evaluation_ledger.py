from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation_ledger import (
    attach_canonical_evaluation_ledger,
    build_canonical_evaluation_ledger,
)
from question_demand_contract import (
    build_question_demand_contract,
)


VMODEL_QUESTION = """🚨 [제어 소프트웨어] 개발 수명 주기(V-Model) 기반 SW 검증 방안
📌 문제 정의
제어 소프트웨어 개발 수명 주기(V-Model)의 단위 시험, 통합 시험, 시스템 시험의 정의
안전 무결성 기준(SIL) 달성을 위한 소프트웨어 검증 방안"""


def _grade() -> dict:
    contract = build_question_demand_contract(VMODEL_QUESTION)
    requirements = contract["requirements"]
    coverage_rows = []
    statuses = ["present", "partial", "missing", "present"]
    for row, status in zip(requirements, statuses):
        coverage_rows.append({
            "requirement_id": row["requirement_id"],
            "requirement": row["requirement_text"],
            "status": status,
            "evidence": f"evidence:{status}",
        })
    return {
        "total_score": 14.3,
        "layer_scores": [{"layer": "B", "score": 4.0}],
        "question_demand_contract": contract,
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": coverage_rows,
            }
        },
    }


def test_vmodel_has_one_ledger_row_per_atomic_requirement() -> None:
    ledger = build_canonical_evaluation_ledger(_grade())
    assert len(ledger["rows"]) == 4
    assert [row["requirement_index"] for row in ledger["rows"]] == [1, 2, 3, 4]
    assert ledger["summary"]["status_counts"] == {
        "unknown": 0,
        "correct": 2,
        "partial": 1,
        "missing": 1,
        "incorrect": 0,
    }


def test_verified_defect_is_canonical_correctness_owner() -> None:
    grade = _grade()
    requirement_id = grade["question_demand_contract"]["requirements"][0]["requirement_id"]
    grade["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "fatal-001",
            "defect_type": "correctness_error",
            "severity": "fatal",
            "owner_layer": "C",
            "requirement_id": requirement_id,
            "explanation": "핵심 정의가 반대임",
        }]
    }
    ledger = build_canonical_evaluation_ledger(grade)
    row = ledger["rows"][0]
    assert row["status"] == "incorrect"
    assert row["status_owner"] == "verified_defect"
    assert row["score_ownership"] == {
        "completeness": "B",
        "correctness": "C",
        "double_deduction_allowed": False,
    }
    assert row["conflict"] is True


def test_unassessed_requirement_never_becomes_false_100_percent() -> None:
    grade = _grade()
    rows = grade["question_type_coverage"]["explicit_requirement_coverage"]["requirements"]
    rows.pop()
    ledger = build_canonical_evaluation_ledger(grade)
    assert ledger["status"] == "incomplete"
    assert ledger["summary"]["status_counts"]["unknown"] == 1
    assert ledger["summary"]["exact_requirement_fulfillment_ratio"] is None
    assert ledger["summary"]["exact_requirement_fulfillment_percent"] is None


def test_native_question_demand_projection_fills_empty_semantic_coverage() -> None:
    grade = _grade()
    requirements = grade["question_demand_contract"]["requirements"]
    grade["question_type_coverage"]["explicit_requirement_coverage"][
        "requirements"
    ] = []
    grade["native_question_demand_projection_v1"] = {
        "states": [
            {
                "demand_id": row["requirement_id"],
                "text": row["requirement_text"],
                "state": state,
            }
            for row, state in zip(requirements, [3, 2, 1, 0])
        ]
    }
    ledger = build_canonical_evaluation_ledger(grade)
    assert [row["status"] for row in ledger["rows"]] == [
        "correct", "partial", "partial", "missing",
    ]
    assert ledger["status"] == "complete"


def test_missing_contract_fails_closed_as_unavailable() -> None:
    ledger = build_canonical_evaluation_ledger({"total_score": 20.0})
    assert ledger["status"] == "unavailable"
    assert ledger["reason"] == "question_demand_contract_missing"
    assert ledger["rows"] == []


def test_attachment_builds_contract_from_normalized_question() -> None:
    grade = attach_canonical_evaluation_ledger(
        {"total_score": 12.0},
        question_text="V-Model과 단위·통합·시스템 시험을 설명하시오.",
    )
    assert grade["question_demand_contract"]["requirements"]
    assert grade["canonical_evaluation_ledger"]["status"] == "incomplete"
    assert len(grade["canonical_evaluation_ledger"]["rows"]) == 4


def test_deterministic_logic_finding_projects_to_referenced_demands() -> None:
    grade = _grade()
    grade.pop("general_evidence_contract", None)
    requirement_id = grade["question_demand_contract"]["requirements"][1][
        "requirement_id"
    ]
    grade["logic_check_evaluation"] = {
        "findings": [{
            "rule_id": "fatal_relation",
            "severity": "fatal",
            "demand_refs": [requirement_id],
            "evidence_trust_tier": "DETERMINISTIC",
            "message": "관계식 오류",
        }],
    }
    ledger = build_canonical_evaluation_ledger(grade)
    rows = {row["requirement_id"]: row for row in ledger["rows"]}
    assert rows[requirement_id]["status"] == "incorrect"
    assert rows[requirement_id]["status_owner"] == "verified_defect"


def test_unreferenced_defect_links_by_unique_exact_demand_phrase() -> None:
    grade = _grade()
    requirements = grade["question_demand_contract"]["requirements"]
    unit = next(row for row in requirements if "단위 시험" in row["requirement_text"])
    integration = next(
        row for row in requirements if "통합 시험" in row["requirement_text"]
    )
    unit["object_text"] = "단위 시험"
    integration["object_text"] = "통합 시험"
    grade["logic_check_evaluation"] = {
        "findings": [{
            "rule_id": "fatal_unit_category_error",
            "severity": "fatal",
            "message": "MISRA를 단위시험 도구로 잘못 분류한다.",
            "evidence": "단위시험 도구: MISRA",
        }],
    }
    ledger = build_canonical_evaluation_ledger(grade)
    rows = {row["requirement_id"]: row for row in ledger["rows"]}
    assert rows[unit["requirement_id"]]["status"] == "incorrect"
    assert rows[integration["requirement_id"]]["status"] != "incorrect"


def test_unreferenced_defect_links_by_unique_two_token_overlap() -> None:
    grade = _grade()
    requirements = grade["question_demand_contract"]["requirements"]
    requirements[0]["requirement_text"] = "요구 RRF와 목표 SIL 계산"
    requirements[1]["requirement_text"] = "PFDavg 계산과 차원 일관성 검증"
    grade["general_evidence_contract"] = {
        "defects": [{
            "defect_id": "fatal_dimension",
            "defect_type": "correctness_error",
            "severity": "fatal",
            "owner_layer": "C",
            "evidence_text": "PFDavg와 고장률의 차원이 다르다.",
            "explanation": "PFDavg 계산에서 차원 오류가 있다.",
        }]
    }
    ledger = build_canonical_evaluation_ledger(grade)
    rows = {row["requirement_id"]: row for row in ledger["rows"]}
    assert rows[requirements[1]["requirement_id"]]["status"] == "incorrect"
    assert rows[requirements[0]["requirement_id"]]["status"] != "incorrect"


def test_ambiguous_unreferenced_defect_stays_unresolved() -> None:
    grade = _grade()
    requirements = grade["question_demand_contract"]["requirements"]
    requirements[0]["requirement_text"] = "정적 분석 검증"
    requirements[1]["requirement_text"] = "동적 분석 검증"
    grade["logic_check_evaluation"] = {
        "findings": [{
            "rule_id": "fatal_generic_analysis",
            "severity": "fatal",
            "message": "분석 검증의 기술관계가 틀렸다.",
        }],
    }
    ledger = build_canonical_evaluation_ledger(grade)
    assert all(row["status"] != "incorrect" for row in ledger["rows"])
    assert ledger["summary"]["unresolved_verified_defect_count"] == 1


def test_unmatched_coverage_is_auditable_not_silently_counted() -> None:
    grade = _grade()
    rows = grade["question_type_coverage"]["explicit_requirement_coverage"]["requirements"]
    rows.append({
        "requirement_id": "invented-axis",
        "requirement": "문제에 없는 임의 축",
        "status": "present",
    })
    ledger = build_canonical_evaluation_ledger(grade)
    assert ledger["summary"]["unmatched_coverage_count"] == 1
    assert ledger["unmatched_coverage"][0]["requirement_id"] == "invented-axis"


def test_attachment_is_idempotent_and_score_neutral() -> None:
    grade = _grade()
    before = copy.deepcopy({
        "total_score": grade["total_score"],
        "layer_scores": grade["layer_scores"],
    })
    once = attach_canonical_evaluation_ledger(grade)
    twice = attach_canonical_evaluation_ledger(once)
    assert once["canonical_evaluation_ledger"] == twice["canonical_evaluation_ledger"]
    assert {
        "total_score": twice["total_score"],
        "layer_scores": twice["layer_scores"],
    } == before


def test_public_display_uses_ledger_and_blocks_false_strong_100() -> None:
    import bot

    grade = _grade()
    coverage_rows = grade["question_type_coverage"]["explicit_requirement_coverage"]["requirements"]
    coverage_rows.pop()
    grade["question_type_coverage_summary"] = {
        "question_type": "IMPLEMENTATION_EVALUATION",
        "overall_coverage": "strong",
        "sub_criteria_total": 4,
        "sub_criteria_present": 4,
        "weighted_coverage_score": 4,
        "weighted_coverage_percent": 100.0,
        "correctness_coverage_percent": 100.0,
    }
    grade = attach_canonical_evaluation_ledger(grade)
    text = bot._format_question_type_coverage_display(grade)
    assert "전체 판정: unknown" in text
    assert "요구사항 정확 충족률: -" in text
    assert "미평가 1" in text
    assert "100.0%" not in text


def test_common_final_boundary_persists_canonical_ledger() -> None:
    import grading_agents

    result = grading_agents._stage17e5_finalize_pipeline_result(
        _grade(),
        {
            "question_answer_boundary": {
                "manual_review_required": False,
            }
        },
    )
    assert result["canonical_evaluation_ledger"]["marker"] == (
        "CANONICAL_EVALUATION_LEDGER_V1"
    )
    assert len(result["canonical_evaluation_ledger"]["rows"]) == 4


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"CANONICAL_EVALUATION_LEDGER_TESTS={len(tests)}_PASS")
