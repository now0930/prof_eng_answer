from __future__ import annotations

import unittest

import semantic_router_shadow as srs


TOPIC_ID = "topic_a"


class SemanticRouterGeneralModeContractTest(unittest.TestCase):
    def test_prompt_has_general_mode_exclusivity(self):
        prompt = srs._append_semantic_router_hard_contract(
            "BASE",
            "question",
            {
                "ok": True,
                "demands": [
                    {
                        "id": "D1",
                        "demand_id": "D1",
                        "text": "demand",
                    }
                ],
            },
            [
                {
                    "topic_id": TOPIC_ID,
                    "title": "Topic A",
                }
            ],
        )

        self.assertIn(
            "[SEMANTIC_ROUTER_GENERAL_MODE_HARD_CONTRACT_V1]",
            prompt,
        )
        self.assertIn(
            'routing_mode == "GENERAL"',
            prompt,
        )
        self.assertIn(
            "primary_topic_ids MUST be []",
            prompt,
        )
        self.assertIn(
            "supporting_topic_ids MUST be []",
            prompt,
        )
        self.assertIn(
            "MUST NOT assign any positive Topic role",
            prompt,
        )
        self.assertIn(
            "every valid question demand id MUST appear in uncovered_demand_ids",
            prompt,
        )
        self.assertIn(
            "If any positive Topic assignment remains, mode MUST NOT be GENERAL",
            prompt,
        )
        self.assertIn(
            "Mixed Topic + uncovered-demand coverage",
            prompt,
        )
        self.assertIn(
            "routing_mode MUST NOT be GENERAL merely because other demands are not",
            prompt,
        )
        self.assertIn(
            "Use SINGLE_TOPIC when exactly one Topic is positively selected",
            prompt,
        )
        self.assertIn(
            "Keep every non-owned demand in uncovered_demand_ids",
            prompt,
        )
        normalized_prompt = " ".join(prompt.split())
        self.assertIn(
            "Do NOT invent a new routing mode named HYBRID",
            normalized_prompt,
        )

    def test_consistent_general_payload_passes(self):
        calls = {"n": 0}

        def fake_llm(prompt):
            calls["n"] += 1
            return {
                "routing_mode": "GENERAL",
                "primary_topic_ids": [],
                "supporting_topic_ids": [],
                "demand_mappings": [],
                "uncovered_demand_ids": ["D1"],
                "confidence": 0.98,
                "reason": "general demand",
            }

        result = srs.semantic_route_shadow(
            "question",
            {
                "ok": True,
                "demands": [
                    {
                        "id": "D1",
                        "demand_id": "D1",
                        "text": "demand",
                    }
                ],
            },
            {
                "matched": True,
                "primary_reference": {
                    "topic_id": TOPIC_ID,
                    "title": "Topic A",
                },
                "candidates": [
                    {
                        "answer": {
                            "topic_id": TOPIC_ID,
                            "title": "Topic A",
                        },
                        "score": 1.0,
                    }
                ],
            },
            llm_call=fake_llm,
            enabled=True,
        )

        self.assertEqual(calls["n"], 1)
        self.assertTrue(result["ok"])
        self.assertEqual(result["routing_mode"], "GENERAL")
        self.assertEqual(result["primary_topic_ids"], [])
        self.assertEqual(result["supporting_topic_ids"], [])

    def test_inconsistent_general_payload_still_fails_closed(self):
        def fake_llm(prompt):
            return {
                "routing_mode": "GENERAL",
                "primary_topic_ids": [TOPIC_ID],
                "supporting_topic_ids": [],
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": TOPIC_ID,
                        "role": "PRIMARY",
                    }
                ],
                "uncovered_demand_ids": [],
                "confidence": 0.98,
                "reason": "invalid mixed mode",
            }

        result = srs.semantic_route_shadow(
            "question",
            {
                "ok": True,
                "demands": [
                    {
                        "id": "D1",
                        "demand_id": "D1",
                        "text": "demand",
                    }
                ],
            },
            {
                "matched": True,
                "primary_reference": {
                    "topic_id": TOPIC_ID,
                    "title": "Topic A",
                },
                "candidates": [
                    {
                        "answer": {
                            "topic_id": TOPIC_ID,
                            "title": "Topic A",
                        },
                        "score": 1.0,
                    }
                ],
            },
            llm_call=fake_llm,
            enabled=True,
        )

        self.assertFalse(result["ok"])
        self.assertIn(
            "GENERAL must not assign positive Topic roles",
            str(result.get("error")),
        )

    def test_no_candidate_general_remains_deterministic(self):
        calls = {"n": 0}

        def forbidden_llm(prompt):
            calls["n"] += 1
            raise AssertionError("LLM must not be called")

        result = srs.semantic_route_shadow(
            "general question",
            {
                "ok": True,
                "demands": [
                    {
                        "id": "D1",
                        "demand_id": "D1",
                        "text": "general demand",
                    }
                ],
            },
            {
                "matched": False,
                "primary_reference": None,
                "candidates": [],
            },
            llm_call=forbidden_llm,
            enabled=True,
        )

        self.assertEqual(calls["n"], 0)
        self.assertTrue(result["ok"])
        self.assertEqual(result["routing_mode"], "GENERAL")
        self.assertEqual(result["uncovered_demand_ids"], ["D1"])


if __name__ == "__main__":
    unittest.main()
