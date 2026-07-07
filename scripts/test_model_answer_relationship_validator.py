#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

from scripts.validate_model_answer_relationships import (
    load_bank,
    order_score,
    similarity,
    validate_expected_vs_outline,
    validate_outline_vs_high_score,
)


ROOT = Path(__file__).resolve().parents[1]
MODEL_BANK = (
    ROOT
    / "rubrics/model_answers"
    / "industrial_instrumentation_control.json"
)


class RelationshipValidatorRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        answers = load_bank(MODEL_BANK)
        cls.by_id = {
            str(row.get("id", "")): row
            for row in answers
        }

    def test_heading_with_korean_particle_is_direct_match(self):
        self.assertEqual(
            similarity(
                "준비 사항",
                "준비 사항으로 입력 자료와 표준기를 정리한다.",
            ),
            1.0,
        )
        self.assertEqual(
            similarity(
                "개요",
                "개요에서 교정 목적과 적용 배경을 제시한다.",
            ),
            1.0,
        )

    def test_unrelated_heading_is_not_forced_to_match(self):
        self.assertLess(
            similarity(
                "개요",
                "위험 원인과 개선 대책을 분석한다.",
            ),
            0.30,
        )

    def test_single_character_abbreviation_does_not_use_containment(self):
        self.assertLess(
            similarity(
                "P",
                "PID 제어기의 비례 동작을 설명한다.",
            ),
            1.0,
        )

    def test_known_complete_outlines_have_no_expected_structure_issue(self):
        answer_ids = [
            "cv_valve_flow_coefficient_CALC_DESIGN_v1",
            "calibration_error_accuracy_precision_PROCEDURE_v1",
            "pid_control_PRINCIPLE_INTERPRETATION_v1",
        ]

        for answer_id in answer_ids:
            with self.subTest(answer_id=answer_id):
                issues = validate_expected_vs_outline(
                    self.by_id[answer_id]
                )
                self.assertEqual(issues, [])

    def test_calibration_outline_order_is_preserved(self):
        row = self.by_id[
            "calibration_error_accuracy_precision_PROCEDURE_v1"
        ]

        self.assertEqual(
            order_score(
                row["expected_structure"],
                row["model_answer_outline"],
            ),
            1.0,
        )

    def test_repaired_cabinet_has_no_relationship_issue(self):
        row = self.by_id[
            "local_instrument_cabinet_installation_"
            "DIAGNOSIS_ACTION_v1"
        ]

        self.assertEqual(
            validate_expected_vs_outline(row),
            [],
        )
        self.assertEqual(
            validate_outline_vs_high_score(row),
            [],
        )

    def test_synthetic_content_gap_remains_visible(self):
        row = {
            "id": "synthetic_content_gap_v1",
            "topic_id": "synthetic_content_gap",
            "expected_structure": [
                "개요",
                "원리",
                "현장 적용",
            ],
            "model_answer_outline": [
                "개요에서 측정 시스템의 목적과 적용 배경을 제시한다.",
                "원리에서 입력과 출력의 기본 관계를 설명한다.",
                "현장 적용에서 설치 위치와 운전 조건을 검토한다.",
            ],
            "high_score_features": [
                "정확도와 정밀도의 차이를 수식과 사례로 설명한다.",
                "교정 전후 오차와 측정 불확도를 정량 비교한다.",
                "표준기 추적성과 교정 주기 관리 기준을 제시한다.",
                "온도와 진동 등 환경 조건에 따른 오차를 평가한다.",
            ],
        }

        expected_issues = validate_expected_vs_outline(row)
        high_score_issues = validate_outline_vs_high_score(row)

        self.assertEqual(expected_issues, [])
        self.assertTrue(
            any(
                issue.relation
                == "model_answer_outline_vs_high_score_features"
                for issue in high_score_issues
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
