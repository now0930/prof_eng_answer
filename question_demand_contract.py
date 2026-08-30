"""Question-only grading demand contract.

The contract derives one primary grading lens and zero or more secondary
demands from the question text only. Answer text is never accepted.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

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



# STAGE35E2_EXPLICIT_QUESTION_SCOPE_AND_CANONICAL_LENS_V1
def extract_explicit_question_scope(value: Any) -> str:
    """Return an explicit problem statement without answer-body contamination."""
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKC", text).replace("\ufe0f", "")
    text = re.sub(r"^\s*/grade\b", "", text, flags=re.IGNORECASE).strip()

    separator = re.search(r"={20,}", text)
    if separator:
        prefix = text[: separator.start()].strip()
        problem = re.search(r"(?:^|\n)\s*문제\s*:\s*(.+)", prefix, re.DOTALL)
        return (problem.group(1) if problem else prefix).strip()

    if "문제 정의" in text or "[화학 플랜트]" in text:
        body_marker = re.search(
            r"(?:^|\n)\s*(?:[🔹▶▷■□●○◆◇※★☆]\s*)?"
            r"1\s*[.)]\s*배경(?:\s*\([^\n]*\))?",
            text,
            flags=re.IGNORECASE,
        )
        if body_marker:
            return text[: body_marker.start()].strip()

    return text.strip()

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



# STAGE18B2_CANONICAL_QTYPE_AND_SCORE_SOURCE_V2
def _canonical_primary_lens(
    value: Any,
) -> str:
    allowed = _ALLOWED_PRIMARY_LENSES
    seen: set[int] = set()

    def walk(
        node: Any,
        *,
        allow_id: bool = False,
    ) -> str:
        if isinstance(node, str):
            normalized = node.strip().upper()

            if normalized in allowed:
                return normalized

            return ""

        if not isinstance(node, dict):
            return ""

        object_id = id(node)

        if object_id in seen:
            return ""

        seen.add(object_id)

        direct_keys = [
            "primary_lens",
            "question_type",
            "type_id",
        ]

        if allow_id:
            direct_keys.append("id")

        for key in direct_keys:
            resolved = walk(
                node.get(key)
            )

            if resolved:
                return resolved

        primary_type = node.get(
            "primary_type"
        )

        if isinstance(primary_type, dict):
            resolved = walk(
                primary_type,
                allow_id=True,
            )

            if resolved:
                return resolved

        for key in (
            "question_type_evaluation",
            "question_type_eval",
            "question_contract",
            "routing_contract",
            "parsed",
        ):
            resolved = walk(
                node.get(key)
            )

            if resolved:
                return resolved

        return ""

    return walk(value)



# STAGE35D_TOPIC_PACK_QUESTION_DEMAND_AXES_V1
_TOPIC_PACK_DEMAND_AXES_FILENAME = "question_demand_axes.json"


def _question_contains_activation_term(
    normalized_question: str,
    term: Any,
) -> bool:
    needle = normalize_question_text(term).casefold()
    haystack = normalized_question.casefold()
    if not needle:
        return False
    if re.fullmatch(r"[a-z0-9]{1,4}", needle):
        return bool(
            re.search(
                rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])",
                haystack,
            )
        )
    return needle in haystack


@lru_cache(maxsize=1)
def _load_topic_pack_demand_axis_contracts() -> tuple[dict[str, Any], ...]:
    topic_root = Path(__file__).resolve().parent / "rubrics" / "topic_packs"
    contracts: list[dict[str, Any]] = []
    if not topic_root.is_dir():
        return ()
    for path in sorted(topic_root.glob(f"*/{_TOPIC_PACK_DEMAND_AXES_FILENAME}")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if not isinstance(payload, dict):
            continue
        payload = copy.deepcopy(payload)
        payload["_source_file"] = path.relative_to(Path(__file__).resolve().parent).as_posix()
        contracts.append(payload)
    return tuple(contracts)


def _topic_pack_demand_requirements(
    normalized_question: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates: list[tuple[int, str, list[dict[str, Any]], dict[str, Any]]] = []
    for payload in _load_topic_pack_demand_axis_contracts():
        activation = payload.get("activation")
        groups = activation.get("all_term_groups") if isinstance(activation, dict) else None
        if not isinstance(groups, list) or not groups:
            continue
        matched_terms: list[str] = []
        matched = True
        for group in groups:
            if not isinstance(group, list) or not group:
                matched = False
                break
            group_hits = [
                str(term)
                for term in group
                if _question_contains_activation_term(normalized_question, term)
            ]
            if not group_hits:
                matched = False
                break
            matched_terms.extend(group_hits)
        if not matched:
            continue
        raw_requirements = payload.get("requirements")
        if not isinstance(raw_requirements, list) or not raw_requirements:
            continue
        rows: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for index, raw in enumerate(raw_requirements):
            if not isinstance(raw, dict):
                continue
            requirement_id = str(raw.get("requirement_id") or "").strip()
            demand_kind = str(raw.get("demand_kind") or "").strip()
            requirement_text = str(raw.get("requirement_text") or "").strip()
            if not requirement_id or not demand_kind or not requirement_text:
                continue
            if requirement_id in seen_ids:
                continue
            seen_ids.add(requirement_id)
            row = copy.deepcopy(raw)
            row.update({
                "requirement_id": requirement_id,
                "clause_index": index + 1,
                "demand_kind": demand_kind,
                "demand_label": str(raw.get("demand_label") or demand_kind).strip(),
                "requirement_text": requirement_text,
                "source": "topic_pack_question_demand_axes",
                "topic_id": str(payload.get("topic_id") or "").strip(),
                "source_file": payload.get("_source_file"),
                "source_json_pointer": f"$/requirements/{index}",
                "answer_text_dependency": "none",
            })
            rows.append(row)
        if not rows:
            continue
        topic_id = str(payload.get("topic_id") or "").strip()
        metadata = {
            "schema_version": payload.get("schema_version"),
            "topic_id": topic_id,
            "source_file": payload.get("_source_file"),
            "canonical_primary_lens": _canonical_primary_lens(
                payload.get("canonical_primary_lens")
            ),
            "matched_activation_terms": sorted(set(matched_terms)),
            "requirement_count": len(rows),
        }
        candidates.append((len(matched_terms), topic_id, rows, metadata))
    if not candidates:
        return [], {}
    candidates.sort(key=lambda item: (-item[0], item[1]))
    _score, _topic_id, rows, metadata = candidates[0]
    return rows, metadata

def build_question_demand_contract(
    question_text: Any,
    *,
    canonical_primary_lens: Any = None,
) -> dict[str, Any]:
    normalized = normalize_question_text(
        extract_explicit_question_scope(question_text)
    )
    topic_pack_requirements, topic_pack_metadata = (
        _topic_pack_demand_requirements(normalized)
    )
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

    generic_requirements = copy.deepcopy(requirements)
    if topic_pack_requirements:
        requirements = copy.deepcopy(topic_pack_requirements)
        all_demand_kinds = [
            row["demand_kind"]
            for row in requirements
        ]

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
    detected_primary_lens, lens_scores = _primary_lens(
        unique_demand_kinds
    )
    topic_pack_canonical_lens = _canonical_primary_lens(
        topic_pack_metadata.get("canonical_primary_lens")
        if isinstance(topic_pack_metadata, dict)
        else None
    )
    canonical_lens = (
        topic_pack_canonical_lens
        or _canonical_primary_lens(canonical_primary_lens)
    )
    primary_lens = canonical_lens or detected_primary_lens
    primary_lens_source = (
        "topic_pack_canonical_primary_lens"
        if topic_pack_canonical_lens
        else (
            "canonical_question_type_router"
            if canonical_lens
            else "question_text_pregrade_fallback"
        )
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
                "demand_label": next(
                    (
                        str(row.get("demand_label") or "").strip()
                        for row in deduped_requirements
                        if row.get("demand_kind") == demand_kind
                    ),
                    _DEMAND_LABELS.get(demand_kind, demand_kind),
                ),
                "requirement_ids": requirement_ids,
            }
        )

    return {
        "schema_version": QUESTION_DEMAND_CONTRACT_SCHEMA_VERSION,
        "contract_marker": QUESTION_DEMAND_CONTRACT_MARKER,
        "mode": "question_only_deterministic",
        "score_effect": "semantic_guidance_only",
        "answer_text_dependency": "none",
        "topic_pack_demand_axes_applied": bool(topic_pack_requirements),
        "topic_pack_demand_axes": topic_pack_metadata,
        "generic_requirements": generic_requirements,
        "normalized_question": normalized,
        "question_hash": _question_hash(normalized),
        "primary_lens": primary_lens,
        "primary_lens_source": primary_lens_source,
        "primary_lens_locked": True,
        "primary_lens_scores": lens_scores,
        "detected_primary_lens": (
            detected_primary_lens
        ),
        "canonical_primary_lens_applied": (
            bool(canonical_lens)
        ),
        "final_primary_lens_owner": (
            "topic_pack_question_demand_axes"
            if topic_pack_canonical_lens
            else (
                "canonical_question_type_router"
                if canonical_lens
                else "not_yet_available"
            )
        ),
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
    *,
    canonical_primary_lens: Any = None,
) -> Any:
    if not isinstance(result, dict):
        return result

    updated = copy.deepcopy(result)
    canonical_lens = (
        _canonical_primary_lens(
            canonical_primary_lens
        )
        or _canonical_primary_lens(
            result
        )
    )
    contract = build_question_demand_contract(
        question_text,
        canonical_primary_lens=canonical_lens,
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
    value: Any = None
    try:
        signature = inspect.signature(function)
        bound = signature.bind_partial(*args, **kwargs)
        value = bound.arguments.get("question_text")
    except (TypeError, ValueError):
        value = None

    if value is None and "question_text" in kwargs:
        value = kwargs["question_text"]
    if value is None and args:
        value = args[0]
    return extract_explicit_question_scope(value)
