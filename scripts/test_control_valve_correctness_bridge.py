from __future__ import annotations

import copy
import unittest
from pathlib import Path

import grading_agents
from control_valve_correctness_bridge import (
    merge_control_valve_findings_into_evidence,
)
from control_valve_formula_checker import (
    TARGET_TOPIC_ID,
    evaluate_control_valve_formula_check,
)
from question_demand_contract import (
    build_question_demand_contract,
)


# DUAL_CONTROL_VALVE_LIVE_CORRECTNESS_REGRESSION_V1

TITLE_ONLY = (
    "공압식 밸브의 불평형력·마찰력과 "
    "Fail Safe 스프링 설계 기준"
)
EXPLICIT_QUESTION = (
    "공압식 밸브 선정시 밸브의 불평형력, "
    "마찰력 개념 설명. "
    "Fail safe 동작 구현을 위한 "
    "Spring 설계 기준 제시"
)

GOOD_ANSWER = '''
밸브 마찰력은 패킹, 스템 가이드, 시트 접촉,
Breakaway Force, Stiction과 Hysteresis로 구성된다.
단순히 속도에 비례하지 않으며 최초 기동 시
정지마찰이 운동마찰보다 클 수 있다.
Fu(x)=Delta_P*A_e(x)
Fs(x)=F0+k*x
Fail Open:
Fs(x)>=Fu,close(x)+Ff,max(x)+Fseat,release+Fmargin
Fail Close:
Fs(x)>=Fu,open(x)+Ff,max(x)+Fseat,required+Fmargin
전 스트로크에서 최소 여유력을 검증한다.
'''

BAD_ANSWER = '''
마찰력은 구동 속도에 비례하여 역방향으로 발생한다.
Fb = C * v
Fa + Fs - Fb + F1 - F2 = 0
Fa + Fs = Fb - F1 + F2
공기원 차단 시 Fa=0이므로
Fs = Fb - F1 + F2
스프링 복원력 Fs는 최대 불평형력
(F1 - F2)과 마찰력 Fb의 합산 요구량보다
항상 크도록 설계한다.
'''


def question_contract():
    return build_question_demand_contract(
        EXPLICIT_QUESTION
    )


def grade_with_contract(
    evaluation,
):
    contract = question_contract()

    return {
        "score": 16.33,
        "total_score": 16.33,
        "topic_id": TARGET_TOPIC_ID,
        "question_demand_contract": copy.deepcopy(
            contract
        ),
        "formula_check_evaluation": copy.deepcopy(
            evaluation
        ),
        "parsed": {
            "question_demand_contract": copy.deepcopy(
                contract
            ),
            "general_evidence_contract": {
                "schema_version": "1.0",
                "contract_marker": (
                    "GENERAL_EVIDENCE_CONTRACT_V1"
                ),
                "mode": "diagnostic_only",
                "score_effect": "none",
                "claims": [],
                "formulas": [],
                "defects": [
                    {
                        "defect_id": "depth_gap",
                        "defect_type": "core_depth_gap",
                        "severity": "partial",
                        "owner_layer": "D",
                        "requirement_id": "",
                        "evidence_text": "",
                        "explanation": (
                            "최악조건 사이징 부족"
                        ),
                    }
                ],
                "field_judgements": [],
                "summary": {},
            },
            "question_type_coverage": {
                "overall_coverage": "strong",
                "explicit_requirement_coverage": {
                    "requirements": [
                        {
                            "requirement": (
                                "불평형력, 마찰력 "
                                "개념 설명"
                            ),
                            "status": "present",
                            "is_core": True,
                        },
                        {
                            "requirement": (
                                "Fail Safe Spring "
                                "설계 기준"
                            ),
                            "status": "present",
                            "is_core": True,
                        },
                    ]
                },
            },
        },
    }


def zero_layers():
    return [
        {
            "layer_id": layer,
            "score": 0.0,
            "max_score": maximum,
            "reason": "",
        }
        for layer, maximum in (
            ("A", 3.0),
            ("B", 6.0),
            ("C", 8.0),
            ("D", 6.0),
            ("E", 2.0),
        )
    ]


def baselines():
    return {
        "A": 2.8,
        "B": 5.7,
        "C": 5.2,
        "D": 5.0,
        "E": 1.7,
    }


def scoring_model():
    return {
        "layers": [
            {"id": "A", "points": 3},
            {"id": "B", "points": 6},
            {"id": "C", "points": 8},
            {"id": "D", "points": 6},
            {"id": "E", "points": 2},
        ]
    }


