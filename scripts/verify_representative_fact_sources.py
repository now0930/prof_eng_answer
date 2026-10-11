#!/usr/bin/env python3
"""Repeat metadata/text-signal checks against a private, read-only WP catalog.

Prints no extracted text, credentials or database path. A match is not approval.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from study.wordpress_fact_projection import load_source_catalog_read_only
from grading.evidence.approved_fact_registry import load_approved_fact_registry


SIGNALS = {
    "sil_target_band_after_metric": ("목표 PFD 또는 PFH", "SIL 구간을 판정"),
    "v_model_design_test_mapping": ("V-모델(V-Model)", "설계 단계와 테스트 단계를"),
    "nyquist_minus_one_critical_point": ("Nyquist Critical Point", "-1+j0"),
}


def audit_catalog(root: Path, catalog: dict[str, dict]) -> dict[str, object]:
    facts = load_approved_fact_registry(root)["facts"]
    outcomes = []
    for fact in facts:
        if not fact["source_refs"]:
            outcomes.append({
                "fact_id": fact["fact_id"],
                "metadata_match": None,
                "text_signal_match": None,
                "source_approved": None,
                "fact_approved": fact["review_status"] == "approved",
                "source_audit": "not_applicable_independently_verified",
            })
            continue
        ref = fact["source_refs"][0]
        master = json.loads((root / "master_topic_packs" / f"{fact['topic_id']}.json").read_text(encoding="utf-8"))
        source = next(row for row in master["sources"] if row["source_id"] == ref["source_id"])
        row = catalog.get(ref["source_id"])
        metadata_match = bool(row) and (
            row["fetch_status"] == "available"
            and row["source_url"] == source["source_url"]
            and str(row["version"]) == str(source["version"]) == ref["source_version"]
            and row["content_sha256"] == ref["source_sha256"]
        )
        body = row.get("extracted_text") if row else None
        text_signal_match = isinstance(body, str) and all(signal in body for signal in SIGNALS[fact["fact_id"]])
        outcomes.append({
            "fact_id": fact["fact_id"],
            "metadata_match": metadata_match,
            "text_signal_match": text_signal_match,
            "source_approved": source["verification_status"] == "verified",
            "fact_approved": fact["review_status"] == "approved",
            "source_audit": "checked",
        })
    source_backed = [row for row in outcomes if row["source_audit"] == "checked"]
    return {"outcomes": outcomes, "all_source_signals_match": all(
        row["metadata_match"] and row["text_signal_match"] for row in source_backed),
        "runtime_scoring_enabled": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    args = parser.parse_args()
    facts = load_approved_fact_registry(ROOT)["facts"]
    catalog = load_source_catalog_read_only(
        args.database,
        {fact["source_refs"][0]["source_id"] for fact in facts if fact["source_refs"]},
    )
    print(json.dumps(audit_catalog(ROOT, catalog), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
