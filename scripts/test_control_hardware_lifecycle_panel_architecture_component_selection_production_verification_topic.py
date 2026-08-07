#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "control_hardware_lifecycle_panel_architecture_component_selection_production_verification"
QUESTION_TYPE = "IMPLEMENTATION_EVALUATION"
DIFFICULTY = "DESIGN_EVALUATION"

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

REQUIRED_BOUNDARY_IDS = {
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
    "instrumentation_installation_wiring_impulse_tubing_inspection_codes",
    "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification",
    "electronics_error_noise_drift_tolerance_aging_power_mitigation",
    "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation",
    "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
}

REQUIRED_BOUNDARY_ANCHORS = {
    "chl_grounding_emc_boundary",
    "chl_field_installation_boundary",
    "chl_environmental_qualification_boundary",
    "chl_tolerance_stack_boundary",
    "chl_fat_boundary",
    "chl_software_lifecycle_boundary",
}

REQUIRED_FATALS = {
    "chl_prototype_equals_production",
    "chl_fat_equals_design_verification",
    "chl_fat_equals_production_verification",
    "chl_nominal_rating_only",
    "chl_same_derating_all",
    "chl_verification_validation_same",
    "chl_production_test_repeat_all_dv",
    "chl_uncontrolled_substitution",
    "chl_fixture_uncontrolled",
    "chl_rework_without_retest",
}

FORBIDDEN_HISTORICAL_PATTERNS = (
    r"\b\d+\s*회\s*출제\b",
    r"\b출제\s*빈도\s*[:=]\s*\d+",
    r"\bhistorical_frequency\s*[:=]\s*[1-9]",
)

FORBIDDEN_FIXED_DERATING_PATTERNS = (
    r"\bderating\s*[:=]?\s*\d+(?:\.\d+)?\s*%",
    r"\b모든\s*부품.{0,30}\d+(?:\.\d+)?\s*%",
)


def load_json(name: str) -> dict:
    path = PACK / name
    assert path.is_file(), f"missing source: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def anchor_map(fact: dict) -> dict[str, dict]:
    return {a["anchor_id"]: a for a in fact["anchors"]}


def statement(anchors: dict[str, dict], aid: str) -> str:
    assert aid in anchors, f"missing anchor: {aid}"
    text = anchors[aid].get("statement", "")
    assert text
    return text


def has_any(text: str, *terms: str) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def require_all(text: str, *terms: str) -> None:
    low = text.lower()
    missing = [term for term in terms if term.lower() not in low]
    assert not missing, f"missing terms {missing} in: {text}"


