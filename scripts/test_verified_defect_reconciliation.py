from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import grade_output_summarizer
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
from verified_defect_reconciliation import (
    reconcile_verified_defects_with_coverage,
)


# VERIFIED_DEFECT_RECONCILIATION_REGRESSION_V1

QUESTION = (
    "공압식 밸브 선정시 밸브의 불평형력, "
    "마찰력 개념 설명. "
    "Fail safe 동작 구현을 위한 "
    "Spring 설계 기준 제시"
)

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

GOOD_ANSWER = '''
밸브 마찰은 패킹, 가이드, Breakaway,
Stiction과 운동마찰을 구분한다.
단순히 속도에 비례하지 않는다.
Fs(x)=F0+k*x이며 전 스트로크에서
저항 방향의 불평형력, 최대 마찰력,
시트 하중과 마진을 극복해야 한다.
'''


def contract():
    return build_question_demand_contract(
        QUESTION
    )


def coverage_rows():
    return [
        {
            "category": "definition_or_concept",
            "requirement": (
                "불평형력과 마찰력 개념 설명"
            ),
            "status": "present",
            "evidence": "개념을 설명함",
            "is_core": True,
        },
        {
            "category": (
                "calculation_or_interpretation"
            ),
            "requirement": (
                "Fail Safe Spring 설계 기준"
            ),
            "status": "present",
            "evidence": "힘 평형식을 제시함",
            "is_core": True,
        },
        {
            "category": "field_application",
            "requirement": "현장 적용",
            "status": "present",
            "evidence": "CBM 제시",
            "is_core": False,
        },
    ]


def grade_for_answer(answer_text):
    evaluation = evaluate_control_valve_formula_check(
        answer_text=answer_text,
        topic_id=TARGET_TOPIC_ID,
    )
    demand_contract = contract()
    grade = {
        "score": 16.33,
        "total_score": 16.33,
        "max_score": 25.0,
        "topic_id": TARGET_TOPIC_ID,
        "question_demand_contract": copy.deepcopy(
            demand_contract
        ),
        "formula_check_evaluation": copy.deepcopy(
            evaluation
        ),
        "parsed": {
            "question_demand_contract": copy.deepcopy(
                demand_contract
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
                "defects": [],
                "field_judgements": [],
                "summary": {},
            },
            "question_type_coverage": {
                "question_type": (
                    "PRINCIPLE_INTERPRETATION"
                ),
                "overall_coverage": "strong",
                "scoring_hint": "",
                "explicit_requirement_coverage": {
                    "source": "question_text",
                    "extraction_confidence": "high",
                    "requirements": coverage_rows(),
                },
            },
        },
    }
    return merge_control_valve_findings_into_evidence(
        grade
    )


class VerifiedDefectReconciliationTests(
    unittest.TestCase
):
    def test_two_verified_errors_mark_two_requirements_incorrect(self):
        grade = grade_for_answer(BAD_ANSWER)
        before = copy.deepcopy(grade)
        reconciled = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )

        self.assertEqual(grade, before)
        self.assertEqual(
            reconciled["score"],
            before["score"],
        )
        self.assertEqual(
            reconciled["total_score"],
            before["total_score"],
        )

        coverage = reconciled["parsed"][
            "question_type_coverage"
        ]
        rows = coverage[
            "explicit_requirement_coverage"
        ]["requirements"]
        statuses = [
            row["status"]
            for row in rows
        ]

        self.assertEqual(
            statuses.count("incorrect"),
            2,
        )
        self.assertEqual(
            coverage["overall_coverage"],
            "weak",
        )
        self.assertEqual(
            coverage["coverage_counts"][
                "incorrect"
            ],
            2,
        )
        self.assertTrue(
            all(
                row.get(
                    "status_before_verified_defect"
                )
                == "present"
                for row in rows[:2]
            )
        )
        self.assertTrue(
            all(
                row.get("verified_defect_ids")
                for row in rows[:2]
            )
        )

    def test_one_verified_error_caps_strong_at_adequate(self):
        grade = grade_for_answer(BAD_ANSWER)
        defects = grade[
            "general_evidence_contract"
        ]["defects"]
        grade[
            "general_evidence_contract"
        ]["defects"] = defects[:1]
        grade["parsed"][
            "general_evidence_contract"
        ]["defects"] = copy.deepcopy(
            defects[:1]
        )

        reconciled = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )
        coverage = reconciled["parsed"][
            "question_type_coverage"
        ]

        self.assertEqual(
            coverage["overall_coverage"],
            "adequate",
        )
        self.assertEqual(
            coverage["coverage_counts"][
                "incorrect"
            ],
            1,
        )

    def test_good_answer_keeps_coverage_unchanged(self):
        grade = grade_for_answer(GOOD_ANSWER)
        before = copy.deepcopy(grade)
        reconciled = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )

        self.assertEqual(
            reconciled,
            before,
        )

    def test_reconciliation_is_idempotent(self):
        once = (
            reconcile_verified_defects_with_coverage(
                grade_for_answer(BAD_ANSWER)
            )
        )
        twice = (
            reconcile_verified_defects_with_coverage(
                once
            )
        )

        self.assertEqual(
            once,
            twice,
        )

    def test_verified_error_uses_existing_hard_verdict_policy(self):
        reconciled = (
            reconcile_verified_defects_with_coverage(
                grade_for_answer(BAD_ANSWER)
            )
        )
        payload = (
            grade_output_summarizer._build_payload(
                reconciled
            )
        )
        summary = (
            grade_output_summarizer._normalise_summary(
                {
                    "headline": "핵심 이론은 정확",
                    "overall": (
                        "핵심 이론은 정확하나 "
                        "상세 해석 보완 필요"
                    ),
                    "key_reasons": [],
                    "section_basis": [],
                    "improvements": [
                        "일반적인 내용을 보완"
                    ],
                },
                payload,
            )
        )
        rendered = json.dumps(
            summary,
            ensure_ascii=False,
            sort_keys=True,
        )

        self.assertNotIn(
            "핵심 이론은 정확",
            rendered,
        )
        self.assertIn("기술", rendered)
        self.assertIn("오류", rendered)

    def test_b_completeness_score_is_not_directly_changed(self):
        grade = grade_for_answer(BAD_ANSWER)
        grade["layer_scores"] = [
            {
                "layer_id": "B",
                "score": 5.5,
                "max_score": 6.0,
            },
            {
                "layer_id": "C",
                "score": 5.0,
                "max_score": 8.0,
            },
        ]
        before = copy.deepcopy(
            grade["layer_scores"]
        )
        reconciled = (
            reconcile_verified_defects_with_coverage(
                grade
            )
        )

        self.assertEqual(
            reconciled["layer_scores"],
            before,
        )
        metadata = reconciled[
            "verified_defect_reconciliation"
        ]
        self.assertEqual(
            metadata["primary_score_owner"],
            "C",
        )
        self.assertFalse(
            metadata[
                "b_completeness_double_deduction"
            ]
        )

    def test_runtime_hook_order_is_exact(self):
        source = Path(
            "grading_agents.py"
        ).read_text(encoding="utf-8")

        bridge_position = source.index(
            "merge_control_valve_findings_into_evidence("
        )
        reconcile_position = source.index(
            "reconcile_verified_defects_with_coverage("
        )
        persistence_position = source.index(
            '"formula_check_evaluation.json"'
        )

        self.assertLess(
            bridge_position,
            reconcile_position,
        )
        self.assertLess(
            reconcile_position,
            persistence_position,
        )


if __name__ == "__main__":
    unittest.main()
