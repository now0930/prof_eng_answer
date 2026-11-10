"""Question-only deterministic Topic routing for verdict-authority migration."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from grading.evidence.fact_anchor_scoring_exclusions import excluded_from_scoring
from grading.evidence.fact_anchor_evidence_adapter import _question_similarity
from grading.routing.model_answer_router import find_model_answer_reference
from grading.routing.question_type_router import detect_question_type
from grading.rubrics.rubric_registry import normalize_text


VERSION = "deterministic_topic_router_v1"
MARKER = "DETERMINISTIC_TOPIC_ROUTER_V1"
ROOT = Path(__file__).resolve().parents[2]

# These are question-demand cues, not engineering subjects. Remove them only
# from the auxiliary text-similarity calculation; explicit aliases, ontology
# concepts, and authored question contracts remain intact.
_GENERIC_DEMAND_CUES = re.compile(
    r"측정\s*원리|발생\s*원리|작동\s*원리|원리|특성|특징|장단점|비교|"
    r"정확도(?:에|를|의)?|오차(?:요인|원인)?|영향을?\s*주는|영향|요인|"
    r"개선\s*대책|개선\s*방안|개선|저감|방지|대책|예방|"
    r"설계\s*기준|설계\s*요소|설계|기준|현장\s*적용|현장|적용\s*조건|적용|조건|"
    r"유지\s*보수|유지보수|경제성|선정|운영\s*고려|고려사항|고려|"
    r"설명하시오|서술하시오|기술하시오|제시하시오|검토하시오|비교하시오|"
    r"설명|기술|제시|검토|하시오|하라|"
    r"measurement\s*principle|measurement|principle|characteristics?|features?|"
    r"accuracy|error\s*factors?|factors?|impact|effects?|improvement|mitigation|"
    r"prevention|design\s*criteria|design|field\s*application|application\s*conditions?|"
    r"maintenance|economics|selection|compare|comparison|explain|describe|discuss|analyze|analyse",
    re.IGNORECASE,
)


def _subject_similarity(left: str, right: str) -> float:
    """Compare technical-subject text after stripping generic demand wording."""
    def clean(value: str) -> str:
        subject = _GENERIC_DEMAND_CUES.sub(" ", value)
        subject = re.sub(r"[\[\]{}()<>.,:;!?·/\\|]+", " ", subject)
        subject = re.sub(
            r"(?<![가-힣])(?:그리고|그러나|및|또는|와|과|의|에|에서|으로|로|를|을|은|는|이|가|시)(?![가-힣])",
            " ", subject,
        )
        return re.sub(r"\s+", " ", subject).strip()

    left_subject = clean(left)
    right_subject = clean(right)
    if not left_subject or not right_subject:
        return 0.0
    return _question_similarity(left_subject, right_subject)


@lru_cache(maxsize=1)
def _ontology_anchor_alias_index() -> dict[str, tuple[dict[str, str], ...]]:
    """Map existing ontology aliases to Topic Packs that own them as anchor terms.

    This is an index over current authored data, not a new fact or an approval
    path. Only exact concept-alias/core-term ownership is used.
    """
    concepts_path = ROOT / "grading_ontology/engineering_concepts.json"
    payload = json.loads(concepts_path.read_text(encoding="utf-8"))
    concepts_by_alias: dict[str, list[dict[str, str]]] = {}
    for row in payload.get("concepts", []):
        concept_id = str(row.get("id") or "")
        for alias in row.get("aliases", []):
            alias_key = normalize_text(str(alias))
            if len(alias_key) < 4:
                continue
            concepts_by_alias.setdefault(alias_key, []).append({
                "concept_id": concept_id,
                "alias": str(alias),
            })
    owners_by_alias: dict[str, list[dict[str, str]]] = {}

    for anchor_path in sorted((ROOT / "rubrics/topic_packs").glob("*/fact_anchor.json")):
        topic_id = anchor_path.parent.name
        anchors = json.loads(anchor_path.read_text(encoding="utf-8")).get("anchors", [])
        for anchor in anchors:
            anchor_id = str(anchor.get("anchor_id") or anchor.get("id") or "")
            if excluded_from_scoring(topic_id=topic_id, anchor_id=anchor_id):
                continue
            terms = anchor.get("core_terms") or anchor.get("keywords") or []
            term_keys = {normalize_text(str(term)) for term in terms if str(term).strip()}
            for alias_key, owners in concepts_by_alias.items():
                if alias_key not in term_keys:
                    continue
                for owner in owners:
                    owner_record = {
                        **owner,
                        "topic_id": topic_id,
                        "anchor_id": anchor_id,
                    }
                    existing = owners_by_alias.setdefault(alias_key, [])
                    if owner_record not in existing:
                        existing.append(owner_record)

    return {key: tuple(rows) for key, rows in owners_by_alias.items()}


def _ontology_subject_hits(question_text: str) -> dict[str, list[dict[str, str]]]:
    normalized_question = normalize_text(question_text)
    hits: dict[str, list[dict[str, str]]] = {}
    for alias_key, owners in _ontology_anchor_alias_index().items():
        if alias_key not in normalized_question:
            continue
        for owner in owners:
            hits.setdefault(owner["topic_id"], []).append(owner)
    return hits


def _pack_candidates(question_text: str) -> list[dict[str, Any]]:
    normalized_question = normalize_text(question_text)
    ontology_hits = _ontology_subject_hits(question_text)
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "rubrics/topic_packs").glob("*/model_answer.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        patterns = []
        pattern_rows: list[dict[str, Any]] = []
        for value in payload.get("expected_question_patterns", []):
            pattern = str(
                value.get("pattern") or value.get("question") or ""
                if isinstance(value, dict) else value
            )
            patterns.append(pattern)
            if isinstance(value, dict):
                pattern_rows.append({
                    "pattern": pattern,
                    "routing_exclusive": bool(value.get("routing_exclusive")),
                    "routing_exclusive_block_terms": [
                        str(term) for term in value.get("routing_exclusive_block_terms", [])
                        if str(term).strip()
                    ],
                })
        patterns.extend(str(value) for value in payload.get("question_examples", []))
        raw_pattern_score = max(
            [_question_similarity(question_text, value) for value in patterns] or [0.0]
        )
        pattern_score = max(
            [_subject_similarity(question_text, value) for value in patterns] or [0.0]
        )
        title = str(payload.get("title_ko") or payload.get("title") or "")
        raw_title_score = 2.0 * _question_similarity(question_text, title)
        title_score = 2.0 * _subject_similarity(question_text, title)
        aliases = list(payload.get("routing_aliases") or payload.get("topic_aliases") or [])
        aliases.extend(payload.get("deterministic_routing_aliases") or [])
        alias_hits = sorted({
            str(value) for value in aliases
            if normalize_text(str(value))
            and normalize_text(str(value)) in normalized_question
        })
        acronym_alias_hits = sorted({
            value.strip() for value in alias_hits
            if re.fullmatch(r"(?=[A-Z0-9]{2,8}\b)(?=.*[A-Z])[A-Z0-9]+", value.strip())
            and re.search(
                rf"(?<![A-Za-z0-9]){re.escape(value.strip())}(?![A-Za-z0-9])",
                question_text,
            )
        })
        rows.append({
            "topic_id": path.parent.name,
            "score": round(max(
                pattern_score,
                title_score,
                1.0 if alias_hits else 0.0,
                1.0 if ontology_hits.get(path.parent.name) else 0.0,
            ), 6),
            "pattern_score": round(pattern_score, 6),
            "raw_pattern_score": round(raw_pattern_score, 6),
            "raw_title_score": round(raw_title_score, 6),
            "alias_hits": alias_hits,
            "acronym_alias_hits": acronym_alias_hits,
            "ontology_subject_hits": ontology_hits.get(path.parent.name, []),
            "selection_reasons": [
                *(["approved_topic_alias"] if alias_hits else []),
                *(["ontology_alias_owned_by_topic_anchor"] if ontology_hits.get(path.parent.name) else []),
                *(["subject_pattern_similarity"] if pattern_score else []),
            ],
            "exclusive_pattern_score": round(max(
                [
                    _subject_similarity(question_text, row["pattern"])
                    for row in pattern_rows
                    if row["routing_exclusive"]
                    and not any(
                        normalize_text(term) in normalized_question
                        for term in row["routing_exclusive_block_terms"]
                    )
                ] or [0.0]
            ), 6),
        })
    return sorted(rows, key=lambda row: (-row["score"], row["topic_id"]))


def route_question_topics(question_text: str) -> dict[str, Any]:
    """Route from the immutable question only; answer text is never consulted."""
    legacy = find_model_answer_reference(
        question_text, "", question_type_eval=detect_question_type(question_text),
    )
    candidates = _pack_candidates(question_text)
    strong_subject_candidates = [
        row for row in candidates
        if row["alias_hits"] or row["ontology_subject_hits"]
    ]
    ontology_only_topics = {
        row["topic_id"] for row in candidates if row["ontology_subject_hits"]
    }
    # A fuzzy exclusive pattern may share only generic demand words, such as
    # "measurement principle" and "application conditions". Preserve a better
    # matching question owner backed by an explicit subject alias in that case.
    # Use pattern similarity here, not the title-weighted candidate score.
    subject_candidates = [
        row for row in candidates
        if (
            any(len(normalize_text(alias)) >= 4 for alias in row["alias_hits"])
            or bool(row["ontology_subject_hits"])
        )
    ]
    exclusive = [
        row for row in candidates if row["exclusive_pattern_score"] >= 0.2
        and not (
            not row["alias_hits"]
            and any(
                other["topic_id"] != row["topic_id"]
                and other["pattern_score"] > row["exclusive_pattern_score"]
                for other in subject_candidates
            )
        )
    ]
    if exclusive:
        selected = max(
            exclusive,
            key=lambda row: (row["exclusive_pattern_score"], row["score"], row["topic_id"]),
        )
        return {
            "version": VERSION,
            "marker": MARKER,
            "engine": "deterministic",
            "provider_calls": 0,
            "answer_text_used": False,
            "status": "ROUTED",
            "source": "exclusive_question_contract",
            "primary_topic_id": selected["topic_id"],
            "topic_ids": [selected["topic_id"]],
            "candidates": candidates[:3],
            "candidate_diagnostics": _candidate_diagnostics(candidates, selected["topic_id"]),
        }
    # Exact ontology concept aliases are strong subject evidence only when an
    # existing eligible Topic Pack anchor owns that exact term. This lets a
    # technical subject outrank generic demand wording without adding aliases
    # or topic-specific code exceptions.
    if ontology_only_topics:
        ontology_candidates = sorted(
            (row for row in candidates if row["topic_id"] in ontology_only_topics),
            key=lambda row: (
                -bool(row["acronym_alias_hits"]),
                -len(row["acronym_alias_hits"]),
                -len(row["alias_hits"]),
                -row["pattern_score"],
                row["topic_id"],
            ),
        )
        selected_topic = None
        if len(ontology_candidates) == 1:
            selected_topic = ontology_candidates[0]["topic_id"]
        elif (
            (
                bool(ontology_candidates[0]["acronym_alias_hits"]),
                len(ontology_candidates[0]["acronym_alias_hits"]),
                len(ontology_candidates[0]["alias_hits"]),
            )
            >
            (
                bool(ontology_candidates[1]["acronym_alias_hits"]),
                len(ontology_candidates[1]["acronym_alias_hits"]),
                len(ontology_candidates[1]["alias_hits"]),
            )
        ):
            selected_topic = ontology_candidates[0]["topic_id"]
        elif (
            ontology_candidates[0]["pattern_score"] >= 0.18
            and ontology_candidates[0]["pattern_score"]
            - ontology_candidates[1]["pattern_score"] >= 0.04
        ):
            # A shared ontology term (such as a platform acronym) may be owned
            # by multiple packs. Resolve only when the subject-only authored
            # question-pattern evidence clearly distinguishes one owner.
            selected_topic = ontology_candidates[0]["topic_id"]
        if selected_topic is None:
            return {
                "version": VERSION,
                "marker": MARKER,
                "engine": "deterministic",
                "provider_calls": 0,
                "answer_text_used": False,
                "status": "ABSTAIN",
                "source": "ambiguous_ontology_topic_ownership",
                "primary_topic_id": None,
                "topic_ids": [],
                "candidates": candidates[:3],
                "candidate_diagnostics": _candidate_diagnostics(candidates, None),
                "diagnostic": {
                    "reason": "ontology_concept_has_multiple_topic_owners_without_clear_pattern_match",
                    "ontology_owner_topic_ids": sorted(ontology_only_topics),
                },
            }
        topic_ids = [selected_topic]
        topic_ids.extend(
            row["topic_id"] for row in ontology_candidates
            if row["topic_id"] != selected_topic
            and row["alias_hits"]
            and (row["acronym_alias_hits"] or row["pattern_score"] >= 0.1)
        )
        return {
            "version": VERSION,
            "marker": MARKER,
            "engine": "deterministic",
            "provider_calls": 0,
            "answer_text_used": False,
            "status": "ROUTED",
            "source": "ontology_subject_anchor",
            "primary_topic_id": selected_topic,
            "topic_ids": topic_ids,
            "candidates": candidates[:3],
            "candidate_diagnostics": _candidate_diagnostics(candidates, selected_topic),
        }
    primary = str((legacy.get("primary_reference") or {}).get("topic_id") or "")
    source = "question_model_answer_router"
    fallback_primary = ""
    if not primary and candidates and candidates[0]["score"] >= 0.1:
        primary = candidates[0]["topic_id"]
        fallback_primary = primary
        source = "question_pack_similarity_fallback"
    # Similarity alone is not sufficient to force a Topic. If neither the
    # question contract nor an approved subject alias identifies an owner,
    # fail closed rather than route on generic prose.
    if source == "question_pack_similarity_fallback" and not strong_subject_candidates:
        best_score = candidates[0]["score"] if candidates else 0.0
        second_score = candidates[1]["score"] if len(candidates) > 1 else 0.0
        if best_score < 0.15 or best_score - second_score < 0.04:
            return {
                "version": VERSION,
                "marker": MARKER,
                "engine": "deterministic",
                "provider_calls": 0,
                "answer_text_used": False,
                "status": "ABSTAIN",
                "source": "ambiguous_or_generic_similarity_only",
                "primary_topic_id": None,
                "topic_ids": [],
                "candidates": candidates[:3],
                "candidate_diagnostics": _candidate_diagnostics(candidates, None),
                "diagnostic": {
                    "reason": "no_approved_specific_subject_evidence_or_candidate_margin",
                    "best_subject_score": best_score,
                    "second_subject_score": second_score,
                },
            }
    if source == "question_pack_similarity_fallback":
        specific_alias_candidates = [
            row for row in candidates
            if row["acronym_alias_hits"]
            or max((len(normalize_text(alias)) for alias in row["alias_hits"]), default=0) >= 4
        ]
        if specific_alias_candidates:
            selected = max(
                specific_alias_candidates,
                key=lambda row: (
                    bool(row["acronym_alias_hits"]),
                    len(row["acronym_alias_hits"]),
                    max(len(normalize_text(alias)) for alias in row["alias_hits"]),
                    row["score"],
                    row["topic_id"],
                ),
            )
            primary = selected["topic_id"]
            source = "specific_question_alias"
    topic_ids = [primary] if primary else []
    # A fuzzy fallback is only a provisional owner. Once an explicit subject
    # alias identifies the primary topic, retaining that fallback can add an
    # unrelated topic (and a synthetic missing question-scope requirement).
    if source == "question_pack_similarity_fallback" and fallback_primary and fallback_primary not in topic_ids:
        topic_ids.append(fallback_primary)
    for row in candidates:
        if (
            row["alias_hits"]
            and (row["acronym_alias_hits"] or row["pattern_score"] >= 0.1)
            and row["topic_id"] not in topic_ids
        ):
            topic_ids.append(row["topic_id"])
    return {
        "version": VERSION,
        "marker": MARKER,
        "engine": "deterministic",
        "provider_calls": 0,
        "answer_text_used": False,
        "status": "ROUTED" if topic_ids else "ABSTAIN",
        "source": source if topic_ids else "no_safe_question_match",
        "primary_topic_id": primary or None,
        "topic_ids": topic_ids,
        "candidates": candidates[:3],
        "candidate_diagnostics": _candidate_diagnostics(candidates, primary or None),
    }


def _candidate_diagnostics(
    candidates: list[dict[str, Any]], selected_topic_id: str | None,
) -> list[dict[str, Any]]:
    """Return compact, deterministic selection/elimination reasons."""
    output = []
    for row in candidates[:5]:
        selected = row["topic_id"] == selected_topic_id
        if selected:
            decision = "selected"
        elif row["acronym_alias_hits"]:
            decision = "specific_identity_alias_not_selected"
        elif row["alias_hits"] or row["ontology_subject_hits"]:
            decision = "subject_conflict_or_secondary_candidate"
        elif (
            row["raw_pattern_score"] > 0
            and row["pattern_score"] < 0.12
        ) or (row["raw_title_score"] > 0 and row["pattern_score"] < 0.12):
            decision = "generic_demand_overlap_only"
        elif row["pattern_score"] > 0:
            decision = "not_selected_lower_subject_match"
        elif row["raw_pattern_score"] > 0 or row["raw_title_score"] > 0:
            decision = "generic_demand_overlap_only"
        else:
            decision = "no_question_evidence"
        output.append({
            "topic_id": row["topic_id"],
            "decision": decision,
            "score": row["score"],
            "subject_pattern_score": row["pattern_score"],
            "raw_pattern_score": row["raw_pattern_score"],
            "alias_hits": row["alias_hits"],
            "acronym_alias_hits": row["acronym_alias_hits"],
            "ontology_subject_concepts": sorted({
                item["concept_id"] for item in row["ontology_subject_hits"]
            }),
            "selection_reasons": row["selection_reasons"],
        })
    return output
