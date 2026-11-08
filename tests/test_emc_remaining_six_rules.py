"""Regression matrix for the six adjudicated EMC rule definitions.

The matrix tests semantic boundaries, rule ownership and contract severity.
It does NOT authorize promotion of held positive scoring anchors.
"""

import json
import unittest
from pathlib import Path

from grading.evidence.engineering_invariant_evaluator import (
    evaluate_engineering_invariants,
)
from grading.evidence.topic_machine_contract import validate_topic_machine_contract
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.scoring.deterministic_requirement_evaluator import (
    evaluate_deterministic_requirements,
)

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC

# Two demonstrably incorrect assertions, two safe/rebuttal statements,
# and one legitimate conditional application for each case.
MATRIX = {
    "EMC_SINGLE_POINT_UNIVERSAL": {
        "wrong": [
            "Single-point grounding이 모든 주파수와 모든 설비에서 항상 최선이다.",
            "모든 조건에서 단일점 접지가 언제나 최적이다.",
        ],
        "safe": [
            "단일점 접지는 저주파 신호에 조건부로 적합할 수 있다.",
            "Single-point grounding이 모든 설비에서 항상 최선이라는 주장은 틀리다.",
            "주파수와 본딩 조건을 비교한 후 단일점 접지를 선택한다.",
        ],
    },
    "EMC_SHIELD_REPLACES_PE": {
        "wrong": [
            "일반 신호 차폐층이 보호접지 도체를 대신할 수 있다.",
            "보호접지 PE를 cable shield로 대체하면 된다.",
        ],
        "safe": [
            "Cable shield는 보호접지 PE를 대신하지 않는다.",
            "Cable shield가 보호접지 도체를 대신할 수 있다는 주장은 잘못이다.",
            "규격에 적합한 단면적과 연속성을 확보한 금속 차폐층을 보호도체로 사용할 수 있는 경우도 있다.",
        ],
    },
    "EMC_REDUNDANCY_IGNORES_CCF": {
        "wrong": [
            "Power supply 두 대를 병렬로 두면 공통고장과 무관하게 완전 이중화가 된다.",
            "전원 이중화 시 공통원인고장은 발생하지 않는다.",
        ],
        "safe": [
            "두 전원장치가 동일 입력을 공유하면 공통원인고장을 검토해야 한다.",
            "Power supply 두 대를 병렬로 두면 공통고장과 무관하다는 주장은 잘못이다.",
            "공통고장을 분리한 두 공급원과 독립 분배 경로로 가용성을 개선할 수 있다.",
        ],
    },
    "EMC_GROUND_LOOP_RESISTANCE_ONLY": {
        "wrong": [
            "Ground-loop 문제는 도체 저항만 낮추면 항상 해결된다.",
            "접지 루프는 접지선 저항만 줄이면 모두 해결된다.",
        ],
        "safe": [
            "Ground-loop는 다중 귀로와 전위차를 확인해야 한다.",
            "Ground-loop 문제는 도체 저항만 낮추면 항상 해결된다는 주장은 틀리다.",
            "저항을 낮춰 특정 공통 임피던스 결합을 완화할 수 있지만 모든 Ground-loop가 해결되는 것은 아니다.",
        ],
    },
    "EMC_SINGLE_COUNTERMEASURE_UNIVERSAL": {
        "wrong": [
            "EMC 문제는 필터 하나를 설치하면 모든 간섭이 해결된다.",
            "노이즈는 접지 한 지점을 바꾸면 항상 완전히 제거된다.",
        ],
        "safe": [
            "특정 주파수의 노이즈는 적절한 필터 하나로 줄일 수 있다.",
            "EMC 문제는 필터 하나로 모든 간섭을 해결한다는 주장은 잘못이다.",
            "간섭원, 결합경로, 피해기기를 구분하여 필요한 대책을 선정한다.",
        ],
    },
    "EMC_REWIRE_BEFORE_EVIDENCE": {
        "wrong": [
            "노이즈가 보이면 측정 없이 shield와 earth를 먼저 재결선하는 것이 표준 진단 절차다.",
            "잡음이 발생하면 원인 분석 없이 차폐 케이블을 먼저 재결선해야 한다.",
        ],
        "safe": [
            "노이즈를 측정하고 원인을 확인한 뒤 차폐의 연결 불량을 재결선한다.",
            "측정 없이 차폐와 접지를 먼저 재결선하는 것이 표준이라는 주장은 틀리다.",
            "작업 중 잘못 연결된 shield는 설계 기준에 맞게 수정한다.",
        ],
    },
}

EXPECTED_CLASSIFICATIONS = {
    "EMC_SINGLE_POINT_UNIVERSAL": "major",
    "EMC_SHIELD_REPLACES_PE": "fatal",
    "EMC_REDUNDANCY_IGNORES_CCF": "major",
    "EMC_GROUND_LOOP_RESISTANCE_ONLY": "major",
    "EMC_SINGLE_COUNTERMEASURE_UNIVERSAL": "major",
    "EMC_REWIRE_BEFORE_EVIDENCE": "major",
}


