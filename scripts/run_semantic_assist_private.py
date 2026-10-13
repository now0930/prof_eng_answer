#!/usr/bin/env python3
"""Run score-neutral LLM assistance on a privately scoped question contract.

Input JSON: question, answer, topic_ids, question_contract. Both output and
SQLite cache must live outside the public repository. No score is produced.
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
from grading.evidence.fact_grounded_contracts import fingerprint, validate_question_contract
from grading.evidence.fact_unresolved_queue import assist_parser_unresolved
from grading.evidence.gemini_semantic_provider import GeminiSemanticProvider, docker_urlopen
from grading.evidence.private_semantic_cache import PrivateSemanticCache


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--model", default=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    parser.add_argument("--review-model", default=os.getenv("GEMINI_REVIEW_MODEL"))
    parser.add_argument("--container", help="Existing container with Gemini key; key remains there")
    parser.add_argument("--max-items", type=int, default=3,
                        help="Limit primary requests per case (default: 3; each may require reviews)")
    args = parser.parse_args(argv)
    if not 0 <= args.max_items <= 20:
        parser.error("max-items must be between 0 and 20")
    for target in (args.output, args.cache):
        if not target.is_absolute() or target.resolve().is_relative_to(ROOT):
            parser.error("private output and cache must be absolute paths outside the repository")
    if args.output.exists() or args.output.is_symlink():
        parser.error("output already exists")
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {
            "question", "answer", "topic_ids", "question_contract",
        }:
            raise ValueError("invalid private input fields")
        question, answer, topic_ids = (payload[k] for k in ("question", "answer", "topic_ids"))
        if (not isinstance(question, str) or not question.strip()
                or not isinstance(answer, str)
                or not isinstance(topic_ids, list) or not topic_ids
                or len(topic_ids) != len(set(topic_ids))
                or not all(isinstance(t, str) and t.strip() for t in topic_ids)):
            raise ValueError("invalid private input content")
        registry = load_approved_fact_registry(ROOT)
        facts = [f for f in registry["facts"] if f["topic_id"] in topic_ids]
        if {f["topic_id"] for f in facts} != set(topic_ids):
            raise ValueError("requested Topic has no approved Facts")
        contract = payload["question_contract"]
        if contract.get("knowledge_snapshot_sha256") != fingerprint(
            sorted(facts, key=lambda f: f["fact_id"])
        ):
            raise ValueError("question contract Fact snapshot mismatch")
        validate_question_contract(contract, question, {f["fact_id"] for f in facts})
        review_model = args.review_model or args.model
        transport = docker_urlopen(args.container) if args.container else None
        # The bridge reads GEMINI_API_KEY only inside the existing container.
        provider_key = "container-managed" if args.container else None
        versions = {"model": args.model, "prompt": "unresolved-semantic-assist-v1",
                    "parser": "canonical_claim_extractor-v1",
                    "verifier": "semantic-review-v1", "policy": "shadow-no-score-v1"}
        with PrivateSemanticCache(args.cache, repository_root=ROOT) as cache:
            result = assist_parser_unresolved(
                question_text=question, answer_text=answer, topic_ids=topic_ids,
                facts=facts, question_contract=contract, versions=versions,
                provider=GeminiSemanticProvider(model=args.model, api_key=provider_key,
                                                urlopen=transport),
                enabled=True, cache=cache,
                reviewer_provider=GeminiSemanticProvider(model=review_model, api_key=provider_key,
                                                         urlopen=transport),
                reviewer_version=review_model, reviewer_cache=cache,
                max_items=args.max_items,
            )
        report = {
            "schema_version": "semantic-assist-private-run-v1",
            "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
            "answer_sha256": hashlib.sha256(answer.encode()).hexdigest(),
            "facts_sha256": contract["knowledge_snapshot_sha256"],
            "question_contract_sha256": fingerprint(contract),
            "versions": versions, "reviewer_model": review_model,
            "question_scope_status": "provisional_unreviewed",
            "scope_complete": False,
            "result": result, "score_effect": "none", "final_grade_allowed": False,
        }
        fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(report, output, ensure_ascii=False, indent=2)
        print(json.dumps({"queued_count": result["queued_count"],
                          "primary_calls": result["assistance"]["provider_calls"],
                          "reviewer_calls": result["reviewer_calls"],
                          "final_grade_allowed": False}))
        return 0
    except Exception as error:
        # Output only exception class; provider errors may contain private text.
        print(json.dumps({"ok": False, "error_type": type(error).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
