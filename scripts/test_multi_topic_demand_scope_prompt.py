from __future__ import annotations

import unittest
from unittest.mock import patch

import gemini_grader


class MultiTopicDemandScopePromptTest(unittest.TestCase):
    def _build(self, subject_rubric=None, base="BASE_PROMPT"):
        with patch.object(
            gemini_grader,
            "_build_hybrid_general_prompt",
            lambda *args, **kwargs: base,
        ):
            return gemini_grader.build_gemini_grading_prompt(
                subject_rubric=subject_rubric,
            )

    def test_multi_topic_appends_scope_contract(self):
        prompt = self._build(
            {
                "multi_topic_grading_evidence": {
                    "applicable": True,
                    "routing_mode": "MULTI_TOPIC",
                }
            }
        )
        normalized = " ".join(prompt.split())
        self.assertIn(
            "[MULTI_TOPIC_DEMAND_SCOPE_CONTRACT_V1]",
            prompt,
        )
        self.assertIn(
            "Use semantic demand_mappings",
            normalized,
        )
        self.assertIn(
            "must not silently expand the question scope",
            normalized,
        )
        self.assertIn(
            "load-cell eccentric-load, overload",
            normalized,
        )
        self.assertIn(
            "Preserve one-question-one-score",
            normalized,
        )

    def test_non_multi_topic_prompt_is_unchanged(self):
        self.assertEqual(
            self._build({}, base="SINGLE_BASE"),
            "SINGLE_BASE",
        )
        self.assertEqual(
            self._build(None, base="GENERAL_BASE"),
            "GENERAL_BASE",
        )

    def test_contract_is_idempotent(self):
        evidence = {
            "multi_topic_grading_evidence": {
                "version": "multi_topic_subject_evidence_v1",
                "routing_mode": "MULTI_TOPIC",
                "primary_topic_ids": ["topic_a", "topic_b"],
                "uncovered_demand_ids": [],
            }
        }
        contract = (
            gemini_grader._multi_topic_demand_scope_prompt_v1()
        )
        prompt = self._build(
            evidence,
            base="BASE\n\n" + contract,
        )
        self.assertEqual(
            prompt.count(
                "[MULTI_TOPIC_DEMAND_SCOPE_CONTRACT_V1]"
            ),
            1,
        )

    def test_real_attached_schema_activates_without_applicable_key(self):
        rubric = {
            "multi_topic_grading_evidence": {
                "version": "multi_topic_subject_evidence_v1",
                "routing_mode": "MULTI_TOPIC",
                "primary_topic_ids": ["topic_a", "topic_b"],
                "uncovered_demand_ids": [],
            }
        }
        self.assertTrue(
            gemini_grader
            ._multi_topic_demand_scope_applicable_v1(rubric)
        )
        prompt = self._build(rubric, base="ATTACHED_BASE")
        self.assertIn(
            "[MULTI_TOPIC_DEMAND_SCOPE_CONTRACT_V1]",
            prompt,
        )

    def test_non_multi_topic_routing_mode_does_not_activate(self):
        for routing_mode in ("SINGLE_TOPIC", "GENERAL", "AMBIGUOUS"):
            rubric = {
                "multi_topic_grading_evidence": {
                    "version": "multi_topic_subject_evidence_v1",
                    "routing_mode": routing_mode,
                }
            }
            self.assertFalse(
                gemini_grader
                ._multi_topic_demand_scope_applicable_v1(rubric)
            )
            self.assertEqual(
                self._build(rubric, base="UNCHANGED"),
                "UNCHANGED",
            )

    def test_contract_preserves_explicit_error_checking(self):
        normalized = " ".join(
            gemini_grader
            ._multi_topic_demand_scope_prompt_v1()
            .split()
        )
        self.assertIn(
            "does not excuse an explicit factual error",
            normalized,
        )
        self.assertIn(
            "Do not transfer requirements between Topics",
            normalized,
        )


if __name__ == "__main__":
    unittest.main()
