#!/usr/bin/env python3
"""Regrade reviewed expert-accuracy cases with the current runtime pipeline."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bot import call_ollama, call_ollama_score_adjudicator
from expert_accuracy_benchmark import (
    load_jsonl,
    prediction_from_grade,
    validate_gold_case,
)
from grade_score_reconciler import reconcile_grade_score
from grade_submission_normalizer import (
    attach_submission_normalization,
    normalize_grade_submission,
)
from grading_agents import (
    _phase2_finalize_verified_coverage_for_persistence,
    run_agent_pipeline,
)
from verdict_consistency import enforce_final_decision_consistency


DEFAULT_GOLDEN = ROOT / "calibration" / "expert_accuracy_golden.jsonl"


def _fixture_input(case: dict) -> str:
    source = case.get("source") or {}
    source_path = ROOT / str(source.get("path") or "")
    fixture = json.loads(source_path.read_text(encoding="utf-8"))
    source_case_id = str(source.get("source_case_id") or "").strip()
    if source_case_id:
        candidates = fixture.get("cases")
        if not isinstance(candidates, list):
            raise ValueError(f"nested cases missing: {case['case_id']}")
        fixture = next(
            (
                row for row in candidates
                if isinstance(row, dict)
                and str(row.get("case_id") or "") == source_case_id
            ),
            None,
        )
        if not isinstance(fixture, dict):
            raise ValueError(f"source case missing: {source_case_id}")
    question = str(fixture.get("question") or "").strip()
    answer = str(
        fixture.get("answer") or fixture.get("original_answer") or ""
    ).strip()
    if not question or not answer:
        raise ValueError(f"question/answer missing: {case['case_id']}")
    return f"문제: {question}\n답안:\n{answer}"


def _grade(case: dict, output_dir: Path, image_count: int) -> dict:
    case_id = case["case_id"]
    session_dir = (
        ROOT / "data" / "sessions"
        / f"expert_accuracy_{case_id}_{uuid.uuid4().hex[:8]}"
    )
    session_dir.mkdir(parents=True, exist_ok=True)
    normalization = normalize_grade_submission(_fixture_input(case))
    raw_text = normalization["normalized_text"]
    (session_dir / "input.raw.txt").write_text(
        _fixture_input(case), encoding="utf-8"
    )
    (session_dir / "input.txt").write_text(raw_text, encoding="utf-8")
    (session_dir / "input.normalized.txt").write_text(
        raw_text, encoding="utf-8"
    )
    rubric = json.loads(
        (ROOT / "rubrics" / "default.json").read_text(encoding="utf-8")
    )
    raw_result, parsed = run_agent_pipeline(
        call_ollama_fn=call_ollama,
        raw_text=raw_text,
        rubric=rubric,
        sid=f"expert_accuracy_{case_id}",
        image_count=image_count,
        session_dir=session_dir,
    )
    if not isinstance(parsed, dict):
        raise RuntimeError(f"grade parse failed: {case_id}: {raw_result!r}")
    parsed = reconcile_grade_score(
        parsed=parsed,
        raw_text=raw_text,
        call_llm_fn=call_ollama_score_adjudicator,
    )
    parsed = _phase2_finalize_verified_coverage_for_persistence(parsed)
    parsed = attach_submission_normalization(
        parsed,
        {key: value for key, value in normalization.items()
         if key not in {"normalized_text", "answer_text"}},
    )
    parsed = enforce_final_decision_consistency(parsed)
    (session_dir / "grade.json").write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    retained_dir = output_dir / case_id
    shutil.copytree(session_dir, retained_dir)
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--image-count", type=int, default=3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    cases = load_jsonl(args.golden.resolve(), validate_gold_case)
    selected = set(args.case_id)
    if selected:
        cases = [case for case in cases if case["case_id"] in selected]
    if not cases:
        raise SystemExit("no matching reviewed cases")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.workers < 1 or args.workers > 4:
        raise SystemExit("--workers must be within 1..4")

    def run_case(case: dict) -> tuple[str, dict]:
        case_id = case["case_id"]
        retained_grade = output_dir / case_id / "grade.json"
        if args.resume and retained_grade.exists():
            grade = json.loads(retained_grade.read_text(encoding="utf-8"))
            marker = "REUSED"
        else:
            grade = _grade(case, output_dir, args.image_count)
            marker = "REGRADED"
        print(f"{marker}={case_id}", flush=True)
        return case_id, prediction_from_grade(case_id, grade)

    prediction_map = {}
    if args.workers == 1:
        for case in cases:
            case_id, prediction = run_case(case)
            prediction_map[case_id] = prediction
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_case, case): case for case in cases}
            for future in as_completed(futures):
                case_id, prediction = future.result()
                prediction_map[case_id] = prediction
    predictions = [prediction_map[case["case_id"]] for case in cases]

    prediction_path = output_dir / "predictions.jsonl"
    prediction_path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in predictions
        ),
        encoding="utf-8",
    )
    print(f"PREDICTIONS={prediction_path}")


if __name__ == "__main__":
    main()
