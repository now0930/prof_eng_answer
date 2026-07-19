from __future__ import annotations

import copy
import unittest

import bot
from control_valve_correctness_bridge import (
    merge_control_valve_findings_into_evidence,
)
from control_valve_formula_checker import (
    TARGET_TOPIC_ID,
    attach_control_valve_formula_check,
    evaluate_control_valve_formula_check,
)
from verified_defect_reconciliation import (
    reconcile_verified_defects_with_coverage,
)


GOOD_NEGATED_ANSWER = """
밸브 마찰력은 단순히 속도에 비례하는 힘이 아니다.
정지 상태의 Breakaway Force와 Stiction을 포함하고
평균 마찰력이 아니라 최대 저항력을 적용한다.
"""

BAD_ANSWER = """
마찰력은 구동 속도에 비례하여 역방향으로 발생합니다.
Fb = C * v
Fa + Fs - Fb + F1 - F2 = 0
Fa + Fs = Fb - F1 + F2
공기원 차단 시 Fa=0이므로
Fs = Fb - F1 + F2
스프링 복원력 Fs는 최대 불평형력
(F1 - F2)과 마찰력 Fb의 합산 요구량보다
항상 크도록 설계해야 합니다.
"""


def finding_ids(answer):
    result = evaluate_control_valve_formula_check(
        answer_text=answer,
        topic_id=TARGET_TOPIC_ID,
    )
    return {
        str(row.get("id") or "")
        for row in result.get("findings") or []
        if isinstance(row, dict)
    }, result


def coverage():
    return {
        "question_type": (
            "PRINCIPLE_INTERPRETATION"
        ),
        "overall_coverage": "strong",
        "explicit_requirement_coverage": {
            "source": "question_text",
            "extraction_confidence": "high",
            "requirements": [
                {
                    "requirement": (
                        "불평형력 개념 설명"
                    ),
                    "status": "present",
                    "evidence": "설명 존재",
                    "is_core": True,
                },
                {
                    "requirement": (
                        "마찰력 개념 설명"
                    ),
                    "status": "present",
                    "evidence": "설명 존재",
                    "is_core": True,
                },
                {
                    "requirement": (
                        "Fail Safe 스프링 설계 기준"
                    ),
                    "status": "present",
                    "evidence": "설계 기준 존재",
                    "is_core": True,
                },
            ],
        },
    }


def empty_contract():
    return {
        "schema_version": "1.0",
        "contract_marker": (
            "GENERAL_EVIDENCE_CONTRACT_V1"
        ),
        "mode": "diagnostic_only",
        "score_effect": "none",
        "claims": [],
        "formulas": [],
        "defects": [],
        "field_judgements": [],
        "summary": {},
    }


def live_shaped_grade():
    root_coverage = coverage()
    contract = empty_contract()
    return {
        "score": 20.0,
        "total_score": 20.0,
        "max_score": 25.0,
        "topic_id": TARGET_TOPIC_ID,
        "question_type_coverage": copy.deepcopy(
            root_coverage
        ),
        "general_evidence_contract": copy.deepcopy(
            contract
        ),
        "parsed": {
            "general_evidence_contract": (
                copy.deepcopy(contract)
            ),
        },
    }


