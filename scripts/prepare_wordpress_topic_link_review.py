#!/usr/bin/env python3
"""Create a non-overwriting blank LLM-review template from a catalog export."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
from typing import Any

from validate_wordpress_topic_link_review import BASE_COLUMNS, LLM_COLUMNS


LINK_STATUSES = {"approved", "pending_review", "unmatched"}
IDENTITY_COLUMNS = ("post_id", "link_status", "candidate_topic_id")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_review_template(source: Path, output: Path) -> dict[str, Any]:
    """Copy an export into a blank LLM review CSV without modifying the source."""
    source_path = source.resolve(strict=True)
    output_requested = output.absolute()
    if output_requested.is_symlink():
        raise FileExistsError(f"review template already exists: {output_requested}")
    output_path = output_requested.parent.resolve() / output_requested.name
    if source_path == output_path:
        raise ValueError("review template output must differ from the source CSV")
    if output_path.exists():
        raise FileExistsError(f"review template already exists: {output_path}")
    if not output_path.parent.is_dir():
        raise FileNotFoundError(f"output directory does not exist: {output_path.parent}")

    source_sha256 = _sha256(source_path)
    with source_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != BASE_COLUMNS:
            raise ValueError("source CSV columns do not match the review-export contract")
        rows = list(reader)
    if _sha256(source_path) != source_sha256:
        raise RuntimeError("source CSV changed while the review template was being prepared")

    identities: set[tuple[str, str, str]] = set()
    counts = {status: 0 for status in sorted(LINK_STATUSES)}
    for row_number, row in enumerate(rows, start=2):
        if None in row:
            raise ValueError(f"source CSV row {row_number} has more fields than its header")
        if any(value is None for value in row.values()):
            raise ValueError(f"source CSV row {row_number} has fewer fields than its header")
        identity = tuple(row[column] for column in IDENTITY_COLUMNS)
        if identity in identities:
            raise ValueError(f"duplicate source row identity at row {row_number}: {identity}")
        identities.add(identity)
        status = row["link_status"]
        if status not in LINK_STATUSES:
            raise ValueError(f"unsupported source link status {status!r} at row {row_number}")
        if status in {"approved", "pending_review"} and not row["candidate_topic_id"]:
            raise ValueError(f"source row {row_number} has no candidate Topic ID")
        if status == "unmatched" and row["candidate_topic_id"]:
            raise ValueError(f"unmatched source row {row_number} has a candidate Topic ID")
        counts[status] += 1

    template_rows = [
        {**row, **{column: "" for column in LLM_COLUMNS}}
        for row in rows
    ]
    created = False
    try:
        with output_path.open("x", encoding="utf-8-sig", newline="") as stream:
            created = True
            writer = csv.DictWriter(stream, fieldnames=BASE_COLUMNS + LLM_COLUMNS)
            writer.writeheader()
            writer.writerows(template_rows)
    except Exception:
        if created:
            output_path.unlink(missing_ok=True)
        raise

    return {
        "source": str(source_path),
        "output": str(output_path),
        "source_sha256": source_sha256,
        "output_sha256": _sha256(output_path),
        "rows": len(rows),
        "counts": counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Original catalog review-export CSV")
    parser.add_argument("--output", type=Path, required=True, help="New blank LLM-review CSV; must not exist")
    args = parser.parse_args()
    result = prepare_review_template(args.source, args.output)
    print("WORDPRESS_TOPIC_LINK_REVIEW_TEMPLATE=CREATED")
    print(f"ROWS={result['rows']}")
    for status, count in result["counts"].items():
        print(f"{status.upper()}={count}")
    print(f"SOURCE_SHA256={result['source_sha256']}")
    print(f"OUTPUT_SHA256={result['output_sha256']}")
    print(f"OUTPUT={result['output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
