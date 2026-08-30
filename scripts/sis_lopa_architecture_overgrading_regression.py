#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from answer_volume import estimate_ascii_answer_volume, normalize_volume_text

HAZOP = "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
FSRM = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"
HAZARDOUS_AREA = (
    "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection"
)
FATAL_ID = "failure_rate_compared_directly_to_pfd"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fatal_ids(items: list[Any]) -> set[str]:
    result: set[str] = set()
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            result.add(item["id"])
        elif isinstance(item, str):
            match = re.match(r"\s*\[([^\]]+)\]", item)
            if match:
                result.add(match.group(1))
    return result


def main() -> None:
    fixture = load_json(
        REPO / "calibration"
        / "sis_lopa_architecture_overgrading_regression.json"
    )
    hazop_model = load_json(
        REPO / "rubrics" / "topic_packs" / HAZOP / "model_answer.json"
    )
    fsrm_logic = load_json(
        REPO / "rubrics" / "topic_packs" / FSRM / "logic_check.json"
    )

    expected = fixture["expected"]
    volume_expected = expected["volume"]
    inline_submission = (
        "/grade\n"
        "문제: "
        + fixture["question"]
        + ("=" * 80)
        + fixture["answer"]
        + "\n끝."
    )

    normalized = normalize_volume_text(inline_submission)
    expected_normalized = normalize_volume_text(fixture["answer"])
    assert normalized == expected_normalized
    assert normalized != fixture["answer"]

    volume = estimate_ascii_answer_volume(inline_submission)
    assert volume["ascii_equivalent_count"] == 1755
    assert volume["ascii_equivalent_count"] == volume_expected["ascii_equivalent_count"]
    assert volume["page_equivalent"] == 2.92
    assert volume["level"] == "three_page_text"
    assert volume["cap"] is None
    assert volume_expected["volume_cap_allowed"] is False

    patterns = hazop_model["expected_question_patterns"]
    assert any(
        item.get("intent")
        == "reactor overpressure target SIL determination and "
        "SIS architecture handoff"
        for item in patterns
    )

    aliases = set(hazop_model["routing_aliases"])
    assert {
        "반응기 과압력 시나리오 SIL 결정 과정",
        "과압력 시나리오 목표 SIL 결정",
        "기존 보호장치 불충분 SIS 도입",
        "SIL 결정과 SIS 아키텍처",
    } <= aliases

    ids = fatal_ids(fsrm_logic["llm_profile"]["fatal_conditions"])
    assert FATAL_ID in ids
    assert fsrm_logic["deterministic_checks"]["enabled"] is False

    fatal_text = "\n".join(fsrm_logic["llm_profile"]["fatal_conditions"])
    assert "lambda_SIS" in fatal_text
    assert "차원이 다르므로 직접 비교할 수 없다" in fatal_text

    activation = fsrm_logic["llm_profile"]["secondary_profile_activation"]
    compact = fsrm_logic["llm_profile"]["compact_batch_verification"]
    assert compact["enabled"] is True
    assert compact["version"] == 2
    assert compact["max_llm_calls"] == 1


    # STAGE34C_V4_FSRM_COMPACT_CONTRACT
    compact_fields = compact["fields"]
    assert len(compact_fields) == 2
    compact_field_ids = [
        row["field_id"]
        for row in compact_fields
        if isinstance(row, dict)
    ]
    assert compact_field_ids == [
        FATAL_ID,
        "correct_lambda_pfd_dimension_separation_control",
    ]
    fatal_compact_field = compact_fields[0]
    assert fatal_compact_field["rule_id"] == FATAL_ID
    assert fatal_compact_field[
        "require_nonempty_evidence_for_true"
    ] is True
    selector_patterns = [
        selector["pattern"]
        for selector in fatal_compact_field["evidence_selectors"]
        if isinstance(selector, dict)
        and isinstance(selector.get("pattern"), str)
    ]
    assert len(selector_patterns) == 2
    assert sum(
        re.search(pattern, fixture["answer"]) is not None
        for pattern in selector_patterns
    ) >= 1

    # STAGE34G_FSRM_STRUCTURED_FALSE_NEGATIVE_OVERRIDE_CONTRACT
    structured_relation = fatal_compact_field["structured_relation"]
    assert structured_relation["authoritative_true"] is True
    structured_pattern = structured_relation["combined_pattern"]
    re.compile(structured_pattern)
    assert re.search(structured_pattern, fixture["answer"]) is not None
    assert re.search(
        structured_pattern,
        (
            "저수요 모드에서 PFDavg는 λDU×TI/2로 근사하며 "
            "고장률과 무차원 PFD를 직접 대소 비교하지 않는다."
        ),
    ) is None
    assert re.search(
        structured_pattern,
        (
            "잘못된 예시: lambda_SIS 비율이 PFD 비율보다 "
            "작도록 시스템을 설계."
        ),
    ) is None
    assert re.search(
        structured_pattern,
        (
            "lambda_SIS 비율이 PFD 비율보다 작도록 시스템을 "
            "설계하면 안 된다."
        ),
    ) is None

    control_field = compact_fields[1]
    assert control_field["field_id"] == "correct_lambda_pfd_dimension_separation_control"
    assert control_field["control_expected"] is False
    assert not any(
        str(row.get("rule_id") or "").startswith("sw05_")
        for row in compact_fields
        if isinstance(row, dict)
    )

    activation_rules = activation["rules"]
    assert len(activation_rules) == 1
    secondary_rule = activation_rules[0]
    assert secondary_rule["id"] == "fsrm_lambda_pfd_dimension_secondary_activation_v2"
    assert (
        secondary_rule["activation_scope"]
        == "claim_triggered_secondary_profile_v1"
    )
    assert secondary_rule["score_effect_requirement"] == "diagnostic_only"

    import logic_check_evaluator
    from logic_check_evaluator import (
        _secondary_profile_rule_match,
        _select_claim_triggered_secondary_profiles,
        _stage25g3e_preselect_compact_secondary,
    )
    import logic_llm_verifier

    activation_match = _secondary_profile_rule_match(
        fixture["answer"],
        secondary_rule,
    )
    assert activation_match["matched"] is True
    assert activation_match["strong_count"] >= 2

    generated_logic_bank = load_json(
        REPO / "rubrics" / "generated" / "logic_checks.generated.json"
    )
    generated_profile_path = (
        REPO
        / "rubrics"
        / "generated"
        / "logic_check_profiles.generated.json"
    )
    original_profile_path = logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH
    logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = generated_profile_path
    try:
        selected = _select_claim_triggered_secondary_profiles(
            fixture["answer"],
            HAZOP,
            generated_logic_bank["topic_logic_checks"],
        )
        compact_candidates, compact_topic_id = (
            _stage25g3e_preselect_compact_secondary(
                fixture["answer"],
                HAZOP,
                generated_logic_bank["topic_logic_checks"],
            )
        )
        negative_selected = {}
        for negative_name, negative_answer in {
            "hazop_only": "HAZOP 노드와 IPL 독립성만 검토한다.",
            "correct_pfd_relation": (
                "저수요 모드에서 PFDavg는 λDU×TI/2로 근사하며 "
                "고장률과 무차원 PFD를 직접 대소 비교하지 않는다."
            ),
            "rate_sum_only": (
                "센서, 로직솔버, 최종요소의 위험 고장률을 합산한다."
            ),
            "pfd_only": "PFDavg 목표로 SIL 달성 여부를 검증한다.",
        }.items():
            negative_selected[negative_name] = [
                row["topic_id"]
                for row in _select_claim_triggered_secondary_profiles(
                    negative_answer,
                    HAZOP,
                    generated_logic_bank["topic_logic_checks"],
                )
            ]
    finally:
        logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = original_profile_path

    assert [row["topic_id"] for row in selected] == [FSRM]
    assert [row["topic_id"] for row in compact_candidates] == [FSRM]
    assert compact_topic_id == FSRM

    # STAGE34C_V4_FULL_EVALUATOR_REPLAY
    generated_profile_bank = load_json(generated_profile_path)
    generated_fsrm_profiles = [
        row
        for row in generated_profile_bank["profiles"]
        if isinstance(row, dict)
        and row.get("topic_id") == FSRM
    ]
    assert len(generated_fsrm_profiles) == 1
    generated_fsrm_profile = generated_fsrm_profiles[0]
    generated_compact_fields = generated_fsrm_profile[
        "compact_batch_verification"
    ]["fields"]
    generated_field_ids = [
        row["field_id"]
        for row in generated_compact_fields
        if isinstance(row, dict)
        and isinstance(row.get("field_id"), str)
    ]
    assert generated_field_ids == [
        FATAL_ID,
        "correct_lambda_pfd_dimension_separation_control",
    ]

    provider_calls = []

    def fake_compact_call(*args, **kwargs):
        prompt = str(
            args[0]
            if args
            else kwargs.get("prompt") or ""
        )
        schema = kwargs.get("format_schema")
        if not isinstance(schema, dict):
            for value in args[1:]:
                if (
                    isinstance(value, dict)
                    and isinstance(value.get("properties"), dict)
                ):
                    schema = value
                    break
        assert isinstance(schema, dict)
        properties = schema.get("properties")
        assert isinstance(properties, dict)
        property_ids = list(properties)
        provider_calls.append(
            {
                "prompt": prompt,
                "property_ids": property_ids,
            }
        )
        return {
            field_id: field_id == FATAL_ID
            for field_id in property_ids
        }

    original_call = logic_llm_verifier._call_ollama_json
    original_profile_path = logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH
    logic_llm_verifier._call_ollama_json = fake_compact_call
    logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = generated_profile_path
    try:
        full_replay = logic_check_evaluator.evaluate_logic_checks(
            answer_text=fixture["answer"],
            grade={"logic_check_topic_id": HAZOP},
            bank_path=(
                REPO
                / "rubrics"
                / "generated"
                / "logic_checks.generated.json"
            ),
        )
    finally:
        logic_llm_verifier._call_ollama_json = original_call
        logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = original_profile_path

    assert len(provider_calls) == 1
    call = provider_calls[0]
    assert call["property_ids"] == generated_field_ids
    assert FATAL_ID in call["prompt"]
    assert "correct_lambda_pfd_dimension_separation_control" in call["prompt"]
    assert isinstance(full_replay, dict)
    assert full_replay.get("fatal_error_detected") is True
    assert full_replay.get("mode") == "fatal"
    assert FSRM in full_replay.get("evaluated_topic_ids", [])

    selection = full_replay.get("secondary_profile_selection")
    assert isinstance(selection, dict)
    assert selection.get("selected_topic_ids") == [FSRM]

    replay_findings = full_replay.get("findings") or []
    fatal_replay_findings = [
        row
        for row in replay_findings
        if isinstance(row, dict)
        and str(row.get("severity") or "").lower() == "fatal"
        and FATAL_ID
        in {
            str(row.get("id") or ""),
            str(row.get("rule_id") or ""),
            str(row.get("source_rule_id") or ""),
        }
    ]
    assert len(fatal_replay_findings) == 1
    assert fatal_replay_findings[0].get("evidence")
    assert fatal_replay_findings[0].get("source_topic_id") == FSRM

    secondary_rows = full_replay.get(
        "secondary_profile_evaluations"
    ) or []
    assert len(secondary_rows) == 1
    assert secondary_rows[0].get("topic_id") == FSRM
    assert FATAL_ID in secondary_rows[0].get(
        "merged_finding_ids", []
    )
    assert all(
        FSRM not in topic_ids
        for topic_ids in negative_selected.values()
    )

    # STAGE34G_FSRM_STRUCTURED_FALSE_NEGATIVE_OVERRIDE_REPLAY
    false_negative_provider_calls = []

    def fake_false_negative_call(*args, **kwargs):
        prompt = str(
            args[0]
            if args
            else kwargs.get("prompt") or ""
        )
        schema = kwargs.get("format_schema")
        if not isinstance(schema, dict):
            for value in args[1:]:
                if (
                    isinstance(value, dict)
                    and isinstance(value.get("properties"), dict)
                ):
                    schema = value
                    break
        assert isinstance(schema, dict)
        properties = schema.get("properties")
        assert isinstance(properties, dict)
        property_ids = list(properties)
        false_negative_provider_calls.append(
            {
                "prompt": prompt,
                "property_ids": property_ids,
            }
        )
        return {
            field_id: False
            for field_id in property_ids
        }

    original_call = logic_llm_verifier._call_ollama_json
    original_profile_path = logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH
    logic_llm_verifier._call_ollama_json = fake_false_negative_call
    logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = generated_profile_path
    try:
        structured_override_replay = (
            logic_check_evaluator.evaluate_logic_checks(
                answer_text=fixture["answer"],
                grade={"logic_check_topic_id": HAZOP},
                bank_path=(
                    REPO
                    / "rubrics"
                    / "generated"
                    / "logic_checks.generated.json"
                ),
            )
        )
    finally:
        logic_llm_verifier._call_ollama_json = original_call
        logic_llm_verifier.LOGIC_CHECK_PROFILE_PATH = original_profile_path

    assert len(false_negative_provider_calls) == 1
    false_call = false_negative_provider_calls[0]
    assert false_call["property_ids"] == generated_field_ids
    assert isinstance(structured_override_replay, dict)
    assert structured_override_replay.get("fatal_error_detected") is True
    assert structured_override_replay.get("mode") == "fatal"

    structured_findings = [
        row
        for row in structured_override_replay.get("findings", [])
        if isinstance(row, dict)
        and str(row.get("severity") or "").lower() == "fatal"
        and row.get("id") == FATAL_ID
    ]
    assert len(structured_findings) == 1
    assert (
        structured_findings[0].get("source")
        == "stage25g3d_compact_structured_evidence_arbitration"
    )
    assert structured_findings[0].get("source_topic_id") == FSRM
    assert structured_findings[0].get("evidence")

    structured_secondary_rows = (
        structured_override_replay.get(
            "secondary_profile_evaluations"
        )
        or []
    )
    assert len(structured_secondary_rows) == 1
    assert structured_secondary_rows[0].get("topic_id") == FSRM
    assert FATAL_ID in structured_secondary_rows[0].get(
        "merged_finding_ids", []
    )

    topics = fixture["expected_topics"]
    assert topics["primary"] == HAZOP
    assert topics["adjacent"] == [FSRM]
    assert topics["forbidden"] == [HAZARDOUS_AREA]

    statuses = expected["demand_status"]
    assert sum(value == "present" for value in statuses.values()) == 1
    assert sum(value == "partial" for value in statuses.values()) == 4
    assert sum(value == "incorrect" for value in statuses.values()) == 2
    assert sum(value == "missing" for value in statuses.values()) == 1

    assert expected["requirements_full_credit_allowed"] is False
    assert expected["strong_verdict_allowed"] is False
    assert expected["passing_score_allowed"] is False
    assert expected["maximum_total_score"] == 13.0
    assert expected["total_range"]["max"] == 13.0
    assert FATAL_ID in expected["required_fatal_ids"]

    forbidden = "\n".join(expected["forbidden_feedback_elements"])
    assert "100%" in forbidden
    assert "0.5쪽 미만" in forbidden
    assert "9.0점" in forbidden
    assert "15점 이상" in forbidden

    print("SIS_LOPA_ARCHITECTURE_OVERGRADING_REGRESSION=PASS")
    print("INLINE_ANSWER_ASCII_COUNT=1755")
    print("INLINE_ANSWER_LEVEL=three_page_text")
    print("VOLUME_CAP=NONE")
    print(f"PRIMARY_TOPIC={HAZOP}")
    print(f"ADJACENT_TOPIC={FSRM}")
    print(f"FATAL_ID={FATAL_ID}")
    print("SECONDARY_PROFILE_ACTIVATION=PASS")
    print("SECONDARY_PROFILE_SELECTION=PASS")
    print("SECONDARY_PROFILE_FSRM_NEGATIVE_GUARD=PASS")
    print("FSRM_COMPACT_PROFILE_RULE_BRIDGE=PASS")
    print("FSRM_COMPACT_FIELD_CONTRACT=PASS")
    print("FULL_EVALUATOR_COMPACT_REPLAY=PASS")
    print("FSRM_STRUCTURED_FALSE_NEGATIVE_OVERRIDE=PASS")
    print("FULL_EVALUATOR_LLM_CALL_COUNT=1")
    print("FULL_EVALUATOR_SCHEMA_PROPERTY_COUNT=2")
    print("COMPACT_SECONDARY_TOPIC=" + FSRM)
    print("DEMAND_STATUS=present:1,partial:4,incorrect:2,missing:1")
    print("TOTAL_MAX=13.0")


if __name__ == "__main__":
    main()
