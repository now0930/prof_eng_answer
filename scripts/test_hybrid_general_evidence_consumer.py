from __future__ import annotations

import unittest
from unittest.mock import patch

from hybrid_general_evidence_consumer import (
    attach_hybrid_general_evidence_to_subject_rubric,
    attach_hybrid_general_summary_to_question_contract,
    build_hybrid_general_question_contract_summary,
    build_hybrid_general_subject_evidence,
    enrich_hybrid_general_model_reference_with_contract,
)


def hybrid_ref() -> dict:
    return {
        "matched": True,
        "primary_reference": {
            "topic_id": "topic_a",
        },
        "hybrid_general_grading_context": {
            "version": "hybrid_general_grading_context_v1",
            "enabled": True,
            "applicable": True,
            "routing_mode": "SINGLE_TOPIC",
            "coverage_kind": "HYBRID_TOPIC_GENERAL",
            "primary_topic_ids": ["topic_a"],
            "topic_evidence": [
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
            "demand_mappings": [
                {
                    "demand_id": "D1",
                    "topic_id": "topic_a",
                    "role": "PRIMARY",
                }
            ],
            "uncovered_demand_ids": ["D2"],
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
        },
    }


class HybridGeneralEvidenceConsumerTest(unittest.TestCase):
    def test_subject_evidence_boundary(self):
        evidence = build_hybrid_general_subject_evidence(
            hybrid_ref()
        )
        self.assertEqual(
            evidence["coverage_kind"],
            "HYBRID_TOPIC_GENERAL",
        )
        row = evidence["topics"][0]
        self.assertIn("model_answer", row)
        self.assertIn("fact_anchor", row)
        self.assertNotIn("logic_check", row)
        self.assertNotIn("topic_importance", row)
        self.assertFalse(
            evidence["general_engineering_evidence"][
                "score_component"
            ]
        )

    def test_subject_rubric_parallel_attachment(self):
        rubric = {"legacy": {"keep": True}}
        result = attach_hybrid_general_evidence_to_subject_rubric(
            rubric,
            hybrid_ref(),
        )
        self.assertEqual(result["legacy"], {"keep": True})
        self.assertIn(
            "hybrid_general_grading_evidence",
            result,
        )
        self.assertNotEqual(id(result), id(rubric))

    def test_question_summary_has_no_full_topic_payload(self):
        summary = build_hybrid_general_question_contract_summary(
            hybrid_ref()
        )
        self.assertEqual(
            summary["uncovered_demand_ids"],
            ["D2"],
        )
        self.assertNotIn("topic_evidence", summary)
        self.assertNotIn(
            "general_engineering_evidence",
            summary,
        )

    def test_contract_rehash_is_required(self):
        contract = {
            "contract_hash": "old",
            "legacy": True,
        }

        def fake_rehash(value):
            output = dict(value)
            output["contract_hash"] = "new"
            return output

        with patch(
            "question_contract.rehash_question_contract",
            side_effect=fake_rehash,
        ) as mocked:
            result = (
                attach_hybrid_general_summary_to_question_contract(
                    contract,
                    hybrid_ref(),
                )
            )

        mocked.assert_called_once()
        self.assertEqual(result["contract_hash"], "new")
        self.assertTrue(result["legacy"])

    def test_model_reference_enrichment_is_parallel(self):
        ref = hybrid_ref()
        contract = {
            "hybrid_general_grading_context_summary": {
                "coverage_kind": "HYBRID_TOPIC_GENERAL"
            }
        }
        result = (
            enrich_hybrid_general_model_reference_with_contract(
                ref,
                contract,
            )
        )
        self.assertEqual(
            result["primary_reference"],
            ref["primary_reference"],
        )
        self.assertEqual(
            result["hybrid_general_grading_context"][
                "question_contract_summary"
            ]["coverage_kind"],
            "HYBRID_TOPIC_GENERAL",
        )

    def test_invalid_context_is_noop(self):
        ref = hybrid_ref()
        ref["hybrid_general_grading_context"][
            "applicable"
        ] = False
        rubric = {"legacy": True}
        self.assertEqual(
            attach_hybrid_general_evidence_to_subject_rubric(
                rubric,
                ref,
            ),
            rubric,
        )


if __name__ == "__main__":
    unittest.main()
