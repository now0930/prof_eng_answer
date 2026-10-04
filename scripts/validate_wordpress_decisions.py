#!/usr/bin/env python3
"""Validate a human WordPress topic-link decision CSV without changing state."""

from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_COLUMNS = [
    "post_id", "post_title", "wordpress_url", "excerpt", "tags", "link_status",
    "candidate_topic_id", "candidate_topic_title", "lexical_score", "matched_terms",
    "assets_json", "review_action", "review_topic_id", "reviewer_notes",
    "decision_status", "confirmed_topic_id", "decision_basis", "follow_up",
]
DECISION_COLUMNS = [
    "suggested_decision", "final_decision", "final_topic_id", "reviewed_by",
    "reviewed_at", "final_evidence", "final_notes",
]
DECISIONS = {"approve", "reject", "defer"}


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return reader.fieldnames, list(reader)


def _key(row: dict[str, str]) -> tuple[str, str, str]:
    return row.get("post_id", ""), row.get("link_status", ""), row.get("candidate_topic_id", "")


def validate_decisions(
    source: Path,
    decisions: Path,
    *,
    topic_pack_root: Path | None = None,
    require_complete: bool = False,
) -> dict[str, Any]:
    """Validate immutable candidate fields and human decision fields."""
    topic_pack_root = topic_pack_root or ROOT / "rubrics" / "topic_packs"
    errors: list[str] = []
    warnings: list[str] = []
    try:
        source_fields, source_rows = _read(source)
        decision_fields, decision_rows = _read(decisions)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "counts": {}}
    expected_source = BASE_COLUMNS
    expected_decisions = BASE_COLUMNS + DECISION_COLUMNS
    if source_fields != expected_source:
        errors.append("source columns do not match confirmed-only contract")
    if decision_fields != expected_decisions:
        errors.append("decision CSV must preserve source columns and append decision columns")
    source_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    decision_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in source_rows:
        key = _key(row)
        if key in source_by_key:
            errors.append(f"duplicate source key: {key}")
        source_by_key[key] = row
    for row in decision_rows:
        key = _key(row)
        if key in decision_by_key:
            errors.append(f"duplicate decision key: {key}")
        decision_by_key[key] = row
    if set(source_by_key) != set(decision_by_key):
        errors.append(
            f"decision keys differ (missing={len(set(source_by_key)-set(decision_by_key))}, "
            f"extra={len(set(decision_by_key)-set(source_by_key))})"
        )
    counts: Counter[str] = Counter()
    for key, row in decision_by_key.items():
        original = source_by_key.get(key)
        if original is None:
            continue
        if any(row.get(column) != original.get(column) for column in BASE_COLUMNS):
            errors.append(f"immutable source field changed: {key}")
        decision = (row.get("final_decision") or "").strip().lower()
        counts[f"decision:{decision or 'pending'}"] += 1
        if not decision:
            if require_complete:
                errors.append(f"missing final_decision: {key}")
            continue
        if decision not in DECISIONS:
            errors.append(f"unsupported final_decision {decision!r}: {key}")
            continue
        topic_id = (row.get("final_topic_id") or "").strip()
        if decision == "approve":
            if topic_id != row.get("candidate_topic_id", ""):
                errors.append(f"approved Topic ID does not match candidate: {key}")
            if not (topic_pack_root / topic_id / "README.md").is_file():
                errors.append(f"approved Topic Pack does not exist: {topic_id}")
        elif topic_id:
            errors.append(f"non-approval must not contain final_topic_id: {key}")
        for field in ("reviewed_by", "reviewed_at", "final_evidence"):
            if not (row.get(field) or "").strip():
                errors.append(f"missing {field}: {key}")
    if counts.get("decision:pending", 0):
        warnings.append("pending decisions are allowed in dry-run and will not be applied")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": dict(sorted(counts.items())),
        "source_rows": len(source_rows),
        "decision_rows": len(decision_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="confirmed-only source CSV")
    parser.add_argument("--decisions", type=Path, required=True, help="human decision CSV")
    parser.add_argument("--require-complete", action="store_true", help="reject blank final_decision cells")
    parser.add_argument("--json", type=Path, help="write a validation report JSON")
    args = parser.parse_args()
    result = validate_decisions(args.source, args.decisions, require_complete=args.require_complete)
    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WORDPRESS_DECISION_VALIDATION={'PASS' if result['valid'] else 'FAIL'}")
    print(f"SOURCE_ROWS={result.get('source_rows', 0)} DECISION_ROWS={result.get('decision_rows', 0)}")
    for name, count in result.get("counts", {}).items():
        print(f"{name.upper()}={count}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
