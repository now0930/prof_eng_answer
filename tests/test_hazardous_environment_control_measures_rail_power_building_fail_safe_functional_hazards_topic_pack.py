from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOPIC_ID = "hazardous_environment_control_measures_rail_power_building_fail_safe_functional_hazards"
TOPIC_CODE = "IC-2027-W-4-2"

PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

FACT_PATH = PACK / "fact_anchor.json"
LOGIC_PATH = PACK / "logic_check.json"
MODEL_PATH = PACK / "model_answer.json"
IMPORTANCE_PATH = PACK / "topic_importance.json"
README_PATH = PACK / "README.md"

EXPECTED_SOURCE_FILES = {
    SHEET,
    README_PATH,
    FACT_PATH,
    LOGIC_PATH,
    MODEL_PATH,
    IMPORTANCE_PATH,
}

# Fact Anchor ownership contract from Stage 8B.
# control_logic is intentionally not required in this single anchor statement.
EXPECTED_ANCHOR_NEIGHBOR_TOPICS = {
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
    "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification",
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
    "sis_sil_safety_software_independence_systematic_failure_verification_validation",
}

# README and Topic Sheet carry the broader human-readable ownership boundary.
EXPECTED_DOCUMENT_NEIGHBOR_TOPICS = EXPECTED_ANCHOR_NEIGHBOR_TOPICS | {
    "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe",
}

EXPECTED_FATAL_IDS = {
    "hazardous_environment_equals_explosion_only",
    "deenergize_always_safe",
    "power_backup_equals_safe_state",
    "stored_energy_disappears_on_power_off",
    "communication_last_value_always_safe",
    "redundancy_eliminates_common_cause",
    "bypass_has_no_safety_effect",
    "rail_keep_last_command",
    "power_trip_all_auxiliaries",
    "building_all_hvac_off",
    "qualification_replaces_installation_review",
    "alarm_replaces_protection",
    "normal_io_test_proves_fail_safe",
    "retrofit_no_legacy_interaction",
}

