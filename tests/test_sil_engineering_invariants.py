import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from engineering_invariant_evaluator import evaluate_engineering_invariants


class SilEngineeringInvariantTests(unittest.TestCase):
    def test_operational_fixture_detects_all_four_sil_invariants(self):
        fixture = json.loads(
            (REPO / "calibration/sil_target_operations_overgrading_regression.json")
            .read_text(encoding="utf-8")
        )
        result = evaluate_engineering_invariants(
            fixture.get("answer") or fixture["original_answer"]
        )
        self.assertEqual({row["code"] for row in result["violations"]}, {
            "INVALID_TARGET_PROBABILITY_FREQUENCY_PRODUCT",
            "DEMAND_MODE_DIAGNOSTIC_ROLE_CONFUSION",
            "PARTIAL_TEST_ROLE_OVERCLAIM",
            "CERTIFICATE_ASSUMPTION_AS_OPERATING_MINIMUM",
        })
        self.assertEqual(result["provider_calls"], 0)

    def test_correct_relations_and_corrections_are_not_flagged(self):
        variants = (
            "PFDavg_target은 F_tolerable/F_unmitigated로 계산한다.",
            "Demand mode는 요구 빈도로 구분하며 고장 검출은 diagnostic coverage의 문제다.",
            "PST는 full proof test를 대체하지 않으며 MTTR은 실제 수리시간이다.",
            "인증서의 시험주기는 가정이며 현장 proof test interval은 계산으로 정한다.",
            "잘못된 예: PFDavg는 허용 사건빈도와 기초 사건빈도의 곱이다.",
        )
        for answer in variants:
            with self.subTest(answer=answer):
                self.assertEqual(evaluate_engineering_invariants(answer)["violations"], [])

    def test_relation_mutations_are_detected(self):
        variants = {
            "PFDavg는 F_tolerable과 F_unmitigated의 곱이다.": "INVALID_TARGET_PROBABILITY_FREQUENCY_PRODUCT",
            "high demand는 고장 즉시 확인되고 low demand는 점검 때까지 고장을 모른다.": "DEMAND_MODE_DIAGNOSTIC_ROLE_CONFUSION",
            "PST를 적용하면 MTTR이 감소한다.": "PARTIAL_TEST_ROLE_OVERCLAIM",
            "인증 시 정한 점검 주기보다 짧게 점검할 이유는 없다.": "CERTIFICATE_ASSUMPTION_AS_OPERATING_MINIMUM",
        }
        for answer, code in variants.items():
            with self.subTest(answer=answer):
                self.assertIn(code, {row["code"] for row in evaluate_engineering_invariants(answer)["violations"]})


if __name__ == "__main__":
    unittest.main()
