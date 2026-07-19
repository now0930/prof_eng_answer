from __future__ import annotations

# PLAN_C_GEMINI_CALIBRATION_TEST_V1
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import gemini_grader
import grading_agents


def scoring_model():
    return {
        "layers": [
            {"id": "A", "points": 3},
            {"id": "B", "points": 6},
            {"id": "C", "points": 8},
            {"id": "D", "points": 6},
            {"id": "E", "points": 2},
        ],
    }


def layer_rows(score=0.0):
    return [
        {
            "layer_id": layer_id,
            "score": score,
            "max_score": maximum,
            "reason": "",
        }
        for layer_id, maximum in (
            ("A", 3.0),
            ("B", 6.0),
            ("C", 8.0),
            ("D", 6.0),
            ("E", 2.0),
        )
    ]


def depth_only_eval():
    return {
        "parsed": {
            "question_type_coverage": {
                "overall_coverage": "adequate",
                "sub_criteria_coverage": [
                    {
                        "criterion": "background_need",
                        "status": "present",
                    },
                    {
                        "criterion": "principle_mechanism",
                        "status": "partial",
                    },
                    {
                        "criterion": "calculation_or_interpretation",
                        "status": "partial",
                    },
                    {
                        "criterion": "result_meaning",
                        "status": "partial",
                    },
                    {
                        "criterion": "field_judgement",
                        "status": "partial",
                    },
                ],
                "explicit_requirement_coverage": {
                    "requirements": [
                        {
                            "requirement": "개념 설명",
                            "status": "present",
                            "is_core": True,
                        },
                        {
                            "requirement": "설계 기준",
                            "status": "present",
                            "is_core": True,
                        },
                    ],
                },
            },
            "layer_issue_ownership": [
                {
                    "issue_id": "detail_gap",
                    "primary_owner_layer": "C",
                    "issue_type": "depth_gap",
                    "severity": "minor",
                    "invalidates_core_conclusion": False,
                },
            ],
        },
    }


class GeminiPromptCalibrationRegressionTest(
    unittest.TestCase
):
    def test_prompt_contains_layer_specific_calibration(self):
        original = (
            gemini_grader
            ._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1
        )

        try:
            gemini_grader._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1 = (
                lambda *args, **kwargs: "BASE"
            )
            prompt = (
                gemini_grader
                .build_gemini_grading_prompt(
                    question_text="원리를 설명하시오.",
                    answer_text="답안",
                )
            )
        finally:
            gemini_grader._PLAN_B_ORIGINAL_BUILD_GEMINI_GRADING_PROMPT_V1 = (
                original
            )

        self.assertIn(
            "[PLAN_C_SEMANTIC_SCORING_CALIBRATION_V2]",
            prompt,
        )
        self.assertIn(
            "요구 항목이 존재하고 핵심 의미가 맞으면 present",
            prompt,
        )
        self.assertIn(
            "동일한 깊이 부족을 E에서 다시 감점하지 않는다",
            prompt,
        )
        self.assertIn(
            "field_judgement는 present",
            prompt,
        )


class SemanticDownwardGuardRegressionTest(
    unittest.TestCase
):
    def test_depth_only_evaluation_limits_downward_drift(self):
        baseline = {
            "A": 2.8,
            "B": 5.7,
            "C": 5.2,
            "D": 5.0,
            "E": 1.7,
        }
        rows = layer_rows()

        for row in rows:
            row["score"] = 1.0

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                rows,
                baseline,
                depth_only_eval(),
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertTrue(
            diagnostic["eligible"]
        )
        self.assertTrue(
            diagnostic["applied"]
        )
        self.assertEqual(
            by_id["A"]["score"],
            2.35,
        )
        self.assertEqual(
            by_id["B"]["score"],
            4.8,
        )
        self.assertEqual(
            by_id["C"]["score"],
            3.6,
        )
        self.assertEqual(
            by_id["D"]["score"],
            4.1,
        )
        self.assertEqual(
            by_id["E"]["score"],
            1.4,
        )

    def test_major_correctness_error_disables_guard(self):
        evaluation = depth_only_eval()
        issue = (
            evaluation["parsed"]
            ["layer_issue_ownership"][0]
        )
        issue["issue_type"] = "correctness_error"
        issue["severity"] = "major"
        issue["invalidates_core_conclusion"] = True

        rows = layer_rows(1.0)
        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                rows,
                {
                    "A": 2.8,
                    "B": 5.7,
                    "C": 5.2,
                    "D": 5.0,
                    "E": 1.7,
                },
                evaluation,
                scoring_model(),
            )
        )

        self.assertFalse(
            diagnostic["eligible"]
        )
        self.assertFalse(
            diagnostic["applied"]
        )
        self.assertTrue(
            all(
                row["score"] == 1.0
                for row in guarded
            )
        )

    def test_core_requirement_missing_disables_guard(self):
        evaluation = depth_only_eval()
        requirement = (
            evaluation["parsed"]
            ["question_type_coverage"]
            ["explicit_requirement_coverage"]
            ["requirements"][0]
        )
        requirement["status"] = "missing"

        rows = layer_rows(1.0)
        _, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                rows,
                {
                    "A": 2.8,
                    "B": 5.7,
                    "C": 5.2,
                    "D": 5.0,
                    "E": 1.7,
                },
                evaluation,
                scoring_model(),
            )
        )

        self.assertFalse(
            diagnostic["eligible"]
        )
        self.assertEqual(
            diagnostic["core_missing"],
            1,
        )

    def test_guard_never_raises_above_pre_semantic_score(self):
        baseline = {
            "A": 2.0,
            "B": 4.0,
            "C": 4.0,
            "D": 3.0,
            "E": 1.0,
        }
        rows = layer_rows(0.0)

        guarded, _ = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                rows,
                baseline,
                depth_only_eval(),
                scoring_model(),
            )
        )

        for row in guarded:
            self.assertLessEqual(
                row["score"],
                baseline[row["layer_id"]],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
