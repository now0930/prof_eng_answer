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


if __name__ == "__main__":
    unittest.main()
