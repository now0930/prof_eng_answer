#!/usr/bin/env python3
"""Regression for source-to-committed-generated drift detection."""

from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from check_generated_rubrics_freshness import check_generated
from validate_generated_rubrics import REQUIRED_GENERATED_FILES


ROOT = Path(__file__).resolve().parents[1]


class GeneratedRubricsFreshnessTest(unittest.TestCase):
    def test_current_bank_matches_rebuild(self) -> None:
        self.assertEqual(check_generated(ROOT / "rubrics" / "generated"), [])

    def test_stale_bank_is_rejected_without_modifying_source(self) -> None:
        with tempfile.TemporaryDirectory(prefix="topic_pack_stale_fixture_") as temporary:
            fixture_dir = Path(temporary)
            for filename in REQUIRED_GENERATED_FILES:
                shutil.copyfile(ROOT / "rubrics" / "generated" / filename, fixture_dir / filename)
            stale_file = fixture_dir / "model_answers.generated.json"
            stale_file.write_bytes(stale_file.read_bytes() + b"\n")
            self.assertEqual(check_generated(fixture_dir), [stale_file.name])


if __name__ == "__main__":
    unittest.main()
