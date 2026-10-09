#!/usr/bin/env python3
"""Validate the 200-anchor review register and its one corrected source claim."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/topic_anchor_fact_review_batch_20261008_200.md"
TOPICS = (
    "sis_sil_safety_software_independence_systematic_failure_verification_validation",
    "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis",
    "final_control_element_sil_sis_esd_valve_partial_stroke_test",
    "hipps_overpressure_protection_relief_system_2oo3_1oo2_architecture",
    "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response",
    "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle",
)
CORRECTED_MCDC = (
    "MC/DC는 각 Decision의 True·False 결과와 각 조건의 True·False, "
    "그리고 대상 조건이 Decision 결과에 독립적으로 영향을 주는 Test Pair를 요구한다. "
    "모든 진입점·종료점 실행은 적용 표준의 전체 구조 커버리지 목표로 함께 확인하되 "
    "MC/DC 정의와 구분한다."
)


class AnchorFactReviewBatchTests(unittest.TestCase):
    def test_register_covers_exactly_200_unique_source_anchors(self) -> None:
        report = REPORT.read_text(encoding="utf-8")
        rows = re.findall(r"^\| `(.*?)` \| (확인|수정|적용조건|추가근거) \|", report, re.M)
        expected = []
        for topic_id in TOPICS:
            pack = json.loads(
                (ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json").read_text(
                    encoding="utf-8"
                )
            )
            limit = 20 if topic_id == TOPICS[-1] else len(pack["anchors"])
            expected.extend(anchor["id"] for anchor in pack["anchors"][:limit])

        actual_ids = [anchor_id for anchor_id, _ in rows]
        self.assertEqual(len(rows), 200)
        self.assertEqual(len(set(actual_ids)), 200)
        self.assertCountEqual(actual_ids, expected)
        self.assertEqual(
            Counter(status for _, status in rows),
            Counter({"확인": 184, "적용조건": 14, "수정": 1, "추가근거": 1}),
        )

    def test_mcdc_definition_correction_is_consistent(self) -> None:
        topic_dir = ROOT / "rubrics/topic_packs" / TOPICS[1]
        fact = json.loads((topic_dir / "fact_anchor.json").read_text(encoding="utf-8"))
        logic = json.loads((topic_dir / "logic_check.json").read_text(encoding="utf-8"))
        anchor = next(row for row in fact["anchors"] if row["anchor_id"] == "mcdc_definition")
        self.assertEqual(anchor["statement"], CORRECTED_MCDC)
        self.assertEqual(anchor["claim"], CORRECTED_MCDC)
        self.assertEqual(anchor["accepted_explanations"][0], CORRECTED_MCDC)
        self.assertIn(CORRECTED_MCDC, logic["llm_profile"]["truth_schema"])


if __name__ == "__main__":
    unittest.main()
