"""Validate a ChatGPT-completed Fact review CSV without approving its claims."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

if __package__:
    from .export_fact_anchor_revision_review import FIELDS, build_rows
else:
    from export_fact_anchor_revision_review import FIELDS, build_rows


DECISIONS = frozenset({
    "UNREVIEWED", "KEEP_WITH_CORRECTION", "HOLD_INSUFFICIENT_EVIDENCE",
    "EXCLUDE_FROM_GENERAL_SCORING",
})
IMMUTABLE_FIELDS = (
    "fact_id", "topic_id", "anchor_id", "queue_priority",
    "current_topic_pack_statement", "current_registry_statement",
    "latest_source_review_report", "existing_primary_source_urls",
)


def validate(path: Path) -> dict[str, int]:
    expected = {row["fact_id"]: row for row in build_rows()}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("Review CSV schema differs from the generated packet")
        rows = list(reader)
    if len(rows) != 80 or len({row["fact_id"] for row in rows}) != 80:
        raise ValueError("Review CSV must contain 80 unique Fact IDs")
    if {row["fact_id"] for row in rows} != set(expected):
        raise ValueError("Review CSV Fact IDs do not match the 80 held candidates")
    counts = {name: 0 for name in DECISIONS}
    for row in rows:
        fact_id = row["fact_id"]
        if any(row[name] != expected[fact_id][name] for name in IMMUTABLE_FIELDS):
            raise ValueError(f"Original source fields were changed: {fact_id}")
        decision = row["chatgpt_review_status"]
        if decision not in DECISIONS:
            raise ValueError(f"Unknown content-review decision: {fact_id}")
        counts[decision] += 1
        if decision == "UNREVIEWED":
            if any(row[name].strip() for name in FIELDS if name not in IMMUTABLE_FIELDS + ("chatgpt_review_status",)):
                raise ValueError(f"Unreviewed row has review output: {fact_id}")
            continue
        if not row["reviewer_model"].strip() or not row["reviewed_at"].strip():
            raise ValueError(f"Reviewer identity/date missing: {fact_id}")
        try:
            date.fromisoformat(row["reviewed_at"])
        except ValueError as exc:
            raise ValueError(f"Invalid review date: {fact_id}") from exc
        if not row["review_notes"].strip():
            raise ValueError(f"Review rationale missing: {fact_id}")
        if decision == "KEEP_WITH_CORRECTION":
            required = ("proposed_statement", "applicable_conditions", "reviewed_source_url",
                        "source_locator", "source_support_explanation")
            if any(not row[name].strip() for name in required):
                raise ValueError(f"Correction evidence fields missing: {fact_id}")
            parsed = urlparse(row["reviewed_source_url"])
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError(f"Correction source must use an HTTPS URL: {fact_id}")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review_csv", type=Path)
    args = parser.parse_args()
    counts = validate(args.review_csv)
    print("review_rows=80 " + " ".join(f"{name}={counts[name]}" for name in sorted(counts)))
    print("format_only=PASS technical_truth=NOT_EVALUATED score_promotion=NONE")


if __name__ == "__main__":
    main()
