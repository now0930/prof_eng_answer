"""Offline comparison of fact evidence with an independently supplied baseline.

No answer text or private session data is stored by this module. Missing baseline
or incomplete interpretation is reported separately, never counted as agreement.
"""

from __future__ import annotations

from typing import Any


def summarize_shadow_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate case-level evidence states without treating a legacy score as truth."""
    if not isinstance(cases, list):
        raise ValueError("cases must be a list")
    seen = set()
    result = {"cases": len(cases), "complete": 0, "incomplete": 0,
              "proved_requirements": 0, "unresolved_requirements": 0,
              "comparable": 0, "agreements": 0, "disagreements": 0,
              "score_effect": "none"}
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"case_id", "shadow", "reference_fact_ids"}:
            raise ValueError("invalid shadow case")
        case_id = case["case_id"]
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError("duplicate or missing case id")
        seen.add(case_id)
        shadow = case["shadow"]
        if not isinstance(shadow, dict) or shadow.get("score_effect") != "none" or shadow.get("final_grade_allowed") is not False:
            raise ValueError("shadow has grading authority")
        rows = shadow.get("requirements")
        if not isinstance(rows, list) or any(
            not isinstance(row, dict) or set(row) != {"requirement_id", "state", "fact_refs"}
            or row["state"] not in {"proved", "unresolved"} or not isinstance(row["fact_refs"], list)
            for row in rows
        ):
            raise ValueError("invalid requirement rows")
        complete = shadow.get("complete") is True and all(row["state"] == "proved" for row in rows)
        result["complete" if complete else "incomplete"] += 1
        proved = {fid for row in rows if row["state"] == "proved" for fid in row["fact_refs"]}
        result["proved_requirements"] += sum(row["state"] == "proved" for row in rows)
        result["unresolved_requirements"] += sum(row["state"] == "unresolved" for row in rows)
        reference = case["reference_fact_ids"]
        if reference is None or not complete:
            continue
        if not isinstance(reference, list) or any(not isinstance(fid, str) for fid in reference):
            raise ValueError("invalid reference facts")
        result["comparable"] += 1
        result["agreements" if proved == set(reference) else "disagreements"] += 1
    return result
