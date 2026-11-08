#!/usr/bin/env python3
"""Read-only, redacted report for failed production qualification cases.

Does not regrade, change expert labels, print answers/provider responses, or
authorize READY/deployment. Operate only on private provider_prediction files.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")
LAYERS = ("A_structure", "B_requirement_completeness", "C_fact_correctness",
          "D_engineering_judgment", "E_linkage")
STATUS = {"CORRECT": "SATISFIED", "SATISFIED": "SATISFIED",
          "INCORRECT": "WRONG", "WRONG": "WRONG",
          "PARTIAL": "PARTIAL", "MISSING": "MISSING"}


def safe_id(value: Any) -> str | None:
    value = str(value or "")
    # IDs are used as private directory components. A dot-path is never safe.
    return value if value not in {".", ".."} and ID.fullmatch(value) else None


def number(value: Any) -> float | None:
    return float(value) if not isinstance(value, bool) and isinstance(
        value, (int, float)) and math.isfinite(value) else None


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def analyze_failures(golden: list[dict], rows: list[dict],
                     grades: Mapping[str, Mapping]) -> dict:
    gold = {c["case_id"]: c for c in golden}
    if len(gold) != len(golden) or len({
        row.get("case_id") for row in rows
    }) != len(rows):
        raise ValueError("duplicate benchmark case ID")
    failures = []
    for row in rows:
        cid = row.get("case_id")
        if cid not in gold or not safe_id(cid):
            raise ValueError("unknown benchmark case ID")
        if row.get("status") not in {"PASS", "FAILED"}:
            raise ValueError("invalid benchmark status")
        if row["status"] != "FAILED":
            continue
        labels = mapping(gold[cid].get("labels"))
        expected = {
            d["demand_id"]: STATUS.get(str(d.get("status") or "").upper())
            for d in labels.get("demands", [])
        }
        if any(not safe_id(key) or not value for key, value in expected.items()):
            raise ValueError("invalid expert demand")
        grade = mapping(grades.get(cid))
        bounds = mapping(labels.get("score_range"))
        summary = {
            "case_id": cid, "grade_available": bool(grade),
            "reason_code": safe_id(row.get("reason_code")) or "unclassified",
            "error_type": safe_id(row.get("error_type")) or "unknown",
            "expert_range": {"min": number(bounds.get("min")),
                             "max": number(bounds.get("max"))},
        }
        if grade:
            observed = {
                key: STATUS.get(str(r.get("status") or "").upper(), "UNKNOWN")
                for r in (grade.get("requirements") or [])
                if isinstance(r, Mapping)
                if (key := safe_id(r.get("requirement_id")))
            }
            matched = sorted(set(expected) & set(observed))
            total = number(grade.get("total_score"))
            minimum, maximum = summary["expert_range"].values()
            gap = round(max(minimum - total, total - maximum, 0), 4) if (
                total is not None and minimum is not None and maximum is not None
            ) else None
            breakdown = mapping(mapping(grade.get("deterministic_score")).get("score_breakdown"))
            de = mapping(grade.get("qualitative_de_evaluation"))
            resolution = mapping(grade.get("resolution_review"))
            summary.update({
                "total_score": total, "outside_expert_range_by": gap,
                "A_to_E": {k: number(breakdown.get(k)) for k in LAYERS},
                "direct_id_status": {k: {"expert": expected[k], "grade": observed[k]}
                                     for k in matched},
                "direct_disagreements": [k for k in matched if expected[k] != observed[k]],
                "unmapped_expert_ids": sorted(set(expected) - set(observed)),
                "unmapped_grade_count": len(set(observed) - set(expected)),
                "unresolved_requirement_ids": sorted(
                    x for x in (safe_id(v) for v in (resolution.get("requirement_ids") or [])) if x
                ),
                "resolution_required": resolution.get("required") is True,
                "argon_status": safe_id(de.get("status")),
                "argon_calls": de.get("provider_calls") if type(de.get("provider_calls")) is int else None,
            })
        failures.append(summary)
    return {"version": "expert_qualification_hold_audit_v1",
            "qualification_status": "HOLD",
            "source_case_count": len(rows),
            "failed_count": len(failures),
            "cases": failures}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-results", type=Path, required=True)
    parser.add_argument("--golden", type=Path,
                        default=ROOT / "calibration/expert_accuracy_golden.jsonl")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    def jsonl(path: Path) -> list[dict]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    golden, results = jsonl(args.golden), jsonl(args.case_results)
    # Validate all row identities BEFORE opening any private grade files.
    approved_ids = {
        case.get("case_id") for case in golden
        if case.get("review_status") in {"reviewed", "adjudicated"}
    }
    if any(
        not safe_id(row.get("case_id")) or row.get("case_id") not in approved_ids
        for row in results
    ):
        raise SystemExit("case_results contains an unreviewed or invalid case ID")
    grades = {}
    for row in results:
        cid = row["case_id"]
        if row.get("status") != "FAILED":
            continue
        grade_file = args.case_results.parent / cid / "grade.json"
        if grade_file.exists():
            grades[cid] = json.loads(grade_file.read_text(encoding="utf-8"))
    report = analyze_failures(golden, results, grades)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(args.output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as writer:
        json.dump(report, writer, ensure_ascii=False, indent=2)
        writer.write("\n")
    print(f"HOLD_DIAGNOSTIC_CREATED failed={report['failed_count']} "
          f"reviewed={report['source_case_count']} status=HOLD")


if __name__ == "__main__":
    main()
