from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import patch

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier_module
import question_type_coverage_adapter as coverage_adapter
from grade_score_reconciler import (
    reconcile_grade_score,
)


SESSION_ID = "20260822_092545_5960502198"
HFT_ID = "sw05_fatal_hft_is_integration_test"
RANDOM_ID = (
    "sw05_fatal_software_test_is_"
    "random_hardware_integrity"
)
ACTUAL_RAW_RESPONSE = {
    "voting_mapping_wrong": False,
    "hft_mapping_wrong": True,
    "random_integrity_mapping_wrong": True,
    "sil_expansion_wrong": False,
    "correct_sil_control_wrong": False,
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


def _root_rows(grade):
    coverage = grade.get(
        "question_type_coverage"
    )
    if not isinstance(coverage, dict):
        return []
    rows = coverage.get(
        "sub_criteria_coverage"
    )
    return (
        rows
        if isinstance(rows, list)
        else []
    )


def _summary_rows(grade):
    coverage = grade.get(
        "question_type_coverage_summary"
    )
    if not isinstance(coverage, dict):
        return []
    rows = coverage.get(
        "criteria_status_rows"
    )
    return (
        rows
        if isinstance(rows, list)
        else []
    )


def _criterion_map(rows):
    return {
        str(
            row.get("criterion")
            or row.get("demand_id")
            or ""
        ): row
        for row in rows
        if isinstance(row, dict)
    }


def test_stage25g3g1_actual_session_only_direct_hft_row_is_wrong():
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

    repaired = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            reconciled
        )
    )

    root = _criterion_map(
        _root_rows(repaired)
    )
    summary = _criterion_map(
        _summary_rows(repaired)
    )

    expected_criteria = {
        "background_need",
        "classification_axis",
        "structure_features",
        "comparison_axis",
        "pros_cons_limits",
        "application_conditions",
        "selection_judgement",
    }
    assert set(root) == expected_criteria
    assert set(summary) == expected_criteria

    assert root[
        "application_conditions"
    ]["status"] == "wrong"
    assert summary[
        "application_conditions"
    ]["status"] == "wrong"

    root_meta = root[
        "application_conditions"
    ]["fatal_logic_reclassification"]
    summary_meta = summary[
        "application_conditions"
    ]["fatal_logic_reclassification"]

    assert root_meta["finding_ids"] == [
        HFT_ID
    ]
    assert summary_meta["finding_ids"] == [
        HFT_ID
    ]
    assert root_meta["matched_tokens"] == [
        "hft"
    ]
    assert summary_meta["matched_tokens"] == [
        "hft"
    ]

    for criterion in sorted(
        expected_criteria
        - {"application_conditions"}
    ):
        assert (
            str(
                root[criterion].get(
                    "status"
                )
                or ""
            ).lower()
            != "wrong"
        )
        assert (
            "fatal_logic_reclassification"
            not in root[criterion]
        )
        assert (
            str(
                summary[criterion].get(
                    "status"
                )
                or ""
            ).lower()
            != "wrong"
        )
        assert (
            "fatal_logic_reclassification"
            not in summary[criterion]
        )

    meta = repaired[
        "fatal_coverage_consistency"
    ]
    assert meta[
        "reclassified_row_count"
    ] == 1
    assert meta[
        "reclassified_physical_row_count"
    ] == 2
    assert meta[
        "match_strategy"
    ] == (
        "stage25g3g1_direct_relation_"
        "anchor_v1"
    )
    assert meta["score_effect"] == "none"


