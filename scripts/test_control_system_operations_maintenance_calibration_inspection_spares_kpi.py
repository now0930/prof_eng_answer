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

    asset_register = by_id["om_asset_register_system_boundary"]["statement"]
    require("기능과 물리적 위치" in asset_register and "taxonomy" in asset_register,
            "asset identification/taxonomy contract incomplete")
    require("완전한 asset-register 필드 목록을 정하지 않는다" in asset_register,
            "ISO 14224 scope must not be expanded to universal asset-register fields")

    # 3. Core O&M lifecycle mechanisms.
    strategy = by_id[
        "maintenance_strategy_corrective_preventive_condition_predictive"
    ]["statement"]
    for token in ("Corrective", "Preventive", "Condition-Based", "Predictive"):
        require(token in strategy, f"maintenance strategy token missing: {token}")

    criticality = by_id["maintenance_criticality_risk_prioritization"]["statement"]
    require(
        "가능성" in criticality and "결과·영향" in criticality and "의사결정 기준" in criticality,
        "criticality likelihood/consequence/criteria boundary incomplete",
    )
    require("공통인 영향요소 목록이나 가중치" in criticality,
            "criticality criteria must not imply a universal factor list")

    work_order = by_id["work_order_history_closed_loop"]["statement"]
    require(
        "Work Order" in work_order and "downtime" in work_order,
        "ISO 14224 maintenance/failure data categories missing",
    )
    require("모든 사업장의" in work_order and "보편적으로 정하지 않는다" in work_order,
            "site-specific work-order boundary missing")

    # 4. Calibration management boundary.
    cal_program = by_id["calibration_program_traceability"]["statement"]
    for token in ("측정결과", "불확도", "추적성", "용도 적합성"):
        require(token in cal_program, f"calibration traceability token missing: {token}")
    require("보편 주기를 지정하지 않는다" in cal_program,
            "calibration interval must not imply a universal NIST interval")

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
    for token in ("HSE Offshore", "offshore SIS", "위험평가", "예상 연기기간", "누적위험", "법적 보편요건"):
        require(token in deferred, f"scoped deferral-management claim missing: {token}")
    require(
        deferred in logic["llm_profile"]["truth_schema"]
        and deferred in logic["llm_profile"]["safe_conditions"],
        "scoped deferral fact not mirrored in logic profile",
    )

    # 6. Spare-parts lifecycle.
    spare_critical = by_id["spares_criticality_classification"]["statement"]
    for token in ("Critical Spare", "중요 자산", "lead time", "보편 분류 알고리즘"):
        require(token in spare_critical, f"critical spare token missing: {token}")

    spare_stock = by_id["spares_stock_policy_reorder_leadtime"]["statement"]
    require("reorder point" in spare_stock.casefold(), "reorder-point policy missing")

    spare_preservation = by_id["spares_preservation_shelf_life_rotation"]["statement"]
    require("shelf-life" in spare_preservation.casefold(), "shelf-life management missing")

    obsolescence = by_id["spares_obsolescence_substitution_moc"]["statement"]
    require(
        "Last Time Buy" in obsolescence and "구성변경 통제" in obsolescence,
        "obsolescence/MOC handoff missing",
    )

    # 7. KPI definitions and formula boundary.
    mtbf = by_id["kpi_mtbf_definition_boundary"]["statement"]
    require("MTBF" in mtbf and "고장횟수" in mtbf, "MTBF definition weak")

    mttr = by_id["kpi_mttr_definition_boundary"]["statement"]
    for token in ("ISO 14224:2016", "ISO/TR 12489", "MTTR", "MTTRes", "시작·종료 경계"):
        require(token in mttr, f"MTTR/MTTRes boundary missing: {token}")
    require(
        mttr in logic["llm_profile"]["truth_schema"]
        and mttr in logic["llm_profile"]["safe_conditions"],
        "MTTR/MTTRes fact not mirrored in logic profile",
    )

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
    require("단일 성과지표" in gaming and "균형" in gaming and "정비 KPI" in gaming,
            "KPI gaming claim scope/balance boundary weak")

    # 8. Data/governance/continuous improvement.
    data = by_id["maintenance_data_quality_cmms_taxonomy"]["statement"]
    require("ISO 14224:2016" in data and "고장 원인·결과" in data and "downtime" in data,
            "standardized reliability-maintenance data categories missing")
    require("CMMS/EAM 사용" in data and "보장하지 않는다" in data,
            "standard scope and analysis-guarantee boundary missing")

    roles = by_id["maintenance_roles_competence_permit_restoration"]["statement"]
    for token in ("29 CFR 1910.147", "격리 상태", "1910.119", "SIS bypass", "뜻하지 않는다"):
        require(token in roles, f"scoped LOTO/restoration claim missing: {token}")
    role_truth = logic["llm_profile"]["truth_schema"]
    role_safe = logic["llm_profile"]["safe_conditions"]
    require(roles in role_truth and roles in role_safe, "scoped maintenance fact not mirrored in logic profile")

    inspection_finding = by_id["inspection_findings_defect_priority_closeout"]["statement"]
    for token in ("29 CFR 1910.119", "허용한계", "추가 사용 전에", "정하지 않는다"):
        require(token in inspection_finding, f"scoped inspection-deficiency claim missing: {token}")
    require(
        inspection_finding in logic["llm_profile"]["truth_schema"]
        and inspection_finding in logic["llm_profile"]["safe_conditions"],
        "scoped inspection deficiency fact not mirrored in logic profile",
    )

    failure_data = by_id["failure_coding_rca_bad_actor_feedback"]["statement"]
    for token in ("ISO 14224:2016", "failure data", "failure mode", "Bad Actor", "RCA", "사업장·프로그램별"):
        require(token in failure_data, f"scoped failure-data claim missing: {token}")
    require(
        failure_data in logic["llm_profile"]["truth_schema"]
        and failure_data in logic["llm_profile"]["safe_conditions"],
        "scoped failure-data fact not mirrored in logic profile",
    )

    change = by_id["maintenance_configuration_backup_change_handoff"]["statement"]
    require("NIST SP 800-82 Rev. 3" in change and "NIST SP 1339" in change,
            "current OT configuration/backup source basis missing")
    require("모든 정비작업 전후" in change and "조직 및 시스템별로 정한다" in change,
            "universal maintenance workflow boundary missing")

    pdca = by_id["om_continuous_improvement_pdca_lifecycle_cost"]["statement"]
    require(
        "ISO 55001:2024" in pdca and "ISO 55000:2024" in pdca,
        "current asset-management standard basis missing",
    )
    require("모든 조직에 동일하게 처방하지 않는다" in pdca,
            "organization-specific review loop boundary missing")

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
