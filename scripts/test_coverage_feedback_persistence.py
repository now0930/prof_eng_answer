from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coverage_feedback_persistence import (
    COVERAGE_FEEDBACK_EVENT_FILENAME,
    persist_session_coverage_feedback_event,
)


def demands():
    return {
        "ok": True,
        "demands": [
            {
                "id": "D1",
                "demand_id": "D1",
                "text": "Topic-owned demand",
            },
            {
                "id": "D2",
                "demand_id": "D2",
                "text": "General gap demand",
            },
        ],
    }


class CoverageFeedbackPersistenceTest(unittest.TestCase):
    def test_writes_one_session_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            event = persist_session_coverage_feedback_event(
                tmp,
                {
                    "ok": True,
                    "routing_mode": "SINGLE_TOPIC",
                    "primary_topic_ids": ["topic_a"],
                    "uncovered_demand_ids": ["D2"],
                },
                demands(),
            )

            self.assertIsNotNone(event)
            path = (
                Path(tmp)
                / COVERAGE_FEEDBACK_EVENT_FILENAME
            )
            self.assertTrue(path.is_file())

            payload = json.loads(
                path.read_text(encoding="utf-8")
            )
            self.assertEqual(
                payload["uncovered_demand_ids"],
                ["D2"],
            )
            self.assertEqual(
                payload["policy"]["score_effect"],
                "none",
            )

    def test_no_gap_creates_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = persist_session_coverage_feedback_event(
                tmp,
                {
                    "ok": True,
                    "routing_mode": "SINGLE_TOPIC",
                    "primary_topic_ids": ["topic_a"],
                    "uncovered_demand_ids": [],
                },
                demands(),
            )

            self.assertIsNone(result)
            self.assertFalse(
                (
                    Path(tmp)
                    / COVERAGE_FEEDBACK_EVENT_FILENAME
                ).exists()
            )

    def test_ambiguous_creates_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = persist_session_coverage_feedback_event(
                tmp,
                {
                    "ok": True,
                    "routing_mode": "AMBIGUOUS",
                    "uncovered_demand_ids": ["D2"],
                },
                demands(),
            )
            self.assertIsNone(result)

    def test_persistence_failure_is_nonfatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(
                Path,
                "write_text",
                side_effect=OSError("disk full"),
            ):
                result = (
                    persist_session_coverage_feedback_event(
                        tmp,
                        {
                            "ok": True,
                            "routing_mode": "GENERAL",
                            "uncovered_demand_ids": ["D1"],
                        },
                        demands(),
                    )
                )

            self.assertIsNone(result)

    def test_same_session_replaces_not_appends(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = persist_session_coverage_feedback_event(
                tmp,
                {
                    "ok": True,
                    "routing_mode": "GENERAL",
                    "uncovered_demand_ids": ["D1"],
                },
                demands(),
            )
            second = persist_session_coverage_feedback_event(
                tmp,
                {
                    "ok": True,
                    "routing_mode": "GENERAL",
                    "uncovered_demand_ids": ["D2"],
                },
                demands(),
            )

            self.assertIsNotNone(first)
            self.assertIsNotNone(second)

            payload = json.loads(
                (
                    Path(tmp)
                    / COVERAGE_FEEDBACK_EVENT_FILENAME
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(
                payload["uncovered_demand_ids"],
                ["D2"],
            )


if __name__ == "__main__":
    unittest.main()
