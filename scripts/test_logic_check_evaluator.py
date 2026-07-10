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



class SemanticCorrectiveContextRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _topic_check() -> dict:
        return {
            "topic_id": (
                "feedback_system_closed_loop_"
                "sensitivity_steady_state_error"
            ),
            "topic_name": "피드백 시스템",
            "fatal_checks": [
                {
                    "id": (
                        "high_loop_gain_always_stable"
                    ),
                    "severity": "fatal",
                    "message": (
                        "루프 이득을 높이면 항상 "
                        "안정해진다고 설명함."
                    ),
                    "correct_rule": (
                        "높은 루프 이득은 안정여유를 "
                        "감소시킬 수도 있다."
                    ),
                    "recommended_ceiling": 10.0,
                    "wrong_patterns": [
                        (
                            r"(루프\s*이득|loop\s*gain)"
                            r".{0,40}(높일수록|클수록)"
                            r".{0,30}(항상|무조건)"
                            r".{0,20}(안정|좋)"
                        )
                    ],
                }
            ],
        }

    @staticmethod
    def _verdict(
        evidence: str,
    ) -> dict:
        return {
            "verdict": "fatal",
            "confidence": 1.0,
            "findings": [
                {
                    "rule_id": (
                        "high_loop_gain_always_stable"
                    ),
                    "severity": "fatal",
                    "confidence": 1.0,
                    "evidence": evidence,
                    "message": (
                        "루프 이득 증가가 항상 안정성을 "
                        "보장한다고 주장함."
                    ),
                    "correct_rule": (
                        "높은 루프 이득은 안정여유를 "
                        "감소시킬 수도 있다."
                    ),
                }
            ],
            "reason": "test",
        }

    def test_corrective_context_is_not_semantic_fatal(
        self,
    ) -> None:
        from unittest.mock import patch

        import logic_check_evaluator

        evidence = (
            "루프 이득을 높이면 항상 안정해진다고"
        )

        answer = (
            "주의할 오류: "
            "루프 이득을 높이면 항상 안정해진다고 "
            "단정하면 안 된다."
        )

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=self._verdict(evidence),
        ):
            findings = (
                logic_check_evaluator
                ._evaluate_topic_fatal_checks_with_llm(
                    answer,
                    self._topic_check(),
                )
            )

        self.assertEqual(
            findings,
            [],
        )

    def test_direct_assertion_remains_semantic_fatal(
        self,
    ) -> None:
        from unittest.mock import patch

        import logic_check_evaluator

        evidence = (
            "루프 이득을 높이면 항상 안정해진다"
        )

        answer = (
            "루프 이득을 높이면 항상 안정해진다."
        )

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=self._verdict(evidence),
        ):
            findings = (
                logic_check_evaluator
                ._evaluate_topic_fatal_checks_with_llm(
                    answer,
                    self._topic_check(),
                )
            )

        self.assertEqual(
            len(findings),
            1,
        )

        self.assertEqual(
            findings[0].get("source_rule_id"),
            "high_loop_gain_always_stable",
        )

        self.assertEqual(
            findings[0].get("severity"),
            "fatal",
        )


