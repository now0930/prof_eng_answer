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
    def test_deploy_rejects_hold_without_running_commands(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / "manifest.json"
            manifest.write_text(json.dumps({
                "candidate_commit": "abc",
                "qualification": {"status": "HOLD"},
            }), encoding="utf-8")
            args = argparse.Namespace(manifest=manifest)
            with patch.object(release, "_run") as run:
                with self.assertRaisesRegex(release.ReleaseFailure, "not READY"):
                    release.deploy(args)
            run.assert_not_called()

    def test_qualify_records_hold_when_accuracy_gate_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            artifact = Path(temporary) / "candidate"

            def fake_run(argv, **kwargs):
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
                skip_release_validation=True,
            )
            def fake_git(*argv, **kwargs):
                return "a" * 40 if argv == ("rev-parse", "HEAD") else ""

            with patch.object(release, "_git", side_effect=fake_git), patch.object(
                release, "_provider_preflight", return_value={"effective_no_chat_provider": "gemini"}
            ), patch.object(
                release, "_run", side_effect=fake_run
            ):
                with self.assertRaisesRegex(release.ReleaseFailure, "HOLD"):
                    release.qualify(args)
            data = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["qualification"]["status"], "HOLD")
            self.assertEqual(data["deployment"]["status"], "NOT_RUN")
            self.assertFalse(data["issue_close_eligible"])
            self.assertEqual(data["qualification"]["prediction_count"], 30)

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

    def test_provider_regeneration_disables_final_grade_cache(self):
        with patch.dict("os.environ", {"CLOVA_API_KEY": "live-secret"}, clear=True):
            provider_env = release._uncached_provider_env()
        self.assertEqual(provider_env["CLOVA_API_KEY"], "live-secret")
        self.assertEqual(provider_env["FINAL_GRADE_CACHE_ENABLED"], "0")
        self.assertEqual(provider_env["PYTHONDONTWRITEBYTECODE"], "1")

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
                "qualification": {"status": "READY", "stages": []},
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
                if argv[:3] == ("docker", "exec", "container123") and "runtime_grading_provenance" in argv[-1]:
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
