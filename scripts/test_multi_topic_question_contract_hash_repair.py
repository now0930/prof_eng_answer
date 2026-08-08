from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from multi_topic_evidence_consumer import (
    attach_multi_topic_summary_to_question_contract,
)
from question_contract import (
    build_question_contract,
    rehash_question_contract,
    validate_question_contract,
)


RTD_TOPIC = (
    "rtd_temperature_sensor_principle_pt100_wiring_compensation"
)
TC_TOPIC = (
    "thermocouple_temperature_sensor_seebeck_"
    "reference_junction_compensation"
)


def multi_topic_reference() -> dict:
    return {
        "version": "model_answer_reference_v1",
        "matched": False,
        "primary_reference": None,
        "candidates": [],
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
                    "model_answer": {
                        "topic_id": RTD_TOPIC,
                    },
                    "fact_anchor": {
                        "topic_id": RTD_TOPIC,
                    },
                },
                {
                    "topic_id": TC_TOPIC,
                    "title": "Thermocouple",
                    "model_answer": {
                        "topic_id": TC_TOPIC,
                    },
                    "fact_anchor": {
                        "topic_id": TC_TOPIC,
                    },
                },
            ],
            "demand_mappings": [],
            "uncovered_demand_ids": [],
        },
    }


def build_valid_contract() -> dict:
    subject_rubric = {
        "name": "stage6h2b fixture",
        "version": "1",
        "question_type_profile": None,
        "fact_anchor_bank": None,
        "model_answer_bank": None,
    }

    with tempfile.TemporaryDirectory() as tmp:
        snapshot = Path(tmp) / "subject_rubric_snapshot.json"
        snapshot.write_text(
            json.dumps(
                subject_rubric,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        contract = build_question_contract(
            grading_identity={
                "normalization_version": "grading_identity_v1",
                "question_hash": "q" * 64,
                "submission_hash": "s" * 64,
            },
            question_type_evaluation={
                "question_type": "DEFINE",
                "confidence": "high",
                "status": "locked",
                "locked": True,
                "source": "rule",
                "matched_rules": ["DEFINE"],
                "warning": None,
            },
            fact_evaluation={},
            model_answer_reference=multi_topic_reference(),
            rubric_snapshot_path=snapshot,
            subject_rubric=subject_rubric,
        )

    validate_question_contract(contract)
    return contract


class MultiTopicQuestionContractHashRepairTest(unittest.TestCase):
    def test_public_rehash_preserves_valid_contract(self):
        contract = build_valid_contract()
        result = rehash_question_contract(contract)

        validate_question_contract(result)
        self.assertEqual(
            result["contract_hash"],
            contract["contract_hash"],
        )

    def test_authoritative_summary_attachment_rehashes(self):
        contract = build_valid_contract()
        before = copy.deepcopy(contract)

        result = attach_multi_topic_summary_to_question_contract(
            contract,
            multi_topic_reference(),
        )

        self.assertEqual(contract, before)
        self.assertIn(
            "multi_topic_grading_context_summary",
            result,
        )
        self.assertNotEqual(
            result["contract_hash"],
            before["contract_hash"],
        )
        validate_question_contract(result)

    def test_summary_is_protected_by_contract_hash(self):
        contract = attach_multi_topic_summary_to_question_contract(
            build_valid_contract(),
            multi_topic_reference(),
        )

        tampered = copy.deepcopy(contract)
        tampered["multi_topic_grading_context_summary"][
            "primary_topic_ids"
        ].append("tampered_topic")

        with self.assertRaisesRegex(
            ValueError,
            "Question contract hash mismatch",
        ):
            validate_question_contract(tampered)

    def test_lightweight_non_authoritative_dict_remains_supported(self):
        contract = {
            "version": "question_contract_v1",
            "required_dimensions": ["principle"],
        }

        result = attach_multi_topic_summary_to_question_contract(
            contract,
            multi_topic_reference(),
        )

        self.assertIn(
            "multi_topic_grading_context_summary",
            result,
        )
        self.assertNotIn("contract_hash", result)


if __name__ == "__main__":
    unittest.main()
