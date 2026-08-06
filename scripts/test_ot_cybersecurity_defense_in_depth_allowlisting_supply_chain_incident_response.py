#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response"
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

class TestSW09Metadata(unittest.TestCase):
    def test_topic_id_consistency(self) -> None:
        for payload in (FACT, LOGIC, MODEL, IMPORTANCE):
            self.assertEqual(payload["topic_id"], TOPIC_ID)

    def test_schema_versions(self) -> None:
        self.assertEqual(FACT["schema_version"], "fact_anchor.v1")
        self.assertEqual(LOGIC["schema_version"], "topic_pack.logic_check.v1")
        self.assertEqual(MODEL["schema_version"], "topic_pack.model_answer.v1")
        self.assertEqual(IMPORTANCE["schema_version"], "topic_pack.topic_importance.v1")

    def test_question_type_consistency(self) -> None:
        self.assertEqual(FACT["question_type_hint"], "PROBLEM_SOLVE")
        self.assertEqual(MODEL["question_type"], "PROBLEM_SOLVE")
        self.assertEqual(IMPORTANCE["question_type"], "PROBLEM_SOLVE")
        self.assertEqual(LOGIC["deterministic_checks"]["question_type"], "PROBLEM_SOLVE")

    def test_difficulty_and_importance(self) -> None:
        self.assertEqual(IMPORTANCE["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(IMPORTANCE["selection_importance"], "HIGH")

    def test_lane_and_topic_documentation(self) -> None:
        for text in (README, SHEET_TEXT):
            self.assertIn("SOFTWARE_LLM_LANE_B", text)
            self.assertIn("SW-09", text)

class TestSW09FactContracts(unittest.TestCase):
    def test_anchor_count(self) -> None:
        self.assertEqual(len(FACT["anchors"]), 40)

    def test_anchor_ids_unique_and_aliased(self) -> None:
        ids = [row["id"] for row in FACT["anchors"]]
        aliases = [row["anchor_id"] for row in FACT["anchors"]]
        self.assertEqual(len(set(ids)), 40)
        self.assertEqual(ids, aliases)

    def test_anchor_required_fields(self) -> None:
        required = {"id","anchor_id","statement","importance","keywords","core_terms","accepted_explanations","rejected_explanations","grading_notes","source_basis","claim","description"}
        for row in FACT["anchors"]:
            self.assertFalse(required - set(row), row["id"])
            self.assertIn(row["importance"], {"core", "important"})
            for key in ("keywords","core_terms","accepted_explanations","rejected_explanations"):
                self.assertTrue(row[key], f"{row['id']}.{key}")

    def test_core_facts_match_anchor_order(self) -> None:
        self.assertEqual(FACT["core_facts"], [row["statement"] for row in FACT["anchors"]])

    def test_fatal_count_and_layer_owner(self) -> None:
        self.assertEqual(len(FACT["fatal_wrong_claims"]), 20)
        for row in FACT["fatal_wrong_claims"]:
            self.assertEqual(row["severity"], "fatal")
            self.assertEqual(row["affected_layers"], ["C"])
            self.assertTrue(row["correction"])

    def test_safe_expression_count(self) -> None:
        self.assertGreaterEqual(len(FACT["safe_expressions"]), 24)

    def test_security_control_markers(self) -> None:
        combined = json.dumps(FACT, ensure_ascii=False)
        for marker in ("Asset inventory","Zone and conduit","Industrial DMZ","Allowlisting","Jump server","MFA","SBOM","Incident response","Business continuity"):
            self.assertIn(marker, combined)

    def test_restore_and_trusted_recovery_are_distinct(self) -> None:
        anchor = next(row for row in FACT["anchors"] if row["id"] == "sw09_trusted_recovery")
        self.assertIn("clean baseline", anchor["statement"])
        fatal = next(row for row in FACT["fatal_wrong_claims"] if row["id"] == "sw09_fatal_restore_equals_eradication")
        self.assertIn("자동 제거", fatal["claim"])

    def test_source_basis_has_primary_reference_families(self) -> None:
        combined = " ".join(row["source_basis"] for row in FACT["anchors"])
        self.assertIn("IEC 62443-3-2", combined)
        self.assertIn("IEC 62443-3-3", combined)
        self.assertIn("NIST SP 800-82", combined)
        self.assertIn("NIST SP 800-161", combined)

class TestSW09LogicContracts(unittest.TestCase):
    def test_deterministic_checks_disabled(self) -> None:
        det = LOGIC["deterministic_checks"]
        self.assertIs(det["enabled"], False)
        self.assertEqual(det["fatal_checks"], [])
        self.assertEqual(det["major_checks"], [])

    def test_deterministic_aliases_nonempty(self) -> None:
        self.assertGreaterEqual(len(LOGIC["deterministic_checks"]["topic_aliases"]), 20)

    def test_llm_profile_enabled(self) -> None:
        self.assertIs(LOGIC["llm_profile"]["enabled"], True)

    def test_candidate_rules_empty_and_terms_rich(self) -> None:
        candidate = LOGIC["llm_profile"]["candidate_extraction"]
        self.assertEqual(candidate["rules"], [])
        self.assertGreaterEqual(len(candidate["key_terms"]), 150)
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
        for marker in ("DMZ","Allowlisting","MFA","Patch","SBOM","Backup"):
            self.assertIn(marker, cautions)

class TestSW09ModelContracts(unittest.TestCase):
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
        forbidden_exact = {"security","cybersecurity","OT","network","firewall","backup","incident"}
        self.assertTrue(forbidden_exact.isdisjoint(set(aliases)))

    def test_routing_fields_cover_ot_security(self) -> None:
        fields = " ".join(MODEL["routing_field_points"])
        for marker in ("Zone","Allowlisting","Jump server","SBOM","immutable backup","trusted recovery"):
            self.assertIn(marker, fields)

    def test_high_score_and_missing_points(self) -> None:
        self.assertGreaterEqual(len(MODEL["high_score_points"]), 18)
        self.assertGreaterEqual(len(MODEL["common_missing_points"]), 18)

class TestSW09BoundaryAndDocuments(unittest.TestCase):
    def test_sw06_boundary_explicit(self) -> None:
        for text in (README, SHEET_TEXT):
            self.assertIn("SW-06", text)
            self.assertIn("MOC", text)
            self.assertIn("trusted recovery", text)

    def test_sw07_sw08_boundaries_explicit(self) -> None:
        for text in (README, SHEET_TEXT):
            self.assertIn("SW-07", text)
            self.assertIn("Protocol", text)
            self.assertIn("SW-08", text)
            self.assertIn("Latency", text)

    def test_full_model_answer_present(self) -> None:
        self.assertIn("## 모범답안", README)
        self.assertIn("### 8. Trusted recovery와 지속성", README)
        self.assertIn("## 12. 모범답안", SHEET_TEXT)

    def test_topic_sheet_has_twelve_sections(self) -> None:
        for index in range(1, 13):
            self.assertIn(f"## {index}.", SHEET_TEXT)

    def test_readme_has_fatal_warn_false_positive(self) -> None:
        self.assertIn("## 핵심 Fatal 오류", README)
        self.assertIn("## Warn/Major 수준의 부족한 표현", README)
        self.assertIn("## False positive 주의사항", README)

    def test_topic_importance_high_band_contract(self) -> None:
        conditions = IMPORTANCE["high_band_unlock_conditions"]
        self.assertGreaterEqual(len(conditions), 10)
        combined = " ".join(conditions)
        self.assertIn("SW-06", combined)
        self.assertIn("SW-07", combined)
        self.assertIn("SW-08", combined)

    def test_files_end_with_newline(self) -> None:
        files = [PACK/"README.md",PACK/"fact_anchor.json",PACK/"logic_check.json",PACK/"model_answer.json",PACK/"topic_importance.json",SHEET,Path(__file__)]
        for path in files:
            self.assertTrue(path.read_bytes().endswith(b"\n"), str(path))


class TestSW09SemanticRepairRegressions(unittest.TestCase):
    def test_equivalent_remote_activity_audit_is_accepted(self) -> None:
        anchor = next(row for row in FACT["anchors"] if row["id"] == "sw09_secure_remote_session")
        text = " ".join([anchor["statement"], *anchor["accepted_explanations"]])
        for marker in (
            "Engineering Change Audit",
            "Protocol Transaction Log",
            "Command Log",
            "Session Metadata",
            "사용자·시간·대상·결과",
            "Audit Trail",
        ):
            self.assertIn(marker, text)
        cautions = " ".join(LOGIC["llm_profile"]["false_positive_cautions"])
        self.assertIn("화면 녹화가 없더라도", cautions)
        self.assertIn("GUI가 없는 장치", cautions)

    def test_missing_remote_audit_trail_remains_major(self) -> None:
        major = next(
            row for row in LOGIC["llm_profile"]["major_checks"]
            if row["id"] == "sw09_major_remote_session_missing"
        )
        self.assertIn("활동기록·audit trail이 없다", major["claim"])
        for marker in ("사용자·시간·대상·결과", "재구성 가능한 audit trail"):
            self.assertIn(marker, major["correction"])
        rejected = " ".join(
            next(row for row in FACT["anchors"] if row["id"] == "sw09_secure_remote_session")["rejected_explanations"]
        )
        self.assertIn("MFA만 적용하면 활동기록은 필요 없다", rejected)
        self.assertIn("Vendor 접속", rejected)

    def test_mttc_definition_and_measurement_interval(self) -> None:
        anchor = next(row for row in FACT["anchors"] if row["id"] == "sw09_exercise_metrics")
        text = " ".join([anchor["statement"], *anchor["accepted_explanations"]])
        self.assertIn("MTTC(Mean Time to Contain", text)
        self.assertIn("탐지 시점 또는 조직이 공식적으로 사용하는 사고 선언 시점", text)
        self.assertIn("확산 경로가 차단되고 추가 전파가 억제된 시점", text)
        for equivalent in ("Time to Containment", "Containment Completion Time", "확산 억제 완료시간"):
            self.assertIn(equivalent, text)

    def test_ambiguous_mttc_acronym_is_incomplete_but_equivalent_terms_are_allowed(self) -> None:
        major = next(
            row for row in LOGIC["llm_profile"]["major_checks"]
            if row["id"] == "sw09_major_exercise_metric_missing"
        )
        self.assertIn("확장어와 측정 시작·종료 경계 없이 약어로만", major["claim"])
        self.assertIn("Mean Time to Contain", major["correction"])
        cautions = " ".join(LOGIC["llm_profile"]["false_positive_cautions"])
        for equivalent in ("Time to Containment", "Containment Completion Time", "확산 억제 완료시간"):
            self.assertIn(equivalent, cautions)

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    count = suite.countTestCases()
    print(f"SW09_FOCUSED_TEST_COUNT={count}")
    if count != 41:
        raise SystemExit(f"expected 41 tests, got {count}")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
