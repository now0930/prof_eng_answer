"""No secrets or scores are promoted by the private HOLD diagnostic."""
from copy import deepcopy
import unittest
from scripts.audit_expert_qualification_failures import analyze_failures, safe_id

class HoldAuditTest(unittest.TestCase):
    def setUp(self):
        self.gold = [
            {"case_id": "sil", "labels": {
                "demands": [{"demand_id": "system", "status": "PARTIAL"},
                            {"demand_id": "lifecycle", "status": "PARTIAL"}],
                "score_range": {"min": 10, "max": 14.5}}},
            {"case_id": "abstained", "labels": {
                "demands": [{"demand_id": "ground", "status": "CORRECT"}],
                "score_range": {"min": 13, "max": 19}}},
        ]
        self.rows = [
            {"case_id": "sil", "status": "FAILED",
             "reason_code": "unresolved_requirement",
             "error_type": "ProductionGradeFailure"},
            {"case_id": "abstained", "status": "FAILED",
             "reason_code": "execution_error",
             "error_type": "DeterministicPrimaryError"},
        ]

    def test_redacts_quotes_and_requires_exact_demand_id_alignment(self):
        private_grade = {
            "total_score": 6.47,
            "learner_answer": "SECRET LEARNER TEXT",
            "provider_raw": "SECRET PROVIDER PROMPT",
            "requirements": [{"requirement_id": "lifecycle", "status": "WRONG"},
                             {"requirement_id": "other", "status": "MISSING"}],
            "deterministic_score": {"score_breakdown": {
                "A_structure": 3, "B_requirement_completeness": 0.97,
                "C_fact_correctness": 2.5,
                "D_engineering_judgment": 0, "E_linkage": 0}},
            "qualitative_de_evaluation": {"status": "APPLIED", "provider_calls": 1,
                                          "quoted_text": "SECRET PROVIDER PROMPT"},
            "resolution_review": {"required": True,
                                  "requirement_ids": ["lifecycle"]},
        }
        original = deepcopy(private_grade)
        report = analyze_failures(self.gold, self.rows, {"sil": private_grade})
        self.assertEqual(report["qualification_status"], "HOLD")
        self.assertEqual(report["failed_count"], 2)
        self.assertEqual(report["cases"][0]["direct_disagreements"], ["lifecycle"])
        self.assertEqual(report["cases"][0]["unmapped_expert_ids"], ["system"])
        self.assertEqual(report["cases"][0]["outside_expert_range_by"], 3.53)
        self.assertEqual(report["cases"][0]["argon_status"], "APPLIED")
        self.assertFalse(report["cases"][1]["grade_available"])
        self.assertNotIn("total_score", report["cases"][1])
        self.assertNotIn("SECRET", str(report))
        self.assertEqual(private_grade, original)

    def test_rejects_directory_traversal_case_id(self):
        self.assertIsNone(safe_id(".."))
        self.assertIsNone(safe_id("."))
        self.assertIsNone(safe_id("../private"))
        self.assertEqual(safe_id("sil_target_operations_issue1"),
                         "sil_target_operations_issue1")

    def test_rejects_unknown_and_duplicate_cases(self):
        with self.assertRaises(ValueError):
            analyze_failures(self.gold, [{"case_id": "absent", "status": "FAILED"}], {})
        with self.assertRaises(ValueError):
            analyze_failures(self.gold, [self.rows[0], self.rows[0]], {})


if __name__ == "__main__":
    unittest.main()
