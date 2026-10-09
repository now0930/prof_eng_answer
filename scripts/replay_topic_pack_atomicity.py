"""Project fixed Topic Pack replay inputs into a reviewable grading baseline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.scoring.deterministic_primary_grader import grade_deterministically


DEFAULT_FIXTURE = ROOT / "tests/fixtures/topic_atomicity_second_order_replay.json"


def project(fixture: dict) -> dict:
    rows = []
    for case in fixture["cases"]:
        grade = grade_deterministically(
            question_text=case["question"], answer_text=case["answer"],
        )
        route = grade["routing_evaluation"]
        rows.append({
            "id": case["id"],
            "primary_topic_id": route["primary_topic_id"],
            "topic_ids": route["topic_ids"],
            "route_source": route["source"],
            "candidate_top3": [
                {"topic_id": row["topic_id"], "score": row["score"]}
                for row in route["candidates"][:3]
            ],
            "scope_exact": grade["question_scope_evaluation"]["exact"],
            "requirements": {
                row["requirement_id"]: row["status"]
                for row in grade["requirements"]
                if any(
                    row["requirement_id"].startswith(prefix)
                    for prefix in fixture.get("tracked_requirement_prefixes", ["so2_"])
                )
            },
            "total_score": grade["total_score"],
            "fatal_error_detected": grade["logic_check_evaluation"]["fatal_error_detected"],
            "verdict": grade["verdict"],
            "pass_required_gap_count": grade["deterministic_score"]["pass_required_gap_count"],
        })
    return {"schema_version": fixture["schema_version"], "cases": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    current = project(fixture)
    if args.baseline:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        before = {row["id"]: row for row in baseline["cases"]}
        after = {row["id"]: row for row in current["cases"]}
        differences = []
        for case_id in sorted(before.keys() | after.keys()):
            if before.get(case_id) == after.get(case_id):
                continue
            fields = sorted(set(before.get(case_id, {})) | set(after.get(case_id, {})))
            for field in fields:
                old = before.get(case_id, {}).get(field)
                new = after.get(case_id, {}).get(field)
                if old != new:
                    differences.append({"case_id": case_id, "field": field, "before": old, "after": new})
        print(json.dumps({"match": not differences, "differences": differences}, ensure_ascii=False, indent=2))
        return 0 if not differences else 1
    print(json.dumps(current, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
