#!/usr/bin/env python3
"""Replay a stored grade through the current final boundary without writing it."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import grading_agents
from persisted_grade_replay import restore_retired_volume_policy_for_replay


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("grade", type=Path)
    args = parser.parse_args()
    stored = json.loads(args.grade.read_text(encoding="utf-8"))
    prepared = restore_retired_volume_policy_for_replay(stored)
    replayed = grading_agents._stage17e5_finalize_pipeline_result(
        prepared,
        {"question_answer_boundary": {"manual_review_required": False}},
    )
    result = {
        "source": str(args.grade),
        "stored_total_score": stored.get("total_score"),
        "replayed_total_score": replayed.get("total_score"),
        "official_pass_met": replayed.get("official_pass_met"),
        "high_score_met": replayed.get("high_score_met"),
        "strong_verdict_allowed": replayed.get("strong_verdict_allowed"),
        "legacy_volume_policy_replay": replayed.get("legacy_volume_policy_replay"),
        "verified_evidence_score_calibration": replayed.get("verified_evidence_score_calibration"),
        "ledger_summary": (replayed.get("canonical_evaluation_ledger") or {}).get("summary"),
        "fatal_findings": [
            row.get("rule_id") or row.get("defect_id")
            for row in ((replayed.get("logic_check_evaluation") or {}).get("findings") or [])
            if isinstance(row, dict) and str(row.get("severity") or "").casefold() == "fatal"
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
