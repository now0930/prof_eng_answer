#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "control_system_operations_maintenance_calibration_inspection_spares_kpi"
EXPECTED_QUESTION_TYPE = "IMPLEMENTATION_EVALUATION"
EXPECTED_DIFFICULTY = "DESIGN_EVALUATION"
EXPECTED_SELECTION_IMPORTANCE = "NORMAL"

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize(text: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", " ", text.casefold()).strip()


def main() -> None:
    fact = load("fact_anchor.json")
    logic = load("logic_check.json")
    model = load("model_answer.json")
    importance = load("topic_importance.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

    # 1. Identity and classification contract.
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

    require(
        fact["question_type_hint"] == EXPECTED_QUESTION_TYPE,
        "fact question type",
    )
    require(
        model["question_type"] == EXPECTED_QUESTION_TYPE,
        "model question type",
    )
    require(
        importance["question_type"] == EXPECTED_QUESTION_TYPE,
        "importance question type",
    )
    require(
        importance["difficulty"] == EXPECTED_DIFFICULTY,
        "importance difficulty",
    )
    require(
        importance["selection_importance"] == EXPECTED_SELECTION_IMPORTANCE,
        "importance selection importance",
    )

    # 2. Exact Fact Anchor ownership.
    anchors = fact["anchors"]
    require(len(anchors) == 26, "anchor count must remain 26")
    anchor_ids = [row["id"] for row in anchors]
    require(len(anchor_ids) == len(set(anchor_ids)), "anchor ids must be unique")

    expected_anchor_ids = {
        "om_asset_register_system_boundary",
        "maintenance_strategy_corrective_preventive_condition_predictive",
        "maintenance_criticality_risk_prioritization",
        "maintenance_plan_task_interval_basis",
        "work_order_history_closed_loop",
        "failure_coding_rca_bad_actor_feedback",
        "calibration_program_traceability",
        "calibration_interval_risk_history",
        "calibration_as_found_as_left_oot",
        "calibration_reference_standard_control",
        "inspection_program_routine_functional_loop",
        "inspection_findings_defect_priority_closeout",
        "deferred_maintenance_risk_control",
        "spares_criticality_classification",
        "spares_stock_policy_reorder_leadtime",
        "spares_preservation_shelf_life_rotation",
        "spares_obsolescence_substitution_moc",
        "kpi_mtbf_definition_boundary",
        "kpi_mttr_definition_boundary",
        "kpi_intrinsic_availability_equation",
        "kpi_pm_compliance_backlog_schedule",
        "kpi_gaming_single_metric_tradeoff",
        "maintenance_data_quality_cmms_taxonomy",
        "maintenance_roles_competence_permit_restoration",
        "maintenance_configuration_backup_change_handoff",
        "om_continuous_improvement_pdca_lifecycle_cost",
    }
    require(set(anchor_ids) == expected_anchor_ids, "anchor set drift")

    by_id = {row["id"]: row for row in anchors}

    # 3. Core O&M lifecycle mechanisms.
    strategy = by_id[
        "maintenance_strategy_corrective_preventive_condition_predictive"
    ]["statement"]
    for token in ("Corrective", "Preventive", "Condition-Based", "Predictive"):
        require(token in strategy, f"maintenance strategy token missing: {token}")

    criticality = by_id["maintenance_criticality_risk_prioritization"]["statement"]
    require(
        "안전" in criticality and "생산" in criticality and "복구시간" in criticality,
        "criticality consequence chain incomplete",
    )

    work_order = by_id["work_order_history_closed_loop"]["statement"]
    require(
        "Work Order" in work_order and "as-found" in work_order.casefold(),
        "work-order loop weak",
    )
    require("환류" in work_order, "work-order feedback missing")

    # 4. Calibration management boundary.
    cal_program = by_id["calibration_program_traceability"]["statement"]
    for token in ("허용오차", "기준기", "추적성", "합격기준"):
        require(token in cal_program, f"calibration program token missing: {token}")

    cal_interval = by_id["calibration_interval_risk_history"]["statement"]
    require("drift" in cal_interval and "As-Found".casefold() in cal_interval.casefold(),
            "calibration interval evidence missing")

    oot = by_id["calibration_as_found_as_left_oot"]["statement"]
    for token in ("As-Found", "As-Left", "Out-of-Tolerance", "영향기간"):
        require(token in oot, f"OOT lifecycle token missing: {token}")

    # 5. Inspection / deferred-maintenance boundary.
    inspection = by_id["inspection_program_routine_functional_loop"]["statement"]
    for token in ("Routine Inspection", "기능시험", "Loop Check"):
        require(token in inspection, f"inspection boundary missing: {token}")

    deferred = by_id["deferred_maintenance_risk_control"]["statement"]
    require("위험평가" in deferred and "승인" in deferred, "deferred-maintenance control weak")

    # 6. Spare-parts lifecycle.
    spare_critical = by_id["spares_criticality_classification"]["statement"]
    for token in ("Critical Spare", "Lead Time", "단종"):
        require(token in spare_critical, f"critical spare token missing: {token}")

    spare_stock = by_id["spares_stock_policy_reorder_leadtime"]["statement"]
    require("reorder point" in spare_stock.casefold(), "reorder-point policy missing")

    spare_preservation = by_id["spares_preservation_shelf_life_rotation"]["statement"]
    require("shelf-life" in spare_preservation.casefold(), "shelf-life management missing")

    obsolescence = by_id["spares_obsolescence_substitution_moc"]["statement"]
    require(
        "Last-Time Buy" in obsolescence and "변경관리" in obsolescence,
        "obsolescence/MOC handoff missing",
    )

    # 7. KPI definitions and formula boundary.
    mtbf = by_id["kpi_mtbf_definition_boundary"]["statement"]
    require("MTBF" in mtbf and "고장횟수" in mtbf, "MTBF definition weak")

    mttr = by_id["kpi_mttr_definition_boundary"]["statement"]
    require("MTTR" in mttr and "시작·종료" in mttr, "MTTR boundary weak")

    availability = by_id["kpi_intrinsic_availability_equation"]["statement"]
    require(
        "A_i=MTBF/(MTBF+MTTR)" in availability,
        "intrinsic availability equation missing",
    )
    require(
        "운영가용도" in availability and "계획정지" in availability,
        "operational availability boundary missing",
    )

    process_kpi = by_id["kpi_pm_compliance_backlog_schedule"]["statement"]
    for token in ("PM Compliance", "Schedule Compliance", "Maintenance Backlog"):
        require(token in process_kpi, f"process KPI missing: {token}")

    gaming = by_id["kpi_gaming_single_metric_tradeoff"]["statement"]
    require("단일 KPI" in gaming and "안전" in gaming, "KPI gaming boundary weak")

    # 8. Data/governance/continuous improvement.
    data = by_id["maintenance_data_quality_cmms_taxonomy"]["statement"]
    require("CMMS/EAM" in data and "failure code" in data, "CMMS taxonomy weak")

    roles = by_id["maintenance_roles_competence_permit_restoration"]["statement"]
    require("LOTO" in roles and "복구승인" in roles, "permit/restoration control weak")

    change = by_id["maintenance_configuration_backup_change_handoff"]["statement"]
    require("backup" in change.casefold() and "as-built" in change.casefold(),
            "configuration handoff weak")

    pdca = by_id["om_continuous_improvement_pdca_lifecycle_cost"]["statement"]
    require(
        "lifecycle cost" in pdca.casefold() and "폐루프" in pdca,
        "continuous-improvement loop weak",
    )

    # 9. Fatal contract: verify exact IDs and projection, not brittle prose fragments.
    fatal = fact["fatal_wrong_claims"]
    require(len(fatal) == 14, "fatal count must remain 14")
    fatal_ids = [row["id"] for row in fatal]
    require(len(fatal_ids) == len(set(fatal_ids)), "fatal ids must be unique")

    expected_fatal_ids = [
        "om_fatal_run_to_failure_for_all",
        "om_fatal_price_only_criticality",
        "om_fatal_calibration_equals_adjustment",
        "om_fatal_fixed_calibration_interval",
        "om_fatal_ignore_as_found_oot",
        "om_fatal_visual_inspection_equals_function_test",
        "om_fatal_more_pm_always_better",
        "om_fatal_low_usage_zero_spares",
        "om_fatal_inventory_count_only",
        "om_fatal_uncontrolled_substitution",
        "om_fatal_mtbf_alone_proves_availability",
        "om_fatal_availability_formula_universal",
        "om_fatal_mttr_hands_on_only_universal",
        "om_fatal_single_kpi_optimization",
    ]
    require(fatal_ids == expected_fatal_ids, "fatal ID/order drift")
    require(
        all(row["severity"] == "fatal" for row in fatal),
        "fact fatal severity drift",
    )
    require(
        all(row["affected_layers"] == ["C"] for row in fatal),
        "fact fatal ownership must remain C-only",
    )

    # 10. LLM-only semantic ownership and 1:1 projections.
    det = logic["deterministic_checks"]
    profile = logic["llm_profile"]

    require(det["enabled"] is False, "deterministic semantic checks must stay disabled")
    require(det["topic_aliases"] == [], "deterministic topic aliases must remain empty")
    require(det["fatal_checks"] == [], "deterministic fatal checks must remain empty")
    require(det["major_checks"] == [], "deterministic major checks must remain empty")
    require(
        det["question_type_checks"] == [],
        "deterministic question-type checks must remain empty",
    )

    require(profile["enabled"] is True, "LLM profile must stay enabled")
    require(
        profile["candidate_extraction"]["rules"] == [],
        "candidate extraction rules must stay empty",
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
        "truth_schema is not exact Fact Anchor projection",
    )
    require(
        len(profile["fatal_conditions"]) == len(fatal),
        "fatal projection cardinality mismatch",
    )
    for idx, row in enumerate(fatal):
        projected = profile["fatal_conditions"][idx]
        require(
            projected.startswith(f"[{row['id']}] "),
            f"fatal ID/order projection mismatch: {row['id']}",
        )
        require(row["claim"] in projected, f"fatal claim missing: {row['id']}")
        require(row["correction"] in projected, f"fatal correction missing: {row['id']}")

    require(len(profile["major_checks"]) == 10, "major check count drift")
    require(
        len(profile["false_positive_cautions"]) == 14,
        "false-positive caution count drift",
    )

    # 11. Model-answer references must cover all anchors.
    anchor_set = set(anchor_ids)
    patterns = model["expected_question_patterns"]
    require(len(patterns) == 10, "question pattern count")
    for row in patterns:
        refs = set(row["required_anchor_ids"])
        require(refs, "question pattern without required anchors")
        require(refs <= anchor_set, f"unknown pattern anchor: {refs - anchor_set}")

    outline = model["recommended_outline"]
    require(len(outline) == 8, "outline section count")
    outline_union: set[str] = set()
    for row in outline:
        refs = set(row["anchor_refs"])
        require(refs <= anchor_set, f"unknown outline anchor: {refs - anchor_set}")
        outline_union |= refs
    require(outline_union == anchor_set, "outline must cover all Fact Anchors")

    # 12. Routing aliases must express O&M management scope, not generic single terms.
    aliases = model["routing_aliases"]
    require(len(aliases) == 18, "routing alias count drift")

    forbidden_generic = {
        "maintenance",
        "calibration",
        "inspection",
        "kpi",
        "mtbf",
        "mttr",
        "operations",
        "운영",
        "정비",
        "교정",
        "점검",
        "예비품",
    }
    normalized = {normalize(alias) for alias in aliases}
    require(
        not (normalized & forbidden_generic),
        f"generic routing alias introduced: {normalized & forbidden_generic}",
    )

    require(
        any("operations maintenance" in alias.casefold() for alias in aliases),
        "O&M management alias coverage missing",
    )
    require(
        any("spare" in alias.casefold() for alias in aliases),
        "spares-management alias coverage missing",
    )
    require(
        any("mtbf" in alias.casefold() and "mttr" in alias.casefold() for alias in aliases),
        "maintenance-KPI alias coverage missing",
    )

    # 13. Human-readable ownership handoffs.
    human_text = readme + "\n" + sheet
    for handoff in (
        "smart_positioner_diagnostics_valve_signature_predictive_maintenance",
        "configuration_change_release_backup_rollback_migration_obsolescence_management",
        "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
        "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability",
    ):
        require(handoff in human_text, f"ownership handoff missing: {handoff}")

    # 14. Historical-frequency prohibition and no placeholder residue.
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
        "historical-frequency policy not documented",
    )
    for forbidden in ("TODO", "TBD", "FIXME", "PLACEHOLDER"):
        require(forbidden not in all_text, f"placeholder residue: {forbidden}")

    print("PASS: control-system O&M management focused regression")
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
