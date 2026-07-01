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


SAFE_CORRECTION_HINTS = [
    "분리",
    "구분",
    "별도",
    "안정",
    "stable",
    "수렴",
    "좌반면",
    "음수",
    "우반면",
    "RHP",
    "불안정 영역",
    "ζ < 0",
    "ζ<0",
    "시간지연",
    "위상 여유",
]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_text(text: str) -> str:
    value = str(text or "")

    replacements = [
        ("\\omega_d", "ωd"),
        ("\\omega_n", "ωn"),
        ("\\omega", "ω"),
        ("\\zeta", "ζ"),
        ("\\sigma", "σ"),
        ("\\theta", "θ"),
        ("\\sqrt", "√"),
        ("omega_d", "ωd"),
        ("omega_n", "ωn"),
        ("omega d", "ωd"),
        ("omega n", "ωn"),
        ("ω_d", "ωd"),
        ("ω_n", "ωn"),
        ("zeta", "ζ"),
        ("Zeta", "ζ"),
        ("sigma", "σ"),
        ("theta", "θ"),
        ("Damping Ratio", "damping ratio"),
        ("Under Damping", "under damping"),
        ("Under damped", "under damped"),
        ("Over Damping", "over damping"),
        ("Critical Damping", "critical damping"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    value = value.replace("{", "").replace("}", "")
    value = value.replace("\\", "")
    value = value.replace("^2", "²")
    value = value.replace("≤", "<=")
    value = value.replace("≥", ">=")

    value = re.sub(r"\s+", " ", value)
    return value.strip()

def _context(text: str, start: int, end: int, window: int = 40) -> str:
    return text[max(0, start - window): min(len(text), end + window)]


def _is_negated_context(ctx: str) -> bool:
    return any(hint in ctx for hint in NEGATION_HINTS)


def _is_safe_correction_context(ctx: str) -> bool:
    normalized = _normalize_text(ctx)
    lowered = normalized.lower()
    return any(hint.lower() in lowered for hint in SAFE_CORRECTION_HINTS)


def _has_good_underdamped_divergence_separation(text: str) -> bool:
    normalized = _normalize_text(text)

    stable_under = re.search(
        r"(부족\s*감쇠|0\s*<\s*ζ\s*<\s*1).{0,160}(안정|stable|수렴|좌반면|음수|감쇠\s*진동)",
        normalized,
        flags=re.IGNORECASE,
    )

    divergence_separated = re.search(
        r"(발산|불안정).{0,120}(분리|구분|별도)|"
        r"(분리|구분|별도).{0,120}(발산|불안정)",
        normalized,
        flags=re.IGNORECASE,
    )

    real_unstable_condition = re.search(
        r"(우반면|RHP|ζ\s*<\s*0|음의\s*감쇠|시간지연|위상\s*여유).{0,160}(발산|불안정)|"
        r"(발산|불안정).{0,160}(우반면|RHP|ζ\s*<\s*0|음의\s*감쇠|시간지연|위상\s*여유)",
        normalized,
        flags=re.IGNORECASE,
    )

    return bool(stable_under and (divergence_separated or real_unstable_condition))


def _find_wrong_pattern(text: str, pattern: str) -> tuple[bool, str]:
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error:
        rx = re.compile(re.escape(pattern), re.IGNORECASE)

    for m in rx.finditer(text):
        ctx = _context(text, m.start(), m.end())
        if _is_negated_context(ctx) or _is_safe_correction_context(ctx):
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




def _normalized_lines(text: str) -> list[str]:
    return [
        _normalize_text(line)
        for line in str(text or "").splitlines()
        if _normalize_text(line)
    ]


def _evaluate_second_order_deterministic_checks(text: str) -> list[dict[str, Any]]:
    """
    Deterministic checks for second-order damping ratio topic.
    These catch table-style mistakes that generic regex rules often miss.
    """
    n = _normalize_text(text)
    findings: list[dict[str, Any]] = []

    def add(check_id: str, message: str, correct_rule: str, layers=None) -> None:
        if any(x.get("id") == check_id for x in findings):
            return
        findings.append(
            {
                "id": check_id,
                "severity": "fatal",
                "message": message,
                "correct_rule": correct_rule,
                "affected_layers": layers or ["C"],
                "recommended_ceiling": 10.0,
            }
        )

    critical = r"(critical\s*damp(?:ed|ing)?|임계\s*감쇠)"
    under = r"(under\s*damp(?:ed|ing)?|부족\s*감쇠)"
    over = r"(over\s*damp(?:ed|ing)?|과\s*감쇠)"

    # 1) Critical damping must be zeta = 1, not 0.7.
    if (
        re.search(critical + r".{0,160}ζ\s*=\s*0\.7", n, flags=re.IGNORECASE)
        or re.search(r"ζ\s*=\s*0\.7.{0,160}" + critical, n, flags=re.IGNORECASE)
    ):
        add(
            "critical_damping_wrong_07_threshold",
            "임계감쇠를 ζ=0.7로 정의하여 표준 감쇠비 구간 정의와 충돌한다.",
            "임계감쇠는 ζ=1이다. ζ≈0.707은 부족감쇠 영역 안의 실무적 최적 타협점일 수 있으나 임계감쇠가 아니다.",
        )

    # 2) Over damping must be zeta > 1, not 0.7 <= zeta < 1.
    if (
        re.search(over + r".{0,200}0\.7\s*(?:<=|≤)\s*ζ\s*<\s*1", n, flags=re.IGNORECASE)
        or re.search(r"0\.7\s*(?:<=|≤)\s*ζ\s*<\s*1.{0,200}" + over, n, flags=re.IGNORECASE)
    ):
        add(
            "overdamped_wrong_less_than_one_region",
            "과감쇠를 0.7≤ζ<1로 정의하여 표준 정의와 충돌한다.",
            "과감쇠는 ζ>1이다. 0<ζ<1은 모두 부족감쇠 영역이다.",
        )

    # 3) Under damping is the whole 0 < zeta < 1 region, not only zeta < 0.7.
    if (
        re.search(under + r".{0,200}ζ\s*<\s*0\.7", n, flags=re.IGNORECASE)
        or re.search(r"ζ\s*<\s*0\.7.{0,200}" + under, n, flags=re.IGNORECASE)
    ):
        add(
            "underdamped_wrong_07_boundary",
            "부족감쇠 영역을 ζ<0.7로 제한하여 표준 정의와 충돌한다.",
            "부족감쇠는 0<ζ<1 전체 영역이다. ζ≈0.707은 부족감쇠 영역 안의 실무적 타협점일 뿐이다.",
        )

    # 4) Table-specific row pattern:
    #    "Under damp | Critical damp | over damp" followed by
    #    "ζ < 0.7 | ζ = 0.7 | 0.7 <= ζ < 1"
    has_table_header = re.search(
        under + r".{0,80}" + critical + r".{0,80}" + over,
        n,
        flags=re.IGNORECASE,
    )
    has_wrong_table_zeta_row = re.search(
        r"ζ\s*<\s*0\.7.{0,80}ζ\s*=\s*0\.7.{0,80}0\.7\s*(?:<=|≤)\s*ζ\s*<\s*1",
        n,
        flags=re.IGNORECASE,
    )

    if has_table_header and has_wrong_table_zeta_row:
        add(
            "damping_region_table_inverted",
            "감쇠비 비교표에서 부족감쇠·임계감쇠·과감쇠의 ζ 구간이 표준 정의와 다르게 배치되었다.",
            "표준 구간은 ζ=0 무감쇠, 0<ζ<1 부족감쇠, ζ=1 임계감쇠, ζ>1 과감쇠이다.",
        )

    # 5) Angle relation mismatch.
    # If theta is defined from the negative real axis, zeta = cos(theta), not sin(theta).
    if re.search(
        r"(음의\s*실수축|실수축).{0,220}sin\s*θ\s*=.{0,100}(σ\s*/\s*ωn|frac\s*σ\s*/\s*ωn|ζ)",
        n,
        flags=re.IGNORECASE,
    ):
        add(
            "angle_relation_sin_cos_mismatch",
            "θ를 음의 실수축과 극점 사이각으로 정의한 뒤 sinθ=σ/ωn=ζ로 표현하여 기하학적 관계가 충돌한다.",
            "θ를 음의 실수축 기준으로 정의하면 ζ=cosθ이다. sinθ 관계를 쓰려면 θ를 허수축 기준 각도로 정의해야 한다.",
            layers=["C", "E"],
        )

    # 6) Step response inversion.
    # Keep this deliberately narrow. Step-response inversion should be fatal only
    # when the wrong response is assigned to the damping region in the same
    # table row / bullet / compact clause. Do not cross concept-definition lines.
    lines = _normalized_lines(text)

    classification_only = re.compile(
        r"ζ\s*=\s*0.*0\s*<\s*ζ\s*<\s*1.*ζ\s*=\s*1.*ζ\s*>\s*1|"
        r"무\s*감쇠.*부족\s*감쇠.*임계\s*감쇠.*과\s*감쇠",
        flags=re.IGNORECASE,
    )

    critical_wrong = re.compile(
        r"(critical\s*damp(?:ed|ing)?|임계\s*감쇠)\s*(?:[:|\\-]|은|는)?\s*.{0,30}"
        r"(진동\s*있|진동\s*발생|오버\s*슈트|overshoot|overshot|충돌\s*위험)",
        flags=re.IGNORECASE,
    )

    over_wrong = re.compile(
        r"(over\s*damp(?:ed|ing)?|과\s*감쇠)\s*(?:[:|\\-]|은|는)?\s*.{0,30}"
        r"(오버\s*슈트|overshoot|overshot|충돌\s*위험|빠른\s*제어)",
        flags=re.IGNORECASE,
    )

    for line in lines:
        # Standard classification lines often contain all damping names; do not
        # treat nearby underdamped overshoot/oscillation as critical/overdamped errors.
        if classification_only.search(line):
            continue

        if critical_wrong.search(line):
            add(
                "critical_damping_step_response_inversion",
                "임계감쇠 응답을 진동 또는 오버슈트 응답처럼 서술하여 표준 응답 특성과 충돌한다.",
                "임계감쇠는 오버슈트와 진동 없이 가장 빠르게 수렴하는 응답이다.",
            )

        if over_wrong.search(line):
            add(
                "overdamped_step_response_inversion",
                "과감쇠 응답을 오버슈트, 충돌 위험 또는 빠른 응답처럼 서술하여 표준 응답 특성과 충돌한다.",
                "과감쇠는 오버슈트가 없고 느리게 수렴하는 응답이다.",
            )

    return findings



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

                if (
                    check.get("id") == "underdamped_as_divergence"
                    and _has_good_underdamped_divergence_separation(text)
                ):
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

        if topic_check.get("topic_id") == "second_order_lag_response_by_damping_ratio":
            for deterministic_finding in _evaluate_second_order_deterministic_checks(text):
                if any(f.get("id") == deterministic_finding.get("id") for f in findings):
                    continue

                findings.append(deterministic_finding)
                _append_unique(
                    deduction_elements,
                    deterministic_finding.get("message", "핵심 이론 오류")
                )

                ceiling = deterministic_finding.get("recommended_ceiling")
                if isinstance(ceiling, (int, float)):
                    recommended_ceiling = (
                        float(ceiling)
                        if recommended_ceiling is None
                        else min(recommended_ceiling, float(ceiling))
                    )

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
