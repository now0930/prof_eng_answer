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

    for row in demand_rows:
        demand_tokens = set(row["tokens"])
        overlap = claim_tokens.intersection(
            demand_tokens
        )

        # One shared generic word is not enough to establish
        # Question Demand scope. Require at least two tokens
        # from the same explicit Demand.
        if len(overlap) >= 2:
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
            "originality numeric bonus unchanged; feedback-only scope sanitation"
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
        "adjustments": [],
    }
    if not isinstance(rows, list) or not isinstance(baseline_scores, dict):
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
        for value in _list(guard.get("blocked_layer_ids"))
        if _text(value)
    }
    diagnostic["active"] = guard.get("active") is True

    for row in rows:
        if not isinstance(row, dict):
            continue
        layer_id = _text(row.get("layer_id"))
        if layer_id not in blocked or layer_id not in baseline_scores:
            continue
        try:
            baseline = float(baseline_scores[layer_id])
            current = float(row.get("score") or 0.0)
        except (TypeError, ValueError, OverflowError):
            continue

        row["score_before_hybrid_demand_scope_guard"] = current
        row["score"] = round(baseline, 3)
        row["hybrid_demand_scope_guard_applied"] = True
        row["reason"] = (
            "Hybrid demand-scope guard: 명시 Question Demand 범위 밖의 "
            "semantic 감점 근거를 제외하여 사전 semantic 점수로 복원함."
        )
        diagnostic["adjustments"].append(
            {
                "layer_id": layer_id,
                "before_guard": current,
                "restored_score": round(baseline, 3),
            }
        )

    diagnostic["applied"] = bool(diagnostic["adjustments"])
    return rows, diagnostic
