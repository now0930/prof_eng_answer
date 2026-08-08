from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List


COVERAGE_FEEDBACK_EVENT_FILENAME = "coverage_feedback_event.json"
COVERAGE_RETENTION_PLAN_VERSION = "coverage_retention_plan_v1"
DEFAULT_MAX_AGE_DAYS = 90


def _session_event_files(
    sessions_root: str | Path,
) -> List[Path]:
    root = Path(sessions_root)
    if not root.is_dir():
        return []

    rows: List[Path] = []
    for session_dir in sorted(root.iterdir()):
        if not session_dir.is_dir():
            continue
        candidate = session_dir / COVERAGE_FEEDBACK_EVENT_FILENAME
        if candidate.is_file():
            rows.append(candidate)
    return rows


def build_coverage_retention_plan(
    sessions_root: str | Path,
    *,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
    now_epoch: float | None = None,
) -> Dict[str, Any]:
    days = max(1, int(max_age_days))
    now = float(time.time() if now_epoch is None else now_epoch)
    cutoff = now - (days * 86400.0)

    candidates = []
    retained = 0

    for path in _session_event_files(sessions_root):
        try:
            mtime = float(path.stat().st_mtime)
        except OSError:
            continue

        if mtime < cutoff:
            candidates.append(
                {
                    "session_id": path.parent.name,
                    "path": str(path),
                    "mtime_epoch": mtime,
                    "age_days": max(
                        0.0,
                        (now - mtime) / 86400.0,
                    ),
                }
            )
        else:
            retained += 1

    candidates.sort(
        key=lambda row: (
            float(row["mtime_epoch"]),
            str(row["session_id"]),
        )
    )

    return {
        "version": COVERAGE_RETENTION_PLAN_VERSION,
        "sessions_root": str(Path(sessions_root)),
        "max_age_days": days,
        "cutoff_epoch": cutoff,
        "candidate_count": len(candidates),
        "retained_count": retained,
        "candidates": candidates,
        "policy": {
            "default_mode": "dry_run",
            "explicit_apply_required": True,
            "eligible_filename": COVERAGE_FEEDBACK_EVENT_FILENAME,
            "delete_session_directory": False,
            "delete_other_session_artifacts": False,
            "grading_runtime_invocation": False,
            "score_effect": "none",
            "routing_effect": "none",
        },
    }


def apply_coverage_retention_plan(
    plan: Any,
    *,
    apply: bool = False,
) -> Dict[str, Any]:
    if not isinstance(plan, dict):
        raise TypeError("plan must be a dict")

    rows = plan.get("candidates") or []
    if not isinstance(rows, list):
        raise TypeError("plan candidates must be a list")

    deleted: List[str] = []
    skipped: List[str] = []

    for raw in rows:
        if not isinstance(raw, dict):
            continue

        raw_path = str(raw.get("path") or "").strip()
        if not raw_path:
            continue

        path = Path(raw_path)

        # Hard safety boundary: only the exact Stage-8 coverage artifact
        # filename is eligible. Never remove session directories or peers.
        if path.name != COVERAGE_FEEDBACK_EVENT_FILENAME:
            skipped.append(str(path))
            continue

        if not apply:
            skipped.append(str(path))
            continue

        try:
            path.unlink(missing_ok=True)
        except OSError:
            skipped.append(str(path))
            continue

        deleted.append(str(path))

    return {
        "version": "coverage_retention_apply_result_v1",
        "apply": bool(apply),
        "deleted_count": len(deleted),
        "skipped_count": len(skipped),
        "deleted_paths": deleted,
        "skipped_paths": skipped,
        "policy": {
            "explicit_apply_required": True,
            "eligible_filename": COVERAGE_FEEDBACK_EVENT_FILENAME,
            "delete_session_directory": False,
            "delete_other_session_artifacts": False,
            "grading_runtime_invocation": False,
            "score_effect": "none",
            "routing_effect": "none",
        },
    }
