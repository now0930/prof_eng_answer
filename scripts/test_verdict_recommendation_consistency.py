from __future__ import annotations

import copy
import unittest

import grade_output_summarizer
from verdict_consistency import (
    VERDICT_CONSISTENCY_MARKER,
    reconcile_verdict_summary,
)


# VERDICT_RECOMMENDATION_CONSISTENCY_REGRESSION_V1


def payload(
    *,
    defects=None,
    requirements=None,
    demand_requirements=None,
    fatal=False,
):
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
            "defects": list(defects or []),
            "field_judgements": [],
            "summary": {},
        },
        "question_demand_contract": {
            "schema_version": "1.0",
            "requirements": list(
                demand_requirements or []
            ),
        },
        "question_type_coverage": {
            "explicit_requirement_coverage": {
                "requirements": list(
                    requirements or []
                ),
            },
        },
    }


class VerdictRecommendationConsistencyTests(
    unittest.TestCase
):
    def test_depth_only_removes_false_core_error_wording(self):
        summary = {
            "headline": "THEORY_CORE 핵심 이론 오류",
            "overall": "핵심 이론 오류가 확인되었습니다.",
            "key_reasons": ["세부 해석이 부족함"],
            "section_basis": [
                "fatal 오류를 보완하지 못합니다.",
            ],
            "improvements": [
                "일반적인 기술사 답안 형식을 보완",
            ],
        }
        result = reconcile_verdict_summary(
            summary,
            payload(
                defects=[
                    {
                        "defect_id": "depth_1",
                        "defect_type": "core_depth_gap",
                        "severity": "partial",
                        "owner_layer": "C",
                        "explanation": (
                            "최악 조건의 상세 해석이 부족하다."
                        ),
                    }
                ]
            ),
        )

        rendered = str(result)

        self.assertEqual(
            result["headline"],
            "핵심 내용은 성립하나 상세 해석 보완 필요",
        )
        self.assertNotIn("핵심 이론 오류", rendered)
        self.assertNotIn("fatal 오류", rendered)
        self.assertIn(
            "핵심 해석·설계 깊이",
            result["improvements"][0],
        )

    def test_presentation_issue_does_not_claim_technical_error(self):
        result = reconcile_verdict_summary(
            {
                "headline": "핵심 이론 오류",
                "overall": "명백한 기술 오류가 있다.",
                "improvements": ["기술 오류를 수정"],
            },
            payload(
                defects=[
                    {
                        "defect_id": "formula_1",
                        "defect_type": "presentation_issue",
                        "severity": "partial",
                        "owner_layer": "C",
                        "explanation": (
                            "수식의 항 연결 연산자가 보이지 않는다."
                        ),
                    }
                ]
            ),
        )

        rendered = str(result)

        self.assertEqual(
            result["headline"],
            "핵심 내용은 유지되며 수식·표현 확인 필요",
        )
        self.assertNotIn("명백한 기술 오류", rendered)
        self.assertIn(
            "수식·표현 무결성",
            result["improvements"][0],
        )

    def test_verified_major_correctness_uses_hard_wording(self):
        result = reconcile_verdict_summary(
            {
                "headline": "상세 해석 보완 필요",
                "overall": "기본 내용은 적절하다.",
                "improvements": [],
            },
            payload(
                defects=[
                    {
                        "defect_id": "error_1",
                        "defect_type": "correctness_error",
                        "severity": "major",
                        "owner_layer": "C",
                        "explanation": "안정성 부호가 반대다.",
                    }
                ]
            ),
        )

        self.assertEqual(
            result["headline"],
            "검증된 핵심 기술 오류 보완 필요",
        )
        self.assertIn(
            "중대 기술 오류",
            result["overall"],
        )
        self.assertTrue(
            result["verdict_consistency"][
                "hard_error_wording_allowed"
            ]
        )

    def test_fulfilled_requirement_is_not_recommended(self):
        result = reconcile_verdict_summary(
            {
                "headline": "채점 결과",
                "overall": "요약",
                "improvements": [
                    "정의와 설계를 모두 다시 작성",
                ],
            },
            payload(
                requirements=[
                    {
                        "requirement_id": "r_define",
                        "status": "present",
                        "is_core": True,
                    },
                    {
                        "requirement_id": "r_design",
                        "status": "missing",
                        "is_core": True,
                    },
                ],
                demand_requirements=[
                    {
                        "requirement_id": "r_define",
                        "demand_label": "정의·개념 설명",
                    },
                    {
                        "requirement_id": "r_design",
                        "demand_label": "설계·설계 기준",
                    },
                ],
            ),
        )

        improvements = " ".join(
            result["improvements"]
        )

        self.assertNotIn("정의·개념 설명", improvements)
        self.assertIn("설계·설계 기준", improvements)
        self.assertNotIn(
            "정의와 설계를 모두 다시 작성",
            improvements,
        )

    def test_verified_logic_fatal_overrides_generic_wording(self):
        original = {
            "headline": "THEORY_CORE 핵심 이론 오류",
            "overall": "핵심 이론 오류가 확인되었습니다.",
            "improvements": ["fatal 오류 수정"],
        }
        result = reconcile_verdict_summary(
            original,
            payload(fatal=True),
        )

        self.assertEqual(
            result["headline"],
            "검증된 핵심 기술 오류 보완 필요",
        )
        self.assertIn(
            "검증된 핵심 기술 오류",
            result["overall"],
        )
        self.assertEqual(
            result["verdict_consistency"]["mode"],
            "preserve_verified_logic_fatal",
        )

    def test_reconciliation_is_score_neutral(self):
        source_payload = payload(
            defects=[
                {
                    "defect_type": "core_depth_gap",
                    "severity": "partial",
                    "owner_layer": "D",
                    "explanation": "검증 조건 부족",
                }
            ]
        )
        source_payload["total_score"] = 18.0
        source_payload["layer_scores"] = [
            {"layer_id": "D", "score": 4.5},
        ]
        before = copy.deepcopy(source_payload)

        reconcile_verdict_summary(
            {
                "headline": "요약",
                "overall": "요약",
                "improvements": [],
            },
            source_payload,
        )

        self.assertEqual(source_payload, before)

    def test_build_payload_exposes_structured_contracts(self):
        grade = {
            "score": 18.0,
            "max_score": 25.0,
            "parsed": {
                "general_evidence_contract": {
                    "mode": "diagnostic_only",
                    "defects": [],
                },
                "question_demand_contract": {
                    "mode": "question_only_deterministic",
                    "requirements": [],
                },
                "question_type_coverage": {
                    "overall_coverage": "adequate",
                },
            },
        }

        built = grade_output_summarizer._build_payload(
            grade
        )

        self.assertIn(
            "general_evidence_contract",
            built,
        )
        self.assertIn(
            "question_demand_contract",
            built,
        )
        self.assertIn(
            "question_type_coverage",
            built,
        )

    def test_effective_normaliser_uses_structured_policy(self):
        source_payload = payload(
            defects=[
                {
                    "defect_type": "presentation_issue",
                    "severity": "warning",
                    "owner_layer": "C",
                    "explanation": "변수 정의가 불명확하다.",
                }
            ]
        )

        result = grade_output_summarizer._normalise_summary(
            {
                "headline": "핵심 이론 오류",
                "overall": "명백한 오류가 있다.",
                "key_reasons": [],
                "section_basis": [],
                "improvements": [
                    "일반적인 내용을 보완",
                ],
            },
            source_payload,
        )

        self.assertEqual(
            result["headline"],
            "핵심 내용은 유지되며 수식·표현 확인 필요",
        )
        self.assertEqual(
            result["verdict_consistency"]["marker"],
            VERDICT_CONSISTENCY_MARKER,
        )


