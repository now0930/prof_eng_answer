#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Callable


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PROMPT_PATH = BASE_DIR / "rubrics" / "output_prompts" / "compact_grade_summary.json"




def _logic_check_corrective_points_from_locals(local_vars, limit=3):
    """Find logic_check_evaluation from the current formatter scope and build correction points."""
    def find_grade_like(obj, depth=0):
        if depth > 4:
            return None

        if isinstance(obj, dict):
            logic_eval = obj.get("logic_check_evaluation")
            if isinstance(logic_eval, dict):
                return obj

            # Sometimes the logic evaluation itself is passed around directly.
            if isinstance(obj.get("findings"), list) and (
                obj.get("mode") is not None or obj.get("fatal_error_detected") is not None
            ):
                return {"logic_check_evaluation": obj}

            for key in [
                "grade",
                "result",
                "grade_data",
                "grade_result",
                "data",
                "summary",
                "payload",
                "formatted",
            ]:
                found = find_grade_like(obj.get(key), depth + 1)
                if found:
                    return found

            for value in obj.values():
                found = find_grade_like(value, depth + 1)
                if found:
                    return found

        elif isinstance(obj, (list, tuple)):
            for value in obj:
                found = find_grade_like(value, depth + 1)
                if found:
                    return found

        return None

    if not isinstance(local_vars, dict):
        return _logic_check_corrective_points({}, limit=limit)

    # Prefer explicit local variable names first.
    for name in [
        "grade",
        "result",
        "grade_data",
        "grade_result",
        "data",
        "summary",
        "payload",
    ]:
        found = find_grade_like(local_vars.get(name))
        if found:
            return _logic_check_corrective_points(found, limit=limit)

    # Fallback: scan every local object.
    for value in local_vars.values():
        found = find_grade_like(value)
        if found:
            return _logic_check_corrective_points(found, limit=limit)

    return _logic_check_corrective_points({}, limit=limit)


def _logic_check_corrective_points(grade, limit=3):
    """Build correction points from logic_check_evaluation findings.

    Prefer topic-specific correct_rule values from fatal logic checks.
    This prevents a fatal fallback for one topic from leaking into another topic.
    """
    logic_eval = {}
    if isinstance(grade, dict):
        logic_eval = grade.get("logic_check_evaluation") or {}

    points = []

    if isinstance(logic_eval, dict):
        findings = logic_eval.get("findings") or []

        # 1) Prefer fatal finding correct_rule.
        for finding in findings:
            if not isinstance(finding, dict):
                continue
            if finding.get("severity") != "fatal":
                continue

            correct_rule = str(finding.get("correct_rule") or "").strip()
            if correct_rule and correct_rule not in points:
                points.append(correct_rule)

        # 2) Fallback to next_practice_points if no correct_rule exists.
        if not points:
            for point in logic_eval.get("next_practice_points") or []:
                point = str(point or "").strip()
                if point and point not in points:
                    points.append(point)

    # 3) Generic fallback only. Do not use topic-specific hardcoded text here.
    if not points:
        points = [
            "핵심 개념과 조건을 정답 기준과 일치시키세요.",
            "공식, 변수 의미, 적용 조건을 함께 설명하세요.",
            "현장 적용 시 한계와 보완 대책을 구분하세요.",
        ]

    return points[:limit]


def _txt(value: Any, limit: int = 260) -> str:
    text = " ".join(str(value or "").split()).strip()
    if len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text


