"""S7 source-to-formula relation ID bridge. RESEARCH ONLY, never grades.

A formula grammar may recognize a surface expression, while the canonical
extractor still lacks the approved Registry subject/predicate/object IDs.
This bridge can show SOURCE-BORROWED relation candidates in a separate audit.
It must never pass its results into the canonical grader or claim extractor.
"""
from __future__ import annotations

from typing import Any

from grading.evidence.s7_registry_formula_shadow import SPECS, _verify_source

VERSION = "s7_registry_relation_bridge.v1"
_SCORE_DISABLED = "DISABLED"
_HOLD = "HOLD"


def build_relation_bridge(
    source_review: dict[str, Any],
    challenge: dict[str, Any],
    formula_shadow: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Join existing independently sourced data, not free-form claim meaning.

    The returned triples are verified Registry IDs *borrowed by identity*, not
    IDs independently parsed from the answer text. This does not demonstrate
    Claim-Fact EXACT_RELATION, asserted conditions, recall, or false-positive rate.
    """
    if (source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
            or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
            or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
            or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
            or formula_shadow.get("schema_version") != "s7_registry_formula_shadow.v1"
            or formula_shadow.get("status") != "SHADOW_FORMULA_PATTERNS_REVIEW_ONLY"
            or any(x.get("score_admission") != _SCORE_DISABLED for x in
                   (source_review, challenge, formula_shadow))
            or any(x.get("score_effect") != "none"
                   for x in (source_review, formula_shadow))
            or formula_shadow.get("automatic_alias_admission") is not False
            or formula_shadow.get("all_candidate_decisions") != _HOLD
            or formula_shadow.get("source_inventory_execution_sha")
            != source_review.get("inventory_execution_sha")
            or formula_shadow.get("execution_commit_sha")
            != source_review.get("inventory_execution_sha")):
        raise ValueError("S7 source/fixture/formula reports are not an identical safe baseline")
    rows = source_review.get("rows")
    cases = challenge.get("cases")
    formulas = formula_shadow.get("rows")
    if not all(isinstance(x, list) for x in (rows, cases, formulas)):
        raise ValueError("source/fixture/formula rows missing")
    if strict and (
        len(rows) != 119 or len(cases) != 20 or len(formulas) != 6
        or source_review.get("unique_topic_fact_count") != 119
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("decision_counts", {}).get(_HOLD) != 119
        or source_review.get("decision_counts", {}).get("ACCEPT") != 0
    ):
        raise ValueError("S7 119/179/20/6 baseline drift")

    index = {(r["owner_topic_id"], r["fact_id"]): r for r in rows}
    f_index = {(r["owner_topic_id"], r["fact_id"]): r for r in formulas}
    if len(index) != len(rows) or len(f_index) != len(formulas):
        raise ValueError("ambiguous Registry or formula shadow identity")
    if set(f_index) != {(spec["owner"], fid) for fid, spec in SPECS.items()}:
        raise ValueError("formula bridge scope has changed")

    cases_seen: set[tuple[str, str]] = set()
    output: list[dict[str, Any]] = []
    borrowed_count = 0
    direction_risk_count = 0
    for case in cases:
        if not isinstance(case, dict) or case.get("score_effect") != "none":
            raise ValueError("invalid challenge or forbidden score effect")
        owner = case["owner_topic_id"]
        fid = case["fact_id"]
        key = owner, fid
        if key in cases_seen:
            raise ValueError("duplicate challenged Fact")
        cases_seen.add(key)
        src = index.get(key)
        if src is None:
            raise ValueError("source review is missing challenge Fact")
        if (src.get("review_decision") != _HOLD
                or src.get("registry_review_status") != "approved"
                or src.get("registry_verification_status") != "verified"
                or not src.get("registry_verification_refs")
                or src.get("score_effect") != "none"
                or src.get("candidate_alias") is not None):
            raise ValueError("unsafe Registry source status")
        if (src.get("relation", {}).get("subject")
                != case.get("relation_subject_id")):
            raise ValueError("challenge/source relation subject drift")
        if (case.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
                or case.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"):
            raise ValueError("challenge semantic labels drift")

        candidate: dict[str, Any] | None = None
        classification = "NO_FORMULA_SHADOW_COVERAGE"
        adversarial_class = "NO_FORMULA_SHADOW_COVERAGE"
        if fid in SPECS:
            spec = SPECS[fid]
            if owner != spec["owner"]:
                raise ValueError("cross-topic borrowed relation")
            _verify_source(src, spec)
            f = f_index[key]
            if (f.get("case_id") != case.get("case_id")
                    or f.get("source_fact_id") != spec["source"]
                    or f.get("formula_family") != spec["family"]
                    or f.get("score_effect") != "none"):
                raise ValueError("borrowed formula evidence identity drift")
            pos = f.get("positive") or {}
            neg = f.get("adversarial") or {}
            if not isinstance(pos, dict) or not isinstance(neg, dict):
                raise ValueError("formula evidence missing")
            if neg.get("formula_syntax") == "EXPECTED_FORMULA_SYNTAX":
                raise ValueError("adversarial case collides with expected formula")
            if (pos.get("formula_syntax") == "EXPECTED_FORMULA_SYNTAX"
                    and neg.get("formula_syntax") == "INVERTED_FORMULA_SYNTAX"):
                # ID provenance is verified, but these IDs are NOT extracted
                # from the answer text. Required conditions remain unproven.
                candidate = {
                    "subject": spec["subject"],
                    "predicate": spec["predicate"],
                    "object": spec["object"],
                    "polarity": "positive",
                    "condition_ids_not_validated": list(spec["conditions"]),
                    "id_provenance": "BORROWED_FROM_VERIFIED_REGISTRY_SOURCE",
                    "answer_relation_extraction": "NOT_ESTABLISHED",
                    "conditions_proven_by_answer": False,
                }
                classification = "FORMULA_TO_SOURCE_IDS_CANDIDATE_ONLY"
                adversarial_class = "FORMULA_DIRECTION_CONFLICT_REVIEW"
                borrowed_count += 1
                direction_risk_count += 1
            else:
                classification = "FORMULA_SYNTAX_AMBIGUOUS_HOLD"
                adversarial_class = "FORMULA_SYNTAX_AMBIGUOUS_HOLD"
        output.append({
            "case_id": case["case_id"],
            "owner_topic_id": owner,
            "fact_id": fid,
            "source_fact_id": src["source_fact_id"],
            "source_relation_candidate_not_answer_parsed": candidate,
            "positive_probe_status": classification,
            "adversarial_probe_status": adversarial_class,
            "claim_exact_relation": "NOT_ESTABLISHED",
            "score_effect": "none",
        })

    if strict and (len(output) != 20 or borrowed_count != 6
                   or direction_risk_count != 6):
        raise ValueError("complete 20-case / 6-formula bridge accounting failed")
    return {
        "schema_version": VERSION,
        "status": "BORROWED_SOURCE_IDS_ONLY_RESEARCH_INCONCLUSIVE",
        "score_effect": "none",
        "score_admission": _SCORE_DISABLED,
        "automatic_alias_admission": False,
        "candidate_decision": _HOLD,
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "draft_fact_pair_count": len(output),
        "formula_source_id_candidate_count": borrowed_count,
        "formula_direction_conflict_review_count": direction_risk_count,
        "uncovered_nonformula_fact_count": len(output) - borrowed_count,
        "answer_extracted_exact_relation_count": None,
        "measured_precision": None,
        "measured_recall": None,
        "measured_accuracy": None,
        "rows": sorted(output, key=lambda x: x["case_id"]),
        "limitations": [
            "The six source triplets are borrowed from Registry, not parsed from answers.",
            "Formula surface syntax alone does not validate condition IDs or claim polarity.",
            "Fourteen nonformula draft cases still have no shadow relation bridge.",
            "All cases are author-drafted and have no independent expert labels.",
            "Canonical Claim Alignment and all grades remain completely untouched.",
        ],
    }
