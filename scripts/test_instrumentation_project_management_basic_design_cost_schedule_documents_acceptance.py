#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "instrumentation_project_management_basic_design_cost_schedule_documents_acceptance"
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


def normalized(text: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", " ", text.casefold()).strip()


def contains_all(text: str, tokens: tuple[str, ...]) -> bool:
    low = text.casefold()
    return all(token.casefold() in low for token in tokens)


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

    expected_anchor_ids = {
        "project_lifecycle_stage_gate",
        "project_scope_boundary_interface",
        "project_design_basis_requirements",
        "project_wbs_responsibility_raci",
        "project_schedule_milestone_dependency_critical_path",
        "project_progress_measurement_forecast",
        "project_cost_estimate_basis_quantity_rate_contingency",
        "project_cost_baseline_commitment_actual_forecast",
        "project_risk_register_mitigation",
        "project_change_control_scope_cost_schedule",
        "project_document_control_revision_transmittal",
        "project_master_deliverable_register",
        "instrument_index_master_tag_register",
        "instrument_datasheet_process_mechanical_interface",
        "instrument_document_set_loop_hookup_cable_jb",
        "io_list_software_project_handoff",
        "instrument_quantity_mto_boq",
        "procurement_requisition_rfq_tbe_po",
        "vendor_document_review_integration",
        "vendor_inspection_acceptance_handoff",
        "construction_installation_readiness",
        "construction_qa_qc_itp_hold_witness",
        "mechanical_completion_punch_systemization",
        "precommissioning_loop_readiness_handoff",
        "project_acceptance_criteria_evidence",
        "asbuilt_handover_document_dossier",
        "operations_maintenance_handover_boundary",
        "project_closeout_lessons_learned",
    }
    require(set(anchor_ids) == expected_anchor_ids, "anchor set drift")
    by_id = {row["id"]: row for row in anchors}

    # 3. Lifecycle / scope / design-basis mechanics.
    require(
        contains_all(
            by_id["project_lifecycle_stage_gate"]["statement"],
            ("기본설계", "상세설계", "조달", "시공", "인수"),
        ),
        "project lifecycle chain incomplete",
    )
    require(
        contains_all(
            by_id["project_scope_boundary_interface"]["statement"],
            ("scope", "battery limit", "interface", "acceptance"),
        ),
        "scope/interface boundary weak",
    )
    require(
        contains_all(
            by_id["project_design_basis_requirements"]["statement"],
            ("PFD", "P&ID", "Control Philosophy", "Design Basis"),
        ),
        "design-basis input chain weak",
    )

    # 4. WBS / schedule / progress / risk.
    require(
        contains_all(
            by_id["project_wbs_responsibility_raci"]["statement"],
            ("WBS", "work package", "RACI"),
        ),
        "WBS/RACI mechanism weak",
    )
    require(
        contains_all(
            by_id["project_schedule_milestone_dependency_critical_path"]["statement"],
            ("milestone", "critical path", "장기납기"),
        ),
        "schedule dependency/critical-path mechanism weak",
    )
    require(
        contains_all(
            by_id["project_progress_measurement_forecast"]["statement"],
            ("milestone", "forecast"),
        ),
        "progress/forecast mechanism weak",
    )
    require(
        contains_all(
            by_id["project_risk_register_mitigation"]["statement"],
            ("Risk Register", "owner", "mitigation", "residual"),
        ),
        "risk register mechanism weak",
    )

    # 5. Cost / change.
    require(
        contains_all(
            by_id["project_cost_estimate_basis_quantity_rate_contingency"]["statement"],
            ("Cost Estimate", "basis", "수량", "단가", "contingency"),
        ),
        "cost-estimate basis weak",
    )
    require(
        contains_all(
            by_id["project_cost_baseline_commitment_actual_forecast"]["statement"],
            ("Budget Baseline", "commitment", "actual", "Estimate to Complete"),
        ),
        "cost-control forecast mechanism weak",
    )
    require(
        contains_all(
            by_id["project_change_control_scope_cost_schedule"]["statement"],
            ("영향분석", "cost", "schedule", "document", "acceptance"),
        ),
        "integrated change-control mechanism weak",
    )

    # 6. Document and instrumentation deliverables.
    require(
        contains_all(
            by_id["project_document_control_revision_transmittal"]["statement"],
            ("revision", "status", "transmittal", "superseded"),
        ),
        "document-control mechanism weak",
    )
    require(
        contains_all(
            by_id["project_master_deliverable_register"]["statement"],
            ("Master Deliverable Register", "revision", "review status"),
        ),
        "MDR mechanism weak",
    )
    require(
        contains_all(
            by_id["instrument_index_master_tag_register"]["statement"],
            ("Instrument Index", "Tag", "P&ID"),
        ),
        "Instrument Index ownership weak",
    )
    require(
        contains_all(
            by_id["instrument_datasheet_process_mechanical_interface"]["statement"],
            ("Instrument Datasheet", "process condition", "vendor"),
        ),
        "instrument datasheet mechanism weak",
    )

    docset = by_id["instrument_document_set_loop_hookup_cable_jb"]["statement"]
    for token in ("Loop Diagram", "Hook-up", "Cable Schedule", "Junction Box"):
        require(token.casefold() in docset.casefold(), f"deliverable missing: {token}")

    require(
        contains_all(
            by_id["instrument_quantity_mto_boq"]["statement"],
            ("MTO", "BOQ", "수량", "procurement"),
        ),
        "MTO/BOQ linkage weak",
    )

    # 7. Explicit software-project ownership handoff.
    io_handoff = by_id["io_list_software_project_handoff"]["statement"]
    require(
        contains_all(io_handoff, ("I/O List", "URS", "FRS", "FDS", "SDS")),
        "I/O/software-design boundary weak",
    )
    require(
        "handoff" in io_handoff.casefold(),
        "software-project handoff wording missing",
    )

    vendor_handoff = by_id["vendor_inspection_acceptance_handoff"]["statement"]
    require(
        contains_all(vendor_handoff, ("vendor inspection", "software", "FAT")),
        "vendor-inspection/software-FAT boundary weak",
    )

    precom_handoff = by_id["precommissioning_loop_readiness_handoff"]["statement"]
    require(
        contains_all(precom_handoff, ("Precommissioning", "SAT", "site integration")),
        "precommissioning/software-SAT boundary weak",
    )

    # 8. Procurement / vendor.
    require(
        contains_all(
            by_id["procurement_requisition_rfq_tbe_po"]["statement"],
            ("Requisition", "RFQ", "Vendor Bid", "PO"),
        ),
        "procurement chain weak",
    )
    require(
        contains_all(
            by_id["vendor_document_review_integration"]["statement"],
            ("Vendor Document", "certified drawing", "project"),
        ),
        "vendor-document integration weak",
    )

    # 9. Construction / QA / completion.
    require(
        contains_all(
            by_id["construction_installation_readiness"]["statement"],
            ("approved-for-construction", "readiness", "설치"),
        ),
        "construction readiness weak",
    )
    require(
        contains_all(
            by_id["construction_qa_qc_itp_hold_witness"]["statement"],
            ("ITP", "hold", "witness", "acceptance"),
        ),
        "QA/QC ITP mechanism weak",
    )
    require(
        contains_all(
            by_id["mechanical_completion_punch_systemization"]["statement"],
            ("Mechanical Completion", "punch", "closeout"),
        ),
        "mechanical-completion mechanism weak",
    )

    # 10. Acceptance / handover / O&M boundary.
    require(
        contains_all(
            by_id["project_acceptance_criteria_evidence"]["statement"],
            ("Project Acceptance", "acceptance criteria", "evidence", "punch"),
        ),
        "acceptance criteria/evidence weak",
    )
    require(
        contains_all(
            by_id["asbuilt_handover_document_dossier"]["statement"],
            ("As-Built", "Handover Dossier", "vendor"),
        ),
        "as-built handover weak",
    )
    om_handoff = by_id["operations_maintenance_handover_boundary"]["statement"]
    require(
        contains_all(om_handoff, ("training", "warranty", "CMMS", "KPI")),
        "post-handover O&M boundary weak",
    )

    # 11. Fatal contract: exact IDs/order and semantic projection.
    fatal = fact["fatal_wrong_claims"]
    require(len(fatal) == 14, "fatal count must remain 14")
    fatal_ids = [row["id"] for row in fatal]
    expected_fatal_ids = [
        "project_fatal_scope_is_equipment_list_only",
        "project_fatal_design_without_basis",
        "project_fatal_no_dependency_schedule",
        "project_fatal_actual_cost_below_budget_means_safe",
        "project_fatal_change_without_impact_approval",
        "project_fatal_uncontrolled_document_revision",
        "project_fatal_instrument_index_independent",
        "project_fatal_lowest_bid_without_technical_review",
        "project_fatal_vendor_document_not_integrated",
        "project_fatal_install_before_afc_readiness",
        "project_fatal_mechanical_completion_equals_installed",
        "project_fatal_acceptance_is_single_successful_run",
        "project_fatal_io_list_replaces_software_design",
        "project_fatal_handover_without_asbuilt",
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

    # 12. LLM-only logic contract.
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
        len(profile["false_positive_cautions"]) == 14,
        "false-positive caution count drift",
    )

    # 13. Model references and complete outline coverage.
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

    # 14. Routing aliases are specific, not generic.
    aliases = model["routing_aliases"]
    require(len(aliases) == 18, "routing alias count drift")

    forbidden_generic = {
        "project",
        "project management",
        "basic design",
        "cost",
        "schedule",
        "acceptance",
        "instrumentation",
        "프로젝트",
        "프로젝트 관리",
        "기본설계",
        "원가",
        "비용",
        "일정",
        "인수",
        "계측",
        "계장",
    }
    normalized_aliases = {normalized(alias) for alias in aliases}
    require(
        not (normalized_aliases & forbidden_generic),
        f"generic alias introduced: {normalized_aliases & forbidden_generic}",
    )
    require(
        any("cost" in a.casefold() and "schedule" in a.casefold() for a in aliases),
        "cost/schedule alias coverage missing",
    )
    require(
        any("procurement" in a.casefold() or "조달" in a for a in aliases),
        "procurement alias coverage missing",
    )
    require(
        any("handover" in a.casefold() or "인수" in a for a in aliases),
        "handover/acceptance alias coverage missing",
    )

    # 15. Human-readable ownership handoffs.
    human_text = readme + "\n" + sheet
    for handoff in (
        "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
        "control_system_operations_maintenance_calibration_inspection_spares_kpi",
        "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative",
    ):
        require(handoff in human_text, f"ownership handoff missing: {handoff}")

    # 16. Historical-frequency policy and no placeholder residue.
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

    print("PASS: instrumentation project management focused regression")
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
