"""
Generic score reconciliation for professional engineer answer grading.

Design principle
----------------
- The LLM judges semantic issues:
  fatal logic error, demand alignment, cap validity, and question type lens.
- Python only performs numeric operations:
  score extraction, sum/average, penalty conversion, final score adjustment,
  and pass/high-score flag recalculation.

This module intentionally avoids topic-specific keyword rules.
It must not contain logic such as "if answer contains FOC" or
"if question contains comparison". Those semantic decisions belong to the LLM.
"""

from __future__ import annotations

import json
from typing import Any, Callable

JsonDict = dict[str, Any]


def _to_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _sum_score_items(items: Any) -> float | None:
    """Sum numeric score-like fields from a list of scoring items."""
    if not isinstance(items, list):
        return None

    total = 0.0
    count = 0

    for item in items:
        if not isinstance(item, dict):
            continue

        score = _to_float(item.get("score"), None)
        if score is None:
            score = _to_float(item.get("points"), None)

        if score is None:
            continue

        total += score
        count += 1

    if count == 0:
        return None

    return round(total, 2)


def _average_rater_total(parsed: JsonDict) -> float | None:
    """Average total_score from rater_results or raters if present."""
    raters = parsed.get("rater_results") or parsed.get("raters") or []
    if not isinstance(raters, list):
        return None

    values: list[float] = []

    for rater in raters:
        if not isinstance(rater, dict):
            continue

        score = _to_float(rater.get("total_score"), None)
        if score is not None:
            values.append(score)

    if not values:
        return None

    return round(sum(values) / len(values), 2)


def best_uncapped_numeric_score(parsed: JsonDict) -> float | None:
    """
    Find the best numeric score candidate before cap/ceiling.

    This function does not judge answer quality.
    It only reads numeric fields already produced by the grading pipeline.
    """
    if not isinstance(parsed, dict):
        return None

    max_score = _to_float(parsed.get("max_score"), 25.0) or 25.0
    candidates: list[float] = []

    direct_keys = [
        "uncapped_total_score",
        "pre_ceiling_total_score",
        "base_total_score",
        "raw_total_score",
        "weighted_total_score",
        "committee_total_score",
    ]

    for key in direct_keys:
        score = _to_float(parsed.get(key), None)
        if score is not None:
            candidates.append(score)

    cap_eval = parsed.get("difficulty_ceiling_evaluation") or {}
    if isinstance(cap_eval, dict):
        cap_keys = direct_keys + [
            "original_score",
            "score_before_cap",
            "pre_cap_score",
            "uncapped_score",
        ]

        for key in cap_keys:
            score = _to_float(cap_eval.get(key), None)
            if score is not None:
                candidates.append(score)

    breakdown_keys = [
        "breakdown",
        "average_breakdown",
        "layer_breakdown",
        "scoring_breakdown",
        "final_breakdown",
    ]

    for key in breakdown_keys:
        score = _sum_score_items(parsed.get(key))
        if score is not None:
            candidates.append(score)

    rater_avg = _average_rater_total(parsed)
    if rater_avg is not None:
        candidates.append(rater_avg)

    clean = []
    for score in candidates:
        score = _to_float(score, None)
        if score is None:
            continue
        if 0 <= score <= max_score + 0.5:
            clean.append(round(score, 2))

    if not clean:
        return None

    return max(clean)


def _logic_check_has_fatal(parsed: JsonDict) -> bool:
    """Check explicit fatal markers already produced by the logic-check layer."""
    logic_eval = (
        parsed.get("logic_check_evaluation")
        or parsed.get("logic_check_result")
        or parsed.get("logic_check")
        or {}
    )

    if not isinstance(logic_eval, dict):
        return False

    if logic_eval.get("fatal_error_detected"):
        return True

    verdict = str(logic_eval.get("verdict") or "").strip().lower()
    if verdict == "fatal":
        return True

    findings = logic_eval.get("findings") or []
    if not isinstance(findings, list):
        return False

    for item in findings:
        if not isinstance(item, dict):
            continue
        severity = str(item.get("severity") or item.get("verdict") or "").strip().lower()
        if severity == "fatal":
            return True

    return False


