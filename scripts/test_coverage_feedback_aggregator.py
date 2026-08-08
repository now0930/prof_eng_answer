from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from coverage_feedback_aggregator import (
    COVERAGE_FEEDBACK_EVENT_FILENAME,
    aggregate_coverage_feedback,
)


def write_event(
    root: Path,
    session_id: str,
    *,
    event_fingerprint: str,
    gap_fingerprint: str,
    demand_text: str,
    routing_mode: str = "GENERAL",
    primary_topic_ids=None,
):
    session = root / session_id
    session.mkdir(parents=True)

    payload = {
        "version": "coverage_gap_event_v1",
        "event_type": "TOPIC_COVERAGE_GAP",
        "event_fingerprint": event_fingerprint,
        "routing_mode": routing_mode,
        "primary_topic_ids": primary_topic_ids or [],
        "supporting_topic_ids": [],
        "uncovered_demand_ids": ["D2"],
        "gaps": [
            {
                "demand_id": "D2",
                "demand_text": demand_text,
                "gap_fingerprint": gap_fingerprint,
            }
        ],
        "policy": {
            "score_effect": "none",
            "routing_effect": "none",
            "student_answer_used": False,
            "auto_topic_pack_creation": False,
        },
    }

    (
        session / COVERAGE_FEEDBACK_EVENT_FILENAME
    ).write_text(
        json.dumps(payload, ensure_ascii=False),
        encoding="utf-8",
    )


class CoverageFeedbackAggregatorTest(unittest.TestCase):
    def test_recurrence_reaches_human_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index in range(3):
                write_event(
                    root,
                    f"s{index}",
                    event_fingerprint=f"event-{index}",
                    gap_fingerprint="gap-a",
                    demand_text="변경관리 원칙",
                )

            result = aggregate_coverage_feedback(
                root,
                human_review_threshold=3,
            )

            self.assertEqual(
                result["valid_event_count"],
                3,
            )
            self.assertEqual(
                result["unique_gap_count"],
                1,
            )
            gap = result["gaps"][0]
            self.assertEqual(
                gap["occurrence_count"],
                3,
            )
            self.assertTrue(
                gap["human_review_candidate"]
            )
            self.assertEqual(
                gap["promotion_action"],
                "HUMAN_REVIEW",
            )
            self.assertFalse(
                gap["auto_topic_pack_creation"]
            )

    def test_below_threshold_remains_observe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_event(
                root,
                "s1",
                event_fingerprint="event-1",
                gap_fingerprint="gap-a",
                demand_text="변경관리 원칙",
            )

            result = aggregate_coverage_feedback(
                root,
                human_review_threshold=3,
            )

            gap = result["gaps"][0]
            self.assertFalse(
                gap["human_review_candidate"]
            )
            self.assertEqual(
                gap["promotion_action"],
                "OBSERVE",
            )

    def test_same_event_fingerprint_across_sessions_counts_recurrence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_event(
                root,
                "s1",
                event_fingerprint="same-event",
                gap_fingerprint="gap-a",
                demand_text="변경관리 원칙",
            )
            write_event(
                root,
                "s2",
                event_fingerprint="same-event",
                gap_fingerprint="gap-a",
                demand_text="변경관리 원칙",
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
                result["gaps"][0][
                    "occurrence_count"
                ],
                2,
            )
            self.assertTrue(
                result["gaps"][0][
                    "human_review_candidate"
                ]
            )

    def test_invalid_scoring_event_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_event(
                root,
                "s1",
                event_fingerprint="event-1",
                gap_fingerprint="gap-a",
                demand_text="변경관리 원칙",
            )

            path = (
                root
                / "s1"
                / COVERAGE_FEEDBACK_EVENT_FILENAME
            )
            payload = json.loads(
                path.read_text(encoding="utf-8")
            )
            payload["policy"]["score_effect"] = "yes"
            path.write_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = aggregate_coverage_feedback(
                root
            )
            self.assertEqual(
                result["valid_event_count"],
                0,
            )
            self.assertEqual(result["gaps"], [])

    def test_hybrid_topic_context_is_observation_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_event(
                root,
                "s1",
                event_fingerprint="event-1",
                gap_fingerprint="gap-a",
                demand_text="변경관리 원칙",
                routing_mode="SINGLE_TOPIC",
                primary_topic_ids=["topic_a"],
            )

            result = aggregate_coverage_feedback(
                root
            )

            gap = result["gaps"][0]
            self.assertEqual(
                gap["routing_modes"],
                ["SINGLE_TOPIC"],
            )
            self.assertEqual(
                gap["primary_topic_ids"],
                ["topic_a"],
            )
            self.assertEqual(
                result["policy"][
                    "current_question_effect"
                ],
                "none",
            )

    def test_missing_root_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = aggregate_coverage_feedback(
                Path(tmp) / "missing"
            )
            self.assertEqual(
                result["valid_event_count"],
                0,
            )
            self.assertEqual(result["gaps"], [])


if __name__ == "__main__":
    unittest.main()
