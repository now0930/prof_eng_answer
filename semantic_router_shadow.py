from __future__ import annotations
import urllib.request

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



def _shadow_recall_signal_score_for_demand(
    question_text: str,
    signals: list[str],
    *,
    term_document_frequency: dict[str, int],
    topic_count: int,
) -> tuple[int, list[str], dict[str, Any]]:
    # Demand-aware recall keeps the global scorer unchanged.
    # A low-DF exact multi-term phrase can establish specificity
    # even when Korean component terms are each only two characters.
    question_compact = _shadow_recall_question_compact(question_text)

    matched_terms: set[str] = set()
    strong_phrase_hits: list[str] = []
    discriminative_strong_phrases: list[str] = []

    df_cap = max(
        2,
        min(
            6,
            max(1, int(topic_count)) // 12,
        ),
    )

    for signal in signals:
        signal_terms = _shadow_recall_terms(signal)
        signal_compact = _shadow_recall_question_compact(signal)

        exact_strong_phrase = (
            len(signal_terms) >= 2
            and len(signal_compact) >= 4
            and signal_compact in question_compact
        )

        if exact_strong_phrase:
            strong_phrase_hits.append(signal)

        for term in signal_terms:
            if term in question_compact:
                matched_terms.add(term)

        if exact_strong_phrase:
            unique_terms = set(signal_terms)
            if (
                len(unique_terms) >= 2
                and all(
                    term_document_frequency.get(
                        term,
                        topic_count,
                    )
                    <= df_cap
                    for term in unique_terms
                )
            ):
                discriminative_strong_phrases.append(signal)

    discriminative_terms = {
        term
        for term in matched_terms
        if term_document_frequency.get(
            term,
            topic_count,
        )
        <= df_cap
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

    specificity_ok = bool(
        distinctive_terms
        or discriminative_strong_phrases
    )

    matched_sorted = sorted(
        matched_terms,
        key=lambda value: (-len(value), value),
    )

    metadata = {
        "df_cap": df_cap,
        "strong_phrase_hits": strong_phrase_hits,
        "discriminative_strong_phrases": (
            discriminative_strong_phrases
        ),
        "distinctive_terms": sorted(
            distinctive_terms,
            key=lambda value: (-len(value), value),
        ),
    }

    if (
        len(matched_terms) < 2
        or not specificity_ok
    ):
        return 0, matched_sorted, metadata

    score = (
        len(matched_terms) * 2
        + len(discriminative_terms) * 4
        + len(strong_phrase_hits) * 4
    )
    return score, matched_sorted, metadata


def build_question_demand_aware_rule_candidates(
    question_text: str,
    question_demand_result: Any,
    *,
    bank: Any | None = None,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
) -> dict[str, Any]:
    # Routing candidates are question-only by construction.
    # Student answer, fact_eval, grading scores, and coverage
    # are intentionally absent from this API and result.
    if bank is None:
        from rubric_registry import (
            load_model_answer_bank,
        )

        bank = load_model_answer_bank()

    demands: list[dict[str, Any]] = []
    if isinstance(question_demand_result, dict):
        raw_demands = (
            question_demand_result.get("demands")
            or []
        )
        if isinstance(raw_demands, list):
            demands = [
                row
                for row in raw_demands
                if isinstance(row, dict)
                and str(row.get("text") or "").strip()
            ]

    topic_entries = list(_iter_topic_entries(bank))
    topic_signals: dict[str, list[str]] = {}
    topic_entry_by_id: dict[str, dict[str, Any]] = {}
    term_document_frequency: dict[str, int] = {}

    for entry in topic_entries:
        if not isinstance(entry, dict):
            continue
        topic_id = str(
            entry.get("topic_id") or ""
        ).strip()
        if (
            not topic_id
            or topic_id in topic_entry_by_id
        ):
            continue

        topic_entry_by_id[topic_id] = entry
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

    topic_count = max(1, len(topic_signals))

    # K2_APPEAR_TOTAL:
    # retain the top two question-only matches for each demand,
    # then rank Topics by cross-demand appearance count first,
    # top-K score sum second, and all-positive score sum third.
    ownership: dict[str, dict[str, Any]] = {}
    demand_winners: list[dict[str, Any]] = []

    for index, demand in enumerate(demands, 1):
        demand_id = str(
            demand.get("demand_id")
            or demand.get("id")
            or f"D{index}"
        ).strip()
        demand_text = str(
            demand.get("text") or ""
        ).strip()

        ranked: list[
            tuple[
                int,
                str,
                list[str],
                dict[str, Any],
            ]
        ] = []

        for topic_id, signals in topic_signals.items():
            (
                score,
                matched_terms,
                metadata,
            ) = _shadow_recall_signal_score_for_demand(
                demand_text,
                signals,
                term_document_frequency=(
                    term_document_frequency
                ),
                topic_count=topic_count,
            )
            if score < 6:
                continue
            ranked.append(
                (
                    score,
                    topic_id,
                    matched_terms,
                    metadata,
                )
            )

        ranked.sort(
            key=lambda row: (
                -row[0],
                row[1],
            )
        )

        if not ranked:
            demand_winners.append(
                {
                    "demand_id": demand_id,
                    "topic_id": None,
                    "score": 0,
                    "matched_terms": [],
                }
            )
            continue

        for (
            score,
            topic_id,
            _matched_terms,
            _metadata,
        ) in ranked:
            if topic_id not in ownership:
                ownership[topic_id] = {
                    "owned_demand_ids": [],
                    "appear_count": 0,
                    "topk_score_sum": 0,
                    "all_score_sum": 0,
                    "matched_terms": set(),
                }
            ownership[topic_id]["all_score_sum"] += int(
                score
            )

        for (
            score,
            topic_id,
            matched_terms,
            _metadata,
        ) in ranked[:2]:
            owner = ownership[topic_id]
            owner["appear_count"] += 1
            owner["topk_score_sum"] += int(score)
            owner["owned_demand_ids"].append(
                demand_id
            )
            owner["matched_terms"].update(
                matched_terms
            )

        (
            score,
            topic_id,
            matched_terms,
            metadata,
        ) = ranked[0]

        demand_winners.append(
            {
                "demand_id": demand_id,
                "topic_id": topic_id,
                "score": int(score),
                "matched_terms": matched_terms,
                "strong_phrase_hits": (
                    metadata.get(
                        "strong_phrase_hits"
                    )
                    or []
                ),
                "discriminative_strong_phrases": (
                    metadata.get(
                        "discriminative_strong_phrases"
                    )
                    or []
                ),
            }
        )

    ranked_owners = sorted(
        (
            (topic_id, owner)
            for topic_id, owner in ownership.items()
            if int(owner["appear_count"]) > 0
        ),
        key=lambda row: (
            -int(row[1]["appear_count"]),
            -int(row[1]["topk_score_sum"]),
            -int(row[1]["all_score_sum"]),
            row[0],
        ),
    )

    candidate_rows: list[dict[str, Any]] = []
    candidate_limit = min(
        2,
        max(0, int(max_candidates)),
    )

    for topic_id, owner in ranked_owners[
        :candidate_limit
    ]:
        entry = topic_entry_by_id[topic_id]

        candidate_rows.append(
            {
                "answer": {
                    "topic_id": topic_id,
                    "id": entry.get("id"),
                    "title": str(
                        entry.get("title")
                        or entry.get("display_name")
                        or entry.get("title_ko")
                        or entry.get("name")
                        or topic_id
                    ),
                },
                "score": int(
                    owner["topk_score_sum"]
                ),
                "question_score": int(
                    owner["topk_score_sum"]
                ),
                "fact_score": 0,
                "answer_score": 0,
                "match_reasons": [
                    (
                        "question-demand-aware K2 aggregate "
                        "candidate for demands: "
                        + ", ".join(
                            owner[
                                "owned_demand_ids"
                            ]
                        )
                    )
                ],
                "question_demand_aware": True,
                "owned_demand_ids": list(
                    owner["owned_demand_ids"]
                ),
                "matched_terms": sorted(
                    owner["matched_terms"],
                    key=lambda value: (
                        -len(value),
                        value,
                    ),
                ),
            }
        )

    if not candidate_rows:
        # QD can be disabled or unavailable. Preserve routing
        # compatibility without reintroducing student-answer or
        # fact-eval signals:
        #   1) neutral legacy rule match (question only),
        #   2) existing question-only shadow recall augmentation,
        #   3) freeze the resulting candidate catalog as authoritative.
        from model_answer_router import (
            find_model_answer_reference,
        )

        neutral = find_model_answer_reference(
            question_text=question_text,
            answer_text="",
            question_type_eval={},
            fact_eval={},
            bank=bank,
        )
        if not isinstance(neutral, dict):
            neutral = {
                "version": (
                    "question_only_neutral_rule_fallback"
                ),
                "routing_status": "no_match",
                "matched": False,
                "candidates": [],
            }

        neutral = dict(neutral)
        isolated_rule_candidates: list[dict[str, Any]] = []
        for candidate in list(
            neutral.get("candidates") or []
        ):
            if not isinstance(candidate, dict):
                continue
            isolated = dict(candidate)
            isolated["fact_score"] = 0
            isolated["answer_score"] = 0
            isolated_rule_candidates.append(isolated)

        neutral["candidates"] = isolated_rule_candidates
        neutral["question_only"] = True
        neutral["student_answer_used"] = False
        neutral["fact_eval_used"] = False

        augmented = augment_rule_candidates_for_shadow(
            question_text=question_text,
            rule_result=neutral,
            bank=bank,
            max_candidates=max_candidates,
        )
        augmented = dict(augmented)

        isolated_candidates: list[dict[str, Any]] = []
        for candidate in list(
            augmented.get("candidates") or []
        ):
            if not isinstance(candidate, dict):
                continue
            isolated = dict(candidate)
            isolated["fact_score"] = 0
            isolated["answer_score"] = 0
            isolated_candidates.append(isolated)
            if len(isolated_candidates) >= int(max_candidates):
                break

        augmented["candidates"] = isolated_candidates
        augmented[
            "question_demand_aware_authoritative"
        ] = True
        augmented["question_only"] = True
        augmented["student_answer_used"] = False
        augmented["fact_eval_used"] = False
        augmented[
            "question_demand_aware_candidate_result"
        ] = {
            "enabled": True,
            "strategy": (
                "neutral_question_only_rule_plus_augment_fallback"
            ),
            "candidate_count": len(
                isolated_candidates
            ),
            "student_answer_used": False,
            "fact_eval_used": False,
            "demand_winners": demand_winners,
        }
        return augmented

    return {
        "version": (
            "question_demand_aware_candidates_v1"
        ),
        "routing_status": (
            "question_demand_aware_candidates"
        ),
        "matched": bool(candidate_rows),
        "candidates": candidate_rows,
        "question_only": True,
        "student_answer_used": False,
        "fact_eval_used": False,
        "question_demand_aware_authoritative": True,
        "question_demand_aware_candidate_result": {
            "enabled": True,
            "strategy": "per_demand_top2_appear_total",
            "candidate_count": len(
                candidate_rows
            ),
            "student_answer_used": False,
            "fact_eval_used": False,
            "demand_winners": demand_winners,
        },
    }


def augment_rule_candidates_for_shadow(
    question_text: str,
    rule_result: Any,
    *,
    bank: Any | None = None,
    max_candidates: int = DEFAULT_MAX_CANDIDATES,
) -> dict[str, Any]:
    if (
        isinstance(rule_result, dict)
        and rule_result.get(
            "question_demand_aware_authoritative"
        )
        is True
    ):
        shadow_result = dict(rule_result)
        candidate_rows: list[dict[str, Any]] = []
        seen_topic_ids: set[str] = set()

        for candidate in list(
            rule_result.get("candidates") or []
        ):
            if not isinstance(candidate, dict):
                continue
            topic_id = _candidate_topic_id(candidate)
            if (
                not topic_id
                or topic_id in seen_topic_ids
            ):
                continue
            seen_topic_ids.add(topic_id)
            candidate_rows.append(candidate)
            if len(candidate_rows) >= int(max_candidates):
                break

        shadow_result["candidates"] = candidate_rows
        shadow_result[
            "shadow_candidate_recall_adapter"
        ] = {
            "enabled": True,
            "augmented_topic_ids": [],
            "candidate_count": len(candidate_rows),
            "legacy_router_mutated": False,
            "student_answer_used": False,
            "authoritative_question_demand_aware": True,
        }
        return shadow_result

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



SEMANTIC_ROUTER_OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
).rstrip("/")
SEMANTIC_ROUTER_MODEL = os.getenv(
    "SEMANTIC_ROUTER_MODEL",
    os.getenv("OLLAMA_MODEL", "gemma4:e4b"),
)
SEMANTIC_ROUTER_TIMEOUT = int(
    os.getenv("SEMANTIC_ROUTER_TIMEOUT", "90")
)


