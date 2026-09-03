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



def _stage7_legacy_attach_native_feedback_observability(payload):
    # NATIVE_FEEDBACK_OBSERVABILITY_V1
    if not isinstance(payload, dict):
        return payload

    out = dict(payload)

    def _append_unique(target, value):
        if isinstance(value, str):
            text = value.strip()
            if text and text not in target:
                target.append(text)
            return
        if isinstance(value, (list, tuple)):
            for item in value:
                _append_unique(target, item)

    feedback_elements = []
    breakdown = out.get("breakdown")
    if isinstance(breakdown, list):
        for row in breakdown:
            if not isinstance(row, dict):
                continue
            _append_unique(feedback_elements, row.get("reason"))
            _append_unique(feedback_elements, row.get("gemini_reason"))
            _append_unique(
                feedback_elements,
                row.get("layer_evidence_guard_blocked_reasons"),
            )

    feedback_characteristics = []
    _append_unique(feedback_characteristics, out.get("comment"))

    connection = out.get("connection_evaluation")
    if isinstance(connection, dict):
        checks = connection.get("checks")
        if isinstance(checks, list):
            for check in checks:
                if isinstance(check, dict):
                    _append_unique(
                        feedback_characteristics,
                        check.get("reason"),
                    )

    caps = out.get("applied_caps")
    if isinstance(caps, list):
        for cap in caps:
            if isinstance(cap, dict):
                _append_unique(
                    feedback_characteristics,
                    cap.get("reason"),
                )

    out["feedback_elements"] = feedback_elements
    out["feedback_characteristics"] = feedback_characteristics
    return out


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

    return _attach_native_feedback_observability({'score': {'total': total, 'max': max_score, 'score_range': score_range, 'confidence': grade.get('confidence') or grade.get('confidence_level') or 'medium', 'official_pass_score': official, 'official_pass_met': _as_float(total) >= _as_float(official, 15), 'practical_target_score': practical, 'practical_target_met': _as_float(total) >= _as_float(practical, 17.5), 'high_score_target': high, 'high_score_met': _as_float(total) >= _as_float(high, 20)}, 'logic_check': logic, 'ceiling': {'cap_applied': bool(ceiling.get('cap_applied')), 'reason': _txt(ceiling.get('reason') or ceiling.get('fatal_error_reason') or '', 320)}, 'volume': {'level': volume.get('level'), 'pages': volume.get('estimated_answer_sheet_pages'), 'cap': volume.get('cap'), 'reason': _txt(volume.get('reason') or '', 260)}, 'question_type': {'lens': qtype.get('question_type_lens') or qtype.get('lens') or qtype.get('type') or '', 'coverage': qtype.get('coverage') or qtype.get('requirement_coverage') or '', 'missing': _items(qtype.get('missing_categories') or qtype.get('missing') or [], 3)}, 'summary': _txt(grade.get('summary') or grade.get('overall_comment') or grade.get('overall_summary') or grade.get('comment') or '', 500), 'strengths': _items(grade.get('strengths'), 4), 'weaknesses': _items(grade.get('weaknesses'), 5), 'improvements': _items(grade.get('rewrite_advice') or grade.get('advice'), 5), 'breakdown': _extract_breakdown(grade)})


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
            headline = "검증된 핵심 기술 오류 — 점수 상한 적용"
            overall = "검증된 핵심 기술 오류가 확인되어 최종 점수 상한이 적용되었습니다."
        else:
            headline = "검증된 핵심 기술 오류 보완 필요"
            overall = (
                "검증된 핵심 기술 오류가 확인되었습니다. "
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
                "검증된 핵심 기술 오류 — 점수 상한 적용"
            )
            summary["overall"] = (
                "검증된 핵심 기술 오류가 확인되어 "
                "최종 점수 상한이 적용되었습니다."
            )
        else:
            summary["headline"] = (
                "검증된 핵심 기술 오류 보완 필요"
            )
            summary["overall"] = (
                "검증된 핵심 기술 오류가 확인되었습니다. "
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


def _stage7_legacy_build_payload_v2(grade):
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
# NATIVE_SEMANTIC_OBSERVABILITY_PROJECTION_V2
def _stage7_find_native_projection(payload, key):
    if isinstance(payload, dict):
        if key in payload and isinstance(payload[key], dict):
            return payload[key]
        for value in payload.values():
            found = _stage7_find_native_projection(value, key)
            if found is not None:
                return found
    elif isinstance(payload, (list, tuple)):
        for value in payload:
            found = _stage7_find_native_projection(value, key)
            if found is not None:
                return found
    return None


def _stage7_append_unique_text(target, value):
    if not isinstance(value, str):
        return
    text = value.strip()
    if text and text not in target:
        target.append(text)


def _attach_native_feedback_observability(payload):
    out = _stage7_legacy_attach_native_feedback_observability(payload)
    if not isinstance(out, dict):
        return out

    out = dict(out)

    qd = _stage7_find_native_projection(
        out, "native_question_demand_projection_v1"
    )
    fact = _stage7_find_native_projection(
        out, "native_fact_projection_v1"
    )

    elements = []
    characteristics = []

    if isinstance(qd, dict):
        coverage = qd.get("coverage")
        if isinstance(coverage, (int, float)) and not isinstance(coverage, bool):
            out["coverage"] = float(coverage)

        states = qd.get("states")
        if isinstance(states, list):
            fulfilled = 0
            explained = 0
            weak = 0
            for row in states:
                if not isinstance(row, dict):
                    continue
                text = row.get("text")
                state = row.get("state")
                if isinstance(text, str) and text.strip():
                    _stage7_append_unique_text(elements, text)
                if state == 3:
                    fulfilled += 1
                elif state == 2:
                    explained += 1
                elif state in (0, 1):
                    weak += 1

            total = fulfilled + explained + weak
            if total:
                if weak == 0 and fulfilled == total:
                    _stage7_append_unique_text(
                        characteristics,
                        "문제의 요구사항을 모두 설명하고 조건까지 충족한 답안이다.",
                    )
                elif weak == 0:
                    _stage7_append_unique_text(
                        characteristics,
                        "문제의 주요 요구사항은 설명했으며 일부 요구는 조건 충족의 구체화가 필요하다.",
                    )
                else:
                    _stage7_append_unique_text(
                        characteristics,
                        "설명이 부족하거나 언급 수준에 머문 문제 요구사항을 구체적으로 보완할 필요가 있다.",
                    )

    if isinstance(fact, dict):
        states = fact.get("states")
        if isinstance(states, list):
            connected = 0
            correct = 0
            weak = 0
            for row in states:
                if not isinstance(row, dict):
                    continue
                text = row.get("text")
                state = row.get("state")
                if isinstance(text, str) and text.strip():
                    _stage7_append_unique_text(elements, text)
                if state == 3:
                    connected += 1
                elif state == 2:
                    correct += 1
                elif state in (0, 1):
                    weak += 1

            total = connected + correct + weak
            if total:
                if weak == 0 and connected == total:
                    _stage7_append_unique_text(
                        characteristics,
                        "핵심 사실을 정확히 설명하고 문제 요구와의 기술적 관계까지 연결한 답안이다.",
                    )
                elif weak == 0:
                    _stage7_append_unique_text(
                        characteristics,
                        "핵심 사실은 대체로 정확하며 문제 요구와의 연결을 더 명확히 하면 완성도가 높아진다.",
                    )
                else:
                    _stage7_append_unique_text(
                        characteristics,
                        "누락되거나 언급 수준인 핵심 사실을 정확한 기술적 관계로 보완할 필요가 있다.",
                    )

    for value in out.get("feedback_elements") or []:
        _stage7_append_unique_text(elements, value)
    for value in out.get("feedback_characteristics") or []:
        _stage7_append_unique_text(characteristics, value)

    out["feedback_elements"] = elements
    out["feedback_characteristics"] = characteristics
    return out
# STAGE7_BUILD_PAYLOAD_NATIVE_OBSERVABILITY_V2
def _stage7_sum_walk_dicts(value, _seen=None):
    if _seen is None:
        _seen = set()
    oid = id(value)
    if oid in _seen:
        return
    _seen.add(oid)
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _stage7_sum_walk_dicts(child, _seen)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _stage7_sum_walk_dicts(child, _seen)


def _stage7_sum_bool(row, keys):
    for key in keys:
        value = row.get(key)
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value == 0:
                return False
            if value == 1:
                return True
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {
                "yes", "true", "pass", "passed", "covered", "verified",
                "correct", "fulfilled", "satisfied",
            }:
                return True
            if normalized in {
                "no", "false", "fail", "failed", "missing", "absent",
                "uncovered", "unverified", "incorrect",
            }:
                return False
    return None


def _stage7_sum_num(row, keys):
    for key in keys:
        value = row.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                pass
    return None


def _stage7_sum_qd_rows(value):
    rows = []
    seen = set()
    for row in _stage7_sum_walk_dicts(value):
        demand_id = row.get("demand_id")
        text = row.get("text") or row.get("demand_text") or row.get("requirement")
        if not isinstance(demand_id, str) or not isinstance(text, str):
            continue
        if not any(
            key in row
            for key in (
                "covered", "verified", "level", "linked_anchor_count",
                "observed_anchor_count", "observed_anchors",
            )
        ):
            continue

        sig = (demand_id.strip(), text.strip())
        if sig in seen:
            continue
        seen.add(sig)

        verified = _stage7_sum_bool(row, ("verified", "explained"))
        covered = _stage7_sum_bool(row, ("covered", "present", "matched"))
        linked = _stage7_sum_num(row, ("linked_anchor_count",))
        observed = _stage7_sum_num(row, ("observed_anchor_count",))
        level = _stage7_sum_num(row, ("level", "demand_level", "level_score"))

        if verified is True:
            if (
                linked is not None
                and linked > 0
                and observed is not None
                and observed >= linked
            ):
                state = 3
            elif level is not None and level >= 1.0:
                state = 3
            else:
                state = 2
        elif covered is True:
            state = 1
        elif covered is False:
            state = 0
        elif level is not None:
            state = 0 if level <= 0 else (3 if level >= 1 else 2)
        else:
            continue

        rows.append(
            {"demand_id": demand_id.strip(), "text": text.strip(), "state": state}
        )
    return rows


def _stage7_sum_qd_projection(value):
    rows = _stage7_sum_qd_rows(value)
    if not rows:
        return None
    substantive = sum(1 for row in rows if row["state"] >= 2)
    mean_state = sum(row["state"] for row in rows) / len(rows)
    return {
        "score": 6.0 * (mean_state / 3.0),
        "coverage": 100.0 * substantive / len(rows),
        "mean_state": mean_state,
        "states": rows,
        "applicable_demand_count": len(rows),
        "substantive_demand_count": substantive,
    }


def _stage7_sum_append_unique(target, value):
    if isinstance(value, str):
        text = value.strip()
        if text and text not in target:
            target.append(text)


def _build_payload(grade):
    payload = _stage7_legacy_build_payload_v2(grade)
    if not isinstance(payload, dict):
        return payload

    out = dict(payload)
    projection = _stage7_find_native_projection(
        grade,
        "native_question_demand_projection_v1",
    )
    if projection is None:
        projection = _stage7_sum_qd_projection(grade)

    if isinstance(projection, dict):
        coverage = projection.get("coverage")
        if isinstance(coverage, (int, float)) and not isinstance(coverage, bool):
            out["coverage"] = max(0.0, min(100.0, float(coverage)))

        elements = []
        for row in projection.get("states") or []:
            if isinstance(row, dict):
                _stage7_sum_append_unique(elements, row.get("text"))
        for value in out.get("feedback_elements") or []:
            _stage7_sum_append_unique(elements, value)

        characteristics = []
        states = [
            row.get("state")
            for row in (projection.get("states") or [])
            if isinstance(row, dict) and isinstance(row.get("state"), int)
        ]
        if states:
            weak = sum(1 for state in states if state < 2)
            fulfilled = sum(1 for state in states if state == 3)
            if weak == 0 and fulfilled == len(states):
                _stage7_sum_append_unique(
                    characteristics,
                    "문제의 요구사항을 모두 설명하고 요구 조건까지 충족한 답안이다.",
                )
            elif weak == 0:
                _stage7_sum_append_unique(
                    characteristics,
                    "문제의 주요 요구사항을 설명했으며 일부 요구 조건의 구체화를 보완할 수 있다.",
                )
            else:
                _stage7_sum_append_unique(
                    characteristics,
                    "언급 수준이거나 설명이 부족한 문제 요구사항을 구체적인 기술 관계로 보완할 필요가 있다.",
                )
        for value in out.get("feedback_characteristics") or []:
            _stage7_sum_append_unique(characteristics, value)

        out["feedback_elements"] = elements
        out["feedback_characteristics"] = characteristics
        out["native_question_demand_projection_v1"] = projection

    return out

# STAGE17E5_FINAL_DECISION_DISPLAY_BOUNDARY_V1
_STAGE17E5_PREVIOUS_BUILD_PAYLOAD = _build_payload


def _build_payload(grade: dict[str, Any]) -> dict[str, Any]:
    payload = _STAGE17E5_PREVIOUS_BUILD_PAYLOAD(
        grade
    )

    if not isinstance(payload, dict):
        return payload

    score = payload.get("score")
    if not isinstance(score, dict):
        return payload

    pass_allowed = (
        grade.get("passing_score_allowed")
        is not False
    )
    strong_allowed = (
        grade.get("strong_verdict_allowed")
        is not False
    )

    if not pass_allowed:
        score["official_pass_met"] = False
        score["practical_target_met"] = False
        score["high_score_met"] = False
    elif not strong_allowed:
        score["high_score_met"] = False

    consistency = grade.get(
        "final_decision_consistency"
    )
    if isinstance(consistency, dict):
        payload["final_decision_consistency"] = {
            "hard_error": bool(
                consistency.get("hard_error")
                or consistency.get(
                    "major_or_fatal_error"
                )
            ),
            "fatal_error": bool(
                consistency.get("fatal_error")
            ),
            "passing_score_allowed": (
                pass_allowed
            ),
            "strong_verdict_allowed": (
                strong_allowed
            ),
        }

    return payload

# STAGE18B3_STRUCTURED_DEFECT_OUTPUT_PRIORITY_V1
from copy import deepcopy as _stage18b3_deepcopy

_STAGE18B3_PREVIOUS_BUILD_PAYLOAD = _build_payload
_STAGE18B3_PREVIOUS_RENDER = _render


def _stage18b4_grade_contract(grade, key):
    if not isinstance(grade, dict):
        return {}
    direct = grade.get(key)
    if isinstance(direct, dict):
        return direct
    parsed = grade.get("parsed")
    if isinstance(parsed, dict) and isinstance(parsed.get(key), dict):
        return parsed[key]
    return {}


def _stage18b4_actual_numeric_cap(grade):
    """Project only *applied* one-way caps into public formatter state."""
    sources = []
    caps = []

    def add(source, cap=None, reason=""):
        if source not in sources:
            sources.append(source)
        try:
            numeric_cap = float(cap)
        except (TypeError, ValueError, OverflowError):
            numeric_cap = None
        if numeric_cap is not None:
            caps.append(numeric_cap)
        return str(reason or "").strip()

    reasons = []
    verified = _stage18b4_grade_contract(
        grade, "verified_correctness_score_cap"
    )
    if verified.get("score_effect") == "hard_cap":
        reasons.append(add(
            "verified_correctness_score_cap",
            verified.get("cap"),
            "검증된 correctness 오류에 따른 총점 상한",
        ))

    difficulty = _stage18b4_grade_contract(
        grade, "difficulty_ceiling_evaluation"
    )
    if difficulty.get("cap_applied") is True:
        reasons.append(add(
            "difficulty_ceiling",
            difficulty.get("capped_score") or difficulty.get("recommended_cap"),
            difficulty.get("reason") or difficulty.get("fatal_error_reason"),
        ))

    explicit = _stage18b4_grade_contract(
        grade, "explicit_requirement_cap_evaluation"
    )
    if explicit.get("applied") is True:
        reasons.append(add(
            "explicit_requirement_missing_cap",
            explicit.get("total_cap"),
            explicit.get("reason"),
        ))

    high_score = _stage18b4_grade_contract(
        grade, "high_score_eligibility"
    )
    if high_score.get("cap_applied") is True:
        reasons.append(add(
            "high_score_evidence_eligibility",
            high_score.get("cap"),
            "고득점 evidence 적격성 미충족에 따른 상한",
        ))

    applied_caps = grade.get("applied_caps") if isinstance(grade, dict) else []
    for row in applied_caps if isinstance(applied_caps, list) else []:
        if not isinstance(row, dict) or row.get("score_effect") != "hard_cap":
            continue
        reasons.append(add(
            str(row.get("type") or "applied_numeric_cap"),
            row.get("cap") or row.get("total_cap"),
            row.get("reason") or ", ".join(
                str(item) for item in row.get("reason_codes", [])
            ),
        ))

    reasons = [reason for reason in reasons if reason]
    return {
        "cap_applied": bool(sources),
        "cap": min(caps) if caps else None,
        "sources": sources,
        "reason": reasons[0] if reasons else "",
    }


def _stage18b4_attach_actual_numeric_cap(payload, grade):
    if not isinstance(payload, dict):
        return payload
    cap = _stage18b4_actual_numeric_cap(grade)
    if not cap["cap_applied"]:
        return payload
    out = dict(payload)
    score = out.get("score")
    if isinstance(score, dict):
        score = dict(score)
        score["score_range"] = f"{score.get('total')}점 cap 적용"
        out["score"] = score
    ceiling = out.get("ceiling")
    ceiling = dict(ceiling) if isinstance(ceiling, dict) else {}
    ceiling.update(cap)
    out["ceiling"] = ceiling
    out["applied_numeric_cap"] = cap
    return out


def _stage18b3_find_reconciliation(
    grade: Any,
) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return {}

    direct = grade.get(
        "verified_defect_reconciliation"
    )

    if isinstance(direct, dict):
        return direct

    parsed = grade.get("parsed")

    if isinstance(parsed, dict):
        nested = parsed.get(
            "verified_defect_reconciliation"
        )

        if isinstance(nested, dict):
            return nested

    coverage = grade.get(
        "question_type_coverage"
    )

    if not isinstance(coverage, dict):
        coverage = {}

    explicit = coverage.get(
        "explicit_requirement_coverage"
    )

    if not isinstance(explicit, dict):
        explicit = {}

    nested = explicit.get(
        "verified_defect_reconciliation"
    )

    return (
        nested
        if isinstance(nested, dict)
        else {}
    )


def _build_payload(
    grade: dict[str, Any],
) -> dict[str, Any]:
    from verdict_consistency import (
        enforce_final_decision_consistency,
    )

    grade = enforce_final_decision_consistency(
        grade
    )
    payload = _STAGE18B3_PREVIOUS_BUILD_PAYLOAD(
        grade
    )

    if not isinstance(payload, dict):
        return payload

    payload = _stage18b4_attach_actual_numeric_cap(
        payload,
        grade,
    )

    reconciliation = (
        _stage18b3_find_reconciliation(
            grade
        )
    )

    if not reconciliation:
        return payload

    out = dict(payload)
    out[
        "verified_defect_reconciliation"
    ] = _stage18b3_deepcopy(
        reconciliation
    )
    out[
        "structured_defect_output_priority"
    ] = {
        "marker": (
            "STAGE18B3_STRUCTURED_DEFECT_OUTPUT_PRIORITY_V1"
        ),
        "source": (
            "existing_verified_defect_reconciliation"
        ),
        "output_priority": (
            "verified_defect_before_generic_feedback"
        ),
        "generic_feedback_can_override": False,
        "new_defect_owner_created": False,
        "score_effect": "none",
        "numeric_score_changed": False,
    }
    return out


def _render(
    summary: dict[str, Any],
    payload: dict[str, Any],
) -> str:
    from verdict_consistency import (
        reconcile_verdict_summary,
    )

    prioritized = reconcile_verdict_summary(
        summary,
        payload,
    )
    return _STAGE18B3_PREVIOUS_RENDER(
        prioritized,
        payload,
    )
