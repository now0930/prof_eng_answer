"""S7 AI-authored candidate quarantine and source-backed structural review.

No raw draft or source text is written to the report. No automatic truth
label, expert label, holdout label, alias, grading change or score promotion.
The input is an *AI-generated probe pool*, NEVER independent benchmark data.
"""
from __future__ import annotations

from collections import Counter
import re
import unicodedata
from typing import Any

from grading.evidence.s7_remaining_five_expert_queue import SCOPE

SCHEMA = "s7_ai_candidate_integrity_gate.v1"
EXPECTED_TYPES = {
    1: "technically_consistent",
    2: "contrary_relation",
    3: "omitted_conditions",
    4: "ambiguous_or_quoted",
}
SOURCE_STATUS = "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
ROLE = "AI_AUTHORED_PROBE_POOL_NOT_INDEPENDENT_HOLDOUT"


def _canonical(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s).casefold()).strip()


def quarantine_ai_candidate_pool(
    source_review: dict[str, Any],
    proposed: dict[str, Any],
    author_challenge: dict[str, Any],
) -> dict[str, Any]:
    """Only classify *proposed case structure*. No semantic content judgment."""
    if (
        source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
        or source_review.get("status") != SOURCE_STATUS
        or source_review.get("inventory_execution_sha") is None
        or source_review.get("score_admission") != "DISABLED"
        or source_review.get("score_effect") != "none"
        or source_review.get("unique_topic_fact_count") != 119
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("decision_counts", {}).get("HOLD") != 119
        or source_review.get("decision_counts", {}).get("ACCEPT") != 0
        or proposed.get("schema_version") != "s7_ai_authored_holdout_candidates.v1"
        or proposed.get("source_head_sha") != source_review.get("inventory_execution_sha")
        or proposed.get("score_admission") != "DISABLED"
        or proposed.get("candidate_count") != 20
        or proposed.get("provenance") !=
            "AI_GENERATED_UNREVIEWED_NOT_INDEPENDENT_EXPERT_NOT_GOLDEN"
        or author_challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
        or author_challenge.get("score_admission") != "DISABLED"
        or author_challenge.get("adjudication_status")
            != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
    ):
        raise ValueError("quarantine requires unchanged unadmitted source and AI provenance")
    source_rows = source_review.get("rows")
    draft_cases = author_challenge.get("cases")
    ai_cases = proposed.get("cases")
    if not all(isinstance(x, list) for x in (source_rows, draft_cases, ai_cases)):
        raise ValueError("source/draft/candidate cases not arrays")
    if len(source_rows) != 119 or len(ai_cases) != 20 or len(draft_cases) != 20:
        raise ValueError("case cardinality changed")
    source_index = {(s["owner_topic_id"], s["fact_id"]): s for s in source_rows}
    if len(source_index) != len(source_rows):
        raise ValueError("duplicate Registry source owner")
    author_index = {(s["owner_topic_id"], s["fact_id"]): s for s in draft_cases}
    if len(author_index) != len(draft_cases):
        raise ValueError("duplicate author-case owner")
    source_texts: set[str] = set()
    for fid, spec in SCOPE.items():
        source = source_index.get((spec["owner"], fid))
        authored = author_index.get((spec["owner"], fid))
        if source is None or authored is None:
            raise ValueError("review scope changed")
        relation = source.get("relation", {})
        expected = {
            "subject": spec["subject"], "predicate": spec["predicate"],
            "object": spec["object"], "conditions": spec["conditions"],
            "polarity": "positive",
        }
        if (
            source.get("source_fact_id") != spec["source_fact_id"]
            or relation != expected
            or source.get("review_decision") != "HOLD"
            or source.get("candidate_alias") is not None
            or source.get("registry_review_status") != "approved"
            or source.get("registry_verification_status") != "verified"
            or not source.get("registry_verification_refs")
            or source.get("technical_equivalence_of_candidate") != "NOT_ASSESSED"
            or source.get("score_effect") != "none"
            or authored.get("score_effect") != "none"
            or authored.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
            or authored.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"
        ):
            raise ValueError("verified original Registry relation or HOLD status drift")
        for field in ("positive_answer", "adversarial_answer"):
            txt = authored.get(field)
            if not isinstance(txt, str) or not txt.strip():
                raise ValueError("missing existing authored draft")
            source_texts.add(_canonical(txt))
    got: set[tuple[str, int]] = set()
    text_seen: set[str] = set()
    report_rows: list[dict[str, Any]] = []
    flags_counter: Counter[str] = Counter()
    for case in ai_cases:
        if not isinstance(case, dict):
            raise ValueError("invalid AI candidate")
        fid, no, proposed_type = case.get("fact_id"), case.get("case_no"), case.get("proposed_type")
        if fid not in SCOPE or type(no) is not int or no not in EXPECTED_TYPES:
            raise ValueError("unknown or malformed AI candidate identity")
        key = (fid, no)
        if key in got:
            raise ValueError("duplicate candidate identity")
        got.add(key)
        if proposed_type != EXPECTED_TYPES[no]:
            raise ValueError("unexpected generated four-case role pattern")
        if case.get("review_status") != "NEEDS_INDEPENDENT_EXPERT_LABEL":
            raise ValueError("author cannot preapprove an AI draft")
        text = case.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("empty/invalid AI-authored text")
        normalized = _canonical(text)
        flags: list[str] = []
        if normalized in text_seen:
            flags.append("DUPLICATE_AI_TEXT_REVIEW")
        text_seen.add(normalized)
        if normalized in source_texts:
            flags.append("EXACT_COPY_OF_ORIGINAL_AUTHOR_DRAFT_REVIEW")
        # A "missing conditions" test is incoherent when the source
        # relation defines zero required conditions; this is a structural
        # check, not a natural-language semantic correctness verdict.
        if proposed_type == "omitted_conditions" and not SCOPE[fid]["conditions"]:
            flags.append("NO_SOURCE_CONDITIONS_TO_OMIT_RETAG_OR_REWRITE")
        for flag in flags:
            flags_counter[flag] += 1
        report_rows.append({
            "candidate_id": fid + "_ai_%02d" % no,
            "fact_id": fid,
            "proposed_type": proposed_type,
            "source_fact_id": SCOPE[fid]["source_fact_id"],
            "source_required_condition_count": len(SCOPE[fid]["conditions"]),
            "research_quality_flags": flags,
            "independently_validated_label": None,
            "model_prediction": None,
            "technical_equivalence": "NOT_ASSESSED",
            "review_status": (
                "STRUCTURAL_RETAG_OR_REWRITE_REQUIRED" if flags
                else "UNVERIFIED_AI_PROPOSAL_HOLD"
            ),
            "score_effect": "none",
        })
    if got != {(f, n) for f in SCOPE for n in EXPECTED_TYPES}:
        raise ValueError("not a complete five-by-four candidate matrix")
    if len(text_seen) != 20:
        # Duplicate items stay quarantined but cannot be called novel.
        pass
    return {
        "schema_version": SCHEMA,
        "status": "AI_CANDIDATES_QUARANTINED_NOT_EXPERT_BENCHMARK",
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "candidate_count": len(report_rows),
        "candidate_role": ROLE,
        "candidate_type_counts": dict(sorted(Counter(
            row["proposed_type"] for row in report_rows
        ).items())),
        "source_condition_ids_total_across_five_facts": sum(
            len(spec["conditions"]) for spec in SCOPE.values()
        ),
        "structurally_flagged_count": sum(
            bool(row["research_quality_flags"]) for row in report_rows
        ),
        "flag_counts": dict(sorted(flags_counter.items())),
        "independently_validated_count": 0,
        "independent_test_set_admission": "PROHIBITED",
        "expert_benchmark_ready": False,
        "parser_accuracy": None,
        "precision": None,
        "recall": None,
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "score_admission": "DISABLED",
        "score_effect": "none",
        "rows": sorted(report_rows, key=lambda row: row["candidate_id"]),
        "limitations": [
            "AI-authored candidates are not independent holdout examples.",
            "Structural consistency is not an engineering truth or expert label.",
            "Proposed types cannot be used as ground truth or scorer thresholds.",
            "Original raw text and Source statements are excluded from this report.",
            "Private manual review and separately sourced expert-authored cases required.",
        ],
    }
