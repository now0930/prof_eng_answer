#!/usr/bin/env python3
"""Deterministically select approved Facts for evidence recheck.

Signals are review priorities, never technical verdicts. The private WordPress
catalog is not opened and no scoring or approval state is changed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "grading/evidence/approved_fact_registry.json"
PACKS = ROOT / "rubrics/topic_packs"
KNOWN_CONDITION_RECHECK = {
    ("second_order_system_resonance_frequency_response", "F2"),
    ("second_order_system_resonance_frequency_response", "F3"),
    ("second_order_lag_response_by_damping_ratio", "so2_overdamped_response"),
}
GENERIC_LOCATOR = re.compile(r"^(?:scope|overview|abstract|introduction|home(?: ?page)?)$", re.I)
FIELDS = ("priority", "fact_id", "topic_id", "anchor_id", "reasons")


def _anchors(root: Path) -> dict[str, tuple[str, dict]]:
    result = {}
    for path in sorted((root / "rubrics/topic_packs").glob("*/fact_anchor.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        for anchor in pack["anchors"]:
            anchor_id = anchor["anchor_id"]
            if anchor_id in result:
                raise ValueError(f"duplicate source Anchor ID: {anchor_id}")
            result[anchor_id] = (path.parent.name, anchor)
    return result


def triage(root: Path, *, sample_per_topic: int = 1) -> tuple[list[dict[str, str]], dict]:
    if sample_per_topic < 0:
        raise ValueError("sample_per_topic cannot be negative")
    registry_path = root / "grading/evidence/approved_fact_registry.json"
    raw = registry_path.read_bytes()
    facts = json.loads(raw)["facts"]
    anchors = _anchors(root)
    by_anchor = Counter(fact.get("legacy_anchor_id") for fact in facts)
    rows = []
    for fact in facts:
        anchor_id = fact.get("legacy_anchor_id") or ""
        matched = anchors.get(anchor_id)
        reasons = []
        if not matched:
            reasons.append("anchor_missing")
        elif matched[0] != fact["topic_id"]:
            reasons.append("anchor_topic_mismatch")
        if anchor_id and by_anchor[anchor_id] > 1:
            reasons.append("multiple_facts_one_anchor")
        if (fact["topic_id"], anchor_id) in KNOWN_CONDITION_RECHECK:
            reasons.append("known_condition_issue")
        refs = fact.get("verification_refs", [])
        if not refs:
            reasons.append("no_verification_ref")
        elif all(ref["authority_type"] == "calculation" for ref in refs):
            reasons.append("calculation_only")
        if any(ref.get("url") is None and ref["authority_type"] != "calculation" for ref in refs):
            reasons.append("noncalculation_without_url")
        if any(len(ref["locator"].strip()) < 15 or GENERIC_LOCATOR.fullmatch(ref["locator"].strip()) for ref in refs):
            reasons.append("coarse_locator")
        critical = {"anchor_missing", "anchor_topic_mismatch", "known_condition_issue", "no_verification_ref"}
        priority = "P0" if critical.intersection(reasons) else "P1" if reasons else "DEFER"
        rows.append({
            "priority": priority,
            "fact_id": fact["fact_id"],
            "topic_id": fact["topic_id"],
            "anchor_id": anchor_id,
            "reasons": ";".join(reasons),
        })

    # A small per-topic quality-control sample guards against systematic blind
    # spots without re-reading every previously verified Fact.
    candidates: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["priority"] == "DEFER":
            candidates[row["topic_id"]].append(row)
    for topic_rows in candidates.values():
        topic_rows.sort(key=lambda row: hashlib.sha256(row["fact_id"].encode()).hexdigest())
        for row in topic_rows[:sample_per_topic]:
            row["priority"] = "SAMPLE"
            row["reasons"] = "per_topic_quality_sample"

    order = {"P0": 0, "P1": 1, "SAMPLE": 2, "DEFER": 3}
    rows.sort(key=lambda row: (order[row["priority"]], row["topic_id"], row["fact_id"]))
    counts = Counter(row["priority"] for row in rows)
    signals = Counter(reason for row in rows for reason in row["reasons"].split(";") if reason)
    summary = {
        "contract": "approved-fact-recheck-triage-v1",
        "registry_sha256": hashlib.sha256(raw).hexdigest(),
        "total_fact_rows": len(facts),
        "unique_anchor_ids": len({row["anchor_id"] for row in rows if row["anchor_id"]}),
        "priority_counts": {key: counts[key] for key in ("P0", "P1", "SAMPLE", "DEFER")},
        "signal_counts": dict(sorted(signals.items())),
        "review_queue_rows": counts["P0"] + counts["P1"] + counts["SAMPLE"],
        "deferred_rows": counts["DEFER"],
        "sample_per_topic": sample_per_topic,
        "meaning": "metadata and lineage triage only; no technical fact reapproval or score change",
    }
    return rows, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "reports/approved_fact_recheck_triage_20261029.csv")
    parser.add_argument("--output-json", type=Path, default=ROOT / "reports/approved_fact_recheck_summary_20261029.json")
    parser.add_argument("--sample-per-topic", type=int, default=1)
    args = parser.parse_args()
    rows, summary = triage(ROOT, sample_per_topic=args.sample_per_topic)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
