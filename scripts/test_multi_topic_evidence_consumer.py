from __future__ import annotations

import ast
import copy
from pathlib import Path
import unittest

from multi_topic_evidence_consumer import (
    MULTI_TOPIC_QUESTION_CONTRACT_VERSION,
    MULTI_TOPIC_SUBJECT_EVIDENCE_VERSION,
    attach_multi_topic_evidence_to_subject_rubric,
    attach_multi_topic_summary_to_question_contract,
    build_multi_topic_question_contract_summary,
    build_multi_topic_subject_evidence,
    enrich_multi_topic_model_reference_with_contract,
)


RTD_TOPIC = (
    "rtd_temperature_sensor_principle_pt100_wiring_compensation"
)
TC_TOPIC = (
    "thermocouple_temperature_sensor_seebeck_"
    "reference_junction_compensation"
)


def reference_fixture() -> dict:
    return {
        "version": "model_answer_reference_v1",
        "matched": False,
        "primary_reference": None,
        "score": 24,
        "multi_topic_grading_context": {
            "version": "multi_topic_grading_context_v1",
            "enabled": True,
            "applicable": True,
            "routing_mode": "MULTI_TOPIC",
            "primary_topic_ids": [
                RTD_TOPIC,
                TC_TOPIC,
            ],
            "topic_evidence": [
                {
                    "topic_id": RTD_TOPIC,
                    "title": "RTD",
                    "candidate_reference": {
                        "topic_id": RTD_TOPIC,
                        "title": "RTD",
                    },
                    "model_answer": {
                        "topic_id": RTD_TOPIC,
                        "expected_structure": ["principle"],
                    },
                    "fact_anchor": {
                        "topic_id": RTD_TOPIC,
                        "core_terms": ["Pt100"],
                    },
                    "logic_check": {
                        "topic_id": RTD_TOPIC,
                        "checks": ["logic"],
                    },
                    "topic_importance": {
                        "topic_id": RTD_TOPIC,
                        "importance": "high",
                    },
                },
                {
                    "topic_id": TC_TOPIC,
                    "title": "Thermocouple",
                    "candidate_reference": {
                        "topic_id": TC_TOPIC,
                        "title": "Thermocouple",
                    },
                    "model_answer": {
                        "topic_id": TC_TOPIC,
                        "expected_structure": ["principle"],
                    },
                    "fact_anchor": {
                        "topic_id": TC_TOPIC,
                        "core_terms": ["Seebeck"],
                    },
                    "logic_check": {
                        "topic_id": TC_TOPIC,
                        "checks": ["logic"],
                    },
                    "topic_importance": {
                        "topic_id": TC_TOPIC,
                        "importance": "high",
                    },
                },
            ],
            "demand_mappings": [
                {
                    "demand_id": "D1",
                    "topic_id": RTD_TOPIC,
                    "role": "PRIMARY",
                },
                {
                    "demand_id": "D1",
                    "topic_id": TC_TOPIC,
                    "role": "PRIMARY",
                },
            ],
            "uncovered_demand_ids": [],
            "policy": {
                "one_question_one_score": True,
                "topic_score_summing": False,
                "topic_score_averaging": False,
            },
        },
    }


