#!/usr/bin/env python3
import unittest

from question_type_taxonomy import (
    normalize_question_type,
    question_type_de_policy,
    resolve_question_type_de_policy,
)


class QuestionTypeDEPolicyTest(unittest.TestCase):
    def test_canonical_and_legacy_normalization(self):
        self.assertEqual(
            normalize_question_type("COMPARE"),
            "COMPARE_SELECTION",
        )
        self.assertEqual(
            normalize_question_type("CAUSE_ACTION"),
            "DIAGNOSIS_ACTION",
        )

    def test_principle_unasked_cost_is_no_penalty(self):
        resolved = resolve_question_type_de_policy(
            "PRINCIPLE_INTERPRETATION",
            [],
        )
        self.assertIn("cost_benefit", resolved["no_penalty"])
        self.assertNotIn("cost_benefit", resolved["mandatory_d"])

    def test_principle_explicit_cost_is_promoted(self):
        resolved = resolve_question_type_de_policy(
            "PRINCIPLE_INTERPRETATION",
            ["cost_benefit"],
        )
        self.assertIn("cost_benefit", resolved["mandatory_d"])
        self.assertNotIn("cost_benefit", resolved["no_penalty"])

    def test_diagnosis_cause_only_does_not_require_action(self):
        resolved = resolve_question_type_de_policy(
            "DIAGNOSIS_ACTION",
            [],
        )
        self.assertNotIn("action_fit", resolved["mandatory_d"])
        self.assertNotIn("cause_to_action", resolved["mandatory_e"])
        self.assertIn(
            "countermeasure_when_only_cause_is_requested",
            resolved["no_penalty"],
        )

    def test_diagnosis_explicit_action_promotes_action_chain(self):
        resolved = resolve_question_type_de_policy(
            "DIAGNOSIS_ACTION",
            ["action_or_countermeasure"],
        )
        self.assertIn("action_fit", resolved["mandatory_d"])
        self.assertIn("cause_to_action", resolved["mandatory_e"])
        self.assertNotIn(
            "countermeasure_when_only_cause_is_requested",
            resolved["no_penalty"],
        )

    def test_compare_only_does_not_require_selection(self):
        resolved = resolve_question_type_de_policy(
            "COMPARE_SELECTION",
            [],
        )
        self.assertNotIn("selection_reason", resolved["mandatory_d"])
        self.assertNotIn("comparison_to_selection", resolved["mandatory_e"])

    def test_compare_explicit_selection_promotes_selection(self):
        resolved = resolve_question_type_de_policy(
            "COMPARE_SELECTION",
            ["selection"],
        )
        self.assertIn("selection_reason", resolved["mandatory_d"])
        self.assertIn("comparison_to_selection", resolved["mandatory_e"])
        self.assertNotIn(
            "single_final_choice_when_only_comparison_is_requested",
            resolved["no_penalty"],
        )

    def test_implementation_evaluation_is_conditional(self):
        base = resolve_question_type_de_policy(
            "IMPLEMENTATION_EVALUATION",
            [],
        )
        explicit = resolve_question_type_de_policy(
            "IMPLEMENTATION_EVALUATION",
            ["evaluation_or_verification"],
        )
        self.assertNotIn("evaluation_interpretation", base["mandatory_d"])
        self.assertNotIn(
            "metric_to_result_or_verification",
            base["mandatory_e"],
        )
        self.assertIn(
            "evaluation_interpretation",
            explicit["mandatory_d"],
        )
        self.assertIn(
            "metric_to_result_or_verification",
            explicit["mandatory_e"],
        )

    def test_profile_accessor_returns_independent_copy(self):
        first = question_type_de_policy("PRINCIPLE_INTERPRETATION")
        first["d_required"].append("MUTATED")
        second = question_type_de_policy("PRINCIPLE_INTERPRETATION")
        self.assertNotIn("MUTATED", second["d_required"])


if __name__ == "__main__":
    unittest.main()