def _items(value: Any, limit: int = 4, text_limit: int = 220) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        return []

    result: list[str] = []
    for item in value:
        if isinstance(item, dict):
            text = _txt(
                item.get("message")
                or item.get("reason")
                or item.get("comment")
                or item.get("evidence")
                or item.get("text")
                or item,
                text_limit,
            )
        else:
            text = _txt(item, text_limit)

        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break

    return result


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _load_prompt_config(path: Path | None = None) -> dict[str, Any]:
    prompt_path = path or DEFAULT_PROMPT_PATH
    try:
        data = json.loads(prompt_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    return data if isinstance(data, dict) else {}


def _extract_logic(grade: dict[str, Any]) -> dict[str, Any]:
    logic = grade.get("logic_check_evaluation") or {}
    if not isinstance(logic, dict):
        return {"fatal": False, "mode": "", "findings": []}

    findings = []
    for item in logic.get("findings") or []:
        if not isinstance(item, dict):
            continue
        findings.append({
            "severity": str(item.get("severity") or ""),
            "message": _txt(item.get("message") or item.get("evidence") or "", 320),
            "evidence": _txt(item.get("evidence") or "", 180),
            "correct_rule": _txt(item.get("correct_rule") or "", 420),
        })

    fatal = bool(logic.get("fatal_error_detected"))
    fatal = fatal or any(x.get("severity") == "fatal" for x in findings)

    return {
        "fatal": fatal,
        "mode": logic.get("mode") or ("fatal" if fatal else ""),
        "findings": findings[:5],
    }


def _extract_breakdown(grade: dict[str, Any]) -> list[dict[str, Any]]:
    rows = grade.get("breakdown") or grade.get("layer_scores") or []
    if not isinstance(rows, list):
        return []

    result = []
    for row in rows[:5]:
        if not isinstance(row, dict):
            continue
        result.append({
            "item": _txt(row.get("item") or row.get("layer_id") or row.get("name") or "", 80),
            "score": row.get("score"),
            "max": row.get("max") or row.get("max_score"),
            "reason": _txt(row.get("reason") or "", 220),
        })

    return result


def _build_payload(grade: dict[str, Any]) -> dict[str, Any]:
    logic = _extract_logic(grade)

    total = grade.get("total_score", grade.get("score", 0))
    max_score = grade.get("max_score", 25)

    official = grade.get("official_pass_score", 15)
    practical = grade.get("practical_target_score", 17.5)
    high = grade.get("high_score_target", 20)

    ceiling = grade.get("difficulty_ceiling_evaluation") or {}
    if not isinstance(ceiling, dict):
        ceiling = {}

    volume = grade.get("volume_evaluation") or {}
    if not isinstance(volume, dict):
        volume = {}

    qtype = grade.get("question_type_coverage") or grade.get("question_type_evaluation") or {}
    if not isinstance(qtype, dict):
        qtype = {}

    score_range = grade.get("score_range") or grade.get("estimated_score_range") or f"{total}~{total}"
    if ceiling.get("cap_applied"):
        score_range = f"{total}점 cap 적용"

    return {
        "score": {
            "total": total,
            "max": max_score,
            "score_range": score_range,
            "confidence": grade.get("confidence") or grade.get("confidence_level") or "medium",
            "official_pass_score": official,
            "official_pass_met": _as_float(total) >= _as_float(official, 15),
            "practical_target_score": practical,
            "practical_target_met": _as_float(total) >= _as_float(practical, 17.5),
            "high_score_target": high,
            "high_score_met": _as_float(total) >= _as_float(high, 20),
        },
        "logic_check": logic,
        "ceiling": {
            "cap_applied": bool(ceiling.get("cap_applied")),
            "reason": _txt(
                ceiling.get("reason")
                or ceiling.get("fatal_error_reason")
                or "",
                320,
            ),
        },
        "volume": {
            "level": volume.get("level"),
            "pages": volume.get("estimated_answer_sheet_pages"),
            "cap": volume.get("cap"),
            "reason": _txt(volume.get("reason") or "", 260),
        },
        "question_type": {
            "lens": qtype.get("question_type_lens") or qtype.get("lens") or qtype.get("type") or "",
            "coverage": qtype.get("coverage") or qtype.get("requirement_coverage") or "",
            "missing": _items(qtype.get("missing_categories") or qtype.get("missing") or [], 3),
        },
        "summary": _txt(
            grade.get("summary")
            or grade.get("overall_comment")
            or grade.get("overall_summary")
            or grade.get("comment")
            or "",
            500,
        ),
        "strengths": _items(grade.get("strengths"), 4),
        "weaknesses": _items(grade.get("weaknesses"), 5),
        "improvements": _items(grade.get("rewrite_advice") or grade.get("advice"), 5),
        "breakdown": _extract_breakdown(grade),
    }


def _parse_llm_json(raw: str) -> dict[str, Any] | None:
    text = str(raw or "").strip()
    if not text:
        return None

    def parse_object(candidate: str) -> dict[str, Any] | None:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    fenced = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        text,
        re.S,
    )
    if fenced:
        parsed = parse_object(fenced.group(1))
        if parsed is not None:
            return parsed

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        return parse_object(text[start : end + 1])

    return None


