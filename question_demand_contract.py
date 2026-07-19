"""Question-only grading demand contract.

The contract derives one primary grading lens and zero or more secondary
demands from the question text only. Answer text is never accepted.
"""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
import re
import unicodedata
from typing import Any, Callable

QUESTION_DEMAND_CONTRACT_SCHEMA_VERSION = "1.0"
QUESTION_DEMAND_CONTRACT_MARKER = "QUESTION_DEMAND_CONTRACT_V1"

_ALLOWED_PRIMARY_LENSES = {
    "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION",
    "IMPLEMENTATION_EVALUATION",
    "PRINCIPLE_INTERPRETATION",
}

_DEMAND_LABELS = {
    "DEFINE_EXPLAIN": "정의·개념 설명",
    "PRINCIPLE_INTERPRET": "원리·동작·해석",
    "COMPARE": "비교·차이 분석",
    "SELECT": "선정·선택 기준",
    "DIAGNOSE_CAUSE": "원인·문제·진단",
    "ACTION_IMPROVE": "대책·개선·조치",
    "PROCEDURE": "절차·방법·순서",
    "CALCULATE": "계산·산정",
    "DESIGN": "설계·설계 기준",
    "IMPLEMENT": "구현·적용·구성",
    "EVALUATE_VERIFY": "평가·검증·시험",
}

_DEMAND_PATTERNS = {
    "DEFINE_EXPLAIN": (
        r"설명",
        r"정의",
        r"개념",
        r"의미",
        r"기술하",
        r"\bdefine\b",
        r"\bexplain\b",
    ),
    "PRINCIPLE_INTERPRET": (
        r"원리",
        r"동작",
        r"메커니즘",
        r"해석",
        r"특성",
        r"관계",
        r"\bprinciple\b",
        r"\bmechanism\b",
        r"\binterpret",
    ),
    "COMPARE": (
        r"비교",
        r"차이",
        r"장단점",
        r"대비",
        r"\bcompare\b",
        r"\bdifference",
        r"\badvantage",
        r"\bdisadvantage",
    ),
    "SELECT": (
        r"선정",
        r"선택",
        r"적용\s*기준",
        r"선정\s*기준",
        r"\bselect",
        r"\bselection\b",
        r"\bchoose\b",
    ),
    "DIAGNOSE_CAUSE": (
        r"원인",
        r"문제점",
        r"고장",
        r"진단",
        r"영향",
        r"\bcause\b",
        r"\bdiagnos",
        r"\bproblem\b",
        r"\bfailure\b",
    ),
    "ACTION_IMPROVE": (
        r"대책",
        r"개선",
        r"조치",
        r"해결",
        r"저감",
        r"방지",
        r"\bcountermeasure",
        r"\bimprove",
        r"\bmitigat",
        r"\baction\b",
    ),
    "PROCEDURE": (
        r"절차",
        r"방법",
        r"순서",
        r"단계",
        r"\bprocedure\b",
        r"\bmethod\b",
        r"\bsequence\b",
    ),
    "CALCULATE": (
        r"계산",
        r"산정",
        r"구하",
        r"도출",
        r"\bcalculat",
        r"\bderive\b",
    ),
    "DESIGN": (
        r"설계",
        r"설계\s*기준",
        r"사이징",
        r"\bdesign\b",
        r"\bsizing\b",
    ),
    "IMPLEMENT": (
        r"구현",
        r"적용",
        r"구성",
        r"도입",
        r"연동",
        r"\bimplement",
        r"\bapply\b",
        r"\bconfiguration\b",
    ),
    "EVALUATE_VERIFY": (
        r"평가",
        r"검증",
        r"시험",
        r"확인",
        r"성능",
        r"\bevaluat",
        r"\bverif",
        r"\btest\b",
        r"\bperformance\b",
    ),
}

_PRIMARY_CORE_DEMANDS = {
    "COMPARE_SELECTION": {"COMPARE", "SELECT"},
    "DIAGNOSIS_ACTION": {
        "DIAGNOSE_CAUSE",
        "ACTION_IMPROVE",
    },
    "IMPLEMENTATION_EVALUATION": {
        "PROCEDURE",
        "IMPLEMENT",
        "EVALUATE_VERIFY",
    },
    "PRINCIPLE_INTERPRETATION": {
        "DEFINE_EXPLAIN",
        "PRINCIPLE_INTERPRET",
    },
}

_PRIMARY_SCORE_WEIGHTS = {
    "COMPARE_SELECTION": {
        "COMPARE": 3,
        "SELECT": 2,
    },
    "DIAGNOSIS_ACTION": {
        "DIAGNOSE_CAUSE": 3,
        "ACTION_IMPROVE": 2,
    },
    "IMPLEMENTATION_EVALUATION": {
        "IMPLEMENT": 3,
        "EVALUATE_VERIFY": 2,
        "PROCEDURE": 2,
    },
    "PRINCIPLE_INTERPRETATION": {
        "PRINCIPLE_INTERPRET": 3,
        "DEFINE_EXPLAIN": 2,
        "CALCULATE": 1,
        "DESIGN": 1,
    },
}

_PRIMARY_TIE_ORDER = (
    "COMPARE_SELECTION",
    "DIAGNOSIS_ACTION",
    "IMPLEMENTATION_EVALUATION",
    "PRINCIPLE_INTERPRETATION",
)

_COMPILED_PATTERNS = {
    demand: tuple(
        re.compile(pattern, re.IGNORECASE)
        for pattern in patterns
    )
    for demand, patterns in _DEMAND_PATTERNS.items()
}


