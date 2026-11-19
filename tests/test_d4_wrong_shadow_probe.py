from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from grading.evidence.d4_wrong_shadow_probe import (
    compare_d4_shadow_candidates,
    extract_d4_shadow_candidates,
)
from grading.scoring.deterministic_requirement_evaluator import (
    evaluate_deterministic_requirements,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "grading/evidence/approved_fact_registry.json"

CASES = {
    "humidity_relative_vs_absolute": (
        "상대습도와 절대습도는 같은 물리량이다.",
        "상대습도는 수증기 분압과 포화수증기압의 비율이고 절대습도는 단위 체적당 수증기 질량이다.",
        "absolute_humidity_definition",
    ),
    "diaphragm_sensor_vs_seal": (
        "압력 감지 다이어프램과 다이어프램 씰은 같은 역할이다.",
        "압력 감지 다이어프램과 다이어프램 씰은 기능이 다르며 씰은 공정유체를 격리한다.",
        "diaphragm_sensor_vs_seal",
    ),
    "rpm_vs_pulse_frequency": (
        "회전속도 rpm은 pulse frequency Hz와 같고 PPR은 무관하다.",
        "회전속도 n[rpm]은 계수 펄스 주파수 f[Hz]와 유효 count/rev N_eff로 계산하므로 PPR 정의와 복호 모드를 확인한다.",
        "pulse_frequency_speed_equation",
    ),
    "thermocouple_intermediate_metal": (
        "열전대 회로의 제3 금속은 접점 온도와 무관하게 항상 추가 기전력을 만든다.",
        "제3 금속을 넣어도 두 새 접점이 같은 온도이면 순 기전력은 변하지 않는다.",
        "thermocouple_law_of_intermediate_metals",
    ),
    "x4_decoding_vs_channel_ppr": (
        "x4 복호는 엔코더 채널 PPR 자체를 증가시킨다.",
        "x4 복호는 유효 에지 계수 N_eff를 바꾸지만 물리 채널 PPR은 바꾸지 않는다.",
        "encoder_resolution_ppr_cpr_definition",
    ),
    "decoded_count_rate_vs_channel_frequency": (
        "수신기 내부 계수율 f_count는 A상 채널 주파수 f_ch와 항상 같다.",
        "f_ch는 채널 PPR로 계산하고 f_count는 N_eff로 계산하므로 복호 모드에 따라 다를 수 있다.",
        "encoder_frequency_limit_selection",
    ),
}


def _registry_rows():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["facts"]


def test_six_bounded_relation_families_emit_audit_candidates_only():
    for family, (wrong, right, _) in CASES.items():
        wrong_result = extract_d4_shadow_candidates(wrong)
        right_result = extract_d4_shadow_candidates(right)
        assert any(
            row["relation_family"] == family
            and row["surface_relation"] == "opposes_fact"
            for row in wrong_result["candidates"]
        ), family
        assert any(
            row["relation_family"] == family
            and row["surface_relation"] == "unresolved"
            for row in right_result["candidates"]
        ), family
        assert "fact_id" not in wrong_result["candidates"][0]
        assert wrong_result["score_admission"] == "DISABLED"
        assert wrong_result["score_effect"] == "none"
        assert wrong_result["accuracy_status"] == "NOT_ESTABLISHED"
        assert all(row["conditions"] == [] for row in wrong_result["candidates"])
        assert all(row["condition_status"] == "NOT_EXTRACTED" for row in wrong_result["candidates"])


def test_quoted_and_rebutted_wrong_claims_do_not_become_asserted_contradictions():
    for family, (wrong, right, _) in CASES.items():
        quoted = extract_d4_shadow_candidates(f"“{wrong}”라고 인용했다.")
        rebutted = extract_d4_shadow_candidates(f"{right} “{wrong}”은 틀린 설명이다.")
        for result in (quoted, rebutted):
            assert all(
                row["assertion_context"] in {"quoted", "rejected"}
                or row["surface_relation"] != "opposes_fact"
                for row in result["candidates"]
            ), family


def test_mixed_answer_is_reported_as_both_candidates_without_score_decision():
    for family, (wrong, right, _) in CASES.items():
        result = extract_d4_shadow_candidates(f"{right} {wrong}")
        states = [
            row["surface_relation"] for row in result["candidates"]
            if row["relation_family"] == family
        ]
        assert "unresolved" in states, family
        assert "opposes_fact" in states, family
        assert result["score_effect"] == "none"


def test_negated_relation_cues_do_not_turn_corrections_into_contradiction_candidates():
    corrections = {
        "humidity_relative_vs_absolute": "상대습도와 절대습도는 같은 물리량이 아니다.",
        "diaphragm_sensor_vs_seal": "압력 감지 다이어프램과 다이어프램 씰은 같은 역할이 아니다.",
        "rpm_vs_pulse_frequency": "회전속도 rpm은 pulse frequency Hz와 같지 않다.",
        "thermocouple_intermediate_metal": "제3 금속이 항상 추가 기전력을 만드는 것은 아니다.",
        "x4_decoding_vs_channel_ppr": "x4 복호는 엔코더 채널 PPR 자체를 증가시키지 않는다.",
        "decoded_count_rate_vs_channel_frequency": "f_count는 A-channel output frequency와 같지 않다.",
    }
    for family, text in corrections.items():
        result = extract_d4_shadow_candidates(text)
        assert not any(
            row["relation_family"] == family and row["surface_relation"] == "opposes_fact"
            for row in result["candidates"]
        ), family


def test_source_spans_are_exact_and_extraction_never_selects_registry_ids():
    for family, (wrong, _, _) in CASES.items():
        result = extract_d4_shadow_candidates(wrong)
        for row in result["candidates"]:
            span = row["source_span"]
            assert 0 <= span["start"] < span["end"] <= len(wrong)
            assert row["relation_family"] == family
            assert "comparison_fact_id" not in row
            assert "fact_id" not in row


def test_keyword_only_relations_abstain_and_malformed_comparison_fails_closed():
    keywords_only = extract_d4_shadow_candidates("rpm, Hz, PPR 및 엔코더를 확인했다.")
    assert keywords_only["candidates"]
    assert all(row["surface_relation"] == "unresolved" for row in keywords_only["candidates"])
    assert keywords_only["accuracy_status"] == "NOT_ESTABLISHED"
    malformed = compare_d4_shadow_candidates(
        {"schema_version": "d4_wrong_shadow_probe_v1", "candidates": None},
        verified_fact_refs=[],
    )
    assert malformed["status"] == "REJECTED_INPUT"
    assert malformed["comparisons"] == []
    assert malformed["score_effect"] == "none"


def test_explicit_approved_registry_scope_maps_only_in_comparator_and_fails_closed():
    rows = _registry_rows()
    by_anchor = {row.get("legacy_anchor_id"): row for row in rows}
    for family, (wrong, _, anchor_id) in CASES.items():
        fact = by_anchor[anchor_id]
        extraction = extract_d4_shadow_candidates(wrong)
        compared = compare_d4_shadow_candidates(
            extraction, verified_fact_refs=[fact],
        )
        matching = [row for row in compared["comparisons"] if row["relation_family"] == family]
        assert len(matching) == 1
        assert matching[0]["comparison_fact_id"] == fact["fact_id"]
        assert matching[0]["status"] == "CONTRADICT_CANDIDATE"
        assert matching[0]["source_match_proven"] is False
        assert compared["score_admission"] == "DISABLED"
        assert compared["score_effect"] == "none"

        unverified = dict(fact, review_status="pending")
        held = compare_d4_shadow_candidates(extraction, verified_fact_refs=[unverified])
        assert held["comparisons"][0]["status"] == "UNRESOLVED"
        forged = dict(fact, statement="forged statement")
        held = compare_d4_shadow_candidates(extraction, verified_fact_refs=[forged])
        assert held["comparisons"][0]["status"] == "UNRESOLVED"
        held = compare_d4_shadow_candidates(extraction, verified_fact_refs=[fact, fact])
        assert held["comparisons"][0]["status"] == "UNRESOLVED"


def test_support_cues_and_unverified_legacy_support_fail_closed():
    text = "x4 에지 계수는 엔코더 출력 채널에 실제로 생성되는 PPR 자체를 네 배로 바꾼다."
    extraction = extract_d4_shadow_candidates(text)
    rows = [r for r in extraction["candidates"] if r["relation_family"] == "x4_decoding_vs_channel_ppr"]
    assert rows and rows[0]["surface_relation"] == "unresolved"
    fact = next(r for r in _registry_rows() if r.get("legacy_anchor_id") == "encoder_resolution_ppr_cpr_definition")
    rows[0]["surface_relation"] = "supports_fact"
    result = compare_d4_shadow_candidates(extraction, verified_fact_refs=[fact])
    assert all(r["status"] != "SUPPORT_CANDIDATE" for r in result["comparisons"])


def test_test_only_canonical_opposite_claims_reach_contradict_wrong_without_scoring():
    rows = {row.get("legacy_anchor_id"): row for row in _registry_rows()}
    for _, (_, _, anchor_id) in CASES.items():
        source = rows[anchor_id]
        relation = source["relation"]
        fact = {
            "fact_id": source["fact_id"],
            "subject": relation["subject"],
            "predicate": relation["predicate"],
            "object": relation["object"],
            "polarity": "positive",
            "conditions": relation.get("conditions", []),
        }
        contract = {
            "owner_topic_id": source["topic_id"],
            "facts": [fact],
            "invariant_bindings": [],
            "requirement_rules": [{
                "requirement_id": anchor_id,
                "required_fact_ids": [source["fact_id"]],
                "minimum_match_count": 1,
                "contradiction_classification": "major",
                "contradiction_rule_id": f"test_{anchor_id}_conflict",
                "contradiction_recommended_ceiling": 10.0,
            }],
        }
        synthetic_claim = {
            "subject": fact["subject"],
            "predicate": fact["predicate"],
            "object": fact["object"],
            "polarity": "negative",
            "conditions": fact["conditions"],
            "assertion_context": "asserted",
            "claim_id": f"test_{anchor_id}_opposite",
        }
        with patch(
            "grading.scoring.deterministic_requirement_evaluator.load_machine_contracts",
            return_value=[contract],
        ):
            result = evaluate_deterministic_requirements(
                claims=[synthetic_claim], invariant_codes=[],
                topic_ids=[source["topic_id"]], extraction_complete=True,
            )
        assert result["requirements"][0]["status"] == "WRONG"
        assert result["requirements"][0]["contradicted_fact_ids"] == [source["fact_id"]]
        assert result["findings"][0]["invariant_code"] == "MACHINE_CONTRACT_RELATION_CONTRADICTION"
        assert result["score_effect"] == "none"