EXPECTED_CORE_ANCHORS = {
    "hec_hazardous_environment_scope",
    "hec_hazard_scenario_chain",
    "hec_required_safe_state_context",
    "hec_fail_safe_not_universal_deenergize",
    "hec_loss_of_power_strategy",
    "hec_residual_stored_energy",
    "hec_loss_of_communication_strategy",
    "hec_local_autonomous_protection",
    "hec_sensor_selection_diagnostics",
    "hec_redundancy_common_cause",
    "hec_final_element_safe_action",
    "hec_permissive_interlock_trip_roles",
    "hec_bypass_override_management",
    "hec_rail_hazard_context",
    "hec_rail_uncertain_authority_response",
    "hec_power_generation_hazard_context",
    "hec_power_shutdown_auxiliaries",
    "hec_building_hazard_context",
    "hec_building_fire_smoke_scenario",
    "hec_environmental_application_controls",
    "hec_alarm_operator_action_boundary",
    "hec_verification_loss_scenarios",
    "hec_maintenance_proof_moc",
    "hec_legacy_retrofit_risk_priority",
    "hec_requirement_traceability",
    "hec_ownership_boundary",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _objects() -> tuple[dict, dict, dict, dict]:
    return (
        _load(FACT_PATH),
        _load(LOGIC_PATH),
        _load(MODEL_PATH),
        _load(IMPORTANCE_PATH),
    )


def test_source_files_exist_and_identify_topic() -> None:
    assert all(path.is_file() for path in EXPECTED_SOURCE_FILES)

    fact, logic, model, importance = _objects()

    expected_schemas = {
        FACT_PATH.name: "topic_pack.fact_anchor.v1",
        LOGIC_PATH.name: "topic_pack.logic_check.v1",
        MODEL_PATH.name: "topic_pack.model_answer.v1",
        IMPORTANCE_PATH.name: "topic_pack.topic_importance.v1",
    }

    for path, obj in [
        (FACT_PATH, fact),
        (LOGIC_PATH, logic),
        (MODEL_PATH, model),
        (IMPORTANCE_PATH, importance),
    ]:
        assert obj["topic_id"] == TOPIC_ID
        assert obj["schema_version"] == expected_schemas[path.name]

    assert TOPIC_CODE in SHEET.read_text(encoding="utf-8")
    assert TOPIC_CODE in README_PATH.read_text(encoding="utf-8")


def test_classification_contract() -> None:
    fact, logic, model, importance = _objects()

    assert fact["question_type_hint"] == "IMPLEMENTATION_EVALUATION"
    assert model["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert importance["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert logic["deterministic_checks"]["question_type"] == "IMPLEMENTATION_EVALUATION"

    assert importance["difficulty"] == "FIELD_APPLICATION"
    assert logic["deterministic_checks"]["difficulty_profile"] == "FIELD_APPLICATION"
    assert logic["llm_profile"]["difficulty"] == "FIELD_APPLICATION"

    assert importance["selection_importance"] == "CORE_MUST_PREPARE"


def test_fact_anchor_semantic_contract() -> None:
    fact, _, _, _ = _objects()

    anchors = fact["anchors"]
    fatals = fact["fatal_wrong_claims"]

    assert len(anchors) == 26
    assert len(fatals) == 14
    assert len(fact["safe_expressions"]) == 16
    assert len(fact["core_facts"]) == 26

    ids = [row["anchor_id"] for row in anchors]
    assert len(ids) == len(set(ids))
    assert set(ids) == EXPECTED_CORE_ANCHORS
    assert all(row["id"] == row["anchor_id"] for row in anchors)
    assert all(row["importance"] in {"must", "important", "optional"} for row in anchors)
    assert all(row["statement"].strip() for row in anchors)
    assert all(row["core_terms"] for row in anchors)
    assert all(row["accepted_explanations"] for row in anchors)
    assert all(row["source_basis"] for row in anchors)

    fatal_ids = {row["id"] for row in fatals}
    assert fatal_ids == EXPECTED_FATAL_IDS
    assert all(row["severity"] == "fatal" for row in fatals)
    assert all(row["affected_layers"] == ["C"] for row in fatals)


def test_llm_only_logic_projection() -> None:
    fact, logic, model, _ = _objects()

    det = logic["deterministic_checks"]
    profile = logic["llm_profile"]

    assert det["enabled"] is False
    assert det["fatal_checks"] == []
    assert det["major_checks"] == []
    assert det["question_type_checks"] == []
    assert det["topic_aliases"] == model["routing_aliases"]

    assert profile["enabled"] is True
    assert profile["candidate_extraction"]["rules"] == []
    assert profile["truth_schema"] == [
        row["statement"] for row in fact["anchors"]
    ]

    expected_fatals = [
        f"[{row['id']}] {row['claim']} | correction: {row['correction']}"
        for row in fact["fatal_wrong_claims"]
    ]
    assert profile["fatal_conditions"] == expected_fatals

    assert profile["score_policy"] == {
        "direct_score_application": False,
        "direct_d_e_effect": "none",
        "affected_layers": ["C"],
    }

    assert len(profile["major_checks"]) == 12
    assert len(profile["false_positive_cautions"]) >= 12


def test_model_answer_traceability_and_coverage() -> None:
    fact, _, model, _ = _objects()

    assert len(model["expected_question_patterns"]) == 10
    assert len(model["recommended_outline"]) == 8
    assert len(model["routing_aliases"]) == 18
    assert len(model["routing_field_points"]) >= 20
    assert len(model["high_score_points"]) >= 12
    assert len(model["common_missing_points"]) >= 10

    anchor_ids = {row["anchor_id"] for row in fact["anchors"]}

    for row in model["expected_question_patterns"]:
        refs = set(row["required_anchor_ids"])
        assert row["pattern"].strip()
        assert row["intent"].strip()
        assert refs
        assert refs <= anchor_ids

    outline_refs = set()
    for row in model["recommended_outline"]:
        refs = set(row["anchor_refs"])
        assert row["section"].strip()
        assert row["intent"].strip()
        assert refs
        assert refs <= anchor_ids
        outline_refs.update(refs)

    assert outline_refs == anchor_ids


def test_required_application_scope_is_present() -> None:
    fact, logic, model, importance = _objects()

    corpus = json.dumps(
        {
            "fact": fact,
            "logic": logic,
            "model": model,
            "importance": importance,
        },
        ensure_ascii=False,
    ).casefold()

    required = {
        "required safe state",
        "fail-safe",
        "loss of power",
        "loss of communication",
        "watchdog",
        "stored energy",
        "common cause failure",
        "railway",
        "power generation",
        "fire",
        "smoke",
        "cause-and-effect",
        "moc",
        "legacy",
    }

    for term in required:
        assert term.casefold() in corpus, term


def test_fatal_misconceptions_lock_safe_behavior() -> None:
    fact, _, _, _ = _objects()

    fatal_by_id = {
        row["id"]: row
        for row in fact["fatal_wrong_claims"]
    }

    assert "모든 설비에서 전원을 모두 끄는 것과 동일" in fatal_by_id[
        "deenergize_always_safe"
    ]["claim"]
    assert "required safe state" in fatal_by_id[
        "deenergize_always_safe"
    ]["correction"]

    assert "마지막 정상값을 무기한 유지" in fatal_by_id[
        "communication_last_value_always_safe"
    ]["claim"]
    assert "timeout" in fatal_by_id[
        "communication_last_value_always_safe"
    ]["correction"]

    assert "common cause failure는 제거" in fatal_by_id[
        "redundancy_eliminates_common_cause"
    ]["claim"]

    assert "마지막 운전명령을 계속 유지" in fatal_by_id[
        "rail_keep_last_command"
    ]["claim"]
    assert "controlled braking" in fatal_by_id[
        "rail_keep_last_command"
    ]["correction"]

    assert "모든 보조펌프" in fatal_by_id[
        "power_trip_all_auxiliaries"
    ]["claim"]
    assert "윤활" in fatal_by_id[
        "power_trip_all_auxiliaries"
    ]["correction"]

    assert "모든 팬과 모든 댐퍼" in fatal_by_id[
        "building_all_hvac_off"
    ]["claim"]
    assert "smoke-control scenario" in fatal_by_id[
        "building_all_hvac_off"
    ]["correction"]


def test_ownership_boundary_prevents_neighbor_duplication() -> None:
    fact, _, _, _ = _objects()

    ownership = next(
        row["statement"]
        for row in fact["anchors"]
        if row["anchor_id"] == "hec_ownership_boundary"
    )

    # Only the four Stage 8B Fact Anchor neighbors are required in this anchor.
    for neighbor in EXPECTED_ANCHOR_NEIGHBOR_TOPICS:
        assert neighbor in ownership

    # control_logic is still required at the human-readable document boundary.
    sheet = SHEET.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")

    for neighbor in EXPECTED_DOCUMENT_NEIGHBOR_TOPICS:
        assert neighbor in sheet
        assert neighbor in readme

    serialized = json.dumps(fact, ensure_ascii=False)

    for forbidden in [
        "Uo ≤ Ui",
        "Io ≤ Ii",
        "Po ≤ Pi",
        "PFDavg",
        "SIL 3이면",
    ]:
        assert forbidden not in serialized


def test_importance_and_coverage_gate() -> None:
    _, _, _, importance = _objects()

    assert importance["selection_importance"] == "CORE_MUST_PREPARE"
    assert len(importance["high_band_unlock_conditions"]) >= 10

    note = importance["note"]
    assert TOPIC_CODE in note
    assert "historical frequency" in note.casefold()
    assert "자동 승격하지 않는다" in note

    sheet = SHEET.read_text(encoding="utf-8")
    assert "COVERED로 승격하지 않는다" in sheet
    assert "Focused validation" in sheet
    assert "semantic re-audit" in sheet


def test_no_placeholder_and_clean_text_files() -> None:
    targets = sorted(EXPECTED_SOURCE_FILES)

    for path in targets:
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert not raw.endswith(b"\n\n")

        text = raw.decode("utf-8")
        assert "TODO" not in text
        assert "보강하세요" not in text
        assert "scaffold" not in text.casefold()

        for line_no, line in enumerate(text.splitlines(), 1):
            assert line == line.rstrip(), f"{path}:{line_no}"


TESTS = [
    test_source_files_exist_and_identify_topic,
    test_classification_contract,
    test_fact_anchor_semantic_contract,
    test_llm_only_logic_projection,
    test_model_answer_traceability_and_coverage,
    test_required_application_scope_is_present,
    test_fatal_misconceptions_lock_safe_behavior,
    test_ownership_boundary_prevents_neighbor_duplication,
    test_importance_and_coverage_gate,
    test_no_placeholder_and_clean_text_files,
]


def main() -> int:
    for test in TESTS:
        test()
        print(f"PASS: {test.__name__}")

    print(f"PASS: focused Topic Pack regression complete: {TOPIC_ID}")
    print(f"FOCUSED_TEST_CASE_COUNT={len(TESTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
