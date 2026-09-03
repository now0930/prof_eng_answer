"""Adversarial text transformations cannot be turned into score uplift later."""

from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verified_evidence_score_calibration import apply_verified_evidence_score_calibration


def _grade(answer_text: str, *, c_score: float = 4.0) -> dict:
    rows = [
        {"layer_id": "A", "score": 2.0, "max": 3.0},
        {"layer_id": "B", "score": 3.0, "max": 6.0},
        {"layer_id": "C", "score": c_score, "max": 8.0},
        {"layer_id": "D", "score": 3.5, "max": 6.0},
        {"layer_id": "E", "score": 1.0, "max": 2.0},
    ]
    total = round(sum(row["score"] for row in rows), 2)
    return {
        "answer_text": answer_text,
        "total_score": total,
        "final_total_score": total,
        "breakdown": rows,
        "volume_evaluation": {"ascii_equivalent_count": len(answer_text) * 3},
    }


def _score_view(grade: dict) -> tuple:
    return grade["total_score"], tuple(row["score"] for row in grade["breakdown"])


def test_repetition_keywords_irrelevant_text_synonyms_and_order_are_score_neutral() -> None:
    baseline = _grade("원리와 검증방법을 설명한다.")
    variants = (
        baseline,
        _grade("원리와 검증방법을 설명한다. " * 30),
        _grade("SIL V-Model HIL MC/DC Traceability " * 50),
        _grade("원리와 검증방법을 설명한다. 무관한 결론과 반복 문장을 추가한다." * 15),
        _grade("검증방법과 원리를 설명한다."),
        _grade("원리 및 검증 절차를 서술한다."),
    )
    expected = _score_view(baseline)
    for variant in variants:
        result = apply_verified_evidence_score_calibration(copy.deepcopy(variant))
        assert _score_view(result) == expected
        assert result["verified_evidence_score_calibration"]["score_effect"] == "none"


def test_lower_c_evidence_is_not_masked_by_padding_or_plausible_wrong_text() -> None:
    supported = _grade("핵심 기술관계를 정확히 설명한다.", c_score=6.0)
    corrupted = _grade("그럴듯하지만 핵심 기술관계를 반대로 설명한다. " * 20, c_score=3.0)
    supported_result = apply_verified_evidence_score_calibration(supported)
    corrupted_result = apply_verified_evidence_score_calibration(corrupted)
    assert corrupted_result["breakdown"][2]["score"] < supported_result["breakdown"][2]["score"]
    assert corrupted_result["total_score"] < supported_result["total_score"]


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"SCORE_PADDING_INVARIANCE_TESTS={len(tests)}_PASS")
