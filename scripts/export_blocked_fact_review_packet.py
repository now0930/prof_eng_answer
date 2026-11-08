"""Export the exact 436 blocked Fact Anchors for external, non-authoritative review.

The export is a read-only projection of public repository sources. It never
changes scoring eligibility or treats a ChatGPT response as approval.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "grading/evidence"
OUTPUT = ROOT / "reports/fact_anchor_blocked_436_chatgpt_20261104.csv"
BATCH_DIR = ROOT / "reports/fact_anchor_blocked_436_chatgpt_batches_20261104"
BATCH_SIZE = 50
FIELDS = (
    "fact_id", "topic_id", "anchor_id", "block_group", "block_reason",
    "current_topic_statement", "current_statement_sha256",
    "current_registry_statement", "registry_verification_status",
    "registry_review_status", "source_basis", "existing_verification_refs_json",
    "latest_review_disposition", "latest_review_report",
    "chatgpt_decision", "proposed_statement", "applicable_conditions",
    "verified_source_url", "source_locator", "source_support_explanation",
    "reviewer_model", "reviewed_at", "review_notes",
)


def _csv_index(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    result = {row["fact_id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"Duplicate Fact ID in {path}")
    return result


def build_rows() -> list[dict[str, str]]:
    manifests = (
        ("revision", EVIDENCE / "fact_anchor_independent_revision_holds_20261101.json", "holds", 80),
        ("source_or_promotion", EVIDENCE / "fact_anchor_unresolved_source_holds_20261101.json", "holds", 80),
        ("general_exclusion", EVIDENCE / "fact_anchor_scoring_exclusions_20261101.json", "exclusions", 276),
    )
    blocked: dict[str, tuple[str, dict]] = {}
    for group, path, field, expected_count in manifests:
        items = json.loads(path.read_text(encoding="utf-8"))[field]
        if len(items) != expected_count:
            raise ValueError(f"Unexpected {group} count: {len(items)}")
        for item in items:
            fact_id = item["fact_id"]
            if fact_id in blocked:
                raise ValueError(f"Overlapping scoring blocks: {fact_id}")
            blocked[fact_id] = group, item
    if len(blocked) != 436:
        raise ValueError(f"Expected 436 blocked Fact IDs, got {len(blocked)}")

    registry_rows = json.loads((EVIDENCE / "approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]
    registry = {row["fact_id"]: row for row in registry_rows}
    if len(registry) != len(registry_rows):
        raise ValueError("Duplicate Registry Fact ID")
    reviews = _csv_index(ROOT / "reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv")
    pack_cache: dict[str, dict[str, dict]] = {}
    rows: list[dict[str, str]] = []
    for fact_id, (group, item) in sorted(blocked.items()):
        fact = registry.get(fact_id)
        if fact is None:
            raise ValueError(f"Missing Registry Fact: {fact_id}")
        topic_id, anchor_id = item["topic_id"], item["anchor_id"]
        if (fact["topic_id"], fact["legacy_anchor_id"]) != (topic_id, anchor_id):
            raise ValueError(f"Registry ownership mismatch: {fact_id}")
        if topic_id not in pack_cache:
            path = ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json"
            anchors = json.loads(path.read_text(encoding="utf-8"))["anchors"]
            pack_cache[topic_id] = {row["anchor_id"]: row for row in anchors}
            if len(pack_cache[topic_id]) != len(anchors):
                raise ValueError(f"Duplicate Topic Anchor: {topic_id}")
        anchor = pack_cache[topic_id].get(anchor_id)
        if anchor is None:
            raise ValueError(f"Missing Topic Anchor: {fact_id}")
        review = reviews.get(fact_id, {})
        refs = [
            {key: ref.get(key, "") for key in ("authority_id", "citation", "url", "edition_or_version", "locator", "supports_claim")}
            for ref in fact.get("verification_refs", []) if isinstance(ref, dict)
        ]
        statement = anchor["statement"]
        rows.append({
            "fact_id": fact_id,
            "topic_id": topic_id,
            "anchor_id": anchor_id,
            "block_group": group,
            "block_reason": item["reason"],
            "current_topic_statement": statement,
            "current_statement_sha256": hashlib.sha256(statement.encode("utf-8")).hexdigest(),
            "current_registry_statement": fact["statement"],
            "registry_verification_status": fact.get("verification_status", ""),
            "registry_review_status": fact.get("review_status", ""),
            "source_basis": (
                anchor.get("source_basis", "")
                if isinstance(anchor.get("source_basis", ""), str)
                else json.dumps(anchor.get("source_basis"), ensure_ascii=False, separators=(",", ":"))
            ),
            "existing_verification_refs_json": json.dumps(refs, ensure_ascii=False, separators=(",", ":")),
            "latest_review_disposition": review.get("latest_report_disposition", ""),
            "latest_review_report": review.get("latest_review_source", ""),
            "chatgpt_decision": "UNREVIEWED",
            "proposed_statement": "",
            "applicable_conditions": "",
            "verified_source_url": "",
            "source_locator": "",
            "source_support_explanation": "",
            "reviewer_model": "",
            "reviewed_at": "",
            "review_notes": "",
        })
    return rows


def render(rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write master and nine 50-row-or-smaller CSV batches")
    args = parser.parse_args()
    rows = build_rows()
    expected = {OUTPUT: render(rows)}
    expected.update({
        BATCH_DIR / f"batch_{index + 1:02d}.csv": render(rows[start:start + BATCH_SIZE])
        for index, start in enumerate(range(0, len(rows), BATCH_SIZE))
    })
    for path, content in expected.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        elif not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise ValueError(f"Missing or stale ChatGPT packet: {path}")
    print(f"blocked={len(rows)} batches={len(expected) - 1} mode={'write' if args.write else 'check'}")


if __name__ == "__main__":
    main()
