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
EXPECTED_FATAL_IDS = {
    "sw05_fatal_hft_is_integration_test",
    "sw05_fatal_software_test_is_random_hardware_integrity",
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


def test_stage25g3f_actual_full_path_merges_one_fatal_ceiling():
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
            "generic verifier must be skipped"
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

    fatal_findings = [
        row
        for row in result["findings"]
        if isinstance(row, dict)
        and str(
            row.get("severity") or ""
        ).strip().lower()
        == "fatal"
    ]
    assert {
        str(row.get("id") or "")
        for row in fatal_findings
    } == EXPECTED_FATAL_IDS

    policy = result["score_policy"]
    assert policy[
        "theory_core_fatal_error"
    ] is True
    assert policy[
        "recommended_ceiling"
    ] == 14.5
    assert policy[
        "score_effect"
    ] == "none"
    assert policy[
        "direct_score_application"
    ] is False
    assert policy["layer_caps"] == {}
    assert policy[
        "direct_d_e_effect"
    ] == "none"

    merge = policy[
        "secondary_fatal_ceiling_merge"
    ]
    assert merge["version"] == (
        "stage25g3f_secondary_fatal_"
        "ceiling_merge_v1"
    )
    assert merge[
        "secondary_topic_id"
    ] == SECONDARY_TOPIC
    assert set(
        merge["fatal_finding_ids"]
    ) == EXPECTED_FATAL_IDS
    assert merge[
        "fatal_finding_count"
    ] == 2
    assert merge[
        "distinct_candidate_ceilings"
    ] == [14.5]
    assert merge[
        "applied_ceiling"
    ] == 14.5
    assert merge[
        "applied_once_per_secondary_evaluation"
    ] is True
    assert merge["merge_count"] == 1
    assert merge[
        "parent_direct_score_application"
    ] is False
    assert merge[
        "direct_d_e_effect"
    ] == "none"


def test_stage25g3f_helper_preserves_existing_stricter_parent_cap():
    parent = {
        "score_policy": {
            "theory_core_fatal_error": True,
            "recommended_ceiling": 12.0,
            "score_effect": "B_C_only",
            "direct_score_application": True,
            "layer_caps": {
                "B": 4.0,
                "C": 5.0,
            },
            "direct_d_e_effect": "none",
        }
    }
    secondary = {
        "findings": [
            {
                "id": "fatal_a",
                "severity": "fatal",
                "recommended_ceiling": 14.5,
            },
            {
                "id": "fatal_b",
                "severity": "fatal",
                "recommended_ceiling": 14.5,
            },
        ],
        "score_policy": {
            "theory_core_fatal_error": True,
            "recommended_ceiling": 14.5,
            "score_effect": "diagnostic_only",
            "direct_score_application": False,
        },
    }

    result = (
        evaluator
        ._stage25g3f_merge_secondary_fatal_ceiling(
            copy.deepcopy(parent),
            copy.deepcopy(secondary),
            SECONDARY_TOPIC,
        )
    )
    policy = result["score_policy"]
    assert policy[
        "recommended_ceiling"
    ] == 12.0
    assert policy[
        "score_effect"
    ] == "B_C_only"
    assert policy[
        "direct_score_application"
    ] is True
    assert policy["layer_caps"] == {
        "B": 4.0,
        "C": 5.0,
    }
    merge = policy[
        "secondary_fatal_ceiling_merge"
    ]
    assert merge[
        "distinct_candidate_ceilings"
    ] == [14.5]
    assert merge[
        "applied_ceiling"
    ] == 12.0
    assert merge[
        "fatal_finding_count"
    ] == 2


def test_stage25g3f_no_secondary_preserves_primary_policy():
    text = (
        "V-model은 요구사항과 시험의 추적성을 "
        "관리한다. 단위시험은 함수와 모듈 로직을 "
        "확인한다."
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
            "compact call is not allowed"
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
    policy = result["score_policy"]
    assert (
        "secondary_fatal_ceiling_merge"
        not in policy
    )
