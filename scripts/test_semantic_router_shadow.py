from __future__ import annotations

import ast
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import grading_agents
import semantic_router_shadow as srs


BASE_DIR = Path(__file__).resolve().parents[1]


def demand_result(*texts):
    return {
        "version": "question_demand_shadow_v1",
        "shadow": True,
        "enabled": True,
        "status": "ok",
        "ok": True,
        "demands": [
            {"id": f"D{i}", "text": text}
            for i, text in enumerate(texts, start=1)
        ],
    }


def candidate(topic_id, title, score=12):
    return {
        "answer": {
            "topic_id": topic_id,
            "title": title,
        },
        "score": score,
        "question_score": score,
        "match_reasons": [
            f"alias matched: {title}"
        ],
    }


class SemanticRouterShadowUnitTest(unittest.TestCase):
    def test_disabled_by_default_has_zero_llm_dependency(self):
        llm = mock.Mock()
        result = srs.semantic_route_shadow(
            "문제",
            demand_result("요구사항"),
            {"candidates": []},
            llm_call=llm,
            enabled=False,
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "disabled")
        self.assertEqual(result["routing_effect"], "none")
        self.assertTrue(result["legacy_router_authoritative"])
        llm.assert_not_called()

    def test_no_rule_candidates_proposes_general_without_llm(self):
        llm = mock.Mock()
        result = srs.semantic_route_shadow(
            "캐비테이션과 플래싱을 설명하시오.",
            demand_result(
                "캐비테이션 발생 원리",
                "플래싱 발생 원리",
            ),
            {"candidates": []},
            llm_call=llm,
            enabled=True,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["routing_mode"], "GENERAL")
        self.assertFalse(result["llm_called"])
        self.assertEqual(
            result["uncovered_demand_ids"],
            ["D1", "D2"],
        )
        llm.assert_not_called()

    def test_valid_multi_topic_result_is_normalized(self):
        rtd = (
            "rtd_temperature_sensor_principle_"
            "pt100_wiring_compensation"
        )
        tc = (
            "thermocouple_temperature_sensor_"
            "seebeck_reference_junction_compensation"
        )
        rule = {
            "candidates": [
                candidate(rtd, "RTD"),
                candidate(tc, "열전대"),
            ]
        }

        result = srs.semantic_route_shadow(
            "RTD와 열전대를 비교하시오.",
            demand_result("RTD와 열전대의 측정 원리 비교"),
            rule,
            llm_call=lambda _prompt: {
                "routing_mode": "MULTI_TOPIC",
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": rtd,
                        "role": "PRIMARY",
                        "confidence": 0.96,
                    },
                    {
                        "demand_id": "D1",
                        "topic_id": tc,
                        "role": "PRIMARY",
                        "confidence": 0.95,
                    },
                ],
                "uncovered_demand_ids": [],
                "reason": "두 센서를 직접 비교",
            },
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["routing_mode"], "MULTI_TOPIC")
        self.assertEqual(
            set(result["primary_topic_ids"]),
            {rtd, tc},
        )
        self.assertTrue(result["llm_called"])
        self.assertFalse(result["student_answer_used"])

    def test_valid_single_topic_result_is_normalized(self):
        topic = "second_order_lag_response_by_damping_ratio"
        rule = {
            "candidates": [
                candidate(
                    topic,
                    "감쇠비에 따른 2차 시스템",
                    score=3,
                )
            ]
        }

        result = srs.semantic_route_shadow(
            "감쇠비에 따른 시간응답 특성을 설명하시오.",
            demand_result("감쇠비에 따른 시간응답 특성 설명"),
            rule,
            llm_call=lambda _prompt: {
                "routing_mode": "SINGLE_TOPIC",
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": topic,
                        "role": "PRIMARY",
                        "confidence": 0.91,
                    }
                ],
                "uncovered_demand_ids": [],
                "reason": "단일 Topic 소유",
            },
            enabled=True,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["routing_mode"], "SINGLE_TOPIC")
        self.assertEqual(result["primary_topic_ids"], [topic])

    def test_invented_topic_is_rejected_to_safe_fallback(self):
        result = srs.semantic_route_shadow(
            "문제",
            demand_result("요구사항"),
            {
                "candidates": [
                    candidate("allowed_topic", "Allowed")
                ]
            },
            llm_call=lambda _prompt: {
                "routing_mode": "SINGLE_TOPIC",
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": "invented_topic",
                        "role": "PRIMARY",
                        "confidence": 0.9,
                    }
                ],
                "uncovered_demand_ids": [],
                "reason": "",
            },
            enabled=True,
            topic_sheet_dir=Path(tempfile.gettempdir()),
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["routing_effect"], "none")

    def test_multi_topic_requires_two_primary_topics(self):
        result = srs.semantic_route_shadow(
            "문제",
            demand_result("요구사항"),
            {
                "candidates": [
                    candidate("one_topic", "One")
                ]
            },
            llm_call=lambda _prompt: {
                "routing_mode": "MULTI_TOPIC",
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": "one_topic",
                        "role": "PRIMARY",
                        "confidence": 0.9,
                    }
                ],
                "uncovered_demand_ids": [],
                "reason": "",
            },
            enabled=True,
            topic_sheet_dir=Path(tempfile.gettempdir()),
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")

    def test_general_cannot_assign_positive_topic(self):
        result = srs.semantic_route_shadow(
            "문제",
            demand_result("요구사항"),
            {
                "candidates": [
                    candidate("one_topic", "One")
                ]
            },
            llm_call=lambda _prompt: {
                "routing_mode": "GENERAL",
                "demand_mappings": [
                    {
                        "demand_id": "D1",
                        "topic_id": "one_topic",
                        "role": "SUPPORTING",
                        "confidence": 0.7,
                    }
                ],
                "uncovered_demand_ids": [],
                "reason": "",
            },
            enabled=True,
            topic_sheet_dir=Path(tempfile.gettempdir()),
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "fallback")


