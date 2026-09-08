#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class AnalogCurrentLoopTopicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.model = load("model_answer.json")
        cls.logic = load("logic_check.json")
        cls.importance = load("topic_importance.json")
        cls.status = load("topic_status.json")
        cls.anchors = {
            row["anchor_id"]: row for row in cls.fact["anchors"]
        }

    def test_identity_and_managed_approval(self) -> None:
        for document in (
            self.fact,
            self.model,
            self.logic,
            self.importance,
            self.status,
        ):
            self.assertEqual(document["topic_id"], TOPIC_ID)
        self.assertEqual(self.status["status"], "approved")
        self.assertEqual(self.status["review_state"], "reviewed")
        self.assertEqual(self.status["review_method"], "human")

    def test_anchor_inventory_and_question_references(self) -> None:
        self.assertEqual(len(self.anchors), 10)
        self.assertEqual(len(self.model["expected_question_patterns"]), 3)
        for pattern in self.model["expected_question_patterns"]:
            self.assertTrue(
                set(pattern["required_anchor_ids"]) <= set(self.anchors)
            )
        outline_refs = {
            anchor_id
            for section in self.model["recommended_outline"]
            for anchor_id in section["anchor_refs"]
        }
        self.assertEqual(outline_refs, set(self.anchors))

    def test_live_zero_and_two_wire_contract(self) -> None:
        live_zero = self.anchors["acl_live_zero_fault_discrimination"]["statement"]
        two_wire = self.anchors["acl_two_wire_loop_powered"]["statement"]
        self.assertIn("4 mA live zero", live_zero)
        self.assertIn("0 mA", live_zero)
        self.assertIn("단선", live_zero)
        self.assertIn("전원과 신호가 한 쌍을 공유", two_wire)
        self.assertIn("loop supply", two_wire)

    def test_source_sink_compatibility_contract(self) -> None:
        source = self.anchors["acl_active_source_output"]["statement"]
        sink = self.anchors["acl_passive_sink_output"]["statement"]
        compatibility = self.anchors["acl_source_sink_compatibility"]["statement"]
        self.assertIn("전원과 전류를 공급", source)
        self.assertIn("외부 전원", sink)
        self.assertIn("전원 충돌", compatibility)
        self.assertIn("극성", compatibility)

    def test_wire_resistance_claim_is_conditioned_by_load_budget(self) -> None:
        budget = self.anchors["acl_compliance_voltage_load_budget"]["statement"]
        self.assertIn("최소 동작전압", budget)
        self.assertIn("최대 전압강하", budget)
        misconception = {
            row["id"]: row for row in self.logic["misconception_contract"]
        }["acl_wire_resistance_irrelevant"]
        self.assertEqual(misconception["severity"], "major")
        self.assertIn("compliance budget", misconception["correct_rule"])

    def test_diagnostics_are_mode_safe_and_end_to_end(self) -> None:
        isolation = self.anchors["acl_calibrator_isolation_workflow"]["statement"]
        verification = self.anchors["acl_closed_loop_verification"]["statement"]
        self.assertIn("measure·source·2-wire simulate", isolation)
        self.assertIn("회로 전원 상태", isolation)
        self.assertIn("4·12·20 mA", verification)
        self.assertIn("alarm·trip 방향", verification)

    def test_semantic_contract_has_no_llm_verdict_authority(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        self.assertFalse(deterministic["enabled"])
        self.assertEqual(deterministic["fatal_checks"], [])
        self.assertEqual(deterministic["major_checks"], [])
        self.assertFalse(self.logic["llm_profile"]["enabled"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
