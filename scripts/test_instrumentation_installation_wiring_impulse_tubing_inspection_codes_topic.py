#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "instrumentation_installation_wiring_impulse_tubing_inspection_codes"
QUESTION_TYPE = "IMPLEMENTATION_EVALUATION"
DIFFICULTY = "FIELD_APPLICATION"

ALLOWED_QUESTION_TYPES = {
    "PRINCIPLE_INTERPRETATION",
    "DIAGNOSIS_ACTION",
    "COMPARE_SELECTION",
    "IMPLEMENTATION_EVALUATION",
}

REQUIRED_CORE_ANCHORS = {
    "iiwic_scope_chain",
    "iiwic_document_hierarchy",
    "iiwic_install_per_approved_drawings",
    "iiwic_accessibility_maintainability",
    "iiwic_environment_installation_protection",
    "iiwic_cable_route_mechanical_protection",
    "iiwic_cable_separation_execution",
    "iiwic_gland_entry_integrity",
    "iiwic_terminal_quality",
    "iiwic_wire_identification",
    "iiwic_shield_execution_boundary",
    "iiwic_intrinsic_safety_segregation_execution",
    "iiwic_impulse_line_general",
    "iiwic_impulse_slope_service_specific",
    "iiwic_steam_service_principle",
    "iiwic_dp_pair_symmetry",
    "iiwic_tubing_fittings_integrity",
    "iiwic_root_manifold_drain_vent",
    "iiwic_cleanliness_pressure_boundary",
    "iiwic_installation_inspection_sequence",
    "iiwic_continuity_insulation_boundary",
    "iiwic_punch_classification",
    "iiwic_fat_sat_boundary",
    "iiwic_design_basis_boundary",
    "iiwic_hazardous_area_boundary",
    "iiwic_topic1_boundary",
    "iiwic_asbuilt_final_acceptance",
}

REQUIRED_BOUNDARY_ANCHORS = {
    "iiwic_fat_sat_boundary",
    "iiwic_design_basis_boundary",
    "iiwic_pid_document_boundary",
    "iiwic_hazardous_area_boundary",
    "iiwic_topic1_boundary",
}

BOUNDARY_TOPIC_IDS = {
    "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
    "instrumentation_system_design_basis_codes_standards_specification_deviation_management",
    "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative",
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
}

REQUIRED_FATALS = {
    "iiwic_fat_means_field_ok",
    "iiwic_same_slope_all_services",
    "iiwic_open_unused_entry",
    "iiwic_ignore_bend_tension",
    "iiwic_spare_bare_core",
    "iiwic_arbitrary_shield_change",
    "iiwic_arbitrary_code_conflict",
    "iiwic_insulation_test_any_voltage",
    "iiwic_punch_signature_only",
}