def _compact_grade_payload_for_llm(parsed: JsonDict) -> JsonDict:
    """Keep the adjudicator prompt focused and reasonably small."""
    keys = [
        "total_score",
        "max_score",
        "score_range",
        "grade_confidence",
        "confidence",
        "summary",
        "one_line_summary",
        "overall_comment",
        "rater_summary",
        "question_type",
        "question_type_v2",
        "question_type_coverage",
        "question_type_coverage_summary",
        "difficulty_ceiling_evaluation",
        "logic_check_evaluation",
        "logic_check_result",
        "breakdown",
        "rater_results",
        "strengths",
        "weaknesses",
        "rewrite_advice",
        "next_practice_focus",
    ]
    return {key: parsed.get(key) for key in keys if key in parsed}


def _safe_extract_json(text: str) -> JsonDict | None:
    """Extract a JSON object from an LLM response."""
    if not text:
        return None

    text = str(text).strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start < 0 or end <= start:
        return None

    try:
        parsed = json.loads(text[start : end + 1])
    except Exception:
        return None

    if not isinstance(parsed, dict):
        return None

    return parsed


def _default_adjudication(reason: str) -> JsonDict:
    return {
        "fatal_logic_error": False,
        "cap_decision": "keep",
        "demand_alignment": "major_drift",
        "question_type_decision": "keep",
        "suggested_question_type": "UNKNOWN",
        "confidence": "low",
        "reason": reason,
        "schema_valid": False,
    }


def _normalize_adjudication(result: Any) -> JsonDict:
    """
    Normalize and validate the LLM adjudicator output.

    This function does not infer semantic quality from answer keywords.
    It only validates enum fields and accepts a small structural legacy alias:
    "decision" may be treated as "cap_decision" only if the value is exactly
    keep, soften, or remove.
    """
    if not isinstance(result, dict):
        return _default_adjudication("LLM adjudicator returned non-object JSON")

    allowed_cap = {"keep", "soften", "remove"}
    allowed_alignment = {"full", "minor_drift", "major_drift", "off_topic"}
    allowed_type_decision = {"keep", "change"}
    allowed_confidence = {"high", "medium", "low"}
    allowed_question_types = {
        "DEFINE",
        "PRINCIPLE_INTERPRETATION",
        "STRUCTURE",
        "COMPARE_SELECTION",
        "DIAGNOSIS_ACTION",
        "IMPLEMENTATION_EVALUATION",
        "PROBLEM_SOLVE",
        "CAUSE_ACTION",
        "PROCEDURE",
        "CALC_DESIGN",
        "UNKNOWN",
    }

    schema_valid = True

    cap_decision = result.get("cap_decision")
    if cap_decision is None:
        legacy = result.get("decision")
        if legacy in allowed_cap:
            cap_decision = legacy
        else:
            schema_valid = False

    if cap_decision not in allowed_cap:
        cap_decision = "keep"
        schema_valid = False

    demand_alignment = result.get("demand_alignment")
    if demand_alignment not in allowed_alignment:
        demand_alignment = "major_drift"
        schema_valid = False

    question_type_decision = result.get("question_type_decision")
    if question_type_decision not in allowed_type_decision:
        question_type_decision = "keep"
        schema_valid = False

    suggested_question_type = result.get("suggested_question_type") or "UNKNOWN"
    if suggested_question_type not in allowed_question_types:
        suggested_question_type = "UNKNOWN"
        schema_valid = False

    confidence = result.get("confidence")
    if confidence not in allowed_confidence:
        confidence = "low"
        schema_valid = False

    reason = result.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        reason = "LLM adjudicator response did not include a valid reason"
        schema_valid = False

    normalized = {
        "fatal_logic_error": bool(result.get("fatal_logic_error")),
        "cap_decision": cap_decision,
        "demand_alignment": demand_alignment,
        "question_type_decision": question_type_decision,
        "suggested_question_type": suggested_question_type,
        "confidence": confidence,
        "reason": reason.strip(),
        "schema_valid": schema_valid,
    }

    if not schema_valid:
        normalized["raw_adjudication"] = result

    return normalized


