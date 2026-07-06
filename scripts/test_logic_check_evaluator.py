#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest.mock import patch

import logic_check_evaluator


TOPIC_ID = "second_order_lag_response_by_damping_ratio"


def evaluate(answer_text: str, semantic_findings: list[dict] | None = None) -> dict:
    grade = {
        "total_score": 20.0,
        "max_score": 25,
        "topic_id": TOPIC_ID,
        "difficulty_strategy": {
            "topic_id": TOPIC_ID,
        },
    }

    # Keep regression tests deterministic and CI-safe:
    # - do not call Ollama / external LLM verifier
    # - inject only the semantic fatal findings needed by the test
    with patch.object(
        logic_check_evaluator,
        "_evaluate_topic_fatal_checks_with_llm",
        return_value=semantic_findings or [],
    ), patch(
        "logic_llm_verifier.verify_logic_with_llm",
        return_value={
            "fatal_error_detected": False,
            "mode": "mocked",
            "findings": [],
        },
    ), patch(
        "logic_llm_verifier._call_ollama_json",
        return_value=None,
    ):
        out = logic_check_evaluator.attach_logic_check_to_grade(grade, answer_text)

    logic = out.get("logic_check_evaluation")
    assert isinstance(logic, dict)
    return logic


class LogicCheckEvaluatorRegressionTest(unittest.TestCase):
    def test_safe_critical_damping_statement_is_not_fatal(self) -> None:
        logic = evaluate(
            "ζ=1은 임계감쇠이고 중근을 갖는다. "
            "안정한 표준 2차계 극점의 실수부는 -ζωn이다."
        )

        self.assertFalse(logic.get("fatal_error_detected"))

        fatal_findings = [
            finding
            for finding in logic.get("findings", [])
            if finding.get("severity") == "fatal"
        ]
        self.assertEqual([], fatal_findings)

    def test_wrong_critical_damping_statement_triggers_deterministic_fatal(self) -> None:
        logic = evaluate("ζ=1은 과감쇠라고 설명하였다.")

        self.assertTrue(logic.get("fatal_error_detected"))

        fatal_findings = [
            finding
            for finding in logic.get("findings", [])
            if finding.get("severity") == "fatal"
        ]

        self.assertTrue(fatal_findings)
        self.assertTrue(
            any(
                finding.get("id") == "zeta_one_as_overdamped"
                and "임계감쇠" in str(finding.get("correct_rule") or "")
                for finding in fatal_findings
            )
        )


if __name__ == "__main__":
    unittest.main()
