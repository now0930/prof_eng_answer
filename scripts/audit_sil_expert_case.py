#!/usr/bin/env python3
"""Private read-only diagnosis of one reviewed expert accuracy grade.

Does not change labels, facts, grading scores, or any public source. Output
contains identifiers, scores and counts only, never learner answer quotes.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLDEN = ROOT / "calibration/expert_accuracy_golden.jsonl"
LAYERS = (
    "A_structure", "B_requirement_completeness", "C_fact_correctness",
    "D_engineering_judgment", "E_linkage",
)


def analyze(grade: Mapping[str, Any], gold: Mapping[str, Any]) -> dict[str, Any]:
    labels = gold["labels"]
    expected = {str(row["demand_id"]): str(row["status"]).upper()
                for row in labels["demands"]}
    requirements = grade.get("requirements") or []
    actual = {str(row.get("requirement_id")): str(row.get("status")).upper()
              for row in requirements if isinstance(row, Mapping)}
    matched = [key for key in expected if key in actual]
    breakdown = (grade.get("deterministic_score") or {}).get("score_breakdown") or {}
    de = grade.get("qualitative_de_evaluation") or {}
    bounds = labels.get("score_range") or {}
    total = grade.get("total_score")
    finite_total = isinstance(total, (int, float)) and not isinstance(total, bool) and math.isfinite(total)
    lower = bounds.get("min")
    upper = bounds.get("max")
    gap = (round(lower - total, 4) if finite_total and isinstance(lower, (int, float))
           and total < lower else round(total - upper, 4)
           if finite_total and isinstance(upper, (int, float)) and total > upper else 0.0
           if finite_total else None)
    expected_fatals = [row["finding_id"] for row in labels.get("findings", [])
                       if row.get("severity") == "fatal"]
    observed_fatals = [
        str(row.get("rule_id") or row.get("finding_id") or "")
        for row in (grade.get("logic_check_evaluation") or {}).get("findings", [])
        if isinstance(row, Mapping) and
        str(row.get("severity") or row.get("classification")).lower() == "fatal"
    ]
    return {
        "case_id": gold["case_id"],
        "grade_marker": grade.get("marker"),
        "grade_total": total,
        "expert_range": bounds,
        "outside_expert_range_by": gap,
        "layer_scores": {key: breakdown.get(key) for key in LAYERS},
        "requirement_count": len(requirements),
        "expert_demand_status": expected,
        "directly_matched_demand_status": {
            key: {"expert": expected[key], "grade": actual[key]}
            for key in matched
        },
        "unmapped_expert_demand_ids": [key for key in expected if key not in matched],
        "grade_requirement_status_counts": {
            status: sum(str(row.get("status")).upper() == status
                        for row in requirements if isinstance(row, Mapping))
            for status in ("SATISFIED", "PARTIAL", "MISSING", "WRONG", "UNKNOWN")
        },
        "evidence_recall_diagnostic": grade.get("evidence_recall_diagnostic"),
        "fatal_gold_ids": expected_fatals,
        "fatal_grade_ids": observed_fatals,
        "argon_mode": de.get("mode"),
        "argon_status": de.get("status"),
        "argon_reason_code": de.get("reason_code"),
        "argon_provider_calls": de.get("provider_calls"),
        "argon_proposed_scores": de.get("proposed_scores"),
        "argon_effective_scores": de.get("effective_scores"),
        "argon_criteria_scores": {
            str(row.get("criterion_id")): row.get("score")
            for row in de.get("criteria", []) if isinstance(row, Mapping)
        },
        "resolution_review": grade.get("resolution_review"),
        "assessment": (
            "Diagnostic only. Distinguish answer deficits, missed spans and "
            "expert label scope through independent source-grounded review. "
            "Never use this report to adjust scores or auto-approve facts."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grade-json", type=Path, required=True)
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--case-id", default="sil_target_operations_issue1")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    grade = json.loads(args.grade_json.read_text(encoding="utf-8"))
    gold = next((
        json.loads(line) for line in args.golden.read_text(encoding="utf-8").splitlines()
        if line.strip() and json.loads(line).get("case_id") == args.case_id
    ), None)
    if not isinstance(gold, dict):
        raise SystemExit("case_id not found in reviewed Golden Set")
    result = analyze(grade, gold)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
