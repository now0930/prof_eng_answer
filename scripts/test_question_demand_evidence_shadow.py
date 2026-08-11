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


if __name__ == "__main__":
    unittest.main()
