"""Non-scoring P2-B7 Claim-fidelity replay for public synthetic fixtures."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.claim_fidelity_audit import assess_claim_fidelity
from scripts.audit_relation_recognition import audit_relation_recognition


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target_doc_path = ROOT / "reports/p2b_b7_claim_fidelity_targets_20261126.json"
    reviewed_path = ROOT / "reports/p2b_generalization_reviewed_cases_20261126.json"
    original_path = ROOT / "reports/p2b_generalization_cases_20261125.json"
    targets = json.loads(target_doc_path.read_text(encoding="utf-8"))
    reviewed = json.loads(reviewed_path.read_text(encoding="utf-8"))
    original = json.loads(original_path.read_text(encoding="utf-8"))
    question_by_req = {}
    for row in [*reviewed["cases"], *original["cases"]]:
        question_by_req.setdefault((row["topic_id"], row["requirement_id"]), row["question"])

    records = []
    for row in targets["targets"]:
        question = question_by_req.get((row["topic_id"], row["requirement_id"]), "")
        extraction = extract_canonical_claim_evidence(
            row["answer"], question_text=question, topic_ids=[row["topic_id"]],
        )
        audit = audit_relation_recognition(
            question_text=question, answer_text=row["answer"], topic_id=row["topic_id"],
            requirement_id=row["requirement_id"],
        )
        expected = row.get("expected_contract_claim_if_grounded")
        candidates = extraction["canonical_evidence"]["claims"]
        exact = [c for c in candidates if expected and all(c.get(k) == expected.get(k)
                 for k in ("subject", "predicate", "object", "polarity"))]
        if exact:
            fidelity = assess_claim_fidelity(
                answer_text=row["answer"], claim=exact[0], topic_id=row["topic_id"],
                expected_claim=expected,
            )
        elif expected is None and candidates:
            fidelity = assess_claim_fidelity(
                answer_text=row["answer"], claim=candidates[0], topic_id=row["topic_id"],
            )
        else:
            fidelity = {"status": "NOT_ESTABLISHED", "reason": "EXPECTED_CLAIM_NOT_EXTRACTED", "score_effect": "none"}
        records.append({
            "case_id": row["case_id"], "category": row["category"],
            "expected_technical_subrelation": row["expected_technical_subrelation"],
            "observed_diagnostic": audit["status"], "diagnostic_reason": audit["reason"],
            "claim_fidelity": fidelity,
            "extracted_claim_count": len(candidates),
            "evidence_spans": audit["evidence_spans"], "score_effect": "none",
        })

    controls = []
    reviewed_by_id = {r["case_id"]: r for r in reviewed["cases"]}
    for row in targets.get("controls", []):
        source = reviewed_by_id.get(row["case_id"])
        if source is None:
            continue
        audit = audit_relation_recognition(
            question_text=source["question"], answer_text=source["answer"],
            topic_id=source["topic_id"], requirement_id=source["requirement_id"],
        )
        controls.append({
            "case_id": row["case_id"], "expected": row["expected_technical_subrelation"],
            "observed": audit["status"], "reason": audit["reason"],
            "score_effect": "none",
        })

    result = {
        "schema_version": "p2b_b7_diagnostic.v1",
        "code_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "working_tree_diff_sha256": hashlib.sha256(subprocess.check_output(["git", "diff", "HEAD"], cwd=ROOT)).hexdigest(),
        "target_fixture_sha256": sha(target_doc_path),
        "reviewed_36_sha256": sha(reviewed_path),
        "original_36_sha256": sha(original_path),
        "score_admission": "DISABLED", "score_effect": "none",
        "independent_accuracy": "NOT_ESTABLISHED",
        "targets": {"count": len(records), "observed": dict(Counter(r["observed_diagnostic"] for r in records)),
                    "fidelity": dict(Counter(r["claim_fidelity"]["status"] for r in records)), "records": records},
        "controls": {"count": len(controls), "observed": dict(Counter(r["observed"] for r in controls)), "records": controls},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k in {"targets", "controls", "score_admission", "score_effect"} and k != "targets" and k != "controls"}, ensure_ascii=False))
    print(json.dumps({"target_count": len(records), "diagnostic": result["targets"]["observed"], "fidelity": result["targets"]["fidelity"], "control_count": len(controls), "control_observed": result["controls"]["observed"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
