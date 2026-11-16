"""Research-only, role-bound formula bridge for six high-risk S7 Registry Facts.

Not an alias dictionary. Never supplies canonical Claim evidence, EXACT_RELATION,
A/B/C credit, Fatal, or changed safety policy. No parser is mutated.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

VERSION = "s7_registry_formula_shadow.v1"

# Exact Registry source identities are review gates, not new ontology aliases.
SPECS: dict[str, dict[str, Any]] = {
    "unbalanced_force_equation": {
        "owner": "balanced_trim_unbalanced_trim_structure_sealing_applications",
        "source": "balanced_trim_unbalance_force_equation",
        "subject": "unbalanced_pressure_force_magnitude",
        "predicate": "equals",
        "object": "net_pressure_differential_times_net_unbalance_area",
        "conditions": ["consistent_units", "static_force_basis"],
        "family": "force_product",
    },
    "hazop_lopa_pfdavg_rrf_relation": {
        "owner": "hazop_lopa_ipl_risk_reduction_sil_target_allocation",
        "source": "hazop_lopa_pfdavg_rrf_relation",
        "subject": "target_pfdavg",
        "predicate": "is_bounded_by",
        "object": "reciprocal_required_rrf",
        "conditions": ["assumptions_stated", "low_demand"],
        "family": "pfd_bound",
    },
    "hazop_lopa_required_rrf": {
        "owner": "hazop_lopa_ipl_risk_reduction_sil_target_allocation",
        "source": "hazop_lopa_required_rrf",
        "subject": "required_rrf",
        "predicate": "equals",
        "object": "residual_frequency_over_tolerable_frequency",
        "conditions": ["same_scenario_endpoint", "same_time_basis"],
        "family": "rrf_ratio",
    },
    "argument_principle_pnz_relation": {
        "owner": "nyquist_stability_criterion_gain_phase_margin",
        "source": "argument_principle_pnz_relation",
        "subject": "nyquist_encirclement_count",
        "predicate": "equals",
        "object": "rhp_zero_count_minus_pole_count",
        "conditions": ["clockwise_positive_convention"],
        "family": "nyquist_sign",
    },
    "required_rrf_relation": {
        "owner": "sil_target_determination_risk_reduction_and_lifecycle",
        "source": "sil_required_rrf_relation",
        "subject": "required_risk_reduction_factor",
        "predicate": "equals",
        "object": "residual_frequency_divided_by_tolerable_frequency",
        "conditions": ["same_scenario_endpoint", "same_time_units"],
        "family": "rrf_ratio",
    },
    "target_pfd_relation": {
        "owner": "sil_target_determination_risk_reduction_and_lifecycle",
        "source": "sil_target_pfd_relation",
        "subject": "low_demand_pfdavg_target",
        "predicate": "is_bounded_by",
        "object": "tolerable_frequency_over_residual_frequency",
        "conditions": ["low_demand", "same_scenario_and_time_basis"],
        "family": "pfd_bound",
    },
}


def _normalize(text: str) -> str:
    return (unicodedata.normalize("NFKC", text).casefold()
            .replace("−", "-").replace("–", "-")
            .replace("≤", "<=").replace("≦", "<=")
            .replace("≥", ">=").replace("≧", ">="))


def _literal_formula(family: str, text: str) -> tuple[str, bool]:
    """Recognize limited formula syntax only, not correctness or conditions."""
    s = _normalize(text)
    qualifiers = {
        "force_product": "정적" in s and "단위" in s,
        "rrf_ratio": "사건" in s and "시간" in s,
        "pfd_bound": "저요구" in s or "low-demand" in s,
        "nyquist_sign": "시계방향" in s and "양수" in s,
    }[family]
    if family == "force_product":
        m = re.search(
            r"(?<!\w)(?:δ\s*p|delta\s*_?\s*p)\s*(?P<op>[×*·/])\s*a\s*_?\s*u(?!\w)",
            s,
        )
        if not m:
            return "NO_LITERAL_PATTERN", qualifiers
        return ("EXPECTED_FORMULA_SYNTAX" if m.group("op") != "/"
                else "INVERTED_FORMULA_SYNTAX", qualifiers)
    if family == "rrf_ratio":
        m = re.search(
            r"(?<!\w)rrf_?required\s*=\s*"
            r"f_(?P<num>residual|tolerable)\s*/\s*f_(?P<den>residual|tolerable)(?!\w)",
            s,
        )
        if not m:
            return "NO_LITERAL_PATTERN", qualifiers
        if (m["num"], m["den"]) == ("residual", "tolerable"):
            return "EXPECTED_FORMULA_SYNTAX", qualifiers
        if (m["num"], m["den"]) == ("tolerable", "residual"):
            return "INVERTED_FORMULA_SYNTAX", qualifiers
        return "NO_LITERAL_PATTERN", qualifiers
    if family == "pfd_bound":
        m = re.search(
            r"(?<!\w)pfdavg(?:_?target)?\s*(?P<op><=|>=|<|>)\s*"
            r"1\s*/\s*rrf_?required(?!\w)",
            s,
        )
        if not m:
            return "NO_LITERAL_PATTERN", qualifiers
        return ("EXPECTED_FORMULA_SYNTAX" if m["op"] in {"<=", "<"}
                else "INVERTED_FORMULA_SYNTAX", qualifiers)
    if family == "nyquist_sign":
        if re.search(r"(?<!\w)n_cw\s*=\s*z\s*-\s*p(?!\w)", s):
            return "EXPECTED_FORMULA_SYNTAX", qualifiers
        if re.search(r"(?<!\w)n_cw\s*=\s*p\s*-\s*z(?!\w)", s):
            return "INVERTED_FORMULA_SYNTAX", qualifiers
        return "NO_LITERAL_PATTERN", qualifiers
    raise ValueError("unsupported formula family")


def _verify_source(row: dict[str, Any], spec: dict[str, Any]) -> None:
    if (row.get("owner_topic_id") != spec["owner"]
            or row.get("source_fact_id") != spec["source"]
            or row.get("review_decision") != "HOLD"):
        raise ValueError("source identity/approval drift")
    relation = row.get("relation")
    if not isinstance(relation, dict):
        raise ValueError("missing verified source relation")
    expected = {field: spec[field] for field in ("subject", "predicate", "object")}
    expected.update({"polarity": "positive", "conditions": spec["conditions"]})
    if relation != expected:
        raise ValueError("source relation/condition drift")


def evaluate_formula_shadow(
    source_review: dict[str, Any], challenge: dict[str, Any],
    *, strict: bool = True,
) -> dict[str, Any]:
    """Draft formula syntax coverage, never validated classification accuracy."""
    if (source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
            or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
            or source_review.get("score_admission") != "DISABLED"
            or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
            or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
            or challenge.get("score_admission") != "DISABLED"):
        raise ValueError("unsafe source/challenge baseline")
    rows = source_review.get("rows")
    cases = challenge.get("cases")
    if not isinstance(rows, list) or not isinstance(cases, list):
        raise ValueError("invalid source/challenge rows")
    if strict and (len(rows) != 119 or len(cases) != 20
                   or source_review.get("unique_topic_fact_count") != 119
                   or source_review.get("projection_count_with_duplicates") != 179):
        raise ValueError("119/179 source and 20 challenge gate mismatch")
    index = {(x["owner_topic_id"], x["fact_id"]): x for x in rows}
    if len(index) != len(rows):
        raise ValueError("ambiguous source review identity")
    selected: dict[str, dict[str, Any]] = {}
    for case in cases:
        fid = case.get("fact_id")
        if case.get("score_effect") != "none":
            raise ValueError("challenge has grade effect")
        if fid not in SPECS:
            continue
        spec = SPECS[fid]
        if case.get("owner_topic_id") != spec["owner"]:
            raise ValueError("challenge owner mismatch")
        if case.get("relation_subject_id") != spec["subject"]:
            raise ValueError("challenge subject mismatch")
        if (case.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
                or case.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"):
            raise ValueError("unrecognized draft labels")
        if fid in selected:
            raise ValueError("duplicate selected Fact")
        source = index.get((spec["owner"], fid))
        if source is None:
            raise ValueError("selected Fact absent from source review")
        _verify_source(source, spec)
        parsed: dict[str, dict[str, Any]] = {}
        for kind, field in (("positive", "positive_answer"),
                            ("adversarial", "adversarial_answer")):
            answer = case.get(field)
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("empty challenge answer")
            literal, qualifier_cue = _literal_formula(spec["family"], answer)
            parsed[kind] = {
                "formula_syntax": literal,
                "qualifier_cue_present_not_validated": qualifier_cue,
            }
        selected[fid] = {
            "case_id": case["case_id"],
            "fact_id": fid,
            "owner_topic_id": spec["owner"],
            "source_fact_id": spec["source"],
            "formula_family": spec["family"],
            "positive": parsed["positive"],
            "adversarial": parsed["adversarial"],
            "score_effect": "none",
        }
    if len(selected) != len(SPECS):
        raise ValueError("six verified source-owned formula subjects required")
    result_rows = [selected[fid] for fid in sorted(selected)]
    positive_patterns = sum(
        r["positive"]["formula_syntax"] == "EXPECTED_FORMULA_SYNTAX"
        for r in result_rows
    )
    negative_false_patterns = sum(
        r["adversarial"]["formula_syntax"] == "EXPECTED_FORMULA_SYNTAX"
        for r in result_rows
    )
    negative_inverted = sum(
        r["adversarial"]["formula_syntax"] == "INVERTED_FORMULA_SYNTAX"
        for r in result_rows
    )
    return {
        "schema_version": VERSION,
        "status": ("COUNTEREXAMPLE_PATTERN_COLLISION_REVIEW"
                   if negative_false_patterns else
                   "SHADOW_FORMULA_PATTERNS_REVIEW_ONLY"),
        "source_inventory_execution_sha": source_review.get("inventory_execution_sha"),
        "score_admission": "DISABLED",
        "score_effect": "none",
        "author_draft_labels_only": True,
        "formula_fact_pairs": len(result_rows),
        "positive_expected_formula_pattern_count": positive_patterns,
        "adversarial_expected_formula_pattern_count": negative_false_patterns,
        "adversarial_inverted_formula_pattern_count": negative_inverted,
        "measured_precision": None,
        "measured_recall": None,
        "measured_accuracy": None,
        "automatic_alias_admission": False,
        "all_candidate_decisions": "HOLD",
        "rows": result_rows,
        "limitations": [
            "Literal formula syntax cues only; not verified Claim-Fact EXACT_RELATION.",
            "Qualifier cue presence does not establish verified conditions.",
            "Six authored draft pairs are not independently expert-adjudicated.",
            "Other 14 pairs have no shadow formula recognizer.",
            "No parser, machine contract, ontology or scoring logic altered.",
        ],
    }