def _fatal_messages(payload: dict[str, Any]) -> list[str]:
    logic = payload.get("logic_check") or {}
    findings = logic.get("findings") or []

    result = []
    for item in findings:
        if not isinstance(item, dict):
            continue
        if item.get("severity") != "fatal":
            continue
        message = _txt(item.get("message") or item.get("evidence") or "", 280)
        if message:
            result.append(message)

    return result[:3]


def _fallback_section_basis(payload: dict[str, Any]) -> list[str]:
    result = []
    for row in payload.get("breakdown") or []:
        item = _txt(row.get("item") or "", 80)
        score = row.get("score")
        max_score = row.get("max")
        reason = _txt(row.get("reason") or "", 150)
        if item:
            result.append(f"{item}: {score}/{max_score} - {reason}")

    return result[:5]


# PLAN_C_VERDICT_CONSISTENCY_V1


def _plan_c_has_major_or_fatal_correctness_error(
    value,
    seen=None,
):
    if seen is None:
        seen = set()

    identity = id(value)

    if identity in seen:
        return False

    seen.add(identity)

    if isinstance(value, dict):
        issue_type = str(
            value.get("issue_type") or ""
        ).strip().lower()
        severity = str(
            value.get("severity") or ""
        ).strip().lower()

        if (
            issue_type == "correctness_error"
            and severity in {"major", "fatal"}
        ):
            return True

        if value.get("fatal") is True:
            return True

        if value.get("fatal_error_detected") is True:
            return True

        if value.get("blocks_originality") is True:
            return True

        return any(
            _plan_c_has_major_or_fatal_correctness_error(
                child,
                seen,
            )
            for child in value.values()
        )

    if isinstance(value, (list, tuple)):
        return any(
            _plan_c_has_major_or_fatal_correctness_error(
                child,
                seen,
            )
            for child in value
        )

    return False


def _plan_c_sanitize_unverified_core_error(
    value,
    payload,
):
    if _plan_c_has_major_or_fatal_correctness_error(
        payload
    ):
        return value

    replacement = (
        "핵심 이론은 정확하나 상세 해석 보완 필요"
    )

    if isinstance(value, str):
        return (
            value
            .replace(
                "THEORY_CORE 핵심 이론 오류 cap 적용",
                replacement,
            )
            .replace(
                "THEORY_CORE 핵심 이론 오류",
                replacement,
            )
            .replace(
                "핵심 이론 오류",
                replacement,
            )
        )

    if isinstance(value, list):
        return [
            _plan_c_sanitize_unverified_core_error(
                child,
                payload,
            )
            for child in value
        ]

    if isinstance(value, tuple):
        return tuple(
            _plan_c_sanitize_unverified_core_error(
                child,
                payload,
            )
            for child in value
        )

    if isinstance(value, dict):
        return {
            key: _plan_c_sanitize_unverified_core_error(
                child,
                payload,
            )
            for key, child in value.items()
        }

    return value

