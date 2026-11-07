"""Production qualification is fail-closed; never changes awarded points."""
from __future__ import annotations

from copy import deepcopy
import os
import unittest
from unittest.mock import patch

from grading.quality.production_grade_gate import (
    ProductionGradeFailure,
    require_production_grade_success,
)
from scripts.release_candidate import (
    ReleaseFailure,
    _current_production_scoring_contract,
)


def valid_grade() -> dict:
    breakdown = {
        "A_structure": 2.0,
        "B_requirement_completeness": 3.0,
        "C_fact_correctness": 3.0,
        "D_engineering_judgment": 2.0,
        "E_linkage": 1.0,
    }
    return {
        "marker": "DETERMINISTIC_GRADING_PRIMARY_V1",
        "grading_engine": "deterministic_abc_argon_de",
        "llm_verdict_authority": 0,
        "external_llm_required_for_verdict": False,
        "llm_score_authority": "D_E_ONLY",
        "total_score": 11.0,
        "resolution_review": {"required": False, "score_status": "final"},
        "requirements": [{"requirement_id": "r1", "status": "PARTIAL"}],
        "deterministic_score": {
            "marker": "DETERMINISTIC_SCORE_ENGINE_V1",
            "decision": "SCORED",
            "llm_verdict_authority": 0,
            "qualitative_de_score_effect": "replace_de",
            "score_breakdown": breakdown,
            "total_score": 11.0,
        },
        "qualitative_de_evaluation": {
            "mode": "argon",
            "status": "APPLIED",
            "provider": "argon",
            "score_effect": "replace_de",
            "provider_calls": 1,
            "request_hash": "1" * 64,
            "input_hash": "2" * 64,
            # Validating literal provenance does NOT certify semantic truth.
            "semantic_truth_verified": False,
            "criteria": [{"criterion_id": name} for name in ("D1", "D2", "D3", "E1", "E2")],
            "proposed_scores": {"D_engineering_judgment": 2.0, "E_linkage": 1.0},
            "effective_scores": {"D_engineering_judgment": 2.0, "E_linkage": 1.0},
        },
    }


class ProductionGradeGateTest(unittest.TestCase):
    def test_accepts_applied_argon_without_altering_grade(self):
        grade = valid_grade()
        original = deepcopy(grade)
        self.assertIsNone(require_production_grade_success(grade, "public-test"))
        self.assertEqual(grade, original)

    def test_rejects_legacy_semantic_result_as_current_production_evidence(self):
        grade = valid_grade()
        grade["marker"] = "phase2_layered_scoring_v1"
        grade["gemini_semantic_evaluation"] = {"parsed": {}, "ok": True}
        with self.assertRaisesRegex(ProductionGradeFailure, "not_deterministic_primary"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_fallback_even_when_deterministic_result_exists(self):
        grade = valid_grade()
        grade["qualitative_de_evaluation"]["status"] = "FALLBACK"
        with self.assertRaisesRegex(ProductionGradeFailure, "argon_de_not_applied"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_missing_provider_call(self):
        grade = valid_grade()
        grade["qualitative_de_evaluation"]["provider_calls"] = 0
        with self.assertRaisesRegex(ProductionGradeFailure, "argon_provider_call_missing"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_missing_deterministic_grade(self):
        grade = valid_grade()
        grade["deterministic_score"]["decision"] = "ABSTAIN"
        with self.assertRaisesRegex(ProductionGradeFailure, "deterministic_score_not_completed"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_invalid_abc_and_argon_scores(self):
        for layer in ("C_fact_correctness", "E_linkage"):
            with self.subTest(layer=layer):
                grade = valid_grade()
                grade["deterministic_score"]["score_breakdown"][layer] = float("nan")
                with self.assertRaises(ProductionGradeFailure):
                    require_production_grade_success(grade, "public-test")

    def test_rejects_mismatch_between_argon_and_applied_de(self):
        grade = valid_grade()
        grade["qualitative_de_evaluation"]["effective_scores"]["E_linkage"] = 0
        with self.assertRaisesRegex(ProductionGradeFailure, "argon_E_linkage_score_mismatch"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_provisional_resolution(self):
        grade = valid_grade()
        grade["resolution_review"] = {"required": True, "score_status": "provisional"}
        with self.assertRaisesRegex(ProductionGradeFailure, "unresolved_requirement"):
            require_production_grade_success(grade, "public-test")

    def test_rejects_provider_exception_not_recast_as_score(self):
        grade = valid_grade()
        grade["qualitative_de_evaluation"]["status"] = "FALLBACK"
        grade["qualitative_de_evaluation"]["reason_code"] = "ProviderHTTPError"
        with self.assertRaises(ProductionGradeFailure):
            require_production_grade_success(grade, "public-test")

    def test_rejects_mismatched_total_without_regrading(self):
        grade = valid_grade()
        grade["total_score"] = 12
        with self.assertRaisesRegex(ProductionGradeFailure, "deterministic_total_mismatch"):
            require_production_grade_success(grade, "public-test")


class RuntimeConfigurationTest(unittest.TestCase):
    def test_requires_actual_runtime_mode_and_exact_argon_credential(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ReleaseFailure, "deterministic A/B/C"):
                _current_production_scoring_contract()
        with patch.dict(os.environ, {"DETERMINISTIC_GRADING_PRIMARY": "true"}, clear=True):
            with self.assertRaisesRegex(ReleaseFailure, "Argon D/E"):
                _current_production_scoring_contract()
        with patch.dict(os.environ, {
            "DETERMINISTIC_GRADING_PRIMARY": "true",
            "QUALITATIVE_DE_MODE": "argon",
            "GOOGLE_API_KEY": "alias-does-not-work-in-transport",
        }, clear=True):
            with self.assertRaisesRegex(ReleaseFailure, "GEMINI_API_KEY"):
                _current_production_scoring_contract()
        with patch.dict(os.environ, {
            "DETERMINISTIC_GRADING_PRIMARY": "true",
            "QUALITATIVE_DE_MODE": "argon",
            "GEMINI_API_KEY": "fake-not-for-real-use",
        }, clear=True):
            self.assertEqual(_current_production_scoring_contract()["qualitative_de_mode"], "argon")


if __name__ == "__main__":
    unittest.main()
