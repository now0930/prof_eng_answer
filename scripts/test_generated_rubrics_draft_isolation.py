from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_generated_rubrics as builder
from scripts import topic_pack_workflow_controller as workflow
from scripts.topic_pack_status import load_status, update_status, write_status


def _write_pack(pack_dir: Path, topic_id: str) -> None:
    pack_dir.mkdir(parents=True)
    (pack_dir / "README.md").write_text(f"# {topic_id}\n", encoding="utf-8")
    for filename in workflow.REQUIRED_SOURCE_FILES[1:]:
        (pack_dir / filename).write_text(
            json.dumps({"topic_id": topic_id}), encoding="utf-8"
        )


def _approve_fixture(root: Path, pack_dir: Path, topic_id: str) -> None:
    sheet = root / "docs" / "topic_sheets" / f"{topic_id}.md"
    sheet.parent.mkdir(parents=True, exist_ok=True)
    sheet.write_text(f"topic_id: {topic_id}\n", encoding="utf-8")
    workflow._write_draft_status(root, topic_id, sheet, generated=False)
    status = load_status(pack_dir, topic_id)
    status = update_status(
        status, set_status="approved", sync_hash=True, mark_reviewed=True
    )
    status.update(
        {
            "reviewer": "fixture-reviewer",
            "approved_source_hash": status["_current_hash"],
        }
    )
    write_status(pack_dir, status)


class GeneratedRubricsDraftIsolationTest(unittest.TestCase):
    def test_draft_is_excluded_while_legacy_and_approved_packs_remain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = root / "rubrics" / "topic_packs"
            base.mkdir(parents=True)

            legacy = base / "legacy_topic"
            _write_pack(legacy, "legacy_topic")

            draft = base / "draft_topic"
            _write_pack(draft, "draft_topic")
            draft_sheet = root / "docs" / "topic_sheets" / "draft_topic.md"
            draft_sheet.parent.mkdir(parents=True, exist_ok=True)
            draft_sheet.write_text("topic_id: draft_topic\n", encoding="utf-8")
            workflow._write_draft_status(root, "draft_topic", draft_sheet, generated=False)

            approved = base / "approved_topic"
            _write_pack(approved, "approved_topic")
            _approve_fixture(root, approved, "approved_topic")

            eligible, skipped = builder.eligible_topic_pack_dirs(
                [approved, draft, legacy], root=root
            )

            self.assertEqual(
                [path.name for path in eligible],
                ["approved_topic", "legacy_topic"],
            )
            self.assertEqual(skipped, ["draft_topic"])

    def test_stale_approval_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack_dir = root / "rubrics" / "topic_packs" / "approved_topic"
            _write_pack(pack_dir, "approved_topic")
            _approve_fixture(root, pack_dir, "approved_topic")
            (pack_dir / "fact_anchor.json").write_text(
                '{"topic_id":"approved_topic","changed":true}\n',
                encoding="utf-8",
            )

            with self.assertRaises(SystemExit):
                builder.eligible_topic_pack_dirs([pack_dir], root=root)

    def test_unknown_managed_status_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack_dir = root / "rubrics" / "topic_packs" / "unknown_topic"
            _write_pack(pack_dir, "unknown_topic")
            status = {
                "topic_id": "unknown_topic",
                "workflow_contract": workflow.WORKFLOW_CONTRACT,
                "status": "mystery",
            }
            (pack_dir / "topic_status.json").write_text(
                json.dumps(status), encoding="utf-8"
            )

            with self.assertRaises(SystemExit):
                builder.eligible_topic_pack_dirs([pack_dir], root=root)


if __name__ == "__main__":
    unittest.main()
