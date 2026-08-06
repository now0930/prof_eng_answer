#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "historian_mes_it_ot_integration_industrial_data_quality_realtime_processing"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC}.md"

FILES = {
    "readme": PACK / "README.md",
    "fact": PACK / "fact_anchor.json",
    "logic": PACK / "logic_check.json",
    "model": PACK / "model_answer.json",
    "importance": PACK / "topic_importance.json",
    "sheet": SHEET,
}

REQUIRED_ANCHORS = {
    "historian_time_series_role",
    "mes_execution_role",
    "erp_business_role",
    "isa95_hierarchy_interface",
    "source_timestamp_event_time",
    "quality_code_semantics",
    "store_and_forward_recovery",
    "compression_deadband_tradeoff",
    "metadata_context_role",
    "information_model_semantics",
    "batch_genealogy",
    "semantic_interoperability",
    "topic_boundary_transport_model",
}

REQUIRED_FATALS = {
    "historian_backup_only",
    "mes_equals_erp",
    "isa95_wire_protocol",
    "mes_replaces_realtime_control",
    "arrival_time_equals_event_time",
    "bad_uncertain_as_valid_zero",
    "compression_deadband_lossless",
    "store_forward_guarantees_no_loss",
    "protocol_guarantees_semantics",
    "realtime_zero_latency",
}