def main() -> int:
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

    assert fact.get("question_type_hint") == QUESTION_TYPE
    assert model.get("question_type") == QUESTION_TYPE
    assert importance.get("question_type") == QUESTION_TYPE
    assert logic["deterministic_checks"].get("question_type") == QUESTION_TYPE

    assert importance.get("difficulty") == DIFFICULTY
    assert logic["deterministic_checks"].get("difficulty_profile") == DIFFICULTY
    assert logic["llm_profile"].get("difficulty") == DIFFICULTY

    # Anchor/model integrity.
    anchors_list = fact.get("anchors", [])
    assert len(anchors_list) == 35, len(anchors_list)
    ids = [a.get("anchor_id") for a in anchors_list]
    assert len(ids) == len(set(ids))
    assert all(isinstance(x, str) and x for x in ids)
    anchors = anchor_map(fact)

    refs: set[str] = set()
    for item in model.get("expected_question_patterns", []):
        refs.update(item.get("required_anchor_ids", []))
    for item in model.get("recommended_outline", []):
        refs.update(item.get("anchor_refs", []))

    assert refs <= set(ids), sorted(refs - set(ids))
    assert len(refs) == 35
    assert len(model.get("expected_question_patterns", [])) == 10
    assert len(model.get("recommended_outline", [])) == 8
    assert len(model.get("routing_aliases", [])) == 15
    assert len(model.get("routing_field_points", [])) == 15
    assert len(fact.get("fatal_wrong_claims", [])) == 10

    fatal_ids = {
        item.get("id")
        for item in fact.get("fatal_wrong_claims", [])
        if isinstance(item, dict)
    }
    assert REQUIRED_FATALS <= fatal_ids, sorted(REQUIRED_FATALS - fatal_ids)

    # Lifecycle chain.
    scope = statement(anchors, "chl_scope_chain")
    require_all(
        scope,
        "requirement",
        "architecture",
        "component selection",
        "design verification",
        "production verification",
        "configuration",
        "release",
    )

    # Architecture / interfaces.
    architecture = statement(anchors, "chl_architecture_partitioning")
    for concept in (
        "power/protection",
        "controller/processing",
        "analog·digital i/o",
        "communication",
        "isolation",
        "terminal/interface",
        "thermal",
    ):
        assert concept.lower() in architecture.lower(), concept

    interface = statement(anchors, "chl_interface_definition")
    require_all(interface, "signal type/range", "electrical level", "isolation", "fault behavior")

    # Power / thermal.
    power = statement(anchors, "chl_power_budget")
    assert has_any(power, "normal/peak/startup load", "startup load")
    require_all(power, "supply tolerance", "conversion loss", "power budget", "fault response")

    thermal = statement(anchors, "chl_thermal_design")
    require_all(thermal, "component loss", "enclosure", "ambient", "hotspot")
    assert has_any(thermal, "계산 또는 시험 evidence", "calculation", "test evidence")

    # Component selection / derating.
    selection = statement(anchors, "chl_component_selection_multicriteria")
    for concept in (
        "electrical rating",
        "temperature/environment",
        "derating margin",
        "interface compatibility",
        "availability/lifecycle",
        "maintainability",
    ):
        assert concept.lower() in selection.lower(), concept

    derating = statement(anchors, "chl_derating_rule")
    require_all(derating, "derating", "manufacturer data", "reliability margin")
    assert "모든 부품에 하나의 고정 percentage" in derating

    # Prototype != production readiness.
    prototype = statement(anchors, "chl_prototype_not_production")
    require_all(prototype, "prototype", "production readiness", "process capability", "production test coverage")
    assert has_any(prototype, "assembly variation", "조립")
    assert "동일하지 않다" in prototype

    # Verification vs validation: semantic equivalence, not literal-only.
    vv = statement(anchors, "chl_verification_vs_validation")
    require_all(vv, "verification", "validation", "requirement")
    assert has_any(vv, "intended use", "intended-use", "최종 사용목적")
    assert has_any(vv, "운용 요구", "operational requirement")

    # Verification planning.
    vplan = statement(anchors, "chl_verification_plan")
    for term in ("analysis", "inspection", "test", "demonstration", "acceptance criterion", "evidence owner"):
        assert term in vplan.lower(), term

    # DFM/DFA and configuration.
    dfm = statement(anchors, "chl_dfm_dfa")
    assert has_any(dfm, "manufacturability", "dfm")
    assert has_any(dfm, "assembly", "dfa")
    assert "오삽입 방지" in dfm

    bom = statement(anchors, "chl_bom_configuration")
    require_all(bom, "bom", "configuration baseline", "revision", "approved component/source")

    # Production verification purpose: semantic Korean/English.
    production = statement(anchors, "chl_production_test_coverage")
    require_all(production, "production verification", "test coverage", "critical path")
    assert "설계검증 전체를 반복" in production
    assert has_any(production, "manufacturing variation", "제조변동")
    assert has_any(production, "assembly error", "오조립")
    assert has_any(production, "component defect", "부품불량")

    eol = statement(anchors, "chl_eol_test")
    for concept in ("power-up", "i/o channels", "communication ports", "diagnostics"):
        assert concept in eol.lower(), concept
    assert "unit-specific result" in eol.lower()

    fixture = statement(anchors, "chl_test_fixture_control")
    require_all(fixture, "test fixture", "test software", "version", "calibration/verification", "change control")

    # NCR/rework/retest.
    ncr = statement(anchors, "chl_nonconformance_rework")
    require_all(ncr, "nonconformance", "containment", "rework", "reinspection/retest")
    assert "임의 repair" in ncr

    # Change / release.
    change = statement(anchors, "chl_change_impact")
    require_all(change, "component substitution", "requalification", "production-test update")

    release = statement(anchors, "chl_release_gate")
    require_all(release, "verification gap", "bom", "production-test gap", "configuration")

    # Exact ownership boundaries.
    assert REQUIRED_BOUNDARY_ANCHORS <= set(ids)
    boundary_blob = "\n".join(statement(anchors, aid) for aid in REQUIRED_BOUNDARY_ANCHORS)
    for adjacent_id in REQUIRED_BOUNDARY_IDS:
        assert adjacent_id in boundary_blob, adjacent_id

    # FAT / Topic 3 / software lifecycle distinctions.
    fat = statement(anchors, "chl_fat_boundary")
    assert "fat" in fat.lower()
    assert "design verification" in fat.lower()
    assert "production process capability" in fat.lower()
    assert "대체하지 않" in fat

    env = statement(anchors, "chl_environmental_qualification_boundary")
    assert "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification" in env
    assert "release gate" in env.lower()

    sw = statement(anchors, "chl_software_lifecycle_boundary")
    assert "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation" in sw
    assert "hardware lifecycle" in sw.lower()

    # No direct deterministic scoring.
    assert logic["deterministic_checks"].get("enabled") is False
    output = logic["llm_profile"].get("output_contract", {})
    assert output.get("direct_score_application") is False
    assert output.get("direct_de_effect") is False
    assert output.get("require_context_confirmation") is True

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

    # No fabricated historical frequency.
    for pattern in FORBIDDEN_HISTORICAL_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, pattern

    # No universal fixed derating percentage.
    for pattern in FORBIDDEN_FIXED_DERATING_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, pattern

    # Routing must strongly identify Topic 4.
    routing = " ".join(model["routing_aliases"] + model["routing_field_points"]).lower()
    for concept in (
        "hardware lifecycle",
        "panel",
        "component",
        "derating",
        "verification",
        "production",
        "bom",
        "test",
    ):
        assert concept in routing, concept

    print("FOCUSED_TOPIC_REGRESSION=PASS")
    print(f"topic_id={TOPIC_ID}")
    print(f"question_type={QUESTION_TYPE}")
    print(f"difficulty={DIFFICULTY}")
    print(f"anchors={len(anchors_list)}")
    print(f"resolved_anchor_refs={len(refs)}")
    print(f"routing_aliases={len(model['routing_aliases'])}")
    print(f"routing_field_points={len(model['routing_field_points'])}")
    print(f"fatal_wrong_claims={len(fatal_ids)}")
    print("ownership_boundaries=6")
    print("hardware_lifecycle_chain=true")
    print("component_selection_derating_semantics=true")
    print("prototype_vs_production_readiness=true")
    print("verification_validation_semantics=true")
    print("manufacturing_variation_semantics=true")
    print("production_test_coverage_semantics=true")
    print("fixture_control=true")
    print("change_release_traceability=true")
    print("fat_not_design_or_production_verification=true")
    print("specific_derating_percentage_hardcoded=false")
    print("historical_frequency_asserted=false")
    print("direct_score_application=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
