from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import release_candidate as release


def completed(argv, stdout="", returncode=0, stderr=""):
    return subprocess.CompletedProcess(argv, returncode, stdout, stderr)


class ReleaseCandidateTest(unittest.TestCase):
    def test_deploy_rejects_missing_pytest_validation_without_running_commands(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / "manifest.json"
            manifest.write_text(json.dumps({
                "candidate_commit": "abc",
                "qualification": {"status": "HOLD"},
            }), encoding="utf-8")
            args = argparse.Namespace(manifest=manifest)
            with patch.object(release, "_run") as run:
                with self.assertRaisesRegex(release.ReleaseFailure, "pytest validation is not PASS"):
                    release.deploy(args)
            run.assert_not_called()

    def test_pytest_validation_without_accuracy_or_provider_calls(self):
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "candidate"
            args = argparse.Namespace(artifact_dir=artifact)
            invoked = []
            def fake_run(argv, **kwargs):
                invoked.append(tuple(argv))
                return completed(argv, "5 passed, 1 deselected\\n")
            with patch.object(release, "_git", side_effect=lambda *parts: "a" * 40 if parts == ("rev-parse", "HEAD") else ""), \
                 patch.object(release, "_pytest_quarantine_nodes", return_value=["tests/test_old.py::test_known"]), \
                 patch.object(release, "_run", side_effect=fake_run):
                path = release.validate(args)
            record = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(record["validation"]["status"], "PASS_WITH_QUARANTINE")
            self.assertIn("--deselect=tests/test_old.py::test_known", invoked[0])
            self.assertTrue(all("qualify" not in item for command in invoked for item in command))
            self.assertEqual(record["deployment"]["status"], "NOT_RUN")

    def test_failed_pytest_cannot_produce_deployable_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "candidate"
            with patch.object(release, "_git", side_effect=lambda *parts: "a" * 40 if parts == ("rev-parse", "HEAD") else ""), \
                 patch.object(release, "_pytest_quarantine_nodes", return_value=[]), \
                 patch.object(release, "_run", return_value=completed(["pytest"], "1 failed\\n", returncode=1)):
                with self.assertRaisesRegex(release.ReleaseFailure, "pytest_validation_failed"):
                    release.validate(argparse.Namespace(artifact_dir=artifact))
            record = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(record["validation"]["status"], "FAIL")

    def test_qualify_records_hold_when_accuracy_gate_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "candidate"
            invoked = []

            def fake_run(argv, **kwargs):
                invoked.append(argv)
                if any(str(item).endswith("regrade_expert_accuracy_seed.py") for item in argv):
                    output = Path(argv[argv.index("--output-dir") + 1])
                    output.mkdir(parents=True)
                    (output / "predictions.jsonl").write_text(
                        "".join(json.dumps({"case_id": str(i)}) + "\n" for i in range(30)),
                        encoding="utf-8",
                    )
                if any(str(item).endswith("check_accuracy_release_gate.py") for item in argv):
                    return completed(argv, '{"ready": false}\n', returncode=2)
                return completed(argv, "PASS\n")

            args = argparse.Namespace(
                allow_dirty=False,
                artifact_dir=artifact,
                golden=release.ROOT / "calibration" / "expert_accuracy_golden.jsonl",
                policy=release.ROOT / "calibration" / "expert_accuracy_release_policy.json",
                workers=1,
                minimum_predictions=30,
                skip_release_validation=False,
            )
            def fake_git(*argv, **kwargs):
                return "a" * 40 if argv == ("rev-parse", "HEAD") else ""

            with patch.dict("os.environ", {
                "VALIDATION_LIVE_API": "1",
                "VALIDATION_GEMINI_API_KEY": "validation-key-example",
                "GEMINI_API_KEY": "different-production-key",
                "VALIDATION_MAX_LIVE_GRADES": "100",
                "VALIDATION_MAX_HTTP_CALLS": "200",
                "VALIDATION_MAX_TOTAL_TOKENS": "1000000",
            }, clear=False), patch.object(release, "_git", side_effect=fake_git), patch.object(
                release, "_provider_preflight", return_value={"effective_no_chat_provider": "gemini"}
            ), patch.object(
                release, "_current_production_scoring_contract", return_value={"primary": "deterministic_abc", "qualitative_de_mode": "argon"}
            ), patch.object(release, "_run", side_effect=fake_run):
                with self.assertRaisesRegex(release.ReleaseFailure, "HOLD"):
                    release.qualify(args)
            data = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["qualification"]["status"], "HOLD")
            self.assertEqual(data["deployment"]["status"], "NOT_RUN")
            self.assertFalse(data["issue_close_eligible"])
            self.assertEqual(data["qualification"]["prediction_count"], 30)
            regeneration = [args for args in invoked if any(
                str(value).endswith("regrade_expert_accuracy_seed.py") for value in args
            )]
            self.assertEqual(len(regeneration), 1)
            self.assertIn("--require-production-success", regeneration[0])
            self.assertNotIn("--require-semantic-success", regeneration[0])
            self.assertTrue(any(any(str(value).endswith("validate_release.sh") for value in argv) for argv in invoked))

    def test_qualify_records_failed_production_case_stage_and_blocks_accuracy(self):
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "candidate"
            invoked = []

            def fake_run(argv, **kwargs):
                invoked.append((argv, kwargs))
                if any(str(item).endswith("regrade_expert_accuracy_seed.py") for item in argv):
                    self.assertFalse(kwargs["check"])
                    self.assertIn("--collect-failures", argv)
                    output = Path(argv[argv.index("--output-dir") + 1])
                    output.mkdir(parents=True)
                    (output / "case_results.jsonl").write_text(
                        '{"case_id":"sis_lopa_architecture_issue1",'
                        '"status":"FAILED","reason_code":"unresolved_requirement"}\\n',
                        encoding="utf-8",
                    )
                    return completed(argv, "FAILURES=1\\n", returncode=1)
                return completed(argv, "PASS\\n")

            args = argparse.Namespace(
                allow_dirty=False,
                artifact_dir=artifact,
                golden=release.ROOT / "calibration" / "expert_accuracy_golden.jsonl",
                policy=release.ROOT / "calibration" / "expert_accuracy_release_policy.json",
                workers=2,
                minimum_predictions=30,
                skip_release_validation=False,
            )

            with patch.dict("os.environ", {
                "VALIDATION_LIVE_API": "1",
                "VALIDATION_GEMINI_API_KEY": "validation-key-example",
                "GEMINI_API_KEY": "different-production-key",
                "VALIDATION_MAX_LIVE_GRADES": "100",
                "VALIDATION_MAX_HTTP_CALLS": "200",
                "VALIDATION_MAX_TOTAL_TOKENS": "1000000",
            }, clear=False), patch.object(
                release, "_git",
                side_effect=lambda *argv, **kwargs:
                "c" * 40 if argv == ("rev-parse", "HEAD") else "",
            ), patch.object(
                release, "_provider_preflight", return_value={}
            ), patch.object(
                release, "_current_production_scoring_contract",
                return_value={"primary": "deterministic_abc", "qualitative_de_mode": "argon"},
            ), patch.object(release, "_run", side_effect=fake_run):
                with self.assertRaisesRegex(release.ReleaseFailure, "reviewed production cases failed"):
                    release.qualify(args)

            manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["qualification"]["status"], "HOLD")
            self.assertEqual(manifest["deployment"]["status"], "NOT_RUN")
            self.assertFalse(manifest["issue_close_eligible"])
            stages = manifest["qualification"]["stages"]
            self.assertEqual(stages[-1]["name"], "provider_prediction_regeneration")
            self.assertEqual(stages[-1]["returncode"], 1)
            self.assertTrue((artifact / "provider_predictions" / "case_results.jsonl").exists())
            self.assertFalse(any(
                any(str(part).endswith("check_accuracy_release_gate.py") for part in argv)
                for argv, _ in invoked
            ))

    def test_qualify_cannot_skip_full_release_or_reduce_accuracy_sample(self):
        with tempfile.TemporaryDirectory() as temporary:
            args = argparse.Namespace(
                allow_dirty=False,
                artifact_dir=Path(temporary) / "unused",
                minimum_predictions=30,
                skip_release_validation=True,
            )
            with patch.object(release, "_run") as run:
                with self.assertRaisesRegex(release.ReleaseFailure, "cannot be skipped"):
                    release.qualify(args)
            run.assert_not_called()

            args.skip_release_validation = False
            args.minimum_predictions = 1
            with patch.object(release, "_run") as run:
                with self.assertRaisesRegex(release.ReleaseFailure, "at least 30"):
                    release.qualify(args)
            run.assert_not_called()

    def test_qualification_checks_actual_48_case_worklist_before_paid_calls(self):
        args = argparse.Namespace(
            minimum_predictions=30,
            stability_runs=2,
            golden=release.ROOT / "calibration" / "expert_accuracy_golden.jsonl",
            skip_release_validation=False,
        )
        with patch.dict("os.environ", {
            "VALIDATION_LIVE_API": "1",
            "VALIDATION_GEMINI_API_KEY": "isolated-validation-key",
            "VALIDATION_MAX_LIVE_GRADES": "60",
            "VALIDATION_MAX_HTTP_CALLS": "200",
            "VALIDATION_MAX_TOTAL_TOKENS": "1000000",
        }, clear=True), patch.object(release, "_run") as run:
            with self.assertRaisesRegex(
                release.ReleaseFailure, "validation_grade_budget_exceeded_actual_worklist",
            ):
                release.qualify(args)
        run.assert_not_called()

    def test_provider_preflight_rejects_missing_credentials_before_ollama(self):
        isolated_env = {
            "LLM_PROVIDER": "auto",
            "LLM_PROVIDER_SETTINGS_FILE": "/tmp/release-candidate-missing-settings.json",
        }
        with patch.dict("os.environ", isolated_env, clear=True), patch(
            "urllib.request.urlopen"
        ) as urlopen:
            with self.assertRaisesRegex(release.ReleaseFailure, "no Gemini or CLOVA"):
                release._provider_preflight()
        urlopen.assert_not_called()

    def test_validation_environment_removes_live_provider_inputs(self):
        values = {key: "secret-or-runtime-value" for key in release.VALIDATION_ENV_KEYS}
        values["ASSISTED_ROUTING_ENABLED"] = "1"
        with patch.dict("os.environ", values, clear=False):
            sanitized = release._deterministic_validation_env()
        for key in release.VALIDATION_ENV_KEYS:
            self.assertNotIn(key, sanitized)
        self.assertNotIn("ASSISTED_ROUTING_ENABLED", sanitized)
        self.assertEqual(sanitized["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertEqual(sanitized["PROMOTE_GENERATED"], "0")
        self.assertEqual(sanitized["RUN_SMOKE_TOPIC_PACKS"], "0")
        self.assertEqual(sanitized["RUN_GRADING_REPRODUCIBILITY"], "0")

    def test_provider_regeneration_disables_cache_and_never_uses_grading_key(self):
        with patch.dict("os.environ", {
            "VALIDATION_LIVE_API": "1",
            "GEMINI_API_KEY": "production-secret",
            "CLOVA_API_KEY": "production-clova-secret",
            "VALIDATION_GEMINI_API_KEY": "separate-validation-secret",
        }, clear=True):
            provider_env = release._uncached_provider_env(
                budget_db=Path("/tmp/test-api-budget.sqlite3"),
                max_grades=96,
                max_http_calls=200,
                max_total_tokens=1000000,
            )
        self.assertEqual(provider_env["GEMINI_API_KEY"], "separate-validation-secret")
        self.assertNotIn("CLOVA_API_KEY", provider_env)
        self.assertNotIn("GOOGLE_API_KEY", provider_env)
        self.assertEqual(provider_env["FINAL_GRADE_CACHE_ENABLED"], "0")
        self.assertEqual(provider_env["PYTHONDONTWRITEBYTECODE"], "1")

    def test_qualify_denies_paid_api_without_validation_opt_in_before_any_work(self):
        args = argparse.Namespace(
            minimum_predictions=30,
            stability_runs=2,
            skip_release_validation=False,
        )
        with patch.dict("os.environ", {
            "GEMINI_API_KEY": "production-key",
            "DETERMINISTIC_GRADING_PRIMARY": "true",
            "QUALITATIVE_DE_MODE": "argon",
        }, clear=True), patch.object(release, "_run") as run:
            with self.assertRaisesRegex(release.ReleaseFailure, "validation_live_api_disabled"):
                release.qualify(args)
        run.assert_not_called()

    def test_qualify_rejects_excessive_live_validation_runs(self):
        args = argparse.Namespace(
            minimum_predictions=30, stability_runs=3, skip_release_validation=False,
        )
        with patch.dict("os.environ", {
            "VALIDATION_LIVE_API": "1",
            "VALIDATION_GEMINI_API_KEY": "validation-key",
            "VALIDATION_MAX_LIVE_GRADES": "60",
            "VALIDATION_MAX_HTTP_CALLS": "200",
            "VALIDATION_MAX_TOTAL_TOKENS": "1000000",
        }, clear=True), patch.object(release, "_run") as run:
            with self.assertRaisesRegex(release.ReleaseFailure, "validation_grade_budget_exceeded"):
                release.qualify(args)
        run.assert_not_called()

    def test_deploy_records_fingerprint_parity_and_close_eligibility(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest_path = root / "manifest.json"
            compose_path = root / "compose.yaml"
            endpoint_path = root / "endpoint-smoke"
            compose_path.write_text("services: {}\n", encoding="utf-8")
            endpoint_path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            endpoint_path.chmod(0o755)
            commit = "b" * 40
            manifest_path.write_text(json.dumps({
                "candidate_commit": commit,
                "qualification": {"status": "NOT_REQUIRED", "stages": []},
                "validation": {"status": "PASS_WITH_QUARANTINE", "stages": []},
                "deployment": {"status": "NOT_RUN", "stages": []},
                "issue_close_eligible": False,
            }), encoding="utf-8")

            def fake_run(argv, **kwargs):
                if argv[-3:] == ("config", "--format", "json"):
                    return completed(argv, json.dumps({
                        "services": {"prof-eng-answer-bot": {"image": "example:test"}}
                    }))
                if "ps" in argv and "-q" in argv:
                    fake_run.ps_calls += 1
                    return completed(argv, "old-container\n" if fake_run.ps_calls == 1 else "container123\n")
                if argv[:2] == ("docker", "inspect"):
                    return completed(argv, json.dumps([{
                        "State": {"StartedAt": "2026-09-05T00:00:00Z"},
                        "Image": "sha256:image",
                        "Config": {"Image": "example:test"},
                    }]))
                if argv[:3] == ("docker", "exec", "container123") and "sha256sum" in argv:
                    relative = argv[-1].split("/workspace/prof_eng_answer/", 1)[1]
                    digest = hashlib.sha256((release.ROOT / relative).read_bytes()).hexdigest()
                    return completed(argv, f"{digest}  {argv[-1]}\n")
                if argv[:3] == ("docker", "exec", "container123") and "from grading.scoring.runtime_grading_provenance" in argv[-1]:
                    return completed(argv, json.dumps({"engine_commit": commit}))
                return completed(argv, "PASS\n")

            fake_run.ps_calls = 0

            args = argparse.Namespace(
                manifest=manifest_path,
                compose_file=compose_path,
                service="prof-eng-answer-bot",
                container_root="/workspace/prof_eng_answer",
                endpoint_smoke_script=endpoint_path,
                allow_dirty=False,
            )
            def fake_git(*argv, **kwargs):
                return commit if argv == ("rev-parse", "HEAD") else ""

            with patch.object(release, "_git", side_effect=fake_git), patch.object(
                release, "_run", side_effect=fake_run
            ):
                release.deploy(args)
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(data["deployment"]["status"], "PASS")
            self.assertEqual(data["deployment"]["fingerprint"]["container_id"], "container123")
            self.assertEqual(data["deployment"]["fingerprint"]["previous_container_id"], "old-container")
            self.assertEqual(set(data["deployment"]["parity"]), set(release.PARITY_FILES))
            self.assertTrue(data["issue_close_eligible"])


if __name__ == "__main__":
    unittest.main()
