from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


TOPIC_ID = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"
REPO_ROOT = Path(__file__).resolve().parents[1]
TOPIC_DIR = REPO_ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = REPO_ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"
README = TOPIC_DIR / "README.md"
FACT = TOPIC_DIR / "fact_anchor.json"
LOGIC = TOPIC_DIR / "logic_check.json"
MODEL = TOPIC_DIR / "model_answer.json"
IMPORTANCE = TOPIC_DIR / "topic_importance.json"

REQUIRED_FILES = [SHEET, README, FACT, LOGIC, MODEL, IMPORTANCE]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TopicPackStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json(FACT)
        cls.logic = load_json(LOGIC)
        cls.model = load_json(MODEL)
        cls.importance = load_json(IMPORTANCE)

    def test_required_files_exist(self) -> None:
        for path in REQUIRED_FILES:
            self.assertTrue(path.is_file(), path)

    def test_topic_id_and_schema_contract(self) -> None:
        expected = {
            FACT: "topic_pack.fact_anchor.v1",
            LOGIC: "topic_pack.logic_check.v1",
            MODEL: "topic_pack.model_answer.v1",
            IMPORTANCE: "topic_pack.topic_importance.v1",
        }
        for path, schema in expected.items():
            data = load_json(path)
            self.assertEqual(data["topic_id"], TOPIC_ID)
            self.assertEqual(data["schema_version"], schema)

    def test_anchor_count_and_uniqueness(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(len(anchors), 31)
        ids = [item["id"] for item in anchors]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.fact["core_facts"], [item["statement"] for item in anchors])

    def test_fatal_count_and_shape(self) -> None:
        fatals = self.fact["fatal_wrong_claims"]
        self.assertEqual(len(fatals), 16)
        self.assertEqual(len(self.logic["deterministic_checks"]["fatal_checks"]), 16)
        self.assertEqual(len(self.logic["llm_profile"]["fatal_conditions"]), 16)
        for item in fatals:
            self.assertEqual(item["severity"], "fatal")
            self.assertTrue(item["wrong_claim"])
            self.assertTrue(item["correct_rule"])

    def test_logic_profile_contract(self) -> None:
        profile = self.logic["llm_profile"]
        self.assertTrue(profile["enabled"])
        self.assertTrue(profile["cap_policy"]["fatal_requires_explicit_contradiction"])
        self.assertTrue(profile["cap_policy"]["omission_is_not_fatal"])
        self.assertEqual(len(profile["truth_schema"]), 31)
        self.assertEqual(len(profile["major_checks"]), 8)
        self.assertEqual(len(profile["false_positive_cautions"]), 10)

    def test_model_references_are_valid(self) -> None:
        anchor_ids = {item["id"] for item in self.fact["anchors"]}
        refs = {
            ref
            for section in self.model["recommended_outline"]
            for ref in section["anchor_refs"]
        }
        self.assertTrue(refs)
        self.assertTrue(refs <= anchor_ids)

    def test_required_semantic_groups(self) -> None:
        statements = " ".join(self.fact["core_facts"]).lower()
        for terms in (
            ("v-model", "요구사항", "시험"),
            ("verification", "validation", "rtm"),
            ("단위시험", "통합시험", "시스템시험"),
            ("정적분석", "동적분석", "회귀시험"),
            ("simulation", "hil", "fault injection"),
            ("결함관리", "변경관리", "baseline"),
        ):
            for term in terms:
                self.assertIn(term.lower(), statements)

    def test_routing_counts_and_no_broad_alias(self) -> None:
        aliases = self.model["routing_aliases"]
        fields = self.model["routing_field_points"]
        self.assertEqual(len(aliases), 20)
        self.assertEqual(len(fields), 45)
        forbidden = {"software", "소프트웨어", "test", "시험", "verification", "검증"}
        self.assertFalse(forbidden & {item.strip().lower() for item in aliases})
        self.assertTrue(all(len(item.split()) >= 2 for item in aliases))

    def test_importance_contract(self) -> None:
        self.assertEqual(self.importance["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(self.importance["selection_importance"], "CORE_MUST_PREPARE")
        self.assertEqual(self.importance["question_type"], "PROCEDURE")
        self.assertEqual(len(self.importance["high_band_unlock_conditions"]), 8)

    def test_scope_boundaries_are_explicit(self) -> None:
        text = "\n".join(
            [
                SHEET.read_text(encoding="utf-8"),
                README.read_text(encoding="utf-8"),
                " ".join(self.fact["core_facts"]),
            ]
        )
        for token in ("SW-05", "Safety Integrity", "SW-10", "FAT", "SAT", "시운전"):
            self.assertIn(token, text)

    def test_text_files_have_clean_whitespace(self) -> None:
        for path in REQUIRED_FILES + [Path(__file__)]:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"), path)
            self.assertNotRegex(text, r"[ \t]+\n", path)


class LifecycleRelationshipTests(unittest.TestCase):
    def test_v_model_mapping(self) -> None:
        mapping = {
            "requirement": "system_test_validation",
            "architecture": "integration_test",
            "detailed_design": "unit_test",
        }
        self.assertEqual(mapping["architecture"], "integration_test")
        self.assertNotEqual(mapping["requirement"], mapping["detailed_design"])

    def test_verification_validation_are_distinct(self) -> None:
        verification = "conformance_to_specification"
        validation = "fitness_for_intended_use"
        self.assertNotEqual(verification, validation)

    def test_bidirectional_traceability(self) -> None:
        requirement_to_test = {"REQ-1": "TC-1"}
        test_to_requirement = {test: req for req, test in requirement_to_test.items()}
        self.assertEqual(test_to_requirement["TC-1"], "REQ-1")

    def test_test_levels_are_not_substitutable(self) -> None:
        defects = {
            "unit": {"boundary", "local_logic"},
            "integration": {"interface", "timing"},
            "system": {"end_to_end", "operational_mode"},
        }
        self.assertFalse(defects["unit"] >= defects["integration"])
        self.assertFalse(defects["unit"] >= defects["system"])

    def test_static_dynamic_execution_boundary(self) -> None:
        analysis_mode = {"static": False, "dynamic": True}
        self.assertFalse(analysis_mode["static"])
        self.assertTrue(analysis_mode["dynamic"])

    def test_regression_includes_affected_existing_behavior(self) -> None:
        changed = {"new_function"}
        affected_existing = {"shared_interface", "existing_sequence"}
        regression_scope = changed | affected_existing
        self.assertTrue(affected_existing <= regression_scope)

    def test_hil_closed_loop_boundary(self) -> None:
        hil = {"real_controller": True, "real_time_plant_model": True, "closed_loop": True}
        self.assertTrue(all(hil.values()))

    def test_fault_injection_checks_recovery(self) -> None:
        expected = {"detect", "isolate", "fallback", "recover"}
        observed = {"detect", "isolate", "fallback", "recover"}
        self.assertEqual(observed, expected)


class DeterministicFatalPatternSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.logic = load_json(LOGIC)
        cls.checks = cls.logic["deterministic_checks"]["fatal_checks"]

    def test_direct_wrong_claims_match_deterministic_aids(self) -> None:
        for check in self.checks:
            wrong = check["examples_or_patterns"][0]
            self.assertTrue(
                any(re.search(pattern, wrong) for pattern in check["wrong_patterns"]),
                check["id"],
            )

    def test_explicit_corrections_do_not_trigger_patterns(self) -> None:
        samples = [
            "Verification과 Validation은 완전히 같은 활동이 아니다. 두 활동의 목적을 구분해야 한다.",
            "V-Model에서는 모든 코딩이 끝난 뒤에 시험을 처음 계획하는 것이 아니라 개발 초기부터 대응 시험을 준비한다.",
            "회귀시험은 새로 추가된 기능만 시험하면 되는 것이 아니라 영향받는 기존 기능도 확인한다.",
            "일반 소프트웨어 V&V를 완료해도 별도 Safety lifecycle 없이 SIS의 SIL 충족이 자동 증명되지는 않는다.",
        ]
        for sample in samples:
            for check in self.checks:
                self.assertFalse(
                    any(re.search(pattern, sample) for pattern in check["wrong_patterns"]),
                    (check["id"], sample),
                )

    def test_patterns_do_not_match_omission(self) -> None:
        neutral = "계측제어 소프트웨어 개발단계와 시험단계를 설명한다."
        for check in self.checks:
            self.assertFalse(any(re.search(p, neutral) for p in check["wrong_patterns"]))


class FocusedRoutingBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_json(MODEL)
        cls.profile = load_json(LOGIC)["llm_profile"]["candidate_extraction"]

    def test_positive_cases_have_local_signal(self) -> None:
        cases = [
            "계측제어 소프트웨어 V-Model과 요구사항 추적성 매트릭스를 설명하시오.",
            "단위시험 통합시험 시스템시험과 Verification Validation을 비교하시오.",
            "Simulation HIL Fault injection을 이용한 제어 SW 검증방안을 설명하시오.",
        ]
        fields = [item.lower() for item in self.model["routing_field_points"]]
        for case in cases:
            lowered = case.lower()
            self.assertTrue(any(field in lowered for field in fields), case)

    def test_sw05_boundary_cases_do_not_match_compound_alias(self) -> None:
        case = "SIS의 SIL 산정, PFDavg, 독립성과 Safety lifecycle을 설명하시오.".lower()
        self.assertFalse(any(alias.lower() in case for alias in self.model["routing_aliases"]))

    def test_sw10_boundary_cases_do_not_match_compound_alias(self) -> None:
        case = "제어 프로젝트 FAT SAT 시운전 Acceptance와 Handover 절차를 설명하시오.".lower()
        self.assertFalse(any(alias.lower() in case for alias in self.model["routing_aliases"]))

    def test_sw03_boundary_cases_do_not_match_compound_alias(self) -> None:
        case = "HMI SCADA Alarm rationalization SOE와 운전자 권한을 설명하시오.".lower()
        self.assertFalse(any(alias.lower() in case for alias in self.model["routing_aliases"]))


class ContentQualityTests(unittest.TestCase):
    def test_no_placeholder_markers(self) -> None:
        for path in REQUIRED_FILES:
            text = path.read_text(encoding="utf-8").lower()
            for marker in ("todo", "scaffold", "보강하세요"):
                self.assertNotIn(marker, text, path)

    def test_question_and_outline_counts(self) -> None:
        model = load_json(MODEL)
        self.assertEqual(len(model["expected_question_patterns"]), 10)
        self.assertEqual(len(model["recommended_outline"]), 8)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    print(f"SW04_FOCUSED_TEST_COUNT={suite.countTestCases()}")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