class DualControlValveCorrectnessTests(
    unittest.TestCase
):
    def test_title_only_contract_is_already_correct(self):
        contract = build_question_demand_contract(
            TITLE_ONLY
        )
        secondary = {
            row["demand_kind"]
            for row in contract[
                "secondary_demands"
            ]
        }

        self.assertEqual(
            contract["primary_lens"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertIn("DESIGN", secondary)
        self.assertTrue(
            contract["primary_lens_locked"]
        )
        self.assertEqual(
            contract["answer_text_dependency"],
            "none",
        )

    def test_bad_answer_emits_two_major_findings(self):
        result = evaluate_control_valve_formula_check(
            answer_text=BAD_ANSWER,
            topic_id=TARGET_TOPIC_ID,
        )
        by_id = {
            row["id"]: row
            for row in result["findings"]
        }

        self.assertIn(
            "friction_viscous_model_overgeneralized",
            by_id,
        )
        self.assertIn(
            "force_balance_requirement_sign_contradiction",
            by_id,
        )
        self.assertEqual(
            by_id[
                "friction_viscous_model_overgeneralized"
            ]["severity"],
            "major",
        )
        self.assertEqual(result["verdict"], "major")
        self.assertTrue(
            result["major_error_detected"]
        )

    def test_good_answer_has_no_new_major_finding(self):
        result = evaluate_control_valve_formula_check(
            answer_text=GOOD_ANSWER,
            topic_id=TARGET_TOPIC_ID,
        )
        ids = {
            row["id"]
            for row in result["findings"]
        }

        self.assertNotIn(
            "friction_viscous_model_overgeneralized",
            ids,
        )
        self.assertNotIn(
            "force_balance_requirement_sign_contradiction",
            ids,
        )

    def test_non_target_topic_is_unchanged(self):
        result = evaluate_control_valve_formula_check(
            answer_text=BAD_ANSWER,
            topic_id="other_topic",
        )

        self.assertFalse(result["applicable"])
        self.assertEqual(result["findings"], [])

    def test_major_findings_merge_as_c_correctness_defects(self):
        evaluation = evaluate_control_valve_formula_check(
            answer_text=BAD_ANSWER,
            topic_id=TARGET_TOPIC_ID,
        )
        grade = grade_with_contract(evaluation)
        before = copy.deepcopy(grade)
        merged = (
            merge_control_valve_findings_into_evidence(
                grade
            )
        )

        self.assertEqual(grade, before)
        self.assertEqual(
            merged["score"],
            before["score"],
        )
        self.assertEqual(
            merged["total_score"],
            before["total_score"],
        )

        defects = merged[
            "general_evidence_contract"
        ]["defects"]
        correctness = [
            row
            for row in defects
            if row["defect_type"]
            == "correctness_error"
        ]

        self.assertEqual(len(correctness), 2)
        self.assertTrue(
            all(
                row["owner_layer"] == "C"
                for row in correctness
            )
        )
        self.assertTrue(
            all(
                row["severity"] == "major"
                for row in correctness
            )
        )
        self.assertTrue(
            all(
                row["requirement_id"]
                for row in correctness
            )
        )
        self.assertEqual(
            merged["parsed"][
                "general_evidence_contract"
            ],
            merged[
                "general_evidence_contract"
            ],
        )

    def test_bridge_is_idempotent(self):
        evaluation = evaluate_control_valve_formula_check(
            answer_text=BAD_ANSWER,
            topic_id=TARGET_TOPIC_ID,
        )
        once = (
            merge_control_valve_findings_into_evidence(
                grade_with_contract(evaluation)
            )
        )
        twice = (
            merge_control_valve_findings_into_evidence(
                once
            )
        )

        self.assertEqual(
            once[
                "general_evidence_contract"
            ],
            twice[
                "general_evidence_contract"
            ],
        )

    def test_existing_layer_guard_blocks_c(self):
        evaluation = evaluate_control_valve_formula_check(
            answer_text=BAD_ANSWER,
            topic_id=TARGET_TOPIC_ID,
        )
        merged = (
            merge_control_valve_findings_into_evidence(
                grade_with_contract(evaluation)
            )
        )
        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                zero_layers(),
                baselines(),
                merged,
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertIn(
            "C",
            diagnostic["blocked_layers"],
        )
        self.assertEqual(
            by_id["C"]["score"],
            0.0,
        )
        self.assertGreater(
            by_id["A"]["score"],
            0.0,
        )

    def test_warning_only_finding_is_not_promoted(self):
        evaluation = {
            "applicable": True,
            "findings": [
                {
                    "id": (
                        "friction_direction_"
                        "reference_ambiguous"
                    ),
                    "severity": "warning",
                    "message": "방향 기준 불명확",
                    "evidence": "",
                    "correct_rule": "",
                }
            ],
        }
        merged = (
            merge_control_valve_findings_into_evidence(
                grade_with_contract(evaluation)
            )
        )
        defects = merged["parsed"][
            "general_evidence_contract"
        ]["defects"]

        self.assertFalse(
            any(
                row.get("defect_type")
                == "correctness_error"
                for row in defects
            )
        )
        self.assertNotIn(
            "control_valve_correctness_bridge",
            merged,
        )

    def test_runtime_hook_order_is_exact(self):
        source = Path(
            "grading_agents.py"
        ).read_text(encoding="utf-8")

        formula_position = source.index(
            "grade = attach_control_valve_formula_check("
        )
        bridge_position = source.index(
            "merge_control_valve_findings_into_evidence("
        )
        persistence_position = source.index(
            '"formula_check_evaluation.json"'
        )

        self.assertLess(
            formula_position,
            bridge_position,
        )
        self.assertLess(
            bridge_position,
            persistence_position,
        )


if __name__ == "__main__":
    unittest.main()
