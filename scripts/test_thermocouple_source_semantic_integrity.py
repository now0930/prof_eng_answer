#!/usr/bin/env python3
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
TOPIC = "thermocouple_temperature_sensor_seebeck_reference_junction_compensation"
PACK = REPO / "rubrics" / "topic_packs" / TOPIC

FACT = PACK / "fact_anchor.json"
LOGIC = PACK / "logic_check.json"
MODEL = PACK / "model_answer.json"
IMPORTANCE = PACK / "topic_importance.json"

TITLE = "열전대 온도센서의 원리, 기준접점 보상 및 보상도선"

REQUIRED_ANCHORS = {
    "thermocouple_temperature_measurement_chain",
    "thermocouple_seebeck_effect_dissimilar_conductors",
    "thermocouple_measures_temperature_difference",
    "thermocouple_reference_junction_compensation",
    "thermocouple_law_of_intermediate_metals",
    "thermocouple_law_of_intermediate_temperatures",
    "thermocouple_type_material_range_atmosphere_selection",
    "thermocouple_extension_compensating_wire_polarity",
    "thermocouple_nonlinearity_reference_tables_polynomial_conversion",
    "thermocouple_junction_construction_response_isolation",
    "thermocouple_thermowell_installation_dynamic_error",
    "thermocouple_signal_conditioning_noise_grounding",
    "thermocouple_calibration_tolerance_uncertainty_drift",
    "thermocouple_fault_diagnostics_open_polarity_cjc_validation",
}

REQUIRED_FATALS = {
    "thermocouple_fatal_absolute_temperature_self_generated_voltage",
    "thermocouple_fatal_reference_junction_no_effect",
    "thermocouple_fatal_cjc_fixed_voltage_subtraction",
    "thermocouple_fatal_every_intermediate_metal_creates_error",
    "thermocouple_fatal_copper_wire_always_equivalent",
    "thermocouple_fatal_compensating_wire_low_resistance_only",
    "thermocouple_fatal_all_types_same_voltage_table",
    "thermocouple_fatal_perfect_linear_and_polarity_irrelevant",
}

RTD_POSITIVE = re.compile(
    r"Pt\s*100|Callendar|Van\s*Dusen|"
    r"(?:2|3|4)\s*[·,/ ]?\s*선식|(?:2|3|4)[- ]?wire|"
    r"Kelvin\s*(?:측정|RTD)|리드선 저항|"
    r"RTD 온도센서의 측정원리|RTD 변환 사슬|RTD의 측정전류",
    re.I,
)

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)

def assert_no_rtd_positive(label: str, value: Any) -> None:
    bad = [text for text in strings(value) if RTD_POSITIVE.search(text)]
    assert not bad, f"{label} contains RTD-positive ownership payload: {bad}"

def test_thermocouple_source_semantic_integrity() -> None:
    fact = load(FACT)
    logic = load(LOGIC)
    model = load(MODEL)
    importance = load(IMPORTANCE)

    for label, obj in (
        ("fact", fact), ("logic", logic), ("model", model), ("importance", importance)
    ):
        assert obj.get("topic_id") == TOPIC, f"{label}.topic_id mismatch"

    assert fact["title_ko"] == TITLE
    assert fact.get("topic_label") == TITLE
    assert logic["title"] == TITLE
    assert logic["deterministic_checks"]["topic_name"] == TITLE
    assert logic["llm_profile"]["display_name"] == TITLE
    assert model["title"] == TITLE
    assert model["title_ko"] == TITLE

    positive_fields = {
        "fact.title_ko": fact["title_ko"],
        "fact.safe_expressions": fact["safe_expressions"],
        "logic.title": logic["title"],
        "logic.deterministic_checks.topic_name": logic["deterministic_checks"]["topic_name"],
        "logic.llm_profile.display_name": logic["llm_profile"]["display_name"],
        "model.title_ko": model["title_ko"],
        "model.expected_question_patterns": model["expected_question_patterns"],
        "model.high_score_points": model["high_score_points"],
        "importance.note": importance["note"],
    }
    for label, value in positive_fields.items():
        assert_no_rtd_positive(label, value)

    assert model["expected_question_patterns"] == model["question_examples"][:10]
    assert model["high_score_points"] == model["high_score_features"]
    assert model["common_missing_points"] == model["low_score_patterns"]

    combined = "\n".join(
        text for value in positive_fields.values() for text in strings(value)
    )
    for marker in ("열전대", "Seebeck", "기준접점", "냉접점 보상", "보상도선"):
        assert marker in combined, f"missing Thermocouple core marker: {marker}"

    anchor_ids = {item.get("id") for item in fact.get("anchors", [])}
    fatal_ids = {item.get("id") for item in fact.get("fatal_wrong_claims", [])}
    assert REQUIRED_ANCHORS <= anchor_ids
    assert REQUIRED_FATALS <= fatal_ids

    rejected = "\n".join(
        item
        for anchor in fact.get("anchors", [])
        for item in anchor.get("rejected_explanations", [])
        if isinstance(item, str)
    )
    assert "RTD 또는 thermistor의 측정원리를 열전대 원리로 혼동한다." in rejected
    assert any("RTD 3선식 보상" in item for item in model.get("low_score_patterns", []))
    assert "RTD와 Thermistor의 상세 원리는 별도 Topic으로 분리한다." in importance["note"]

def main() -> int:
    test_thermocouple_source_semantic_integrity()
    print("PASS: thermocouple source semantic integrity")
    print("topic_id=" + TOPIC)
    print("required_anchor_count=14")
    print("required_fatal_count=8")
    print("positive_rtd_contamination_count=0")
    print("rtd_boundary_references_preserved=true")
    print("model_legacy_rich_field_alignment=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
