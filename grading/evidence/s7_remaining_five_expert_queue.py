"""S7 five pending nonformula Facts: source-owned independent-review queue.

This is a metadata-only, unscored research audit.  No answer fragments,
accepted aliases, expert verdicts, or grading changes are generated here.
The five Fact scopes are fixed to the last five NOT_PROBED in the 14-Fact triage.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

VERSION = "s7_remaining_five_expert_queue.v1"
PENDING = "PENDING_INDEPENDENT_ADJUDICATION"
SCOPE = {
    "effective_unbalanced_area": {
        "owner": "balanced_trim_unbalanced_trim_structure_sealing_applications",
        "source_fact_id": "control_valve_effective_unbalance_area_definition",
        "subject": "effective_unbalance_area",
        "predicate": "is",
        "object": "equivalent_projected_area_for_net_pressure_force",
        "conditions": ["configuration_specific", "defined_for_actual_pressure_geometry"],
        "focus": "PROJECTED_AREA_VS_NOMINAL_SEAT",
    },
    "sw06_baseline_approved_reference": {
        "owner": "configuration_change_release_backup_rollback_migration_obsolescence_management",
        "source_fact_id": "configuration_baseline_is_approved_point_in_time_reference",
        "subject": "configuration_baseline",
        "predicate": "is",
        "object": "approved_point_in_time_configuration_reference",
        "conditions": ["configuration_information_is_identified", "formal_approval_or_agreement"],
        "focus": "FORMALLY_APPROVED_VS_NEWEST_FILE",
    },
    "deadband_definition_direction_reversal": {
        "owner": "control_valve_deadband_stiction_response_time_positioner_dynamic_performance",
        "source_fact_id": "control_valve_deadband_is_reversal_input_interval_without_observed_output_change",
        "subject": "control_valve_assembly",
        "predicate": "has",
        "object": "direction_reversal_deadband",
        "conditions": [
            "input_direction_reversal_is_part_of_definition",
            "magnitude_is_assembly_and_test_condition_specific",
            "output_change_is_not_observable_over_deadband_interval",
        ],
        "focus": "INPUT_REVERSAL_INTERVAL_VS_OUTPUT_TIME_DELAY",
    },
    "sw04_v_model_definition": {
        "owner": "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation",
        "source_fact_id": "v_model_design_test_mapping",
        "subject": "v_model",
        "predicate": "maps",
        "object": "design_and_test_stages",
        "conditions": [],
        "focus": "V_MODEL_CORRESPONDENCE_VS_GENERIC_TRACEABILITY_ADDITION",
    },
    "nyquist_contour_and_mapping": {
        "owner": "nyquist_stability_criterion_gain_phase_margin",
        "source_fact_id": "nyquist_contour_and_mapping",
        "subject": "nyquist_contour",
        "predicate": "maps",
        "object": "loop_transfer_curve",
        "conditions": ["rhp_stability_analysis"],
        "focus": "S_PLANE_CONTOUR_VS_L_PLANE_IMAGE",
    },
}


def evaluate_remaining_five_queue(
    source_review: dict[str, Any],
    nonformula_triage: dict[str, Any],
    condition_scope_shadow: dict[str, Any],
    challenge: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Make an ID-only review queue; fail closed on any authority/scope drift."""
    if (
        source_review.get("schema_version") != "s7_alias_registry_source_review.v1"
        or source_review.get("status") != "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD"
        or nonformula_triage.get("schema_version") != "s7_nonformula_surface_triage.v1"
        or nonformula_triage.get("status") != "NONFORMULA_DRAFT_SURFACE_REVIEW_ONLY"
        or condition_scope_shadow.get("schema_version") != "s7_condition_scope_shadow.v1"
        or condition_scope_shadow.get("status") != "CONDITION_SCOPE_DRAFT_CUES_REVIEW_ONLY"
        or challenge.get("schema_version") != "s7_negative_claim_challenge.v1"
        or challenge.get("adjudication_status") != "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED"
        or any(x.get("score_admission") != "DISABLED"
               for x in (source_review, nonformula_triage,
                         condition_scope_shadow, challenge))
        or any(x.get("score_effect") != "none"
               for x in (source_review, nonformula_triage, condition_scope_shadow))
        or any(x.get("candidate_decision") != "HOLD"
               for x in (nonformula_triage, condition_scope_shadow))
        or any(x.get("automatic_alias_admission") is not False
               for x in (nonformula_triage, condition_scope_shadow))
        or any(x.get("source_inventory_execution_sha")
               != source_review.get("inventory_execution_sha")
               for x in (nonformula_triage, condition_scope_shadow))
        or any(x.get("execution_commit_sha")
               != source_review.get("inventory_execution_sha")
               for x in (nonformula_triage, condition_scope_shadow))
    ):
        raise ValueError("source, triage, condition and author-draft baselines unsafe")
    source_rows = source_review.get("rows")
    triage_rows = nonformula_triage.get("rows")
    scope_rows = condition_scope_shadow.get("rows")
    cases = challenge.get("cases")
    if not all(isinstance(v, list) for v in
               (source_rows, triage_rows, scope_rows, cases)):
        raise ValueError("missing evidence rows")
    if strict and (
        len(source_rows) != 119 or len(triage_rows) != 14
        or len(scope_rows) != 5 or len(cases) != 20
        or source_review.get("unique_topic_fact_count") != 119
        or source_review.get("projection_count_with_duplicates") != 179
        or source_review.get("decision_counts", {}).get("HOLD") != 119
        or source_review.get("decision_counts", {}).get("ACCEPT") != 0
        or nonformula_triage.get("nonformula_fact_count") != 14
        or nonformula_triage.get("unprobed_nonformula_fact_count") != 10
        or condition_scope_shadow.get("draft_pair_count") != 5
        or condition_scope_shadow.get("source_conditions_proven") != 0
    ):
        raise ValueError("119/179/14/5 source coverage or HOLD baseline drift")
    src = {(x["owner_topic_id"], x["fact_id"]): x for x in source_rows}
    triage = {(x["owner_topic_id"], x["fact_id"]): x for x in triage_rows}
    if len(src) != len(source_rows) or len(triage) != len(triage_rows):
        raise ValueError("ambiguous source and nonformula identities")
    scoped = {(x["owner_topic_id"], x["fact_id"]) for x in scope_rows}
    if len(scoped) != len(scope_rows):
        raise ValueError("duplicate conditional shadow Fact")
    if scoped & {(s["owner"], fid) for fid, s in SCOPE.items()}:
        raise ValueError("remaining five overlap prior condition/scope pilot")
    selected = set()
    rows: list[dict[str, Any]] = []
    risk_counts: Counter[str] = Counter()
    for case in cases:
        fid = case.get("fact_id")
        if fid not in SCOPE:
            continue
        spec = SCOPE[fid]
        owner = spec["owner"]
        key = (owner, fid)
        if (
            case.get("owner_topic_id") != owner
            or case.get("relation_subject_id") != spec["subject"]
            or case.get("positive_label") != "SOURCE_CONSISTENT_DRAFT"
            or case.get("adversarial_label") != "SOURCE_INCONSISTENT_DRAFT"
            or case.get("score_effect") != "none"
            or not isinstance(case.get("positive_answer"), str)
            or not case["positive_answer"].strip()
            or not isinstance(case.get("adversarial_answer"), str)
            or not case["adversarial_answer"].strip()
        ):
            raise ValueError("source case lacks required owner or is score-active")
        if key in selected:
            raise ValueError("duplicate source Fact in five-case queue")
        selected.add(key)
        s = src.get(key)
        t = triage.get(key)
        if not isinstance(s, dict) or not isinstance(t, dict):
            raise ValueError("missing Registry source or nonformula triage Fact")
        expected_relation = {
            "subject": spec["subject"],
            "predicate": spec["predicate"],
            "object": spec["object"],
            "conditions": spec["conditions"],
            "polarity": "positive",
        }
        if (
            s.get("source_fact_id") != spec["source_fact_id"]
            or s.get("relation") != expected_relation
            or s.get("registry_review_status") != "approved"
            or s.get("registry_verification_status") != "verified"
            or not s.get("registry_verification_refs")
            or s.get("review_decision") != "HOLD"
            or s.get("candidate_alias") is not None
            or s.get("technical_equivalence_of_candidate") != "NOT_ASSESSED"
            or s.get("score_effect") != "none"
            or t.get("source_fact_id") != spec["source_fact_id"]
            or t.get("source_predicate_id") != spec["predicate"]
            or t.get("pilot_selected") is not False
            or t.get("positive_surface_cue") != "NOT_PROBED"
            or t.get("adversarial_surface_cue") != "NOT_PROBED"
            or t.get("score_effect") != "none"
        ):
            raise ValueError("Registry truth or prior triage status changed")
        risks = sorted(set(s.get("risk_flags") or []))
        for risk in risks:
            risk_counts[risk] += 1
        rows.append({
            "case_id": case["case_id"],
            "owner_topic_id": owner,
            "fact_id": fid,
            "source_fact_id": spec["source_fact_id"],
            "source_subject_id": spec["subject"],
            "source_predicate_id": spec["predicate"],
            "source_object_id": spec["object"],
            "source_condition_ids_not_asserted": list(spec["conditions"]),
            "source_verification_reference_count": len(s["registry_verification_refs"]),
            "review_focus_code": spec["focus"],
            "original_author_adversarial_type": case.get("adversarial_type"),
            "risk_flags": risks,
            "review_status": PENDING,
            "independent_condition_coverage": "NOT_EVALUATED",
            "independent_claim_label": "NOT_EVALUATED",
            "answer_relation_extraction": "NOT_ESTABLISHED",
            "score_effect": "none",
        })
    if len(rows) != 5 or len(selected) != 5:
        raise ValueError("not all five unprobed Facts accounted for")
    return {
        "schema_version": VERSION,
        "status": "FIVE_UNPROBED_FACTS_QUEUED_FOR_INDEPENDENT_REVIEW",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "candidate_decision": "HOLD",
        "automatic_alias_admission": False,
        "source_inventory_execution_sha": source_review["inventory_execution_sha"],
        "queued_fact_count": len(rows),
        "authored_draft_answer_count": 2 * len(rows),
        "source_condition_ids_total": sum(len(r["source_condition_ids_not_asserted"]) for r in rows),
        "review_pending_count": len(rows),
        "independently_labeled_answer_count": 0,
        "answer_parsed_exact_relation_count": None,
        "measured_precision": None,
        "measured_recall": None,
        "measured_accuracy": None,
        "risk_flag_counts_nonexclusive": dict(sorted(risk_counts.items())),
        "rows": sorted(rows, key=lambda r: r["case_id"]),
        "limitations": [
            "This is a source/condition identity inventory, not a new text parser.",
            "No author draft answer, raw Fact statement or references are copied.",
            "Author-provided positive/adversarial labels are not independent labels.",
            "V-Model author draft mentions traceability beyond the bare Registry triplet: review separately.",
            "No condition in an answer is proved by this queue.",
            "No automatic alias, Truth, EXACT_RELATION or scoring admission.",
        ],
    }
