#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing"
MODEL = ROOT / "rubrics" / "topic_packs" / TOPIC_ID / "model_answer.json"
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

Q_TSN = "산업 Ethernet의 실시간 통신과 TSN을 설명하시오."
Q_ZERO = "산업제어시스템 Network Segmentation과 Zero Trust를 설명하시오."


class SW11CrossLaneOwnershipRepairTests(unittest.TestCase):
    def test_model_owner_contract(self) -> None:
        data = json.loads(MODEL.read_text(encoding="utf-8"))
        rows = data["negative_boundary_questions"]
        self.assertEqual(8, len(rows))
        owners = {row["question"]: row["owner"] for row in rows}
        self.assertEqual("SW-08", owners[Q_TSN])
        self.assertEqual("SW-09", owners[Q_ZERO])

    def test_topic_sheet_matches_model(self) -> None:
        body = SHEET.read_text(encoding="utf-8")
        self.assertIn(f"{Q_TSN} → SW-08", body)
        self.assertIn(f"{Q_ZERO} → SW-09", body)
        self.assertNotIn(f"{Q_TSN} → SW-07", body)
        self.assertNotIn(f"{Q_ZERO} → SW-08", body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
