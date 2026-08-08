from __future__ import annotations

import inspect
import unittest

from coverage_feedback_event import (
    build_coverage_feedback_event,
)


def demands() -> dict:
    return {
        "ok": True,
        "demands": [
            {
                "id": "D1",
                "demand_id": "D1",
                "text": "RTD 측정 원리를 설명한다.",
            },
            {
                "id": "D2",
                "demand_id": "D2",
                "text": "변경관리 원칙을 제시한다.",
            },
        ],
    }


class CoverageFeedbackEventTest(unittest.TestCase):
    def test_pure_general_records_all_explicit_gaps(self):
        event = build_coverage_feedback_event(
            {
                "ok": True,
                "routing_mode": "GENERAL",
                "primary_topic_ids": [],
                "supporting_topic_ids": [],
                "uncovered_demand_ids": ["D1", "D2"],
            },
            demands(),
        )
        self.assertEqual(
            event["uncovered_demand_ids"],
            ["D1", "D2"],
        )
        self.assertEqual(len(event["gaps"]), 2)
        self.assertEqual(
            event["policy"]["score_effect"],
            "none",
        )
        self.assertEqual(
            event["policy"]["routing_effect"],
            "none",
        )

    def test_hybrid_records_only_uncovered_demand(self):
        event = build_coverage_feedback_event(
            {
                "ok": True,
                "routing_mode": "SINGLE_TOPIC",
                "primary_topic_ids": ["topic_a"],
                "supporting_topic_ids": [],
                "uncovered_demand_ids": ["D2"],
            },
            demands(),
        )
        self.assertEqual(
            event["primary_topic_ids"],
            ["topic_a"],
        )
        self.assertEqual(
            event["uncovered_demand_ids"],
            ["D2"],
        )
        self.assertEqual(
            event["gaps"][0]["demand_text"],
            "변경관리 원칙을 제시한다.",
        )

    def test_ambiguous_is_not_gap_feedback(self):
        event = build_coverage_feedback_event(
            {
                "ok": True,
                "routing_mode": "AMBIGUOUS",
                "uncovered_demand_ids": ["D1"],
            },
            demands(),
        )
        self.assertIsNone(event)

    def test_no_uncovered_is_no_event(self):
        event = build_coverage_feedback_event(
            {
                "ok": True,
                "routing_mode": "SINGLE_TOPIC",
                "primary_topic_ids": ["topic_a"],
                "uncovered_demand_ids": [],
            },
            demands(),
        )
        self.assertIsNone(event)

    def test_unknown_demand_ids_are_not_invented(self):
        event = build_coverage_feedback_event(
            {
                "ok": True,
                "routing_mode": "GENERAL",
                "uncovered_demand_ids": ["D2", "D999"],
            },
            demands(),
        )
        self.assertEqual(
            event["uncovered_demand_ids"],
            ["D2"],
        )

    def test_event_fingerprint_is_deterministic(self):
        semantic = {
            "ok": True,
            "routing_mode": "GENERAL",
            "uncovered_demand_ids": ["D1", "D2"],
        }
        first = build_coverage_feedback_event(
            semantic,
            demands(),
        )
        second = build_coverage_feedback_event(
            semantic,
            demands(),
        )
        self.assertEqual(
            first["event_fingerprint"],
            second["event_fingerprint"],
        )
        self.assertEqual(
            first["gaps"][0]["gap_fingerprint"],
            second["gaps"][0]["gap_fingerprint"],
        )

    def test_builder_has_no_student_answer_parameter(self):
        params = inspect.signature(
            build_coverage_feedback_event
        ).parameters
        self.assertEqual(
            list(params),
            [
                "semantic_result",
                "question_demand_result",
            ],
        )


if __name__ == "__main__":
    unittest.main()
