#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TOPIC_ID = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
QUESTION_TYPE = "DIAGNOSIS_ACTION"
DIFFICULTY = "FIELD_APPLICATION"

ALLOWED_QUESTION_TYPES = {
    "PRINCIPLE_INTERPRETATION",
    "DIAGNOSIS_ACTION",
    "COMPARE_SELECTION",
    "IMPLEMENTATION_EVALUATION",
}

OTHER_LANE_A_TOPICS = {
    "instrumentation_installation_wiring_impulse_tubing_inspection_codes",
    "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification",
    "control_hardware_lifecycle_panel_architecture_component_selection_production_verification",
    "electronics_error_noise_drift_tolerance_aging_power_mitigation",
}

EXPECTED_BOUNDARY_ANCHORS = {
    "ipgse_topic2_boundary",
    "ipgse_topic3_boundary",
    "ipgse_topic4_boundary",
    "ipgse_topic5_boundary",
}

REQUIRED_SAFETY_FATALS = {
    "ipgse_remove_pe_to_fix_noise",
    "ipgse_single_point_always_best",
    "ipgse_shield_always_one_end",
    "ipgse_shield_replaces_pe",
    "ipgse_ups_solves_all_emc",
}

REQUIRED_CORE_ANCHORS = {
    "ipgse_pe_signal_reference_boundary",
    "ipgse_bonding_impedance_frequency",
    "ipgse_single_multi_point_conditional",
    "ipgse_ground_loop_mechanism",
    "ipgse_ground_loop_safe_mitigation",
    "ipgse_common_differential_mode",
    "ipgse_shield_not_pe",
    "ipgse_shield_termination_frequency",
    "ipgse_emi_coupling_paths",
    "ipgse_source_path_victim_mitigation",
    "ipgse_power_quality_scope",
    "ipgse_redundant_supply_boundary",
    "ipgse_ups_function_boundary",
    "ipgse_ups_sizing_factors",
    "ipgse_ups_bypass_grounding",
    "ipgse_diagnostic_workflow",
    "ipgse_evidence_before_rewire",
    "ipgse_final_verification",
}

REQUIRED_ROUTING_CONCEPTS = {
    "ground loop",
    "shield",
    "ups",
    "emc",
    "protective earth",
    "signal ground",
    "vfd",
}

FORBIDDEN_HISTORICAL_PATTERNS = (
    r"\b\d+\s*회\s*출제\b",
    r"\b출제\s*빈도\s*[:=]\s*\d+",
    r"\bhistorical_frequency\s*[:=]\s*[1-9]",
)

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load_json(name: str) -> dict:
    path = PACK / name
    assert path.is_file(), f"missing source file: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{name} must contain a JSON object"
    return data


def collect_anchor_refs(model: dict) -> set[str]:
    refs: set[str] = set()

    for item in model.get("expected_question_patterns", []):
        refs.update(item.get("required_anchor_ids", []))

    for item in model.get("recommended_outline", []):
        refs.update(item.get("anchor_refs", []))

    return refs


