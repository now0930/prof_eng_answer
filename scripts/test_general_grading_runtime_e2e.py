from __future__ import annotations

import copy
import inspect
import json
import unittest

import gemini_grader
import grade_output_summarizer
import grading_agents
from general_evidence_contract import attach_general_evidence_contract
from question_demand_contract import attach_question_demand_contract


# GENERAL_GRADING_RUNTIME_E2E_RELEASE_GATE_V1


def scoring_model():
    return {
        "layers": [
            {"id": "A", "points": 3},
            {"id": "B", "points": 6},
            {"id": "C", "points": 8},
            {"id": "D", "points": 6},
            {"id": "E", "points": 2},
        ]
    }


def zero_layers():
    return [
        {"layer_id": layer, "score": 0.0, "max_score": maximum, "reason": ""}
        for layer, maximum in (
            ("A", 3.0),
            ("B", 6.0),
            ("C", 8.0),
            ("D", 6.0),
            ("E", 2.0),
        )
    ]


def baselines():
    return {"A": 2.8, "B": 5.7, "C": 5.2, "D": 5.0, "E": 1.7}


class GeneralGradingRuntimeE2ETests(unittest.TestCase):
    def test_effective_runtime_interfaces_are_callable(self):
        prompt = gemini_grader.build_gemini_grading_prompt(
            question_text="원리를 설명하고 설계 기준을 제시하시오.",
            answer_text="답안",
            scoring_model={},
            subject_rubric={},
            rater_profile={},
            volume={},
            fact_eval={},
            connection_eval={},
        )

        self.assertIsInstance(prompt, str)
        self.assertIn(
            "[GENERAL_EVIDENCE_CONTRACT_V1]",
            prompt,
        )
        self.assertIn(
            "[QUESTION_DEMAND_CONTRACT_V1]",
            prompt,
        )
        self.assertTrue(
            callable(
                gemini_grader.build_gemini_grading_prompt
            )
        )
        self.assertEqual(
            tuple(
                inspect.signature(
                    grading_agents
                    ._phase6_apply_semantic_downward_guard
                ).parameters
            ),
            (
                "layer_scores",
                "baseline_scores",
                "gemini_eval",
                "scoring_model",
            ),
        )
        self.assertEqual(
            tuple(
                inspect.signature(
                    grade_output_summarizer
                    ._build_payload
                ).parameters
            ),
            ("grade",),
        )
        self.assertEqual(
            tuple(
                inspect.signature(
                    grade_output_summarizer
                    ._normalise_summary
                ).parameters
            ),
            ("llm_obj", "payload"),
        )

    def test_prompt_contains_runtime_contracts(self):
        prompt = gemini_grader.build_gemini_grading_prompt(
            question_text=(
                "밸브 불평형력과 마찰력의 개념을 설명하고 "
                "Fail-safe 스프링 설계 기준을 제시하시오."
            ),
            answer_text="답안",
            scoring_model={},
            subject_rubric={},
            rater_profile={},
            volume={},
            fact_eval={},
            connection_eval={},
        )

        self.assertIn("[GENERAL_EVIDENCE_CONTRACT_V1]", prompt)
        self.assertIn("[QUESTION_DEMAND_CONTRACT_V1]", prompt)
        self.assertIn('"primary_lens": "PRINCIPLE_INTERPRETATION"', prompt)
        self.assertIn('"demand_kind": "DESIGN"', prompt)

    def test_multiline_formula_survives_attachment_pipeline(self):
        raw = {
            "score": 20.0,
            "total_score": 20.0,
            "parsed": {
                "general_evidence_contract": {
                    "schema_version": "1.0",
                    "mode": "diagnostic_only",
                    "score_effect": "none",
                    "claims": [],
                    "formulas": [
                        {
                            "formula_id": "force_balance",
                            "formula_text": (
                                "F_available = F_spring\n"
                                "F_unbalance\n"
                                "F_friction"
                            ),
                            "variables": [],
                            "conditions": [],
                            "interpretation": "",
                            "integrity_status": "not_evaluated",
                            "integrity_notes": [],
                            "owner_layer": "C",
                        }
                    ],
                    "defects": [],
                    "field_judgements": [],
                    "summary": {},
                }
            },
        }
        before = copy.deepcopy(raw)
        attached = attach_general_evidence_contract(raw)
        formula = attached["general_evidence_contract"]["formulas"][0]

        self.assertEqual(raw, before)
        self.assertIn("\n", formula["formula_text"])
        self.assertEqual(formula["integrity_status"], "warning")
        self.assertTrue(
            any(
                issue["code"] == "missing_term_operator"
                for issue in formula["generic_integrity"]["issues"]
            )
        )
        self.assertEqual(attached["score"], 20.0)
        self.assertEqual(attached["total_score"], 20.0)

    def test_contract_guard_and_verdict_pipeline(self):
        question = (
            "밸브 불평형력과 마찰력의 개념을 설명하고 "
            "Fail-safe 스프링 설계 기준을 제시하시오."
        )
        grade = {
            "score": 18.0,
            "total_score": 18.0,
            "max_score": 25.0,
            "logic_check": {"fatal": False, "findings": []},
            "layer_scores": zero_layers(),
            "parsed": {
                "general_evidence_contract": {
                    "schema_version": "1.0",
                    "mode": "diagnostic_only",
                    "score_effect": "none",
                    "claims": [],
                    "formulas": [
                        {
                            "formula_id": "force_balance",
                            "formula_text": "F_available = F_spring\nF_unbalance",
                            "variables": [],
                            "conditions": [],
                            "interpretation": "",
                            "integrity_status": "not_evaluated",
                            "integrity_notes": [],
                            "owner_layer": "C",
                        }
                    ],
                    "defects": [],
                    "field_judgements": [],
                    "summary": {},
                }
            },
        }

        grade = attach_general_evidence_contract(grade)
        grade = attach_question_demand_contract(grade, question)
        requirements = [
            {
                "requirement_id": row["requirement_id"],
                "status": "present",
                "is_core": True,
            }
            for row in grade["question_demand_contract"]["requirements"]
        ]
        grade["parsed"]["question_type_coverage"] = {
            "overall_coverage": "adequate",
            "explicit_requirement_coverage": {"requirements": requirements},
        }

        guarded, diagnostic = grading_agents._phase6_apply_semantic_downward_guard(
            zero_layers(),
            baselines(),
            grade,
            scoring_model(),
        )
        by_id = {row["layer_id"]: row for row in guarded}

        self.assertEqual(diagnostic["blocked_layers"], [])
        self.assertEqual(by_id["C"]["score"], 3.6)

        payload = grade_output_summarizer._build_payload(grade)
        summary = grade_output_summarizer._normalise_summary(
            {
                "headline": "명백한 기술 오류",
                "overall": "명백한 기술 오류가 있다.",
                "key_reasons": [],
                "section_basis": [],
                "improvements": ["일반적인 내용을 보완"],
            },
            payload,
        )
        rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)

        self.assertEqual(
            summary["headline"],
            "핵심 내용은 유지되며 수식·표현 확인 필요",
        )
        self.assertNotIn("명백한 기술 오류", rendered)
        self.assertIn("수식·표현 무결성", " ".join(summary["improvements"]))
        self.assertEqual(grade["score"], 18.0)

    def test_major_correctness_blocks_only_owner_layer(self):
        evaluation = {
            "parsed": {
                "general_evidence_contract": {
                    "schema_version": "1.0",
                    "mode": "diagnostic_only",
                    "score_effect": "none",
                    "claims": [],
                    "formulas": [],
                    "defects": [
                        {
                            "defect_id": "verified_error",
                            "defect_type": "correctness_error",
                            "severity": "major",
                            "owner_layer": "C",
                            "explanation": "부호가 반대다.",
                        }
                    ],
                    "field_judgements": [],
                    "summary": {},
                },
                "question_demand_contract": {
                    "schema_version": "1.0",
                    "requirements": [],
                },
                "question_type_coverage": {
                    "overall_coverage": "adequate",
                    "explicit_requirement_coverage": {"requirements": []},
                },
            }
        }

        guarded, diagnostic = grading_agents._phase6_apply_semantic_downward_guard(
            zero_layers(),
            baselines(),
            evaluation,
            scoring_model(),
        )
        by_id = {row["layer_id"]: row for row in guarded}

        self.assertEqual(diagnostic["blocked_layers"], ["C"])
        self.assertEqual(by_id["C"]["score"], 0.0)
        self.assertGreater(by_id["D"]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
