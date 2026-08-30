from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import logic_check_evaluator as evaluator
from question_demand_evidence import project_logic_relationship_conflicts

TOPIC_ID = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)
PACK_ROOT = REPO_ROOT / "rubrics" / "topic_packs" / TOPIC_ID
ANSWER = "\n".join(
    [
        "단위시험은 Random Hardware Integrity를 전담하고 독점적으로 입증한다.",
        "통합시험은 Architectural Constraints(HFT/SFF)를 전담하고 독점적으로 입증한다.",
        "시스템시험은 Systematic Integrity를 단독으로 완성하고 입증한다.",
    ]
)
TARGETS = (
    (
        "sw04_unit_test",
        "unit_test.exclusively_establishes.random_hardware_integrity",
        ANSWER.splitlines()[0],
        "D-UNIT",
    ),
    (
        "sw04_integration_test",
        "integration_test.exclusively_establishes.architectural_constraints",
        ANSWER.splitlines()[1],
        "D-INTEGRATION",
    ),
    (
        "sw04_system_test",
        "system_test.exclusively_establishes.systematic_integrity",
        ANSWER.splitlines()[2],
        "D-SYSTEM",
    ),
)
FORBIDDEN_SCORE_KEYS = {
    "score",
    "score_delta",
    "deduction",
    "points",
    "recommended_ceiling",
    "layer_caps",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _pack_docs() -> dict:
    return {
        "model_answer": _load_json(PACK_ROOT / "model_answer.json"),
        "fact_anchor": _load_json(PACK_ROOT / "fact_anchor.json"),
        "logic_check": _load_json(PACK_ROOT / "logic_check.json"),
        "topic_importance": _load_json(PACK_ROOT / "topic_importance.json"),
    }


def _anchor_map() -> dict[str, dict]:
    anchors = _pack_docs()["fact_anchor"].get("anchors") or []
    return {
        str(row.get("anchor_id") or row.get("id")): row
        for row in anchors
        if isinstance(row, dict)
    }


def _demand_evidence() -> dict:
    anchors = _anchor_map()
    demands = []
    for anchor_id, _, _, demand_id in TARGETS:
        anchor = anchors[anchor_id]
        demands.append(
            {
                "demand_id": demand_id,
                "text": anchor["statement"],
                "covered": True,
                "verified": True,
                "level": 1.0,
                "anchor_refs": [anchor_id],
            }
        )
    return {
        "version": "QUESTION_DEMAND_EVIDENCE_V1",
        "status": "shadow_only",
        "score_effect": "none",
        "demand_count": len(demands),
        "demands": demands,
        "summary": {
            "covered_ratio": 1.0,
            "verified_ratio": 1.0,
            "mean_demand_level": 1.0,
        },
    }


def _grade() -> dict:
    docs = _pack_docs()
    return {
        "topic_id": TOPIC_ID,
        "logic_check_topic_id": TOPIC_ID,
        "model_answer_reference": {"topic_id": TOPIC_ID, **docs},
        "question_demand_evidence_for_score": _demand_evidence(),
    }


def _find_axis(axes: list[dict], anchor_id: str) -> dict:
    matches = [
        axis
        for axis in axes
        if isinstance(axis, dict)
        and (
            str(axis.get("axis_id") or "") == anchor_id
            or str(axis.get("axis_id") or "").startswith(anchor_id + "_")
            or anchor_id in (axis.get("anchor_refs") or [])
        )
    ]
    if not matches:
        raise AssertionError(f"axis missing: {anchor_id}")
    return matches[0]


class Stage22CanonicalAxisRuntimeIntegrationTests(unittest.TestCase):
    def test_source_owned_axis_cannot_be_escalated_by_llm(self) -> None:
        axes = [
            {
                "axis_id": "AX-CORE",
                "axis_name": "core axis",
                "canonical_claim": "source canonical relation",
                "criticality": "core",
                "source_fields": ["fact_anchor.anchors"],
                "anchor_refs": ["A-SOURCE"],
                "demand_refs": ["D-SOURCE"],
            }
        ]
        raw = {
            "alignments": [
                {
                    "axis_id": "AX-CORE",
                    "status": "FATAL_CONTRADICTION",
                    "answer_claim": "explicit wrong relation",
                    "canonical_claim": "invented canonical relation",
                    "claim_signature": "source.ownership",
                    "error_class": "INVENTED",
                    "anchor_refs": ["A-INVENTED"],
                    "demand_refs": ["D-INVENTED"],
                    "criticality": "fatal_core",
                    "confidence": 0.99,
                    "reason": "attempted escalation",
                }
            ]
        }

        normalized = evaluator._normalize_canonical_axis_alignment_response(
            raw,
            canonical_axes=axes,
            answer_text="explicit wrong relation",
        )
        row = normalized["alignments"][0]

        self.assertEqual("CONTRADICTED", row["status"])
        self.assertFalse(row["fatal"])
        self.assertEqual("core", row["criticality"])
        self.assertEqual(["A-SOURCE"], row["anchor_refs"])
        self.assertEqual(["D-SOURCE"], row["demand_refs"])
        self.assertEqual("source canonical relation", row["canonical_claim"])

    def test_unknown_axis_and_invented_evidence_fail_open(self) -> None:
        axes = [
            {
                "axis_id": "AX-KNOWN",
                "axis_name": "known axis",
                "canonical_claim": "known relation",
                "criticality": "fatal_core",
                "source_fields": ["fact_anchor.anchors"],
                "anchor_refs": ["A-KNOWN"],
                "demand_refs": ["D-KNOWN"],
            }
        ]
        raw = {
            "alignments": [
                {
                    "axis_id": "AX-UNKNOWN",
                    "status": "FATAL_CONTRADICTION",
                    "answer_claim": "actual answer",
                    "canonical_claim": "invented",
                    "claim_signature": "unknown.axis",
                    "error_class": "INVENTED",
                    "anchor_refs": ["A-FAKE"],
                    "demand_refs": ["D-FAKE"],
                    "criticality": "fatal_core",
                    "confidence": 0.99,
                    "reason": "unknown axis",
                },
                {
                    "axis_id": "AX-KNOWN",
                    "status": "FATAL_CONTRADICTION",
                    "answer_claim": "claim not present",
                    "canonical_claim": "known relation",
                    "claim_signature": "invented.evidence",
                    "error_class": "INVENTED",
                    "anchor_refs": ["A-KNOWN"],
                    "demand_refs": ["D-KNOWN"],
                    "criticality": "fatal_core",
                    "confidence": 0.99,
                    "reason": "invented evidence",
                },
            ]
        }

        normalized = evaluator._normalize_canonical_axis_alignment_response(
            raw,
            canonical_axes=axes,
            answer_text="actual answer",
        )

        self.assertEqual(
            ["UNSUPPORTED", "UNSUPPORTED"],
            [row["status"] for row in normalized["alignments"]],
        )
        self.assertEqual(
            [],
            evaluator._canonical_axis_alignment_to_findings(normalized),
        )

    def test_actual_topic_uses_one_call_and_detects_three_conflicts(self) -> None:
        captured: list[tuple[str, dict | None]] = []

        def fake_call(prompt: str, *, format_schema: dict | None = None) -> dict:
            captured.append((prompt, format_schema))
            marker = "canonical axes:\n"
            self.assertIn(marker, prompt)
            axes = json.loads(prompt.rsplit(marker, 1)[1])
            alignments = []
            for anchor_id, signature, answer_claim, demand_id in TARGETS:
                axis = _find_axis(axes, anchor_id)
                self.assertEqual("fatal_core", axis["criticality"])
                self.assertIn(demand_id, axis.get("demand_refs") or [])
                alignments.append(
                    {
                        "axis_id": axis["axis_id"],
                        "status": "FATAL_CONTRADICTION",
                        "answer_claim": answer_claim,
                        "canonical_claim": "LLM must not own this",
                        "claim_signature": signature,
                        "error_class": "CANONICAL_RELATION_CONTRADICTION",
                        "anchor_refs": ["A-INVENTED"],
                        "demand_refs": ["D-INVENTED"],
                        "criticality": "supporting",
                        "confidence": 0.99,
                        "reason": "explicitly reverses the canonical test-level relationship",
                    }
                )
            return {
                "verdict": "fatal",
                "confidence": 0.99,
                "reason": "three explicit canonical relationship conflicts",
                "checks": [],
                "findings": [],
                "alignments": alignments,
            }

        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=fake_call,
        ) as mocked:
            result = evaluator.evaluate_logic_checks(ANSWER, grade=_grade())

        self.assertEqual(1, mocked.call_count)
        self.assertEqual(1, len(captured))
        prompt, schema = captured[0]
        self.assertIn("GLOBAL_CANONICAL_AXIS_COMPARISON_V1", prompt)
        self.assertIsInstance(schema, dict)
        self.assertIn("alignments", schema["properties"])

        axis_eval = result["canonical_axis_alignment_evaluation"]
        self.assertEqual(3, axis_eval["summary"]["alignment_count"])
        self.assertEqual(3, axis_eval["summary"]["fatal_count"])

        axis_findings = [
            finding
            for finding in result["findings"]
            if finding.get("engine") == "canonical_axis_alignment_v1"
        ]
        self.assertEqual(3, len(axis_findings))
        self.assertTrue(
            all(finding["severity"] == "fatal" for finding in axis_findings)
        )
        self.assertEqual(
            {target[1] for target in TARGETS},
            {finding["claim_signature"] for finding in axis_findings},
        )
        for finding in axis_findings:
            self.assertFalse(FORBIDDEN_SCORE_KEYS & set(finding))
            self.assertNotIn("A-INVENTED", finding["anchor_refs"])
            self.assertNotIn("D-INVENTED", finding["demand_refs"])

        # STAGE22E21S40_EVALUATOR_TO_PROMPT_NEWLINE_REGRESSION_V1

        prompt = captured[0][0]
        hit = prompt.find("global_answer_context")
        self.assertGreaterEqual(hit, 0)
        decoder = json.JSONDecoder()
        candidate_payload = None
        positions = [
            index
            for index, character in enumerate(prompt[: hit + 1])
            if character == "["
        ]
        for position in reversed(positions):
            try:
                value, _ = decoder.raw_decode(prompt[position:])
            except json.JSONDecodeError:
                continue
            if (
                isinstance(value, list)
                and any(
                    isinstance(item, dict)
                    and item.get("kind") == "global_answer_context"
                    for item in value
                )
            ):
                candidate_payload = value
                break

        self.assertIsNotNone(candidate_payload)
        global_candidates = [
            item
            for item in candidate_payload
            if (
                isinstance(item, dict)
                and item.get("kind") == "global_answer_context"
            )
        ]
        self.assertEqual(1, len(global_candidates))
        expected_claims = [
            line.strip()
            for line in ANSWER.splitlines()
            if line.strip()
        ]
        self.assertEqual(
            expected_claims,
            global_candidates[0].get("claims"),
        )
        self.assertNotIn("text", global_candidates[0])

    def test_stage21_projection_remains_score_neutral(self) -> None:
        def fake_call(prompt: str, *, format_schema: dict | None = None) -> dict:
            axes = json.loads(prompt.rsplit("canonical axes:\n", 1)[1])
            alignments = []
            for anchor_id, signature, answer_claim, _ in TARGETS:
                axis = _find_axis(axes, anchor_id)
                alignments.append(
                    {
                        "axis_id": axis["axis_id"],
                        "status": "FATAL_CONTRADICTION",
                        "answer_claim": answer_claim,
                        "canonical_claim": axis["canonical_claim"],
                        "claim_signature": signature,
                        "error_class": "CANONICAL_RELATION_CONTRADICTION",
                        "anchor_refs": axis["anchor_refs"],
                        "demand_refs": axis["demand_refs"],
                        "criticality": axis["criticality"],
                        "confidence": 0.99,
                        "reason": "direct contradiction",
                    }
                )
            return {
                "verdict": "fatal",
                "confidence": 0.99,
                "reason": "three explicit canonical relationship conflicts",
                "checks": [],
                "findings": [],
                "alignments": alignments,
            }

        grade = _grade()
        evidence = grade["question_demand_evidence_for_score"]
        snapshot = copy.deepcopy(evidence)
        with patch(
            "logic_llm_verifier._call_ollama_json",
            side_effect=fake_call,
        ):
            result = evaluator.evaluate_logic_checks(ANSWER, grade=grade)

        projected = project_logic_relationship_conflicts(evidence, result)
        self.assertEqual(snapshot, evidence)
        self.assertEqual("none", projected["score_effect"])
        self.assertEqual(snapshot["demands"], projected["demands"])
        self.assertEqual(snapshot["summary"], projected["summary"])
        summary = projected["relationship_conflict_summary"]
        self.assertEqual("none", summary["score_effect"])
        self.assertEqual(3, summary["conflict_count"])
        self.assertEqual(
            {"D-UNIT", "D-INTEGRATION", "D-SYSTEM"},
            set(summary["affected_demand_refs"]),
        )

    # STAGE22E21S52_SOURCE_IDENTITY_OWNER_REBIND_REGRESSION_V1
    @staticmethod
    def _source_identity_owner_axes():
        return [
            {
                "axis_id": "sw04_unit_test",
                "axis_name": "sw04_unit_test",
                "canonical_claim": (
                    "단위시험은 최소 설계단위를 검증한다."
                ),
                "criticality": "fatal_core",
                "anchor_refs": ["sw04_unit_test"],
                "demand_refs": ["D-UNIT", "D-INTEGRATION"],
            },
            {
                "axis_id": "sw04_integration_test",
                "axis_name": "sw04_integration_test",
                "canonical_claim": (
                    "통합시험은 모듈 상호작용을 검증한다."
                ),
                "criticality": "fatal_core",
                "anchor_refs": ["sw04_integration_test"],
                "demand_refs": ["D-UNIT", "D-INTEGRATION"],
            },
            {
                "axis_id": "sw04_system_test",
                "axis_name": "sw04_system_test",
                "canonical_claim": (
                    "시스템시험은 시스템 요구사항을 검증한다."
                ),
                "criticality": "fatal_core",
                "anchor_refs": ["sw04_system_test"],
                "demand_refs": ["D-SYSTEM"],
            },
            {
                "axis_id": "sw04_integration_test_5",
                "axis_name": "sw04_integration_test",
                "canonical_claim": (
                    "단위시험을 통과한 모듈의 상호작용 결함을 찾는다."
                ),
                "criticality": "fatal_core",
                "anchor_refs": ["sw04_integration_test"],
                "demand_refs": ["D-UNIT", "D-INTEGRATION"],
            },
            {
                "axis_id": "canonical_axis_041",
                "axis_name": "4. 단위·통합·시스템시험",
                "canonical_claim": (
                    "시험수준별 대상과 종료기준을 비교한다."
                ),
                "criticality": "supporting",
                "anchor_refs": [
                    "sw04_unit_test",
                    "sw04_integration_test",
                    "sw04_system_test",
                ],
                "demand_refs": [
                    "D-UNIT",
                    "D-INTEGRATION",
                    "D-SYSTEM",
                ],
            },
            {
                "axis_id": "sw04_major_test_levels_not_distinct",
                "axis_name": "sw04_major_test_levels_not_distinct",
                "canonical_claim": (
                    "단위는 최소 설계단위, 통합은 상호작용, "
                    "시스템은 end-to-end 요구사항을 검증한다."
                ),
                "criticality": "supporting",
                "anchor_refs": [],
                "demand_refs": ["D-UNIT"],
            },
        ]

    @staticmethod
    def _captured_relation_rows():
        umbrella = "sw04_major_test_levels_not_distinct"
        return [
            {
                "axis_id": umbrella,
                "answer_claim": ANSWER.splitlines()[0],
                "claim_signature": (
                    "단위시험.exclusively_establishes."
                    "Random Hardware Integrity"
                ),
                "status": "CONTRADICTED",
                "criticality": "fatal_core",
                "confidence": 0.9,
                "error_class": (
                    "CANONICAL_RELATION_CONTRADICTION"
                ),
                "anchor_refs": [],
                "demand_refs": [],
            },
            {
                "axis_id": umbrella,
                "answer_claim": ANSWER.splitlines()[1],
                "claim_signature": (
                    "통합시험.exclusively_establishes."
                    "Architectural Constraints(HFT/SFF)"
                ),
                "status": "CONTRADICTED",
                "criticality": "fatal_core",
                "confidence": 0.9,
                "error_class": (
                    "CANONICAL_RELATION_CONTRADICTION"
                ),
                "anchor_refs": [],
                "demand_refs": [],
            },
            {
                "axis_id": umbrella,
                "answer_claim": ANSWER.splitlines()[2],
                "claim_signature": (
                    "시스템시험.exclusively_establishes."
                    "Systematic Integrity"
                ),
                "status": "CONTRADICTED",
                "criticality": "fatal_core",
                "confidence": 0.9,
                "error_class": (
                    "CANONICAL_RELATION_CONTRADICTION"
                ),
                "anchor_refs": [],
                "demand_refs": [],
            },
        ]

    def test_source_identity_owner_rebinds_three_captured_relation_rows(self):
        payload = {
            "alignments": self._captured_relation_rows(),
        }
        prepared = (
            evaluator
            ._rebind_exclusive_relation_rows_to_source_owner(
                payload,
                canonical_axes=self._source_identity_owner_axes(),
                answer_text=ANSWER,
            )
        )
        rows = prepared["alignments"]

        self.assertEqual(
            [
                "sw04_unit_test",
                "sw04_integration_test",
                "sw04_system_test",
            ],
            [row["axis_id"] for row in rows],
        )
        self.assertEqual(
            ["FATAL_CONTRADICTION"] * 3,
            [row["status"] for row in rows],
        )
        self.assertEqual(
            "sw04_major_test_levels_not_distinct",
            payload["alignments"][0]["axis_id"],
        )

    def test_source_identity_owner_rebind_fails_closed_matrix(self):
        import copy

        axes = self._source_identity_owner_axes()
        base = self._captured_relation_rows()[0]
        umbrella = "sw04_major_test_levels_not_distinct"

        cases = []

        row = copy.deepcopy(base)
        row["claim_signature"] = (
            "단위시험.supports.Random Hardware Integrity"
        )
        cases.append((row, axes, ANSWER))

        row = copy.deepcopy(base)
        row["answer_claim"] = (
            "알수없는시험은 Random Hardware Integrity를 "
            "독점적으로 입증한다."
        )
        row["claim_signature"] = (
            "알수없는시험.exclusively_establishes."
            "Random Hardware Integrity"
        )
        cases.append((row, axes, ANSWER + "\n" + row["answer_claim"]))

        duplicate = copy.deepcopy(axes[0])
        duplicate["axis_id"] = "duplicate_unit_test"
        duplicate["anchor_refs"] = ["duplicate_unit_test"]
        duplicate["demand_refs"] = ["D-DUPLICATE"]
        cases.append(
            (
                copy.deepcopy(base),
                [*axes, duplicate],
                ANSWER,
            )
        )

        cases.append(
            (
                copy.deepcopy(base),
                axes,
                "다른 문장만 존재한다.",
            )
        )

        row = copy.deepcopy(base)
        row["confidence"] = 0.79
        cases.append((row, axes, ANSWER))

        row = copy.deepcopy(base)
        row["axis_id"] = "sw04_integration_test"
        cases.append((row, axes, ANSWER))

        for row, case_axes, case_answer in cases:
            original = copy.deepcopy(row)
            prepared = (
                evaluator
                ._rebind_exclusive_relation_rows_to_source_owner(
                    {"alignments": [row]},
                    canonical_axes=case_axes,
                    answer_text=case_answer,
                )
            )
            actual = prepared["alignments"][0]
            self.assertEqual(
                original["axis_id"],
                actual["axis_id"],
            )
            self.assertEqual(
                original["status"],
                actual["status"],
            )
            self.assertEqual(
                umbrella
                if original["axis_id"] == umbrella
                else "sw04_integration_test",
                actual["axis_id"],
            )

    def test_source_identity_owner_rebind_keeps_direct_owner_idempotent(self):
        row = self._captured_relation_rows()[0]
        row["axis_id"] = "sw04_unit_test"

        first = (
            evaluator
            ._rebind_exclusive_relation_rows_to_source_owner(
                {"alignments": [row]},
                canonical_axes=self._source_identity_owner_axes(),
                answer_text=ANSWER,
            )
        )
        second = (
            evaluator
            ._rebind_exclusive_relation_rows_to_source_owner(
                first,
                canonical_axes=self._source_identity_owner_axes(),
                answer_text=ANSWER,
            )
        )

        self.assertEqual(
            "sw04_unit_test",
            first["alignments"][0]["axis_id"],
        )
        self.assertEqual(
            "FATAL_CONTRADICTION",
            first["alignments"][0]["status"],
        )
        self.assertEqual(first, second)

    # STAGE22E21S54_EXACT_RELATION_STATUS_COMPATIBILITY_REGRESSION_V1
    def test_source_identity_owner_rebind_accepts_exact_relation_status_pair_only(self):
        import copy

        axes = self._source_identity_owner_axes()
        base = self._captured_relation_rows()[0]
        exact = copy.deepcopy(base)
        exact["status"] = "CANONICAL_RELATION_CONTRADICTION"
        exact["error_class"] = (
            "CANONICAL_RELATION_CONTRADICTION"
        )

        prepared = (
            evaluator
            ._rebind_exclusive_relation_rows_to_source_owner(
                {"alignments": [exact]},
                canonical_axes=axes,
                answer_text=ANSWER,
            )
        )
        actual = prepared["alignments"][0]
        self.assertEqual(
            "sw04_unit_test",
            actual["axis_id"],
        )
        self.assertEqual(
            "FATAL_CONTRADICTION",
            actual["status"],
        )

        fail_closed = [
            (
                "CANONICAL_RELATION_CONTRADICTION",
                "OTHER_ERROR",
            ),
            (
                "UNSUPPORTED",
                "CANONICAL_RELATION_CONTRADICTION",
            ),
            (
                "ARBITRARY",
                "CANONICAL_RELATION_CONTRADICTION",
            ),
        ]
        for status, error_class in fail_closed:
            row = copy.deepcopy(base)
            row["status"] = status
            row["error_class"] = error_class
            output = (
                evaluator
                ._rebind_exclusive_relation_rows_to_source_owner(
                    {"alignments": [row]},
                    canonical_axes=axes,
                    answer_text=ANSWER,
                )
            )["alignments"][0]
            self.assertEqual(
                base["axis_id"],
                output["axis_id"],
            )
            self.assertEqual(
                status,
                output["status"],
            )

        existing = copy.deepcopy(base)
        existing["status"] = "CONTRADICTED"
        existing["error_class"] = (
            "CANONICAL_RELATION_CONTRADICTION"
        )
        output = (
            evaluator
            ._rebind_exclusive_relation_rows_to_source_owner(
                {"alignments": [existing]},
                canonical_axes=axes,
                answer_text=ANSWER,
            )
        )["alignments"][0]
        self.assertEqual(
            "sw04_unit_test",
            output["axis_id"],
        )
        self.assertEqual(
            "FATAL_CONTRADICTION",
            output["status"],
        )




