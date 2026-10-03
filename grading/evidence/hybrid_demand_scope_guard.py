from __future__ import annotations

import copy
import re
from typing import Any

HYBRID_DEMAND_SCOPE_GUARD_VERSION = "hybrid_demand_scope_guard_v1"
HYBRID_DEMAND_SCOPE_GUARD_MARKER = "HYBRID_DEMAND_SCOPE_GUARD_V1"

_NEGATIVE_CUES = (
    "부족", "누락", "미흡", "없음", "없다", "필요", "보완",
    "추가", "낮아", "제한", "취약", "incorrect", "missing",
    "insufficient",
)
_STOPWORDS = {
    "설명", "설명하시오", "제시", "제시하시오",
    "방법", "대한", "대해", "등", "및",
}
_PARTICLES = (
    "에서", "으로", "에게", "부터", "까지", "처럼", "보다",
    "의", "을", "를", "은", "는", "이", "가", "에", "로", "과", "와",
)
_SPLIT_RE = re.compile(
    r"[,;]|(?:\s+및\s+)|(?:\s+또한\s+)|"
    r"(?:\s+그러나\s+)|(?:\s+하지만\s+)|(?:\s+또는\s+)"
)
_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[가-힣]+")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value or "").strip()


def _strip_particle(token: str) -> str:
    for suffix in _PARTICLES:
        if token.endswith(suffix) and len(token) >= len(suffix) + 2:
            return token[:-len(suffix)]
    return token


def _tokens(value: Any) -> list[str]:
    out = []
    for raw in _TOKEN_RE.findall(_text(value).lower()):
        token = _strip_particle(raw)
        if not token or token in _STOPWORDS:
            continue
        if token not in out:
            out.append(token)
    return out


def _hybrid_evidence(subject_rubric: Any) -> dict[str, Any] | None:
    if not isinstance(subject_rubric, dict):
        return None
    evidence = subject_rubric.get("hybrid_general_grading_evidence")
    if not isinstance(evidence, dict):
        return None
    if evidence.get("coverage_kind") != "HYBRID_TOPIC_GENERAL":
        return None
    if evidence.get("routing_mode") != "SINGLE_TOPIC":
        return None
    mappings = evidence.get("demand_mappings")
    if not isinstance(mappings, list) or not mappings:
        return None
    if not all(
        isinstance(row, dict)
        and _text(row.get("demand_id"))
        and _text(row.get("demand_text"))
        for row in mappings
    ):
        return None
    return evidence


