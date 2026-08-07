#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

TOPIC_ID = "industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread"
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

    # 2. Exact 29-anchor ownership.
    anchors = fact["anchors"]
    require(len(anchors) == 29, "anchor count must remain 29")
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
        "iiot_smart_factory_scope",
        "iiot_layered_architecture_device_edge_platform_cloud",
        "iiot_ot_control_boundary",
        "iiot_protocol_connectivity_handoff",
        "iiot_edge_gateway_functions",
        "iiot_workload_placement_latency_bandwidth_cost",
        "iiot_offline_degraded_mode",
        "iiot_data_contract_timestamp_quality_context",
        "iiot_historian_mes_data_handoff",
        "iiot_syntactic_semantic_interoperability",
        "iiot_information_model_asset_relationship",
        "iiot_asset_namespace_identifier",
        "iiot_asset_model_version_lifecycle",
        "iiot_aas_open_model_optional",
        "iiot_digital_thread_definition",
        "iiot_digital_thread_traceability_links",
        "iiot_digital_twin_handoff",
        "iiot_api_event_interface_contract",
        "iiot_edge_device_onboarding_identity",
        "iiot_device_edge_fleet_management",
        "iiot_remote_update_rollback",
        "iiot_observability_logs_metrics_traces",
        "iiot_security_zero_trust_least_privilege",
        "iiot_data_privacy_residency_governance",
        "iiot_scalability_capacity_multi_site",
        "iiot_availability_resilience_rto_rpo",
        "iiot_value_use_case_kpi_architecture",
        "iiot_incremental_brownfield_migration",
        "iiot_lifecycle_governance_pdca",
    }
    require(set(anchor_ids) == expected_anchor_ids, "anchor set drift")
    by_id = {row["id"]: row for row in anchors}

    # 3. IIoT / Smart Factory scope and layered architecture.
    require(
        has_all(
            row_surface(by_id["iiot_smart_factory_scope"]),
            (
                ("iiot", "산업 iot"),
                ("smart factory", "스마트공장"),
                ("edge",),
                ("cloud",),
                ("asset", "자산"),
            ),
        ),
        "IIoT/Smart Factory scope weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_layered_architecture_device_edge_platform_cloud"]),
            (
                ("device",),
                ("edge",),
                ("platform",),
                ("cloud",),
                ("책임", "responsibility"),
            ),
        ),
        "layered Device/Edge/Platform/Cloud architecture weak",
    )

    # 4. OT control boundary.
    require(
        has_all(
            row_surface(by_id["iiot_ot_control_boundary"]),
            (
                ("실시간 제어", "real time control"),
                ("interlock",),
                ("sis",),
                ("cloud",),
                ("ot",),
            ),
        ),
        "OT control boundary weak",
    )

    # 5. Communication handoff and Edge functions.
    protocol_surface = row_surface(by_id["iiot_protocol_connectivity_handoff"])
    require(
        has_all(
            protocol_surface,
            (
                ("fieldbus",),
                ("industrial ethernet",),
                ("wireless",),
                ("gateway",),
                ("handoff", "소유"),
            ),
        ),
        "communication handoff weak",
    )
    require(
        "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection"
        in by_id["iiot_protocol_connectivity_handoff"]["statement"],
        "communication Topic ID handoff missing",
    )

    require(
        has_all(
            row_surface(by_id["iiot_edge_gateway_functions"]),
            (
                ("buffer",),
                ("filter",),
                ("store-and-forward", "store and forward"),
                ("local", "현장"),
            ),
        ),
        "Edge/Gateway function set weak",
    )

    # 6. Workload placement and offline/degraded operation.
    require(
        has_all(
            row_surface(by_id["iiot_workload_placement_latency_bandwidth_cost"]),
            (
                ("workload placement",),
                ("latency",),
                ("bandwidth",),
                ("compute",),
                ("cost", "비용"),
            ),
        ),
        "workload placement trade-off weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_offline_degraded_mode"]),
            (
                ("offline", "단절"),
                ("degraded",),
                ("buffer",),
                ("backlog",),
                ("resynchronization", "재동기화"),
            ),
        ),
        "offline/degraded recovery weak",
    )

    # 7. Data contract and Historian/MES handoff.
    require(
        has_all(
            row_surface(by_id["iiot_data_contract_timestamp_quality_context"]),
            (
                ("unit",),
                ("timestamp",),
                ("quality",),
                ("context",),
                ("schema version",),
            ),
        ),
        "IIoT data contract weak",
    )
    historian_handoff = by_id["iiot_historian_mes_data_handoff"]["statement"]
    require(
        "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing"
        in historian_handoff,
        "Historian/MES Topic ID handoff missing",
    )
    require(
        has_all(
            row_surface(by_id["iiot_historian_mes_data_handoff"]),
            (
                ("historian",),
                ("mes",),
                ("erp",),
                ("data governance",),
            ),
        ),
        "Historian/MES boundary weak",
    )

    # 8. Interoperability / information model / asset identity.
    require(
        has_all(
            row_surface(by_id["iiot_syntactic_semantic_interoperability"]),
            (
                ("connectivity",),
                ("syntactic",),
                ("semantic interoperability",),
                ("protocol",),
            ),
        ),
        "syntactic/semantic interoperability boundary weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_information_model_asset_relationship"]),
            (
                ("information model",),
                ("asset",),
                ("property",),
                ("relationship",),
                ("semantic",),
            ),
        ),
        "information-model semantics weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_asset_namespace_identifier"]),
            (
                ("asset hierarchy",),
                ("namespace",),
                ("identifier",),
                ("mapping", "연결"),
            ),
        ),
        "asset namespace/identifier weak",
    )

    # 9. Asset model / AAS.
    require(
        has_all(
            row_surface(by_id["iiot_asset_model_version_lifecycle"]),
            (
                ("asset model",),
                ("schema",),
                ("firmware",),
                ("configuration",),
                ("revision",),
            ),
        ),
        "asset-model lifecycle versioning weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_aas_open_model_optional"]),
            (
                ("asset administration shell", "aas"),
                ("submodel",),
                ("interoperability",),
            ),
        ),
        "AAS optional standardization example weak",
    )

    # 10. Digital Thread and Digital Twin boundary.
    require(
        has_all(
            row_surface(by_id["iiot_digital_thread_definition"]),
            (
                ("digital thread",),
                ("lifecycle",),
                ("identifier",),
                ("configuration",),
                ("traceability",),
            ),
        ),
        "Digital Thread definition weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_digital_thread_traceability_links"]),
            (
                ("p&id",),
                ("datasheet",),
                ("vendor",),
                ("configuration",),
                ("operational event", "운전"),
            ),
        ),
        "Digital Thread traceability links weak",
    )
    twin_handoff = by_id["iiot_digital_twin_handoff"]["statement"]
    require(
        "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control"
        in twin_handoff,
        "Digital Twin Topic ID handoff missing",
    )
    require(
        has_all(
            row_surface(by_id["iiot_digital_twin_handoff"]),
            (
                ("digital thread",),
                ("digital twin",),
                ("fidelity",),
                ("synchronization",),
            ),
        ),
        "Digital Thread / Digital Twin boundary weak",
    )

    # 11. API/event contract.
    require(
        has_all(
            row_surface(by_id["iiot_api_event_interface_contract"]),
            (
                ("api",),
                ("schema",),
                ("version",),
                ("idempotency",),
                ("retry",),
            ),
        ),
        "API/event interface contract weak",
    )

    # 12. Device onboarding / fleet / update / observability.
    require(
        has_all(
            row_surface(by_id["iiot_edge_device_onboarding_identity"]),
            (
                ("device onboarding",),
                ("identity",),
                ("credential",),
                ("certificate",),
                ("baseline",),
            ),
        ),
        "device onboarding weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_device_edge_fleet_management"]),
            (
                ("fleet",),
                ("health",),
                ("firmware",),
                ("certificate",),
                ("rolling",),
            ),
        ),
        "fleet-management weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_remote_update_rollback"]),
            (
                ("remote update", "원격"),
                ("integrity",),
                ("rollout",),
                ("rollback",),
            ),
        ),
        "remote-update/rollback weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_observability_logs_metrics_traces"]),
            (
                ("metrics",),
                ("log",),
                ("event",),
                ("trace",),
                ("correlation",),
            ),
        ),
        "observability weak",
    )

    # 13. Security / governance / scalability / resilience.
    require(
        has_all(
            row_surface(by_id["iiot_security_zero_trust_least_privilege"]),
            (
                ("identity",),
                ("authentication",),
                ("least privilege",),
                ("segmentation",),
                ("certificate",),
            ),
        ),
        "IIoT security contract weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_data_privacy_residency_governance"]),
            (
                ("privacy",),
                ("data residency",),
                ("retention",),
                ("export",),
            ),
        ),
        "privacy/residency governance weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_scalability_capacity_multi_site"]),
            (
                ("device",),
                ("message rate",),
                ("storage",),
                ("multi-site", "multi site"),
                ("cost", "비용"),
            ),
        ),
        "scalability/capacity weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_availability_resilience_rto_rpo"]),
            (
                ("failover",),
                ("backup",),
                ("rto",),
                ("rpo",),
                ("ot",),
            ),
        ),
        "availability/resilience weak",
    )

    # 14. Use-case value / brownfield / lifecycle governance.
    require(
        has_all(
            row_surface(by_id["iiot_value_use_case_kpi_architecture"]),
            (
                ("use case",),
                ("kpi",),
                ("traceability",),
                ("downtime",),
                ("energy",),
            ),
        ),
        "use-case/KPI architecture weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_incremental_brownfield_migration"]),
            (
                ("brownfield",),
                ("legacy",),
                ("pilot",),
                ("migration",),
                ("rollback",),
            ),
        ),
        "brownfield migration weak",
    )
    require(
        has_all(
            row_surface(by_id["iiot_lifecycle_governance_pdca"]),
            (
                ("lifecycle",),
                ("asset model",),
                ("schema",),
                ("security",),
                ("technical debt",),
            ),
        ),
        "lifecycle governance weak",
    )

    # 15. Fatal contract: exact IDs/order and C-only ownership.
    fatal = fact["fatal_wrong_claims"]
    require(len(fatal) == 14, "fatal count must remain 14")
    expected_fatal_ids = [
        "iiot_fatal_internet_connection_equals_smart_factory",
        "iiot_fatal_cloud_replaces_ot_control",
        "iiot_fatal_edge_is_protocol_converter_only",
        "iiot_fatal_all_workloads_cloud",
        "iiot_fatal_protocol_equals_semantic_interop",
        "iiot_fatal_tag_name_is_information_model",
        "iiot_fatal_digital_thread_is_cloud_trend",
        "iiot_fatal_digital_thread_equals_digital_twin",
        "iiot_fatal_offline_auto_recovers",
        "iiot_fatal_untrusted_device_auto_onboard",
        "iiot_fatal_mass_update_without_rollback",
        "iiot_fatal_cloud_removes_capacity_planning",
        "iiot_fatal_platform_ha_replaces_local_safety",
        "iiot_fatal_adjacent_topics_owned_all",
    ]
    require([row["id"] for row in fatal] == expected_fatal_ids, "fatal ID/order drift")
    require(all(row["severity"] == "fatal" for row in fatal), "fatal severity drift")
    require(
        all(row["affected_layers"] == ["C"] for row in fatal),
        "fatal affected_layers must remain C-only",
    )

    # 16. LLM-only semantic contract.
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

    # 17. Model references and complete outline coverage.
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
    require(outline_union == anchor_set, "outline does not cover all 29 anchors")

    # 18. Routing aliases are specific multi-concept phrases.
    aliases = model["routing_aliases"]
    require(len(aliases) == 18, "routing alias count drift")

    forbidden_generic = {
        "iiot",
        "smart factory",
        "edge",
        "cloud",
        "interoperability",
        "digital thread",
        "스마트공장",
        "스마트 팩토리",
        "엣지",
        "클라우드",
        "상호운용성",
        "디지털 스레드",
    }
    normalized_aliases = {norm(alias) for alias in aliases}
    require(
        not (normalized_aliases & forbidden_generic),
        f"generic alias introduced: {normalized_aliases & forbidden_generic}",
    )
    require(
        any(
            "edge" in a.casefold()
            and "cloud" in a.casefold()
            and ("iiot" in a.casefold() or "smart" in a.casefold())
            for a in aliases
        ),
        "IIoT Edge/Cloud alias coverage missing",
    )
    require(
        any(
            ("digital thread" in a.casefold() or "디지털 스레드" in a)
            and ("asset" in a.casefold() or "자산" in a)
            for a in aliases
        ),
        "Digital Thread/Asset alias coverage missing",
    )
    require(
        any(
            ("information model" in a.casefold() or "정보모델" in a)
            and ("interoperability" in a.casefold() or "상호운용" in a)
            for a in aliases
        ),
        "information-model/interoperability alias coverage missing",
    )

    # 19. Human-readable adjacent ownership handoffs.
    human_text = readme + "\n" + sheet
    for handoff in (
        "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing",
        "industrial_wired_wireless_communication_fieldbus_ethernet_interoperability_selection",
        "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control",
        "instrumentation_production_management_planning_quality_cost_resources",
    ):
        require(handoff in human_text, f"ownership handoff missing: {handoff}")

    # 20. Historical-frequency prohibition and no placeholder residue.
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

    print("PASS: industrial IIoT smart factory focused regression")
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
