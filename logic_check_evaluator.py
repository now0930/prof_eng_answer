from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_BANK = ROOT / "rubrics" / "logic_checks" / "industrial_instrumentation_control.json"


NEGATION_HINTS = [
    "아니다",
    "아니며",
    "않",
    "틀림",
    "틀렸",
    "오류",
    "잘못",
    "금지",
    "표현하지 않",
    "정의하지 않",
]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_text(text: str) -> str:
    value = str(text or "")

    replacements = {
        "\\zeta": "ζ",
        "\\omega": "ω",
        "\\omega_n": "ωn",
        "\\omega_d": "ωd",
        "omega_n": "ωn",
        "omega_d": "ωd",
        "omega n": "ωn",
        "omega d": "ωd",
        "zeta": "ζ",
        "Zeta": "ζ",
        "Damping Ratio": "damping ratio",
        "Under Damping": "under damping",
        "Under damped": "under damped",
        "Over Damping": "over damping",
        "Critical Damping": "critical damping",
        "σ": "σ",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _context(text: str, start: int, end: int, window: int = 40) -> str:
    return text[max(0, start - window): min(len(text), end + window)]


def _is_negated_context(ctx: str) -> bool:
    return any(hint in ctx for hint in NEGATION_HINTS)


def _find_wrong_pattern(text: str, pattern: str) -> tuple[bool, str]:
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error:
        rx = re.compile(re.escape(pattern), re.IGNORECASE)

    for m in rx.finditer(text):
        ctx = _context(text, m.start(), m.end())
        if _is_negated_context(ctx):
            continue
        return True, ctx

    return False, ""


def _count_required_patterns(text: str, patterns: list[str]) -> tuple[int, list[str]]:
    hits = []
    for pattern in patterns:
        try:
            matched = re.search(pattern, text, flags=re.IGNORECASE) is not None
        except re.error:
            matched = pattern.lower() in text.lower()

        if matched:
            hits.append(pattern)

    return len(hits), hits


def _topic_applies(text: str, grade: dict[str, Any], topic_check: dict[str, Any]) -> bool:
    topic_id = topic_check.get("topic_id")

    strategy = grade.get("difficulty_strategy") or {}
    if strategy.get("topic_id") == topic_id or strategy.get("topic") == topic_id:
        return True

    topic_aliases = topic_check.get("topic_aliases") or []
    lowered = text.lower()

    for alias in topic_aliases:
        if str(alias).lower() in lowered:
            return True

    return False


def _mode_from_findings(findings: list[dict[str, Any]]) -> str:
    severities = {f.get("severity") for f in findings}
    if "fatal" in severities:
        return "fatal"
    if "major" in severities:
        return "warn"
    if "minor" in severities:
        return "warn"
    return "pass"


def _append_unique(target: list[str], value: str) -> None:
    value = str(value or "").strip()
    if value and value not in target:
        target.append(value)


def evaluate_logic_checks(
    answer_text: str,
    grade: dict[str, Any] | None = None,
    bank_path: str | Path | None = None,
) -> dict[str, Any]:
    grade = grade or {}
    path = Path(bank_path) if bank_path else DEFAULT_BANK

    if not path.exists():
        return {
            "version": "logic_check_evaluator_v1",
            "applicable": False,
            "mode": "skip",
            "reason": f"logic check bank not found: {path}",
            "findings": [],
        }

    bank = _load_json(path)
    text = _normalize_text(answer_text)

    findings: list[dict[str, Any]] = []
    deduction_elements: list[str] = []
    next_practice_points: list[str] = []
    topic_id = None
    topic_name = None
    recommended_ceiling: float | None = None

    for topic_check in bank.get("topic_logic_checks", []):
        if not topic_check.get("enabled", True):
            continue

        if not _topic_applies(text, grade, topic_check):
            continue

        topic_id = topic_check.get("topic_id")
        topic_name = topic_check.get("topic_name")

        for check in topic_check.get("fatal_checks", []):
            for pattern in check.get("wrong_patterns", []):
                matched, ctx = _find_wrong_pattern(text, pattern)
                if not matched:
                    continue

                findings.append(
                    {
                        "id": check.get("id"),
                        "severity": check.get("severity", "fatal"),
                        "message": check.get("message"),
                        "correct_rule": check.get("correct_rule"),
                        "affected_layers": check.get("affected_layers", []),
                        "evidence": ctx,
                        "matched_pattern": pattern,
                    }
                )
                _append_unique(deduction_elements, check.get("message", "핵심 이론 오류"))
                ceiling = check.get("recommended_ceiling")
                if isinstance(ceiling, (int, float)):
                    recommended_ceiling = ceiling if recommended_ceiling is None else min(recommended_ceiling, float(ceiling))
                break

        for check in topic_check.get("major_checks", []):
            required = check.get("required_patterns", [])
            min_required = int(check.get("min_required", len(required)))
            count, hits = _count_required_patterns(text, required)

            if count < min_required:
                findings.append(
                    {
                        "id": check.get("id"),
                        "severity": check.get("severity", "major"),
                        "message": check.get("message"),
                        "correct_rule": check.get("correct_rule"),
                        "affected_layers": check.get("affected_layers", []),
                        "hit_count": count,
                        "min_required": min_required,
                        "matched_patterns": hits,
                    }
                )
                _append_unique(deduction_elements, check.get("message", "핵심 이론 설명 부족"))

        for check in topic_check.get("question_type_checks", []):
            axes = check.get("required_axes", [])
            min_required = int(check.get("min_required", 0))
            hit_axes = [axis for axis in axes if str(axis).lower() in text.lower()]

            if len(hit_axes) < min_required:
                findings.append(
                    {
                        "id": check.get("id"),
                        "severity": check.get("severity", "minor"),
                        "message": check.get("message"),
                        "affected_layers": check.get("affected_layers", []),
                        "hit_count": len(hit_axes),
                        "min_required": min_required,
                        "matched_axes": hit_axes,
                        "required_axes": axes,
                    }
                )
                _append_unique(deduction_elements, check.get("message", "비교축 부족"))

        for check in topic_check.get("advanced_tradeoff_checks", []):
            triggers = check.get("trigger_patterns", [])
            context_patterns = check.get("required_context_patterns", [])

            trigger_count, trigger_hits = _count_required_patterns(text, triggers)
            context_count, context_hits = _count_required_patterns(text, context_patterns)

            if trigger_count > 0 and context_count == 0:
                findings.append(
                    {
                        "id": check.get("id"),
                        "severity": check.get("severity", "minor"),
                        "message": check.get("message"),
                        "affected_layers": check.get("affected_layers", []),
                        "trigger_hits": trigger_hits,
                        "context_hits": context_hits,
                    }
                )
                _append_unique(deduction_elements, check.get("message", "고급 기술 trade-off 설명 부족"))

        for point in topic_check.get("next_practice_points", []):
            _append_unique(next_practice_points, point)

        break

    mode = _mode_from_findings(findings)
    fatal_error_detected = any(f.get("severity") == "fatal" for f in findings)

    result = {
        "version": "logic_check_evaluator_v1",
        "applicable": topic_id is not None,
        "topic_id": topic_id,
        "topic_name": topic_name,
        "mode": mode,
        "fatal_error_detected": fatal_error_detected,
        "findings": findings,
        "deduction_elements": deduction_elements,
        "next_practice_points": next_practice_points,
        "score_policy": {
            "theory_core_fatal_error": fatal_error_detected,
            "recommended_ceiling": recommended_ceiling,
            "reason": "Logic Check에서 THEORY_CORE 핵심 이론 오류가 감지됨" if fatal_error_detected else "",
        },
    }

    return result


def attach_logic_check_to_grade(
    grade: dict[str, Any],
    answer_text: str,
) -> dict[str, Any]:
    logic_eval = evaluate_logic_checks(answer_text=answer_text, grade=grade)

    if not logic_eval.get("applicable"):
        return grade

    grade["logic_check_evaluation"] = logic_eval

    weaknesses = grade.get("weaknesses")
    if isinstance(weaknesses, list):
        weakness_items = [str(x) for x in weaknesses if str(x).strip()]
    elif isinstance(weaknesses, str) and weaknesses.strip():
        weakness_items = [weaknesses.strip()]
    else:
        weakness_items = []

    for finding in logic_eval.get("findings", []):
        severity = finding.get("severity", "warn")
        msg = finding.get("message")
        if msg:
            _append_unique(weakness_items, f"[Logic Check/{severity}] {msg}")

    grade["weaknesses"] = weakness_items

    advice = grade.get("rewrite_advice")
    if isinstance(advice, list):
        advice_items = [str(x) for x in advice if str(x).strip()]
    elif isinstance(advice, str) and advice.strip():
        advice_items = [advice.strip()]
    else:
        advice_items = []

    for point in logic_eval.get("next_practice_points", [])[:3]:
        _append_unique(advice_items, f"[Logic Check] {point}")

    grade["rewrite_advice"] = advice_items

    return grade