class Stage22ProfileEmptyCandidateFallbackTests(
    unittest.TestCase
):
    def test_global_axes_preserve_one_call_when_profile_candidates_empty(
        self,
    ) -> None:
        from logic_llm_verifier import verify_logic_with_llm

        profile = {
            "topic_id": "stage22_empty_candidate_profile",
            "display_name": "Stage22 empty candidate profile",
            "truth_schema": [],
            "fatal_conditions": [],
            "safe_conditions": [],
            "candidate_extraction": {
                "rules": [],
                "key_terms": [],
            },
            "cap_policy": {
                "fatal_confidence_threshold": 0.80,
                "fatal_recommended_ceiling": 10.0,
            },
        }
        axes = [
            {
                "axis_id": "AX-EMPTY-CANDIDATE",
                "axis_name": "empty candidate axis",
                "canonical_claim": (
                    "단위시험은 소프트웨어 단위의 체계적 결함을 "
                    "검출한다."
                ),
                "criticality": "fatal_core",
                "source_fields": [
                    "fact_anchor.anchors[sw04_unit_test]"
                ],
                "anchor_refs": ["sw04_unit_test"],
                "demand_refs": ["D-UNIT"],
            }
        ]
        response = {
            "verdict": "fatal",
            "confidence": 0.99,
            "reason": "direct contradiction",
            "findings": [],
            "alignments": [
                {
                    "axis_id": "AX-EMPTY-CANDIDATE",
                    "status": "FATAL_CONTRADICTION",
                    "answer_claim": (
                        "단위시험은 Random Hardware Integrity를 "
                        "전담한다."
                    ),
                    "canonical_claim": (
                        "단위시험은 소프트웨어 단위의 체계적 결함을 "
                        "검출한다."
                    ),
                    "claim_signature": (
                        "unit_test.exclusively_establishes."
                        "random_hardware_integrity"
                    ),
                    "error_class": (
                        "CANONICAL_RELATION_CONTRADICTION"
                    ),
                    "anchor_refs": ["sw04_unit_test"],
                    "demand_refs": ["D-UNIT"],
                    "criticality": "fatal_core",
                    "confidence": 0.99,
                    "reason": "direct contradiction",
                }
            ],
        }

        with (
            patch(
                "logic_llm_verifier.load_logic_check_profile",
                return_value=profile,
            ),
            patch(
                "logic_llm_verifier."
                "extract_logic_evidence_candidates",
                return_value=[],
            ),
            patch(
                "logic_llm_verifier._call_ollama_json",
                return_value=response,
            ) as mocked_call,
        ):
            result = verify_logic_with_llm(
                (
                    "단위시험은 Random Hardware Integrity를 "
                    "전담한다."
                ),
                "stage22_empty_candidate_profile",
                canonical_axes=axes,
            )

        self.assertEqual(1, mocked_call.call_count)
        prompt = mocked_call.call_args.args[0]
        kwargs = mocked_call.call_args.kwargs
        self.assertIn(
            "GLOBAL_CANONICAL_AXIS_COMPARISON_V1",
            prompt,
        )
        self.assertIn("format_schema", kwargs)
        self.assertEqual(
            "global_answer_context",
            result["candidates"][0]["kind"],
        )
        self.assertEqual(
            1,
            result[
                "canonical_axis_alignment_evaluation"
            ]["summary"]["alignment_count"],
        )
if __name__ == "__main__":
    unittest.main()
