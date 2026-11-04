"""Validate the private 1,656-row proposal and build fail-closed review data.

This tool does not approve any Fact or edit a Topic Pack. The source CSV and
full staging JSON stay outside the public repository.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_BUCKETS = {
    "PREVIOUS_STRICT_VERDICT_RETAINED": 415,
    "SOURCE_MATCHED_TEXT_REVISED_29": 29,
    "RELAXED_TEXTBOOK_CANDIDATE_937": 937,
    "REVISED_199_SUPPORTED_CANDIDATE": 36,
    "REVISED_199_SCOPE_CANDIDATE": 133,
    "REVISED_199_HOLD_SOURCE_17": 17,
    "REVISED_199_HOLD_FORMULA_SAFETY_8": 8,
    "EXCLUDE_NONSCORING_76": 76,
    "EXCLUDE_NONFACT_ROUTING_5": 5,
}
REASONS = {
    "REVISED_199_HOLD_SOURCE_17": "candidate_source_review_pending",
    "REVISED_199_HOLD_FORMULA_SAFETY_8": "candidate_formula_safety_review_pending",
    "EXCLUDE_NONSCORING_76": "candidate_non_scoring_metadata",
    "EXCLUDE_NONFACT_ROUTING_5": "candidate_nonfact_routing_metadata",
}
LEGACY_CONTRACT_CONFLICTS = {
    ("nyquist_stability_criterion_gain_phase_margin", "argument_principle_pnz_relation"),
    ("sil_target_determination_risk_reduction_and_lifecycle", "required_rrf_relation"),
    ("sil_target_determination_risk_reduction_and_lifecycle", "target_pfd_relation"),
}


def build(repo: Path, source_csv: Path) -> tuple[list[dict], list[dict]]:
    with source_csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 1656:
        raise ValueError(f"expected 1656 rows, got {len(rows)}")
    buckets = Counter(row["latest_final_proposal_bucket_NOT_APPROVED"] for row in rows)
    if buckets != EXPECTED_BUCKETS:
        raise ValueError(f"unexpected proposal buckets: {buckets}")
    anchors = {}
    for path in sorted((repo / "rubrics/topic_packs").glob("*/fact_anchor.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        for anchor in pack["anchors"]:
            key = (pack["topic_id"], anchor["anchor_id"])
            if key in anchors:
                raise ValueError(f"duplicate Topic Anchor: {key}")
            anchors[key] = anchor

    seen = set()
    staged = []
    holds = []
    for row in rows:
        key = (row["topic_id"], row["anchor_id"])
        if key in seen:
            raise ValueError(f"duplicate proposal key: {key}")
        seen.add(key)
        anchor = anchors.get(key)
        if anchor is None:
            raise ValueError(f"missing Topic Anchor: {key}")
        original = anchor["statement"]
        digest = hashlib.sha256(original.encode("utf-8")).hexdigest()
        if row["original_statement"] != original or row["statement_sha256"] != digest:
            raise ValueError(f"original statement/hash mismatch: {key}")
        candidate = row["canonical_candidate_statement_NOT_OPERATIONAL"]
        if hashlib.sha256(candidate.encode("utf-8")).hexdigest() != row["candidate_statement_sha256_NOT_ORIGINAL"]:
            raise ValueError(f"candidate hash mismatch: {key}")
        if row["runtime_operational_approval_new"] != "NO":
            raise ValueError(f"unexpected operational approval: {key}")
        bucket = row["latest_final_proposal_bucket_NOT_APPROVED"]
        staged.append({
            "topic_id": key[0], "anchor_id": key[1],
            "original_statement_sha256": digest,
            "strict_verdict_immutable": row["strict_verdict_immutable"],
            "candidate_statement": candidate,
            "candidate_statement_sha256": row["candidate_statement_sha256_NOT_ORIGINAL"],
            "candidate_verdict": row["latest_technical_verdict_CANDIDATE_NOT_APPROVED"],
            "evidence_tier": row["evidence_tier"],
            "gate": row["latest_gate"],
            "approval_status": "NOT_APPROVED",
            "risk_flags": row["risk_flags"],
            "score_contract_id": "",
            "source_locator": "",
            "proposal_bucket": bucket,
        })
        # The new proposal is held, but these three *existing* canonical
        # requirements remain live until source review resolves the conflict.
        # Silently disabling them breaks protected SIL/Nyquist Golden tests.
        if bucket in REASONS and key not in LEGACY_CONTRACT_CONFLICTS:
            holds.append({
                "topic_id": key[0], "anchor_id": key[1],
                "statement_sha256": digest, "reason": REASONS[bucket],
            })
    if len(holds) != 103:
        raise ValueError(f"expected 103 holds, got {len(holds)}")
    return staged, sorted(holds, key=lambda row: (row["topic_id"], row["anchor_id"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-csv", type=Path, required=True)
    parser.add_argument("--private-stage", type=Path, required=True)
    parser.add_argument("--hold-manifest", type=Path, required=True)
    args = parser.parse_args()
    staged, holds = build(args.repo, args.source_csv)
    args.private_stage.parent.mkdir(parents=True, exist_ok=True)
    args.private_stage.write_text(
        json.dumps({"version": "fact-anchor-review-staging-v1", "rows": staged}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.hold_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.hold_manifest.write_text(
        json.dumps({"version": "fact-anchor-1656-candidate-holds-v1", "holds": holds}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"STAGING_ONLY={len(staged)} NEW_APPROVALS=0 HOLDS={len(holds)}")


if __name__ == "__main__":
    main()