def _build_cap_adjudicator_prompt(
    *,
    raw_text: str,
    parsed: JsonDict,
    current_score: float,
    uncapped_score: float,
) -> str:
    payload = {
        "student_submission": raw_text,
        "current_score_after_cap": current_score,
        "uncapped_numeric_score_before_cap": uncapped_score,
        "score_gap": round(uncapped_score - current_score, 2),
        "grade_result": _compact_grade_payload_for_llm(parsed),
    }

    return f"""
너는 기술사 논술형 답안의 사후 검증자다.

너의 임무는 점수를 새로 매기는 것이 아니다.
너의 임무는 기존 채점 결과에서 difficulty ceiling 또는 cap이 의미적으로 타당한지 판정하는 것이다.

용어 정의:
- current_score_after_cap: 현재 최종 점수다. 이미 cap이 적용된 뒤의 점수일 수 있다.
- uncapped_numeric_score_before_cap: Python이 기존 채점 결과의 A/B/C/D/E, rater total, pre-cap 필드에서 추출한 cap 적용 전 후보 점수다.
- cap_decision:
  - keep: 현재 cap 점수를 그대로 유지해야 한다.
  - soften: cap은 일부 타당하지만 너무 강하므로 current_score와 uncapped_score 사이로 부분 회복해야 한다.
  - remove: fatal 오류가 없고 문제 요구를 충족하므로 cap을 제거하고 uncapped_score를 기준으로 해야 한다.

중요 판단 원칙:
- 숫자 점수를 새로 계산하지 마라.
- 최종 점수 숫자를 제안하지 마라.
- 특정 단어 포함 여부로 판정하지 마라.
- 문제 요구와 답안 내용의 의미 관계를 판단하라.
- 핵심 이론 fatal이 명시적으로 있으면 fatal_logic_error=true로 한다.
- 단순 누락, 표현 부족, 일부 전개 미흡, 추가 설명은 fatal이 아니다.
- 답안이 문제 핵심 요구를 충족하고 fatal이 없으면, 큰 score_gap을 만드는 strict cap은 보통 keep이 아니라 soften 또는 remove 대상이다.
- 답안이 문제 요구를 벗어나거나 핵심 요구를 흐리면 demand_alignment를 낮게 판단한다.
- cap_decision의 keep은 피드백을 유지한다는 뜻이 아니라 낮아진 cap 점수를 유지한다는 뜻이다.

반드시 아래 JSON 형식으로만 답하라.
다른 설명, markdown, 코드블록을 출력하지 마라.

{{
  "fatal_logic_error": false,
  "cap_decision": "remove",
  "demand_alignment": "full",
  "question_type_decision": "keep",
  "suggested_question_type": "UNKNOWN",
  "confidence": "high",
  "reason": "판정 사유를 한두 문장으로 설명"
}}

허용값:
- cap_decision: keep, soften, remove
- demand_alignment: full, minor_drift, major_drift, off_topic
- question_type_decision: keep, change
- suggested_question_type: DEFINE, PRINCIPLE_INTERPRETATION, STRUCTURE, COMPARE_SELECTION, DIAGNOSIS_ACTION, IMPLEMENTATION_EVALUATION, PROBLEM_SOLVE, CAUSE_ACTION, PROCEDURE, CALC_DESIGN, UNKNOWN
- confidence: high, medium, low

입력:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def _build_schema_repair_prompt(
    *,
    first_response: str,
    raw_text: str,
    parsed: JsonDict,
    current_score: float,
    uncapped_score: float,
) -> str:
    payload = {
        "student_submission": raw_text,
        "current_score_after_cap": current_score,
        "uncapped_numeric_score_before_cap": uncapped_score,
        "score_gap": round(uncapped_score - current_score, 2),
        "grade_result": _compact_grade_payload_for_llm(parsed),
        "invalid_previous_response": first_response,
    }

    return f"""
이전 응답은 요구 JSON 스키마를 지키지 않았다.

