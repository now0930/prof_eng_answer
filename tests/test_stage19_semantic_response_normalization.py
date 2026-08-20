from __future__ import annotations

import unittest
from unittest.mock import patch

import json

from logic_check_evaluator import (
    _evaluate_topic_fatal_checks_with_llm,
    _normalize_topic_fatal_semantic_response,
    _topic_fatal_semantic_json_schema,
)
from logic_llm_verifier import _call_ollama_json


RULE_ID = "sw04_fatal_misra_is_unit_test_tool"

TOPIC_CHECK = {
    "topic_id": (
        "instrumentation_control_software_lifecycle_"
        "v_model_traceability_verification_validation"
    ),
    "topic_name": "V-Model 및 SIL 소프트웨어 검증",
    "fatal_checks": [
        {
            "id": RULE_ID,
            "message": "MISRA를 단위시험 도구로 분류하였다.",
            "correct_rule": (
                "MISRA C는 코딩 지침 및 정적 분석 근거이다."
            ),
            "recommended_ceiling": 14.5,
            "affected_layers": ["C"],
            "wrong_patterns": [],
        }
    ],
}


class Stage19SemanticResponseNormalizationTests(unittest.TestCase):
    def test_nested_checks_are_flattened(self):
        normalized = _normalize_topic_fatal_semantic_response(
            {
                "result": {
                    "verdict": "fatal",
                    "confidence": 0.94,
                    "checks": [
                        {
                            "rule_id": RULE_ID,
                            "status": "fatal",
                            "asserted": True,
                            "candidate_id": "C1",
                            "evidence": "단일 모듈 / xUnit, MISRA",
                            "reason": "MISRA를 시험 도구로 분류함",
                            "correction": "MISRA는 코딩 지침이다.",
                        }
                    ],
                }
            }
        )
        self.assertEqual(normalized["verdict"], "fatal")
        self.assertEqual(normalized["confidence"], 0.94)
        self.assertEqual(len(normalized["findings"]), 1)
        self.assertEqual(
            normalized["findings"][0]["rule_id"],
            RULE_ID,
        )

    def test_unasserted_fatal_is_excluded(self):
        normalized = _normalize_topic_fatal_semantic_response(
            {
                "verdict": "fatal",
                "confidence": 0.99,
                "checks": [
                    {
                        "rule_id": RULE_ID,
                        "status": "fatal",
                        "asserted": False,
                    }
                ],
            }
        )
        self.assertEqual(normalized["findings"], [])

    def test_pass_check_is_excluded(self):
        normalized = _normalize_topic_fatal_semantic_response(
            {
                "verdict": "pass",
                "confidence": 0.99,
                "checks": [
                    {
                        "rule_id": RULE_ID,
                        "status": "pass",
                        "asserted": False,
                    }
                ],
            }
        )
        self.assertEqual(normalized["findings"], [])

    def test_existing_findings_are_preserved(self):
        original = {
            "verdict": "major",
            "confidence": 0.8,
            "findings": [
                {
                    "rule_id": RULE_ID,
                    "severity": "major",
                }
            ],
        }
        normalized = _normalize_topic_fatal_semantic_response(
            original
        )
        self.assertEqual(
            normalized["findings"],
            original["findings"],
        )

    def test_live_evaluator_path_accepts_checks_shape(self):
        response = {
            "result": {
                "verdict": "fatal",
                "confidence": 0.94,
                "checks": [
                    {
                        "rule_id": RULE_ID,
                        "status": "fatal",
                        "asserted": True,
                        "candidate_id": "C1",
                        "evidence": "단일 모듈 / xUnit, MISRA",
                        "reason": "MISRA를 시험 도구로 분류함",
                        "correction": "MISRA는 코딩 지침이다.",
                    }
                ],
            }
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding["source_rule_id"], RULE_ID)
        self.assertEqual(finding["severity"], "fatal")
        self.assertEqual(finding["confidence"], 0.94)
        self.assertNotEqual(
            finding["id"],
            "topic_fatal_semantic_llm_error",
        )



