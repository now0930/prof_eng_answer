#!/usr/bin/env python3
from __future__ import annotations

import hybrid_general_grading_context as hgc
from hybrid_general_evidence_consumer import (
    build_hybrid_general_subject_evidence,
)
from hybrid_general_prompt import (
    build_hybrid_general_prompt_section,
)

TOPIC = "topic_a"


def main():
    semantic = {
        "ok": True,
        "routing_mode": "SINGLE_TOPIC",
        "primary_topic_ids": [TOPIC],
        "uncovered_demand_ids": ["D4", "D5"],
        "demand_mappings": [
            {"demand_id": "D1", "role": "PRIMARY", "topic_id": TOPIC, "confidence": 1.0},
            {"demand_id": "D2", "role": "PRIMARY", "topic_id": TOPIC, "confidence": 1.0},
            {"demand_id": "D3", "role": "PRIMARY", "topic_id": TOPIC, "confidence": 1.0},
            {"demand_id": "D4", "role": "NONE", "topic_id": TOPIC, "confidence": 0.0},
            {"demand_id": "D5", "role": "NONE", "topic_id": TOPIC, "confidence": 0.0},
        ],
    }
    question_demands = {
        "ok": True,
        "demands": [
            {"id": "D1", "text": "스트레인 게이지의 측정 원리를 설명하시오."},
            {"id": "D2", "text": "Wheatstone Bridge를 설명하시오."},
            {"id": "D3", "text": "온도 보상 방법을 설명하시오."},
            {"id": "D4", "text": "기록 보존기간 결정 기준을 제시하시오."},
            {"id": "D5", "text": "기록 폐기 원칙을 제시하시오."},
        ],
    }

    old_candidates = hgc._candidate_topic_ids
    old_find = hgc._find_topic_object
    hgc._candidate_topic_ids = lambda value: [TOPIC]
    hgc._find_topic_object = lambda value, topic_id: {
        "topic_id": topic_id,
        "title": "Topic A",
        "anchors": [],
    }
    try:
        context = hgc.build_hybrid_general_grading_context(
            semantic_result=semantic,
            question_demand_result=question_demands,
            shadow_candidate_result={},
            generated_sources={"model_answer": {}, "fact_anchor": {}},
            enabled=True,
        )
    finally:
        hgc._candidate_topic_ids = old_candidates
        hgc._find_topic_object = old_find

    assert context["applicable"] is True
    assert context["coverage_kind"] == "HYBRID_TOPIC_GENERAL"
    assert context["routing_mode"] == "SINGLE_TOPIC"

    rows = context["demand_mappings"]
    assert [row["demand_id"] for row in rows] == ["D1", "D2", "D3", "D4", "D5"]
    expected = {
        "D1": "스트레인 게이지의 측정 원리를 설명하시오.",
        "D2": "Wheatstone Bridge를 설명하시오.",
        "D3": "온도 보상 방법을 설명하시오.",
        "D4": "기록 보존기간 결정 기준을 제시하시오.",
        "D5": "기록 폐기 원칙을 제시하시오.",
    }
    for row in rows:
        assert row["demand_text"] == expected[row["demand_id"]]

    by_id = {row["demand_id"]: row for row in rows}
    assert by_id["D1"]["role"] == "PRIMARY"
    assert by_id["D3"]["role"] == "PRIMARY"
    assert by_id["D4"]["role"] == "NONE"
    assert by_id["D5"]["role"] == "NONE"

    assert all("demand_text" not in row for row in semantic["demand_mappings"])

    model_ref = {
        "hybrid_general_grading_context": context
    }
    evidence = build_hybrid_general_subject_evidence(model_ref)
    assert evidence is not None
    assert evidence['demand_mappings'][0]['demand_text'] == expected['D1']
    assert evidence['demand_mappings'][4]['demand_text'] == expected['D5']

    rubric = {
        "hybrid_general_grading_evidence": evidence
    }
    prompt = build_hybrid_general_prompt_section(rubric)
    assert "[HYBRID_GENERAL_GRADING_EVIDENCE_V1]" in prompt
    assert '"demand_mappings":' in prompt
    assert expected["D1"] in prompt
    assert expected["D2"] in prompt
    assert expected["D3"] in prompt
    assert expected["D4"] in prompt
    assert expected["D5"] in prompt
    assert '"role":"PRIMARY"' in prompt
    assert '"role":"NONE"' in prompt

    general = context["general_engineering_evidence"]
    assert [row["demand_id"] for row in general["demands"]] == ["D4", "D5"]
    assert general["score_component"] is False

    print("HYBRID_ALL_DEMAND_TEXT_PRESERVED=PASS")
    print("PRIMARY_DEMAND_TEXT_IN_PROMPT=PASS")
    print("UNCOVERED_DEMAND_TEXT_IN_PROMPT=PASS")
    print("SEMANTIC_SOURCE_IMMUTABLE=PASS")
    print("HYBRID_GENERAL_SCOPE_UNCHANGED=PASS")
    print("ONE_QUESTION_ONE_SCORE_UNCHANGED=PASS")
    print("LLM_CALLS=0")


if __name__ == "__main__":
    main()
