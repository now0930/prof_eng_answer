#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from unittest.mock import patch

import semantic_router_shadow as sr


RTD = "rtd_temperature_sensor_principle_pt100_wiring_compensation"
TC = (
    "thermocouple_temperature_sensor_seebeck_"
    "reference_junction_compensation"
)

DEMAND_RESULT = {
    "demands": [
        {"id": "D1", "text": "원리 비교"},
        {"id": "D2", "text": "오차 비교"},
        {"id": "D3", "text": "적용성 비교"},
    ]
}

CATALOG = [
    {"topic_id": RTD, "title": "RTD"},
    {"topic_id": TC, "title": "Thermocouple"},
]


class FakeResponse:
    def __init__(self, payload):
        self._raw = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._raw


def main():
    expected = {
        "routing_mode": "MULTI_TOPIC",
        "demand_mappings": [
            {
                "demand_id": "D1",
                "topic_id": RTD,
                "role": "PRIMARY",
                "confidence": 0.95,
            },
            {
                "demand_id": "D1",
                "topic_id": TC,
                "role": "PRIMARY",
                "confidence": 0.95,
            },
        ],
        "uncovered_demand_ids": [],
        "reason": "fixture",
    }

    envelope = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": json.dumps(
                                expected,
                                ensure_ascii=False,
                            )
                        }
                    ]
                }
            }
        ]
    }

    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["headers"] = {
            k.lower(): v
            for k, v in request.header_items()
        }
        captured["payload"] = json.loads(
            request.data.decode("utf-8")
        )
        return FakeResponse(envelope)

    with patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "test-secret-not-real",
            "GEMINI_MODEL": "gemini-3.1-flash-lite",
            "SEMANTIC_ROUTER_PROVIDER": "auto",
        },
        clear=False,
    ):
        with patch.object(
            sr.urllib.request,
            "urlopen",
            side_effect=fake_urlopen,
        ):
            result = sr._call_semantic_router_json(
                "semantic router prompt"
            )

    assert result == expected
    assert (
        captured["url"]
        == "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.1-flash-lite:generateContent"
    )
    assert captured["headers"]["x-goog-api-key"] == "test-secret-not-real"

    cfg = captured["payload"]["generationConfig"]
    assert cfg["temperature"] == 0.0
    assert cfg["topP"] == 1.0
    assert cfg["candidateCount"] == 1
    assert cfg["maxOutputTokens"] == 4096

    with patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "x",
            "SEMANTIC_ROUTER_PROVIDER": "auto",
        },
        clear=False,
    ):
        assert sr._semantic_router_should_use_gemini() is True

    with patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "x",
            "SEMANTIC_ROUTER_PROVIDER": "ollama",
        },
        clear=False,
    ):
        assert sr._semantic_router_should_use_gemini() is False

    with patch.dict(
        os.environ,
        {
            "GEMINI_API_KEY": "",
            "GOOGLE_API_KEY": "",
            "GOOGLE_GENERATIVE_AI_API_KEY": "",
            "SEMANTIC_ROUTER_PROVIDER": "gemini",
        },
        clear=False,
    ):
        try:
            sr._call_semantic_router_json("prompt")
        except ValueError as exc:
            assert "credential is missing" in str(exc)
        else:
            raise AssertionError("missing Gemini credential was accepted")

    hard = sr._append_semantic_router_hard_contract(
        "BASE",
        "RTD와 열전대를 비교",
        DEMAND_RESULT,
        CATALOG,
    )
    assert "This is NOT an exam-answering task." in hard
    assert "Do not score anything." in hard
    assert '"D1"' in hard
    assert '"D2"' in hard
    assert '"D3"' in hard
    assert RTD in hard
    assert TC in hard
    assert "MULTI_TOPIC" in hard
    assert "PRIMARY" in hard

    print("GEMINI_TRANSPORT_CREDENTIAL_CONTRACT=PASS")
    print("GEMINI_TRANSPORT_RUNTIME_MODEL_CONTRACT=PASS")
    print("GEMINI_TRANSPORT_ENDPOINT_CONTRACT=PASS")
    print("GEMINI_TRANSPORT_GENERATION_CONFIG_CONTRACT=PASS")
    print("GEMINI_TRANSPORT_AUTO_SELECTION=PASS")
    print("GEMINI_TRANSPORT_OLLAMA_OVERRIDE=PASS")
    print("GEMINI_TRANSPORT_MISSING_CREDENTIAL_GUARD=PASS")
    print("SEMANTIC_ROUTER_HARD_CONTRACT=PASS")
    print("ACTUAL_LLM_NETWORK_CALL_PERFORMED=false")
    print("PASS: semantic router Gemini transport regression")


if __name__ == "__main__":
    main()
