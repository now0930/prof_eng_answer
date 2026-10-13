#!/usr/bin/env python3
"""Prepare limited, answer-independent question scopes for three private pilots.

These manually selected Fact references exercise transport and abstention only.
They do not certify complete question scope or authorize a final grade.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_grounded_contracts import VERSION, fingerprint, validate_question_contract


SCOPES = {
    "sil_target_operations_issue1": [
        ("SIL 결정 방법", "explain", ["sil_sis_sif_scope", "sil_target_pfd_relation"]),
        ("실제 플랜트 운영", "apply", ["sil_proof_test_pst_role"]),
        ("최신 산업 이슈", "explain", ["ot_cyber_safety_risk_and_ai_code_lifecycle_boundary"]),
    ],
    "mcdc_vmodel_sil_issue1": [
        ("V-Model", "explain", ["v_model_design_test_mapping"]),
        ("단위·통합·시스템시험", "explain", [
            "sw04_unit_test_verifies_isolated_software_units",
            "sw04_integration_test_verifies_software_interfaces",
            "sw04_system_test_checks_system_requirements_in_intended_environment",
        ]),
        ("MC/DC", "explain", ["mcdc_structural_criterion_targets_independent_condition_effect"]),
    ],
    "risk_nyquist_normal_01": [
        ("임계점", "explain", ["nyquist_minus_one_critical_point"]),
        ("P, N, Z 관계", "explain", ["argument_principle_pnz_relation"]),
    ],
}


def prepare(case_id: str) -> dict:
    cases = [json.loads(line) for line in
             (ROOT / "calibration/expert_accuracy_golden.jsonl").read_text(encoding="utf-8").splitlines()
             if line.strip()]
    case = next(row for row in cases if row["case_id"] == case_id)
    source = case["source"]
    fixture = json.loads((ROOT / source["path"]).read_text(encoding="utf-8"))
    if "source_case_id" in source:
        fixture = next(row for row in fixture["cases"] if row["case_id"] == source["source_case_id"])
    question = fixture["question"]
    answer = fixture.get("answer") or fixture["original_answer"]
    registry = load_approved_fact_registry(ROOT)
    facts = [row for row in registry["facts"] if row["topic_id"] in case["topic_ids"]]
    known = {row["fact_id"] for row in facts}
    requirements = []
    for index, (phrase, task, refs) in enumerate(SCOPES[case_id], start=1):
        if question.count(phrase) != 1 or not set(refs) <= known:
            raise ValueError("pilot question scope is no longer valid")
        start = question.index(phrase)
        requirements.append({
            "requirement_id": f"pilot_{index}",
            "source_span": {"start": start, "end": start + len(phrase)},
            "source_text": phrase, "task": task, "fact_refs": refs,
            "resolution": "resolved",
        })
    contract = {
        "schema_version": VERSION,
        "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
        "knowledge_snapshot_sha256": fingerprint(sorted(facts, key=lambda row: row["fact_id"])),
        "requirements": requirements, "score_effect": "none",
    }
    validate_question_contract(contract, question, known)
    return {"question": question, "answer": answer,
            "topic_ids": case["topic_ids"], "question_contract": contract}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", choices=sorted(SCOPES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    output = args.output
    if not output.is_absolute() or output.resolve().is_relative_to(ROOT):
        parser.error("pilot input must be outside the public repository")
    if output.exists() or output.is_symlink():
        parser.error("output already exists")
    payload = prepare(args.case_id)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False)
    print(json.dumps({"case_id": args.case_id,
                      "provisional_requirements": len(payload["question_contract"]["requirements"]),
                      "scope_complete": False, "final_grade_allowed": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
