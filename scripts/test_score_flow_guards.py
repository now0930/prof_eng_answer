#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading_agents import _phase6_limit_gemini_score
from grade_score_reconciler import _apply_numeric_flags
from difficulty_score_ceiling import (
    _prefer_question_type_adjusted_score,
)
import question_type_coverage_score_adjuster as coverage_adjuster
import question_type_coverage_adapter as qtype_coverage_adapter
from grading_agents import (
    _phase10_apply_generated_single_topic_overrides,
    _phase2_resolve_difficulty_topic_id,
    _phase2_resolve_logic_topic_id,
)


class ScoreFlowGuardTest(unittest.TestCase):
    def test_gemini_d_layer_raise_is_capped(self) -> None:
        result = _phase6_limit_gemini_score(
            layer_id="D",
            base_score=1.62,
            gemini_score=4.5,
            max_score=6.0,
        )

        self.assertEqual(result["effective_score"], 2.37)
        self.assertEqual(result["raise_cap"], 0.75)
        self.assertTrue(result["raise_limited"])

    def test_gemini_c_layer_raise_is_capped(self) -> None:
        result = _phase6_limit_gemini_score(
            layer_id="C",
            base_score=3.64,
            gemini_score=5.0,
            max_score=8.0,
        )

        self.assertEqual(result["effective_score"], 4.39)
        self.assertTrue(result["raise_limited"])

    def test_gemini_downward_adjustment_is_preserved(self) -> None:
        result = _phase6_limit_gemini_score(
            layer_id="C",
            base_score=5.0,
            gemini_score=3.5,
            max_score=8.0,
        )

        self.assertEqual(result["effective_score"], 3.5)
        self.assertFalse(result["raise_limited"])

    def test_coverage_adjusted_score_is_applied(self) -> None:
        grade = {
            "total_score": 18.06,
            "max_score": 25.0,
            "official_pass_score": 15.0,
            "practical_target_score": 17.5,
            "high_score_target": 20.0,
        }

        decision = {
            "original_score": 18.06,
            "adjusted_score": 17.79,
            "applied": False,
            "total_penalty": 0.27,
        }

        with patch.object(
            coverage_adjuster,
            "evaluate_question_type_coverage_score_adjustment",
            return_value=decision,
        ):
            result = (
                coverage_adjuster
                .apply_question_type_coverage_score_adjustment(
                    grade
                )
            )

        self.assertEqual(result["total_score"], 17.79)

        adjustment = result[
            "question_type_coverage_score_adjustment"
        ]

        self.assertTrue(adjustment["applied"])
        self.assertTrue(adjustment["score_flow_applied"])
        self.assertEqual(
            result["pre_question_type_coverage_total_score"],
            18.06,
        )

    def test_ceiling_prefers_lower_coverage_score(self) -> None:
        score, applied = _prefer_question_type_adjusted_score(
            {
                "question_type_coverage_score_adjustment": {
                    "adjusted_score": 17.79,
                }
            },
            18.06,
        )

        self.assertEqual(score, 17.79)
        self.assertTrue(applied)

    def test_ceiling_does_not_raise_score(self) -> None:
        score, applied = _prefer_question_type_adjusted_score(
            {
                "question_type_coverage_score_adjustment": {
                    "adjusted_score": 18.5,
                }
            },
            18.06,
        )

        self.assertEqual(score, 18.06)
        self.assertFalse(applied)




