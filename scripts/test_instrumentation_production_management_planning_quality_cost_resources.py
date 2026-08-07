#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

TOPIC_ID = "instrumentation_production_management_planning_quality_cost_resources"
QUESTION_TYPE = "IMPLEMENTATION_EVALUATION"
DIFFICULTY = "DESIGN_EVALUATION"
SELECTION_IMPORTANCE = "NORMAL"

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def norm(text: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", " ", text.casefold()).strip()


def row_surface(row: dict) -> str:
    parts: list[str] = []
    for key in (
        "statement",
        "claim",
        "description",
        "keywords",
        "core_terms",
        "accepted_explanations",
        "grading_notes",
    ):
        value = row.get(key)
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
    return "\n".join(parts).casefold()


def has_all(surface: str, groups: Iterable[Iterable[str]]) -> bool:
    for alternatives in groups:
        if not any(token.casefold() in surface for token in alternatives):
            return False
    return True


def main() -> None:
    fact = load("fact_anchor.json")
    logic = load("logic_check.json")
    model = load("model_answer.json")
    importance = load("topic_importance.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

    # 1. Identity and classification.
    require(fact["schema_version"] == "fact_anchor.v1", "fact schema")
    require(logic["schema_version"] == "topic_pack.logic_check.v1", "logic schema")
    require(model["schema_version"] == "topic_pack.model_answer.v1", "model schema")
    require(
        importance["schema_version"] == "topic_pack.topic_importance.v1",
        "importance schema",
    )

    for name, obj in (
        ("fact", fact),
        ("logic", logic),
        ("model", model),
        ("importance", importance),
    ):
        require(obj["topic_id"] == TOPIC_ID, f"{name} topic_id")

    require(fact["question_type_hint"] == QUESTION_TYPE, "fact question type")
    require(model["question_type"] == QUESTION_TYPE, "model question type")
    require(importance["question_type"] == QUESTION_TYPE, "importance question type")
    require(importance["difficulty"] == DIFFICULTY, "difficulty")
    require(
        importance["selection_importance"] == SELECTION_IMPORTANCE,
        "selection importance",
    )

    # 2. Exact 28-anchor ownership.
    anchors = fact["anchors"]
    require(len(anchors) == 28, "anchor count must remain 28")
    anchor_ids = [row["id"] for row in anchors]
    require(len(anchor_ids) == len(set(anchor_ids)), "anchor IDs must be unique")
    require(
        all(row["id"] == row["anchor_id"] for row in anchors),
        "anchor id/anchor_id drift",
    )
    require(
        all(row["statement"] == row["claim"] == row["description"] for row in anchors),
        "anchor statement/claim/description projection drift",
    )

    expected_anchor_ids = {
        "production_management_objective_scope",
        "production_demand_order_plan_translation",
        "production_horizon_master_detailed_schedule",
        "production_takt_cycle_time_boundary",
        "production_capacity_available_time_rate",
        "production_bottleneck_throughput_constraint",
        "production_line_balancing_workload",
        "production_finite_capacity_schedule_dispatch",
        "production_changeover_sequence_batch_tradeoff",
        "production_wip_flow_lead_time",
        "production_material_requirement_availability",
        "production_manpower_skill_shift",
        "production_equipment_resource_availability",
        "production_quality_plan_ctq_spec",
        "production_fpy_yield_scrap_rework",
        "production_process_quality_feedback",
        "production_defect_containment_traceability",
        "production_cost_structure",
        "production_standard_actual_cost_variance",
        "production_unit_cost_volume_yield",
        "production_energy_consumables_cost",
        "production_oee_apq_formula_boundary",
        "production_throughput_cycle_lead_wip_kpi",
        "production_schedule_adherence_delivery_kpi",
        "production_mes_data_handoff",
        "production_erp_mes_role_boundary",
        "production_daily_management_visual_control",
        "production_pdca_tradeoff_improvement",
    }
    require(set(anchor_ids) == expected_anchor_ids, "anchor set drift")
    by_id = {row["id"]: row for row in anchors}

    # 3. Production-management objective / planning hierarchy.
    require(
        has_all(
            row_surface(by_id["production_management_objective_scope"]),
            (
                ("생산관리", "production management"),
                ("품질", "quality"),
                ("납기", "delivery"),
                ("원가", "cost"),
                ("생산능력", "capacity"),
                ("인력", "manpower"),
                ("자재", "material"),
                ("설비", "equipment"),
            ),
        ),
        "production-management objective/trade-off weak",
    )
    require(
        has_all(
            row_surface(by_id["production_demand_order_plan_translation"]),
            (
                ("수요", "demand"),
                ("주문", "order"),
                ("제품 mix", "product mix"),
                ("rolling", "재계획"),
            ),
        ),
        "demand/order-to-plan mechanism weak",
    )
    require(
        has_all(
            row_surface(by_id["production_horizon_master_detailed_schedule"]),
            (
                ("planning horizon", "시간 horizon"),
                ("master production schedule", "mps"),
                ("상세일정", "detailed schedule"),
            ),
        ),
        "planning hierarchy weak",
    )

    # 4. Takt / Cycle Time / capacity / bottleneck.
    require(
        has_all(
            row_surface(by_id["production_takt_cycle_time_boundary"]),
            (
                ("takt time",),
                ("cycle time",),
                ("고객 요구수량", "customer demand"),
                ("가용 생산시간", "available production time"),
            ),
        ),
        "Takt/Cycle boundary weak",
    )
    require(
        has_all(
            row_surface(by_id["production_capacity_available_time_rate"]),
            (
                ("생산능력", "capacity"),
                ("가용시간", "available time"),
                ("이론능력", "theoretical capacity"),
                ("유효능력", "effective capacity"),
            ),
        ),
        "capacity boundary weak",
    )
    require(
        has_all(
            row_surface(by_id["production_bottleneck_throughput_constraint"]),
            (
                ("bottleneck", "병목"),
                ("throughput",),
                ("blocking", "차단"),
                ("starvation", "기아"),
            ),
        ),
        "bottleneck/throughput mechanism weak",
    )
    require(
        has_all(
            row_surface(by_id["production_line_balancing_workload"]),
            (
                ("line balancing", "라인 밸런싱"),
                ("takt",),
                ("precedence", "작업순서"),
            ),
        ),
        "line-balancing mechanism weak",
    )

    # 5. Finite schedule / changeover / WIP.
    require(
        has_all(
            row_surface(by_id["production_finite_capacity_schedule_dispatch"]),
            (
                ("finite",),
                ("dispatch", "작업순서"),
                ("due date", "납기"),
                ("changeover",),
            ),
        ),
        "finite-capacity scheduling weak",
    )
    require(
        has_all(
            row_surface(by_id["production_changeover_sequence_batch_tradeoff"]),
            (
                ("changeover",),
                ("sequence",),
                ("batch size",),
                ("wip",),
                ("lead time",),
            ),
        ),
        "changeover/batch trade-off weak",
    )
    require(
        has_all(
            row_surface(by_id["production_wip_flow_lead_time"]),
            (
                ("wip",),
                ("lead time",),
                ("buffer", "완충"),
            ),
        ),
        "WIP/flow/lead-time mechanism weak",
    )

    # 6. Material / manpower / equipment resources.
    require(
        has_all(
            row_surface(by_id["production_material_requirement_availability"]),
            (
                ("bom",),
                ("lead time",),
                ("결품", "stockout"),
                ("라인투입", "material availability"),
            ),
        ),
        "material planning weak",
    )
    require(
        has_all(
            row_surface(by_id["production_manpower_skill_shift"]),
            (
                ("shift",),
                ("skill matrix",),
                ("표준작업", "standard work"),
            ),
        ),
        "manpower planning weak",
    )
    equipment_surface = row_surface(by_id["production_equipment_resource_availability"])
    require(
        has_all(
            equipment_surface,
            (
                ("가용시간", "available time"),
                ("capability",),
                ("tooling",),
                ("o&m", "maintenance"),
            ),
        ),
        "equipment-resource/O&M handoff weak",
    )

    # 7. Production quality.
    require(
        has_all(
            row_surface(by_id["production_quality_plan_ctq_spec"]),
            (
                ("ctq",),
                ("specification",),
                ("inspection", "검사"),
                ("reaction plan",),
            ),
        ),
        "CTQ/control-plan mechanism weak",
    )
    require(
        has_all(
            row_surface(by_id["production_fpy_yield_scrap_rework"]),
            (
                ("fpy",),
                ("yield",),
                ("scrap",),
                ("rework",),
            ),
        ),
        "quality KPI boundary weak",
    )
    require(
        has_all(
            row_surface(by_id["production_process_quality_feedback"]),
            (
                ("trend",),
                ("관리한계", "control limit"),
                ("격리", "containment"),
                ("재발방지", "corrective action"),
            ),
        ),
        "process-quality feedback weak",
    )
    require(
        has_all(
            row_surface(by_id["production_defect_containment_traceability"]),
            (
                ("traceability",),
                ("lot",),
                ("genealogy",),
                ("격리", "containment"),
            ),
        ),
        "defect containment/traceability weak",
    )

    # 8. Production cost.
    require(
        has_all(
            row_surface(by_id["production_cost_structure"]),
            (
                ("생산원가", "production cost"),
                ("재료비", "direct material"),
                ("노무비", "direct labor"),
                ("제조간접비", "manufacturing overhead"),
            ),
        ),
        "production-cost structure weak",
    )
    require(
        has_all(
            row_surface(by_id["production_standard_actual_cost_variance"]),
            (
                ("standard cost", "표준"),
                ("actual cost",),
                ("variance", "편차"),
                ("scrap",),
                ("downtime",),
            ),
        ),
        "standard/actual cost variance weak",
    )
    require(
        has_all(
            row_surface(by_id["production_unit_cost_volume_yield"]),
            (
                ("단위원가", "unit cost"),
                ("양품", "good units"),
                ("yield",),
                ("scrap",),
            ),
        ),
        "unit-cost/yield/volume relationship weak",
    )
    require(
        has_all(
            row_surface(by_id["production_energy_consumables_cost"]),
            (
                ("energy", "에너지"),
                ("utility",),
                ("소모품", "consumable"),
                ("idle",),
            ),
        ),
        "energy/consumables cost weak",
    )

    # 9. OEE and flow/delivery KPI.
    oee_surface = row_surface(by_id["production_oee_apq_formula_boundary"])
    require(
        has_all(
            oee_surface,
            (
                ("oee",),
                ("availability",),
                ("performance",),
                ("quality",),
                ("planned production",),
            ),
        ),
        "OEE A/P/Q contract weak",
    )
    require(
        has_all(
            row_surface(by_id["production_throughput_cycle_lead_wip_kpi"]),
            (
                ("throughput",),
                ("cycle time",),
                ("lead time",),
                ("wip",),
            ),
        ),
        "flow KPI boundary weak",
    )
    require(
        has_all(
            row_surface(by_id["production_schedule_adherence_delivery_kpi"]),
            (
                ("schedule adherence", "계획 준수율"),
                ("on-time", "납기"),
                ("due",),
            ),
        ),
        "delivery KPI boundary weak",
    )

    # 10. MES / ERP / production-decision ownership.
    mes_surface = row_surface(by_id["production_mes_data_handoff"])
    require(
        has_all(
            mes_surface,
            (
                ("mes",),
                ("historian",),
                ("genealogy",),
                ("생산관리", "production management"),
            ),
        ),
        "MES/Historian handoff weak",
    )
    erp_surface = row_surface(by_id["production_erp_mes_role_boundary"])
    require(
        has_all(
            erp_surface,
            (
                ("erp",),
                ("mes",),
                ("capacity",),
                ("resource", "자원"),
            ),
        ),
        "ERP/MES/production-management hierarchy weak",
    )

    # 11. Daily management and multi-objective PDCA.
    require(
        has_all(
            row_surface(by_id["production_daily_management_visual_control"]),
            (
                ("daily", "일일"),
                ("shift",),
                ("owner",),
                ("due date",),
            ),
        ),
        "daily-management action loop weak",
    )
    require(
        has_all(
            row_surface(by_id["production_pdca_tradeoff_improvement"]),
            (
                ("plan-do-check-act", "pdca"),
                ("bottleneck", "병목"),
                ("resource", "자원"),
                ("안전", "safety"),
                ("품질", "quality"),
                ("납기", "delivery"),
                ("원가", "cost"),
            ),
        ),
        "PDCA multi-objective improvement weak",
    )

    # 12. Fatal contract: exact IDs/order and C-only ownership.
    fatal = fact["fatal_wrong_claims"]
    require(len(fatal) == 14, "fatal count must remain 14")
    fatal_ids = [row["id"] for row in fatal]
    expected_fatal_ids = [
        "production_fatal_max_output_only",
        "production_fatal_takt_equals_cycle",
        "production_fatal_nameplate_equals_capacity",
        "production_fatal_local_oee_guarantees_throughput",
        "production_fatal_infinite_capacity_schedule",
        "production_fatal_large_batch_always_best",
        "production_fatal_more_wip_always_better",
        "production_fatal_quality_final_inspection_only",
        "production_fatal_fpy_equals_final_yield",
        "production_fatal_material_cost_only",
        "production_fatal_oee_proves_all_performance",
        "production_fatal_flow_kpis_interchangeable",
        "production_fatal_mes_automates_management",
        "production_fatal_project_or_maintenance_scope_takeover",
    ]
    require(fatal_ids == expected_fatal_ids, "fatal ID/order drift")
    require(
        all(row["severity"] == "fatal" for row in fatal),
        "fatal severity drift",
    )
    require(
        all(row["affected_layers"] == ["C"] for row in fatal),
        "fatal affected_layers must remain C-only",
    )

    # 13. LLM-only logic contract and exact projections.
    det = logic["deterministic_checks"]
    profile = logic["llm_profile"]

    require(det["enabled"] is False, "deterministic checks must stay disabled")
    require(det["topic_aliases"] == [], "deterministic topic aliases must stay empty")
    require(det["fatal_checks"] == [], "deterministic fatal checks must stay empty")
    require(det["major_checks"] == [], "deterministic major checks must stay empty")
    require(
        det["question_type_checks"] == [],
        "deterministic question-type checks must stay empty",
    )

    require(profile["enabled"] is True, "LLM profile must stay enabled")
    require(
        profile["candidate_extraction"]["rules"] == [],
        "candidate-extraction rules must stay empty",
    )
    require(
        profile["score_policy"]
        == {
            "direct_score_application": False,
            "direct_d_e_effect": "none",
            "affected_layers": ["C"],
        },
        "LLM score policy drift",
    )
    require(
        profile["truth_schema"] == [row["statement"] for row in anchors],
        "truth_schema must be exact Fact Anchor projection",
    )
    require(
        len(profile["fatal_conditions"]) == len(fatal),
        "fatal projection cardinality mismatch",
    )
    for idx, row in enumerate(fatal):
        projected = profile["fatal_conditions"][idx]
        require(
            projected.startswith(f"[{row['id']}] "),
            f"fatal projection ID/order mismatch: {row['id']}",
        )
        require(row["claim"] in projected, f"fatal claim missing: {row['id']}")
        require(
            row["correction"] in projected,
            f"fatal correction missing: {row['id']}",
        )

    require(len(profile["major_checks"]) == 10, "major-check count drift")
    require(
        len(profile["false_positive_cautions"]) == 15,
        "false-positive caution count drift",
    )

    # 14. Model references and full outline coverage.
    anchor_set = set(anchor_ids)
    patterns = model["expected_question_patterns"]
    require(len(patterns) == 10, "question-pattern count drift")
    for row in patterns:
        refs = set(row["required_anchor_ids"])
        require(refs, "question pattern missing anchor refs")
        require(refs <= anchor_set, f"unknown question-pattern anchor: {refs - anchor_set}")

    outline = model["recommended_outline"]
    require(len(outline) == 8, "outline section count drift")
    outline_union: set[str] = set()
    for row in outline:
        refs = set(row["anchor_refs"])
        require(refs <= anchor_set, f"unknown outline anchor: {refs - anchor_set}")
        outline_union |= refs
    require(outline_union == anchor_set, "outline does not cover all 28 anchors")

    # 15. Routing aliases must be production-management specific.
    aliases = model["routing_aliases"]
    require(len(aliases) == 18, "routing alias count drift")
    forbidden_generic = {
        "production",
        "production management",
        "quality",
        "cost",
        "resource",
        "oee",
        "생산",
        "생산관리",
        "생산 관리",
        "품질",
        "원가",
        "비용",
        "자원",
    }
    normalized_aliases = {norm(alias) for alias in aliases}
    require(
        not (normalized_aliases & forbidden_generic),
        f"generic alias introduced: {normalized_aliases & forbidden_generic}",
    )
    require(
        any(
            ("capacity" in a.casefold() or "생산능력" in a)
            and ("quality" in a.casefold() or "품질" in a)
            for a in aliases
        ),
        "capacity/quality alias coverage missing",
    )
    require(
        any(
            ("oee" in a.casefold())
            and ("throughput" in a.casefold() or "생산성" in a)
            for a in aliases
        ),
        "OEE/performance alias coverage missing",
    )
    require(
        any(
            ("manpower" in a.casefold() or "인력" in a)
            and ("material" in a.casefold() or "자재" in a)
            for a in aliases
        ),
        "resource-planning alias coverage missing",
    )

    # 16. Human-readable ownership handoffs.
    human_text = readme + "\n" + sheet
    for handoff in (
        "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing",
        "control_system_operations_maintenance_calibration_inspection_spares_kpi",
        "instrumentation_project_management_basic_design_cost_schedule_documents_acceptance",
    ):
        require(handoff in human_text, f"ownership handoff missing: {handoff}")

    # 17. Historical-frequency prohibition and no placeholder residue.
    all_text = "\n".join(
        [
            readme,
            sheet,
            json.dumps(fact, ensure_ascii=False),
            json.dumps(logic, ensure_ascii=False),
            json.dumps(model, ensure_ascii=False),
            json.dumps(importance, ensure_ascii=False),
        ]
    )
    require(
        "Historical frequency used" in readme,
        "historical-frequency policy missing",
    )
    for forbidden in ("TODO", "TBD", "FIXME", "PLACEHOLDER"):
        require(forbidden not in all_text, f"placeholder residue: {forbidden}")

    print("PASS: instrumentation production management focused regression")
    print(f"topic_id={TOPIC_ID}")
    print(f"anchors={len(anchors)}")
    print(f"fatals={len(fatal)}")
    print(f"major_checks={len(profile['major_checks'])}")
    print(f"false_positive_cautions={len(profile['false_positive_cautions'])}")
    print(f"question_patterns={len(patterns)}")
    print(f"routing_aliases={len(aliases)}")
    print(f"question_type={importance['question_type']}")
    print(f"difficulty={importance['difficulty']}")
    print("semantic_execution=LLM_ONLY")
    print("deterministic_topic_aliases_empty=INTENTIONAL")
    print("historical_frequency_used=false")


if __name__ == "__main__":
    main()