다시 판정하라.

주의:
- decision 이라는 키를 쓰지 마라.
- 반드시 cap_decision 키를 써라.
- confidence를 반드시 high, medium, low 중 하나로 써라.
- demand_alignment를 반드시 full, minor_drift, major_drift, off_topic 중 하나로 써라.
- question_type_decision을 반드시 keep 또는 change 중 하나로 써라.
- suggested_question_type을 반드시 허용값 중 하나로 써라.
- 숫자 점수를 제안하지 마라.
- cap_decision은 현재 cap 점수를 유지할지 여부에 대한 판단이다.

반드시 아래 JSON만 출력하라.

{{
  "fatal_logic_error": false,
  "cap_decision": "remove",
  "demand_alignment": "full",
  "question_type_decision": "keep",
  "suggested_question_type": "UNKNOWN",
  "confidence": "high",
  "reason": "판정 사유를 한두 문장으로 설명"
}}

허용값:
- cap_decision: keep, soften, remove
- demand_alignment: full, minor_drift, major_drift, off_topic
- question_type_decision: keep, change
- suggested_question_type: DEFINE, PRINCIPLE_INTERPRETATION, STRUCTURE, COMPARE_SELECTION, DIAGNOSIS_ACTION, IMPLEMENTATION_EVALUATION, PROBLEM_SOLVE, CAUSE_ACTION, PROCEDURE, CALC_DESIGN, UNKNOWN
- confidence: high, medium, low

입력:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def call_llm_cap_adjudicator(
    *,
    raw_text: str,
    parsed: JsonDict,
    current_score: float,
    uncapped_score: float,
    call_llm_fn: Callable[[str], str],
) -> JsonDict:
    """
    Ask the LLM to judge cap validity semantically.

    The LLM must not calculate a score.
    It only returns enum decisions.

    If the LLM violates the schema, run one schema-repair retry.
    """
    first_prompt = _build_cap_adjudicator_prompt(
        raw_text=raw_text,
        parsed=parsed,
        current_score=current_score,
        uncapped_score=uncapped_score,
    )

    first_raw = call_llm_fn(first_prompt)
    first_result = _safe_extract_json(first_raw)
    first_normalized = _normalize_adjudication(first_result)

    if first_normalized.get("schema_valid"):
        first_normalized.pop("schema_valid", None)
        return first_normalized

    repair_prompt = _build_schema_repair_prompt(
        first_response=first_raw,
        raw_text=raw_text,
        parsed=parsed,
        current_score=current_score,
        uncapped_score=uncapped_score,
    )

    repair_raw = call_llm_fn(repair_prompt)
    repair_result = _safe_extract_json(repair_raw)
    repair_normalized = _normalize_adjudication(repair_result)

    if repair_normalized.get("schema_valid"):
        repair_normalized["schema_repaired"] = True
        repair_normalized["first_invalid_response"] = first_raw
        repair_normalized.pop("schema_valid", None)
        return repair_normalized

    return _structured_cap_fallback(
        parsed=parsed,
        current_score=current_score,
        uncapped_score=uncapped_score,
        first_invalid_response=first_raw,
        repair_invalid_response=repair_raw,
    )



def _nested_dict(value: Any) -> JsonDict:
    return value if isinstance(value, dict) else {}


def _semantic_coverage_is_strong(parsed: JsonDict) -> bool:
    """
    Use already-structured semantic coverage from the grading pipeline.

    This function does not inspect topic-specific words.
    It only reads normalized coverage fields already produced upstream.
    """
    coverage = _nested_dict(parsed.get("question_type_coverage"))

    overall = str(
        coverage.get("overall_coverage")
        or coverage.get("detail_coverage")
        or coverage.get("coverage")
        or ""
    ).strip().lower()

    if overall in {"strong", "excellent", "high", "full"}:
        return True

    missing = coverage.get("missing_sub_criteria")
    if isinstance(missing, list) and len(missing) == 0:
        c_focus = _nested_dict(coverage.get("c_fact_focus_coverage"))
        d_focus = _nested_dict(coverage.get("d_field_judgement_focus_coverage"))

        c_missing = c_focus.get("missing")
        d_missing = d_focus.get("missing")

        if isinstance(c_missing, list) and isinstance(d_missing, list):
            return len(c_missing) == 0 and len(d_missing) == 0

    return False


