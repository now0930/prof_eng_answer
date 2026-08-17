#!/usr/bin/env python3
# Focused regression for V-Model/SIL/MC-DC category overgrading.

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]

TARGET = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
SW04 = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
SW05 = "sis_sil_safety_software_independence_systematic_failure_verification_validation"

SW04_FATAL = "sw04_fatal_misra_is_unit_test_tool"
SW05_RANDOM_FATAL = "sw05_fatal_software_test_is_random_hardware_integrity"
SW05_HFT_FATAL = "sw05_fatal_hft_is_integration_test"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fatal_ids(items: list[Any]) -> set[str]:
    result: set[str] = set()
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result.add(item["id"])
        elif isinstance(item, str):
            match = re.match(r"\s*\[([^\]]+)\]", item)
            if match:
                result.add(match.group(1))
    return result


def main() -> None:
    sw04_logic = load_json(
        REPO / "rubrics" / "topic_packs" / SW04 / "logic_check.json"
    )
    sw05_logic = load_json(
        REPO / "rubrics" / "topic_packs" / SW05 / "logic_check.json"
    )
    mcdc_logic = load_json(
        REPO / "rubrics" / "topic_packs" / TARGET / "logic_check.json"
    )
    sw04_model = load_json(
        REPO / "rubrics" / "topic_packs" / SW04 / "model_answer.json"
    )
    sw05_model = load_json(
        REPO / "rubrics" / "topic_packs" / SW05 / "model_answer.json"
    )
    fixture = load_json(
        REPO / "calibration"
        / "mcdc_vmodel_sil_overgrading_regression.json"
    )
    production_pi = load_json(
        REPO / "calibration" / "qtype_golden" / "cases"
        / "principle_interpretation.json"
    )

    sw04_det = fatal_ids(
        sw04_logic["deterministic_checks"]["fatal_checks"]
    )
    sw04_llm = fatal_ids(sw04_logic["llm_profile"]["fatal_conditions"])
    sw05_det = fatal_ids(
        sw05_logic["deterministic_checks"]["fatal_checks"]
    )
    sw05_llm = fatal_ids(sw05_logic["llm_profile"]["fatal_conditions"])
    mcdc_llm = fatal_ids(mcdc_logic["llm_profile"]["fatal_conditions"])

    assert SW04_FATAL in sw04_det
    assert SW04_FATAL in sw04_llm
    assert SW05_RANDOM_FATAL in sw05_det
    assert SW05_RANDOM_FATAL in sw05_llm
    assert SW05_HFT_FATAL in sw05_det
    assert SW05_HFT_FATAL in sw05_llm
    assert "mcdc_proves_requirements" in mcdc_llm
    assert "sil_four_universal_rule" in mcdc_llm
    assert sw05_logic["deterministic_checks"]["enabled"] is False

    det_item = next(
        item
        for item in sw04_logic["deterministic_checks"]["fatal_checks"]
        if item.get("id") == SW04_FATAL
    )
    samples = [
        "| 단위 | 단일 모듈 | xUnit, MISRA | Random Integrity |",
        "단위시험 도구: MISRA",
        "MISRA를 단위시험 도구로 사용한다.",
    ]
    compiled = [re.compile(pattern) for pattern in det_item["wrong_patterns"]]
    for sample in samples:
        assert any(regex.search(sample) for regex in compiled), sample

    sw04_high = "\n".join(sw04_model["high_score_points"])
    sw05_high = "\n".join(sw05_model["high_score_points"])
    assert "MISRA" in sw04_high and "단위시험" in sw04_high
    assert "Random Hardware Integrity" in sw05_high
    assert "HFT" in sw05_high and "통합시험" in sw05_high

    # Production Golden remains atomic: LOW, PASS and HIGH exactly once.
    assert len(production_pi["cases"]) == 3
    assert sorted(
        case["answer_level"] for case in production_pi["cases"]
    ) == ["HIGH", "LOW", "PASS"]
    assert not any(
        case.get("case_id") == "QG-PI-LOW-02"
        for case in production_pi["cases"]
    )

    assert fixture["schema_version"] == (
        "mcdc_vmodel_sil_overgrading_regression.v1"
    )
    assert fixture["regression_id"] == "MCDC-VMODEL-SIL-OVERGRADING-01"
    assert fixture["source_session_id"] == "20260815_060014_5960502198"
    assert fixture["question_type"] == "PRINCIPLE_INTERPRETATION"
    assert fixture["expected_topic_ids"] == [SW04, SW05, TARGET]

    expected = fixture["expected"]
    assert expected["fatal_logic_expectation"] == "FATAL_EXPECTED"
    assert expected["fact_cap_behavior"] == "CAP_EXPECTED"
    assert expected["critical_fact_expectation"] == (
        "CRITICAL_ERROR_EXPECTED"
    )
    assert expected["maximum_total_score"] == 14.5
    assert expected["total_range"]["max"] == 14.5
    assert expected["requirements_full_credit_allowed"] is False
    assert expected["strong_verdict_allowed"] is False
    assert expected["passing_score_allowed"] is False

    statuses = expected["demand_status"]
    assert sum(value == "incorrect" for value in statuses.values()) == 4
    assert sum(value == "partial" for value in statuses.values()) == 2
    assert "present" not in statuses.values()

    required_ids = set(expected["required_fatal_ids"])
    assert {
        SW04_FATAL,
        SW05_RANDOM_FATAL,
        SW05_HFT_FATAL,
        "mcdc_proves_requirements",
        "sil_four_universal_rule",
        "sw04_fatal_general_vv_proves_sil",
    } <= required_ids

    forbidden = "\n".join(expected["forbidden_feedback_elements"])
    assert "strong" in forbidden
    assert "15점 이상" in forbidden
    assert "100%" in forbidden

    print("MCDC_VMODEL_SIL_OVERGRADING_REGRESSION=PASS")
    print("PRODUCTION_PI_CASES=3")
    print("FIXTURE=MCDC-VMODEL-SIL-OVERGRADING-01")
    print("FATAL_IDS=6")
    print("TOTAL_MAX=14.5")
    print("INCORRECT_DEMANDS=4")
    print("PARTIAL_DEMANDS=2")


if __name__ == "__main__":
    main()
