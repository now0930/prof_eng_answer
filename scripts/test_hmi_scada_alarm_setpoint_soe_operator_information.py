#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "hmi_scada_alarm_setpoint_trip_interlock_soe_operator_information_management"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

EXPECTED_ANCHOR_COUNT = 31
EXPECTED_FATAL_COUNT = 16
EXPECTED_MAJOR_COUNT = 8
EXPECTED_ALIAS_COUNT = 20
EXPECTED_FIELD_POINT_COUNT = 45
EXPECTED_PATTERN_COUNT = 10
EXPECTED_OUTLINE_COUNT = 8

def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))

FACT = load("fact_anchor.json")
LOGIC = load("logic_check.json")
MODEL = load("model_answer.json")
IMPORTANCE = load("topic_importance.json")

class TopicPackStructureTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        required = [
            SHEET,
            PACK / "README.md",
            PACK / "fact_anchor.json",
            PACK / "logic_check.json",
            PACK / "model_answer.json",
            PACK / "topic_importance.json",
        ]
        self.assertTrue(all(path.is_file() for path in required))

    def test_topic_id_and_schema_contract(self) -> None:
        self.assertEqual(FACT["schema_version"], "topic_pack.fact_anchor.v1")
        self.assertEqual(LOGIC["schema_version"], "topic_pack.logic_check.v1")
        self.assertEqual(MODEL["schema_version"], "topic_pack.model_answer.v1")
        self.assertEqual(IMPORTANCE["schema_version"], "topic_pack.topic_importance.v1")
        for data in (FACT, LOGIC, MODEL, IMPORTANCE):
            self.assertEqual(data["topic_id"], TOPIC_ID)

    def test_anchor_count_and_uniqueness(self) -> None:
        anchors = FACT["anchors"]
        ids = [item["anchor_id"] for item in anchors]
        self.assertEqual(len(anchors), EXPECTED_ANCHOR_COUNT)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(item["id"] == item["anchor_id"] for item in anchors))

    def test_required_semantic_groups(self) -> None:
        ids = {item["anchor_id"] for item in FACT["anchors"]}
        required = {
            "sw03_hmi_scada_architecture",
            "sw03_high_performance_hmi",
            "sw03_alarm_definition",
            "sw03_alarm_rationalization",
            "sw03_alarm_priority",
            "sw03_alarm_state_acknowledgement",
            "sw03_alarm_deadband",
            "sw03_alarm_delay",
            "sw03_alarm_shelving",
            "sw03_alarm_suppression",
            "sw03_setpoint_governance",
            "sw03_soe_definition",
            "sw03_time_sync_resolution",
            "sw03_audit_trail",
            "sw03_operator_authority",
            "sw03_abnormal_situation_management",
            "sw03_sw02_boundary",
            "sw03_sw04_sw10_boundary",
        }
        self.assertTrue(required <= ids)

    def test_fatal_count_and_shape(self) -> None:
        self.assertEqual(len(FACT["fatal_wrong_claims"]), EXPECTED_FATAL_COUNT)
        det = LOGIC["deterministic_checks"]["fatal_checks"]
        llm = LOGIC["llm_profile"]["fatal_conditions"]
        self.assertEqual(len(det), EXPECTED_FATAL_COUNT)
        self.assertEqual(len(llm), EXPECTED_FATAL_COUNT)
        self.assertTrue(all(item["severity"] == "fatal" for item in det))

    def test_logic_profile_contract(self) -> None:
        profile = LOGIC["llm_profile"]
        self.assertTrue(profile["enabled"])
        self.assertEqual(len(profile["major_checks"]), EXPECTED_MAJOR_COUNT)
        self.assertGreaterEqual(len(profile["false_positive_cautions"]), 10)
        self.assertTrue(profile["output_contract"]["fatal_requires_direct_opposite_claim"])

    def test_model_references_are_valid(self) -> None:
        anchor_ids = {item["anchor_id"] for item in FACT["anchors"]}
        self.assertEqual(len(MODEL["expected_question_patterns"]), EXPECTED_PATTERN_COUNT)
        self.assertEqual(len(MODEL["recommended_outline"]), EXPECTED_OUTLINE_COUNT)
        for pattern in MODEL["expected_question_patterns"]:
            self.assertTrue(set(pattern["required_anchor_ids"]) <= anchor_ids)
        for section in MODEL["recommended_outline"]:
            self.assertTrue(set(section["anchor_refs"]) <= anchor_ids)

    def test_routing_counts_and_no_broad_alias(self) -> None:
        aliases = MODEL["routing_aliases"]
        self.assertEqual(len(aliases), EXPECTED_ALIAS_COUNT)
        self.assertEqual(len(MODEL["routing_field_points"]), EXPECTED_FIELD_POINT_COUNT)
        forbidden = {"HMI", "SCADA", "Alarm", "SOE", "Setpoint", "경보", "운전정보"}
        self.assertFalse(forbidden & set(aliases))

    def test_importance_contract(self) -> None:
        self.assertEqual(IMPORTANCE["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(IMPORTANCE["selection_importance"], "CORE_MUST_PREPARE")
        self.assertEqual(IMPORTANCE["question_type"], "PRINCIPLE_INTERPRETATION")
        self.assertGreaterEqual(len(IMPORTANCE["high_band_unlock_conditions"]), 8)

    def test_scope_boundaries_are_explicit(self) -> None:
        text = "\n".join(item["statement"] for item in FACT["anchors"])
        self.assertIn("SW-02", text)
        self.assertIn("SW-04", text)
        self.assertIn("SW-10", text)
        self.assertIn("실제 논리구조", text)
        self.assertIn("V-Model", text)
        self.assertIn("FAT", text)

    def test_text_files_have_clean_whitespace(self) -> None:
        paths = [SHEET, PACK / "README.md", *(PACK / name for name in (
            "fact_anchor.json", "logic_check.json", "model_answer.json", "topic_importance.json"
        ))]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"), path)
            self.assertFalse(any(line != line.rstrip() for line in text.splitlines()), path)

class AlarmRelationshipTests(unittest.TestCase):
    def test_high_alarm_deadband_delay_logic(self) -> None:
        def active(pv: float, sp: float, held: float, on_delay: float) -> bool:
            return pv >= sp and held >= on_delay
        def clear(pv: float, sp: float, deadband: float, held: float, off_delay: float) -> bool:
            return pv <= sp - deadband and held >= off_delay
        self.assertTrue(active(101.0, 100.0, 3.0, 2.0))
        self.assertFalse(active(101.0, 100.0, 1.0, 2.0))
        self.assertFalse(clear(99.0, 100.0, 2.0, 3.0, 2.0))
        self.assertTrue(clear(98.0, 100.0, 2.0, 3.0, 2.0))

    def test_acknowledge_does_not_clear_condition(self) -> None:
        condition_active = True
        acknowledged = True
        alarm_active = condition_active
        self.assertTrue(acknowledged)
        self.assertTrue(alarm_active)

    def test_priority_uses_consequence_and_time(self) -> None:
        def score(severity: int, urgency: int) -> int:
            return severity * urgency
        self.assertGreater(score(4, 4), score(4, 1))
        self.assertGreater(score(4, 4), score(1, 4))

    def test_shelving_and_suppression_are_distinct(self) -> None:
        shelving = {"actor": "operator", "temporary": True, "expires": True}
        suppression = {"actor": "logic", "temporary": False, "state_conditioned": True}
        self.assertNotEqual(shelving["actor"], suppression["actor"])
        self.assertTrue(shelving["expires"])
        self.assertTrue(suppression["state_conditioned"])

    def test_soe_order_requires_common_timebase(self) -> None:
        events = [
            ("PLC_A", 1000.001, "Trip"),
            ("PLC_B", 1000.004, "ValveClosed"),
        ]
        ordered = sorted(events, key=lambda item: item[1])
        self.assertEqual([item[2] for item in ordered], ["Trip", "ValveClosed"])

    def test_command_and_feedback_are_distinct(self) -> None:
        command_sent = True
        feedback_on = False
        self.assertTrue(command_sent)
        self.assertFalse(feedback_on)
        self.assertNotEqual(command_sent, feedback_on)

class DeterministicFatalPatternSafetyTests(unittest.TestCase):
    def test_direct_wrong_claims_match_deterministic_aids(self) -> None:
        checks = LOGIC["deterministic_checks"]["fatal_checks"]
        for check in checks:
            pattern = re.compile(check["wrong_patterns"][0])
            self.assertRegex(check["examples_or_patterns"][0], pattern, check["id"])

    def test_explicit_corrections_do_not_trigger_patterns(self) -> None:
        checks = LOGIC["deterministic_checks"]["fatal_checks"]
        corrections = {
            item["id"]: item["correction"] for item in FACT["fatal_wrong_claims"]
        }
        for check in checks:
            pattern = re.compile(check["wrong_patterns"][0])
            sentence = f"오답은 '{check['message']}'이지만 실제로는 {corrections[check['id']]}"
            self.assertIsNone(pattern.search(sentence), check["id"])

    def test_patterns_do_not_match_omission(self) -> None:
        text = "Alarm 관리에서는 운전자 조치와 응답시간을 검토한다."
        for check in LOGIC["deterministic_checks"]["fatal_checks"]:
            self.assertIsNone(re.compile(check["wrong_patterns"][0]).search(text))

class FocusedRoutingBoundaryTests(unittest.TestCase):
    def _matched_aliases(self, text: str) -> list[str]:
        lower = text.lower()
        return [alias for alias in MODEL["routing_aliases"] if alias.lower() in lower]

    def test_positive_cases_have_local_signal(self) -> None:
        cases = [
            "HMI SCADA alarm management SOE를 설명하시오.",
            "alarm deadband delay shelving suppression 차이를 설명하시오.",
            "sequence of events audit trail time synchronization을 설명하시오.",
            "high performance HMI display hierarchy 설계기준을 설명하시오.",
        ]
        for case in cases:
            self.assertTrue(self._matched_aliases(case), case)

    def test_sw02_boundary_cases_do_not_match_compound_alias(self) -> None:
        cases = [
            "Sequence state transition trip latch reset logic을 설명하시오.",
            "Interlock의 상태전이와 Fail-safe Restart를 설명하시오.",
        ]
        for case in cases:
            self.assertFalse(self._matched_aliases(case), case)

    def test_sw04_boundary_cases_do_not_match_compound_alias(self) -> None:
        cases = [
            "V-Model requirement traceability unit integration test를 설명하시오.",
            "Static analysis와 regression test를 설명하시오.",
        ]
        for case in cases:
            self.assertFalse(self._matched_aliases(case), case)

    def test_sw10_boundary_cases_do_not_match_compound_alias(self) -> None:
        cases = [
            "FAT SAT commissioning acceptance와 punch list를 설명하시오.",
            "URS FRS FDS와 site integration test를 설명하시오.",
        ]
        for case in cases:
            self.assertFalse(self._matched_aliases(case), case)

class ContentQualityTests(unittest.TestCase):
    def test_no_placeholder_markers(self) -> None:
        forbidden = ("TODO", "scaffold", "보강하세요", "작성한다")
        for name in ("README.md", "fact_anchor.json", "logic_check.json", "model_answer.json", "topic_importance.json"):
            text = (PACK / name).read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token.lower(), text.lower(), f"{name}:{token}")

    def test_alarm_event_boundary(self) -> None:
        fact = next(item for item in FACT["anchors"] if item["anchor_id"] == "sw03_alarm_definition")
        self.assertIn("운전자", fact["statement"])
        self.assertIn("Event", fact["statement"])
        self.assertIn("구분", fact["statement"])

    def test_audit_soe_boundary(self) -> None:
        audit = next(item for item in FACT["anchors"] if item["anchor_id"] == "sw03_audit_trail")
        soe = next(item for item in FACT["anchors"] if item["anchor_id"] == "sw03_soe_definition")
        self.assertIn("사용자", audit["statement"])
        self.assertIn("상태", soe["statement"])
        self.assertNotEqual(audit["statement"], soe["statement"])


class SemanticAuditRepairTests(unittest.TestCase):
    def test_all_anchor_rejections_are_specific(self) -> None:
        rejected = [tuple(item["rejected_explanations"]) for item in FACT["anchors"]]
        self.assertEqual(len(rejected), 31)
        self.assertEqual(len(set(rejected)), 31)
        generic = "서로 다른 정보관리 기능을 같은 의미로 취급하거나 조건, 권한, 이력과 운전자 조치를 생략한다."
        self.assertFalse(any(generic in value for values in rejected for value in values))

    def test_rejections_cover_key_function_boundaries(self) -> None:
        by_id = {item["id"]: " ".join(item["rejected_explanations"]) for item in FACT["anchors"]}
        self.assertIn("동일 장치", by_id["sw03_hmi_scada_architecture"])
        self.assertIn("모든 Event", by_id["sw03_alarm_definition"])
        self.assertIn("공정 원인 제거", by_id["sw03_alarm_state_acknowledgement"])
        self.assertIn("PV 크기", by_id["sw03_alarm_priority"])
        self.assertIn("시간지연", by_id["sw03_alarm_deadband"])
        self.assertIn("임의 Shelving", by_id["sw03_alarm_suppression"])
        self.assertIn("Historian 표본값", by_id["sw03_historian_vs_soe"])
        self.assertIn("사용자·대상", by_id["sw03_audit_trail"])

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    count = suite.countTestCases()
    print(f"SW03_FOCUSED_TEST_COUNT={count}")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
