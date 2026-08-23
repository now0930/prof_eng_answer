#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC = "sis_sil_safety_software_independence_systematic_failure_verification_validation"
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
    "sil_property_of_safety_function", "systematic_failure",
    "verification_definition", "validation_definition", "proof_test_relation",
    "separation_shared_resources", "certified_product_scope",
    "tool_qualification_basis", "modification_revalidation",
    "bypass_override_controls", "pfd_pfh_mode_boundary",
}
REQUIRED_FATALS = {
    "certified_product_auto_sil", "software_random_failure_rate_only",
    "pfd_pfh_interchangeable", "proof_test_equals_validation",
    "different_cpu_guarantees_independence", "diversity_eliminates_ccf",
    "tool_output_infallible", "bypass_no_sil_effect",
    "small_change_no_regression",
}
BROAD_ALIASES = {"sis", "sil", "trip", "interlock", "plc", "verification", "validation", "safety"}

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

class SW05SourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(FILES["fact"])
        cls.logic = load_json(FILES["logic"])
        cls.model = load_json(FILES["model"])
        cls.importance = load_json(FILES["importance"])
        cls.sheet = FILES["sheet"].read_text(encoding="utf-8")
        cls.readme = FILES["readme"].read_text(encoding="utf-8")

    def test_01_all_allowed_files_exist(self) -> None:
        for name, path in FILES.items():
            with self.subTest(name=name): self.assertTrue(path.is_file(), path)

    def test_02_topic_and_modern_root_contracts(self) -> None:
        for row in (self.fact, self.logic, self.model, self.importance):
            self.assertEqual(row["topic_id"], TOPIC)
        self.assertEqual(self.fact["schema_version"], "fact_anchor.v1")
        self.assertEqual(self.logic["schema_version"], "topic_pack.logic_check.v1")
        self.assertEqual(self.model["schema_version"], "topic_pack.model_answer.v1")
        self.assertEqual(self.importance["schema_version"], "topic_pack.topic_importance.v1")

    def test_03_anchor_schema_and_counts(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(len(anchors), len(self.fact["core_facts"]))
        required = {"id","anchor_id","statement","importance","keywords","core_terms","accepted_explanations","rejected_explanations","grading_notes","source_basis","claim","description"}
        for row in anchors:
            self.assertTrue(required <= set(row), required-set(row))
            self.assertIn(row["importance"], {"core","important"})
        self.assertEqual(self.fact["core_facts"], [row["statement"] for row in anchors])

    def test_04_fatal_and_major_contracts(self) -> None:
        fatal = self.fact["fatal_wrong_claims"]
        major = self.logic["llm_profile"]["major_checks"]
        self.assertEqual(len(major), 12)
        profile_fatal_conditions = self.logic["llm_profile"]["fatal_conditions"]
        profile_fatal_dicts = [
            row
            for row in profile_fatal_conditions
            if isinstance(row, dict)
        ]
        profile_selector_strings = [
            row
            for row in profile_fatal_conditions
            if isinstance(row, str)
        ]
        self.assertEqual(profile_fatal_dicts, fatal)
        self.assertEqual(len(profile_selector_strings), 2)
        for finding_id in (
            "sw05_fatal_sil_expanded_as_safety_instrument_level",
            "sw05_fatal_software_test_mapped_to_voting_architecture",
        ):
            self.assertEqual(
                sum(
                    finding_id in row
                    for row in profile_selector_strings
                ),
                1,
            )
        self.assertTrue(all(row["severity"] == "fatal" and isinstance(row["affected_layers"], list) and row["affected_layers"] and len(row["affected_layers"]) == len(set(row["affected_layers"])) and "C" in row["affected_layers"] for row in fatal))
        self.assertTrue(all(row["severity"] == "major" and row["affected_layers"] == ["C"] for row in major))

    def test_05_required_anchor_and_fatal_ids(self) -> None:
        aids = {row["id"] for row in self.fact["anchors"]}
        fids = {row["id"] for row in self.fact["fatal_wrong_claims"]}
        self.assertTrue(REQUIRED_ANCHORS <= aids, REQUIRED_ANCHORS-aids)
        self.assertTrue(REQUIRED_FATALS <= fids, REQUIRED_FATALS-fids)

    def test_06_llm_profile_single_owner_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        profile = self.logic["llm_profile"]
        self.assertFalse(deterministic["enabled"])
        expected_fatal_ids = [
            "sw05_fatal_hft_is_integration_test",
            "sw05_fatal_sil_expanded_as_safety_instrument_level",
            "sw05_fatal_software_test_is_random_hardware_integrity",
            "sw05_fatal_software_test_mapped_to_voting_architecture",
        ]
        for key in (
            "fatal_checks",
            "major_checks",
            "question_type_checks",
        ):
            self.assertEqual(
                sorted(
                    item["id"]
                    for item in deterministic[key]
                ),
                (
                    expected_fatal_ids
                    if key == "fatal_checks"
                    else []
                ),
            )
        self.assertEqual(profile["candidate_extraction"]["rules"], [])
        self.assertGreaterEqual(len(profile["candidate_extraction"]["key_terms"]), 100)
        self.assertEqual([item for item in profile['truth_schema'] if isinstance(item, str)], [row['statement'] for row in self.fact['anchors']])
        self.assertEqual(sorted(item['id'] for item in profile['truth_schema'] if isinstance(item, dict)), sorted(row['id'] for row in self.logic['llm_profile']['truth_schema'] if isinstance(row, dict) and row.get('id') in ['sw05_hft_vs_integration_test_boundary', 'sw05_random_hardware_vs_software_vv_boundary']))
        self.assertFalse(profile["score_policy"]["direct_score_application"])
        self.assertIsNone(profile["score_policy"]["recommended_ceiling"])
        self.assertEqual(profile["score_policy"]["direct_d_e_effect"], "none")
        self.assertEqual(profile["score_policy"]["affected_layers"], ["C"])
        self.assertEqual(profile["output_contract"]["direct_score_layers"], ["C"])
        self.assertEqual(profile["output_contract"]["excluded_score_layers"], ["D","E"])

    def test_07_model_anchor_reference_contract(self) -> None:
        anchor_set = {row["id"] for row in self.fact["anchors"]}
        patterns = self.model["expected_question_patterns"]
        outlines = self.model["recommended_outline"]
        self.assertEqual(len(patterns), 10)
        self.assertEqual(len(outlines), 8)
        for row in patterns:
            refs = set(row["required_anchor_ids"])
            self.assertTrue(refs and refs <= anchor_set)
        union = set().union(*(set(row["anchor_refs"]) for row in outlines))
        self.assertEqual(union, anchor_set)
        self.assertEqual(self.model["topic_aliases"], self.model["routing_aliases"])

    def test_08_sw02_sw04_and_final_element_boundaries(self) -> None:
        for marker in ("SW-02와의 경계","SW-04와의 경계","일반 Sequence","일반 제어 소프트웨어","Final Element/PST Topic"):
            self.assertIn(marker, self.sheet)

    def test_09_proof_test_and_certificate_fatal_guards(self) -> None:
        combined = json.dumps({"fact":self.fact,"logic":self.logic}, ensure_ascii=False)
        for marker in ("proof_test_equals_validation","certified_product_auto_sil","전체 SIF","Safety Manual"):
            self.assertIn(marker, combined)

    def test_10_formula_markers(self) -> None:
        for marker in ("RRF", r"PFD_{\mathrm{avg}}", r"\lambda_{DU}T_1", "PFH", r"C_{\mathrm{trace}}", "C_{PT}"):
            self.assertIn(marker, self.sheet)

    def test_11_routing_alias_specificity(self) -> None:
        aliases = self.model["routing_aliases"]
        self.assertEqual(len(aliases), 14)
        normalized = {x.strip().casefold() for x in aliases}
        self.assertTrue(BROAD_ALIASES.isdisjoint(normalized), BROAD_ALIASES & normalized)
        for marker in ("SRS","systematic failure","tool qualification"):
            self.assertTrue(any(marker.casefold() in x.casefold() for x in aliases))

    def test_12_positive_and_negative_question_boundaries(self) -> None:
        self.assertEqual(len(self.model["question_examples"]), 10)
        for marker in ("일반 PLC Sequence","일반 Software V-Model","ESD Valve의 PST Coverage","Industrial Ethernet Protocol"):
            self.assertIn(marker, self.sheet)

    def test_13_importance_contract(self) -> None:
        self.assertEqual(self.importance["difficulty"], "THEORY_CORE")
        self.assertEqual(self.importance["selection_importance"], "CORE_MUST_PREPARE")
        self.assertEqual(self.importance["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertGreaterEqual(len(self.importance["high_band_unlock_conditions"]), 8)

    def test_14_model_answer_depth(self) -> None:
        self.assertGreaterEqual(len(self.model["high_score_points"]), 12)
        self.assertGreaterEqual(len(self.model["common_missing_points"]), 10)
        self.assertGreaterEqual(len(self.model["routing_field_points"]), 17)

    def test_15_verify_first_and_false_positive_contract(self) -> None:
        combined = self.sheet + self.readme + json.dumps(self.logic, ensure_ascii=False)
        for marker in ("verify-first","적용 Edition","Certificate Scope","독립성 수준"):
            self.assertIn(marker, combined)
        self.assertGreaterEqual(len(self.fact["safe_expressions"]), 16)
        self.assertGreaterEqual(len(self.logic["llm_profile"]["false_positive_cautions"]), 10)

    def test_16_no_forbidden_runtime_output_contract(self) -> None:
        for forbidden in ("rubrics/generated/","model_answer_router.py","validate-all","git commit","git push"):
            self.assertNotIn(forbidden, self.readme)

if __name__ == "__main__":
    unittest.main(verbosity=2)