SEMANTIC_ROUTER_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "routing_mode": {
            "type": "string",
            "enum": [
                "SINGLE_TOPIC",
                "MULTI_TOPIC",
                "GENERAL",
                "AMBIGUOUS",
            ],
        },
        "demand_mappings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "demand_id": {
                        "type": "string",
                    },
                    "topic_id": {
                        "type": "string",
                    },
                    "role": {
                        "type": "string",
                        "enum": [
                            "PRIMARY",
                            "SUPPORTING",
                            "NONE",
                        ],
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                    },
                },
                "required": [
                    "demand_id",
                    "topic_id",
                    "role",
                    "confidence",
                ],
                "additionalProperties": False,
            },
        },
        "uncovered_demand_ids": {
            "type": "array",
            "items": {
                "type": "string",
            },
        },
        "reason": {
            "type": "string",
        },
    },
    "required": [
        "routing_mode",
        "demand_mappings",
        "uncovered_demand_ids",
        "reason",
    ],
    "additionalProperties": False,
}


def _resolve_semantic_router_gemini_api_key():
    # Reuse the existing Telegram Gemini credential contract.
    return str(
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
        or ""
    ).strip()


def _semantic_router_should_use_gemini():
    # Production auto-selects Gemini when the existing credential is present.
    provider = str(
        os.getenv("SEMANTIC_ROUTER_PROVIDER", "auto") or "auto"
    ).strip().lower()

    if provider == "gemini":
        return True
    if provider == "ollama":
        return False
    if provider != "auto":
        raise ValueError(
            "SEMANTIC_ROUTER_PROVIDER must be auto, gemini, or ollama"
        )

    return bool(_resolve_semantic_router_gemini_api_key())


