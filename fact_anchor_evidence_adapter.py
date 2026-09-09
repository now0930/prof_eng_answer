"""Deterministic Topic Pack Fact Anchor evidence and requirement adapter."""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable


VERSION = "fact_anchor_evidence_adapter_v1"
MARKER = "FACT_ANCHOR_EVIDENCE_ADAPTER_V1"
ROOT = Path(__file__).resolve().parent
STOP_TOKENS = {
    "그리고", "그러나", "대한", "또는", "따라", "위한", "으로", "에서", "한다",
    "설명", "정의", "적용", "확인", "포함", "구분", "평가", "검증", "필요",
    "the", "and", "for", "with", "from", "that", "this", "into", "shall",
}


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value).casefold()).strip()


def _terms(anchor: dict[str, Any]) -> list[str]:
    values = anchor.get("core_terms") or anchor.get("keywords") or []
    result: list[str] = []
    for value in values:
        normalized = _normalize(str(value))
        if len(normalized) >= 2 and normalized not in result:
            result.append(normalized)
    return result


def _anchor_tokens(anchor: dict[str, Any]) -> list[str]:
    """Return compact concept tokens from human-authored engineering statements."""
    texts = [str(anchor.get("statement") or "")]
    explanations = anchor.get("accepted_explanations") or []
    if explanations:
        texts.append(str(explanations[0]))
    result: list[str] = []
    for token in re.findall(r"[0-9a-zㄱ-ㆎ가-힣]+", _normalize(" ".join(texts))):
        if len(token) >= 2 and token not in STOP_TOKENS and token not in result:
            result.append(token)
    return result


def _tokens(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[0-9a-zㄱ-ㆎ가-힣]+", _normalize(value))
        if len(token) >= 2
    }


def _term_present(term: str, normalized_answer: str) -> bool:
    """Match an authored concept term, tolerating OCR/spacing variation."""
    if term in normalized_answer:
        return True
    compact_term = re.sub(r"[\s·_-]+", "", term)
    if len(compact_term) < 4:
        return False
    compact_answer = re.sub(r"[\s·_-]+", "", normalized_answer)
    return compact_term in compact_answer


def _question_similarity(left: str, right: str) -> float:
    """Return deterministic lexical similarity; this selects scope, not correctness."""
    left_normalized = _normalize(left)
    right_normalized = _normalize(right)
    if not left_normalized or not right_normalized:
        return 0.0
    if left_normalized == right_normalized:
        return 1.0
    left_tokens = _tokens(left_normalized)
    right_tokens = _tokens(right_normalized)
    token_score = (
        len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
        if left_tokens and right_tokens else 0.0
    )
    left_grams = {left_normalized[index:index + 3] for index in range(len(left_normalized) - 2)}
    right_grams = {right_normalized[index:index + 3] for index in range(len(right_normalized) - 2)}
    gram_score = (
        len(left_grams & right_grams) / len(left_grams | right_grams)
        if left_grams and right_grams else 0.0
    )
    return max(token_score, gram_score)


def _required_anchor_ids(topic_path: Path, question_text: str) -> tuple[set[str] | None, dict[str, Any]]:
    """Select the closest explicit question contract, if the Topic Pack owns one."""
    model_answer_path = topic_path / "model_answer.json"
    if not question_text or not model_answer_path.is_file():
        return None, {"mode": "all_anchors", "reason": "question_contract_unavailable"}
    payload = json.loads(model_answer_path.read_text(encoding="utf-8"))
    candidates: list[tuple[float, int, dict[str, Any]]] = []
    for index, row in enumerate(payload.get("expected_question_patterns", [])):
        if not isinstance(row, dict) or not row.get("required_anchor_ids"):
            continue
        pattern = str(row.get("pattern") or row.get("question") or "")
        candidates.append((_question_similarity(question_text, pattern), -index, row))
    if not candidates:
        return None, {"mode": "all_anchors", "reason": "explicit_anchor_mapping_unavailable"}
    similarity, _, selected = max(candidates, key=lambda row: (row[0], row[1]))
    if similarity < 0.2:
        return None, {
            "mode": "all_anchors",
            "reason": "question_contract_match_below_threshold",
            "best_similarity": round(similarity, 6),
        }
    return {
        str(anchor_id) for anchor_id in selected.get("required_anchor_ids", [])
        if str(anchor_id).strip()
    }, {
        "mode": "explicit_question_contract",
        "pattern": str(selected.get("pattern") or selected.get("question") or ""),
        "similarity": round(similarity, 6),
    }


def _source_span(answer_text: str, matched_terms: list[str]) -> dict[str, int] | None:
    normalized = unicodedata.normalize("NFKC", answer_text).casefold()
    positions = [normalized.find(term) for term in matched_terms]
    positions = [row for row in positions if row >= 0]
    if not positions:
        return None
    start = min(positions)
    line_start = answer_text.rfind("\n", 0, start) + 1
    line_end = answer_text.find("\n", start)
    if line_end < 0:
        line_end = len(answer_text)
    return {"start": line_start, "end": line_end}