class SemanticCatalogTest(unittest.TestCase):
    def test_catalog_uses_only_rule_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "topic_a.md").write_text(
                "# Topic A\n\n"
                "## 2. 출제 의도\nA 의도\n\n"
                "## 포함 범위\nA positive\n\n"
                "## 제외 범위\nB는 제외\n",
                encoding="utf-8",
            )
            (root / "topic_b.md").write_text(
                "# Topic B\n\n## 포함 범위\nB positive",
                encoding="utf-8",
            )

            catalog = srs.build_candidate_semantic_catalog(
                {
                    "candidates": [
                        candidate("topic_a", "Topic A")
                    ]
                },
                topic_sheet_dir=root,
            )

        self.assertEqual(len(catalog), 1)
        self.assertEqual(catalog[0]["topic_id"], "topic_a")
        self.assertIn("포함 범위", catalog[0]["semantic_excerpt"])
        self.assertNotIn("B positive", catalog[0]["semantic_excerpt"])

    def test_heterogeneous_heading_falls_back_without_invention(self):
        raw = (
            "# Odd Topic\n\n"
            "본문 첫 문단.\n"
            "정형화된 ownership 제목이 없다.\n"
        )
        compact = srs._compact_topic_sheet_semantics(
            raw,
            max_chars=300,
        )
        self.assertIn("Odd Topic", compact)
        self.assertIn("본문 첫 문단", compact)


class Phase10SemanticShadowIsolationTest(unittest.TestCase):
    def test_disabled_semantic_shadow_has_zero_persistence(self):
        fake = {
            "version": srs.SEMANTIC_ROUTER_SHADOW_VERSION,
            "shadow": True,
            "enabled": False,
            "status": "disabled",
            "ok": False,
            "routing_mode": None,
            "candidate_topic_ids": [],
            "demand_mappings": [],
            "uncovered_demand_ids": [],
            "primary_topic_ids": [],
            "supporting_topic_ids": [],
            "reason": "",
            "error": "disabled",
            "llm_called": False,
            "routing_effect": "none",
            "score_effect": "none",
            "student_answer_used": False,
            "legacy_router_authoritative": True,
        }

        with mock.patch(
            "semantic_router_shadow.semantic_route_shadow",
            return_value=fake,
        ), mock.patch.object(
            grading_agents,
            "_phase2_json_write",
        ) as write_mock:
            result = grading_agents._phase10_run_semantic_router_shadow(
                question_text="문제",
                question_demand_result=demand_result("요구사항"),
                rule_result={"candidates": []},
                session_dir=Path("/not/used"),
            )

        self.assertEqual(result["status"], "disabled")
        write_mock.assert_not_called()

    def test_enabled_semantic_shadow_persists_separately(self):
        fake = {
            "version": srs.SEMANTIC_ROUTER_SHADOW_VERSION,
            "shadow": True,
            "enabled": True,
            "status": "ok",
            "ok": True,
            "routing_mode": "GENERAL",
            "candidate_topic_ids": [],
            "demand_mappings": [],
            "uncovered_demand_ids": ["D1"],
            "primary_topic_ids": [],
            "supporting_topic_ids": [],
            "reason": "no candidates",
            "error": "",
            "llm_called": False,
            "routing_effect": "none",
            "score_effect": "none",
            "student_answer_used": False,
            "legacy_router_authoritative": True,
        }

        with tempfile.TemporaryDirectory() as tmp:
            session_dir = Path(tmp)
            with mock.patch(
                "semantic_router_shadow.semantic_route_shadow",
                return_value=fake,
            ):
                result = grading_agents._phase10_run_semantic_router_shadow(
                    question_text="문제",
                    question_demand_result=demand_result("요구사항"),
                    rule_result={"candidates": []},
                    session_dir=session_dir,
                )

            path = session_dir / srs.SEMANTIC_ROUTER_SHADOW_FILE
            self.assertTrue(path.exists())
            persisted = json.loads(
                path.read_text(encoding="utf-8")
            )

        self.assertEqual(result, fake)
        self.assertEqual(persisted, fake)


class StaticIsolationContractTest(unittest.TestCase):
    def test_semantic_module_api_has_no_answer_text(self):
        tree = ast.parse(
            (BASE_DIR / "semantic_router_shadow.py").read_text(
                encoding="utf-8"
            )
        )
        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "semantic_route_shadow"
        )
        arg_names = {
            arg.arg
            for arg in (
                list(fn.args.posonlyargs)
                + list(fn.args.args)
                + list(fn.args.kwonlyargs)
            )
        }
        self.assertNotIn("answer_text", arg_names)
        self.assertIn("question_text", arg_names)
        self.assertIn("rule_result", arg_names)

    def test_phase10_semantic_call_result_is_not_used_for_legacy_return(self):
        tree = ast.parse(
            (BASE_DIR / "grading_agents.py").read_text(
                encoding="utf-8"
            )
        )
        fn = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_phase10_run_model_answer_reference"
        )

        calls = [
            node
            for node in ast.walk(fn)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id
                == "_phase10_run_semantic_router_shadow"
            )
        ]
        self.assertEqual(len(calls), 1)

        parents = {}
        for parent in ast.walk(fn):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent

        parent = parents.get(calls[0])
        self.assertIsInstance(parent, ast.Expr)

        cur = parent
        guarded = False
        while cur in parents:
            cur = parents[cur]
            if isinstance(cur, ast.Try):
                guarded = True
                break

        self.assertTrue(guarded)


if __name__ == "__main__":
    unittest.main(verbosity=2)
