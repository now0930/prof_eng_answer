from __future__ import annotations

import copy
import unittest

import grading_agents
from layer_evidence_guard import (
    LAYER_EVIDENCE_GUARD_MARKER,
    build_layer_evidence_policy,
)


# LAYER_SPECIFIC_EVIDENCE_GUARD_REGRESSION_V1


def scoring_model():
    return {
        "layers": [
            {"id": "A", "points": 3},
            {"id": "B", "points": 6},
            {"id": "C", "points": 8},
            {"id": "D", "points": 6},
            {"id": "E", "points": 2},
        ],
    }


def layer_rows(score=0.0):
    return [
        {
            "layer_id": layer_id,
            "score": score,
            "max_score": maximum,
            "reason": "",
        }
        for layer_id, maximum in (
            ("A", 3.0),
            ("B", 6.0),
            ("C", 8.0),
            ("D", 6.0),
            ("E", 2.0),
        )
    ]


def baseline_scores():
    return {
        "A": 2.8,
        "B": 5.7,
        "C": 5.2,
        "D": 5.0,
        "E": 1.7,
    }


def general_eval(
    *,
    defects=None,
    requirements=None,
    demand_requirements=None,
    legacy_issues=None,
):
    return {
        "parsed": {
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
                "mode": "question_only_deterministic",
                "requirements": list(
                    demand_requirements or []
                ),
            },
            "question_type_coverage": {
                "overall_coverage": "adequate",
                "explicit_requirement_coverage": {
                    "requirements": list(
                        requirements or []
                    ),
                },
            },
            "layer_issue_ownership": list(
                legacy_issues or []
            ),
        },
    }


def present_requirement(
    requirement_id,
    demand_kind,
):
    return (
        {
            "requirement_id": requirement_id,
            "status": "present",
            "is_core": True,
        },
        {
            "requirement_id": requirement_id,
            "demand_kind": demand_kind,
        },
    )


class LayerSpecificEvidenceGuardTests(
    unittest.TestCase
):
    def test_c_correctness_error_blocks_only_c(self):
        evaluation = general_eval(
            defects=[
                {
                    "defect_id": "physics_error",
                    "defect_type": "correctness_error",
                    "severity": "partial",
                    "owner_layer": "C",
                    "explanation": "부호가 반대다.",
                }
            ]
        )

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                layer_rows(0.0),
                baseline_scores(),
                evaluation,
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(
            diagnostic["marker"],
            LAYER_EVIDENCE_GUARD_MARKER,
        )
        self.assertEqual(
            diagnostic["blocked_layers"],
            ["C"],
        )
        self.assertEqual(by_id["C"]["score"], 0.0)
        self.assertEqual(by_id["A"]["score"], 2.35)
        self.assertEqual(by_id["B"]["score"], 4.8)
        self.assertEqual(by_id["D"]["score"], 4.1)
        self.assertEqual(by_id["E"]["score"], 1.4)

    def test_d_major_depth_gap_blocks_only_d(self):
        evaluation = general_eval(
            defects=[
                {
                    "defect_id": "field_gap",
                    "defect_type": "core_depth_gap",
                    "severity": "major",
                    "owner_layer": "D",
                    "explanation": "최악 조건 검증이 없다.",
                }
            ]
        )

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                layer_rows(0.0),
                baseline_scores(),
                evaluation,
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(
            diagnostic["blocked_layers"],
            ["D"],
        )
        self.assertEqual(by_id["D"]["score"], 0.0)
        self.assertGreater(by_id["C"]["score"], 0.0)

    def test_presentation_issue_does_not_disable_c_guard(self):
        evaluation = general_eval(
            defects=[
                {
                    "defect_id": "formula_format",
                    "defect_type": "presentation_issue",
                    "severity": "partial",
                    "owner_layer": "C",
                    "explanation": "연산자 유실 가능성",
                }
            ]
        )

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                layer_rows(0.0),
                baseline_scores(),
                evaluation,
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(
            diagnostic["blocked_layers"],
            [],
        )
        self.assertEqual(by_id["C"]["score"], 3.6)

    def test_missing_design_requirement_blocks_b_and_d(self):
        requirement_id = "r_design"
        evaluation = general_eval(
            requirements=[
                {
                    "requirement_id": requirement_id,
                    "status": "missing",
                    "is_core": True,
                }
            ],
            demand_requirements=[
                {
                    "requirement_id": requirement_id,
                    "demand_kind": "DESIGN",
                }
            ],
        )

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                layer_rows(0.0),
                baseline_scores(),
                evaluation,
                scoring_model(),
            )
        )
        by_id = {
            row["layer_id"]: row
            for row in guarded
        }

        self.assertEqual(
            diagnostic["blocked_layers"],
            ["B", "D"],
        )
        self.assertEqual(by_id["B"]["score"], 0.0)
        self.assertEqual(by_id["D"]["score"], 0.0)
        self.assertGreater(by_id["C"]["score"], 0.0)

    def test_one_issue_uses_one_canonical_owner(self):
        evaluation = general_eval(
            defects=[
                {
                    "defect_id": "shared_issue",
                    "defect_type": "correctness_error",
                    "severity": "major",
                    "owner_layer": "C",
                    "explanation": "기술 오류",
                },
                {
                    "defect_id": "shared_issue",
                    "defect_type": "correctness_error",
                    "severity": "major",
                    "owner_layer": "D",
                    "explanation": "같은 오류 중복",
                },
            ]
        )

        policy = build_layer_evidence_policy(
            evaluation
        )

        self.assertTrue(policy["one_issue_one_owner"])
        self.assertEqual(
            policy["blocked_layers"],
            ["C"],
        )
        self.assertEqual(
            len(policy["canonical_issue_rows"]),
            1,
        )
        self.assertEqual(
            len(policy["ownership_conflicts"]),
            1,
        )

    def test_guard_never_raises_above_baseline(self):
        evaluation = general_eval()
        guarded, _ = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                layer_rows(0.0),
                {
                    "A": 2.0,
                    "B": 4.0,
                    "C": 4.0,
                    "D": 3.0,
                    "E": 1.0,
                },
                evaluation,
                scoring_model(),
            )
        )

        baseline = {
            "A": 2.0,
            "B": 4.0,
            "C": 4.0,
            "D": 3.0,
            "E": 1.0,
        }

        for row in guarded:
            self.assertLessEqual(
                row["score"],
                baseline[row["layer_id"]],
            )

    def test_legacy_contract_keeps_existing_global_behavior(self):
        evaluation = {
            "parsed": {
                "question_type_coverage": {
                    "overall_coverage": "adequate",
                    "explicit_requirement_coverage": {
                        "requirements": [
                            {
                                "requirement": "설명",
                                "status": "present",
                                "is_core": True,
                            }
                        ]
                    },
                },
                "layer_issue_ownership": [
                    {
                        "issue_id": "legacy_error",
                        "primary_owner_layer": "C",
                        "issue_type": "correctness_error",
                        "severity": "major",
                        "invalidates_core_conclusion": True,
                    }
                ],
            }
        }
        rows = layer_rows(1.0)
        before = copy.deepcopy(rows)

        guarded, diagnostic = (
            grading_agents
            ._phase6_apply_semantic_downward_guard(
                rows,
                baseline_scores(),
                evaluation,
                scoring_model(),
            )
        )

        self.assertFalse(diagnostic["eligible"])
        self.assertFalse(diagnostic["applied"])
        self.assertEqual(guarded, before)


if __name__ == "__main__":
    unittest.main()