def _normalise_summary(llm_obj: dict[str, Any] | None, payload: dict[str, Any]) -> dict[str, Any]:
    llm_obj = llm_obj if isinstance(llm_obj, dict) else {}
    llm_obj = (
        _plan_c_sanitize_unverified_core_error(
            llm_obj,
            payload,
        )
    )

    fatal = bool((payload.get("logic_check") or {}).get("fatal"))

    if fatal:
        key_reasons = _fatal_messages(payload) or ["Logic Check에서 핵심 이론 오류가 확인되었습니다."]
        cap_applied = bool(
            (payload.get("ceiling") or {}).get(
                "cap_applied"
            )
        )

        if cap_applied:
            headline = "THEORY_CORE 핵심 이론 오류 cap 적용"
            overall = "핵심 이론 오류가 확인되어 최종 cap이 적용되었습니다."
        else:
            headline = "THEORY_CORE 핵심 이론 오류"
            overall = (
                "핵심 이론 오류가 확인되었습니다. "
                "현재 점수가 권장 ceiling보다 낮아 "
                "추가적인 수치 cap은 적용되지 않았습니다."
            )

        return {
            "headline": headline,
            "overall": overall,
            "key_reasons": key_reasons,
            "section_basis": [
                "C항목: 핵심 이론 정의 오류로 내용 점수가 제한됩니다.",
                "D/E항목: 현장 적용 설명은 일부 장점이나 fatal 오류를 보완하지 못합니다.",
            ],
            "improvements": _logic_check_corrective_points_from_locals(locals()),
        }

    section_basis = _items(
        llm_obj.get("section_basis")
        or llm_obj.get("항목별 핵심 근거")
        or llm_obj.get("basis")
        or [],
        5,
        240,
    )
    if not section_basis:
        section_basis = _fallback_section_basis(payload)

    improvements = _items(
        llm_obj.get("improvements")
        or llm_obj.get("보완 방향")
        or llm_obj.get("advice")
        or payload.get("improvements")
        or payload.get("weaknesses")
        or [],
        4,
        240,
    )

    return {
        "headline": _txt(
            llm_obj.get("headline")
            or llm_obj.get("판정")
            or llm_obj.get("judgement")
            or "채점 결과 요약",
            120,
        ),
        "overall": _txt(
            llm_obj.get("overall")
            or llm_obj.get("총평")
            or llm_obj.get("summary")
            or payload.get("summary")
            or "",
            520,
        ),
        "key_reasons": _items(
            llm_obj.get("key_reasons")
            or llm_obj.get("핵심 판정 근거")
            or llm_obj.get("reasons")
            or [],
            4,
            240,
        ),
        "section_basis": section_basis,
        "improvements": improvements,
    }


def _status(flag: bool) -> str:
    return "달성" if bool(flag) else "미달"


def _build_prompt(payload: dict[str, Any]) -> str:
    config = _load_prompt_config()
    system = config.get("system") or "너는 채점 결과 출력 편집기다."
    rules = config.get("rules") or []
    schema = config.get("output_schema") or {}
    template = config.get("user_template") or "입력 JSON:\n{{GRADE_PAYLOAD_JSON}}"

    prompt_parts = [str(system).strip()]

    if rules:
        prompt_parts.append("규칙:")
        for rule in rules:
            prompt_parts.append(f"- {rule}")

    if schema:
        prompt_parts.append("출력 JSON 스키마:")
        prompt_parts.append(json.dumps(schema, ensure_ascii=False, indent=2))

    user_part = str(template).replace(
        "{{GRADE_PAYLOAD_JSON}}",
        json.dumps(payload, ensure_ascii=False, indent=2),
    )
    prompt_parts.append(user_part)

    return "\n\n".join(x for x in prompt_parts if x)


