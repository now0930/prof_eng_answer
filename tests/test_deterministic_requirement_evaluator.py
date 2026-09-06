import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_requirement_evaluator import evaluate_deterministic_requirements


SIL_TOPIC = "sil_target_determination_risk_reduction_and_lifecycle"


class DeterministicRequirementEvaluatorTests(unittest.TestCase):
    def test_invariant_forces_wrong_and_blocks_full_credit(self):
        result = evaluate_deterministic_requirements(
            claims=[],
            invariant_codes=["INVALID_TARGET_PROBABILITY_FREQUENCY_PRODUCT"],
            topic_ids=[SIL_TOPIC],
        )
        states = {row["requirement_id"]: row["status"] for row in result["requirements"]}
        self.assertEqual(states["target_pfd_relation"], "WRONG")
        self.assertTrue(result["fatal_or_core_error"])
        self.assertFalse(result["requirement_full_credit_allowed"])
        self.assertFalse(result["perfect_theory_comment_allowed"])

    def test_unresolved_evidence_is_unknown_not_missing(self):
        result = evaluate_deterministic_requirements(
            claims=[], invariant_codes=[], topic_ids=[SIL_TOPIC]
        )
        self.assertEqual({row["status"] for row in result["requirements"]}, {"UNKNOWN"})

    def test_complete_extraction_may_produce_missing(self):
        result = evaluate_deterministic_requirements(
            claims=[], invariant_codes=[], topic_ids=[SIL_TOPIC], extraction_complete=True
        )
        self.assertEqual({row["status"] for row in result["requirements"]}, {"MISSING"})

    def test_matching_canonical_fact_is_satisfied(self):
        claim = {
            "subject": "target_probability", "predicate": "derived_by_ratio",
            "object": "event_frequencies", "polarity": "positive",
        }
        result = evaluate_deterministic_requirements(
            claims=[claim], invariant_codes=[], topic_ids=[SIL_TOPIC]
        )
        row = next(row for row in result["requirements"] if row["requirement_id"] == "target_pfd_relation")
        self.assertEqual(row["status"], "SATISFIED")

    def test_global_invariant_owner_survives_neighbor_primary_routing(self):
        result = evaluate_deterministic_requirements(
            claims=[],
            invariant_codes=["DIMENSIONALLY_INVALID_COMPARISON"],
            topic_ids=["hazop_lopa_ipl_risk_reduction_sil_target_allocation"],
        )

        finding = next(
            row for row in result["findings"]
            if row["invariant_code"] == "DIMENSIONALLY_INVALID_COMPARISON"
        )
        self.assertEqual(
            finding["owner_topic_id"],
            "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh",
        )
        self.assertTrue(result["fatal_or_core_error"])


if __name__ == "__main__":
    unittest.main()
