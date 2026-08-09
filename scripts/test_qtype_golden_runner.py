#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from run_qtype_golden_regression import (
    RunnerError,
    compare_inventory,
    load_golden_inventory,
    load_normalized_results,
)

QTYPES = {
    "COMPARE_SELECTION": ("B", "CS", "cases/compare_selection.json"),
    "DIAGNOSIS_ACTION": ("C", "DA", "cases/diagnosis_action.json"),
    "IMPLEMENTATION_EVALUATION": ("D", "IE", "cases/implementation_evaluation.json"),
    "PRINCIPLE_INTERPRETATION": ("A", "PI", "cases/principle_interpretation.json"),
}


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_manifest(root: Path) -> None:
    qtypes = {}
    for qtype, (lane, short, case_file) in QTYPES.items():
        qtypes[qtype] = {
            "lane": lane,
            "short_code": short,
            "case_file": case_file,
            "required_case_count": 3,
        }
    write_json(
        root / "manifest.json",
        {
            "version": "test",
            "question_types": qtypes,
            "score_policy": {
                "layer_max": {"A": 3.0, "B": 6.0, "C": 8.0, "D": 6.0, "E": 2.0},
                "total_max": 25.0,
            },
        },
    )


def expected_for(level: str, topic: str) -> dict:
    if level == "LOW":
        total = {"min": 9.0, "max": 14.0}
    elif level == "PASS":
        total = {"min": 15.0, "max": 19.0}
    else:
        total = {"min": 20.0, "max": 24.0}
    return {
        "question_demands": [{"id": "D1", "text": "demand", "is_core": True}],
        "demand_status": {"D1": "MET"},
        "expected_topic_ids": [topic],
        "routing_mode": "SINGLE_TOPIC",
        "evidence_scope": "TOPIC_ONLY",
        "layer_ranges": {
            "A": {"min": 1.0, "max": 3.0},
            "B": {"min": 2.0, "max": 6.0},
            "C": {"min": 2.0, "max": 8.0},
            "D": {"min": 1.0, "max": 6.0},
            "E": {"min": 0.0, "max": 2.0},
        },
        "total_range": total,
        "coverage_range": {"min": 50.0, "max": 100.0},
        "fact_cap_behavior": "NO_CAP_EXPECTED",
        "critical_fact_expectation": "NO_CRITICAL_ERROR",
        "fatal_logic_expectation": "NO_FATAL",
        "originality_scope": {
            "eligible_axes": ["O1", "O2"],
            "forbidden_axes": ["O3", "O4", "O5"],
        },
        "feedback_scope": {
            "required_elements": ["strength"],
            "forbidden_elements": ["fabricated"],
        },
        "required_feedback_characteristics": ["actionable"],
        "forbidden_feedback": ["unsupported"],
    }


def make_case(qtype: str, short: str, level: str, seq: int) -> dict:
    topic = f"topic_{short.lower()}"
    return {
        "case_id": f"QG-{short}-{level}-{seq:02d}",
        "version": "qtype_golden_case_v1",
        "question_type": qtype,
        "answer_level": level,
        "topic_id_basis": topic,
        "question": "question",
        "answer": "answer",
        "expected": expected_for(level, topic),
    }


def make_complete_collections(root: Path) -> list[dict]:
    all_cases = []
    for qtype, (lane, short, case_file) in QTYPES.items():
        cases = [
            make_case(qtype, short, "LOW", 1),
            make_case(qtype, short, "PASS", 2),
            make_case(qtype, short, "HIGH", 3),
        ]
        write_json(
            root / case_file,
            {
                "version": "qtype_golden_collection_v1",
                "question_type": qtype,
                "lane": lane,
                "cases": cases,
            },
        )
        all_cases.extend(cases)
    return all_cases


