from __future__ import annotations

import unittest
from unittest.mock import patch

import gemini_grader
from hybrid_general_prompt import (
    HYBRID_GENERAL_PROMPT_MARKER,
    build_hybrid_general_prompt_section,
)


def rubric() -> dict:
    return {
        "hybrid_general_grading_evidence": {
            "version": "hybrid_general_subject_evidence_v1",
            "routing_mode": "SINGLE_TOPIC",
            "coverage_kind": "HYBRID_TOPIC_GENERAL",
            "primary_topic_ids": ["topic_a"],
            "topics": [
                {
                    "topic_id": "topic_a",
                    "title": "Topic A",
                    "model_answer": {
                        "topic_id": "topic_a",
                        "body": "model",
                    },
                    "fact_anchor": {
                        "topic_id": "topic_a",
                        "anchors": [],
                    },
                }
            ],
            "general_engineering_evidence": {
                "basis": "question_demands_only",
                "demands": [
                    {
                        "demand_id": "D2",
                        "demand_text": "general demand",
                    }
                ],
                "score_component": False,
            },
            "uncovered_demand_ids": ["D2"],
        }
    }


class HybridGeneralPromptTest(unittest.TestCase):
    def test_no_evidence_is_noop(self):
        self.assertEqual(
            build_hybrid_general_prompt_section({}),
            "",
        )

    def test_prompt_contract(self):
        section = build_hybrid_general_prompt_section(
            rubric()
        )
        self.assertIn(
            HYBRID_GENERAL_PROMPT_MARKER,
            section,
        )
        self.assertIn(
            "HYBRID_TOPIC_GENERAL",
            section,
        )
        self.assertIn('"D2"', section)
        self.assertIn("합산·평균하지 않는다", section)
        self.assertIn("총점 25점 산식을 변경하지 않는다", section)
        self.assertIn(
            "학생 답안으로 routing_mode",
            section,
        )

    def test_invalid_score_component_rejected(self):
        value = rubric()
        value[
            "hybrid_general_grading_evidence"
        ][
            "general_engineering_evidence"
        ][
            "score_component"
        ] = True
        self.assertEqual(
            build_hybrid_general_prompt_section(value),
            "",
        )

    def test_wrapper_appends_once(self):
        with patch.object(
            gemini_grader,
            "_hybrid_general_prompt_previous_build_gemini_grading_prompt",
            return_value="BASE",
        ):
            result = gemini_grader.build_gemini_grading_prompt(
                subject_rubric=rubric()
            )

        self.assertTrue(result.startswith("BASE"))
        self.assertEqual(
            result.count(HYBRID_GENERAL_PROMPT_MARKER),
            1,
        )

    def test_wrapper_no_evidence_preserves_base(self):
        with patch.object(
            gemini_grader,
            "_hybrid_general_prompt_previous_build_gemini_grading_prompt",
            return_value="BASE",
        ):
            result = gemini_grader.build_gemini_grading_prompt(
                subject_rubric={}
            )

        self.assertEqual(result, "BASE")

    def test_wrapper_does_not_duplicate_marker(self):
        base = "BASE\n" + HYBRID_GENERAL_PROMPT_MARKER
        with patch.object(
            gemini_grader,
            "_hybrid_general_prompt_previous_build_gemini_grading_prompt",
            return_value=base,
        ):
            result = gemini_grader.build_gemini_grading_prompt(
                subject_rubric=rubric()
            )

        self.assertEqual(
            result.count(HYBRID_GENERAL_PROMPT_MARKER),
            1,
        )


if __name__ == "__main__":
    unittest.main()
