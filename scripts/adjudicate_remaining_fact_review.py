#!/usr/bin/env python3
"""Combine deterministic Fact scope flags with advisory local-LLM screens.

This produces *review actions*, not source verification or approval. A model
cannot override a structural/scope flag to GENERAL_PRINCIPLE_CANDIDATE.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from audit_remaining_fact_contracts import ROOT, audit


FIELDS = ("fact_id", "topic_id", "anchor_id", "priority", "review_action", "contract_status",
          "flags", "model_verdict", "model_reason", "technical_verification")


def action_for(contract: dict, model: dict) -> str:
    flags = set(filter(None, contract["flags"].split(";")))
    if contract["contract_status"] == "CONTRACT_ISSUE" or model["status"] != "MODEL_SCREENED":
        return "HOLD_CONTRACT_OR_MODEL_ERROR"
    if model["verdict"] == "UNCERTAIN":
        return "HOLD_UNCERTAIN"
    if model["verdict"] == "NARROW":
        return "NARROW_CLAIM_REVIEW"
    if flags & {"universal_wording_vendor_only", "company_or_model_scope_check", "standard_scope_check"}:
        return "SOURCE_SCOPE_REVIEW"
    if model["verdict"] == "SOURCE_SCOPE":
        return "SOURCE_SCOPE_REVIEW"
    if "numeric_condition_check" in flags:
        return "NUMERIC_CONDITION_REVIEW"
    return "GENERAL_PRINCIPLE_CANDIDATE"


def adjudicate(root: Path = ROOT, *, model_path: Path | None = None) -> tuple[list[dict[str, str]], dict]:
    contracts, contract_summary = audit(root)
    model_path = model_path or root / "reports/remaining_fact_local_review_20261030.jsonl"
    model_rows = {}
    for line in model_path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        fact_id = row["fact_id"]
        if fact_id in model_rows:
            raise ValueError(f"duplicate model Fact ID: {fact_id}")
        if row["registry_sha256"] != contract_summary["registry_sha256"]:
            raise ValueError(f"stale model review: {fact_id}")
        model_rows[fact_id] = row
    expected = {row["fact_id"] for row in contracts}
    if set(model_rows) != expected:
        raise ValueError(f"incomplete local model review: missing={len(expected-set(model_rows))}, extra={len(set(model_rows)-expected)}")
    output = []
    for contract in contracts:
        model = model_rows[contract["fact_id"]]
        output.append({"fact_id": contract["fact_id"], "topic_id": contract["topic_id"],
                       "anchor_id": contract["anchor_id"], "priority": contract["priority"],
                       "review_action": action_for(contract, model),
                       "contract_status": contract["contract_status"], "flags": contract["flags"],
                       "model_verdict": model["verdict"], "model_reason": model["reason"],
                       "technical_verification": "NOT_SOURCE_VERIFIED"})
    counts = Counter(row["review_action"] for row in output)
    return output, {"contract": "remaining-fact-general-review-actions-v1",
                    "registry_sha256": contract_summary["registry_sha256"],
                    "rows": len(output), "review_action_counts": dict(sorted(counts.items())),
                    "final_technical_approvals": 0,
                    "score_effect": "none"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-jsonl", type=Path)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "reports/remaining_fact_review_actions_20261030.csv")
    parser.add_argument("--output-json", type=Path, default=ROOT / "reports/remaining_fact_review_actions_20261030.json")
    args = parser.parse_args()
    rows, summary = adjudicate(model_path=args.model_jsonl)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
