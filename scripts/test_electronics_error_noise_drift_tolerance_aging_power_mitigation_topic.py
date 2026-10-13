#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "electronics_error_noise_drift_tolerance_aging_power_mitigation"
QUESTION_TYPE = "PRINCIPLE_INTERPRETATION"
DIFFICULTY = "FIELD_APPLICATION"
SELECTION_IMPORTANCE = "HIGH"

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

REQUIRED_FATALS = {
    "eem_noise_equals_all_error",
    "eem_tolerance_equals_drift",
    "eem_aging_equals_initial_tolerance",
    "eem_adc_resolution_equals_accuracy",
    "eem_filter_removes_offset_gain",
    "eem_calibration_removes_future_drift_noise",
    "eem_psrr_constant_all_conditions",
    "eem_all_errors_linear_sum",
    "eem_field_grounding_owned_here",
    "eem_fixed_universal_cal_interval",
}

REQUIRED_BOUNDARY_ANCHORS = {
    "eem_ground_emc_boundary",
    "eem_environment_qualification_boundary",
    "eem_hardware_lifecycle_boundary",
    "eem_sensor_specific_boundary",
    "eem_metrology_boundary",
}

FORBIDDEN_HISTORICAL_PATTERNS = (
    r"\b\d+\s*회\s*출제\b",
    r"\b출제\s*빈도\s*[:=]\s*\d+",
    r"\bhistorical_frequency\s*[:=]\s*[1-9]",
)

FORBIDDEN_FIXED_NUMERIC_PATTERNS = (
    r"\bpsrr\s*[:=]?\s*\d+(?:\.\d+)?\s*(?:db)?",
    r"\bdrift\s*[:=]?\s*\d+(?:\.\d+)?",
    r"\btolerance\s*[:=]?\s*\d+(?:\.\d+)?\s*%",
    r"\bcalibration interval\s*[:=]?\s*\d+",
)


