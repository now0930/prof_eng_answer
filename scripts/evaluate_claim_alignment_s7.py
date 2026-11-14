#!/usr/bin/env python3
"""Offline S7 experiment against reviewed expert cases, never score admission.

Run:
  python3 -B scripts/evaluate_claim_alignment_s7.py \
    --output /private/s7_claim_alignment_YYYYMMDD.json

Optional independently reviewed per-candidate labels:
  --adjudications /private/s7_adjudications.jsonl

Only identifiers, hashes, spans, counts and existing expert baseline accuracy
are written; raw answers remain in their original local regression fixtures.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.claim_alignment_engine import analyze_claim_alignment
from grading.quality.claim_alignment_s7_benchmark import (
    build_s7_case_snapshot, evaluate_s7_adjudications,
)
from grading.quality.expert_accuracy_benchmark import (
    FINAL_REVIEW_STATUSES, load_jsonl, measure_accuracy,
    prediction_from_grade, validate_gold_case,
)
from grading.scoring.deterministic_primary_grader import grade_deterministically


def _source_case(case: dict) -> tuple[str, str]:
    """Only load checked-in calibration fixtures, never arbitrary file paths."""
    source = case.get("source") or {}
    relative = Path(str(source.get("path") or ""))
    root = (ROOT / "calibration").resolve()
    if (relative.is_absolute() or ".." in relative.parts
            or relative.suffix != ".json"):
        raise ValueError("invalid calibration source path")
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("calibration source unavailable")
    data = json.loads(path.read_text(encoding="utf-8"))
    source_case_id = str(source.get("source_case_id") or "").strip()
    if source_case_id:
        if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
            raise ValueError("nested source cases missing")
        data = next((
            row for row in data["cases"]
            if isinstance(row, dict)
            and str(row.get("case_id") or "") == source_case_id
        ), None)
    if not isinstance(data, dict):
        raise ValueError("source case missing")
    question = data.get("question")
    answer = data.get("answer") or data.get("original_answer")
    if (not isinstance(question, str) or not question.strip()
            or not isinstance(answer, str) or not answer.strip()):
        raise ValueError("source question or answer missing")
    return question.strip(), answer.strip()


def evaluate_cases(
    gold_cases: list[dict],
    *, adjudications: list[dict] | None = None,
) -> dict:
    """Build fresh alignment only from the same question/answer graded OFF.

    Reviewed expert score ranges are a case-level reference. They cannot
    silently become labels on unrelated Fact Anchors.
    """
    eligible = [
        validate_gold_case(case) for case in gold_cases
        if case.get("review_status") in FINAL_REVIEW_STATUSES
    ]
    snapshots: list[dict] = []
    predictions: list[dict] = []
    failures: list[dict[str, str]] = []
    for case in eligible:
        case_id = case["case_id"]
        try:
            question, answer = _source_case(case)
            with patch.dict(os.environ, {
                "CLAIM_ALIGNMENT_MODE": "off",
                "QUALITATIVE_DE_MODE": "off",
                "VALIDATION_LIVE_API": "0",
            }):
                baseline = grade_deterministically(
                    question_text=question, answer_text=answer,
                    qualitative_de_mode="off",
                )
            predictions.append(prediction_from_grade(case_id, baseline))
            accepted_statuses = {
                "SATISFIED", "PARTIAL", "MISSING", "UNKNOWN", "WRONG",
            }
            grade_rows = [
                row for row in baseline.get("requirements", [])
                if isinstance(row, dict)
                and row.get("status") in accepted_statuses
                and row.get("requirement_id") != "__question_scope__"
            ]
            selected: dict[str, set[str]] = {}
            for row in grade_rows:
                topic = str(row.get("owner_topic_id") or "")
                requirement_id = str(row.get("requirement_id") or "")
                if topic and requirement_id:
                    selected.setdefault(topic, set()).add(requirement_id)
            aligned = analyze_claim_alignment(
                question_text=question, answer_text=answer,
                topic_ids=baseline["topic_ids"],
                required_by_topic=selected,
            )
            snapshots.append(build_s7_case_snapshot(
                case_id=case_id,
                question_text=question,
                answer_text=answer,
                alignment=aligned,
                requirement_evaluation={"requirements": grade_rows},
                provisional=bool(
                    (baseline.get("resolution_review") or {}).get("required")
                ),
                fatal_or_core_error=bool(
                    (baseline.get("logic_check_evaluation") or {}).get(
                        "fatal_error_detected",
                    )
                ),
            ))
        except Exception as error:
            # Never leak source answer or exception strings into reports.
            failures.append({
                "case_id": case_id,
                "error_type": type(error).__name__,
            })
    independent = evaluate_s7_adjudications(snapshots, adjudications or [])
    expert = measure_accuracy(eligible, predictions)
    return {
        "schema_version": "claim_alignment_s7_experiment.v1",
        "status": (
            "INCOMPLETE_BASELINE" if failures
            else "RESEARCH_ONLY"
        ),
        "score_effect": "none",
        "score_admission": "DISABLED",
        "expert_gold_label_scope": "CASE_LEVEL_ONLY",
        "expert_gold_mapped_to_fact_ids": False,
        "expert_accuracy_baseline": expert,
        "s7_independent_review": independent,
        "eligible_case_count": len(eligible),
        "graded_case_count": len(predictions),
        "alignment_snapshot_count": len(snapshots),
        "failures": failures,
        "case_snapshots": snapshots,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--golden", type=Path,
        default=ROOT / "calibration" / "expert_accuracy_golden.jsonl",
    )
    parser.add_argument("--adjudications", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if (not args.output.is_absolute()
            or args.output.resolve().is_relative_to(ROOT.resolve())):
        parser.error("output must be absolute and outside the repository")
    if args.output.exists() or args.output.is_symlink():
        parser.error("refusing to overwrite existing private report")
    if args.adjudications is not None and (
        not args.adjudications.is_absolute()
        or args.adjudications.resolve().is_relative_to(ROOT.resolve())
    ):
        parser.error("expert adjudications must remain outside the repository")
    golden = load_jsonl(args.golden, validate_gold_case)
    if not golden:
        parser.error("reviewed expert golden data is missing")
    adjudications: list[dict] = []
    if args.adjudications is not None:
        if not args.adjudications.is_file():
            parser.error("adjudication file is missing")
        for index, line in enumerate(
            args.adjudications.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                parser.error(f"invalid adjudication JSON at line {index}")
            adjudications.append(value)
    report = evaluate_cases(golden, adjudications=adjudications)
    args.output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    summary = {
        "status": report["status"],
        "graded_cases": report["graded_case_count"],
        "failed_cases": len(report["failures"]),
        "candidate_count": report["s7_independent_review"]["candidate_count"],
        "reviewed_candidates": report[
            "s7_independent_review"
        ]["reviewed_candidate_count"],
        "score_admission": report["score_admission"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