def _structured_cap_fallback(
    *,
    parsed: JsonDict,
    current_score: float,
    uncapped_score: float,
    first_invalid_response: str = "",
    repair_invalid_response: str = "",
) -> JsonDict:
    """
    Fallback when the LLM adjudicator repeatedly fails the JSON contract.

    This fallback does not use topic-specific keywords.
    It relies only on structured outputs already produced by earlier grading phases:
    - difficulty_ceiling_evaluation
    - theory_core_evidence
    - logic_check flags
    - question_type_coverage
    """
    max_score = _to_float(parsed.get("max_score"), 25.0) or 25.0
    high_target = _to_float(parsed.get("high_score_target"), round(max_score * 0.8, 2))

    cap_eval = _nested_dict(parsed.get("difficulty_ceiling_evaluation"))
    theory_evidence = _nested_dict(cap_eval.get("theory_core_evidence"))

    original_score = _to_float(cap_eval.get("original_score"), uncapped_score)
    if original_score is None:
        original_score = uncapped_score

    score_gap = round(uncapped_score - current_score, 2)

    cap_applied = bool(cap_eval.get("cap_applied")) or score_gap >= 1.0
    unlock_high_band = bool(theory_evidence.get("unlock_high_band")) or bool(
        cap_eval.get("unlock_high_band")
    )

    fatal = (
        _logic_check_has_fatal(parsed)
        or bool(theory_evidence.get("fatal_error_suspected"))
        or bool(cap_eval.get("logic_check_fatal_error_detected"))
    )

    coverage_strong = _semantic_coverage_is_strong(parsed)

    base = {
        "fatal_logic_error": fatal,
        "question_type_decision": "keep",
        "suggested_question_type": "UNKNOWN",
        "confidence": "medium",
        "schema_fallback": True,
        "first_invalid_response": first_invalid_response,
        "repair_invalid_response": repair_invalid_response,
        "structured_signals": {
            "current_score": current_score,
            "uncapped_score": uncapped_score,
            "original_score": original_score,
            "score_gap": score_gap,
            "cap_applied": cap_applied,
            "unlock_high_band": unlock_high_band,
            "coverage_strong": coverage_strong,
            "fatal": fatal,
            "high_target": high_target,
        },
    }

    if fatal:
        return {
            **base,
            "cap_decision": "keep",
            "demand_alignment": "major_drift",
            "reason": (
                "LLM adjudicator가 JSON 스키마를 반복 실패했으나, "
                "기존 구조화 logic-check 신호에서 fatal 가능성이 있어 cap을 유지함."
            ),
        }

    if not cap_applied or score_gap < 1.0:
        return {
            **base,
            "cap_decision": "keep",
            "demand_alignment": "major_drift",
            "reason": (
                "LLM adjudicator가 JSON 스키마를 반복 실패했고, "
                "구조화 점수 신호상 cap 보정이 필요한 큰 점수 차이가 없어 cap을 유지함."
            ),
        }

    if original_score >= high_target and coverage_strong and unlock_high_band:
        return {
            **base,
            "cap_decision": "soften",
            "demand_alignment": "full",
            "reason": (
                "LLM adjudicator가 JSON 스키마를 반복 실패했으나, "
                "기존 구조화 채점 결과에서 fatal 없음, high-band unlock, strong coverage, "
                "큰 cap gap이 확인되어 strict cap을 부분 완화함."
            ),
        }

    if original_score >= high_target and coverage_strong:
        return {
            **base,
            "cap_decision": "soften",
            "demand_alignment": "minor_drift",
            "reason": (
                "LLM adjudicator가 JSON 스키마를 반복 실패했으나, "
                "기존 구조화 채점 결과에서 고득점권 원점수와 strong coverage가 확인되어 "
                "strict cap을 제한적으로 완화함."
            ),
        }

    return {
        **base,
        "cap_decision": "keep",
        "demand_alignment": "major_drift",
        "reason": (
            "LLM adjudicator가 JSON 스키마를 반복 실패했고, "
            "구조화 신호만으로 cap 완화 조건을 충분히 확인하지 못해 cap을 유지함."
        ),
    }


