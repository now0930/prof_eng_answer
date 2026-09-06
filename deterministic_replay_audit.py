"""Gemini-off replay audit for deterministic correctness coverage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from expert_accuracy_benchmark import load_jsonl, validate_gold_case
from quantity_dimension_evaluator import analyze_quantity_dimensions
from topic_machine_contract import validate_topic_machine_contract


VERSION = "deterministic_replay_audit_v1"
MARKER = "DETERMINISTIC_REPLAY_AUDIT_V1"


def _fixture(root: Path, case: dict[str, Any]) -> tuple[str, str]:
    source = case.get("source") or {}
    payload = json.loads((root / str(source.get("path") or "")).read_text(encoding="utf-8"))
    source_case_id = str(source.get("source_case_id") or "").strip()
    if source_case_id:
        payload = next(
            row for row in payload.get("cases", [])
            if isinstance(row, dict) and row.get("case_id") == source_case_id
        )
    question = str(payload.get("question") or "").strip()
    answer = str(payload.get("answer") or payload.get("original_answer") or "").strip()
    if not question or not answer:
        raise ValueError(f"fixture input missing: {case.get('case_id')}")
    return question, answer


def _invariant_bindings(root: Path) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((root / "rubrics/topic_packs").glob("*/logic_check.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        contract = payload.get("machine_contract")
        if not isinstance(contract, dict):
            continue
        fatal_ids = {
            str(row).split("]", 1)[0].lstrip("[").strip()
            for row in payload.get("llm_profile", {}).get("fatal_conditions", [])
            if str(row).lstrip().startswith("[")
        }
        validated = validate_topic_machine_contract(
            contract,
            topic_id=path.parent.name,
            known_rule_ids=fatal_ids,
        )
        for binding in validated["invariant_bindings"]:
            result.setdefault(binding["invariant_code"], []).append(binding)
    return result


def run_deterministic_replay_audit(
    *,
    root: Path,
    golden_path: Path,
) -> dict[str, Any]:
    cases = load_jsonl(golden_path, validate_gold_case)
    bindings = _invariant_bindings(root)
    rows: list[dict[str, Any]] = []
    known_fatal_count = 0
    true_positive = 0
    false_positive = 0
    repeatability_failures = 0
    unexplained: list[dict[str, Any]] = []

    for case in cases:
        question, answer = _fixture(root, case)
        first = analyze_quantity_dimensions(answer, question_text=question)
        second = analyze_quantity_dimensions(answer, question_text=question)
        repeatable = first == second
        if not repeatable:
            repeatability_failures += 1
        detected_ids = {
            binding["rule_id"]
            for violation in first["violations"]
            for binding in bindings.get(violation["code"], [])
            if binding["classification"] == "fatal"
        }
        gold_ids = {
            finding["finding_id"]
            for finding in case["labels"]["findings"]
            if finding["severity"] == "fatal"
        }
        known_fatal_count += len(gold_ids)
        true_positive += len(gold_ids & detected_ids)
        false_positive += len(detected_ids - gold_ids)
        for finding_id in sorted(gold_ids - detected_ids):
            unexplained.append({
                "case_id": case["case_id"],
                "finding_id": finding_id,
                "reason": "no_deterministic_invariant_owner",
            })
        rows.append({
            "case_id": case["case_id"],
            "gold_fatal_ids": sorted(gold_ids),
            "detected_fatal_ids": sorted(detected_ids),
            "dimension_violation_codes": sorted({
                violation["code"] for violation in first["violations"]
            }),
            "repeatable": repeatable,
        })

    recall = true_positive / known_fatal_count if known_fatal_count else 1.0
    ready = bool(
        recall == 1.0
        and false_positive == 0
        and repeatability_failures == 0
        and not unexplained
    )
    return {
        "version": VERSION,
        "marker": MARKER,
        "provider_calls": 0,
        "case_count": len(cases),
        "known_fatal_count": known_fatal_count,
        "known_fatal_true_positive": true_positive,
        "known_fatal_recall": round(recall, 6),
        "fatal_false_positive_count": false_positive,
        "deterministic_repeatability": (
            1.0 if not repeatability_failures else round(
                (len(cases) - repeatability_failures) / len(cases), 6
            )
        ),
        "unexplained_verdict_diff_count": len(unexplained),
        "external_llm_required_for_verdict": not ready,
        "llm_verdict_authority_removal_ready": ready,
        "decision": "READY" if ready else "HOLD",
        "unexplained_differences": unexplained,
        "cases": rows,
    }
