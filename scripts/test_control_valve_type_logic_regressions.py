from __future__ import annotations

import os

import json
import copy
import sys
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from question_type_taxonomy import detect_question_type_from_text
from question_type_router import (
    detect_question_type,
    load_question_type_profile,
)
from grading_identity import (
    NORMALIZATION_VERSION,
    build_grading_identity,
    normalize_grading_text,
)
from grading_agents import (
    _phase3_extract_answer_text,
    _phase3_extract_question_text,
    _phase3_load_fact_anchor_bank,
    _phase3_select_fact_anchors,
)
from logic_check_evaluator import (
    _logic_layer_score_snapshot,
    attach_logic_check_to_grade,
)
from logic_llm_verifier import (
    _build_logic_prompt,
    extract_logic_evidence_candidates,
    load_logic_check_profile,
)
from semantic_question_type_postprocess import ensure_question_type_coverage


TARGET_TOPIC_ID = (
    "control_valve_fluid_forces_unbalance_friction_"
    "actuator_sizing_fail_safe"
)

TARGET_QUESTION = (
    "공압식 밸브 선정시 밸브의 불평형력, 마찰력 개념 설명.\n"
    "Fail safe 동작 구현을 위한 Spring 설계 기준 제시"
)

REAL_COMPARE_SELECTION_QUESTION = (
    "공압식 액추에이터와 전동식 액추에이터를 "
    "구조, 장단점, Fail-Safe 성능 및 적용 조건에 따라 "
    "비교하고 적합한 방식을 선정하시오."
)

EXPECTED_TYPE = "PRINCIPLE_INTERPRETATION"
COMPARE_TYPE = "COMPARE_SELECTION"

NEW_FATAL_ID = "control_valve_fto_ftc_fail_action_conflation"

LOGIC_PROFILE_PATH = (
    ROOT
    / "rubrics"
    / "topic_packs"
    / TARGET_TOPIC_ID
    / "logic_check.json"
)


class ControlValveQuestionTypeRegressionTests(unittest.TestCase):
    def test_selection_context_does_not_override_demand_verbs(self) -> None:
        actual = detect_question_type_from_text(TARGET_QUESTION)

        self.assertEqual(
            actual,
            EXPECTED_TYPE,
            (
                "'선정시'는 적용 문맥일 뿐이다. "
                "'개념 설명'과 '설계 기준 제시'라는 요구동사가 "
                "PRINCIPLE_INTERPRETATION보다 우선되어야 한다."
            ),
        )


    def test_phase9_router_uses_principle_interpretation(self) -> None:
        result = detect_question_type(TARGET_QUESTION)
        primary = result.get("primary_type") or {}

        self.assertEqual(
            primary.get("id"),
            EXPECTED_TYPE,
            (
                "Phase 9 must consume the V2 dict profile "
                "and follow the actual demand verbs."
            ),
        )

    def test_real_compare_and_selection_question_remains_compare(self) -> None:
        actual = detect_question_type_from_text(
            REAL_COMPARE_SELECTION_QUESTION
        )

        self.assertEqual(actual, COMPARE_TYPE)

    def test_semantic_compare_is_canonicalized_by_question_demand(self) -> None:
        semantic_result = {
            "question_type": COMPARE_TYPE,
            "question_type_coverage": {
                "question_type": COMPARE_TYPE,
                "source": "semantic_grader",
                "extraction_confidence": "high",
                "requirements": [
                    {
                        "id": "R1",
                        "text": "불평형력과 마찰력의 개념 설명",
                        "status": "present",
                    },
                    {
                        "id": "R2",
                        "text": "Fail-Safe 스프링 설계 기준 제시",
                        "status": "present",
                    },
                ],
            },
        }

        normalized = ensure_question_type_coverage(
            semantic_result,
            question_text=TARGET_QUESTION,
            existing_question_type=EXPECTED_TYPE,
        )

        coverage = normalized.get("question_type_coverage") or {}

        self.assertEqual(
            coverage.get("question_type"),
            EXPECTED_TYPE,
            (
                "Semantic grader가 COMPARE_SELECTION을 반환해도 "
                "실제 문제 요구동사와 canonical type 신호가 "
                "PRINCIPLE_INTERPRETATION이면 이를 보존해야 한다."
            ),
        )

        self.assertEqual(
            normalized.get("question_type"),
            EXPECTED_TYPE,
        )


