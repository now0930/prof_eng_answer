#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification"
QUESTION_TYPE = "IMPLEMENTATION_EVALUATION"
DIFFICULTY = "FIELD_APPLICATION"

ALLOWED_QUESTION_TYPES = {
    "PRINCIPLE_INTERPRETATION",
    "DIAGNOSIS_ACTION",
    "COMPARE_SELECTION",
    "IMPLEMENTATION_EVALUATION",
}

REQUIRED_CORE_ANCHORS = {
    "ieeq_scope_chain",
    "ieeq_requirement_traceability",
    "ieeq_emc_emi_distinction",
    "ieeq_emission_immunity_distinction",
    "ieeq_emc_test_categories",
    "ieeq_test_setup_representative",
    "ieeq_operating_mode_worst_case",
    "ieeq_pretest_baseline",
    "ieeq_in_test_monitoring",
    "ieeq_acceptance_criteria_predefined",
    "ieeq_temperature_operating_storage",
    "ieeq_temperature_transition_boundary",
    "ieeq_humidity_failure_mechanisms",
    "ieeq_condensation_condition",
    "ieeq_vibration_sine_random",
    "ieeq_vibration_mounting",
    "ieeq_vibration_functional_monitor",
    "ieeq_post_vibration_inspection",
    "ieeq_measurement_instrument_control",
    "ieeq_failure_evidence_capture",
    "ieeq_failure_root_cause",
    "ieeq_corrective_action_retest",
    "ieeq_qualification_vs_field_troubleshooting",
    "ieeq_topic2_boundary",
    "ieeq_topic4_boundary",
    "ieeq_topic5_boundary",
    "ieeq_standard_edition_policy",
    "ieeq_traceable_report",
    "ieeq_change_control_requalification",
}

REQUIRED_BOUNDARY_ANCHORS = {
    "ieeq_qualification_vs_field_troubleshooting",
    "ieeq_topic2_boundary",
    "ieeq_topic4_boundary",
    "ieeq_topic5_boundary",
}

BOUNDARY_TOPIC_IDS = {
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
    "instrumentation_installation_wiring_impulse_tubing_inspection_codes",
    "control_hardware_lifecycle_panel_architecture_component_selection_production_verification",
    "electronics_error_noise_drift_tolerance_aging_power_mitigation",
}

REQUIRED_FATALS = {
    "ieeq_emc_emi_same",
    "ieeq_emission_immunity_same",
    "ieeq_same_severity_all_devices",
    "ieeq_post_power_on_only",
    "ieeq_same_impulse_as_field_fix",
    "ieeq_temperature_one_rule",
    "ieeq_humidity_condensation_same",
    "ieeq_vibration_fixture_irrelevant",
    "ieeq_failure_fix_without_retest",
    "ieeq_previous_pass_auto_inherit",
}

REQUIRED_ROUTING_CONCEPTS = {
    "environmental qualification",
    "emc",
    "emission",
    "immunity",
    "temperature",
    "humidity",
    "vibration",
    "acceptance",
    "retest",
}

FORBIDDEN_HISTORICAL_PATTERNS = (
    r"\b\d+\s*회\s*출제\b",
    r"\b출제\s*빈도\s*[:=]\s*\d+",
    r"\bhistorical_frequency\s*[:=]\s*[1-9]",
)

FORBIDDEN_UNSOURCED_NUMERIC_PATTERNS = (
    # Guard against hard-coded test severities/durations in this source pack.
    r"\b\d+(?:\.\d+)?\s*(?:kv|v/m|a/m|mhz|ghz|hz|g|m/s2|°c|celsius|%rh|hour|hours|hr|hrs|min|minutes)\b",
)

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load_json(name: str) -> dict:
    path = PACK / name
    assert path.is_file(), f"missing source file: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{name} must contain JSON object"
    return data


def normalize(text: str) -> str:
    text = text.lower().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def collect_anchor_refs(model: dict) -> set[str]:
    refs: set[str] = set()
    for item in model.get("expected_question_patterns", []):
        refs.update(item.get("required_anchor_ids", []))
    for item in model.get("recommended_outline", []):
        refs.update(item.get("anchor_refs", []))
    return refs


