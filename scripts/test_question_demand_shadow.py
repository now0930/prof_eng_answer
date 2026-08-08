from __future__ import annotations

import ast
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import grading_agents
import question_demand_shadow as qds


BASE_DIR = Path(__file__).resolve().parents[1]


class QuestionDemandShadowUnitTest(unittest.TestCase):
    def test_disabled_by_default_has_no_llm_dependency(self):
        with mock.patch.dict(
            os.environ,
            {"QUESTION_DEMAND_SHADOW_ENABLED": ""},
            clear=False,
        ):
            result = qds.extract_question_demands(
                "RTD와 열전대를 비교하시오."
            )

        self.assertFalse(result["ok"])
        self.assertFalse(result["enabled"])
        self.assertEqual(result["status"], "disabled")
        self.assertEqual(result["demands"], [])
        self.assertEqual(result["routing_effect"], "none")
        self.assertEqual(result["score_effect"], "none")
        self.assertFalse(result["student_answer_used"])
        self.assertFalse(result["topic_selection_performed"])

    def test_valid_llm_result_is_normalized_and_deduplicated(self):
        def fake_llm(prompt):
            self.assertIn("RTD와 열전대", prompt)
            return {
                "demands": [
                    {
                        "id": "anything",
                        "text": "RTD 측정원리",
                        "topic_id": "must_not_survive",
                    },
                    {
                        "id": "anything2",
                        "text": "열전대 측정원리",
                    },
                    {
                        "id": "anything3",
                        "text": "RTD 측정원리",
                    },
                ]
            }

        result = qds.extract_question_demands(
            "RTD와 열전대의 측정원리를 비교하시오.",
            llm_call=fake_llm,
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            result["demands"],
            [
                {"id": "D1", "text": "RTD 측정원리"},
                {"id": "D2", "text": "열전대 측정원리"},
            ],
        )
        self.assertNotIn(
            "topic_id",
            result["demands"][0],
        )
        self.assertFalse(
            result["topic_selection_performed"]
        )

    def test_llm_exception_returns_safe_shadow_fallback(self):
        def fail_llm(_prompt):
            raise RuntimeError("simulated shadow failure")

        result = qds.extract_question_demands(
            "PID 튜닝 순서를 설명하시오.",
            llm_call=fail_llm,
            enabled=True,
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["demands"], [])
        self.assertEqual(result["routing_effect"], "none")
        self.assertEqual(result["score_effect"], "none")

    def test_malformed_payload_returns_safe_shadow_fallback(self):
        result = qds.extract_question_demands(
            "2차 시스템을 설명하시오.",
            llm_call=lambda _prompt: {"not_demands": []},
            enabled=True,
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["demand_count"], 0)

    def test_max_demand_limit_is_enforced(self):
        payload = {
            "demands": [
                {"text": f"요구사항 {i}"}
                for i in range(20)
            ]
        }

        result = qds.extract_question_demands(
            "복합 문제",
            llm_call=lambda _prompt: payload,
            max_demands=4,
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["demand_count"], 4)


class QuestionDemandShadowPersistenceTest(unittest.TestCase):
    def test_phase10_shadow_disabled_has_zero_persistence_side_effect(self):
        with mock.patch(
            "question_demand_shadow.extract_question_demands",
            return_value={
                "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
                "shadow": True,
                "enabled": False,
                "status": "disabled",
                "ok": False,
                "mode": "question_demand_decomposition_only",
                "demands": [],
                "demand_count": 0,
                "error": "disabled",
                "routing_effect": "none",
                "score_effect": "none",
                "student_answer_used": False,
                "topic_selection_performed": False,
            },
        ), mock.patch.object(
            grading_agents,
            "_phase2_json_write",
        ) as write_mock:
            result = (
                grading_agents
                ._phase10_run_question_demand_shadow(
                    "문제",
                    Path("/not/used"),
                )
            )

        self.assertEqual(result["status"], "disabled")
        write_mock.assert_not_called()

    def test_phase10_shadow_persists_separately(self):
        fake = {
            "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
            "shadow": True,
            "enabled": True,
            "status": "ok",
            "ok": True,
            "mode": "question_demand_decomposition_only",
            "demands": [
                {"id": "D1", "text": "측정원리 설명"}
            ],
            "demand_count": 1,
            "error": "",
            "routing_effect": "none",
            "score_effect": "none",
            "student_answer_used": False,
            "topic_selection_performed": False,
        }

        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            with mock.patch(
                "question_demand_shadow.extract_question_demands",
                return_value=fake,
            ):
                result = (
                    grading_agents
                    ._phase10_run_question_demand_shadow(
                        "센서의 측정원리를 설명하시오.",
                        session_dir,
                    )
                )

            persisted = (
                session_dir
                / qds.QUESTION_DEMAND_SHADOW_FILE
            )
            self.assertTrue(persisted.exists())
            self.assertEqual(result, fake)
            self.assertFalse(
                (session_dir / "model_answer_reference.json")
                .exists()
            )

    def test_persistence_failure_does_not_raise(self):
        with mock.patch(
            "question_demand_shadow.extract_question_demands",
            return_value={
                "version": qds.QUESTION_DEMAND_SHADOW_VERSION,
                "shadow": True,
                "enabled": True,
                "status": "ok",
                "ok": True,
                "mode": "question_demand_decomposition_only",
                "demands": [
                    {"id": "D1", "text": "요구사항"}
                ],
                "demand_count": 1,
                "error": "",
                "routing_effect": "none",
                "score_effect": "none",
                "student_answer_used": False,
                "topic_selection_performed": False,
            },
        ), mock.patch.object(
            grading_agents,
            "_phase2_json_write",
            side_effect=OSError("simulated write failure"),
        ):
            result = (
                grading_agents
                ._phase10_run_question_demand_shadow(
                    "문제",
                    Path("/not/used"),
                )
            )

        self.assertIsInstance(result, dict)
        self.assertEqual(result["routing_effect"], "none")


class Phase10IsolationStaticContractTest(unittest.TestCase):
    def test_shadow_call_is_guarded_and_result_is_not_assigned(self):
        path = BASE_DIR / "grading_agents.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))

        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name
            == "_phase10_run_model_answer_reference"
        )

        shadow_calls = []
        for node in ast.walk(fn):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id
                == "_phase10_run_question_demand_shadow"
            ):
                shadow_calls.append(node)

        self.assertEqual(len(shadow_calls), 1)

        call = shadow_calls[0]

        parents = {}
        for parent in ast.walk(fn):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent

        parent = parents.get(call)
        self.assertIsInstance(parent, ast.Expr)

        cur = parent
        guarded = False
        while cur in parents:
            cur = parents[cur]
            if isinstance(cur, ast.Try):
                guarded = True
                break

        self.assertTrue(guarded)

    def test_shadow_module_has_no_answer_text_parameter(self):
        tree = ast.parse(
            (BASE_DIR / "question_demand_shadow.py")
            .read_text(encoding="utf-8")
        )

        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "extract_question_demands"
        )
        arg_names = {
            arg.arg
            for arg in (
                list(fn.args.posonlyargs)
                + list(fn.args.args)
                + list(fn.args.kwonlyargs)
            )
        }

        self.assertEqual(
            arg_names,
            {
                "question_text",
                "llm_call",
                "max_demands",
                "enabled",
            },
        )
        self.assertNotIn("answer_text", arg_names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