def _alignment_penalty(alignment: Any) -> float:
    """
    Convert LLM demand-alignment enum into a numeric penalty.

    The semantic choice is made by the LLM.
    Python only applies this fixed numeric table.
    """
    table = {
        "full": 0.0,
        "minor_drift": 1.0,
        "major_drift": 2.5,
        "off_topic": 999.0,
    }
    return table.get(str(alignment or "").strip(), 2.5)


def _apply_numeric_flags(parsed: JsonDict) -> JsonDict:
    """Recalculate pass/target/high-score flags from final total_score."""
    try:
        from explicit_requirement_cap import (
            enforce_existing_explicit_requirement_cap,
        )

        parsed = enforce_existing_explicit_requirement_cap(parsed)
    except Exception:
        pass

    total = _to_float(parsed.get("total_score"), 0.0) or 0.0
    max_score = _to_float(parsed.get("max_score"), 25.0) or 25.0

    official = _to_float(parsed.get("official_pass_score"), round(max_score * 0.60, 2))
    practical = _to_float(parsed.get("practical_target_score"), round(max_score * 0.70, 2))
    high = _to_float(parsed.get("high_score_target"), round(max_score * 0.80, 2))

    parsed["official_pass_score"] = official
    parsed["practical_target_score"] = practical
    parsed["high_score_target"] = high

    parsed["official_pass_met"] = total >= official
    parsed["practical_target_met"] = total >= practical
    parsed["average_target_met"] = total >= practical
    parsed["high_score_met"] = total >= high

    return parsed


