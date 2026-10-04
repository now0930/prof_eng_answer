"""Keep the public entry points separate from implementation modules."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PUBLIC_ENTRYPOINTS = {"bot.py", "grading_agents.py"}
DOMAIN_PACKAGES = (
    "coverage_feedback",
    "evidence",
    "providers",
    "quality",
    "routing",
    "rubrics",
    "scoring",
)


class PythonLayoutContractTests(unittest.TestCase):
    def test_root_contains_only_public_python_entrypoints(self) -> None:
        root_modules = {path.name for path in ROOT.glob("*.py")}
        self.assertEqual(root_modules, PUBLIC_ENTRYPOINTS)

    def test_domain_packages_are_importable(self) -> None:
        for name in DOMAIN_PACKAGES:
            with self.subTest(package=name):
                package_dir = ROOT / "grading" / name
                self.assertTrue((package_dir / "__init__.py").is_file())
                self.assertIsNotNone(importlib.util.find_spec(f"grading.{name}"))

    def test_maintenance_tools_do_not_live_at_root(self) -> None:
        for name in ("apply_readme_update.py", "fix_encoding.py"):
            with self.subTest(tool=name):
                self.assertTrue((ROOT / "scripts" / "maintenance" / name).is_file())


if __name__ == "__main__":
    unittest.main()
