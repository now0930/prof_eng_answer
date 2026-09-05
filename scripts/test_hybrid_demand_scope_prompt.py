#!/usr/bin/env python3
from __future__ import annotations

import gemini_grader


def build_without_network(subject_rubric):
    previous = (
        gemini_grader
        ._build_hybrid_general_prompt
    )
    gemini_grader._build_hybrid_general_prompt = (
        lambda *args, **kwargs: "BASE_PROMPT"
    )
    try:
        return gemini_grader.build_gemini_grading_prompt(
            subject_rubric=subject_rubric
        )
    finally:
        gemini_grader._build_hybrid_general_prompt = (
            previous
        )


def main():
    hybrid = {
        "hybrid_general_grading_evidence": {
            "coverage_kind": "HYBRID_TOPIC_GENERAL",
            "routing_mode": "SINGLE_TOPIC",
            "primary_topic_ids": ["topic_a"],
            "demand_mappings": [
                {
                    "demand_id": "D1",
                    "role": "PRIMARY",
                    "topic_id": "topic_a",
                    "confidence": 1.0,
                },
                {
                    "demand_id": "D5",
                    "role": "NONE",
                    "topic_id": "topic_a",
                    "confidence": 0.0,
                },
                {
                    "demand_id": "D6",
                    "role": "NONE",
                    "topic_id": "topic_a",
                    "confidence": 0.0,
                },
            ],
            "uncovered_demand_ids": ["D5", "D6"],
            "general_engineering_evidence": {
                "basis": "question_demands_only",
                "demands": [
                    {
                        "demand_id": "D5",
                        "demand_text": "보존기간 결정 기준",
                        "source": "question_demand",
                    },
                    {
                        "demand_id": "D6",
                        "demand_text": "폐기 원칙",
                        "source": "question_demand",
                    },
                ],
                "score_component": False,
            },
        }
    }

    assert (
        gemini_grader
        ._multi_topic_demand_scope_applicable_v1(hybrid)
        is True
    )

    prompt = build_without_network(hybrid)
    for token in (
        "[MULTI_TOPIC_DEMAND_SCOPE_CONTRACT_V1]",
        "HYBRID_TOPIC_GENERAL",
        "from Topic evidence into",
        "uncovered General Demands",
        "record-retention or disposal",
        "role=NONE / uncovered Demands",
        "General Engineering evidence in Hybrid mode applies only to uncovered",
        "Preserve one-question-one-score",
    ):
        assert token in prompt, token

    multi = {
        "multi_topic_grading_evidence": {
            "routing_mode": "MULTI_TOPIC",
        }
    }
    assert (
        gemini_grader
        ._multi_topic_demand_scope_applicable_v1(multi)
        is True
    )

    single_non_hybrid = {
        "multi_topic_grading_evidence": {
            "routing_mode": "SINGLE_TOPIC",
        }
    }
    assert (
        gemini_grader
        ._multi_topic_demand_scope_applicable_v1(single_non_hybrid)
        is False
    )

    pure_general = {
        "hybrid_general_grading_evidence": {
            "coverage_kind": "PURE_GENERAL",
            "routing_mode": "GENERAL",
            "uncovered_demand_ids": ["D1"],
        }
    }
    assert (
        gemini_grader
        ._multi_topic_demand_scope_applicable_v1(pure_general)
        is False
    )

    ambiguous = {
        "hybrid_general_grading_evidence": {
            "coverage_kind": "HYBRID_TOPIC_GENERAL",
            "routing_mode": "AMBIGUOUS",
        }
    }
    assert (
        gemini_grader
        ._multi_topic_demand_scope_applicable_v1(ambiguous)
        is False
    )

    print("MULTI_TOPIC_SCOPE_PRESERVED=PASS")
    print("HYBRID_TOPIC_GENERAL_SCOPE=PASS")
    print("PURE_GENERAL_ISOLATION=PASS")
    print("SINGLE_TOPIC_NON_HYBRID_ISOLATION=PASS")
    print("AMBIGUOUS_ISOLATION=PASS")
    print("ONE_QUESTION_ONE_SCORE_CONTRACT=PASS")
    print("LLM_CALLS=0")


if __name__ == "__main__":
    main()
