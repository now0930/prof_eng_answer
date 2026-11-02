"""Build a source-preserving, undecided 80-Fact packet for ChatGPT review.

This tool performs format/identity checks only. It never decides technical
truth, changes grading eligibility, or edits canonical Topic Packs.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/fact_anchor_independent_verification_audit_20261101.csv"
REVIEW = ROOT / "reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv"
REGISTRY = ROOT / "grading/evidence/approved_fact_registry.json"
OUTPUT = ROOT / "reports/fact_anchor_revision_chatgpt_review_80_20261102.csv"
FIELDS = (
    "fact_id", "topic_id", "anchor_id", "queue_priority",
    "current_topic_pack_statement", "current_registry_statement",
    "latest_source_review_report", "existing_primary_source_urls",
    "chatgpt_review_status", "proposed_statement", "applicable_conditions",
    "reviewed_source_url", "source_locator", "source_support_explanation",
    "reviewer_model", "reviewed_at", "review_notes",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def build_rows() -> list[dict[str, str]]:
    audit = {row["fact_id"]: row for row in read_csv(AUDIT)}
    review = read_csv(REVIEW)
    registry = {
        row["fact_id"]: row
        for row in json.loads(REGISTRY.read_text(encoding="utf-8"))["facts"]
    }
    rows = []
    for item in review:
        if item["latest_report_disposition"] != "REVISE_REQUIRED":
            continue
        fact_id, topic_id, anchor_id = (item[name] for name in ("fact_id", "topic_id", "anchor_id"))
        if audit[fact_id]["final_technical_verdict"] != "REVISE_REQUIRED":
            raise ValueError(f"Unreconciled audit verdict: {fact_id}")
        fact = registry[fact_id]
        if (fact["topic_id"], fact["legacy_anchor_id"]) != (topic_id, anchor_id):
            raise ValueError(f"Registry identity mismatch: {fact_id}")
        pack_path = ROOT / "rubrics/topic_packs" / topic_id / "fact_anchor.json"
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        anchor = next((row for row in pack["anchors"] if row["anchor_id"] == anchor_id), None)
        if anchor is None:
            raise ValueError(f"Missing canonical anchor: {fact_id}")
        urls = sorted({
            ref["url"] for ref in fact.get("verification_refs", [])
            if isinstance(ref, dict) and isinstance(ref.get("url"), str) and ref["url"]
        })
        rows.append({
            "fact_id": fact_id,
            "topic_id": topic_id,
            "anchor_id": anchor_id,
            "queue_priority": item["queue_priority"],
            "current_topic_pack_statement": anchor["statement"],
            "current_registry_statement": fact["statement"],
            "latest_source_review_report": item["latest_review_source"],
            "existing_primary_source_urls": " | ".join(urls),
            "chatgpt_review_status": "UNREVIEWED",
            "proposed_statement": "",
            "applicable_conditions": "",
            "reviewed_source_url": "",
            "source_locator": "",
            "source_support_explanation": "",
            "reviewer_model": "",
            "reviewed_at": "",
            "review_notes": "",
        })
    if len(rows) != 80 or len({row["fact_id"] for row in rows}) != 80:
        raise ValueError("Expected 80 unique revision candidates")
    return rows


def render(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the review packet")
    args = parser.parse_args()
    content = render(build_rows())
    if args.write:
        OUTPUT.write_text(content, encoding="utf-8")
    elif not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
        raise ValueError("ChatGPT review packet is missing or stale")
    print(f"revision_review_packet=80 mode={'write' if args.write else 'check'}")


if __name__ == "__main__":
    main()
