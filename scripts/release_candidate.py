#!/usr/bin/env python3
"""Fail-closed qualification and deployment orchestration.

This command deliberately keeps Topic Pack, accuracy, and deployment ownership
separate.  It only sequences their canonical commands and records evidence.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any, Sequence
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT_ROOT = ROOT / "reports" / "release_candidates"
PARITY_FILES = (
    "question_type_router.py",
    "logic_check_evaluator.py",
    "logic_llm_verifier.py",
    "grade_score_reconciler.py",
    "verified_defect_reconciliation.py",
)


class ReleaseFailure(RuntimeError):
    """A release gate failed and later stages must not run."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _run(
    argv: Sequence[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    print("RUN:", shlex.join(str(item) for item in argv), flush=True)
    try:
        result = subprocess.run(
            [str(item) for item in argv],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        raise ReleaseFailure(f"cannot execute {argv[0]}: {exc}") from exc
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
    if check and result.returncode:
        raise ReleaseFailure(f"command failed ({result.returncode}): {shlex.join(argv)}")
    return result


def _git(*args: str, check: bool = True) -> str:
    return _run(("git", *args), check=check).stdout.strip()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _new_manifest(artifact_dir: Path, commit: str) -> dict[str, Any]:
    return {
        "schema_version": "release_candidate_evidence_v1",
        "candidate_commit": commit,
        "created_at": _utc_now(),
        "artifact_dir": str(artifact_dir),
        "qualification": {"status": "PENDING", "stages": []},
        "deployment": {"status": "NOT_RUN", "stages": []},
        "issue_close_eligible": False,
    }


def _provider_context() -> dict[str, Any]:
    settings = Path(os.getenv("LLM_PROVIDER_SETTINGS_FILE", "data/user_settings/llm_provider_settings.json"))
    if not settings.is_absolute():
        settings = ROOT / settings
    saved_providers: list[str] = []
    if settings.is_file():
        try:
            payload = json.loads(settings.read_text(encoding="utf-8"))
            configured = payload.get("chat_providers", {})
            if isinstance(configured, dict):
                saved_providers = sorted({str(value) for value in configured.values()})
        except (OSError, json.JSONDecodeError):
            saved_providers = ["INVALID_SETTINGS"]
    default_provider = os.getenv("LLM_PROVIDER", "auto")
    return {
        "default_provider": default_provider,
        "saved_provider_values": saved_providers,
        "effective_no_chat_provider": saved_providers[0] if len(saved_providers) == 1 else default_provider,
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        "clova_model": os.getenv("CLOVA_MODEL", "HCX-003"),
        "ollama_model": os.getenv("OLLAMA_MODEL", "hermes3:latest"),
        "settings_file": str(settings),
        "settings_sha256": _sha256(settings) if settings.is_file() else "MISSING",
    }


def _safe_endpoint(raw_url: str) -> str:
    parsed = urllib.parse.urlsplit(raw_url)
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    return urllib.parse.urlunsplit((parsed.scheme, host, parsed.path, "", ""))


def _provider_preflight() -> dict[str, Any]:
    """Verify required local model reachability and provider credentials."""
    context = _provider_context()
    provider = str(context["effective_no_chat_provider"]).strip().lower()
    gemini_ready = bool(
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    )
    clova_ready = bool(os.getenv("CLOVA_API_KEY"))
    if provider == "gemini" and not gemini_ready:
        raise ReleaseFailure("Gemini is selected but its API credential is missing")
    if provider == "clova" and not clova_ready:
        raise ReleaseFailure("CLOVA is selected but CLOVA_API_KEY is missing")
    if provider == "auto" and not (gemini_ready or clova_ready):
        raise ReleaseFailure("auto provider has no Gemini or CLOVA API credential")
    if provider not in {"auto", "gemini", "clova"}:
        raise ReleaseFailure(f"invalid effective provider: {provider}")

    ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip("/")
    tags_url = f"{ollama_url}/api/tags"
    try:
        with urllib.request.urlopen(tags_url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise ReleaseFailure(f"Ollama preflight failed: {_safe_endpoint(ollama_url)}") from exc
    model = str(context["ollama_model"])
    available = {
        str(item.get("name") or item.get("model") or "")
        for item in payload.get("models", [])
        if isinstance(item, dict)
    }
    if model not in available:
        raise ReleaseFailure(f"Ollama model is unavailable: {model}")
    context.update({
        "gemini_credential_present": gemini_ready,
        "clova_credential_present": clova_ready,
        "ollama_endpoint": _safe_endpoint(ollama_url),
        "ollama_model_available": True,
    })
    return context


def _record_stage(
    manifest: dict[str, Any],
    section: str,
    name: str,
    result: subprocess.CompletedProcess[str],
) -> None:
    manifest[section]["stages"].append({
        "name": name,
        "returncode": result.returncode,
        "completed_at": _utc_now(),
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    })


def _assert_clean(allow_dirty: bool) -> None:
    dirty = _git("status", "--porcelain")
    if dirty and not allow_dirty:
        raise ReleaseFailure("worktree is dirty; commit or stash changes before release")


def qualify(args: argparse.Namespace) -> Path:
    """Run source/code gates, regenerate predictions, and require READY."""
    commit = _git("rev-parse", "HEAD")
    _assert_clean(args.allow_dirty)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_dir = (args.artifact_dir or DEFAULT_ARTIFACT_ROOT / f"{stamp}_{commit[:12]}").resolve()
    if artifact_dir.exists() and any(artifact_dir.iterdir()):
        raise ReleaseFailure(f"artifact directory is not empty: {artifact_dir}")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = artifact_dir / "manifest.json"
    manifest = _new_manifest(artifact_dir, commit)
    manifest["qualification"]["provider_context"] = _provider_context()
    _atomic_json(manifest_path, manifest)

    try:
        manifest["qualification"]["provider_context"] = _provider_preflight()
        manifest["qualification"]["stages"].append({
            "name": "provider_preflight",
            "returncode": 0,
            "completed_at": _utc_now(),
        })
        _atomic_json(manifest_path, manifest)

        command = (sys.executable, "scripts/rubric_manager.py", "validate-topic-pack-release", "--all")
        result = _run(command)
        _record_stage(manifest, "qualification", "topic_pack_all", result)
        _atomic_json(manifest_path, manifest)

        if not args.skip_release_validation:
            result = _run(("bash", "scripts/validate_release.sh"))
            _record_stage(manifest, "qualification", "full_release", result)
            _atomic_json(manifest_path, manifest)

        prediction_dir = artifact_dir / "provider_predictions"
        result = _run((
            sys.executable,
            "scripts/regrade_expert_accuracy_seed.py",
            "--golden", str(args.golden),
            "--output-dir", str(prediction_dir),
            "--workers", str(args.workers),
        ))
        _record_stage(manifest, "qualification", "provider_prediction_regeneration", result)
        predictions = prediction_dir / "predictions.jsonl"
        count = sum(1 for line in predictions.read_text(encoding="utf-8").splitlines() if line.strip())
        if count < args.minimum_predictions:
            raise ReleaseFailure(f"only {count} predictions generated; require {args.minimum_predictions}")
        manifest["qualification"]["prediction_count"] = count
        manifest["qualification"]["predictions_sha256"] = _sha256(predictions)
        _atomic_json(manifest_path, manifest)

        report_path = artifact_dir / "accuracy_report.json"
        result = _run((
            sys.executable,
            "scripts/measure_expert_accuracy.py",
            "--golden", str(args.golden),
            "--predictions", str(predictions),
            "--require-cases",
            "--output", str(report_path),
        ))
        _record_stage(manifest, "qualification", "accuracy_measurement", result)
        _atomic_json(manifest_path, manifest)

        gate_path = artifact_dir / "accuracy_gate.json"
        result = _run((
            sys.executable,
            "scripts/check_accuracy_release_gate.py",
            "--golden", str(args.golden),
            "--policy", str(args.policy),
            "--report", str(report_path),
            "--require-ready",
        ), check=False)
        gate_path.write_text(result.stdout, encoding="utf-8")
        _record_stage(manifest, "qualification", "accuracy_gate", result)
        if result.returncode:
            raise ReleaseFailure("accuracy Gate is HOLD; deployment is blocked")

        manifest["qualification"].update({
            "status": "READY",
            "completed_at": _utc_now(),
            "accuracy_report": str(report_path),
            "accuracy_gate": str(gate_path),
        })
        _atomic_json(manifest_path, manifest)
        print(f"QUALIFICATION=READY\nMANIFEST={manifest_path}")
        return manifest_path
    except Exception as exc:
        manifest["qualification"].update({
            "status": "HOLD",
            "failed_at": _utc_now(),
            "reason": str(exc),
        })
        _atomic_json(manifest_path, manifest)
        raise


def _compose_prefix(compose_file: Path) -> tuple[str, ...]:
    return ("docker", "compose", "-f", str(compose_file))


def _container_sha(container_id: str, container_root: str, relative: str) -> str:
    target = f"{container_root.rstrip('/')}/{relative}"
    result = _run(("docker", "exec", container_id, "sha256sum", target))
    return result.stdout.split()[0]


def deploy(args: argparse.Namespace) -> Path:
    """Deploy one READY candidate and capture runtime proof."""
    manifest_path = args.manifest.resolve()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseFailure(f"cannot load candidate manifest: {manifest_path}") from exc
    if manifest.get("qualification", {}).get("status") != "READY":
        raise ReleaseFailure("candidate is not READY; deployment is blocked")
    manifest["deployment"].update({"status": "RUNNING", "started_at": _utc_now()})
    _atomic_json(manifest_path, manifest)
    try:
        commit = _git("rev-parse", "HEAD")
        if commit != manifest.get("candidate_commit"):
            raise ReleaseFailure("HEAD differs from qualified candidate commit")
        _assert_clean(args.allow_dirty)
        compose_file = args.compose_file.resolve()
        if not compose_file.is_file():
            raise ReleaseFailure(f"compose file not found: {compose_file}")
        endpoint_script = args.endpoint_smoke_script.resolve()
        if not endpoint_script.is_file() or not os.access(endpoint_script, os.X_OK):
            raise ReleaseFailure(f"endpoint smoke script is not executable: {endpoint_script}")
        prefix = _compose_prefix(compose_file)
        config = _run((*prefix, "config", "--format", "json"))
        parsed_config = json.loads(config.stdout)
        service_config = parsed_config.get("services", {}).get(args.service)
        if not isinstance(service_config, dict):
            raise ReleaseFailure(f"service missing from compose config: {args.service}")
        mode = "image_build" if service_config.get("build") else "bind_mount_recreate"
        _record_stage(manifest, "deployment", "compose_config", config)

        previous_result = _run((*prefix, "ps", "-q", args.service), check=False)
        previous_container_id = previous_result.stdout.strip()

        if mode == "image_build":
            result = _run((*prefix, "build", args.service))
            _record_stage(manifest, "deployment", "image_build", result)
        result = _run((*prefix, "up", "-d", "--force-recreate", args.service))
        _record_stage(manifest, "deployment", "container_recreate", result)

        container_id_result = _run((*prefix, "ps", "-q", args.service))
        container_id = container_id_result.stdout.strip()
        if not container_id:
            raise ReleaseFailure("compose did not return a container id")
        if previous_container_id and previous_container_id == container_id:
            raise ReleaseFailure("container identity did not change after --force-recreate")
        inspect_result = _run(("docker", "inspect", container_id))
        inspect_data = json.loads(inspect_result.stdout)[0]
        fingerprint = {
            "candidate_commit": commit,
            "deployment_mode": mode,
            "previous_container_id": previous_container_id or None,
            "container_id": container_id,
            "container_started_at": inspect_data.get("State", {}).get("StartedAt"),
            "image_id": inspect_data.get("Image"),
            "image_name": inspect_data.get("Config", {}).get("Image"),
        }

        provenance_result = _run((
            "docker", "exec", container_id, "python3", "-c",
            "import json; from runtime_grading_provenance import build_runtime_grading_provenance as b; print(json.dumps(b(), sort_keys=True))",
        ))
        try:
            runtime_provenance = json.loads(provenance_result.stdout)
        except json.JSONDecodeError as exc:
            raise ReleaseFailure("container runtime provenance is not valid JSON") from exc
        if runtime_provenance.get("engine_commit") != commit:
            raise ReleaseFailure("container engine_commit differs from qualified candidate")
        fingerprint["runtime_grading_provenance"] = runtime_provenance

        parity: dict[str, dict[str, str]] = {}
        for relative in PARITY_FILES:
            host_sha = _sha256(ROOT / relative)
            container_sha = _container_sha(container_id, args.container_root, relative)
            parity[relative] = {"host": host_sha, "container": container_sha}
            if host_sha != container_sha:
                raise ReleaseFailure(f"host/container parity mismatch: {relative}")

        replay = _run((
            *prefix, "exec", "-T", args.service,
            "python3", "-B", "tests/test_sil_runtime_replay.py",
        ))
        _record_stage(manifest, "deployment", "production_replay", replay)
        endpoint_env = dict(os.environ)
        endpoint_env.update({
            "RELEASE_CANDIDATE_COMMIT": commit,
            "RELEASE_CONTAINER_ID": container_id,
            "RELEASE_SERVICE": args.service,
        })
        endpoint = _run((str(endpoint_script),), env=endpoint_env)
        _record_stage(manifest, "deployment", "endpoint_smoke", endpoint)

        manifest["deployment"].update({
            "status": "PASS",
            "completed_at": _utc_now(),
            "fingerprint": fingerprint,
            "parity": parity,
        })
        manifest["issue_close_eligible"] = True
        _atomic_json(manifest_path, manifest)
        print(f"DEPLOYMENT=PASS\nISSUE_CLOSE_ELIGIBLE=true\nMANIFEST={manifest_path}")
        return manifest_path
    except Exception as exc:
        manifest["deployment"].update({
            "status": "FAIL",
            "failed_at": _utc_now(),
            "reason": str(exc),
        })
        manifest["issue_close_eligible"] = False
        _atomic_json(manifest_path, manifest)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    qualify_parser = sub.add_parser("qualify", help="produce a READY/HOLD release candidate")
    qualify_parser.add_argument("--artifact-dir", type=Path)
    qualify_parser.add_argument("--golden", type=Path, default=ROOT / "calibration" / "expert_accuracy_golden.jsonl")
    qualify_parser.add_argument("--policy", type=Path, default=ROOT / "calibration" / "expert_accuracy_release_policy.json")
    qualify_parser.add_argument("--workers", type=int, choices=range(1, 5), default=1)
    qualify_parser.add_argument("--minimum-predictions", type=int, default=30)
    qualify_parser.add_argument("--skip-release-validation", action="store_true")
    qualify_parser.add_argument("--allow-dirty", action="store_true", help="development only; never use for deployment evidence")

    deploy_parser = sub.add_parser("deploy", help="deploy a READY candidate and capture proof")
    deploy_parser.add_argument("--manifest", type=Path, required=True)
    deploy_parser.add_argument("--compose-file", type=Path, required=True)
    deploy_parser.add_argument("--service", default="prof-eng-answer-bot")
    deploy_parser.add_argument("--container-root", default="/workspace/prof_eng_answer")
    deploy_parser.add_argument("--endpoint-smoke-script", type=Path, required=True)
    deploy_parser.set_defaults(allow_dirty=False)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "qualify":
            qualify(args)
        else:
            deploy(args)
    except Exception as exc:
        print(f"HOLD: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
