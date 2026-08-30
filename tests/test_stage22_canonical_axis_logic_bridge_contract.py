from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import logic_check_evaluator as evaluator


TOPIC_ID = (
    "instrumentation_control_software_lifecycle_"
    "v_model_traceability_verification_validation"
)
PACK_ROOT = REPO_ROOT / "rubrics" / "topic_packs" / TOPIC_ID

REQUIRED_SYMBOLS = (
    "_build_canonical_axis_context",
    "_normalize_canonical_axis_alignment_response",
    "_canonical_axis_alignment_to_findings",
)
STATUS_VALUES = {
    "ALIGNED",
    "PARTIAL",
    "OFF_AXIS",
    "UNSUPPORTED",
    "CONTRADICTED",
    "FATAL_CONTRADICTION",
}
STAGE21_METADATA_KEYS = {
    "error_class",
    "claim_signature",
    "anchor_refs",
    "demand_refs",
}
FORBIDDEN_SCORE_KEYS = {
    "score",
    "score_delta",
    "deduction",
    "points",
    "recommended_ceiling",
    "layer_caps",
}


def _symbols_ready() -> bool:
    return all(hasattr(evaluator, name) for name in REQUIRED_SYMBOLS)


def _load_json(name: str) -> dict[str, Any]:
    return json.loads((PACK_ROOT / name).read_text(encoding="utf-8"))


def _existing_topic_context() -> dict[str, Any]:
    return {
        "topic_id": TOPIC_ID,
        "model_answer": _load_json("model_answer.json"),
        "fact_anchor": _load_json("fact_anchor.json"),
        "logic_check": _load_json("logic_check.json"),
        "topic_importance": _load_json("topic_importance.json"),
    }


def _axis(
    *,
    axis_id: str,
    claim: str,
    criticality: str = "core",
    anchor_refs: list[str] | None = None,
    demand_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "axis_id": axis_id,
        "axis_name": axis_id,
        "canonical_claim": claim,
        "criticality": criticality,
        "source_fields": ["fact_anchor.anchors"],
        "anchor_refs": ([f"A-{axis_id}"] if anchor_refs is None else anchor_refs),
        "demand_refs": ([f"D-{axis_id}"] if demand_refs is None else demand_refs),
    }


def _raw_alignment(
    *,
    status: str,
    claim_signature: str,
    confidence: float = 0.95,
    criticality: str = "core",
    anchor_refs: list[str] | None = None,
    demand_refs: list[str] | None = None,
    answer_claim: str = "answer claim",
    canonical_claim: str = "canonical claim",
) -> dict[str, Any]:
    return {
        "status": status,
        "answer_claim": answer_claim,
        "canonical_claim": canonical_claim,
        "claim_signature": claim_signature,
        "error_class": "CANONICAL_RELATION_CONTRADICTION",
        "anchor_refs": ([f"A-{claim_signature}"] if anchor_refs is None else anchor_refs),
        "demand_refs": ([f"D-{claim_signature}"] if demand_refs is None else demand_refs),
        "criticality": criticality,
        "confidence": confidence,
        "reason": "direct canonical relationship comparison",
    }


