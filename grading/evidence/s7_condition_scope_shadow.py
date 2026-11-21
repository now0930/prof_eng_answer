"""S7 source-owned condition/scope cue pilot, research-only and score-neutral.

Never routes to canonical Claim Alignment, a Fact admission, or a grader.
This isolates the five drafted conditional and Nyquist P/Z cases that were
NOT_PROBED in the prior 14-Fact nonformula triage.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

VERSION = "s7_condition_scope_shadow.v1"
SPECS: dict[str, dict[str, Any]] = {
    "safe_state_process_hazard_basis": {
        "owner": "final_control_element_sil_sis_esd_valve_partial_stroke_test",
        "source": "final_element_safe_action_process_dependent",
        "subject": "protective_system_safe_action",
        "predicate": "depends_on",
        "object": "process_hazard_and_safety_requirement",
        "conditions": ["safe_action_is_defined_for_the_specific_process",
                       "valve_mechanical_fail_action_is_not_assumed_to_equal_process_safe_state"],
    },
    "residual_frequency_before_sif": {
        "owner": "sil_target_determination_risk_reduction_and_lifecycle",
        "source": "sil_residual_frequency_before_sif",
        "subject": "pre_sif_residual_frequency",
        "predicate": "equals",
        "object": "initiating_rate_times_modifiers_and_existing_ipl_pfds",
        "conditions": ["consistent_consequence_endpoint", "independent_ipl_credits"],
    },
    "thermocouple_measures_temperature_difference": {
        "owner": "thermocouple_temperature_sensor_seebeck_reference_junction_compensation",
        "source": "thermocouple_measures_temperature_difference",
        "subject": "thermocouple_emf",
        "predicate": "depends_on",
        "object": "measuring_and_reference_junction_temperatures",
        "conditions": ["thermocouple_material_pair_known"],
    },
    "closed_loop_rhp_poles_count": {
        "owner": "nyquist_stability_criterion_gain_phase_margin",
        "source": "closed_loop_rhp_poles_count",
        "subject": "z_parameter",
        "predicate": "counts",
        "object": "closed_loop_rhp_poles",
        "conditions": ["no_unmodeled_cancellation", "standard_negative_feedback"],
    },
    "open_loop_rhp_poles_count": {
        "owner": "nyquist_stability_criterion_gain_phase_margin",
        "source": "open_loop_rhp_poles_count",
        "subject": "p_parameter",
        "predicate": "counts",
        "object": "open_loop_rhp_poles",
        "conditions": ["multiplicity_included"],
    },
}

_EXPECTED = "AUTHOR_DRAFT_EXPECTED_CUE_ONLY"
_CONTRARY = "AUTHOR_DRAFT_CONTRARY_CUE_REVIEW"
_AMBIGUOUS = "CONFLICTING_ASSERTIONS_HOLD"
_UNRESOLVED = "SCOPE_OR_CONDITION_CUE_MISSING_HOLD"
_REJECTED = "REJECTION_CONTEXT_HOLD"
_REJECTION = re.compile(
    r"(?:틀리(?:다|다고|며)|잘못된|오류|성립하지|부정확|incorrect|invalid)",
    re.I,
)


def _norm(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def _all(s: str, *parts: str) -> bool:
    return all(part in s for part in parts)


def _cue(fid: str, text: str) -> str:
    """Strict literal evidence cue, *not* truth, engineering meaning or condition proof."""
    if fid not in SPECS:
        raise ValueError("unreviewed Fact ID")
    s = _norm(text)
    if _REJECTION.search(s):
        return _REJECTED
    if fid == "safe_state_process_hazard_basis":
        yes = _all(s, "보호시스템", "안전 동작", "공정", "위험",
                   "안전 요구사항", "따라 결정")
        no = _all(s, "모든 공정", "무조건", "fail-close", "불필요")
    elif fid == "residual_frequency_before_sif":
        yes = _all(s, "동일 사고 시나리오", "독립 ipl", "인정 pfd",
                   "수정인자", "개시 사건 빈도", "곱", "sif 전 잔여빈도")
        no = _all(s, "의존적인 ipl", "독립으로 계산", "두 번 공제")
    elif fid == "thermocouple_measures_temperature_difference":
        yes = _all(s, "재질쌍이 알려진", "열전대 기전력", "측정접점 온도",
                   "기준접점 온도를 알아야")
        no = _all(s, "열전대 기전력만", "재질쌍", "기준접점 온도",
                  "몰라도", "절대온도", "항상")
    elif fid == "closed_loop_rhp_poles_count":
        yes = _all(s, "표준 음의 피드백", "미모델링 상쇄가 없다",
                   "z는", "1+l(s)", "우반평면 영점",
                   "폐루프 우반평면 극점")
        no = _all(s, "z는", "폐루프와 무관", "l(s) 자체", "우반평면 영점")
    else:
        yes = _all(s, "p는", "중복도를 포함", "열린 우반평면",
                   "개루프 l(s) 극점")
        no = _all(s, "p는", "중복도를 무시", "폐루프 극점")
    if yes and no:
        return _AMBIGUOUS
    if yes:
        return _EXPECTED
    if no:
        return _CONTRARY
    return _UNRESOLVED


def evaluate_condition_scope_shadow(
    source_review: dict[str, Any],
    nonformula_triage: dict[str, Any],
    challenge: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Join only five pre-reviewed IDs and never assert factual correctness."""
    if (
        source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
        or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
        or nonformula_triage.get("schema_version") != "s7_nonformula_surface_triage.v1"
        or nonformula_triage.get("status") != "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY"
        or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
        or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
        or any(x.get("score_admission") != "DISABLED"
               for x in (source_review, nonformula_triage, challenge))
        or source_review.get("score_effect") != "none"
        or nonformula_triage.get("score_effect") != "none"
        or nonformula_triage.get("candidate_decision") != "HOLD"
        or nonformula_triage.get("automatic_alias_admission") is not False
        or nonformula_triage.get("source_inventory_execution_sha")
        != source_review.get("inventory_execution_sha")
        or nonformula_triage.get("execution_commit_sha")
        != source_review.get("inventory_execution_sha")
    ):
        raise ValueError("unsafe or cross-run source and triage evidence")
    source_rows = source_review.get("rows")
    triage_rows = nonformula_triage.get("rows")
    challenge_cases = challenge.get("cases")
    if not all(isinstance(v, list) for v in (source_rows, triage_rows, challenge_cases)):
        raise ValueError("missing source, triage or draft cases")
    if strict and (
        len(source_rows) != 119 or len(triage_rows) != 14
        or len(challenge_cases) != 20
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("unique_topic_fact_count") != 119
        or source_review.get("decision_counts", {}).get("HOLD") != 119
        or source_review.get("decision_counts", {}).get("ACCEPT") != 0
        or nonformula_triage.get("nonformula_fact_count") != 14
        or nonformula_triage.get("unprobed_nonformula_fact_count") != 10
    ):
        raise ValueError("full source 119/179, triage 14/10 baseline required")
    source_idx = {(r["owner_topic_id"], r["fact_id"]): r for r in source_rows}
    triage_idx = {(r["owner_topic_id"], r["fact_id"]): r for r in triage_rows}
    if len(source_idx) != len(source_rows) or len(triage_idx) != len(triage_rows):
        raise ValueError("ambiguous Fact owner identity")
    out: list[dict[str, Any]] = []
    visited: set[str] = set()
    for case in challenge_cases:
        fid = case.get("fact_id")
        if fid not in SPECS:
            continue
        if fid in visited or case.get("score_effect") != "none":
            raise ValueError("duplicate or score-active case")
        visited.add(fid)
        spec = SPECS[fid]
        owner = spec["owner"]
        if (case.get("owner_topic_id") != owner
                or case.get("relation_subject_id") != spec["subject"]
                or case.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
                or case.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"):
            raise ValueError("author-draft owner/subject/label drift")
        src = source_idx.get((owner, fid))
        triage = triage_idx.get((owner, fid))
        if src is None or triage is None:
            raise ValueError("missing independent Registry source or 14-Fact triage")
        expected_relation = {
            "subject": spec["subject"], "predicate": spec["predicate"],
            "object": spec["object"], "polarity": "positive",
            "conditions": spec["conditions"],
        }
        if (
            src.get("source_fact_id") != spec["source"]
            or src.get("relation") != expected_relation
            or src.get("review_decision") != "HOLD"
            or src.get("registry_review_status") != "approved"
            or src.get("registry_verification_status") != "verified"
            or not src.get("registry_verification_refs")
            or src.get("technical_equivalence_of_candidate") != "NOT_ASSESSED"
            or src.get("candidate_alias") is not None
            or src.get("score_effect") != "none"
            or triage.get("source_fact_id") != spec["source"]
            or triage.get("source_predicate_id") != spec["predicate"]
            or triage.get("pilot_selected") is not False
            or triage.get("positive_surface_cue") != "NOT_PROBED"
            or triage.get("adversarial_surface_cue") != "NOT_PROBED"
            or triage.get("score_effect") != "none"
        ):
            raise ValueError("verified Registry relation, approval or prior pilot drift")
        answer_yes = case.get("positive_answer")
        answer_no = case.get("adversarial_answer")
        if not all(isinstance(v, str) and v.strip() for v in (answer_yes, answer_no)):
            raise ValueError("empty author draft")
        out.append({
            "case_id": case["case_id"],
            "owner_topic_id": owner,
            "fact_id": fid,
            "source_fact_id": spec["source"],
            "source_condition_ids_unproven": list(spec["conditions"]),
            "positive_surface_cue": _cue(fid, answer_yes),
            "adversarial_surface_cue": _cue(fid, answer_no),
            "answer_subject_predicate_object_extraction": "NOT_ESTABLISHED",
            "conditions_validated": False,
            "score_effect": "none",
        })
    if len(out) != 5 or len(visited) != 5:
        raise ValueError("expected five condition/scope Fact draft pairs")
    pos_count = sum(r["positive_surface_cue"] == _EXPECTED for r in out)
    contrary_count = sum(r["adversarial_surface_cue"] == _CONTRARY for r in out)
    return {
        "schema_version": VERSION,
        "status": ("CONDITION_SCOPE_DRAFT_CUES_REVIEW_ONLY"
                   if pos_count == contrary_count == 5
                   else "CONDITION_SCOPE_PILOT_MISMATCH_HOLD"),
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "score_effect": "none",
        "score_admission": "DISABLED",
        "automatic_alias_admission": False,
        "candidate_decision": "HOLD",
        "draft_pair_count": 5,
        "condition_dependency_fact_count": 3,
        "nyquist_scope_fact_count": 2,
        "positive_surface_cues": pos_count,
        "adversarial_contrary_cues": contrary_count,
        "source_conditions_proven": 0,
        "answer_parsed_exact_relation_count": None,
        "measured_precision": None,
        "measured_recall": None,
        "measured_accuracy": None,
        "author_draft_labels_only": True,
        "rows": sorted(out, key=lambda r: r["case_id"]),
        "limitations": [
            "Literal authored-case cues only, not claim extraction or validation.",
            "Source relation and condition IDs are borrowed, not inferred from answers.",
            "No condition ID is independently verified by these surface matches.",
            "No independent expert-adjudicated labels, precision, recall or accuracy.",
            "No scoring, Registry, Ontology, Topic Pack, machine contract or alias updates.",
        ],
    }
