"""Provider transport checks without real network calls or credentials."""

import io
import json
import urllib.error
from unittest.mock import patch

import pytest

from scripts.run_qualitative_de_repeatability import ProviderHTTPError, _argon_call, _gemini_call


def _prompt():
    answer = "조건에 따라 방법 A를 선택하고 기준 입력으로 검증한다."
    return json.dumps({
        "instruction": "D/E만 제안하세요.", "answer": answer,
        "requirements": [{"status": "SATISFIED", "owner_topic_id": "topic_a",
                          "source_span": {"start": 0, "end": len(answer)}}],
    }, ensure_ascii=False)


def test_gemini_transport_is_json_bounded_and_resolves_zero_scores():
    captured = []
    proposal = {
        "criteria": [{"criterion_id": key, "score": 0, "reason": "근거 없음",
                      "topic_id": "topic_a", "evidence_id": None}
                     for key in ("D1", "D2", "D3", "E1", "E2")],
        "interview_questions": [], "abc_observations": [],
    }

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *_):
            self.close()

    def fake_urlopen(request, timeout):
        captured.append(request)
        body = {"candidates": [{"finishReason": "STOP", "content": {
            "parts": [{"text": json.dumps(proposal)}]}}]}
        return Response(json.dumps(body).encode())

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = json.loads(_gemini_call("test-model", "test-key", 0, 4096)(_prompt()))
    sent = json.loads(captured[0].data)
    assert sent["generationConfig"]["responseMimeType"] == "application/json"
    assert sent["generationConfig"]["maxOutputTokens"] == 4096
    assert captured[0].get_header("X-goog-api-key") == "test-key"
    assert "test-key" not in json.dumps(sent)
    assert all(row["quote"] is None and row["start"] is None and row["end"] is None
               for row in result["criteria"])


def test_gemini_http_error_does_not_expose_provider_body():
    error = urllib.error.HTTPError("https://example.invalid", 402, "secret error", {}, io.BytesIO(b"private"))
    with patch("urllib.request.urlopen", side_effect=error):
        with pytest.raises(ProviderHTTPError, match="provider_http_402") as raised:
            _gemini_call("test-model", "test-key", 0)(_prompt())
    assert "private" not in str(raised.value)


def test_argon_uses_interactions_api_and_completed_model_output():
    captured = []
    proposal = {
        "criteria": [{"criterion_id": key, "score": 0, "reason": "근거 없음",
                      "topic_id": "topic_a", "evidence_id": None}
                     for key in ("D1", "D2", "D3", "E1", "E2")],
        "interview_questions": [], "abc_observations": [],
    }

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *_):
            self.close()

    def fake_urlopen(request, timeout):
        captured.append((request, timeout))
        body = {"status": "completed", "steps": [{"type": "model_output",
                "content": [{"type": "text", "text": json.dumps(proposal)}]}]}
        return Response(json.dumps(body).encode())

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = json.loads(_argon_call("test-key")(_prompt()))
    request, timeout = captured[0]
    sent = json.loads(request.data)
    assert request.full_url.endswith("/v1beta/interactions")
    assert timeout == 120
    assert sent["model"] == "gemini-4-argon"
    assert sent["generation_config"] == {"max_output_tokens": 32768,
                                          "thinking_level": "medium"}
    assert sent["response_format"]["mime_type"] == "application/json"
    assert "test-key" not in json.dumps(sent)
    assert all(row["score"] == 0 for row in result["criteria"])
