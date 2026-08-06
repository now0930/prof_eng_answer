#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"

JSON_FILES = [
    "fact_anchor.json",
    "logic_check.json",
    "model_answer.json",
    "topic_importance.json",
]
BROAD_ALIASES = {
    "plc", "dcs", "scada", "hmi", "alarm", "trip", "interlock",
    "permissive", "sis", "sil", "sequence", "watchdog", "bypass",
}
SW03_MARKERS = {
    "alarm philosophy", "alarm rationalization", "alarm priority",
    "deadband", "shelving", "suppression", "display hierarchy",
    "operator authority",
}
SW05_MARKERS = {
    "pfdavg", "pfh", "safety lifecycle", "systematic failure",
    "safety v&v", "sil calculation",
}


def load_json(name: str) -> dict[str, Any]:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def permissive_all(values: list[bool]) -> bool:
    return all(values)


def transition_enable(
    command: bool,
    permissives: list[bool],
    feedback_ok: bool,
    trip: bool,
    inhibit: bool,
) -> bool:
    return (
        command
        and permissive_all(permissives)
        and feedback_ok
        and not trip
        and not inhibit
    )


def vote_moo_n(values: list[bool], m: int) -> bool:
    if not values or m < 1 or m > len(values):
        raise ValueError("invalid M-out-of-N configuration")
    return sum(bool(value) for value in values) >= m


def trip_latch(previous: bool, event: bool, reset_valid: bool) -> bool:
    return event or (previous and not reset_valid)


def watchdog_expired(now: float, last_heartbeat: float, timeout: float) -> bool:
    if timeout <= 0 or now < last_heartbeat:
        raise ValueError("invalid watchdog time")
    return now - last_heartbeat > timeout


def local_topic_score(text: str, aliases: list[str], field_points: list[str]) -> int:
    norm = normalize(text)
    alias_hits = sum(1 for alias in aliases if normalize(alias) in norm)
    field_hits = sum(1 for term in field_points if normalize(term) in norm)
    return alias_hits * 5 + min(field_hits, 12)


class TopicPackStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")
        cls.model = load_json("model_answer.json")
        cls.importance = load_json("topic_importance.json")
        cls.readme = (PACK / "README.md").read_text(encoding="utf-8")
        cls.sheet = SHEET.read_text(encoding="utf-8")

    def test_required_files_exist(self) -> None:
        self.assertTrue(SHEET.is_file())
        self.assertTrue((PACK / "README.md").is_file())
        for name in JSON_FILES:
            self.assertTrue((PACK / name).is_file(), name)

    def test_topic_id_and_schema_contract(self) -> None:
        expected_schema = {
            "fact_anchor.json": "topic_pack.fact_anchor.v1",
            "logic_check.json": "topic_pack.logic_check.v1",
            "model_answer.json": "topic_pack.model_answer.v1",
            "topic_importance.json": "topic_pack.topic_importance.v1",
        }
        for name, schema in expected_schema.items():
            data = load_json(name)
            self.assertEqual(data["topic_id"], TOPIC_ID, name)
            self.assertEqual(data["schema_version"], schema, name)

    def test_anchor_count_and_uniqueness(self) -> None:
        anchors = self.fact["anchors"]
        self.assertEqual(len(anchors), 28)
        anchor_ids = [item["anchor_id"] for item in anchors]
        self.assertEqual(len(anchor_ids), len(set(anchor_ids)))
        for item in anchors:
            self.assertEqual(item["id"], item["anchor_id"])
            self.assertIn(item["importance"], {"must", "important", "optional"})
            self.assertTrue(item["statement"].strip())
            self.assertTrue(item["core_terms"])

    def test_fatal_count_and_shape(self) -> None:
        fatals = self.fact["fatal_wrong_claims"]
        self.assertEqual(len(fatals), 16)
        ids = [item["id"] for item in fatals]
        self.assertEqual(len(ids), len(set(ids)))
        for item in fatals:
            self.assertEqual(item["severity"], "fatal")
            self.assertTrue(item["wrong_claim"])
            self.assertTrue(item["correct_rule"])
            self.assertTrue(item["affected_layers"])

    def test_model_references_are_valid(self) -> None:
        anchor_ids = {item["anchor_id"] for item in self.fact["anchors"]}
        self.assertEqual(len(self.model["expected_question_patterns"]), 10)
        self.assertEqual(len(self.model["recommended_outline"]), 8)
        for pattern in self.model["expected_question_patterns"]:
            self.assertTrue(pattern["pattern"].strip())
            self.assertTrue(set(pattern["required_anchor_ids"]) <= anchor_ids)
        for section in self.model["recommended_outline"]:
            self.assertTrue(set(section["anchor_refs"]) <= anchor_ids)

    def test_importance_contract(self) -> None:
        self.assertEqual(self.importance["difficulty"], "DESIGN_EVALUATION")
        self.assertEqual(
            self.importance["selection_importance"],
            "CORE_MUST_PREPARE",
        )
        self.assertEqual(
            self.importance["question_type"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertGreaterEqual(
            len(self.importance["high_band_unlock_conditions"]),
            8,
        )

    def test_logic_profile_contract(self) -> None:
        deterministic = self.logic["deterministic_checks"]
        llm = self.logic["llm_profile"]
        self.assertTrue(deterministic["enabled"])
        self.assertEqual(len(deterministic["fatal_checks"]), 16)
        self.assertEqual(len(llm["fatal_conditions"]), 16)
        self.assertGreaterEqual(len(llm["major_checks"]), 8)
        self.assertGreaterEqual(len(llm["false_positive_cautions"]), 8)
        for check in deterministic["fatal_checks"]:
            self.assertTrue(check["wrong_patterns"])
            self.assertEqual(check["severity"], "fatal")

    def test_sw03_and_sw05_boundaries_are_explicit(self) -> None:
        combined = normalize(
            json.dumps(self.fact, ensure_ascii=False)
            + json.dumps(self.logic, ensure_ascii=False)
            + self.readme
            + self.sheet
        )
        for marker in [
            "sw-03", "alarm philosophy", "soe", "operator authority",
            "sw-05", "sil 산정", "안전수명주기", "safety v&v",
        ]:
            self.assertIn(normalize(marker), combined)

    def test_no_broad_routing_alias(self) -> None:
        aliases = {normalize(value) for value in self.model["routing_aliases"]}
        self.assertTrue(aliases)
        self.assertFalse(aliases & BROAD_ALIASES)

    def test_scope_does_not_claim_sw03_or_sw05_ownership(self) -> None:
        scope_anchor = next(
            item for item in self.fact["anchors"]
            if item["anchor_id"] == "sw02_scope_operational_logic"
        )
        scope = normalize(scope_anchor["statement"])
        for marker in SW03_MARKERS | SW05_MARKERS:
            self.assertNotIn(marker, scope)

    def test_required_semantic_groups(self) -> None:
        combined = normalize(
            json.dumps(self.fact, ensure_ascii=False)
            + json.dumps(self.model, ensure_ascii=False)
        )
        groups = {
            "state": ["sequence", "state transition", "상태전이", "transition guard"],
            "protection": ["permissive", "interlock", "trip", "shutdown"],
            "diagnosis": ["voting", "first-out", "watchdog", "bad quality"],
            "governance": ["bypass", "override", "command arbitration"],
            "recovery": ["restart", "recovery", "state reconciliation"],
        }
        for group, markers in groups.items():
            with self.subTest(group=group):
                self.assertGreaterEqual(
                    sum(normalize(marker) in combined for marker in markers),
                    3,
                )

    def test_text_files_have_clean_whitespace(self) -> None:
        paths = [SHEET, PACK / "README.md"] + [PACK / name for name in JSON_FILES]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"), path)
            for line_number, line in enumerate(text.splitlines(), start=1):
                self.assertEqual(line, line.rstrip(), f"{path}:{line_number}")


class DeterministicFatalPatternSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")

    def test_direct_wrong_claims_match_deterministic_aids(self) -> None:
        checks = {
            item["id"]: item
            for item in self.logic["deterministic_checks"]["fatal_checks"]
        }
        for fatal in self.fact["fatal_wrong_claims"]:
            with self.subTest(fatal=fatal["id"]):
                patterns = checks[fatal["id"]]["wrong_patterns"]
                self.assertTrue(
                    any(
                        re.search(
                            pattern,
                            fatal["wrong_claim"],
                            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
                        )
                        for pattern in patterns
                    )
                )

    def test_explicit_corrections_do_not_trigger_patterns(self) -> None:
        corrections = [
            "Permissive와 Trip은 같은 개념이 아니며 시작 허가와 강제 정지로 구분한다.",
            "Interlock은 Alarm만을 의미하지 않고 동작 금지 또는 강제 전이를 수행한다.",
            "Trip 원인이 사라져도 즉시 자동 Reset하면 안 된다.",
            "Bypass에는 승인, 표시와 시간제한이 반드시 필요하다.",
            "Fail-safe는 항상 Close가 아니라 공정별 안전상태로 정한다.",
            "Voting을 적용하면 항상 안전성이 증가하는 것은 아니다.",
            "First-out은 마지막 원인이 아니라 최초 성립 원인을 보존한다.",
            "Watchdog은 감시 표시만 하는 것이 아니라 Timeout 시 안전 동작을 수행한다.",
            "Restart 시 조건 확인 없이 이전 Step을 그대로 재개하면 안 된다.",
            "Cause & Effect 표는 실행논리 프로그램을 완성하거나 대체하지 않는다.",
            "Timer 만료만으로 실제 Feedback을 대신할 수 없다.",
            "Override와 Bypass는 동일하지 않다.",
            "정상 Shutdown과 Trip은 같은 개념이 아니다.",
            "모든 Interlock가 자동으로 SIS 또는 SIL 기능이 되는 것은 아니다.",
            "Manual 모드에서도 보호 Interlock와 Trip을 모두 해제하면 안 된다.",
            "Bad quality 신호를 정상으로 간주하면 안 된다.",
        ]
        checks = self.logic["deterministic_checks"]["fatal_checks"]
        for correction in corrections:
            with self.subTest(correction=correction):
                hits = [
                    check["id"]
                    for check in checks
                    if any(
                        re.search(
                            pattern,
                            correction,
                            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
                        )
                        for pattern in check["wrong_patterns"]
                    )
                ]
                self.assertEqual(hits, [])


class LogicRelationshipTests(unittest.TestCase):
    def test_transition_requires_all_guards(self) -> None:
        self.assertTrue(
            transition_enable(True, [True, True], True, False, False)
        )
        self.assertFalse(
            transition_enable(True, [True, False], True, False, False)
        )
        self.assertFalse(
            transition_enable(True, [True, True], True, True, False)
        )
        self.assertFalse(
            transition_enable(True, [True, True], True, False, True)
        )

    def test_voting_logic(self) -> None:
        self.assertTrue(vote_moo_n([True, True, False], 2))
        self.assertFalse(vote_moo_n([True, False, False], 2))
        with self.assertRaises(ValueError):
            vote_moo_n([True, False], 3)

    def test_trip_latch_is_set_dominant(self) -> None:
        self.assertTrue(trip_latch(False, True, True))
        self.assertTrue(trip_latch(True, False, False))
        self.assertFalse(trip_latch(True, False, True))
        self.assertFalse(trip_latch(False, False, False))

    def test_watchdog_timeout_boundary(self) -> None:
        self.assertFalse(watchdog_expired(10.0, 5.0, 5.0))
        self.assertTrue(watchdog_expired(10.01, 5.0, 5.0))
        with self.assertRaises(ValueError):
            watchdog_expired(4.0, 5.0, 1.0)


class FocusedRoutingBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        model = load_json("model_answer.json")
        cls.aliases = model["routing_aliases"]
        cls.fields = model["routing_field_points"]

    def test_positive_cases_have_local_signal(self) -> None:
        samples = [
            "Sequence control의 state transition과 permissive, interlock, trip 우선순위를 설명하시오.",
            "Cause & Effect와 2oo3 voting, first-out 로직을 설계하시오.",
            "Bypass와 override의 차이 및 manual auto command arbitration을 설명하시오.",
            "Watchdog timeout과 restart recovery의 state reconciliation을 설명하시오.",
            "PLC sequence에서 feedback confirmation, trip latch와 abnormal transition을 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertGreaterEqual(
                    local_topic_score(sample, self.aliases, self.fields),
                    4,
                )

    def test_sw03_boundary_cases_do_not_match_compound_alias(self) -> None:
        samples = [
            "Alarm philosophy, priority, deadband, delay, shelving과 suppression을 설명하시오.",
            "High-performance HMI display hierarchy와 operator authority를 설명하시오.",
            "SCADA SOE report와 audit trail 관리방안을 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                alias_hits = sum(
                    normalize(alias) in normalize(sample)
                    for alias in self.aliases
                )
                self.assertEqual(alias_hits, 0)

    def test_sw05_boundary_cases_do_not_match_compound_alias(self) -> None:
        samples = [
            "SIL 산정과 PFDavg, PFH 계산방법을 설명하시오.",
            "Safety lifecycle, systematic failure, independence와 Safety V&V를 설명하시오.",
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                alias_hits = sum(
                    normalize(alias) in normalize(sample)
                    for alias in self.aliases
                )
                self.assertEqual(alias_hits, 0)


class SemanticAuditRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = load_json("fact_anchor.json")
        cls.logic = load_json("logic_check.json")
        cls.anchors = {item["id"]: item for item in cls.fact["anchors"]}
        cls.fatals = {item["id"]: item for item in cls.fact["fatal_wrong_claims"]}

    def test_rejected_explanations_are_anchor_specific(self) -> None:
        rejected = [tuple(item["rejected_explanations"]) for item in self.fact["anchors"]]
        self.assertEqual(len(rejected), 28)
        self.assertEqual(len(set(rejected)), 28)
        generic = "용어를 서로 같은 의미로 취급하거나 보호동작의 조건·우선순위·복구를 생략한다."
        self.assertFalse(any(generic in value for values in rejected for value in values))

    def test_transition_guard_is_representative_not_universal(self) -> None:
        text = self.anchors["sw02_transition_guard"]["statement"]
        self.assertIn("기동·명령 기반 전이의 대표식", text)
        self.assertIn("Command 없이", text)
        self.assertIn("선행조건 또는 동작 완료 확인조건", text)

    def test_timer_fatal_is_limited_to_physical_action_steps(self) -> None:
        fatal = self.fatals["sw02_fatal_timer_is_feedback"]
        for field in ("claim", "wrong_claim"):
            self.assertIn("물리적 동작 확인이 필요한 Step", fatal[field])
            self.assertIn("실제 설비 Feedback", fatal[field])
        for field in ("correction", "correct_rule", "description"):
            self.assertIn("Purge 유지시간", fatal[field])
            self.assertIn("시간 자체가", fatal[field])
            self.assertIn("정상 완료조건", fatal[field])
        self.assertNotEqual(fatal["claim"], "Timer가 만료되면 실제 설비 피드백과 관계없이 Step 완료로 판단해도 된다.")

    def test_timer_and_noncritical_watchdog_safe_boundaries(self) -> None:
        cautions = " ".join(self.logic["llm_profile"]["false_positive_cautions"])
        self.assertIn("혼합시간", cautions)
        self.assertIn("Historian", cautions)
        self.assertIn("Alarm-only", cautions)
        fatal = self.fatals["sw02_fatal_watchdog_monitor_only"]
        for field in ("correction", "correct_rule", "description"):
            self.assertIn("제어기 Task", fatal[field])
            self.assertIn("필수 통신", fatal[field])
            self.assertIn("원격 I/O", fatal[field])
            self.assertIn("Historian", fatal[field])
            self.assertIn("Alarm-only", fatal[field])
        self.assertNotIn("연결해야 한다.", fatal["description"].split("비중요 Historian", 1)[-1])

    def test_fail_safe_negated_absolute_remains_unchanged(self) -> None:
        text = self.anchors["sw02_fail_safe"]["statement"]
        self.assertIn("항상 Fail-close 또는 항상 De-energize로 고정되는 개념이 아니라", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
