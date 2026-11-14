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
    actual_false_official_pass_ids: list[str] = []
    failures: list[dict[str, str]] = []
    projected_status_counts: dict[str, int] = {}
    alignment_relation_counts: dict[str, int] = {}
    recall_disposition_counts: dict[str, int] = {}
    alignment_case_diagnostics: list[dict] = []
    no_candidate_reason_counts: dict[str, int] = {}
    for case in eligible:
        case_id = case["case_id"]
        stage = "fixture"
        try:
            question, answer = _source_case(case)
            stage = "deterministic_grade"
            with patch.dict(os.environ, {
                "CLAIM_ALIGNMENT_MODE": "off",
                "QUALITATIVE_DE_MODE": "off",
                "VALIDATION_LIVE_API": "0",
            }):
                baseline = grade_deterministically(
                    question_text=question, answer_text=answer,
                    qualitative_de_mode="off",
                )
            stage = "gold_prediction"
            predictions.append(prediction_from_grade(case_id, baseline))
            if (
                baseline.get("official_pass_met") is True
                and not case["labels"]["flags"]["passing_score_allowed"]
            ):
                actual_false_official_pass_ids.append(case_id)
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
            stage = "canonical_claim_alignment"
            aligned = analyze_claim_alignment(
                question_text=question, answer_text=answer,
                topic_ids=baseline["topic_ids"],
                required_by_topic=selected,
            )
            stage = "recall_review_snapshot"
            snapshot = build_s7_case_snapshot(
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
            )
            snapshots.append(snapshot)
            relation_counts = aligned["summary"]["relation_counts"]
            projected_verified = sum(
                row.get("projection_status") == "VERIFIED_REGISTRY_RELATION"
                for row in aligned["fact_projection"]
            )
            selected_requirement_count = sum(
                len(anchors) for anchors in selected.values()
            )
            exact_count = int(relation_counts.get("EXACT_RELATION", 0))
            if snapshot["candidate_count"]:
                reason = "HAS_REVIEW_CANDIDATES"
            elif not selected_requirement_count:
                reason = "NO_SELECTED_REQUIREMENTS"
            elif not aligned["fact_projection"]:
                reason = "NO_PROJECTED_ANCHORS"
            elif not projected_verified:
                reason = "NO_VERIFIED_FACT_PROJECTION"
            elif not exact_count:
                reason = "NO_EXACT_RELATION"
            else:
                reason = "EXACT_WITHOUT_MISSED_RECALL"
            no_candidate_reason_counts[reason] = (
                no_candidate_reason_counts.get(reason, 0) + 1
            )
            extraction_summary = baseline.get("canonical_claim_extraction") or {}
            alignment_case_diagnostics.append({
                "case_id": case_id,
                "selected_requirement_count": selected_requirement_count,
                "projected_anchor_count": len(aligned["fact_projection"]),
                "verified_fact_projection_count": projected_verified,
                "canonical_claim_count": extraction_summary.get("claim_count"),
                "exact_relation_count": exact_count,
                "review_candidate_count": snapshot["candidate_count"],
                "coverage_disposition": reason,
            })
            for fact in aligned["fact_projection"]:
                key = str(fact.get("projection_status") or "UNKNOWN")
                projected_status_counts[key] = projected_status_counts.get(key, 0) + 1
            for relation, count in aligned["summary"]["relation_counts"].items():
                alignment_relation_counts[relation] = (
                    alignment_relation_counts.get(relation, 0) + int(count)
                )
            for disposition, count in snapshot["candidate_dispositions"].items():
                recall_disposition_counts[disposition] = (
                    recall_disposition_counts.get(disposition, 0) + int(count)
                )
        except Exception as error:
            # Public reviewed fixture IDs and exception classes are safe.
            # No private answer, stack trace, model output or exception message.
            failures.append({
                "case_id": case_id,
                "stage": stage,
                "error_type": type(error).__name__,
            })
    independent = evaluate_s7_adjudications(snapshots, adjudications or [])
    expert = measure_accuracy(eligible, predictions)
    baseline_failure_stages = {
        "fixture", "deterministic_grade", "gold_prediction",
    }
    baseline_failures = [
        row for row in failures if row["stage"] in baseline_failure_stages
    ]
    alignment_failures = [
        row for row in failures if row["stage"] not in baseline_failure_stages
    ]
    type_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    reviewed_counts: dict[str, int] = {}
    unique_topics: set[str] = set()
    for case in eligible:
        kind = str(case.get("question_type") or "UNKNOWN")
        type_counts[kind] = type_counts.get(kind, 0) + 1
        source_kind = str((case.get("source") or {}).get("kind") or "UNKNOWN")
        source_counts[source_kind] = source_counts.get(source_kind, 0) + 1
        reviewed_counts[case["review_status"]] = reviewed_counts.get(
            case["review_status"], 0
        ) + 1
        unique_topics.update(str(topic) for topic in case.get("topic_ids") or [])
    candidate_topics: dict[str, int] = {}
    for snapshot in snapshots:
        for candidate in snapshot["review_candidates"]:
            topic = candidate["owner_topic_id"]
            candidate_topics[topic] = candidate_topics.get(topic, 0) + 1
    predictions_by_id = {row["case_id"]: row for row in predictions}
    baseline_false_pass_case_ids = sorted(
        case["case_id"]
        for case in eligible
        if (case["case_id"] in predictions_by_id
            and predictions_by_id[case["case_id"]]["passing_score_allowed"]
            and not case["labels"]["flags"]["passing_score_allowed"])
    )
    coverage = {
        "review_status_counts": dict(sorted(reviewed_counts.items())),
        "question_type_counts": dict(sorted(type_counts.items())),
        "source_kind_counts": dict(sorted(source_counts.items())),
        "expert_topic_count": len(unique_topics),
        "aligned_case_count": len(snapshots),
        "candidate_counts_by_topic": dict(sorted(candidate_topics.items())),
        "fact_projection_status_counts": dict(sorted(projected_status_counts.items())),
        "alignment_relation_counts": dict(sorted(alignment_relation_counts.items())),
        "recall_disposition_counts": dict(sorted(recall_disposition_counts.items())),
        "no_candidate_is_not_perfect_accuracy": True,
        "no_candidate_reason_counts": dict(sorted(no_candidate_reason_counts.items())),
        "case_diagnostics": alignment_case_diagnostics,
    }
    return {
        "schema_version": "claim_alignment_s7_experiment.v1",
        "status": (
            "INCOMPLETE_BASELINE" if baseline_failures
            else "INCOMPLETE_ALIGNMENT" if alignment_failures
            else "RESEARCH_ONLY"
        ),
        "baseline_failure_count": len(baseline_failures),
        "alignment_failure_count": len(alignment_failures),
        "score_effect": "none",
        "score_admission": "DISABLED",
        "expert_gold_label_scope": "CASE_LEVEL_ONLY",
        "expert_gold_mapped_to_fact_ids": False,
        "expert_accuracy_baseline": expert,
        "golden_coverage": coverage,
        "s7_independent_review": independent,
        "eligible_case_count": len(eligible),
        "graded_case_count": len(predictions),
        "alignment_snapshot_count": len(snapshots),
        "failures": failures,
        "baseline_false_pass_case_ids": baseline_false_pass_case_ids,
        "baseline_false_official_pass_case_ids": sorted(
            actual_false_official_pass_ids
        ),
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
        "baseline_failed_cases": report["baseline_failure_count"],
        "alignment_failed_cases": report["alignment_failure_count"],
        "failure_details": report["failures"],
        "candidate_count": report["s7_independent_review"]["candidate_count"],
        "fact_projection_status_counts": report[
            "golden_coverage"
        ]["fact_projection_status_counts"],
        "alignment_relation_counts": report[
            "golden_coverage"
        ]["alignment_relation_counts"],
        "recall_disposition_counts": report[
            "golden_coverage"
        ]["recall_disposition_counts"],
        "no_candidate_reason_counts": report[
            "golden_coverage"
        ]["no_candidate_reason_counts"],
        "case_diagnostics": report[
            "golden_coverage"
        ]["case_diagnostics"],
        "reviewed_candidates": report[
            "s7_independent_review"
        ]["reviewed_candidate_count"],
        "alignment_snapshot_count": report["alignment_snapshot_count"],
        "claim_precision_reviewed_only": report[
            "s7_independent_review"
        ]["observed_precision_labeled_only"],
        "golden_topic_count": report["golden_coverage"]["expert_topic_count"],
        "question_type_counts": report[
            "golden_coverage"
        ]["question_type_counts"],
        "baseline_false_pass_count": report[
            "expert_accuracy_baseline"
        ]["false_pass_count"],
        "baseline_false_pass_case_ids": report[
            "baseline_false_pass_case_ids"
        ],
        "baseline_false_official_pass_count": len(
            report["baseline_false_official_pass_case_ids"]
        ),
        "baseline_false_official_pass_case_ids": report[
            "baseline_false_official_pass_case_ids"
        ],
        "baseline_false_strong_count": report[
            "expert_accuracy_baseline"
        ]["false_strong_count"],
        "baseline_mean_out_of_range_distance": report[
            "expert_accuracy_baseline"
        ]["mean_out_of_range_distance"],
        "score_admission": report["score_admission"],
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