REQUIRED_ROUTING_CONCEPTS = {
    "instrumentation installation",
    "cable tray",
    "cable gland",
    "termination",
    "impulse tubing",
    "gas liquid steam",
    "punch",
    "as built",
    "inspection",
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
    assert isinstance(data, dict), f"{name} must contain object"
    return data


def normalize(text: str) -> str:
    text = text.lower().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def collect_refs(model: dict) -> set[str]:
    refs: set[str] = set()
    for item in model.get("expected_question_patterns", []):
        refs.update(item.get("required_anchor_ids", []))
    for item in model.get("recommended_outline", []):
        refs.update(item.get("anchor_refs", []))
    return refs


def main() -> int:
    assert PACK.is_dir()
    assert SHEET.is_file()

    fact = load_json("fact_anchor.json")
    model = load_json("model_answer.json")
    importance = load_json("topic_importance.json")
    logic = load_json("logic_check.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

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

    anchors = fact.get("anchors", [])
    assert len(anchors) == 33, f"unexpected anchor count: {len(anchors)}"

    anchor_ids = [a.get("anchor_id") for a in anchors]
    assert len(anchor_ids) == len(set(anchor_ids)), "duplicate anchor_id"
    anchor_set = set(anchor_ids)

    missing_core = REQUIRED_CORE_ANCHORS - anchor_set
    assert not missing_core, f"missing required core anchors: {sorted(missing_core)}"

    missing_boundaries = REQUIRED_BOUNDARY_ANCHORS - anchor_set
    assert not missing_boundaries, f"missing boundary anchors: {sorted(missing_boundaries)}"

    for anchor in anchors:
        assert anchor.get("statement"), f"anchor statement missing: {anchor.get('anchor_id')}"
        assert anchor.get("importance") in {"core", "must", "important", "optional"}
        assert isinstance(anchor.get("keywords"), list) and anchor["keywords"]

    refs = collect_refs(model)
    unresolved = refs - anchor_set
    assert not unresolved, f"unresolved anchor refs: {sorted(unresolved)}"
    assert len(refs) >= 25, f"model answer references too few anchors: {len(refs)}"

    assert len(model.get("expected_question_patterns", [])) == 10
    assert len(model.get("recommended_outline", [])) == 8
    assert len(model.get("routing_aliases", [])) >= 10
    assert len(model.get("routing_field_points", [])) >= 10
    assert len(model.get("high_score_points", [])) >= 8
    assert len(model.get("common_missing_points", [])) >= 8

    routing_blob = normalize(
        " ".join(model.get("routing_aliases", []) + model.get("routing_field_points", []))
    )
    missing_routing = {
        concept for concept in REQUIRED_ROUTING_CONCEPTS
        if normalize(concept) not in routing_blob
    }
    assert not missing_routing, f"missing routing concepts: {sorted(missing_routing)}"

    fatal_ids = {
        item.get("id")
        for item in fact.get("fatal_wrong_claims", [])
        if isinstance(item, dict)
    }
    missing_fatals = REQUIRED_FATALS - fatal_ids
    assert not missing_fatals, f"missing fatal misconception contracts: {sorted(missing_fatals)}"

    boundary_text = "\n".join(
        a.get("statement", "")
        for a in anchors
        if a.get("anchor_id") in REQUIRED_BOUNDARY_ANCHORS
    )
    for adjacent_id in BOUNDARY_TOPIC_IDS:
        assert adjacent_id in boundary_text, f"missing exact adjacent Topic ID: {adjacent_id}"

    # Verify the recovered FAT/SAT boundary stays synchronized across copies.
    fat = next(a for a in anchors if a.get("anchor_id") == "iiwic_fat_sat_boundary")
    exact_fat_topic = (
        "control_software_project_engineering_documents_fat_sat_commissioning_acceptance"
    )
    assert exact_fat_topic in fat["statement"]
    assert fat["claim"] == fat["statement"]
    assert fat["accepted_explanations"][0] == fat["statement"]
    assert fat["statement"] in fact.get("core_facts", [])
    assert fat["statement"] in logic.get("llm_profile", {}).get("truth_schema", [])

    # Service-specific impulse-line semantics: universal slope must be rejected.
    service_anchor = next(
        a for a in anchors if a.get("anchor_id") == "iiwic_impulse_slope_service_specific"
    )
    service_text = normalize(service_anchor["statement"])
    for token in ("gas", "liquid", "steam"):
        assert token in service_text
    assert "동일" in service_anchor["statement"]

    # Installation execution must not claim ownership of grounding/EMC design.
    shield_boundary = next(
        a for a in anchors if a.get("anchor_id") == "iiwic_shield_execution_boundary"
    )
    assert "instrumentation_power_grounding_shielding_ups_ground_loop_emc" not in (
        model.get("routing_aliases", [])
    ), "Topic 2 routing alias must not become Topic 1 ID"
    assert "승인" in shield_boundary["statement"]

    # No direct deterministic score mutation.
    deterministic = logic.get("deterministic_checks", {})
    assert deterministic.get("enabled") is False
    output_contract = logic.get("llm_profile", {}).get("output_contract", {})
    assert output_contract.get("direct_score_application") is False
    assert output_contract.get("direct_de_effect") is False
    assert output_contract.get("require_context_confirmation") is True

    # Specific code edition must not be hard-coded as a universal rule.
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
    normalized_corpus = normalize(corpus)
    assert "project execution" in normalized_corpus or "프로젝트 실행" in corpus
    assert "specific code edition" in normalized_corpus or "특정 법규" in corpus or "특정 edition" in corpus

    # Historical frequency must not be invented.
    for pattern in FORBIDDEN_HISTORICAL_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, (
            f"unsupported historical-frequency claim detected: {pattern}"
        )

    # High-value implementation semantics.
    semantic_expectations = (
        "approved drawing",
        "accessibility",
        "cable gland",
        "bend radius",
        "pulling tension",
        "spare core",
        "impulse tubing",
        "gas service",
        "liquid service",
        "steam service",
        "high low",
        "root valve",
        "manifold",
        "continuity",
        "punch",
        "reinspection",
        "as built",
        "fat",
        "field installation",
    )
    missing_semantics = [
        item for item in semantic_expectations
        if normalize(item) not in normalized_corpus
    ]
    assert not missing_semantics, f"required semantic coverage missing: {missing_semantics}"

    print("FOCUSED_TOPIC_REGRESSION=PASS")
    print(f"topic_id={TOPIC_ID}")
    print(f"question_type={QUESTION_TYPE}")
    print(f"difficulty={DIFFICULTY}")
    print(f"anchors={len(anchors)}")
    print(f"resolved_anchor_refs={len(refs)}")
    print(f"routing_aliases={len(model.get('routing_aliases', []))}")
    print(f"routing_field_points={len(model.get('routing_field_points', []))}")
    print(f"fatal_wrong_claims={len(fatal_ids)}")
    print("ownership_boundaries=5")
    print("fat_sat_boundary_exact_topic_id=true")
    print("service_specific_impulse_slope=true")
    print("specific_code_edition_hardcoded=false")
    print("historical_frequency_asserted=false")
    print("direct_score_application=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
