from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from coverage_feedback_retention import (
    COVERAGE_FEEDBACK_EVENT_FILENAME,
    apply_coverage_retention_plan,
    build_coverage_retention_plan,
)


NOW = 2_000_000_000.0


def _write_session(
    root: Path,
    session_id: str,
    *,
    age_days: int,
):
    session = root / session_id
    session.mkdir(parents=True)

    coverage = session / COVERAGE_FEEDBACK_EVENT_FILENAME
    coverage.write_text(
        json.dumps({"event_type": "TOPIC_COVERAGE_GAP"}),
        encoding="utf-8",
    )

    # Protected unrelated artifacts.
    (session / "grade.json").write_text(
        '{"score": 17}',
        encoding="utf-8",
    )
    (session / "semantic_router_shadow.json").write_text(
        '{"ok": true}',
        encoding="utf-8",
    )

    mtime = NOW - (age_days * 86400.0)
    os.utime(coverage, (mtime, mtime))
    return session, coverage


class CoverageFeedbackRetentionTest(unittest.TestCase):
    def test_plan_selects_only_old_coverage_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, old = _write_session(
                root,
                "old",
                age_days=120,
            )
            _, new = _write_session(
                root,
                "new",
                age_days=10,
            )

            plan = build_coverage_retention_plan(
                root,
                max_age_days=90,
                now_epoch=NOW,
            )

            self.assertEqual(plan["candidate_count"], 1)
            self.assertEqual(
                plan["candidates"][0]["path"],
                str(old),
            )
            self.assertEqual(plan["retained_count"], 1)
            self.assertTrue(new.is_file())

    def test_default_apply_is_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, old = _write_session(
                root,
                "old",
                age_days=120,
            )

            plan = build_coverage_retention_plan(
                root,
                max_age_days=90,
                now_epoch=NOW,
            )
            result = apply_coverage_retention_plan(
                plan
            )

            self.assertFalse(result["apply"])
            self.assertEqual(
                result["deleted_count"],
                0,
            )
            self.assertTrue(old.is_file())

    def test_explicit_apply_deletes_only_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session, old = _write_session(
                root,
                "old",
                age_days=120,
            )

            plan = build_coverage_retention_plan(
                root,
                max_age_days=90,
                now_epoch=NOW,
            )
            result = apply_coverage_retention_plan(
                plan,
                apply=True,
            )

            self.assertEqual(
                result["deleted_count"],
                1,
            )
            self.assertFalse(old.exists())
            self.assertTrue(
                (session / "grade.json").is_file()
            )
            self.assertTrue(
                (
                    session
                    / "semantic_router_shadow.json"
                ).is_file()
            )
            self.assertTrue(session.is_dir())

    def test_malicious_plan_path_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            protected = root / "grade.json"
            protected.write_text(
                '{"score": 17}',
                encoding="utf-8",
            )

            result = apply_coverage_retention_plan(
                {
                    "candidates": [
                        {"path": str(protected)}
                    ]
                },
                apply=True,
            )

            self.assertEqual(
                result["deleted_count"],
                0,
            )
            self.assertTrue(protected.is_file())

    def test_cli_without_apply_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, old = _write_session(
                root,
                "old",
                age_days=120,
            )

            before = old.read_bytes()

            subprocess.check_output(
                [
                    sys.executable,
                    "scripts/manage_coverage_feedback_retention.py",
                    "--sessions-root",
                    str(root),
                    "--max-age-days",
                    "1",
                ],
                text=True,
            )

            self.assertTrue(old.is_file())
            self.assertEqual(
                old.read_bytes(),
                before,
            )

    def test_grading_path_does_not_import_retention(self):
        text = Path("grading_agents.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn(
            "coverage_feedback_retention",
            text,
        )
        self.assertNotIn(
            "manage_coverage_feedback_retention",
            text,
        )


if __name__ == "__main__":
    unittest.main()
