"""Positive EMC fact identity and evidence boundaries; held anchors stay on HOLD.

These tests assert technical relationship identity, not scoring authorization.
They intentionally do not alter the five Fact Anchor scoring exclusions.
"""

import json
import unittest
from pathlib import Path

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.evidence.topic_machine_contract import validate_topic_machine_contract

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC
HOLDS = {
    "ipgse_scope_chain", "ipgse_emi_coupling_paths", "ipgse_power_quality_scope",
    "ipgse_final_verification", "ipgse_diagnostic_workflow",
}
FACT_IDS = {
    "ipgse_scope_chain": {"emc_scope_source_path", "emc_scope_path_victim"},
    "ipgse_emi_coupling_paths": {"emc_coupling_paths_check"},
    "ipgse_power_quality_scope": {"emc_power_reliability_scope"},
    "ipgse_final_verification": {
        "emc_verification_repeat_conditions", "emc_verification_before_after",
    },
}

SAMPLES = {
    "ipgse_scope_chain": (
        "간섭원, 결합경로, 영향을 받는 신호·기기를 구분하고 실제 배선 및 측정을 통해 원인을 좁힌다."
    ),
    "ipgse_emi_coupling_paths": (
        "Conducted/radiated/capacitive/inductive/common-impedance coupling을 "
        "source-path-victim으로 진단한다."
    ),
    "ipgse_power_quality_scope": (
        "계장 전원 이상을 분석할 때 전압 강하·상승과 순간정전 등 전원품질 항목을 측정한다."
    ),
    "ipgse_final_verification": (
        "간섭 대책은 동일 조건에서 재검증한다. 간섭 대책을 적용하고 조치 전의 측정 기록과 "
        "비교하여 개선 여부를 평가한다."
    ),
}


class EMCAnchorMeaningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = validate_topic_machine_contract(
            json.loads((PACK / "logic_check.json").read_text(encoding="utf-8"))["machine_contract"],
            topic_id=TOPIC,
        )
        cls.facts = {row["fact_id"]: row for row in cls.contract["facts"]}
        cls.rules = {row["requirement_id"]: row for row in cls.contract["requirement_rules"]}

    @staticmethod
    def extract_claim_keys(text):
        evidence = extract_canonical_claim_evidence(text, topic_ids=[TOPIC])
        return {
            (c["subject"], c["predicate"], c["object"], c["polarity"])
            for c in evidence["canonical_evidence"]["claims"]
            if c.get("assertion_context") in {"asserted", "corrected"}
        }

    def test_no_duplicate_or_off_topic_fact_identity(self):
        actual = {anchor: set(self.rules[anchor]["required_fact_ids"]) for anchor in FACT_IDS}
        self.assertEqual(actual, FACT_IDS)
        distinct = set.union(*actual.values())
        self.assertEqual(len(distinct), sum(map(len, actual.values())))
        self.assertEqual(self.rules["ipgse_scope_chain"]["minimum_match_count"], 2)
        self.assertEqual(self.rules["ipgse_final_verification"]["minimum_match_count"], 2)
        for anchor, fact_ids in actual.items():
            for fid in fact_ids:
                self.assertIn(fid, self.facts)
                fact = self.facts[fid]
                self.assertNotEqual(fact["object"], "emc_signal_reference" if anchor != "ipgse_scope_chain" else "emc_protective_earth")
                self.assertNotEqual(fact["subject"], "emc_ups")
                self.assertNotEqual(fact["subject"], "emc_shield")

    def test_positive_sentences_emit_only_their_own_fact_relations(self):
        all_facts = {
            fid: (f["subject"], f["predicate"], f["object"], f["polarity"])
            for fid, f in self.facts.items()
            if fid in set.union(*FACT_IDS.values())
        }
        for anchor, text in SAMPLES.items():
            with self.subTest(anchor=anchor):
                keys = self.extract_claim_keys(text)
                observed = {fid for fid, key in all_facts.items() if key in keys}
                self.assertEqual(observed, FACT_IDS[anchor], observed)

    def test_pe_shield_ups_truths_are_not_scoring_evidence_for_other_anchors(self):
        unrelated = (
            "보호접지와 신호접지를 구분한다. "
            "Shield termination은 주파수 조건에 따라 결정한다. "
            "UPS가 모든 EMC 문제를 해결하지는 못한다."
        )
        keys = self.extract_claim_keys(unrelated)
        for fid in set.union(*FACT_IDS.values()):
            f = self.facts[fid]
            self.assertNotIn((f["subject"], f["predicate"], f["object"], f["polarity"]), keys)

    def test_incorrect_emc_shortcuts_do_not_produce_positive_contract_evidence(self):
        wrong = "UPS를 설치하면 모든 EMC 문제가 해결된다. 필터 하나로 EMI가 사라진다."
        keys = self.extract_claim_keys(wrong)
        for fid in set.union(*FACT_IDS.values()):
            f = self.facts[fid]
            self.assertNotIn((f["subject"], f["predicate"], f["object"], f["polarity"]), keys)

    def test_explicit_negations_do_not_become_positive_credit(self):
        cases = {
            "ipgse_scope_chain": "간섭원, 결합경로, 피해기기를 구분하지 않는다.",
            "ipgse_emi_coupling_paths": (
                "Conducted/radiated/capacitive/inductive coupling을 "
                "source-path-victim으로 진단하지 않는다."
            ),
            "ipgse_power_quality_scope": (
                "계장 전원 이상에서 순간정전을 측정할 필요가 없다."
            ),
            "ipgse_final_verification": (
                "간섭 대책은 동일 조건에서 재검증하지 않는다."
            ),
        }
        for anchor, text in cases.items():
            with self.subTest(anchor=anchor):
                keys = self.extract_claim_keys(text)
                for fid in FACT_IDS[anchor]:
                    f = self.facts[fid]
                    self.assertNotIn(
                        (f["subject"], f["predicate"], f["object"], "positive"),
                        keys,
                    )

    def test_all_five_positive_holds_unchanged(self):
        for anchor in HOLDS:
            with self.subTest(anchor=anchor):
                self.assertTrue(excluded_from_scoring(topic_id=TOPIC, anchor_id=anchor))


if __name__ == "__main__":
    unittest.main()
