import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from demand_evidence_resolution import resolve_semantic_demand_evidence


class DemandEvidenceResolutionTests(unittest.TestCase):
    def _result(self, status, quote, mentioned=True, confidence="high"):
        return {"parsed": {
            "question_demand_contract": {"requirements": [
                {"requirement_id": "D1", "requirement_text": "검증 방안"}
            ]},
            "question_type_coverage": {
                "explicit_requirement_coverage": {"requirements": [{
                    "requirement_id": "D1", "status": status,
                    "mentioned": mentioned, "evidence": "모델의 요약",
                    "evidence_quote": quote, "state_confidence": confidence,
                }]}
            },
        }}

    @staticmethod
    def _row(result):
        return result["parsed"]["question_type_coverage"][
            "explicit_requirement_coverage"
        ]["requirements"][0]

    def test_exact_answer_quote_authorizes_correct(self):
        result = resolve_semantic_demand_evidence(
            self._result("present", "추적성 매트릭스를 작성한다"),
            "검증 시 추적성 매트릭스를 작성한다.",
        )
        row = self._row(result)
        self.assertEqual(row["resolved_status"], "correct")
        self.assertTrue(row["deterministic_evidence"]["exact_answer_quote_verified"])

    def test_paraphrase_cannot_authorize_correct(self):
        result = resolve_semantic_demand_evidence(
            self._result("present", "요구사항 추적을 충분히 수행함"),
            "추적성 매트릭스를 작성한다.",
        )
        self.assertEqual(self._row(result)["resolved_status"], "partial")

    def test_quote_contradicts_missing_proposal(self):
        result = resolve_semantic_demand_evidence(
            self._result("missing", "형상 관리를 수행", mentioned=False),
            "형상 관리를 수행한다.",
        )
        self.assertEqual(self._row(result)["resolved_status"], "partial")

    def test_uncertain_missing_is_downgraded(self):
        result = resolve_semantic_demand_evidence(
            self._result("missing", "", mentioned=False, confidence="medium"),
            "형상 관리를 수행한다.",
        )
        row = self._row(result)
        self.assertEqual(row["resolved_status"], "unknown")
        self.assertTrue(row["deterministic_evidence"]["uncertainty_downgraded"])


if __name__ == "__main__":
    unittest.main()
