"""Replay 12 frozen ChatGPT review responses through existing P2-B8 Python paths.
Not live provider evaluation; no credentials, network, grading authority or private answers.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.p2b8_llm_claim_extractor import (
    extract_with_provider, evaluate_extracted_evidence, combine_deterministic_first,
)
from scripts.audit_relation_recognition import audit_relation_recognition

FROZEN = ROOT / "reports/p2b_chatgpt_recorded_responses_20261126.json"
PILOT = ROOT / "reports/p2b_b8l_experiment_contract_20261126.json"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def input_key(question, answer, topic_id):
    return question, answer, topic_id

class RecordedProvider:
    model = "chatgpt_direct_review_recorded_not_api"

    def __init__(self, responses):
        self.responses = responses
        self.calls = 0

    def __call__(self, request):
        assert not {"case_id", "expected_label", "expected_claim", "fact", "facts"} & set(request)
        key = input_key(request["question"], request["answer"], request["topic_id"])
        self.calls += 1
        return copy.deepcopy(self.responses[key])

def summary(records, arm, field=None):
    from collections import Counter
    results = []
    for row in records:
        value = row.get(arm, {})
        if field:
            value = value.get(field, {})
        results.append(value.get("status", "EXECUTION_ERROR"))
    return {"count": len(records), "observed": dict(Counter(results)),
            "agreements": sum(result == row["expected"] for result, row in zip(results, records)),
            "errors": results.count("EXECUTION_ERROR")}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    source = ROOT / frozen["source_fixture"]
    source_raw = source.read_bytes()
    if sha(source_raw) != frozen["source_fixture_sha256"]:
        raise SystemExit("source fixture drift")
    cases = {r["case_id"]: r for r in json.loads(source_raw)["cases"]}
    ids = json.loads(PILOT.read_text(encoding="utf-8"))["datasets"]["pilot"]["cases"]
    entries = {r["case_id"]: r for r in frozen["records"]}
    if len(ids) != 12 or len(entries) != 12 or set(ids) != set(entries):
        raise SystemExit("pilot mismatch")
    responses = {}
    for case_id in ids:
        row = cases[case_id]
        key = input_key(row["question"], row["answer"], row["topic_id"])
        if key in responses:
            raise SystemExit("duplicate pilot input")
        responses[key] = entries[case_id]["response"]
    provider = RecordedProvider(responses)
    records = []
    sensitivity = None
    for case_id in ids:
        row = cases[case_id]
        kw = {"question_text": row["question"], "answer_text": row["answer"], "topic_id": row["topic_id"]}
        comparison_kw = {**kw, "requirement_id": row["requirement_id"]}
        item = {"case_id": case_id, "expected": row["expected_technical_subrelation"]}
        try:
            a = extract_canonical_claim_evidence(row["answer"], question_text=row["question"], topic_ids=[row["topic_id"]])
            item["A"] = audit_relation_recognition(**comparison_kw)
            b = extract_with_provider(**kw, provider=provider)
            evidence = b["canonical_evidence"]
            item["B"] = evaluate_extracted_evidence(**comparison_kw, canonical_evidence=evidence)
            item["B_claims"] = evidence["claims"]
            item["request_sha256"] = b["request_sha256"]
            item["prompt_sha256"] = b["prompt_sha256"]
            c = combine_deterministic_first(**kw, deterministic_evidence=a["canonical_evidence"],
                llm_evidence=evidence, deterministic_unresolved_spans=a.get("unresolved_spans", []))
            item["C"] = evaluate_extracted_evidence(**comparison_kw, canonical_evidence=c)
            item["C_claims"] = c["claims"]
            if case_id == "GEN-20":
                strict = extract_with_provider(**kw, provider=lambda request: {"claims": []})
                sensitivity = evaluate_extracted_evidence(**comparison_kw, canonical_evidence=strict["canonical_evidence"])
        except Exception as exc:
            item["error_type"] = type(exc).__name__
        records.append(item)
    result = {
        "schema_version": "p2b_chatgpt_recorded_replay.v1",
        "code_sha": git("rev-parse", "HEAD"),
        "tree_sha": git("rev-parse", "HEAD^{tree}"),
        "tracked_diff_sha256": sha(subprocess.check_output(["git", "diff", "HEAD"], cwd=ROOT)),
        "source_fixture_sha256": sha(source_raw),
        "recorded_responses_sha256": sha(FROZEN.read_bytes()),
        "pilot_contract_sha256": sha(PILOT.read_bytes()),
        "source": frozen["source"],
        "recorded_provider_calls": provider.calls,
        "live_api_calls": 0,
        "live_provider_status": "NOT_RUN",
        "score_admission": "DISABLED", "score_effect": "none",
        "independent_accuracy": "NOT_ESTABLISHED",
        "protected_143_replay": "NOT_RUN",
        "summary": {
            "A": summary(records, "A"),
            "B_raw": summary(records, "B", "raw_contract_result"),
            "B_grounded": summary(records, "B", "grounded_diagnostic_result"),
            "C_raw": summary(records, "C", "raw_contract_result"),
            "C_grounded": summary(records, "C", "grounded_diagnostic_result"),
        },
        "GEN-20_strict_subject_sensitivity": sensitivity,
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return int(any("error_type" in row for row in records))

if __name__ == "__main__":
    raise SystemExit(main())
