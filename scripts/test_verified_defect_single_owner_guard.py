from __future__ import annotations

import copy
import unittest

import grading_agents


# VERIFIED_DEFECT_SINGLE_OWNER_GUARD_REGRESSION_V1


def layers():
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


def coverage_row(
    requirement_id,
    *,
    status="incorrect",
    previous="present",
    defect_id="defect_c_1",
):
    row = {
        "requirement_id": requirement_id,
        "requirement": requirement_id,
        "status": status,
        "is_core": True,
        "evidence": "검증 근거",
    }

    if previous is not None:
        row[
            "status_before_verified_defect"
        ] = previous

    if defect_id is not None:
        row["verified_defect_ids"] = [
            defect_id
        ]

    return row


def payload(
    *,
    owner="C",
    defect_type="correctness_error",
    severity="major",
    status="incorrect",
    previous="present",
    include_reconciliation=True,
    defect_id="defect_c_1",
):
    coverage = {
        "question_type": (
            "PRINCIPLE_INTERPRETATION"
        ),
        "overall_coverage": "weak",
        "explicit_requirement_coverage": {
            "requirements": [
                coverage_row(
                    "requirement_1",
                    status=status,
                    previous=previous,
                    defect_id=defect_id,
                )
            ]
        },
    }
    contract = {
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
                "defect_id": defect_id,
                "defect_type": defect_type,
                "severity": severity,
                "owner_layer": owner,
                "requirement_id": (
                    "requirement_1"
                ),
                "evidence_text": "오류",
                "explanation": "검증 오류",
            }
        ],
        "field_judgements": [],
        "summary": {},
    }
    result = {
        "question_type_coverage": copy.deepcopy(
            coverage
        ),
        "general_evidence_contract": copy.deepcopy(
            contract
        ),
        "parsed": {
            "question_type_coverage": copy.deepcopy(
                coverage
            ),
            "general_evidence_contract": copy.deepcopy(
                contract
            ),
        },
    }

    if include_reconciliation:
        result[
            "verified_defect_reconciliation"
        ] = {
            "marker": (
                "VERIFIED_DEFECT_RECONCILIATION_V1"
            ),
            "score_effect": "none",
            "primary_score_owner": "C",
            "b_completeness_double_deduction": False,
        }

    return result


def run_guard(value):
    return (
        grading_agents
        ._phase6_apply_semantic_downward_guard(
            layers(),
            baselines(),
            value,
            scoring_model(),
        )
    )


class VerifiedDefectSingleOwnerGuardTests(
    unittest.TestCase
):
    def test_c_owned_verified_error_blocks_only_c(self):
        original = payload()
        before = copy.deepcopy(original)
        guarded, diagnostic = run_guard(
            original
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(original, before)
        self.assertEqual(
            set(
                diagnostic["blocked_layers"]
            ),
            {"C"},
        )
        self.assertGreater(
            by_id["B"]["score"],
            0.0,
        )
        self.assertEqual(
            by_id["C"]["score"],
            0.0,
        )
        self.assertGreater(
            by_id["D"]["score"],
            0.0,
        )
        marker = diagnostic[
            "verified_defect_single_owner_guard"
        ]
        self.assertEqual(
            marker["primary_score_owner"],
            "C",
        )
        self.assertEqual(
            marker[
                "suppressed_duplicate_layers"
            ],
            ["B", "D"],
        )

    def test_display_coverage_remains_incorrect(self):
        original = payload()
        _guarded, _diagnostic = run_guard(
            original
        )
        direct = original[
            "question_type_coverage"
        ]["explicit_requirement_coverage"][
            "requirements"
        ][0]
        parsed = original["parsed"][
            "question_type_coverage"
        ]["explicit_requirement_coverage"][
            "requirements"
        ][0]

        self.assertEqual(
            direct["status"],
            "incorrect",
        )
        self.assertEqual(
            parsed["status"],
            "incorrect",
        )

    def test_raw_semantic_incorrect_still_blocks_b(self):
        value = payload(
            include_reconciliation=False,
            previous=None,
            defect_id="raw_error",
        )
        guarded, diagnostic = run_guard(
            value
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertIn(
            "B",
            diagnostic["blocked_layers"],
        )
        self.assertEqual(
            by_id["B"]["score"],
            0.0,
        )
        self.assertNotIn(
            "verified_defect_single_owner_guard",
            diagnostic,
        )

    def test_missing_core_requirement_is_not_suppressed(self):
        value = payload(
            status="missing",
            previous=None,
            defect_id="missing_case",
        )
        before = copy.deepcopy(value)
        guarded, diagnostic = run_guard(
            value
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(value, before)
        self.assertIn(
            "B",
            diagnostic["blocked_layers"],
        )
        self.assertEqual(
            by_id["B"]["score"],
            0.0,
        )
        self.assertNotIn(
            "verified_defect_single_owner_guard",
            diagnostic,
        )
        self.assertEqual(
            value["parsed"][
                "question_type_coverage"
            ]["explicit_requirement_coverage"][
                "requirements"
            ][0]["status"],
            "missing",
        )

    def test_non_c_owner_is_not_suppressed(self):
        value = payload(
            owner="D",
        )
        guarded, diagnostic = run_guard(
            value
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertIn(
            "B",
            diagnostic["blocked_layers"],
        )
        self.assertIn(
            "D",
            diagnostic["blocked_layers"],
        )
        self.assertEqual(
            by_id["B"]["score"],
            0.0,
        )
        self.assertEqual(
            by_id["D"]["score"],
            0.0,
        )
        self.assertNotIn(
            "verified_defect_single_owner_guard",
            diagnostic,
        )

    def test_partial_original_status_remains_partial_for_guard(self):
        value = payload(
            previous="partial",
        )
        guarded, diagnostic = run_guard(
            value
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertNotIn(
            "B",
            diagnostic["blocked_layers"],
        )
        self.assertNotIn(
            "D",
            diagnostic["blocked_layers"],
        )
        self.assertGreater(
            by_id["B"]["score"],
            0.0,
        )
        self.assertGreater(
            by_id["D"]["score"],
            0.0,
        )

    def test_unknown_defect_id_is_not_suppressed(self):
        value = payload()
        for location in (
            value["question_type_coverage"],
            value["parsed"][
                "question_type_coverage"
            ],
        ):
            location[
                "explicit_requirement_coverage"
            ]["requirements"][0][
                "verified_defect_ids"
            ] = ["unknown_defect"]

        guarded, diagnostic = run_guard(
            value
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertIn(
            "B",
            diagnostic["blocked_layers"],
        )
        self.assertEqual(
            by_id["B"]["score"],
            0.0,
        )
        self.assertNotIn(
            "verified_defect_single_owner_guard",
            diagnostic,
        )


if __name__ == "__main__":
    unittest.main()
