from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import logic_check_evaluator as evaluator
import logic_llm_verifier as verifier


SW04 = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
SW05 = "sis_sil_safety_software_independence_systematic_failure_verification_validation"
MCDC = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
MISRA_FATAL = "sw04_fatal_misra_is_unit_test_tool"


def _fixture() -> dict:
    return json.loads(
        (ROOT / "calibration" / "mcdc_vmodel_sil_overgrading_regression.json")
        .read_text(encoding="utf-8")
    )


def test_batch_merges_topics_into_exactly_one_llm_call() -> None:
    calls = []

    def fake_call(prompt, **kwargs):
        calls.append((prompt, kwargs))
        return {
            "verdict": "fatal",
            "confidence": 0.95,
            "reason": "표의 범주 대응 오류",
            "checks": [],
            "findings": [{
                "candidate_id": "C1",
                "rule_id": MISRA_FATAL,
                "severity": "fatal",
                "message": "MISRA를 단위시험 도구로 분류함",
                "correct_rule": "MISRA는 코딩 지침이다.",
                "confidence": 0.95,
            }],
            "alignments": [],
        }

    with patch.object(verifier, "_call_ollama_json", side_effect=fake_call):
        result = verifier.verify_logic_topics_with_llm(
            _fixture()["answer"],
            [SW04, MCDC, SW05],
        )

    assert len(calls) == 1
    assert result["llm_call_count"] == 1
    assert result["topic_ids"] == [SW04, MCDC, SW05]
    assert result["findings"][0]["source_rule_id"] == MISRA_FATAL
    prompt = calls[0][0]
    schema = calls[0][1]["format_schema"]
    rule_ids = schema["properties"]["findings"]["items"]["properties"][
        "rule_id"
    ]["enum"]
    assert MISRA_FATAL in prompt
    assert MISRA_FATAL in rule_ids
    assert "sil_four_universal_rule" in prompt
    assert "sw05_fatal_hft_is_integration_test" in prompt


def test_explicit_topics_precede_claim_secondary_in_same_batch() -> None:
    bank = json.loads(
        (ROOT / "rubrics" / "generated" / "logic_checks.generated.json")
        .read_text(encoding="utf-8")
    )
    grade = {
        "question_contract": {
            "multi_topic_grading_context_summary": {
                "routing_mode": "MULTI_TOPIC",
                "primary_topic_ids": [SW04, MCDC],
            }
        }
    }
    topic_ids = evaluator._stage25g3e_multi_topic_batch_ids(
        grade,
        _fixture()["answer"],
        SW04,
        bank["topic_logic_checks"],
    )
    assert topic_ids[:2] == [SW04, MCDC]
    assert SW05 in topic_ids
    assert len(topic_ids) == len(set(topic_ids))


def test_markdown_table_rows_keep_header_value_relations() -> None:
    profile = {
        "candidate_extraction": {
            "max_candidates": 20,
            "nearby_window": 1,
            "rules": [],
            "key_terms": ["MISRA", "HFT", "Random Integrity"],
        }
    }
    candidates = verifier.extract_logic_evidence_candidates(
        _fixture()["answer"],
        profile,
    )
    table_rows = [
        row["text"] for row in candidates
        if row["kind"] == "structured_table_relation"
    ]
    assert any("단계=단위" in row and "SIL 요소=Random Integrity" in row for row in table_rows)
    assert any("단계=통합" in row and "HFT 0,1,2" in row for row in table_rows)


def test_profile_owned_authoritative_relations_survive_batching() -> None:
    profile = verifier._combined_logic_profile(
        [SW04, MCDC, SW05],
        _fixture()["answer"],
    )
    findings = verifier._authoritative_structured_findings(
        _fixture()["answer"],
        profile,
        10.0,
    )
    rule_ids = {row["source_rule_id"] for row in findings}
    assert "sw05_fatal_hft_is_integration_test" in rule_ids
    assert "sw05_fatal_software_test_is_random_hardware_integrity" in rule_ids

    safe_answer = (
        "통합시험은 인터페이스를 검증한다.\n"
        "HFT는 별도의 하드웨어 아키텍처 제약이다."
    )
    assert verifier._authoritative_structured_findings(
        safe_answer,
        profile,
        10.0,
    ) == []


if __name__ == "__main__":
    tests = [
        value for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    ]
    for test in tests:
        test()
    print(f"MULTI_TOPIC_LOGIC_BATCH_TESTS={len(tests)}_PASS")
