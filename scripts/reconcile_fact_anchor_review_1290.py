"""Synchronize the 1,290-ID source audit and fail-closed scoring holds.

The latest review report is a disposition ledger, not permission to promote a
Fact into general scoring.  Previously held KEEP_BOUNDED entries remain held.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv"
REVIEW = ROOT / "reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv"
SOURCE_HOLDS = ROOT / "grading/evidence/fact_anchor_unresolved_source_holds_20261101.json"
REVISION_HOLDS = ROOT / "grading/evidence/fact_anchor_independent_revision_holds_20261101.json"
EXCLUSIONS = ROOT / "grading/evidence/fact_anchor_scoring_exclusions_20261101.json"

SOURCE_REASONS = {
    "HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE": "insufficient_direct_primary_source_scope",
    "SOURCE_CHECKED_SCOPED_STANDARD_HOLD": "source_checked_scoped_standard_not_generic",
    "SOURCE_CHECKED_VENDOR_APPLICATION_HOLD": "source_checked_vendor_application_not_generic",
}


def csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["fact_id"], row["topic_id"], row["anchor_id"]


def unique_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, str]]:
    index = {key(row): row for row in rows}
    if len(index) != len(rows):
        raise ValueError("Duplicate Fact/Topic/Anchor key")
    return index


def build() -> tuple[list[str], list[dict[str, str]], dict, dict, dict]:
    fields, audit = csv_rows(AUDIT)
    _, review = csv_rows(REVIEW)
    audit_by_key, review_by_key = unique_index(audit), unique_index(review)
    if set(audit_by_key) != set(review_by_key) or len(audit) != 1290:
        raise ValueError("The two 1,290-ID ledgers do not have identical keys")

    source = json.loads(SOURCE_HOLDS.read_text(encoding="utf-8"))
    revision = json.loads(REVISION_HOLDS.read_text(encoding="utf-8"))
    exclusion = json.loads(EXCLUSIONS.read_text(encoding="utf-8"))
    previous_source_keys = set(unique_index(source["holds"]))
    exclusion_keys = set(unique_index(exclusion["exclusions"]))
    if len(exclusion_keys) != 276:
        raise ValueError("The original 276 exclusions must not change")

    for row in audit:
        new = review_by_key[key(row)]["latest_report_disposition"]
        if row["final_technical_verdict"] != new:
            row["final_technical_verdict"] = new
            row["new_independent_external_verification"] = "RECONCILED_TO_LATER_SOURCE_REVIEW_2026-11-01"

    revision_keys = {key(row) for row in audit if row["final_technical_verdict"] == "REVISE_REQUIRED"}
    source_keys = {
        key(row) for row in audit
        if row["final_technical_verdict"] in SOURCE_REASONS
        or (row["final_technical_verdict"] == "KEEP_BOUNDED" and key(row) in previous_source_keys)
    }
    if (len(revision_keys), len(source_keys)) != (80, 184):
        raise ValueError("Expected exactly 80 revision and 184 source/promotion holds")
    if revision_keys & source_keys or revision_keys & exclusion_keys or source_keys & exclusion_keys:
        raise ValueError("Scoring overlays overlap")
    if len(revision_keys | source_keys | exclusion_keys) != 540:
        raise ValueError("The 540 fail-closed scoring blocks changed")

    source["holds"] = [
        dict(zip(("fact_id", "topic_id", "anchor_id"), item), reason=(
            "reviewed_but_canonical_promotion_pending"
            if audit_by_key[item]["final_technical_verdict"] == "KEEP_BOUNDED"
            else SOURCE_REASONS[audit_by_key[item]["final_technical_verdict"]]
        ))
        for item in sorted(source_keys)
    ]
    source["purpose"] = "Fail-closed scoring: 112 reviewed but not promoted, 50 insufficient-source, 11 standard-scoped and 11 vendor-scoped holds."
    revision["holds"] = [
        dict(zip(("fact_id", "topic_id", "anchor_id"), item), reason="primary_source_revision_pending")
        for item in sorted(revision_keys)
    ]
    return fields, audit, source, revision, exclusion


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write reconciled audit and manifests")
    args = parser.parse_args()
    fields, audit, source, revision, exclusion = build()
    if args.write:
        with AUDIT.open("w", newline="", encoding="utf-8") as stream:
            stream.write(",".join(fields) + "\n")
            writer = csv.DictWriter(stream, fieldnames=fields, quoting=csv.QUOTE_ALL, lineterminator="\n")
            writer.writerows(audit)
        for path, value in ((SOURCE_HOLDS, source), (REVISION_HOLDS, revision)):
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        _, current_audit = csv_rows(AUDIT)
        if current_audit != audit:
            raise ValueError("Original-source audit differs from the latest review")
        for path, expected in ((SOURCE_HOLDS, source), (REVISION_HOLDS, revision)):
            if json.loads(path.read_text(encoding="utf-8")) != expected:
                raise ValueError(f"Stale scoring hold manifest: {path}")
    print("audit=1290 revision=80 source_or_promotion_hold=184 exclusion=276 blocked=540")
    print("mode=" + ("write" if args.write else "check"))


if __name__ == "__main__":
    main()
