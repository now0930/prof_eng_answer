#!/usr/bin/env python3
from __future__ import annotations

import ast
import unittest
from pathlib import Path
from typing import Any

import grading_agents


ROOT = Path(__file__).resolve().parents[1]
GRADING_AGENTS_PATH = ROOT / "grading_agents.py"


class JsonParserContractRegressionTest(unittest.TestCase):
    def parse(self, raw: Any) -> Any:
        return grading_agents.extract_json(raw)

    def test_valid_object_returns_dict(self) -> None:
        self.assertEqual(
            self.parse('{"score": 10, "result": "ok"}'),
            {
                "score": 10,
                "result": "ok",
            },
        )

    def test_fenced_json_returns_dict(self) -> None:
        self.assertEqual(
            self.parse(
                '```json\n'
                '{"score": 11, "result": "ok"}\n'
                '```'
            ),
            {
                "score": 11,
                "result": "ok",
            },
        )

    def test_uppercase_fenced_json_returns_dict(self) -> None:
        self.assertEqual(
            self.parse(
                '```JSON\n'
                '{"score": 12}\n'
                '```'
            ),
            {
                "score": 12,
            },
        )

    def test_trailing_comma_is_repaired(self) -> None:
        self.assertEqual(
            self.parse('{"score": 21,}'),
            {
                "score": 21,
            },
        )

    def test_missing_closing_brace_is_repaired(self) -> None:
        self.assertEqual(
            self.parse('{"score": 24'),
            {
                "score": 24,
            },
        )

    def test_valid_array_is_preserved_as_list(self) -> None:
        result = self.parse('[{"score": 16}]')

        self.assertIsInstance(result, list)
        self.assertEqual(
            result,
            [
                {
                    "score": 16,
                }
            ],
        )

    def test_non_json_inputs_return_none(self) -> None:
        for raw in (
            "채점 결과를 생성하지 못했습니다.",
            "",
            None,
        ):
            with self.subTest(raw=raw):
                self.assertIsNone(
                    self.parse(raw)
                )

    def test_legacy_pipeline_rejects_non_dict_parser_result(
        self,
    ) -> None:
        text = GRADING_AGENTS_PATH.read_text(
            encoding="utf-8",
        )
        tree = ast.parse(
            text,
            filename=str(GRADING_AGENTS_PATH),
        )

        functions = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_legacy_run_agent_pipeline"
        ]

        self.assertEqual(
            len(functions),
            1,
            "_legacy_run_agent_pipeline must exist exactly once",
        )

        function = functions[0]
        parser_assignment_index: int | None = None
        fallback_if_index: int | None = None

        for index, statement in enumerate(function.body):
            if (
                isinstance(statement, ast.Assign)
                and len(statement.targets) == 1
                and isinstance(
                    statement.targets[0],
                    ast.Name,
                )
                and statement.targets[0].id == "analysis"
                and isinstance(statement.value, ast.Call)
                and isinstance(
                    statement.value.func,
                    ast.Name,
                )
                and statement.value.func.id == "extract_json"
            ):
                parser_assignment_index = index
                continue

            if not isinstance(statement, ast.If):
                continue

            test = statement.test

            if not (
                isinstance(test, ast.UnaryOp)
                and isinstance(test.op, ast.Not)
                and isinstance(test.operand, ast.Call)
                and isinstance(
                    test.operand.func,
                    ast.Name,
                )
                and test.operand.func.id == "isinstance"
                and len(test.operand.args) == 2
                and isinstance(
                    test.operand.args[0],
                    ast.Name,
                )
                and test.operand.args[0].id == "analysis"
                and isinstance(
                    test.operand.args[1],
                    ast.Name,
                )
                and test.operand.args[1].id == "dict"
            ):
                continue

            assigns_fallback = any(
                isinstance(child, ast.Assign)
                and len(child.targets) == 1
                and isinstance(
                    child.targets[0],
                    ast.Name,
                )
                and child.targets[0].id == "analysis"
                and isinstance(child.value, ast.Call)
                and isinstance(
                    child.value.func,
                    ast.Name,
                )
                and child.value.func.id == "fallback_analysis"
                for child in statement.body
            )

            if assigns_fallback:
                fallback_if_index = index
                break

        self.assertIsNotNone(
            parser_assignment_index,
            "pipeline must assign extract_json result to analysis",
        )
        self.assertIsNotNone(
            fallback_if_index,
            "pipeline must replace non-dict analysis with fallback",
        )
        self.assertLess(
            parser_assignment_index,
            fallback_if_index,
            "dict contract check must follow JSON extraction",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
