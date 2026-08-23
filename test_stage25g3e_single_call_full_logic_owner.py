from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import patch

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier_module


PRIMARY_TOPIC = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)
SECONDARY_TOPIC = (
    "sis_sil_safety_software_independence_"
    "systematic_failure_verification_validation"
)
SESSION_ID = "20260822_092545_5960502198"

ACTUAL_RAW_RESPONSE = {
    "voting_mapping_wrong": False,
    "hft_mapping_wrong": True,
    "random_integrity_mapping_wrong": True,
    "sil_expansion_wrong": False,
    "correct_sil_control_wrong": False,
}


def _repo() -> Path:
    return Path(__file__).resolve().parent


def _actual_session():
    session = (
        _repo()
        / "data"
        / "sessions"
        / SESSION_ID
    )
    text = (
        session / "input.raw.txt"
    ).read_text(encoding="utf-8")
    grade = json.loads(
        (session / "grade.json").read_text(
            encoding="utf-8"
        )
    )
    return text, grade


def _pass_profile_result():
    return {
        "verdict": "pass",
        "confidence": "high",
        "reason": "focused test pass",
        "checks": [],
        "findings": [],
        "alignments": [],
    }


def test_stage25g3e_actual_full_path_uses_one_compact_call():
    text, grade = _actual_session()
    compact_calls = []
    generic_calls = []

    def fake_compact(prompt, format_schema=None):
        compact_calls.append(
            (prompt, format_schema)
        )
        return copy.deepcopy(
            ACTUAL_RAW_RESPONSE
        )

    def forbidden_generic(*args, **kwargs):
        generic_calls.append(
            (args, kwargs)
        )
        raise AssertionError(
            "generic verifier must be skipped when "
            "compact secondary owns the single call"
        )

    with patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=fake_compact,
    ), patch.object(
        verifier_module,
        "verify_logic_with_llm",
        side_effect=forbidden_generic,
    ):
        result = evaluator.evaluate_logic_checks(
            answer_text=text,
            grade=copy.deepcopy(grade),
        )

    assert len(compact_calls) == 1
    assert generic_calls == []

    prompt, schema = compact_calls[0]
    assert isinstance(prompt, str)
    assert (
        "sw05_fatal_hft_is_integration_test"
        in prompt
    )
    assert (
        "sw05_fatal_software_test_is_random_hardware_integrity"
        in prompt
    )
    assert isinstance(schema, dict)
    assert set(
        schema.get("properties", {})
    ) == set(ACTUAL_RAW_RESPONSE)

    all_findings = [
        row
        for row in result["findings"]
        if isinstance(row, dict)
    ]
    fatal_findings = [
        row
        for row in all_findings
        if str(
            row.get("severity") or ""
        ).strip().lower()
        == "fatal"
    ]
    fatal_finding_ids = {
        str(row.get("id") or "")
        for row in fatal_findings
    }
    assert fatal_finding_ids == {
        "sw05_fatal_hft_is_integration_test",
        "sw05_fatal_software_test_is_random_hardware_integrity",
    }, {
        "all_finding_ids": [
            str(row.get("id") or "")
            for row in all_findings
        ],
        "fatal_finding_ids": sorted(
            fatal_finding_ids
        ),
        "severities": [
            str(row.get("severity") or "")
            for row in all_findings
        ],
    }
    assert len(fatal_findings) == 2
    assert all(
        isinstance(row, dict)
        for row in fatal_findings
    )
    assert all(
        str(row.get("id") or "").startswith(
            "sw05_fatal_"
        )
        for row in fatal_findings
    )

    assert result["fatal_error_detected"] is True
    assert result["mode"] == "fatal"

    all_layers = {
        layer
        for row in all_findings
        for layer in (
            row.get("affected_layers")
            if isinstance(
                row.get("affected_layers"),
                list,
            )
            else []
        )
    }
    assert all_layers <= {"A", "B", "C"}
    assert "D" not in all_layers
    assert "E" not in all_layers

    owner = result[
        "single_llm_owner_evaluation"
    ]
    assert owner == {
        "version": (
            "stage25g3e_single_call_owner_v7"
        ),
        "compact_secondary_topic_id": (
            SECONDARY_TOPIC
        ),
        "internal_compact_secondary": False,
        "primary_profile_verifier_skipped": True,
        "semantic_llm_owner": (
            "secondary_compact_helper"
        ),
        "max_llm_calls": 1,
    }


def test_stage25g3e_no_secondary_preserves_primary_verifier():
    text = (
        "V-model은 요구사항과 시험의 추적성을 "
        "관리하는 소프트웨어 수명주기 모델이다. "
        "단위시험은 함수와 모듈 로직을 확인한다."
    )
    grade = {
        "logic_check_topic_id": PRIMARY_TOPIC,
        "model_answer_reference": {},
        "question_analysis": {},
    }

    generic_calls = []
    compact_calls = []

    def fake_generic(*args, **kwargs):
        generic_calls.append(
            (args, kwargs)
        )
        return _pass_profile_result()

    def forbidden_compact(*args, **kwargs):
        compact_calls.append(
            (args, kwargs)
        )
        raise AssertionError(
            "compact call is not allowed without "
            "an activated compact secondary"
        )

    with patch.object(
        verifier_module,
        "verify_logic_with_llm",
        side_effect=fake_generic,
    ), patch.object(
        verifier_module,
        "_call_ollama_json",
        side_effect=forbidden_compact,
    ):
        result = evaluator.evaluate_logic_checks(
            answer_text=text,
            grade=copy.deepcopy(grade),
        )

    assert len(generic_calls) == 1
    assert compact_calls == []
    assert generic_calls[0][0][1] == PRIMARY_TOPIC

    owner = result[
        "single_llm_owner_evaluation"
    ]
    assert owner[
        "compact_secondary_topic_id"
    ] == ""
    assert owner[
        "primary_profile_verifier_skipped"
    ] is False
    assert owner[
        "semantic_llm_owner"
    ] == "primary_profile_verifier"
    assert owner["max_llm_calls"] == 1


def test_stage25g3e_compact_profile_selection_contract():
    text, grade = _actual_session()
    logic_path = (
        _repo()
        / "rubrics"
        / "generated"
        / "logic_checks.generated.json"
    )
    assert logic_path.is_file()
    bank = json.loads(
        logic_path.read_text(
            encoding="utf-8"
        )
    )
    candidates, topic_id = (
        evaluator
        ._stage25g3e_preselect_compact_secondary(
            text,
            PRIMARY_TOPIC,
            bank.get("topic_logic_checks", []),
        )
    )

    assert topic_id == SECONDARY_TOPIC
    assert len(candidates) == 1
    assert (
        evaluator._stage25g3e_candidate_topic_id(
            candidates[0]
        )
        == SECONDARY_TOPIC
    )

    profile = (
        evaluator._stage25g3e_compact_profile_v2(
            SECONDARY_TOPIC
        )
    )
    assert isinstance(profile, dict)
    compact = profile[
        "compact_batch_verification"
    ]
    assert compact["version"] == 2
    assert compact["max_llm_calls"] == 1