class MultiTopicEvidenceConsumerUnitTest(unittest.TestCase):
    def test_subject_evidence_uses_model_and_fact_only(self):
        ref = reference_fixture()
        result = build_multi_topic_subject_evidence(ref)

        self.assertEqual(
            result["version"],
            MULTI_TOPIC_SUBJECT_EVIDENCE_VERSION,
        )
        self.assertEqual(
            result["primary_topic_ids"],
            [RTD_TOPIC, TC_TOPIC],
        )
        self.assertEqual(len(result["topics"]), 2)

        for row in result["topics"]:
            self.assertIn("model_answer", row)
            self.assertIn("fact_anchor", row)
            self.assertNotIn("logic_check", row)
            self.assertNotIn("topic_importance", row)

        policy = result["policy"]
        self.assertTrue(policy["one_question_one_score"])
        self.assertFalse(policy["topic_score_summing"])
        self.assertFalse(policy["topic_score_averaging"])
        self.assertFalse(
            policy["logic_topic_id_list_overload"]
        )
        self.assertFalse(
            policy["difficulty_aggregation"]
        )

    def test_subject_rubric_attachment_is_parallel(self):
        ref = reference_fixture()
        rubric = {
            "legacy_key": "keep",
            "model_answer_reference": {
                "topic_id": "legacy_topic"
            },
        }
        before = copy.deepcopy(rubric)

        result = attach_multi_topic_evidence_to_subject_rubric(
            rubric,
            ref,
        )

        self.assertEqual(rubric, before)
        self.assertEqual(
            result["legacy_key"],
            "keep",
        )
        self.assertEqual(
            result["model_answer_reference"],
            before["model_answer_reference"],
        )
        self.assertIn(
            "multi_topic_grading_evidence",
            result,
        )

    def test_question_contract_summary_is_non_scoring(self):
        ref = reference_fixture()

        summary = build_multi_topic_question_contract_summary(
            ref
        )
        self.assertEqual(
            summary["version"],
            MULTI_TOPIC_QUESTION_CONTRACT_VERSION,
        )
        self.assertEqual(
            summary["primary_topic_ids"],
            [RTD_TOPIC, TC_TOPIC],
        )
        self.assertTrue(
            summary["coverage_policy"][
                "combined_primary_topic_coverage"
            ]
        )
        self.assertFalse(
            summary["coverage_policy"][
                "primary_reference_overloaded"
            ]
        )

    def test_contract_attachment_preserves_legacy_fields(self):
        ref = reference_fixture()
        contract = {
            "version": "question_contract_v1",
            "required_dimensions": ["principle"],
        }
        before = copy.deepcopy(contract)

        result = attach_multi_topic_summary_to_question_contract(
            contract,
            ref,
        )

        self.assertEqual(contract, before)
        for key, value in before.items():
            self.assertEqual(result[key], value)
        self.assertIn(
            "multi_topic_grading_context_summary",
            result,
        )

    def test_model_reference_enrichment_stays_inside_parallel_context(self):
        ref = reference_fixture()
        contract = attach_multi_topic_summary_to_question_contract(
            {
                "version": "question_contract_v1",
            },
            ref,
        )
        before = copy.deepcopy(ref)

        result = enrich_multi_topic_model_reference_with_contract(
            ref,
            contract,
        )

        self.assertEqual(ref, before)
        self.assertEqual(
            result["matched"],
            before["matched"],
        )
        self.assertEqual(
            result["primary_reference"],
            before["primary_reference"],
        )
        self.assertEqual(
            result["score"],
            before["score"],
        )
        self.assertIn(
            "question_contract_summary",
            result["multi_topic_grading_context"],
        )

    def test_non_multi_reference_is_identity(self):
        ref = {
            "matched": True,
            "primary_reference": {
                "topic_id": RTD_TOPIC,
            },
        }
        rubric = {"legacy": True}
        contract = {"legacy": True}

        self.assertIs(
            attach_multi_topic_evidence_to_subject_rubric(
                rubric,
                ref,
            ),
            rubric,
        )
        self.assertIs(
            attach_multi_topic_summary_to_question_contract(
                contract,
                ref,
            ),
            contract,
        )
        self.assertIs(
            enrich_multi_topic_model_reference_with_contract(
                ref,
                contract,
            ),
            ref,
        )


class MultiTopicEvidenceConsumerIntegrationShapeTest(
    unittest.TestCase
):
    def test_phase2_contains_exact_three_consumer_calls(self):
        path = Path("grading_agents.py")
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)

        fn = next(
            node
            for node in tree.body
            if (
                isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and node.name == "_phase2_postprocess_grade"
            )
        )

        def call_name(call):
            func = call.func
            if isinstance(func, ast.Name):
                return func.id
            if isinstance(func, ast.Attribute):
                return func.attr
            return None

        expected = {
            "attach_multi_topic_summary_to_question_contract": 1,
            "enrich_multi_topic_model_reference_with_contract": 1,
            "attach_multi_topic_evidence_to_subject_rubric": 1,
        }

        lines = {}
        for name, expected_count in expected.items():
            calls = [
                node
                for node in ast.walk(fn)
                if (
                    isinstance(node, ast.Call)
                    and call_name(node) == name
                )
            ]
            self.assertEqual(
                len(calls),
                expected_count,
            )
            lines[name] = calls[0].lineno

        self.assertLess(
            lines[
                "attach_multi_topic_summary_to_question_contract"
            ],
            lines[
                "enrich_multi_topic_model_reference_with_contract"
            ],
        )
        self.assertLess(
            lines[
                "enrich_multi_topic_model_reference_with_contract"
            ],
            lines[
                "attach_multi_topic_evidence_to_subject_rubric"
            ],
        )

    def test_scalar_logic_and_difficulty_contracts_not_overloaded(self):
        text = Path(
            "grading_agents.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn(
            "multi_topic_logic_topic_ids",
            text,
        )
        self.assertNotIn(
            "multi_topic_difficulty",
            text,
        )


if __name__ == "__main__":
    unittest.main()
