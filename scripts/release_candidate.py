#!/usr/bin/env python3
"""Pytest-based release validation and deployment orchestration.

Accuracy/LLM qualification remain available as optional diagnostics but never
block the user-approved pytest-only deployment pathway.
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
sys.path.insert(0, str(ROOT))
from grading.quality.validation_credentials import (
    ValidationCredentialError,
    require_validation_key,
    validation_provider_environment,
)
from grading.quality.validation_api_budget import write_summary as write_api_usage_summary

DEFAULT_ARTIFACT_ROOT = ROOT / "reports" / "release_candidates"
PARITY_FILES = (
    "bot.py",
    "study/learning_runtime.py",
    "study/review_presentation.py",
    "study/review_model_answer.py",
    "grading/quality/production_grade_gate.py",
    "grading/routing/question_type_router.py",
    "grading/evidence/logic_check_evaluator.py",
    "grading/evidence/logic_llm_verifier.py",
    "grading/scoring/grade_score_reconciler.py",
    "grading/evidence/verified_defect_reconciliation.py",
)
VALIDATION_ENV_KEYS = (
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_GENERATIVE_AI_API_KEY",
    "GEMINI_MODEL",
    "CLOVA_API_KEY",
    "CLOVA_APIGW_API_KEY",
    "CLOVA_MODEL",
    "CLOVA_HOST",
    "CLOVA_ENDPOINT",
    "LLM_PROVIDER",
    "LLM_PROVIDER_SETTINGS_FILE",
    "OLLAMA_URL",
    "OLLAMA_MODEL",
    "QUESTION_DEMAND_SHADOW_ENABLED",
    "SEMANTIC_ROUTER_SHADOW_ENABLED",
    "DETERMINISTIC_GRADING_PRIMARY",
    "QUALITATIVE_DE_MODE",
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
    return _run(
        ("git", "-c", f"safe.directory={ROOT}", *args),
        check=check,
    ).stdout.strip()


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
        "qualification": {"status": "NOT_REQUIRED", "stages": []},
        "validation": {"status": "NOT_RUN", "stages": []},
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


def _provider_preflight(provider_env: dict[str, str] | None = None) -> dict[str, Any]:
    """Check the *validation* provider, never the grading credential."""
    env = provider_env if provider_env is not None else validation_provider_environment()
    context = _provider_context()
    provider = str(context["effective_no_chat_provider"]).strip().lower()
    gemini_ready = bool(env.get("GEMINI_API_KEY"))
    clova_ready = bool(env.get("CLOVA_API_KEY"))
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


def _current_production_scoring_contract() -> dict[str, str]:
    """Validate the configured runtime path, without changing any settings."""
    primary = str(os.getenv("DETERMINISTIC_GRADING_PRIMARY", "")).strip().lower()
    de_mode = str(os.getenv("QUALITATIVE_DE_MODE", "off")).strip().lower()
    if primary not in {"1", "true", "yes", "on"}:
        raise ReleaseFailure("production qualification requires configured deterministic A/B/C primary")
    if de_mode != "argon":
        raise ReleaseFailure("production qualification requires configured Argon D/E mode")
    # Provider transports retain their legacy env interface, but qualification
    # supplies *only* the separately authorized validation key.
    try:
        require_validation_key("gemini")
    except ValidationCredentialError as exc:
        raise ReleaseFailure(str(exc)) from None
    return {
        "primary": "deterministic_abc",
        "qualitative_de_mode": "argon",
        "argon_model": "gemini-4-argon",
        "success_contract": "deterministic_scored_and_argon_de_applied",
    }


def _deterministic_validation_env() -> dict[str, str]:
    """Return a CI-like environment without live provider routing inputs."""
    passthrough = (
        "PATH",
        "HOME",
        "LANG",
        "LANGUAGE",
        "LC_ALL",
        "TZ",
        "TMPDIR",
        "TERM",
        "USER",
        "CI",
    )
    env = {key: os.environ[key] for key in passthrough if key in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Match the GitHub Actions release gate. Qualification must validate the
    # committed generated artifacts, never rewrite/promote them in-place.
    env["PROMOTE_GENERATED"] = "0"
    env["RUN_SMOKE_TOPIC_PACKS"] = "0"
    env["RUN_GRADING_REPRODUCIBILITY"] = "0"
    return env


def _uncached_provider_env(
    *, budget_db: Path, max_grades: int, max_http_calls: int, max_total_tokens: int,
) -> dict[str, str]:
    """Use ONLY isolated validation credentials for uncached accuracy runs."""
    env = validation_provider_environment()
    env["FINAL_GRADE_CACHE_ENABLED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["VALIDATION_API_BUDGET_DB"] = str(budget_db)
    env["VALIDATION_MAX_LIVE_GRADES"] = str(max_grades)
    env["VALIDATION_MAX_HTTP_CALLS"] = str(max_http_calls)
    env["VALIDATION_MAX_TOTAL_TOKENS"] = str(max_total_tokens)
    return env


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
    if args.skip_release_validation:
        raise ReleaseFailure("full release validation cannot be skipped in production qualification")
    if args.minimum_predictions < 30:
        raise ReleaseFailure("production accuracy qualification requires at least 30 predictions")
    stability_runs = int(getattr(args, "stability_runs", 2))
    if stability_runs < 2:
        raise ReleaseFailure("stability_runs must be at least 2")
    try:
        max_grades = int(os.getenv("VALIDATION_MAX_LIVE_GRADES", "60"))
    except ValueError:
        raise ReleaseFailure("invalid VALIDATION_MAX_LIVE_GRADES") from None
    # Bound *submitted grades*, not raw provider tokens or nested retries.
    # Provider-side quota is still necessary for a strict spend ceiling.
    if max_grades <= 0 or args.minimum_predictions * stability_runs > max_grades:
        raise ReleaseFailure("validation_grade_budget_exceeded")
    try:
        validation_env = validation_provider_environment()
        require_validation_key("gemini")  # Argon D/E is mandatory for this release gate.
    except ValidationCredentialError as exc:
        raise ReleaseFailure(str(exc)) from None
    explicit_budgets: dict[str, int] = {}
    for name in ("VALIDATION_MAX_HTTP_CALLS", "VALIDATION_MAX_TOTAL_TOKENS"):
        raw = str(os.getenv(name, "")).strip()
        if not raw.isdecimal() or int(raw) <= 0:
            raise ReleaseFailure(f"{name.lower()}_must_be_explicit_positive_integer")
        explicit_budgets[name] = int(raw)
    # Count the actual worklist, not only --minimum-predictions: a larger
    # Golden Set must never silently exceed the validation grade budget.
    try:
        case_count = sum(
            bool(line.strip()) for line in Path(args.golden).read_text(encoding="utf-8").splitlines()
        )
    except OSError as exc:
        raise ReleaseFailure("validation_golden_unreadable") from exc
    if case_count * stability_runs > max_grades:
        raise ReleaseFailure("validation_grade_budget_exceeded_actual_worklist")
    commit = _git("rev-parse", "HEAD")
    _assert_clean(args.allow_dirty)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_dir = (args.artifact_dir or DEFAULT_ARTIFACT_ROOT / f"{stamp}_{commit[:12]}").resolve()
    if artifact_dir.exists() and any(artifact_dir.iterdir()):
        raise ReleaseFailure(f"artifact directory is not empty: {artifact_dir}")
    artifact_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    artifact_dir.chmod(0o700)
    budget_db = artifact_dir / "api_usage.sqlite3"
    manifest_path = artifact_dir / "manifest.json"
    manifest = _new_manifest(artifact_dir, commit)
    manifest["qualification"]["provider_context"] = _provider_context()
    manifest["qualification"]["api_usage_report"] = str(artifact_dir / "api_usage.json")
    manifest["qualification"]["validation_budget"] = {
        "max_live_grades": max_grades,
        "max_http_calls": explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
        "max_total_tokens": explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
    }
    _atomic_json(manifest_path, manifest)

    try:
        manifest["qualification"]["production_scoring_contract"] = _current_production_scoring_contract()
        _atomic_json(manifest_path, manifest)
        manifest["qualification"]["provider_context"] = _provider_preflight(validation_env)
        manifest["qualification"]["stages"].append({
            "name": "provider_preflight",
            "returncode": 0,
            "completed_at": _utc_now(),
        })
        _atomic_json(manifest_path, manifest)

        command = (sys.executable, "scripts/rubric_manager.py", "validate-topic-pack-release", "--all")
        result = _run(command, env=_deterministic_validation_env())
        _record_stage(manifest, "qualification", "topic_pack_all", result)
        _atomic_json(manifest_path, manifest)

        result = _run(
            ("bash", "scripts/validate_release.sh"),
            env=_deterministic_validation_env(),
        )
        _record_stage(manifest, "qualification", "full_release", result)
        _atomic_json(manifest_path, manifest)

        prediction_dir = artifact_dir / "provider_predictions"
        result = _run((
            sys.executable,
            "scripts/regrade_expert_accuracy_seed.py",
            "--golden", str(args.golden),
            "--output-dir", str(prediction_dir),
            "--workers", str(args.workers),
            "--require-production-success", "--collect-failures",
        ), env=_uncached_provider_env(
            budget_db=budget_db,
            max_grades=max_grades,
            max_http_calls=explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
            max_total_tokens=explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
        ), check=False)
        write_api_usage_summary(
            artifact_dir / "api_usage.json", db_path=budget_db,
            max_live_grades=max_grades,
            max_http_calls=explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
            max_total_tokens=explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
        )
        _record_stage(manifest, "qualification", "provider_prediction_regeneration", result)
        _atomic_json(manifest_path, manifest)
        if result.returncode:
            raise ReleaseFailure(
                "reviewed production cases failed; inspect private "
                "provider_predictions/case_results.jsonl; deployment is blocked"
            )
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

        prediction_paths = [predictions]
        for run_index in range(2, stability_runs + 1):
            repeat_dir = artifact_dir / f"provider_predictions_run_{run_index:02d}"
            result = _run((
                sys.executable,
                "scripts/regrade_expert_accuracy_seed.py",
                "--golden", str(args.golden),
                "--output-dir", str(repeat_dir),
                "--workers", str(args.workers),
                "--require-production-success", "--collect-failures",
            ), env=_uncached_provider_env(
                budget_db=budget_db,
                max_grades=max_grades,
                max_http_calls=explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
                max_total_tokens=explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
            ), check=False)
            write_api_usage_summary(
                artifact_dir / "api_usage.json", db_path=budget_db,
                max_live_grades=max_grades,
                max_http_calls=explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
                max_total_tokens=explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
            )
            _record_stage(
                manifest, "qualification", f"provider_prediction_repeat_{run_index:02d}", result
            )
            _atomic_json(manifest_path, manifest)
            if result.returncode:
                raise ReleaseFailure(
                    f"stability run {run_index} has failed production cases; "
                    f"inspect private provider_predictions_run_{run_index:02d}/"
                    "case_results.jsonl; deployment is blocked"
                )
            repeat_predictions = repeat_dir / "predictions.jsonl"
            repeat_count = sum(
                1 for line in repeat_predictions.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if repeat_count < args.minimum_predictions:
                raise ReleaseFailure(
                    f"stability run {run_index} generated {repeat_count} predictions; "
                    f"require {args.minimum_predictions}"
                )
            prediction_paths.append(repeat_predictions)
            _atomic_json(manifest_path, manifest)

        stability_report = artifact_dir / "demand_state_stability_report.json"
        stability_markdown = artifact_dir / "demand_state_stability_report.md"
        command = [
            sys.executable,
            "scripts/analyze_demand_state_stability.py",
            "--golden", str(args.golden),
        ]
        for path in prediction_paths:
            command.extend(("--predictions", str(path)))
        command.extend((
            "--output-json", str(stability_report),
            "--output-md", str(stability_markdown),
        ))
        result = _run(command)
        _record_stage(manifest, "qualification", "demand_state_stability_measurement", result)

        stability_gate = artifact_dir / "demand_state_stability_gate.json"
        result = _run((
            sys.executable,
            "scripts/check_demand_state_stability_gate.py",
            "--report", str(stability_report),
            "--policy", str(args.stability_policy),
            "--require-stable",
        ), check=False)
        stability_gate.write_text(result.stdout, encoding="utf-8")
        _record_stage(manifest, "qualification", "demand_state_stability_gate", result)
        if result.returncode:
            raise ReleaseFailure("demand-state stability Gate is HOLD; deployment is blocked")

        manifest["qualification"].update({
            "status": "READY",
            "completed_at": _utc_now(),
            "accuracy_report": str(report_path),
            "accuracy_gate": str(gate_path),
            "stability_run_count": stability_runs,
            "demand_state_stability_report": str(stability_report),
            "demand_state_stability_gate": str(stability_gate),
        })
        _atomic_json(manifest_path, manifest)
        print(f"QUALIFICATION=READY\nMANIFEST={manifest_path}")
        return manifest_path
    except Exception as exc:
        if budget_db.exists():
            try:
                write_api_usage_summary(
                    artifact_dir / "api_usage.json", db_path=budget_db,
                    max_live_grades=max_grades,
                    max_http_calls=explicit_budgets["VALIDATION_MAX_HTTP_CALLS"],
                    max_total_tokens=explicit_budgets["VALIDATION_MAX_TOTAL_TOKENS"],
                )
            except Exception:
                pass
        manifest["qualification"].update({
            "status": "HOLD",
            "failed_at": _utc_now(),
            "reason": str(exc),
        })
        _atomic_json(manifest_path, manifest)
        raise


def _pytest_quarantine_nodes() -> list[str]:
    """Explicit user-approved legacy failures only; no wildcard suppression."""
    path = ROOT / "calibration" / "pytest_quarantine.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes = payload.get("excluded_nodeids")
    if not isinstance(nodes, list) or len(nodes) > 8 or len(nodes) != len(set(nodes)):
        raise ReleaseFailure("pytest_quarantine_must_list_at_most_eight_unique_nodeids")
    if any(
        not isinstance(node, str)
        or not node.startswith("tests/")
        or "::" not in node
        or any(wildcard in node for wildcard in ("*", "?", "[", "]"))
        for node in nodes
    ):
        raise ReleaseFailure("pytest_quarantine_contains_nonexact_nodeid")
    return nodes


def validate(args: argparse.Namespace) -> Path:
    """Offline full pytest, excluding only the exact, documented legacy failures."""
    commit = _git("rev-parse", "HEAD")
    _assert_clean(False)
    nodes = _pytest_quarantine_nodes()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_dir = (args.artifact_dir or DEFAULT_ARTIFACT_ROOT / f"{stamp}_{commit[:12]}_pytest").resolve()
    if artifact_dir.exists() and any(artifact_dir.iterdir()):
        raise ReleaseFailure("validation artifact directory is not empty")
    artifact_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    manifest = _new_manifest(artifact_dir, commit)
    manifest["validation"] = {
        "status": "RUNNING",
        "stages": [],
        "excluded_nodeids": nodes,
        "gate": "offline_full_pytest",
    }
    path = artifact_dir / "manifest.json"
    _atomic_json(path, manifest)
    command = (
        sys.executable, "-B", "-m", "pytest", "-q", "--tb=short",
        "tests", *(f"--deselect={node}" for node in nodes),
    )
    try:
        result = _run(command, env=_deterministic_validation_env(), check=False)
        _record_stage(manifest, "validation", "pytest", result)
        if result.returncode:
            raise ReleaseFailure("pytest_validation_failed")
        manifest["validation"]["status"] = "PASS_WITH_QUARANTINE" if nodes else "PASS"
        _atomic_json(path, manifest)
        print(f"VALIDATION={manifest['validation']['status']}\nMANIFEST={path}")
        return path
    except Exception as exc:
        manifest["validation"]["status"] = "FAIL"
        manifest["validation"]["reason"] = str(exc)
        _atomic_json(path, manifest)
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
    if manifest.get("validation", {}).get("status") not in {"PASS", "PASS_WITH_QUARANTINE"}:
        raise ReleaseFailure("pytest validation is not PASS; deployment is blocked")
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
            "import json; from grading.scoring.runtime_grading_provenance import build_runtime_grading_provenance as b; print(json.dumps(b(), sort_keys=True))",
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

    validate_parser = sub.add_parser("validate", help="offline pytest-only validation for deployment")
    validate_parser.add_argument("--artifact-dir", type=Path)

    qualify_parser = sub.add_parser("qualify", help="optional provider accuracy/stability audit (not a deployment gate)")
    qualify_parser.add_argument("--artifact-dir", type=Path)
    qualify_parser.add_argument("--golden", type=Path, default=ROOT / "calibration" / "expert_accuracy_golden.jsonl")
    qualify_parser.add_argument("--policy", type=Path, default=ROOT / "calibration" / "expert_accuracy_release_policy.json")
    qualify_parser.add_argument("--workers", type=int, choices=range(1, 5), default=1)
    qualify_parser.add_argument("--minimum-predictions", type=int, default=30)
    qualify_parser.add_argument("--stability-runs", type=int, default=2)
    qualify_parser.add_argument(
        "--stability-policy",
        type=Path,
        default=ROOT / "calibration" / "demand_state_stability_policy.json",
    )
    qualify_parser.add_argument("--skip-release-validation", action="store_true", help="deprecated; rejected for READY qualification")
    qualify_parser.add_argument("--allow-dirty", action="store_true", help="development only; never use for deployment evidence")

    deploy_parser = sub.add_parser("deploy", help="deploy a pytest-validated candidate and capture proof")
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
        if args.command == "validate":
            validate(args)
        elif args.command == "qualify":
            qualify(args)
        else:
            deploy(args)
    except Exception as exc:
        print(f"HOLD: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
