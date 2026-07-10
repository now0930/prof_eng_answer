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

    def test_coverage_adjusted_score_is_applied(
        self,
    ) -> None:
        grade = {
            "total_score": 18.06,
            "max_score": 25.0,
            "official_pass_score": 15.0,
            "practical_target_score": 17.5,
            "high_score_target": 20.0,
        }

        decision = {
            "mode": "strict",
            "original_score": 18.06,
            "adjusted_score": 17.79,
            "applied": False,
            "recommended_penalty": 0.27,
        }

        with patch.object(
            coverage_adjuster,
            (
                "evaluate_question_type_coverage_"
                "score_adjustment"
            ),
            return_value=decision,
        ):
            result = (
                coverage_adjuster
                .apply_question_type_coverage_score_adjustment(
                    grade
                )
            )

        self.assertEqual(
            result["total_score"],
            17.79,
        )

        adjustment = result[
            "question_type_coverage_score_adjustment"
        ]

        self.assertTrue(
            adjustment["applied"]
        )
        self.assertTrue(
            adjustment[
                "score_flow_applied"
            ]
        )
        self.assertEqual(
            result[
                "pre_question_type_coverage_total_score"
            ],
            18.06,
        )

    def test_ceiling_prefers_lower_coverage_score(
        self,
    ) -> None:
        score, applied = (
            _prefer_question_type_adjusted_score(
                {
                    (
                        "question_type_coverage_"
                        "score_adjustment"
                    ): {
                        "mode": "strict",
                        "applied": True,
                        "score_flow_applied": True,
                        "adjusted_score": 17.79,
                    }
                },
                18.06,
            )
        )

        self.assertEqual(
            score,
            17.79,
        )
        self.assertTrue(
            applied
        )

    def test_ceiling_does_not_raise_score(
        self,
    ) -> None:
        score, applied = (
            _prefer_question_type_adjusted_score(
                {
                    (
                        "question_type_coverage_"
                        "score_adjustment"
                    ): {
                        "mode": "strict",
                        "applied": True,
                        "score_flow_applied": True,
                        "adjusted_score": 18.5,
                    }
                },
                18.06,
            )
        )

        self.assertEqual(
            score,
            18.06,
        )
        self.assertFalse(
            applied
        )




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
        import os
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

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

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.dict(
                    os.environ,
                    {"RUBRIC_BANK_MODE": "legacy"},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="원리를 설명하시오.",
                ),
                patch(
                    "model_answer_router."
                    "load_model_answer_bank",
                    return_value={"model_answers": []},
                ),
                patch(
                    "model_answer_router."
                    "find_model_answer_reference",
                    return_value=reference_result,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                ) as write_mock,
                patch(
                    "builtins.print",
                    side_effect=RuntimeError(
                        "simulated print failure"
                    ),
                ),
            ):
                result = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        "문제: 원리를 설명하시오.",
                        "원리에 대한 답안",
                        {},
                        {},
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result,
            reference_result,
        )
        write_mock.assert_called_once_with(
            session_dir / "model_answer_reference.json",
            reference_result,
        )

    def test_phase10_success_persists_reference(
        self,
    ) -> None:
        import os
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        reference_result = {
            "version": "model_answer_reference_v1",
            "matched": True,
            "primary_reference": {
                "id": "reference-2",
                "topic_id": "topic-2",
                "question_type": "COMPARE",
            },
            "candidates": [],
        }
        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.dict(
                    os.environ,
                    {"RUBRIC_BANK_MODE": "legacy"},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="두 방식을 비교하시오.",
                ),
                patch(
                    "model_answer_router."
                    "load_model_answer_bank",
                    return_value={"model_answers": []},
                ),
                patch(
                    "model_answer_router."
                    "find_model_answer_reference",
                    return_value=reference_result,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                ) as write_mock,
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        "문제: 두 방식을 비교하시오.",
                        "비교 답안",
                        {},
                        {},
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result,
            reference_result,
        )
        write_mock.assert_called_once_with(
            session_dir / "model_answer_reference.json",
            reference_result,
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "selected"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "reference-2",
            output.getvalue(),
        )

    def test_phase10_router_failure_persists_fallback(
        self,
    ) -> None:
        import os
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.dict(
                    os.environ,
                    {"RUBRIC_BANK_MODE": "legacy"},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="구성을 설명하시오.",
                ),
                patch(
                    "model_answer_router."
                    "load_model_answer_bank",
                    return_value={"model_answers": []},
                ),
                patch(
                    "model_answer_router."
                    "find_model_answer_reference",
                    side_effect=RuntimeError(
                        "simulated phase10 router failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                ) as write_mock,
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        "문제: 구성을 설명하시오.",
                        "구성에 대한 답안",
                        {},
                        {},
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result["version"],
            "model_answer_reference_v1_fallback",
        )
        self.assertFalse(result["matched"])
        self.assertIn(
            "simulated phase10 router failure",
            result["error"],
        )
        write_mock.assert_called_once_with(
            session_dir / "model_answer_reference.json",
            result,
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "failed"
            ),
            output.getvalue(),
        )

    def test_phase10_persistence_failure_is_reported_and_preserves_result(
        self,
    ) -> None:
        import os
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        reference_result = {
            "version": "model_answer_reference_v1",
            "matched": False,
            "primary_reference": None,
            "candidates": [],
        }
        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.dict(
                    os.environ,
                    {"RUBRIC_BANK_MODE": "legacy"},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="절차를 설명하시오.",
                ),
                patch(
                    "model_answer_router."
                    "load_model_answer_bank",
                    return_value={"model_answers": []},
                ),
                patch(
                    "model_answer_router."
                    "find_model_answer_reference",
                    return_value=reference_result,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=OSError(
                        "simulated phase10 persistence failure"
                    ),
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        "문제: 절차를 설명하시오.",
                        "절차에 대한 답안",
                        {},
                        {},
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result,
            reference_result,
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "persistence failed"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "simulated phase10 persistence failure",
            output.getvalue(),
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "not matched"
            ),
            output.getvalue(),
        )

    def test_phase10_fallback_persistence_failure_preserves_result(
        self,
    ) -> None:
        import os
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.dict(
                    os.environ,
                    {"RUBRIC_BANK_MODE": "legacy"},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="원리를 설명하시오.",
                ),
                patch(
                    "model_answer_router."
                    "load_model_answer_bank",
                    return_value={"model_answers": []},
                ),
                patch(
                    "model_answer_router."
                    "find_model_answer_reference",
                    side_effect=RuntimeError(
                        "simulated phase10 fallback trigger"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=OSError(
                        "simulated fallback persistence failure"
                    ),
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase10_run_model_answer_reference(
                        "문제: 원리를 설명하시오.",
                        "원리에 대한 답안",
                        {},
                        {},
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result["version"],
            "model_answer_reference_v1_fallback",
        )
        self.assertFalse(result["matched"])
        self.assertIn(
            "simulated phase10 fallback trigger",
            result["error"],
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "persistence failed"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "simulated fallback persistence failure",
            output.getvalue(),
        )
        self.assertIn(
            (
                "phase10 model answer reference "
                "failed"
            ),
            output.getvalue(),
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


    def test_phase9_success_persists_evaluation(self) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        evaluation = {
            "version": "question_type_lens_v1",
            "confidence": "high",
            "primary_type": {
                "id": "COMPARE",
                "name": "비교·선정형",
            },
            "candidates": [],
        }

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="두 방식을 비교하시오.",
                ),
                patch(
                    "question_type_router."
                    "load_question_type_profile",
                    return_value={"types": []},
                ),
                patch(
                    "question_type_router.detect_question_type",
                    return_value=evaluation,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                ) as write_mock,
            ):
                result = (
                    grading_agents
                    ._phase9_run_question_type_lens(
                        "문제: 두 방식을 비교하시오.",
                        "두 방식의 특징과 선정 기준",
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(result, evaluation)
        write_mock.assert_called_once_with(
            session_dir / "question_type_evaluation.json",
            evaluation,
        )

    def test_phase9_router_failure_persists_fallback(
        self,
    ) -> None:
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="원리를 설명하시오.",
                ),
                patch(
                    "question_type_router."
                    "load_question_type_profile",
                    return_value={"types": []},
                ),
                patch(
                    "question_type_router.detect_question_type",
                    side_effect=RuntimeError(
                        "simulated phase9 router failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                ) as write_mock,
            ):
                result = (
                    grading_agents
                    ._phase9_run_question_type_lens(
                        "문제: 원리를 설명하시오.",
                        "원리에 대한 답안",
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result["version"],
            "question_type_lens_v1_fallback",
        )
        self.assertEqual(
            result["primary_type"]["id"],
            "GENERAL",
        )
        self.assertIn(
            "simulated phase9 router failure",
            result["error"],
        )
        write_mock.assert_called_once_with(
            session_dir / "question_type_evaluation.json",
            result,
        )

    def test_phase9_persistence_failure_is_reported_and_preserves_result(
        self,
    ) -> None:
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        evaluation = {
            "version": "question_type_lens_v1",
            "confidence": "medium",
            "primary_type": {
                "id": "PROCEDURE",
                "name": "절차·방법론형",
            },
            "candidates": [],
        }
        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="절차를 설명하시오.",
                ),
                patch(
                    "question_type_router."
                    "load_question_type_profile",
                    return_value={"types": []},
                ),
                patch(
                    "question_type_router.detect_question_type",
                    return_value=evaluation,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=OSError(
                        "simulated phase9 persistence failure"
                    ),
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase9_run_question_type_lens(
                        "문제: 절차를 설명하시오.",
                        "절차에 대한 답안",
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(result, evaluation)
        self.assertIn(
            (
                "phase9 question type lens "
                "persistence failed"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "simulated phase9 persistence failure",
            output.getvalue(),
        )
        self.assertIn(
            "phase9 question type lens selected",
            output.getvalue(),
        )

    def test_phase9_fallback_persistence_failure_preserves_result(
        self,
    ) -> None:
        from contextlib import redirect_stdout
        from io import StringIO
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from unittest.mock import patch

        import grading_agents

        output = StringIO()

        with TemporaryDirectory() as temporary_directory:
            session_dir = Path(temporary_directory)

            with (
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    return_value="구성을 설명하시오.",
                ),
                patch(
                    "question_type_router."
                    "load_question_type_profile",
                    return_value={"types": []},
                ),
                patch(
                    "question_type_router.detect_question_type",
                    side_effect=RuntimeError(
                        "simulated phase9 fallback trigger"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=OSError(
                        "simulated fallback persistence failure"
                    ),
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase9_run_question_type_lens(
                        "문제: 구성을 설명하시오.",
                        "구성에 대한 답안",
                        session_dir=session_dir,
                    )
                )

        self.assertEqual(
            result["version"],
            "question_type_lens_v1_fallback",
        )
        self.assertEqual(
            result["primary_type"]["id"],
            "GENERAL",
        )
        self.assertIn(
            "simulated phase9 fallback trigger",
            result["error"],
        )
        self.assertIn(
            (
                "phase9 question type lens "
                "persistence failed"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "simulated fallback persistence failure",
            output.getvalue(),
        )
        self.assertIn(
            "phase9 question type lens failed",
            output.getvalue(),
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




class DifficultyCeilingFallbackRegressionTest(
    unittest.TestCase
):
    def test_phase2_preserves_grade_when_difficulty_ceiling_fails(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import difficulty_score_ceiling
        import grading_agents
        from grading_config import (
            load_active_config,
            save_active_config_snapshots,
        )

        legacy_result = {
            "score": 22.0,
            "total_score": 22.0,
            "final_score": 22.0,
            "raw_score": 22.0,
            "score_25": 22.0,
            "criteria": {
                "A": {
                    "score": 5.0,
                    "max_score": 5.0,
                },
                "B": {
                    "score": 5.0,
                    "max_score": 5.0,
                },
                "C": {
                    "score": 5.0,
                    "max_score": 5.0,
                },
                "D": {
                    "score": 4.0,
                    "max_score": 5.0,
                },
                "E": {
                    "score": 3.0,
                    "max_score": 5.0,
                },
            },
            "scores": {
                "A": 5.0,
                "B": 5.0,
                "C": 5.0,
                "D": 4.0,
                "E": 3.0,
            },
            "feedback": [],
            "findings": [],
            "caps": [],
            "metadata": {},
        }

        input_text = """문제:
피드백 제어계의 안정성을 설명하시오.

답안:
폐루프 극점이 좌반평면에 있으면 시스템은 안정하며,
우반평면에 있으면 불안정하다.
"""

        json_write_calls = []
        ceiling_calls = []

        def capture_json_write(
            path_value,
            data,
        ) -> None:
            json_write_calls.append(
                {
                    "path": str(path_value),
                    "data": deepcopy(data),
                }
            )

        def fail_ceiling(
            grade,
            *,
            question_text=None,
            answer_text=None,
        ):
            ceiling_calls.append(
                {
                    "grade": deepcopy(grade),
                    "question_text": question_text,
                    "answer_text": answer_text,
                }
            )

            raise RuntimeError(
                "simulated difficulty ceiling failure"
            )

        with TemporaryDirectory() as directory:
            session_dir = Path(directory)

            config = load_active_config(
                grading_agents.BASE_DIR
            )

            save_active_config_snapshots(
                session_dir,
                config,
            )

            (session_dir / "input.txt").write_text(
                input_text,
                encoding="utf-8",
            )

            for snapshot_name in (
                "scoring_model_snapshot.json",
                "subject_rubric_snapshot.json",
                "layered_rater_snapshot.json",
            ):
                self.assertTrue(
                    (
                        session_dir
                        / snapshot_name
                    ).is_file()
                )

            stdout_buffer = io.StringIO()

            with (
                patch.object(
                    grading_agents,
                    "_phase2_latest_session_dir",
                    return_value=session_dir,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_json_write,
                ),
                patch.object(
                    grading_agents,
                    "_phase6_run_gemini_semantic_grader",
                    return_value={},
                ),
                patch.object(
                    difficulty_score_ceiling,
                    "apply_difficulty_score_ceiling",
                    side_effect=fail_ceiling,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase2_postprocess_grade(
                        deepcopy(legacy_result)
                    )
                )

        self.assertEqual(
            len(ceiling_calls),
            1,
        )
        self.assertIsInstance(
            result,
            dict,
        )
        self.assertEqual(
            result,
            ceiling_calls[0]["grade"],
        )
        self.assertGreater(
            len(json_write_calls),
            0,
        )
        self.assertEqual(
            ceiling_calls[0]["question_text"],
            "피드백 제어계의 안정성을 설명하시오.",
        )
        self.assertIn(
            "폐루프 극점이 좌반평면에 있으면",
            ceiling_calls[0]["answer_text"],
        )
        self.assertIn(
            "simulated difficulty ceiling failure",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "phase21 final difficulty ceiling skipped",
            stdout_buffer.getvalue(),
        )




class GeminiSemanticPersistenceRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _call_arguments(
        session_dir,
    ):
        return {
            "input_text": (
                "문제:\n"
                "PID 제어기의 동작 원리를 설명하시오.\n\n"
                "답안:\n"
                "비례, 적분, 미분 동작으로 제어한다."
            ),
            "answer_text": (
                "비례, 적분, 미분 동작으로 제어한다."
            ),
            "scoring_model": {
                "total_points": 25,
                "layers": [],
            },
            "subject_rubric": {
                "name": "contract-test",
            },
            "rater_profile": {
                "raters": [],
            },
            "volume": {
                "level": "text_only_short_answer",
            },
            "fact_eval": {},
            "connection_eval": {},
            "session_dir": session_dir,
        }

    @staticmethod
    def _valid_result():
        return {
            "ok": True,
            "error": None,
            "parsed": {
                "scores": {
                    "A": 1.0,
                },
            },
            "raw_text": '{"ok": true}',
        }

    def test_gemini_success_persists_only_semantic_result(
        self,
    ) -> None:
        from tempfile import TemporaryDirectory

        import gemini_grader
        import grading_agents

        valid_result = self._valid_result()
        writes = []

        def capture_write(
            path_value,
            data,
        ) -> None:
            writes.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    gemini_grader,
                    "gemini_semantic_grade",
                    return_value=deepcopy(valid_result),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_write,
                ),
            ):
                result = (
                    grading_agents
                    ._phase6_run_gemini_semantic_grader(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertEqual(
            result,
            valid_result,
        )
        self.assertEqual(
            [item["filename"] for item in writes],
            ["gemini_semantic_evaluation.json"],
        )
        self.assertEqual(
            writes[0]["data"],
            valid_result,
        )

    def test_gemini_exception_persists_fallback_result(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import gemini_grader
        import grading_agents

        writes = []

        def capture_write(
            path_value,
            data,
        ) -> None:
            writes.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

        stdout_buffer = io.StringIO()

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    gemini_grader,
                    "gemini_semantic_grade",
                    side_effect=RuntimeError(
                        "simulated Gemini dependency failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase6_run_gemini_semantic_grader(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertFalse(
            result["ok"],
        )
        self.assertIn(
            "simulated Gemini dependency failure",
            result["error"],
        )
        self.assertEqual(
            [item["filename"] for item in writes],
            ["gemini_semantic_evaluation.json"],
        )
        self.assertEqual(
            writes[0]["data"],
            result,
        )
        self.assertIn(
            "Gemini semantic grader exception",
            stdout_buffer.getvalue(),
        )

    def test_gemini_persistence_failure_is_reported_and_preserves_result(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import gemini_grader
        import grading_agents

        valid_result = self._valid_result()
        write_attempts = []
        stdout_buffer = io.StringIO()

        def fail_write(
            path_value,
            data,
        ) -> None:
            write_attempts.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

            raise PermissionError(
                "simulated Gemini persistence write failure"
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    gemini_grader,
                    "gemini_semantic_grade",
                    return_value=deepcopy(valid_result),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=fail_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase6_run_gemini_semantic_grader(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertEqual(
            result,
            valid_result,
        )
        self.assertEqual(
            [item["filename"] for item in write_attempts],
            ["gemini_semantic_evaluation.json"],
        )
        self.assertEqual(
            write_attempts[0]["data"],
            valid_result,
        )
        self.assertIn(
            "Gemini semantic grader persistence failed",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "simulated Gemini persistence write failure",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "Gemini semantic grader applied",
            stdout_buffer.getvalue(),
        )




class OriginalityPersistenceRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _call_arguments(
        session_dir,
    ):
        return {
            "input_text": (
                "문제:\n"
                "PID 제어기의 동작 원리를 설명하시오.\n\n"
                "답안:\n"
                "비례, 적분, 미분 동작으로 제어한다."
            ),
            "answer_text": (
                "비례, 적분, 미분 동작으로 제어한다."
            ),
            "layer_scores": {
                "A": 1.0,
                "B": 2.0,
                "C": 3.0,
                "D": 2.0,
                "E": 1.0,
            },
            "volume": {
                "level": "text_only_short_answer",
            },
            "fact_eval": {},
            "connection_eval": {},
            "session_dir": session_dir,
        }

    @staticmethod
    def _valid_grader_result():
        return {
            "ok": True,
            "error": "",
            "model": "contract-test-model",
            "raw_text": '{"ok": true}',
            "parsed": {
                "originality_level": "independent",
                "template_dependency": False,
                "evidence": [
                    "현장 적용 설명 포함",
                ],
            },
        }

    @staticmethod
    def _normalized_valid_result():
        return {
            "originality_level": "independent",
            "template_dependency": False,
            "evidence": [
                "현장 적용 설명 포함",
            ],
        }

    @staticmethod
    def _normalized_fallback_result():
        return {
            "originality_level": "fallback",
            "template_dependency": False,
            "evidence": [],
        }

    def test_originality_success_persists_evaluation(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import grading_agents
        import originality_grader

        writes = []
        stdout_buffer = io.StringIO()

        def capture_write(
            path_value,
            data,
        ) -> None:
            writes.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    originality_grader,
                    "gemini_originality_evaluate",
                    return_value=deepcopy(
                        self._valid_grader_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_normalize_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_valid_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase8_run_originality_evaluator(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertTrue(
            result["ok"],
        )
        self.assertEqual(
            result["parsed"],
            self._normalized_valid_result(),
        )
        self.assertEqual(
            [item["filename"] for item in writes],
            ["originality_evaluation.json"],
        )
        self.assertEqual(
            writes[0]["data"],
            result,
        )
        self.assertIn(
            "phase8 originality evaluator applied",
            stdout_buffer.getvalue(),
        )

    def test_originality_grader_failure_persists_fallback(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import grading_agents
        import originality_grader

        writes = []
        stdout_buffer = io.StringIO()

        def capture_write(
            path_value,
            data,
        ) -> None:
            writes.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    originality_grader,
                    "gemini_originality_evaluate",
                    side_effect=RuntimeError(
                        "simulated originality grader failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_fallback_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_fallback_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_normalize_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_fallback_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase8_run_originality_evaluator(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertFalse(
            result["ok"],
        )
        self.assertIn(
            "simulated originality grader failure",
            result["error"],
        )
        self.assertEqual(
            result["parsed"],
            self._normalized_fallback_result(),
        )
        self.assertEqual(
            [item["filename"] for item in writes],
            ["originality_evaluation.json"],
        )
        self.assertEqual(
            writes[0]["data"],
            result,
        )
        self.assertIn(
            "phase8 originality evaluator failed",
            stdout_buffer.getvalue(),
        )

    def test_originality_persistence_failure_is_reported_and_preserves_result(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import grading_agents
        import originality_grader

        write_attempts = []
        stdout_buffer = io.StringIO()

        def fail_write(
            path_value,
            data,
        ) -> None:
            write_attempts.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

            raise PermissionError(
                "simulated originality persistence failure"
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    originality_grader,
                    "gemini_originality_evaluate",
                    return_value=deepcopy(
                        self._valid_grader_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_normalize_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_valid_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=fail_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase8_run_originality_evaluator(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertTrue(
            result["ok"],
        )
        self.assertEqual(
            result["parsed"],
            self._normalized_valid_result(),
        )
        self.assertEqual(
            [item["filename"] for item in write_attempts],
            ["originality_evaluation.json"],
        )
        self.assertEqual(
            write_attempts[0]["data"],
            result,
        )
        self.assertIn(
            "phase8 originality evaluator persistence failed",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "simulated originality persistence failure",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "phase8 originality evaluator applied",
            stdout_buffer.getvalue(),
        )

    def test_originality_fallback_persistence_failure_preserves_result(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import grading_agents
        import originality_grader

        write_attempts = []
        stdout_buffer = io.StringIO()

        def fail_write(
            path_value,
            data,
        ) -> None:
            write_attempts.append(
                {
                    "filename": Path(path_value).name,
                    "data": deepcopy(data),
                }
            )

            raise PermissionError(
                "simulated fallback persistence failure"
            )

        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    originality_grader,
                    "gemini_originality_evaluate",
                    side_effect=RuntimeError(
                        "simulated originality grader failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_fallback_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_fallback_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase8_normalize_originality_evaluation",
                    return_value=deepcopy(
                        self._normalized_fallback_result()
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=fail_write,
                ),
                redirect_stdout(stdout_buffer),
            ):
                result = (
                    grading_agents
                    ._phase8_run_originality_evaluator(
                        **self._call_arguments(
                            Path(directory)
                        )
                    )
                )

        self.assertFalse(
            result["ok"],
        )
        self.assertEqual(
            result["parsed"],
            self._normalized_fallback_result(),
        )
        self.assertEqual(
            [item["filename"] for item in write_attempts],
            ["originality_evaluation.json"],
        )
        self.assertEqual(
            write_attempts[0]["data"],
            result,
        )
        self.assertIn(
            "phase8 originality evaluator persistence failed",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "simulated fallback persistence failure",
            stdout_buffer.getvalue(),
        )
        self.assertIn(
            "phase8 originality evaluator failed",
            stdout_buffer.getvalue(),
        )



class LlmJsonParserRegressionTest(unittest.TestCase):
    def test_llm_json_parser_parses_fenced_object(
        self,
    ) -> None:
        import grade_output_summarizer

        result = grade_output_summarizer._parse_llm_json(
            """```json
            {
                "summary": "정상 결과",
                "score": 17.5
            }
            ```"""
        )

        self.assertEqual(
            result,
            {
                "summary": "정상 결과",
                "score": 17.5,
            },
        )

    def test_llm_json_parser_falls_back_after_truncated_fence_match(
        self,
    ) -> None:
        import grade_output_summarizer

        result = grade_output_summarizer._parse_llm_json(
            """```json
            {
                "summary": "중첩 JSON",
                "details": {
                    "grade": "B",
                    "score": 16.0
                }
            }
            ```"""
        )

        self.assertEqual(
            result,
            {
                "summary": "중첩 JSON",
                "details": {
                    "grade": "B",
                    "score": 16.0,
                },
            },
        )

    def test_llm_json_parser_parses_embedded_object(
        self,
    ) -> None:
        import grade_output_summarizer

        result = grade_output_summarizer._parse_llm_json(
            (
                "다음은 요약 결과입니다.\n"
                '{"summary": "본문 객체", "passed": true}\n'
                "검토를 완료했습니다."
            )
        )

        self.assertEqual(
            result,
            {
                "summary": "본문 객체",
                "passed": True,
            },
        )

    def test_llm_json_parser_rejects_malformed_or_non_object_response(
        self,
    ) -> None:
        import grade_output_summarizer

        invalid_inputs = (
            "",
            "JSON 응답이 없습니다.",
            '{"summary": "닫히지 않은 객체"',
            "[1, 2, 3]",
            "```json\n[1, 2, 3]\n```",
        )

        for raw in invalid_inputs:
            with self.subTest(raw=raw):
                self.assertIsNone(
                    grade_output_summarizer._parse_llm_json(
                        raw
                    )
                )


class Phase2PostprocessDiagnosticsRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _prepare_session(
        session_dir,
        grading_agents,
        input_text,
    ) -> None:
        from grading_config import (
            load_active_config,
            save_active_config_snapshots,
        )

        config = load_active_config(
            grading_agents.BASE_DIR
        )

        save_active_config_snapshots(
            session_dir,
            config,
        )

        (session_dir / "input.txt").write_text(
            input_text,
            encoding="utf-8",
        )

    @staticmethod
    def _question_type_result() -> dict:
        return {
            "version": "question_type_lens_v1",
            "confidence": "high",
            "primary_type": {
                "id": "PRINCIPLE",
                "name": "원리·메커니즘형",
            },
            "candidates": [],
        }

    @staticmethod
    def _model_reference_result() -> dict:
        return {
            "version": "model_answer_reference_v1",
            "matched": False,
            "primary_reference": None,
            "candidates": [],
        }

    def test_phase2_logic_persistence_failure_is_reported_and_preserves_grade(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import difficulty_output_adapter
        import difficulty_score_ceiling
        import grading_agents
        import logic_check_evaluator

        input_text = """문제:
피드백 제어계의 안정성을 설명하시오.

답안:
폐루프 극점이 좌반평면에 있으면 안정하다.
"""

        write_names: list[str] = []

        def capture_json_write(
            path_value,
            data,
        ) -> None:
            file_name = Path(path_value).name
            write_names.append(file_name)

            if file_name == "logic_check_evaluation.json":
                raise OSError(
                    "simulated logic persistence failure"
                )

        def attach_logic(
            grade,
            _input_text,
        ):
            result = deepcopy(grade)
            result["logic_check_evaluation"] = {
                "topic_id": "feedback_stability",
                "mode": "rule",
                "fatal_error_detected": False,
            }
            return result

        with TemporaryDirectory() as directory:
            session_dir = Path(directory)

            self._prepare_session(
                session_dir,
                grading_agents,
                input_text,
            )

            output = io.StringIO()

            with (
                patch.object(
                    grading_agents,
                    "_phase2_latest_session_dir",
                    return_value=session_dir,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    side_effect=capture_json_write,
                ),
                patch.object(
                    grading_agents,
                    "_phase6_run_gemini_semantic_grader",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase8_run_originality_evaluator",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase9_run_question_type_lens",
                    return_value=self._question_type_result(),
                ),
                patch.object(
                    grading_agents,
                    "_phase10_run_model_answer_reference",
                    return_value=self._model_reference_result(),
                ),
                patch.object(
                    logic_check_evaluator,
                    "attach_logic_check_to_grade",
                    side_effect=attach_logic,
                ),
                patch.object(
                    difficulty_output_adapter,
                    "attach_difficulty_strategy_to_grade",
                    side_effect=lambda grade, **kwargs: grade,
                ),
                patch.object(
                    difficulty_score_ceiling,
                    "apply_difficulty_score_ceiling",
                    side_effect=lambda grade, **kwargs: grade,
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase2_postprocess_grade(
                        {"total_score": 22.0}
                    )
                )

        self.assertIsInstance(result, dict)
        self.assertIn(
            "logic_check_evaluation.json",
            write_names,
        )
        self.assertIn(
            "grade.json",
            write_names,
        )
        self.assertIn(
            "phase3b logic check persistence failed",
            output.getvalue(),
        )
        self.assertIn(
            "simulated logic persistence failure",
            output.getvalue(),
        )

    def test_phase2_question_extraction_failure_uses_input_text(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import difficulty_output_adapter
        import difficulty_score_ceiling
        import grading_agents
        import logic_check_evaluator

        input_text = """문제:
제어밸브 액추에이터를 비교하시오.

답안:
공압식, 전동식, 유압식을 비교한다.
"""

        difficulty_questions: list[str | None] = []

        def capture_strategy(
            grade,
            *,
            question_text=None,
        ):
            difficulty_questions.append(question_text)
            return grade

        with TemporaryDirectory() as directory:
            session_dir = Path(directory)

            self._prepare_session(
                session_dir,
                grading_agents,
                input_text,
            )

            output = io.StringIO()

            with (
                patch.object(
                    grading_agents,
                    "_phase2_latest_session_dir",
                    return_value=session_dir,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    return_value=None,
                ),
                patch.object(
                    grading_agents,
                    "_phase3_evaluate_fact_anchors",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase3_extract_question_text",
                    side_effect=RuntimeError(
                        "simulated question extraction failure"
                    ),
                ),
                patch.object(
                    grading_agents,
                    "_phase6_run_gemini_semantic_grader",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase8_run_originality_evaluator",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase9_run_question_type_lens",
                    return_value=self._question_type_result(),
                ),
                patch.object(
                    grading_agents,
                    "_phase10_run_model_answer_reference",
                    return_value=self._model_reference_result(),
                ),
                patch.object(
                    logic_check_evaluator,
                    "attach_logic_check_to_grade",
                    side_effect=lambda grade, _text: grade,
                ),
                patch.object(
                    difficulty_output_adapter,
                    "attach_difficulty_strategy_to_grade",
                    side_effect=capture_strategy,
                ),
                patch.object(
                    difficulty_score_ceiling,
                    "apply_difficulty_score_ceiling",
                    side_effect=lambda grade, **kwargs: grade,
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase2_postprocess_grade(
                        {"total_score": 18.0}
                    )
                )

        self.assertIsInstance(result, dict)
        self.assertEqual(
            difficulty_questions,
            [input_text],
        )
        self.assertIn(
            (
                "phase20 question extraction failed; "
                "using input text"
            ),
            output.getvalue(),
        )
        self.assertIn(
            "simulated question extraction failure",
            output.getvalue(),
        )

    def test_phase2_traceback_format_failure_preserves_grade(
        self,
    ) -> None:
        import io
        import traceback
        from contextlib import redirect_stdout
        from tempfile import TemporaryDirectory

        import difficulty_output_adapter
        import difficulty_score_ceiling
        import grading_agents
        import logic_check_evaluator

        input_text = """문제:
2차 시스템의 감쇠비를 설명하시오.

답안:
감쇠비에 따라 과도응답이 달라진다.
"""

        ceiling_inputs: list[dict] = []

        def fail_strategy(
            grade,
            *,
            question_text=None,
        ):
            raise RuntimeError(
                "simulated difficulty strategy failure"
            )

        def capture_ceiling(
            grade,
            *,
            question_text=None,
            answer_text=None,
        ):
            ceiling_inputs.append(deepcopy(grade))
            return grade

        with TemporaryDirectory() as directory:
            session_dir = Path(directory)

            self._prepare_session(
                session_dir,
                grading_agents,
                input_text,
            )

            output = io.StringIO()

            with (
                patch.object(
                    grading_agents,
                    "_phase2_latest_session_dir",
                    return_value=session_dir,
                ),
                patch.object(
                    grading_agents,
                    "_phase2_json_write",
                    return_value=None,
                ),
                patch.object(
                    grading_agents,
                    "_phase6_run_gemini_semantic_grader",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase8_run_originality_evaluator",
                    return_value={},
                ),
                patch.object(
                    grading_agents,
                    "_phase9_run_question_type_lens",
                    return_value=self._question_type_result(),
                ),
                patch.object(
                    grading_agents,
                    "_phase10_run_model_answer_reference",
                    return_value=self._model_reference_result(),
                ),
                patch.object(
                    logic_check_evaluator,
                    "attach_logic_check_to_grade",
                    side_effect=lambda grade, _text: grade,
                ),
                patch.object(
                    difficulty_output_adapter,
                    "attach_difficulty_strategy_to_grade",
                    side_effect=fail_strategy,
                ),
                patch.object(
                    traceback,
                    "format_exc",
                    side_effect=RuntimeError(
                        "simulated traceback formatting failure"
                    ),
                ),
                patch.object(
                    difficulty_score_ceiling,
                    "apply_difficulty_score_ceiling",
                    side_effect=capture_ceiling,
                ),
                redirect_stdout(output),
            ):
                result = (
                    grading_agents
                    ._phase2_postprocess_grade(
                        {"total_score": 17.0}
                    )
                )

        self.assertIsInstance(result, dict)
        self.assertEqual(len(ceiling_inputs), 1)
        self.assertEqual(
            result,
            ceiling_inputs[0],
        )
        self.assertIn(
            "phase20 final difficulty strategy skipped",
            output.getvalue(),
        )
        self.assertIn(
            "simulated difficulty strategy failure",
            output.getvalue(),
        )
        self.assertIn(
            "phase20 traceback formatting failed",
            output.getvalue(),
        )
        self.assertIn(
            "simulated traceback formatting failure",
            output.getvalue(),
        )


class OriginalityGraderJsonContractRegressionTest(
    unittest.TestCase
):
    def test_originality_extract_json_parses_fenced_and_embedded_objects(
        self,
    ) -> None:
        import originality_grader

        cases = (
            (
                """```json
                {
                    "originality_score": 3.5,
                    "judgment": "independent"
                }
                ```""",
                {
                    "originality_score": 3.5,
                    "judgment": "independent",
                },
            ),
            (
                (
                    "Gemini 분석 결과입니다.\n"
                    '{"originality_score": 2.5, '
                    '"judgment": "partial"}\n'
                    "검토를 완료했습니다."
                ),
                {
                    "originality_score": 2.5,
                    "judgment": "partial",
                },
            ),
            (
                """```json
                {
                    "originality_score": 4.0,
                    "evidence": {
                        "independent_reasoning": true
                    }
                }
                ```""",
                {
                    "originality_score": 4.0,
                    "evidence": {
                        "independent_reasoning": True,
                    },
                },
            ),
        )

        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(
                    originality_grader._extract_json(
                        raw
                    ),
                    expected,
                )

    def test_originality_extract_json_rejects_malformed_and_non_object_payloads(
        self,
    ) -> None:
        import originality_grader

        invalid_payloads = (
            "",
            "JSON 응답이 없습니다.",
            '{"originality_score": 3.0',
            "[1, 2, 3]",
            "```json\n[1, 2, 3]\n```",
            '"plain string"',
            "null",
        )

        for raw in invalid_payloads:
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(
                    ValueError,
                    "JSON object not found",
                ):
                    originality_grader._extract_json(
                        raw
                    )

    def test_originality_http_body_read_failure_is_reported(
        self,
    ) -> None:
        import os
        import urllib.error

        import originality_grader

        class BrokenBody:
            def read(self):
                raise OSError(
                    "simulated response body read failure"
                )

            def close(self) -> None:
                return

        http_error = urllib.error.HTTPError(
            url="https://example.invalid/gemini",
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=BrokenBody(),
        )

        with (
            patch.dict(
                os.environ,
                {
                    "GEMINI_API_KEY": "test-key",
                    "GEMINI_MODEL": "test-model",
                },
                clear=True,
            ),
            patch.object(
                originality_grader.urllib.request,
                "urlopen",
                side_effect=http_error,
            ),
        ):
            result = (
                originality_grader
                .gemini_originality_evaluate(
                    question_text="질문",
                    answer_text="답안",
                )
            )

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["model"],
            "test-model",
        )
        self.assertIsNone(result["parsed"])
        self.assertIn(
            "HTTPError 429",
            result["error"],
        )
        self.assertIn(
            "response body unavailable",
            result["error"],
        )
        self.assertIn(
            "simulated response body read failure",
            result["error"],
        )


class LogicTopicRoutingFailureRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _write_bank(
        directory,
    ) -> Path:
        bank_path = Path(directory) / "logic_checks.json"

        bank_path.write_text(
            """
            {
              "version": "test",
              "topic_logic_checks": [
                {
                  "topic_id": "neighbor_topic",
                  "topic_name": "Neighbor Topic",
                  "enabled": true,
                  "fatal_checks": [
                    {
                      "id": "neighbor_fatal",
                      "severity": "fatal",
                      "wrong_patterns": ["wrong marker"],
                      "message": "neighbor rule leaked",
                      "recommended_ceiling": 10
                    }
                  ],
                  "major_checks": [],
                  "question_type_checks": [],
                  "next_practice_points": []
                }
              ]
            }
            """,
            encoding="utf-8",
        )

        return bank_path

    def test_logic_topic_routing_failure_skips_full_bank_and_reports_diagnostic(
        self,
    ) -> None:
        from tempfile import TemporaryDirectory

        import logic_check_evaluator

        class ExplodingGrade(dict):
            def get(
                self,
                key,
                default=None,
            ):
                raise RuntimeError(
                    "simulated logic topic routing failure"
                )

        with TemporaryDirectory() as directory:
            bank_path = self._write_bank(directory)

            with patch.object(
                logic_check_evaluator,
                "_topic_applies",
                side_effect=AssertionError(
                    "full logic-check bank must not be evaluated"
                ),
            ) as topic_applies:
                result = (
                    logic_check_evaluator
                    .evaluate_logic_checks(
                        answer_text="wrong marker",
                        grade=ExplodingGrade(
                            {
                                "topic_id": "target_topic",
                            }
                        ),
                        bank_path=bank_path,
                    )
                )

        self.assertFalse(result["applicable"])
        self.assertEqual(result["mode"], "pass")
        self.assertFalse(
            result["fatal_error_detected"]
        )
        self.assertEqual(result["findings"], [])
        self.assertEqual(
            topic_applies.call_count,
            0,
        )

        diagnostic = result.get(
            "topic_routing_diagnostic"
        )

        self.assertIsInstance(diagnostic, dict)
        self.assertFalse(diagnostic["ok"])
        self.assertEqual(
            diagnostic["fallback"],
            "skip_topic_logic_checks",
        )
        self.assertIn(
            "simulated logic topic routing failure",
            diagnostic["error"],
        )
        self.assertIn(
            "전체 로직 체크 bank 적용을 중단",
            diagnostic["reason"],
        )

    def test_logic_topic_routing_ignores_malformed_reference_candidate(
        self,
    ) -> None:
        from tempfile import TemporaryDirectory

        import logic_check_evaluator

        grade = {
            "model_answer_reference": {
                "primary_reference": None,
                "candidates": [
                    "malformed candidate",
                ],
            },
        }

        with TemporaryDirectory() as directory:
            bank_path = self._write_bank(directory)

            with patch.object(
                logic_check_evaluator,
                "_topic_applies",
                return_value=False,
            ) as topic_applies:
                result = (
                    logic_check_evaluator
                    .evaluate_logic_checks(
                        answer_text="정상 답안",
                        grade=grade,
                        bank_path=bank_path,
                    )
                )

        self.assertFalse(result["applicable"])
        self.assertEqual(result["findings"], [])
        self.assertNotIn(
            "topic_routing_diagnostic",
            result,
        )
        self.assertEqual(
            topic_applies.call_count,
            1,
        )


class GeminiScoreFiniteNormalizationRegressionTest(
    unittest.TestCase
):
    def test_non_finite_gemini_score_falls_back_to_base(
        self,
    ) -> None:
        from grading_agents import (
            _phase6_limit_gemini_score,
        )

        for value in (
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(value=value):
                result = (
                    _phase6_limit_gemini_score(
                        layer_id="C",
                        base_score=5.0,
                        gemini_score=value,
                        max_score=10.0,
                    )
                )

                self.assertEqual(
                    result["base_score"],
                    5.0,
                )
                self.assertEqual(
                    result["raw_gemini_score"],
                    5.0,
                )
                self.assertEqual(
                    result["effective_score"],
                    5.0,
                )
                self.assertFalse(
                    result["raise_limited"]
                )
                self.assertEqual(
                    result[
                        "normalization_fallbacks"
                    ],
                    [
                        "gemini_score_non_finite",
                    ],
                )

    def test_non_finite_base_score_uses_zero_fallback(
        self,
    ) -> None:
        from grading_agents import (
            _phase6_limit_gemini_score,
        )

        for value in (
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(value=value):
                result = (
                    _phase6_limit_gemini_score(
                        layer_id="C",
                        base_score=value,
                        gemini_score=5.0,
                        max_score=10.0,
                    )
                )

                self.assertEqual(
                    result["base_score"],
                    0.0,
                )
                self.assertEqual(
                    result["raw_gemini_score"],
                    5.0,
                )
                self.assertEqual(
                    result["effective_score"],
                    0.75,
                )
                self.assertTrue(
                    result["raise_limited"]
                )
                self.assertEqual(
                    result[
                        "normalization_fallbacks"
                    ],
                    [
                        "base_score_non_finite",
                    ],
                )

    def test_non_finite_maximum_disables_layer_score(
        self,
    ) -> None:
        from grading_agents import (
            _phase6_limit_gemini_score,
        )

        for value in (
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(value=value):
                result = (
                    _phase6_limit_gemini_score(
                        layer_id="C",
                        base_score=5.0,
                        gemini_score=7.0,
                        max_score=value,
                    )
                )

                self.assertEqual(
                    result["base_score"],
                    0.0,
                )
                self.assertEqual(
                    result["raw_gemini_score"],
                    0.0,
                )
                self.assertEqual(
                    result["effective_score"],
                    0.0,
                )
                self.assertFalse(
                    result["raise_limited"]
                )
                self.assertEqual(
                    result[
                        "normalization_fallbacks"
                    ],
                    [
                        "max_score_non_finite",
                    ],
                )


class RaterScoreFiniteNormalizationRegressionTest(
    unittest.TestCase
):
    def test_rater_score_coercion_rejects_invalid_and_non_finite_values(
        self,
    ) -> None:
        from grading_agents import (
            _coerce_finite_rater_score,
        )

        self.assertEqual(
            _coerce_finite_rater_score(3.5),
            3.5,
        )
        self.assertEqual(
            _coerce_finite_rater_score("3.5"),
            3.5,
        )

        for value in (
            "invalid",
            None,
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(value=value):
                result = (
                    _coerce_finite_rater_score(
                        value,
                    )
                )

                self.assertEqual(result, 0.0)

    def test_score_map_rejects_non_finite_rater_scores(
        self,
    ) -> None:
        from grading_agents import (
            score_map_from_rows,
        )

        rows = [
            {
                "item": "A",
                "score": float("nan"),
                "reason": "nan",
            },
            {
                "item": "B",
                "score": float("inf"),
                "reason": "positive infinity",
            },
            {
                "item": "C",
                "score": float("-inf"),
                "reason": "negative infinity",
            },
            {
                "item": "D",
                "score": "invalid",
                "reason": "invalid",
            },
            {
                "item": "E",
                "score": "2.5",
                "reason": "numeric string",
            },
        ]

        result = score_map_from_rows(rows)

        self.assertEqual(
            result["A"]["score"],
            0.0,
        )
        self.assertEqual(
            result["B"]["score"],
            0.0,
        )
        self.assertEqual(
            result["C"]["score"],
            0.0,
        )
        self.assertEqual(
            result["D"]["score"],
            0.0,
        )
        self.assertEqual(
            result["E"]["score"],
            2.5,
        )


class GeminiGraderJsonContractRegressionTest(
    unittest.TestCase
):
    def test_gemini_grader_extract_json_parses_object_variants(
        self,
    ) -> None:
        from gemini_grader import _extract_json

        cases = {
            "plain": (
                '{"score": 1}',
                {"score": 1},
            ),
            "fenced_json": (
                '```json\n{"score": 2}\n```',
                {"score": 2},
            ),
            "fenced_plain": (
                '```\n{"score": 3}\n```',
                {"score": 3},
            ),
            "embedded": (
                'prefix {"score": 4} suffix',
                {"score": 4},
            ),
            "nested": (
                'prefix {"outer": {"inner": 5}} suffix',
                {
                    "outer": {
                        "inner": 5,
                    },
                },
            ),
            "truncated_fence_with_later_object": (
                (
                    '```json\n{"broken":\n'
                    'text {"score": 6} suffix'
                ),
                {"score": 6},
            ),
            "multiple_objects_uses_first": (
                (
                    'first {"score": 7} '
                    'second {"score": 8}'
                ),
                {"score": 7},
            ),
            "brace_inside_string": (
                (
                    'prefix {"text": "value with } brace", '
                    '"score": 9} suffix'
                ),
                {
                    "text": "value with } brace",
                    "score": 9,
                },
            ),
        }

        for label, (
            payload,
            expected,
        ) in cases.items():
            with self.subTest(label=label):
                self.assertEqual(
                    _extract_json(payload),
                    expected,
                )

    def test_gemini_grader_extract_json_rejects_non_object_and_malformed_payloads(
        self,
    ) -> None:
        from gemini_grader import _extract_json

        payloads = {
            "plain_array": '[{"score": 1}]',
            "fenced_array": (
                '```json\n[{"score": 2}]\n```'
            ),
            "string": '"scalar"',
            "number": '3',
            "boolean": 'true',
            "null": 'null',
            "empty": '',
            "whitespace": '   \n\t ',
            "malformed": '{"score": 4',
        }

        for label, payload in payloads.items():
            with self.subTest(label=label):
                with self.assertRaises(
                    ValueError,
                ):
                    _extract_json(payload)


class MigrationCompatibilityImportRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _migration_import_statement():
        import ast
        from pathlib import Path

        source_path = Path(
            "scripts/migrations/"
            "apply_fact_anchors_and_cleanup.py"
        )
        source = source_path.read_text(
            encoding="utf-8"
        )
        tree = ast.parse(
            source,
            filename=str(source_path),
        )

        matches = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.Try):
                continue

            imported_names = {
                alias.name
                for statement in node.body
                if isinstance(
                    statement,
                    ast.ImportFrom,
                )
                and statement.module
                == "rubric_registry"
                for alias in statement.names
            }

            if imported_names == {
                "load_model_answer_bank",
                "save_model_answer_bank",
                "validate_model_answer_bank",
                "question_type_ids",
            }:
                matches.append(node)

        if len(matches) != 1:
            raise AssertionError(
                "rubric_registry compatibility "
                f"try count={len(matches)}"
            )

        isolated = ast.Module(
            body=[matches[0]],
            type_ignores=[],
        )
        ast.fix_missing_locations(isolated)

        return compile(
            isolated,
            str(source_path),
            "exec",
        )

    def test_migration_compatibility_import_allows_missing_registry(
        self,
    ) -> None:
        import builtins
        from unittest.mock import patch

        compiled = (
            self._migration_import_statement()
        )
        real_import = builtins.__import__

        def missing_registry(
            name,
            globals=None,
            locals=None,
            fromlist=(),
            level=0,
        ):
            if name == "rubric_registry":
                raise ModuleNotFoundError(
                    "simulated legacy repository"
                )

            return real_import(
                name,
                globals,
                locals,
                fromlist,
                level,
            )

        namespace = {}

        with patch(
            "builtins.__import__",
            side_effect=missing_registry,
        ):
            exec(compiled, namespace)

        for name in (
            "load_model_answer_bank",
            "save_model_answer_bank",
            "validate_model_answer_bank",
            "question_type_ids",
        ):
            with self.subTest(name=name):
                self.assertIsNone(
                    namespace[name]
                )

    def test_migration_compatibility_import_does_not_hide_runtime_error(
        self,
    ) -> None:
        import builtins
        from unittest.mock import patch

        compiled = (
            self._migration_import_statement()
        )
        real_import = builtins.__import__

        def broken_registry(
            name,
            globals=None,
            locals=None,
            fromlist=(),
            level=0,
        ):
            if name == "rubric_registry":
                raise RuntimeError(
                    "simulated registry initialization bug"
                )

            return real_import(
                name,
                globals,
                locals,
                fromlist,
                level,
            )

        namespace = {}

        with patch(
            "builtins.__import__",
            side_effect=broken_registry,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "registry initialization bug",
            ):
                exec(compiled, namespace)

        for name in (
            "load_model_answer_bank",
            "save_model_answer_bank",
            "validate_model_answer_bank",
            "question_type_ids",
        ):
            with self.subTest(name=name):
                self.assertNotIn(
                    name,
                    namespace,
                )


class BotStateLoadingRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _default_state():
        return {
            "last_update_id": 0,
            "chats": {},
        }

    def test_load_state_missing_file_returns_default_without_diagnostic(
        self,
    ) -> None:
        import io
        import tempfile
        from contextlib import redirect_stdout
        from pathlib import Path
        from unittest.mock import patch

        import bot

        with tempfile.TemporaryDirectory(
            prefix="state_missing_"
        ) as temp_dir:
            state_path = (
                Path(temp_dir) / "state.json"
            )
            output = io.StringIO()

            with (
                patch.object(
                    bot,
                    "STATE_FILE",
                    state_path,
                ),
                patch.object(
                    bot,
                    "ensure_dirs",
                    lambda: None,
                ),
                redirect_stdout(output),
            ):
                result = bot.load_state()

        self.assertEqual(
            result,
            self._default_state(),
        )
        self.assertEqual(
            output.getvalue(),
            "",
        )

    def test_load_state_valid_object_is_returned_and_missing_fields_are_normalized(
        self,
    ) -> None:
        import json
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        import bot

        cases = (
            (
                {
                    "last_update_id": 14,
                    "chats": {
                        "100": {
                            "mode": "test",
                        },
                    },
                    "custom": "preserved",
                },
                {
                    "last_update_id": 14,
                    "chats": {
                        "100": {
                            "mode": "test",
                        },
                    },
                    "custom": "preserved",
                },
            ),
            (
                {},
                self._default_state(),
            ),
            (
                {
                    "chats": {
                        "200": {},
                    },
                },
                {
                    "last_update_id": 0,
                    "chats": {
                        "200": {},
                    },
                },
            ),
            (
                {
                    "last_update_id": 4,
                },
                {
                    "last_update_id": 4,
                    "chats": {},
                },
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="state_valid_"
        ) as temp_dir:
            state_path = (
                Path(temp_dir) / "state.json"
            )

            for payload, expected in cases:
                with self.subTest(
                    payload=payload
                ):
                    state_path.write_text(
                        json.dumps(
                            payload,
                            ensure_ascii=False,
                        ),
                        encoding="utf-8",
                    )

                    with (
                        patch.object(
                            bot,
                            "STATE_FILE",
                            state_path,
                        ),
                        patch.object(
                            bot,
                            "ensure_dirs",
                            lambda: None,
                        ),
                    ):
                        result = (
                            bot.load_state()
                        )

                    self.assertEqual(
                        result,
                        expected,
                    )

    def test_load_state_malformed_json_reports_recovery(
        self,
    ) -> None:
        import io
        import tempfile
        from contextlib import redirect_stdout
        from pathlib import Path
        from unittest.mock import patch

        import bot

        with tempfile.TemporaryDirectory(
            prefix="state_malformed_"
        ) as temp_dir:
            state_path = (
                Path(temp_dir) / "state.json"
            )
            state_path.write_text(
                '{"last_update_id":',
                encoding="utf-8",
            )
            output = io.StringIO()

            with (
                patch.object(
                    bot,
                    "STATE_FILE",
                    state_path,
                ),
                patch.object(
                    bot,
                    "ensure_dirs",
                    lambda: None,
                ),
                redirect_stdout(output),
            ):
                result = bot.load_state()

        self.assertEqual(
            result,
            self._default_state(),
        )
        self.assertIn(
            "[bot] state load failed; "
            "using default state:",
            output.getvalue(),
        )
        self.assertIn(
            "JSONDecodeError",
            output.getvalue(),
        )

    def test_load_state_rejects_non_object_json_roots(
        self,
    ) -> None:
        import io
        import json
        import tempfile
        from contextlib import redirect_stdout
        from pathlib import Path
        from unittest.mock import patch

        import bot

        payloads = (
            [],
            "scalar",
            None,
            True,
            3,
        )

        with tempfile.TemporaryDirectory(
            prefix="state_non_object_"
        ) as temp_dir:
            state_path = (
                Path(temp_dir) / "state.json"
            )

            for payload in payloads:
                with self.subTest(
                    payload=payload
                ):
                    state_path.write_text(
                        json.dumps(payload),
                        encoding="utf-8",
                    )
                    output = io.StringIO()

                    with (
                        patch.object(
                            bot,
                            "STATE_FILE",
                            state_path,
                        ),
                        patch.object(
                            bot,
                            "ensure_dirs",
                            lambda: None,
                        ),
                        redirect_stdout(output),
                    ):
                        result = (
                            bot.load_state()
                        )

                    self.assertEqual(
                        result,
                        self._default_state(),
                    )
                    self.assertIn(
                        "state root must be "
                        "a JSON object",
                        output.getvalue(),
                    )

    def test_load_state_rejects_invalid_required_field_types(
        self,
    ) -> None:
        import io
        import json
        import tempfile
        from contextlib import redirect_stdout
        from pathlib import Path
        from unittest.mock import patch

        import bot

        cases = (
            (
                {
                    "last_update_id": True,
                    "chats": {},
                },
                "state.last_update_id",
            ),
            (
                {
                    "last_update_id": "15",
                    "chats": {},
                },
                "state.last_update_id",
            ),
            (
                {
                    "last_update_id": -1,
                    "chats": {},
                },
                "state.last_update_id",
            ),
            (
                {
                    "last_update_id": float(
                        "nan"
                    ),
                    "chats": {},
                },
                "state.last_update_id",
            ),
            (
                {
                    "last_update_id": 0,
                    "chats": [],
                },
                "state.chats",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="state_invalid_fields_"
        ) as temp_dir:
            state_path = (
                Path(temp_dir) / "state.json"
            )

            for payload, marker in cases:
                with self.subTest(
                    payload=payload
                ):
                    state_path.write_text(
                        json.dumps(
                            payload,
                            allow_nan=True,
                        ),
                        encoding="utf-8",
                    )
                    output = io.StringIO()

                    with (
                        patch.object(
                            bot,
                            "STATE_FILE",
                            state_path,
                        ),
                        patch.object(
                            bot,
                            "ensure_dirs",
                            lambda: None,
                        ),
                        redirect_stdout(output),
                    ):
                        result = (
                            bot.load_state()
                        )

                    self.assertEqual(
                        result,
                        self._default_state(),
                    )
                    self.assertIn(
                        marker,
                        output.getvalue(),
                    )

    def test_load_state_read_failure_reports_recovery(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch

        import bot

        class FailingStatePath:
            def exists(self):
                return True

            def read_text(
                self,
                *args,
                **kwargs,
            ):
                raise OSError(
                    "simulated state read failure"
                )

        output = io.StringIO()

        with (
            patch.object(
                bot,
                "STATE_FILE",
                FailingStatePath(),
            ),
            patch.object(
                bot,
                "ensure_dirs",
                lambda: None,
            ),
            redirect_stdout(output),
        ):
            result = bot.load_state()

        self.assertEqual(
            result,
            self._default_state(),
        )
        self.assertIn(
            "simulated state read failure",
            output.getvalue(),
        )
        self.assertIn(
            "[bot] state load failed; "
            "using default state:",
            output.getvalue(),
        )


class QuestionTypeCoveragePenaltyDisplayRegressionTest(
    unittest.TestCase
):
    COVERAGE_KEY = 'question_type_coverage_score_adjustment'

    @classmethod
    def _display(
        cls,
        penalty,
    ) -> str:
        import bot

        return (
            bot._format_question_type_coverage_display(
                {
                    cls.COVERAGE_KEY: {
                        "recommended_penalty": penalty,
                    },
                }
            )
        )

    def test_question_type_coverage_display_accepts_finite_penalties(
        self,
    ) -> None:
        numeric = self._display(1.5)
        numeric_string = self._display("1.5")
        zero = self._display(0)

        self.assertTrue(numeric)
        self.assertEqual(
            numeric_string,
            numeric,
        )
        self.assertNotIn(
            "확인 불가",
            numeric,
        )
        self.assertNotIn(
            "확인 불가",
            zero,
        )

    def test_question_type_coverage_display_marks_invalid_penalty_unavailable(
        self,
    ) -> None:
        for penalty in (
            "invalid",
            None,
            True,
            [],
            {},
        ):
            with self.subTest(
                penalty=penalty
            ):
                display = self._display(
                    penalty
                )

                self.assertIn(
                    "권고 감점: 확인 불가",
                    display,
                )

    def test_question_type_coverage_display_rejects_non_finite_penalty(
        self,
    ) -> None:
        for penalty in (
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(
                penalty=penalty
            ):
                display = self._display(
                    penalty
                )

                self.assertIn(
                    "권고 감점: 확인 불가",
                    display,
                )
                self.assertNotIn(
                    "nan",
                    display.lower(),
                )
                self.assertNotIn(
                    "inf",
                    display.lower(),
                )


class OriginalityMergeScoreCoercionRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _merge(
        final_score_marker,
        *,
        include_score=True,
        comment="현장 판단 반영",
    ):
        import grading_agents

        parsed = {
            "raw_originality_score": 1.7,
            "overall_comment": comment,
            "improvement_advice": [],
        }

        if include_score:
            parsed[
                "final_originality_score"
            ] = final_score_marker

        grade = {
            "summary": "기존 요약",
            "strengths": [],
            "weaknesses": [],
            "rewrite_advice": [],
        }

        return (
            grading_agents
            ._phase8_merge_originality_feedback(
                grade,
                {
                    "ok": True,
                    "parsed": parsed,
                },
            )
        )

    def test_originality_merge_accepts_finite_final_scores(
        self,
    ) -> None:
        high = self._merge(1.5)
        medium = self._merge("0.8")
        low = self._merge(0)

        self.assertEqual(
            high["originality_score"],
            1.5,
        )
        self.assertEqual(
            medium["originality_score"],
            0.8,
        )
        self.assertEqual(
            low["originality_score"],
            0.0,
        )

        self.assertTrue(
            any(
                "독창성/기술사적 판단성: "
                "1.5/2.0"
                in item
                for item in high["strengths"]
            )
        )
        self.assertTrue(
            any(
                "독창성/기술사적 판단성 보통: "
                "0.8/2.0"
                in item
                for item
                in medium["weaknesses"]
            )
        )
        self.assertTrue(
            any(
                "독창성/기술사적 판단성 부족: "
                "0/2.0"
                in item
                for item in low["weaknesses"]
            )
        )

        for result in (
            high,
            medium,
            low,
        ):
            self.assertNotIn(
                "originality_feedback_diagnostic",
                result,
            )
            self.assertIn(
                "독창성/기술사적 판단성 평가는",
                result["summary"],
            )

    def test_originality_merge_preserves_missing_score_semantics(
        self,
    ) -> None:
        missing = self._merge(
            None,
            include_score=False,
        )
        none_value = self._merge(None)

        for result in (
            missing,
            none_value,
        ):
            self.assertNotIn(
                "originality_score",
                result,
            )
            self.assertNotIn(
                "originality_raw_score",
                result,
            )
            self.assertNotIn(
                "originality_feedback_diagnostic",
                result,
            )
            self.assertEqual(
                result["summary"],
                "기존 요약",
            )
            self.assertEqual(
                result["strengths"],
                [],
            )
            self.assertEqual(
                result["weaknesses"],
                [],
            )

    def test_originality_merge_rejects_malformed_final_scores(
        self,
    ) -> None:
        import io
        from contextlib import redirect_stdout

        for value in (
            "invalid",
            True,
            [],
            {},
        ):
            with self.subTest(value=value):
                output = io.StringIO()

                with redirect_stdout(output):
                    result = self._merge(
                        value
                    )

                self.assertNotIn(
                    "originality_score",
                    result,
                )
                self.assertNotIn(
                    "originality_raw_score",
                    result,
                )
                self.assertEqual(
                    result["summary"],
                    "기존 요약",
                )
                self.assertEqual(
                    result["strengths"],
                    [],
                )
                self.assertEqual(
                    result["weaknesses"],
                    [],
                )

                diagnostic = result[
                    "originality_feedback_diagnostic"
                ]

                self.assertEqual(
                    diagnostic["field"],
                    "final_originality_score",
                )
                self.assertIn(
                    "final_originality_score",
                    diagnostic["error"],
                )
                self.assertIn(
                    "[agent] phase8 originality "
                    "feedback score invalid:",
                    output.getvalue(),
                )

    def test_originality_merge_rejects_non_finite_final_scores(
        self,
    ) -> None:
        import io
        import math
        from contextlib import redirect_stdout

        for value in (
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(value=value):
                output = io.StringIO()

                with redirect_stdout(output):
                    result = self._merge(
                        value
                    )

                self.assertNotIn(
                    "originality_score",
                    result,
                )
                self.assertNotIn(
                    "originality_raw_score",
                    result,
                )
                self.assertEqual(
                    result["summary"],
                    "기존 요약",
                )
                self.assertEqual(
                    result["strengths"],
                    [],
                )
                self.assertEqual(
                    result["weaknesses"],
                    [],
                )

                diagnostic = result[
                    "originality_feedback_diagnostic"
                ]

                self.assertIn(
                    "must be finite",
                    diagnostic["error"],
                )

                self.assertFalse(
                    any(
                        isinstance(item, float)
                        and not math.isfinite(item)
                        for item
                        in result.values()
                    )
                )
                self.assertIn(
                    "[agent] phase8 originality "
                    "feedback score invalid:",
                    output.getvalue(),
                )


class LogicLlmFatalCheckDiagnosticRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _topic_check():
        return {
            "topic_id": "logic_llm_probe",
            "topic_name": "Logic LLM probe",
            "fatal_checks": [
                {
                    "id": "fatal_probe",
                    "message": "probe message",
                    "correct_rule": (
                        "probe correction"
                    ),
                    "recommended_ceiling": 10.0,
                    "affected_layers": ["C"],
                    "wrong_patterns": [],
                },
            ],
        }

    @classmethod
    def _run_verifier(
        cls,
        verifier,
    ):
        import copy
        import sys
        import types

        import logic_check_evaluator

        fake_module = types.ModuleType(
            "logic_llm_verifier"
        )
        fake_module._call_ollama_json = verifier

        original_module = sys.modules.get(
            "logic_llm_verifier"
        )

        try:
            sys.modules[
                "logic_llm_verifier"
            ] = fake_module

            return (
                logic_check_evaluator
                ._evaluate_topic_fatal_checks_with_llm(
                    "logic LLM probe answer",
                    copy.deepcopy(
                        cls._topic_check()
                    ),
                )
            )
        finally:
            if original_module is None:
                sys.modules.pop(
                    "logic_llm_verifier",
                    None,
                )
            else:
                sys.modules[
                    "logic_llm_verifier"
                ] = original_module

    def _assert_diagnostic(
        self,
        result,
        reason,
    ) -> None:
        self.assertIsInstance(
            result,
            list,
        )
        self.assertEqual(
            len(result),
            1,
        )

        finding = result[0]

        self.assertEqual(
            finding["id"],
            "topic_fatal_semantic_llm_error",
        )
        self.assertEqual(
            finding["severity"],
            "minor",
        )
        self.assertEqual(
            finding["affected_layers"],
            ["C"],
        )
        self.assertNotIn(
            "recommended_ceiling",
            finding,
        )
        self.assertEqual(
            finding["diagnostic"]["ok"],
            False,
        )
        self.assertEqual(
            finding["diagnostic"]["reason"],
            reason,
        )
        self.assertIn(
            "fatal cap을 적용하지 않습니다",
            finding["correct_rule"],
        )

    def test_logic_llm_call_failure_returns_diagnostic_finding(
        self,
    ) -> None:
        def raise_failure(prompt):
            raise RuntimeError(
                "simulated verifier failure"
            )

        result = self._run_verifier(
            raise_failure
        )

        self._assert_diagnostic(
            result,
            "verifier_call_failed",
        )
        self.assertIn(
            "simulated verifier failure",
            result[0]["diagnostic"]["error"],
        )

    def test_logic_llm_non_object_response_returns_diagnostic_finding(
        self,
    ) -> None:
        for payload in (
            None,
            [],
            "invalid",
        ):
            with self.subTest(
                payload=payload
            ):
                result = self._run_verifier(
                    lambda prompt, payload=payload: (
                        payload
                    )
                )

                self._assert_diagnostic(
                    result,
                    "response_must_be_object",
                )

    def test_logic_llm_invalid_findings_shape_returns_diagnostic_finding(
        self,
    ) -> None:
        payloads = (
            (
                {
                    "confidence": 0.9,
                },
                "findings_field_missing",
            ),
            (
                {
                    "confidence": 0.9,
                    "findings": {},
                },
                "findings_must_be_list",
            ),
            (
                {
                    "confidence": 0.9,
                    "findings": "invalid",
                },
                "findings_must_be_list",
            ),
        )

        for payload, reason in payloads:
            with self.subTest(
                payload=payload
            ):
                result = self._run_verifier(
                    lambda prompt, payload=payload: (
                        payload
                    )
                )

                self._assert_diagnostic(
                    result,
                    reason,
                )

    def test_logic_llm_non_dict_finding_returns_diagnostic_finding(
        self,
    ) -> None:
        result = self._run_verifier(
            lambda prompt: {
                "verdict": "fatal",
                "confidence": 0.9,
                "findings": [
                    "invalid",
                ],
            }
        )

        self._assert_diagnostic(
            result,
            "finding_item_must_be_object",
        )

    def test_logic_llm_invalid_global_confidence_returns_diagnostic_finding(
        self,
    ) -> None:
        payloads = (
            {},
            {
                "confidence": None,
            },
            {
                "confidence": True,
            },
            {
                "confidence": "invalid",
            },
            {
                "confidence": float("nan"),
            },
            {
                "confidence": float("inf"),
            },
            {
                "confidence": float("-inf"),
            },
        )

        for extra in payloads:
            with self.subTest(
                extra=extra
            ):
                payload = {
                    "verdict": "fatal",
                    "findings": [
                        {
                            "rule_id": "fatal_probe",
                            "severity": "fatal",
                        },
                    ],
                }
                payload.update(extra)

                result = self._run_verifier(
                    lambda prompt, payload=payload: (
                        payload
                    )
                )

                self._assert_diagnostic(
                    result,
                    "invalid_global_confidence",
                )

    def test_logic_llm_invalid_item_confidence_returns_diagnostic_finding(
        self,
    ) -> None:
        for confidence in (
            None,
            True,
            "invalid",
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(
                confidence=confidence
            ):
                result = self._run_verifier(
                    lambda prompt, confidence=confidence: {
                        "verdict": "fatal",
                        "confidence": 0.9,
                        "findings": [
                            {
                                "rule_id": (
                                    "fatal_probe"
                                ),
                                "severity": "fatal",
                                "confidence": (
                                    confidence
                                ),
                            },
                        ],
                    }
                )

                self._assert_diagnostic(
                    result,
                    "invalid_item_confidence",
                )

    def test_logic_llm_valid_empty_findings_remain_empty(
        self,
    ) -> None:
        result = self._run_verifier(
            lambda prompt: {
                "verdict": "pass",
                "confidence": 0.9,
                "findings": [],
                "reason": "no fatal claim",
            }
        )

        self.assertEqual(
            result,
            [],
        )

    def test_logic_llm_valid_fatal_finding_is_preserved(
        self,
    ) -> None:
        result = self._run_verifier(
            lambda prompt: {
                "verdict": "fatal",
                "confidence": "0.9",
                "findings": [
                    {
                        "rule_id": "fatal_probe",
                        "severity": "fatal",
                        "confidence": "0.85",
                        "message": "probe",
                        "evidence": (
                            "probe evidence"
                        ),
                    },
                ],
            }
        )

        self.assertEqual(
            len(result),
            1,
        )

        finding = result[0]

        self.assertEqual(
            finding["id"],
            "llm_semantic_fatal_probe",
        )
        self.assertEqual(
            finding["severity"],
            "fatal",
        )
        self.assertEqual(
            finding["confidence"],
            0.9,
        )
        self.assertEqual(
            finding["recommended_ceiling"],
            10.0,
        )
        self.assertNotIn(
            "diagnostic",
            finding,
        )


class LogicVerifierConfidenceRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _run_with_verdict(
        verdict,
    ):
        import logic_llm_verifier as verifier

        function = (
            verifier.verify_logic_with_llm
        )

        with patch.dict(
            function.__globals__,
            {
                "_call_ollama_json": (
                    lambda prompt: verdict
                ),
            },
            clear=False,
        ):
            return function(
                answer_text=(
                    "시스템은 우반평면에 극점이 "
                    "있어도 안정하다. 감쇠비가 "
                    "음수이면 진동이 감소한다."
                ),
                topic_id=(
                    "second_order_lag_"
                    "response_by_damping_ratio"
                ),
            )

    def test_logic_verifier_invalid_confidence_returns_warn_diagnostic(
        self,
    ) -> None:
        for confidence in (
            None,
            True,
            "invalid",
            [],
            {},
            float("nan"),
            float("inf"),
            float("-inf"),
        ):
            with self.subTest(
                confidence=confidence
            ):
                result = (
                    self._run_with_verdict(
                        {
                            "verdict": "fatal",
                            "confidence": (
                                confidence
                            ),
                            "findings": [],
                            "reason": "probe",
                        }
                    )
                )

                self.assertEqual(
                    result["verdict"],
                    "warn",
                )
                self.assertIsNone(
                    result["confidence"],
                )
                self.assertEqual(
                    result["mode"],
                    "warn",
                )
                self.assertFalse(
                    result[
                        "fatal_error_detected"
                    ]
                )
                self.assertIsNone(
                    result[
                        "recommended_ceiling"
                    ]
                )
                self.assertEqual(
                    result["reason"],
                    (
                        "LLM verifier invalid "
                        "confidence"
                    ),
                )

                findings = result[
                    "findings"
                ]

                self.assertEqual(
                    len(findings),
                    1,
                )
                self.assertEqual(
                    findings[0]["id"],
                    (
                        "llm_verifier_"
                        "invalid_confidence"
                    ),
                )
                self.assertEqual(
                    findings[0]["severity"],
                    "minor",
                )
                self.assertIn(
                    "fatal cap을 적용하지 않습니다",
                    findings[0][
                        "correct_rule"
                    ],
                )

                diagnostic = result[
                    "confidence_diagnostic"
                ]

                self.assertEqual(
                    diagnostic["ok"],
                    False,
                )
                self.assertTrue(
                    diagnostic["error"],
                )

    def test_logic_verifier_accepts_finite_numeric_string_confidence(
        self,
    ) -> None:
        result = self._run_with_verdict(
            {
                "verdict": "pass",
                "confidence": "0.85",
                "findings": [],
                "reason": "valid probe",
            }
        )

        self.assertEqual(
            result["confidence"],
            0.85,
        )
        self.assertEqual(
            result["mode"],
            "pass",
        )
        self.assertFalse(
            result[
                "fatal_error_detected"
            ]
        )
        self.assertEqual(
            result["findings"],
            [],
        )
        self.assertNotIn(
            "confidence_diagnostic",
            result,
        )


class PhaseScoreHelperFiniteContractRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _helpers():
        import grading_agents

        return {
            "phase4": (
                grading_agents
                ._phase4_cap_layer_score
            ),
            "phase6": (
                grading_agents
                ._phase6_clamp_score
            ),
        }

    def test_phase_score_helpers_accept_finite_values(
        self,
    ) -> None:
        cases = (
            (
                "valid_zero",
                0,
                5,
                0.0,
            ),
            (
                "valid_finite",
                3.25,
                5,
                3.25,
            ),
            (
                "numeric_strings",
                "3.25",
                "5",
                3.25,
            ),
            (
                "negative_score",
                -2,
                5,
                0.0,
            ),
            (
                "above_maximum",
                8,
                5,
                5.0,
            ),
        )

        for helper_name, helper in (
            self._helpers().items()
        ):
            for (
                case_name,
                score,
                maximum,
                expected,
            ) in cases:
                with self.subTest(
                    helper=helper_name,
                    case=case_name,
                ):
                    self.assertEqual(
                        helper(
                            score,
                            maximum,
                        ),
                        expected,
                    )

    def test_phase_score_helpers_reject_invalid_values(
        self,
    ) -> None:
        invalid_values = (
            None,
            True,
            False,
            "invalid",
            [],
            {},
            float("nan"),
            float("inf"),
            float("-inf"),
            10 ** 10000,
        )

        for helper_name, helper in (
            self._helpers().items()
        ):
            for invalid in invalid_values:
                with self.subTest(
                    helper=helper_name,
                    field="score",
                    invalid_type=type(invalid).__name__,
                ):
                    with self.assertRaisesRegex(
                        ValueError,
                        "score",
                    ):
                        helper(
                            invalid,
                            5,
                        )

                with self.subTest(
                    helper=helper_name,
                    field="max_score",
                    invalid_type=type(invalid).__name__,
                ):
                    with self.assertRaisesRegex(
                        ValueError,
                        "max_score",
                    ):
                        helper(
                            3,
                            invalid,
                        )


class PhaseScoreCallerDiagnosticRegressionTest(
    unittest.TestCase
):
    def test_phase4_invalid_score_preserves_grade_with_diagnostic(
        self,
    ) -> None:
        import copy

        import grading_agents

        grade = {
            "max_score": 25,
            "breakdown": [
                {
                    "layer_id": "A",
                    "item": "배경",
                    "score": True,
                    "max": 5,
                    "reason": "base",
                },
            ],
        }
        original_breakdown = copy.deepcopy(
            grade["breakdown"]
        )

        result = (
            grading_agents
            ._phase4_apply_rater_weighted_scoring(
                grade,
                {
                    "total_points": 25,
                    "rater_weights_by_layer": {
                        "A": {
                            "professor": 1.0,
                        },
                    },
                },
                {
                    "raters": [
                        {
                            "id": "professor",
                            "name": "교수",
                            "enabled": True,
                        },
                    ],
                },
            )
        )

        self.assertIs(
            result,
            grade,
        )
        self.assertEqual(
            result["breakdown"],
            original_breakdown,
        )
        self.assertNotIn(
            "rater_results",
            result,
        )

        diagnostic = result[
            "rater_weighted_scoring_diagnostic"
        ]

        self.assertEqual(
            diagnostic["ok"],
            False,
        )
        self.assertEqual(
            diagnostic["fallback"],
            "preserve_existing_grade",
        )
        self.assertIn(
            "must not be bool",
            diagnostic["error"],
        )

    def test_phase6_invalid_gemini_score_preserves_layer_with_diagnostic(
        self,
    ) -> None:
        import grading_agents

        result = (
            grading_agents
            ._phase6_apply_gemini_layer_scores(
                [
                    {
                        "layer_id": "A",
                        "item": "배경",
                        "score": 2.0,
                        "max": 5.0,
                        "reason": "base",
                    },
                ],
                {
                    "ok": True,
                    "parsed": {
                        "layers": [
                            {
                                "layer_id": "A",
                                "score": float(
                                    "nan"
                                ),
                                "reason": (
                                    "invalid probe"
                                ),
                                "evidence": [],
                            },
                        ],
                    },
                },
                {},
            )
        )

        self.assertEqual(
            len(result),
            1,
        )
        self.assertEqual(
            result[0]["score"],
            2.0,
        )
        self.assertNotIn(
            "gemini_semantic_score",
            result[0],
        )
        self.assertEqual(
            result[0][
                "gemini_semantic_score_applied"
            ],
            False,
        )

        diagnostic = result[0][
            "gemini_semantic_diagnostic"
        ]

        self.assertEqual(
            diagnostic["ok"],
            False,
        )
        self.assertEqual(
            diagnostic["fallback"],
            "preserve_base_layer_score",
        )
        self.assertIn(
            "must be finite",
            diagnostic["error"],
        )


class TelegramSummaryFallbackRegressionTest(
    unittest.TestCase
):
    @staticmethod
    def _grade():
        return {
            "total_score": 10.0,
            "max_score": 25.0,
            "score_range": "10~10",
            "breakdown": [],
            "summary": "기존 요약",
        }

    def test_telegram_summary_disabled_returns_none(
        self,
    ) -> None:
        import os

        import grade_output_summarizer

        with patch.dict(
            os.environ,
            {
                "GRADE_OUTPUT_LLM_SUMMARY": (
                    "off"
                ),
            },
            clear=False,
        ):
            result = (
                grade_output_summarizer
                .summarize_grade_for_telegram(
                    self._grade(),
                    lambda prompt: "{}",
                )
            )

        self.assertIsNone(result)

    def test_telegram_summary_unavailable_callable_returns_none(
        self,
    ) -> None:
        import os

        import grade_output_summarizer

        with patch.dict(
            os.environ,
            {
                "GRADE_OUTPUT_LLM_SUMMARY": (
                    "1"
                ),
            },
            clear=False,
        ):
            result = (
                grade_output_summarizer
                .summarize_grade_for_telegram(
                    self._grade(),
                    None,
                )
            )

        self.assertIsNone(result)

    def test_telegram_summary_exception_uses_deterministic_fallback(
        self,
    ) -> None:
        import os

        import grade_output_summarizer

        def fail_summary(
            prompt,
        ):
            raise RuntimeError(
                "simulated summary failure"
            )

        with patch.dict(
            os.environ,
            {
                "GRADE_OUTPUT_LLM_SUMMARY": (
                    "1"
                ),
            },
            clear=False,
        ):
            failed_result = (
                grade_output_summarizer
                .summarize_grade_for_telegram(
                    self._grade(),
                    fail_summary,
                )
            )
            malformed_result = (
                grade_output_summarizer
                .summarize_grade_for_telegram(
                    self._grade(),
                    lambda prompt: (
                        "not valid json"
                    ),
                )
            )

        self.assertIsInstance(
            failed_result,
            str,
        )
        self.assertTrue(
            failed_result.strip(),
        )
        self.assertEqual(
            failed_result,
            malformed_result,
        )

    def test_telegram_summary_object_response_returns_text(
        self,
    ) -> None:
        import os

        import grade_output_summarizer

        with patch.dict(
            os.environ,
            {
                "GRADE_OUTPUT_LLM_SUMMARY": (
                    "1"
                ),
            },
            clear=False,
        ):
            result = (
                grade_output_summarizer
                .summarize_grade_for_telegram(
                    self._grade(),
                    lambda prompt: "{}",
                )
            )

        self.assertIsInstance(
            result,
            str,
        )
        self.assertTrue(
            result.strip(),
        )

class CoverageWarnModeScoreFlowRegressionTest(
    unittest.TestCase
):
    def test_warn_candidate_does_not_mutate_score(
        self,
    ) -> None:
        from unittest.mock import patch

        import question_type_coverage_score_adjuster as adjuster

        grade = {
            "total_score": 1.02,
            "final_total_score": 1.02,
            "max_score": 25.0,
            "score_range": "0.5~1.5",
        }

        decision = {
            "mode": "warn",
            "original_score": 1.02,
            "adjusted_score": 0.27,
            "recommended_penalty": 0.75,
            "applied": False,
        }

        with patch.object(
            adjuster,
            (
                "evaluate_question_type_coverage_"
                "score_adjustment"
            ),
            return_value=decision,
        ):
            result = (
                adjuster
                .apply_question_type_coverage_score_adjustment(
                    grade
                )
            )

        adjustment = result[
            "question_type_coverage_score_adjustment"
        ]

        self.assertEqual(
            result["total_score"],
            1.02,
        )
        self.assertEqual(
            result["final_total_score"],
            1.02,
        )
        self.assertEqual(
            result["score_range"],
            "0.5~1.5",
        )
        self.assertFalse(
            adjustment["applied"]
        )
        self.assertNotEqual(
            adjustment.get(
                "score_flow_applied"
            ),
            True,
        )
        self.assertNotIn(
            (
                "pre_question_type_coverage_"
                "total_score"
            ),
            result,
        )

    def test_ceiling_ignores_warn_candidate(
        self,
    ) -> None:
        from difficulty_score_ceiling import (
            _prefer_question_type_adjusted_score,
        )

        score, applied = (
            _prefer_question_type_adjusted_score(
                {
                    (
                        "question_type_coverage_"
                        "score_adjustment"
                    ): {
                        "mode": "warn",
                        "applied": False,
                        "adjusted_score": 0.27,
                    }
                },
                1.02,
            )
        )

        self.assertEqual(
            score,
            1.02,
        )
        self.assertFalse(
            applied
        )

    def test_fatal_without_numeric_cap_has_normal_range(
        self,
    ) -> None:
        from grade_score_reconciler import (
            _apply_numeric_flags,
        )

        result = _apply_numeric_flags(
            {
                "total_score": 1.02,
                "max_score": 25.0,
                "logic_check_evaluation": {
                    "fatal_error_detected": True,
                    "mode": "fatal",
                },
                "difficulty_ceiling_evaluation": {
                    "mode": "strict",
                    "recommended_cap": 10.0,
                    "capped_score": 1.02,
                    "cap_applied": False,
                },
                "explicit_requirement_cap_evaluation": {
                    "triggered": False,
                    "applied": False,
                },
            }
        )

        self.assertEqual(
            result["total_score"],
            1.02,
        )
        self.assertEqual(
            result["final_total_score"],
            1.02,
        )
        self.assertEqual(
            result["score_range"],
            "0.5~1.5",
        )
        self.assertNotIn(
            "cap 적용",
            result["score_range"],
        )

class FinalBindingCapRegressionTest(
    unittest.TestCase
):
    def test_logic_fatal_without_applied_cap_is_not_binding(
        self,
    ) -> None:
        from grade_score_reconciler import (
            _apply_numeric_flags,
        )

        result = _apply_numeric_flags(
            {
                "total_score": 1.02,
                "max_score": 25.0,
                "logic_check_evaluation": {
                    "fatal_error_detected": True,
                    "mode": "fatal",
                },
                "difficulty_ceiling_evaluation": {
                    "mode": "strict",
                    "recommended_cap": 10.0,
                    "capped_score": 1.02,
                    "cap_applied": False,
                },
                "explicit_requirement_cap_evaluation": {
                    "triggered": False,
                    "applied": False,
                },
            }
        )

        self.assertEqual(
            result["total_score"],
            1.02,
        )
        self.assertEqual(
            result["final_total_score"],
            1.02,
        )
        self.assertEqual(
            result["score_range"],
            "0.5~1.5",
        )
        self.assertNotIn(
            "cap 적용",
            result["score_range"],
        )

    def test_applied_difficulty_cap_is_binding(
        self,
    ) -> None:
        from grade_score_reconciler import (
            _apply_numeric_flags,
        )

        result = _apply_numeric_flags(
            {
                "total_score": 10.0,
                "max_score": 25.0,
                "difficulty_ceiling_evaluation": {
                    "mode": "strict",
                    "recommended_cap": 10.0,
                    "capped_score": 10.0,
                    "cap_applied": True,
                },
            }
        )

        self.assertEqual(
            result["score_range"],
            "10점 cap 적용",
        )

    def test_applied_nonbinding_upper_cap_uses_normal_range(
        self,
    ) -> None:
        from grade_score_reconciler import (
            _apply_numeric_flags,
        )

        result = _apply_numeric_flags(
            {
                "total_score": 8.0,
                "max_score": 25.0,
                "difficulty_ceiling_evaluation": {
                    "mode": "strict",
                    "recommended_cap": 10.0,
                    "capped_score": 10.0,
                    "cap_applied": True,
                },
            }
        )

        self.assertEqual(
            result["score_range"],
            "7.5~8.5",
        )
        self.assertNotIn(
            "cap 적용",
            result["score_range"],
        )

    def test_bot_fallback_does_not_claim_unapplied_cap(
        self,
    ) -> None:
        from unittest.mock import patch

        import bot

        grade = {
            "total_score": 1.02,
            "max_score": 25.0,
            "score_range": "0.5~1.5",
            "summary": "핵심 이론 오류가 있습니다.",
            "rater_results": [
                {
                    "rater_name": "채점자",
                    "total_score": 1.02,
                    "max_score": 25.0,
                }
            ],
            "logic_check_evaluation": {
                "fatal_error_detected": True,
                "mode": "fatal",
            },
            "difficulty_ceiling_evaluation": {
                "recommended_cap": 10.0,
                "capped_score": 1.02,
                "cap_applied": False,
            },
        }

        with patch.object(
            bot,
            "summarize_grade_for_telegram",
            return_value=None,
        ):
            text = bot.format_result(
                grade
            )

        self.assertNotIn(
            "cap을 우선 적용",
            text,
        )
        self.assertNotIn(
            "실제 적용된 ceiling",
            text,
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
