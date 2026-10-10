#!/usr/bin/env python3
"""Metadata-only source signal audit for every legacy Topic Pack.

Reads a private WordPress catalog in SQLite read-only mode and writes only
aggregate per-topic counts. Text overlap is a review-priority signal, never an
automatic technical approval.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sqlite3
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "reports" / "full_topic_fact_source_audit_20261010.json"
TOKEN_RE = re.compile(r"[가-힣]{2,}|[A-Za-z0-9]{3,}")


def _tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def _load_catalog(database: Path, source_ids: set[str]) -> dict[str, dict[str, Any]]:
    path = database.resolve()
    if not path.is_file():
        raise FileNotFoundError("private WordPress source catalog not found")
    connection = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        connection.execute("PRAGMA query_only=ON")
        catalog = {}
        for source_id in sorted(source_ids):
            row = connection.execute(
                "SELECT source_id,source_url,version,content_sha256,fetch_status,extracted_text,first_party "
                "FROM sources WHERE source_id=?", (source_id,),
            ).fetchone()
            if row:
                catalog[source_id] = dict(zip(
                    ("source_id", "source_url", "version", "content_sha256", "fetch_status", "extracted_text", "first_party"), row
                ))
        return catalog
    finally:
        connection.close()


def audit_all(root: Path, database: Path) -> dict[str, Any]:
    topic_dir = root / "rubrics" / "topic_packs"
    master_dir = root / "master_topic_packs"
    pack_paths = sorted(topic_dir.glob("*/fact_anchor.json"))
    masters = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in master_dir.glob("*.json")}
    packs = [(path.parent.name, json.loads(path.read_text(encoding="utf-8"))) for path in pack_paths]
    source_ids = {ref["source_id"] for topic, _ in packs for ref in masters.get(topic, {}).get("sources", [])}
    catalog = _load_catalog(database, source_ids)
    totals = {"topics": len(packs), "anchors": 0, "approved_fact_count": len(json.loads((root / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]),
              "anchors_without_first_party_extracted_source": 0, "best_current_signal_ge_80pct": 0,
              "best_current_signal_50_to_79pct": 0, "best_current_signal_lt_50pct": 0,
              "best_stale_signal_ge_80pct": 0, "best_stale_signal_below_80pct": 0,
              "master_source_refs": {"verified": 0, "unverified": 0, "stale": 0, "unavailable": 0}}
    topic_rows = []
    for topic_id, pack in packs:
        master = masters.get(topic_id)
        if not master:
            raise ValueError(f"Master pack missing for {topic_id}")
        refs = master["sources"]
        for ref in refs:
            row = catalog.get(ref["source_id"])
            state = "unavailable"
            if row and row["fetch_status"] == "available" and row.get("content_sha256"):
                expected_url = ref.get("source_url") or ref.get("wordpress_url")
                if expected_url == row["source_url"] and str(ref["version"]) == str(row["version"]):
                    state = "verified" if ref.get("verification_status") == "verified" and ref.get("content_sha256") == row["content_sha256"] else "unverified"
                else:
                    state = "stale"
            elif row and row.get("fetch_status") == "available":
                state = "unavailable"
            totals["master_source_refs"][state] += 1
        eligible_sources = []
        for ref in refs:
            row = catalog.get(ref["source_id"])
            if not row or not row.get("first_party") or row["fetch_status"] != "available" or not row.get("extracted_text"):
                continue
            expected_url = ref.get("source_url") or ref.get("wordpress_url")
            current = expected_url == row["source_url"] and str(ref["version"]) == str(row["version"])
            eligible_sources.append((row["extracted_text"], current))
        counts = {"anchors": 0, "no_first_party_extracted_source": 0, "current_ge_80pct": 0,
                  "current_50_to_79pct": 0, "current_lt_50pct": 0,
                  "stale_ge_80pct": 0, "stale_below_80pct": 0}
        for anchor in pack.get("anchors", []):
            statement = anchor.get("statement", "") if isinstance(anchor, dict) else str(anchor)
            statement = " ".join(str(statement).split())
            tokens = _tokens(statement)
            counts["anchors"] += 1
            if not tokens or not eligible_sources:
                counts["no_first_party_extracted_source"] += 1
                continue
            best_current = max((sum(token in text for token in tokens) / len(tokens) for text, current in eligible_sources if current), default=None)
            best_stale = max((sum(token in text for token in tokens) / len(tokens) for text, current in eligible_sources if not current), default=None)
            if best_current is not None:
                if best_current >= 0.8:
                    counts["current_ge_80pct"] += 1
                elif best_current >= 0.5:
                    counts["current_50_to_79pct"] += 1
                else:
                    counts["current_lt_50pct"] += 1
            elif best_stale is not None:
                if best_stale >= 0.8:
                    counts["stale_ge_80pct"] += 1
                else:
                    counts["stale_below_80pct"] += 1
            else:
                counts["no_first_party_extracted_source"] += 1
        totals["anchors"] += counts["anchors"]
        totals["anchors_without_first_party_extracted_source"] += counts["no_first_party_extracted_source"]
        for name in ("current_ge_80pct", "current_50_to_79pct", "current_lt_50pct", "stale_ge_80pct", "stale_below_80pct"):
            total_name = {"current_ge_80pct": "best_current_signal_ge_80pct", "current_50_to_79pct": "best_current_signal_50_to_79pct", "current_lt_50pct": "best_current_signal_lt_50pct", "stale_ge_80pct": "best_stale_signal_ge_80pct", "stale_below_80pct": "best_stale_signal_below_80pct"}[name]
            totals[total_name] += counts[name]
        topic_rows.append({"topic_id": topic_id, **counts})
    return {"audit_date": "2026-10-10", "method": "whitespace token containment against first-party extracted text; metadata revision checked", "counts_are_not_technical_approval": True, "totals": totals, "topics": topic_rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit_all(ROOT, args.database)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
