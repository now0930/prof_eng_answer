#!/usr/bin/env python3
"""Build the reviewed 30-case expert-accuracy corpus from frozen references."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from expert_accuracy_benchmark import load_jsonl, validate_gold_case
from question_demand_contract import build_question_demand_contract


GOLDEN = ROOT / "calibration" / "expert_accuracy_golden.jsonl"
MODEL_FIXTURE = ROOT / "calibration" / "expert_accuracy_model_answer_cases.json"
REVIEW_EVIDENCE = "calibration/reviews/expert_accuracy_expansion_30.review.md"
REVIEWED_AT = "2026-09-02T22:30:00+09:00"

MODEL_TOPICS = (
    "piezoelectric_sensor_charge_amplifier_dynamic_force_pressure_acceleration",
    "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error",
    "control_valve_authority_rangeability_gain_installed_performance",
    "control_valve_types_globe_rotary_body_actuator_selection",
    "humidity_measurement_capacitive_resistive_dew_point_selection_compensation",
    "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection",
    "smart_positioner_diagnostics_valve_signature_predictive_maintenance",
    "instrumentation_power_grounding_shielding_ups_ground_loop_emc",
    "electronics_error_noise_drift_tolerance_aging_power_mitigation",
    "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response",
    "configuration_change_release_backup_rollback_migration_obsolescence_management",
    "control_hardware_lifecycle_panel_architecture_component_selection_production_verification",
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
    "control_valve_deadband_stiction_response_time_positioner_dynamic_performance",
    "final_control_element_sil_sis_esd_valve_partial_stroke_test",
)

QTYPE_MAP = {
    "PRINCIPLE_INTERPRETATION": "PRINCIPLE_INTERPRETATION",
    "COMPARE_SELECTION": "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION": "DIAGNOSIS_ACTION",
    "IMPLEMENTATION_EVALUATION": "IMPLEMENTATION_EVALUATION",
    "PROBLEM_SOLVE": "IMPLEMENTATION_EVALUATION",
    "DESIGN": "IMPLEMENTATION_EVALUATION",
}


def _review() -> dict[str, str]:
    return {
        "reviewer": "workspace_owner_delegated_review",
        "method": "user_approval",
        "reviewed_at": REVIEWED_AT,
        "evidence_path": REVIEW_EVIDENCE,
    }


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]


def _qtype_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "calibration" / "qtype_golden" / "cases").glob("*.json")):
        collection = json.loads(path.read_text(encoding="utf-8"))
        for case in collection["cases"]:
            expected = case["expected"]
            demands = []
            status_map = expected["demand_status"]
            for demand in expected["question_demands"]:
                demand_id = str(demand["id"])
                demands.append({
                    "demand_id": demand_id,
                    "requirement": str(demand["text"]),
                    "core": bool(demand.get("is_core", True)),
                    "status": status_map[demand_id],
                })
            level = str(case["answer_level"]).upper()
            rows.append({
                "version": "expert_accuracy_case_v1",
                "case_id": f"qtype_{case['case_id'].lower()}",
                "review_status": "reviewed",
                "review": _review(),
                "source": {
                    "kind": "qtype_golden_case",
                    "path": str(path.relative_to(ROOT)),
                    "source_case_id": case["case_id"],
                },
                "topic_ids": expected["expected_topic_ids"],
                "question_type": case["question_type"],
                "labels": {
                    "demands": demands,
                    "findings": [],
                    "score_range": expected["total_range"],
                    "flags": {
                        "passing_score_allowed": level in {"PASS", "HIGH"},
                        "strong_verdict_allowed": level == "HIGH",
                        "confidence_ceiling": "high",
                    },
                },
                "notes": "기존 Production QType Golden의 독립 정답·점수 범위를 전문가 정확도 형식으로 투영.",
            })
    return rows


def _model_cases() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fixtures: list[dict[str, Any]] = []
    gold: list[dict[str, Any]] = []
    for index, topic_id in enumerate(MODEL_TOPICS, start=1):
        source_path = ROOT / "rubrics" / "topic_packs" / topic_id / "model_answer.json"
        source = json.loads(source_path.read_text(encoding="utf-8"))
        questions = _strings(source.get("question_examples"))
        if not questions:
            raise ValueError(f"question_examples missing: {topic_id}")
        question = questions[0]
        high_points = _strings(source.get("high_score_points"))
        field_points = _strings(source.get("routing_field_points"))[:4]
        if len(high_points) < 5:
            raise ValueError(f"insufficient high_score_points: {topic_id}")
        answer_lines = ["1. 핵심 원리·판단 기준"]
        answer_lines.extend(f"- {point}" for point in high_points)
        if field_points:
            answer_lines.append("\n2. 현장 적용·검증")
            answer_lines.extend(f"- {point}" for point in field_points)
        answer_lines.append("\n3. 결론")
        answer_lines.append("- 요구조건, 적용경계, 검증기준과 운전 피드백을 연결하여 관리한다.")
        answer = "\n".join(answer_lines)
        case_id = f"model_reference_{index:02d}_{topic_id}"
        fixtures.append({
            "case_id": case_id,
            "topic_id": topic_id,
            "question": question,
            "answer": answer,
            "source_model_answer": str(source_path.relative_to(ROOT)),
        })
        contract = build_question_demand_contract(question)
        demands = [
            {
                "demand_id": row["requirement_id"],
                "requirement": row["requirement_text"],
                "core": True,
                "status": "CORRECT",
            }
            for row in contract["requirements"]
        ]
        raw_qtype = str(source.get("question_type") or contract["primary_lens"])
        question_type = QTYPE_MAP.get(raw_qtype, contract["primary_lens"])
        gold.append({
            "version": "expert_accuracy_case_v1",
            "case_id": case_id,
            "review_status": "reviewed",
            "review": _review(),
            "source": {
                "kind": "topic_pack_model_reference",
                "path": str(MODEL_FIXTURE.relative_to(ROOT)),
                "source_case_id": case_id,
                "authoritative_path": str(source_path.relative_to(ROOT)),
            },
            "topic_ids": [topic_id],
            "question_type": question_type,
            "labels": {
                "demands": demands,
                "findings": [],
                "score_range": {"min": 14.0, "max": 24.0},
                "flags": {
                    "passing_score_allowed": True,
                    "strong_verdict_allowed": True,
                    "confidence_ceiling": "high",
                },
            },
            "notes": "Topic Pack 정본 high_score_points 전체로 구성한 정답 참조 사례.",
        })
    return fixtures, gold


def main() -> None:
    existing = load_jsonl(GOLDEN, validate_gold_case)
    seed_ids = {
        "sil_target_operations_issue1",
        "sis_lopa_architecture_issue1",
        "mcdc_vmodel_sil_issue1",
    }
    seed = [row for row in existing if row["case_id"] in seed_ids]
    if len(seed) != 3:
        raise ValueError("three reviewed seed cases are required")
    fixtures, model_gold = _model_cases()
    rows = seed + _qtype_cases() + model_gold
    if len(rows) != 30 or len({row["case_id"] for row in rows}) != 30:
        raise ValueError("expanded corpus must contain exactly 30 unique cases")
    for row in rows:
        validate_gold_case(row)
    MODEL_FIXTURE.write_text(
        json.dumps(
            {
                "schema_version": "expert_accuracy_model_reference_cases_v1",
                "cases": fixtures,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    GOLDEN.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )
    print(f"EXPERT_ACCURACY_CASES={len(rows)}")
    print(f"QTYPE_CASES={len(_qtype_cases())}")
    print(f"MODEL_REFERENCE_CASES={len(model_gold)}")


if __name__ == "__main__":
    main()