class PostReleaseControlValveLiveTests(
    unittest.TestCase
):
    def test_copula_negation_is_not_major(self):
        ids, result = finding_ids(
            "밸브 마찰력은 단순히 속도에 "
            "비례하는 힘이 아니다."
        )

        self.assertNotIn(
            "friction_viscous_model_overgeneralized",
            ids,
        )
        self.assertFalse(
            result["major_error_detected"]
        )
        self.assertEqual(
            result["negation_filter"]["marker"],
            "CONTROL_VALVE_NEGATION_FILTER_V3",
        )

    def test_negated_context_is_not_major(self):
        ids, _result = finding_ids(
            GOOD_NEGATED_ANSWER
        )
        self.assertNotIn(
            "friction_viscous_model_overgeneralized",
            ids,
        )

    def test_positive_proportional_claim_stays_major(self):
        ids, result = finding_ids(
            "밸브 마찰력은 구동 속도에 비례한다."
        )
        self.assertIn(
            "friction_viscous_model_overgeneralized",
            ids,
        )
        self.assertTrue(
            result["major_error_detected"]
        )

    def test_explicit_viscous_formula_stays_major(self):
        ids, result = finding_ids(
            "Fb = C * v"
        )
        self.assertIn(
            "friction_viscous_model_overgeneralized",
            ids,
        )
        self.assertTrue(
            result["major_error_detected"]
        )

    def test_good_live_shape_has_no_correctness_defect(self):
        grade = live_shaped_grade()
        grade = attach_control_valve_formula_check(
            grade,
            GOOD_NEGATED_ANSWER,
        )
        grade = (
            merge_control_valve_findings_into_evidence(
                grade
            )
        )
        grade = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )

        defects = grade[
            "general_evidence_contract"
        ]["defects"]
        statuses = [
            row["status"]
            for row in grade[
                "question_type_coverage"
            ]["explicit_requirement_coverage"][
                "requirements"
            ]
        ]

        self.assertEqual(defects, [])
        self.assertEqual(
            statuses,
            ["present", "present", "present"],
        )
        self.assertEqual(
            grade["question_type_coverage"][
                "overall_coverage"
            ],
            "strong",
        )

    def test_bad_live_shape_maps_empty_ids_to_two_rows(self):
        grade = live_shaped_grade()
        before_scores = (
            grade["score"],
            grade["total_score"],
        )
        grade = attach_control_valve_formula_check(
            grade,
            BAD_ANSWER,
        )
        grade = (
            merge_control_valve_findings_into_evidence(
                grade
            )
        )

        defects_before = grade[
            "general_evidence_contract"
        ]["defects"]
        self.assertEqual(
            len(defects_before),
            2,
        )
        self.assertTrue(
            all(
                not str(
                    row.get("requirement_id")
                    or ""
                )
                for row in defects_before
            )
        )

        grade = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )
        rows = grade[
            "question_type_coverage"
        ]["explicit_requirement_coverage"][
            "requirements"
        ]
        statuses = [
            row["status"]
            for row in rows
        ]

        self.assertEqual(
            statuses,
            ["present", "incorrect", "incorrect"],
        )
        self.assertIn(
            "friction_viscous_model_overgeneralized",
            rows[1][
                "verified_source_finding_ids"
            ],
        )
        self.assertIn(
            "force_balance_requirement_sign_contradiction",
            rows[2][
                "verified_source_finding_ids"
            ],
        )
        self.assertEqual(
            grade["question_type_coverage"][
                "coverage_counts"
            ]["incorrect"],
            2,
        )
        self.assertEqual(
            grade["question_type_coverage"][
                "overall_coverage"
            ],
            "weak",
        )
        self.assertEqual(
            grade["parsed"][
                "question_type_coverage"
            ],
            grade["question_type_coverage"],
        )
        self.assertEqual(
            (
                grade["score"],
                grade["total_score"],
            ),
            before_scores,
        )
        self.assertEqual(
            grade[
                "verified_defect_reconciliation"
            ]["unresolved_defect_ids"],
            [],
        )

        summary = grade[
            "question_type_coverage_summary"
        ]
        self.assertEqual(
            summary["sub_criteria_total"],
            3,
        )
        self.assertEqual(
            summary["sub_criteria_present"],
            1,
        )
        self.assertEqual(
            summary["sub_criteria_incorrect"],
            2,
        )
        self.assertEqual(
            summary["overall_coverage"],
            "weak",
        )
        self.assertEqual(
            summary["weighted_coverage_score"],
            1.0,
        )
        self.assertEqual(
            summary["weighted_coverage_percent"],
            33.3,
        )
        self.assertEqual(
            summary["incorrect_criteria"],
            [
                "마찰력 개념 설명",
                "Fail Safe 스프링 설계 기준",
            ],
        )
        self.assertEqual(
            summary[
                "verified_defect_display_sync"
            ]["marker"],
            "VERIFIED_DEFECT_DISPLAY_SUMMARY_SYNC_V4",
        )

        rendered = bot.format_result(grade)
        self.assertIn(
            "전체 판정: weak",
            rendered,
        )
        self.assertIn(
            "오답 2",
            rendered,
        )

    def test_unknown_empty_id_defect_remains_unresolved(self):
        grade = live_shaped_grade()
        defect = {
            "defect_id": "unknown_1",
            "defect_type": "correctness_error",
            "severity": "major",
            "owner_layer": "C",
            "requirement_id": "",
            "source": "control_valve_formula_check",
            "source_finding_id": "unknown_finding",
            "evidence_text": "unknown",
            "explanation": "unknown",
        }
        grade["general_evidence_contract"][
            "defects"
        ] = [copy.deepcopy(defect)]
        grade["parsed"][
            "general_evidence_contract"
        ]["defects"] = [copy.deepcopy(defect)]

        result = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )

        self.assertNotIn(
            "verified_defect_reconciliation",
            result,
        )
        statuses = [
            row["status"]
            for row in result[
                "question_type_coverage"
            ]["explicit_requirement_coverage"][
                "requirements"
            ]
        ]
        self.assertEqual(
            statuses,
            ["present", "present", "present"],
        )


if __name__ == "__main__":
    unittest.main()