def reconcile_grade_score(
    *,
    parsed: JsonDict,
    raw_text: str,
    call_llm_fn: Callable[[str], str],
) -> JsonDict:
    """
    Generic cap reconciliation.

    Semantic judgment:
    - LLM adjudicator

    Numeric calculation:
    - Python only

    No topic-specific keyword rules are used.
    """
    if not isinstance(parsed, dict):
        return parsed

    max_score = _to_float(parsed.get("max_score"), 25.0) or 25.0
    current_score = _to_float(parsed.get("total_score"), None)

    if current_score is None:
        return parsed

    uncapped_score = best_uncapped_numeric_score(parsed)

    if uncapped_score is None:
        parsed["llm_cap_adjudication_skipped"] = {
            "reason": "uncapped numeric score 후보가 없어 보정하지 않음",
        }
        return _apply_numeric_flags(parsed)

    cap_eval = parsed.get("difficulty_ceiling_evaluation")
    if not isinstance(cap_eval, dict):
        cap_eval = {}
        parsed["difficulty_ceiling_evaluation"] = cap_eval

    score_gap = round(uncapped_score - current_score, 2)

    if score_gap < 1.0:
        parsed["llm_cap_adjudication_skipped"] = {
            "reason": "uncapped_score와 current_score 차이가 작아 보정 불필요",
            "current_score": current_score,
            "uncapped_score": uncapped_score,
            "score_gap": score_gap,
        }
        return _apply_numeric_flags(parsed)

    if _logic_check_has_fatal(parsed):
        parsed["llm_cap_adjudication_skipped"] = {
            "reason": "기존 Logic Check fatal이 있어 cap 유지",
            "current_score": current_score,
            "uncapped_score": uncapped_score,
            "score_gap": score_gap,
        }
        return _apply_numeric_flags(parsed)

    adjudication = call_llm_cap_adjudicator(
        raw_text=raw_text,
        parsed=parsed,
        current_score=current_score,
        uncapped_score=uncapped_score,
        call_llm_fn=call_llm_fn,
    )

    parsed["llm_cap_adjudication"] = adjudication

    fatal = bool(adjudication.get("fatal_logic_error"))
    cap_decision = str(adjudication.get("cap_decision") or "keep").strip()
    alignment = str(adjudication.get("demand_alignment") or "major_drift").strip()
    confidence = str(adjudication.get("confidence") or "low").strip()

    if fatal:
        cap_eval["llm_cap_reconciliation"] = "kept_due_to_llm_fatal"
        return _apply_numeric_flags(parsed)

    if confidence == "low":
        cap_eval["llm_cap_reconciliation"] = "kept_due_to_low_confidence"
        return _apply_numeric_flags(parsed)

    if alignment == "off_topic":
        cap_eval["llm_cap_reconciliation"] = "kept_due_to_off_topic"
        return _apply_numeric_flags(parsed)

    if cap_decision == "keep":
        cap_eval["llm_cap_reconciliation"] = "kept_by_llm"
        return _apply_numeric_flags(parsed)

    penalty = _alignment_penalty(alignment)

    if cap_decision == "soften":
        target = current_score + (score_gap * 0.6) - penalty
    elif cap_decision == "remove":
        target = uncapped_score - penalty
    else:
        cap_eval["llm_cap_reconciliation"] = "kept_due_to_unknown_decision"
        return _apply_numeric_flags(parsed)

    adjusted = round(max(current_score, min(target, max_score)), 1)

    if adjusted <= current_score:
        cap_eval["llm_cap_reconciliation"] = "no_numeric_raise_after_penalty"
        cap_eval["uncapped_score_detected"] = uncapped_score
        cap_eval["alignment_penalty"] = penalty
        return _apply_numeric_flags(parsed)

    parsed["total_score"] = adjusted
    parsed["score_range"] = (
        f"{max(0.0, adjusted - 0.5):.1f}~"
        f"{min(max_score, adjusted + 0.5):.1f}"
    )

    cap_eval["cap_applied"] = False
    cap_eval["cap_overridden_by_llm_adjudication"] = True
    cap_eval["original_capped_score"] = current_score
    cap_eval["uncapped_score_detected"] = uncapped_score
    cap_eval["alignment_penalty"] = penalty
    cap_eval["adjusted_score"] = adjusted
    cap_eval["effective_score"] = adjusted
    cap_eval["effective_policy"] = "llm_adjusted_cap_relaxation"
    cap_eval["llm_cap_reconciliation"] = "adjusted"

    # Keep final grade-level score metadata consistent with the adjusted score.
    # Deterministic strict cap was calculated first, but later adjudication
    # partially relaxed it because fatal error was not found and high-band
    # unlock evidence existed.
    parsed["total_score"] = adjusted
    parsed["final_total_score"] = adjusted
    parsed["pre_ceiling_total_score"] = uncapped_score

    try:
        parsed["score_range"] = (
            f"{max(0.0, adjusted - 0.5):.1f}~"
            f"{min(max_score, adjusted + 0.5):.1f}"
        )
    except Exception:
        pass

    cap_eval["reason"] = (
        f"THEORY_CORE strict ceiling 후보 {current_score}점이 산출되었으나, "
        f"fatal 오류 없음, high-band unlock 근거, 구조화 채점 강도를 반영하여 "
        f"최종 점수를 {adjusted}점으로 부분 완화했습니다."
    )
    cap_eval["llm_reason"] = adjudication.get("reason", "")

    if adjudication.get("question_type_decision") == "change":
        suggested = adjudication.get("suggested_question_type")
        if suggested and suggested != "UNKNOWN":
            parsed["question_type"] = suggested

            coverage = parsed.get("question_type_coverage")
            if not isinstance(coverage, dict):
                coverage = {}
                parsed["question_type_coverage"] = coverage

            coverage["question_type_lens"] = suggested
            coverage["reason"] = adjudication.get("reason", "")

    parsed["ceiling_reconciliation_note"] = (
        f"LLM cap adjudication applied: {current_score} -> {adjusted}. "
        f"uncapped={uncapped_score}, cap_decision={cap_decision}, "
        f"demand_alignment={alignment}, penalty={penalty}."
    )

    return _apply_numeric_flags(parsed)