def _check_grading_consistency_documentation() -> None:
    # Validate the canonical project-wide grading-consistency documentation.
    import re as _grading_consistency_re
    from pathlib import Path as _GradingConsistencyPath

    _root = _GradingConsistencyPath(__file__).resolve().parents[1]
    _canonical_path = _root / "docs" / "grading_architecture.md"
    _linked_docs = (
        _root / "docs" / "topic_pack_workflow.md",
        _root / "docs" / "rubric_authoring_guide.md",
    )
    _readme_path = _root / "README.md"
    _markers = ('QUESTION_AXIS_FIRST',
 'ANSWER_AXIS_ALLOWED',
 'AXIS_CONSISTENCY_EARNS_LIMITED_CREDIT',
 'AXIS_CREDIT_DOES_NOT_IMPLY_FACT_CREDIT',
 'MENTION_IS_NOT_VERIFIED_COVERAGE',
 'NO_SUPPORT_NO_POSITIVE_FACT_CREDIT',
 'UNSUPPORTED_IS_NOT_AUTOMATICALLY_WRONG',
 'CONTRADICTION_ONLY_TRIGGERS_ERROR_PENALTY',
 'ENGINEERING_CREDIT_REQUIRES_TRUSTED_PREMISES',
 'STRONG_REQUIRES_FACT_SUPPORT_AND_AXIS_COHERENCE',
 'GENERALIZED_FIX_BEFORE_CASE_SPECIFIC_RULE',
 'SOURCE_FIRST_GENERATED_BY_BUILD_ONLY',
 'DOCUMENTATION_CHANGES_WITH_CONTRACT')
    _required_phrases = ('답안이 모범답안과 다른 축을 선택해도',
 '`UNSUPPORTED`: Fact 가산 금지, 자동 감점 금지',
 '축 일관성은 Fact 정확성이나 요구사항 100% 충족을 자동으로 의미하지 않는다',
 '미검증 기술 주장을 기술사 판단이나 현장성 점수로 우회 가산하지 않는다',
 '`strong` 판정은 핵심 요구별 검증된 Fact',
 '개별 답안의 모든 틀린 문장을 규칙으로 추가하지 않는다',
 'generated 파일은 build 결과이며 직접 수정하지 않는다')
    _prohibited_topic_specific_paths = (
        _root
        / "docs"
        / "topic_sheets"
        / (
            "sis_sil_safety_software_independence_"
            "systematic_failure_verification_validation.md"
        ),
        _root
        / "scripts"
        / "test_control_valve_authority_rangeability_gain_topic.py",
    )

    def _read_required_document(path: _GradingConsistencyPath) -> str:
        if not path.is_file():
            raise AssertionError(
                f"missing required file: {path.relative_to(_root)}"
            )
        return path.read_text(encoding="utf-8")

    _canonical = _read_required_document(_canonical_path)

    for _marker in _markers:
        _count = _canonical.count(_marker)
        if _count != 1:
            raise AssertionError(
                f"canonical marker count mismatch: {_marker}={_count}"
            )

    for _phrase in _required_phrases:
        if _phrase not in _canonical:
            raise AssertionError(f"missing canonical phrase: {_phrase}")

    if "## 12.1 최종 판정 일관성 계약" not in _canonical:
        raise AssertionError(
            "existing 12.1 최종 판정 일관성 계약 section was not preserved"
        )

    _nested_heading = _grading_consistency_re.search(
        r"^#{3,6}\s+공통 판정 경계와 실행 계약\s*$",
        _canonical,
        _grading_consistency_re.MULTILINE,
    )
    if not _nested_heading:
        raise AssertionError(
            "nested consistency augmentation heading missing"
        )

    _linked_marker_total = 0
    for _path in _linked_docs:
        _text = _read_required_document(_path)
        if "grading_architecture.md" not in _text:
            raise AssertionError(
                f"canonical link missing: {_path.relative_to(_root)}"
            )
        if "채점 일관성 정본" not in _text:
            raise AssertionError(
                f"normative link note missing: {_path.relative_to(_root)}"
            )
        _linked_marker_total += sum(
            _text.count(_marker) for _marker in _markers
        )

    if _linked_marker_total != 0:
        raise AssertionError(
            "linked execution guides duplicate machine-readable "
            "contract markers"
        )

    _readme = _read_required_document(_readme_path)
    if "grading_architecture.md" not in _readme:
        raise AssertionError("README canonical reference missing")

    _topic_sheet = _read_required_document(
        _prohibited_topic_specific_paths[0]
    )
    if "채점 일관성 정본" in _topic_sheet:
        raise AssertionError(
            "Topic-specific sheet received project-wide link"
        )

    _control_valve_test = _read_required_document(
        _prohibited_topic_specific_paths[1]
    )
    if "NO_SUPPORT_NO_POSITIVE_FACT_CREDIT" in _control_valve_test:
        raise AssertionError(
            "Topic-specific control-valve test owns project-wide contract"
        )

    print("CANONICAL_MARKERS=13_OF_13_PASS")
    print("CANONICAL_REQUIRED_PHRASES=7_OF_7_PASS")
    print("LINKED_DOCUMENTS=2_OF_2_PASS")
    print("README_REFERENCE=PASS")
    print("TOPIC_SPECIFIC_LINK_EXCLUSION=PASS")
    print("TOPIC_SPECIFIC_TEST_OWNER_EXCLUSION=PASS")


if __name__ == "__main__":
    _check_grading_consistency_documentation()
    unittest.main()