class ControlValveLogicProfileRegressionTests(unittest.TestCase):
    def test_fto_ftc_fail_action_conflation_fatal_contract_exists(self) -> None:
        self.assertTrue(
            LOGIC_PROFILE_PATH.is_file(),
            f"Logic profile not found: {LOGIC_PROFILE_PATH}",
        )

        profile = json.loads(
            LOGIC_PROFILE_PATH.read_text(encoding="utf-8")
        )

        serialized = json.dumps(
            profile,
            ensure_ascii=False,
            sort_keys=True,
        )

        self.assertIn(
            NEW_FATAL_ID,
            serialized,
            (
                "FTO/FTC를 Fail-to-Open/Fail-to-Close로 정의하는 "
                "오류를 검출하는 fatal contract가 필요하다."
            ),
        )


class ControlValveFactRoutingRegressionTests(
    unittest.TestCase
):
    TOPIC_ID = (
        "control_valve_fluid_forces_unbalance_friction_"
        "actuator_sizing_fail_safe"
    )

    SESSION_DIR = Path(
        "data/sessions/20260715_133052_5960502198"
    )

    def test_generated_fact_topic_has_runtime_routing_metadata(
        self,
    ) -> None:
        bank = json.loads(
            Path(
                "rubrics/generated/"
                "fact_anchors.generated.json"
            ).read_text(encoding="utf-8")
        )

        topic = next(
            item
            for item in bank.get("topics", [])
            if item.get("topic_id") == self.TOPIC_ID
        )

        self.assertTrue(topic.get("triggers"))
        self.assertTrue(topic.get("aliases"))
        self.assertEqual(
            len(topic.get("anchors") or []),
            22,
        )

        trigger_text = json.dumps(
            topic.get("triggers"),
            ensure_ascii=False,
        )

        self.assertIn("불평형력", trigger_text)
        self.assertIn("마찰력", trigger_text)

        for anchor in topic.get("anchors") or []:
            self.assertTrue(anchor.get("expected"))
            self.assertIsInstance(
                anchor.get("core_terms"),
                list,
            )

    def test_markdown_session_input_is_split_correctly(
        self,
    ) -> None:
        raw_text = (
            self.SESSION_DIR / "input.txt"
        ).read_text(
            encoding="utf-8",
            errors="replace",
        )

        question = _phase3_extract_question_text(
            raw_text
        )
        answer = _phase3_extract_answer_text(
            raw_text
        )

        self.assertEqual(
            question,
            TARGET_QUESTION,
        )
        self.assertTrue(answer.startswith("## 1."))
        self.assertNotEqual(question, answer)
        self.assertLess(len(question), 100)
        self.assertGreater(len(answer), 3000)

    def test_generated_fact_bank_selects_force_topic(
        self,
    ) -> None:
        raw_text = (
            self.SESSION_DIR / "input.txt"
        ).read_text(
            encoding="utf-8",
            errors="replace",
        )

        subject_rubric = json.loads(
            (
                self.SESSION_DIR
                / "subject_rubric_snapshot.json"
            ).read_text(encoding="utf-8")
        )

        question = _phase3_extract_question_text(
            raw_text
        )
        answer = _phase3_extract_answer_text(
            raw_text
        )

        with mock.patch.dict(
            os.environ,
            {"RUBRIC_BANK_MODE": "generated"},
        ):
            bank = _phase3_load_fact_anchor_bank(
                subject_rubric
            )
            anchors = _phase3_select_fact_anchors(
                question,
                answer,
                subject_rubric,
            )

        self.assertGreater(
            len(bank.get("topics") or []),
            55,
        )
        self.assertEqual(len(anchors), 22)

        topic_ids = {
            anchor.get("topic_id")
            for anchor in anchors
            if isinstance(anchor, dict)
        }

        self.assertEqual(
            topic_ids,
            {self.TOPIC_ID},
        )

        anchor_ids = {
            anchor.get("id")
            for anchor in anchors
            if isinstance(anchor, dict)
        }

        self.assertIn(
            "control_valve_unbalance_force_effective_area_approximation",
            anchor_ids,
        )
        self.assertIn(
            "control_valve_friction_opposes_motion_not_actuator",
            anchor_ids,
        )
        self.assertIn(
            "control_valve_spring_preload_rate_travel_force",
            anchor_ids,
        )

    def test_logic_candidates_cover_confirmed_errors(
        self,
    ) -> None:
        answer = """
        F.T.O. (Fail to Open)는 공기원 차단 시 열린다.
        F.T.C. (Fail to Close)는 공기원 차단 시 닫힌다.
        마찰력은 항상 구동기 힘 Fa와 반대 방향이다.
        패킹 마찰력은 Fb = C * v로 계산한다.
        Fa + Fs = Fb - F1 + F2이다.
        비상 시 Fs = Fb - F1 + F2이다.
        설계 시 Fs는 (F1 - F2) + Fb보다 크게 한다.
        """

        profile = load_logic_check_profile(
            self.TOPIC_ID
        )

        candidates = (
            extract_logic_evidence_candidates(
                answer,
                profile,
            )
        )

        self.assertGreater(len(candidates), 0)

        evidence = "\n".join(
            str(candidate.get("text") or "")
            for candidate in candidates
            if isinstance(candidate, dict)
        )

        self.assertIn("Fail to Open", evidence)
        self.assertIn("Fail to Close", evidence)
        self.assertIn("항상 구동기 힘", evidence)
        self.assertIn("Fb = C * v", evidence)
        self.assertIn("Fb - F1 + F2", evidence)
        self.assertIn("(F1 - F2) + Fb", evidence)

        prompt = _build_logic_prompt(
            profile,
            candidates,
        )

        self.assertIn(NEW_FATAL_ID, prompt)
        self.assertIn("Fail to Open", prompt)
        self.assertIn("Fb = C * v", prompt)
        self.assertIn("Fb - F1 + F2", prompt)


