from __future__ import annotations

import copy
import unittest

import grade_output_summarizer
from verdict_consistency import (
    VERDICT_CONSISTENCY_MARKER,
    reconcile_verdict_summary,
)


# VERDICT_RECOMMENDATION_CONSISTENCY_REGRESSION_V1


def payload(
    *,
    defects=None,
    requirements=None,
    demand_requirements=None,
    fatal=False,
):
    return {
        "score": {
            "total": 18.0,
            "max": 25.0,
        },
        "logic_check": {
            "fatal": fatal,
            "findings": (
                [
                    {
                        "severity": "fatal",
                        "message": "검증된 fatal",
                    }
                ]
                if fatal
                else []
            ),
        },
        "general_evidence_contract": {
            "schema_version": "1.0",
            "mode": "diagnostic_only",
            "score_effect": "none",
            "claims": [],
            "formulas": [],
            "defects": list(defects or []),
            "field_judgements": [],
            "summary": {},
        },
        "question_demand_contract": {
            "schema_version": "1.0",
            "requirements": list(
                demand_requirements or []
            ),
        },
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": list(
                    requirements or []
                ),
            },
        },
    }


class VerdictRecommendationConsistencyTests(
    unittest.TestCase
):
    def test_depth_only_removes_false_core_error_wording(self):
        summary = {
            "headline": "THEORY_CORE 핵심 이론 오류",
            "overall": "핵심 이론 오류가 확인되었습니다.",
            "key_reasons": ["세부 해석이 부족함"],
            "section_basis": [
                "fatal 오류를 보완하지 못합니다.",
            ],
            "improvements": [
                "일반적인 기술사 답안 형식을 보완",
            ],
        }
        result = reconcile_verdict_summary(
            summary,
            payload(
                defects=[
                    {
                        "defect_id": "depth_1",
                        "defect_type": "core_depth_gap",
                        "severity": "partial",
                        "owner_layer": "C",
                        "explanation": (
                            "최악 조건의 상세 해석이 부족하다."
                        ),
                    }
                ]
            ),
        )

        rendered = str(result)

        self.assertEqual(
            result["headline"],
            "핵심 내용은 성립하나 상세 해석 보완 필요",
        )
        self.assertNotIn("핵심 이론 오류", rendered)
        self.assertNotIn("fatal 오류", rendered)
        self.assertIn(
            "핵심 해석·설계 깊이",
            result["improvements"][0],
        )

    def test_presentation_issue_does_not_claim_technical_error(self):
        result = reconcile_verdict_summary(
            {
                "headline": "핵심 이론 오류",
                "overall": "명백한 기술 오류가 있다.",
                "improvements": ["기술 오류를 수정"],
            },
            payload(
                defects=[
                    {
                        "defect_id": "formula_1",
                        "defect_type": "presentation_issue",
                        "severity": "partial",
                        "owner_layer": "C",
                        "explanation": (
                            "수식의 항 연결 연산자가 보이지 않는다."
                        ),
                    }
                ]
            ),
        )

        rendered = str(result)

        self.assertEqual(
            result["headline"],
            "핵심 내용은 유지되며 수식·표현 확인 필요",
        )
        self.assertNotIn("명백한 기술 오류", rendered)
        self.assertIn(
            "수식·표현 무결성",
            result["improvements"][0],
        )

    def test_verified_major_correctness_uses_hard_wording(self):
        result = reconcile_verdict_summary(
            {
                "headline": "상세 해석 보완 필요",
                "overall": "기본 내용은 적절하다.",
                "improvements": [],
            },
            payload(
                defects=[
                    {
                        "defect_id": "error_1",
                        "defect_type": "correctness_error",
                        "severity": "major",
                        "owner_layer": "C",
                        "explanation": "안정성 부호가 반대다.",
                    }
                ]
            ),
        )

        self.assertEqual(
            result["headline"],
            "검증된 핵심 기술 오류 보완 필요",
        )
        self.assertIn(
            "중대 기술 오류",
            result["overall"],
        )
        self.assertTrue(
            result["verdict_consistency"][
                "hard_error_wording_allowed"
            ]
        )

    def test_fulfilled_requirement_is_not_recommended(self):
        result = reconcile_verdict_summary(
            {
                "headline": "채점 결과",
                "overall": "요약",
                "improvements": [
                    "정의와 설계를 모두 다시 작성",
                ],
            },
            payload(
                requirements=[
                    {
                        "requirement_id": "r_define",
                        "status": "present",
                        "is_core": True,
                    },
                    {
                        "requirement_id": "r_design",
                        "status": "missing",
                        "is_core": True,
                    },
                ],
                demand_requirements=[
                    {
                        "requirement_id": "r_define",
                        "demand_label": "정의·개념 설명",
                    },
                    {
                        "requirement_id": "r_design",
                        "demand_label": "설계·설계 기준",
                    },
                ],
            ),
        )

        improvements = " ".join(
            result["improvements"]
        )

        self.assertNotIn("정의·개념 설명", improvements)
        self.assertIn("설계·설계 기준", improvements)
        self.assertNotIn(
            "정의와 설계를 모두 다시 작성",
            improvements,
        )

    def test_verified_logic_fatal_is_preserved(self):
        original = {
            "headline": "THEORY_CORE 핵심 이론 오류",
            "overall": "핵심 이론 오류가 확인되었습니다.",
            "improvements": ["fatal 오류 수정"],
        }
        result = reconcile_verdict_summary(
            original,
            payload(fatal=True),
        )

        self.assertEqual(
            result["headline"],
            original["headline"],
        )
        self.assertEqual(
            result["overall"],
            original["overall"],
        )
        self.assertEqual(
            result["verdict_consistency"]["mode"],
            "preserve_verified_logic_fatal",
        )

    def test_reconciliation_is_score_neutral(self):
        source_payload = payload(
            defects=[
                {
                    "defect_type": "core_depth_gap",
                    "severity": "partial",
                    "owner_layer": "D",
                    "explanation": "검증 조건 부족",
                }
            ]
        )
        source_payload["total_score"] = 18.0
        source_payload["layer_scores"] = [
            {"layer_id": "D", "score": 4.5},
        ]
        before = copy.deepcopy(source_payload)

        reconcile_verdict_summary(
            {
                "headline": "요약",
                "overall": "요약",
                "improvements": [],
            },
            source_payload,
        )

        self.assertEqual(source_payload, before)

    def test_build_payload_exposes_structured_contracts(self):
        grade = {
            "score": 18.0,
            "max_score": 25.0,
            "parsed": {
                "general_evidence_contract": {
                    "mode": "diagnostic_only",
                    "defects": [],
                },
                "question_demand_contract": {
                    "mode": "question_only_deterministic",
                    "requirements": [],
                },
                "question_type_coverage": {
                    "overall_coverage": "adequate",
                },
            },
        }

        built = grade_output_summarizer._build_payload(
            grade
        )

        self.assertIn(
            "general_evidence_contract",
            built,
        )
        self.assertIn(
            "question_demand_contract",
            built,
        )
        self.assertIn(
            "question_type_coverage",
            built,
        )

    def test_effective_normaliser_uses_structured_policy(self):
        source_payload = payload(
            defects=[
                {
                    "defect_type": "presentation_issue",
                    "severity": "warning",
                    "owner_layer": "C",
                    "explanation": "변수 정의가 불명확하다.",
                }
            ]
        )

        result = grade_output_summarizer._normalise_summary(
            {
                "headline": "핵심 이론 오류",
                "overall": "명백한 오류가 있다.",
                "key_reasons": [],
                "section_basis": [],
                "improvements": [
                    "일반적인 내용을 보완",
                ],
            },
            source_payload,
        )

        self.assertEqual(
            result["headline"],
            "핵심 내용은 유지되며 수식·표현 확인 필요",
        )
        self.assertEqual(
            result["verdict_consistency"]["marker"],
            VERDICT_CONSISTENCY_MARKER,
        )


if __name__ == "__main__":
    unittest.main()
