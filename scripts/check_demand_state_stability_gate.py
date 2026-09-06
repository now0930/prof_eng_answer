#!/usr/bin/env python3
"""Fail closed unless repeated demand-state predictions are stable."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(report: dict, policy: dict) -> dict:
    violations: list[str] = []

    def minimum(field: str, value, threshold) -> None:
        if value is None or value < threshold:
            violations.append(f"{field}={value!r} < {threshold!r}")

    def maximum(field: str, value, threshold) -> None:
        if value is None or value > threshold:
            violations.append(f"{field}={value!r} > {threshold!r}")

    minimum("run_count", report.get("run_count"), policy["minimum_runs"])
    minimum(
        "all_run_state_agreement",
        report.get("all_run_state_agreement"),
        policy["minimum_all_run_state_agreement"],
    )
    for row in report.get("pairwise") or []:
        minimum(
            f"pairwise[{row.get('left')}:{row.get('right')}].agreement",
            row.get("agreement"),
            policy["minimum_pairwise_state_agreement"],
        )
    demand_count = report.get("reviewed_demand_count") or 0
    material_count = report.get("materially_unstable_demand_count")
    material_rate = material_count / demand_count if demand_count and material_count is not None else None
    maximum(
        "material_transition_rate",
        round(material_rate, 6) if material_rate is not None else None,
        policy["maximum_material_transition_rate"],
    )
    maximum(
        "maximum_case_score_spread",
        report.get("maximum_case_score_spread"),
        policy["maximum_case_score_spread"],
    )
    for row in report.get("runs") or []:
        maximum(
            f"runs[{row.get('name')}].missing_case_count",
            row.get("missing_case_count"),
            policy["maximum_missing_cases_per_run"],
        )
    return {
        "schema_version": "demand_state_stability_gate_v1",
        "status": "STABLE" if not violations else "HOLD",
        "violations": violations,
        "material_transition_rate": round(material_rate, 6)
        if material_rate is not None else None,
        "policy_version": policy.get("version"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--require-stable", action="store_true")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    result = evaluate(report, policy)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.require_stable and result["status"] != "STABLE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
