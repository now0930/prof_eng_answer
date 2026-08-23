from __future__ import annotations

from unittest.mock import patch

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier_module
from logic_llm_verifier import load_logic_check_profile


TOPIC_ID = "sis_sil_safety_software_independence_systematic_failure_verification_validation"

SYNTHETIC_TEXT = (
    "비교 항목 | 단위 시험 | 통합 시험 | 시스템 시험\n"
    "SIL 대응 요소 | Random Integrity | "
    "Architectural Constraints (HFT 0,1,2) | "
    "Systematic Integrity\n\n"
    "Architectural Constraints: "
    "HFT(1oo2, 2oo3) 이중화 검증.\n"
    "통합 시험 → 1oo2 voting architecture.\n\n"
    "SIL: Safety Instrument Level.\n"
    "정상 대조군 표현: Safety Integrity Level.\n"
)



def _profile():
    return load_logic_check_profile(TOPIC_ID)


def _expected_response():
    return {
        "voting_mapping_wrong": True,
        "hft_mapping_wrong": True,
        "random_integrity_mapping_wrong": True,
        "sil_expansion_wrong": True,
        "correct_sil_control_wrong": False,
    }


def test_stage25g3c_profile_contract_and_activation_owner():
    profile = _profile()
    assert profile["candidate_extraction"]["rules"] == []
    activation = profile["secondary_profile_activation"]
    assert len(activation["rules"]) == 1
    assert activation["rules"][0]["id"] == (
        "sw05_claim_triggered_secondary_profile_v1"
    )
    compact = profile["compact_batch_verification"]
    assert compact["enabled"] is True
    assert compact["max_llm_calls"] == 1
    assert len(compact["fields"]) == 5


def test_stage25g3c_compact_batch_calls_llm_once_and_builds_findings():
    profile = _profile()
    calls = []

    def fake_call(prompt, format_schema=None):
        calls.append((prompt, format_schema))
        return _expected_response()

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=fake_call,
    ):
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                SYNTHETIC_TEXT,
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert len(calls) == 1
    assert result["fatal_error_detected"] is True
    assert result["diagnostics"] == []
    assert result[
        "compact_batch_verification"
    ]["llm_call_count"] == 1
    assert {
        finding["id"]
        for finding in result["findings"]
    } == {
        "sw05_fatal_software_test_mapped_to_voting_architecture",
        "sw05_fatal_hft_is_integration_test",
        "sw05_fatal_software_test_is_random_hardware_integrity",
        "sw05_fatal_sil_expanded_as_safety_instrument_level",
    }


def test_stage25g3c_invalid_schema_is_warn_without_retry_or_fatal():
    profile = _profile()
    calls = []

    def fake_call(prompt, format_schema=None):
        calls.append(1)
        return {"voting_mapping_wrong": True}

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=fake_call,
    ):
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                SYNTHETIC_TEXT,
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert len(calls) == 1
    assert result["mode"] == "warn"
    assert result["fatal_error_detected"] is False
    assert result["findings"] == []
    assert (
        result["diagnostics"][0]["reason"]
        == "compact_batch_invalid_boolean_schema"
    )


def test_stage25g3c_control_mismatch_is_warn_without_finding():
    profile = _profile()
    response = _expected_response()
    response["correct_sil_control_wrong"] = True

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        return_value=response,
    ) as mocked:
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                SYNTHETIC_TEXT,
                profile["fatal_conditions"],
                {"profile": profile},
            )
        )

    assert mocked.call_count == 1
    assert result["mode"] == "warn"
    assert result["fatal_error_detected"] is False
    assert result["findings"] == []
    assert (
        result["diagnostics"][0]["reason"]
        == "compact_batch_control_mismatch"
    )


def test_stage25g3c_nonconfigured_profile_keeps_generic_path():
    calls = []

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=lambda *args, **kwargs: calls.append(1),
    ):
        result = (
            evaluator
            ._stage25g3c_compact_batch_secondary_once(
                "text",
                [],
                {"profile": {}},
            )
        )

    assert result is None
    assert calls == []
