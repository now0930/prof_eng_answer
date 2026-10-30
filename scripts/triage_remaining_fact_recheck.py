#!/usr/bin/env python3
"""Select *unreviewed* approved Facts for general-principle review.

This is a read-only, deterministic queue builder. A priority is not a technical
verdict and never changes the approved Registry or the runtime scoring bank.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re

from validate_selected_fact_recheck_coverage import REPORTS, ROW


ROOT = Path(__file__).resolve().parents[1]

# Signals deliberately over-select. They are review prompts, not assertions of
# error. Company-specific evidence is not itself a general-principle approval.
SIGNALS = (
    ("universal_or_mandatory", re.compile(r"모든|항상|반드시|무조건|필수|유일|일률|universal|always|must|shall|required", re.I)),
    ("numeric_or_formula", re.compile(r"\d|[=≤≥≈∝]|\b(?:pfd|pfh|sil|mttr|mttf|mttd)\b", re.I)),
    ("standard_or_clause", re.compile(r"\b(?:IEC|ISO|ISA|IEEE|API|NFPA|NIST|ASME|EN)\s*[- ]?\d|표준|규격|조항", re.I)),
    ("scope_or_comparison", re.compile(r"조건|범위|한정|비교|보다|따라|경우|적용|depends?|only if|unless|compared", re.I)),
    ("vendor_specific", re.compile(r"Emerson|Fisher|Siemens|Yokogawa|Honeywell|ABB|제품|모델|제조사|매뉴얼", re.I)),
)


def _historically_reviewed(root: Path) -> set[str]:
    with (root / "reports/approved_fact_recheck_triage_20261029.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = {row["fact_id"] for row in rows if row["priority"] != "DEFER"}
    reported = set()
    for path in REPORTS:
        text = (root / "reports" / path.name).read_text(encoding="utf-8")
        reported.update(fact_id for fact_id, _, _ in ROW.findall(text))
    extra = {fact_id for fact_id in reported if fact_id not in selected}
    if len(selected) != 225 or len(extra) != 8:
        raise ValueError(f"historical review coverage changed: selected={len(selected)}, extra={len(extra)}")
    return selected | extra


def triage(root: Path = ROOT, *, sample_per_topic: int = 1) -> tuple[list[dict[str, str]], dict]:
    if sample_per_topic < 0:
        raise ValueError("sample_per_topic must be nonnegative")
    raw = (root / "grading/evidence/approved_fact_registry.json").read_bytes()
    facts = json.loads(raw)["facts"]
    reviewed = _historically_reviewed(root)
    current_ids = {fact["fact_id"] for fact in facts}
    unreviewed = [fact for fact in facts if fact["fact_id"] not in reviewed]
    rows = []
    for fact in unreviewed:
        # Examine the claim and its stated conditions, not merely the title or
        # reference metadata. This is still only a lexical risk screen.
        relation = fact.get("relation") or {}
        statement = fact.get("statement") or ""
        claim = " ".join((statement, " ".join(relation.get("conditions") or [])))
        # A condition field often *limits* a claim. Do not promote such a
        # qualifier to a universal-claim alarm by itself.
        signals = [name for name, pattern in SIGNALS
                   if pattern.search(statement if name == "universal_or_mandatory" else claim)]
        refs = fact.get("verification_refs") or []
        if refs and all(ref.get("authority_type") == "official_documentation" for ref in refs):
            signals.append("vendor_only_evidence_check")
        if not refs:
            signals.append("no_evidence")
        if "universal_or_mandatory" in signals or "no_evidence" in signals:
            priority = "P0"
        elif len(signals) >= 2:
            priority = "P1"
        else:
            priority = "DEFER"
        rows.append({"priority": priority, "fact_id": fact["fact_id"], "topic_id": fact["topic_id"],
                     "anchor_id": fact.get("legacy_anchor_id") or "", "signals": ";".join(signals),
                     "review_status": "UNREVIEWED"})
    by_topic: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["priority"] == "DEFER":
            by_topic[row["topic_id"]].append(row)
    for topic_rows in by_topic.values():
        topic_rows.sort(key=lambda row: hashlib.sha256(row["fact_id"].encode()).hexdigest())
        for row in topic_rows[:sample_per_topic]:
            row["priority"] = "SAMPLE"
            row["signals"] = (row["signals"] + ";" if row["signals"] else "") + "per_topic_sample"
    order = {"P0": 0, "P1": 1, "SAMPLE": 2, "DEFER": 3}
    rows.sort(key=lambda row: (order[row["priority"]], row["topic_id"], row["fact_id"]))
    counts = Counter(row["priority"] for row in rows)
    summary = {
        "contract": "remaining-approved-fact-recheck-triage-v1",
        "registry_sha256": hashlib.sha256(raw).hexdigest(),
        "current_registry_rows": len(facts),
        "historically_reviewed_current_rows": len(reviewed & current_ids),
        "unreviewed_rows": len(rows),
        "priority_counts": {key: counts[key] for key in ("P0", "P1", "SAMPLE", "DEFER")},
        "sample_per_topic": sample_per_topic,
        "score_effect": "none",
        "meaning": "risk triage only; no fact reapproval, no pack or scoring change",
    }
    return rows, summary


def select_batch(rows: list[dict[str, str]], *, size: int = 20, max_per_topic: int = 1) -> list[dict[str, str]]:
    """Pick a bounded, topic-diverse first review batch; no approval semantics."""
    if size < 0 or max_per_topic < 1:
        raise ValueError("size must be nonnegative and max_per_topic positive")
    if size == 0:
        return []
    picked = []
    topic_counts: Counter[str] = Counter()
    for row in rows:
        if row["priority"] == "DEFER" or topic_counts[row["topic_id"]] >= max_per_topic:
            continue
        picked.append(row)
        topic_counts[row["topic_id"]] += 1
        if len(picked) == size:
            break
    return picked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "reports/remaining_fact_recheck_queue_20261030.csv")
    parser.add_argument("--output-json", type=Path, default=ROOT / "reports/remaining_fact_recheck_summary_20261030.json")
    parser.add_argument("--output-batch", type=Path, default=ROOT / "reports/remaining_fact_recheck_first_batch_20261030.csv")
    parser.add_argument("--sample-per-topic", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()
    rows, summary = triage(sample_per_topic=args.sample_per_topic)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("priority", "fact_id", "topic_id", "anchor_id", "signals", "review_status"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with args.output_batch.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("priority", "fact_id", "topic_id", "anchor_id", "signals", "review_status"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(select_batch(rows, size=args.batch_size))
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
