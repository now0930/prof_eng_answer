import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_replay_audit import run_deterministic_replay_audit


class DeterministicReplayAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_deterministic_replay_audit(
            root=REPO,
            golden_path=REPO / "calibration/expert_accuracy_golden.jsonl",
        )

    def test_replay_is_provider_free_and_repeatable(self):
        self.assertEqual(self.report["provider_calls"], 0)
        self.assertEqual(self.report["case_count"], 30)
        self.assertEqual(self.report["deterministic_repeatability"], 1.0)

    def test_stage34c1_fatal_is_recalled(self):
        row = next(
            row for row in self.report["cases"]
            if row["case_id"] == "sis_lopa_architecture_issue1"
        )
        self.assertIn("failure_rate_compared_directly_to_pfd", row["detected_fatal_ids"])

    def test_audit_fails_closed_on_unimplemented_invariants(self):
        self.assertLess(self.report["known_fatal_recall"], 1.0)
        self.assertGreater(self.report["unexplained_verdict_diff_count"], 0)
        self.assertEqual(self.report["decision"], "HOLD")
        self.assertTrue(self.report["external_llm_required_for_verdict"])

    def test_runtime_has_no_llm_imports(self):
        source = (REPO / "deterministic_replay_audit.py").read_text(encoding="utf-8")
        for forbidden in ("gemini_grader", "logic_llm_verifier", "clova_grader"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
