#!/usr/bin/env python3
"""Run an explicitly opted-in, tightly capped live validation smoke.

Default invocation is a no-network plan. This smoke is diagnostic only and can
never create a READY release qualification.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.quality.validation_api_budget import write_summary
from grading.quality.validation_credentials import (
    ValidationCredentialError,
    require_validation_key,
    validation_provider_environment,
)
from grading.quality.expert_accuracy_benchmark import load_jsonl, validate_gold_case


def _ensure_external_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise ValueError("smoke_output_must_be_outside_repository")
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--golden", type=Path, default=ROOT / "calibration" / "expert_accuracy_golden.jsonl")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--max-http-calls", type=int, default=24)
    parser.add_argument("--max-total-tokens", type=int, default=250_000)
    parser.add_argument("--execute-live", action="store_true", help="explicitly authorize this capped paid API smoke")
    args = parser.parse_args(argv)

    case_ids = list(dict.fromkeys(str(value).strip() for value in args.case_id))
    if not 3 <= len(case_ids) <= 5 or any(not value for value in case_ids):
        parser.error("provide 3 to 5 distinct --case-id values")
    if args.max_http_calls <= 0 or args.max_total_tokens <= 0:
        parser.error("budgets must be positive integers")
    try:
        output_dir = _ensure_external_output(args.output_dir)
    except ValueError as exc:
        parser.error(str(exc))
    if output_dir.exists() and any(output_dir.iterdir()):
        parser.error("output directory must be new or empty")

    cases = load_jsonl(args.golden.resolve(), validate_gold_case)
    known = {case["case_id"] for case in cases}
    unknown = sorted(set(case_ids) - known)
    if unknown:
        parser.error("unknown_case_id:" + ",".join(unknown))

    plan = {
        "mode": "LIVE" if args.execute_live else "DRY_RUN",
        "case_count": len(case_ids),
        "case_ids": case_ids,
        "max_live_grades": len(case_ids),
        "max_http_calls": args.max_http_calls,
        "max_total_tokens": args.max_total_tokens,
        "release_qualification": False,
        "api_calls_expected_by_dry_run": 0,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if not args.execute_live:
        print("DRY_RUN_ONLY: no provider credential check and no network call")
        return 0

    try:
        if os.getenv("VALIDATION_LIVE_API", "0").strip() != "1":
            raise ValidationCredentialError("validation_live_api_disabled")
        require_validation_key("gemini")
        if str(os.getenv("DETERMINISTIC_GRADING_PRIMARY", "")).strip().lower() not in {"1", "true", "yes", "on"}:
            raise ValidationCredentialError("deterministic_abc_primary_required")
        if str(os.getenv("QUALITATIVE_DE_MODE", "")).strip().lower() != "argon":
            raise ValidationCredentialError("argon_de_mode_required")
        provider_env = validation_provider_environment()
    except ValidationCredentialError as exc:
        print(f"LIVE_SMOKE_BLOCKED: {exc}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    output_dir.chmod(0o700)
    ledger = output_dir / "api_usage.sqlite3"
    provider_env.update({
        "VALIDATION_API_BUDGET_DB": str(ledger),
        "VALIDATION_MAX_LIVE_GRADES": str(len(case_ids)),
        "VALIDATION_MAX_HTTP_CALLS": str(args.max_http_calls),
        "VALIDATION_MAX_TOTAL_TOKENS": str(args.max_total_tokens),
        "FINAL_GRADE_CACHE_ENABLED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(ROOT),
    })
    command = [
        sys.executable, "-B", "scripts/regrade_expert_accuracy_seed.py",
        "--golden", str(args.golden.resolve()),
        "--output-dir", str(output_dir / "provider_predictions"),
        "--workers", str(args.workers),
        "--require-production-success", "--collect-failures",
    ]
    for case_id in case_ids:
        command.extend(("--case-id", case_id))
    # Do not echo the child environment or exception detail: it may contain
    # provider diagnostics. The child itself emits only safe case/status codes.
    result = subprocess.run(command, cwd=ROOT, env=provider_env, text=True, capture_output=True)
    report_path = output_dir / "api_usage.json"
    try:
        usage = write_summary(report_path)
    except Exception as exc:
        print(f"LIVE_SMOKE_FAILED: usage_report_{type(exc).__name__}", file=sys.stderr)
        return 2
    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.returncode:
        print(f"LIVE_SMOKE=HOLD\nAPI_USAGE={report_path}", file=sys.stderr)
        return 2
    totals = usage["totals"]
    if totals["over_budget"] or totals["grades"] != len(case_ids):
        print(f"LIVE_SMOKE=HOLD\nAPI_USAGE={report_path}", file=sys.stderr)
        return 2
    print(f"LIVE_SMOKE=PASS\nAPI_USAGE={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
