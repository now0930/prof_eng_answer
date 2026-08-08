#!/usr/bin/env python3
from __future__ import annotations

import copy

from hybrid_demand_scope_guard import (
    HYBRID_DEMAND_SCOPE_GUARD_MARKER,
    restore_blocked_semantic_layer_scores,
    sanitize_hybrid_originality_evaluation,
    sanitize_hybrid_semantic_evaluation,
)
from hybrid_demand_scope_guard import _demand_token_rows, _hybrid_evidence, _traceable
from hybrid_demand_scope_guard import project_hybrid_model_answer_feedback

TOPIC = (
    "strain_gauge_load_cell_"
    "wheatstone_bridge_temperature_compensation_error"
)


def hybrid_rubric():
    mappings = [
        ("D1", "PRIMARY", "스트레인 게이지의 측정 원리를 설명하시오."),
        ("D2", "PRIMARY", "로드셀의 측정 원리를 설명하시오."),
        ("D3", "PRIMARY", "Wheatstone Bridge 방법을 설명하시오."),
        ("D4", "PRIMARY", "온도 보상 방법을 설명하시오."),
        (
            "D5",
            "NONE",
            "계측설비의 교정·점검 기록에 대한 "
            "보존기간 결정 기준을 제시하시오.",
        ),
        (
            "D6",
            "NONE",
            "계측설비의 교정·점검 기록에 대한 "
            "폐기 원칙을 제시하시오.",
        ),
    ]
    return {
        "hybrid_general_grading_evidence": {
            "routing_mode": "SINGLE_TOPIC",
            "coverage_kind": "HYBRID_TOPIC_GENERAL",
            "primary_topic_ids": [TOPIC],
            "uncovered_demand_ids": ["D5", "D6"],
            "demand_mappings": [
                {
                    "demand_id": demand_id,
                    "role": role,
                    "topic_id": TOPIC,
                    "confidence": 1.0 if role == "PRIMARY" else 0.0,
                    "demand_text": demand_text,
                }
                for demand_id, role, demand_text in mappings
            ],
        }
    }


