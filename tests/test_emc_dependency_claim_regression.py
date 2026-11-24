"""Fail-closed EMC dependency relation regression, independent of LLM scoring.

This tests the real extractor -> canonical evidence -> deterministic requirement
path on synthetic answers.  No Fact/score approval is implied.
"""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.evidence.canonical_claim_extractor import (
    extract_canonical_claim_evidence,
    _load_predicates,
    _load_aliases,
)
from grading.scoring.deterministic_requirement_evaluator import (
    evaluate_deterministic_requirements,
)

TOPIC = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
TARGET = "ipgse_shield_termination_frequency"
SUBJECT = "emc_shield"
PREDICATE = "depends_on"
OBJECT = "emc_frequency_bonding"
POSITIVE = "차폐 케이블은 주파수·본딩 조건에 따라 달라진다."
NEGATIVE = "차폐 케이블은 주파수·본딩 조건에 따라 달라지지 않는다."
OTHER_NEGATIVE = "차폐 케이블은 주파수·본딩 조건에 따라 결정되지 않는다."


def evaluate(answer):
    extraction = extract_canonical_claim_evidence(
        answer, question_text="EMC 차폐 케이블의 종단 방식 선정조건을 설명하시오.",
        topic_ids=[TOPIC],
    )
    evaluation = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[], topic_ids=[TOPIC],
        extraction_complete=extraction["extraction_complete"],
    )
    rows = {row["requirement_id"]: row for row in evaluation["requirements"]}
    return extraction, rows, evaluation


class EMCDependencyClaimTests(unittest.TestCase):

    def test_contract_predicate_is_declared_and_bounded(self):
        aliases = _load_predicates()
        self.assertIn(PREDICATE, aliases)
        self.assertTrue(any("에 따라 달라" in term for term in aliases[PREDICATE]))
        self.assertNotIn("조건", aliases[PREDICATE])
        self.assertNotIn("따라", aliases[PREDICATE])
        self.assertNotIn("주파수", _load_aliases()[OBJECT])

    def test_positive_explicit_dependency_is_satisfied(self):
        extraction, rows, result = evaluate(POSITIVE)
        self.assertEqual(rows[TARGET]["status"], "SATISFIED")
        self.assertTrue(any(
            claim["subject"] == SUBJECT
            and claim["predicate"] == PREDICATE
            and claim["object"] == OBJECT
            and claim["polarity"] == "positive"
            and claim["assertion_context"] == "asserted"
            for claim in extraction["canonical_evidence"]["claims"]
        ))
        self.assertEqual(result["score_effect"], "none")
        self.assertEqual(extraction["provider_calls"], 0)
        self.assertEqual(result["llm_verdict_authority"], 0)

    def test_korean_negated_dependency_is_wrong_not_satisfied(self):
        for answer in (NEGATIVE, OTHER_NEGATIVE):
            with self.subTest(answer=answer):
                extraction, rows, result = evaluate(answer)
                self.assertEqual(rows[TARGET]["status"], "WRONG")
                self.assertTrue(any(
                    claim["subject"] == SUBJECT
                    and claim["predicate"] == PREDICATE
                    and claim["object"] == OBJECT
                    and claim["polarity"] == "negative"
                    for claim in extraction["canonical_evidence"]["claims"]
                ))
                self.assertFalse(result["fatal_or_core_error"])

    def test_unrelated_object_mention_cannot_earn_credit(self):
        for answer in (
            "차폐 케이블은 주파수·본딩 조건이라는 용어를 정리한다.",
            "차폐 케이블과 주파수·본딩 조건을 함께 표시한다.",
            "차폐 케이블은 주파수·본딩 조건을 목록에 기록한다.",
        ):
            with self.subTest(answer=answer):
                _, rows, _ = evaluate(answer)
                self.assertNotEqual(rows[TARGET]["status"], "SATISFIED")

    def test_frequency_only_does_not_earn_composite_credit(self):
        _, rows, _ = evaluate("차폐 케이블은 주파수에 따라 달라진다.")
        self.assertNotEqual(rows[TARGET]["status"], "SATISFIED")

    def test_quoted_relation_does_not_earn_credit(self):
        extraction, rows, evaluation = evaluate(
            '일부는 "차폐 케이블은 주파수·본딩 조건에 따라 달라진다"라고 주장한다.'
        )
        self.assertNotEqual(rows[TARGET]["status"], "SATISFIED")
        self.assertTrue(evaluation["evidence_allocation"]["ignored_nonasserted_claim_ids"])

    def test_dependency_cannot_credit_neighboring_topic(self):
        extraction = extract_canonical_claim_evidence(
            POSITIVE, topic_ids=["functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"],
        )
        self.assertFalse(any(
            row["subject"] == SUBJECT and row["predicate"] == PREDICATE
            for row in extraction["canonical_evidence"]["claims"]
        ))

    def test_correct_relation_changes_only_target_requirement(self):
        _, before, _ = evaluate("")
        _, after, result = evaluate(POSITIVE)
        changed = {
            key for key in before
            if before[key]["status"] != after[key]["status"]
        }
        self.assertEqual(changed, {TARGET})
        self.assertEqual(result["evidence_allocation"]["duplicate_credit_count"], 0)

    def test_extraction_deterministic_repeated(self):
        first, rows, _ = evaluate(POSITIVE)
        for _ in range(3):
            again, more_rows, _ = evaluate(POSITIVE)
            self.assertEqual(first, again)
            self.assertEqual(rows[TARGET], more_rows[TARGET])


if __name__ == "__main__":
    unittest.main()
