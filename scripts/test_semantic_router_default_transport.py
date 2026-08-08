from __future__ import annotations

import json
import unittest
from unittest.mock import patch

import semantic_router_shadow as sr


TOPIC = "topic_fixture"


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self) -> bytes:
        return json.dumps(
            self._payload,
            ensure_ascii=False,
        ).encode("utf-8")


def _single_topic_payload() -> dict:
    return {
        "routing_mode": "SINGLE_TOPIC",
        "demand_mappings": [
            {
                "demand_id": "D1",
                "topic_id": TOPIC,
                "role": "PRIMARY",
                "confidence": 0.99,
            }
        ],
        "uncovered_demand_ids": [],
        "reason": "fixture",
    }


def _demand_result() -> dict:
    return {
        "ok": True,
        "status": "ok",
        "demands": [
            {
                "id": "D1",
                "text": "Explain the fixture topic.",
            }
        ],
    }


def _rule_result() -> dict:
    return {
        "candidates": [
            {
                "score": 100,
                "question_score": 100,
                "match_reasons": ["fixture"],
                "answer": {
                    "topic_id": TOPIC,
                    "title": "Fixture topic",
                },
            }
        ],
    }


class SemanticRouterDefaultTransportTest(unittest.TestCase):
    def test_transport_uses_structured_json_contract(self):
        captured = {}

        def fake_urlopen(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return _FakeResponse(
                {
                    "message": {
                        "content": json.dumps(
                            _single_topic_payload(),
                            ensure_ascii=False,
                        )
                    }
                }
            )

        with patch.object(
            sr,
            "SEMANTIC_ROUTER_OLLAMA_URL",
            "http://ollama:11434",
        ), patch.object(
            sr,
            "SEMANTIC_ROUTER_MODEL",
            "fixture-model",
        ), patch.object(
            sr,
            "SEMANTIC_ROUTER_TIMEOUT",
            17,
        ), patch.object(
            sr.urllib.request,
            "urlopen",
            side_effect=fake_urlopen,
        ):
            result = sr._call_semantic_router_json(
                "fixture prompt"
            )

        self.assertEqual(
            result,
            _single_topic_payload(),
        )

        request = captured["request"]
        self.assertEqual(
            request.full_url,
            "http://ollama:11434/api/chat",
        )
        self.assertEqual(captured["timeout"], 17)

        payload = json.loads(
            request.data.decode("utf-8")
        )

        self.assertEqual(
            payload["model"],
            "fixture-model",
        )
        self.assertFalse(payload["stream"])
        response_schema = payload["format"]
        self.assertIsInstance(response_schema, dict)
        self.assertEqual(response_schema["type"], "object")
        self.assertFalse(
            response_schema["additionalProperties"]
        )
        self.assertEqual(
            set(response_schema["required"]),
            {
                "routing_mode",
                "demand_mappings",
                "uncovered_demand_ids",
                "reason",
            },
        )
        self.assertEqual(
            set(
                response_schema["properties"][
                    "routing_mode"
                ]["enum"]
            ),
            {
                "SINGLE_TOPIC",
                "MULTI_TOPIC",
                "GENERAL",
                "AMBIGUOUS",
            },
        )
        mapping_schema = (
            response_schema["properties"][
                "demand_mappings"
            ]["items"]
        )
        self.assertFalse(
            mapping_schema["additionalProperties"]
        )
        self.assertEqual(
            set(mapping_schema["required"]),
            {
                "demand_id",
                "topic_id",
                "role",
                "confidence",
            },
        )
        self.assertEqual(
            set(
                mapping_schema["properties"][
                    "role"
                ]["enum"]
            ),
            {
                "PRIMARY",
                "SUPPORTING",
                "NONE",
            },
        )
        self.assertEqual(
            payload["options"]["temperature"],
            0.0,
        )
        self.assertEqual(
            payload["options"]["top_p"],
            1.0,
        )
        self.assertEqual(
            payload["options"]["top_k"],
            64,
        )
        self.assertEqual(
            payload["options"]["seed"],
            0,
        )
        self.assertEqual(
            payload["messages"][0]["role"],
            "system",
        )
        self.assertIn(
            "Topic Router v2",
            payload["messages"][0]["content"],
        )
        self.assertIn(
            "Do not answer the examination question",
            payload["messages"][0]["content"],
        )
        self.assertEqual(
            payload["messages"][1],
            {
                "role": "user",
                "content": "fixture prompt",
            },
        )

    def test_transport_rejects_non_object_content(self):
        with patch.object(
            sr.urllib.request,
            "urlopen",
            return_value=_FakeResponse(
                {
                    "message": {
                        "content": "[]",
                    }
                }
            ),
        ):
            with self.assertRaisesRegex(
                ValueError,
                "must be JSON object",
            ):
                sr._call_semantic_router_json(
                    "fixture prompt"
                )

    def test_default_route_uses_dedicated_transport(self):
        with patch.object(
            sr,
            "_call_semantic_router_json",
            return_value=_single_topic_payload(),
        ) as mocked:
            result = sr.semantic_route_shadow(
                question_text="fixture question",
                question_demand_result=_demand_result(),
                rule_result=_rule_result(),
                enabled=True,
            )

        mocked.assert_called_once()
        self.assertTrue(result["ok"])
        self.assertEqual(
            result["routing_mode"],
            "SINGLE_TOPIC",
        )
        self.assertEqual(
            result["primary_topic_ids"],
            [TOPIC],
        )
        self.assertTrue(result["llm_called"])
        self.assertFalse(
            result["student_answer_used"]
        )
        self.assertTrue(
            result["legacy_router_authoritative"]
        )


if __name__ == "__main__":
    unittest.main()