def evaluate_fact_anchor_requirements(
    *,
    answer_text: str,
    topic_ids: Iterable[str],
    question_text: str = "",
) -> dict[str, Any]:
    normalized_answer = _normalize(answer_text)
    requirements: list[dict[str, Any]] = []
    selections: list[dict[str, Any]] = []
    for topic_id in sorted({str(row).strip() for row in topic_ids if str(row).strip()}):
        topic_path = ROOT / "rubrics" / "topic_packs" / topic_id
        path = topic_path / "fact_anchor.json"
        if not path.is_file():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        required_ids, selection = _required_anchor_ids(topic_path, question_text)
        selections.append({"owner_topic_id": topic_id, **selection})
        for anchor in payload.get("anchors", []):
            anchor_id = str(anchor.get("anchor_id") or anchor.get("id") or "")
            if required_ids is not None and anchor_id not in required_ids:
                continue
            terms = _terms(anchor)
            matched = [term for term in terms if _term_present(term, normalized_answer)]
            threshold = max(2, math.ceil(len(terms) * 0.6)) if terms else 1
            anchor_tokens = _anchor_tokens(anchor)
            matched_tokens = [
                token for token in anchor_tokens if token in normalized_answer
            ]
            token_coverage = (
                len(matched_tokens) / len(anchor_tokens) if anchor_tokens else 0.0
            )
            identity_term_matched = bool(terms and terms[0] in matched)
            if (
                len(matched) >= threshold
                or (len(matched_tokens) >= 3 and token_coverage >= 0.3)
            ):
                status = "SATISFIED"
            elif matched or (len(matched_tokens) >= 2 and token_coverage >= 0.12):
                status = "PARTIAL"
            else:
                status = "MISSING"
            evidence_terms = matched or matched_tokens
            span = _source_span(answer_text, evidence_terms)
            requirements.append({
                "owner_topic_id": topic_id,
                "requirement_id": anchor_id,
                "status": status,
                "evidence_mode": "lexical_fact_anchor",
                "importance": str(anchor.get("importance") or "normal"),
                "matched_terms": matched,
                "matched_concept_tokens": matched_tokens,
                "concept_token_coverage": round(token_coverage, 6),
                "required_term_count": len(terms),
                "match_threshold": threshold,
                "identity_term_matched": identity_term_matched,
                "source_span": span,
                "evidence_text": (
                    answer_text[span["start"]:span["end"]] if span is not None else ""
                ),
            })
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
        "extraction_complete": True,
        "requirements": requirements,
        "question_contract_selections": selections,
        "summary": {
            status: sum(row["status"] == status for row in requirements)
            for status in ("SATISFIED", "PARTIAL", "WRONG", "MISSING")
        },
    }


def augment_requirement_evaluation(
    base: dict[str, Any],
    fact_anchor_evaluation: dict[str, Any],
) -> dict[str, Any]:
    """Add source-owned anchor requirements without weakening invariants."""
    output = dict(base)
    existing = {
        (row.get("owner_topic_id"), row.get("requirement_id"))
        for row in base.get("requirements", [])
    }
    lexical_rows = list(fact_anchor_evaluation.get("requirements", []))
    base_by_key = {
        (row.get("owner_topic_id"), row.get("requirement_id")): row
        for row in base.get("requirements", [])
    }
    comparisons = []
    for row in lexical_rows:
        key = (row.get("owner_topic_id"), row.get("requirement_id"))
        canonical = base_by_key.get(key)
        if canonical is None:
            continue
        comparisons.append({
            "owner_topic_id": key[0],
            "requirement_id": key[1],
            "lexical_status": row.get("status"),
            "canonical_status": canonical.get("status"),
            "selected_mode": "canonical_claim",
            "status_changed": row.get("status") != canonical.get("status"),
        })
    output["requirements"] = list(base.get("requirements", [])) + [
        row for row in fact_anchor_evaluation.get("requirements", [])
        if (row.get("owner_topic_id"), row.get("requirement_id")) not in existing
    ]
    output["summary"] = {
        status: sum(row.get("status") == status for row in output["requirements"])
        for status in ("SATISFIED", "PARTIAL", "WRONG", "MISSING", "UNKNOWN")
    }
    output["canonical_promotion"] = {
        "comparison_count": len(comparisons),
        "status_change_count": sum(row["status_changed"] for row in comparisons),
        "canonical_selected_count": len(comparisons),
        "lexical_selected_count": 0,
        "comparisons": comparisons,
    }
    return output


def requirement_scope_by_topic(
    fact_anchor_evaluation: dict[str, Any],
) -> dict[str, list[str]]:
    """Project question-selected anchor IDs into machine-contract scope."""
    output: dict[str, set[str]] = {}
    for row in fact_anchor_evaluation.get("requirements", []):
        topic_id = str(row.get("owner_topic_id") or "").strip()
        requirement_id = str(row.get("requirement_id") or "").strip()
        if topic_id and requirement_id:
            output.setdefault(topic_id, set()).add(requirement_id)
    return {key: sorted(value) for key, value in sorted(output.items())}
