import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from quantity_dimension_evaluator import (
    analyze_quantity_dimensions,
    load_quantity_dimension_ontology,
)


class QuantityDimensionEvaluatorTests(unittest.TestCase):
    def test_global_ontology_owns_quantity_dimensions(self):
        ontology = load_quantity_dimension_ontology()
        self.assertEqual(ontology["quantities"]["failure_rate"]["dimension"], "inverse_time")
        self.assertEqual(ontology["quantities"]["pfh"]["dimension"], "inverse_time")
        self.assertEqual(ontology["quantities"]["pfd"]["dimension"], "dimensionless")
        self.assertEqual(ontology["quantities"]["pfdavg"]["dimension"], "dimensionless")

    def test_stage34c1_operating_failure_is_a_deterministic_invariant(self):
        fixture = json.loads(
            (REPO / "calibration/sis_lopa_architecture_overgrading_regression.json")
            .read_text(encoding="utf-8")
        )
        result = analyze_quantity_dimensions(fixture["answer"], question_text=fixture["question"])
        codes = {row["code"] for row in result["violations"]}
        self.assertIn("DIMENSIONALLY_INVALID_COMPARISON", codes)
        self.assertTrue(result["technical_error_detected"])
        self.assertFalse(result["requirement_full_credit_allowed"])
        self.assertFalse(result["perfect_theory_comment_allowed"])
        self.assertEqual(result["engine"], "deterministic")

    def test_symbolic_and_language_variants_use_the_same_rule(self):
        variants = (
            "lambda < PFDavg로 설계한다.",
            "PFD가 고장률보다 크게 유지되도록 설계한다.",
            "failure rate is less than PFD.",
            "PFH를 PFD와 직접 비교한다.",
        )
        for answer in variants:
            with self.subTest(answer=answer):
                result = analyze_quantity_dimensions(answer)
                self.assertEqual(result["violations"][0]["code"], "DIMENSIONALLY_INVALID_COMPARISON")

    def test_same_dimension_ordering_is_valid(self):
        for answer in ("lambda < PFH로 설계한다.", "PFDavg는 PFD보다 작다."):
            with self.subTest(answer=answer):
                result = analyze_quantity_dimensions(answer)
                self.assertFalse(result["technical_error_detected"])

    def test_corrective_or_negated_examples_are_not_errors(self):
        variants = (
            "lambda와 PFDavg는 차원이 달라 직접 비교할 수 없다.",
            "잘못된 예시: lambda < PFDavg.",
            "lambda가 PFD보다 작도록 설계하면 안 된다.",
        )
        for answer in variants:
            with self.subTest(answer=answer):
                result = analyze_quantity_dimensions(answer)
                self.assertFalse(result["technical_error_detected"])

    def test_invalid_dimension_assertion_mutation(self):
        result = analyze_quantity_dimensions("PFDavg는 시간당 고장률이다.")
        self.assertEqual(
            result["violations"][0]["code"],
            "DIMENSIONALLY_INVALID_COMPARISON",
        )

    def test_multiple_correct_dimension_assertions_do_not_cross_bind(self):
        result = analyze_quantity_dimensions(
            "PFDavg는 무차원이고 lambda는 시간당 고장률이다."
        )
        self.assertEqual(result["checked_claim_count"], 2)
        self.assertFalse(result["technical_error_detected"])

    def test_repeatability_is_exact(self):
        answer = "lambda_SIS 비율이 PFD 비율보다 작도록 시스템을 설계."
        first = analyze_quantity_dimensions(answer)
        for _ in range(10):
            self.assertEqual(first, analyze_quantity_dimensions(answer))


if __name__ == "__main__":
    unittest.main()
