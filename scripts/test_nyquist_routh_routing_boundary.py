#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model_answer_router import find_model_answer_reference
from rubric_registry import load_model_answer_bank


NYQUIST = "nyquist_stability_criterion_gain_phase_margin"
ROUTH = "routh_hurwitz_stability_criterion_gain_range"
TOPICS = (NYQUIST, ROUTH)
PACK_ROOT = ROOT / "rubrics" / "topic_packs"
FIXTURE = ROOT / "scripts" / "fixtures" / "nyquist_routh_routing_boundary_cases.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"JSON root must be an object: {path}")
    return value


def source_bank() -> dict[str, Any]:
    return {
        "policy": {},
        "answers": [load_json(PACK_ROOT / topic / "model_answer.json") for topic in TOPICS],
    }


class NyquistRouthRoutingBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = load_json(FIXTURE)
        cls.banks = {
            "source": source_bank(),
            "generated": load_model_answer_bank(),
        }
        cls.question_type = {
            "primary_type": {"id": cls.fixture["question_type"]},
        }

    def test_reviewed_routing_cases(self) -> None:
        for case in self.fixture["cases"]:
            for bank_name, bank in self.banks.items():
                with self.subTest(case=case["id"], bank=bank_name):
                    result = find_model_answer_reference(
                        question_text=case["question"],
                        answer_text=case.get("answer", ""),
                        question_type_eval=self.question_type,
                        bank=bank,
                    )
                    self.assertEqual(result["routing_status"], case["expected_status"])
                    selected = (result.get("primary_reference") or {}).get("topic_id")
                    self.assertEqual(selected, case["expected_topic_id"])
                    if "expected_margin" in case:
                        self.assertEqual(result.get("score_margin"), case["expected_margin"])
                    forbidden = case.get("forbidden_candidate_topic_id")
                    if forbidden:
                        candidates = {
                            row["answer"]["topic_id"] for row in result.get("candidates", [])
                        }
                        self.assertNotIn(forbidden, candidates)

    def test_alias_owners_are_disjoint_and_method_specific(self) -> None:
        models = {row["topic_id"]: row for row in self.banks["source"]["answers"]}
        nyquist_aliases = set(models[NYQUIST]["routing_aliases"])
        routh_aliases = set(models[ROUTH]["routing_aliases"])
        self.assertFalse(nyquist_aliases & routh_aliases)
        self.assertNotIn("라우스 후르비츠", nyquist_aliases)
        for broad in (
            "특성방정식 안정도",
            "우반평면 극점",
            "이득 안정 범위",
            "제어기 이득 범위",
        ):
            self.assertNotIn(broad, nyquist_aliases)
            self.assertNotIn(broad, routh_aliases)

    def test_modern_question_contract_is_router_evidence(self) -> None:
        routh = next(
            row for row in self.banks["source"]["answers"] if row["topic_id"] == ROUTH
        )
        self.assertNotIn("question_examples", routh)
        result = find_model_answer_reference(
            question_text=routh["expected_question_patterns"][0]["pattern"],
            question_type_eval=self.question_type,
            bank={"policy": {}, "answers": [routh]},
        )
        reasons = "\n".join(result.get("match_reasons", []))
        self.assertTrue(result["matched"])
        self.assertIn("question example matched in question", reasons)
        self.assertGreaterEqual(result["top_score"], 100)


if __name__ == "__main__":
    unittest.main()
