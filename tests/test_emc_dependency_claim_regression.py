"""Regression lock for noncore EMC requirement, not a new scoring feature.

The real machine contract is excluded from positive scoring.  Only an explicit
independent invariant is permitted to trigger a WRONG/fatal requirement record.
Use the repository's actual extractor and deterministic evaluator.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.scoring.deterministic_requirement_evaluator import (
    evaluate_deterministic_requirements,
    load_machine_contracts,
)

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
TARGET = "ipgse_shield_termination_frequency"
FACT_ID = "emc_shield_termination_depends_on_conditions"
INVARIANT = "EMC_SHIELD_ONE_END_UNIVERSAL"


def evaluate(answer, *, invariant_codes=()):
    extraction = extract_canonical_claim_evidence(
        answer,
        question_text="EMC 차폐 케이블의 종단 방식 선정조건을 설명하시오.",
        topic_ids=[TOPIC],
    )
    evaluation = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=list(invariant_codes),
        topic_ids=[TOPIC],
        extraction_complete=extraction["extraction_complete"],
    )
    return extraction, evaluation


class EMCNoncoreScoringGateTests(unittest.TestCase):
    def test_excluded_requirement_and_machine_fact_are_still_declared(self):
        self.assertTrue(excluded_from_scoring(topic_id=TOPIC, anchor_id=TARGET))
        contract = next(c for c in load_machine_contracts([TOPIC])
                        if c["owner_topic_id"] == TOPIC)
        self.assertTrue(any(f["fact_id"] == FACT_ID for f in contract["facts"]))
        self.assertTrue(any(
            r["requirement_id"] == TARGET and FACT_ID in r["required_fact_ids"]
            for r in contract["requirement_rules"]
        ))

    def test_asserted_positive_answer_is_omitted_not_satisfied(self):
        extraction, evaluation = evaluate(
            "차폐 케이블은 주파수·본딩 조건에 따라 달라진다."
        )
        self.assertFalse(any(r["requirement_id"] == TARGET
                             for r in evaluation["requirements"]))
        self.assertFalse(evaluation["fatal_or_core_error"])
        self.assertEqual(evaluation["score_effect"], "none")
        self.assertEqual(extraction["provider_calls"], 0)

    def test_direct_exact_machine_claim_cannot_bypass_exclusion(self):
        exact_claim = {
            "claim_id": "direct_exact",
            "subject": "emc_shield",
            "predicate": "depends_on",
            "object": "emc_frequency_bonding",
            "polarity": "positive",
            "assertion_context": "asserted",
        }
        evaluation = evaluate_deterministic_requirements(
            claims=[exact_claim], invariant_codes=[], topic_ids=[TOPIC],
            extraction_complete=True,
        )
        self.assertFalse(any(r["requirement_id"] == TARGET
                             for r in evaluation["requirements"]))
        self.assertEqual(evaluation["score_effect"], "none")

    def test_negation_quotation_hypothesis_and_mention_do_not_open_scoring(self):
        answers = (
            "차폐 케이블은 주파수·본딩 조건에 따라 달라지지 않는다.",
            "차폐 케이블은 주파수·본딩 조건에 따라 달라지지 않는 것은 아니다.",
            "차폐 케이블의 종단은 주파수·본딩 조건에 따라 달라질 수 있다면 검토한다.",
            '일부는 "차폐 케이블은 주파수·본딩 조건에 따라 달라진다"라고 주장한다.',
            "차폐 케이블과 주파수·본딩 조건을 함께 표시한다.",
            "차폐 케이블은 주파수에 따라 달라진다.",
        )
        for answer in answers:
            with self.subTest(answer=answer):
                _, evaluation = evaluate(answer)
                self.assertFalse(any(r["requirement_id"] == TARGET
                                     for r in evaluation["requirements"]))
                self.assertFalse(evaluation["fatal_or_core_error"])

    def test_negative_machine_claim_alone_cannot_create_wrong(self):
        direct_negative = {
            "claim_id": "direct_negative",
            "subject": "emc_shield",
            "predicate": "depends_on",
            "object": "emc_frequency_bonding",
            "polarity": "negative",
            "assertion_context": "asserted",
        }
        evaluation = evaluate_deterministic_requirements(
            claims=[direct_negative], invariant_codes=[], topic_ids=[TOPIC],
            extraction_complete=True,
        )
        self.assertFalse(any(r["requirement_id"] == TARGET
                             for r in evaluation["requirements"]))
        self.assertFalse(evaluation["fatal_or_core_error"])

    def test_explicit_independent_invariant_remains_wrong_and_fatal(self):
        _, evaluation = evaluate(
            "차폐 케이블은 주파수·본딩 조건에 따라 달라진다.",
            invariant_codes=[INVARIANT],
        )
        target_rows = [r for r in evaluation["requirements"]
                       if r["requirement_id"] == TARGET]
        self.assertEqual(len(target_rows), 1)
        self.assertEqual(target_rows[0]["status"], "WRONG")
        self.assertEqual(target_rows[0]["evidence_mode"], "canonical_claim")
        self.assertTrue(evaluation["fatal_or_core_error"])
        self.assertFalse(evaluation["requirement_full_credit_allowed"])
        self.assertTrue(any(
            row["invariant_code"] == INVARIANT and row["owner_topic_id"] == TOPIC
            for row in evaluation["findings"]
        ))

    def test_no_scoring_admission_by_other_topic_routing(self):
        _, evaluation = evaluate("차폐 케이블은 주파수·본딩 조건에 따라 달라진다.")
        self.assertEqual(
            sum(r["requirement_id"] == TARGET for r in evaluation["requirements"]),
            0,
        )
        self.assertEqual(evaluation["evidence_allocation"]["duplicate_credit_count"], 0)


if __name__ == "__main__":
    unittest.main()
