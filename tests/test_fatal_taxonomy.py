import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from deterministic_replay_audit import run_deterministic_replay_audit
from fatal_taxonomy import load_fatal_taxonomy


class FatalTaxonomyTests(unittest.TestCase):
    def test_each_current_unexplained_fatal_has_one_owner(self):
        report = run_deterministic_replay_audit(
            root=REPO,
            golden_path=REPO / "calibration" / "expert_accuracy_golden.jsonl",
        )
        unexplained = {row["finding_id"] for row in report["unexplained_differences"]}
        taxonomy = load_fatal_taxonomy()
        self.assertLessEqual(unexplained, set(taxonomy))
        self.assertEqual(len(taxonomy), 8)
        self.assertEqual(len({row["invariant_code"] for row in taxonomy.values()}), 8)

    def test_taxonomy_does_not_embed_fixture_text(self):
        text = (REPO / "grading_ontology" / "fatal_taxonomy.json").read_text(encoding="utf-8")
        for fixture_name in (
            "sil_target_operations_overgrading_regression.json",
            "mcdc_vmodel_sil_overgrading_regression.json",
            "lambda_SIS 비율이 PFD 비율보다 작도록",
        ):
            self.assertNotIn(fixture_name, text)


if __name__ == "__main__":
    unittest.main()
