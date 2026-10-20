"""Synthetic D/E scoring examples; calibration guidance, not answer keys."""

from __future__ import annotations

from copy import deepcopy


VERSION = "qualitative_de_prompt_examples_v1"

# These fragments are deliberately generic. They illustrate how a decision
# changes with A/B/C evidence; they do not assert facts for a live Topic.
_EXAMPLES = (
    {
        "case": "supported_choice_and_tradeoff",
        "question_demand": "두 계측 방식의 선택 조건과 오차 저감 방안을 설명",
        "abc_evidence": [
            {"claim": "방식 A의 측정 조건을 설명", "status": "SATISFIED"},
            {"claim": "방식 B의 제한 조건을 설명", "status": "PARTIAL"},
        ],
        "answer_excerpt": "고온 조건에서는 방식 A를 선택한다. 방식 B는 정밀도가 필요할 때 대안이지만 사용 범위를 확인해야 한다.",
        "de_guidance": {
            "D1": "조건을 붙인 선택은 일부 가점, 기술적 근거가 부족하여 만점 아님",
            "D2": "독립적인 기술적 근거가 없어 가점하지 않음",
            "D3": "대안과 제한을 함께 언급한 부분만 일부 가점",
            "E1_E2": "후속 설명의 근거가 없어 전문성을 추정하지 않음",
        },
        "illustrative_scores": {"D1": 1, "D2": 0, "D3": 1, "E1": 0, "E2": 0},
    },
    {
        "case": "generic_conclusion_without_supported_evidence",
        "question_demand": "현장 적용 조건을 판단",
        "abc_evidence": [{"claim": "적용 판단의 구체적 근거 없음", "status": "MISSING"}],
        "answer_excerpt": "상황에 맞게 종합적으로 판단하여 최선의 방법을 선택한다.",
        "de_guidance": {
            "D1_D2_D3": "구체적인 조건·선택·근거가 없으므로 이 문장만으로 양수 점수를 주지 않음",
            "E1_E2": "이 문장만으로 후속 기술 설명 능력을 추정하지 않음",
        },
        "illustrative_scores": {"D1": 0, "D2": 0, "D3": 0, "E1": 0, "E2": 0},
    },
    {
        "case": "contradicted_claim_cannot_support_credit",
        "question_demand": "기술적 개선 방안을 설명",
        "abc_evidence": [{"claim": "개선 원리의 반대 설명", "status": "WRONG"}],
        "answer_excerpt": "해당 오차는 아무 조건 없이 완전히 제거된다.",
        "de_guidance": {
            "D1_D2_D3": "WRONG으로 확정된 주장에는 긍정 점수를 주지 않음",
            "E1_E2": "오류를 후속 면접 질문의 전문성 근거로 사용하지 않음",
        },
        "illustrative_scores": {"D1": 0, "D2": 0, "D3": 0, "E1": 0, "E2": 0},
    },
    {
        "case": "distinct_supported_evidence_for_full_credit",
        "question_demand": "두 계측 방식의 현장 선택·근거·대안·검증을 설명",
        "abc_evidence": [
            {"claim": "선택 조건", "status": "SATISFIED"},
            {"claim": "선택 근거", "status": "SATISFIED"},
            {"claim": "대안의 제한", "status": "SATISFIED"},
            {"claim": "오차 진단", "status": "SATISFIED"},
            {"claim": "검증 절차", "status": "SATISFIED"},
        ],
        "answer_excerpt": (
            "요구 범위가 B의 허용 범위를 넘는 조건에서는 A를 선택한다. "
            "A의 교정 범위가 실제 공정 조건을 포함하는지 확인한다. "
            "B는 정밀도가 필요한 구간의 대안이지만 허용 범위를 먼저 확인한다. "
            "오차가 증가하면 배선과 센서의 영향을 분리해 원인을 진단한다. "
            "검증 시 기준 입력을 주고 측정값과 기준값의 차이를 기록한다."
        ),
        "de_guidance": {
            "D1": "명시된 조건과 선택을 연결",
            "D2": "선택의 검증 가능한 기술적 근거를 별도 제시",
            "D3": "대안과 적용 한계를 분리해 설명",
            "E1": "오차 진단에 관한 구체적인 후속 질문을 만들 수 있음",
            "E2": "기준 입력과 기록에 관한 답안 근거로 후속 설명 가능",
        },
        "illustrative_scores": {"D1": 2, "D2": 2, "D3": 2, "E1": 1, "E2": 1},
    },
)


def scoring_examples() -> list[dict]:
    """Return isolated examples so callers cannot mutate the shared policy."""
    return deepcopy(_EXAMPLES)