class Stage19SemanticSchemaRepairTests(unittest.TestCase):
    def test_valid_first_response_does_not_retry(self):
        valid = {
            "verdict": "pass",
            "confidence": 0.95,
            "reason": "직접 오개념 없음",
            "findings": [],
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=valid,
        ) as mocked:
            findings = _evaluate_topic_fatal_checks_with_llm(
                "정상 답안",
                TOPIC_CHECK,
            )

        self.assertEqual(findings, [])
        self.assertEqual(mocked.call_count, 1)

    def test_invalid_then_valid_response_repairs_once(self):
        invalid = {
            "verdict": "fatal",
            "reason": "MISRA 분류 오류",
        }
        repaired = {
            "verdict": "fatal",
            "confidence": 0.94,
            "checks": [
                {
                    "rule_id": RULE_ID,
                    "status": "fatal",
                    "asserted": True,
                    "candidate_id": "C1",
                    "evidence": "xUnit, MISRA",
                    "reason": "MISRA를 시험 도구로 분류함",
                    "correction": "MISRA는 코딩 지침이다.",
                }
            ],
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=[invalid, repaired],
        ) as mocked:
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["source_rule_id"], RULE_ID)
        self.assertEqual(findings[0]["severity"], "fatal")

    def test_invalid_then_invalid_remains_fail_open(self):
        invalid_first = {
            "verdict": "fatal",
            "reason": "형식 누락",
        }
        invalid_second = {
            "verdict": "fatal",
            "reason": "여전히 형식 누락",
            "suggestions": ["schema를 지켜야 함"],
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=[invalid_first, invalid_second],
        ) as mocked:
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(len(findings), 1)
        self.assertEqual(
            findings[0]["id"],
            "topic_fatal_semantic_llm_error",
        )
        self.assertEqual(
            findings[0]["diagnostic"]["reason"],
            "findings_field_missing",
        )

    def test_repair_prompt_uses_existing_rule_ids(self):
        invalid = {
            "verdict": "fatal",
            "reason": "형식 누락",
        }
        repaired = {
            "verdict": "pass",
            "confidence": 0.9,
            "checks": [
                {
                    "rule_id": RULE_ID,
                    "status": "pass",
                    "asserted": False,
                }
            ],
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=[invalid, repaired],
        ) as mocked:
            findings = _evaluate_topic_fatal_checks_with_llm(
                "정상 답안",
                TOPIC_CHECK,
            )

        self.assertEqual(findings, [])
        self.assertEqual(mocked.call_count, 2)
        repair_prompt = mocked.call_args_list[1].args[0]
        self.assertIn(RULE_ID, repair_prompt)
        self.assertIn("새로운 rule id를 만들지 말고", repair_prompt)



class Stage19OllamaStructuredOutputTests(unittest.TestCase):
    def test_schema_uses_only_existing_rule_ids(self):
        schema = _topic_fatal_semantic_json_schema(
            TOPIC_CHECK
        )

        self.assertIn(
            "findings",
            schema["required"],
        )
        check_rule = schema[
            "properties"
        ]["checks"]["items"]["properties"]["rule_id"]
        finding_rule = schema[
            "properties"
        ]["findings"]["items"]["properties"]["rule_id"]

        self.assertEqual(
            check_rule["enum"],
            [RULE_ID],
        )
        self.assertEqual(
            finding_rule["enum"],
            [RULE_ID],
        )

    def test_ollama_payload_contains_format_schema(self):
        schema = _topic_fatal_semantic_json_schema(
            TOPIC_CHECK
        )

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "verdict": "pass",
                                    "confidence": 0.9,
                                    "reason": "정상",
                                    "checks": [],
                                    "findings": [],
                                },
                                ensure_ascii=False,
                            )
                        }
                    },
                    ensure_ascii=False,
                ).encode("utf-8")

        with patch(
            "urllib.request.urlopen",
            return_value=Response(),
        ) as mocked:
            result = _call_ollama_json(
                "JSON으로 답하라",
                format_schema=schema,
            )

        request = mocked.call_args.args[0]
        payload = json.loads(
            request.data.decode("utf-8")
        )

        self.assertEqual(
            payload["format"],
            schema,
        )
        self.assertEqual(
            result["findings"],
            [],
        )

    def test_live_evaluator_passes_schema_on_initial_call(self):
        captured = []

        def fake_call(
            prompt,
            *,
            format_schema=None,
        ):
            captured.append(format_schema)
            return {
                "verdict": "pass",
                "confidence": 0.9,
                "reason": "정상",
                "checks": [],
                "findings": [],
            }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=fake_call,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "정상 답안",
                TOPIC_CHECK,
            )

        self.assertEqual(findings, [])
        self.assertEqual(len(captured), 1)
        self.assertIn(
            "findings",
            captured[0]["required"],
        )



