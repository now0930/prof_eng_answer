from __future__ import annotations

import ast
import json
import os
import unittest
from pathlib import Path
from unittest import mock

import clova_grader
import gemini_grader
import originality_grader
from llm_sampling import (
    SAMPLING_CONTRACT_VERSION,
    build_llm_request_contract,
)


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ):
        return None

    def read(self):
        return self.body


def gemini_response(parsed):
    return FakeResponse(
        {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps(
                                    parsed,
                                    ensure_ascii=False,
                                )
                            }
                        ]
                    }
                }
            ]
        }
    )


def clova_response(parsed):
    return FakeResponse(
        {
            "result": {
                "message": {
                    "content": json.dumps(
                        parsed,
                        ensure_ascii=False,
                    )
                }
            }
        }
    )


class DeterministicSamplingTests(
    unittest.TestCase
):
    def test_contract_is_stable(self):
        args = {
            "provider": "gemini",
            "model": "model-a",
            "prompt": "same prompt",
            "requested_sampling": {
                "temperature": 0.0,
                "top_p": 1.0,
            },
            "applied_sampling": {
                "temperature": 0.0,
                "top_p": 1.0,
            },
            "unsupported_settings": [
                "seed",
                "top_k",
            ],
        }

        first = build_llm_request_contract(
            **args
        )
        second = build_llm_request_contract(
            **args
        )

        self.assertEqual(first, second)
        self.assertEqual(
            first["version"],
            SAMPLING_CONTRACT_VERSION,
        )
        self.assertEqual(
            len(first["prompt_hash"]),
            64,
        )
        self.assertEqual(
            len(first["request_hash"]),
            64,
        )

    def test_prompt_changes_hash(self):
        first = build_llm_request_contract(
            provider="gemini",
            model="model-a",
            prompt="prompt-a",
            requested_sampling={},
            applied_sampling={
                "temperature": 0.0,
            },
        )
        second = build_llm_request_contract(
            provider="gemini",
            model="model-a",
            prompt="prompt-b",
            requested_sampling={},
            applied_sampling={
                "temperature": 0.0,
            },
        )

        self.assertNotEqual(
            first["request_hash"],
            second["request_hash"],
        )

    def test_gemini_payload_and_metadata(self):
        captured = []

        def fake_urlopen(request, timeout=None):
            del timeout
            captured.append(
                bytes(request.data)
            )
            return gemini_response(
                {
                    "version": "test",
                    "confidence": "medium",
                    "overall_comment": "test",
                    "layers": [],
                }
            )

        base_call = (
            gemini_grader
            ._ORIGINAL_GEMINI_SEMANTIC_GRADE_PHASE18
        )

        with mock.patch.dict(
            os.environ,
            {
                "GEMINI_API_KEY": "test-key",
                "GEMINI_MODEL": "test-model",
            },
            clear=False,
        ), mock.patch(
            "gemini_grader."
            "urllib.request.urlopen",
            side_effect=fake_urlopen,
        ):
            result = base_call(
                question_text="문제",
                answer_text="답안",
                scoring_model={
                    "layers": [],
                },
                subject_rubric={},
                rater_profile={
                    "raters": [],
                },
                volume={},
                fact_eval={},
                connection_eval={},
            )

        payload = json.loads(
            captured[0].decode("utf-8")
        )
        config = payload[
            "generationConfig"
        ]

        self.assertEqual(
            config["temperature"],
            0.0,
        )
        self.assertEqual(
            config["topP"],
            1.0,
        )
        self.assertEqual(
            config["candidateCount"],
            1,
        )
        self.assertEqual(
            result["llm_request"]["model"],
            "test-model",
        )

    def test_gemini_retry_payload_identical(self):
        captured = []
        count = 0

        def fake_urlopen(request, timeout=None):
            nonlocal count
            del timeout
            count += 1
            captured.append(
                bytes(request.data)
            )

            if count == 1:
                raise TimeoutError(
                    "timed out"
                )

            return gemini_response(
                {
                    "version": "test",
                    "confidence": "medium",
                    "overall_comment": "test",
                    "layers": [],
                }
            )

        with mock.patch.dict(
            os.environ,
            {
                "GEMINI_API_KEY": "test-key",
                "GEMINI_MODEL": "test-model",
            },
            clear=False,
        ), mock.patch(
            "gemini_grader."
            "urllib.request.urlopen",
            side_effect=fake_urlopen,
        ), mock.patch(
            "time.sleep",
            return_value=None,
        ):
            result = (
                gemini_grader
                .gemini_semantic_grade(
                    question_text="문제",
                    answer_text="답안",
                    scoring_model={
                        "layers": [],
                    },
                    subject_rubric={},
                    rater_profile={
                        "raters": [],
                    },
                    volume={},
                    fact_eval={},
                    connection_eval={},
                )
            )

        self.assertTrue(result.get("ok"))
        self.assertEqual(
            captured[0],
            captured[1],
        )

    def test_originality_contract(self):
        captured = []

        def fake_urlopen(request, timeout=None):
            del timeout
            captured.append(
                bytes(request.data)
            )
            return gemini_response(
                {
                    "version": "test",
                    "overall_score": 1.0,
                    "overall_comment": "test",
                }
            )

        with mock.patch.dict(
            os.environ,
            {
                "GEMINI_API_KEY": "test-key",
                "GEMINI_MODEL": "test-model",
            },
            clear=False,
        ), mock.patch(
            "originality_grader."
            "urllib.request.urlopen",
            side_effect=fake_urlopen,
        ):
            result = (
                originality_grader
                .gemini_originality_evaluate(
                    question_text="문제",
                    answer_text="답안",
                    layer_scores=[],
                    volume={},
                    fact_eval={},
                    connection_eval={},
                )
            )

        payload = json.loads(
            captured[0].decode("utf-8")
        )
        config = payload[
            "generationConfig"
        ]

        self.assertEqual(
            config["temperature"],
            0.0,
        )
        self.assertEqual(
            config["topP"],
            1.0,
        )
        self.assertEqual(
            config["candidateCount"],
            1,
        )
        self.assertEqual(
            result["llm_request"]["provider"],
            "gemini",
        )

    def test_clova_exact_impl_and_retry(self):
        source = Path(
            "clova_grader.py"
        ).read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)

        definitions = [
            node
            for node in tree.body
            if isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == "clova_semantic_grade"
        ]

        self.assertEqual(
            len(definitions),
            2,
        )

        first = ast.get_source_segment(
            source,
            definitions[0],
        ) or ""
        second = ast.get_source_segment(
            source,
            definitions[1],
        ) or ""

        self.assertIn(
            "sampling_contract",
            first,
        )
        self.assertIn(
            "ensure_question_type_coverage",
            second,
        )

        captured = []
        count = 0

        def fake_urlopen(request, timeout=None):
            nonlocal count
            del timeout
            count += 1
            captured.append(
                bytes(request.data)
            )

            if count == 1:
                raise TimeoutError(
                    "timed out"
                )

            return clova_response(
                {
                    "ok": True,
                    "semantic_scores": {},
                }
            )

        with mock.patch.dict(
            os.environ,
            {
                "CLOVA_API_KEY": "test-key",
                "CLOVA_MODEL": "test-model",
                "CLOVA_RETRIES": "1",
            },
            clear=False,
        ), mock.patch(
            "clova_grader."
            "urllib.request.urlopen",
            side_effect=fake_urlopen,
        ), mock.patch(
            "clova_grader.time.sleep",
            return_value=None,
        ):
            result = (
                clova_grader
                .clova_semantic_grade(
                    question_text="문제",
                    answer_text="답안",
                )
            )

        self.assertEqual(
            captured[0],
            captured[1],
        )

        body = json.loads(
            captured[0].decode("utf-8")
        )

        self.assertEqual(
            body["temperature"],
            0.0,
        )
        self.assertEqual(
            body["topP"],
            1.0,
        )
        self.assertEqual(
            result["llm_request"]["provider"],
            "clova",
        )

    def test_grade_metadata_persistence(self):
        source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"llm_request": '
            'gemini_eval.get("llm_request")',
            source,
        )
        self.assertIn(
            '"llm_request": '
            'result.get("llm_request")',
            source,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
