#!/usr/bin/env python3
"""Metadata-only readiness inventory; no private WordPress DB or score changes."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.approved_fact_registry import load_approved_fact_registry


PROPOSALS = ROOT / "reports" / "fact_grounded_representative_candidates_20261010.json"


def coverage_report(root: Path = ROOT, candidate_file: Path = PROPOSALS) -> dict[str, object]:
    records = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((root / "master_topic_packs").glob("*.json"))]
    candidates = json.loads(candidate_file.read_text(encoding="utf-8"))["facts"]
    approved = load_approved_fact_registry(root)["facts"]
    topic_ids = {row["topic_id"] for row in records}
    if len(topic_ids) != len(records):
        raise ValueError("duplicate Master topic id")
    if any(row["topic_id"] not in topic_ids for row in candidates):
        raise ValueError("candidate topic missing from Master")
    statuses = {"verified": 0, "unverified": 0, "stale": 0, "unavailable": 0}
    for record in records:
        for source in record["sources"]:
            state = source["verification_status"]
            if state not in statuses:
                raise ValueError("unknown source verification state")
            statuses[state] += 1
    return {
        "master_topics": len(records),
        "representative_topics": len({row["topic_id"] for row in candidates}),
        "submitted_fact_proposals": len(candidates),
        "reviewed_proposals": len(candidates),
        "approved_facts": len(approved),
        "unapproved_proposals": sum(row["fact_id"] not in {fact["fact_id"] for fact in approved} for row in candidates),
        "master_declared_source_status": statuses,
        "eligible_for_runtime_activation": False,
    }


if __name__ == "__main__":
    print(json.dumps(coverage_report(), ensure_ascii=False, sort_keys=True))
