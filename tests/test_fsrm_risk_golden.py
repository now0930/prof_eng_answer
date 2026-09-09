import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from canonical_claim_extractor import extract_canonical_claim_evidence
from deterministic_requirement_evaluator import evaluate_deterministic_requirements
from deterministic_score_engine import calculate_deterministic_score
from deterministic_topic_router import route_question_topics
from engineering_invariant_evaluator import evaluate_engineering_invariants
from fact_anchor_evidence_adapter import (
    augment_requirement_evaluation,
    evaluate_fact_anchor_requirements,
    requirement_scope_by_topic,
)
from quantity_dimension_evaluator import evaluate_quantity_dimension_consistency


TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"


class FsrmRiskGoldenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads((
            REPO / "calibration/risk_golden/functional_safety_demand_mode_cases.json"
        ).read_text(encoding="utf-8"))
        cls.cases = {row["case_id"]: row for row in payload["cases"]}

    def evaluate(self, case_id):
        case = self.cases[case_id]
        route = route_question_topics(case["question"])
        extraction = extract_canonical_claim_evidence(
            case["answer"], question_text=case["question"], topic_ids=route["topic_ids"],
        )
        quantity = evaluate_quantity_dimension_consistency(extraction["canonical_evidence"])
        engineering = evaluate_engineering_invariants(case["answer"])
        invariant_codes = {
            row["code"] for row in quantity["violations"] + engineering["violations"]
        }
        anchors = evaluate_fact_anchor_requirements(
            answer_text=case["answer"], topic_ids=route["topic_ids"],
            question_text=case["question"],
        )
        result = evaluate_deterministic_requirements(
            claims=extraction["canonical_evidence"]["claims"],
            invariant_codes=invariant_codes,
            topic_ids=route["topic_ids"], extraction_complete=True,
            requirement_scope_by_topic=requirement_scope_by_topic(anchors),
        )
        result = augment_requirement_evaluation(result, anchors)
        return route, {row["requirement_id"]: row for row in result["requirements"]}, result, calculate_deterministic_score(result, answer_text=case["answer"])

    def test_normal_partial_and_fatal_mutations_keep_one_topic_owner(self):
        for case_id in self.cases:
            with self.subTest(case_id=case_id):
                route, _, _, _ = self.evaluate(case_id)
                self.assertEqual(route["topic_ids"], [TOPIC])

    def test_normal_case_has_no_fatal_and_passes(self):
        _, rows, result, score = self.evaluate("risk_fsrm_demand_mode_normal_01")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "SATISFIED")
        self.assertEqual(rows["quantitative_verification_dimension"]["status"], "SATISFIED")
        self.assertFalse(result["fatal_or_core_error"])
        self.assertTrue(score["official_pass_met"])

    def test_partial_case_does_not_false_pass(self):
        _, rows, result, score = self.evaluate("risk_fsrm_demand_mode_partial_01")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "PARTIAL")
        self.assertNotEqual(rows["quantitative_verification_dimension"]["status"], "WRONG")
        self.assertFalse(result["fatal_or_core_error"])
        self.assertFalse(score["official_pass_met"])

    def test_dimension_and_mode_mutation_is_fatal(self):
        _, rows, result, score = self.evaluate("risk_fsrm_demand_mode_fatal_01")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "WRONG")
        self.assertEqual(rows["quantitative_verification_dimension"]["status"], "WRONG")
        self.assertTrue(result["fatal_or_core_error"])
        self.assertFalse(score["official_pass_met"])


if __name__ == "__main__":
    unittest.main()
