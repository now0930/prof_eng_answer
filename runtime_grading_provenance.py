"""Process-stable provenance for final grading results."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import subprocess
from typing import Any


PROVENANCE_VERSION = "runtime_grading_provenance_v1"
SCORING_POLICY_VERSION = "stage23_generic_grading_contract_v1"
PROVENANCE_FIELDS = (
    "engine_commit",
    "engine_process_started_at",
    "router_version",
    "evaluator_sha",
    "verifier_sha",
    "scoring_policy_version",
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def _sha256_file(path: Path) -> str:
    try:
        return hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    except OSError:
        return "UNAVAILABLE"


def _git_head(root: Path) -> str:
    configured = str(
        os.getenv("ENGINE_COMMIT") or ""
    ).strip()
    if configured:
        return configured

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "rev-parse",
                "HEAD",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (
        OSError,
        subprocess.SubprocessError,
    ):
        return "UNAVAILABLE"

    return (
        result.stdout.strip()
        or "UNAVAILABLE"
    )


_MODULE_ROOT = Path(__file__).resolve().parent
_ENGINE_PROCESS_STARTED_AT = _utc_now_iso()
_ENGINE_COMMIT = _git_head(_MODULE_ROOT)
_ROUTER_VERSION = (
    "sha256:"
    + _sha256_file(
        _MODULE_ROOT / "question_type_router.py"
    )
)
_EVALUATOR_SHA = _sha256_file(
    _MODULE_ROOT / "logic_check_evaluator.py"
)
_VERIFIER_SHA = _sha256_file(
    _MODULE_ROOT / "logic_llm_verifier.py"
)


def build_runtime_grading_provenance() -> dict[str, str]:
    """Return a fresh copy of one process-stable snapshot."""
    return {
        "engine_commit": _ENGINE_COMMIT,
        "engine_process_started_at": (
            _ENGINE_PROCESS_STARTED_AT
        ),
        "router_version": _ROUTER_VERSION,
        "evaluator_sha": _EVALUATOR_SHA,
        "verifier_sha": _VERIFIER_SHA,
        "scoring_policy_version": (
            SCORING_POLICY_VERSION
        ),
    }


def attach_runtime_grading_provenance(
    grade: Mapping[str, Any] | Any,
) -> Any:
    """Return an enriched copy without mutating its source."""
    if not isinstance(grade, Mapping):
        return grade

    output = dict(grade)
    output["runtime_grading_provenance"] = (
        build_runtime_grading_provenance()
    )
    return output


def attach_runtime_provenance_to_pipeline_result(
    value: Any,
    is_grade_dict: Callable[[Any], bool],
) -> Any:
    """Recursively enrich grade elements in a pipeline result."""
    if is_grade_dict(value):
        return attach_runtime_grading_provenance(
            value
        )

    if isinstance(value, list):
        return [
            attach_runtime_provenance_to_pipeline_result(
                item,
                is_grade_dict,
            )
            for item in value
        ]

    if isinstance(value, tuple):
        return tuple(
            attach_runtime_provenance_to_pipeline_result(
                item,
                is_grade_dict,
            )
            for item in value
        )

    if isinstance(value, dict):
        return {
            key: attach_runtime_provenance_to_pipeline_result(
                item,
                is_grade_dict,
            )
            for key, item in value.items()
        }

    return value