def _extract_semantic_router_json_object(raw_text):
    # Parser tolerance only; semantic validation remains in the strict normalizer.
    text = str(raw_text or "").strip()
    if not text:
        raise ValueError("semantic router Gemini response content is empty")

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end < start:
            raise
        value = json.loads(text[start : end + 1])

    if not isinstance(value, dict):
        raise ValueError(
            "semantic router Gemini content must be JSON object"
        )
    return value


def _call_semantic_router_gemini_json(prompt):
    # Same credential, model, endpoint, and generation contract as Telegram.
    import urllib.error
    import urllib.request

    api_key = _resolve_semantic_router_gemini_api_key()
    model = str(
        os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        or "gemini-2.5-flash"
    ).strip()
    timeout = float(
        os.getenv("SEMANTIC_ROUTER_GEMINI_TIMEOUT", "180") or "180"
    )

    if not api_key:
        raise ValueError(
            "semantic router Gemini credential is missing"
        )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + model
        + ":generateContent"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": str(prompt or "")}],
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "topP": 1.0,
            "candidateCount": 1,
            "maxOutputTokens": 4096,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            envelope = json.loads(
                response.read().decode(
                    "utf-8",
                    errors="replace",
                )
            )
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode(
                "utf-8",
                errors="replace",
            )
        except Exception:
            pass
        raise RuntimeError(
            "semantic router Gemini HTTPError "
            + str(exc.code)
            + ": "
            + body[:1000]
        ) from exc

    if not isinstance(envelope, dict):
        raise ValueError(
            "semantic router Gemini response envelope must be object"
        )

    candidates = envelope.get("candidates") or []
    if not candidates:
        raise ValueError(
            "semantic router Gemini response has no candidates"
        )

    first = candidates[0]
    if not isinstance(first, dict):
        raise ValueError(
            "semantic router Gemini candidate must be object"
        )

    content = first.get("content") or {}
    parts = (
        content.get("parts") or []
        if isinstance(content, dict)
        else []
    )

    raw_text = "".join(
        str(part.get("text") or "")
        for part in parts
        if isinstance(part, dict)
    )

    return _extract_semantic_router_json_object(raw_text)


