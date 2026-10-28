import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from grading.scoring.deterministic_score_evidence import evaluate_score_evidence


class DeterministicScoreEvidenceTests(unittest.TestCase):
    def test_structured_engineering_answer_has_auditable_axis_evidence(self):
        answer = """1. 원리
- 공정 조건과 위험을 기준으로 선정한다.
- 현장 시험과 측정 기록으로 검증한다.
- 비용과 영향의 한계를 비교한다.
2. 절차
- 변경 후 운전 결과를 확인한다.
3. 결론
- 따라서 검증 결과를 설계에 연결한다.
"""
        result = evaluate_score_evidence(answer)
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["structure"]["score"], 3.0)
        self.assertGreaterEqual(result["engineering_judgment"]["score"], 5.0)
        self.assertGreater(result["linkage"]["score"], 0.0)

    def test_short_statement_does_not_receive_structure_or_judgment_full_credit(self):
        result = evaluate_score_evidence("센서의 원리를 설명한다.")
        self.assertLess(result["structure"]["score"], 3.0)
        self.assertLess(result["engineering_judgment"]["score"], 6.0)

    def test_design_constraints_earn_judgment_only_when_bound_to_fact_evidence(self):
        import os
        from unittest.mock import patch

        fact = "Q는 상태를, R은 제어입력을 가중한다."
        design = "단위 정규화와 입력 포화 한계를 포함해 반복 조정한다."
        with patch.dict(os.environ, {"ESSAY_STRICT_EVIDENCE_BINDING": "1"}):
            supported = evaluate_score_evidence(
                fact + design, technical_evidence_texts=[fact + design],
            )
            unrelated = evaluate_score_evidence(
                fact + design, technical_evidence_texts=[fact],
            )
        self.assertEqual(supported["engineering_judgment"]["score"], 2.5)
        self.assertEqual(unrelated["engineering_judgment"]["score"], 0.0)
        default_policy = evaluate_score_evidence(
            fact + design, technical_evidence_texts=[fact],
        )
        self.assertEqual(default_policy["engineering_judgment"]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
