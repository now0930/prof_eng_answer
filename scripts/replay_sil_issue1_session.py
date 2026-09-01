#!/usr/bin/env python3
"""Deterministic host/container replay for the Issue #1 SIL session.

The replay intentionally starts after provider scoring.  It exercises the
production normalization, question-demand, logic, final-decision, persistence,
and Telegram display boundaries without calling an external LLM.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import bot
from grade_submission_normalizer import (
    attach_submission_normalization,
    normalize_grade_submission,
)
from logic_check_evaluator import evaluate_logic_checks
from question_demand_contract import build_question_demand_contract
from question_type_coverage_adapter import (
    attach_question_type_coverage_feedback,
)
from sil_relation_integrity import SIL_TARGET_TOPIC_ID
from verdict_consistency import enforce_final_decision_consistency


VERSION = "sil_issue1_runtime_replay_v1"
FIXTURE_PATH = REPO / "calibration" / (
    "sil_target_operations_overgrading_regression.json"
)
EXPECTED_AXES = [
    "system_scope_and_sil_role",
    "risk_scenario_and_tolerable_target",
    "existing_ipl_and_independence",
    "required_rrf_and_target_sil",
    "demand_mode_metric_selection",
    "quantitative_verification_dimension",
    "proof_test_diagnostics_reliability",
    "operations_moc_security_ai_lifecycle",
]
FORBIDDEN_OUTPUT = (
    "요구사항 충족률 100%",
    "전체 판정: strong",
    "핵심 관계식과 PFH/PFD 설명이 정확",
    "치명적인 기술 오류나 누락이 없",
    "D/E 구체성뿐",
)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_fixture() -> dict[str, Any]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("SIL replay fixture must be a JSON object")
    return payload


def raw_submission(fixture: dict[str, Any]) -> str:
    return (
        "/grade\n"
        f"문제: {fixture['question']}\n"
        "답안:\n"
        f"{fixture['original_answer']}\n"
        "끝.\n"
    )


def coverage_rows(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    statuses = fixture["expected"]["original"]["demand_status"]
    if list(statuses) != EXPECTED_AXES:
        raise RuntimeError("fixture demand axis order changed")
    return [
        {
            "requirement_id": requirement_id,
            "requirement": requirement_id,
            "status": status,
            "mentioned": status != "missing",
            "evidence": "frozen regression assessment" if status != "missing" else "",
            "is_core": True,
        }
        for requirement_id, status in statuses.items()
    ]


def build_replayed_grade(
    fixture: dict[str, Any],
    normalization: dict[str, Any],
) -> dict[str, Any]:
    answer_text = str(normalization.get("answer_text") or "")
    logic = evaluate_logic_checks(
        answer_text,
        {"logic_check_topic_id": SIL_TARGET_TOPIC_ID},
    )
    grade: dict[str, Any] = {
        "total_score": 13.52,
        "max_score": 25.0,
        "score_range": "13.0~14.0",
        "confidence": "high",
        "grade_confidence": "high",
        "confidence_level": "high",
        "official_pass_score": 15.0,
        "practical_target_score": 17.5,
        "high_score_target": 20.0,
        "official_pass_met": True,
        "practical_target_met": True,
        "high_score_met": True,
        "verdict": "strong",
        "summary": (
            "SIL 결정 방법론과 최신 이슈 연계가 매우 우수하며 "
            "핵심 관계식과 PFH/PFD 설명이 정확합니다."
        ),
        "logic_check_evaluation": logic,
        "question_type_coverage": {
            "question_type": "IMPLEMENTATION_EVALUATION",
            "overall_coverage": "strong",
            "explicit_requirement_coverage": {
                "requirements": coverage_rows(fixture),
            },
        },
        "general_evidence_contract": {"defects": []},
    }
    grade = attach_question_type_coverage_feedback(grade)
    normalization_evidence = {
        key: value
        for key, value in normalization.items()
        if key not in {"normalized_text", "answer_text"}
    }
    grade = attach_submission_normalization(
        grade,
        normalization_evidence,
    )
    return enforce_final_decision_consistency(grade)


def telegram_text(grade: dict[str, Any]) -> str:
    previous = os.environ.get("GRADE_OUTPUT_LLM_SUMMARY")
    os.environ["GRADE_OUTPUT_LLM_SUMMARY"] = "0"
    try:
        return bot.format_result(grade)
    finally:
        if previous is None:
            os.environ.pop("GRADE_OUTPUT_LLM_SUMMARY", None)
        else:
            os.environ["GRADE_OUTPUT_LLM_SUMMARY"] = previous


def replay_fingerprint(
    fixture: dict[str, Any],
    normalization: dict[str, Any],
    contract: dict[str, Any],
    grade: dict[str, Any],
    telegram: str,
) -> dict[str, Any]:
    logic = grade["logic_check_evaluation"]
    coverage = grade["question_type_coverage_summary"]
    core = {
        "version": VERSION,
        "regression_id": fixture["regression_id"],
        "source_session_id": fixture["source_session_id"],
        "question_sha256": sha256_text(normalization["question_text"]),
        "answer_sha256": sha256_text(normalization["answer_text"]),
        "boundary_status": normalization[
            "question_answer_boundary"
        ]["status"],
        "topic_id": contract["topic_pack_demand_axes"]["topic_id"],
        "requirement_ids": [
            row["requirement_id"]
            for row in contract["requirements"]
        ],
        "logic_mode": logic["mode"],
        "fatal_rule_ids": [
            row.get("rule_id")
            for row in logic["findings"]
            if row.get("severity") == "fatal"
        ],
        "confidence": grade["confidence"],
        "passing_score_allowed": grade["passing_score_allowed"],
        "strong_verdict_allowed": grade["strong_verdict_allowed"],
        "requirements_full_credit_allowed": grade[
            "requirements_full_credit_allowed"
        ],
        "mention_coverage_percent": coverage[
            "mention_coverage_percent"
        ],
        "correctness_coverage_percent": coverage[
            "correctness_coverage_percent"
        ],
        "telegram_sha256": sha256_text(telegram),
    }
    return {
        "core": core,
        "core_sha256": sha256_text(canonical_json(core)),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }


def assert_replay(
    contract: dict[str, Any],
    grade: dict[str, Any],
    telegram: str,
) -> None:
    requirement_ids = [
        row["requirement_id"]
        for row in contract["requirements"]
    ]
    if requirement_ids != EXPECTED_AXES:
        raise AssertionError(
            "exact eight-axis contract mismatch: "
            f"expected={EXPECTED_AXES!r}, actual={requirement_ids!r}, "
            "topic="
            f"{contract.get('topic_pack_demand_axes', {}).get('topic_id')!r}"
        )
    if contract["topic_pack_demand_axes"]["topic_id"] != SIL_TARGET_TOPIC_ID:
        raise AssertionError("SIL topic owner mismatch")
    logic = grade["logic_check_evaluation"]
    if logic.get("fatal_error_detected") is not True:
        raise AssertionError("fatal SIL relation was not detected")
    if {
        row.get("rule_id")
        for row in logic.get("findings", [])
    } != {"fatal_target_pfd_frequency_product"}:
        raise AssertionError("unexpected SIL fatal rule set")
    if grade.get("confidence") != "medium":
        raise AssertionError("fatal confidence ceiling was not applied")
    for key in (
        "passing_score_allowed",
        "strong_verdict_allowed",
        "requirements_full_credit_allowed",
    ):
        if grade.get(key) is not False:
            raise AssertionError(f"{key} must be false")
    coverage = grade["question_type_coverage_summary"]
    if coverage.get("mention_coverage_percent") != 87.5:
        raise AssertionError("mention coverage mismatch")
    if coverage.get("correctness_coverage_percent") != 25.0:
        raise AssertionError("correctness coverage mismatch")
    required_output = (
        "신뢰도: medium",
        "검증된 핵심 기술 오류가 확인되었습니다.",
        "요구사항 언급률: 87.5%",
        "요구사항 정확 충족률: 25.0%",
        "오답 3",
    )
    for phrase in required_output:
        if phrase not in telegram:
            raise AssertionError(f"Telegram output missing: {phrase}")
    for phrase in FORBIDDEN_OUTPUT:
        if phrase in telegram:
            raise AssertionError(f"forbidden Telegram output: {phrase}")


def write_replay(
    output_dir: Path,
    raw: str,
    normalization: dict[str, Any],
    contract: dict[str, Any],
    grade: dict[str, Any],
    telegram: str,
    manifest: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, str] = {
        "input.raw.txt": raw,
        "input.txt": str(normalization["normalized_text"]),
        "submission_normalization.json": json.dumps(
            {
                key: value
                for key, value in normalization.items()
                if key not in {"normalized_text", "answer_text"}
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        "question_demand_contract.json": json.dumps(
            contract,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        "logic_check_evaluation.json": json.dumps(
            grade["logic_check_evaluation"],
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        "grade.json": json.dumps(
            grade,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        "telegram.txt": telegram + "\n",
        "replay_manifest.json": json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    }
    for name, content in artifacts.items():
        (output_dir / name).write_text(content, encoding="utf-8")


def run(output_dir: Path) -> dict[str, Any]:
    fixture = load_fixture()
    raw = raw_submission(fixture)
    normalization = normalize_grade_submission(raw)
    contract = build_question_demand_contract(
        normalization["question_text"]
    )
    grade = build_replayed_grade(fixture, normalization)
    telegram = telegram_text(grade)
    assert_replay(contract, grade, telegram)
    manifest = replay_fingerprint(
        fixture,
        normalization,
        contract,
        grade,
        telegram,
    )
    write_replay(
        output_dir,
        raw,
        normalization,
        contract,
        grade,
        telegram,
        manifest,
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )
    args = parser.parse_args()
    manifest = run(args.output_dir.resolve())
    print(
        json.dumps(
            {
                "status": "PASS",
                "version": VERSION,
                "core_sha256": manifest["core_sha256"],
                "output_dir": str(args.output_dir.resolve()),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
