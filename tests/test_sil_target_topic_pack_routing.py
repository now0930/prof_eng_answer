from __future__ import annotations

import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from model_answer_router import find_model_answer_reference
from rubric_registry import load_model_answer_bank
from semantic_router_shadow import (
    build_question_demand_aware_rule_candidates,
)


TOPIC = "sil_target_determination_risk_reduction_and_lifecycle"
HAZOP = "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
FSRM = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
SAFETY_SW = (
    "sis_sil_safety_software_independence_systematic_failure_"
    "verification_validation"
)
SOURCE = REPO / "rubrics" / "topic_packs" / TOPIC
GENERATED = REPO / "rubrics" / "generated"
QUESTION = (
    "SIL 결정 방법을 설명하고 이를 실제 플랜트 운영 및 "
    "최신 산업 이슈와 연계하여 설명하시오."
)
EXPECTED_AXES = {
    "system_scope_and_sil_role",
    "risk_scenario_and_tolerable_target",
    "existing_ipl_and_independence",
    "required_rrf_and_target_sil",
    "demand_mode_metric_selection",
    "quantitative_verification_dimension",
    "proof_test_diagnostics_reliability",
    "operations_moc_security_ai_lifecycle",
}


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def primary_topic(result: dict[str, object]) -> str:
    reference = result.get("primary_reference") or {}
    return str(reference.get("topic_id") or "")


def qd_route(question: str) -> dict[str, object]:
    return build_question_demand_aware_rule_candidates(
        question,
        {
            "status": "ok",
            "demands": [{"id": "D1", "text": question}],
        },
    )


def test_source_pack_owns_core_sil_target_flow() -> None:
    fact = load(SOURCE / "fact_anchor.json")
    anchors = {
        row["id"]: row
        for row in fact["anchors"]
    }

    assert len(anchors) == 16
    assert fact["question_type_hint"] == "IMPLEMENTATION_EVALUATION"
    assert "RRF_required = F_residual / F_tolerable" in anchors[
        "required_rrf_relation"
    ]["statement"]
    assert "F_tolerable / F_residual" in anchors[
        "target_pfd_relation"
    ]["statement"]
    assert "고장 발견 시점이 아니라" in anchors[
        "demand_mode_metric_selection"
    ]["statement"]

    fatal = {
        row["claim_signature"]
        for row in fact["fatal_wrong_claims"]
    }
    assert {
        "target_pfd_equals_frequency_product",
        "demand_mode_equals_fault_detection_timing",
        "pst_replaces_full_test_and_reduces_mttr",
        "certificate_interval_is_minimum_test_interval",
    } <= fatal


def test_issue_question_maps_to_exact_eight_required_anchors() -> None:
    model = load(SOURCE / "model_answer.json")
    pattern = next(
        row
        for row in model["expected_question_patterns"]
        if row["pattern"] == QUESTION
    )
    required = set(pattern["required_anchor_ids"])

    assert len(required) == 8
    assert required == {
        "sis_sif_sil_scope",
        "method_selection",
        "required_rrf_relation",
        "target_pfd_relation",
        "demand_mode_metric_selection",
        "achieved_sil_verification",
        "operations_moc_revalidation",
        "cyber_ai_safety_boundary",
    }


def test_generated_banks_contain_one_runtime_topic() -> None:
    manifest = load(GENERATED / "topic_pack_manifest.generated.json")
    ids = [row["topic_id"] for row in manifest["topics"]]
    assert ids.count(TOPIC) == 1

    model_bank = load(GENERATED / "model_answers.generated.json")
    entries = [
        row for row in model_bank["answers"]
        if row.get("topic_id") == TOPIC
    ]
    assert len(entries) == 1
    assert QUESTION in entries[0]["question_examples"]


def test_question_only_route_owns_generic_issue_question() -> None:
    result = qd_route(QUESTION)
    candidates = result["candidates"]

    assert candidates[0]["answer"]["topic_id"] == TOPIC
    assert result["student_answer_used"] is False
    assert result["fact_eval_used"] is False
    winner = result["question_demand_aware_candidate_result"][
        "demand_winners"
    ][0]
    assert winner["topic_id"] == TOPIC
    assert "SIL 결정 방법" in winner["discriminative_strong_phrases"]


def test_legacy_route_is_answer_independent_for_same_question() -> None:
    bank = load_model_answer_bank()
    first = find_model_answer_reference(
        QUESTION,
        "ESD valve PST final element Markov beta factor",
        bank=bank,
    )
    second = find_model_answer_reference(
        QUESTION,
        "safety software AI cybersecurity HAZOP LOPA",
        bank=bank,
    )

    assert primary_topic(first) == TOPIC
    assert primary_topic(second) == TOPIC
    assert first["candidates"][0]["answer_score"] == 0
    assert second["candidates"][0]["answer_score"] == 0


def test_narrow_neighbor_questions_keep_their_owners() -> None:
    cases = {
        HAZOP: (
            "HAZOP 결과를 LOPA scenario로 전환하고 IPL을 고려하여 "
            "목표 SIL을 결정하는 절차를 설명하시오."
        ),
        FSRM: (
            "SIF의 1oo2, 2oo3 구조와 공통원인 beta factor를 반영하여 "
            "PFDavg와 PFH를 계산하시오."
        ),
        SAFETY_SW: (
            "SIS SIL safety software의 independence systematic failure "
            "verification validation을 설명하시오."
        ),
    }

    for expected, question in cases.items():
        result = qd_route(question)
        actual = result["candidates"][0]["answer"]["topic_id"]
        assert actual == expected, (expected, actual, result)
        assert actual != TOPIC


def test_golden_contract_primary_topic_matches_runtime_owner() -> None:
    fixture = load(
        REPO
        / "calibration"
        / "sil_target_operations_overgrading_regression.json"
    )
    assert fixture["expected_topics"]["primary"] == TOPIC
    assert set(
        fixture["expected"]["original"]["demand_status"]
    ) == EXPECTED_AXES


def main() -> None:
    tests = sorted(
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    for name, test in tests:
        test()
        print(f"PASS: {name}")
    print(f"PASS: {len(tests)}/{len(tests)} SIL Topic routing checks")


if __name__ == "__main__":
    main()