@unittest.skipUnless(
    _symbols_ready(),
    "Stage22 production helpers are not implemented yet.",
)
class Stage22CanonicalAxisBehaviorTests(unittest.TestCase):
    def test_builds_axes_from_existing_topic_pack_without_schema_change(
        self,
    ) -> None:
        context = _existing_topic_context()
        snapshot = copy.deepcopy(context)

        axes = evaluator._build_canonical_axis_context(context)

        self.assertEqual(snapshot, context)
        self.assertIsInstance(axes, list)
        self.assertGreaterEqual(len(axes), 1)

        required = {
            "axis_id",
            "axis_name",
            "canonical_claim",
            "criticality",
            "source_fields",
            "anchor_refs",
            "demand_refs",
        }
        for axis in axes:
            self.assertIsInstance(axis, dict)
            self.assertTrue(required.issubset(axis))
            self.assertTrue(str(axis["canonical_claim"]).strip())
            self.assertNotIn("wrong_claim", axis)
            self.assertNotIn("wrong_patterns", axis)

    def test_normalizer_supports_complete_axis_status_vocabulary(
        self,
    ) -> None:
        axes = [
            _axis(
                axis_id=f"axis_{index}",
                claim=f"canonical claim {index}",
            )
            for index, _ in enumerate(sorted(STATUS_VALUES), start=1)
        ]
        raw = {
            "alignments": [
                _raw_alignment(
                    status=status,
                    claim_signature=f"claim_{index}",
                    criticality=(
                        "fatal_core"
                        if status == "FATAL_CONTRADICTION"
                        else "core"
                    ),
                )
                for index, status in enumerate(
                    sorted(STATUS_VALUES),
                    start=1,
                )
            ]
        }

        normalized = (
            evaluator._normalize_canonical_axis_alignment_response(
                raw,
                canonical_axes=axes,
            )
        )

        statuses = {
            row["status"]
            for row in normalized["alignments"]
        }
        self.assertEqual(STATUS_VALUES, statuses)

    def test_low_confidence_cannot_be_fatal(
        self,
    ) -> None:
        raw = {
            "alignments": [
                _raw_alignment(
                    status="FATAL_CONTRADICTION",
                    claim_signature="ambiguous_claim",
                    confidence=0.49,
                    criticality="fatal_core",
                )
            ]
        }

        normalized = (
            evaluator._normalize_canonical_axis_alignment_response(
                raw,
                canonical_axes=[
                    _axis(
                        axis_id="ambiguous",
                        claim="canonical claim",
                        criticality="fatal_core",
                    )
                ],
            )
        )
        row = normalized["alignments"][0]

        self.assertNotEqual("FATAL_CONTRADICTION", row["status"])
        self.assertFalse(row.get("fatal", False))

    def test_missing_provenance_cannot_be_fatal(
        self,
    ) -> None:
        raw = {
            "alignments": [
                _raw_alignment(
                    status="FATAL_CONTRADICTION",
                    claim_signature="missing_provenance",
                    confidence=0.99,
                    criticality="fatal_core",
                    anchor_refs=[],
                    demand_refs=[],
                )
            ]
        }

        normalized = (
            evaluator._normalize_canonical_axis_alignment_response(
                raw,
                canonical_axes=[
                    _axis(
                        axis_id="missing_provenance",
                        claim="canonical claim",
                        criticality="fatal_core",
                        anchor_refs=[],
                        demand_refs=[],
                    )
                ],
            )
        )
        row = normalized["alignments"][0]

        self.assertNotEqual("FATAL_CONTRADICTION", row["status"])
        self.assertFalse(row.get("fatal", False))

    def test_only_direct_contradictions_become_findings(
        self,
    ) -> None:
        rows = [
            _raw_alignment(
                status=status,
                claim_signature=f"claim_{status.lower()}",
                criticality=(
                    "fatal_core"
                    if status == "FATAL_CONTRADICTION"
                    else "core"
                ),
            )
            for status in (
                "ALIGNED",
                "PARTIAL",
                "OFF_AXIS",
                "UNSUPPORTED",
                "CONTRADICTED",
                "FATAL_CONTRADICTION",
            )
        ]
        normalized = (
            evaluator._normalize_canonical_axis_alignment_response(
                {"alignments": rows},
                canonical_axes=[
                    _axis(
                        axis_id=f"axis_{index}",
                        claim=f"canonical {index}",
                        criticality=(
                            "fatal_core"
                            if index == 6
                            else "core"
                        ),
                    )
                    for index in range(1, 7)
                ],
            )
        )

        findings = evaluator._canonical_axis_alignment_to_findings(
            normalized
        )

        signatures = {
            finding["claim_signature"]
            for finding in findings
        }
        self.assertEqual(
            {
                "claim_contradicted",
                "claim_fatal_contradiction",
            },
            signatures,
        )

    def test_generated_findings_preserve_stage21_metadata_without_scores(
        self,
    ) -> None:
        normalized = {
            "alignments": [
                _raw_alignment(
                    status="CONTRADICTED",
                    claim_signature="unit_test.targets.random_integrity",
                ),
                _raw_alignment(
                    status="FATAL_CONTRADICTION",
                    claim_signature=(
                        "integration_test.exclusively_establishes."
                        "architectural_constraints"
                    ),
                    criticality="fatal_core",
                ),
            ]
        }

        findings = evaluator._canonical_axis_alignment_to_findings(
            normalized
        )

        self.assertEqual(2, len(findings))
        for finding in findings:
            self.assertTrue(STAGE21_METADATA_KEYS.issubset(finding))
            self.assertTrue(finding["anchor_refs"])
            self.assertTrue(finding["demand_refs"])
            self.assertTrue(finding["claim_signature"])
            self.assertFalse(FORBIDDEN_SCORE_KEYS & set(finding))

        severity_by_signature = {
            finding["claim_signature"]: finding["severity"]
            for finding in findings
        }
        self.assertNotEqual(
            "fatal",
            severity_by_signature[
                "unit_test.targets.random_integrity"
            ],
        )
        self.assertEqual(
            "fatal",
            severity_by_signature[
                "integration_test.exclusively_establishes."
                "architectural_constraints"
            ],
        )

    def test_duplicate_contradictions_are_deduplicated(
        self,
    ) -> None:
        row = _raw_alignment(
            status="FATAL_CONTRADICTION",
            claim_signature="duplicate.relationship",
            criticality="fatal_core",
            anchor_refs=["A1", "A1"],
            demand_refs=["D1", "D1"],
        )

        findings = evaluator._canonical_axis_alignment_to_findings(
            {"alignments": [row, copy.deepcopy(row)]}
        )

        self.assertEqual(1, len(findings))
        self.assertEqual(["A1"], findings[0]["anchor_refs"])
        self.assertEqual(["D1"], findings[0]["demand_refs"])

    def test_vmodel_relationship_errors_need_no_new_wrong_claim_rules(
        self,
    ) -> None:
        rows = [
            _raw_alignment(
                status="FATAL_CONTRADICTION",
                claim_signature=(
                    "unit_test.exclusively_establishes."
                    "random_hardware_integrity"
                ),
                criticality="fatal_core",
                answer_claim=(
                    "Unit Test exclusively establishes "
                    "Random Hardware Integrity."
                ),
                canonical_claim=(
                    "Unit Test verifies software units and contributes "
                    "to systematic capability."
                ),
            ),
            _raw_alignment(
                status="FATAL_CONTRADICTION",
                claim_signature=(
                    "integration_test.exclusively_establishes."
                    "architectural_constraints"
                ),
                criticality="fatal_core",
                answer_claim=(
                    "Integration Test exclusively establishes "
                    "Architectural Constraints."
                ),
                canonical_claim=(
                    "Integration Test verifies software architecture "
                    "and interfaces; HFT/SFF remain hardware axes."
                ),
            ),
            _raw_alignment(
                status="FATAL_CONTRADICTION",
                claim_signature=(
                    "system_test.exclusively_establishes."
                    "systematic_integrity"
                ),
                criticality="fatal_core",
                answer_claim=(
                    "System Test alone establishes "
                    "Systematic Integrity."
                ),
                canonical_claim=(
                    "V-model verification stages collectively support "
                    "systematic capability; System Test is not an "
                    "exclusive one-to-one owner."
                ),
            ),
        ]

        findings = evaluator._canonical_axis_alignment_to_findings(
            {"alignments": rows}
        )

        self.assertEqual(3, len(findings))
        self.assertTrue(
            all(
                finding["severity"] == "fatal"
                for finding in findings
            )
        )
        self.assertTrue(
            all(
                "wrong_pattern" not in finding
                and "wrong_patterns" not in finding
                for finding in findings
            )
        )


class Stage22CanonicalAxisContractPresenceTests(unittest.TestCase):
    def test_required_stage22_symbols_exist(self) -> None:
        missing = [
            name
            for name in REQUIRED_SYMBOLS
            if not hasattr(evaluator, name)
        ]
        self.assertEqual(
            [],
            missing,
            "Missing Stage22 helpers: " + ", ".join(missing),
        )

    def test_current_topic_pack_has_no_new_axis_schema_fields(
        self,
    ) -> None:
        forbidden = {
            "canonical_axes",
            "axis_contract",
            "answer_claims",
            "alignment_contract",
        }
        for name in (
            "fact_anchor.json",
            "logic_check.json",
            "model_answer.json",
            "topic_importance.json",
        ):
            data = _load_json(name)
            self.assertFalse(
                forbidden & set(data),
                f"{name} unexpectedly changed schema",
            )


if __name__ == "__main__":
    unittest.main()