def normalize(text: str) -> str:
    text = text.lower().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    assert PACK.is_dir(), f"missing Topic Pack: {PACK}"
    assert SHEET.is_file(), f"missing Topic Sheet: {SHEET}"

    fact = load_json("fact_anchor.json")
    model = load_json("model_answer.json")
    importance = load_json("topic_importance.json")
    logic = load_json("logic_check.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

    # Identity and taxonomy contract.
    for label, data in (
        ("fact_anchor", fact),
        ("model_answer", model),
        ("topic_importance", importance),
        ("logic_check", logic),
    ):
        assert data.get("topic_id") == TOPIC_ID, f"{label}: topic_id mismatch"

    assert QUESTION_TYPE in ALLOWED_QUESTION_TYPES
    assert fact.get("question_type_hint") == QUESTION_TYPE
    assert model.get("question_type") == QUESTION_TYPE
    assert importance.get("question_type") == QUESTION_TYPE
    assert logic["deterministic_checks"].get("question_type") == QUESTION_TYPE

    assert importance.get("difficulty") == DIFFICULTY
    assert logic["deterministic_checks"].get("difficulty_profile") == DIFFICULTY
    assert logic["llm_profile"].get("difficulty") == DIFFICULTY

    # Fact Anchor integrity and semantic coverage.
    anchors = fact.get("anchors", [])
    assert len(anchors) >= 20, f"fact anchors unexpectedly sparse: {len(anchors)}"

    anchor_ids = [a.get("anchor_id") for a in anchors]
    assert all(isinstance(x, str) and x for x in anchor_ids)
    assert len(anchor_ids) == len(set(anchor_ids)), "duplicate anchor_id"
    anchor_set = set(anchor_ids)

    missing_core = REQUIRED_CORE_ANCHORS - anchor_set
    assert not missing_core, f"missing required core anchors: {sorted(missing_core)}"

    missing_boundary = EXPECTED_BOUNDARY_ANCHORS - anchor_set
    assert not missing_boundary, f"missing ownership boundary anchors: {sorted(missing_boundary)}"

    for anchor in anchors:
        assert anchor.get("statement"), f"anchor missing statement: {anchor.get('anchor_id')}"
        assert anchor.get("importance") in {"core", "must", "important", "optional"}
        assert isinstance(anchor.get("keywords"), list) and anchor["keywords"], (
            f"anchor missing keywords: {anchor.get('anchor_id')}"
        )

    # Model-answer references must resolve to authored anchors.
    refs = collect_anchor_refs(model)
    unresolved = refs - anchor_set
    assert not unresolved, f"unresolved model anchor refs: {sorted(unresolved)}"

    assert len(model.get("expected_question_patterns", [])) >= 8
    assert len(model.get("recommended_outline", [])) >= 6
    assert len(model.get("high_score_points", [])) >= 8
    assert len(model.get("common_missing_points", [])) >= 6
    assert len(model.get("routing_aliases", [])) >= 5
    assert len(model.get("routing_field_points", [])) >= 5

    # Routing aliases must be specific enough to represent the owned topic.
    routing_blob = normalize(
        " ".join(model.get("routing_aliases", []) + model.get("routing_field_points", []))
    )
    missing_routing = {
        concept for concept in REQUIRED_ROUTING_CONCEPTS
        if normalize(concept) not in routing_blob
    }
    assert not missing_routing, f"missing routing concepts: {sorted(missing_routing)}"

    # Fatal misconception coverage.
    fatal_ids = {
        item.get("id")
        for item in fact.get("fatal_wrong_claims", [])
        if isinstance(item, dict)
    }
    missing_fatals = REQUIRED_SAFETY_FATALS - fatal_ids
    assert not missing_fatals, f"missing safety fatal claims: {sorted(missing_fatals)}"

    # No direct deterministic scoring from this newly authored pack.
    deterministic = logic.get("deterministic_checks", {})
    assert deterministic.get("enabled") is False
    output_contract = logic.get("llm_profile", {}).get("output_contract", {})
    assert output_contract.get("direct_score_application") is False
    assert output_contract.get("direct_de_effect") is False
    assert output_contract.get("require_context_confirmation") is True

    # Ownership boundaries must name all four adjacent Lane A topics.
    boundary_text = " ".join(
        a.get("statement", "")
        for a in anchors
        if a.get("anchor_id") in EXPECTED_BOUNDARY_ANCHORS
    )
    for adjacent_topic in OTHER_LANE_A_TOPICS:
        assert adjacent_topic in boundary_text, (
            f"adjacent lane ownership boundary missing: {adjacent_topic}"
        )

    # Topic Sheet and README must preserve the chosen scope/taxonomy.
    for text_label, text in (("README", readme), ("Topic Sheet", sheet)):
        assert TOPIC_ID in text, f"{text_label}: Topic ID missing"
        assert QUESTION_TYPE in text, f"{text_label}: Question Type missing"
        assert DIFFICULTY in text, f"{text_label}: difficulty missing"
        assert "Historical frequency" in text or "historical frequency" in text.lower()

    # Historical frequency must not be invented.
    corpus = "\n".join(
        [
            readme,
            sheet,
            json.dumps(fact, ensure_ascii=False),
            json.dumps(model, ensure_ascii=False),
            json.dumps(importance, ensure_ascii=False),
            json.dumps(logic, ensure_ascii=False),
        ]
    )
    for pattern in FORBIDDEN_HISTORICAL_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, (
            f"unsupported historical-frequency claim detected: {pattern}"
        )

    # High-value semantics that prevent unsafe or over-generalized answers.
    semantic_blob = normalize(corpus)
    semantic_expectations = (
        "protective earth",
        "signal reference",
        "single point",
        "multi point",
        "ground loop",
        "circulating current",
        "common mode",
        "differential mode",
        "one end",
        "both end",
        "360 degree",
        "source path victim",
        "power quality",
        "battery aging",
        "ups bypass",
        "before after",
        "closed loop verification",
    )
    missing_semantics = [
        item for item in semantic_expectations
        if normalize(item) not in semantic_blob
    ]
    assert not missing_semantics, (
        f"required semantic coverage missing: {missing_semantics}"
    )

    print("FOCUSED_TOPIC_REGRESSION=PASS")
    print(f"topic_id={TOPIC_ID}")
    print(f"question_type={QUESTION_TYPE}")
    print(f"difficulty={DIFFICULTY}")
    print(f"anchors={len(anchors)}")
    print(f"resolved_anchor_refs={len(refs)}")
    print(f"routing_aliases={len(model.get('routing_aliases', []))}")
    print(f"routing_field_points={len(model.get('routing_field_points', []))}")
    print(f"fatal_wrong_claims={len(fatal_ids)}")
    print("historical_frequency_asserted=false")
    print("direct_score_application=false")
    print("ownership_boundaries=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
