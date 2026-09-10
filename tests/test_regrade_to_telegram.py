import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from scripts.regrade_to_telegram import (
    build_copyable_submission,
    answer_content_hash,
    completed_sources,
    create_regrade_session,
    current_commit,
    deduplicate_sources,
    eligible_source_sessions,
    grade_signature,
    latest_source_session,
    read_session_input,
    resolve_source_session,
)


class RegradeToTelegramTests(unittest.TestCase):
    def test_duplicate_answers_are_graded_only_once(self):
        sources = [
            ("session_1", "동일  답안\n내용", None),
            ("session_2", "동일 답안 내용", None),
            ("session_3", "다른 답안", None),
        ]

        def normalize(value):
            return {"normalized_text": value}

        unique, duplicates = deduplicate_sources(sources, normalize)
        self.assertEqual([row[0] for row in unique], ["session_1", "session_3"])
        self.assertEqual(duplicates[0]["source"], "session_2")
        self.assertEqual(duplicates[0]["duplicate_of"], "session_1")
        self.assertEqual(duplicates[0]["status"], "SKIPPED_DUPLICATE")
        self.assertEqual(
            duplicates[0]["content_sha256"],
            answer_content_hash("동일 답안 내용"),
        )

    def test_commit_identity_works_without_git_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "engine.py").write_text("VERSION = 1\n", encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True), mock.patch(
                "scripts.regrade_to_telegram.subprocess.run",
                side_effect=subprocess.CalledProcessError(128, "git"),
            ):
                first = current_commit(root)
                self.assertTrue(first.startswith("sha256:"))
                self.assertEqual(first, current_commit(root))
                (root / "engine.py").write_text("VERSION = 2\n", encoding="utf-8")
                self.assertNotEqual(first, current_commit(root))

    def test_configured_commit_has_precedence(self):
        with mock.patch.dict("os.environ", {"ENGINE_COMMIT": "deploy-123"}):
            self.assertEqual(current_commit(Path("/missing")), "deploy-123")

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

    def test_all_selection_and_commit_scoped_resume(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "20260910_120000_123"
            source.mkdir()
            (source / "input.raw.txt").write_text("answer", encoding="utf-8")
            (source / "meta.json").write_text(
                '{"status":"graded","chat_id":123}', encoding="utf-8"
            )
            draft = root / "20260910_120100_123"
            draft.mkdir()
            (draft / "input.txt").write_text("draft", encoding="utf-8")
            (draft / "meta.json").write_text(
                '{"status":"created","chat_id":123}', encoding="utf-8"
            )
            regrade = root / "regrade_20260910_123"
            regrade.mkdir()
            (regrade / "meta.json").write_text(
                '{"status":"graded","provider_calls":0,'
                '"engine_commit":"abc","regrade_source":"20260910_120000_123",'
                '"dry_run":true}',
                encoding="utf-8",
            )
            self.assertEqual(eligible_source_sessions(root), [source])
            self.assertEqual(
                completed_sources(root, "abc"), {"20260910_120000_123"}
            )
            self.assertEqual(
                completed_sources(root, "abc", include_dry_runs=False), set()
            )
            self.assertEqual(completed_sources(root, "def"), set())

    def test_changed_only_signature_uses_score_pass_and_fatal(self):
        base = {
            "total_score": 12.0,
            "official_pass_met": False,
            "high_score_met": False,
            "logic_check_evaluation": {"findings": []},
        }
        same = dict(base)
        changed = dict(base, total_score=13.0)
        self.assertEqual(grade_signature(base), grade_signature(same))
        self.assertNotEqual(grade_signature(base), grade_signature(changed))


if __name__ == "__main__":
    unittest.main()
