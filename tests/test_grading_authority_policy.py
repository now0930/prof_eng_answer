from __future__ import annotations

import unittest
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading_authority_policy import (
    GradingAuthorityError,
    enforce_requested_authority_mode,
    evaluate_authority_removal_gate,
)


def _replay(**overrides):
    value = {
        "known_fatal_recall": 1.0,
        "fatal_false_positive_count": 0,
        "deterministic_repeatability": 1.0,
        "unexplained_verdict_diff_count": 0,
        "external_llm_required_for_verdict": False,
    }
    value.update(overrides)
    return value


class GradingAuthorityPolicyTests(unittest.TestCase):
    def test_all_required_evidence_is_ready(self):
        result = evaluate_authority_removal_gate(
            _replay(), known_overgrading_regression_pass=True,
            normal_answer_regression_pass=True, score_verdict_consistency_pass=True,
        )
        self.assertEqual(result["decision"], "READY")
        self.assertEqual(result["requested_target"]["LLM_VERDICT_AUTHORITY"], 0)

    def test_current_recall_gap_holds_authority_removal(self):
        result = evaluate_authority_removal_gate(
            _replay(
                known_fatal_recall=0.111111,
                unexplained_verdict_diff_count=8,
                external_llm_required_for_verdict=True,
            ),
            known_overgrading_regression_pass=False,
            normal_answer_regression_pass=True,
            score_verdict_consistency_pass=False,
        )
        self.assertEqual(result["decision"], "HOLD")
        self.assertIn("KNOWN_FATAL_RECALL", {row["code"] for row in result["blockers"]})

    def test_default_runtime_preserves_legacy_primary(self):
        result = enforce_requested_authority_mode(environ={})
        self.assertFalse(result["DETERMINISTIC_GRADING_PRIMARY"])
        self.assertEqual(result["LLM_VERDICT_AUTHORITY"], 1)

    def test_premature_activation_is_rejected_fail_closed(self):
        with self.assertRaises(GradingAuthorityError):
            enforce_requested_authority_mode(
                environ={"DETERMINISTIC_GRADING_PRIMARY": "true"},
                gate_report={"ready": False},
            )

    def test_even_ready_gate_cannot_enable_unconnected_primary_engine(self):
        with self.assertRaisesRegex(GradingAuthorityError, "not connected"):
            enforce_requested_authority_mode(
                environ={"DETERMINISTIC_GRADING_PRIMARY": "true"},
                gate_report={"ready": True},
            )


if __name__ == "__main__":
    unittest.main()
