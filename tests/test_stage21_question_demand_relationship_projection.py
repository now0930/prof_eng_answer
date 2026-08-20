from __future__ import annotations

import copy
import unittest
from pathlib import Path

from question_demand_evidence import (
    project_logic_relationship_conflicts,
)


class Stage21QuestionDemandRelationshipProjectionTests(
    unittest.TestCase
):
    def _evidence(self) -> dict:
        return {
            "version": "QUESTION_DEMAND_EVIDENCE_V1",
            "status": "shadow_only",
            "score_effect": "none",
            "demand_count": 2,
            "demands": [
                {
                    "demand_id": "D1",
                    "text": "Explain relationship direction.",
                    "covered": True,
                    "verified": True,
                    "level": 1.0,
                },
                {
                    "demand_id": "D2",
                    "text": "Explain operating conditions.",
                    "covered": False,
                    "verified": False,
                    "level": 0.0,
                },
            ],
            "summary": {
                "covered_ratio": 0.5,
                "verified_ratio": 0.5,
                "mean_demand_level": 0.5,
            },
        }

    def _metadata_finding(self) -> dict:
        return {
            "candidate_id": "C1",
            "rule_id": "R1",
            "severity": "fatal",
            "message": "relationship direction is reversed",
            "correct_rule": "B causes A",
            "error_class": "RELATIONSHIP_DIRECTION",
            "claim_signature": "A->B",
            "anchor_refs": ["A1", "A1"],
            "demand_refs": ["D1", "UNKNOWN", "D1"],
            "untrusted_extra": "must not be projected",
        }

    def test_projects_only_matching_demand_refs_score_neutrally(
        self,
    ) -> None:
        evidence = self._evidence()
        baseline = copy.deepcopy(evidence)

        projected = project_logic_relationship_conflicts(
            evidence,
            {"findings": [self._metadata_finding()]},
        )

        self.assertEqual(baseline, evidence)
        self.assertEqual(
            baseline["demands"],
            projected["demands"],
        )
        self.assertEqual(
            baseline["summary"],
            projected["summary"],
        )
        self.assertEqual("none", projected["score_effect"])

        conflicts = projected["relationship_conflicts"]
        self.assertEqual(1, len(conflicts))
        self.assertEqual(["D1"], conflicts[0]["matched_demand_refs"])
        self.assertEqual(
            ["D1", "UNKNOWN"],
            conflicts[0]["demand_refs"],
        )
        self.assertEqual(["A1"], conflicts[0]["anchor_refs"])
        self.assertNotIn("untrusted_extra", conflicts[0])

        summary = projected["relationship_conflict_summary"]
        self.assertEqual("none", summary["score_effect"])
        self.assertEqual(1, summary["conflict_count"])
        self.assertEqual(["D1"], summary["affected_demand_refs"])

    def test_legacy_finding_does_not_materialize_projection(
        self,
    ) -> None:
        evidence = self._evidence()
        projected = project_logic_relationship_conflicts(
            evidence,
            {
                "findings": [
                    {
                        "candidate_id": "C2",
                        "rule_id": "R2",
                        "severity": "fatal",
                        "message": "legacy finding",
                        "correct_rule": "legacy rule",
                    }
                ]
            },
        )

        self.assertEqual(evidence, projected)
        self.assertNotIn("relationship_conflicts", projected)
        self.assertNotIn(
            "relationship_conflict_summary",
            projected,
        )

    def test_unmatched_demand_refs_do_not_change_payload(
        self,
    ) -> None:
        evidence = self._evidence()
        finding = self._metadata_finding()
        finding["demand_refs"] = ["UNKNOWN"]

        projected = project_logic_relationship_conflicts(
            evidence,
            {"findings": [finding]},
        )

        self.assertEqual(evidence, projected)

    def test_duplicate_findings_are_deduplicated(
        self,
    ) -> None:
        evidence = self._evidence()
        finding = self._metadata_finding()

        projected = project_logic_relationship_conflicts(
            evidence,
            {"findings": [finding, copy.deepcopy(finding)]},
        )

        self.assertEqual(
            1,
            len(projected["relationship_conflicts"]),
        )
        self.assertEqual(
            1,
            projected[
                "relationship_conflict_summary"
            ]["conflict_count"],
        )

    def test_orchestrator_projects_after_scoring_before_formula(
        self,
    ) -> None:
        source = Path("grading_agents.py").read_text(
            encoding="utf-8"
        )

        qd_score_index = source.index(
            "_phase3_apply_question_demand_evidence_to_layer_scores("
        )
        logic_attach_index = source.index(
            "grade = attach_logic_check_to_grade("
        )
        logic_eval_index = source.index(
            'logic_eval = grade.get("logic_check_evaluation")'
        )
        projection_index = source.index(
            "project_logic_relationship_conflicts("
        )
        formula_index = source.index(
            "grade = attach_control_valve_formula_check("
        )

        self.assertLess(qd_score_index, logic_attach_index)
        self.assertLess(logic_attach_index, logic_eval_index)
        self.assertLess(logic_eval_index, projection_index)
        self.assertLess(projection_index, formula_index)
        self.assertIn(
            "question_demand_evidence_for_score",
            source[logic_eval_index:formula_index],
        )


if __name__ == "__main__":
    unittest.main()
