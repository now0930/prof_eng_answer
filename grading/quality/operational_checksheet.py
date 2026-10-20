"""Score-neutral, private operational checksheet for deterministic grading.

The sheet identifies review work, not factual truth. It must never be an input
to the A/B/C/D/E score owner or be committed with personal session history.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


VERSION = "grading-quality-checksheet-v1"
FILE_NAME = "quality_checksheet.json"
_REVIEW = "needs_review"


def _fingerprint(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_quality_checksheet(grade: dict[str, Any], *, created_at: str | None = None) -> dict:
    """Build deterministic diagnostics without copying question or answer text."""
    if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
        raise ValueError("checksheet requires deterministic-primary grade")
    topic_id = str(grade.get("topic_id") or "")
    if not topic_id:
        raise ValueError("grade has no primary Topic")
    created = created_at or _utc_now()
    scope = grade.get("question_scope_evaluation") or {}
    recall = grade.get("evidence_recall_diagnostic") or {}
    extraction = grade.get("canonical_claim_extraction") or {}
    score = grade.get("deterministic_score") or {}
    fatal = bool((grade.get("logic_check_evaluation") or {}).get("fatal_error_detected"))
    cross_topic = grade.get("cross_topic_evidence") or {}
    llm_audit = cross_topic.get("llm_evidence_audit") or {}
    diagnostic_provider_only = bool(
        llm_audit.get("score_effect") == "none"
        and llm_audit.get("provider_calls") == grade.get("provider_calls")
        and all(row.get("score_effect") == "none" for row in cross_topic.get("llm_evidence_suggestions") or [])
    )
    score_consistent = (
        score.get("decision") == "SCORED"
        and grade.get("total_score") == score.get("total_score")
        and grade.get("llm_verdict_authority") == 0
        and (grade.get("provider_calls") == 0 or diagnostic_provider_only)
    )
    checks = [
        {"check_id": "score_authority", "result": "pass" if score_consistent else "fail",
         "category": "system_defect", "priority": "P0",
         "metric": {"deterministic_score_matches": score_consistent},
         "retest_rule": "same fixed input and revision preserve deterministic score authority"},
        {"check_id": "fatal_verdict_consistency",
         "result": "pass" if not fatal or grade.get("official_pass_met") is False else "fail",
         "category": "system_defect", "priority": "P0",
         "metric": {"fatal_detected": fatal, "official_pass_met": grade.get("official_pass_met")},
         "retest_rule": "fatal finding never yields official pass"},
        {"check_id": "question_scope", "result": "pass" if scope.get("exact") else _REVIEW,
         "category": "scope_gap", "priority": "P1",
         "metric": {"exact": bool(scope.get("exact")), "resolved": bool(scope.get("resolved"))},
         "retest_rule": "legacy explicit question contract is resolved; Fact completeness is separate"},
        {"check_id": "evidence_recall", "result": _REVIEW if recall.get("warning") else "pass",
         "category": "evidence_gap", "priority": "P1",
         "metric": {"warning": bool(recall.get("warning")),
                    "missing_requirement_count": int(recall.get("missing_requirement_count") or 0)},
         "retest_rule": "review accepted paraphrases and false-positive mutations"},
        {"check_id": "unresolved_claims",
         "result": _REVIEW if int(extraction.get("unresolved_span_count") or 0) else "pass",
         "category": "parser_gap", "priority": "P2",
         "metric": {"count": int(extraction.get("unresolved_span_count") or 0)},
         "retest_rule": "classify unresolved spans; do not auto-credit or penalize them"},
    ]
    issues = [{
        "issue_id": check["check_id"], "check_id": check["check_id"],
        "category": check["category"], "priority": check["priority"],
        "status": "open", "finding": check["result"],
        "fix_reference": None, "review_note": None,
        "retest_sheet_sha256": None, "updated_at": created,
    } for check in checks if check["result"] != "pass"]
    return {
        "schema_version": VERSION, "created_at": created,
        "topic_id": topic_id, "topic_ids": list(grade.get("topic_ids") or [topic_id]),
        "grade_sha256": _fingerprint(grade), "score_effect": "none",
        "checks": checks, "issues": issues, "audit": [],
    }


def save_quality_checksheet(session_dir: str | Path, sheet: dict,
                            *, overwrite: bool = False) -> Path:
    """Atomically save beside a private grade; never follow an existing symlink."""
    session = Path(session_dir)
    if not session.is_dir() or not (session / "deterministic_grade.json").is_file():
        raise ValueError("private deterministic grade session required")
    path = session / FILE_NAME
    if path.is_symlink() or (path.exists() and not overwrite):
        raise ValueError("checksheet exists or is a symlink")
    if sheet.get("schema_version") != VERSION or sheet.get("score_effect") != "none":
        raise ValueError("invalid score-neutral checksheet")
    grade = json.loads((session / "deterministic_grade.json").read_text(encoding="utf-8"))
    if sheet.get("grade_sha256") != _fingerprint(grade):
        raise ValueError("checksheet grade snapshot mismatch")
    raw = json.dumps(sheet, ensure_ascii=False, indent=2, allow_nan=False)
    descriptor, tmp_name = tempfile.mkstemp(prefix=".quality_checksheet_", dir=session)
    tmp_path = Path(tmp_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(raw)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
    return path


def load_quality_checksheet(session_dir: str | Path) -> dict:
    path = Path(session_dir) / FILE_NAME
    if path.is_symlink() or not path.is_file():
        raise ValueError("private checksheet not found")
    sheet = json.loads(path.read_text(encoding="utf-8"))
    if sheet.get("schema_version") != VERSION or sheet.get("score_effect") != "none":
        raise ValueError("invalid checksheet")
    grade_path = Path(session_dir) / "deterministic_grade.json"
    if not grade_path.is_file() or grade_path.is_symlink():
        raise ValueError("deterministic grade snapshot is missing")
    grade = json.loads(grade_path.read_text(encoding="utf-8"))
    if sheet.get("grade_sha256") != _fingerprint(grade):
        raise ValueError("checksheet grade snapshot mismatch")
    return sheet


_TRANSITIONS = {
    "open": {"triaged", "deferred"},
    "triaged": {"fix_pending_retest", "deferred"},
    "deferred": {"triaged"},
    "fix_pending_retest": {"retested", "triaged"},
    "retested": {"closed", "triaged"},
    "closed": set(),
}


def add_manual_issue(sheet: dict, *, category: str, priority: str,
                     note: str, recorded_at: str | None = None) -> dict:
    """Record a human-observed grading defect without making it a score input."""
    if category not in {"benchmark_conflict", "false_high", "false_low", "wrong_route", "missing_fact",
                        "source_conflict", "formatting", "other"}:
        raise ValueError("invalid manual issue category")
    if priority not in {"P0", "P1", "P2", "P3"}:
        raise ValueError("invalid manual issue priority")
    if not isinstance(note, str) or not note.strip():
        raise ValueError("manual issue note required")
    now = recorded_at or _utc_now()
    existing = {row["issue_id"] for row in sheet.get("issues", [])}
    index = 1
    while f"manual_{index:03d}" in existing:
        index += 1
    issue_id = f"manual_{index:03d}"
    sheet["issues"].append({
        "issue_id": issue_id, "check_id": None, "category": category,
        "priority": priority, "status": "open", "finding": "manual_report",
        "fix_reference": None, "review_note": note.strip(),
        "retest_sheet_sha256": None, "updated_at": now,
    })
    sheet["audit"].append({"issue_id": issue_id, "from": None, "to": "open",
                           "changed_at": now, "note": note.strip(),
                           "fix_reference": None, "retest_sheet_sha256": None})
    return sheet


def reclassify_issue(sheet: dict, *, issue_id: str, category: str,
                     note: str, changed_at: str | None = None) -> dict:
    """Correct a premature diagnosis while retaining the original audit trail."""
    if category not in {"benchmark_conflict", "false_high", "false_low", "wrong_route",
                        "missing_fact", "source_conflict", "formatting", "other"}:
        raise ValueError("invalid issue category")
    if not isinstance(note, str) or not note.strip():
        raise ValueError("reclassification note required")
    rows = [row for row in sheet.get("issues", []) if row.get("issue_id") == issue_id]
    if len(rows) != 1:
        raise ValueError("issue ID not found or duplicated")
    issue = rows[0]
    old_category = issue["category"]
    if old_category == category:
        raise ValueError("issue category is unchanged")
    now = changed_at or _utc_now()
    issue.update(category=category, review_note=note.strip(), updated_at=now)
    sheet["audit"].append({"issue_id": issue_id,
                           "from_category": old_category, "to_category": category,
                           "changed_at": now, "note": note.strip()})
    return sheet


def advance_issue(sheet: dict, *, issue_id: str, status: str, note: str,
                  fix_reference: str | None = None, retest_sheet: dict | None = None,
                  changed_at: str | None = None) -> dict:
    """Require a distinct passing retest before calling any issue retested."""
    if not isinstance(note, str) or not note.strip():
        raise ValueError("review note required")
    rows = [row for row in sheet.get("issues", []) if row.get("issue_id") == issue_id]
    if len(rows) != 1:
        raise ValueError("issue ID not found or duplicated")
    issue = rows[0]
    previous = issue["status"]
    if status not in _TRANSITIONS.get(previous, set()):
        raise ValueError("invalid issue status transition")
    if status == "fix_pending_retest" and not (fix_reference and fix_reference.strip()):
        raise ValueError("fix reference required")
    retest_hash = None
    if status == "retested":
        if not isinstance(retest_sheet, dict) or retest_sheet.get("schema_version") != VERSION:
            raise ValueError("retest checksheet required")
        if retest_sheet.get("topic_id") != sheet.get("topic_id"):
            raise ValueError("retest Topic mismatch")
        if retest_sheet.get("grade_sha256") == sheet.get("grade_sha256"):
            raise ValueError("retest must use a new grade snapshot")
        if issue["check_id"] is not None:
            checks = [row for row in retest_sheet.get("checks", [])
                      if row.get("check_id") == issue["check_id"]]
            if len(checks) != 1 or checks[0].get("result") != "pass":
                raise ValueError("retest check has not passed")
        elif not issue.get("fix_reference"):
            raise ValueError("manual retest requires recorded fix reference")
        retest_hash = _fingerprint(retest_sheet)
    now = changed_at or _utc_now()
    issue.update(status=status, review_note=note.strip(), updated_at=now)
    if fix_reference:
        issue["fix_reference"] = fix_reference.strip()
    if retest_hash:
        issue["retest_sheet_sha256"] = retest_hash
    sheet["audit"].append({"issue_id": issue_id, "from": previous, "to": status,
                           "changed_at": now, "note": note.strip(),
                           "fix_reference": issue["fix_reference"],
                           "retest_sheet_sha256": retest_hash})
    return sheet
