#!/usr/bin/env python3
"""Validate an LLM topic-link review CSV against its original export."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_COLUMNS = [
    "post_id", "post_title", "wordpress_url", "excerpt", "tags", "link_status",
    "candidate_topic_id", "candidate_topic_title", "lexical_score", "matched_terms",
    "assets_json", "review_action", "review_topic_id", "reviewer_notes",
]
LLM_COLUMNS = [
    "llm_recommendation", "llm_confidence", "llm_topic_id", "llm_evidence", "llm_notes",
]
RECOMMENDATIONS = {
    "recommend_approve", "recommend_reject", "recommend_link", "retain_approved",
    "unmatched", "manual_review",
}
CONFIDENCE = {"high", "medium", "low"}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return reader.fieldnames, list(reader)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_review_csv(
    source_path: Path,
    review_path: Path,
    *,
    topic_pack_root: Path | None = None,
) -> dict[str, Any]:
    """Validate row identity, preserved source fields, and recommendation contract."""
    topic_pack_root = topic_pack_root or ROOT / "rubrics" / "topic_packs"
    errors: list[str] = []
    warnings: list[str] = []
    redundant_retained_topic_ids = 0
    try:
        source_fields, source_rows = _read_csv(source_path)
        review_fields, review_rows = _read_csv(review_path)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "counts": {}}

    if source_fields != BASE_COLUMNS:
        errors.append("source CSV columns do not match the review-export contract")
    if review_fields != BASE_COLUMNS + LLM_COLUMNS:
        errors.append("review CSV must preserve base columns and append the five llm_* columns")

    def row_key(row: dict[str, str]) -> tuple[str, str, str]:
        return row.get("post_id", ""), row.get("link_status", ""), row.get("candidate_topic_id", "")

    source_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in source_rows:
        key = row_key(row)
        if key in source_by_key:
            errors.append(f"duplicate source row key: {key}")
        source_by_key[key] = row
    review_by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in review_rows:
        key = row_key(row)
        if key in review_by_key:
            errors.append(f"duplicate review row key: {key}")
        review_by_key[key] = row
    if set(source_by_key) != set(review_by_key):
        errors.append(
            f"row identities differ (missing={len(set(source_by_key)-set(review_by_key))}, "
            f"extra={len(set(review_by_key)-set(source_by_key))})"
        )

    counts: Counter[str] = Counter()
    for key, row in review_by_key.items():
        original = source_by_key.get(key)
        if original is None:
            continue
        if any(row.get(column) != original.get(column) for column in BASE_COLUMNS):
            errors.append(f"source data was changed for row {key}")
        if any((row.get(column) or "").strip() for column in ("review_action", "review_topic_id", "reviewer_notes")):
            errors.append(f"LLM filled human-decision fields for row {key}")

        status = row.get("link_status", "")
        recommendation = row.get("llm_recommendation", "")
        confidence = row.get("llm_confidence", "")
        llm_topic_id = (row.get("llm_topic_id") or "").strip()
        counts[f"recommendation:{recommendation}"] += 1
        counts[f"confidence:{confidence}"] += 1
        if recommendation not in RECOMMENDATIONS:
            errors.append(f"unsupported recommendation {recommendation!r} for row {key}")
            continue
        if confidence not in CONFIDENCE:
            errors.append(f"unsupported confidence {confidence!r} for row {key}")
        if not (row.get("llm_evidence") or "").strip():
            errors.append(f"missing evidence for row {key}")
        if status == "approved":
            if recommendation != "retain_approved":
                errors.append(f"approved row is not retained: {key}")
            # Repeating the already-approved Topic ID is redundant but harmless.
            if llm_topic_id and llm_topic_id != row.get("candidate_topic_id"):
                errors.append(f"retain_approved row changes Topic ID: {key}")
            elif llm_topic_id:
                redundant_retained_topic_ids += 1
        elif recommendation == "retain_approved":
            errors.append(f"non-approved row is marked retain_approved: {key}")

        if status == "pending_review":
            if recommendation not in {"recommend_approve", "recommend_reject", "manual_review"}:
                errors.append(f"invalid recommendation for pending candidate: {key}")
            if recommendation == "recommend_approve":
                if confidence != "high":
                    errors.append(f"approval recommendation must have high confidence: {key}")
                if llm_topic_id != row.get("candidate_topic_id"):
                    errors.append(f"approval recommendation Topic ID differs from candidate: {key}")
        elif status == "unmatched":
            if recommendation not in {"recommend_link", "unmatched", "manual_review"}:
                errors.append(f"invalid recommendation for unmatched post: {key}")
            if recommendation == "recommend_link" and confidence != "high":
                errors.append(f"new-link recommendation must have high confidence: {key}")
        elif status not in {"approved", "pending_review", "unmatched"}:
            errors.append(f"unsupported source link status {status!r} for row {key}")

        if recommendation in {"recommend_approve", "recommend_link"} or (status == "approved" and llm_topic_id):
            topic_id = llm_topic_id or row.get("candidate_topic_id", "")
            if not topic_id or not (topic_pack_root / topic_id / "README.md").is_file():
                errors.append(f"recommendation references an unknown Topic Pack {topic_id!r}: {key}")
        elif llm_topic_id:
            errors.append(f"non-link recommendation unexpectedly names a Topic ID: {key}")

    if redundant_retained_topic_ids:
        warnings.append(
            f"{redundant_retained_topic_ids} retain_approved rows repeat their existing Topic ID; "
            "this is redundant and does not imply a new mapping"
        )
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": dict(sorted(counts.items())),
        "source_rows": len(source_rows),
        "review_rows": len(review_rows),
        "source_sha256": _sha256(source_path),
        "review_sha256": _sha256(review_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Original topic-link review export CSV")
    parser.add_argument("--review", type=Path, required=True, help="LLM-enriched review CSV")
    parser.add_argument("--json", type=Path, help="Create a non-overwriting JSON validation report")
    args = parser.parse_args()
    result = validate_review_csv(args.source, args.review)
    if args.json:
        with args.json.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(f"WORDPRESS_TOPIC_LINK_REVIEW_VALIDATION={'PASS' if result['valid'] else 'FAIL'}")
    print(f"SOURCE_ROWS={result.get('source_rows', 0)} REVIEW_ROWS={result.get('review_rows', 0)}")
    for name, count in result.get("counts", {}).items():
        print(f"{name.upper()}={count}")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
