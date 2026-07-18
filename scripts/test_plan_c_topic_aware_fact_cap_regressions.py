from __future__ import annotations

# PLAN_C_TEST_REPO_BOOTSTRAP_V1
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import gemini_grader
import grading_agents
import grade_output_summarizer


def strong_semantic_eval():
    return {
        "parsed": {
            "layers": [
                {
                    "layer_id": "C",
                    "score": 6.5,
                    "max": 8.0,
                },
                {
                    "layer_id": "D",
                    "score": 5.0,
                    "max": 6.0,
                },
                {
                    "layer_id": "E",
                    "score": 1.8,
                    "max": 2.0,
                },
            ],
            "question_type_coverage": {
                "overall_coverage": "strong",
                "sub_criteria_coverage": [
                    {
                        "criterion": "principle",
                        "status": "present",
                    },
                    {
                        "criterion": "calculation",
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
                    "issue_id": "advanced_derivation",
                    "issue_type": "depth_gap",
                    "severity": "partial",
                    "primary_owner_layer": "C",
                    "reason": "상세 유도 부족",
                },
            ],
        },
    }


def field_policy():
    return {
        "topic_id": "field_application_example",
        "difficulty": "FIELD_APPLICATION",
        "selection_importance": "NORMAL",
        "source": "test",
        "resolved": True,
    }


def theory_policy():
    return {
        "topic_id": "theory_core_example",
        "difficulty": "THEORY_CORE",
        "selection_importance": "CORE_MUST_PREPARE",
        "source": "test",
        "resolved": True,
    }


def context_for(policy):
    calibration = (
        grading_agents
        ._plan_c_semantic_calibration_from_eval(
            strong_semantic_eval()
        )
    )
    decision = (
        grading_agents
        ._plan_c_cap_policy_decision(
            policy,
            calibration,
        )
    )

    return {
        "topic_policy": policy,
        "semantic_calibration": calibration,
        "decision": decision,
    }


def base_layers():
    return [
        {
            "layer_id": "A",
            "score": 2.8,
            "max_score": 3.0,
        },
        {
            "layer_id": "B",
            "score": 5.7,
            "max_score": 6.0,
        },
        {
            "layer_id": "C",
            "score": 4.61,
            "max_score": 8.0,
        },
        {
            "layer_id": "D",
            "score": 6.0,
            "max_score": 6.0,
        },
        {
            "layer_id": "E",
            "score": 2.0,
            "max_score": 2.0,
        },
    ]


class PlanCPromptContractRegressionTest(
    unittest.TestCase
):
    def test_prompt_contains_plan_b_and_plan_c_contracts(self):
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
            "[PLAN_B_GENERAL_LAYER_OWNERSHIP_V1]",
            prompt,
        )
        self.assertIn(
            "[PLAN_C_DEPTH_VS_ERROR_CALIBRATION_V1]",
            prompt,
        )
        self.assertIn("correctness_error", prompt)
        self.assertIn("depth_gap", prompt)


class PlanCTopicPolicyRegressionTest(
    unittest.TestCase
):
    def test_exact_conjunction_is_hard_cap(self):
        decision = context_for(
            theory_policy()
        )["decision"]

        self.assertEqual(decision["mode"], "hard")
        self.assertTrue(
            decision[
                "must_prepare_control_theory"
            ]
        )

    def test_field_application_is_soft_candidate(self):
        decision = context_for(
            field_policy()
        )["decision"]

        self.assertEqual(decision["mode"], "soft")

    def test_unresolved_policy_stays_hard(self):
        decision = context_for(
            {
                "resolved": False,
                "source": "unresolved",
            }
        )["decision"]

        self.assertEqual(decision["mode"], "hard")


class PlanCIntegratedCapRegressionTest(
    unittest.TestCase
):
    def test_field_answer_uses_soft_cap(self):
        rows = base_layers()

        before, after, caps = (
            grading_agents._phase2_apply_caps(
                rows,
                {"cap": None},
                context_for(field_policy()),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in rows
        }

        self.assertEqual(before, 21.11)
        self.assertEqual(after, 19.61)
        self.assertEqual(by_id["D"]["score"], 4.88)
        self.assertEqual(by_id["E"]["score"], 1.62)
        self.assertEqual(caps[-1]["mode"], "soft")

    def test_theory_answer_keeps_hard_cap(self):
        rows = base_layers()

        _, after, caps = (
            grading_agents._phase2_apply_caps(
                rows,
                {"cap": None},
                context_for(theory_policy()),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in rows
        }

        self.assertEqual(after, 17.11)
        self.assertEqual(by_id["D"]["score"], 3.0)
        self.assertEqual(by_id["E"]["score"], 1.0)
        self.assertEqual(caps[-1]["mode"], "hard")


class PlanCSemanticGuardRegressionTest(
    unittest.TestCase
):
    def test_major_correctness_error_stays_hard(self):
        evaluation = strong_semantic_eval()
        issue = (
            evaluation["parsed"]
            ["layer_issue_ownership"][0]
        )
        issue["issue_type"] = "correctness_error"
        issue["severity"] = "major"

        calibration = (
            grading_agents
            ._plan_c_semantic_calibration_from_eval(
                evaluation
            )
        )
        decision = (
            grading_agents
            ._plan_c_cap_policy_decision(
                field_policy(),
                calibration,
            )
        )

        self.assertFalse(
            calibration["semantic_quality_ok"]
        )
        self.assertEqual(decision["mode"], "hard")

    def test_semantic_c_below_75_percent_stays_hard(self):
        evaluation = strong_semantic_eval()
        evaluation["parsed"]["layers"][0]["score"] = 5.5

        calibration = (
            grading_agents
            ._plan_c_semantic_calibration_from_eval(
                evaluation
            )
        )
        decision = (
            grading_agents
            ._plan_c_cap_policy_decision(
                field_policy(),
                calibration,
            )
        )

        self.assertFalse(
            calibration["semantic_quality_ok"]
        )
        self.assertEqual(decision["mode"], "hard")


class PlanCVerdictConsistencyRegressionTest(
    unittest.TestCase
):
    def test_unverified_error_wording_is_softened(self):
        payload = {
            "logic_check": {
                "fatal": False,
            },
            "semantic": {
                "layer_issue_ownership": [
                    {
                        "issue_type": "depth_gap",
                        "severity": "partial",
                    },
                ],
            },
        }
        value = {
            "headline": (
                "핵심 이론 오류: "
                "물리적 해석 깊이 보완 필요"
            ),
        }

        cleaned = (
            grade_output_summarizer
            ._plan_c_sanitize_unverified_core_error(
                value,
                payload,
            )
        )

        self.assertNotIn(
            "핵심 이론 오류",
            cleaned["headline"],
        )
        self.assertIn(
            "핵심 이론은 정확하나",
            cleaned["headline"],
        )

    def test_major_correctness_error_preserves_wording(self):
        payload = {
            "layer_issue_ownership": [
                {
                    "issue_type": "correctness_error",
                    "severity": "major",
                },
            ],
        }
        value = "핵심 이론 오류"

        cleaned = (
            grade_output_summarizer
            ._plan_c_sanitize_unverified_core_error(
                value,
                payload,
            )
        )

        self.assertEqual(cleaned, value)

    def test_logic_fatal_preserves_wording(self):
        payload = {
            "logic_check": {
                "fatal": True,
            },
        }
        value = "THEORY_CORE 핵심 이론 오류"

        cleaned = (
            grade_output_summarizer
            ._plan_c_sanitize_unverified_core_error(
                value,
                payload,
            )
        )

        self.assertEqual(cleaned, value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
