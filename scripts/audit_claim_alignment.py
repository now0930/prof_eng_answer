#!/usr/bin/env python3
"""Offline, private-safe claim alignment audit against a single synthetic case.

Usage:
  python3 -B scripts/audit_claim_alignment.py --case /private/synthetic_case.json \
      --output /private/claim_alignment_audit.json

The file must contain {question_text, answer_text}. Output contains only hashes
and counts, never the answer or remote provider traffic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.scoring.deterministic_primary_grader import grade_deterministically


def audit_case(question: str, answer: str) -> dict:
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "off"}):
        baseline = grade_deterministically(
            question_text=question, answer_text=answer, qualitative_de_mode="off",
        )
    with patch.dict(os.environ, {"CLAIM_ALIGNMENT_MODE": "shadow"}):
        shadow = grade_deterministically(
            question_text=question, answer_text=answer, qualitative_de_mode="off",
        )
    fields = (
        "deterministic_score", "total_score", "requirements", "requirement_summary",
        "verdict", "official_pass_met", "high_score_met", "passing_score_allowed",
        "logic_check_evaluation",
    )
    changed = [field for field in fields if baseline.get(field) != shadow.get(field)]
    audit = shadow.get("claim_alignment_audit") or {}
    return {
        "schema_version": "claim_alignment_offline_audit.v1",
        "status": "PASS" if not changed and audit.get("status") == "SHADOW" else "FAIL",
        "question_sha256": hashlib.sha256(question.encode("utf-8")).hexdigest(),
        "answer_sha256": hashlib.sha256(answer.encode("utf-8")).hexdigest(),
        "shadow_status": audit.get("status"),
        "shadow_reason_code": audit.get("error_type"),
        "shadow_score_effect": audit.get("score_effect"),
        "alignment_fingerprint": audit.get("fingerprint"),
        "summary": audit.get("summary"),
        "changed_score_fields": changed,
        "provider_calls": shadow.get("provider_calls"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("refusing to overwrite existing audit")
    source = json.loads(args.case.read_text(encoding="utf-8"))
    if not isinstance(source, dict) or set(source) != {"question_text", "answer_text"}:
        parser.error("case must contain only question_text and answer_text")
    report = audit_case(source["question_text"], source["answer_text"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation avoids accidentally exposing or replacing private audits.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    file_desc = os.open(args.output, flags, 0o600)
    with os.fdopen(file_desc, "w", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": report["status"],
                      "shadow_status": report["shadow_status"],
                      "changed_score_fields": report["changed_score_fields"]}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
