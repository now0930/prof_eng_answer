from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path
from typing import Any, Callable


SEMANTIC_ROUTER_SHADOW_VERSION = "semantic_router_shadow_v1"
SEMANTIC_ROUTER_SHADOW_FILE = "semantic_router_shadow.json"

VALID_ROUTING_MODES = {
    "SINGLE_TOPIC",
    "MULTI_TOPIC",
    "GENERAL",
    "AMBIGUOUS",
}
VALID_RUNTIME_ROLES = {
    "PRIMARY",
    "SUPPORTING",
    "NONE",
}

DEFAULT_MAX_CANDIDATES = 5
DEFAULT_MAX_TOPIC_EXCERPT_CHARS = 6000

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TOPIC_SHEET_DIR = BASE_DIR / "docs" / "topic_sheets"

_SEMANTIC_SECTION_TERMS = (
    "출제 의도",
    "대표 문제",
    "포함 범위",
    "제외 범위",
    "scope",
    "boundary",
    "경계",
    "ownership",
    "소유",
    "positive routing",
    "negative boundary",
    "적용 대상",
)


def _env_flag(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def semantic_router_shadow_enabled() -> bool:
    return _env_flag(
        "SEMANTIC_ROUTER_SHADOW_ENABLED",
        default=False,
    )


def _markdown_sections(text: str) -> list[tuple[str, str]]:
    lines = str(text or "").splitlines()
    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_heading, current_lines
        body = "\n".join(current_lines).strip()
        if current_heading or body:
            sections.append(
                (
                    current_heading.strip(),
                    body,
                )
            )
        current_heading = ""
        current_lines = []

    for line in lines:
        if re.match(r"^#{1,6}\s+\S", line):
            flush()
            current_heading = re.sub(
                r"^#{1,6}\s+",
                "",
                line,
            ).strip()
            continue
        current_lines.append(line)

    flush()
    return sections


def _compact_topic_sheet_semantics(
    text: str,
    *,
    max_chars: int = DEFAULT_MAX_TOPIC_EXCERPT_CHARS,
) -> str:
    raw = str(text or "").strip()
    if not raw:
        return ""

    sections = _markdown_sections(raw)
    selected: list[str] = []

    # Topic Sheet headings are heterogeneous. Keep initial context and then
    # select semantically relevant sections by broad heading/body keywords.
    for heading, body in sections[:2]:
        block = "\n".join(
            x
            for x in (
                f"## {heading}" if heading else "",
                body,
            )
            if x
        ).strip()
        if block:
            selected.append(block)

    for heading, body in sections:
        haystack = f"{heading}\n{body[:400]}".casefold()
        if not any(
            term.casefold() in haystack
            for term in _SEMANTIC_SECTION_TERMS
        ):
            continue

        block = "\n".join(
            x
            for x in (
                f"## {heading}" if heading else "",
                body,
            )
            if x
        ).strip()

        if block and block not in selected:
            selected.append(block)

    compact = "\n\n".join(selected).strip()
    if not compact:
        compact = raw

    if len(compact) > int(max_chars):
        compact = (
            compact[: int(max_chars)]
            + "\n...[TRUNCATED]..."
        )

    return compact


def _candidate_topic_id(candidate: Any) -> str:
    if not isinstance(candidate, dict):
        return ""

    answer = candidate.get("answer")
    if not isinstance(answer, dict):
        answer = {}

    return str(
        answer.get("topic_id")
        or candidate.get("topic_id")
        or ""
    ).strip()


def _candidate_title(candidate: Any) -> str:
    if not isinstance(candidate, dict):
        return ""

    answer = candidate.get("answer")
    if not isinstance(answer, dict):
        answer = {}

    return str(
        answer.get("title")
        or candidate.get("title")
        or ""
    ).strip()


_SHADOW_RECALL_STOP_TERMS = {
    "설명",
    "설명하시오",
    "비교",
    "특성",
    "영향",
    "관계",
    "역할",
    "원리",
    "방법",
    "기준",
    "적용",
    "동작",
    "제어",
    "시스템",
    "및",
    "with",
    "and",
    "the",
}

SHADOW_RECALL_SCORE_DELTA = 4


def _shadow_recall_terms(text: str) -> set[str]:
    raw_terms = re.findall(
        r"[0-9A-Za-z가-힣]+",
        str(text or "").casefold(),
    )

    terms: set[str] = set()
    for raw in raw_terms:
        term = raw.strip()
        if len(term) < 2:
            continue
        if term in _SHADOW_RECALL_STOP_TERMS:
            continue
        terms.add(term)

    return terms


def _shadow_recall_question_compact(
    text: str,
) -> str:
    return "".join(
        re.findall(
            r"[0-9A-Za-z가-힣]+",
            str(text or "").casefold(),
        )
    )


def _iter_topic_entries(value: Any):
    if isinstance(value, dict):
        topic_id = str(
            value.get("topic_id") or ""
        ).strip()
        if topic_id:
            yield value
            return

        for child in value.values():
            yield from _iter_topic_entries(child)

    elif isinstance(value, list):
        for child in value:
            yield from _iter_topic_entries(child)


def _collect_shadow_routing_signals(
    entry: dict[str, Any],
) -> list[str]:
    signals: list[str] = []
    seen: set[str] = set()

    def add(value: Any) -> None:
        text = str(value or "").strip()
        if not text:
            return
        key = text.casefold()
        if key in seen:
            return
        seen.add(key)
        signals.append(text)

    add(entry.get("title"))
    add(entry.get("display_name"))
    add(entry.get("name"))

    def walk(value: Any, key_hint: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_l = str(key).casefold()
                relevant = any(
                    token in key_l
                    for token in (
                        "alias",
                        "field",
                        "connection",
                        "question",
                        "example",
                        "keyword",
                    )
                )

                if relevant:
                    if isinstance(child, str):
                        add(child)
                    elif isinstance(child, list):
                        for item in child:
                            if isinstance(item, str):
                                add(item)
                            elif isinstance(item, (dict, list)):
                                walk(item, key_l)
                    elif isinstance(child, dict):
                        walk(child, key_l)
                else:
                    walk(child, key_l)

        elif isinstance(value, list):
            for child in value:
                walk(child, key_hint)

        elif isinstance(value, str) and key_hint:
            if any(
                token in key_hint
                for token in (
                    "alias",
                    "field",
                    "connection",
                    "question",
                    "example",
                    "keyword",
                )
            ):
                add(value)

    walk(entry)
    return signals


def _shadow_recall_signal_score(
    question_text: str,
    signals: list[str],
    *,
    term_document_frequency: dict[str, int],
    topic_count: int,
) -> tuple[int, list[str]]:
    question_compact = _shadow_recall_question_compact(
        question_text
    )

    matched_terms: set[str] = set()
    strong_phrase_hits = 0

    for signal in signals:
        signal_terms = _shadow_recall_terms(signal)
        signal_compact = _shadow_recall_question_compact(
            signal
        )

        if (
            len(signal_terms) >= 2
            and len(signal_compact) >= 4
            and signal_compact in question_compact
        ):
            strong_phrase_hits += 1

        for term in signal_terms:
            if term in question_compact:
                matched_terms.add(term)

    df_cap = max(
        2,
        min(
            6,
            max(1, int(topic_count)) // 12,
        ),
    )

    discriminative_terms = {
        term
        for term in matched_terms
        if term_document_frequency.get(
            term,
            topic_count,
        ) <= df_cap
    }

    distinctive_terms = {
        term
        for term in discriminative_terms
        if (
            len(term) >= 3
            or (
                term.isascii()
                and len(term) >= 2
            )
        )
    }

    if (
        len(matched_terms) < 2
        or not distinctive_terms
    ):
        return 0, sorted(
            matched_terms,
            key=lambda value: (-len(value), value),
        )

    score = (
        len(matched_terms) * 2
        + len(discriminative_terms) * 4
        + strong_phrase_hits * 4
    )

    return score, sorted(
        matched_terms,
        key=lambda value: (-len(value), value),
    )


def augment_rule_candidates_for_shadow(
    question_text: str,
    rule_result: Any,
    *,
    bank: Any | None = None,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
) -> dict[str, Any]:
    # Broaden candidate recall for semantic shadow only.
    # The legacy Rule Router result is copied and never mutated in-place.
    if isinstance(rule_result, dict):
        shadow_result = dict(rule_result)
        existing = list(
            rule_result.get("candidates") or []
        )
    else:
        shadow_result = {}
        existing = []

    if bank is None:
        from rubric_registry import (
            load_model_answer_bank,
        )
        bank = load_model_answer_bank()

    candidate_rows: list[dict[str, Any]] = []
    seen_topic_ids: set[str] = set()

    for candidate in existing:
        if not isinstance(candidate, dict):
            continue

        topic_id = _candidate_topic_id(candidate)
        if not topic_id or topic_id in seen_topic_ids:
            continue

        seen_topic_ids.add(topic_id)
        candidate_rows.append(candidate)

        if len(candidate_rows) >= int(max_candidates):
            break

    discovered: list[
        tuple[int, str, list[str], dict[str, Any]]
    ] = []

    topic_entries = list(
        _iter_topic_entries(bank)
    )

    topic_signals: dict[str, list[str]] = {}
    term_document_frequency: dict[str, int] = {}

    for entry in topic_entries:
        topic_id = str(
            entry.get("topic_id") or ""
        ).strip()
        if not topic_id:
            continue

        signals = _collect_shadow_routing_signals(
            entry
        )
        topic_signals[topic_id] = signals

        topic_terms: set[str] = set()
        for signal in signals:
            topic_terms.update(
                _shadow_recall_terms(signal)
            )

        for term in topic_terms:
            term_document_frequency[term] = (
                term_document_frequency.get(term, 0)
                + 1
            )

    topic_count = max(
        1,
        len(topic_signals),
    )

    for entry in topic_entries:
        topic_id = str(
            entry.get("topic_id") or ""
        ).strip()

        if (
            not topic_id
            or topic_id in seen_topic_ids
        ):
            continue

        signals = topic_signals.get(
            topic_id,
            [],
        )
        score, matched_terms = (
            _shadow_recall_signal_score(
                question_text,
                signals,
                term_document_frequency=(
                    term_document_frequency
                ),
                topic_count=topic_count,
            )
        )

        if score < 6:
            continue

        discovered.append(
            (
                score,
                topic_id,
                matched_terms,
                entry,
            )
        )

    discovered.sort(
        key=lambda row: (
            -row[0],
            row[1],
        )
    )

    if discovered:
        score_floor = max(
            6,
            discovered[0][0]
            - SHADOW_RECALL_SCORE_DELTA,
        )
        discovered = [
            row
            for row in discovered
            if row[0] >= score_floor
        ]

    augmented_ids: list[str] = []

    for (
        score,
        topic_id,
        matched_terms,
        entry,
    ) in discovered:
        if len(candidate_rows) >= int(max_candidates):
            break

        if topic_id in seen_topic_ids:
            continue

        seen_topic_ids.add(topic_id)
        augmented_ids.append(topic_id)

        candidate_rows.append(
            {
                "answer": {
                    "topic_id": topic_id,
                    "title": str(
                        entry.get("title")
                        or entry.get("display_name")
                        or entry.get("name")
                        or topic_id
                    ),
                },
                "score": score,
                "question_score": score,
                "fact_score": 0,
                "answer_score": 0,
                "match_reasons": [
                    "shadow recall adapter matched routing "
                    "terms: "
                    + repr(matched_terms[:8])
                ],
                "shadow_recall_adapter": True,
            }
        )

    shadow_result["candidates"] = candidate_rows
    shadow_result[
        "shadow_candidate_recall_adapter"
    ] = {
        "enabled": True,
        "augmented_topic_ids": augmented_ids,
        "candidate_count": len(candidate_rows),
        "legacy_router_mutated": False,
        "student_answer_used": False,
    }

    return shadow_result


def build_candidate_semantic_catalog(
    rule_result: Any,
    *,
    topic_sheet_dir: str | Path | None = None,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
    max_excerpt_chars: int = DEFAULT_MAX_TOPIC_EXCERPT_CHARS,
) -> list[dict[str, Any]]:
    if not isinstance(rule_result, dict):
        return []

    candidates = rule_result.get("candidates")
    if not isinstance(candidates, list):
        return []

    sheet_dir = Path(
        topic_sheet_dir
        if topic_sheet_dir is not None
        else DEFAULT_TOPIC_SHEET_DIR
    )

    catalog: list[dict[str, Any]] = []
    seen: set[str] = set()

    for candidate in candidates:
        topic_id = _candidate_topic_id(candidate)
        if not topic_id or topic_id in seen:
            continue

        seen.add(topic_id)
        sheet_path = sheet_dir / f"{topic_id}.md"
        semantic_excerpt = ""
        topic_sheet_available = sheet_path.is_file()

        if topic_sheet_available:
            try:
                semantic_excerpt = _compact_topic_sheet_semantics(
                    sheet_path.read_text(encoding="utf-8"),
                    max_chars=max_excerpt_chars,
                )
            except Exception:
                semantic_excerpt = ""

        reasons = candidate.get("match_reasons")
        if not isinstance(reasons, list):
            reasons = []

        catalog.append(
            {
                "topic_id": topic_id,
                "title": _candidate_title(candidate),
                "rule_score": candidate.get("score"),
                "question_score": candidate.get("question_score"),
                "match_reasons": [
                    str(x)
                    for x in reasons[:8]
                ],
                "topic_sheet_available": topic_sheet_available,
                "semantic_excerpt": semantic_excerpt,
            }
        )

        if len(catalog) >= int(max_candidates):
            break

    return catalog


def build_semantic_router_prompt(
    question_text: str,
    question_demand_result: dict[str, Any],
    candidate_catalog: list[dict[str, Any]],
) -> str:
    question = str(question_text or "").strip()
    demands = (
        question_demand_result.get("demands")
        if isinstance(question_demand_result, dict)
        else []
    )
    if not isinstance(demands, list):
        demands = []

    candidate_ids = [
        str(row.get("topic_id") or "")
        for row in candidate_catalog
        if str(row.get("topic_id") or "").strip()
    ]

    return f"""
You are the semantic adjudication layer of Topic Router v2
for the Korean Professional Engineer examination.

You receive:
1. the examination question,
2. already-decomposed question demands,
3. ONLY the deterministic Rule Router candidates.

You must NOT use or infer a student's answer.
You must NOT invent a Topic.
You may use only these candidate topic_ids:
{json.dumps(candidate_ids, ensure_ascii=False)}

Routing modes:
- SINGLE_TOPIC: one candidate Topic owns the substantive demands.
- MULTI_TOPIC: two or more candidate Topics are explicitly required.
- GENERAL: the question is clear but supplied Topic candidates do not
  adequately own the demands.
- AMBIGUOUS: the question/candidate boundary is genuinely insufficient
  to determine stable ownership.

Runtime roles:
- PRIMARY
- SUPPORTING
- NONE

Important:
- Multiple candidate Topics do NOT automatically mean AMBIGUOUS.
- Low Rule score does NOT automatically mean GENERAL.
- Use Topic Sheet positive scope and negative boundary.
- If candidate evidence is insufficient, choose GENERAL rather than
  forcing the closest Topic.
- Return JSON only.
- Every non-empty topic_id must be copied EXACTLY from the supplied
  candidate topic_id list.
- routing_mode and topic_id are different fields with different types.
- NEVER put SINGLE_TOPIC, MULTI_TOPIC, GENERAL, or AMBIGUOUS in topic_id.
- NEVER put PRIMARY, SUPPORTING, or NONE in topic_id.
- For MULTI_TOPIC, use separate demand_mappings whose topic_id values are
  exact candidate topic ids. MULTI_TOPIC itself belongs only in routing_mode.
- If no candidate owns a demand, list that demand id in
  uncovered_demand_ids instead of inventing a topic_id.

Field contract:
- routing_mode enum = SINGLE_TOPIC | MULTI_TOPIC | GENERAL | AMBIGUOUS
- topic_id enum = one of the exact candidate ids shown above, or empty only
  when role is NONE
- role enum = PRIMARY | SUPPORTING | NONE
- confidence = finite number from 0.0 through 1.0

Mode/role consistency is mandatory:
- First decide PRIMARY/SUPPORTING/NONE for each demand mapping.
- Count DISTINCT topic_id values whose role is PRIMARY.
- Exactly 1 distinct PRIMARY topic => routing_mode MUST be SINGLE_TOPIC.
- 2 or more distinct PRIMARY topics => routing_mode MUST be MULTI_TOPIC.
- SUPPORTING topics NEVER make a route MULTI_TOPIC.
- Multiple candidate topics NEVER by themselves make a route MULTI_TOPIC.
- A closely related candidate may be SUPPORTING or NONE while the route
  remains SINGLE_TOPIC when only one Topic owns the question.
- Use GENERAL only when no candidate Topic positively owns the demand.
- Use AMBIGUOUS only when ownership itself cannot be resolved from the
  supplied evidence; do not use it merely because several candidates exist.

Forbidden topic_id values:
["SINGLE_TOPIC", "MULTI_TOPIC", "GENERAL", "AMBIGUOUS",
 "PRIMARY", "SUPPORTING", "NONE"]

Required JSON:
{{
  "routing_mode": "MULTI_TOPIC",
  "demand_mappings": [
    {{
      "demand_id": "D1",
      "topic_id": "<COPY_EXACT_CANDIDATE_TOPIC_ID>",
      "role": "PRIMARY",
      "confidence": 0.95
    }}
  ],
  "uncovered_demand_ids": [],
  "reason": "short reason"
}}

Question:
{question}

Question demands:
{json.dumps(demands, ensure_ascii=False, indent=2)}

Rule candidate semantic catalog:
{json.dumps(candidate_catalog, ensure_ascii=False, indent=2)}
""".strip()


def _finite_confidence(value: Any) -> float:
    if isinstance(value, bool):
        raise ValueError("confidence must be numeric, not bool")

    try:
        confidence = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"invalid confidence: {exc!r}"
        ) from exc

    if not math.isfinite(confidence):
        raise ValueError("confidence must be finite")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError(
            "confidence must be between 0 and 1"
        )

    return round(confidence, 6)


def _normalize_semantic_payload(
    payload: Any,
    *,
    demands: list[dict[str, Any]],
    allowed_topic_ids: set[str],
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError(
            "semantic router result root must be object"
        )

    mode = str(
        payload.get("routing_mode") or ""
    ).strip().upper()

    if mode not in VALID_ROUTING_MODES:
        raise ValueError(
            f"invalid routing_mode: {mode!r}"
        )

    demand_ids = {
        str(row.get("id") or "").strip()
        for row in demands
        if isinstance(row, dict)
        and str(row.get("id") or "").strip()
    }

    raw_mappings = payload.get("demand_mappings")
    if raw_mappings is None:
        raw_mappings = []
    if not isinstance(raw_mappings, list):
        raise ValueError(
            "demand_mappings must be a list"
        )

    normalized_mappings: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for row in raw_mappings:
        if not isinstance(row, dict):
            continue

        demand_id = str(
            row.get("demand_id") or ""
        ).strip()
        topic_id = str(
            row.get("topic_id") or ""
        ).strip()
        role = str(
            row.get("role") or ""
        ).strip().upper()

        if demand_id not in demand_ids:
            raise ValueError(
                f"unknown demand_id: {demand_id!r}"
            )

        if role not in VALID_RUNTIME_ROLES:
            raise ValueError(
                f"invalid runtime role: {role!r}"
            )

        if topic_id and topic_id not in allowed_topic_ids:
            raise ValueError(
                "LLM returned topic outside Rule candidates: "
                f"{topic_id}"
            )

        if role in {"PRIMARY", "SUPPORTING"} and not topic_id:
            raise ValueError(
                f"{role} mapping requires topic_id"
            )

        confidence = _finite_confidence(
            row.get("confidence", 0.0)
        )

        key = (demand_id, topic_id, role)
        if key in seen:
            continue
        seen.add(key)

        normalized_mappings.append(
            {
                "demand_id": demand_id,
                "topic_id": topic_id or None,
                "role": role,
                "confidence": confidence,
            }
        )

    raw_uncovered = payload.get("uncovered_demand_ids")
    if raw_uncovered is None:
        raw_uncovered = []
    if not isinstance(raw_uncovered, list):
        raise ValueError(
            "uncovered_demand_ids must be a list"
        )

    uncovered: list[str] = []
    for value in raw_uncovered:
        demand_id = str(value or "").strip()
        if demand_id not in demand_ids:
            raise ValueError(
                "unknown uncovered demand_id: "
                f"{demand_id!r}"
            )
        if demand_id not in uncovered:
            uncovered.append(demand_id)

    primary_topic_ids: list[str] = []
    supporting_topic_ids: list[str] = []

    for row in normalized_mappings:
        topic_id = row.get("topic_id")
        if not topic_id:
            continue

        if (
            row.get("role") == "PRIMARY"
            and topic_id not in primary_topic_ids
        ):
            primary_topic_ids.append(topic_id)

        if (
            row.get("role") == "SUPPORTING"
            and topic_id not in supporting_topic_ids
        ):
            supporting_topic_ids.append(topic_id)

    supporting_topic_ids = [
        topic_id
        for topic_id in supporting_topic_ids
        if topic_id not in primary_topic_ids
    ]

    if mode == "SINGLE_TOPIC":
        if len(primary_topic_ids) != 1:
            raise ValueError(
                "SINGLE_TOPIC requires exactly one PRIMARY topic"
            )

    elif mode == "MULTI_TOPIC":
        if len(primary_topic_ids) < 2:
            raise ValueError(
                "MULTI_TOPIC requires at least two PRIMARY topics"
            )

    elif mode == "GENERAL":
        if primary_topic_ids or supporting_topic_ids:
            raise ValueError(
                "GENERAL must not assign positive Topic roles"
            )

    return {
        "routing_mode": mode,
        "demand_mappings": normalized_mappings,
        "uncovered_demand_ids": uncovered,
        "primary_topic_ids": primary_topic_ids,
        "supporting_topic_ids": supporting_topic_ids,
        "reason": str(payload.get("reason") or "").strip(),
    }


def _base_result(
    *,
    enabled: bool,
    status: str,
    ok: bool,
    error: str = "",
    routing_mode: str | None = None,
    candidate_topic_ids: list[str] | None = None,
    demand_mappings: list[dict[str, Any]] | None = None,
    uncovered_demand_ids: list[str] | None = None,
    primary_topic_ids: list[str] | None = None,
    supporting_topic_ids: list[str] | None = None,
    reason: str = "",
    llm_called: bool = False,
) -> dict[str, Any]:
    return {
        "version": SEMANTIC_ROUTER_SHADOW_VERSION,
        "shadow": True,
        "enabled": bool(enabled),
        "status": str(status),
        "ok": bool(ok),
        "routing_mode": routing_mode,
        "candidate_topic_ids": candidate_topic_ids or [],
        "demand_mappings": demand_mappings or [],
        "uncovered_demand_ids": uncovered_demand_ids or [],
        "primary_topic_ids": primary_topic_ids or [],
        "supporting_topic_ids": supporting_topic_ids or [],
        "reason": str(reason or ""),
        "error": str(error or ""),
        "llm_called": bool(llm_called),
        "routing_effect": "none",
        "score_effect": "none",
        "student_answer_used": False,
        "legacy_router_authoritative": True,
    }


def semantic_route_shadow(
    question_text: str,
    question_demand_result: Any,
    rule_result: Any,
    *,
    llm_call: Callable[[str], Any] | None = None,
    enabled: bool | None = None,
    topic_sheet_dir: str | Path | None = None,
) -> dict[str, Any]:
    if enabled is None:
        enabled = semantic_router_shadow_enabled()

    if not enabled:
        return _base_result(
            enabled=False,
            status="disabled",
            ok=False,
            error=(
                "SEMANTIC_ROUTER_SHADOW_ENABLED "
                "is not enabled"
            ),
        )

    question = str(question_text or "").strip()
    if not question:
        return _base_result(
            enabled=True,
            status="skipped",
            ok=False,
            error="question text is empty",
        )

    if not isinstance(question_demand_result, dict):
        return _base_result(
            enabled=True,
            status="fallback",
            ok=False,
            error="question demand shadow result missing",
        )

    if question_demand_result.get("ok") is not True:
        return _base_result(
            enabled=True,
            status="fallback",
            ok=False,
            error=(
                "question demand shadow is not usable: "
                + str(
                    question_demand_result.get("status")
                    or "unknown"
                )
            ),
        )

    demands = question_demand_result.get("demands")
    if not isinstance(demands, list) or not demands:
        return _base_result(
            enabled=True,
            status="fallback",
            ok=False,
            error="question demands are empty",
        )

    catalog = build_candidate_semantic_catalog(
        rule_result,
        topic_sheet_dir=topic_sheet_dir,
    )

    allowed_topic_ids = {
        str(row.get("topic_id") or "").strip()
        for row in catalog
        if str(row.get("topic_id") or "").strip()
    }
    candidate_topic_ids = sorted(allowed_topic_ids)

    # Stage 3 does not repair candidate recall. No Rule candidate means
    # deterministic GENERAL and zero semantic-LLM calls.
    if not candidate_topic_ids:
        return _base_result(
            enabled=True,
            status="ok",
            ok=True,
            routing_mode="GENERAL",
            candidate_topic_ids=[],
            uncovered_demand_ids=[
                str(row.get("id") or "").strip()
                for row in demands
                if isinstance(row, dict)
                and str(row.get("id") or "").strip()
            ],
            reason=(
                "Rule Router supplied no candidate Topic; "
                "semantic shadow does not invent Topics."
            ),
            llm_called=False,
        )

    prompt = build_semantic_router_prompt(
        question,
        question_demand_result,
        catalog,
    )

    if llm_call is None:
        from logic_llm_verifier import _call_ollama_json
        llm_call = _call_ollama_json

    try:
        payload = llm_call(prompt)
        normalized = _normalize_semantic_payload(
            payload,
            demands=demands,
            allowed_topic_ids=allowed_topic_ids,
        )
    except Exception as exc:
        return _base_result(
            enabled=True,
            status="fallback",
            ok=False,
            candidate_topic_ids=candidate_topic_ids,
            error=(
                "semantic router shadow failed: "
                f"{exc!r}"
            ),
            llm_called=True,
        )

    return _base_result(
        enabled=True,
        status="ok",
        ok=True,
        routing_mode=normalized["routing_mode"],
        candidate_topic_ids=candidate_topic_ids,
        demand_mappings=normalized["demand_mappings"],
        uncovered_demand_ids=normalized["uncovered_demand_ids"],
        primary_topic_ids=normalized["primary_topic_ids"],
        supporting_topic_ids=normalized["supporting_topic_ids"],
        reason=normalized["reason"],
        llm_called=True,
    )