def test_stage25g3g1_random_hardware_phrase_matches_exact_row():
    grade = {
        "logic_check_evaluation": {
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": RANDOM_ID,
                    "severity": "fatal",
                    "message": (
                        "software test를 Random "
                        "Hardware Integrity와 "
                        "직접 대응시킨 오류"
                    ),
                }
            ],
        },
        "question_type_coverage": {
            "sub_criteria_coverage": [
                {
                    "criterion": (
                        "random_integrity_axis"
                    ),
                    "status": "partial",
                    "evidence": (
                        "Random Hardware Integrity "
                        "대응축을 제시함"
                    ),
                },
                {
                    "criterion": "sil_context",
                    "status": "present",
                    "evidence": (
                        "SIL 달성 방안을 설명함"
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
    rows = _criterion_map(
        _root_rows(result)
    )
    assert rows[
        "random_integrity_axis"
    ]["status"] == "wrong"
    assert rows[
        "random_integrity_axis"
    ][
        "fatal_logic_reclassification"
    ]["finding_ids"] == [RANDOM_ID]
    assert rows[
        "sil_context"
    ]["status"] == "present"
    assert (
        "fatal_logic_reclassification"
        not in rows["sil_context"]
    )


def test_stage25g3g1_hft_finding_rejects_integration_test_side():
    finding = {
        "id": HFT_ID,
        "severity": "fatal",
        "message": (
            "통합시험을 HFT와 직접 대응시킨 오류"
        ),
    }

    anchors = (
        coverage_adapter
        ._stage25g3g1_finding_direct_anchors(
            finding
        )
    )
    assert anchors == ["hft"]
    assert "integration test" not in anchors

    matched, matched_anchors = (
        coverage_adapter
        ._stage25g3g_row_match(
            {
                "criterion": "classification_axis",
                "status": "present",
                "evidence": (
                    "unit test, integration test, "
                    "system test로 구분함"
                ),
            },
            finding,
            {},
        )
    )
    assert matched is False
    assert matched_anchors == []


def test_stage25g3g1_random_finding_does_not_inherit_hft_from_context():
    finding = {
        "id": RANDOM_ID,
        "severity": "fatal",
        "message": (
            "software test를 Random Hardware "
            "Integrity와 직접 대응시킨 오류"
        ),
        "profile_context": (
            "공통 프로파일에는 HFT와 SIL도 "
            "함께 설명되어 있음"
        ),
    }

    anchors = (
        coverage_adapter
        ._stage25g3g1_finding_direct_anchors(
            finding
        )
    )
    assert anchors == [
        "random hardware integrity"
    ]
    assert "hft" not in anchors
    assert "software test" not in anchors

    matched, matched_anchors = (
        coverage_adapter
        ._stage25g3g_row_match(
            {
                "criterion": "application_conditions",
                "status": "partial",
                "evidence": "SIL 3/4 및 HFT 조건을 언급",
            },
            finding,
            {},
        )
    )
    assert matched is False
    assert matched_anchors == []


def test_stage25g3g1_generic_sil_model_system_tokens_do_not_match():
    finding = {
        "id": HFT_ID,
        "severity": "fatal",
        "message": (
            "통합시험을 HFT와 직접 "
            "대응시킨 오류"
        ),
    }
    rows = [
        {
            "criterion": "background_need",
            "status": "present",
            "evidence": (
                "V-Model과 SIL의 배경을 설명"
            ),
        },
        {
            "criterion": "classification_axis",
            "status": "present",
            "evidence": (
                "단위, 통합, 시스템 시험으로 분류"
            ),
        },
        {
            "criterion": "structure_features",
            "status": "present",
            "evidence": (
                "각 시험 단계별 검증 대상을 설명"
            ),
        },
    ]

    for row in rows:
        matched, anchors = (
            coverage_adapter
            ._stage25g3g_row_match(
                row,
                finding,
                {},
            )
        )
        assert matched is False
        assert anchors == []


def test_stage25g3g1_reconciliation_is_idempotent():
    grade = {
        "logic_check_evaluation": {
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": HFT_ID,
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
                    "criterion": (
                        "application_conditions"
                    ),
                    "status": "partial",
                    "evidence": (
                        "HFT 조건을 언급함"
                    ),
                }
            ]
        },
    }

    first = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            copy.deepcopy(grade)
        )
    )
    second = (
        coverage_adapter
        .attach_question_type_coverage_feedback(
            first
        )
    )

    root = _criterion_map(
        _root_rows(second)
    )
    metadata = root[
        "application_conditions"
    ]["fatal_logic_reclassification"]

    assert metadata["original_status"] == (
        "partial"
    )
    assert metadata["finding_ids"] == [
        HFT_ID
    ]
    assert metadata["matched_tokens"] == [
        "hft"
    ]

    meta = second[
        "fatal_coverage_consistency"
    ]
    assert meta[
        "reclassified_row_count"
    ] == 1
    assert meta[
        "reclassified_physical_row_count"
    ] == 2