def _render(summary: dict[str, Any], payload: dict[str, Any]) -> str:
    score = payload["score"]
    summary = (
        _plan_c_sanitize_unverified_core_error(
            summary,
            payload,
        )
    )

    # FINAL_FATAL_RENDER_PRECEDENCE
    # _render is the final trust boundary and may also be called directly by
    # deterministic tests or fallback code. A verified Logic Check fatal must
    # therefore override any LLM-authored headline at this boundary.
    logic_payload = payload.get("logic_check") or {}

    if bool(logic_payload.get("fatal")):
        summary = dict(
            summary
            if isinstance(summary, dict)
            else {}
        )

        ceiling_payload = payload.get("ceiling") or {}
        cap_applied = bool(
            ceiling_payload.get("cap_applied")
        )

        if cap_applied:
            summary["headline"] = (
                "THEORY_CORE 핵심 이론 오류 cap 적용"
            )
            summary["overall"] = (
                "핵심 이론 오류가 확인되어 "
                "최종 cap이 적용되었습니다."
            )
        else:
            summary["headline"] = (
                "THEORY_CORE 핵심 이론 오류"
            )
            summary["overall"] = (
                "핵심 이론 오류가 확인되었습니다. "
                "현재 점수가 권장 ceiling보다 낮아 "
                "추가적인 수치 cap은 적용되지 않았습니다."
            )

        fatal_reasons = _fatal_messages(payload)

        if fatal_reasons:
            summary["key_reasons"] = fatal_reasons

        summary["section_basis"] = [
            (
                "C항목: 핵심 이론 정의 오류로 "
                "내용 점수가 제한됩니다."
            ),
            (
                "D/E항목: 현장 적용 설명은 일부 장점이나 "
                "fatal 오류를 보완하지 못합니다."
            ),
        ]

        corrections = []

        for finding in logic_payload.get("findings") or []:
            if not isinstance(finding, dict):
                continue

            if finding.get("severity") != "fatal":
                continue

            correction = str(
                finding.get("correct_rule") or ""
            ).strip()

            if (
                correction
                and correction not in corrections
            ):
                corrections.append(correction)

        if corrections:
            summary["improvements"] = corrections[:3]

    lines = [
        f"채점 완료: {score['total']}/{score['max']}",
        f"예상 점수대: {score['score_range']}",
        f"신뢰도: {score['confidence']}",
        f"공식 합격선: {score['official_pass_score']}점 ({_status(score['official_pass_met'])})",
        f"실전 목표선: {score['practical_target_score']}점 ({_status(score['practical_target_met'])})",
        f"고득점 기준: {score['high_score_target']}점 ({_status(score['high_score_met'])})",
        "",
        f"판정: {summary.get('headline') or '채점 결과 요약'}",
        "",
    ]

    overall = _txt(summary.get("overall") or "", 520)
    if overall:
        lines.append(f"총평: {overall}")
        lines.append("")

    key_reasons = _items(summary.get("key_reasons"), 4, 260)
    if key_reasons:
        lines.append("[핵심 판정 근거]")
        for item in key_reasons:
            lines.append(f"- {item}")
        lines.append("")

    section_basis = _items(summary.get("section_basis"), 5, 260)
    if section_basis:
        lines.append("[항목별 핵심 근거]")
        for item in section_basis:
            lines.append(f"- {item}")
        lines.append("")

    improvements = _items(summary.get("improvements"), 4, 260)
    if improvements:
        lines.append("[보완 방향]")
        for item in improvements:
            lines.append(f"- {item}")

    return "\n".join(lines).strip()


def summarize_grade_for_telegram(
    grade: dict[str, Any],
    call_ollama_fn: Callable[[str], str] | None,
) -> str | None:
    """Build compact Telegram output.

    Return None only when compact summarization is
    explicitly disabled or no callable is available.
    LLM failures use the deterministic normalisation
    and rendering fallback.
    """
    if (
        os.getenv(
            "GRADE_OUTPUT_LLM_SUMMARY",
            "1",
        )
        .strip()
        .lower()
        in {
            "0",
            "false",
            "off",
            "no",
        }
    ):
        return None

    if (
        not isinstance(grade, dict)
        or call_ollama_fn is None
    ):
        return None

    payload = _build_payload(grade)
    prompt = _build_prompt(payload)

    try:
        raw = str(
            call_ollama_fn(prompt)
            or ""
        ).strip()
    except Exception:
        raw = ""

    llm_obj = _parse_llm_json(raw)
    summary = _normalise_summary(
        llm_obj,
        payload,
    )

    return _render(
        summary,
        payload,
    )

# STRUCTURED_VERDICT_CONSISTENCY_INTEGRATION_V1
from copy import deepcopy as _verdict_consistency_deepcopy

_verdict_consistency_previous_build_payload = (
    _build_payload
)


def _build_payload(grade):
    payload = _verdict_consistency_previous_build_payload(
        grade
    )

    if not isinstance(payload, dict):
        return payload

    if not isinstance(grade, dict):
        return payload

    parsed = grade.get("parsed")

    if not isinstance(parsed, dict):
        parsed = {}

    for key in (
        "general_evidence_contract",
        "question_demand_contract",
        "question_type_coverage",
        "layer_issue_ownership",
        "semantic_downward_guard",
    ):
        value = grade.get(key)

        if value is None:
            value = parsed.get(key)

        if value is not None:
            payload[key] = (
                _verdict_consistency_deepcopy(
                    value
                )
            )

    return payload


_verdict_consistency_previous_normalise_summary = (
    _normalise_summary
)


def _normalise_summary(llm_obj, payload):
    summary = (
        _verdict_consistency_previous_normalise_summary(
            llm_obj,
            payload,
        )
    )

    from verdict_consistency import (
        reconcile_verdict_summary,
    )

    return reconcile_verdict_summary(
        summary,
        payload,
    )
