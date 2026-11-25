"""Offline P2-B diagnostic runner; not imported by grading or pytest.
Run from a checkout of the P2-B draft branch. No production changes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.canonical_grading_evidence import (
    CanonicalEvidenceError, build_canonical_grading_evidence,
    validate_canonical_grading_evidence,
)
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.scoring.deterministic_requirement_evaluator import evaluate_deterministic_requirements
from scripts.audit_relation_recognition import audit_relation_recognition

BASE = "45c7d146e4673e885005c04535e65dc9b9d7c8a5"
CASES = ROOT / "reports/p2b_relation_cases_20261125.json"
INVENTORY = ROOT / "reports/p2b_relation_inventory_20261125"
UNCERTAIN = "RECOGNITION_UNCERTAIN"
ALLOWED_CODE_CHANGES = {
    "grading/scoring/deterministic_requirement_evaluator.py",
    "scripts/audit_relation_recognition.py",
    "reports/run_p2b_relation_diagnostic_20261125.py",
    "tests/test_deterministic_requirement_evaluator.py",
    "tests/test_audit_relation_recognition.py",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check_source():
    # Only reports/docs may differ; check working-tree bytes as well.
    for args in (("diff", "--name-only", BASE, "HEAD"),
                 ("diff", "--name-only", "HEAD")):
        changes = git(*args).splitlines()
        unexpected = [
            p for p in changes
            if not p.startswith(("reports/", "docs/"))
            and p not in ALLOWED_CODE_CHANGES
        ]
        if unexpected:
            raise RuntimeError(f"non-document drift: {unexpected}")
    for i in range(1, 7):
        batch = json.loads((INVENTORY / f"batch_{i}.json").read_text(encoding="utf-8"))
        if batch["baseline"] != BASE:
            raise RuntimeError("inventory baseline drift")
        for row in batch["rows"]:
            for key, file in (("anchor", "fact_anchor"), ("logic", "logic_check"), ("model", "model_answer")):
                path = f"rubrics/topic_packs/{row['topic']}/{file}.json"
                if git("hash-object", path) != row["source_blobs"][key]:
                    raise RuntimeError(f"source hash drift: {path}")
    if git("hash-object", "grading/evidence/approved_fact_registry.json") != "69124be63df2216e5077a1d74ddfc887503bedd5":
        raise RuntimeError("registry drift")
    for name, sha in {
        "fact_anchor_scoring_exclusions_20261101.json": "1a06463c3adfc34c95ce0d262603453394019a0e",
        "fact_anchor_independent_revision_holds_20261101.json": "798febc4034f9b9a4dc6172c8338b598fe6b81a3",
        "fact_anchor_unresolved_source_holds_20261101.json": "309cb114227b7963deeb7a03c06c20acf7807dc1",
        "fact_anchor_1656_candidate_holds_20261104.json": "714ab29da4b7d26dc901192e742990d3fb4c62ab",
    }.items():
        if git("hash-object", f"grading/evidence/{name}") != sha:
            raise RuntimeError(f"exclusion drift: {name}")


def compare_structured(row):
    fid = row["expected_fact"]["fact_id"]
    try:
        evidence = build_canonical_grading_evidence(
            question_text=row["question"], answer_text=row["answer"],
            source={"mode": "human_adapter", "resolver_id": "p2b_fixture", "resolver_version": "1"},
            claims=row["claims"],
        )
        validate_canonical_grading_evidence(evidence, answer_text=row["answer"])
    except CanonicalEvidenceError as exc:
        return {"observed": "INVALID_EVIDENCE", "validator_error": str(exc)}
    scope = {row["topic_id"]: [row["requirement_id"]] if row["scope_ok"] else []}
    evaluated = evaluate_deterministic_requirements(
        claims=evidence["claims"], invariant_codes=[], topic_ids=[row["topic_id"]],
        extraction_complete=False, requirement_scope_by_topic=scope,
    )
    target = next((r for r in evaluated["requirements"]
                   if r["owner_topic_id"] == row["topic_id"] and r["requirement_id"] == row["requirement_id"]), None)
    observed = UNCERTAIN
    if target:
        if fid in target.get("contradicted_fact_ids", []):
            observed = "CONFIRMED_CONTRADICTION"
        elif fid in target.get("matched_fact_ids", []):
            observed = "CONFIRMED_RELATION"
    # This is an observation of the existing comparator, NOT a newly
    # admitted diagnostic or grade. Do not silently impose the reference
    # guard on the result, since that would hide discrepancies.
    return {"observed": observed, "target_requirement": target,
            "raw_findings": evaluated["findings"], "evidence_sha256": evidence["evidence_sha256"]}


def compare_natural(row):
    extraction = extract_canonical_claim_evidence(
        row["answer"], question_text=row["question"], topic_ids=[row["topic_id"]])
    audit = audit_relation_recognition(
        question_text=row["question"], answer_text=row["answer"],
        topic_id=row["topic_id"], requirement_id=row["requirement_id"])
    evidence = extraction["canonical_evidence"]
    return {"observed": audit["status"], "audit": audit, "claims": evidence["claims"],
            "extraction_complete": extraction["extraction_complete"],
            "unresolved_spans": extraction["unresolved_spans"],
            "symbolic_formula_candidates": extraction["symbolic_formula_candidates"],
            "evidence_sha256": evidence["evidence_sha256"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    check_source()
    raw = CASES.read_bytes()
    cases = json.loads(raw)
    if cases["baseline_main"] != BASE or cases["score_admission"] != "DISABLED":
        raise RuntimeError("case baseline/authority mismatch")
    result = {"baseline_main": BASE, "checkout": git("rev-parse", "HEAD"),
              "cases_sha256": hashlib.sha256(raw).hexdigest(),
              "score_admission": "DISABLED", "score_effect": "none"}
    for name, comparator, expected_key in (
        ("structured", compare_structured, "expected_reference"),
        ("natural", compare_natural, "expected_technical_subrelation"),
    ):
        records = []
        for row in cases[name]:
            try:
                observation = comparator(row)
            except Exception as exc:
                observation = {"observed": "EXECUTION_ERROR", "error": f"{type(exc).__name__}: {exc}"}
            records.append({"case_id": row["case_id"], "expected": row[expected_key],
                            **observation, "agrees": observation["observed"] == row[expected_key]})
        result[name] = {"count": len(records),
                        "observed": dict(Counter(r["observed"] for r in records)),
                        "confusion": dict(Counter(r["expected"] + " -> " + r["observed"] for r in records)),
                        "agreements": sum(r["agrees"] for r in records),
                        "records": records}
    execution_errors = sum(
        row["observed"] == "EXECUTION_ERROR"
        for group in ("structured", "natural")
        for row in result[group]["records"]
    )
    result["execution_errors"] = execution_errors
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Never overwrite a previous experiment or modify source in-place.
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: {i: v for i, v in result[k].items() if i != "records"}
                      for k in ("structured", "natural")}, ensure_ascii=False, indent=2))
    print(json.dumps({"execution_errors": execution_errors}, ensure_ascii=False))
    return 1 if execution_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