class ControlValveLogicScoreRegressionTests(
    unittest.TestCase
):
    SESSION_GRADE = Path(
        "data/sessions/20260715_133052_5960502198/"
        "grade.json"
    )

    TOPIC_ID = (
        "control_valve_fluid_forces_unbalance_friction_"
        "actuator_sizing_fail_safe"
    )

    def _fatal_logic_result(self) -> dict:
        return {
            "applicable": True,
            "topic_id": self.TOPIC_ID,
            "mode": "fatal",
            "verdict": "fatal",
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": (
                        "control_valve_fto_ftc_"
                        "fail_action_conflation"
                    ),
                    "severity": "fatal",
                    "message": (
                        "FTO/FTC를 fail action으로 "
                        "잘못 정의했다."
                    ),
                }
            ],
            "next_practice_points": [],
            "score_policy": {
                "theory_core_fatal_error": True,
                "status": "provisional",
                "scope": "theory_core_topic_profile",
                "score_effect": "diagnostic_only",
                "direct_score_application": False,
                "layer_caps": {},
                "recommended_ceiling": None,
                "direct_d_e_effect": "none",
            },
        }

    def test_logic_fatal_is_diagnostic_only_and_preserves_scores(
        self,
    ) -> None:
        grade = json.loads(
            self.SESSION_GRADE.read_text(
                encoding="utf-8"
            )
        )

        before_layers = (
            _logic_layer_score_snapshot(
                grade
            )
        )

        numeric_keys = [
            "total_score",
            "final_total_score",
            "score_range",
            "official_pass_met",
            "practical_target_met",
            "average_target_met",
            "high_score_met",
        ]

        before_numeric = {
            key: copy.deepcopy(
                grade.get(key)
            )
            for key in numeric_keys
        }

        with mock.patch(
            "logic_check_evaluator."
            "evaluate_logic_checks",
            return_value=self._fatal_logic_result(),
        ):
            adjusted = (
                attach_logic_check_to_grade(
                    copy.deepcopy(grade),
                    "synthetic answer",
                )
            )

        self.assertEqual(
            _logic_layer_score_snapshot(
                adjusted
            ),
            before_layers,
        )

        for key, expected in (
            before_numeric.items()
        ):
            self.assertEqual(
                adjusted.get(key),
                expected,
                key,
            )

        metadata = adjusted.get(
            "logic_score_adjustment"
        ) or {}

        self.assertFalse(
            metadata.get("applied")
        )
        self.assertEqual(
            metadata.get("policy"),
            "diagnostic_only",
        )
        self.assertFalse(
            metadata.get(
                "direct_score_application"
            )
        )
        self.assertEqual(
            adjusted.get(
                "grade_confidence"
            ),
            "low",
        )
        self.assertEqual(
            adjusted.get(
                "logic_trust_status"
            ),
            "limited",
        )

    def test_nonfatal_logic_does_not_change_scores(
        self,
    ) -> None:
        grade = json.loads(
            self.SESSION_GRADE.read_text(
                encoding="utf-8"
            )
        )

        before = _logic_layer_score_snapshot(
            grade
        )
        before_total = grade.get(
            "total_score"
        )

        nonfatal = {
            "applicable": True,
            "topic_id": self.TOPIC_ID,
            "mode": "pass",
            "verdict": "pass",
            "fatal_error_detected": False,
            "findings": [],
            "next_practice_points": [],
            "score_policy": {
                "theory_core_fatal_error": False,
                "recommended_ceiling": None,
            },
        }

        with mock.patch(
            "logic_check_evaluator."
            "evaluate_logic_checks",
            return_value=nonfatal,
        ):
            adjusted = (
                attach_logic_check_to_grade(
                    copy.deepcopy(grade),
                    "synthetic answer",
                )
            )

        after = _logic_layer_score_snapshot(
            adjusted
        )

        self.assertEqual(after, before)
        self.assertEqual(
            adjusted.get("total_score"),
            before_total,
        )

        metadata = adjusted.get(
            "logic_score_adjustment"
        ) or {}

        self.assertFalse(
            metadata.get("applied")
        )


    def test_unscoped_fatal_does_not_change_scores(
        self,
    ) -> None:
        grade = json.loads(
            self.SESSION_GRADE.read_text(
                encoding="utf-8"
            )
        )

        before = _logic_layer_score_snapshot(
            grade
        )
        before_total = grade.get(
            "total_score"
        )

        unscoped = {
            "applicable": True,
            "topic_id": "cv_valve_flow_coefficient",
            "mode": "fatal",
            "verdict": "fatal",
            "fatal_error_detected": True,
            "findings": [
                {
                    "id": "synthetic_fatal",
                    "severity": "fatal",
                    "message": "synthetic fatal",
                }
            ],
            "next_practice_points": [],
            "score_policy": {
                "theory_core_fatal_error": True,
                "recommended_ceiling": 10.0,
                "scope": "legacy_logic_check",
                "score_effect": "none",
                "layer_caps": {},
            },
        }

        with mock.patch(
            "logic_check_evaluator."
            "evaluate_logic_checks",
            return_value=unscoped,
        ):
            adjusted = (
                attach_logic_check_to_grade(
                    copy.deepcopy(grade),
                    "synthetic answer",
                )
            )

        after = _logic_layer_score_snapshot(
            adjusted
        )

        self.assertEqual(after, before)
        self.assertEqual(
            adjusted.get("total_score"),
            before_total,
        )
        self.assertEqual(
            adjusted.get("final_total_score"),
            grade.get("final_total_score"),
        )

        metadata = adjusted.get(
            "logic_score_adjustment"
        ) or {}

        self.assertFalse(
            metadata.get("applied")
        )

    def test_profile_contains_scoped_fatal_score_policy(
        self,
    ) -> None:
        profile = load_logic_check_profile(
            self.TOPIC_ID
        )

        score_policy = profile.get(
            "score_policy"
        ) or {}

        self.assertEqual(
            score_policy.get("status"),
            "provisional",
        )
        self.assertEqual(
            score_policy.get("scope"),
            "theory_core_topic_profile",
        )
        self.assertEqual(
            score_policy.get(
                "score_effect"
            ),
            "diagnostic_only",
        )
        self.assertFalse(
            score_policy.get(
                "direct_score_application"
            )
        )
        self.assertEqual(
            score_policy.get(
                "fatal_layer_caps"
            ),
            {},
        )
        self.assertIsNone(
            score_policy.get(
                "recommended_ceiling"
            )
        )
        self.assertEqual(
            score_policy.get(
                "direct_d_e_effect"
            ),
            "none",
        )

    def test_diagnostic_only_policy_has_no_numeric_ceiling(
        self,
    ) -> None:
        grade = json.loads(
            self.SESSION_GRADE.read_text(
                encoding="utf-8"
            )
        )

        with mock.patch(
            "logic_check_evaluator."
            "evaluate_logic_checks",
            return_value=self._fatal_logic_result(),
        ):
            adjusted = (
                attach_logic_check_to_grade(
                    copy.deepcopy(grade),
                    "synthetic answer",
                )
            )

        logic_eval = adjusted.get(
            "logic_check_evaluation"
        ) or {}

        score_policy = logic_eval.get(
            "score_policy"
        ) or {}

        self.assertEqual(
            score_policy.get(
                "score_effect"
            ),
            "diagnostic_only",
        )
        self.assertFalse(
            score_policy.get(
                "direct_score_application"
            )
        )
        self.assertEqual(
            score_policy.get(
                "layer_caps"
            ),
            {},
        )
        self.assertIsNone(
            score_policy.get(
                "recommended_ceiling"
            )
        )
        self.assertEqual(
            adjusted.get("total_score"),
            grade.get("total_score"),
        )
        self.assertEqual(
            adjusted.get(
                "final_total_score"
            ),
            grade.get(
                "final_total_score"
            ),
        )




