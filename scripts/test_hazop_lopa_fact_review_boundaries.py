#!/usr/bin/env python3
"""Keep the source-backed LOPA/ALARP/MOC distinctions in the Topic contract."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPIC = ROOT / "rubrics/topic_packs/hazop_lopa_ipl_risk_reduction_sil_target_allocation"


class HazopLopaFactReviewBoundariesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = json.loads((TOPIC / "fact_anchor.json").read_text(encoding="utf-8"))
        cls.truth = json.loads((TOPIC / "logic_check.json").read_text(encoding="utf-8"))[
            "llm_profile"
        ]["truth_schema"]
        cls.anchors = {row["anchor_id"]: row for row in cls.fact["anchors"]}

    def test_independent_ipl_does_not_claim_zero_common_cause(self) -> None:
        anchor = self.anchors["hazop_lopa_ipl_independence"]
        self.assertIn("공통원인", anchor["statement"])
        self.assertIn("평가·관리", anchor["statement"])
        self.assertNotIn("동시에 상실되지 않는다", anchor["statement"])
        self.assertIn(anchor["statement"], self.truth)

    def test_ratio_below_one_does_not_erase_alarp(self) -> None:
        anchor = self.anchors["hazop_lopa_no_additional_sif_when_ratio_below_one"]
        self.assertIn("해당 빈도 기준만으로는", anchor["statement"])
        self.assertIn("ALARP", anchor["statement"])
        self.assertTrue(any("1 이하이면" in row and "ALARP" in row for row in self.truth))

    def test_moc_revalidation_depends_on_impact(self) -> None:
        anchor = self.anchors["hazop_lopa_scenario_aggregation_moc"]
        self.assertIn("MOC 영향평가", anchor["statement"])
        self.assertIn("영향이 있을 때", anchor["statement"])
        self.assertIn("필요한 범위", anchor["statement"])
        self.assertIn(anchor["statement"], self.truth)


if __name__ == "__main__":
    unittest.main()