def _append_semantic_router_hard_contract(
    prompt,
    question_text,
    question_demand_result,
    candidate_catalog,
):
    demand_rows = (
        question_demand_result.get("demands") or []
        if isinstance(question_demand_result, dict)
        else []
    )
    demand_ids = [
        str(row.get("id") or "").strip()
        for row in demand_rows
        if isinstance(row, dict)
        and str(row.get("id") or "").strip()
    ]
    candidate_ids = [
        str(row.get("topic_id") or "").strip()
        for row in (candidate_catalog or [])
        if isinstance(row, dict)
        and str(row.get("topic_id") or "").strip()
    ]

    lines = [
        "",
        "",
        "STRICT ROUTER CONTRACT:",
        "",
        "This is NOT an exam-answering task.",
        "Do NOT answer, solve, summarize, or explain the examination question.",
        "Your only task is Topic Router v2 semantic adjudication.",
        "",
        "Question:",
        str(question_text or ""),
        "",
        "You MUST evaluate ALL supplied demands:",
        json.dumps(demand_rows, ensure_ascii=False, sort_keys=True),
        "",
        "Allowed demand_id values ONLY:",
        json.dumps(demand_ids, ensure_ascii=False),
        "",
        "Allowed candidate topic_id values ONLY:",
        json.dumps(candidate_ids, ensure_ascii=False),
        "",
        "Rules:",
        "1. Never invent a demand_id.",
        "2. Never invent a topic_id.",
        "3. Consider every supplied demand separately.",
        "4. A Topic is PRIMARY when it directly owns the semantic knowledge needed to answer that demand.",
        "5. A Topic is SUPPORTING only when useful but not an owner.",
        "6. Use NONE only when no supplied Topic covers that demand.",
        "7. If two or more distinct Topics are PRIMARY anywhere in the mappings, routing_mode MUST be MULTI_TOPIC.",
        "8. If exactly one distinct Topic is PRIMARY, routing_mode MUST be SINGLE_TOPIC.",
        "9. Do not use the student's answer.",
        "10. Do not score anything.",
        "11. Do not collapse distinct candidate Topics into one generic Topic merely because they belong to the same broad technical family.",
        "",
        "Return exactly one JSON object and no markdown/prose outside it.",
        "",
        "Required top-level keys exactly:",
        "routing_mode, demand_mappings, uncovered_demand_ids, reason",
        "",
        "Every demand_mappings item must contain exactly:",
        "demand_id, topic_id, role, confidence",
        "",
        "routing_mode must be one of:",
        "SINGLE_TOPIC, MULTI_TOPIC, GENERAL, AMBIGUOUS",
        "",
        "role must be one of:",
        "PRIMARY, SUPPORTING, NONE",
        "",
        "confidence must be a number from 0.0 through 1.0.",
    ]

    return str(prompt or "") + "\n".join(lines)