def semantic_eval():
    return {
        "ok": True,
        "raw_text": "RAW MUST REMAIN BYTE-FOR-BYTE",
        "parsed": {
            "overall_comment": (
                "온도 보상 방법의 구체성과 로드셀의 "
                "성능 오차 및 설치 고려사항이 부족함."
            ),
            "layers": [
                {
                    "layer_id": "A",
                    "score": 2.0,
                    "max": 3.0,
                    "reason": "구조가 명확함.",
                    "evidence": ["목차가 명확함."],
                },
                {
                    "layer_id": "B",
                    "score": 4.0,
                    "max": 6.0,
                    "reason": "모든 요구를 다룸.",
                    "evidence": ["요구사항에 응답함."],
                },
                {
                    "layer_id": "C",
                    "score": 5.0,
                    "max": 8.0,
                    "reason": "로드셀의 성능 오차(크리프, 히스테리시스)가 부족함.",
                    "evidence": [
                        "온도 보상 원리는 정확함.",
                        "로드셀 성능 오차 설명이 누락됨.",
                    ],
                },
                {
                    "layer_id": "D",
                    "score": 3.0,
                    "max": 6.0,
                    "reason": "로드셀 현장 설치 기준이 부족함.",
                    "evidence": ["편심하중과 과부하 방지 설치 기준이 누락됨."],
                },
                {
                    "layer_id": "E",
                    "score": 1.5,
                    "max": 2.0,
                    "reason": "논리 연결이 양호함.",
                    "evidence": ["전개가 자연스러움."],
                },
            ],
            "rater_comments": [
                {
                    "rater_id": "professor",
                    "comment": (
                        "온도 보상은 좋으나 로드셀 "
                        "성능 오차를 보완할 필요가 있음."
                    ),
                },
                {
                    "rater_id": "executive",
                    "comment": "기록 폐기 원칙과 승인 절차는 적절함.",
                },
            ],
            "improvement_advice": [
                "로드셀의 성능 오차(크리프, 히스테리시스)를 설명할 것.",
                "로드셀 설치 시 편심하중과 과부하 방지 기준을 제시할 것.",
                "온도 보상 시 더미 게이지와 자기온도보상 게이지 조건을 보완할 것.",
                "보존기간 결정 기준의 근거를 구체화할 것.",
            ],
            "question_type_coverage": {
                "sub_criteria_coverage": [
                    {
                        "criterion": "calculation_or_interpretation",
                        "status": "partial",
                        "evidence": "로드셀 성능 오차 해석이 부족함.",
                        "impact": "C 점수에 부정적",
                    },
                    {
                        "criterion": "result_meaning",
                        "status": "partial",
                        "evidence": "온도 보상 결과 설명이 부족함.",
                        "impact": "C 점수에 부정적",
                    },
                    {
                        "criterion": "field_judgement",
                        "status": "partial",
                        "evidence": "로드셀 설치 현장 판단이 누락됨.",
                        "impact": "D 점수에 부정적",
                    },
                ],
                "c_fact_focus_coverage": {
                    "covered": ["원리"],
                    "missing": ["성능 오차 해석", "온도 보상 결과"],
                },
                "d_field_judgement_focus_coverage": {
                    "covered": ["기록 관리"],
                    "missing": ["현장 설치 기준"],
                },
                "overall_coverage": "weak",
                "scoring_hint": "C 성능 오차와 D 현장 설치 기준 보완이 필요함.",
                "explicit_requirement_coverage": {
                    "requirements": [
                        {
                            "requirement": "온도 보상 방법 설명",
                            "status": "present",
                            "is_core": True,
                        },
                        {
                            "requirement": "보존기간 결정 기준",
                            "status": "present",
                            "is_core": True,
                        },
                    ]
                },
            },
            "layer_issue_ownership": [
                {
                    "issue_id": "performance",
                    "issue_type": "core_depth_gap",
                    "primary_owner_layer": "C",
                    "severity": "partial",
                    "reason": "로드셀의 성능 오차(크리프, 히스테리시스) 설명 부족",
                },
                {
                    "issue_id": "installation",
                    "issue_type": "core_depth_gap",
                    "primary_owner_layer": "D",
                    "severity": "partial",
                    "reason": "로드셀 설치 시 편심하중과 과부하 방지 기준 누락",
                },
                {
                    "issue_id": "temperature",
                    "issue_type": "core_depth_gap",
                    "primary_owner_layer": "C",
                    "severity": "partial",
                    "reason": "온도 보상 방법의 적용 조건 설명 부족",
                },
            ],
            "general_evidence_contract": {
                "defects": [
                    {
                        "defect_type": "core_depth_gap",
                        "owner_layer": "C",
                        "severity": "partial",
                        "explanation": (
                            "크리프와 히스테리시스 성능 오차 설명이 필요함."
                        ),
                    },
                    {
                        "defect_type": "core_depth_gap",
                        "owner_layer": "C",
                        "severity": "partial",
                        "explanation": "온도 보상 방법의 적용 조건이 부족함.",
                    },
                ]
            },
        },
    }


def originality_eval():
    return {
        "ok": True,
        "raw_text": "ORIGINALITY RAW MUST REMAIN",
        "parsed": {
            "raw_originality_score": 0.8,
            "improvement_advice": [
                "로드셀 설치 시 편심하중과 과부하를 보강할 것.",
                "기록 보존기간 결정 기준의 근거를 보강할 것.",
                "온도 보상 방법의 적용 조건을 구체화할 것.",
            ],
        },
    }