class GradingIdentityRegressionTests(
    unittest.TestCase
):
    SESSION_DIR = Path(
        "data/sessions/"
        "20260715_133052_5960502198"
    )

    def test_emoji_variation_selector_is_ignored(
        self,
    ) -> None:
        with_selector = (
            build_grading_identity(
                "동일 문제",
                "▶️ 동일 답안",
            )
        )
        without_selector = (
            build_grading_identity(
                "동일 문제",
                "▶ 동일 답안",
            )
        )

        self.assertEqual(
            with_selector.question_hash,
            without_selector.question_hash,
        )
        self.assertEqual(
            with_selector.submission_hash,
            without_selector.submission_hash,
        )

    def test_question_and_submission_hash_scope(
        self,
    ) -> None:
        first = build_grading_identity(
            "문제",
            "답안 A",
        )
        second = build_grading_identity(
            "문제",
            "답안 B",
        )
        whitespace_only = (
            build_grading_identity(
                " 문제 ",
                "\n답안 A\n\n\n",
            )
        )

        self.assertEqual(
            first.question_hash,
            second.question_hash,
        )
        self.assertNotEqual(
            first.submission_hash,
            second.submission_hash,
        )
        self.assertEqual(
            first.submission_hash,
            whitespace_only.submission_hash,
        )
        self.assertEqual(
            first.normalization_version,
            NORMALIZATION_VERSION,
        )
        self.assertEqual(
            len(first.question_hash),
            64,
        )
        self.assertEqual(
            len(first.submission_hash),
            64,
        )

    def test_real_session_uses_final_split_text(
        self,
    ) -> None:
        raw_text = (
            self.SESSION_DIR / "input.txt"
        ).read_text(
            encoding="utf-8",
            errors="replace",
        )

        question = (
            _phase3_extract_question_text(
                raw_text
            )
        )
        answer = (
            _phase3_extract_answer_text(
                raw_text
            )
        )

        identity = build_grading_identity(
            question,
            answer,
        )

        self.assertEqual(
            identity.normalized_question,
            normalize_grading_text(
                question
            ),
        )
        self.assertEqual(
            identity.normalized_answer,
            normalize_grading_text(
                answer
            ),
        )
        self.assertNotEqual(
            identity.question_hash,
            identity.submission_hash,
        )
        self.assertLess(
            len(identity.normalized_question),
            100,
        )
        self.assertGreater(
            len(identity.normalized_answer),
            3000,
        )

        agent_source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"grading_identity": '
            "grading_identity_dict",
            agent_source,
        )
        self.assertIn(
            'session_dir / '
            '"grading_identity.json"',
            agent_source,
        )




