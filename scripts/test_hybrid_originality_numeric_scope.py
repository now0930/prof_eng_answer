#!/usr/bin/env python3
from __future__ import annotations

import inspect

from grading_agents import (
    _phase8_normalize_originality_evaluation,
    _phase8_run_originality_evaluator,
)
from hybrid_demand_scope_guard import (
    build_hybrid_originality_scope_contract,
    project_hybrid_originality_pre_normalization,
    sanitize_hybrid_originality_evaluation,
)
from originality_grader import (
    build_originality_prompt,
)
from scripts.test_hybrid_demand_scope_guard import (
    hybrid_rubric,
)


def synthetic_eval():
    return {
        "ok": True,
        "raw_text": "raw audit must be preserved",
        "parsed": {
            "version": "originality_evaluator_v1",
            "overall_comment": "synthetic",
            "anchors": [
                {
                    "id": "O1",
                    "name": "문제 재해석 능력",
                    "level": 0.7,
                    "reason": (
                        "편심하중 설치 대책까지 확장하여 좋음."
                    ),
                    "evidence": [
                        "편심하중 설치 대책을 제시함."
                    ],
                },
                {
                    "id": "O2",
                    "name": "현장 조건 반영",
                    "level": 0.5,
                    "reason": (
                        "온도 보상은 설명했으나 설치 환경 "
                        "고려가 부족함."
                    ),
                    "evidence": [
                        "온도 보상 적용 조건을 구분함."
                    ],
                },
                {
                    "id": "O3",
                    "name": "대안 비교와 trade-off",
                    "level": 0.0,
                    "reason": "없음",
                    "evidence": [],
                },
                {
                    "id": "O4",
                    "name": "적용 우선순위 제시",
                    "level": 0.0,
                    "reason": "없음",
                    "evidence": [],
                },
                {
                    "id": "O5",
                    "name": "검증 가능성",
                    "level": 0.3,
                    "reason": (
                        "보존기간 결정 기준은 제시했으나 "
                        "폐기 원칙 설명이 다소 부족함."
                    ),
                    "evidence": [
                        "보존기간 결정 기준의 근거를 제시함."
                    ],
                },
            ],
            "average_level": 0.3,
            "raw_originality_score": 1.8,
            "reported_raw_originality_score": 1.8,
            "improvement_advice": [
                "온도 보상 적용 조건을 더 명확히 할 것.",
                "교정 주기 결정 시 RBM을 적용할 것.",
            ],
        },
    }


def main():
    rubric = hybrid_rubric()

    contract = build_hybrid_originality_scope_contract(
        rubric
    )
    assert contract["active"] is True
    assert contract["coverage_kind"] == "HYBRID_TOPIC_GENERAL"
    assert contract["routing_mode"] == "SINGLE_TOPIC"
    assert [
        row["demand_id"]
        for row in contract["demand_mappings"]
    ] == ["D1", "D2", "D3", "D4", "D5", "D6"]

    prompt = build_originality_prompt(
        question_text="synthetic question",
        answer_text="synthetic answer",
        question_scope_contract=contract,
    )

    assert "[HYBRID_ORIGINALITY_DEMAND_SCOPE_V1]" in prompt
    assert (
        "명시 Question Demand를 정확히 설명한 사실 자체는 "
        "기본 충족이며 Originality 가점이 아니다."
        in prompt
    )
    assert "보존기간 결정 기준" in prompt
    assert "폐기 원칙" in prompt

    original = synthetic_eval()

    projected = (
        project_hybrid_originality_pre_normalization(
            original,
            rubric,
        )
    )

    assert projected["raw_text"] == original["raw_text"]

    anchors = {
        row["id"]: row
        for row in projected["parsed"]["anchors"]
    }

    assert anchors["O1"]["level"] == 0.0
    assert anchors["O1"]["evidence"] == []

    assert anchors["O2"]["level"] == 0.5
    assert anchors["O2"]["evidence"] == [
        "온도 보상 적용 조건을 구분함."
    ]
    assert "설치 환경" not in anchors["O2"]["reason"]

    assert anchors["O5"]["level"] == 0.3
    assert "폐기 원칙" in anchors["O5"]["reason"]
    assert "부족" in anchors["O5"]["reason"]

    assert projected["parsed"]["average_level"] == 0.16
    assert projected["parsed"]["raw_originality_score"] == 0.32
    assert (
        "reported_raw_originality_score"
        not in projected["parsed"]
    )

    normalized = _phase8_normalize_originality_evaluation(
        projected["parsed"]
    )

    assert normalized["average_level"] == 0.16
    assert normalized["anchor_derived_originality_score"] == 0.32
    assert normalized["raw_originality_score"] == 0.32
    assert normalized["reported_raw_originality_score"] == 0.32

    projected["parsed"] = normalized
    sanitized = sanitize_hybrid_originality_evaluation(
        projected,
        rubric,
    )

    assert sanitized["parsed"]["improvement_advice"] == [
        "온도 보상 적용 조건을 더 명확히 할 것."
    ]
    assert (
        sanitized[
            "hybrid_originality_scope_projection"
        ]["active"]
        is True
    )
    assert (
        sanitized[
            "hybrid_originality_scope_projection"
        ]["zeroed_anchor_ids"]
        == ["O1"]
    )

    ordinary = synthetic_eval()
    assert (
        project_hybrid_originality_pre_normalization(
            ordinary,
            {"subject": "ordinary"},
        )
        == ordinary
    )

    source = inspect.getsource(
        _phase8_run_originality_evaluator
    )
    assert (
        source.find(
            "project_hybrid_originality_pre_normalization"
        )
        < source.find(
            "_phase8_normalize_originality_evaluation"
        )
    )

    print("HYBRID_ORIGINALITY_SCOPE_CONTRACT=PASS")
    print("EXPLICIT_DEMAND_FULFILLMENT_BASELINE_CONTRACT=PASS")
    print("PRE_NORMALIZATION_ANCHOR_PROJECTION=PASS")
    print("OUT_OF_SCOPE_POSITIVE_BONUS_BLOCKED=PASS")
    print("OUT_OF_SCOPE_NEGATIVE_REASON_NEUTRALIZED=PASS")
    print("MIXED_NEGATIVE_REASON_FRAGMENT_SCOPE=PASS")
    print("IN_SCOPE_NEGATIVE_REASON_PRESERVED=PASS")
    print("PROJECTED_NUMERIC_SCORE_RECOMPUTED=PASS")
    print("ORIGINALITY_ADVICE_SCOPE_PRESERVED=PASS")
    print("NON_HYBRID_NOOP=PASS")
    print("RAW_TEXT_AUDIT_PRESERVED=PASS")


if __name__ == "__main__":
    main()
