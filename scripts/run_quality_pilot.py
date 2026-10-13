#!/usr/bin/env python3
"""Run three reviewed regression answers through the real deterministic entrypoint.

Creates private, git-ignored grade sessions and quality checksheets. A score
outside an expert-reviewed range becomes a manual issue, never an auto-fix.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.quality.operational_checksheet import (
    add_manual_issue, load_quality_checksheet, save_quality_checksheet,
)
from grading_agents import run_agent_pipeline


CASE_IDS = ("sil_target_operations_issue1", "mcdc_vmodel_sil_issue1",
            "risk_nyquist_normal_01")


def _fixture(case: dict) -> dict:
    source = case["source"]
    path = (ROOT / source["path"]).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("case source escaped repository")
    fixture = json.loads(path.read_text(encoding="utf-8"))
    if "source_case_id" in source:
        fixture = next(row for row in fixture["cases"]
                       if row["case_id"] == source["source_case_id"])
    return fixture


def main() -> int:
    rows = [json.loads(line) for line in
            (ROOT / "calibration/expert_accuracy_golden.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()]
    by_id = {row["case_id"]: row for row in rows}
    sessions_root = ROOT / "data/sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    old_mode = os.environ.get("DETERMINISTIC_GRADING_PRIMARY")
    os.environ["DETERMINISTIC_GRADING_PRIMARY"] = "true"
    report = []
    try:
        for case_id in CASE_IDS:
            case = by_id[case_id]
            fixture = _fixture(case)
            question = fixture["question"]
            answer = fixture.get("answer") or fixture["original_answer"]
            session_name = ("quality_pilot_" + case_id + "_"
                            + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                            + "_" + uuid4().hex[:8])
            session = sessions_root / session_name
            session.mkdir(mode=0o700)

            def no_provider(_prompt):
                raise AssertionError("deterministic pilot must not call a provider")

            _, grade = run_agent_pipeline(
                call_ollama_fn=no_provider,
                raw_text=f"[문제] {question}\n[답안]\n{answer}",
                rubric={}, sid=session_name, image_count=0,
                session_dir=session,
            )
            if grade.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
                raise RuntimeError("pilot did not use deterministic authority")
            lower = float(case["labels"]["score_range"]["min"])
            upper = float(case["labels"]["score_range"]["max"])
            actual = float(grade["total_score"])
            sheet = load_quality_checksheet(session)
            issue_id = None
            if actual < lower or actual > upper:
                direction = "below" if actual < lower else "above"
                priority = "P1" if (actual < 15 <= lower or upper < 15 <= actual) else "P2"
                add_manual_issue(
                    sheet, category="benchmark_conflict", priority=priority,
                    note=(f"Reviewed case {case_id}: deterministic score {actual:.2f} "
                          f"{direction} approved range {lower:.2f}-{upper:.2f}. "
                          "This does not prove a grading defect. Review answer content, "
                          "reference label, question scope and evidence before changing a Topic Pack."),
                )
                issue_id = sheet["issues"][-1]["issue_id"]
                save_quality_checksheet(session, sheet, overwrite=True)
            report.append({"case_id": case_id, "topic_id": grade["topic_id"],
                           "score": actual, "expert_range": [lower, upper],
                           "range_match": issue_id is None,
                           "issue_id": issue_id, "session_dir": str(session)})
    finally:
        if old_mode is None:
            os.environ.pop("DETERMINISTIC_GRADING_PRIMARY", None)
        else:
            os.environ["DETERMINISTIC_GRADING_PRIMARY"] = old_mode
    print(json.dumps({"schema_version": "quality-pilot-v1", "results": report},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