def main() -> int:
    assert PACK.is_dir(), f"missing Topic Pack: {PACK}"
    assert SHEET.is_file(), f"missing Topic Sheet: {SHEET}"

    fact = load_json("fact_anchor.json")
    model = load_json("model_answer.json")
    importance = load_json("topic_importance.json")
    logic = load_json("logic_check.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

    # Identity / taxonomy.
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

    # Fact Anchor integrity.
    anchors = fact.get("anchors", [])
    assert len(anchors) == 32, f"unexpected anchor count: {len(anchors)}"

    anchor_ids = [a.get("anchor_id") for a in anchors]
    assert all(isinstance(x, str) and x for x in anchor_ids)
    assert len(anchor_ids) == len(set(anchor_ids)), "duplicate anchor_id"
    anchor_set = set(anchor_ids)

    missing_core = REQUIRED_CORE_ANCHORS - anchor_set
    assert not missing_core, f"missing required core anchors: {sorted(missing_core)}"

    missing_boundaries = REQUIRED_BOUNDARY_ANCHORS - anchor_set
    assert not missing_boundaries, f"missing ownership anchors: {sorted(missing_boundaries)}"

    for anchor in anchors:
        assert anchor.get("statement"), f"anchor missing statement: {anchor.get('anchor_id')}"
        assert anchor.get("importance") in {"core", "must", "important", "optional"}
        assert isinstance(anchor.get("keywords"), list) and anchor["keywords"]

    # Model references.
    refs = collect_anchor_refs(model)
    unresolved = refs - anchor_set
    assert not unresolved, f"unresolved model anchor refs: {sorted(unresolved)}"
    assert len(refs) >= 25, f"too few referenced anchors: {len(refs)}"

    assert len(model.get("expected_question_patterns", [])) == 10
    assert len(model.get("recommended_outline", [])) == 8
    assert len(model.get("routing_aliases", [])) >= 10
    assert len(model.get("routing_field_points", [])) >= 10
    assert len(model.get("high_score_points", [])) >= 8
    assert len(model.get("common_missing_points", [])) >= 8

    # Routing specificity.
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
    missing_fatals = REQUIRED_FATALS - fatal_ids
    assert not missing_fatals, f"missing fatal misconception contracts: {sorted(missing_fatals)}"

    # Ownership boundary exact IDs.
    boundary_text = "\n".join(
        a.get("statement", "")
        for a in anchors
        if a.get("anchor_id") in REQUIRED_BOUNDARY_ANCHORS
    )
    for adjacent_id in BOUNDARY_TOPIC_IDS:
        assert adjacent_id in boundary_text, f"missing exact adjacent Topic ID: {adjacent_id}"

    # EMC/EMI and emission/immunity distinctions.
    emc = next(a for a in anchors if a.get("anchor_id") == "ieeq_emc_emi_distinction")
    emission = next(
        a for a in anchors if a.get("anchor_id") == "ieeq_emission_immunity_distinction"
    )
    assert "EMC" in emc["statement"] and "EMI" in emc["statement"]
    assert "emission" in emission["statement"].lower()
    assert "immunity" in emission["statement"].lower()

    # Pre-test / in-test / acceptance chain.
    baseline = next(a for a in anchors if a.get("anchor_id") == "ieeq_pretest_baseline")
    monitoring = next(a for a in anchors if a.get("anchor_id") == "ieeq_in_test_monitoring")
    acceptance = next(
        a for a in anchors if a.get("anchor_id") == "ieeq_acceptance_criteria_predefined"
    )
    assert "baseline" in baseline["statement"].lower()
    assert "시험 중" in monitoring["statement"] or "in-test" in monitoring["statement"].lower()
    assert "시험 전에" in acceptance["statement"] or "전에" in acceptance["statement"]

    # Environmental semantics.
    temp = next(a for a in anchors if a.get("anchor_id") == "ieeq_temperature_operating_storage")
    humidity = next(a for a in anchors if a.get("anchor_id") == "ieeq_condensation_condition")
    vibration = next(a for a in anchors if a.get("anchor_id") == "ieeq_vibration_mounting")
    assert "operating" in temp["statement"].lower() and "storage" in temp["statement"].lower()
    assert "condensation" in humidity["statement"].lower()
    for token in ("fixture", "mounting", "orientation"):
        assert token in vibration["statement"].lower()

    # Failure -> root cause -> corrective action -> retest.
    root_cause = next(a for a in anchors if a.get("anchor_id") == "ieeq_failure_root_cause")
    corrective = next(a for a in anchors if a.get("anchor_id") == "ieeq_corrective_action_retest")
    root_cause_statement = root_cause["statement"].lower()
    assert root_cause.get("anchor_id") == "ieeq_failure_root_cause"
    assert "인과 chain" in root_cause["statement"]
    assert "affected circuit/function" in root_cause_statement
    assert "symptom" in root_cause_statement
    assert "re" in corrective["statement"].lower() and "검증" in corrective["statement"]

    # Field troubleshooting boundary.
    field_boundary = next(
        a for a in anchors if a.get("anchor_id") == "ieeq_qualification_vs_field_troubleshooting"
    )
    assert "instrumentation_power_grounding_shielding_ups_ground_loop_emc" in field_boundary["statement"]
    assert "laboratory" in field_boundary["statement"].lower() or "test" in field_boundary["statement"].lower()

    # No direct deterministic scoring.
    deterministic = logic.get("deterministic_checks", {})
    assert deterministic.get("enabled") is False
    output_contract = logic.get("llm_profile", {}).get("output_contract", {})
    assert output_contract.get("direct_score_application") is False
    assert output_contract.get("direct_de_effect") is False
    assert output_contract.get("require_context_confirmation") is True

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

    # Historical frequency must not be invented.
    for pattern in FORBIDDEN_HISTORICAL_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, (
            f"unsupported historical-frequency claim detected: {pattern}"
        )

    # No unsupported fixed test-level/severity numbers.
    for pattern in FORBIDDEN_UNSOURCED_NUMERIC_PATTERNS:
        match = re.search(pattern, corpus, flags=re.IGNORECASE)
        assert match is None, (
            f"potential unsupported hard-coded environmental/EMC test value detected: {match.group(0)!r}"
        )

    # High-value semantic coverage.
    semantic_expectations = (
        "environmental qualification",
        "emc",
        "emi",
        "emission",
        "immunity",
        "conducted",
        "radiated",
        "esd",
        "eft",
        "surge",
        "operating mode",
        "pre test",
        "functional monitoring",
        "acceptance criteria",
        "operating temperature",
        "storage temperature",
        "condensation",
        "sine",
        "random vibration",
        "fixture",
        "measurement uncertainty",
        "failure evidence",
        "root cause",
        "corrective action",
        "retest",
        "qualification report",
        "requalification",
    )
    missing_semantics = [
        token for token in semantic_expectations
        if normalize(token) not in normalized_corpus
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
    print("ownership_boundaries=4")
    print("emc_emi_distinction=true")
    print("emission_immunity_distinction=true")
    print("pretest_intest_acceptance_chain=true")
    print("temperature_humidity_vibration_semantics=true")
    print("field_troubleshooting_boundary=true")
    print("specific_test_level_hardcoded=false")
    print("historical_frequency_asserted=false")
    print("direct_score_application=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
