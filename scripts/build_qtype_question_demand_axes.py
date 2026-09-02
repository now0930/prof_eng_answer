#!/usr/bin/env python3
"""Publish reviewed QType question demands as question-only Topic Pack axes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "calibration" / "qtype_golden" / "cases"
PACK_ROOT = ROOT / "rubrics" / "topic_packs"

ACTIVATION = {
    "control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe": [
        ["제어밸브", "control valve"], ["완전 닫힘", "close failure"],
        ["스템 마찰", "stiction"],
    ],
    "thermocouple_temperature_sensor_seebeck_reference_junction_compensation": [
        ["열전대", "thermocouple"], ["기준접점", "reference junction"],
    ],
    "rtd_temperature_sensor_principle_pt100_wiring_compensation": [
        ["rtd", "pt100"], ["2선식", "3선식", "4선식"],
    ],
    "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error": [
        ["스트레인 게이지", "strain gauge"], ["로드셀", "load cell"],
        ["휘트스톤", "wheatstone"],
    ],
    "balanced_trim_unbalanced_trim_structure_sealing_applications": [
        ["balanced trim"], ["unbalanced trim"],
    ],
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection": [
        ["zone 0"], ["위험장소", "hazardous area"],
    ],
    "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection": [
        ["fieldbus"], ["industrial ethernet", "산업용 이더넷"],
        ["산업용 무선", "wireless"],
    ],
    "configuration_change_release_backup_rollback_migration_obsolescence_management": [
        ["plc", "dcs"], ["release"], ["backup"], ["rollback"],
        ["regression"],
    ],
}

KINDS = {
    "PRINCIPLE_INTERPRETATION": "PRINCIPLE_INTERPRET",
    "COMPARE_SELECTION": "COMPARE",
    "DIAGNOSIS_ACTION": "DIAGNOSE_CAUSE",
    "IMPLEMENTATION_EVALUATION": "IMPLEMENT",
}


def main() -> None:
    published: set[str] = set()
    for path in sorted(CASE_ROOT.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        lens = str(payload["question_type"])
        for case in payload["cases"]:
            topic_id = str(case["expected"]["expected_topic_ids"][0])
            if topic_id in published:
                continue
            demands = case["expected"]["question_demands"]
            output = {
                "schema_version": "topic_pack_question_demand_axes_v1",
                "topic_id": topic_id,
                "mode": "question_only_deterministic",
                "score_effect": "semantic_guidance_only",
                "answer_text_dependency": "none",
                "activation": {"all_term_groups": ACTIVATION[topic_id]},
                "requirements": [
                    {
                        "requirement_id": str(row["id"]),
                        "demand_kind": KINDS[lens],
                        "demand_label": str(row["text"]),
                        "requirement_text": str(row["text"]),
                        "is_core": bool(row.get("is_core", True)),
                        "source_json_pointers": [
                            f"calibration/qtype_golden/cases/{path.name}#/{case['case_id']}/{index}"
                        ],
                    }
                    for index, row in enumerate(demands)
                ],
                "canonical_primary_lens": lens,
            }
            target = PACK_ROOT / topic_id / "question_demand_axes.json"
            target.write_text(
                json.dumps(output, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            published.add(topic_id)
            print(target.relative_to(ROOT))
    missing = set(ACTIVATION) - published
    if missing:
        raise SystemExit(f"unpublished topic demand axes: {sorted(missing)}")


if __name__ == "__main__":
    main()
