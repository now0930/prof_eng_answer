"""Stage23 generic grading engine fixtures.

The two cases are copied from existing production sessions and are fixtures for
the generic engine only. They are not topic-pack data, fact anchors, or model
answers.

This file intentionally contains nine RED integration tests. Stage23E confirms
that all nine fail against the current production wiring.
"""

from __future__ import annotations

import ast
import importlib
import unittest
from pathlib import Path
from typing import Any

from generic_grading_contract import (
    AlignmentStatus,
    ClaimRelationType,
    DERequirementClass,
    DemandAssessment,
    DemandState,
    EvidenceTrustTier,
    classify_de_requirement,
    contract_snapshot,
    de_penalty_allowed,
    demand_matrix_summary,
    evidence_credit_weight,
    structured_consistency_issues,
)

ROOT = Path(__file__).resolve().parent
FIXTURES: dict[str, dict[str, Any]] = {'A': {'label': 'A',
       'session_id': '20260822_003132_5960502198',
       'question': '제어 소프트웨어 개발 수명 주기(V-model)에 따른 단위 시험, 통합 시험, 시스템 시험의 정의와 SIL 달성을 위한 소프트웨어 검증 '
                   '방안을 설명',
       'answer': '\u200b[문제] 제어 소프트웨어 개발 수명 주기(V-model) 따른 단위 시험, 통합 시험, 시스템 시험의 정의, 안전 무결성(SIL) '
                 '달성을 위한 소프트웨어 검증 방안을 설명\n'
                 '\u200b1. 배경: V-Model과 SIL에 대한 배경 설명\n'
                 '\u200bV-model: 폭포수 모델 변형. 개발과 테스트를 병행하여 안전 필수 시스템의 결함을 제거함. 요구사항 추적 Matrix로 정합성 '
                 '검증.  \n'
                 '\u200b단점: 문서화 및 테스트 공수로 개발 기간/비용 증가 (Trade-off 발생).  \n'
                 '\u200bSIL (Safety Integrity Level): SIS/SIF가 갖춰야 할 안전 성능 요구사항 (PFD_{avg} 기준 SIL '
                 '1~4).  \n'
                 '\u200b연계성: V-Model의 단계별 검증을 통해 Systematic Fault 및 Random Fault를 차단함.  \n'
                 '\u200b2. 본문\n'
                 '\u200b1) 단위·통합·시스템 시험 정의 및 비교\n'
                 '\u200b단위 시험: 모듈/함수 단위 로직 검증. C0/C1 커버리지, 한계값 검증.  \n'
                 '\u200b통합 시험: 모듈 간 인터페이스, SW 아키텍처 및 통신 프로토콜 검증.  \n'
                 '\u200b시스템 시험: HW+SW 통합 SIS 전체의 SRS 요구사항 및 Fail-Safe 동작 검증.\n'
                 '비교 항목 (비교축)단위 시험통합 시험시스템 시험\n'
                 '검증 대상 / 도구단일 모듈 / xUnit, MISRA인터페이스 / Stub, S/W HIL전체 SIS / HIL 시뮬레이터\n'
                 'SIL 대응 요소Random IntegrityArch. Constraints (HFT 0,1,2)Systematic Integrity\n'
                 '2) V-model 장단점\n'
                 '\u200b장점: 단계별 즉시 결함 수정 가능, 높은 검증 신뢰성 확보.  \n'
                 '\u200b단점: 작성 문서 및 테스트 작업량 과다.  \n'
                 '\u200b3) SIL 달성을 위한 소프트웨어 검증 방안\n'
                 '\u200bSystematic Integrity: 정적 분석(MISRA C), 동적 분석(SIL 3/4 시 MC/DC 100%), '
                 'Fail-Safe 로직 검증.  \n'
                 '\u200bRandom Integrity: PFD_{avg} 제어, 타임아웃/체크섬 구현, Fault Injection(결함 주입) 시험.  \n'
                 '\u200bArchitectural Constraints: HFT(1oo2, 2oo3) 이중화 검증, '
                 'HIL(Hardware-in-the-Loop) 시뮬레이션 기반 실시간 모의 검증.  \n'
                 '\u200b3. 결론\n'
                 '\u200bV-model은 SIL 달성을 위한 가장 확실한 검증 수단임.  \n'
                 '\u200b문서화/코드량 과다 단점은 Agentic AI(Test Case/Harness 자동 생성)로 상쇄 가능.  \n'
                 '\u200bAI 활용 시에도 시험 격리 환경(Sandbox) 구축 및 전문가 Review Know-how가 필수적임.',
       'answer_sha256': '1928a93587eafa942cd509a1c9e8e5468f4d39a54472ef4eed7fed2f5f62bf6d',
       'source_path': 'input.raw.txt',
       'baseline_score': 19.16,
       'baseline_question_type': 'COMPARE_SELECTION',
       'baseline_false_claim_flags': ['SYSTEM_SYSTEMATIC_INTEGRITY',
                                      'MCDC_ALWAYS_100',
                                      'VMODEL_RANDOM_FAULT_BLOCK',
                                      'MISRA_UNIT_TEST_TOOL'],
       'baseline_generic_de_feedback': True,
       'baseline_exact_fact_narrative': False,
       'baseline_provenance_present': 0,
       'baseline_provenance_missing': 6,
       'extraction_confidence_score': 296.46},
 'B': {'label': 'B',
       'session_id': '20260822_003300_5960502198',
       'question': '제어 소프트웨어 개발 수명 주기(V-model)에 따른 단위 시험, 통합 시험, 시스템 시험의 정의와 SIL 달성을 위한 소프트웨어 검증 '
                   '방안을 설명',
       'answer': '문제: 제어 소프트웨어 개발 수명 주기 (V-model) 따른 단위 시험, 통합 시험, 시스템 시험 정의. 안전 무결성 (SIL) 달성을 위한 '
                 '소프트웨어 검증 방안을 설명\n'
                 '1. 배경.: V-model과 SIL에 대한 배경 설명\n'
                 ' * V-model : 전통적 모델로 폭포수 모델에서 변형. 안정적인 소프트웨어 개발을 위해 개발과 테스트를 같이 진행. 추적 matrix '
                 '필요. 요구사항이 정확하게 반영되어 있는지 검증.\n'
                 ' * V-Model 단점: 안정적인 소프트웨어 작성 가능하나, 문서화에 시간 많이 필요. 구현, 테스트에 따라 개발 기간 증가.\n'
                 ' * SIL: Safety Instrument Level. 기기. 시스템이 안정적으로 동작하기 위한 성능 요구 사항.\n'
                 '   * SIS는 설비 시스템의 BPCS위에서 독립적으로 동작.\n'
                 '   * SIS를 만족하기 위해서는 SIF를 세부적으로 정의.\n'
                 '   * SIL은 SIF가 필요한 성능 요구사항.\n'
                 '2. 본문.\n'
                 '1) 단위 시험, 통합 시험, 시스템 시험 정의\n'
                 ' * 시스템 설계, 아키텍쳐 설계, 단위\n'
                 '   * 1 V-model은 설계, 구현, 단위 시험, 통합 시험, 시스템 시험순으로 진행됨.\n'
                 '   * 2 단위 시험은 단위 설계, 구현된 모든 기능이 사양서에 명기된 수치 이상 달성을 확인하는 과정.\n'
                 '   * 3 통합 시험은 아키텍쳐 설계가 사양을 만족하는지 확인하는 과정.\n'
                 '   * 4 시스템 시험은 사양에 명기된 시스템이 만족하는지 평가.\n'
                 '2) V-model 장단점\n'
                 ' * 시험은 구분 후 즉시 수행되어야 하고, 시험 과정 중 발생하는 문제는 바로 수정.\n'
                 ' * 그리고 구현과 테스트를 같이 수행하여 작업량이 많고 문서를 많이 만들어야 함.\n'
                 '3) SIL 달성을 위한 소프트웨어 검증 방안\n'
                 ' * 1 SIL은 SIF가 달성해야 하는 성능 수준.\n'
                 ' * 2 SIF는 센서+ 제어기+ FCE 등으로 구성됨.\n'
                 ' * 3 SIL은 $PFD_{avg}$로 표현되고 SIL1, 2, 3, 4 4가지가 있음.\n'
                 ' * 4 SIL을 달성하기 위해서는 3가지 필요:\n'
                 '   * a. Systematic Integrity: 시스템이 정확하게 동작\n'
                 '   * b. Random Integrity: 단위 설비의 $PFD_{avg}$에 영향\n'
                 '   * c. Architectural Constraints: 리던던시에 영향\n'
                 ' * 5 각 시험은 위 3가지에 대응하여 시행:\n'
                 '   * 단위 시험은 Random Integrity 달성을 목표.\n'
                 '   * 통합 시험은 Architectural Constraints 달성 목표 (Hardware Fault-Tolerance. HFT0, 1, '
                 '2)\n'
                 '   * 시스템 시험은 Systematic Integrity 달성을 검증 (Fail Safe)\n'
                 '3. 결론\n'
                 ' * V-model은 검증된 SIL 달성 수단임.\n'
                 ' * 단점으로 문서화, 작업이 많고 작성코드가 많음.\n'
                 ' * 그러나 검증은 확실하게 가능.\n'
                 ' * 오래된 설비 migration, 신규 장비의 SIL 달성을 위해 V-model 적극 사용.\n'
                 ' * 단점은 agentic AI 활용하여 상쇄가능.\n'
                 ' * 그러나 코드 품질을 향상 시키기 위해서는 계약 수립, 시험 설정, 격리의 know-how가 필요.',
       'answer_sha256': 'f36021496190785882ecd8d6689dce597eb4b1041e7eb9d48e8e4244c8b247f6',
       'source_path': 'input.normalized.txt',
       'baseline_score': 19.44,
       'baseline_question_type': 'COMPARE_SELECTION',
       'baseline_false_claim_flags': ['SAFETY_INSTRUMENT_LEVEL',
                                      'UNIT_RANDOM_INTEGRITY',
                                      'INTEGRATION_ARCH_CONSTRAINT',
                                      'SYSTEM_SYSTEMATIC_INTEGRITY',
                                      'MISRA_UNIT_TEST_TOOL'],
       'baseline_generic_de_feedback': True,
       'baseline_exact_fact_narrative': False,
       'baseline_provenance_present': 0,
       'baseline_provenance_missing': 6,
       'extraction_confidence_score': 297.79}}


