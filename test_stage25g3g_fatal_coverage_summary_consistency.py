from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import patch

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier_module
import question_type_coverage_adapter as coverage_adapter
import verdict_consistency
from grade_score_reconciler import (
    reconcile_grade_score,
)


PRIMARY_TOPIC = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)
SESSION_ID = "20260822_092545_5960502198"

ACTUAL_RAW_RESPONSE = {
    "voting_mapping_wrong": False,
    "hft_mapping_wrong": True,
    "random_integrity_mapping_wrong": True,
    "sil_expansion_wrong": False,
    "correct_sil_control_wrong": False,
}
EXPECTED_FATAL_IDS = {
    "sw05_fatal_hft_is_integration_test",
    "sw05_fatal_software_test_is_random_hardware_integrity",
}


def _repo() -> Path:
    return Path(__file__).resolve().parent


def _actual_session():
    session = (
        _repo()
        / "data"
        / "sessions"
        / SESSION_ID
    )
    text = (
        session / "input.raw.txt"
    ).read_text(encoding="utf-8")
    grade = json.loads(
        (session / "grade.json").read_text(
            encoding="utf-8"
        )
    )
    return text, grade


def _coverage_rows(
    grade: dict,
) -> list[dict]:
    rows = []
    for container_name, row_key in (
        (
            "question_type_coverage",
            "sub_criteria_coverage",
        ),
        (
            "question_type_coverage_summary",
            "criteria_status_rows",
        ),
    ):
        container = grade.get(container_name)
        if not isinstance(container, dict):
            continue
        raw_rows = container.get(row_key)
        if isinstance(raw_rows, list):
            rows.extend(
                row
                for row in raw_rows
                if isinstance(row, dict)
            )
    return rows


def _related_rows(
    grade: dict,
) -> list[dict]:
    terms = (
        "HFT",
        "Architectural Constraints",
        "Random Hardware Integrity",
        "하드웨어 결함허용도",
    )
    return [
        row
        for row in _coverage_rows(grade)
        if any(
            term.casefold()
            in str(
                row.get("evidence")
                or row.get("criterion")
                or ""
            ).casefold()
            for term in terms
        )
    ]


def test_stage25g3g_actual_full_path_repairs_coverage_and_summary():
    text, baseline = _actual_session()
    compact_calls = []
    generic_calls = []

    def fake_compact(prompt, format_schema=None):
        compact_calls.append(
            (prompt, format_schema)
        )
        return copy.deepcopy(
            ACTUAL_RAW_RESPONSE
        )

    def forbidden_generic(*args, **kwargs):
        generic_calls.append(
            (args, kwargs)
        )
        raise AssertionError(
            "generic verifier must be skipped"
        )

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=fake_compact,
    ), patch.object(
        verifier_module,
        "verify_logic_with_llm",
        side_effect=forbidden_generic,
    ):
        logic_eval = evaluator.evaluate_logic_checks(
            answer_text=text,
            grade=copy.deepcopy(baseline),
        )

    assert len(compact_calls) == 1
    assert generic_calls == []

    fatal_ids = {
        str(row.get("id") or "")
        for row in logic_eval.get(
            "findings",
            [],
        )
        if isinstance(row, dict)
        and str(
            row.get("severity") or ""
        ).strip().lower()
        == "fatal"
    }
    assert fatal_ids == EXPECTED_FATAL_IDS
    assert logic_eval[
        "score_policy"
    ]["recommended_ceiling"] == 14.5

    projected = copy.deepcopy(baseline)
    projected[
        "logic_check_evaluation"
    ] = copy.deepcopy(logic_eval)
    projected["total_score"] = 14.5
    projected["final_total_score"] = 14.5
    projected[
        "total_score_before_logic_cap"
    ] = 15.25

    reconciler_calls = []

    def forbidden_reconciler(prompt):
        reconciler_calls.append(prompt)
        raise AssertionError(
            "reconciler LLM must not be called"
        )

    reconciled = reconcile_grade_score(
        parsed=projected,
        raw_text=text,
        call_llm_fn=forbidden_reconciler,
    )
    assert reconciler_calls == []
    assert reconciled["total_score"] == 14.5
    assert (
        reconciled["official_pass_met"]
        is False
    )

    coverage_result = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            copy.deepcopy(reconciled)
        )
    )
    related = _related_rows(
        coverage_result
    )
    assert len(related) >= 2
    assert all(
        str(
            row.get("status")
            or row.get("demand_state")
            or ""
        ).strip().lower()
        == "wrong"
        for row in related
    )
    assert all(
        isinstance(
            row.get(
                "fatal_logic_reclassification"
            ),
            dict,
        )
        for row in related
    )
    assert coverage_result[
        "question_type_coverage_summary"
    ]["sub_criteria_wrong"] >= 1
    assert coverage_result[
        "fatal_coverage_consistency"
    ]["reclassified_row_count"] >= 1

    final = (
        verdict_consistency
        .enforce_final_score_status_narrative_consistency(
            coverage_result
        )
    )
    assert final["total_score"] == 14.5
    assert final["final_total_score"] == 14.5
    assert final["official_pass_met"] is False
    for key in (
        "summary",
        "overall_comment",
    ):
        value = str(final.get(key) or "")
        assert "오답 또는 충돌" in value
        assert "충실히 다루" not in value
        assert "구조적으로 잘 서술" not in value


