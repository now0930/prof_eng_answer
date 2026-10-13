#!/usr/bin/env python3
"""Extract unverified Stage 6 candidates using existing container credentials."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.fact_grounded_contracts import FactGroundedContractError, fingerprint
from grading.evidence.fact_semantic_candidates import GEMINI_WORKER, build_request, parse_candidates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--input", type=Path,
                        help="Private JSON: question, answer, topic_ids (no reference labels)")
    inputs.add_argument("--case-id", choices=["sil_target_operations_issue1", "mcdc_vmodel_sil_issue1",
                                             "risk_nyquist_normal_01"],
                        help="Existing regression pilot; not an independent holdout")
    parser.add_argument("--output", type=Path, required=True, help="New private JSON artifact")
    parser.add_argument("--container", default="prof_eng_answer_bot")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; choose a new artifact path")
    if args.case_id:
        cases = [json.loads(line) for line in (ROOT / "calibration/expert_accuracy_golden.jsonl").read_text().splitlines() if line.strip()]
        case = next(row for row in cases if row["case_id"] == args.case_id)
        source = case["source"]
        fixture = json.loads((ROOT / source["path"]).read_text())
        if "source_case_id" in source:
            fixture = next(row for row in fixture["cases"] if row["case_id"] == source["source_case_id"])
        data = {"question": fixture["question"],
                "answer": fixture.get("answer") or fixture["original_answer"],
                "topic_ids": case["topic_ids"]}
    else:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    if set(data) != {"question", "answer", "topic_ids"}:
        parser.error("input must contain only question, answer and topic_ids")
    if (not all(isinstance(data[k], str) and data[k].strip() for k in ("question", "answer"))
            or not isinstance(data["topic_ids"], list)
            or not data["topic_ids"] or not all(isinstance(t, str) for t in data["topic_ids"])):
        parser.error("invalid input types")
    registry = load_approved_fact_registry(ROOT)
    facts = [f for f in registry["facts"] if f["topic_id"] in data["topic_ids"]]
    if {f["topic_id"] for f in facts} != set(data["topic_ids"]):
        parser.error("one or more topics have no approved facts")
    report = {
        "version": "fact_shadow_extraction_v1", "score_effect": "none",
        "independently_verified": False, "stage6_complete": False,
        "question_sha256": hashlib.sha256(data["question"].encode()).hexdigest(),
        "answer_sha256": hashlib.sha256(data["answer"].encode()).hexdigest(),
        "facts_sha256": fingerprint(sorted(facts, key=lambda f: f["fact_id"])),
        "requests": [], "candidates": [],
    }
    os.umask(0o077)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    failed = False
    for kind in ("question_requirement", "answer_claim"):
        request = build_request(data["question"], data["answer"], facts, kind=kind)
        started = time.monotonic()
        entry = {"kind": kind, "request_sha256": fingerprint(request)}
        try:
            proc = subprocess.run(
                ["docker", "exec", "-i", args.container, "python3", "-c", GEMINI_WORKER],
                input=json.dumps(request, ensure_ascii=False), text=True, capture_output=True,
                timeout=110, check=False,
            )
            if not proc.stdout.strip():
                raise RuntimeError("container transport failed")
            reply = json.loads(proc.stdout)
            entry["provider_response"] = reply
            if proc.returncode or reply.get("ok") is not True:
                raise RuntimeError("provider request failed")
            candidates = parse_candidates(reply["result"], question=data["question"],
                                          answer=data["answer"], kind=kind, model=reply["model"])
            if not candidates:
                raise FactGroundedContractError("empty candidate list for non-empty source")
            report["candidates"].extend(candidates)
            entry.update(ok=True, candidate_count=len(candidates))
        except Exception as error:
            # Never expose stderr, arbitrary provider error bodies or environment values.
            entry.update(ok=False, error_type=type(error).__name__)
            if isinstance(error, FactGroundedContractError):
                entry["validation_error"] = str(error)
            failed = True
        entry["elapsed_seconds"] = round(time.monotonic() - started, 3)
        report["requests"].append(entry)
    report["ok"] = not failed
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
    print(json.dumps({"ok": not failed, "candidate_count": len(report["candidates"]),
                      "independently_verified": False, "stage6_complete": False}))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