class DeterministicQuestionTypeContractTests(
    unittest.TestCase
):
    TARGET_QUESTION = (
        "공압식 밸브 선정시 밸브의 불평형력, "
        "마찰력 개념 설명. Fail safe 동작 구현을 "
        "위한 Spring 설계 기준 제시"
    )

    def test_answer_text_cannot_change_locked_lens(
        self,
    ) -> None:
        profile = (
            load_question_type_profile()
        )

        clean = detect_question_type(
            question_text=(
                self.TARGET_QUESTION
            ),
            answer_text="정확한 답안",
            profile=profile,
        )

        compare_like = (
            detect_question_type(
                question_text=(
                    self.TARGET_QUESTION
                ),
                answer_text=(
                    "두 방식을 비교하고 장단점을 "
                    "선정하여 최적안을 선택한다."
                ),
                profile=profile,
            )
        )

        self.assertEqual(
            (
                clean.get(
                    "primary_type"
                )
                or {}
            ).get("id"),
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            (
                compare_like.get(
                    "primary_type"
                )
                or {}
            ).get("id"),
            "PRINCIPLE_INTERPRETATION",
        )
        self.assertEqual(
            clean.get("confidence"),
            "high",
        )
        self.assertEqual(
            clean.get("status"),
            "locked",
        )
        self.assertTrue(
            clean.get(
                "question_type_locked"
            )
        )
        self.assertEqual(
            clean.get("warning"),
            "",
        )
        self.assertEqual(
            clean.get("source"),
            "deterministic_rule",
        )

        for result in [
            clean,
            compare_like,
        ]:
            for candidate in (
                result.get("candidates")
                or []
            ):
                self.assertEqual(
                    candidate.get(
                        "answer_hits"
                    ),
                    [],
                )

    def test_generic_explanation_is_provisional(
        self,
    ) -> None:
        result = detect_question_type(
            question_text=(
                "제어밸브에 대하여 설명하시오."
            ),
            answer_text=(
                "비교, 장단점, 선정이라는 표현이 "
                "답안에 반복된다."
            ),
            profile=(
                load_question_type_profile()
            ),
        )

        self.assertIn(
            result.get("confidence"),
            {
                "medium",
                "low",
            },
        )
        self.assertEqual(
            result.get("status"),
            "provisional",
        )
        self.assertFalse(
            result.get(
                "question_type_locked"
            )
        )
        self.assertEqual(
            result.get("warning"),
            (
                "⚠ 이 문제의 유형 분류는 잠정 상태이며 "
                "확인이 필요합니다"
            ),
        )

    def test_locked_lens_has_later_override_guard(
        self,
    ) -> None:
        agent_source = Path(
            "grading_agents.py"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'question_type_eval.get(\n'
            '            "question_type_locked"',
            agent_source,
        )
        self.assertIn(
            "return (\n"
            "            question_type_eval,\n"
            "            fact_eval,",
            agent_source,
        )
        self.assertNotIn(
            "answer_text=answer_text,\n"
            "            profile=profile,",
            agent_source,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