def _source_has_function(path: str, function_name: str) -> bool:
    source_path = ROOT / path
    if not source_path.is_file():
        return False
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
        for node in ast.walk(tree)
    )


class GenericContractModuleGreenTests(unittest.TestCase):
    def test_demand_states(self) -> None:
        self.assertEqual([item.value for item in DemandState], ["CORRECT", "PARTIAL", "WRONG", "MISSING"])

    def test_relation_types(self) -> None:
        self.assertEqual(len(list(ClaimRelationType)), 10)

    def test_alignment_states(self) -> None:
        self.assertEqual({item.value for item in AlignmentStatus}, {"ALIGNED", "PARTIAL", "CONTRADICTED", "UNSUPPORTED", "NOT_APPLICABLE"})

    def test_evidence_tiers(self) -> None:
        self.assertEqual({item.value for item in EvidenceTrustTier}, {"DETERMINISTIC", "VERIFIED_STRUCTURED", "SEMANTIC_INFERRED", "UNSUPPORTED"})

    def test_wrong_mention_is_not_correctness_credit(self) -> None:
        summary = demand_matrix_summary([DemandAssessment(demand_id="D1", status=DemandState.WRONG, mentioned=True)])
        self.assertEqual(summary["mention_coverage_percent"], 100.0)
        self.assertEqual(summary["correctness_coverage_percent"], 0.0)
        self.assertFalse(summary["full_correct_coverage"])

    def test_evidence_credit_rejects_contradiction(self) -> None:
        self.assertEqual(evidence_credit_weight(EvidenceTrustTier.VERIFIED_STRUCTURED, AlignmentStatus.CONTRADICTED), 0.0)

    def test_unrequested_de_is_no_penalty(self) -> None:
        classification = classify_de_requirement(explicitly_requested=False)
        self.assertIs(classification, DERequirementClass.NO_PENALTY)
        self.assertFalse(de_penalty_allowed(classification))

    def test_structured_consistency_detects_false_full_coverage(self) -> None:
        issues = structured_consistency_issues(
            demand_summary={"wrong_count": 1, "missing_count": 0, "full_correct_coverage": False},
            narrative_flags={"claims_exact_fact": True, "claims_zero_wrong": True, "claims_full_coverage": True},
        )
        self.assertGreaterEqual(len(issues), 3)
        self.assertEqual(contract_snapshot()["schema_version"], "stage23.generic_grading_contract.v1")


