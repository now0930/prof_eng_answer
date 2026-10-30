#!/usr/bin/env python3
"""Audit all remaining Fact contracts without pretending to verify their truth.

Every row is checked for current Registry/Anchor linkage, statement and
condition shape, and evidence scope. Results are review dispositions only.
No approval, generated bank, or scoring file is changed.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

from triage_remaining_fact_recheck import ROOT, triage


FIELDS = ("fact_id", "topic_id", "anchor_id", "priority", "contract_status", "flags",
          "evidence_classes", "source_domains", "technical_verdict")
VENDOR_DOMAINS = ("emerson.com", "rockwellautomation.com", "siemens.com", "yokogawa.com", "abb.com")


def _pack_anchors(root: Path) -> dict[tuple[str, str], dict]:
    result = {}
    for path in sorted((root / "rubrics/topic_packs").glob("*/fact_anchor.json")):
        for anchor in json.loads(path.read_text(encoding="utf-8"))["anchors"]:
            key = (path.parent.name, anchor["anchor_id"])
            if key in result:
                raise ValueError(f"duplicate Topic Anchor: {key}")
            result[key] = anchor
    return result


def audit(root: Path = ROOT) -> tuple[list[dict[str, str]], dict]:
    queue, queue_summary = triage(root)
    first_batch_path = root / "reports/remaining_fact_recheck_first_batch_20261030.csv"
    with first_batch_path.open(encoding="utf-8", newline="") as handle:
        first_batch = {row["fact_id"] for row in csv.DictReader(handle)}
    expected_first = {row["fact_id"] for row in queue if row["fact_id"] in first_batch}
    if len(first_batch) != 20 or len(expected_first) != 20:
        raise ValueError("first-batch snapshot drifted from the current queue")
    remaining = [row for row in queue if row["fact_id"] not in first_batch]
    facts = {fact["fact_id"]: fact for fact in json.loads(
        (root / "grading/evidence/approved_fact_registry.json").read_text(encoding="utf-8"))["facts"]}
    anchors = _pack_anchors(root)
    output = []
    for item in remaining:
        fact = facts[item["fact_id"]]
        flags = []
        anchor = anchors.get((item["topic_id"], item["anchor_id"]))
        if anchor is None:
            flags.append("anchor_missing_or_wrong_topic")
        elif not (anchor.get("statement") or "").strip():
            flags.append("anchor_statement_empty")
        if not (fact.get("statement") or "").strip():
            flags.append("fact_statement_empty")
        relation = fact.get("relation") or {}
        if not isinstance(relation.get("conditions"), list):
            flags.append("conditions_not_list")
        refs = fact.get("verification_refs") or []
        if not refs:
            flags.append("verification_refs_missing")
        domains = set()
        types = set()
        for ref in refs:
            types.add(ref.get("authority_type") or "unknown")
            url = ref.get("url")
            if url:
                parsed = urlparse(url)
                if parsed.scheme not in {"https", "http"} or not parsed.hostname:
                    flags.append("invalid_source_url")
                else:
                    domains.add(parsed.hostname.lower())
            elif ref.get("authority_type") != "calculation":
                flags.append("noncalculation_url_missing")
            if not (ref.get("locator") or "").strip():
                flags.append("locator_missing")
        vendor_only = bool(domains) and all(any(domain == vendor or domain.endswith("." + vendor)
                                               for vendor in VENDOR_DOMAINS) for domain in domains)
        if "universal_or_mandatory" in item["signals"].split(";") and vendor_only:
            flags.append("universal_wording_vendor_only")
        if "vendor_specific" in item["signals"].split(";"):
            flags.append("company_or_model_scope_check")
        if "numeric_or_formula" in item["signals"].split(";"):
            flags.append("numeric_condition_check")
        if "standard_or_clause" in item["signals"].split(";"):
            flags.append("standard_scope_check")
        flags = sorted(set(flags))
        hard = {"anchor_missing_or_wrong_topic", "anchor_statement_empty", "fact_statement_empty",
                "conditions_not_list", "verification_refs_missing", "invalid_source_url",
                "noncalculation_url_missing", "locator_missing"}
        status = "CONTRACT_ISSUE" if hard.intersection(flags) else "SCOPE_REVIEW" if flags else "CONTRACT_PASS"
        output.append({"fact_id": item["fact_id"], "topic_id": item["topic_id"],
                       "anchor_id": item["anchor_id"], "priority": item["priority"],
                       "contract_status": status, "flags": ";".join(flags),
                       "evidence_classes": ";".join(sorted(types)),
                       "source_domains": ";".join(sorted(domains)),
                       "technical_verdict": "NOT_ASSESSED"})
    if len(output) != len(queue) - len(first_batch) or len({row["fact_id"] for row in output}) != len(output):
        raise ValueError("remaining Fact inventory drifted; regenerate the queue and audit plan")
    counts = Counter(row["contract_status"] for row in output)
    flag_counts = Counter(flag for row in output for flag in row["flags"].split(";") if flag)
    summary = {"contract": "remaining-fact-contract-audit-v1",
               "registry_sha256": queue_summary["registry_sha256"],
               "reviewed_first_batch": 20, "audited_remaining": len(output),
               "contract_status_counts": dict(sorted(counts.items())),
               "flag_counts": dict(sorted(flag_counts.items())),
               "technical_verdict": "NOT_ASSESSED",
               "score_effect": "none"}
    return output, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-csv", type=Path, default=ROOT / "reports/remaining_fact_contract_audit_20261030.csv")
    parser.add_argument("--output-json", type=Path, default=ROOT / "reports/remaining_fact_contract_audit_20261030.json")
    args = parser.parse_args()
    rows, summary = audit()
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    args.output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