def test_stage25g3g_coverage_overlap_guard_preserves_unrelated_row():
    grade = {
        "logic_check_evaluation": {
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": (
                        "sw05_fatal_hft_"
                        "is_integration_test"
                    ),
                    "severity": "fatal",
                    "message": (
                        "통합시험을 HFT와 직접 "
                        "대응시킨 오류"
                    ),
                }
            ],
        },
        "question_type_coverage": {
            "sub_criteria_coverage": [
                {
                    "criterion": "SIL 검증 방안",
                    "status": "partial",
                    "evidence": (
                        "HFT 조건을 언급했으나 "
                        "설명이 축약됨"
                    ),
                },
                {
                    "criterion": "V-model 정의",
                    "status": "present",
                    "evidence": (
                        "개발과 시험의 추적성을 설명"
                    ),
                },
            ]
        },
    }

    result = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            copy.deepcopy(grade)
        )
    )
    rows = result[
        "question_type_coverage"
    ]["sub_criteria_coverage"]
    assert rows[0]["status"] == "wrong"
    assert rows[0]["demand_state"] == "WRONG"
    assert rows[1]["status"] == "present"
    assert (
        "fatal_logic_reclassification"
        not in rows[1]
    )


def test_stage25g3g_nonfatal_finding_does_not_reclassify_coverage():
    grade = {
        "logic_check_evaluation": {
            "fatal_error_detected": False,
            "findings": [
                {
                    "id": "minor_hft_wording",
                    "severity": "minor",
                    "message": "HFT 표현 보완",
                }
            ],
        },
        "question_type_coverage": {
            "sub_criteria_coverage": [
                {
                    "criterion": "SIL 검증 방안",
                    "status": "partial",
                    "evidence": "HFT 조건을 언급",
                }
            ]
        },
    }

    result = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            copy.deepcopy(grade)
        )
    )
    row = result[
        "question_type_coverage"
    ]["sub_criteria_coverage"][0]
    assert row["status"] == "partial"
    assert (
        "fatal_logic_reclassification"
        not in row
    )


def test_stage25g3g_summary_marker_extension_requires_conflict():
    positive = (
        "본 답안은 핵심 내용을 충실히 다루고 "
        "구조적으로 잘 서술하였습니다."
    )
    fatal_grade = {
        "total_score": 14.5,
        "final_total_score": 14.5,
        "official_pass_score": 15.0,
        "summary": positive,
        "overall_comment": positive,
        "logic_check_evaluation": {
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": "fatal_control",
                    "severity": "fatal",
                }
            ],
        },
    }
    repaired = (
        verdict_consistency
        .enforce_final_score_status_narrative_consistency(
            copy.deepcopy(fatal_grade)
        )
    )
    assert "오답 또는 충돌" in repaired["summary"]
    assert (
        "오답 또는 충돌"
        in repaired["overall_comment"]
    )

    clean_grade = {
        "total_score": 16.0,
        "final_total_score": 16.0,
        "official_pass_score": 15.0,
        "summary": positive,
        "overall_comment": positive,
        "logic_check_evaluation": {
            "fatal_error_detected": False,
            "findings": [],
        },
    }
    clean = (
        verdict_consistency
        .enforce_final_score_status_narrative_consistency(
            copy.deepcopy(clean_grade)
        )
    )
    assert clean["summary"] == positive
    assert clean["overall_comment"] == positive
