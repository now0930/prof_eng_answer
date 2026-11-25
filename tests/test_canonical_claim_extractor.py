import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.evidence.canonical_claim_extractor import extract_canonical_claim_evidence
from grading.scoring.deterministic_requirement_evaluator import evaluate_deterministic_requirements


TOPIC = "functional_safety_reliability_modeling_fta_markov_rbd_ccf_pfd_pfh"


def evaluate(answer: str, *, complete: bool = True):
    extraction = extract_canonical_claim_evidence(
        answer,
        question_text="요구모드별 PFDavg와 PFH를 설명하시오.",
        topic_ids=[TOPIC],
    )
    result = evaluate_deterministic_requirements(
        claims=extraction["canonical_evidence"]["claims"],
        invariant_codes=[],
        topic_ids=[TOPIC],
        extraction_complete=complete,
    )
    return extraction, {
        row["requirement_id"]: row for row in result["requirements"]
    }, result


class CanonicalClaimExtractorTests(unittest.TestCase):

    def test_short_ascii_alias_boundaries(self):
        from grading.evidence.canonical_claim_extractor import (
            _find_alias,
            _find_subject_alias,
        )

        self.assertIsNone(_find_alias("traceability", ["AC"]))
        self.assertIsNone(_find_alias("blockchain", ["AI"]))

        self.assertIsNotNone(_find_alias("AC/DC 변환기", ["AC"]))
        self.assertIsNotNone(_find_alias("AC/DC 변환기", ["DC"]))
        self.assertIsNotNone(_find_alias("AI가 작성한 코드", ["AI"]))

        self.assertIsNone(
            _find_subject_alias("traceability", ["AC"])
        )

    def test_normal_relation_is_canonical_and_satisfied(self):
        extraction, rows, _ = evaluate(
            "PFDavg는 저수요 모드에 적용한다. "
            "PFH는 고수요 및 연속수요 모드에 적용한다."
        )
        claims = extraction["canonical_evidence"]["claims"]
        self.assertTrue(any(
            row["subject"] == "pfdavg"
            and row["predicate"] == "applies_to"
            and row["object"] == "low_demand"
            for row in claims
        ))
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "SATISFIED")
        self.assertEqual(extraction["provider_calls"], 0)

    def test_korean_object_first_word_order_selects_nearest_metric(self):
        extraction, rows, _ = evaluate(
            "저수요에는 PFDavg를 사용한다. 고수요와 연속수요에는 PFH를 적용한다."
        )
        claims = extraction["canonical_evidence"]["claims"]
        relations = {
            (row["subject"], row["predicate"], row["object"])
            for row in claims
        }
        self.assertIn(("pfdavg", "applies_to", "low_demand"), relations)
        self.assertIn(("pfh", "applies_to", "high_demand"), relations)
        self.assertIn(("pfh", "applies_to", "continuous_demand"), relations)
        self.assertNotIn(("pfdavg", "applies_to", "high_demand"), relations)
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "SATISFIED")

    def test_partial_relation_is_not_promoted_to_satisfied(self):
        _, rows, _ = evaluate("PFDavg는 저수요 모드에 적용한다.")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "PARTIAL")

    def test_explicit_opposite_polarity_is_wrong(self):
        _, rows, _ = evaluate("PFDavg는 저수요 모드에 적용하지 않는다.")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "WRONG")

    def test_wrong_relation_object_is_not_treated_as_partial(self):
        _, rows, _ = evaluate("PFDavg는 고수요 모드에 적용한다.")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "WRONG")

    def test_quoted_claim_is_not_adopted_as_credit(self):
        _, rows, result = evaluate(
            '일부는 "PFDavg는 저수요 모드에 적용한다"라고 주장한다.',
            complete=False,
        )
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "UNKNOWN")
        self.assertTrue(result["evidence_allocation"]["ignored_nonasserted_claim_ids"])

    def test_rejected_wrong_example_then_correction_uses_final_claim(self):
        extraction, rows, _ = evaluate(
            "잘못된 예시는 PFDavg를 고수요 모드에 적용하는 것이다. "
            "올바르게는 PFDavg를 저수요 모드에 적용한다."
        )
        corrected = [
            row for row in extraction["canonical_evidence"]["claims"]
            if row["object"] == "low_demand"
        ]
        self.assertEqual(corrected[0]["assertion_context"], "corrected")
        self.assertEqual(rows["demand_mode_metric_selection"]["status"], "PARTIAL")

    def test_one_claim_cannot_credit_two_requirements(self):
        claim = {
            "claim_id": "one_claim",
            "subject": "pfdavg",
            "predicate": "applies_to",
            "object": "low_demand",
            "polarity": "positive",
        }
        result = evaluate_deterministic_requirements(
            claims=[claim], invariant_codes=[], topic_ids=[TOPIC],
            extraction_complete=True,
        )
        credited = [
            row for row in result["requirements"]
            if "one_claim" in row["evidence_claim_ids"]
        ]
        self.assertEqual(len(credited), 1)
        self.assertEqual(result["evidence_allocation"]["duplicate_credit_count"], 0)

    def test_repeatability_is_exact(self):
        answer = "PFDavg는 저수요 모드에 적용하고 PFH는 고수요 모드에 적용한다."
        first = extract_canonical_claim_evidence(answer, topic_ids=[TOPIC])
        for _ in range(10):
            self.assertEqual(first, extract_canonical_claim_evidence(answer, topic_ids=[TOPIC]))

    def test_neighboring_clauses_do_not_cross_bind_relations(self):
        extraction, _, _ = evaluate(
            "고장률은 시간당 고장률이고 PFDavg는 무차원이다."
        )
        claims = extraction["canonical_evidence"]["claims"]
        self.assertFalse(any(
            row["subject"] == "pfdavg"
            and row["predicate"] == "equivalent_to"
            and row["object"] == "failure_rate"
            and row["polarity"] == "positive"
            for row in claims
        ))

    def test_ratio_prose_preserves_numerator_denominator_order(self):
        topic = "hazop_lopa_ipl_risk_reduction_sil_target_allocation"
        answer = "요구 RRF는 residual frequency를 tolerable frequency로 나눈 값이다."
        evidence = extract_canonical_claim_evidence(
            answer,
            question_text="LOPA의 계산 절차와 residual frequency 및 RRF 산정방법을 설명하시오.",
            topic_ids=[topic],
        )["canonical_evidence"]["claims"]
        self.assertTrue(any(
            (row["subject"], row["predicate"], row["object"], row["polarity"])
            == ("required_rrf", "derived_by_ratio", "residual_tolerable_frequency_ratio", "positive")
            for row in evidence
        ))
        reverse = extract_canonical_claim_evidence(
            "요구 RRF는 residual frequency를 tolerable frequency로 나눈 값이 아니다.",
            question_text="LOPA의 계산 절차와 residual frequency 및 RRF 산정방법을 설명하시오.",
            topic_ids=[topic],
        )["canonical_evidence"]["claims"]
        self.assertTrue(any(
            row["subject"] == "required_rrf"
            and row["object"] == "residual_tolerable_frequency_ratio"
            and row["polarity"] == "negative"
            for row in reverse
        ))

    def test_slash_space_alias_and_negative_distinct_relation(self):
        topic = "instrumentation_power_grounding_shielding_ups_ground_loop_emc"
        question = "보호접지, signal/reference ground와 bonding의 역할 및 설계 유의점을 설명하시오."
        for answer, polarity in (
            ("보호접지와 signal reference ground의 목적은 구분된다.", "positive"),
            ("보호접지와 signal reference ground의 목적은 구분되지 않고 동일하다.", "negative"),
        ):
            claims = extract_canonical_claim_evidence(
                answer, question_text=question, topic_ids=[topic],
            )["canonical_evidence"]["claims"]
            self.assertTrue(any(
                row["subject"] == "emc_protective_earth"
                and row["predicate"] == "distinct_from"
                and row["object"] == "emc_signal_reference"
                and row["polarity"] == polarity
                for row in claims
            ))

    def test_encoded_negative_predicate_inverts_only_positive_surface_claim(self):
        topic = "safety_critical_software_structural_coverage_mcdc_static_dynamic_analysis"
        question = "MC/DC의 개념, 목적과 충족조건을 설명하시오."
        expected = {
            "100% MC/DC는 전체 SIL 달성을 단독으로 보장하지 않는다.": "positive",
            "100% MC/DC는 전체 SIL 달성을 단독으로 보장한다.": "negative",
        }
        for answer, polarity in expected.items():
            claims = extract_canonical_claim_evidence(
                answer, question_text=question, topic_ids=[topic],
            )["canonical_evidence"]["claims"]
            self.assertTrue(any(
                row["subject"] == "mcdc"
                and row["predicate"] == "does_not_guarantee"
                and row["object"] == "total_sil_assurance"
                and row["polarity"] == polarity
                for row in claims
            ))


if __name__ == "__main__":
    unittest.main()
