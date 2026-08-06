#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "configuration_change_release_backup_rollback_migration_obsolescence_management"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

def load(name: str) -> dict[str, Any]:
    return json.loads((PACK / name).read_text(encoding="utf-8"))

FACT = load("fact_anchor.json")
LOGIC = load("logic_check.json")
MODEL = load("model_answer.json")
IMPORTANCE = load("topic_importance.json")
README = (PACK / "README.md").read_text(encoding="utf-8")
SHEET_TEXT = SHEET.read_text(encoding="utf-8")

class TestSW06Metadata(unittest.TestCase):
    def test_topic_id_consistency(self) -> None:
        for payload in (FACT, LOGIC, MODEL, IMPORTANCE):
            self.assertEqual(payload["topic_id"], TOPIC_ID)

    def test_schema_versions(self) -> None:
        self.assertEqual(FACT["schema_version"], "fact_anchor.v1")
        self.assertEqual(LOGIC["schema_version"], "topic_pack.logic_check.v1")
        self.assertEqual(MODEL["schema_version"], "topic_pack.model_answer.v1")
        self.assertEqual(IMPORTANCE["schema_version"], "topic_pack.topic_importance.v1")

    def test_question_type_consistency(self) -> None:
        self.assertEqual(FACT["question_type_hint"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(MODEL["question_type"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(IMPORTANCE["question_type"], "IMPLEMENTATION_EVALUATION")
        self.assertEqual(LOGIC["deterministic_checks"]["question_type"], "IMPLEMENTATION_EVALUATION")

    def test_difficulty_and_importance(self) -> None:
        self.assertEqual(IMPORTANCE["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(IMPORTANCE["selection_importance"], "NORMAL")

    def test_lane_and_topic_documentation(self) -> None:
        self.assertIn("SOFTWARE_LLM_LANE_B", README)
        self.assertIn("SW-06", README)
        self.assertIn("SOFTWARE_LLM_LANE_B", SHEET_TEXT)
        self.assertIn("SW-06", SHEET_TEXT)

class TestSW06FactContracts(unittest.TestCase):
    def test_anchor_count(self) -> None:
        self.assertEqual(len(FACT["anchors"]), 40)

    def test_anchor_ids_unique_and_aliased(self) -> None:
        ids = [row["id"] for row in FACT["anchors"]]
        aliases = [row["anchor_id"] for row in FACT["anchors"]]
        self.assertEqual(len(set(ids)), 40)
        self.assertEqual(ids, aliases)

    def test_anchor_required_fields(self) -> None:
        required = {
            "id", "anchor_id", "statement", "importance", "keywords",
            "core_terms", "accepted_explanations", "rejected_explanations",
            "grading_notes", "source_basis", "claim", "description",
        }
        for row in FACT["anchors"]:
            self.assertFalse(required - set(row), row["id"])
            self.assertIn(row["importance"], {"core", "important"})
            for key in ("keywords", "core_terms", "accepted_explanations", "rejected_explanations"):
                self.assertTrue(row[key], f"{row['id']}.{key}")

    def test_core_facts_match_anchor_order(self) -> None:
        self.assertEqual(
            FACT["core_facts"],
            [row["statement"] for row in FACT["anchors"]],
        )

    def test_fatal_count_and_layer_owner(self) -> None:
        self.assertEqual(len(FACT["fatal_wrong_claims"]), 20)
        for row in FACT["fatal_wrong_claims"]:
            self.assertEqual(row["severity"], "fatal")
            self.assertEqual(row["affected_layers"], ["C"])
            self.assertTrue(row["correction"])

    def test_safe_expression_count(self) -> None:
        self.assertGreaterEqual(len(FACT["safe_expressions"]), 20)

    def test_core_distinctions_present(self) -> None:
        combined = json.dumps(FACT, ensure_ascii=False).lower()
        for marker in (
            "baseline", "version control", "as-built", "restore",
            "rollback", "migration", "obsolescence", "firmware",
            "license", "vendor lock-in",
        ):
            self.assertIn(marker.lower(), combined)

    def test_restore_and_rollback_are_distinct(self) -> None:
        anchor = next(
            row for row in FACT["anchors"]
            if row["id"] == "sw06_restore_rollback_distinction"
        )
        self.assertIn("동일하지", anchor["accepted_explanations"][0])

    def test_source_basis_has_primary_references(self) -> None:
        combined = " ".join(row["source_basis"] for row in FACT["anchors"])
        self.assertIn("ISO 10007:2017", combined)
        self.assertIn("IEC 62402:2019", combined)
        self.assertIn("NIST SP 800-82 Rev.3", combined)

class TestSW06LogicContracts(unittest.TestCase):
    def test_deterministic_checks_disabled(self) -> None:
        det = LOGIC["deterministic_checks"]
        self.assertIs(det["enabled"], False)
        self.assertEqual(det["fatal_checks"], [])
        self.assertEqual(det["major_checks"], [])

    def test_deterministic_aliases_nonempty(self) -> None:
        self.assertGreaterEqual(
            len(LOGIC["deterministic_checks"]["topic_aliases"]),
            20,
        )

    def test_llm_profile_enabled(self) -> None:
        self.assertIs(LOGIC["llm_profile"]["enabled"], True)

    def test_candidate_rules_empty_and_terms_rich(self) -> None:
        candidate = LOGIC["llm_profile"]["candidate_extraction"]
        self.assertEqual(candidate["rules"], [])
        self.assertGreaterEqual(len(candidate["key_terms"]), 100)
        self.assertIs(candidate["require_semantic_verification"], True)

    def test_truth_schema_matches_fact(self) -> None:
        self.assertEqual(LOGIC["llm_profile"]["truth_schema"], FACT["core_facts"])

    def test_fatal_conditions_and_major_checks(self) -> None:
        profile = LOGIC["llm_profile"]
        self.assertEqual(len(profile["fatal_conditions"]), 20)
        self.assertEqual(len(profile["major_checks"]), 12)
        for row in profile["major_checks"]:
            self.assertEqual(row["severity"], "major")
            self.assertEqual(row["affected_layers"], ["C"])

    def test_score_single_owner_contract(self) -> None:
        score = LOGIC["llm_profile"]["score_policy"]
        self.assertIs(score["direct_score_application"], False)
        self.assertIsNone(score["recommended_ceiling"])
        self.assertEqual(score["direct_d_e_effect"], "none")
        self.assertEqual(score["affected_layers"], ["C"])

    def test_output_contract_excludes_d_e(self) -> None:
        out = LOGIC["llm_profile"]["output_contract"]
        self.assertEqual(out["direct_score_layers"], ["C"])
        self.assertEqual(out["excluded_score_layers"], ["D", "E"])

    def test_false_positive_cautions_cover_conditional_cases(self) -> None:
        cautions = " ".join(LOGIC["llm_profile"]["false_positive_cautions"])
        for marker in ("Parallel operation", "Emergency change", "Vendor-specific", "Legacy"):
            self.assertIn(marker, cautions)

class TestSW06ModelContracts(unittest.TestCase):
    def test_question_pattern_count(self) -> None:
        self.assertEqual(len(MODEL["expected_question_patterns"]), 10)

    def test_question_pattern_anchor_refs_local(self) -> None:
        ids = {row["id"] for row in FACT["anchors"]}
        for row in MODEL["expected_question_patterns"]:
            self.assertTrue(row["required_anchor_ids"])
            self.assertLessEqual(set(row["required_anchor_ids"]), ids)

    def test_outline_count_and_refs(self) -> None:
        ids = {row["id"] for row in FACT["anchors"]}
        self.assertEqual(len(MODEL["recommended_outline"]), 8)
        for row in MODEL["recommended_outline"]:
            self.assertTrue(row["anchor_refs"])
            self.assertLessEqual(set(row["anchor_refs"]), ids)

    def test_question_examples_count(self) -> None:
        self.assertEqual(len(MODEL["question_examples"]), 10)

    def test_routing_aliases_are_narrow(self) -> None:
        aliases = MODEL["routing_aliases"]
        self.assertGreaterEqual(len(aliases), 20)
        forbidden_exact = {
            "software", "lifecycle", "V&V", "verification",
            "validation", "cybersecurity", "firewall",
            "incident response", "communication", "network",
        }
        self.assertTrue(forbidden_exact.isdisjoint(set(aliases)))

    def test_routing_fields_cover_operation(self) -> None:
        fields = " ".join(MODEL["routing_field_points"]).lower()
        for marker in ("plc", "dcs", "hmi", "checksum", "cutover", "license"):
            self.assertIn(marker, fields)

    def test_high_score_and_missing_points(self) -> None:
        self.assertGreaterEqual(len(MODEL["high_score_points"]), 12)
        self.assertGreaterEqual(len(MODEL["common_missing_points"]), 10)

class TestSW06BoundaryAndDocuments(unittest.TestCase):
    def test_sw04_boundary_explicit(self) -> None:
        for text in (README, SHEET_TEXT):
            self.assertIn("SW-04", text)
            self.assertIn("V&V", text)
            self.assertIn("개발 수명주기", text)

    def test_sw09_boundary_explicit(self) -> None:
        for text in (README, SHEET_TEXT):
            self.assertIn("SW-09", text)
            self.assertIn("사이버 사고대응", text)

    def test_full_model_answer_present(self) -> None:
        self.assertIn("## 모범답안", README)
        self.assertIn("### 8. 결론", README)
        self.assertIn("## 모범답안", SHEET_TEXT)

    def test_topic_sheet_has_twelve_sections(self) -> None:
        for index in range(1, 13):
            self.assertIn(f"## {index}.", SHEET_TEXT)

    def test_readme_has_fatal_warn_false_positive(self) -> None:
        self.assertIn("## 핵심 Fatal 오류", README)
        self.assertIn("## Warn/Major 수준의 부족한 표현", README)
        self.assertIn("## False positive 주의사항", README)

    def test_topic_importance_high_band_contract(self) -> None:
        conditions = IMPORTANCE["high_band_unlock_conditions"]
        self.assertGreaterEqual(len(conditions), 8)
        combined = " ".join(conditions)
        self.assertIn("SW-04", combined)
        self.assertIn("SW-09", combined)

    def test_files_end_with_newline(self) -> None:
        files = [
            PACK / "README.md",
            PACK / "fact_anchor.json",
            PACK / "logic_check.json",
            PACK / "model_answer.json",
            PACK / "topic_importance.json",
            SHEET,
            Path(__file__),
        ]
        for path in files:
            self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"), str(path))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    count = suite.countTestCases()
    print(f"SW06_FOCUSED_TEST_COUNT={count}")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
