from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import datetime as real_datetime
from pathlib import Path
from unittest.mock import patch

import bot
import grading_agents


class FixedDatetime:
    @classmethod
    def now(cls):
        return real_datetime(
            2026,
            7,
            19,
            21,
            45,
            30,
        )


def stale_verified_grade():
    coverage = {
        "question_type": (
            "PRINCIPLE_INTERPRETATION"
        ),
        "name_ko": "원리·해석형",
        "overall_coverage": "strong",
        "explicit_requirement_coverage": {
            "source": "question_text",
            "extraction_confidence": "high",
            "requirements": [
                {
                    "requirement": (
                        "불평형력 개념 설명"
                    ),
                    "status": "present",
                    "evidence": "설명 존재",
                    "is_core": True,
                },
                {
                    "requirement": (
                        "마찰력 개념 설명"
                    ),
                    "status": "present",
                    "evidence": "설명 존재",
                    "is_core": True,
                },
                {
                    "requirement": (
                        "Fail Safe 스프링 설계 기준"
                    ),
                    "status": "present",
                    "evidence": "기준 존재",
                    "is_core": True,
                },
            ],
        },
    }

    defects = [
        {
            "defect_id": "friction_defect",
            "defect_type": "correctness_error",
            "severity": "major",
            "owner_layer": "C",
            "requirement_id": "",
            "source": "control_valve_formula_check",
            "source_finding_id": (
                "friction_viscous_model_"
                "overgeneralized"
            ),
            "evidence_text": "Fb = C * v",
            "explanation": "마찰력 일반화",
        },
        {
            "defect_id": "spring_defect",
            "defect_type": "correctness_error",
            "severity": "major",
            "owner_layer": "C",
            "requirement_id": "",
            "source": "control_valve_formula_check",
            "source_finding_id": (
                "force_balance_requirement_"
                "sign_contradiction"
            ),
            "evidence_text": "Fs 부호 모순",
            "explanation": "힘 평형 부호 모순",
        },
    ]

    contract = {
        "schema_version": "1.0",
        "contract_marker": (
            "GENERAL_EVIDENCE_CONTRACT_V1"
        ),
        "mode": "diagnostic_only",
        "score_effect": "none",
        "claims": [],
        "formulas": [],
        "defects": copy.deepcopy(defects),
        "field_judgements": [],
        "summary": {},
    }

    return {
        "score": 16.33,
        "total_score": 16.33,
        "final_total_score": 16.33,
        "score_range": "15.8~16.8",
        "layer_scores": [
            {
                "layer_id": "A",
                "score": 2.56,
                "max": 3.0,
            },
            {
                "layer_id": "B",
                "score": 5.31,
                "max": 6.0,
            },
            {
                "layer_id": "C",
                "score": 2.27,
                "max": 8.0,
            },
            {
                "layer_id": "D",
                "score": 4.64,
                "max": 6.0,
            },
            {
                "layer_id": "E",
                "score": 1.55,
                "max": 2.0,
            },
        ],
        "question_type_coverage": copy.deepcopy(
            coverage
        ),
        "question_type_coverage_summary": {
            "question_type": (
                "PRINCIPLE_INTERPRETATION"
            ),
            "overall_coverage": "strong",
            "sub_criteria_total": 7,
            "sub_criteria_present": 6,
            "sub_criteria_partial": 1,
            "sub_criteria_incorrect": 0,
            "sub_criteria_missing": 0,
            "weighted_coverage_score": 6.5,
            "weighted_coverage_percent": 92.9,
            "incorrect_criteria": [],
        },
        "general_evidence_contract": copy.deepcopy(
            contract
        ),
        "parsed": {
            "general_evidence_contract": copy.deepcopy(
                contract
            ),
        },
    }


