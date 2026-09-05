from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import generate_topic_pack_from_sheet as generator
from scripts import smoke_topic_pack as smoke
from scripts import topic_review_llm
from scripts import topic_pack_tool
from scripts import validate_topic_pack_release as release


class TopicPackAuthoringWorkflowTest(unittest.TestCase):
    def test_rendered_prompts_are_topic_neutral(self) -> None:
        sheet = (
            "topic_id: ultrasonic_flow_meter_installation\n"
            "초음파 유량계의 직관부, 기포 및 설치 오차를 다룬다."
        )
        templates = {
            f"existing_{name}_json": json.dumps(
                {"topic_id": "ultrasonic_flow_meter_installation"},
                ensure_ascii=False,
            )
            for name in generator.TOPIC_PACK_SOURCE_FILENAMES
        }

        prompts = generator.render_prompts(sheet, templates=templates)

        self.assertNotIn("감쇠비", generator.GENERIC_SYSTEM_PROMPT)
        self.assertIn("실제로 있는 field", generator.GENERIC_SYSTEM_PROMPT)

        for name, prompt in prompts.items():
            self.assertIn("초음파 유량계", prompt, name)
            self.assertNotIn("ζ=1", prompt, name)
            self.assertNotIn("감쇠비", prompt, name)
            self.assertNotIn(
                "second_order_lag_response_by_damping_ratio",
                prompt,
                name,
            )

    def test_existing_reviewed_source_is_rejected_before_llm(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_id = "reviewed_topic"
            pack = root / "rubrics" / "topic_packs" / topic_id
            pack.mkdir(parents=True)
            sheet = root / "sheet.md"
            sheet.write_text(f"topic_id: {topic_id}\n", encoding="utf-8")
            for filename in generator.TOPIC_PACK_SOURCE_FILENAMES.values():
                (pack / filename).write_text(
                    json.dumps({"topic_id": topic_id}),
                    encoding="utf-8",
                )

            with mock.patch.object(generator, "project_root", return_value=root):
                with mock.patch.object(generator, "call_llm") as call_llm:
                    with self.assertRaises(SystemExit):
                        generator.main(
                            [
                                "--topic-id",
                                topic_id,
                                "--sheet",
                                str(sheet),
                            ]
                        )

            call_llm.assert_not_called()

    def test_candidate_mode_and_scaffold_promotion_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pack = Path(temporary)
            source = pack / "fact_anchor.json"
            source.write_text('{"note":"TODO"}\n', encoding="utf-8")

            self.assertEqual(
                generator.output_path(pack, "fact_anchor", False),
                source,
            )
            self.assertEqual(
                generator.output_path(
                    pack,
                    "fact_anchor",
                    False,
                    candidate_only=True,
                ),
                pack / "fact_anchor.candidate.json",
            )

    def test_generation_model_environment_has_precedence(self) -> None:
        environment = {
            "TOPIC_PACK_GENERATION_GEMINI_MODEL": "generation-model",
            "TOPIC_REVIEW_GEMINI_MODEL": "review-model",
            "GEMINI_MODEL": "global-model",
        }
        with mock.patch.dict(os.environ, environment, clear=True):
            settings = topic_review_llm.get_topic_review_llm_settings()
        self.assertEqual(settings.model, "generation-model")

    def test_logic_schema_variants_do_not_receive_foreign_rules(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pack = Path(temporary)
            existing = {
                "topic_id": "industrial_network_topic",
                "deterministic_checks": {
                    "fatal_checks": [
                        {
                            "id": "network_failure",
                            "condition": "network path is unavailable",
                        }
                    ]
                },
                "llm_profile": {"enabled": True},
            }
            (pack / "logic_check.json").write_text(
                json.dumps(existing),
                encoding="utf-8",
            )

            merged = generator.enforce_schema_lock(
                "logic_check",
                existing,
                pack,
            )

        text = json.dumps(merged, ensure_ascii=False)
        self.assertIn("network_failure", text)
        self.assertNotIn("zeta_one_as_overdamped", text)
        self.assertNotIn("de_claim_trust", text)

    def test_smoke_supports_object_question_and_outline_shapes(self) -> None:
        model_answer = {
            "expected_question_patterns": [
                {"pattern": "객체형 대표 문제"}
            ],
            "recommended_outline": [
                {"section": "정의"},
                {"intent": "현장 적용"},
            ],
        }
        self.assertEqual(
            smoke._question_from_model_answer(model_answer),
            "객체형 대표 문제",
        )
        self.assertEqual(
            smoke._outline_items(model_answer),
            ["정의", "현장 적용"],
        )

    def test_compiler_release_uses_fast_targeted_entrypoint(self) -> None:
        argv = topic_pack_tool._release_argv(
            Path("scripts/validate_topic_pack_release.py"),
            "new_topic",
        )
        self.assertEqual(
            argv[1:],
            [
                "scripts/validate_topic_pack_release.py",
                "--topic-id",
                "new_topic",
                "--promote-generated",
            ],
        )

    def test_failed_release_restores_generated_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_id = "new_topic"
            (root / "rubrics" / "topic_packs" / topic_id).mkdir(
                parents=True
            )
            generated = root / "rubrics" / "generated"
            generated.mkdir()
            artifact = generated / "bank.json"
            artifact.write_bytes(b"before")

            calls = 0

            def fake_run(_root: Path, _cmd: list[str], **_: object) -> int:
                nonlocal calls
                calls += 1
                if calls == 4:
                    artifact.write_bytes(b"after")
                    (generated / "temporary.json").write_bytes(b"temporary")
                    raise SystemExit(2)
                return 0

            with mock.patch.object(release, "project_root", return_value=root):
                with mock.patch.object(release, "_run", side_effect=fake_run):
                    with self.assertRaises(SystemExit):
                        release.main(
                            [
                                "--topic-id",
                                topic_id,
                                "--promote-generated",
                            ]
                        )

            self.assertEqual(artifact.read_bytes(), b"before")
            self.assertFalse((generated / "temporary.json").exists())

    def test_release_defaults_to_git_changed_topics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "rubrics" / "topic_packs" / "changed_topic").mkdir(
                parents=True
            )
            with mock.patch.object(
                release,
                "_git_changed_topic_ids",
                return_value=["changed_topic"],
            ):
                selected = release._topic_ids(root, None)
        self.assertEqual(selected, ["changed_topic"])

    def test_release_requires_explicit_all_when_nothing_changed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "rubrics" / "topic_packs").mkdir(parents=True)
            with mock.patch.object(
                release,
                "_git_changed_topic_ids",
                return_value=[],
            ):
                with self.assertRaises(SystemExit):
                    release._topic_ids(root, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