def _demand_token_rows(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for mapping in _list(evidence.get("demand_mappings")):
        if not isinstance(mapping, dict):
            continue
        demand_id = _text(mapping.get("demand_id"))
        demand_text = _text(mapping.get("demand_text"))
        tokens = _tokens(demand_text)
        if not demand_id or not demand_text or not tokens:
            continue
        rows.append(
            {
                "demand_id": demand_id,
                "demand_text": demand_text,
                "tokens": tokens,
                "intent_tokens": tokens[-2:],
                "role": _text(mapping.get("role")),
            }
        )
    return rows


def _traceable(
    claim_text: Any,
    demand_rows: list[dict[str, Any]],
) -> bool:
    claim_tokens = set(_tokens(claim_text))
    if not claim_tokens:
        return False

    token_sets = [
        set(_list(row.get("tokens")))
        for row in demand_rows
        if isinstance(row, dict)
    ]

    for index, row in enumerate(demand_rows):
        if not isinstance(row, dict):
            continue

        demand_tokens = set(
            _list(row.get("tokens"))
        )
        intent_tokens = set(
            _list(row.get("intent_tokens"))
        )

        if not demand_tokens:
            continue

        # Two-token demands such as "온도 보상" and
        # "Wheatstone Bridge" are scope-safe only when the
        # complete phrase is represented.
        if len(demand_tokens) <= 2:
            if demand_tokens.issubset(
                claim_tokens
            ):
                return True
            continue

        # A complete demand intent such as "측정 원리",
        # "결정 기준", or "폐기 원칙" is independently
        # strong enough to establish traceability.
        if (
            intent_tokens
            and intent_tokens.issubset(
                claim_tokens
            )
        ):
            return True

        # Otherwise require BOTH:
        #   1) one intent token, and
        #   2) one subject token distinctive to this Demand.
        #
        # This prevents generic collisions such as
        # "교정 + 결정", "점검 + 기준", or an entity name
        # alone from expanding the explicit question scope.
        subject_tokens = (
            demand_tokens - intent_tokens
        )

        other_tokens = set()
        for other_index, other_set in enumerate(
            token_sets
        ):
            if other_index == index:
                continue
            other_tokens.update(other_set)

        distinctive_subject = (
            subject_tokens - other_tokens
        )

        if (
            distinctive_subject.intersection(
                claim_tokens
            )
            and intent_tokens.intersection(
                claim_tokens
            )
        ):
            return True

    return False


def _negative(value: Any) -> bool:
    text = _text(value).lower()
    return any(cue.lower() in text for cue in _NEGATIVE_CUES)


def _negative_fragments_traceable(
    value: Any,
    demand_rows: list[dict[str, Any]],
) -> bool:
    text = _text(value)
    if not text:
        return True
    negative_fragments = [
        fragment.strip()
        for fragment in _SPLIT_RE.split(text)
        if fragment.strip() and _negative(fragment)
    ]
    if not negative_fragments:
        return True
    return all(_traceable(fragment, demand_rows) for fragment in negative_fragments)


def _issue_is_scope_safe(
    row: Any,
    demand_rows: list[dict[str, Any]],
) -> bool:
    if not isinstance(row, dict):
        return False
    issue_type = _text(
        row.get("defect_type")
        or row.get("issue_type")
        or row.get("type")
    ).lower()
    if issue_type == "correctness_error":
        return True
    claim = (
        _text(row.get("explanation"))
        or _text(row.get("reason"))
        or _text(row.get("evidence_text"))
        or _text(row.get("evidence"))
        or _text(row.get("description"))
    )
    if not claim:
        return True
    return _negative_fragments_traceable(claim, demand_rows)


def _generic_summary(parsed: dict[str, Any]) -> str:
    advice = [
        _text(item)
        for item in _list(parsed.get("improvement_advice"))
        if _text(item)
    ]
    base = (
        "명시된 Question Demand 기준으로 평가했으며, "
        "Topic evidence의 비요구 항목은 감점·보완 요구에서 제외했습니다."
    )
    if advice:
        return base + " 주요 보완 범위: " + " / ".join(advice[:2])
    return base


def sanitize_hybrid_semantic_evaluation(
    evaluation: Any,
    subject_rubric: Any,
) -> Any:
    evidence = _hybrid_evidence(subject_rubric)
    if evidence is None or not isinstance(evaluation, dict):
        return evaluation
    parsed = evaluation.get("parsed")
    if not isinstance(parsed, dict):
        return evaluation
    demand_rows = _demand_token_rows(evidence)
    if not demand_rows:
        return evaluation

    updated = copy.deepcopy(evaluation)
    parsed = updated["parsed"]
    removed = []
    blocked_layer_ids = set()

    def remove(path: str, text: Any, layer_id: str = ""):
        removed.append(
            {
                "path": path,
                "text": _text(text),
                "layer_id": layer_id,
                "reason": "not_traceable_to_explicit_demand",
            }
        )
        if layer_id:
            blocked_layer_ids.add(layer_id)

    layers = parsed.get("layers")
    if isinstance(layers, list):
        for index, row in enumerate(layers):
            if not isinstance(row, dict):
                continue
            layer_id = _text(row.get("layer_id"))
            reason = _text(row.get("reason"))
            if (
                reason
                and _negative(reason)
                and not _negative_fragments_traceable(reason, demand_rows)
            ):
                remove(f"parsed.layers[{index}].reason", reason, layer_id)
                row["reason"] = (
                    "Hybrid demand-scope guard: "
                    "명시 Question Demand 범위 밖 semantic 감점 근거를 제외함."
                )

            evidence_rows = row.get("evidence")
            if isinstance(evidence_rows, list):
                kept = []
                for evidence_index, item in enumerate(evidence_rows):
                    if (
                        isinstance(item, str)
                        and _negative(item)
                        and not _negative_fragments_traceable(item, demand_rows)
                    ):
                        remove(
                            f"parsed.layers[{index}].evidence[{evidence_index}]",
                            item,
                            layer_id,
                        )
                        continue
                    kept.append(item)
                row["evidence"] = kept

    advice = parsed.get("improvement_advice")
    if isinstance(advice, list):
        kept = []
        for index, item in enumerate(advice):
            if not isinstance(item, str):
                kept.append(item)
                continue
            if not _traceable(item, demand_rows):
                remove(f"parsed.improvement_advice[{index}]", item)
                continue
            kept.append(item)
        parsed["improvement_advice"] = kept

    raters = parsed.get("rater_comments")
    if isinstance(raters, list):
        kept = []
        for index, row in enumerate(raters):
            if not isinstance(row, dict):
                kept.append(row)
                continue
            comment = _text(row.get("comment"))
            if (
                comment
                and _negative(comment)
                and not _negative_fragments_traceable(comment, demand_rows)
            ):
                remove(f"parsed.rater_comments[{index}].comment", comment)
                continue
            kept.append(row)
        parsed["rater_comments"] = kept

    coverage = _dict(parsed.get("question_type_coverage"))
    coverage_changed = False

    for focus_key in (
        "c_fact_focus_coverage",
        "d_field_judgement_focus_coverage",
    ):
        focus = _dict(coverage.get(focus_key))
        missing = focus.get("missing")
        if not isinstance(missing, list):
            continue
        kept = []
        for index, item in enumerate(missing):
            if isinstance(item, str) and not _traceable(item, demand_rows):
                remove(
                    f"parsed.question_type_coverage.{focus_key}.missing[{index}]",
                    item,
                )
                coverage_changed = True
                continue
            kept.append(item)
        focus["missing"] = kept
        coverage[focus_key] = focus

    sub_criteria = coverage.get("sub_criteria_coverage")
    if isinstance(sub_criteria, list):
        for index, row in enumerate(sub_criteria):
            if not isinstance(row, dict):
                continue
            status = _text(row.get("status")).lower()
            evidence_text = _text(row.get("evidence"))
            if status not in {"partial", "missing", "incorrect"}:
                continue
            if (
                evidence_text
                and not _negative_fragments_traceable(evidence_text, demand_rows)
            ):
                remove(
                    f"parsed.question_type_coverage.sub_criteria_coverage[{index}]",
                    evidence_text,
                )
                row["status"] = "present"
                row["evidence"] = (
                    "Hybrid demand-scope guard: "
                    "명시 Question Demand 범위 밖 보완 요구를 제외함."
                )
                row["impact"] = "scope-neutral"
                coverage_changed = True

    scoring_hint = _text(coverage.get("scoring_hint"))
    if (
        coverage_changed
        or (
            scoring_hint
            and _negative(scoring_hint)
            and not _negative_fragments_traceable(scoring_hint, demand_rows)
        )
    ):
        if scoring_hint:
            remove("parsed.question_type_coverage.scoring_hint", scoring_hint)
        coverage["scoring_hint"] = (
            "명시 Question Demand와 직접 연결되는 근거만 채점에 사용함."
        )

    if coverage:
        statuses = [
            _text(row.get("status")).lower()
            for row in _list(coverage.get("sub_criteria_coverage"))
            if isinstance(row, dict)
        ]
        if statuses and not any(
            status in {"missing", "incorrect"} for status in statuses
        ):
            coverage["overall_coverage"] = "adequate"
        parsed["question_type_coverage"] = coverage

    issues = parsed.get("layer_issue_ownership")
    if isinstance(issues, list):
        kept = []
        for index, row in enumerate(issues):
            if _issue_is_scope_safe(row, demand_rows):
                kept.append(row)
                continue
            remove(
                f"parsed.layer_issue_ownership[{index}]",
                _dict(row).get("reason") or _dict(row).get("explanation"),
                _text(
                    _dict(row).get("primary_owner_layer")
                    or _dict(row).get("owner_layer")
                ),
            )
        parsed["layer_issue_ownership"] = kept

    general = _dict(parsed.get("general_evidence_contract"))
    defects = general.get("defects")
    if isinstance(defects, list):
        kept = []
        for index, row in enumerate(defects):
            if _issue_is_scope_safe(row, demand_rows):
                kept.append(row)
                continue
            remove(
                f"parsed.general_evidence_contract.defects[{index}]",
                _dict(row).get("explanation") or _dict(row).get("evidence_text"),
                _text(_dict(row).get("owner_layer")),
            )
        general["defects"] = kept
        parsed["general_evidence_contract"] = general

    if removed:
        parsed["overall_comment"] = _generic_summary(parsed)

    updated["hybrid_demand_scope_guard"] = {
        "version": HYBRID_DEMAND_SCOPE_GUARD_VERSION,
        "marker": HYBRID_DEMAND_SCOPE_GUARD_MARKER,
        "active": True,
        "routing_mode": evidence.get("routing_mode"),
        "coverage_kind": evidence.get("coverage_kind"),
        "demand_ids": [row["demand_id"] for row in demand_rows],
        "blocked_layer_ids": sorted(blocked_layer_ids),
        "removed_claims": removed,
        "raw_text_preserved": (
            updated.get("raw_text") == evaluation.get("raw_text")
        ),
        "score_effect": (
            "blocked semantic layers restored to pre-semantic baseline by caller"
        ),
    }
    return updated


def sanitize_hybrid_originality_evaluation(
    evaluation: Any,
    subject_rubric: Any,
) -> Any:
    evidence = _hybrid_evidence(subject_rubric)
    if evidence is None or not isinstance(evaluation, dict):
        return evaluation
    parsed = evaluation.get("parsed")
    if not isinstance(parsed, dict):
        return evaluation
    demand_rows = _demand_token_rows(evidence)
    if not demand_rows:
        return evaluation

    updated = copy.deepcopy(evaluation)
    parsed = updated["parsed"]
    removed = []
    advice = parsed.get("improvement_advice")

    if isinstance(advice, list):
        kept = []
        for index, item in enumerate(advice):
            if isinstance(item, str) and not _traceable(item, demand_rows):
                removed.append(
                    {
                        "path": f"parsed.improvement_advice[{index}]",
                        "text": item,
                        "reason": "not_traceable_to_explicit_demand",
                    }
                )
                continue
            kept.append(item)
        parsed["improvement_advice"] = kept

    updated["hybrid_demand_scope_guard"] = {
        "version": HYBRID_DEMAND_SCOPE_GUARD_VERSION,
        "marker": HYBRID_DEMAND_SCOPE_GUARD_MARKER,
        "active": True,
        "routing_mode": evidence.get("routing_mode"),
        "coverage_kind": evidence.get("coverage_kind"),
        "removed_claims": removed,
        "raw_text_preserved": (
            updated.get("raw_text") == evaluation.get("raw_text")
        ),
        "score_effect": (
            "numeric scope handled by pre-normalization O1-O5 projection; feedback sanitation applied here"
        ),
    }
    return updated


def restore_blocked_semantic_layer_scores(
    layer_scores: Any,
    baseline_scores: Any,
    gemini_eval: Any,
):
    rows = (
        copy.deepcopy(layer_scores)
        if isinstance(layer_scores, list)
        else layer_scores
    )
    diagnostic = {
        "version": HYBRID_DEMAND_SCOPE_GUARD_VERSION,
        "marker": HYBRID_DEMAND_SCOPE_GUARD_MARKER,
        "active": False,
        "applied": False,
        "policy": (
            "scope_neutral_downward_only_v1"
        ),
        "adjustments": [],
        "preserved_upward_layers": [],
    }

    if not isinstance(rows, list):
        return rows, diagnostic
    if not isinstance(baseline_scores, dict):
        return rows, diagnostic

    guard = (
        gemini_eval.get("hybrid_demand_scope_guard")
        if isinstance(gemini_eval, dict)
        else None
    )
    if not isinstance(guard, dict):
        return rows, diagnostic

    blocked = {
        _text(value)
        for value in _list(
            guard.get("blocked_layer_ids")
        )
        if _text(value)
    }
    diagnostic["active"] = (
        guard.get("active") is True
    )

    for row in rows:
        if not isinstance(row, dict):
            continue

        layer_id = _text(row.get("layer_id"))
        if (
            layer_id not in blocked
            or layer_id not in baseline_scores
        ):
            continue

        try:
            baseline = float(
                baseline_scores[layer_id]
            )
            current = float(
                row.get("score") or 0.0
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
        ):
            continue

        # Scope guard is directional. If semantic scoring is
        # already above the pre-semantic baseline, an out-of-scope
        # negative claim did not create a downward score effect.
        # Keep the score and remove only the invalid rationale.
        if current >= baseline:
            row[
                "hybrid_demand_scope_guard_applied"
            ] = False
            row[
                "hybrid_demand_scope_guard_policy"
            ] = (
                "preserve_non_downward_semantic_score"
            )
            diagnostic[
                "preserved_upward_layers"
            ].append(
                {
                    "layer_id": layer_id,
                    "baseline": round(
                        baseline,
                        3,
                    ),
                    "semantic_score": round(
                        current,
                        3,
                    ),
                }
            )
            continue

        row[
            "score_before_hybrid_demand_scope_guard"
        ] = current
        row["score"] = round(baseline, 3)
        row[
            "hybrid_demand_scope_guard_applied"
        ] = True
        row[
            "hybrid_demand_scope_guard_policy"
        ] = (
            "block_out_of_scope_downward_effect"
        )
        row["reason"] = (
            "Hybrid demand-scope guard: "
            "명시 Question Demand 범위 밖의 "
            "semantic 감점 근거가 점수를 낮춘 경우에만 "
            "사전 semantic 점수를 하한으로 적용함."
        )
        diagnostic["adjustments"].append(
            {
                "layer_id": layer_id,
                "before_guard": round(
                    current,
                    3,
                ),
                "restored_score": round(
                    baseline,
                    3,
                ),
            }
        )

    diagnostic["applied"] = bool(
        diagnostic["adjustments"]
    )
    return rows, diagnostic

def project_hybrid_model_answer_feedback(
    model_answer_ref: Any,
):
    diagnostic = {
        "version": HYBRID_DEMAND_SCOPE_GUARD_VERSION,
        "marker": HYBRID_DEMAND_SCOPE_GUARD_MARKER,
        "active": False,
        "removed_feedback_items": [],
        "preserved_feedback_items": [],
        "score_effect": "none",
        "evidence_mutated": False,
    }

    if not isinstance(model_answer_ref, dict):
        return {}, diagnostic

    evidence = model_answer_ref.get(
        "hybrid_general_grading_context"
    )
    subject_rubric = {
        "hybrid_general_grading_evidence": (
            evidence
        )
    }
    hybrid = _hybrid_evidence(
        subject_rubric
    )

    primary = model_answer_ref.get(
        "primary_reference"
    )
    if not isinstance(primary, dict):
        return {}, diagnostic

    if hybrid is None:
        return primary, diagnostic

    demand_rows = _demand_token_rows(
        hybrid
    )
    if not demand_rows:
        return primary, diagnostic

    projected = copy.deepcopy(primary)
    diagnostic["active"] = True

    for field in (
        "expected_structure",
        "field_connection_points",
        "low_score_patterns",
    ):
        value = primary.get(field)
        if not isinstance(value, list):
            continue

        kept = []

        for index, item in enumerate(value):
            if not isinstance(item, str):
                kept.append(item)
                continue

            if _traceable(
                item,
                demand_rows,
            ):
                kept.append(item)
                diagnostic[
                    "preserved_feedback_items"
                ].append(
                    {
                        "field": field,
                        "index": index,
                        "text": item,
                    }
                )
            else:
                diagnostic[
                    "removed_feedback_items"
                ].append(
                    {
                        "field": field,
                        "index": index,
                        "text": item,
                        "reason": (
                            "not_traceable_to_explicit_demand"
                        ),
                    }
                )

        projected[field] = kept

    return projected, diagnostic
def build_hybrid_originality_scope_contract(
    subject_rubric: Any,
) -> dict[str, Any]:
    evidence = _hybrid_evidence(subject_rubric)

    if evidence is None:
        return {}

    rows = _demand_token_rows(evidence)

    if not rows:
        return {}

    return {
        "version": "hybrid_originality_demand_scope_v1",
        "marker": "HYBRID_ORIGINALITY_DEMAND_SCOPE_V1",
        "active": True,
        "routing_mode": evidence.get("routing_mode"),
        "coverage_kind": evidence.get("coverage_kind"),
        "demand_mappings": [
            {
                "demand_id": row.get("demand_id"),
                "demand_text": row.get("demand_text"),
                "role": row.get("role"),
            }
            for row in rows
        ],
        "policy": {
            "explicit_demand_fulfillment_is_baseline": True,
            "out_of_scope_absence_is_not_originality_defect": True,
            "bonus_requires_scope_traceable_judgement": True,
            "topic_evidence_is_not_checklist": True,
            "one_question_one_score": True,
        },
    }


def _originality_text_is_negative_or_limiting(
    value: Any,
) -> bool:
    text = _text(value).lower()

    if not text:
        return False

    markers = (
        "부족",
        "미흡",
        "누락",
        "없음",
        "없다",
        "않음",
        "않다",
        "언급되지",
        "제시되지",
        "고려되지",
        "일반론",
        "단순",
        "키워드만",
        "만 제시",
        "그치",
    )

    return any(marker in text for marker in markers)


def _originality_evidence_supports_positive_bonus(
    anchor_id: Any,
    evidence_text: Any,
    demand_rows: list[dict[str, Any]],
) -> bool:
    text = _text(evidence_text)

    if not text or not _traceable(text, demand_rows):
        return False

    if _originality_text_is_negative_or_limiting(text):
        return False

    anchor = _text(anchor_id).upper()
    signals = {
        "O1": (
            "재해석", "설계", "운전", "유지보수", "관리",
            "위험", "제약", "문제 정의",
        ),
        "O2": (
            "조건", "환경", "제약", "적용", "선정",
            "기존 설비", "운전",
        ),
        "O3": (
            "비교", "대비", "trade", "비용", "리스크",
            "정밀도", "성능", "장단점", "대안",
        ),
        "O4": (
            "우선", "먼저", "단계", "순서", "필요 시",
            "적용 후", "검토 후",
        ),
        "O5": (
            "검증", "시험", "확인", "판정", "추적",
            "as-found", "as-left",
        ),
    }

    required = signals.get(anchor)
    if not required:
        return True

    lowered = text.lower()
    return any(signal.lower() in lowered for signal in required)


def _originality_reason_has_untraceable_negative_fragment(
    reason: Any,
    demand_rows: list[dict[str, Any]],
) -> bool:
    text = _text(reason)

    if not text:
        return False

    if not (
        _negative(text)
        or _originality_text_is_negative_or_limiting(text)
    ):
        return False

    import re as _re

    # Split explanatory reasons at punctuation and contrast boundaries.
    # This catches mixed reasons such as:
    #   "온도 보상은 설명했으나 설치 환경 고려가 부족함"
    # where the first clause is in-scope but the negative requirement is not.
    fragments = [
        fragment.strip()
        for fragment in _re.split(
            r"(?:[.!?;]\s*|,\s*|"
            r"했으나\s*|하지만\s*|그러나\s*|다만\s*)",
            text,
        )
        if fragment.strip()
    ]

    negative_fragments = [
        fragment
        for fragment in fragments
        if (
            _negative(fragment)
            or _originality_text_is_negative_or_limiting(fragment)
        )
    ]

    if not negative_fragments:
        return not _traceable(
            text,
            demand_rows,
        )

    return any(
        not _traceable(
            fragment,
            demand_rows,
        )
        for fragment in negative_fragments
    )


def project_hybrid_originality_pre_normalization(
    evaluation: Any,
    subject_rubric: Any,
) -> Any:
    evidence = _hybrid_evidence(subject_rubric)

    if (
        evidence is None
        or not isinstance(evaluation, dict)
    ):
        return evaluation

    parsed = evaluation.get("parsed")

    if not isinstance(parsed, dict):
        return evaluation

    demand_rows = _demand_token_rows(evidence)

    if not demand_rows:
        return evaluation

    updated = copy.deepcopy(evaluation)
    parsed = updated["parsed"]
    anchors = parsed.get("anchors")

    diagnostic = {
        "version": HYBRID_DEMAND_SCOPE_GUARD_VERSION,
        "marker": "HYBRID_ORIGINALITY_PRE_NORMALIZATION_SCOPE_V1",
        "active": True,
        "routing_mode": evidence.get("routing_mode"),
        "coverage_kind": evidence.get("coverage_kind"),
        "removed_anchor_evidence": [],
        "neutralized_anchor_reasons": [],
        "zeroed_anchor_ids": [],
        "positive_support_evidence": {},
        "projected_anchor_ids": [],
        "raw_text_preserved": (
            updated.get("raw_text")
            == evaluation.get("raw_text")
        ),
        "score_effect": (
            "O1-O5 projected to explicit Question Demand before "
            "average/raw originality normalization"
        ),
    }

    projected_levels = []

    if isinstance(anchors, list):
        for index, anchor in enumerate(anchors):
            if not isinstance(anchor, dict):
                continue

            anchor_id = _text(anchor.get("id"))
            evidence_rows = anchor.get("evidence")
            kept_evidence = []
            positive_support_evidence = []

            if isinstance(evidence_rows, list):
                for evidence_index, item in enumerate(
                    evidence_rows
                ):
                    if not isinstance(item, str):
                        kept_evidence.append(item)
                        continue

                    if _traceable(
                        item,
                        demand_rows,
                    ):
                        kept_evidence.append(item)

                        if _originality_evidence_supports_positive_bonus(
                            anchor_id,
                            item,
                            demand_rows,
                        ):
                            positive_support_evidence.append(item)

                        continue

                    diagnostic[
                        "removed_anchor_evidence"
                    ].append(
                        {
                            "path": (
                                "parsed.anchors"
                                f"[{index}].evidence"
                                f"[{evidence_index}]"
                            ),
                            "anchor_id": anchor_id,
                            "text": item,
                            "reason": (
                                "not_traceable_to_explicit_demand"
                            ),
                        }
                    )

                anchor["evidence"] = kept_evidence

            reason = _text(anchor.get("reason"))

            if (
                reason
                and _originality_reason_has_untraceable_negative_fragment(
                    reason,
                    demand_rows,
                )
            ):
                diagnostic[
                    "neutralized_anchor_reasons"
                ].append(
                    {
                        "path": (
                            f"parsed.anchors[{index}].reason"
                        ),
                        "anchor_id": anchor_id,
                        "text": reason,
                        "reason": (
                            "out_of_scope_negative_requirement"
                        ),
                    }
                )

                if kept_evidence:
                    anchor["reason"] = (
                        "Hybrid demand-scope projection: "
                        "명시 Question Demand와 직접 연결되는 "
                        "답안 근거만 Originality 판단에 사용함."
                    )
                else:
                    anchor["reason"] = (
                        "Hybrid demand-scope projection: "
                        "명시 Question Demand 범위 밖의 "
                        "Originality 요구는 점수 근거에서 제외함."
                    )

            try:
                level = float(anchor.get("level") or 0.0)
            except (
                TypeError,
                ValueError,
                OverflowError,
            ):
                level = 0.0

            level = max(
                0.0,
                min(1.0, level),
            )

            if level > 0.0 and not positive_support_evidence:
                diagnostic[
                    "zeroed_anchor_ids"
                ].append(anchor_id)
                level = 0.0
                anchor["level"] = 0.0

                reason_is_scope_safe = (
                    bool(reason)
                    and not _originality_reason_has_untraceable_negative_fragment(
                        reason,
                        demand_rows,
                    )
                    and _traceable(
                        reason,
                        demand_rows,
                    )
                )

                if not reason_is_scope_safe:
                    anchor["reason"] = (
                        "Hybrid demand-scope projection: "
                        "명시 Demand의 단순 충족 또는 부족 설명만으로는 "
                        "독립적인 Originality 가점을 지지하지 못하므로 "
                        "이 anchor 가점을 0으로 함."
                    )
            else:
                anchor["level"] = round(
                    level,
                    3,
                )

            diagnostic[
                "positive_support_evidence"
            ][anchor_id] = list(positive_support_evidence)

            projected_levels.append(level)
            diagnostic[
                "projected_anchor_ids"
            ].append(anchor_id)

    average = (
        sum(projected_levels)
        / len(projected_levels)
        if projected_levels
        else 0.0
    )
    raw_score = average * 2.0

    for key in (
        "reported_raw_originality_score",
        "bounded_reported_raw_originality_score",
        "anchor_derived_originality_score",
        "originality_score_source",
        "originality_score_consistency_adjustment",
        "max_allowed_after_gates",
        "final_originality_score",
        "applied_caps",
        "final_bonus_to_D",
        "final_bonus_to_E",
        "bonus_policy",
    ):
        parsed.pop(key, None)

    parsed["average_level"] = round(
        average,
        3,
    )
    parsed["raw_originality_score"] = round(
        raw_score,
        3,
    )
    parsed[
        "hybrid_originality_scope_projection"
    ] = diagnostic

    updated[
        "hybrid_originality_scope_projection"
    ] = diagnostic

    return updated
