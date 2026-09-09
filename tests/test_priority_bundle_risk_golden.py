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


class PriorityBundleRiskGoldenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads((
            REPO / "calibration/risk_golden/stage50_54_priority_bundle_cases.json"
        ).read_text(encoding="utf-8"))
        cls.cases = payload["cases"]

    def evaluate(self, case):
        route = route_question_topics(case["question"])
        extraction = extract_canonical_claim_evidence(
            case["answer"], question_text=case["question"],
            topic_ids=route["topic_ids"],
        )
        result = evaluate_deterministic_requirements(
            claims=extraction["canonical_evidence"]["claims"],
            invariant_codes=[], topic_ids=route["topic_ids"],
            extraction_complete=True,
        )
        score = calculate_deterministic_score(result, answer_text=case["answer"])
        return route, result, score

    def test_each_case_keeps_its_owner_in_routing(self):
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                route, _, _ = self.evaluate(case)
                self.assertIn(case["topic_id"], route["topic_ids"])

    def test_normal_lanes_are_satisfied_without_fatal(self):
        for case in (row for row in self.cases if row["lane"] == "normal"):
            with self.subTest(case_id=case["case_id"]):
                _, result, _ = self.evaluate(case)
                self.assertGreaterEqual(result["summary"]["SATISFIED"], 1)
                self.assertEqual(result["summary"]["WRONG"], 0)
                self.assertFalse(result["fatal_or_core_error"])

    def test_adverse_lanes_are_incomplete_without_false_fatal(self):
        for case in (row for row in self.cases if row["lane"] == "adverse"):
            with self.subTest(case_id=case["case_id"]):
                _, result, _ = self.evaluate(case)
                self.assertGreater(
                    result["summary"]["PARTIAL"] + result["summary"]["MISSING"], 0
                )
                self.assertEqual(result["summary"]["WRONG"], 0)
                self.assertFalse(result["fatal_or_core_error"])

    def test_fatal_lanes_are_wrong_capped_and_never_pass(self):
        for case in (row for row in self.cases if row["lane"] == "fatal"):
            with self.subTest(case_id=case["case_id"]):
                _, result, score = self.evaluate(case)
                self.assertGreaterEqual(result["summary"]["WRONG"], 1)
                self.assertTrue(result["fatal_or_core_error"])
                self.assertFalse(score["official_pass_met"])


if __name__ == "__main__":
    unittest.main()
