from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "logic_llm_verifier.py"


def _key(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


class Stage22OllamaNumCtxContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = VERIFIER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_num_ctx_is_environment_backed_with_8192_default(self) -> None:
        expressions: list[str] = []
        for node in self.tree.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Name)
                and target.id == "LOGIC_LLM_NUM_CTX"
                for target in targets
            ):
                expressions.append(ast.unparse(node.value))

        self.assertEqual(
            expressions,
            ["int(os.getenv('LOGIC_LLM_VERIFIER_NUM_CTX', '8192'))"],
        )

    def test_request_options_forward_num_ctx_without_changing_sampling(self) -> None:
        options: list[dict[str, str]] = []

        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Dict):
                continue

            mapping: dict[str, ast.AST] = {}
            for key, value in zip(node.keys, node.values):
                name = _key(key)
                if name is not None:
                    mapping[name] = value

            if not {"model", "messages", "stream", "options"}.issubset(mapping):
                continue

            option_node = mapping["options"]
            self.assertIsInstance(option_node, ast.Dict)
            option_map = {
                _key(key): ast.unparse(value)
                for key, value in zip(option_node.keys, option_node.values)
            }
            options.append(option_map)

        self.assertEqual(len(options), 1)
        self.assertEqual(options[0].get("temperature"), "0")
        self.assertEqual(options[0].get("top_p"), "0.1")
        self.assertEqual(options[0].get("num_ctx"), "LOGIC_LLM_NUM_CTX")

    def test_existing_90_second_timeout_contract_is_unchanged(self) -> None:
        expressions: list[str] = []

        for node in self.tree.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(
                isinstance(target, ast.Name)
                and target.id == "LOGIC_LLM_TIMEOUT"
                for target in targets
            ):
                expressions.append(ast.unparse(node.value))

        self.assertEqual(
            expressions,
            ["int(os.getenv('LOGIC_LLM_VERIFIER_TIMEOUT', '90'))"],
        )


if __name__ == "__main__":
    unittest.main()
