"""Validate a returned ChatGPT CSV against the immutable blocked-Fact packet.

Format validation only: a passing result does not approve or unblock any Fact.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.export_blocked_fact_review_packet import BATCH_SIZE, FIELDS, build_rows


REVIEW_FIELDS = frozenset({
    "chatgpt_decision", "proposed_statement", "applicable_conditions",
    "verified_source_url", "source_locator", "source_support_explanation",
    "reviewer_model", "reviewed_at", "review_notes",
})
DECISIONS = frozenset({
    "UNREVIEWED", "GENERAL_CANDIDATE", "REVISE_CANDIDATE", "SCOPED_ONLY",
    "NONCORE", "DUPLICATE", "HOLD_EVIDENCE", "INCORRECT",
})


def validate(path: Path, *, batch: int | None = None, require_all: bool = False) -> dict[str, int]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("CSV columns/order differ from the review contract")
        rows = list(reader)
    all_rows = build_rows()
    baseline = {row["fact_id"]: row for row in all_rows}
    if not rows or len(rows) > len(baseline):
        raise ValueError("Invalid review row count")
    seen = set()
    counts: dict[str, int] = {}
    for row in rows:
        fact_id = row["fact_id"]
        if fact_id in seen or fact_id not in baseline:
            raise ValueError(f"Duplicate or unknown Fact ID: {fact_id}")
        seen.add(fact_id)
        for field in FIELDS:
            if field not in REVIEW_FIELDS and row[field] != baseline[fact_id][field]:
                raise ValueError(f"Original field changed: {fact_id}.{field}")
        decision = row["chatgpt_decision"]
        if decision not in DECISIONS:
            raise ValueError(f"Invalid decision: {fact_id}")
        if decision in {"GENERAL_CANDIDATE", "REVISE_CANDIDATE"}:
            required = ("verified_source_url", "source_locator", "source_support_explanation", "reviewer_model", "reviewed_at")
            if any(not row[field].strip() for field in required):
                raise ValueError(f"Source-grounded review incomplete: {fact_id}")
        if decision == "REVISE_CANDIDATE" and not row["proposed_statement"].strip():
            raise ValueError(f"Missing proposed statement: {fact_id}")
        counts[decision] = counts.get(decision, 0) + 1
    if batch is not None:
        if not 1 <= batch <= 9:
            raise ValueError("Batch number must be 1 through 9")
        expected = {row["fact_id"] for row in all_rows[(batch - 1) * BATCH_SIZE:batch * BATCH_SIZE]}
        if seen != expected:
            raise ValueError(f"Batch {batch} has missing or unexpected Fact IDs")
    if require_all and seen != set(baseline):
        raise ValueError("Full review has missing Fact IDs")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review_csv", type=Path)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--batch", type=int, help="require the exact IDs in batch 1–9")
    scope.add_argument("--all", action="store_true", help="require all 436 Fact IDs")
    args = parser.parse_args()
    counts = validate(args.review_csv, batch=args.batch, require_all=args.all)
    print("FORMAT_VALID_ONLY rows=" + str(sum(counts.values())))
    for decision, count in sorted(counts.items()):
        print(f"{decision}={count}")


if __name__ == "__main__":
    main()