class FinalVerifiedCoveragePersistenceTests(
    unittest.TestCase
):
    def test_final_persistence_repairs_stale_display(self):
        grade = stale_verified_grade()
        score_before = (
            grade["score"],
            grade["total_score"],
            grade["final_total_score"],
            copy.deepcopy(grade["layer_scores"]),
        )

        result = (
            grading_agents
            ._phase2_finalize_verified_coverage_for_persistence(
                grade
            )
        )

        rows = result[
            "question_type_coverage"
        ]["explicit_requirement_coverage"][
            "requirements"
        ]
        statuses = [
            row["status"]
            for row in rows
        ]
        summary = result[
            "question_type_coverage_summary"
        ]

        self.assertEqual(
            statuses,
            [
                "present",
                "incorrect",
                "incorrect",
            ],
        )
        self.assertEqual(
            result["question_type_coverage"][
                "overall_coverage"
            ],
            "weak",
        )
        self.assertEqual(
            summary["overall_coverage"],
            "weak",
        )
        self.assertEqual(
            summary["sub_criteria_incorrect"],
            2,
        )
        self.assertEqual(
            summary[
                "verified_defect_display_sync"
            ]["marker"],
            "VERIFIED_DEFECT_DISPLAY_SUMMARY_SYNC_V4",
        )
        self.assertEqual(
            result[
                "verified_defect_reconciliation"
            ]["final_persistence"]["marker"],
            "FINAL_VERIFIED_COVERAGE_PERSISTENCE_V1",
        )
        self.assertEqual(
            (
                result["score"],
                result["total_score"],
                result["final_total_score"],
                result["layer_scores"],
            ),
            score_before,
        )

    def test_final_hook_is_after_aliases_before_write(self):
        source = Path(
            grading_agents.__file__
        ).read_text(encoding="utf-8")

        aliases = source.index(
            "grade = _phase2_add_display_aliases(grade)"
        )
        final_hook = source.index(
            "# FINAL_VERIFIED_COVERAGE_PERSISTENCE_V1",
            aliases,
        )
        write = source.index(
            '_phase2_json_write(session_dir / "grade.json", grade)',
            final_hook,
        )

        self.assertLess(
            aliases,
            final_hook,
        )
        self.assertLess(
            final_hook,
            write,
        )


class GradeSessionIsolationTests(
    unittest.TestCase
):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.sessions = Path(self.temp.name)
        self.state = {
            "chats": {},
        }

    def tearDown(self):
        self.temp.cleanup()

    def _write_meta(
        self,
        sid,
        status,
    ):
        session = self.sessions / sid
        (session / "images").mkdir(
            parents=True,
            exist_ok=True,
        )
        (session / "meta.json").write_text(
            json.dumps(
                {
                    "session_id": sid,
                    "images": [],
                    "status": status,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def test_new_session_is_collision_safe(self):
        with (
            patch.object(
                bot,
                "SESSIONS_DIR",
                self.sessions,
            ),
            patch.object(
                bot,
                "datetime",
                FixedDatetime,
            ),
            patch.object(
                bot,
                "save_state",
                lambda _state: None,
            ),
        ):
            first = bot.new_session(
                5960502198,
                self.state,
            )
            second = bot.new_session(
                5960502198,
                self.state,
            )

        self.assertNotEqual(
            first,
            second,
        )
        self.assertEqual(
            first,
            "20260719_214530_5960502198",
        )
        self.assertEqual(
            second,
            "20260719_214530_1_5960502198",
        )
        self.assertTrue(
            (self.sessions / first).is_dir()
        )
        self.assertTrue(
            (self.sessions / second).is_dir()
        )

    def test_graded_session_is_replaced(self):
        old_sid = "20260719_210000_5960502198"
        self._write_meta(
            old_sid,
            "graded",
        )
        self.state["chats"]["5960502198"] = {
            "active_session": old_sid,
        }

        with (
            patch.object(
                bot,
                "SESSIONS_DIR",
                self.sessions,
            ),
            patch.object(
                bot,
                "datetime",
                FixedDatetime,
            ),
            patch.object(
                bot,
                "save_state",
                lambda _state: None,
            ),
        ):
            fresh = (
                bot._ensure_fresh_grade_session(
                    5960502198,
                    self.state,
                )
            )

        self.assertNotEqual(
            fresh,
            old_sid,
        )
        self.assertEqual(
            self.state["chats"][
                "5960502198"
            ]["active_session"],
            fresh,
        )

    def test_ungraded_session_is_preserved(self):
        active_sid = "20260719_210100_5960502198"
        self._write_meta(
            active_sid,
            "created",
        )
        self.state["chats"]["5960502198"] = {
            "active_session": active_sid,
        }

        with (
            patch.object(
                bot,
                "SESSIONS_DIR",
                self.sessions,
            ),
            patch.object(
                bot,
                "save_state",
                lambda _state: None,
            ),
        ):
            selected = (
                bot._ensure_fresh_grade_session(
                    5960502198,
                    self.state,
                )
            )

        self.assertEqual(
            selected,
            active_sid,
        )


if __name__ == "__main__":
    unittest.main()
