"""Offline P2-B8 dataset replay; provider calls are disabled by default.

Only synthetic public cases are loaded. Protected 143-answer sources are not
opened or included. A/B/C performance comparison requires an explicit live
pilot and is reported NOT_RUN when validation credentials/config are absent.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.p2b8_llm_claim_extractor import (
    evaluate_extracted_evidence,
    extract_with_provider,
)
from scripts.audit_relation_recognition import audit_relation_recognition
from reports.run_p2b_relation_diagnostic_20261125 import (
    compare_structured as compare_structured_baseline_contract,
)


BASE_CASES = ROOT / "reports/p2b_relation_cases_20261125.json"
REVIEWED_CASES = ROOT / "reports/p2b_generalization_reviewed_cases_20261126.json"
CONTRACT = ROOT / "reports/p2b_b8_experiment_contract_20261126.json"
# The contract points at this B8-named path, which is absent in this checkout.
# The existing B7 artifact is accepted only after schema/count/subset checks.
FIDELITY_TARGETS = ROOT / "reports/p2b_b7_claim_fidelity_targets_20261126.json"
OUTPUT = ROOT / "reports/p2b_b8_comparison_20261126.json"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def read_json(path: Path):
    raw = path.read_bytes()
    return json.loads(raw), sha(raw)


def compare_structured(row: dict) -> dict:
    # Reuse the exact historical comparator, including its condition-grounding
    # checks, instead of reimplementing the structured arm here.
    return compare_structured_baseline_contract(row)


def compare_natural(row: dict) -> dict:
    extraction = extract_canonical_claim_evidence(
        row["answer"], question_text=row["question"], topic_ids=[row["topic_id"]],
    )
    result = audit_relation_recognition(
        question_text=row["question"], answer_text=row["answer"],
        topic_id=row["topic_id"], requirement_id=row["requirement_id"],
    )
    return {
        "observed": result["status"],
        "reason": result["reason"],
        "claim_count": len(extraction["canonical_evidence"]["claims"]),
        "unresolved_span_count": len(extraction.get("unresolved_spans", [])),
        "claim_fidelity_check_count": len(result.get("claim_fidelity_checks", [])),
        "claim_fidelity_failure_count": len(result.get("claim_fidelity_failures", [])),
    }


def summarize(rows: list[dict]) -> dict:
    return {
        "count": len(rows),
        "observed": dict(sorted(Counter(row["observed"] for row in rows).items())),
        "expected": dict(sorted(Counter(row["expected"] for row in rows).items())),
        "agreements": sum(row["observed"] == row["expected"] for row in rows),
        "disagreements": sum(row["observed"] != row["expected"] for row in rows),
        "execution_errors": sum(row["observed"] == "EXECUTION_ERROR" for row in rows),
    }


def run_mock_guard_probes(reviewed_cases: list[dict]) -> list[dict]:
    """Use crafted mock responses only to verify fail-closed fidelity guards."""
    by_id = {row["case_id"]: row for row in reviewed_cases}
    probes = [
        ("GEN-09", "mass_flow", "equivalent_to", "density_volume_flow_product"),
        ("GEN-26", "emc_protective_earth", "distinct_from", "emc_signal_reference"),
    ]
    results = []
    for case_id, subject, predicate, object_ in probes:
        row = by_id[case_id]
        source_text = row["answer"]
        claim = {
            "subject": subject, "predicate": predicate, "object": object_,
            "polarity": "positive", "conditions": [],
            "assertion_context": "asserted", "source_text": source_text,
            "source_span": {"start": 0, "end": len(source_text)},
            "extraction_confidence": 0.99,
        }

        class Mock:
            def __call__(self, request):
                # The case identifier/label is intentionally not in request.
                return {"claims": [claim]}

        extracted = extract_with_provider(
            question_text=row["question"], answer_text=source_text,
            topic_id=row["topic_id"], provider=Mock(),
        )
        comparison = evaluate_extracted_evidence(
            question_text=row["question"], answer_text=source_text,
            topic_id=row["topic_id"], requirement_id=row["requirement_id"],
            canonical_evidence=extracted["canonical_evidence"],
        )
        results.append({
            "case_id": case_id,
            "source": "crafted_mock_response_not_model_output",
            "raw_contract_status": comparison["raw_contract_result"]["status"],
            "raw_reason": comparison["raw_contract_result"]["reason"],
            "claim_fidelity_status": comparison["claim_fidelity"]["status"],
            "grounded_status": comparison["grounded_diagnostic_result"]["status"],
            "grounded_reason": comparison["grounded_diagnostic_result"]["reason"],
            "score_admission": comparison["score_admission"],
            "score_effect": comparison["score_effect"],
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    contract, contract_sha = read_json(CONTRACT)
    base, base_sha = read_json(BASE_CASES)
    reviewed, reviewed_sha = read_json(REVIEWED_CASES)
    targets, targets_sha = read_json(FIDELITY_TARGETS)
    if contract.get("score_admission") != "DISABLED" or contract.get("score_effect") != "none":
        raise SystemExit("experiment authority contract mismatch")
    if len(base.get("structured", [])) != 64 or len(base.get("natural", [])) != 47:
        raise SystemExit("base fixture counts differ from contract")
    if len(reviewed.get("cases", [])) != 36:
        raise SystemExit("reviewed fixture count differs from contract")
    target_ids = {row["case_id"] for row in targets.get("targets", [])}
    control_ids = {row["case_id"] for row in targets.get("controls", [])}
    reviewed_ids = {row["case_id"] for row in reviewed["cases"]}
    base_natural_ids = {row["case_id"] for row in base["natural"]}
    if len(target_ids) != 28 or len(control_ids) != 16 or not target_ids <= (reviewed_ids | base_natural_ids) or not control_ids <= reviewed_ids:
        raise SystemExit("focus/control subsets do not match available public cases")
    if target_ids & control_ids:
        raise SystemExit("focus and controls overlap unexpectedly")

    structured = []
    for row in base["structured"]:
        try:
            value = compare_structured(row)
        except Exception as error:
            value = {"observed": "EXECUTION_ERROR", "error_type": type(error).__name__}
        structured.append({"case_id": row["case_id"], "expected": row["expected_reference"], **value})
    natural_rows = []
    source_sets = [("natural_47", base["natural"]), ("reviewed_36", reviewed["cases"])]
    ids_seen: set[str] = set()
    input_to_cases: dict[str, list[str]] = {}
    input_topics: set[str] = set()
    for set_name, cases in source_sets:
        for row in cases:
            if row["case_id"] in ids_seen:
                raise SystemExit("overlapping natural case IDs; unique count would be overstated")
            ids_seen.add(row["case_id"])
            input_fingerprint = sha(json.dumps(
                {"topic_id": row["topic_id"], "question": row["question"], "answer": row["answer"]},
                ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8"))
            input_to_cases.setdefault(input_fingerprint, []).append(row["case_id"])
            input_topics.add(row["topic_id"])
            try:
                value = compare_natural(row)
            except Exception as error:
                value = {"observed": "EXECUTION_ERROR", "error_type": type(error).__name__}
            natural_rows.append({
                "set": set_name,
                "case_id": row["case_id"],
                "expected": row["expected_technical_subrelation"],
                "label_status": row.get("label_status", "DEVELOPMENT_FIXTURE_NOT_INDEPENDENT_HUMAN"),
                **value,
            })
    if len(natural_rows) != 83:
        raise SystemExit("unique natural input count is not 83")
    duplicate_input_groups = [sorted(values) for values in input_to_cases.values() if len(values) > 1]

    live_ready = all(os.getenv(name) for name in (
        "VALIDATION_GEMINI_API_KEY", "P2B8_GEMINI_MODEL", "P2B8_APPROVED_BUDGET_USD",
    )) and os.getenv("VALIDATION_LIVE_API") == "1"
    result = {
        "schema_version": "p2b_b8_comparison.v1",
        "baseline_checkout": git("rev-parse", "HEAD"),
        "code_file_sha256": {
            name: sha((ROOT / name).read_bytes())
            for name in (
                "grading/evidence/p2b8_llm_claim_extractor.py",
                "grading/evidence/gemini_semantic_provider.py",
                "scripts/audit_relation_recognition.py",
                "tests/test_p2b_b8_llm_claim_extractor.py",
                "reports/run_p2b_b8_experiment_20261126.py",
            )
        },
        "inputs": {
            str(CONTRACT.relative_to(ROOT)): contract_sha,
            str(BASE_CASES.relative_to(ROOT)): base_sha,
            str(REVIEWED_CASES.relative_to(ROOT)): reviewed_sha,
            str(FIDELITY_TARGETS.relative_to(ROOT)): targets_sha,
            "contract_referenced_b8_target_path": "MISSING; used existing B7 target artifact after count/subset verification",
        },
        "unique_counts": {"structured_cases": 64, "natural_case_rows": 83,
                           "distinct_natural_question_answer_topic_inputs": len(input_to_cases),
                           "natural_exact_duplicate_groups": duplicate_input_groups,
                           "distinct_topics_in_natural_inputs": len(input_topics),
                           "natural_topic_ids": sorted(input_topics),
                           "base_case_rows": 147,
                           "focus_targets_subset": 28, "defensive_controls_subset": 16,
                           "additional_unique_for_focus_or_controls": 0},
        "A_deterministic": {
            "structured": summarize(structured),
            "natural": summarize(natural_rows),
            "records": {"structured": structured, "natural": natural_rows},
        },
        "B_live_llm": {
            "status": "NOT_RUN",
            "reason": "dedicated validation key, explicit model/budget, and live opt-in are not configured; fixture has five topics rather than the six-topic pilot balance in the contract",
            "candidate_calls": 0,
            "model": None,
            "cost_usd": 0,
            "records": [],
        },
        "C_deterministic_then_llm": {
            "status": "NOT_RUN",
            "reason": "requires the same explicitly authorized live provider as B; no live extraction output exists",
            "candidate_calls": 0,
            "cost_usd": 0,
            "records": [],
        },
        "mock_provider": {
            "status": "CONTRACT_TESTED_ONLY",
            "test_file": "tests/test_p2b_b8_llm_claim_extractor.py",
            "is_performance_evidence": False,
            "live_cost_usd": 0,
            "guard_probes": run_mock_guard_probes(reviewed["cases"]),
        },
        "live_environment_ready": live_ready and len(input_topics) == 6,
        "human_semantic_validation": "NOT_ESTABLISHED",
        "score_admission": "DISABLED",
        "score_effect": "none",
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({
        "output": str(output),
        "A_structured": result["A_deterministic"]["structured"],
        "A_natural": result["A_deterministic"]["natural"],
        "B": result["B_live_llm"]["status"], "C": result["C_deterministic_then_llm"]["status"],
        "execution_errors": result["A_deterministic"]["structured"]["execution_errors"] + result["A_deterministic"]["natural"]["execution_errors"],
    }, ensure_ascii=False, indent=2))
    return 0 if result["A_deterministic"]["structured"]["execution_errors"] + result["A_deterministic"]["natural"]["execution_errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