def normalize_question_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\ufe0f", "")
    text = re.sub(r"[\u200b-\u200d\u2060]", "", text)
    text = re.sub(r"[▶▷■□●○◆◇※★☆]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _question_hash(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def _stable_id(prefix: str, value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:12]
    return f"{prefix}_{digest}"


def _split_clauses(text: str) -> list[str]:
    if not text:
        return []

    parts = re.split(
        r"(?:\n+|[.;!?。；]+|(?<=다)\s+(?=[가-힣A-Za-z0-9]))",
        text,
    )
    clauses = []

    for part in parts:
        clause = re.sub(
            r"^\s*(?:\d+[.)]|[-*•]+)\s*",
            "",
            part,
        ).strip(" ,")

        if clause:
            clauses.append(clause)

    return clauses or [text]


def _detect_demands(clause: str) -> list[str]:
    matches = []

    for demand, patterns in _COMPILED_PATTERNS.items():
        if any(pattern.search(clause) for pattern in patterns):
            matches.append(demand)

    return matches


def _primary_lens(
    demand_kinds: list[str],
) -> tuple[str, dict[str, int]]:
    scores = {
        lens: 0
        for lens in _ALLOWED_PRIMARY_LENSES
    }

    for lens, weights in _PRIMARY_SCORE_WEIGHTS.items():
        for demand in demand_kinds:
            scores[lens] += weights.get(demand, 0)

    best_score = max(scores.values(), default=0)

    if best_score <= 0:
        return "PRINCIPLE_INTERPRETATION", scores

    for lens in _PRIMARY_TIE_ORDER:
        if scores[lens] == best_score:
            return lens, scores

    return "PRINCIPLE_INTERPRETATION", scores


def build_question_demand_contract(
    question_text: Any,
) -> dict[str, Any]:
    normalized = normalize_question_text(question_text)
    clauses = _split_clauses(normalized)
    requirements = []
    all_demand_kinds = []

    for clause_index, clause in enumerate(clauses, start=1):
        demand_kinds = _detect_demands(clause)

        if not demand_kinds:
            demand_kinds = ["DEFINE_EXPLAIN"]

        for demand_kind in demand_kinds:
            payload = {
                "clause_index": clause_index,
                "demand_kind": demand_kind,
                "requirement_text": clause,
            }
            requirements.append(
                {
                    "requirement_id": _stable_id(
                        "requirement",
                        payload,
                    ),
                    "clause_index": clause_index,
                    "demand_kind": demand_kind,
                    "demand_label": _DEMAND_LABELS[demand_kind],
                    "requirement_text": clause,
                    "source": "question_text_only",
                    "answer_text_dependency": "none",
                }
            )
            all_demand_kinds.append(demand_kind)

    deduped_requirements = []
    seen_requirements = set()

    for requirement in requirements:
        key = (
            requirement["demand_kind"],
            requirement["requirement_text"],
        )

        if key in seen_requirements:
            continue

        seen_requirements.add(key)
        deduped_requirements.append(requirement)

    unique_demand_kinds = list(
        dict.fromkeys(all_demand_kinds)
    )
    primary_lens, lens_scores = _primary_lens(
        unique_demand_kinds
    )
    primary_core = _PRIMARY_CORE_DEMANDS[primary_lens]

    secondary_demands = []

    for demand_kind in unique_demand_kinds:
        if demand_kind in primary_core:
            continue

        requirement_ids = [
            requirement["requirement_id"]
            for requirement in deduped_requirements
            if requirement["demand_kind"] == demand_kind
        ]
        secondary_demands.append(
            {
                "demand_kind": demand_kind,
                "demand_label": _DEMAND_LABELS[demand_kind],
                "requirement_ids": requirement_ids,
            }
        )

    return {
        "schema_version": QUESTION_DEMAND_CONTRACT_SCHEMA_VERSION,
        "contract_marker": QUESTION_DEMAND_CONTRACT_MARKER,
        "mode": "question_only_deterministic",
        "score_effect": "semantic_guidance_only",
        "answer_text_dependency": "none",
        "normalized_question": normalized,
        "question_hash": _question_hash(normalized),
        "primary_lens": primary_lens,
        "primary_lens_source": "question_text_only",
        "primary_lens_locked": True,
        "primary_lens_scores": lens_scores,
        "secondary_demands": secondary_demands,
        "requirements": deduped_requirements,
        "summary": {
            "requirement_count": len(deduped_requirements),
            "secondary_demand_count": len(
                secondary_demands
            ),
            "demand_kinds": unique_demand_kinds,
        },
    }


def attach_question_demand_contract(
    result: Any,
    question_text: Any,
) -> Any:
    if not isinstance(result, dict):
        return result

    updated = copy.deepcopy(result)
    contract = build_question_demand_contract(
        question_text
    )
    updated["question_demand_contract"] = contract

    parsed = updated.get("parsed")

    if isinstance(parsed, dict):
        parsed["question_demand_contract"] = copy.deepcopy(
            contract
        )

    return updated


def extract_question_text_from_call(
    function: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    try:
        signature = inspect.signature(function)
        bound = signature.bind_partial(*args, **kwargs)
        value = bound.arguments.get("question_text")
        if value is not None:
            return str(value)
    except (TypeError, ValueError):
        pass

    if "question_text" in kwargs:
        return str(kwargs["question_text"])

    if args:
        return str(args[0])

    return ""
