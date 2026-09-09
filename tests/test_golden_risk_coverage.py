import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from golden_risk_coverage import audit_golden_risk_coverage


class GoldenRiskCoverageTests(unittest.TestCase):
    def test_repository_inventory_is_complete_and_ranked(self):
        report = audit_golden_risk_coverage(
            root=REPO,
            golden_path=REPO / "calibration/expert_accuracy_golden.jsonl",
        )
        topic_count = len(list((REPO / "rubrics/topic_packs").iterdir()))
        self.assertEqual(report["topic_count"], topic_count)
        priorities = [row["expansion_priority"] for row in report["topics"]]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_normal_adverse_and_fatal_lanes_are_counted_separately(self):
        topic = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
        base = {
            "version": "expert_accuracy_case_v1",
            "review_status": "reviewed",
            "review": {
                "reviewer": "test", "method": "expert_review",
                "reviewed_at": "2026-09-09T00:00:00+09:00",
                "evidence_path": "test",
            },
            "source": {}, "topic_ids": [topic], "question_type": "PRINCIPLE_INTERPRETATION",
            "labels": {
                "demands": [{"demand_id": "d", "requirement": "r", "core": True, "status": "CORRECT"}],
                "score_range": {"min": 1, "max": 2},
                "flags": {"passing_score_allowed": True, "strong_verdict_allowed": False, "confidence_ceiling": "high"},
            },
        }
        normal = {**base, "case_id": "normal", "labels": {**base["labels"], "findings": []}}
        fatal = {**base, "case_id": "fatal", "labels": {
            **base["labels"], "findings": [{"finding_id": "f", "severity": "fatal"}],
            "flags": {**base["labels"]["flags"], "passing_score_allowed": False},
        }}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "golden.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in (normal, fatal)) + "\n", encoding="utf-8")
            report = audit_golden_risk_coverage(root=REPO, golden_path=path)
        row = next(item for item in report["topics"] if item["topic_id"] == topic)
        self.assertEqual(row["normal_case_count"], 1)
        self.assertEqual(row["adverse_case_count"], 1)
        self.assertEqual(row["fatal_case_count"], 1)
        self.assertEqual(row["missing_lanes"], [])


if __name__ == "__main__":
    unittest.main()
