from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import grading_agents
from generic_formula_integrity import (
    analyze_formula_text,
)
from question_demand_contract import (
    build_question_demand_contract,
)
from verdict_consistency import (
    reconcile_verdict_summary,
)


# CROSS_TOPIC_CALIBRATION_CORPUS_REGRESSION_V1

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = (
    REPO_ROOT
    / "calibration"
    / "general_grading_cross_topic_cases.json"
)


def load_corpus():
    return json.loads(
        CORPUS_PATH.read_text(encoding="utf-8")
    )


def scoring_model():
    return {
        "layers": [
            {"id": "A", "points": 3},
            {"id": "B", "points": 6},
            {"id": "C", "points": 8},
            {"id": "D", "points": 6},
            {"id": "E", "points": 2},
        ],
    }


def layer_rows():
    return [
        {
            "layer_id": layer_id,
            "score": 0.0,
            "max_score": maximum,
            "reason": "",
        }
        for layer_id, maximum in (
            ("A", 3.0),
            ("B", 6.0),
            ("C", 8.0),
            ("D", 6.0),
            ("E", 2.0),
        )
    ]


def baseline_scores():
    return {
        "A": 2.8,
        "B": 5.7,
        "C": 5.2,
        "D": 5.0,
        "E": 1.7,
    }


def guard_evaluation(case):
    return {
        "parsed": {
            "general_evidence_contract": {
                "schema_version": "1.0",
                "mode": "diagnostic_only",
                "score_effect": "none",
                "claims": [],
                "formulas": [],
                "defects": copy.deepcopy(
                    case["defects"]
                ),
                "field_judgements": [],
                "summary": {},
            },
            "question_demand_contract": {
                "schema_version": "1.0",
                "mode": "question_only_deterministic",
                "requirements": copy.deepcopy(
                    case["demand_requirements"]
                ),
            },
            "question_type_coverage": {
                "overall_coverage": "adequate",
                "explicit_requirement_coverage": {
                    "requirements": copy.deepcopy(
                        case["requirements"]
                    ),
                },
            },
            "layer_issue_ownership": [],
        },
    }


def verdict_payload(case):
    fatal = case["logic_fatal"]

    return {
        "score": {
            "total": 18.0,
            "max": 25.0,
        },
        "logic_check": {
            "fatal": fatal,
            "findings": (
                [
                    {
                        "severity": "fatal",
                        "message": "검증된 fatal",
                    }
                ]
                if fatal
                else []
            ),
        },
        "general_evidence_contract": {
            "schema_version": "1.0",
            "mode": "diagnostic_only",
            "score_effect": "none",
            "claims": [],
            "formulas": [],
            "defects": copy.deepcopy(
                case["defects"]
            ),
            "field_judgements": [],
            "summary": {},
        },
        "question_demand_contract": {
            "schema_version": "1.0",
            "requirements": copy.deepcopy(
                case["demand_requirements"]
            ),
        },
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": copy.deepcopy(
                    case["requirements"]
                ),
            },
        },
    }


class CrossTopicCalibrationCorpusTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls):
        cls.corpus = load_corpus()

    def test_corpus_schema_and_diversity(self):
        corpus = self.corpus

        self.assertEqual(
            corpus["schema_version"],
            "1.0",
        )

        all_cases = []

        for key in (
            "question_contract_cases",
            "formula_integrity_cases",
            "guard_cases",
            "verdict_cases",
        ):
            rows = corpus[key]
            self.assertTrue(rows, key)
            all_cases.extend(rows)

        identifiers = [
            row["id"]
            for row in all_cases
        ]
        self.assertEqual(
            len(identifiers),
            len(set(identifiers)),
        )

        domains = {
            row["domain"]
            for row in all_cases
        }
        self.assertTrue(
            {
                "VALVE",
                "SENSOR",
                "PID",
                "SAFETY",
                "COMMUNICATION",
                "NOISE",
                "CONTROL_THEORY",
            }.issubset(domains)
        )

        lenses = {
            row["expected_primary_lens"]
            for row in corpus[
                "question_contract_cases"
            ]
        }
        self.assertEqual(
            lenses,
            {
                "COMPARE_SELECTION",
                "DIAGNOSIS_ACTION",
                "IMPLEMENTATION_EVALUATION",
                "PRINCIPLE_INTERPRETATION",
            },
        )

        statuses = {
            row["expected_status"]
            for row in corpus[
                "formula_integrity_cases"
            ]
        }
        self.assertEqual(
            statuses,
            {"valid", "warning", "invalid"},
        )

        defect_types = {
            defect["defect_type"]
            for row in corpus["verdict_cases"]
            for defect in row["defects"]
        }
        self.assertEqual(
            defect_types,
            {
                "correctness_error",
                "core_depth_gap",
                "advanced_detail_missing",
                "presentation_issue",
            },
        )

    def test_question_contract_cases(self):
        for case in self.corpus[
            "question_contract_cases"
        ]:
            with self.subTest(case=case["id"]):
                contract = (
                    build_question_demand_contract(
                        case["question"]
                    )
                )
                self.assertEqual(
                    contract["primary_lens"],
                    case[
                        "expected_primary_lens"
                    ],
                )
                self.assertTrue(
                    contract["primary_lens_locked"]
                )
                self.assertEqual(
                    contract[
                        "answer_text_dependency"
                    ],
                    "none",
                )

                secondary = {
                    row["demand_kind"]
                    for row in contract[
                        "secondary_demands"
                    ]
                }
                self.assertTrue(
                    set(
                        case[
                            "required_secondary_demands"
                        ]
                    ).issubset(secondary)
                )

                detected = set(
                    contract["summary"][
                        "demand_kinds"
                    ]
                )
                self.assertTrue(
                    set(
                        case[
                            "required_demand_kinds"
                        ]
                    ).issubset(detected)
                )

    def test_question_normalization_cases(self):
        for case in self.corpus[
            "normalization_cases"
        ]:
            with self.subTest(case=case["id"]):
                contracts = [
                    build_question_demand_contract(
                        question
                    )
                    for question in case[
                        "question_variants"
                    ]
                ]
                first = contracts[0]

                for contract in contracts[1:]:
                    self.assertEqual(
                        contract[
                            "normalized_question"
                        ],
                        first[
                            "normalized_question"
                        ],
                    )
                    self.assertEqual(
                        contract["question_hash"],
                        first["question_hash"],
                    )
                    self.assertEqual(
                        contract["requirements"],
                        first["requirements"],
                    )

    def test_formula_integrity_cases(self):
        for case in self.corpus[
            "formula_integrity_cases"
        ]:
            with self.subTest(case=case["id"]):
                result = analyze_formula_text(
                    case["formula"]
                )
                self.assertEqual(
                    result["status"],
                    case["expected_status"],
                )
                issue_codes = {
                    row["code"]
                    for row in result["issues"]
                }
                self.assertTrue(
                    set(
                        case[
                            "required_issue_codes"
                        ]
                    ).issubset(issue_codes)
                )

    def test_layer_guard_cases(self):
        for case in self.corpus[
            "guard_cases"
        ]:
            with self.subTest(case=case["id"]):
                baseline = baseline_scores()
                guarded, diagnostic = (
                    grading_agents
                    ._phase6_apply_semantic_downward_guard(
                        layer_rows(),
                        baseline,
                        guard_evaluation(case),
                        scoring_model(),
                    )
                )
                self.assertEqual(
                    diagnostic["blocked_layers"],
                    case[
                        "expected_blocked_layers"
                    ],
                )

                for row in guarded:
                    self.assertLessEqual(
                        row["score"],
                        baseline[row["layer_id"]],
                    )

    def test_verdict_cases(self):
        for case in self.corpus[
            "verdict_cases"
        ]:
            with self.subTest(case=case["id"]):
                summary = {
                    "headline": case[
                        "initial_headline"
                    ],
                    "overall": (
                        "명백한 기술 오류가 있다."
                    ),
                    "key_reasons": [],
                    "section_basis": [],
                    "improvements": [
                        "일반적인 내용을 보완",
                    ],
                }
                source_payload = verdict_payload(
                    case
                )
                before = copy.deepcopy(
                    source_payload
                )
                result = reconcile_verdict_summary(
                    summary,
                    source_payload,
                )

                self.assertEqual(
                    source_payload,
                    before,
                )
                self.assertEqual(
                    result["headline"],
                    case["expected_headline"],
                )

                rendered = json.dumps(
                    result,
                    ensure_ascii=False,
                    sort_keys=True,
                )
                improvements = " ".join(
                    result.get(
                        "improvements",
                        [],
                    )
                )

                for fragment in case[
                    "required_improvement_fragments"
                ]:
                    self.assertIn(
                        fragment,
                        improvements,
                    )

                for fragment in case[
                    "forbidden_fragments"
                ]:
                    self.assertNotIn(
                        fragment,
                        rendered,
                    )


if __name__ == "__main__":
    unittest.main()
