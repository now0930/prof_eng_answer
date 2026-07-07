from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import validate_release_test_coverage as target


class ReleaseTestCoverageValidatorTest(
    unittest.TestCase
):
    def test_py_compile_reference_is_not_execution(
        self,
    ) -> None:
        text = """
python3 -m py_compile \\
  scripts/test_compile_only.py
"""

        self.assertNotIn(
            "scripts/test_compile_only.py",
            target.collect_executed_test_paths(text),
        )

    def test_direct_script_execution_is_covered(
        self,
    ) -> None:
        text = """
python3 scripts/test_direct.py
"""

        self.assertIn(
            "scripts/test_direct.py",
            target.collect_executed_test_paths(text),
        )

    def test_unittest_module_execution_is_covered(
        self,
    ) -> None:
        text = """
python3 -m unittest scripts.test_module
"""

        self.assertIn(
            "scripts/test_module.py",
            target.collect_executed_test_paths(text),
        )

    def test_unittest_test_case_suffix_is_covered(
        self,
    ) -> None:
        text = """
python3 -m unittest scripts.test_module.Case.test_one
"""

        self.assertIn(
            "scripts/test_module.py",
            target.collect_executed_test_paths(text),
        )

    def test_python_runtime_option_is_supported(
        self,
    ) -> None:
        text = """
PYTHONPATH=. python3 -u scripts/test_runtime.py
"""

        self.assertIn(
            "scripts/test_runtime.py",
            target.collect_executed_test_paths(text),
        )

    def test_compile_only_module_is_reported_missing(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            scripts.mkdir()

            (scripts / "test_compile_only.py").write_text(
                "def test_example():\n    pass\n",
                encoding="utf-8",
            )

            release_text = """
python3 -m py_compile \\
  scripts/test_compile_only.py
"""

            self.assertEqual(
                target.find_missing_test_paths(
                    root,
                    release_text,
                ),
                ["scripts/test_compile_only.py"],
            )

    def test_executed_module_is_not_missing(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / "scripts"
            scripts.mkdir()

            (scripts / "test_executed.py").write_text(
                "def test_example():\n    pass\n",
                encoding="utf-8",
            )

            release_text = """
python3 -m unittest scripts.test_executed
"""

            self.assertEqual(
                target.find_missing_test_paths(
                    root,
                    release_text,
                ),
                [],
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
