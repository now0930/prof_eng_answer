from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.topic_pack_contract import load_profile
from scripts.topic_pack_tool import (
    SOURCE_FILES,
    _atomic_install,
    build_spec,
    create_parser,
    plan_spec,
    release_topic,
    render_topic,
    validate_rendered_topic,
    _resolve_projection_targets,
)


class TopicPackToolTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load_profile(
            "implementation_evaluation_v1"
        )

    def make_spec(self) -> dict:
        return {
            "$schema": "../../schemas/topic_pack_spec.schema.json",
            "schema_version": "topic-spec-v1",
            "profile_id": "implementation_evaluation_v1",
            "topic_id": "compiler_managed_acceptance_topic",
            "title_ko": "컴파일러 관리 승인 토픽",
            "question_type": "IMPLEMENTATION_EVALUATION",
            "difficulty": "HIGH",
            "selection_importance": "HIGH",
            "scope_summary": (
                "Topic Pack compiler의 plan과 build를 검증한다."
            ),
            "ownership_statements": [
                {
                    "kind": "OWNED",
                    "statement": "기술 내용과 경계를 소유한다.",
                },
                {
                    "kind": "EXCLUDED",
                    "statement": "파일 구조는 compiler가 소유한다.",
                },
            ],
            "counts": {
                "anchors": 2,
                "fatal_wrong_claims": 1,
                "major_checks": 1,
                "question_patterns": 1,
                "recommended_outline": 1,
                "routing_aliases": 2,
                "high_band_unlock_conditions": 1,
                "revision_notes": 1,
            },
            "anchors": [
                {
                    "id": "definition",
                    "title": "정의",
                    "content": "컴파일러 관리 경계를 정의한다.",
                    "keywords": ["컴파일러", "경계"],
                    "importance": "core",
                },
                {
                    "id": "application",
                    "title": "적용",
                    "content": "plan과 build 적용 방법을 설명한다.",
                    "keywords": ["plan", "build"],
                    "importance": "core",
                },
            ],
            "fatal_wrong_claims": [
                {
                    "id": "fatal_manual_structure",
                    "claim": "LLM이 파일 구조를 임의로 만든다.",
                    "correct_rule": "고정 compiler가 구조를 생성한다.",
                    "rationale": "구조 추정 오류를 방지한다.",
                    "keywords": ["구조", "compiler"],
                }
            ],
            "major_checks": [
                {
                    "id": "major_atomic_install",
                    "check": "atomic install을 적용했는가.",
                    "expected": "신규 디렉터리만 원자적으로 설치한다.",
                    "rationale": "부분 설치를 방지한다.",
                    "keywords": ["atomic", "rollback"],
                }
            ],
            "question_patterns": [
                {
                    "id": "pattern_explain_build",
                    "pattern": "plan과 build 절차를 설명하라.",
                    "required_anchor_ids": [
                        "definition",
                        "application",
                    ],
                }
            ],
            "recommended_outline": [
                {
                    "section": "정의와 적용",
                    "purpose": "구조와 실행 경계를 설명한다.",
                    "anchor_ids": [
                        "definition",
                        "application",
                    ],
                }
            ],
            "routing_aliases": [
                "compiler managed acceptance topic",
                "topic pack build acceptance",
            ],
            "high_band_unlock_conditions": [
                "rollback 경계를 명확히 설명한다."
            ],
            "revision_notes": [
                "Stage 17D generic acceptance fixture"
            ],
            "handoffs": [
                {
                    "topic_id": "existing_handoff_topic",
                    "trigger": "인접 세부 범위가 필요할 때",
                    "scope": "인접 세부만 이관한다.",
                }
            ],
            "standards_and_sources": [],

            "expected_question_patterns": [{"pattern": "Topic Pack plan 계약을 설명하라.", "intent": "Topic Pack plan의 입력 계약, projection 결과, 검증 및 rollback 경계를 설명한다."}],
            "high_score_points": ["핵심 채점 포인트를 구조, 검증, 운영 경계와 함께 설명한다."],}

    def make_topic_root(self, root: Path) -> Path:
        topic_root = root / "rubrics" / "topic_packs"
        (
            topic_root / "existing_handoff_topic"
        ).mkdir(parents=True)
        return topic_root

    def git(
        self,
        root: Path,
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )

    def write_source_topic(
        self,
        topic_dir: Path,
    ) -> None:
        topic_dir.mkdir(parents=True, exist_ok=True)
        for file_name in SOURCE_FILES:
            payload = (
                "{}\n"
                if file_name.endswith(".json")
                else "# Test Topic\n"
            )
            (topic_dir / file_name).write_text(
                payload,
                encoding="utf-8",
            )

    def make_release_repo(
        self,
        root: Path,
    ) -> tuple[Path, Path, Path, Path]:
        (root / "scripts").mkdir(parents=True)
        entrypoint = root / "scripts" / "validate_release.sh"
        entrypoint.write_text(
            "#!/usr/bin/env bash\nexit 0\n",
            encoding="utf-8",
        )

        reports = root / "reports"
        reports.mkdir()
        report_file = reports / "state.txt"
        report_file.write_text(
            "before\n",
            encoding="utf-8",
        )

        legacy_topic = (
            root
            / "rubrics"
            / "topic_packs"
            / "legacy_topic"
        )
        self.write_source_topic(legacy_topic)

        self.git(root, "init", "-q")
        self.git(
            root,
            "config",
            "user.email",
            "topic-pack-test@example.invalid",
        )
        self.git(
            root,
            "config",
            "user.name",
            "Topic Pack Test",
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "baseline")

        target_topic = (
            root
            / "rubrics"
            / "topic_packs"
            / "new_compiler_topic"
        )
        self.write_source_topic(target_topic)
        return entrypoint, report_file, legacy_topic, target_topic

    @staticmethod
    def issue_codes(result: dict) -> set[str]:
        return {
            str(issue["error_code"])
            for issue in result["issues"]
        }

    def test_parser_has_plan_build_and_release(self) -> None:
        parser = create_parser()
        plan = parser.parse_args(
            ["plan", "--spec", "example.json"]
        )
        build = parser.parse_args(
            ["build", "--spec", "example.json"]
        )
        release = parser.parse_args(
            ["release", "--topic", "new_topic"]
        )
        self.assertEqual(plan.command, "plan")
        self.assertEqual(build.command, "build")
        self.assertEqual(release.command, "release")
        self.assertEqual(release.topic, "new_topic")
        self.assertFalse(build.install)

    def test_plan_is_read_only_and_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_root = self.make_topic_root(root)
            before = sorted(
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
            )
            result = plan_spec(
                self.make_spec(),
                self.profile,
                topic_root=topic_root,
            )
            after = sorted(
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
            )
        self.assertEqual(result["result"], "PASS")
        self.assertFalse(result["repository_mutation"])
        self.assertEqual(before, after)

    def test_plan_rejects_topic_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_root = self.make_topic_root(root)
            (
                topic_root
                / self.make_spec()["topic_id"]
            ).mkdir()
            result = plan_spec(
                self.make_spec(),
                self.profile,
                topic_root=topic_root,
            )
        self.assertEqual(result["result"], "FAIL")
        self.assertIn(
            "TP003_TOPIC_ID_COLLISION",
            {
                issue["error_code"]
                for issue in result["issues"]
            },
        )

    def test_renderer_emits_exact_five_files(self) -> None:
        rendered = render_topic(
            self.make_spec(),
            self.profile,
        )
        self.assertEqual(tuple(rendered), SOURCE_FILES)
        self.assertNotIn(
            "source_topic",
            "\n".join(rendered.values()),
        )
        self.assertNotIn(
            "donor_topic",
            "\n".join(rendered.values()),
        )

    def test_build_stages_and_validates_without_install(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_root = self.make_topic_root(root)
            output_root = root / "output"
            result = build_spec(
                self.make_spec(),
                self.profile,
                output_root=output_root,
                topic_root=topic_root,
                install=False,
            )
            staged = output_root / self.make_spec()["topic_id"]
            issues = validate_rendered_topic(
                staged,
                self.profile,
            )
            target_exists = (
                topic_root / self.make_spec()["topic_id"]
            ).exists()

        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["rendered_file_count"], 5)
        self.assertFalse(result["installed"])
        self.assertFalse(target_exists)
        self.assertEqual(issues, [])

    def test_build_atomically_installs_new_topic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            topic_root = self.make_topic_root(root)
            output_root = root / "output"
            result = build_spec(
                self.make_spec(),
                self.profile,
                output_root=output_root,
                topic_root=topic_root,
                install=True,
            )
            target = topic_root / self.make_spec()["topic_id"]
            installed_files = sorted(
                path.name
                for path in target.iterdir()
                if path.is_file()
            )

        self.assertEqual(result["result"], "PASS")
        self.assertTrue(result["installed"])
        self.assertEqual(installed_files, sorted(SOURCE_FILES))

    def test_atomic_install_rolls_back_after_injected_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            staged = root / "staged"
            staged.mkdir()
            for name in SOURCE_FILES:
                (staged / name).write_text(
                    "{}\n" if name.endswith(".json") else "# Test\n",
                    encoding="utf-8",
                )
            target_root = root / "topics"
            target_root.mkdir()
            target = target_root / "rollback_topic"

            with self.assertRaises(RuntimeError):
                _atomic_install(
                    staged,
                    target,
                    fail_after_rename=True,
                )

            residues = [
                path.name
                for path in target_root.iterdir()
            ]

        self.assertFalse(target.exists())
        self.assertEqual(residues, [])

    def test_actual_projection_modes_and_targets(
        self,
    ) -> None:
        projections = self.profile["projections"]
        self.assertEqual(
            {
                item["projection_mode"]
                for item in projections
            },
            {
                "EXACT",
                "PROFILE",
                "PROFILE_SCHEMA",
                "RENDERED",
                "FIXED",
                "VALIDATION_ONLY",
            },
        )

        resolved_projection_count = 0
        validation_only_count = 0
        for projection in projections:
            targets = _resolve_projection_targets(
                projection["target"],
                self.profile,
            )
            self.assertTrue(targets)
            resolved_projection_count += 1
            validation_only_count += sum(
                target["kind"]
                == "VALIDATION_ONLY"
                for target in targets
            )

        self.assertEqual(
            resolved_projection_count,
            18,
        )
        self.assertEqual(
            validation_only_count,
            1,
        )

    def test_routing_and_question_type_projection(
        self,
    ) -> None:
        spec = self.make_spec()
        rendered = render_topic(
            spec,
            self.profile,
        )
        model_answer = json.loads(
            rendered["model_answer.json"]
        )
        topic_importance = json.loads(
            rendered["topic_importance.json"]
        )

        self.assertEqual(
            model_answer["question_type"],
            spec["question_type"],
        )
        self.assertEqual(
            topic_importance["question_type"],
            spec["question_type"],
        )

        routing_aliases = model_answer[
            "routing_aliases"
        ]
        self.assertIn(
            spec["routing_aliases"][0],
            routing_aliases,
        )
        self.assertTrue(
            any(
                spec["handoffs"][0]["topic_id"]
                in value
                for value in routing_aliases
                if isinstance(value, str)
            )
        )

    def test_rendered_json_uses_real_newline(
        self,
    ) -> None:
        rendered = render_topic(
            self.make_spec(),
            self.profile,
        )
        for file_name in (
            "fact_anchor.json",
            "logic_check.json",
            "model_answer.json",
            "topic_importance.json",
        ):
            payload = rendered[file_name]
            self.assertTrue(
                payload.endswith("\n"),
                file_name,
            )
            self.assertFalse(
                payload.endswith(r"\n"),
                file_name,
            )
            self.assertEqual(
                payload.encode("utf-8")[-1:],
                bytes([10]),
                file_name,
            )
            json.loads(payload)

    def test_release_rejects_invalid_topic_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_release_repo(root)
            result = release_topic(
                "Invalid-Topic",
                repo_root=root,
            )

        self.assertEqual(result["result"], "FAIL")
        self.assertIn(
            "TP015_RELEASE_VALIDATION_FAILED",
            self.issue_codes(result),
        )
        self.assertFalse(result["repository_mutation"])

    def test_release_rejects_missing_and_incomplete_source(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, _, _, target = (
                self.make_release_repo(root)
            )
            missing = release_topic(
                "missing_topic",
                repo_root=root,
                release_entrypoint=entrypoint,
            )
            (target / "README.md").unlink()
            incomplete = release_topic(
                target.name,
                repo_root=root,
                release_entrypoint=entrypoint,
            )

        self.assertIn(
            "TP015_RELEASE_VALIDATION_FAILED",
            self.issue_codes(missing),
        )
        self.assertIn(
            "TP015_RELEASE_VALIDATION_FAILED",
            self.issue_codes(incomplete),
        )

    def test_release_rejects_tracked_legacy_topic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, _, legacy, _ = (
                self.make_release_repo(root)
            )
            result = release_topic(
                legacy.name,
                repo_root=root,
                release_entrypoint=entrypoint,
            )

        self.assertIn(
            "TP016_LEGACY_MUTATION_FORBIDDEN",
            self.issue_codes(result),
        )
        self.assertFalse(result["repository_mutation"])

    def test_release_success_uses_topic_id_entrypoint_option(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, report_file, _, target = (
                self.make_release_repo(root)
            )

            def runner(argv: list[str], **_: object):
                self.assertEqual(
                    argv,
                    [
                        "bash",
                        entrypoint.as_posix(),
                        "--topic-id",
                        target.name,
                    ],
                )
                report_file.write_text(
                    "after\n",
                    encoding="utf-8",
                )
                docs = root / "docs"
                docs.mkdir()
                (docs / "new.json").write_text(
                    "{}\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(
                    argv,
                    0,
                    "RESULT=PASS\n",
                )

            result = release_topic(
                target.name,
                repo_root=root,
                release_entrypoint=entrypoint,
                runner=runner,
            )

            self.assertEqual(result["result"], "PASS")
            self.assertTrue(result["repository_mutation"])
            self.assertEqual(
                result["adapter_topic_option"],
                "--topic",
            )
            self.assertEqual(
                result["entrypoint_topic_option"],
                "--topic-id",
            )
            self.assertTrue(target.exists())
            self.assertEqual(
                report_file.read_text(encoding="utf-8"),
                "after\n",
            )
            self.assertTrue((root / "docs" / "new.json").is_file())

    def test_release_failure_restores_tracked_and_untracked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, report_file, _, target = (
                self.make_release_repo(root)
            )

            def runner(argv: list[str], **_: object):
                report_file.write_text(
                    "after\n",
                    encoding="utf-8",
                )
                docs = root / "docs"
                docs.mkdir()
                (docs / "new.json").write_text(
                    "{}\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(
                    argv,
                    2,
                    "release validation failed\n",
                )

            result = release_topic(
                target.name,
                repo_root=root,
                release_entrypoint=entrypoint,
                runner=runner,
            )

            self.assertEqual(result["result"], "FAIL")
            self.assertIn(
                "TP015_RELEASE_VALIDATION_FAILED",
                self.issue_codes(result),
            )
            self.assertTrue(result["rollback_performed"])
            self.assertTrue(result["rollback_pass"])
            self.assertFalse(result["repository_mutation"])
            self.assertFalse(target.exists())
            self.assertFalse((root / "docs" / "new.json").exists())
            self.assertEqual(
                report_file.read_text(encoding="utf-8"),
                "before\n",
            )

    def test_release_classifies_generated_and_projection_failures(
        self,
    ) -> None:
        for output, expected_code in (
            (
                "generated rebuild failed\n",
                "TP013_GENERATED_REBUILD_FAILED",
            ),
            (
                "projection mismatch\n",
                "TP014_PROJECTION_MISMATCH",
            ),
        ):
            with self.subTest(expected_code=expected_code):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    entrypoint, _, _, target = (
                        self.make_release_repo(root)
                    )

                    def runner(
                        argv: list[str],
                        **_: object,
                    ):
                        return subprocess.CompletedProcess(
                            argv,
                            2,
                            output,
                        )

                    result = release_topic(
                        target.name,
                        repo_root=root,
                        release_entrypoint=entrypoint,
                        runner=runner,
                    )

                    self.assertIn(
                        expected_code,
                        self.issue_codes(result),
                    )
                    self.assertTrue(result["rollback_pass"])
                    self.assertFalse(target.exists())

    def test_release_rolls_back_legacy_topic_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, _, legacy, target = (
                self.make_release_repo(root)
            )
            legacy_readme = legacy / "README.md"
            before = legacy_readme.read_bytes()

            def runner(argv: list[str], **_: object):
                legacy_readme.write_text(
                    "# Mutated\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(
                    argv,
                    0,
                    "RESULT=PASS\n",
                )

            result = release_topic(
                target.name,
                repo_root=root,
                release_entrypoint=entrypoint,
                runner=runner,
            )

            self.assertIn(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                self.issue_codes(result),
            )
            self.assertTrue(result["rollback_pass"])
            self.assertEqual(legacy_readme.read_bytes(), before)
            self.assertFalse(target.exists())

    def test_release_reports_rollback_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            entrypoint, report_file, _, target = (
                self.make_release_repo(root)
            )

            def runner(argv: list[str], **_: object):
                report_file.write_text(
                    "after\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(
                    argv,
                    2,
                    "release validation failed\n",
                )

            result = release_topic(
                target.name,
                repo_root=root,
                release_entrypoint=entrypoint,
                runner=runner,
                fail_rollback=True,
            )

            self.assertEqual(result["result"], "FAIL")
            self.assertIn(
                "TP016_LEGACY_MUTATION_FORBIDDEN",
                self.issue_codes(result),
            )
            self.assertFalse(result["rollback_pass"])
            self.assertEqual(
                result["repository_mutation"],
                "ROLLBACK_FAILED",
            )

    def test_fixed_projection_is_profile_owned(self) -> None:
        projections = self.profile["projections"]
        fixed = [
            item
            for item in projections
            if item["projection_mode"] == "FIXED"
        ]
        self.assertEqual(len(fixed), 1)
        self.assertEqual(
            fixed[0]["spec_field"],
            "finding_fields",
        )
        self.assertIn(
            "finding_fields",
            self.profile["fixed_values"],
        )
        self.assertNotIn(
            "finding_fields",
            self.make_spec(),
        )


# STAGE17C4_IMPORTANCE_TOOL_TESTS_V1
import json as _stage17c4_json
import subprocess as _stage17c4_subprocess
import sys as _stage17c4_sys
import tempfile as _stage17c4_tempfile
import unittest as _stage17c4_unittest
from pathlib import Path as _Stage17C4Path


class Stage17C4ImportanceToolTests(_stage17c4_unittest.TestCase):
    _allowed = ("core", "must", "important")
    _base_spec_json = '{"$schema":"../../schemas/topic_pack_spec.schema.json","schema_version":"topic-spec-v1","profile_id":"implementation_evaluation_v1","topic_id":"stage17d2_plan_acceptance_topic","title_ko":"Stage 17D-2 Plan 읽기 전용 승인 토픽","question_type":"IMPLEMENTATION_EVALUATION","difficulty":"HIGH","selection_importance":"HIGH","scope_summary":"Topic Pack compiler의 plan 명령이 저장소를 변경하지 않고 계약을 검증하는지 확인한다.","ownership_statements":[{"kind":"OWNED","statement":"기술 내용과 Topic 경계를 소유한다."},{"kind":"EXCLUDED","statement":"파일 구조와 설치는 compiler가 소유한다."}],"counts":{"anchors":2,"fatal_wrong_claims":1,"major_checks":1,"question_patterns":1,"recommended_outline":1,"routing_aliases":2,"high_band_unlock_conditions":1,"revision_notes":1},"anchors":[{"id":"plan_definition","title":"Plan 정의","content":"Plan은 Spec을 검증하고 계획 경로를 산출한다.","keywords":["plan","검증"],"importance":"core"},{"id":"readonly_boundary","title":"읽기 전용 경계","content":"Plan은 저장소 파일을 생성하거나 수정하지 않는다.","keywords":["read-only","mutation"],"importance":"core"}],"fatal_wrong_claims":[{"id":"fatal_plan_mutates_repository","claim":"Plan 단계가 Topic Pack 파일을 설치한다.","correct_rule":"Plan 단계는 저장소를 변경하지 않는다.","rationale":"검증과 mutation 경계를 분리해야 한다.","keywords":["plan","repository mutation"]}],"major_checks":[{"id":"major_structured_issue","check":"오류가 구조화된 issue로 반환되는가.","expected":"error_code, path, message를 반환한다.","rationale":"실패 원인을 자동 처리할 수 있어야 한다.","keywords":["structured error","issue"]}],"question_patterns":[{"id":"pattern_plan_contract","pattern":"Topic Pack plan 계약을 설명하라.","required_anchor_ids":["plan_definition","readonly_boundary"]}],"recommended_outline":[{"section":"Plan과 읽기 전용 경계","purpose":"검증·계획·mutation 금지를 설명한다.","anchor_ids":["plan_definition","readonly_boundary"]}],"routing_aliases":["stage17d2 plan readonly acceptance","stage17d2 topic pack planning contract"],"high_band_unlock_conditions":["정상·오류 Spec 모두에서 저장소 무변경을 입증한다."],"revision_notes":["Stage 17D-2 plan read-only acceptance fixture"],"handoffs":[{"topic_id":"bode_frequency_response_stability_margin_bandwidth","trigger":"기존 Topic의 상세 기술 내용이 필요할 때","scope":"기존 Topic의 세부 내용만 이관한다."}],"standards_and_sources":[]}'

    def _run_tool(self, command, spec, output_root=None):
        root = _Stage17C4Path(__file__).resolve().parents[1]
        with _stage17c4_tempfile.TemporaryDirectory() as temp_dir:
            spec_path = _Stage17C4Path(temp_dir) / "spec.json"
            spec_path.write_text(
                _stage17c4_json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            argv = [
                _stage17c4_sys.executable,
                "-B",
                str(root / "scripts/topic_pack_tool.py"),
                command,
                "--spec",
                str(spec_path),
            ]
            if output_root is not None:
                argv.extend(["--output-root", str(output_root)])
            argv.append("--json")
            completed = _stage17c4_subprocess.run(
                argv,
                cwd=root,
                text=True,
                stdout=_stage17c4_subprocess.PIPE,
                stderr=_stage17c4_subprocess.STDOUT,
                check=False,
            )
            payload = _stage17c4_json.loads(completed.stdout)
            return completed.returncode, payload

    def _base_spec(self):
        return _stage17c4_json.loads(self._base_spec_json)

    @staticmethod
    def _isolate_identity(spec, case):
        topic_id = f"stage17c4_importance_{case}_topic"
        spec["topic_id"] = topic_id
        alias_count = len(spec.get("routing_aliases", []))
        spec["routing_aliases"] = [
            f"{topic_id}_alias_{index + 1}"
            for index in range(alias_count)
        ]
        return spec

    def test_allowed_importance_values_plan_build_and_project(self):
        for value in self._allowed:
            with self.subTest(value=value):
                spec = self._isolate_identity(
                    self._base_spec(),
                    value,
                )
                for anchor in spec["anchors"]:
                    anchor["importance"] = value
                spec["expected_question_patterns"] = [
                    {
                        "pattern": "Topic Pack plan 계약을 설명하라.",
                        "intent": "Topic Pack plan의 입력 계약, projection 결과, 검증 및 rollback 경계를 설명한다.",
                    },
                ]
                spec["high_score_points"] = ["핵심 채점 포인트를 구조, 검증, 운영 경계와 함께 설명한다."]
                plan_rc, plan_payload = self._run_tool("plan", spec)
                self.assertEqual(plan_rc, 0, plan_payload)
                self.assertEqual(plan_payload["result"], "PASS")
                with _stage17c4_tempfile.TemporaryDirectory() as temp_dir:
                    output_root = _Stage17C4Path(temp_dir)
                    build_rc, build_payload = self._run_tool(
                        "build",
                        spec,
                        output_root=output_root,
                    )
                    self.assertEqual(build_rc, 0, build_payload)
                    self.assertEqual(build_payload["result"], "PASS")
                    rendered = _stage17c4_json.loads(
                        (
                            output_root
                            / spec["topic_id"]
                            / "fact_anchor.json"
                        ).read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        [anchor["importance"] for anchor in rendered["anchors"]],
                        [value] * len(spec["anchors"]),
                    )

    def test_missing_empty_null_and_invalid_importance_are_rejected(self):
        cases = (
            ("missing", None, True),
            ("empty", "", False),
            ("null", None, False),
            ("invalid", "critical", False),
        )
        for name, value, remove in cases:
            with self.subTest(case=name):
                spec = self._isolate_identity(
                    self._base_spec(),
                    name,
                )
                if remove:
                    spec["anchors"][0].pop("importance", None)
                else:
                    spec["anchors"][0]["importance"] = value
                rc, payload = self._run_tool("plan", spec)
                self.assertEqual(rc, 2, payload)
                self.assertEqual(payload["result"], "FAIL")
                self.assertTrue(
                    any(
                        issue["error_code"] == "TP001_SPEC_SCHEMA_INVALID"
                        and issue["path"].startswith("$.anchors[0]")
                        for issue in payload["issues"]
                    ),
                    payload["issues"],
                )

if __name__ == "__main__":
    unittest.main()
