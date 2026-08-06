#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control"
MODEL = ROOT / "rubrics" / "topic_packs" / TOPIC_ID / "model_answer.json"
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

OLD_QUESTION = "Robot용 Ethernet의 Frame, QoS와 Redundancy Protocol을 설명하시오."
NEW_QUESTION = "Robot 제어망의 QoS, Redundancy와 장애복구 성능을 설명하시오."
PROTOCOL_QUESTION = "OPC UA와 MQTT Protocol의 상호운용성을 설명하시오."


class SW13CrossLaneOwnershipRepairTests(unittest.TestCase):
    def test_model_owner_contract(self) -> None:
        data = json.loads(MODEL.read_text(encoding="utf-8"))
        rows = data["negative_boundary_examples"]
        self.assertEqual(8, len(rows))
        owners = {row["question"]: row["owner"] for row in rows}
        self.assertEqual("SW-08", owners[NEW_QUESTION])
        self.assertEqual("SW-07", owners[PROTOCOL_QUESTION])
        self.assertNotIn(OLD_QUESTION, owners)

    def test_topic_sheet_matches_model(self) -> None:
        body = SHEET.read_text(encoding="utf-8")
        self.assertIn(f"{NEW_QUESTION} → SW-08", body)
        self.assertIn(f"{PROTOCOL_QUESTION} → SW-07", body)
        self.assertNotIn(OLD_QUESTION, body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