def normalized_for(case: dict) -> dict:
    level = case["answer_level"]
    total = {"LOW": 12.0, "PASS": 17.0, "HIGH": 22.0}[level]
    expected = case["expected"]
    return {
        "case_id": case["case_id"],
        "question_type": case["question_type"],
        "topic_ids": list(expected["expected_topic_ids"]),
        "routing_mode": expected["routing_mode"],
        "evidence_scope": expected["evidence_scope"],
        "layer_scores": {"A": 2.0, "B": 4.0, "C": 4.0, "D": 3.0, "E": 1.0},
        "total_score": total,
        "coverage": 80.0,
        "fact_cap_applied": False,
        "critical_fact_error": False,
        "fatal_logic_error": False,
        "originality_axes": ["O1"],
        "feedback_elements": ["strength"],
        "feedback_characteristics": ["actionable"],
    }


class QTypeGoldenRunnerTest(unittest.TestCase):
    def test_g0_empty_inventory_is_valid_without_require_complete(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            inventory = load_golden_inventory(root)
            self.assertEqual(len(inventory.cases), 0)
            self.assertEqual(inventory.expected_case_count, 12)
            self.assertEqual(sum(inventory.qtype_counts.values()), 0)
            self.assertEqual(len(inventory.missing_case_files), 4)

    def test_require_complete_rejects_missing_collections(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            with self.assertRaises(RunnerError):
                load_golden_inventory(root, require_complete=True)

    def test_complete_inventory_and_happy_path_compare(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            cases = make_complete_collections(root)
            inventory = load_golden_inventory(root, require_complete=True)
            results = [normalized_for(case) for case in cases]
            report = compare_inventory(inventory, results)
            self.assertTrue(report.passed, report.failures)
            self.assertEqual(report.golden_case_count, 12)
            self.assertEqual(report.checked_case_count, 12)

    def test_comparator_catches_contract_mismatches(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            cases = make_complete_collections(root)
            inventory = load_golden_inventory(root)
            results = [normalized_for(case) for case in cases]
            broken = results[0]
            broken["question_type"] = "WRONG"
            broken["topic_ids"] = ["wrong_topic"]
            broken["routing_mode"] = "GENERAL"
            broken["evidence_scope"] = "GENERAL_ONLY"
            broken["layer_scores"]["A"] = 99.0
            broken["total_score"] = 99.0
            broken["coverage"] = 101.0
            broken["fact_cap_applied"] = True
            broken["critical_fact_error"] = True
            broken["fatal_logic_error"] = True
            broken["originality_axes"] = ["O3"]
            broken["feedback_elements"] = ["fabricated"]
            broken["feedback_characteristics"] = ["unsupported"]
            report = compare_inventory(inventory, results)
            joined = "\n".join(report.failures)
            self.assertFalse(report.passed)
            for token in (
                "question_type",
                "topic_ids",
                "routing_mode",
                "evidence_scope",
                "layer_scores.A",
                "total_score",
                "coverage",
                "fact_cap_applied",
                "critical_fact_error",
                "fatal_logic_error",
                "originality_axes",
                "feedback_elements",
                "feedback_characteristics",
            ):
                self.assertIn(token, joined)

    def test_missing_and_unexpected_result_cases_are_reported(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            cases = make_complete_collections(root)
            inventory = load_golden_inventory(root)
            results = [normalized_for(case) for case in cases[1:]]
            unexpected = normalized_for(cases[0])
            unexpected["case_id"] = "QG-UNEXPECTED"
            results.append(unexpected)
            report = compare_inventory(inventory, results)
            joined = "\n".join(report.failures)
            self.assertIn(f"{cases[0]['case_id']}:missing-result", joined)
            self.assertIn("QG-UNEXPECTED:unexpected-result", joined)

    def test_duplicate_normalized_result_is_rejected_at_load(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "results.json"
            write_json(path, [{"case_id": "X"}, {"case_id": "X"}])
            with self.assertRaises(RunnerError):
                load_normalized_results(path)

    def test_partial_collection_is_rejected_even_in_inventory_mode(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            make_manifest(root)
            qtype = "PRINCIPLE_INTERPRETATION"
            lane, short, case_file = QTYPES[qtype]
            write_json(
                root / case_file,
                {
                    "version": "qtype_golden_collection_v1",
                    "question_type": qtype,
                    "lane": lane,
                    "cases": [make_case(qtype, short, "LOW", 1)],
                },
            )
            with self.assertRaises(RunnerError):
                load_golden_inventory(root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
