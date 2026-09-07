#!/usr/bin/env python3
"""Exercise the production entrypoint while forbidding every LLM call."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading_agents import run_agent_pipeline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    calls: list[str] = []

    def forbidden_provider(prompt: str) -> str:
        calls.append(prompt)
        raise RuntimeError("provider call is forbidden in deterministic-primary smoke")

    previous = os.environ.get("DETERMINISTIC_GRADING_PRIMARY")
    os.environ["DETERMINISTIC_GRADING_PRIMARY"] = "true"
    try:
        with tempfile.TemporaryDirectory() as session_dir:
            _, grade = run_agent_pipeline(
                call_ollama_fn=forbidden_provider,
                raw_text=(
                    "[문제] SIL 결정 방법을 설명하시오.\n"
                    "[답안]\nlambda_SIS 비율이 PFD 비율보다 작도록 설계한다."
                ),
                rubric={},
                sid="deterministic-primary-smoke",
                image_count=0,
                session_dir=session_dir,
            )
            persisted = (Path(session_dir) / "deterministic_grade.json").is_file()
    finally:
        if previous is None:
            os.environ.pop("DETERMINISTIC_GRADING_PRIMARY", None)
        else:
            os.environ["DETERMINISTIC_GRADING_PRIMARY"] = previous

    passed = bool(
        not calls
        and persisted
        and grade.get("marker") == "DETERMINISTIC_GRADING_PRIMARY_V1"
        and grade.get("provider_calls") == 0
        and grade.get("llm_verdict_authority") == 0
        and grade.get("external_llm_required_for_verdict") is False
        and grade.get("logic_check_evaluation", {}).get("fatal_error_detected") is True
        and grade.get("official_pass_met") is False
    )
    report = {
        "marker": "DETERMINISTIC_PRIMARY_PRODUCTION_SMOKE_V1",
        "decision": "PASS" if passed else "FAIL",
        "production_entrypoint": "grading_agents.run_agent_pipeline",
        "provider_call_count": len(calls),
        "grade_marker": grade.get("marker"),
        "llm_verdict_authority": grade.get("llm_verdict_authority"),
        "external_llm_required_for_verdict": grade.get(
            "external_llm_required_for_verdict"
        ),
        "fatal_error_detected": grade.get("logic_check_evaluation", {}).get(
            "fatal_error_detected"
        ),
        "official_pass_met": grade.get("official_pass_met"),
        "persistence_created": persisted,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