class LogicTopicFallbackRegressionTest(unittest.TestCase):
    def test_primary_reference_topic_has_highest_priority(self) -> None:
        topic_id = _phase2_resolve_logic_topic_id(
            {
                "primary_reference": {
                    "topic_id": "primary_topic",
                },
                "candidates": [
                    {
                        "answer": {
                            "topic_id": "candidate_topic",
                        }
                    }
                ],
            },
            {
                "topic_id": "grade_topic",
            },
            {
                "topic_id": "fact_topic",
            },
        )

        self.assertEqual(
            topic_id,
            "primary_topic",
        )

    def test_first_valid_candidate_topic_is_selected(self) -> None:
        topic_id = _phase2_resolve_logic_topic_id(
            {
                "primary_reference": None,
                "candidates": [
                    None,
                    "invalid",
                    {
                        "answer": {
                            "topic_id": "candidate_topic",
                        }
                    },
                ],
            },
            {
                "topic_id": "grade_topic",
            },
            {
                "topic_id": "fact_topic",
            },
        )

        self.assertEqual(
            topic_id,
            "candidate_topic",
        )

    def test_malformed_candidates_do_not_block_grade_fallback(
        self,
    ) -> None:
        topic_id = _phase2_resolve_logic_topic_id(
            {
                "candidates": [
                    None,
                    "invalid",
                    123,
                    {
                        "answer": "invalid",
                    },
                ],
            },
            {
                "inferred_topic_id": "grade_inferred_topic",
            },
            {
                "topic_id": "fact_topic",
            },
        )

        self.assertEqual(
            topic_id,
            "grade_inferred_topic",
        )

    def test_malformed_candidates_do_not_block_fact_fallback(
        self,
    ) -> None:
        topic_id = _phase2_resolve_logic_topic_id(
            {
                "candidates": [
                    None,
                    {
                        "answer": [],
                    },
                ],
            },
            {},
            {
                "topic_id": "fact_topic",
            },
        )

        self.assertEqual(
            topic_id,
            "fact_topic",
        )

    def test_missing_topic_returns_none(self) -> None:
        topic_id = _phase2_resolve_logic_topic_id(
            {
                "primary_reference": {},
                "candidates": [
                    None,
                    {},
                    {
                        "answer": {},
                    },
                ],
            },
            {},
            {},
        )

        self.assertIsNone(topic_id)




class DifficultyTopicFallbackRegressionTest(unittest.TestCase):
    def test_fact_topic_has_highest_priority(self) -> None:
        topic_id = _phase2_resolve_difficulty_topic_id(
            {
                "topic_id": "fact_topic",
            },
            {
                "primary_reference": {
                    "topic_id": "primary_topic",
                },
                "candidates": [
                    {
                        "answer": {
                            "topic_id": "candidate_topic",
                        }
                    }
                ],
            },
        )

        self.assertEqual(
            topic_id,
            "fact_topic",
        )

    def test_primary_reference_topic_is_selected(self) -> None:
        topic_id = _phase2_resolve_difficulty_topic_id(
            {},
            {
                "primary_reference": {
                    "topic_id": "primary_topic",
                },
                "candidates": [
                    {
                        "answer": {
                            "topic_id": "candidate_topic",
                        }
                    }
                ],
            },
        )

        self.assertEqual(
            topic_id,
            "primary_topic",
        )

    def test_malformed_primary_falls_through_to_candidate(
        self,
    ) -> None:
        topic_id = _phase2_resolve_difficulty_topic_id(
            {},
            {
                "primary_reference": "invalid",
                "candidates": [
                    {
                        "answer": {
                            "topic_id": "candidate_topic",
                        }
                    }
                ],
            },
        )

        self.assertEqual(
            topic_id,
            "candidate_topic",
        )

    def test_invalid_first_candidate_does_not_block_later_candidate(
        self,
    ) -> None:
        topic_id = _phase2_resolve_difficulty_topic_id(
            {},
            {
                "candidates": [
                    None,
                    "invalid",
                    123,
                    {
                        "answer": [],
                    },
                    {
                        "answer": {
                            "topic_id": "later_candidate",
                        }
                    },
                ],
            },
        )

        self.assertEqual(
            topic_id,
            "later_candidate",
        )

    def test_missing_difficulty_topic_returns_none(self) -> None:
        topic_id = _phase2_resolve_difficulty_topic_id(
            {},
            {
                "primary_reference": {},
                "candidates": [
                    None,
                    {},
                    {
                        "answer": {},
                    },
                ],
            },
        )

        self.assertIsNone(topic_id)




class GeneratedSingleTopicOverrideRegressionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bank = {
            "answers": [
                {
                    "topic_id": "generated_topic",
                    "question_type": (
                        "PRINCIPLE_INTERPRETATION"
                    ),
                }
            ]
        }

    def test_general_primary_applies_both_overrides(self) -> None:
        question_type, fact_eval = (
            _phase10_apply_generated_single_topic_overrides(
                self.bank,
                {
                    "primary_type": {
                        "id": "GENERAL",
                    }
                },
                {},
            )
        )

        self.assertEqual(
            question_type["primary_type"]["id"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            fact_eval["topic_id"],
            "generated_topic",
        )

    def test_malformed_primary_applies_both_overrides(self) -> None:
        for malformed_primary in (
            "GENERAL",
            123,
        ):
            with self.subTest(
                primary=malformed_primary,
            ):
                question_type, fact_eval = (
                    _phase10_apply_generated_single_topic_overrides(
                        self.bank,
                        {
                            "primary_type": malformed_primary,
                        },
                        {},
                    )
                )

                self.assertEqual(
                    question_type["primary_type"]["id"],
                    "PRINCIPLE_INTERPRETATION",
                )
                self.assertEqual(
                    fact_eval["topic_id"],
                    "generated_topic",
                )

    def test_answers_none_is_ignored_safely(self) -> None:
        original_question_type = {
            "primary_type": {
                "id": "GENERAL",
            }
        }
        original_fact_eval = {}

        question_type, fact_eval = (
            _phase10_apply_generated_single_topic_overrides(
                {
                    "answers": None,
                },
                original_question_type,
                original_fact_eval,
            )
        )

        self.assertIs(
            question_type,
            original_question_type,
        )
        self.assertIs(
            fact_eval,
            original_fact_eval,
        )

    def test_strong_primary_is_preserved_and_fact_is_filled(
        self,
    ) -> None:
        question_type, fact_eval = (
            _phase10_apply_generated_single_topic_overrides(
                self.bank,
                {
                    "primary_type": {
                        "id": "COMPARE_SELECTION",
                    }
                },
                {},
            )
        )

        self.assertEqual(
            question_type["primary_type"]["id"],
            "COMPARE_SELECTION",
        )
        self.assertNotIn(
            "generated_single_topic_override",
            question_type,
        )
        self.assertEqual(
            fact_eval["topic_id"],
            "generated_topic",
        )

    def test_existing_fact_topic_is_preserved(self) -> None:
        question_type, fact_eval = (
            _phase10_apply_generated_single_topic_overrides(
                self.bank,
                {
                    "primary_type": {
                        "id": "GENERAL",
                    }
                },
                {
                    "topic_id": "existing_fact",
                },
            )
        )

        self.assertEqual(
            question_type["primary_type"]["id"],
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            fact_eval["topic_id"],
            "existing_fact",
        )
        self.assertNotIn(
            "generated_single_topic_override",
            fact_eval,
        )




class ExplicitRequirementCapEnforcementRegressionTest(
    unittest.TestCase
):
    def test_numeric_flags_use_enforced_cap_result(self) -> None:
        def enforce_cap(grade):
            updated = dict(grade)
            updated["total_score"] = 14.0
            updated["explicit_requirement_cap_evaluation"] = {
                "cap_applied": True,
                "capped_score": 14.0,
            }
            return updated

        with patch(
            "explicit_requirement_cap."
            "enforce_existing_explicit_requirement_cap",
            side_effect=enforce_cap,
        ):
            result = _apply_numeric_flags(
                {
                    "total_score": 18.0,
                    "max_score": 25.0,
                }
            )

        self.assertEqual(
            result["total_score"],
            14.0,
        )
        self.assertEqual(
            result["final_total_score"],
            14.0,
        )
        self.assertFalse(
            result["official_pass_met"],
        )

    def test_numeric_flags_propagate_cap_enforcement_failure(
        self,
    ) -> None:
        with patch(
            "explicit_requirement_cap."
            "enforce_existing_explicit_requirement_cap",
            side_effect=RuntimeError(
                "simulated cap enforcement failure"
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "simulated cap enforcement failure",
            ):
                _apply_numeric_flags(
                    {
                        "total_score": 18.0,
                        "max_score": 25.0,
                    }
                )




class QuestionTypeCleanupBootstrapRegressionTest(
    unittest.TestCase
):
    def test_qtype_cleanup_wrapper_is_installed(self) -> None:
        self.assertIs(
            qtype_coverage_adapter
            ._QTYPE_CLEAN_GENERAL_V2_INSTALLED,
            True,
        )
        self.assertTrue(
            callable(
                qtype_coverage_adapter
                ._cleanup_legacy_general_text_v2
            )
        )

    def test_qtype_cleanup_removes_legacy_general_sentence(
        self,
    ) -> None:
        grade = {
            "summary": (
                "문제 유형은 GENERAL(일반 설명형)로 "
                "판단했습니다. 핵심 원리를 설명했습니다."
            ),
        }

        result = (
            qtype_coverage_adapter
            ._cleanup_legacy_general_text_v2(grade)
        )

        self.assertEqual(
            result["summary"],
            "핵심 원리를 설명했습니다.",
        )

    def test_qtype_cleanup_replaces_general_c_feedback(
        self,
    ) -> None:
        grade = {
            "question_type": "PRINCIPLE_INTERPRETATION",
            "question_type_v2": {
                "name_ko": "원리·해석형",
                "c_fact_focus": [
                    "원리",
                    "인과관계",
                ],
            },
            "improvement_points": [
                (
                    "C항목 보완: 일반 설명형 유형에서는 "
                    "정의와 특징을 보완하세요."
                ),
            ],
        }

        result = (
            qtype_coverage_adapter
            ._cleanup_legacy_general_text_v2(grade)
        )

        feedback = result["improvement_points"][0]

        self.assertIn(
            "원리·해석형",
            feedback,
        )
        self.assertIn(
            "원리, 인과관계",
            feedback,
        )
        self.assertNotIn(
            "일반 설명형 유형에서는",
            feedback,
        )

    def test_qtype_cleanup_handles_malformed_qv2(
        self,
    ) -> None:
        grade = {
            "question_type": "GENERAL",
            "question_type_v2": "invalid",
            "summary": (
                "문제 유형은 GENERAL(일반 설명형)로 "
                "판단했습니다."
            ),
        }

        result = (
            qtype_coverage_adapter
            ._cleanup_legacy_general_text_v2(grade)
        )

        self.assertEqual(
            result["summary"],
            "",
        )
        self.assertEqual(
            result["question_type_v2"],
            "invalid",
        )




class QuestionTypeRootPromotionBootstrapRegressionTest(
    unittest.TestCase
):
    def test_qtype_root_promotion_wrapper_chain_is_installed(
        self,
    ) -> None:
        required_callables = (
            "_promote_question_type_coverage_to_root_v1",
            "_ORIGINAL_ATTACH_QTYPE_COVERAGE_FEEDBACK_PROMOTE_ROOT_V1",
            "_ORIGINAL_ENSURE_GRADE_QTYPE_COVERAGE_PROMOTE_ROOT_V1",
            "attach_question_type_coverage_feedback",
            "ensure_grade_question_type_coverage",
        )

        for name in required_callables:
            with self.subTest(name=name):
                self.assertTrue(
                    callable(
                        getattr(
                            qtype_coverage_adapter,
                            name,
                            None,
                        )
                    )
                )

    def test_qtype_root_promotion_matches_locked_contract(
        self,
    ) -> None:
        grade = {'question_type': 'EXISTING_ROOT_TYPE',
 'question_type_coverage': {'c_fact_focus': ['fact-a'],
                            'coverage_ratio': 0.73,
                            'coverage_score': 5.8,
                            'covered_requirements': ['covered-a', 'covered-b'],
                            'layer_points': {'A': 3, 'B': 6, 'C': 8},
                            'max_coverage_score': 8.0,
                            'missing_requirements': ['missing-a'],
                            'name_ko': '중첩 이름',
                            'primary_type': 'NESTED_PRIMARY',
                            'question_type': 'NESTED_TYPE',
                            'question_type_lens': 'NESTED_LENS',
                            'reason': 'sentinel reason',
                            'strategy_warnings': ['warning-a'],
                            'strengths': ['strength-a'],
                            'type_name': '중첩 유형',
                            'weaknesses': ['weakness-a']}}
        expected_promoted = {'question_type': 'PRINCIPLE_INTERPRETATION',
 'question_type_v2': {'c_fact_focus': ['대상 시스템·계기·회로·제어 loop의 구성요소',
                                       '동작 원리와 물리적 의미',
                                       '수식·모델·변수·단위',
                                       '계산 또는 해석 과정',
                                       '결과값 또는 응답특성의 의미'],
                      'd_field_judgement_focus': ['선정 또는 설계 판단',
                                                  'tuning, 안정성, 제어성, 오차 영향',
                                                  '현장 적용 한계',
                                                  '유지보수와 운전 조건',
                                                  '비용·성능 trade-off'],
                      'name_ko': '중첩 이름',
                      'note': 'question_type_v2는 B항목 요구사항 완전성과 C항목 Fact 전개, '
                              'D항목 현장 판단을 보완하는 평가 lens입니다.',
                      'question_type': 'PRINCIPLE_INTERPRETATION',
                      'sub_criteria': ['background_need',
                                       'structure_components',
                                       'principle_mechanism',
                                       'formula_model_variables',
                                       'calculation_or_interpretation',
                                       'result_meaning',
                                       'field_judgement']}}

        helper_result = (
            qtype_coverage_adapter
            ._promote_question_type_coverage_to_root_v1(
                deepcopy(grade)
            )
        )

        attach_result = (
            qtype_coverage_adapter
            .attach_question_type_coverage_feedback(
                deepcopy(grade)
            )
        )

        ensure_result = (
            qtype_coverage_adapter
            .ensure_grade_question_type_coverage(
                deepcopy(grade)
            )
        )

        self.assertTrue(expected_promoted)

        for key, value in expected_promoted.items():
            with self.subTest(
                function="helper",
                key=key,
            ):
                self.assertEqual(
                    helper_result.get(key),
                    value,
                )

            with self.subTest(
                function="attach",
                key=key,
            ):
                self.assertEqual(
                    attach_result.get(key),
                    value,
                )

            with self.subTest(
                function="ensure",
                key=key,
            ):
                self.assertEqual(
                    ensure_result.get(key),
                    value,
                )

    def test_qtype_root_promotion_handles_malformed_coverage(
        self,
    ) -> None:
        grade = {'question_type': 'GENERAL', 'question_type_coverage': 'invalid'}

        result = (
            qtype_coverage_adapter
            ._promote_question_type_coverage_to_root_v1(
                deepcopy(grade)
            )
        )

        self.assertEqual(
            result,
            grade,
        )




class QuestionTypeFallbackRecoveryRegressionTest(
    unittest.TestCase
):
    def test_qtype_fallback_generator_exception_preserves_grade(
        self,
    ) -> None:
        grade = {
            "question_type": "COMPARE",
            "total_score": 16.5,
            "summary": "keep this result",
        }

        with patch(
            "semantic_question_type_prompt."
            "empty_question_type_coverage",
            side_effect=RuntimeError(
                "simulated fallback failure"
            ),
        ):
            result = (
                qtype_coverage_adapter
                .ensure_grade_question_type_coverage(
                    deepcopy(grade),
                    question_text="두 방식을 비교하시오.",
                )
            )

        self.assertEqual(
            result["total_score"],
            16.5,
        )
        self.assertEqual(
            result["summary"],
            "keep this result",
        )
        self.assertNotIn(
            "question_type_coverage",
            result,
        )
        self.assertIn(
            "simulated fallback failure",
            result.get(
                "question_type_coverage_error",
                "",
            ),
        )

    def test_qtype_fallback_malformed_return_records_error(
        self,
    ) -> None:
        grade = {
            "question_type": "PROCEDURE",
            "total_score": 15.5,
        }

        with patch(
            "semantic_question_type_prompt."
            "empty_question_type_coverage",
            return_value=[],
        ):
            result = (
                qtype_coverage_adapter
                .ensure_grade_question_type_coverage(
                    deepcopy(grade),
                    question_text="절차를 설명하시오.",
                )
            )

        self.assertEqual(
            result["total_score"],
            15.5,
        )
        self.assertNotIn(
            "question_type_coverage",
            result,
        )
        self.assertIn(
            "fallback coverage generation failed",
            result.get(
                "question_type_coverage_error",
                "",
            ),
        )




class ModelAnswerReferenceResultContractRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _invoke_phase10_reference(
        reference_result,
        *,
        fail_log=False,
    ):
        import os
        from contextlib import ExitStack

        import grading_agents as grading_agents_module
        import model_answer_router as model_answer_router_module

        function = (
            grading_agents_module
            ._phase10_run_model_answer_reference
        )

        log_messages = []

        def fake_log(
            message,
            *args,
            **kwargs,
        ):
            log_messages.append(str(message))

            if fail_log:
                raise RuntimeError(
                    "simulated phase10 logging failure"
                )

        with ExitStack() as stack:
            stack.enter_context(
                patch.dict(
                    os.environ,
                    {
                        "RUBRIC_BANK_MODE": "legacy",
                    },
                )
            )

            stack.enter_context(
                patch.dict(
                    function.__globals__,
                    {
                        "_phase3_extract_question_text": (
                            lambda input_text: (
                                "모델 답안 참조 계약 시험"
                            )
                        ),
                        "_phase2_log": fake_log,
                    },
                    clear=False,
                )
            )

            stack.enter_context(
                patch.object(
                    model_answer_router_module,
                    "load_model_answer_bank",
                    return_value={
                        "answers": [],
                    },
                )
            )

            stack.enter_context(
                patch.object(
                    model_answer_router_module,
                    "find_model_answer_reference",
                    return_value=reference_result,
                )
            )

            result = function(
                input_text=(
                    "문제: 모델 답안 참조 계약 시험"
                ),
                answer_text="시험 답안",
                question_type_eval={
                    "primary_type": {
                        "question_type": "PRINCIPLE",
                    },
                },
                fact_eval={
                    "topic_id": "contract_test_topic",
                },
                subject_rubric=None,
                session_dir=None,
            )

        return result, log_messages

    def test_phase10_logging_failure_preserves_valid_reference(
        self,
    ) -> None:
        reference_result = {
            "version": "model_answer_reference_v1",
            "matched": True,
            "primary_reference": {
                "id": "reference-1",
                "topic_id": "topic-1",
                "question_type": "PRINCIPLE",
            },
            "candidates": [],
        }

        result, log_messages = (
            self._invoke_phase10_reference(
                reference_result,
                fail_log=True,
            )
        )

        self.assertEqual(
            result,
            reference_result,
        )
        self.assertTrue(
            log_messages,
        )

    def test_phase10_malformed_reference_uses_outer_fallback(
        self,
    ) -> None:
        malformed_results = (
            [],
            None,
            "malformed-reference",
        )

        for malformed_result in malformed_results:
            with self.subTest(
                malformed_result=repr(
                    malformed_result
                ),
            ):
                result, _ = (
                    self._invoke_phase10_reference(
                        malformed_result,
                    )
                )

                self.assertIsInstance(
                    result,
                    dict,
                )
                self.assertEqual(
                    result.get("version"),
                    "model_answer_reference_v1_fallback",
                )
                self.assertFalse(
                    result.get("matched"),
                )
                self.assertIsNone(
                    result.get(
                        "primary_reference"
                    )
                )
                self.assertEqual(
                    result.get("candidates"),
                    [],
                )
                self.assertIn(
                    "TypeError",
                    result.get("error", ""),
                )
                self.assertIn(
                    (
                        "find_model_answer_reference "
                        "must return dict"
                    ),
                    result.get("error", ""),
                )




class TopicImportanceFallbackRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _topic_without_profile_defaults():
        return {
            "topic_id": "contract_topic",
            "label": "계약 시험 주제",
            "difficulty": "THEORY_CORE",
            "difficulty_label": "핵심 이론",
            "selection_importance": "CORE_MUST_PREPARE",
            "requires_band_unlock": True,
            "high_band_unlock_conditions": [
                "핵심 이론 정확성",
            ],
            "note": "contract topic",
        }

    def test_topic_importance_profile_failure_preserves_topic_match(
        self,
    ) -> None:
        import difficulty_output_adapter as adapter
        import rubric_registry

        function = (
            adapter
            ._topic_importance_strategy_from_topic_id
        )

        def fail_profile_policy(
            difficulty,
        ):
            raise RuntimeError(
                "simulated profile policy failure"
            )

        with patch.object(
            rubric_registry,
            "load_topic_importance_bank",
            return_value={
                "topics": [
                    self._topic_without_profile_defaults(),
                ],
            },
        ), patch.dict(
            function.__globals__,
            {
                "get_profile_policy": (
                    fail_profile_policy
                ),
            },
            clear=False,
        ):
            result = function(
                "contract_topic",
                "시험 문제",
            )

        self.assertIsInstance(
            result,
            dict,
        )
        self.assertTrue(
            result.get("matched"),
        )
        self.assertEqual(
            result.get("topic_id"),
            "contract_topic",
        )
        self.assertEqual(
            result.get("difficulty"),
            "THEORY_CORE",
        )
        self.assertEqual(
            result.get("excellent_score_band"),
            [21, 25],
        )
        self.assertIsNone(
            result.get("selection_policy"),
        )
        self.assertIsNone(
            result.get("default_score_ceiling"),
        )

    def test_topic_importance_bank_failure_returns_unmatched_diagnostic(
        self,
    ) -> None:
        import difficulty_output_adapter as adapter
        import rubric_registry

        function = (
            adapter
            ._topic_importance_strategy_from_topic_id
        )

        with patch.object(
            rubric_registry,
            "load_topic_importance_bank",
            side_effect=RuntimeError(
                "simulated topic bank failure"
            ),
        ):
            result = function(
                "contract_topic",
                "시험 문제",
            )

        self.assertIsInstance(
            result,
            dict,
        )
        self.assertFalse(
            result.get("matched"),
        )
        self.assertEqual(
            result.get("topic_id"),
            "contract_topic",
        )
        self.assertEqual(
            result.get("question"),
            "시험 문제",
        )
        self.assertIn(
            "simulated topic bank failure",
            result.get("error", ""),
        )




class LogicLlmVerifierFallbackRegressionTest(
    unittest.TestCase
):
    def test_logic_llm_failure_returns_safe_warn_fallback(
        self,
    ) -> None:
        import logic_llm_verifier as verifier

        function = verifier.verify_logic_with_llm
        prompts = []

        def fail_ollama_call(
            prompt,
        ):
            prompts.append(prompt)
            raise RuntimeError(
                "simulated Ollama verifier failure"
            )

        with patch.dict(
            function.__globals__,
            {
                "_call_ollama_json": fail_ollama_call,
            },
            clear=False,
        ):
            result = function(
                answer_text='시스템은 우반평면에 극점이 있어도 안정하다. 감쇠비가 음수이면 진동이 감소한다.',
                topic_id='second_order_lag_response_by_damping_ratio',
            )

        self.assertEqual(
            len(prompts),
            1,
        )
        self.assertIsInstance(
            result,
            dict,
        )
        self.assertTrue(
            result.get("applicable"),
        )
        self.assertEqual(
            result.get("engine"),
            "llm_verifier_profile_v1",
        )
        self.assertEqual(
            result.get("topic_id"),
            'second_order_lag_response_by_damping_ratio',
        )
        self.assertEqual(
            result.get("verdict"),
            "warn",
        )
        self.assertEqual(
            result.get("confidence"),
            0.0,
        )
        self.assertFalse(
            result.get("fatal_error_detected"),
        )
        self.assertIsNone(
            result.get("recommended_ceiling"),
        )
        self.assertEqual(
            result.get("mode"),
            "warn",
        )
        self.assertEqual(
            result.get("reason"),
            "LLM verifier unavailable",
        )

        findings = result.get("findings")

        self.assertIsInstance(
            findings,
            list,
        )
        self.assertTrue(
            findings,
        )
        self.assertEqual(
            findings[0].get("id"),
            "llm_verifier_unavailable",
        )
        self.assertEqual(
            findings[0].get("severity"),
            "minor",
        )
        self.assertIn(
            "simulated Ollama verifier failure",
            findings[0].get("message", ""),
        )
        self.assertIn(
            "fatal cap을 적용하지 않습니다",
            findings[0].get("correct_rule", ""),
        )




class GeminiMandatoryPromptBootstrapRegressionTest(
    unittest.TestCase
):
    def test_gemini_mandatory_prompt_wrappers_are_installed(
        self,
    ) -> None:
        import gemini_grader

        self.assertTrue(
            callable(
                getattr(
                    gemini_grader,
                    (
                        "_ORIGINAL_BUILD_GEMINI_GRADING_"
                        "PROMPT_QTYPE_V4_EOF"
                    ),
                    None,
                )
            )
        )
        self.assertTrue(
            callable(
                getattr(
                    gemini_grader,
                    (
                        "_ORIGINAL_BUILD_GEMINI_PROMPT_"
                        "EXPLICIT_REQ_V1"
                    ),
                    None,
                )
            )
        )

        prompt = (
            gemini_grader
            .build_gemini_grading_prompt(
                question_text=(
                    "공압식, 전동식, 유압식 제어밸브 "
                    "액추에이터를 비교하고 선정 기준을 "
                    "설명하시오."
                ),
                answer_text=(
                    "공압식은 압축공기를 사용하고 "
                    "전동식은 전원을 사용하며 "
                    "유압식은 큰 추력에 적합하다. "
                    "추력, 응답속도, 방폭, 유지보수성을 "
                    "기준으로 선정한다."
                ),
                scoring_model={
                    "total_score": 25,
                    "criteria": {},
                },
                subject_rubric={
                    "subject": "산업계측제어기술사",
                },
                rater_profile={
                    "name": "contract-test",
                },
                volume={
                    "target_pages": 3,
                    "target_lines_per_page": 12,
                },
                fact_eval={
                    "matched": True,
                    "topic_id": (
                        "control_valve_actuator"
                    ),
                },
                connection_eval={
                    "matched": True,
                    "score": 1.0,
                },
            )
        )

        self.assertIsInstance(prompt, str)
        self.assertIn(
            "question_type_coverage",
            prompt,
        )
        self.assertIn(
            "explicit_requirement_coverage",
            prompt,
        )
        self.assertGreaterEqual(
            prompt.count(
                "QTYPE_HARD_JSON_TEMPLATE_V4"
            ),
            2,
        )
        self.assertIn(
            (
                "FINAL MANDATORY EXPLICIT "
                "REQUIREMENT CONTRACT"
            ),
            prompt,
        )

        qtype_position = prompt.rfind(
            "QTYPE_HARD_JSON_TEMPLATE_V4"
        )
        explicit_position = prompt.rfind(
            (
                "FINAL MANDATORY EXPLICIT "
                "REQUIREMENT CONTRACT"
            )
        )

        self.assertGreater(
            explicit_position,
            qtype_position,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
