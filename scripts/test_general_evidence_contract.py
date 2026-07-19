from __future__ import annotations

import copy
import unittest

import gemini_grader
from general_evidence_contract import (
    GENERAL_EVIDENCE_CONTRACT_MARKER,
    attach_general_evidence_contract,
    empty_general_evidence_contract,
    normalize_general_evidence_contract,
)


# GENERAL_EVIDENCE_CONTRACT_REGRESSION_V1


class GeneralEvidenceContractTests(unittest.TestCase):
    def test_empty_contract_is_diagnostic_only(self):
        contract = empty_general_evidence_contract()

        self.assertEqual(contract["mode"], "diagnostic_only")
        self.assertEqual(contract["score_effect"], "none")
        self.assertEqual(contract["summary"]["defect_count"], 0)

    def test_defect_aliases_are_normalized(self):
        contract = normalize_general_evidence_contract(
            {
                "defects": [
                    {
                        "issue_type": "depth_gap",
                        "severity": "major",
                        "primary_owner_layer": "D",
                        "reason": "핵심 설계 조건이 부족하다.",
                    },
                    {
                        "issue_type": "formula_integrity_warning",
                        "severity": "warning",
                        "primary_owner_layer": "C",
                        "reason": "연산자 누락 가능성이 있다.",
                    },
                ]
            }
        )

        first, second = contract["defects"]

        self.assertEqual(first["defect_type"], "core_depth_gap")
        self.assertEqual(first["severity"], "partial")
        self.assertEqual(first["owner_layer"], "D")
        self.assertEqual(second["defect_type"], "presentation_issue")
        self.assertTrue(first["diagnostic_only"])
        self.assertTrue(second["diagnostic_only"])

    def test_presentation_issue_is_not_correctness_error(self):
        contract = normalize_general_evidence_contract(
            {
                "defects": [
                    {
                        "defect_type": "operator_missing",
                        "severity": "major",
                        "explanation": "우변 항 사이 연산자가 보이지 않는다.",
                    }
                ]
            }
        )

        defect = contract["defects"][0]

        self.assertEqual(defect["defect_type"], "presentation_issue")
        self.assertEqual(defect["severity"], "partial")
        self.assertNotEqual(defect["defect_type"], "correctness_error")

    def test_claim_formula_and_defect_are_normalized(self):
        contract = normalize_general_evidence_contract(
            {
                "claims": [
                    {
                        "id": "claim-1",
                        "claim": "최소 공급압력에서 구동력을 확인한다.",
                        "evidence": "P_air,min 조건을 제시했다.",
                        "type": "field_judgement",
                        "status": "present",
                        "owner_layer": "D",
                    }
                ],
                "formulas": [
                    {
                        "id": "formula-1",
                        "formula": "F = P * A",
                        "variables": {
                            "F": "force",
                            "P": "pressure",
                            "A": "area",
                        },
                        "status": "not_evaluated",
                    }
                ],
                "defects": [
                    {
                        "id": "defect-1",
                        "type": "advanced_missing",
                        "description": "정량 예시가 없다.",
                    }
                ],
            }
        )

        self.assertEqual(contract["claims"][0]["status"], "supported")
        self.assertEqual(
            contract["claims"][0]["evidence_type"],
            "field_judgement",
        )
        self.assertEqual(len(contract["formulas"][0]["variables"]), 3)
        self.assertEqual(
            contract["defects"][0]["defect_type"],
            "advanced_detail_missing",
        )

    def test_attach_preserves_score_bearing_fields(self):
        original = {
            "score": 17.46,
            "total_score": 17.46,
            "layer_scores": {
                "A": {"score": 2.5, "max_score": 3.0},
                "B": {"score": 5.0, "max_score": 6.0},
            },
            "parsed": {
                "general_evidence_contract": {
                    "defects": [
                        {
                            "defect_type": "correctness_error",
                            "severity": "partial",
                            "explanation": "부호가 반대다.",
                        }
                    ]
                }
            },
        }
        before = copy.deepcopy(original)

        attached = attach_general_evidence_contract(original)

        self.assertEqual(original, before)
        self.assertEqual(attached["score"], before["score"])
        self.assertEqual(attached["total_score"], before["total_score"])
        self.assertEqual(attached["layer_scores"], before["layer_scores"])
        self.assertEqual(
            attached["general_evidence_contract"],
            attached["parsed"]["general_evidence_contract"],
        )

    def test_final_prompt_contains_general_contract(self):
        prompt = gemini_grader.build_gemini_grading_prompt(
            question_text="문제",
            answer_text="답안",
            scoring_model={},
            subject_rubric={},
            rater_profile={},
            volume={},
            fact_eval={},
            connection_eval={},
        )

        self.assertIn(GENERAL_EVIDENCE_CONTRACT_MARKER, prompt)
        self.assertIn('"general_evidence_contract"', prompt)
        self.assertIn("presentation_issue", prompt)
        self.assertIn("core_depth_gap", prompt)
        self.assertIn(
            "점수·상한·하드캡을 직접 변경하지 않는다",
            prompt,
        )


if __name__ == "__main__":
    unittest.main()
