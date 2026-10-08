#!/usr/bin/env python3
"""Regression checks for the four confirmed Topic Pack anchor corrections."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.fact_anchor_evidence_adapter import evaluate_fact_anchor_requirements


SW05 = "sis_sil_safety_software_independence_systematic_failure_verification_validation"
SIL_TARGET = "sil_target_determination_risk_reduction_and_lifecycle"
BOUNDARY_CASES = (
    (
        "random_hardware_failure__unit_test_not_random_hardware_integrity",
        "단위시험(Unit Testing)은 소프트웨어 모듈의 결함을 검출하는 활동이다. random hardware failure에 대한 하드웨어 무결성 입증과 동일하지 않다.",
        "Random Hardware Failure는 시간에 따른 물리적 열화에서 발생하는 확률적 고장이다.",
    ),
    (
        "random_hardware_failure_unit_test_not_random_hardware_integrity__misra_not_unit_test_tool",
        "MISRA는 코딩 표준 준수와 정적분석 관점의 규칙 집합이다. 단위시험 도구로 분류하지 않는다.",
        "Random Hardware Failure는 시간에 따른 물리적 열화에서 발생하는 확률적 고장이다.",
    ),
    (
        "sis_mcdc_structural_coverage_boundary__vmodel_does_not_guarantee_sil",
        "V-model은 생명주기 검증 구조를 제공하지만 그 자체만으로 SIL 달성을 보장하지 않는다.",
        "SW-05는 SIL 안전수명주기와 Safety V&V의 적용근거를 소유하되 MC/DC 증거 상세는 전용 Topic으로 이관한다.",
    ),
)


def load_fact(topic_id: str) -> dict:
    return json.loads(
        (ROOT / "rubrics" / "topic_packs" / topic_id / "fact_anchor.json").read_text(encoding="utf-8")
    )


class ConfirmedAnchorCorrectionsTests(unittest.TestCase):
    def test_sw05_boundary_statements_match_scoring_evidence(self) -> None:
        fact = load_fact(SW05)
        anchors = {row["anchor_id"]: row for row in fact["anchors"]}
        logic = json.loads(
            (ROOT / "rubrics" / "topic_packs" / SW05 / "logic_check.json").read_text(encoding="utf-8")
        )
        truth = logic["llm_profile"]["truth_schema"]
        for anchor_id, correct, unrelated in BOUNDARY_CASES:
            with self.subTest(anchor_id=anchor_id):
                anchor = anchors[anchor_id]
                self.assertIn(anchor["statement"], fact["core_facts"])
                self.assertIn(anchor["statement"], truth)
                self.assertNotIn("[", anchor["statement"])
                for answer, expected in ((correct, "SATISFIED"), (unrelated, "NOT_SATISFIED")):
                    result = evaluate_fact_anchor_requirements(
                        question_text=correct,
                        answer_text=answer,
                        topic_ids=[SW05],
                    )
                    status = next(
                        row["status"] for row in result["requirements"]
                        if row["requirement_id"] == anchor_id
                    )
                    if expected == "SATISFIED":
                        self.assertEqual(status, "SATISFIED")
                    else:
                        self.assertNotEqual(status, "SATISFIED")

    def test_alarp_boundary_is_consistent(self) -> None:
        fact = load_fact(SIL_TARGET)
        anchor = next(row for row in fact["anchors"] if row["anchor_id"] == "tolerable_risk_alarp")
        for key in ("statement", "claim", "accepted_explanations"):
            value = anchor[key]
            text = " ".join(value) if isinstance(value, list) else value
            self.assertIn("현저히 불균형", text)
            self.assertIn("위험저감", text)
        self.assertIn("단순한 비용 대비 편익", anchor["rejected_explanations"][1])


if __name__ == "__main__":
    unittest.main()
