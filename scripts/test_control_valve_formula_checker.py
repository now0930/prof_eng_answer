from __future__ import annotations

import copy
import unittest
from pathlib import Path

from control_valve_formula_checker import (
    TARGET_TOPIC_ID,
    attach_control_valve_formula_check,
    evaluate_control_valve_formula_check,
)


class ControlValveFormulaCheckerTests(
    unittest.TestCase
):
    def test_non_target_topic_is_skipped(
        self,
    ):
        result = (
            evaluate_control_valve_formula_check(
                answer_text="Fu=(P1-P2)*A",
                topic_id="other_topic",
            )
        )

        self.assertFalse(
            result["applicable"]
        )
        self.assertEqual(
            result["verdict"],
            "not_applicable",
        )

    def test_korean_postposition_direction_is_recognized(
        self,
    ):
        answer = """
        열림 방향을 양(+)의 방향으로 정의한다.
        P1은 열림 방향으로 작용한다.
        P2는 닫힘 방향으로 작용한다.
        Fu = P1*A - P2*A
        """

        result = (
            evaluate_control_valve_formula_check(
                answer_text=answer,
                topic_id=TARGET_TOPIC_ID,
            )
        )

        context = result[
            "direction_context"
        ]

        self.assertEqual(
            context["positive_direction"],
            "open",
        )
        self.assertEqual(
            context["p1_direction"],
            "open",
        )
        self.assertEqual(
            context["p2_direction"],
            "close",
        )
        self.assertEqual(
            context[
                "expected_formula_sign"
            ],
            "p1_minus_p2",
        )
        self.assertEqual(
            result["verdict"],
            "pass",
        )

    def test_equivalent_pressure_formula_passes(
        self,
    ):
        answer = """
        열림 방향을 양(+)의 방향으로 정의한다.
        P1은 열림 방향으로 작용한다.
        P2는 닫힘 방향으로 작용한다.
        Fu = (P1-P2)*A
        """

        result = (
            evaluate_control_valve_formula_check(
                answer_text=answer,
                topic_id=TARGET_TOPIC_ID,
            )
        )

        self.assertEqual(
            result["verdict"],
            "pass",
        )
        self.assertFalse(
            result[
                "major_error_detected"
            ]
        )
        self.assertEqual(
            result["findings"],
            [],
        )

    def test_reversed_sign_is_major_only_with_premise(
        self,
    ):
        answer = """
        열림 방향을 양(+)의 방향으로 정의한다.
        P1은 열림 방향으로 작용한다.
        P2는 닫힘 방향으로 작용한다.
        Fu = (P2-P1)*A
        """

        result = (
            evaluate_control_valve_formula_check(
                answer_text=answer,
                topic_id=TARGET_TOPIC_ID,
            )
        )

        ids = {
            item["id"]
            for item in result["findings"]
        }

        self.assertEqual(
            result["verdict"],
            "major",
        )
        self.assertIn(
            "pressure_difference_"
            "direction_reversed",
            ids,
        )

    def test_missing_direction_is_warning(
        self,
    ):
        result = (
            evaluate_control_valve_formula_check(
                answer_text=(
                    "Fu=(P1-P2)*A"
                ),
                topic_id=TARGET_TOPIC_ID,
            )
        )

        ids = {
            item["id"]
            for item in result["findings"]
        }

        self.assertEqual(
            result["verdict"],
            "warn",
        )
        self.assertFalse(
            result[
                "major_error_detected"
            ]
        )
        self.assertIn(
            "pressure_direction_"
            "not_declared",
            ids,
        )

    def test_pressure_force_without_area_is_major(
        self,
    ):
        result = (
            evaluate_control_valve_formula_check(
                answer_text=(
                    "불평형력 Fu=P1-P2"
                ),
                topic_id=TARGET_TOPIC_ID,
            )
        )

        ids = {
            item["id"]
            for item in result["findings"]
        }

        self.assertEqual(
            result["verdict"],
            "major",
        )
        self.assertIn(
            "pressure_force_missing_area",
            ids,
        )

    def test_friction_assisting_motion_is_major(
        self,
    ):
        answer = """
        열림 방향을 양(+)의 방향으로 정의한다.
        P1은 열림 방향으로 작용한다.
        P2는 닫힘 방향으로 작용한다.
        Fu=(P1-P2)*A
        마찰력은 이동 방향과 같은 방향으로 작용한다.
        """

        result = (
            evaluate_control_valve_formula_check(
                answer_text=answer,
                topic_id=TARGET_TOPIC_ID,
            )
        )

        ids = {
            item["id"]
            for item in result["findings"]
        }

        self.assertIn(
            "friction_direction_"
            "assists_motion",
            ids,
        )
        self.assertEqual(
            result["verdict"],
            "major",
        )

    def test_attach_preserves_scores_and_order(
        self,
    ):
        grade = {
            "topic_id": TARGET_TOPIC_ID,
            "total_score": 12.34,
            "final_total_score": 12.34,
            "total_before_cap": 12.34,
            "score_range": "12~12",
            "breakdown": {
                "A": {"score": 2.0},
                "B": {"score": 3.0},
                "C": {"score": 4.0},
                "D": {"score": 2.0},
                "E": {"score": 1.34},
            },
            "applied_caps": [],
            "rater_results": [
                {"score": 12.34}
            ],
        }
        before = copy.deepcopy(grade)

        output = (
            attach_control_valve_formula_check(
                grade,
                "Fu=(P1-P2)*A",
            )
        )

        for key in [
            "total_score",
            "final_total_score",
            "total_before_cap",
            "score_range",
            "breakdown",
            "applied_caps",
            "rater_results",
        ]:
            self.assertEqual(
                output[key],
                before[key],
            )

        self.assertEqual(
            grade,
            before,
        )

        evaluation = output[
            "formula_check_evaluation"
        ]

        self.assertEqual(
            evaluation["score_effect"],
            "diagnostic_only",
        )
        self.assertFalse(
            evaluation[
                "direct_score_application"
            ]
        )

        source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )

        logic_position = source.index(
            "grade = "
            "attach_logic_check_to_grade("
        )
        formula_position = source.index(
            "grade = "
            "attach_control_valve_formula_check("
        )
        phase15_position = source.index(
            "grade = "
            "_phase15_hide_internal_metric_dict("
        )
        persistence_position = source.index(
            '"formula_check_evaluation.json"'
        )

        self.assertLess(
            logic_position,
            formula_position,
        )
        self.assertLess(
            formula_position,
            phase15_position,
        )
        self.assertLess(
            formula_position,
            persistence_position,
        )

        checker_source = Path(
            "control_valve_formula_checker.py"
        ).read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "eval(",
            checker_source,
        )
        self.assertNotIn(
            "exec(",
            checker_source,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
