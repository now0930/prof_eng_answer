"""Merge three model-review batches by exact Fact ID; never promote scores."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

if __package__:
    from .export_fact_anchor_revision_review import FIELDS, build_rows, render
    from .validate_fact_anchor_content_review import IMMUTABLE_FIELDS, validate
else:
    from export_fact_anchor_revision_review import FIELDS, build_rows, render
    from validate_fact_anchor_content_review import IMMUTABLE_FIELDS, validate


ROOT = Path(__file__).resolve().parents[1]
BATCHES = (
    ("p0", {"P0"}, ROOT / "reports/fact_anchor_chatgpt_p0_review_rows_20261102.csv"),
    ("p1", {"P1"}, ROOT / "reports/fact_anchor_chatgpt_p1_review_rows_20261102.csv"),
    ("rest", {"DEFER", "SAMPLE"}, ROOT / "reports/fact_anchor_chatgpt_rest_review_rows_20261102.csv"),
)
MERGED = ROOT / "reports/fact_anchor_chatgpt_review_completed_80_20261102.csv"
SOURCE_SNAPSHOT = ROOT / "reports/fact_anchor_revision_chatgpt_review_80_20261102.csv"


def merge() -> list[dict[str, str]]:
    originals = {row["fact_id"]: row for row in build_rows()}
    with SOURCE_SNAPSHOT.open(newline="", encoding="utf-8") as stream:
        snapshot_reader = csv.DictReader(stream)
        if tuple(snapshot_reader.fieldnames or ()) != FIELDS:
            raise ValueError("historical source snapshot schema mismatch")
        snapshot_rows = list(snapshot_reader)
    snapshot = {row["fact_id"]: row for row in snapshot_rows}
    if len(snapshot_rows) != 80 or len(snapshot) != 80:
        raise ValueError("historical source snapshot must contain 80 unique Fact IDs")
    reviewed: dict[str, dict[str, str]] = {}
    for label, priorities, path in BATCHES:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            if tuple(reader.fieldnames or ()) != FIELDS:
                raise ValueError(f"{label} schema mismatch")
            rows = list(reader)
        expected = {fid for fid, row in originals.items() if row["queue_priority"] in priorities}
        actual = {row["fact_id"] for row in rows}
        if len(rows) != len(expected) or actual != expected:
            raise ValueError(f"{label} exact Fact IDs mismatch")
        for row in rows:
            original = snapshot.get(row["fact_id"])
            if original is None or any(
                row[name] != original[name] for name in IMMUTABLE_FIELDS
            ):
                raise ValueError(f"{label} source snapshot mismatch: {row['fact_id']}")
        if actual & reviewed.keys():
            raise ValueError(f"{label} overlaps another batch")
        reviewed.update({row["fact_id"]: row for row in rows})
    # The completed packet is a historical record of the exact source text
    # reviewers saw. Preserve that immutable snapshot and its row order even
    # when current canonical Topic Pack wording later changes.
    return [reviewed[row["fact_id"]] for row in snapshot_rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = render(merge())
    if args.write:
        MERGED.write_text(content, encoding="utf-8")
    elif not MERGED.exists() or MERGED.read_text(encoding="utf-8") != content:
        raise ValueError("Merged review is missing or stale")
    counts = validate(MERGED, source_snapshot=SOURCE_SNAPSHOT)
    print("merged_review_rows=80 " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print("format_only=PASS score_promotion=NONE")


if __name__ == "__main__":
    main()