def load_json(name: str) -> dict:
    path = PACK / name
    assert path.is_file(), f"missing source: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


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
    assert importance.get("selection_importance") == SELECTION_IMPORTANCE

    # Anchor and model integrity.
    anchors_list = fact.get("anchors", [])
    assert len(anchors_list) == 36, len(anchors_list)
    ids = [a.get("anchor_id") for a in anchors_list]
    assert len(ids) == len(set(ids))
    assert all(isinstance(x, str) and x for x in ids)
    anchors = {a["anchor_id"]: a for a in anchors_list}

    refs: set[str] = set()
    for item in model.get("expected_question_patterns", []):
        refs.update(item.get("required_anchor_ids", []))
    for item in model.get("recommended_outline", []):
        refs.update(item.get("anchor_refs", []))

    assert refs <= set(ids), sorted(refs - set(ids))
    assert len(refs) == 36
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

    def st(aid: str) -> str:
        assert aid in anchors, aid
        value = anchors[aid].get("statement", "")
        assert value, aid
        return value

    # Signal-chain error budget: contributors depend on the actual circuit;
    # do not require one universal ordered block list in this scope anchor.
    scope = st("eem_scope_chain")
    require_all(
        scope,
        "실제 구성에 존재하는",
        "센서·아날로그 단계·reference·ADC",
        "오차와 잡음 기여",
        "공통 기준점(입력 또는 출력)",
        "잔류 불확도",
    )
    scope_notes = anchors["eem_scope_chain"].get("grading_notes", "")
    require_all(
        scope_notes,
        "실제 측정 신호체인",
        "회로 전달관계",
        "모든 설계에 동일한 오차 항목이나 고정 블록 순서를 강요하지 않는다",
    )

    # Systematic/random/drift distinction.
    classification = st("eem_error_classification")
    require_all(classification, "systematic error", "random error", "drift")
    assert has_any(classification, "하나의 'noise'", "one noise")
    assert "잘못 선택" in classification

    # Offset / gain / linearity distinction.
    offset = st("eem_offset_error")
    require_all(offset, "offset error", "bias", "input offset", "reference mismatch")

    gain = st("eem_gain_error")
    require_all(gain, "gain error", "transfer slope", "resistor ratio", "full-scale")

    linearity = st("eem_linearity_error")
    require_all(linearity, "linearity error", "offset", "gain")
    assert has_any(linearity, "zero/span calibration", "zero span calibration")
    assert "완전히 제거되지 않을" in linearity

    # Random noise / bandwidth / SNR.
    noise = st("eem_random_noise")
    require_all(noise, "random noise", "thermal noise", "shot noise", "bandwidth")
    assert has_any(noise, "repeatability", "반복")

    bandwidth = st("eem_noise_bandwidth")
    require_all(bandwidth, "spectral density", "bandwidth", "response time")
    assert has_any(bandwidth, "integrated noise", "적분 noise")
    assert "trade-off" in bandwidth.lower()

    snr = st("eem_snr_dynamic_range")
    require_all(snr, "signal-to-noise ratio", "dynamic range", "noise floor", "adc bit")
    assert "자동으로 낮아지는 것은 아니다" in snr

    # Tolerance / drift / aging distinction.
    drift = st("eem_drift_definition")
    require_all(
        drift,
        "instrumental drift",
        "계량특성 변화",
        "시간에 따라",
        "영향량 변화",
        "온도·전원",
        "시간변화",
        "구분",
    )

    tolerance = st("eem_tolerance_definition")
    require_all(tolerance, "tolerance", "nominal value", "drift")
    assert has_any(tolerance, "제조", "manufacturing")
    assert "동일하지 않다" in tolerance

    aging = st("eem_aging_definition")
    require_all(aging, "aging", "tolerance", "temperature drift", "calibration stability")
    assert has_any(aging, "장기", "long term", "long-term")

    # Temperature coefficient and tolerance propagation.
    tempco = st("eem_temperature_coefficient")
    require_all(tempco, "temperature coefficient", "resistor ratio", "reference", "error budget")

    propagation = st("eem_tolerance_propagation")
    require_all(propagation, "tolerance", "sensitivity", "worst-case", "통계", "error budget")
    assert "dominant contributor" in propagation.lower()

    # Local supply/reference/PSRR.
    supply = st("eem_power_supply_sensitivity")
    for concept in ("supply variation", "ripple", "regulator noise", "reference", "sensor excitation"):
        assert concept in supply.lower(), concept
    assert "error path" in supply.lower()

    psrr = st("eem_psrr")
    require_all(psrr, "psrr", "power-supply", "input-referred", "operating condition")
    assert has_any(psrr, "frequency", "주파수")
    assert "고정 수치" in psrr

    reference = st("eem_reference_error")
    for concept in (
        "initial accuracy",
        "temperature coefficient",
        "noise",
        "load sensitivity",
        "aging",
        "gain/scale error",
    ):
        assert concept in reference.lower(), concept

    # ADC distinction.
    adcq = st("eem_adc_quantization")
    require_all(adcq, "adc quantization", "resolution", "offset", "gain", "inl/dnl", "reference error", "accuracy")
    assert "동일하지 않다" in adcq

    adcra = st("eem_adc_resolution_accuracy")
    require_all(adcra, "adc resolution", "accuracy", "bit", "code step", "true value")
    assert has_any(adcra, "반드시 고정확도", "not necessarily")

    aliasing = st("eem_adc_aliasing_boundary")
    require_all(aliasing, "nyquist", "anti-alias", "aliasing", "quantization")
    assert "구분" in aliasing

    # Filtering and calibration limitations.
    filtering = st("eem_filter_noise_mitigation")
    require_all(filtering, "filtering", "noise", "cutoff", "response delay", "signal bandwidth")

    filter_limit = st("eem_filter_not_offset_fix")
    require_all(filter_limit, "filter", "offset", "gain error", "random", "deterministic")
    assert "자동 보정하지 못" in filter_limit

    calibration = st("eem_calibration_systematic")
    require_all(calibration, "calibration", "traceable reference", "offset/gain/scale", "random noise", "future drift", "aging")
    assert "영구 제거" in calibration

    cal_interval = st("eem_calibration_interval")
    for concept in ("stability history", "drift rate", "uncertainty", "criticality", "maintenance cost"):
        assert concept in cal_interval.lower(), concept
    assert "동일한 고정 주기" in cal_interval

    # Error budget / combination.
    budget = st("eem_error_budget")
    for concept in (
        "offset", "gain", "linearity", "tolerance", "temperature drift",
        "noise", "reference", "adc", "power sensitivity",
    ):
        assert concept in budget.lower(), concept
    assert has_any(budget, "input-referred", "output-referred")
    assert "dominant source" in budget.lower()

    combine = st("eem_rss_worstcase")
    require_all(combine, "worst-case", "rss", "random")
    assert has_any(combine, "correlation", "상관")
    assert "동일 방식으로 합산하지 않는다" in combine

    # Diagnosis / mitigation / residual.
    diagnosis = st("eem_diagnosis_chain")
    require_all(
        diagnosis,
        "예상과 다른 오프셋 또는 잡음",
        "원인을 곧바로 특정 오차로 단정하지 않는다",
        "DAQ 입력 단자",
        "독립 계측기",
        "입력 설정·배선·센서·샘플링 조건",
        "교정 상태",
        "신호원과 계측 경로",
        "단계적으로 분리한다",
        "장치와 측정 조건",
    )

    mitigation = st("eem_mitigation_hierarchy")
    require_all(
        mitigation,
        "확인된 기여항목과 회로 구조에 맞춰 선택한다",
        "Calibration·compensation·signal processing",
        "모든 오차를 제거하지는 않으며",
        "잔류 성분",
        "보편적인 대책 순서를 가정하지 않는다",
    )

    residual = st("eem_residual_verification")
    require_all(
        residual,
        "표준값과 지시값을 비교",
        "영향량·운전조건",
        "분해능·반복성",
        "잔류 성능의 검증 범위",
        "측정불확도",
        "시스템의 용도와 적용 기준",
    )

    # Adjacent ownership boundaries.
    assert REQUIRED_BOUNDARY_ANCHORS <= set(ids)

    grounding = st("eem_ground_emc_boundary")
    assert "instrumentation_power_grounding_shielding_ups_ground_loop_emc" in grounding
    assert "facility/panel grounding topology" in grounding.lower()
    assert "pcb/local electronics" in grounding.lower()

    env = st("eem_environment_qualification_boundary")
    assert "instrumentation_environmental_emc_emi_temperature_humidity_vibration_qualification" in env
    assert "test setup" in env.lower()
    assert "temperature/drift/aging" in env.lower()

    hw = st("eem_hardware_lifecycle_boundary")
    assert "control_hardware_lifecycle_panel_architecture_component_selection_production_verification" in hw
    assert "error budget" in hw.lower()

    sensor = st("eem_sensor_specific_boundary")
    for concept in ("rtd", "thermocouple", "strain gauge", "lvdt/rvdt", "piezoelectric"):
        assert concept in sensor.lower(), concept
    assert "electronics error chain" in sensor.lower()

    metrology = st("eem_metrology_boundary")
    for concept in ("accuracy", "precision", "repeatability", "uncertainty"):
        assert concept in metrology.lower(), concept
    assert "circuit-level" in metrology.lower()

    # Local layout, not plant grounding.
    layout = st("eem_layout_local_mitigation")
    require_all(
        layout,
        "회로 토폴로지",
        "return-current 경로",
        "저임피던스 전원/ground",
        "decoupling",
        "ground split은 모든 보드에 일률 적용하지 않고",
        "고임피던스 입력",
        "누설이 유의한 조건",
        "guard 구조",
    )

    # Deterministic direct scoring disabled.
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

    # No universal fixed numeric values.
    for pattern in FORBIDDEN_FIXED_NUMERIC_PATTERNS:
        assert re.search(pattern, corpus, flags=re.IGNORECASE) is None, pattern

    # Routing strength.
    routing = " ".join(model["routing_aliases"] + model["routing_field_points"]).lower()
    for concept in (
        "electronics",
        "noise",
        "drift",
        "tolerance",
        "aging",
        "psrr",
        "reference",
        "adc",
        "error budget",
        "calibration",
    ):
        assert concept in routing, concept

    print("FOCUSED_TOPIC_REGRESSION=PASS")
    print(f"topic_id={TOPIC_ID}")
    print(f"question_type={QUESTION_TYPE}")
    print(f"difficulty={DIFFICULTY}")
    print(f"selection_importance={SELECTION_IMPORTANCE}")
    print(f"anchors={len(anchors_list)}")
    print(f"resolved_anchor_refs={len(refs)}")
    print(f"routing_aliases={len(model['routing_aliases'])}")
    print(f"routing_field_points={len(model['routing_field_points'])}")
    print(f"fatal_wrong_claims={len(fatal_ids)}")
    print("ownership_boundaries=5")
    print("noise_systematic_drift_distinction=true")
    print("offset_gain_linearity_distinction=true")
    print("tolerance_drift_aging_distinction=true")
    print("noise_bandwidth_snr_semantics=true")
    print("psrr_reference_error_path=true")
    print("adc_resolution_accuracy_distinction=true")
    print("filter_calibration_limitations=true")
    print("error_budget_combination=true")
    print("diagnosis_mitigation_residual_chain=true")
    print("specific_universal_numeric_values_hardcoded=false")
    print("historical_frequency_asserted=false")
    print("direct_score_application=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