class SystemTypeClosedLoopOrderRegressionTest(
    unittest.TestCase
):
    TOPIC_ID = (
        "feedback_system_closed_loop_"
        "sensitivity_steady_state_error"
    )

    @classmethod
    def _grade(cls) -> dict:
        return {
            "topic_id": cls.TOPIC_ID,
            "logic_check_topic_id": cls.TOPIC_ID,
            "total_score": 20.0,
            "max_score": 25.0,
            "difficulty_strategy": {
                "topic_id": cls.TOPIC_ID,
            },
        }

    def test_llm_profile_fatal_is_applied(
        self,
    ) -> None:
        answer = (
            "폐루프가 2차이면 "
            "Type 2 시스템이다."
        )

        profile_result = {
            "applicable": True,
            "engine": "llm_verifier_profile_v1",
            "topic_id": self.TOPIC_ID,
            "verdict": "fatal",
            "confidence": 0.98,
            "checks": [
                {
                    "rule_id": (
                        "system_type_from_"
                        "closed_loop_order"
                    ),
                    "status": "fatal",
                    "asserted": True,
                    "candidate_id": "C1",
                    "evidence": answer,
                    "reason": (
                        "시스템 형을 폐루프 "
                        "차수로 정의했다."
                    ),
                    "correction": (
                        "시스템 형은 개루프 "
                        "원점 극 수이다."
                    ),
                    "confidence": 0.98,
                },
            ],
            "findings": [
                {
                    "id": (
                        "llm_profile_system_type_"
                        "from_closed_loop_order"
                    ),
                    "source_rule_id": (
                        "system_type_from_"
                        "closed_loop_order"
                    ),
                    "severity": "fatal",
                    "message": (
                        "시스템 형을 폐루프 "
                        "차수로 잘못 정의했다."
                    ),
                    "correct_rule": (
                        "시스템 형은 개루프 "
                        "L(s)의 원점 극 수이다."
                    ),
                    "affected_layers": ["C"],
                    "evidence": answer,
                    "confidence": 0.98,
                    "recommended_ceiling": 10.0,
                },
            ],
            "fatal_error_detected": True,
            "recommended_ceiling": 10.0,
            "mode": "fatal",
            "reason": "직접적인 핵심 오개념",
        }

        with patch(
            "logic_llm_verifier."
            "verify_logic_with_llm",
            return_value=profile_result,
        ) as verifier, patch.object(
            logic_check_evaluator,
            "_evaluate_topic_fatal_checks_with_llm",
            side_effect=AssertionError(
                "LLM-only topic used legacy "
                "semantic fallback"
            ),
        ):
            output = (
                logic_check_evaluator
                .attach_logic_check_to_grade(
                    self._grade(),
                    answer,
                )
            )

        verifier.assert_called_once()

        evaluation = output.get(
            "logic_check_evaluation",
            {},
        )

        fatal_ids = {
            str(
                finding.get(
                    "source_rule_id"
                )
                or finding.get("id")
                or ""
            )
            for finding in evaluation.get(
                "findings",
                [],
            )
            if (
                isinstance(finding, dict)
                and finding.get("severity")
                == "fatal"
            )
        }

        self.assertTrue(
            evaluation.get(
                "fatal_error_detected"
            )
        )

        self.assertEqual(
            evaluation.get("topic_id"),
            self.TOPIC_ID,
        )

        self.assertIn(
            (
                "system_type_from_"
                "closed_loop_order"
            ),
            fatal_ids,
        )

        self.assertEqual(
            (
                evaluation.get(
                    "score_policy"
                )
                or {}
            ).get(
                "recommended_ceiling"
            ),
            10.0,
        )

    def test_llm_profile_pass_does_not_apply_fatal(
        self,
    ) -> None:
        answer = (
            "시스템 형은 개루프 L(s)의 "
            "원점 극 수로 정한다."
        )

        profile_result = {
            "applicable": True,
            "engine": "llm_verifier_profile_v1",
            "topic_id": self.TOPIC_ID,
            "verdict": "pass",
            "confidence": 0.99,
            "checks": [
                {
                    "rule_id": (
                        "system_type_from_"
                        "closed_loop_order"
                    ),
                    "status": "pass",
                    "asserted": False,
                    "candidate_id": "C1",
                    "evidence": answer,
                    "reason": (
                        "개루프 원점 극 수로 "
                        "정확히 정의했다."
                    ),
                    "correction": (
                        "시스템 형은 개루프 "
                        "원점 극 수이다."
                    ),
                    "confidence": 0.99,
                },
            ],
            "findings": [],
            "fatal_error_detected": False,
            "recommended_ceiling": None,
            "mode": "pass",
            "reason": "핵심 정의가 정확함",
        }

        with patch(
            "logic_llm_verifier."
            "verify_logic_with_llm",
            return_value=profile_result,
        ) as verifier, patch.object(
            logic_check_evaluator,
            "_evaluate_topic_fatal_checks_with_llm",
            side_effect=AssertionError(
                "LLM-only topic used legacy "
                "semantic fallback"
            ),
        ):
            output = (
                logic_check_evaluator
                .attach_logic_check_to_grade(
                    self._grade(),
                    answer,
                )
            )

        verifier.assert_called_once()

        evaluation = output.get(
            "logic_check_evaluation",
            {},
        )

        self.assertFalse(
            evaluation.get(
                "fatal_error_detected"
            )
        )

        self.assertEqual(
            evaluation.get("mode"),
            "pass",
        )

        self.assertEqual(
            evaluation.get("findings"),
            [],
        )





class LogicCandidateKeyTermFallbackRegressionTest(
    unittest.TestCase
):
    def test_empty_rules_extract_key_term_context(
        self,
    ) -> None:
        import logic_llm_verifier as verifier

        profile = {
            "candidate_extraction": {
                "max_candidates": 20,
                "nearby_window": 2,
                "key_terms": [
                    "첫 열",
                    "부호 변화",
                    "우반평면",
                ],
                "rules": [],
            }
        }

        answer = """
Routh 배열 첫 열의 부호 변화 횟수는
좌반평면 극점의 개수이다.
따라서 첫 열에서 부호가 두 번 변하면
좌반평면 극점이 두 개 존재한다.
""".strip()

        candidates = (
            verifier
            .extract_logic_evidence_candidates(
                answer,
                profile,
            )
        )

        self.assertGreaterEqual(
            len(candidates),
            1,
        )
        self.assertTrue(
            all(
                candidate.get("kind")
                == "key_term_context"
                for candidate in candidates
            )
        )
        self.assertTrue(
            any(
                "좌반평면 극점의 개수" in str(
                    candidate.get("text")
                )
                for candidate in candidates
            )
        )

    def test_empty_rules_without_key_term_match_is_empty(
        self,
    ) -> None:
        import logic_llm_verifier as verifier

        profile = {
            "candidate_extraction": {
                "max_candidates": 20,
                "nearby_window": 2,
                "key_terms": [
                    "첫 열",
                    "부호 변화",
                ],
                "rules": [],
            }
        }

        candidates = (
            verifier
            .extract_logic_evidence_candidates(
                "센서 교정 주기를 설명한다.",
                profile,
            )
        )

        self.assertEqual(
            candidates,
            [],
        )

    def test_explicit_rules_preserve_rule_only_behavior(
        self,
    ) -> None:
        import logic_llm_verifier as verifier

        profile = {
            "candidate_extraction": {
                "max_candidates": 20,
                "nearby_window": 2,
                "key_terms": [
                    "첫 열",
                    "부호 변화",
                ],
                "rules": [
                    {
                        "kind": "claim",
                        "type": "line_regex",
                        "regex": (
                            "절대로-일치하지-않는-패턴"
                        ),
                    }
                ],
            }
        }

        candidates = (
            verifier
            .extract_logic_evidence_candidates(
                "첫 열의 부호 변화 의미를 설명한다.",
                profile,
            )
        )

        self.assertEqual(
            candidates,
            [],
        )


if __name__ == "__main__":
    unittest.main()
