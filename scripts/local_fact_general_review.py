#!/usr/bin/env python3
"""Resumable local-LLM *screen* for the remaining approved Fact claims.

Model output is advisory. It cannot confirm the cited source text or change
approval/score state. The script sends only public Fact/Anchor text to Ollama.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request

from audit_remaining_fact_contracts import ROOT, audit


MODEL = "qwen3.5:9b"
ENDPOINT = "http://127.0.0.1:11434/api/generate"
VERDICTS = {"GENERAL_OK", "SOURCE_SCOPE", "NARROW", "UNCERTAIN"}


def prompt_for(fact: dict, anchor: dict) -> str:
    refs = fact.get("verification_refs") or []
    ref_summary = "; ".join(f"{r.get('authority_type', '')}: {r.get('citation', '')}" for r in refs[:2])
    return (
        "Conservatively screen this engineering Fact at a GENERAL PRINCIPLE level. "
        "You have NOT opened sources. Do not claim source verification. "
        "GENERAL_OK: core principle is broadly correct with stated conditions, not a universal mandate. "
        "SOURCE_SCOPE: exact standard clause, company/product claim, test method, or number needs source-specific check. "
        "NARROW: wording overstates the generally supported principle or omits a crucial condition. "
        "UNCERTAIN: cannot tell. Prefer uncertainty to invention. "
        "Return one JSON object with verdict and one short reason only.\n"
        f"Fact: {fact.get('statement', '')}\n"
        f"Conditions: {json.dumps(fact.get('relation', {}).get('conditions', []), ensure_ascii=False)}\n"
        f"Anchor: {anchor.get('statement', '')}\n"
        f"Cited reference titles (not verified): {ref_summary}"
    )


def _call(prompt: str, *, model: str, timeout: int) -> dict:
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "think": False, "format": "json",
                       "options": {"temperature": 0, "num_predict": 160}}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        envelope = json.load(response)
    parsed = json.loads(envelope.get("response") or "{}")
    verdict = parsed.get("verdict")
    if verdict not in VERDICTS:
        raise ValueError(f"invalid model verdict: {verdict!r}")
    reason = " ".join(str(parsed.get("reason") or "").split())[:400]
    if not reason:
        raise ValueError("empty model reason")
    return {"verdict": verdict, "reason": reason,
            "eval_count": envelope.get("eval_count")}


def _call_batch(items: list[dict], *, model: str, timeout: int) -> list[dict]:
    prompt = (
        "Conservatively classify every engineering claim at a GENERAL PRINCIPLE level. "
        "You have NOT read the cited sources. Never claim source verification. "
        "GENERAL_OK only if the claim is a broadly accepted principle with necessary conditions. "
        "SOURCE_SCOPE for exact company, product, standard, test-method or numeric claims needing source-specific check. "
        "NARROW when wording overstates a general principle or misses a crucial condition. "
        "UNCERTAIN when in doubt. Return JSON object with items array: "
        "each item has exact id, verdict and a reason of at most 12 words. "
        "Return exactly one result per input; omit all other commentary.\n"
        "INPUT=" + json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    )
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "think": False, "format": "json",
                       "options": {"temperature": 0, "num_predict": max(500, len(items) * 85)}}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        envelope = json.load(response)
    parsed = json.loads(envelope.get("response") or "{}")
    rows = parsed.get("items")
    expected = {item["id"] for item in items}
    if not isinstance(rows, list) or len(rows) != len(items) or {row.get("id") for row in rows} != expected:
        raise ValueError("batch model response has missing/duplicate Fact IDs")
    by_id = {}
    for row in rows:
        if row.get("verdict") not in VERDICTS or not str(row.get("reason") or "").strip():
            raise ValueError("batch model response has invalid verdict or reason")
        by_id[row["id"]] = {"verdict": row["verdict"],
                            "reason": " ".join(str(row["reason"]).split())[:400],
                            "eval_count": envelope.get("eval_count"),
                            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}
    return [by_id[item["id"]] for item in items]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--limit", type=int, default=0, help="0 means all remaining Facts")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/remaining_fact_local_review_20261030.jsonl")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit must be nonnegative")
    if args.batch_size < 1 or args.batch_size > 10:
        parser.error("--batch-size must be between 1 and 10")
    rows, audit_summary = audit(ROOT)
    facts = {f["fact_id"]: f for f in json.loads(
        (ROOT / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]}
    anchors = {}
    for path in (ROOT / "rubrics/topic_packs").glob("*/fact_anchor.json"):
        for anchor in json.loads(path.read_text(encoding="utf-8"))["anchors"]:
            anchors[(path.parent.name, anchor["anchor_id"])] = anchor
    completed = {}
    successful_lines = []
    discarded_errors = 0
    if args.output.exists():
        for line in args.output.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            if item.get("registry_sha256") != audit_summary["registry_sha256"]:
                raise ValueError("existing model review uses a different Registry SHA; choose a new output path")
            key = (item["fact_id"], item["model"])
            if key in completed:
                raise ValueError(f"duplicate local review row: {key}")
            if item["status"] == "MODEL_SCREENED":
                completed[key] = item
                successful_lines.append(line)
            else:
                discarded_errors += 1
    if discarded_errors:
        # Generated review data only: replace failed model outputs atomically
        # so the next pass can retry without duplicate Fact IDs.
        temporary = args.output.with_name(args.output.name + ".retry.tmp")
        temporary.write_text("\n".join(successful_lines) + ("\n" if successful_lines else ""), encoding="utf-8")
        os.replace(temporary, args.output)
        print(json.dumps({"discarded_model_errors_for_retry": discarded_errors}), flush=True)
    selected = rows[:args.limit] if args.limit else rows
    pending = [row for row in selected if (row["fact_id"], args.model) not in completed]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    done = 0
    with args.output.open("a", encoding="utf-8") as handle:
        for offset in range(0, len(pending), args.batch_size):
            batch = pending[offset:offset + args.batch_size]
            items = [{"id": row["fact_id"],
                      "claim": facts[row["fact_id"]].get("statement", ""),
                      "conditions": facts[row["fact_id"]].get("relation", {}).get("conditions", []),
                      "anchor": anchors[(row["topic_id"], row["anchor_id"])].get("statement", "")}
                     for row in batch]
            try:
                results = _call_batch(items, model=args.model, timeout=args.timeout)
                statuses = ["MODEL_SCREENED"] * len(batch)
            except Exception as batch_exc:
                # Do not discard an entire batch because one structured JSON
                # response was truncated. Retry each Fact independently.
                results = []
                statuses = []
                for row in batch:
                    fact = facts[row["fact_id"]]
                    anchor = anchors[(row["topic_id"], row["anchor_id"])]
                    prompt = prompt_for(fact, anchor)
                    try:
                        result = _call(prompt, model=args.model, timeout=args.timeout)
                        result["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
                        statuses.append("MODEL_SCREENED")
                    except Exception as exc:
                        result = {"verdict": "UNCERTAIN", "reason": f"local model error: {type(exc).__name__}; batch={type(batch_exc).__name__}",
                                  "eval_count": None, "prompt_sha256": ""}
                        statuses.append("MODEL_ERROR")
                    results.append(result)
            for row, result in zip(batch, results):
                record = {"fact_id": row["fact_id"], "model": args.model,
                          "registry_sha256": audit_summary["registry_sha256"], "status": statuses.pop(0), **result,
                          "technical_verification": "NOT_SOURCE_VERIFIED", "score_effect": "none"}
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                done += 1
            handle.flush()
            if done % 50 < len(batch):
                print(json.dumps({"screened_this_run": done, "elapsed_s": round(time.monotonic()-start, 1)}, ensure_ascii=False), flush=True)
    print(json.dumps({"screened_this_run": done, "requested": len(selected), "model": args.model,
                      "elapsed_s": round(time.monotonic()-start, 1)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
