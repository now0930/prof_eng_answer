from __future__ import annotations

import json
import unittest
from pathlib import Path


TOPIC_ID = "instrumentation_system_design_basis_codes_standards_specification_deviation_management"
REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = REPO / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


class InstrumentationDesignBasisTopicPackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load("fact_anchor.json")
        cls.logic = load("logic_check.json")
        cls.model = load("model_answer.json")
        cls.importance = load("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = SHEET.read_text(encoding="utf-8")
        cls.serialized = json.dumps(
            {
                "fact": cls.fact,
                "logic": cls.logic,
                "model": cls.model,
                "importance": cls.importance,
            },
            ensure_ascii=False,
        )

    def test_01_identity_question_type_and_difficulty_contract(self) -> None:
        for obj in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(obj["topic_id"], TOPIC_ID)

        self.assertEqual(self.fact["question_type_hint"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(self.model["question_type"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(self.importance["question_type"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(self.importance["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(self.importance["selection_importance"], "NORMAL")

    def test_02_anchor_integrity_and_outline_full_coverage(self) -> None:
        anchors = self.fact["anchors"]
        anchor_ids = [row["id"] for row in anchors]
        self.assertEqual(len(anchors), 22)
        self.assertEqual(len(set(anchor_ids)), 22)

        outline = self.model["recommended_outline"]
        self.assertEqual(len(outline), 8)
        covered: set[str] = set()
        for row in outline:
            refs = row["anchor_refs"]
            self.assertTrue(refs)
            self.assertTrue(set(refs) <= set(anchor_ids))
            covered.update(refs)

        self.assertEqual(covered, set(anchor_ids))

    def test_03_governing_requirements_design_basis_and_document_precedence(self) -> None:
        required = (
            "governing requirements",
            "Design Basis",
            "document precedence",
            "project cut-off",
            "Code",
            "Standard",
            "Specification",
        )
        for term in required:
            self.assertIn(term, self.serialized)

        # A correct negative teaching sentence contains the prohibited concept
        # as a substring. Validate the semantic rule directly instead.
        self.assertIn(
            "특정 표준의 최신판이 모든 기존설비에 자동 소급된다고 단정하지 않는다.",
            self.readme,
        )
        fatal = {
            row["id"]: row for row in self.fact["fatal_wrong_claims"]
        }["design_fatal_latest_retroactive"]
        self.assertIn("항상 최신 표준판을 기존 설비에 소급 적용해야 한다", fatal["claim"])
        self.assertIn("법규", fatal["correction"])
        self.assertIn("계약", fatal["correction"])
        self.assertIn("프로젝트 기준일", fatal["correction"])

    def test_04_design_document_chain_and_interface_traceability(self) -> None:
        required = (
            "P&ID",
            "Instrument Index",
            "Datasheet",
            "I/O List",
            "ISA-5.1",
            "traceability",
        )
        for term in required:
            self.assertIn(term, self.serialized)

        # Design Basis must be translated into controlled engineering deliverables,
        # not treated as a stand-alone narrative with no downstream linkage.
        self.assertIn("Specification", self.serialized)
        self.assertIn("Datasheet", self.serialized)

    def test_05_vendor_deviation_requires_formal_evaluation_and_authority(self) -> None:
        required = (
            "vendor deviation",
            "TBE",
            "impact assessment",
            "approval authority",
            "disposition",
            "closure",
        )
        for term in required:
            self.assertIn(term, self.serialized)

        combined = self.sheet + "\n" + self.readme + "\n" + self.serialized
        self.assertIn("Vendor와 담당자의 구두합의만으로 baseline을 바꾸지 않는다", combined)

    def test_06_moc_and_project_deviation_boundaries_remain_distinct(self) -> None:
        self.assertIn("Management of Change", self.serialized)
        self.assertIn("MOC", self.serialized)
        self.assertIn("deviation", self.serialized.lower())

        # Existing-plant change governance belongs in the answer boundary,
        # but the pack must not collapse project deviation and MOC into one concept.
        combined = self.sheet + "\n" + self.readme + "\n" + self.serialized
        self.assertIn("deviation", combined.lower())
        self.assertIn("MOC", combined)

    def test_07_fat_sat_as_built_and_handover_close_the_traceability_loop(self) -> None:
        for term in ("FAT", "SAT", "as-built", "traceability"):
            self.assertIn(term, self.serialized)

        # Closeout must be represented as verification + controlled document update,
        # not as approval-only paperwork.
        self.assertIn("closure", self.serialized)
        self.assertIn("document", self.serialized.lower())

    def test_08_llm_semantic_guardrails_without_deterministic_fatal_scoring(self) -> None:
        det = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]

        self.assertFalse(det["enabled"])
        self.assertEqual(det["fatal_checks"], [])
        self.assertEqual(det["major_checks"], [])
        self.assertEqual(det["question_type_checks"], [])

        self.assertTrue(profile["enabled"])
        self.assertFalse(profile["candidate_extraction"]["enabled"])
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(profile["score_policy"]["affected_layers"], ["C"])

        self.assertEqual(
            [row["id"] for row in profile["fatal_conditions"]],
            [row["id"] for row in self.fact["fatal_wrong_claims"]],
        )

    def test_09_routing_aliases_unique_and_neighbor_topic_ownership_is_preserved(self) -> None:
        aliases = self.model["routing_aliases"]
        self.assertEqual(len(aliases), 18)
        normalized = [" ".join(a.casefold().split()) for a in aliases]
        self.assertEqual(len(normalized), len(set(normalized)))

        ownership_topics = (
            "hazardous_area_explosion_protection_intrinsic_safety_equipment_selection",
            "sis_sil_safety_software_independence_systematic_failure_verification_validation",
            "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation",
            "control_software_project_engineering_documents_fat_sat_commissioning_acceptance",
            "pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative",
            "configuration_change_release_backup_rollback_migration_obsolescence_management",
        )
        for neighbor in ownership_topics:
            self.assertIn(neighbor, self.sheet)

        self.assertIn("특정 표준의 세부 requirement를 이 Topic이 모두 소유하지 않는다", self.sheet)
        self.assertIn("Historical frequency: 근거가 없어 사용하지 않음", self.sheet)
        self.assertIn("비용만으로 정당화할 수 없다", self.sheet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
