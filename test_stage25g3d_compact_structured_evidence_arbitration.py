from __future__ import annotations

from unittest.mock import patch

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier_module
from logic_llm_verifier import load_logic_check_profile


TOPIC_ID = "sis_sil_safety_software_independence_systematic_failure_verification_validation"

ACTUAL_OCR_TABLE_TEXT = (
    "비교 항목 (비교축)단위 시험통합 시험시스템 시험\n"
    "검증 대상 / 도구단일 모듈 / xUnit, MISRA"
    "인터페이스 / Stub, S/W HIL전체 SIS / HIL 시뮬레이터\n"
    "SIL 대응 요소Random Integrity"
    "Arch. Constraints (HFT 0,1,2)Systematic Integrity\n"
    "Architectural Constraints: HFT(1oo2, 2oo3) "
    "이중화 검증, HIL 시뮬레이션 기반 검증.\n"
    "SIL (Safety Integrity Level): 정상 정의.\n"
)

DIRECT_VOTING_TEXT = (
    "통합 시험 → 1oo2 voting architecture.\n"
    "SIL (Safety Integrity Level): 정상 정의.\n"
)


def _profile():
    return load_logic_check_profile(TOPIC_ID)


def _raw_response_for_actual_ocr():
    return {
        "voting_mapping_wrong": True,
        "hft_mapping_wrong": False,
        "random_integrity_mapping_wrong": False,
        "sil_expansion_wrong": False,
        "correct_sil_control_wrong": False,
    }


def test_stage25g3d_profile_v2_evidence_policy_contract():
    compact = _profile()["compact_batch_verification"]
    assert compact["version"] == 2
    assert compact["max_llm_calls"] == 1

    fields = {
        row["field_id"]: row
        for row in compact["fields"]
    }
    assert fields["voting_mapping_wrong"][
        "require_nonempty_evidence_for_true"
    ] is True
    assert (
        "structured_relation"
        not in fields["voting_mapping_wrong"]
    )
    assert fields["hft_mapping_wrong"][
        "structured_relation"
    ]["authoritative_true"] is True
    assert fields["random_integrity_mapping_wrong"][
        "structured_relation"
    ]["authoritative_true"] is True


def test_stage25g3d_actual_ocr_table_arbitrates_model_errors_once():
    profile = _profile()
    calls = []

    def fake_call(prompt, format_schema=None):
        calls.append((prompt, format_schema))
        return _raw_response_for_actual_ocr()

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=fake_call,
    ):
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                ACTUAL_OCR_TABLE_TEXT,
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert len(calls) == 1
    finding_ids = {
        row["id"]
        for row in result["findings"]
    }
    assert finding_ids == {
        "sw05_fatal_hft_is_integration_test",
        "sw05_fatal_software_test_is_random_hardware_integrity",
    }

    meta = result["compact_batch_verification"]
    assert meta["raw_field_values"] == (
        _raw_response_for_actual_ocr()
    )
    assert meta["field_values"] == {
        "voting_mapping_wrong": False,
        "hft_mapping_wrong": True,
        "random_integrity_mapping_wrong": True,
        "sil_expansion_wrong": False,
        "correct_sil_control_wrong": False,
    }
    assert set(meta["structured_true_fields"]) == {
        "hft_mapping_wrong",
        "random_integrity_mapping_wrong",
    }

    actions = {
        row["field_id"]: row["action"]
        for row in meta["arbitration"]
    }
    assert actions == {
        "voting_mapping_wrong": (
            "true_without_field_evidence_suppressed"
        ),
        "hft_mapping_wrong": (
            "structured_relation_false_negative_override"
        ),
        "random_integrity_mapping_wrong": (
            "structured_relation_false_negative_override"
        ),
    }

    prompt = calls[0][0]
    assert (
        "sw05_fatal_hft_is_integration_test"
        in prompt
    )
    assert (
        "sw05_fatal_software_test_is_random_hardware_integrity"
        in prompt
    )
    assert (
        "OCR 표 열 대응: 통합시험 → "
        "Architectural Constraints (HFT)"
        in prompt
    )
    assert (
        "OCR 표 열 대응: 단위시험 → "
        "Random Hardware Integrity"
        in prompt
    )
    assert (
        "한 field의 evidence를 다른 field의 근거로"
        in prompt
    )


def test_stage25g3d_direct_voting_evidence_is_not_suppressed():
    profile = _profile()
    response = {
        "voting_mapping_wrong": True,
        "hft_mapping_wrong": False,
        "random_integrity_mapping_wrong": False,
        "sil_expansion_wrong": False,
        "correct_sil_control_wrong": False,
    }

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        return_value=response,
    ) as mocked:
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                DIRECT_VOTING_TEXT,
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert mocked.call_count == 1
    assert {
        row["id"]
        for row in result["findings"]
    } == {
        "sw05_fatal_software_test_mapped_to_voting_architecture"
    }
    meta = result["compact_batch_verification"]
    assert meta["field_values"][
        "voting_mapping_wrong"
    ] is True
    assert meta["arbitration"] == []


def test_stage25g3d_empty_evidence_true_is_suppressed():
    profile = _profile()
    response = {
        "voting_mapping_wrong": False,
        "hft_mapping_wrong": False,
        "random_integrity_mapping_wrong": False,
        "sil_expansion_wrong": True,
        "correct_sil_control_wrong": False,
    }

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        return_value=response,
    ) as mocked:
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                "SIL 관련 일반 설명만 있다.",
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert mocked.call_count == 1
    assert result["findings"] == []
    meta = result["compact_batch_verification"]
    assert meta["raw_field_values"][
        "sil_expansion_wrong"
    ] is True
    assert meta["field_values"][
        "sil_expansion_wrong"
    ] is False
    assert meta["arbitration"] == [
        {
            "field_id": "sil_expansion_wrong",
            "action": (
                "true_without_field_evidence_suppressed"
            ),
            "raw_value": True,
            "effective_value": False,
        }
    ]