class GenericEngineFixtureRedTests(unittest.TestCase):
    def test_red_01_router_primary_is_implementation_evaluation(self) -> None:
        from question_type_router import detect_question_type
        for fixture in FIXTURES.values():
            result = detect_question_type(fixture["question"], fixture["answer"])
            self.assertEqual(result.get("question_type"), "IMPLEMENTATION_EVALUATION")
            self.assertNotEqual(result.get("question_type"), "COMPARE_SELECTION")

    def test_red_02_router_preserves_definition_as_secondary_evidence(self) -> None:
        from question_type_router import detect_question_type
        result = detect_question_type(FIXTURES["A"]["question"], FIXTURES["A"]["answer"])
        secondary = result.get("secondary_types") or result.get("secondary_demands") or []
        normalized = {str(item.get("id") if isinstance(item, dict) else item).upper() for item in secondary}
        self.assertIn("DEFINITION_EXPLANATION", normalized)

    def test_red_03_semantic_coverage_cannot_overwrite_canonical_router_type(self) -> None:
        from semantic_question_type_postprocess import ensure_question_type_coverage
        payload = {
            "question_type": "COMPARE_SELECTION",
            "question_type_coverage": {
                "question_type": "COMPARE_SELECTION",
                "overall_coverage": "strong",
                "sub_criteria_coverage": [],
            },
        }
        result = ensure_question_type_coverage(
            payload,
            question_text=FIXTURES["A"]["question"],
            existing_question_type="IMPLEMENTATION_EVALUATION",
        )
        self.assertEqual(result.get("question_type"), "IMPLEMENTATION_EVALUATION")
        self.assertEqual(result["question_type_coverage"].get("question_type"), "IMPLEMENTATION_EVALUATION")

    def test_red_04_coverage_adapter_preserves_wrong_state(self) -> None:
        from question_type_coverage_adapter import _criteria_details
        details = _criteria_details({
            "sub_criteria_coverage": [
                {"criterion": "mapped relationship", "status": "WRONG", "evidence": "mentioned but contradicted"}
            ]
        })
        self.assertEqual(details.get("wrong_criteria"), ["mapped relationship"])
        self.assertEqual(details.get("wrong"), 1)

    def test_red_05_coverage_adapter_separates_mention_from_correctness(self) -> None:
        from question_type_coverage_adapter import attach_question_type_coverage_feedback
        grade = {
            "question_type": "IMPLEMENTATION_EVALUATION",
            "question_type_coverage": {
                "question_type": "IMPLEMENTATION_EVALUATION",
                "overall_coverage": "weak",
                "sub_criteria_coverage": [
                    {"criterion": "definition", "status": "WRONG", "evidence": "mentioned but contradicted"}
                ],
            },
        }
        result = attach_question_type_coverage_feedback(grade)
        summary = result["question_type_coverage_summary"]
        self.assertEqual(summary.get("mention_coverage_percent"), 100.0)
        self.assertEqual(summary.get("correctness_coverage_percent"), 0.0)
        self.assertEqual(summary.get("sub_criteria_wrong"), 1)

    def test_red_06_logic_evaluator_exposes_generic_relation_normalizer(self) -> None:
        self.assertTrue(_source_has_function("logic_check_evaluator.py", "normalize_generic_claim_relations"))

    def test_red_07_score_reconciler_exposes_generic_de_policy(self) -> None:
        self.assertTrue(_source_has_function("grade_score_reconciler.py", "apply_generic_de_policy"))

    def test_red_08_final_consistency_gate_exists(self) -> None:
        self.assertTrue(_source_has_function("verdict_consistency.py", "enforce_generic_contract_consistency"))

    def test_red_09_runtime_provenance_process_snapshot_exists(self) -> None:
        try:
            module = importlib.import_module("runtime_grading_provenance")
        except ModuleNotFoundError:
            self.fail("runtime_grading_provenance module is absent")
        self.assertTrue(hasattr(module, "build_runtime_grading_provenance"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
