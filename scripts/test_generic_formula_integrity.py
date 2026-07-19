from __future__ import annotations

import copy
import unittest

from general_evidence_contract import (
    attach_general_evidence_contract,
)
from generic_formula_integrity import (
    GENERIC_FORMULA_INTEGRITY_MARKER,
    analyze_formula_text,
    apply_formula_integrity_to_contract,
)


# GENERIC_FORMULA_INTEGRITY_REGRESSION_V1


class GenericFormulaIntegrityTests(unittest.TestCase):
    def test_complete_single_line_formula_is_valid(self):
        result = analyze_formula_text("F = P * A")

        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["issues"], [])

    def test_two_line_missing_operator_is_warning(self):
        result = analyze_formula_text("Y = K\nX")

        self.assertEqual(result["status"], "warning")
        self.assertTrue(
            any(
                issue["code"] == "missing_term_operator"
                for issue in result["issues"]
            )
        )

    def test_two_line_explicit_continuation_is_valid(self):
        result = analyze_formula_text("Y =\nK * X")

        self.assertEqual(result["status"], "valid")

    def test_unbalanced_delimiter_is_invalid(self):
        result = analyze_formula_text("F = (P * A")

        self.assertEqual(result["status"], "invalid")
        self.assertTrue(
            any(
                issue["code"] == "unbalanced_delimiter"
                for issue in result["issues"]
            )
        )

    def test_broken_multiline_rhs_is_warning(self):
        result = analyze_formula_text(
            "\n".join(
                [
                    "P_air,min * A_a * eta",
                    "= F_s(x)",
                    "F_u,opp(x)",
                    "F_f,max(x)",
                    "F_seat(x)",
                    "F_margin",
                ]
            )
        )

        self.assertEqual(result["status"], "warning")
        self.assertTrue(
            any(
                issue["code"] == "missing_term_operator"
                for issue in result["issues"]
            )
        )

    def test_explicit_multiline_operators_are_valid(self):
        result = analyze_formula_text(
            "\n".join(
                [
                    "P_air,min * A_a * eta",
                    ">= F_s(x)",
                    "+ F_u,opp(x)",
                    "+ F_f,max(x)",
                    "+ F_margin",
                ]
            )
        )

        self.assertEqual(result["status"], "valid")

    def test_formula_warning_creates_presentation_issue_only(self):
        contract = {
            "mode": "diagnostic_only",
            "score_effect": "none",
            "claims": [],
            "formulas": [
                {
                    "formula_id": "f1",
                    "requirement_id": "r1",
                    "formula_text": (
                        "Output = Term1\n"
                        "Term2\n"
                        "Term3"
                    ),
                    "integrity_status": "not_evaluated",
                    "integrity_notes": [],
                    "owner_layer": "C",
                }
            ],
            "defects": [],
            "summary": {},
        }

        updated = apply_formula_integrity_to_contract(contract)

        self.assertEqual(
            updated["formulas"][0]["integrity_status"],
            "warning",
        )
        self.assertTrue(updated["defects"])
        self.assertTrue(
            all(
                defect["defect_type"] == "presentation_issue"
                for defect in updated["defects"]
            )
        )
        self.assertTrue(
            all(
                defect["diagnostic_only"]
                for defect in updated["defects"]
            )
        )
        self.assertEqual(
            updated["formula_integrity"]["marker"],
            GENERIC_FORMULA_INTEGRITY_MARKER,
        )

    def test_attachment_preserves_score_fields(self):
        grade = {
            "score": 20.0,
            "total_score": 20.0,
            "layer_scores": [
                {"layer_id": "C", "score": 6.5},
            ],
            "parsed": {
                "general_evidence_contract": {
                    "mode": "diagnostic_only",
                    "score_effect": "none",
                    "claims": [],
                    "formulas": [
                        {
                            "formula_id": "f1",
                            "formula_text": (
                                "Output = Term1\n"
                                "Term2"
                            ),
                            "integrity_status": "not_evaluated",
                            "integrity_notes": [],
                            "owner_layer": "C",
                        }
                    ],
                    "defects": [],
                    "summary": {},
                }
            },
        }
        before = copy.deepcopy(grade)

        attached = attach_general_evidence_contract(grade)

        self.assertEqual(grade, before)
        self.assertEqual(attached["score"], before["score"])
        self.assertEqual(
            attached["total_score"],
            before["total_score"],
        )
        self.assertEqual(
            attached["layer_scores"],
            before["layer_scores"],
        )
        self.assertEqual(
            attached["general_evidence_contract"],
            attached["parsed"]["general_evidence_contract"],
        )

    def test_contract_application_is_idempotent(self):
        contract = {
            "mode": "diagnostic_only",
            "score_effect": "none",
            "claims": [],
            "formulas": [
                {
                    "formula_id": "f1",
                    "formula_text": "Output = Term1\nTerm2",
                    "integrity_status": "not_evaluated",
                    "integrity_notes": [],
                    "owner_layer": "C",
                }
            ],
            "defects": [],
            "summary": {},
        }

        once = apply_formula_integrity_to_contract(contract)
        twice = apply_formula_integrity_to_contract(once)

        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
