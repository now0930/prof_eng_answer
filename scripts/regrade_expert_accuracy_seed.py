#!/usr/bin/env python3
"""Regrade reviewed expert-accuracy cases with the current runtime pipeline."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bot import call_ollama, call_ollama_score_adjudicator
from grading.quality.validation_credentials import (
    ValidationCredentialError, live_validation_enabled,
    validation_provider_environment,
)
from grading.quality.production_grade_gate import (
    ProductionGradeFailure,
    require_production_grade_success,
)
from grading.quality.validation_api_budget import install_http_meter, reserve_grade
from grading.quality.expert_accuracy_benchmark import (
    load_jsonl,
    prediction_from_grade,
    validate_gold_case,
)
from grading.scoring.grade_score_reconciler import reconcile_grade_score
from grading.scoring.grade_submission_normalizer import (
    attach_submission_normalization,
    normalize_grade_submission,
)
from grading_agents import (
    finalize_grade_after_score_reconciliation,
    run_agent_pipeline,
)
from grading.scoring.verdict_consistency import enforce_final_decision_consistency


DEFAULT_GOLDEN = ROOT / "calibration" / "expert_accuracy_golden.jsonl"


def _safe_failure_reason(error: Exception) -> str:
    """Keep private answer/provider details out of benchmark status logs."""
    if isinstance(error, ProductionGradeFailure):
        match = re.search(r"reason=([a-z0-9_]+)$", str(error))
        return match.group(1) if match else "production_grade_incomplete"
    return "execution_error"



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


def _require_semantic_success(grade: dict, case_id: str) -> None:
    evaluation = grade.get("gemini_semantic_evaluation")
    parsed = evaluation.get("parsed") if isinstance(evaluation, dict) else None
    if (
        not isinstance(evaluation, dict)
        or evaluation.get("ok") is False
        or not isinstance(parsed, dict)
    ):
        provider = (
            str(evaluation.get("llm_provider") or "unknown")
            if isinstance(evaluation, dict) else "unknown"
        )
        error = (
            str(evaluation.get("error") or "semantic result missing")[:300]
            if isinstance(evaluation, dict) else "semantic evaluation missing"
        )
        raise RuntimeError(
            f"semantic provider failure: case={case_id}, provider={provider}, error={error}"
        )


def _grade(
    case: dict,
    output_dir: Path,
    image_count: int,
    require_semantic_success: bool = False,
    require_production_success: bool = False,
) -> dict:
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
    if require_semantic_success:
        _require_semantic_success(parsed, case_id)
    parsed = reconcile_grade_score(
        parsed=parsed,
        raw_text=raw_text,
        call_llm_fn=call_ollama_score_adjudicator,
    )
    parsed = finalize_grade_after_score_reconciliation(parsed)
    parsed = attach_submission_normalization(
        parsed,
        {key: value for key, value in normalization.items()
         if key not in {"normalized_text", "answer_text"}},
    )
    if parsed.get("marker") != "DETERMINISTIC_GRADING_PRIMARY_V1":
        parsed = enforce_final_decision_consistency(parsed)
    # Preserve a complete private diagnostic artifact even when the
    # production gate rejects an otherwise completed grade. Never promote it
    # to a benchmark prediction unless the gate actually succeeds.
    (session_dir / "grade.json").write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    retained_dir = output_dir / case_id
    shutil.copytree(session_dir, retained_dir)
    if require_production_success:
        require_production_grade_success(parsed, case_id)
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--image-count", type=int, default=3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--collect-failures", action="store_true",
        help="continue all reviewed production cases, record safe failure codes, "
             "and exit nonzero with no predictions if any case fails",
    )
    parser.add_argument(
        "--require-semantic-success",
        action="store_true",
        help="fail instead of turning provider errors into benchmark predictions",
    )
    parser.add_argument(
        "--require-production-success", action="store_true",
        help="fail unless deterministic A/B/C completed and Argon D/E was actually applied",
    )
    args = parser.parse_args()
    if args.require_production_success and args.require_semantic_success:
        parser.error("choose one production or legacy semantic success contract")
    if args.collect_failures and not args.require_production_success:
        parser.error("--collect-failures requires --require-production-success")

    # This is a benchmark/regrade script, NOT the Telegram bot. Its live
    # requests must never spend the runtime grading API quota. Every provider
    # subprocess inherits only the separately mapped validation credentials.
    if args.require_production_success or args.require_semantic_success:
        if not live_validation_enabled():
            parser.error("validation_live_api_disabled")
    if args.require_production_success and not os.getenv("VALIDATION_GEMINI_API_KEY"):
        parser.error("missing_validation_gemini_api_key")
    if os.getenv("VALIDATION_CREDENTIAL_CONTEXT") == "isolated":
        # The release orchestrator already substituted the validation key.
        # Do not re-compare that remapped legacy name against itself.
        if (os.getenv("VALIDATION_LIVE_API") == "1" and
                os.getenv("VALIDATION_GEMINI_API_KEY") and
                os.getenv("GEMINI_API_KEY") != os.getenv("VALIDATION_GEMINI_API_KEY")):
            parser.error("validation_credential_context_mismatch")
    else:
        try:
            isolated = validation_provider_environment()
        except ValidationCredentialError as exc:
            parser.error(str(exc))
        from grading.quality.validation_credentials import PRODUCTION_CREDENTIAL_KEYS
        for key in PRODUCTION_CREDENTIAL_KEYS:
            os.environ.pop(key, None)
            if key in isolated:
                os.environ[key] = isolated[key]
        os.environ["VALIDATION_CREDENTIAL_CONTEXT"] = "isolated"

    # Live API validation is metered in one SQLite ledger shared by all worker
    # threads and qualification subprocesses. Ordinary offline runs do not
    # install the network meter.
    install_http_meter()

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
            if args.require_production_success:
                require_production_grade_success(grade, case_id)
            if args.require_semantic_success:
                _require_semantic_success(grade, case_id)
            marker = "REUSED"
        else:
            reserve_grade()
            grade = _grade(
                case,
                output_dir,
                args.image_count,
                require_semantic_success=args.require_semantic_success,
                require_production_success=args.require_production_success,
            )
            marker = "REGRADED"
        print(f"{marker}={case_id}", flush=True)
        return case_id, prediction_from_grade(case_id, grade)

    prediction_map: dict[str, dict] = {}
    failures: dict[str, dict[str, str]] = {}

    def record_failure(case: dict, error: Exception) -> None:
        case_id = case["case_id"]
        reason = _safe_failure_reason(error)
        failures[case_id] = {
            "case_id": case_id,
            "status": "FAILED",
            "error_type": type(error).__name__,
            "reason_code": reason,
        }
        print(f"FAILED={case_id} reason={reason}", flush=True)

    if args.workers == 1:
        for case in cases:
            try:
                case_id, prediction = run_case(case)
                prediction_map[case_id] = prediction
            except Exception as error:
                if not args.collect_failures:
                    raise
                record_failure(case, error)
    else:
        executor = ThreadPoolExecutor(max_workers=args.workers)
        futures = {executor.submit(run_case, case): case for case in cases}
        try:
            for future in as_completed(futures):
                try:
                    case_id, prediction = future.result()
                    prediction_map[case_id] = prediction
                except Exception as error:
                    if not args.collect_failures:
                        raise
                    record_failure(futures[future], error)
        except BaseException:
            for future in futures:
                future.cancel()
            executor.shutdown(wait=True, cancel_futures=True)
            raise
        else:
            executor.shutdown(wait=True)

    if args.collect_failures:
        # This sidecar contains only public case IDs and safe reason codes.
        # Raw answers and full grade.json stay inside the private output tree.
        status_path = output_dir / "case_results.jsonl"
        status_path.write_text(
            "".join(
                json.dumps(
                    failures.get(case["case_id"], {
                        "case_id": case["case_id"], "status": "PASS",
                    }),
                    ensure_ascii=False, separators=(",", ":"),
                ) + "\n"
                for case in cases
            ),
            encoding="utf-8",
        )
        print(f"CASE_RESULTS={status_path} FAILURES={len(failures)}", flush=True)
        if failures:
            # A partial prediction set is never eligible for the accuracy gate.
            raise SystemExit(
                f"production qualification failed in {len(failures)} "
                f"of {len(cases)} reviewed cases"
            )

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
