from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

import difficulty_output_adapter as adapter


IDENTITY_PATCHES = (
    "attach_question_type_v2_to_grade",
    "ensure_grade_question_type_coverage",
    "attach_question_type_coverage_feedback",
    "apply_explicit_requirement_hard_cap",
    "apply_question_type_coverage_score_adjustment",
)


def identity(grade, *args, **kwargs):
    return grade


class DifficultyFeedbackOwnerPolicyTest(unittest.TestCase):
    def _run(self, strategy: dict, source: dict | None = None) -> dict:
        source = deepcopy(source or {
            "summary": "UPSTREAM SUMMARY",
            "improvement_points": ["UPSTREAM IMPROVEMENT"],
            "rewrite_advice": ["UPSTREAM ADVICE"],
            "weaknesses": ["UPSTREAM WEAKNESS"],
            "next_practice_focus": ["UPSTREAM FOCUS"],
        })

        patches = [
            patch.object(adapter, name, side_effect=identity)
            for name in IDENTITY_PATCHES
        ]
        for ctx in patches:
            ctx.start()

        try:
            with (
                patch.object(
                    adapter,
                    "summarize_question_strategy",
                    return_value=deepcopy(strategy),
                ),
                patch.object(
                    adapter,
                    "_difficulty_topic_id_from_grade",
                    return_value=None,
                ),
                patch.object(
                    adapter,
                    "_topic_importance_strategy_from_topic_id",
                    return_value={},
                ),
            ):
                return adapter.attach_difficulty_strategy_to_grade(
                    source,
                    question_text="시험 문제",
                )
        finally:
            for ctx in reversed(patches):
                ctx.stop()

    def _assert_public_feedback_preserved(self, result: dict) -> None:
        self.assertEqual(result["summary"], "UPSTREAM SUMMARY")
        self.assertEqual(result["improvement_points"], ["UPSTREAM IMPROVEMENT"])
        self.assertEqual(result["rewrite_advice"], ["UPSTREAM ADVICE"])
        self.assertEqual(result["weaknesses"], ["UPSTREAM WEAKNESS"])
        self.assertEqual(result["next_practice_focus"], ["UPSTREAM FOCUS"])

    def test_field_application_does_not_inject_public_feedback(self) -> None:
        result = self._run({
            "matched": True,
            "difficulty": "FIELD_APPLICATION",
            "difficulty_label": "현장 적용형",
            "selection_importance": "NORMAL",
            "selection_policy": "BALANCED",
            "default_score_ceiling": 20,
            "topic_id": "sentinel_field",
        })
        self._assert_public_feedback_preserved(result)
        self.assertEqual(
            result["difficulty_strategy"]["difficulty"],
            "FIELD_APPLICATION",
        )
        public_text = "\n".join(
            str(result.get(key) or "")
            for key in (
                "summary",
                "improvement_points",
                "rewrite_advice",
                "weaknesses",
                "next_practice_focus",
            )
        )
        self.assertNotIn("비용·유지보수", public_text)
        self.assertNotIn("실제 설비 적용 판단", public_text)

    def test_theory_core_does_not_inject_public_feedback(self) -> None:
        result = self._run({
            "matched": True,
            "difficulty": "THEORY_CORE",
            "difficulty_label": "핵심 이론형",
            "selection_importance": "NORMAL",
            "selection_policy": "CORE",
            "excellent_score_band": [21, 25],
            "topic_id": "sentinel_theory",
        })
        self._assert_public_feedback_preserved(result)
        self.assertEqual(
            result["difficulty_strategy"]["difficulty"],
            "THEORY_CORE",
        )
        self.assertTrue(
            any(
                "THEORY_CORE" in str(item)
                for item in result.get("strategy_warnings", [])
            )
        )

    def test_absent_feedback_is_not_created_by_difficulty(self) -> None:
        result = self._run(
            {
                "matched": True,
                "difficulty": "FIELD_APPLICATION",
                "selection_importance": "NORMAL",
            },
            source={"summary": ""},
        )
        self.assertEqual(result.get("summary"), "")
        self.assertNotIn("improvement_points", result)


if __name__ == "__main__":
    unittest.main(verbosity=0)
