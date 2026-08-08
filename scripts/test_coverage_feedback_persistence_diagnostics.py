from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import coverage_feedback_persistence as cfp


def _demands() -> dict:
    return {
        "ok": True,
        "demands": [
            {
                "id": "D1",
                "demand_id": "D1",
                "text": "민감한 질문 텍스트 SHOULD_NOT_LOG",
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


class CoverageFeedbackPersistenceDiagnosticsTest(
    unittest.TestCase
):
    def test_failure_is_nonfatal_and_warns_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(
                Path,
                "write_text",
                side_effect=OSError(
                    "SECRET_EXCEPTION_DETAIL"
                ),
            ), patch.object(
                cfp._LOG,
                "warning",
            ) as warning:
                result = (
                    cfp.persist_session_coverage_feedback_event(
                        tmp,
                        _semantic(),
                        _demands(),
                    )
                )

        self.assertIsNone(result)
        warning.assert_called_once()

        args = warning.call_args.args
        self.assertEqual(
            args[0],
            "coverage_feedback_persistence_failed "
            "exception_type=%s",
        )
        self.assertEqual(args[1], "OSError")

        rendered = " ".join(
            str(value)
            for value in (
                list(warning.call_args.args)
                + list(
                    warning.call_args.kwargs.values()
                )
            )
        )
        self.assertNotIn(
            "SHOULD_NOT_LOG",
            rendered,
        )
        self.assertNotIn(
            "SECRET_EXCEPTION_DETAIL",
            rendered,
        )
        self.assertNotIn(
            str(tmp),
            rendered,
        )

    def test_success_path_is_quiet(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(
                cfp._LOG,
                "warning",
            ) as warning:
                result = (
                    cfp.persist_session_coverage_feedback_event(
                        tmp,
                        _semantic(),
                        _demands(),
                    )
                )

            self.assertIsNotNone(result)
            warning.assert_not_called()
            self.assertTrue(
                (
                    Path(tmp)
                    / cfp.COVERAGE_FEEDBACK_EVENT_FILENAME
                ).is_file()
            )

    def test_diagnostic_has_no_retry_or_network(self):
        source = Path(
            "coverage_feedback_persistence.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("requests.", source)
        self.assertNotIn("urllib", source)
        self.assertNotIn("retry", source.lower())
        self.assertNotIn("answer_text", source)
        self.assertNotIn("question_text", source)
        self.assertIn(
            "coverage_feedback_persistence_failed",
            source,
        )


if __name__ == "__main__":
    unittest.main()
