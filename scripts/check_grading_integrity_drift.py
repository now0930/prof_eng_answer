#!/usr/bin/env python3
"""Fail the release when Issue #1 grading semantics drift across boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from question_demand_contract import build_question_demand_contract
from scripts.replay_sil_issue1_session import run as replay_issue1
from sil_relation_integrity import evaluate_sil_relation_integrity


DEFAULT_BASELINE = REPO / "calibration" / "grading_integrity_drift_baseline.json"
GENERAL_CORPUS = REPO / "calibration" / "general_grading_cross_topic_cases.json"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"JSON object required: {path}")
    return value


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _source_text(case: dict[str, Any], field_key: str, inline_key: str) -> str:
    if inline_key in case:
        return str(case[inline_key])
    source = REPO / str(case["source"])
    payload = _load(source)
    return str(payload[case[field_key]])


def _check_sources(baseline: dict[str, Any]) -> list[str]:
    observed: list[str] = []
    for row in baseline["required_regression_sources"]:
        payload = _load(REPO / row["path"])
        actual = str(payload.get("regression_id") or "")
        assert actual == row["regression_id"], (row["path"], actual)
        observed.append(actual)
    return observed


def _check_routing(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    observed: list[dict[str, Any]] = []
    for case in baseline["routing_cases"]:
        question = _source_text(case, "question_field", "question")
        contract = build_question_demand_contract(question)
        topic_id = contract.get("topic_pack_demand_axes", {}).get("topic_id")
        requirement_ids = [row["requirement_id"] for row in contract["requirements"]]
        assert contract["primary_lens"] == case["expected_primary_lens"], case["id"]
        assert topic_id == case.get("expected_topic_id"), case["id"]
        if "expected_requirement_ids" in case:
            assert requirement_ids == case["expected_requirement_ids"], case["id"]
        assert topic_id not in set(case.get("forbidden_topic_ids", [])), case["id"]
        observed.append({
            "id": case["id"],
            "primary_lens": contract["primary_lens"],
            "topic_id": topic_id,
            "requirement_ids": requirement_ids,
        })
    return observed


def _check_relations(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    observed: list[dict[str, Any]] = []
    for case in baseline["relation_cases"]:
        answer = _source_text(case, "answer_field", "answer")
        result = evaluate_sil_relation_integrity(answer)
        fatal_ids = [row["rule_id"] for row in result["findings"]]
        recognized_ids = sorted({
            row["relation_id"] for row in result["recognized_correct_relations"]
        })
        assert result["status"] == case["expected_status"], case["id"]
        assert fatal_ids == case["expected_fatal_rule_ids"], case["id"]
        assert set(case.get("required_recognized_relation_ids", [])).issubset(
            recognized_ids
        ), case["id"]
        observed.append({
            "id": case["id"],
            "status": result["status"],
            "fatal_rule_ids": fatal_ids,
            "recognized_relation_ids": recognized_ids,
        })
    return observed


def _check_output(baseline: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temporary:
        output_dir = Path(temporary) / "replay"
        manifest = replay_issue1(output_dir)
        telegram = (output_dir / "telegram.txt").read_text(encoding="utf-8")
    expected = baseline["output_case"]["expected"]
    core = manifest["core"]
    observed = {
        "source_session_id": core["source_session_id"],
        "confidence": core["confidence"],
        "passing_score_allowed": core["passing_score_allowed"],
        "strong_verdict_allowed": core["strong_verdict_allowed"],
        "requirements_full_credit_allowed": core["requirements_full_credit_allowed"],
        "mention_coverage_percent": core["mention_coverage_percent"],
        "correctness_coverage_percent": core["correctness_coverage_percent"],
        "fatal_rule_ids": core["fatal_rule_ids"],
    }
    assert observed["source_session_id"] == baseline["output_case"]["source_session_id"]
    for key, value in expected.items():
        assert observed[key] == value, (key, observed[key], value)
    for fragment in baseline["output_case"]["required_telegram_fragments"]:
        assert fragment in telegram, fragment
    for fragment in baseline["output_case"]["forbidden_telegram_fragments"]:
        assert fragment not in telegram, fragment
    return observed


def _check_cross_topic_minimums(baseline: dict[str, Any]) -> list[str]:
    corpus = _load(GENERAL_CORPUS)
    domains = sorted({
        row["domain"]
        for key, rows in corpus.items()
        if key.endswith("_cases") and isinstance(rows, list)
        for row in rows
        if isinstance(row, dict) and row.get("domain")
    })
    limits = baseline["cross_topic_minimums"]
    assert len(domains) >= limits["minimum_domains"]
    assert set(limits["required_domains"]).issubset(domains)
    return domains


def _collect_semantic(baseline: dict[str, Any]) -> dict[str, Any]:
    assert baseline["schema_version"] == "grading_integrity_drift_baseline.v1"
    return {
        "baseline_id": baseline["baseline_id"],
        "regression_ids": _check_sources(baseline),
        "routing": _check_routing(baseline),
        "relations": _check_relations(baseline),
        "output": _check_output(baseline),
        "cross_topic_domains": _check_cross_topic_minimums(baseline),
    }


def _report(baseline: dict[str, Any], semantic: dict[str, Any]) -> dict[str, Any]:
    digest = _sha256(semantic)
    expected_digest = str(baseline.get("expected_semantic_sha256") or "")
    return {
        "status": "PASS" if digest == expected_digest else "DRIFT",
        "baseline_id": baseline["baseline_id"],
        "semantic_sha256": digest,
        "expected_semantic_sha256": expected_digest,
        "semantic": semantic,
    }


def check(baseline_path: Path = DEFAULT_BASELINE) -> dict[str, Any]:
    baseline = _load(baseline_path)
    report = _report(baseline, _collect_semantic(baseline))
    digest = report["semantic_sha256"]
    expected_digest = report["expected_semantic_sha256"]
    if digest != expected_digest:
        raise AssertionError(
            "grading integrity semantic drift: "
            f"expected={expected_digest}, actual={digest}"
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--show-current-fingerprint",
        action="store_true",
        help="Print current observations even when the stored fingerprint differs.",
    )
    args = parser.parse_args()
    if args.show_current_fingerprint:
        baseline = _load(args.baseline.resolve())
        report = _report(baseline, _collect_semantic(baseline))
    else:
        report = check(args.baseline.resolve())
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({
        "status": report["status"],
        "baseline_id": report["baseline_id"],
        "semantic_sha256": report["semantic_sha256"],
        "expected_semantic_sha256": report["expected_semantic_sha256"],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
