#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import logic_llm_verifier


class _FakeResponse:
    def __init__(
        self,
        body: bytes,
        status: int = 200,
    ) -> None:
        self._body = body
        self.status = status

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> bool:
        return False

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        if size < 0:
            return self._body
        return self._body[:size]


class EndpointSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        logic_llm_verifier._reset_ollama_endpoint_selection_for_tests()

    def tearDown(self) -> None:
        logic_llm_verifier._reset_ollama_endpoint_selection_for_tests()

    def test_selects_first_healthy_endpoint_once(self):
        calls = []

        def fake_probe(url):
            calls.append(url)
            return url.endswith("good")

        with patch.object(
            logic_llm_verifier,
            "_ollama_url_candidates",
            return_value=[
                "http://bad",
                "http://good",
            ],
        ), patch.object(
            logic_llm_verifier,
            "_probe_ollama_endpoint",
            side_effect=fake_probe,
        ):
            first = logic_llm_verifier._select_ollama_base_url()
            second = logic_llm_verifier._select_ollama_base_url()

        self.assertEqual(first, "http://good")
        self.assertEqual(second, "http://good")
        self.assertEqual(
            calls,
            [
                "http://bad",
                "http://good",
            ],
        )

    def test_ordered_candidates_promote_selected_endpoint(self):
        logic_llm_verifier._remember_ollama_base_url(
            "http://good"
        )

        with patch.object(
            logic_llm_verifier,
            "_ollama_url_candidates",
            return_value=[
                "http://bad",
                "http://good",
                "http://other",
            ],
        ):
            ordered = (
                logic_llm_verifier
                ._ordered_ollama_url_candidates()
            )

        self.assertEqual(
            ordered,
            [
                "http://good",
                "http://bad",
                "http://other",
            ],
        )

    def test_call_avoids_chat_request_to_failed_probe_endpoint(self):
        urls = []

        def fake_urlopen(
            request,
            timeout,
        ):
            url = request.full_url
            urls.append(url)

            if url == "http://bad/api/tags":
                raise URLError("offline")

            if url == "http://good/api/tags":
                return _FakeResponse(
                    b'{"models":[]}'
                )

            if url == "http://good/api/chat":
                body = {
                    "message": {
                        "content": json.dumps(
                            {
                                "findings": [],
                            }
                        )
                    }
                }
                return _FakeResponse(
                    json.dumps(body).encode(
                        "utf-8"
                    )
                )

            raise AssertionError(
                f"unexpected URL: {url}"
            )

        with patch.object(
            logic_llm_verifier,
            "_ollama_url_candidates",
            return_value=[
                "http://bad",
                "http://good",
            ],
        ), patch.object(
            logic_llm_verifier.urllib.request,
            "urlopen",
            side_effect=fake_urlopen,
        ):
            result = logic_llm_verifier._call_ollama_json(
                "probe"
            )

        self.assertEqual(
            result,
            {
                "findings": [],
            },
        )
        self.assertNotIn(
            "http://bad/api/chat",
            urls,
        )
        self.assertIn(
            "http://good/api/chat",
            urls,
        )

    def test_failed_selected_chat_promotes_fallback(self):
        logic_llm_verifier._remember_ollama_base_url(
            "http://bad"
        )
        chat_urls = []

        def fake_urlopen(
            request,
            timeout,
        ):
            url = request.full_url

            if url.endswith("/api/tags"):
                return _FakeResponse(
                    b'{"models":[]}'
                )

            chat_urls.append(url)

            if url == "http://bad/api/chat":
                raise URLError("chat failed")

            if url == "http://good/api/chat":
                body = {
                    "message": {
                        "content": json.dumps(
                            {
                                "findings": [],
                            }
                        )
                    }
                }
                return _FakeResponse(
                    json.dumps(body).encode(
                        "utf-8"
                    )
                )

            raise AssertionError(
                f"unexpected URL: {url}"
            )

        with patch.object(
            logic_llm_verifier,
            "_ollama_url_candidates",
            return_value=[
                "http://bad",
                "http://good",
            ],
        ), patch.object(
            logic_llm_verifier.urllib.request,
            "urlopen",
            side_effect=fake_urlopen,
        ):
            result = logic_llm_verifier._call_ollama_json(
                "probe"
            )

        self.assertEqual(
            result,
            {
                "findings": [],
            },
        )
        self.assertEqual(
            chat_urls,
            [
                "http://bad/api/chat",
                "http://good/api/chat",
            ],
        )
        self.assertEqual(
            logic_llm_verifier._OLLAMA_SELECTED_BASE_URL,
            "http://good",
        )


class TimingTelemetryContractTests(unittest.TestCase):
    def test_phase2_timing_is_score_neutral_and_persisted_separately(self):
        source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)

        phase2 = [
            node
            for node in ast.walk(tree)
            if isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == "_phase2_postprocess_grade"
        ]

        self.assertEqual(
            len(phase2),
            1,
        )

        phase_source = ast.get_source_segment(
            source,
            phase2[0],
        ) or ""

        for marker in (
            "_phase20_timed",
            "_phase20_question_type_started",
            "_phase20_connection_started",
            "_phase20_gemini_started",
            "question_type_eval = _phase9_run_question_type_lens(",
            "connection_eval = _phase3_evaluate_connections(",
            "gemini_eval = _phase6_run_gemini_semantic_grader(",
            "gemini_semantic_grader",
            "logic_check",
            "grading_timing_evaluation.json",
            "total_phase2_seconds",
        ):
            self.assertIn(
                marker,
                phase_source,
            )

        self.assertNotIn(
            'grade["grading_timing_evaluation"]',
            phase_source,
        )
        self.assertNotIn(
            "'grading_timing_evaluation':",
            phase_source,
        )


if __name__ == "__main__":
    unittest.main()
