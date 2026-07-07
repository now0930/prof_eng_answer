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

    def test_real_cabinet_content_gap_remains_visible(self):
        row = self.by_id[
            "local_instrument_cabinet_installation_"
            "DIAGNOSIS_ACTION_v1"
        ]

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
