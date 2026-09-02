from __future__ import annotations

from pathlib import Path
import tempfile
import json
import unittest

import question_demand_evidence as qde


class QuestionDemandEvidenceShadowTests(unittest.TestCase):
    def test_version_and_no_score_connection_markers(self):
        self.assertEqual(
            qde.QUESTION_DEMAND_EVIDENCE_VERSION,
            "QUESTION_DEMAND_EVIDENCE_V1",
        )

        source = Path(qde.__file__).read_text(encoding="utf-8")

        self.assertNotIn("total_range", source)
        self.assertNotIn("reconcile_grade_score", source)
        self.assertNotIn("layer_scores[", source)
        self.assertNotIn("total_score", source)
        self.assertNotIn("final_score", source)

    def test_token_link_is_deterministic(self):
        assets = {
            "patterns": [
                {
                    "source_field": "expected_question_patterns",
                    "index": 0,
                    "text": "Pt100 3선식 리드선 저항 보상",
                    "anchor_refs": ["A-3WIRE"],
                },
                {
                    "source_field": "expected_question_patterns",
                    "index": 1,
                    "text": "열전대 기준접점 보상",
                    "anchor_refs": ["A-TC"],
                },
            ],
            "anchors": [
                {
                    "anchor_id": "A-3WIRE",
                    "text": "3선식 RTD 리드선 저항 보상",
                },
                {
                    "anchor_id": "A-TC",
                    "text": "열전대 기준접점",
                },
            ],
        }

        result = qde._rank_pattern_links(
            "3선식 RTD의 리드선 저항 보상 원리",
            assets,
        )

        self.assertEqual(
            result["method"],
            "model_pattern_anchor_refs",
        )
        self.assertEqual(
            result["anchor_ids"],
            ["A-3WIRE"],
        )

    def test_mean_linked_anchor_level_is_arithmetic_mean(self):
        source = Path(qde.__file__).read_text(encoding="utf-8")

        self.assertIn(
            "sum(levels) / len(levels)",
            source,
        )
        self.assertNotIn(
            "demand_level = max(levels)",
            source,
        )

    def test_explicit_mapping_requires_exact_demand_identity(self):
        self.assertTrue(
            callable(
                qde._load_explicit_demand_anchor_mapping
            )
        )

        source = Path(qde.__file__).read_text(encoding="utf-8")

        self.assertIn(
            "expected_demands",
            source,
        )
        self.assertIn(
            "primary_topic_ids",
            source,
        )
        self.assertNotIn(
            "question_sha",
            source,
        )

    def test_multi_topic_without_mapping_is_not_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp)

            (
                session / "semantic_router_shadow.json"
            ).write_text(
                json.dumps(
                    {
                        "routing_mode": "MULTI_TOPIC",
                        "primary_topic_ids": ["A", "B"],
                        "demand_mappings": [],
                    }
                ),
                encoding="utf-8",
            )

            routing = qde._load_routing(session)

            self.assertEqual(
                routing["demand_topic_map"],
                {},
            )

    def test_general_route_is_valid_and_has_no_topic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp)
            (session / "semantic_router_shadow.json").write_text(
                json.dumps({
                    "routing_mode": "GENERAL",
                    "primary_topic_ids": [],
                    "demand_mappings": [],
                }),
                encoding="utf-8",
            )
            routing = qde._load_routing(session)
            self.assertEqual(routing["routing_mode"], "GENERAL")
            self.assertEqual(routing["primary_topic_ids"], [])
            self.assertEqual(routing["demand_topic_map"], {})

    def test_missing_manual_cache_uses_runtime_question_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, demands = qde._load_canonical_demands(
                Path(tmp),
                "V-Model과 단위·통합·시스템 시험을 설명하시오.",
            )
        self.assertEqual(source, "runtime:question_demand_contract")
        self.assertEqual(len(demands), 4)
        self.assertTrue(all(row["demand_id"] for row in demands))

    def test_runtime_contract_evidence_is_diagnostic_only(self):
        source = Path(qde.__file__).read_text(encoding="utf-8")
        self.assertIn(
            '"score_eligible": not str(canonical_path).startswith("runtime:")',
            source,
        )

    def test_runtime_lexical_fallback_requires_two_exact_tokens(self):
        scenario = qde._lexical_demand_mention(
            "반응기 과압력의 원인과 시나리오 경계를 정의한다.",
            "반응기 과압력 시나리오의 SIL 결정 과정을 설명한다.",
        )
        self.assertTrue(scenario["covered"])
        self.assertGreaterEqual(scenario["matched_token_count"], 2)

        generic = qde._lexical_demand_mention(
            "잔여빈도와 허용빈도로 요구 RRF와 목표 SIL을 결정한다.",
            "SIL을 언급한다.",
        )
        self.assertFalse(generic["covered"])
        self.assertEqual(generic["matched_tokens"], ["sil"])


if __name__ == "__main__":
    unittest.main()
