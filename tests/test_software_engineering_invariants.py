import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from engineering_invariant_evaluator import evaluate_engineering_invariants


class SoftwareEngineeringInvariantTests(unittest.TestCase):
    def test_operational_fixture_detects_all_four_software_invariants(self):
        fixture = json.loads(
            (REPO / "calibration/mcdc_vmodel_sil_overgrading_regression.json")
            .read_text(encoding="utf-8")
        )
        answer = fixture.get("answer") or fixture["original_answer"]
        codes = {row["code"] for row in evaluate_engineering_invariants(answer)["violations"]}
        self.assertEqual(codes, {
            "CODING_GUIDELINE_AS_UNIT_TEST_TOOL",
            "SOFTWARE_TEST_AS_RANDOM_HARDWARE_INTEGRITY",
            "HARDWARE_ARCHITECTURE_AS_INTEGRATION_TEST",
            "UNQUALIFIED_UNIVERSAL_SIL4_MCDC_RULE",
        })

    def test_correct_role_mappings_are_not_flagged(self):
        variants = (
            "MISRA는 코딩 지침이며 단위시험 도구로 분류하지 않는다.",
            "소프트웨어 단위시험은 systematic 결함을 다루고 Random Hardware Integrity는 별도 평가한다.",
            "HFT는 하드웨어 아키텍처 제약이고 통합시험과는 다른 분류축이다.",
            "SIL 4에서 MC/DC 100% 적용 여부는 적용 표준에 따라 결정한다.",
        )
        for answer in variants:
            with self.subTest(answer=answer):
                self.assertEqual(evaluate_engineering_invariants(answer)["violations"], [])

    def test_role_mutations_are_detected(self):
        variants = {
            "단위시험의 적용 도구는 MISRA C이다.": "CODING_GUIDELINE_AS_UNIT_TEST_TOOL",
            "소프트웨어 통합시험은 Random Hardware Integrity의 직접 통제수단이다.": "SOFTWARE_TEST_AS_RANDOM_HARDWARE_INTEGRITY",
            "통합시험은 HFT를 확인하는 시험단계다.": "HARDWARE_ARCHITECTURE_AS_INTEGRATION_TEST",
            "모든 SIL4 소프트웨어는 MC/DC 100%가 반드시 필요하다.": "UNQUALIFIED_UNIVERSAL_SIL4_MCDC_RULE",
        }
        for answer, code in variants.items():
            with self.subTest(answer=answer):
                self.assertIn(code, {row["code"] for row in evaluate_engineering_invariants(answer)["violations"]})


if __name__ == "__main__":
    unittest.main()