BROAD_ALIASES = {
    "historian", "mes", "erp", "isa-95", "edge", "gateway",
    "timestamp", "metadata", "streaming", "data quality"
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SW11SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        for name, path in FILES.items():
            if not path.is_file():
                raise AssertionError(f"missing {name}: {path}")
        cls.fact = load_json(FILES["fact"])
        cls.logic = load_json(FILES["logic"])
        cls.model = load_json(FILES["model"])
        cls.importance = load_json(FILES["importance"])
        cls.sheet = FILES["sheet"].read_text(encoding="utf-8")
        cls.readme = FILES["readme"].read_text(encoding="utf-8")

    def test_01_all_allowed_files_exist(self) -> None:
        for name, path in FILES.items():
            with self.subTest(name=name):
                self.assertTrue(path.is_file(), path)

    def test_02_topic_and_modern_root_contracts(self) -> None:
        for row in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(row["topic_id"], TOPIC)
        self.assertEqual(self.fact["schema_version"], "fact_anchor.v1")
        self.assertEqual(
            self.logic["schema_version"], "topic_pack.logic_check.v1"
        )
        self.assertEqual(
            self.model["schema_version"], "topic_pack.model_answer.v1"
        )
        self.assertEqual(
            self.importance["schema_version"],
            "topic_pack.topic_importance.v1",
        )

    def test_03_anchor_schema_and_counts(self) -> None:
        self.assertEqual(len(self.fact["anchors"]), 30)
        required = {
            "id", "anchor_id", "statement", "importance", "keywords",
            "core_terms", "accepted_explanations", "rejected_explanations",
            "grading_notes", "source_basis", "claim", "description",
        }
        for row in self.fact["anchors"]:
            self.assertTrue(required.issubset(row), required - set(row))
            self.assertEqual(row["id"], row["anchor_id"])
            self.assertEqual(row["statement"], row["claim"])
            self.assertEqual(row["claim"], row["description"])

    def test_04_fatal_and_major_contracts(self) -> None:
        self.assertEqual(len(self.fact["fatal_wrong_claims"]), 16)
        self.assertEqual(
            len(self.logic["llm_profile"]["major_checks"]), 12
        )
        for row in self.fact["fatal_wrong_claims"]:
            self.assertEqual(row["severity"], "fatal")
            self.assertEqual(row["affected_layers"], ["C"])

    def test_05_required_anchor_and_fatal_ids(self) -> None:
        anchor_ids = {row["id"] for row in self.fact["anchors"]}
        fatal_ids = {row["id"] for row in self.fact["fatal_wrong_claims"]}
        self.assertTrue(REQUIRED_ANCHORS.issubset(anchor_ids))
        self.assertTrue(REQUIRED_FATALS.issubset(fatal_ids))

    def test_06_llm_profile_single_owner_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        self.assertFalse(deterministic["enabled"])
        for key in ("fatal_checks", "major_checks", "question_type_checks"):
            self.assertEqual(deterministic[key], [])
        profile = self.logic["llm_profile"]
        self.assertTrue(profile["enabled"])
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(profile["score_policy"]["affected_layers"], ["C"])

    def test_07_model_anchor_reference_contract(self) -> None:
        anchor_ids = {row["id"] for row in self.fact["anchors"]}
        outline_union: set[str] = set()
        for row in self.model["expected_question_patterns"]:
            self.assertTrue(set(row["required_anchor_ids"]).issubset(anchor_ids))
        for row in self.model["recommended_outline"]:
            refs = set(row["anchor_refs"])
            self.assertTrue(refs.issubset(anchor_ids))
            outline_union.update(refs)
        self.assertEqual(outline_union, anchor_ids)

    def test_08_historian_mes_erp_isa95_boundaries(self) -> None:
        for marker in (
            "Historian은 단순 백업 저장소가 아니며",
            "MES는 생산지시를 현장 실행으로 전개",
            "ERP는 주문, 계획, 자재, 원가",
            "ISA-95",
            "단일 통신 Protocol이 아니다",
        ):
            self.assertIn(marker, self.sheet)

    def test_09_time_and_quality_contracts(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic},
            ensure_ascii=False,
        )
        for marker in (
            "Event Time",
            "Time alignment",
            "Quality Code",
            "Bad",
            "Uncertain",
            "arrival_time_equals_event_time",
            "quality_code_discard",
        ):
            self.assertIn(marker, combined)

    def test_10_formula_markers(self) -> None:
        for marker in (
            "C_{\\mathrm{complete}}",
            "t_{\\mathrm{available}}",
            "E_{\\mathrm{align}}",
            "N_{\\mathrm{raw}}",
            "B(t)",
            "C_{\\mathrm{trace}}",
        ):
            self.assertIn(marker, self.sheet)

    def test_11_compression_and_store_forward_guards(self) -> None:
        combined = json.dumps(
            {"fact": self.fact, "logic": self.logic},
            ensure_ascii=False,
        )
        for marker in (
            "compression_deadband_lossless",
            "store_forward_guarantees_no_loss",
            "Quality 변경",
            "Backlog",
            "중복",
        ):
            self.assertIn(marker, combined + self.sheet)

    def test_12_semantic_context_and_genealogy(self) -> None:
        for marker in (
            "Tag Naming",
            "Namespace",
            "Metadata",
            "Master Data",
            "Information Model",
            "Semantic Interoperability",
            "Batch Genealogy",
        ):
            self.assertIn(marker, self.sheet)

    def test_13_sw07_sw12_boundaries(self) -> None:
        for marker in (
            "SW-07과의 경계",
            "SW-12와의 경계",
            "Protocol Frame",
            "Feature Engineering",
            "학습·추론",
        ):
            self.assertIn(marker, self.sheet)

    def test_14_routing_alias_specificity(self) -> None:
        aliases = self.model["routing_aliases"]
        self.assertEqual(len(aliases), 14)
        normalized = {x.strip().lower() for x in aliases}
        self.assertTrue(BROAD_ALIASES.isdisjoint(normalized))
        self.assertTrue(any("quality code" in x.lower() for x in aliases))
        self.assertTrue(any("genealogy" in x.lower() for x in aliases))
        self.assertTrue(any("semantic" in x.lower() for x in aliases))

    def test_15_importance_and_model_depth(self) -> None:
        self.assertEqual(self.importance["difficulty"], "THEORY_CORE")
        self.assertEqual(
            self.importance["selection_importance"], "CORE_MUST_PREPARE"
        )
        self.assertEqual(
            self.importance["question_type"], "PRINCIPLE_INTERPRETATION"
        )
        self.assertEqual(len(self.model["expected_question_patterns"]), 10)
        self.assertEqual(len(self.model["recommended_outline"]), 8)
        self.assertGreaterEqual(len(self.model["high_score_points"]), 13)
        self.assertGreaterEqual(len(self.model["common_missing_points"]), 14)

    def test_16_no_forbidden_runtime_output_contract(self) -> None:
        combined = self.readme + self.sheet
        self.assertIn("Generated Bank promotion: excluded", combined)
        self.assertIn(
            "Production Python/Common Router modification: excluded",
            combined,
        )
        self.assertNotIn("rubrics/generated/", combined)
        self.assertNotIn("model_answer_router.py", combined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
