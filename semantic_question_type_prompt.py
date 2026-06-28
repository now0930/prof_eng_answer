"""Question type guidance block for semantic graders.

This module provides prompt text for Gemini/CLOVA semantic graders.
It asks the model to check whether the answer covers the v2 question_type
sub-criteria. It does not score directly by itself.
"""

from __future__ import annotations

import json
from typing import Any

from question_type_taxonomy import (
    detect_question_type_from_text,
    get_question_type_profile,
    normalize_question_type,
)


def build_question_type_semantic_guidance(
    question_text: str | None,
    existing_question_type: str | None = None,
) -> str:
    """Return a prompt block for v2 question_type coverage evaluation."""
    if existing_question_type:
        question_type = normalize_question_type(existing_question_type)
    else:
        question_type = detect_question_type_from_text(question_text or "")

    profile = get_question_type_profile(question_type)

    payload: dict[str, Any] = {
        "question_type": question_type,
        "name_ko": profile.get("name_ko"),
        "intent": profile.get("intent"),
        "c_fact_focus": profile.get("c_fact_focus", []),
        "d_field_judgement_focus": profile.get("d_field_judgement_focus", []),
        "sub_criteria": profile.get("sub_criteria", []),
    }

    payload_text = json.dumps(payload, ensure_ascii=False, indent=2)

    return f"""
[Question Type v2 평가 지침]

아래 question_type은 별도 점수체계가 아니라, A/B/C/D/E 채점 중 C항목 Fact 기반 설명과 D항목 현장 적용·판단·제언을 점검하기 위한 lens이다.

{payload_text}

평가 시 반드시 확인할 것:
1. 답안이 sub_criteria를 언급했는지 확인한다.
2. 단순 키워드 존재 여부가 아니라, 문맥상 의미 있게 설명했는지 판단한다.
3. C항목에서는 fact, 구조, 원리, 절차, 비교축, 평가 지표 등 기술 설명의 충족도를 본다.
4. D항목에서는 현장 적용 조건, 기존 설비 영향, 비용, 유지보수, 실현 가능성, trade-off, 검증 방법을 본다.
5. IMPLEMENTATION_EVALUATION의 경우 C항목은 적용 대상·시스템 구성·절차·평가 기준이고, D항목은 적용 후 운영 판단·검증·개선·확장성이다.
6. 누락된 sub_criteria가 있으면 missing_sub_criteria에 기록한다.
7. 부분적으로만 언급되었으면 partial로 표시하고, 왜 partial인지 설명한다.

semantic evaluation JSON에는 다음 필드를 반드시 포함한다.

"question_type_coverage": {{
  "question_type": "{question_type}",
  "name_ko": "{profile.get("name_ko")}",
  "sub_criteria_coverage": [
    {{
      "criterion": "sub_criteria 이름",
      "status": "present | partial | missing",
      "evidence": "답안에서 확인되는 근거 또는 누락 설명",
      "impact": "이 항목이 C 또는 D 점수에 주는 영향"
    }}
  ],
  "c_fact_focus_coverage": {{
    "covered": ["충족된 C항목 focus"],
    "missing": ["부족한 C항목 focus"]
  }},
  "d_field_judgement_focus_coverage": {{
    "covered": ["충족된 D항목 focus"],
    "missing": ["부족한 D항목 focus"]
  }},
  "missing_sub_criteria": ["누락된 sub_criteria"],
  "overall_coverage": "strong | adequate | weak | poor",
  "scoring_hint": "A/B/C/D/E 중 어느 항목을 보수적으로 볼지 간단히 설명"
}}

주의:
- 이 평가는 최종 점수를 직접 결정하지 않는다.
- 기존 A/B/C/D/E 구조를 유지하되, C와 D 점수 판단 근거를 보강한다.
- 답안에 없는 내용을 추정해서 채워 넣지 않는다.
""".strip()


def empty_question_type_coverage(
    question_text: str | None,
    existing_question_type: str | None = None,
) -> dict[str, Any]:
    """Return a safe default coverage object."""
    if existing_question_type:
        question_type = normalize_question_type(existing_question_type)
    else:
        question_type = detect_question_type_from_text(question_text or "")

    profile = get_question_type_profile(question_type)
    return {
        "question_type": question_type,
        "name_ko": profile.get("name_ko"),
        "sub_criteria_coverage": [
            {
                "criterion": item,
                "status": "missing",
                "evidence": "semantic grader coverage was not available",
                "impact": "manual review required",
            }
            for item in profile.get("sub_criteria", [])
        ],
        "c_fact_focus_coverage": {
            "covered": [],
            "missing": profile.get("c_fact_focus", []),
        },
        "d_field_judgement_focus_coverage": {
            "covered": [],
            "missing": profile.get("d_field_judgement_focus", []),
        },
        "missing_sub_criteria": profile.get("sub_criteria", []),
        "overall_coverage": "weak",
        "scoring_hint": "question_type coverage was not evaluated by semantic grader",
    }
