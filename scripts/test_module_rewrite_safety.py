"""Regression checks for mechanical module relocation."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.maintenance.rewrite_module_imports import rewrite


class ModuleRewriteSafetyTests(unittest.TestCase):
    def test_changes_imports_and_patch_targets_without_renaming_data_files(self) -> None:
        original = (
            "from semantic_router_shadow import build_shadow\n"
            "import semantic_router_shadow\n"
            "mock.patch('semantic_router_shadow.build_shadow')\n"
            "ARTIFACT = 'semantic_router_shadow.json'\n"
            "SOURCE = 'semantic_router_shadow.py'\n"
        )
        rewritten = rewrite(
            original, "semantic_router_shadow", "grading.routing.semantic_router_shadow"
        )
        self.assertIn("from grading.routing.semantic_router_shadow import build_shadow", rewritten)
        self.assertIn("import grading.routing.semantic_router_shadow as semantic_router_shadow", rewritten)
        self.assertIn("mock.patch('grading.routing.semantic_router_shadow.build_shadow')", rewritten)
        self.assertIn("ARTIFACT = 'semantic_router_shadow.json'", rewritten)
        self.assertIn("SOURCE = 'grading/routing/semantic_router_shadow.py'", rewritten)


if __name__ == "__main__":
    unittest.main()