class Stage19PerRuleEvaluationTests(unittest.TestCase):
    def test_two_rules_are_evaluated_separately(self):
        topic = {
            "fatal_checks": [
                {
                    "id": "rule_a",
                    "message": "A 오류",
                    "correct_rule": "A 정정",
                    "affected_layers": ["C"],
                },
                {
                    "id": "rule_b",
                    "message": "B 오류",
                    "correct_rule": "B 정정",
                    "affected_layers": ["C"],
                },
            ]
        }
        schemas = []

        def fake_call(
            prompt,
            *,
            format_schema=None,
        ):
            schemas.append(format_schema)
            return {
                "findings": [],
            }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=fake_call,
        ) as mocked:
            findings = _evaluate_topic_fatal_checks_with_llm(
                "정상 답안",
                topic,
            )

        self.assertEqual(findings, [])
        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(
            schemas[0]["properties"]["findings"]
            ["items"]["properties"]["rule_id"]["const"],
            "rule_a",
        )
        self.assertEqual(
            schemas[1]["properties"]["findings"]
            ["items"]["properties"]["rule_id"]["const"],
            "rule_b",
        )

    def test_exact_answer_evidence_creates_existing_finding_shape(self):
        response = {
            "findings": [
                {
                    "rule_id": RULE_ID,
                    "severity": "fatal",
                    "evidence": "xUnit, MISRA",
                    "confidence": 0.95,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(
            finding["id"],
            f"llm_semantic_{RULE_ID}",
        )
        self.assertEqual(
            finding["source_rule_id"],
            RULE_ID,
        )
        self.assertEqual(
            finding["engine"],
            "topic_fatal_semantic_llm_per_rule_v1",
        )
        self.assertEqual(
            finding["semantic_rule_evaluation"]["batch_size"],
            1,
        )

    def test_evidence_not_in_answer_is_fail_open(self):
        response = {
            "findings": [
                {
                    "rule_id": RULE_ID,
                    "severity": "fatal",
                    "evidence": "답안에 없는 문장",
                    "confidence": 0.99,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        fatal = [
            row
            for row in findings
            if row.get("severity") == "fatal"
        ]
        self.assertEqual(fatal, [])
        self.assertEqual(
            findings[-1]["diagnostic"]["reason"],
            "per_rule_evaluation_partial",
        )

    def test_low_confidence_is_fail_open(self):
        response = {
            "findings": [
                {
                    "rule_id": RULE_ID,
                    "severity": "fatal",
                    "evidence": "xUnit, MISRA",
                    "confidence": 0.5,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "단일 모듈 / xUnit, MISRA",
                TOPIC_CHECK,
            )

        self.assertFalse(
            any(
                row.get("severity") == "fatal"
                for row in findings
            )
        )

    def test_corrective_context_is_excluded(self):
        response = {
            "findings": [
                {
                    "rule_id": RULE_ID,
                    "severity": "fatal",
                    "evidence": "MISRA는 단위시험 도구가 아니다",
                    "confidence": 0.99,
                }
            ]
        }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            return_value=response,
        ):
            findings = _evaluate_topic_fatal_checks_with_llm(
                "주의 오류: MISRA는 단위시험 도구가 아니다.",
                TOPIC_CHECK,
            )

        self.assertFalse(
            any(
                row.get("severity") == "fatal"
                for row in findings
            )
        )



def _run_stage19z_v3_submission_context_tests():
    import ast
    import inspect
    import textwrap

    import grading_agents
    from grading_identity import (
        build_grading_identity,
    )
    from question_contract import (
        build_question_contract,
    )

    helper = (
        grading_agents
        ._phase2_extract_submission_context
    )

    bracketed = (
        "[문제] SIS의 SIL과 소프트웨어 MC/DC를 "
        "V-Model 관점에서 비교하시오.\n"
        "1. V-Model 추적성을 설명한다.\n"
        "2. SIL과 MC/DC의 차이를 설명한다."
    )
    bracketed_question, bracketed_answer = helper(
        bracketed
    )
    assert "SIS의 SIL" in bracketed_question
    assert "V-Model 추적성" in bracketed_answer
    assert (
        bracketed_question
        != bracketed_answer
    )

    colon = (
        "문제: SIS의 SIL과 소프트웨어 MC/DC를 "
        "비교하시오.\n"
        "1. SIL을 설명한다.\n"
        "2. MC/DC를 설명한다."
    )
    colon_question, colon_answer = helper(
        colon
    )
    assert "SIS의 SIL" in colon_question
    assert "SIL을 설명한다" in colon_answer
    assert colon_question != colon_answer

    plain = (
        "1. 기능안전의 개념을 설명한다.\n"
        "2. 검증 절차를 정리한다."
    )
    plain_question, plain_answer = helper(plain)
    assert plain_question == plain
    assert plain_answer == plain

    identity = build_grading_identity(
        bracketed_question,
        bracketed_answer,
    )
    assert (
        identity.normalized_question
        != identity.normalized_answer
    )

    phase2_source = textwrap.dedent(
        inspect.getsource(
            grading_agents
            ._phase2_postprocess_grade
        )
    )
    phase2_tree = ast.parse(phase2_source)

    def _call_name(call):
        if isinstance(call.func, ast.Name):
            return call.func.id

        if isinstance(call.func, ast.Attribute):
            return call.func.attr

        return ""

    def _target_text(node):
        targets = (
            node.targets
            if isinstance(node, ast.Assign)
            else [node.target]
        )

        if len(targets) != 1:
            return ""

        return ast.unparse(targets[0])

    def _assignment_value(node):
        if isinstance(
            node,
            (ast.Assign, ast.AnnAssign),
        ):
            return node.value

        return None

    def _resolve_argument(
        call,
        function,
        parameter_name,
    ):
        parameters = list(
            inspect.signature(function).parameters
        )

        for keyword in call.keywords:
            if keyword.arg == parameter_name:
                return keyword.value

        if parameter_name in parameters:
            index = parameters.index(
                parameter_name
            )

            if index < len(call.args):
                return call.args[index]

        return None

    parent = {}

    for node in ast.walk(phase2_tree):
        for child in ast.iter_child_nodes(node):
            parent[id(child)] = node

    def _nearest_assignment(node):
        current = node

        while id(current) in parent:
            current = parent[id(current)]

            if isinstance(
                current,
                (ast.Assign, ast.AnnAssign),
            ):
                return current

            if isinstance(
                current,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                break

        return None

    calls = [
        node
        for node in ast.walk(phase2_tree)
        if isinstance(node, ast.Call)
    ]

    helper_assignments = []

    for node in ast.walk(phase2_tree):
        if not isinstance(
            node,
            (ast.Assign, ast.AnnAssign),
        ):
            continue

        value = _assignment_value(node)

        if (
            isinstance(value, ast.Call)
            and _call_name(value)
            == "_phase2_extract_submission_context"
        ):
            helper_assignments.append(node)

    assert len(helper_assignments) == 1
    assert (
        _target_text(helper_assignments[0])
        == "(question_text, answer_text)"
    )

    residual_calls = [
        call
        for call in calls
        if _call_name(call)
        in {
            "_phase3_extract_question_text",
            "_phase3_extract_answer_text",
        }
    ]
    residual_targets = []

    for call in residual_calls:
        assignment = _nearest_assignment(call)
        residual_targets.append(
            _target_text(assignment)
            if assignment is not None
            else ""
        )

    assert all(
        target
        not in {
            "question_text",
            "answer_text",
        }
        for target in residual_targets
    )
    assert residual_targets == [
        "_question_for_difficulty_final"
    ]

    identity_calls = [
        call
        for call in calls
        if _call_name(call)
        == "build_grading_identity"
    ]
    assert len(identity_calls) == 1

    identity_question = _resolve_argument(
        identity_calls[0],
        build_grading_identity,
        "question_text",
    )
    identity_answer = _resolve_argument(
        identity_calls[0],
        build_grading_identity,
        "answer_text",
    )

    assert isinstance(identity_question, ast.Name)
    assert identity_question.id == "question_text"
    assert isinstance(identity_answer, ast.Name)
    assert identity_answer.id == "answer_text"

    identity_assignment_target = None

    for node in ast.walk(phase2_tree):
        if not isinstance(
            node,
            (ast.Assign, ast.AnnAssign),
        ):
            continue

        value = _assignment_value(node)

        if (
            isinstance(value, ast.Call)
            and _call_name(value)
            == "build_grading_identity"
        ):
            identity_assignment_target = (
                _target_text(node)
            )

    assert identity_assignment_target == (
        "grading_identity"
    )

    identity_dict_valid = False

    for node in ast.walk(phase2_tree):
        if not isinstance(
            node,
            (ast.Assign, ast.AnnAssign),
        ):
            continue

        if _target_text(node) != (
            "grading_identity_dict"
        ):
            continue

        value = _assignment_value(node)

        if not isinstance(value, ast.Call):
            continue

        if not isinstance(
            value.func,
            ast.Attribute,
        ):
            continue

        if value.func.attr != "to_dict":
            continue

        if not isinstance(
            value.func.value,
            ast.Name,
        ):
            continue

        if value.func.value.id != (
            "grading_identity"
        ):
            continue

        identity_dict_valid = True

    assert identity_dict_valid

    contract_calls = [
        call
        for call in calls
        if _call_name(call)
        == "build_question_contract"
    ]
    assert len(contract_calls) == 1

    contract_identity = _resolve_argument(
        contract_calls[0],
        build_question_contract,
        "grading_identity",
    )
    assert isinstance(
        contract_identity,
        ast.Name,
    )
    assert contract_identity.id == (
        "grading_identity_dict"
    )


if __name__ == "__main__":
    _run_stage19z_v3_submission_context_tests()
    unittest.main()
