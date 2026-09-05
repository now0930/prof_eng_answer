from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import topic_pack_workflow_controller as workflow
from scripts import validate_topic_pack_release as release


def _write_sources(pack_dir: Path, topic_id: str, title: str = "테스트 주제") -> None:
    pack_dir.mkdir(parents=True, exist_ok=True)
    (pack_dir / "README.md").write_text(f"# {title}\n", encoding="utf-8")
    for filename in workflow.REQUIRED_SOURCE_FILES[1:]:
        (pack_dir / filename).write_text(
            json.dumps({"topic_id": topic_id, "title": title}, ensure_ascii=False),
            encoding="utf-8",
        )


class TopicPackWorkflowControllerTest(unittest.TestCase):
    def test_human_docs_and_agent_instructions_name_managed_entrypoints(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for relative in [
            "README.md",
            "docs/topic_pack_workflow.md",
            "docs/rubric_authoring_guide.md",
            "scripts/README.md",
        ]:
            text = (root / relative).read_text(encoding="utf-8")
            self.assertIn("add-topic", text, relative)
            self.assertIn("approve-topic", text, relative)
        agent_text = (root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("docs/topic_pack_workflow.md", agent_text)
        self.assertIn("validate-topic-pack-release --all", agent_text)

    def test_add_topic_creates_managed_human_review_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "rubrics" / "topic_packs").mkdir(parents=True)
            sheet = root / "docs" / "topic_sheets" / "new_topic.md"
            sheet.parent.mkdir(parents=True)
            sheet.write_text("topic_id: new_topic\n핵심 사실\n", encoding="utf-8")

            def fake_create(args: argparse.Namespace) -> Path:
                pack = root / "rubrics" / "topic_packs" / args.topic_id
                _write_sources(pack, args.topic_id, args.title)
                return pack

            args = argparse.Namespace(
                topic_id="new_topic",
                title="새 주제",
                sheet=str(sheet),
                question_type="PRINCIPLE_INTERPRETATION",
                difficulty="THEORY_CORE",
                importance="HIGH",
                generate=False,
                model=None,
            )
            with mock.patch.object(workflow, "project_root", return_value=root):
                with mock.patch.object(workflow, "create_topic_pack", side_effect=fake_create):
                    self.assertEqual(workflow.add_topic(args), 0)

            status = json.loads(
                (root / "rubrics" / "topic_packs" / "new_topic" / "topic_status.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(status["workflow_contract"], workflow.WORKFLOW_CONTRACT)
            self.assertEqual(status["status"], "draft")
            self.assertEqual(status["review_state"], "human_review_required")
            self.assertEqual(status["content_hash"], "")

    def test_add_generation_failure_removes_only_new_managed_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = root / "rubrics" / "topic_packs"
            base.mkdir(parents=True)
            existing = base / "existing_topic"
            _write_sources(existing, "existing_topic")
            sheet = root / "sheet.md"
            sheet.write_text("topic_id: new_topic\n", encoding="utf-8")

            def fake_create(args: argparse.Namespace) -> Path:
                pack = base / args.topic_id
                _write_sources(pack, args.topic_id, args.title)
                return pack

            args = argparse.Namespace(
                topic_id="new_topic",
                title="새 주제",
                sheet=str(sheet),
                question_type="PRINCIPLE_INTERPRETATION",
                difficulty="THEORY_CORE",
                importance="HIGH",
                generate=True,
                model=None,
            )
            with mock.patch.object(workflow, "project_root", return_value=root):
                with mock.patch.object(workflow, "create_topic_pack", side_effect=fake_create):
                    with mock.patch.object(workflow, "_run", side_effect=SystemExit(2)):
                        with self.assertRaises(SystemExit):
                            workflow.add_topic(args)

            self.assertFalse((base / "new_topic").exists())
            self.assertTrue(existing.exists())

    def test_approve_records_reviewer_hash_and_runs_validation_then_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack = root / "rubrics" / "topic_packs" / "new_topic"
            _write_sources(pack, "new_topic")
            sheet = root / "docs" / "topic_sheets" / "new_topic.md"
            sheet.parent.mkdir(parents=True)
            sheet.write_text("topic_id: new_topic\n", encoding="utf-8")
            workflow._write_draft_status(root, "new_topic", sheet, generated=False)
            calls: list[list[str]] = []

            args = argparse.Namespace(
                topic_id="new_topic",
                reviewer="expert-01",
                smoke=False,
            )
            with mock.patch.object(workflow, "project_root", return_value=root):
                with mock.patch.object(
                    workflow,
                    "_run",
                    side_effect=lambda _root, command: calls.append(command),
                ):
                    self.assertEqual(workflow.approve_topic(args), 0)

            status = workflow.load_status(pack, "new_topic")
            self.assertEqual(status["status"], "approved")
            self.assertEqual(status["review_state"], "reviewed")
            self.assertEqual(status["reviewer"], "expert-01")
            self.assertEqual(status["content_hash"], status["_current_hash"])
            self.assertEqual(status["approved_source_hash"], status["_current_hash"])
            self.assertEqual(len(calls), 2)
            self.assertNotIn("--promote-generated", calls[0])
            self.assertIn("--promote-generated", calls[1])

    def test_source_change_invalidates_managed_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack = root / "rubrics" / "topic_packs" / "new_topic"
            _write_sources(pack, "new_topic")
            sheet = root / "sheet.md"
            sheet.write_text("topic_id: new_topic\n", encoding="utf-8")
            workflow._write_draft_status(root, "new_topic", sheet, generated=False)
            status = workflow.load_status(pack, "new_topic")
            status = workflow.update_status(
                status,
                set_status="approved",
                sync_hash=True,
                mark_reviewed=True,
            )
            status.update(
                {
                    "reviewer": "expert-01",
                    "approved_source_hash": status["content_hash"],
                }
            )
            workflow.write_status(pack, status)
            self.assertEqual(workflow.managed_approval_errors(root, "new_topic"), [])

            (pack / "fact_anchor.json").write_text(
                '{"topic_id":"new_topic","changed":true}\n',
                encoding="utf-8",
            )
            errors = workflow.managed_approval_errors(root, "new_topic")
            self.assertIn("approved content hash does not match current source", errors)
            self.assertIn("approved_source_hash does not match current source", errors)

    def test_failed_promotion_restores_draft_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack = root / "rubrics" / "topic_packs" / "new_topic"
            _write_sources(pack, "new_topic")
            sheet = root / "sheet.md"
            sheet.write_text("topic_id: new_topic\n", encoding="utf-8")
            workflow._write_draft_status(root, "new_topic", sheet, generated=False)
            before = (pack / "topic_status.json").read_bytes()
            calls = 0

            def fail_promotion(_root: Path, _command: list[str]) -> None:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise SystemExit(2)

            args = argparse.Namespace(
                topic_id="new_topic",
                reviewer="expert-01",
                smoke=False,
            )
            with mock.patch.object(workflow, "project_root", return_value=root):
                with mock.patch.object(workflow, "_run", side_effect=fail_promotion):
                    with self.assertRaises(SystemExit):
                        workflow.approve_topic(args)

            self.assertEqual((pack / "topic_status.json").read_bytes(), before)

    def test_integration_and_promotion_reject_unapproved_managed_topic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack = root / "rubrics" / "topic_packs" / "new_topic"
            _write_sources(pack, "new_topic")
            sheet = root / "sheet.md"
            sheet.write_text("topic_id: new_topic\n", encoding="utf-8")
            workflow._write_draft_status(root, "new_topic", sheet, generated=False)

            with self.assertRaises(SystemExit):
                release._require_managed_approval(root, ["new_topic"])

    def test_legacy_topic_without_workflow_contract_is_not_retroactively_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            pack = root / "rubrics" / "topic_packs" / "legacy_topic"
            _write_sources(pack, "legacy_topic")
            self.assertEqual(
                workflow.managed_approval_errors(root, "legacy_topic"),
                [],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
