from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from logic_check_evaluator import (
    _evaluate_topic_fatal_checks_with_llm,
)


def topic_with_two_rules() -> dict:
    return {
        "topic_id": "stage20_batch_test_topic",
        "fatal_checks": [
            {
                "id": "rule_a",
                "message": "A 오류",
                "correct_rule": "A 정정",
                "affected_layers": ["C"],
                "recommended_ceiling": 11.0,
            },
            {
                "id": "rule_b",
                "message": "B 오류",
                "correct_rule": "B 정정",
                "affected_layers": ["C"],
                "recommended_ceiling": 12.0,
            },
        ],
    }


class Stage20LogicBatchContractTests(unittest.TestCase):
    def test_two_rules_use_one_primary_call(self) -> None:
        captured = []

        def fake_call(
            prompt,
            *,
            format_schema=None,
        ):
            captured.append(
                (prompt, format_schema)
            )
            return {
                "findings": [
                    {
                        "rule_id": "rule_b",
                        "severity": "fatal",
                        "evidence": "B 오류를 직접 주장한다",
                        "confidence": 0.96,
                    }
                ]
            }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=fake_call,
        ) as mocked:
            findings = (
                _evaluate_topic_fatal_checks_with_llm(
                    "B 오류를 직접 주장한다",
                    topic_with_two_rules(),
                )
            )

        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(len(captured), 1)

        schema = captured[0][1]
        rule_schema = (
            schema["properties"]["findings"]
            ["items"]["properties"]["rule_id"]
        )

        self.assertEqual(
            rule_schema["enum"],
            ["rule_a", "rule_b"],
        )
        self.assertEqual(
            schema["properties"]["findings"]["maxItems"],
            2,
        )

        fatal = [
            row
            for row in findings
            if row.get("severity") == "fatal"
        ]
        self.assertEqual(len(fatal), 1)
        self.assertEqual(
            fatal[0]["source_rule_id"],
            "rule_b",
        )
        self.assertEqual(
            fatal[0]["engine"],
            "topic_fatal_semantic_llm_batch_v1",
        )
        self.assertEqual(
            fatal[0]["semantic_rule_evaluation"]["batch_size"],
            2,
        )

    def test_invalid_response_repairs_batch_once(self) -> None:
        invalid = {
            "verdict": "fatal",
            "reason": "findings 누락",
        }
        repaired = {
            "findings": [
                {
                    "rule_id": "rule_a",
                    "severity": "major",
                    "evidence": "A 오류를 직접 주장한다",
                    "confidence": 0.92,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=[invalid, repaired],
        ) as mocked:
            findings = (
                _evaluate_topic_fatal_checks_with_llm(
                    "A 오류를 직접 주장한다",
                    topic_with_two_rules(),
                )
            )

        self.assertEqual(mocked.call_count, 2)
        repair_prompt = mocked.call_args_list[1].args[0]
        self.assertIn("rule_a", repair_prompt)
        self.assertIn("rule_b", repair_prompt)
        self.assertIn(
            "새로운 rule id를 만들지 말고",
            repair_prompt,
        )
        self.assertEqual(
            findings[0]["source_rule_id"],
            "rule_a",
        )

    def test_unknown_rule_is_fail_open_diagnostic(self) -> None:
        response = {
            "findings": [
                {
                    "rule_id": "new_rule",
                    "severity": "fatal",
                    "evidence": "새로운 오류",
                    "confidence": 0.99,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ) as mocked:
            findings = (
                _evaluate_topic_fatal_checks_with_llm(
                    "새로운 오류",
                    topic_with_two_rules(),
                )
            )

        self.assertEqual(mocked.call_count, 1)
        self.assertFalse(
            any(
                row.get("severity") == "fatal"
                for row in findings
            )
        )
        self.assertEqual(
            findings[-1]["diagnostic"]["reason"],
            "batch_evaluation_partial",
        )

    def test_corrective_context_is_excluded_without_diagnostic(
        self,
    ) -> None:
        response = {
            "findings": [
                {
                    "rule_id": "rule_a",
                    "severity": "fatal",
                    "evidence": "A 오류가 아니다",
                    "confidence": 0.99,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ) as mocked:
            findings = (
                _evaluate_topic_fatal_checks_with_llm(
                    "주의 오류: A 오류가 아니다.",
                    topic_with_two_rules(),
                )
            )

        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(findings, [])

    def test_single_rule_compatibility_shape_is_preserved(
        self,
    ) -> None:
        topic = {
            "fatal_checks": [
                {
                    "id": "single_rule",
                    "message": "단일 오류",
                    "correct_rule": "단일 정정",
                    "affected_layers": ["C"],
                }
            ]
        }
        response = {
            "findings": [
                {
                    "rule_id": "single_rule",
                    "severity": "fatal",
                    "evidence": "단일 오류를 주장한다",
                    "confidence": 0.95,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ) as mocked:
            findings = (
                _evaluate_topic_fatal_checks_with_llm(
                    "단일 오류를 주장한다",
                    topic,
                )
            )

        self.assertEqual(mocked.call_count, 1)
        self.assertEqual(
            findings[0]["engine"],
            "topic_fatal_semantic_llm_per_rule_v1",
        )
        self.assertEqual(
            findings[0]["semantic_rule_evaluation"]["mode"],
            "single_rule",
        )
        self.assertEqual(
            findings[0]["semantic_rule_evaluation"]["batch_size"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
