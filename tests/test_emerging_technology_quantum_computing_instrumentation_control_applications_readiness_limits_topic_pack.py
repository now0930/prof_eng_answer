from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = (
    "emerging_technology_quantum_computing_"
    "instrumentation_control_applications_readiness_limits"
)
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load_json(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def test_topic_pack_schema_identity_and_classification_contract() -> None:
    fact = load_json("fact_anchor.json")
    logic = load_json("logic_check.json")
    model = load_json("model_answer.json")
    importance = load_json("topic_importance.json")

    assert fact["schema_version"] == "topic_pack.fact_anchor.v1"
    assert logic["schema_version"] == "topic_pack.logic_check.v1"
    assert model["schema_version"] == "topic_pack.model_answer.v1"
    assert importance["schema_version"] == "topic_pack.topic_importance.v1"

    for obj in (fact, logic, model, importance):
        assert obj["topic_id"] == TOPIC_ID

    assert fact["question_type_hint"] == "IMPLEMENTATION_EVALUATION"
    assert model["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert importance["question_type"] == "IMPLEMENTATION_EVALUATION"
    assert importance["difficulty"] == "DESIGN_EVALUATION"
    assert importance["selection_importance"] == "HIGH"


def test_fact_anchor_counts_ids_and_projection_contract() -> None:
    fact = load_json("fact_anchor.json")

    anchors = fact["anchors"]
    fatals = fact["fatal_wrong_claims"]

    assert len(anchors) == 27
    assert len(fatals) == 14
    assert len(fact["safe_expressions"]) == 18

    ids = [row["id"] for row in anchors]
    assert len(ids) == len(set(ids))
    assert [row["anchor_id"] for row in anchors] == ids

    assert fact["core_facts"] == [row["statement"] for row in anchors]

    fatal_ids = [row["id"] for row in fatals]
    assert len(fatal_ids) == len(set(fatal_ids))
    assert all(row["severity"] == "fatal" for row in fatals)
    assert all(row["affected_layers"] == ["C"] for row in fatals)


def test_quantum_principle_chain_is_covered_without_universal_speedup() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    required = {
        "etc_quantum_computing_definition",
        "etc_qubit_vs_classical_bit",
        "etc_superposition_role",
        "etc_measurement_readout",
        "etc_entanglement_role",
        "etc_interference_role",
    }
    assert required <= set(by_id)

    text = " ".join(by_id[row]["statement"] for row in required).casefold()
    for term in (
        "qubit",
        "superposition",
        "measurement",
        "entanglement",
        "interference",
    ):
        assert term in text

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "quantum_universal_speedup" in fatal_ids
    assert "qubit_directly_reads_zero_and_one" in fatal_ids
    assert "measurement_reads_all_amplitudes" in fatal_ids
    assert "entanglement_faster_than_light" in fatal_ids


def test_gate_annealing_and_hybrid_architecture_are_separate_axes() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    gate = by_id["etc_gate_model"]["statement"].casefold()
    annealing = by_id["etc_annealing_boundary"]["statement"].casefold()
    hybrid = by_id["etc_hybrid_quantum_classical"]["statement"].casefold()

    assert "gate" in gate
    assert "annealing" in annealing
    assert "최적화" in annealing or "optimization" in annealing
    assert "hybrid" in hybrid
    assert "classical" in hybrid

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "annealing_equals_gate" in fatal_ids


def test_industrial_use_cases_require_problem_fit_and_classical_baseline() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    assert "classical baseline" in by_id["etc_problem_fit_first"]["statement"].casefold()
    optimization_statement = by_id["etc_optimization_candidate"]["statement"].casefold()
    assert "최적화" in optimization_statement or "optimization" in optimization_statement
    assert "estimation" in by_id["etc_estimation_candidate"]["statement"].casefold()
    baseline_statement = by_id["etc_classical_baseline_benchmark"]["statement"].casefold()
    assert "classical" in baseline_statement
    assert "accuracy" in baseline_statement
    assert "runtime" in baseline_statement
    assert "robustness" in baseline_statement
    assert "비교" in baseline_statement

    model = load_json("model_answer.json")
    patterns = " ".join(
        row["pattern"] + " " + row["intent"]
        for row in model["expected_question_patterns"]
    ).casefold()

    assert "최적화" in patterns
    assert "classical baseline" in patterns


def test_input_output_noise_and_error_limits_are_end_to_end() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    required = {
        "etc_data_encoding_bottleneck",
        "etc_output_sampling_bottleneck",
        "etc_noise_decoherence",
        "etc_error_mitigation_correction_boundary",
        "etc_scale_quality_tradeoff",
    }
    assert required <= set(by_id)

    text = " ".join(by_id[row]["statement"] for row in required).casefold()

    for term in (
        "encoding",
        "sampling",
        "decoherence",
        "error mitigation",
        "error correction",
    ):
        assert term in text

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "data_loading_free" in fatal_ids
    assert "single_run_exact_output" in fatal_ids
    assert "mitigation_equals_fault_tolerance" in fatal_ids


def test_latency_determinism_preserve_plc_dcs_sis_ownership() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    latency = by_id["etc_latency_determinism"]["statement"].casefold()
    boundary = by_id["etc_plc_dcs_boundary"]["statement"].casefold()
    supervisory = by_id["etc_offline_supervisory_boundary"]["statement"].casefold()

    assert "latency" in latency
    assert "determinism" in latency
    for term in ("plc", "dcs", "sis"):
        assert term in boundary
    assert "hard real-time" in supervisory

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "quantum_replaces_plc_dcs" in fatal_ids


def test_quantum_sensing_is_adjacent_not_identical() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    statement = by_id["etc_quantum_sensing_boundary"]["statement"].casefold()
    assert "quantum sensing" in statement
    assert "quantum computing" in statement
    assert "동일" in statement

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "quantum_sensing_equals_computing" in fatal_ids


def test_readiness_pilot_tco_and_governance_form_adoption_chain() -> None:
    fact = load_json("fact_anchor.json")
    by_id = {row["id"]: row for row in fact["anchors"]}

    required = {
        "etc_readiness_maturity",
        "etc_classical_baseline_benchmark",
        "etc_pilot_verification",
        "etc_tco_skills_integration",
        "etc_security_governance",
    }
    assert required <= set(by_id)

    text = " ".join(by_id[row]["statement"] for row in required).casefold()

    for term in (
        "readiness",
        "classical",
        "pilot",
        "tco",
        "auditability",
    ):
        assert term in text

    fatal_ids = {row["id"] for row in fact["fatal_wrong_claims"]}
    assert "research_equals_production_ready" in fatal_ids
    assert "vendor_benchmark_proves_roi" in fatal_ids


def test_llm_only_semantics_do_not_directly_apply_score() -> None:
    logic = load_json("logic_check.json")

    deterministic = logic["deterministic_checks"]
    profile = logic["llm_profile"]

    assert deterministic["enabled"] is False
    assert deterministic["fatal_checks"] == []
    assert deterministic["major_checks"] == []
    assert deterministic["question_type_checks"] == []

    assert profile["enabled"] is True
    assert profile["candidate_extraction"]["rules"] == []
    assert profile["score_policy"] == {
        "direct_score_application": False,
        "direct_d_e_effect": "none",
        "affected_layers": ["C"],
    }

    assert len(profile["major_checks"]) == 12
    assert len(profile["false_positive_cautions"]) == 14


def test_model_answer_patterns_and_outline_reference_real_anchors() -> None:
    fact = load_json("fact_anchor.json")
    model = load_json("model_answer.json")

    anchor_ids = {row["anchor_id"] for row in fact["anchors"]}

    assert len(model["expected_question_patterns"]) == 10
    assert len(model["recommended_outline"]) == 8
    assert len(model["routing_aliases"]) == 18
    assert len(model["routing_field_points"]) == 26

    for row in model["expected_question_patterns"]:
        refs = set(row["required_anchor_ids"])
        assert refs
        assert refs <= anchor_ids

    outline_refs = {
        ref
        for row in model["recommended_outline"]
        for ref in row["anchor_refs"]
    }
    assert outline_refs == anchor_ids


def test_topic_sheet_and_readme_lock_ownership_and_dynamic_boundary() -> None:
    sheet = SHEET.read_text(encoding="utf-8")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    combined = sheet + "\n" + readme

    for owner in (
        "industrial_ai_machine_learning_anomaly_predictive_maintenance_model_lifecycle",
        "physical_ai_robot_sensor_fusion_digital_twin_autonomous_manufacturing_safety_control",
        "industrial_iot_smart_factory_edge_cloud_interoperability_digital_thread",
        "plc_dcs_scada_remote_io_architecture_redundancy_availability_reliability",
        "sis_sil_safety_software_independence_systematic_failure_verification_validation",
    ):
        assert owner in combined

    assert "IC-2027-W-5-2 / DYNAMIC_REVIEW_LANE" in combined
    assert "Historical frequency: 근거가 없어 사용하지 않음" in combined
    assert "즉시 `COVERED`로 승격하지 않는다" in combined


def _run_all_tests_directly() -> None:
    tests = sorted(
        (name, obj)
        for name, obj in globals().items()
        if name.startswith("test_") and callable(obj)
    )

    assert len(tests) == 12, len(tests)

    for name, fn in tests:
        fn()
        print(f"FOCUSED_TEST_CASE={name}|RESULT=PASS")

    print("FOCUSED_TEST_PASSED_COUNT=12")
    print("FOCUSED_TEST_RESULT=PASS")


if __name__ == "__main__":
    _run_all_tests_directly()
