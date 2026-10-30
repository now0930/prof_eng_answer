#!/usr/bin/env python3
"""Check that the selected Fact review has one traceable verdict per Fact."""

from __future__ import annotations

from collections import Counter
import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TRIAGE = ROOT / "reports/approved_fact_recheck_triage_20261029.csv"
REPORTS = (
    ROOT / "reports/fact_recheck_p0_p1_first40_20261029.md",
    ROOT / "reports/fact_recheck_p1_rest_20261029.md",
    ROOT / "reports/fact_recheck_sample_20261029.md",
)
# The two review batches overlap here. The equation is sound, but the
# Registry's explanatory derivation contains a wrong intermediate step.
RESOLUTIONS = {
    "two_layer_interface_dp_equation_under_submerged_tap_conditions": "EVIDENCE_ONLY_FIX",
}
ROW = re.compile(
    r"^\|\s*(?:\d+|—)\s*\|\s*`?([a-z][a-z0-9_]*)`?\s*\|\s*"
    r"(VERIFIED_AS_IS|CORRECT_STATEMENT_OR_CONDITION|EVIDENCE_ONLY_FIX|RECLASSIFY_INTERNAL|HOLD)\s*\|\s*(.*?)\s*\|\s*$",
    re.M,
)
FINAL_HOLD_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([a-z][a-z0-9_]*)\s*\|", re.M)


def validate() -> dict:
    with TRIAGE.open(encoding="utf-8", newline="") as handle:
        triage = list(csv.DictReader(handle))
    by_id = {row["fact_id"]: row for row in triage}
    if len(by_id) != len(triage):
        raise ValueError("duplicate fact_id in triage")
    # The last HOLD table has no verdict column, so the general ROW parser
    # does not cover it. Its CSV row number is a provenance key, not prose.
    p1_text = REPORTS[1].read_text(encoding="utf-8")
    final_hold_text = p1_text.split("### Final follow-up: remaining unresolved and omitted selected facts", 1)[1]
    final_hold_text = final_hold_text.split("| CSV 행 | Fact ID | 판정 |", 1)[0]
    for csv_line, fact_id in FINAL_HOLD_ROW.findall(final_hold_text):
        line_number = int(csv_line)
        if line_number < 2 or line_number > len(triage) + 1:
            raise ValueError(f"invalid final HOLD CSV row: {line_number}")
        expected_id = triage[line_number - 2]["fact_id"]
        if fact_id != expected_id:
            raise ValueError(
                f"final HOLD row {line_number} Fact ID mismatch: {fact_id} != {expected_id}"
            )
    selected = {row["fact_id"] for row in triage if row["priority"] != "DEFER"}
    parsed = []
    for path in REPORTS:
        if not path.is_file():
            raise ValueError(f"missing review report: {path.name}")
        rows = ROW.findall(path.read_text(encoding="utf-8"))
        if not rows:
            raise ValueError(f"empty review report: {path.name}")
        for fact_id, verdict, evidence in rows:
            if fact_id not in by_id:
                raise ValueError(f"unknown Fact in {path.name}: {fact_id}")
            if not evidence.strip():
                raise ValueError(f"empty evidence for {fact_id}")
            parsed.append((fact_id, verdict, path.name))
    grouped = {}
    for fact_id, verdict, report in parsed:
        grouped.setdefault(fact_id, []).append((verdict, report))
    missing = selected - set(grouped)
    if missing:
        raise ValueError(f"selected Facts lack review: {len(missing)}; first={sorted(missing)[:3]}")
    for fact_id, entries in grouped.items():
        # Adjacent review batches overlap on five rows; repeated identical
        # verdicts are harmless. A HOLD-resolution addendum may also revisit
        # the same Fact in its original report.
        if len(entries) > 1 and fact_id not in RESOLUTIONS and not (
            len({verdict for verdict, _ in entries}) == 1
            or (entries[0][0] == "HOLD" and len({report for _, report in entries}) == 1)
        ):
            raise ValueError(f"ambiguous duplicate review: {fact_id}")
        if fact_id in RESOLUTIONS and RESOLUTIONS[fact_id] not in {v for v, _ in entries}:
            raise ValueError(f"resolution is unsupported: {fact_id}")
    extra = set(grouped) - selected
    trigger_topics = {
        by_id[fact_id]["topic_id"]
        for fact_id, entries in grouped.items()
        if by_id[fact_id]["priority"] == "SAMPLE"
        and entries[-1][0] in {"CORRECT_STATEMENT_OR_CONDITION", "RECLASSIFY_INTERNAL"}
    }
    if any(by_id[fact_id]["priority"] != "DEFER" or by_id[fact_id]["topic_id"] not in trigger_topics for fact_id in extra):
        raise ValueError("adaptive extra Fact is not in a sample-triggered Topic")
    def final_verdict(fact_id: str) -> str:
        return RESOLUTIONS.get(fact_id, grouped[fact_id][-1][0])

    counts = Counter(final_verdict(fact_id) for fact_id in selected)
    extra_counts = Counter(final_verdict(fact_id) for fact_id in extra)
    return {
        "selected": len(selected),
        "selected_reviewed": len(selected & set(grouped)),
        "selected_verdicts": dict(sorted(counts.items())),
        "adaptive_extra": len(extra),
        "adaptive_verdicts": dict(sorted(extra_counts.items())),
        "trigger_topics": sorted(trigger_topics),
        "meaning": "review coverage only; verdict correctness requires cited evidence",
    }


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
