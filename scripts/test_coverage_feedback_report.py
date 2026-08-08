from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from coverage_feedback_report import (
    build_coverage_review_report,
    render_coverage_review_markdown,
)


def aggregate() -> dict:
    return {
        "version": "coverage_feedback_aggregate_v1",
        "valid_event_count": 5,
        "unique_gap_count": 2,
        "human_review_threshold": 3,
        "gaps": [
            {
                "gap_fingerprint": "gap-a",
                "occurrence_count": 4,
                "session_ids": ["s1", "s2", "s3", "s4"],
                "sample_demand_texts": [
                    "변경관리 원칙을 설명한다."
                ],
                "routing_modes": ["GENERAL"],
                "primary_topic_ids": [],
                "human_review_candidate": True,
                "promotion_action": "HUMAN_REVIEW",
                "auto_topic_pack_creation": False,
            },
            {
                "gap_fingerprint": "gap-b",
                "occurrence_count": 1,
                "session_ids": ["s5"],
                "sample_demand_texts": [
                    "예비품 표준화를 설명한다."
                ],
                "routing_modes": ["SINGLE_TOPIC"],
                "primary_topic_ids": ["topic_a"],
                "human_review_candidate": False,
                "promotion_action": "OBSERVE",
                "auto_topic_pack_creation": False,
            },
        ],
    }


class CoverageFeedbackReportTest(unittest.TestCase):
    def test_review_candidate_is_first(self):
        report = build_coverage_review_report(
            aggregate()
        )
        self.assertEqual(
            report["human_review_candidate_count"],
            1,
        )
        self.assertEqual(
            report["candidates"][0][
                "review_status"
            ],
            "HUMAN_REVIEW",
        )
        self.assertEqual(
            report["candidates"][1][
                "review_status"
            ],
            "OBSERVE",
        )

    def test_report_policy_is_advisory_only(self):
        report = build_coverage_review_report(
            aggregate()
        )
        policy = report["policy"]
        self.assertTrue(policy["report_only"])
        self.assertEqual(
            policy["current_question_effect"],
            "none",
        )
        self.assertEqual(
            policy["score_effect"],
            "none",
        )
        self.assertEqual(
            policy["routing_effect"],
            "none",
        )
        self.assertFalse(
            policy["auto_topic_pack_creation"]
        )
        self.assertFalse(
            policy["auto_topic_pack_update"]
        )
        self.assertTrue(
            policy["human_review_required"]
        )

    def test_markdown_contains_governance(self):
        report = build_coverage_review_report(
            aggregate()
        )
        text = render_coverage_review_markdown(
            report
        )
        self.assertIn(
            "HUMAN_REVIEW",
            text,
        )
        self.assertIn(
            "OBSERVE",
            text,
        )
        self.assertIn(
            "does not change routing, scoring",
            text,
        )

    def test_cli_empty_sessions_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            root.mkdir()

            out = subprocess.check_output(
                [
                    sys.executable,
                    "scripts/report_coverage_feedback.py",
                    "--sessions-root",
                    str(root),
                    "--format",
                    "json",
                ],
                text=True,
            )
            payload = json.loads(out)
            self.assertEqual(
                payload["valid_event_count"],
                0,
            )
            self.assertEqual(
                payload["candidates"],
                [],
            )
            self.assertEqual(
                list(root.iterdir()),
                [],
            )


if __name__ == "__main__":
    unittest.main()