class EMCRemainingSixTests(unittest.TestCase):
    def test_variants_rebuttals_conditions(self):
        for code, sentences in MATRIX.items():
            for label, expected_hit in (("wrong", True), ("safe", False)):
                for i, sentence in enumerate(sentences[label]):
                    with self.subTest(code=code, label=label, index=i):
                        hits = {
                            item["code"]
                            for item in evaluate_engineering_invariants(
                                sentence, topic_ids=[TOPIC]
                            )["violations"]
                            if item["code"] in EXPECTED_CLASSIFICATIONS
                        }
                        self.assertEqual(hits, {code} if expected_hit else set())

    def test_other_topics_do_not_inherit_scoped_emc_rules(self):
        for code, sentences in MATRIX.items():
            for sentence in sentences["wrong"]:
                with self.subTest(code=code):
                    hits = {
                        item["code"]
                        for item in evaluate_engineering_invariants(
                            sentence, topic_ids=["thermocouple_temperature_sensor_seebeck_reference_junction_compensation"]
                        )["violations"]
                    }
                    self.assertFalse(hits & set(MATRIX))

    def test_contract_classification_and_scoring_exclusions(self):
        logic = json.loads((PACK / "logic_check.json").read_text(encoding="utf-8"))
        facts = json.loads((PACK / "fact_anchor.json").read_text(encoding="utf-8"))
        contract = validate_topic_machine_contract(logic["machine_contract"], topic_id=TOPIC)
        bound = {row["invariant_code"]: row for row in contract["invariant_bindings"]}
        self.assertEqual(len(bound), 9)
        for code, severity in EXPECTED_CLASSIFICATIONS.items():
            with self.subTest(code=code):
                self.assertEqual(bound[code]["classification"], severity)
                # The standalone source bundle omits the external hold-list JSON.
                # Run this assertion and downstream adapter check on the server.
                hold_files_present = (ROOT / "grading/evidence/fact_anchor_scoring_exclusions_20261101.json").is_file()
                if hold_files_present:
                    self.assertTrue(all(excluded_from_scoring(topic_id=TOPIC, anchor_id=anchor_id)
                                        for anchor_id in bound[code]["requirement_refs"]))
                    evaluation = evaluate_deterministic_requirements(
                    claims=[], invariant_codes=[code], topic_ids=[TOPIC],
                    extraction_complete=True,
                )
                    matched = [row for row in evaluation["findings"] if row["invariant_code"] == code]
                    self.assertEqual(len(matched), 1)
                    self.assertEqual(matched[0]["classification"], severity)
                    self.assertEqual(evaluation["fatal_or_core_error"], severity == "fatal")
                    refs = set(matched[0]["requirement_refs"])
                    actual_wrong = {row["requirement_id"] for row in evaluation["requirements"]
                                    if row["status"] == "WRONG"}
                    self.assertTrue(refs <= actual_wrong)
        fact_sev = {row["id"]: row["severity"] for row in facts["fatal_wrong_claims"]}
        for binding in bound.values():
            self.assertEqual(binding["classification"], fact_sev[binding["rule_id"]])

    def test_original_fatal_rules_retained(self):
        cases = [
            ("EMC_UNSAFE_PE_DISCONNECTION", "계장 노이즈를 없애기 위해 보호접지 PE를 제거한다."),
            ("EMC_SHIELD_ONE_END_UNIVERSAL", "모든 차폐 케이블은 반드시 한쪽만 접지한다."),
            ("EMC_UPS_UNIVERSAL_FIX", "UPS를 사용하면 모든 EMC 문제가 해결된다."),
        ]
        for code, sentence in cases:
            with self.subTest(code=code):
                hits = {item["code"] for item in evaluate_engineering_invariants(sentence, topic_ids=[TOPIC])["violations"]}
                self.assertIn(code, hits)

    def test_integration_scoring_unchanged_and_golden_abstains(self):
        from grading.scoring.deterministic_primary_grader import (
            DeterministicPrimaryError, grade_deterministically,
        )
        data = json.loads((ROOT / "calibration/expert_accuracy_model_answer_cases.json").read_text(encoding="utf-8"))
        model = next(item for item in data["cases"] if item["case_id"].startswith("model_reference_08_instrumentation_power"))
        with self.assertRaisesRegex(DeterministicPrimaryError, "deterministic score engine abstained"):
            grade_deterministically(question_text=model["question"], answer_text=model["answer"], qualitative_de_mode="off")
        # No need to lift positive Anchor holds to check that a direct
        # contradiction reaches the deterministic requirement evaluator.
        for code, severity in EXPECTED_CLASSIFICATIONS.items():
            sentence = MATRIX[code]["wrong"][0]
            violations = evaluate_engineering_invariants(sentence, topic_ids=[TOPIC])["violations"]
            evaluation = evaluate_deterministic_requirements(
                claims=[], invariant_codes=[v["code"] for v in violations],
                topic_ids=[TOPIC], extraction_complete=True,
            )
            matched = [f for f in evaluation["findings"] if f["invariant_code"] == code]
            self.assertEqual(len(matched), 1)
            self.assertEqual(matched[0]["classification"], severity)


if __name__ == "__main__":
    unittest.main()