def main():
    rubric = hybrid_rubric()
    # GENERIC_ONE_TOKEN_COLLISION_ASSERTIONS_V1
    demand_rows = _demand_token_rows(
        _hybrid_evidence(rubric)
    )

    assert _traceable(
        "온도 보상 결과 설명이 부족함.",
        demand_rows,
    )
    assert _traceable(
        "보존기간 결정 기준의 근거를 구체화할 것.",
        demand_rows,
    )
    assert _traceable(
        "폐기 원칙의 승인 절차를 구체화할 것.",
        demand_rows,
    )

    assert not _traceable(
        "로드셀 현장 설치 기준이 부족함.",
        demand_rows,
    )
    assert not _traceable(
        "편심하중과 과부하 방지 설치 기준이 누락됨.",
        demand_rows,
    )
    assert not _traceable(
        "로드셀 성능 오차 해석이 부족함.",
        demand_rows,
    )

    semantic = semantic_eval()
    before = copy.deepcopy(semantic)
    sanitized = sanitize_hybrid_semantic_evaluation(semantic, rubric)

    assert semantic == before
    assert sanitized["raw_text"] == semantic["raw_text"]
    guard = sanitized["hybrid_demand_scope_guard"]
    assert guard["marker"] == HYBRID_DEMAND_SCOPE_GUARD_MARKER
    assert set(guard["blocked_layer_ids"]) == {"C", "D"}

    advice = sanitized["parsed"]["improvement_advice"]
    assert len(advice) == 2
    assert any("온도 보상" in item for item in advice)
    assert any("보존기간 결정 기준" in item for item in advice)
    assert all("크리프" not in item for item in advice)
    assert all("편심하중" not in item for item in advice)
    assert all("과부하" not in item for item in advice)

    issues = sanitized["parsed"]["layer_issue_ownership"]
    assert len(issues) == 1
    assert issues[0]["issue_id"] == "temperature"

    defects = sanitized["parsed"]["general_evidence_contract"]["defects"]
    assert len(defects) == 1
    assert "온도 보상" in defects[0]["explanation"]

    coverage = sanitized["parsed"]["question_type_coverage"]
    assert coverage["sub_criteria_coverage"][0]["status"] == "present"
    assert coverage["sub_criteria_coverage"][1]["status"] == "partial"
    assert coverage["sub_criteria_coverage"][2]["status"] == "present"
    assert coverage["c_fact_focus_coverage"]["missing"] == ["온도 보상 결과"]
    assert coverage["d_field_judgement_focus_coverage"]["missing"] == []

    layers = [
        {"layer_id": "A", "score": 1.5, "max": 3.0, "reason": ""},
        {"layer_id": "B", "score": 4.0, "max": 6.0, "reason": ""},
        {"layer_id": "C", "score": 5.0, "max": 8.0, "reason": ""},
        {"layer_id": "D", "score": 3.0, "max": 6.0, "reason": ""},
        {"layer_id": "E", "score": 1.5, "max": 2.0, "reason": ""},
    ]
    baseline = {"A": 1.5, "B": 4.0, "C": 6.2, "D": 4.1, "E": 1.5}
    restored, score_guard = restore_blocked_semantic_layer_scores(
        layers, baseline, sanitized
    )
    by_id = {row["layer_id"]: row for row in restored}
    assert by_id["C"]["score"] == 6.2
    assert by_id["D"]["score"] == 4.1
    assert by_id["A"]["score"] == 1.5
    assert by_id["B"]["score"] == 4.0
    assert by_id["E"]["score"] == 1.5
    assert score_guard["applied"] is True

    originality = originality_eval()
    originality_before = copy.deepcopy(originality)
    originality_sanitized = sanitize_hybrid_originality_evaluation(
        originality, rubric
    )
    assert originality == originality_before
    assert originality_sanitized["raw_text"] == originality["raw_text"]
    original_advice = originality_sanitized["parsed"]["improvement_advice"]
    assert len(original_advice) == 2
    assert all("편심하중" not in item and "과부하" not in item for item in original_advice)
    assert any("보존기간 결정 기준" in item for item in original_advice)
    assert any("온도 보상" in item for item in original_advice)

    non_hybrid = {
        "hybrid_general_grading_evidence": {
            "routing_mode": "GENERAL",
            "coverage_kind": "PURE_GENERAL",
            "demand_mappings": [],
        }
    }
    assert sanitize_hybrid_semantic_evaluation(semantic, non_hybrid) is semantic

    # SCOPE_NEUTRAL_SCORE_AND_MODEL_FEEDBACK_V1
    upward_layers = [
        {
            "layer_id": "C",
            "score": 3.69,
            "max": 8.0,
            "reason": "sanitized",
        },
        {
            "layer_id": "D",
            "score": 1.71,
            "max": 6.0,
            "reason": "sanitized",
        },
    ]
    upward_baseline = {
        "C": 2.94,
        "D": 0.96,
    }

    upward_guarded, upward_diag = (
        restore_blocked_semantic_layer_scores(
            upward_layers,
            upward_baseline,
            sanitized,
        )
    )
    upward_by_id = {
        row["layer_id"]: row
        for row in upward_guarded
    }

    assert upward_by_id["C"]["score"] == 3.69
    assert upward_by_id["D"]["score"] == 1.71
    assert upward_diag["adjustments"] == []
    assert {
        row["layer_id"]
        for row in upward_diag[
            "preserved_upward_layers"
        ]
    } == {"C", "D"}

    model_ref = {
        "matched": True,
        "hybrid_general_grading_context": (
            rubric[
                "hybrid_general_grading_evidence"
            ]
        ),
        "primary_reference": {
            "id": "T1",
            "topic_id": TOPIC,
            "expected_structure": [
                (
                    "스트레인 게이지의 측정 원리와 "
                    "저항 변화를 설명한다."
                ),
                (
                    "로드셀의 크리프와 히스테리시스 "
                    "오차를 설명한다."
                ),
                (
                    "온도 보상 방법과 적용 조건을 "
                    "설명한다."
                ),
            ],
            "field_connection_points": [
                (
                    "로드셀 현장 설치에서 편심하중과 "
                    "과부하 방지 기준을 제시한다."
                ),
                (
                    "교정 기록의 보존기간 결정 기준을 "
                    "정한다."
                ),
            ],
            "low_score_patterns": [
                (
                    "Wheatstone Bridge의 평형조건을 "
                    "반대로 설명한다."
                ),
                (
                    "로드셀 측하중 대책을 누락한다."
                ),
            ],
        },
    }

    projected, projection_diag = (
        project_hybrid_model_answer_feedback(
            model_ref
        )
    )

    assert projection_diag["active"] is True
    assert len(
        projected["expected_structure"]
    ) == 2
    assert all(
        "크리프" not in item
        and "히스테리시스" not in item
        for item in projected[
            "expected_structure"
        ]
    )
    assert projected[
        "field_connection_points"
    ] == [
        "교정 기록의 보존기간 결정 기준을 정한다."
    ]
    assert projected[
        "low_score_patterns"
    ] == [
        "Wheatstone Bridge의 평형조건을 반대로 설명한다."
    ]

    # MODEL_FEEDBACK_MERGE_INTEGRATION_V1
    from grading_agents import (
        _phase10_merge_model_answer_feedback,
    )

    merged = _phase10_merge_model_answer_feedback(
        {
            "summary": "",
            "rewrite_advice": [],
        },
        model_ref,
    )
    merged_advice = merged["rewrite_advice"]

    assert any(
        "스트레인 게이지" in item
        for item in merged_advice
    )
    assert any(
        "온도 보상" in item
        for item in merged_advice
    )
    assert any(
        "보존기간 결정 기준" in item
        for item in merged_advice
    )
    assert all(
        "크리프" not in item
        and "히스테리시스" not in item
        and "편심하중" not in item
        and "과부하" not in item
        and "측하중" not in item
        for item in merged_advice
    )
    assert (
        merged[
            "model_answer_reference"
        ]
        is model_ref
    )
    assert (
        merged[
            "hybrid_model_answer_feedback_scope_guard"
        ]["active"]
        is True
    )

    print("SCOPE_NEUTRAL_DOWNWARD_ONLY_POLICY=PASS")
    print("UPWARD_SEMANTIC_SCORE_PRESERVED=PASS")
    print("HYBRID_MODEL_FEEDBACK_PROJECTION=PASS")
    print("FULL_MODEL_REFERENCE_PRESERVED=PASS")
    print("HYBRID_SCOPE_GUARD_ACTIVATION=PASS")
    print("RAW_TEXT_IMMUTABLE=PASS")
    print("OUT_OF_SCOPE_SEMANTIC_CLAIMS_REMOVED=PASS")
    print("IN_SCOPE_TEMPERATURE_ADVICE_PRESERVED=PASS")
    print("IN_SCOPE_RECORD_ADVICE_PRESERVED=PASS")
    print("CONTAMINATED_C_D_SCORES_RESTORED=PASS")
    print("ORIGINALITY_ADVICE_SCOPE_GUARDED=PASS")
    print("NON_HYBRID_NOOP=PASS")
    print("ONE_QUESTION_ONE_SCORE_UNCHANGED=PASS")
    print("LLM_CALLS=0")


if __name__ == "__main__":
    main()
