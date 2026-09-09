import tempfile
import unittest
from pathlib import Path

from scripts.regrade_to_telegram import (
    build_copyable_submission,
    create_regrade_session,
    latest_source_session,
    read_session_input,
    resolve_source_session,
)


class RegradeToTelegramTests(unittest.TestCase):
    def test_copyable_submission_has_grade_and_end_markers(self):
        rendered = build_copyable_submission("문제: 시험\n답안: 내용")
        self.assertEqual(
            rendered,
            "[재채점 원문 — 복사용]\n/grade\n문제: 시험\n답안: 내용\n끝.",
        )

    def test_resolves_only_safe_session_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = root / "20260910_120000_123"
            session.mkdir()
            self.assertEqual(
                resolve_source_session(root, session.name), session,
            )
            with self.assertRaises(ValueError):
                resolve_source_session(root, "../outside")

    def test_latest_ignores_regrade_sessions_and_prefers_raw_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "ordinary_old"
            old.mkdir()
            (old / "input.txt").write_text("old", encoding="utf-8")
            newest = root / "ordinary_new"
            newest.mkdir()
            (newest / "input.raw.txt").write_text("raw", encoding="utf-8")
            regrade = root / "regrade_20990101_1"
            regrade.mkdir()
            (regrade / "input.raw.txt").write_text("ignore", encoding="utf-8")
            self.assertEqual(latest_source_session(root), newest)
            self.assertEqual(read_session_input(newest), "raw")

    def test_regrade_session_is_collision_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = create_regrade_session(root, "-123")
            second = create_regrade_session(root, "-123")
            self.assertNotEqual(first, second)
            self.assertTrue(first.is_dir())
            self.assertTrue(second.is_dir())


if __name__ == "__main__":
    unittest.main()
