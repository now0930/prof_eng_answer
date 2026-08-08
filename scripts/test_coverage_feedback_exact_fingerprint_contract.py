from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from coverage_feedback_aggregator import (
    COVERAGE_FEEDBACK_EVENT_FILENAME,
    aggregate_coverage_feedback,
)
from coverage_feedback_event import (
    build_coverage_feedback_event,
)
from coverage_feedback_report import (
    build_coverage_review_report,
    render_coverage_review_markdown,
)


def _demand_result(text: str) -> dict:
    return {
        "ok": True,
        "demands": [
            {
                "id": "D1",
                "demand_id": "D1",
                "text": text,
            }
        ],
    }


def _semantic() -> dict:
    return {
        "ok": True,
        "routing_mode": "GENERAL",
        "primary_topic_ids": [],
        "supporting_topic_ids": [],
        "uncovered_demand_ids": ["D1"],
    }


def _write_event(
    root: Path,
    session_id: str,
    text: str,
) -> dict:
    event = build_coverage_feedback_event(
        _semantic(),
        _demand_result(text),
    )
    assert event is not None

    session = root / session_id
    session.mkdir(parents=True)
    (
        session / COVERAGE_FEEDBACK_EVENT_FILENAME
    ).write_text(
        json.dumps(event, ensure_ascii=False),
        encoding="utf-8",
    )
    return event


class ExactFingerprintCoverageContractTest(
    unittest.TestCase
):
    def test_identical_normalized_text_counts_distinct_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            first = _write_event(
                root,
                "s1",
                "계측설비   변경관리 원칙을 설명한다.",
            )
            second = _write_event(
                root,
                "s2",
                "  계측설비 변경관리 원칙을 설명한다.  ",
            )

            self.assertEqual(
                first["event_fingerprint"],
                second["event_fingerprint"],
            )
            self.assertEqual(
                first["gaps"][0]["gap_fingerprint"],
                second["gaps"][0]["gap_fingerprint"],
            )

            result = aggregate_coverage_feedback(
                root,
                human_review_threshold=2,
            )

            self.assertEqual(
                result["valid_event_count"],
                2,
            )
            self.assertEqual(
                result["unique_gap_count"],
                1,
            )
            self.assertEqual(
                result["gaps"][0]["occurrence_count"],
                2,
            )
            self.assertTrue(
                result["gaps"][0][
                    "human_review_candidate"
                ]
            )

    def test_semantic_paraphrases_remain_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            first = _write_event(
                root,
                "s1",
                "계측설비 변경관리 원칙을 설명한다.",
            )
            second = _write_event(
                root,
                "s2",
                "계장 설비 변경 시 관리 절차를 설명한다.",
            )

            self.assertNotEqual(
                first["gaps"][0]["gap_fingerprint"],
                second["gaps"][0]["gap_fingerprint"],
            )

            result = aggregate_coverage_feedback(
                root,
                human_review_threshold=2,
            )

            self.assertEqual(
                result["valid_event_count"],
                2,
            )
            self.assertEqual(
                result["unique_gap_count"],
                2,
            )
            self.assertEqual(
                sorted(
                    row["occurrence_count"]
                    for row in result["gaps"]
                ),
                [1, 1],
            )
            self.assertEqual(
                result["human_review_candidate_count"],
                0,
            )

    def test_aggregate_exposes_exact_grouping_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = aggregate_coverage_feedback(
                Path(tmp)
            )

        policy = result["policy"]
        self.assertEqual(
            policy["gap_grouping_strategy"],
            "normalized_exact_text_sha256",
        )
        self.assertEqual(
            policy["cross_session_recurrence_unit"],
            "distinct_session",
        )
        self.assertFalse(
            policy["semantic_clustering_performed"]
        )
        self.assertFalse(
            policy["semantic_equivalence_inferred"]
        )
        self.assertTrue(
            policy["paraphrases_may_remain_separate"]
        )

    def test_empty_report_still_exposes_limit(self):
        aggregate = {
            "version": "coverage_feedback_aggregate_v1",
            "valid_event_count": 0,
            "unique_gap_count": 0,
            "human_review_threshold": 3,
            "gaps": [],
            "policy": {
                "gap_grouping_strategy": (
                    "normalized_exact_text_sha256"
                ),
                "cross_session_recurrence_unit": (
                    "distinct_session"
                ),
                "semantic_clustering_performed": False,
                "semantic_equivalence_inferred": False,
                "paraphrases_may_remain_separate": True,
            },
        }

        report = build_coverage_review_report(
            aggregate
        )
        grouping = report["coverage_grouping"]

        self.assertEqual(
            grouping["strategy"],
            "normalized_exact_text_sha256",
        )
        self.assertEqual(
            grouping["cross_session_recurrence_unit"],
            "distinct_session",
        )
        self.assertFalse(
            grouping["semantic_clustering_performed"]
        )
        self.assertFalse(
            grouping["semantic_equivalence_inferred"]
        )
        self.assertTrue(
            grouping["paraphrases_may_remain_separate"]
        )

        markdown = render_coverage_review_markdown(
            report
        )
        self.assertIn("## Governance", markdown)
        self.assertIn(
            "counts distinct sessions",
            markdown,
        )
        self.assertIn(
            "normalized exact-text fingerprints only",
            markdown,
        )
        self.assertIn(
            "no semantic clustering",
            markdown,
        )


if __name__ == "__main__":
    unittest.main()