def _call_semantic_router_json(
    prompt: str,
) -> dict[str, Any]:
    # Dedicated structured-JSON transport for Topic Router v2.
    if _semantic_router_should_use_gemini():
        return _call_semantic_router_gemini_json(prompt)

    payload = {
        "model": SEMANTIC_ROUTER_MODEL,
        "stream": False,
        "format": SEMANTIC_ROUTER_RESPONSE_SCHEMA,
        "options": {
            "temperature": 0.0,
            "top_p": 1.0,
            "top_k": 64,
            "seed": 0,
        },
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the semantic adjudication transport for "
                    "Topic Router v2. Return exactly one JSON object "
                    "matching the user-supplied routing schema. "
                    "Do not answer the examination question. "
                    "Do not add markdown or prose outside JSON."
                ),
            },
            {
                "role": "user",
                "content": str(prompt or ""),
            },
        ],
    }

    request = urllib.request.Request(
        SEMANTIC_ROUTER_OLLAMA_URL + "/api/chat",
        data=json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(
        request,
        timeout=SEMANTIC_ROUTER_TIMEOUT,
    ) as response:
        raw = response.read().decode(
            "utf-8",
            errors="replace",
        )

    envelope = json.loads(raw)
    if not isinstance(envelope, dict):
        raise ValueError(
            "semantic router Ollama response envelope must be object"
        )

    content = (
        (envelope.get("message") or {}).get("content")
        or envelope.get("response")
        or ""
    )

    if isinstance(content, dict):
        result = content
    else:
        content_text = str(content or "").strip()
        if not content_text:
            raise ValueError(
                "semantic router Ollama response content is empty"
            )
        result = json.loads(content_text)

    if not isinstance(result, dict):
        raise ValueError(
            "semantic router Ollama content must be JSON object"
        )

    return result


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
    prompt = _append_semantic_router_hard_contract(
        prompt,
        question,
        question_demand_result,
        catalog,
    )

    if llm_call is None:
        llm_call = _call_semantic_router_json

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

# SEMANTIC_ROUTER_GENERAL_MODE_HARD_CONTRACT_V1
_semantic_router_previous_append_hard_contract = (
    _append_semantic_router_hard_contract
)


def _append_semantic_router_hard_contract(
    prompt,
    question_text,
    question_demand_result,
    candidate_catalog,
):
    base_prompt = _semantic_router_previous_append_hard_contract(
        prompt,
        question_text,
        question_demand_result,
        candidate_catalog,
    )

    return (
        str(base_prompt).rstrip()
        + """

[SEMANTIC_ROUTER_GENERAL_MODE_HARD_CONTRACT_V1]

The following mode-consistency rules are mandatory and override any
conflicting interpretation:

1. routing_mode == "GENERAL":
   - primary_topic_ids MUST be [].
   - supporting_topic_ids MUST be [].
   - demand_mappings MUST NOT assign any positive Topic role.
   - every valid question demand id MUST appear in uncovered_demand_ids.
   - do not retain a Topic merely because it appeared in the candidate catalog.

2. routing_mode == "SINGLE_TOPIC":
   - primary_topic_ids MUST contain exactly one allowed candidate Topic id.
   - any supporting_topic_ids and positive Topic demand mappings MUST use only
     allowed candidate Topic ids.
   - demands not sufficiently owned by an allowed Topic MUST remain in
     uncovered_demand_ids.

3. routing_mode == "MULTI_TOPIC":
   - primary_topic_ids MUST contain only allowed candidate Topic ids.
   - supporting_topic_ids and positive Topic demand mappings MUST use only
     allowed candidate Topic ids.
   - demands not sufficiently owned by an allowed Topic MUST remain in
     uncovered_demand_ids.

4. Mixed Topic + uncovered-demand coverage:
   - If at least one allowed candidate Topic clearly owns at least one demand,
     routing_mode MUST NOT be GENERAL merely because other demands are not
     covered by Topic Packs.
   - Use SINGLE_TOPIC when exactly one Topic is positively selected.
   - Use MULTI_TOPIC when multiple Topics are positively selected.
   - Keep every non-owned demand in uncovered_demand_ids.
   - This is how hybrid Topic + General coverage is represented. Do NOT invent
     a new routing mode named HYBRID.
   - Example: D1 is owned by Topic A and D2 is not owned by any Topic:
     routing_mode="SINGLE_TOPIC", primary_topic_ids=["Topic A"],
     D1 has a positive Topic mapping, and uncovered_demand_ids=["D2"].

5. routing_mode == "AMBIGUOUS":
   - do not convert uncertainty into GENERAL merely to avoid choosing a Topic.

6. Never invent Topic ids. Never use the student answer for routing.

Before returning JSON, perform this consistency check:
- If mode is GENERAL, erase all positive Topic assignments and mark all valid
  demand ids uncovered.
- If any positive Topic assignment remains, mode MUST NOT be GENERAL.
"""
    )
