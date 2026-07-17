from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from rubric_bank_paths import resolve_rubric_bank_path


ROOT = Path(__file__).resolve().parent
DEFAULT_BANK = resolve_rubric_bank_path("logic_checks")


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


def _semantic_evidence_is_corrective_context(
    text: str,
    evidence: str,
) -> bool:
    """Return True only for explicitly corrective evidence contexts."""

    normalized_text = _normalize_text(text)
    normalized_evidence = _normalize_text(evidence)

    if not normalized_text or not normalized_evidence:
        return False

    evidence_pattern = re.compile(
        re.escape(normalized_evidence),
        flags=re.IGNORECASE,
    )

    correction_prefix = re.compile(
        r"(?:"
        r"주의(?:할)?\s*오류"
        r"|오류\s*(?:항목|사례|표현)?"
        r"|잘못된?\s*(?:주장|설명|표현|오개념)"
        r"|틀린\s*(?:주장|설명|표현)"
        r"|금지\s*(?:표현|사항)"
        r"|오개념"
        r"|반대로\s*(?:쓰|설명|표현)"
        r")\s*[:：\-]?\s*$",
        flags=re.IGNORECASE,
    )

    explicit_negation = re.compile(
        r"(?:"
        r"아니(?:다|며|고|므로|라는)"
        r"|않(?:다|으며|고|아야|도록)"
        r"|안\s*된(?:다|다고|다는|다며)"
        r"|해서는\s*안\s*된"
        r"|하면\s*안\s*된"
        r"|단정(?:하면|해서는)\s*안"
        r"|잘못(?:이다|이며|된|되었)"
        r"|틀리(?:다|며|고|므로)"
        r"|오류(?:이다|이며|로)"
        r"|금지(?:한다|해야|된다)"
        r")",
        flags=re.IGNORECASE,
    )

    for match in evidence_pattern.finditer(
        normalized_text
    ):
        start = match.start()
        end = match.end()

        prefix = normalized_text[
            max(0, start - 50):start
        ]

        suffix = normalized_text[
            end:min(
                len(normalized_text),
                end + 70,
            )
        ]

        if correction_prefix.search(prefix):
            return True

        if explicit_negation.search(
            normalized_evidence
        ):
            return True

        if explicit_negation.search(suffix):
            return True

    return False


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
            layers=["C"],
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




def _apply_second_order_claim_evaluator(text: str, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Second-order damping topic uses JSON-profile LLM verification:
    - JSON profile defines truth_schema, fatal_conditions, safe_conditions, and candidate rules.
    - Python extracts only candidate evidence from the profile.
    - LLM verifies whether the candidate contains a direct contradiction.
    - Legacy hard-coded fatal findings are removed to prevent false caps.
    - Non-fatal major/minor findings remain as supplemental feedback.
    """
    legacy_second_order_fatal_ids = {
        "critical_damping_wrong_07_threshold",
        "overdamped_wrong_less_than_one_region",
        "underdamped_wrong_07_boundary",
        "damping_region_table_inverted",
        "angle_relation_sin_cos_mismatch",
        "step_response_region_inversion",
        "critical_damping_step_response_inversion",
        "overdamped_step_response_inversion",
    }

    filtered: list[dict[str, Any]] = []

    for finding in findings:
        if not isinstance(finding, dict):
            continue

        fid = str(finding.get("id") or "")
        severity = finding.get("severity")

        if severity == "fatal" and (
            fid in legacy_second_order_fatal_ids
            or fid.startswith("claim_")
        ):
            continue

        filtered.append(finding)

    try:
        from logic_llm_verifier import verify_logic_with_llm

        llm_eval = verify_logic_with_llm(
            text,
            "second_order_lag_response_by_damping_ratio",
        )
    except Exception as exc:
        filtered.append(
            {
                "id": "llm_second_order_verifier_error",
                "severity": "minor",
                "message": f"2차 시스템 LLM verifier 실행 오류: {exc}",
                "correct_rule": "LLM verifier 실패 시 fatal cap을 적용하지 않습니다.",
                "affected_layers": ["C"],
            }
        )
        return filtered

    for finding in llm_eval.get("findings") or []:
        if isinstance(finding, dict):
            filtered.append(finding)

    return filtered



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
    profile: dict[str, Any] = {}


    # LOGIC_CHECK_PREFERRED_TOPIC_PATCH
    # Prefer a precise topic selected by upstream model-answer routing.
    # Without this, broad keyword overlap can make phase3b apply a neighboring
    # topic's deterministic checks, e.g. damping-ratio checks on a resonance
    # frequency-response answer.
    _topic_logic_checks_for_evaluation = bank.get("topic_logic_checks", [])
    _topic_routing_error = ""

    try:
        _preferred_logic_topic_id = None

        for _key in ("logic_check_topic_id", "topic_id", "inferred_topic_id", "primary_topic_id"):
            _value = grade.get(_key) if isinstance(grade, dict) else None
            if isinstance(_value, str) and _value.strip():
                _preferred_logic_topic_id = _value.strip()
                break

        if not _preferred_logic_topic_id and isinstance(grade, dict):
            _ref = grade.get("model_answer_reference") or {}
            if isinstance(_ref, dict):
                _primary = _ref.get("primary_reference") or {}
                if isinstance(_primary, dict):
                    _value = _primary.get("topic_id")
                    if isinstance(_value, str) and _value.strip():
                        _preferred_logic_topic_id = _value.strip()

                if not _preferred_logic_topic_id:
                    _candidates = _ref.get("candidates") or []
                    if isinstance(_candidates, list) and _candidates:
                        _candidate = _candidates[0]

                        if isinstance(_candidate, dict):
                            _answer = _candidate.get("answer") or {}

                            if isinstance(_answer, dict):
                                _value = _answer.get("topic_id")

                                if isinstance(_value, str) and _value.strip():
                                    _preferred_logic_topic_id = _value.strip()

        if _preferred_logic_topic_id and isinstance(_topic_logic_checks_for_evaluation, list):
            _matched_topic_checks = [
                _topic_check
                for _topic_check in _topic_logic_checks_for_evaluation
                if isinstance(_topic_check, dict)
                and _topic_check.get("topic_id") == _preferred_logic_topic_id
            ]

            if _matched_topic_checks:
                _topic_logic_checks_for_evaluation = _matched_topic_checks
    except Exception as routing_error:
        _topic_logic_checks_for_evaluation = []
        _topic_routing_error = repr(routing_error)

    for topic_check in _topic_logic_checks_for_evaluation:
        deterministic_enabled = bool(
            topic_check.get("enabled", True)
        )

        if not _topic_applies(
            text,
            grade,
            topic_check,
        ):
            continue

        topic_id = topic_check.get("topic_id")
        topic_name = topic_check.get("topic_name")

        # A generated Topic Pack may intentionally disable deterministic
        # checks while keeping an active JSON-profile LLM verifier.
        #
        # In that case, enabled=false means "profile-only", not
        # "disable the entire topic". Do not execute wrong_patterns,
        # deterministic major checks, or question-type pattern checks.
        if not deterministic_enabled:
            try:
                from logic_llm_verifier import (
                    load_logic_check_profile,
                    verify_logic_with_llm,
                )

                profile = load_logic_check_profile(
                    str(topic_id)
                )

                profile_evaluation = (
                    verify_logic_with_llm(
                        text,
                        str(topic_id),
                    )
                )
            except Exception as error:
                findings.append(
                    {
                        "id": (
                            "llm_profile_verifier_"
                            "unavailable"
                        ),
                        "severity": "minor",
                        "message": (
                            "JSON-profile LLM Logic "
                            "Check를 실행하지 못해 "
                            "fatal 판정을 건너뛰었습니다: "
                            f"{error}"
                        ),
                        "correct_rule": (
                            "LLM verifier 실패 시 "
                            "fatal cap을 적용하지 않습니다."
                        ),
                        "affected_layers": ["C"],
                        "engine": (
                            "llm_verifier_profile_v1"
                        ),
                        "diagnostic": {
                            "ok": False,
                            "error": repr(error),
                        },
                    }
                )

                profile = {}
                profile_evaluation = {}
            else:
                if not isinstance(
                    profile_evaluation,
                    dict,
                ):
                    profile_evaluation = {}

                topic_name = (
                    profile.get("display_name")
                    or topic_name
                )

                for profile_finding in (
                    profile_evaluation.get(
                        "findings"
                    )
                    or []
                ):
                    if not isinstance(
                        profile_finding,
                        dict,
                    ):
                        continue

                    profile_finding = dict(
                        profile_finding
                    )

                    profile_finding.setdefault(
                        "engine",
                        "llm_verifier_profile_v1",
                    )

                    if any(
                        isinstance(existing, dict)
                        and (
                            existing.get("id")
                            == profile_finding.get("id")
                            or (
                                existing.get(
                                    "source_rule_id"
                                )
                                and existing.get(
                                    "source_rule_id"
                                )
                                == profile_finding.get(
                                    "source_rule_id"
                                )
                            )
                        )
                        for existing in findings
                    ):
                        continue

                    findings.append(
                        profile_finding
                    )

            practice_source = (
                profile.get(
                    "next_practice_points"
                )
                if isinstance(profile, dict)
                else None
            )

            if not practice_source:
                practice_source = (
                    topic_check.get(
                        "next_practice_points"
                    )
                    or []
                )

            for point in practice_source:
                _append_unique(
                    next_practice_points,
                    point,
                )

            break

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

        # Semantic fatal fallback:
        # wrong_patterns are only a fast deterministic aid. If they do not catch
        # a fatal misconception, ask the LLM verifier to interpret the answer
        # against this topic's fatal rules in context.
        if not any(f.get("severity") == "fatal" for f in findings):
            for semantic_finding in _evaluate_topic_fatal_checks_with_llm(text, topic_check):
                if any(
                    f.get("id") == semantic_finding.get("id")
                    or f.get("source_rule_id") == semantic_finding.get("source_rule_id")
                    for f in findings
                    if isinstance(f, dict)
                ):
                    continue

                findings.append(semantic_finding)
                _append_unique(
                    deduction_elements,
                    semantic_finding.get("message", "핵심 이론 오류")
                )

                ceiling = semantic_finding.get("recommended_ceiling")
                if semantic_finding.get("severity") == "fatal" and isinstance(ceiling, (int, float)):
                    recommended_ceiling = (
                        float(ceiling)
                        if recommended_ceiling is None
                        else min(recommended_ceiling, float(ceiling))
                    )

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

        for point in topic_check.get("next_practice_points", []):
            _append_unique(next_practice_points, point)

        break

    # The second-order damping claim evaluator is topic-specific.
    # Do not apply it to neighboring topics such as frequency-response/resonance,
    # otherwise damping-ratio profile findings leak into resonance evaluations.
    if topic_id == "second_order_lag_response_by_damping_ratio":
        findings = _apply_second_order_claim_evaluator(text, findings)
    # Logic Check는 D/E를 직접 평가하지 않는다.
    # D/E는 de_claim_trust metadata의 target일 뿐 finding affected layer가 아니다.
    for _finding in findings:
        if isinstance(_finding, dict):
            _layers = _finding.get("affected_layers")
            if isinstance(_layers, list):
                _clean_layers = [layer for layer in _layers if layer in ("A", "B", "C")]
                _finding["affected_layers"] = _clean_layers or ["C"]

    # Rebuild deduction/cap state after claim-based fatal arbitration.
    deduction_elements = []
    recommended_ceiling = None
    for finding in findings:
        if not isinstance(finding, dict):
            continue

        msg = str(finding.get("message") or "").strip()
        if msg:
            _append_unique(deduction_elements, msg)

        ceiling = finding.get("recommended_ceiling")
        if finding.get("severity") == "fatal" and isinstance(ceiling, (int, float)):
            recommended_ceiling = (
                float(ceiling)
                if recommended_ceiling is None
                else min(recommended_ceiling, float(ceiling))
            )

    mode = _mode_from_findings(findings)
    fatal_error_detected = any(
        isinstance(finding, dict)
        and finding.get("severity") == "fatal"
        for finding in findings
    )

    profile_score_policy = (
        profile.get("score_policy")
        if isinstance(profile, dict)
        else {}
    )

    if not isinstance(profile_score_policy, dict):
        profile_score_policy = {}

    explicit_score_effect = str(
        profile_score_policy.get("score_effect")
        or ""
    ).strip()

    diagnostic_only_policy = (
        explicit_score_effect
        == "diagnostic_only"
    )

    configured_caps = {}
    raw_caps = profile_score_policy.get(
        "fatal_layer_caps"
    )

    if isinstance(raw_caps, dict):
        for layer_id in ("B", "C"):
            value = raw_caps.get(layer_id)

            if (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and float(value) >= 0.0
            ):
                configured_caps[layer_id] = float(value)

    configured_ceiling = profile_score_policy.get(
        "recommended_ceiling"
    )

    if (
        fatal_error_detected
        and isinstance(
            configured_ceiling,
            (int, float),
        )
        and not isinstance(
            configured_ceiling,
            bool,
        )
    ):
        configured_ceiling = float(
            configured_ceiling
        )

        recommended_ceiling = (
            configured_ceiling
            if recommended_ceiling is None
            else min(
                recommended_ceiling,
                configured_ceiling,
            )
        )

    elif (
        fatal_error_detected
        and recommended_ceiling is None
        and not configured_caps
        and not diagnostic_only_policy
    ):
        # Profiles without explicit diagnostic-only retain legacy fallback.
        recommended_ceiling = 10.0

    score_effect = "none"

    if diagnostic_only_policy:
        score_effect = "diagnostic_only"
        configured_caps = {}
        recommended_ceiling = None

    elif (
        fatal_error_detected
        and configured_caps
        and profile_score_policy.get(
            "scope"
        )
        == "theory_core_topic_profile"
    ):
        score_effect = "B_C_only"

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
            "reason": (
                profile_score_policy.get("reason")
                or (
                    "Logic Check에서 THEORY_CORE 핵심 "
                    "이론 오류가 감지됨"
                    if fatal_error_detected
                    else ""
                )
            ),
            "scope": profile_score_policy.get(
                "scope",
                "legacy_logic_check",
            ),
            "status": profile_score_policy.get(
                "status",
                "active",
            ),
            "score_effect": score_effect,
            "direct_score_application": bool(
                profile_score_policy.get(
                    "direct_score_application",
                    score_effect == "B_C_only",
                )
            )
            and score_effect == "B_C_only",
            "layer_caps": (
                configured_caps
                if score_effect == "B_C_only"
                else {}
            ),
            "direct_d_e_effect": "none",
        },
    }

    if _topic_routing_error:
        result["topic_routing_diagnostic"] = {
            "ok": False,
            "error": _topic_routing_error,
            "fallback": "skip_topic_logic_checks",
            "reason": (
                "주제 라우팅 실패로 전체 로직 체크 bank 적용을 "
                "중단했습니다."
            ),
        }

    major_error_detected = any(f.get("severity") == "major" for f in findings)
    minor_or_warn_detected = any(
        f.get("severity") in {"minor", "warn", "warning"} for f in findings
    )

    if fatal_error_detected:
        de_claim_trust_status = "limited"
        de_claim_trust_message = (
            "Logic Check fatal이 감지되어 이 topic을 전제로 한 D/E 현장 적용·결론 주장은 제한적으로 신뢰합니다."
        )
    elif major_error_detected:
        de_claim_trust_status = "not_invalidated"
        de_claim_trust_message = (
            "Logic Check fatal은 없지만 major gap이 남아 있어, 이 topic 기반 D/E 주장은 반증되지는 않았으나 충분히 입증된 것으로 보지는 않습니다."
        )
    elif minor_or_warn_detected:
        de_claim_trust_status = "trusted_with_notes"
        de_claim_trust_message = (
            "Logic Check fatal/major는 없어 이 topic 기반 D/E 주장은 대체로 신뢰 가능하나, 일부 보완 지점이 있습니다."
        )
    else:
        de_claim_trust_status = "trusted"
        de_claim_trust_message = (
            "Logic Check finding이 없어 이 topic을 기반으로 한 D/E 현장 적용·결론 주장은 이론적으로 신뢰 가능합니다."
        )

    result["de_claim_trust_evaluation"] = {
        "enabled": topic_id is not None,
        "target_layers": ["D", "E"],
        "score_effect": "none",
        "status": de_claim_trust_status,
        "message": de_claim_trust_message,
        "rule": "D/E 점수는 A/B/C/D/E scoring model에서만 산정하며 Logic Check는 D/E claim trust만 제공합니다.",
    }

    return result



def _evaluate_topic_fatal_checks_with_llm(text: str, topic_check: dict[str, Any]) -> list[dict[str, Any]]:
    """Use an LLM to semantically verify topic fatal rules.

    Regex wrong_patterns are kept as a fast deterministic path, but they are not
    expressive enough for professional-engineering answers. This verifier reads
    the answer in context and checks whether the answer actually asserts one of
    the topic's fatal misconceptions.

    Safety:
    - If the verifier is unavailable, return no fatal finding.
    - If confidence is below threshold, downgrade fatal to major.
    - Contrastive/corrective statements must not be treated as fatal.
    """
    fatal_checks = topic_check.get("fatal_checks") or []
    if not isinstance(fatal_checks, list) or not fatal_checks:
        return []

    topic_id = str(topic_check.get("topic_id") or "").strip()
    topic_name = str(topic_check.get("topic_name") or "").strip()

    rules: list[dict[str, Any]] = []
    rule_map: dict[str, dict[str, Any]] = {}

    for check in fatal_checks:
        if not isinstance(check, dict):
            continue

        rid = str(check.get("id") or "").strip()
        if not rid:
            continue

        rule = {
            "id": rid,
            "message": check.get("message"),
            "correct_rule": check.get("correct_rule"),
            "recommended_ceiling": check.get("recommended_ceiling", 10.0),
            "examples_or_patterns": check.get("wrong_patterns", []),
        }
        rules.append(rule)
        rule_map[rid] = check

    if not rules:
        return []

    def _diagnostic_finding(
        reason: str,
        error: Exception | None = None,
    ) -> list[dict[str, Any]]:
        diagnostic = {
            "ok": False,
            "reason": reason,
            "error": (
                repr(error)
                if error is not None
                else ""
            ),
        }

        return [
            {
                "id": (
                    "topic_fatal_semantic_"
                    "llm_error"
                ),
                "severity": "minor",
                "message": (
                    "Topic fatal LLM verifier를 "
                    "사용할 수 없어 semantic "
                    "fatal 판정을 건너뛰었습니다: "
                    f"{reason}"
                ),
                "correct_rule": (
                    "LLM verifier 실패 시 fatal "
                    "cap을 적용하지 않습니다."
                ),
                "affected_layers": ["C"],
                "engine": (
                    "topic_fatal_semantic_llm_v1"
                ),
                "diagnostic": diagnostic,
            }
        ]

    def _finite_confidence(
        value: Any,
        field_name: str,
    ) -> float:
        if isinstance(value, bool):
            raise ValueError(
                f"{field_name} must not be bool"
            )

        try:
            confidence = float(value)
        except (
            TypeError,
            ValueError,
            OverflowError,
        ) as error:
            raise ValueError(
                f"{field_name} must be numeric"
            ) from error

        if not math.isfinite(confidence):
            raise ValueError(
                f"{field_name} must be finite"
            )

        return confidence

    prompt = f"""
너는 산업계측제어기술사 답안 채점용 Logic Check verifier다.

중요 원칙:
- 정규표현식 매칭이 아니라 답안의 문맥과 주장을 해석한다.
- 아래 Fatal rules는 이미 fatal로 정의된 규칙이다.
- 답안이 Fatal rule의 wrong claim을 실제로 주장하면 severity는 반드시 "fatal"이다.
- "major"는 답안이 의심스럽지만 wrong claim을 직접 주장했다고 보기 어려운 경우에만 사용한다.
- 단순 누락, 짧은 답안, 설명 부족은 fatal이 아니다.
- 정답을 대비 설명하거나 오류를 부정하는 문장은 fatal이 아니다.
- 애매하면 fatal로 판정하지 말고 major 또는 none으로 둔다.
- 특히 topic_id가 second_order_system_resonance_frequency_response일 때:
  * "공진주파수는 ωr=ωn√(1-ζ²)이다"라고 설명하면 fatal이다.
  * "ωr와 ωd가 같다", "감쇠진동수와 공진주파수가 같다"라고 설명하면 fatal이다.
  * "ζ=1에서 공진 peak가 발생한다" 또는 "ζ=1이 공진 조건이다"라고 설명하면 fatal이다.
  * "ζ=1/√2 또는 0.707이 임계감쇠/중근 조건이다"라고 설명하면 fatal이다.
  * "0<ζ<1이면 공진 peak가 존재한다"처럼 overshoot 조건을 resonance 조건으로 동일시하면 fatal이다.
- 출력은 JSON object 하나만 반환한다.

Topic:
- topic_id: {topic_id}
- topic_name: {topic_name}

Fatal rules:
{json.dumps(rules, ensure_ascii=False, indent=2)}

False-positive caution:
- ζ=1을 시간응답의 임계감쇠로만 설명하면 정상이다.
- ζ=1을 공진 조건 또는 공진 peak 발생 조건으로 설명할 때만 fatal이다.
- ωd=ωn√(1-ζ²)를 시간응답 감쇠진동수로 설명하면 정상이다.
- ωd를 공진주파수 ωr와 같다고 하거나, ωr=ωn√(1-ζ²)로 설명하면 fatal이다.
- ωr≈ωn은 감쇠비가 매우 작은 경우의 근사 설명이면 정상이다.
- ζ=1/√2 또는 0.707을 공진 peak가 사라지는 경계로 설명하면 정상이다.
- ζ=1/√2 또는 0.707을 임계감쇠/중근 조건으로 설명하면 fatal이다.
- overshoot와 resonance가 관련 있다고 말하는 것은 정상이다.
- overshoot 조건 0<ζ<1을 resonance peak 조건으로 동일시하면 fatal이다.

Answer:
<<<ANSWER>>>
{text}
<<<END_ANSWER>>>

Return JSON only:
{{
  "verdict": "fatal | major | pass",
  "confidence": 0.0,
  "findings": [
    {{
      "rule_id": "fatal rule id",
      "severity": "fatal | major",
      "evidence": "답안에서 실제로 문제 되는 주장 요약 또는 짧은 인용",
      "message": "왜 이 rule에 해당하는지",
      "correct_rule": "정정 기준"
    }}
  ],
  "reason": "brief reason"
}}
""".strip()

    try:
        from logic_llm_verifier import _call_ollama_json

        verdict = _call_ollama_json(prompt)
    except Exception as error:
        return _diagnostic_finding(
            "verifier_call_failed",
            error,
        )

    if not isinstance(verdict, dict):
        return _diagnostic_finding(
            "response_must_be_object",
            TypeError(
                "logic LLM response must be "
                f"dict, got "
                f"{type(verdict).__name__}"
            ),
        )

    if "findings" not in verdict:
        return _diagnostic_finding(
            "findings_field_missing",
            KeyError("findings"),
        )

    raw_findings = verdict.get("findings")

    if not isinstance(raw_findings, list):
        return _diagnostic_finding(
            "findings_must_be_list",
            TypeError(
                "findings must be list, got "
                f"{type(raw_findings).__name__}"
            ),
        )

    if not all(
        isinstance(item, dict)
        for item in raw_findings
    ):
        return _diagnostic_finding(
            "finding_item_must_be_object",
            TypeError(
                "every findings item must be dict"
            ),
        )

    try:
        global_confidence = _finite_confidence(
            verdict.get("confidence"),
            "confidence",
        )
    except ValueError as error:
        return _diagnostic_finding(
            "invalid_global_confidence",
            error,
        )

    fatal_threshold = 0.75
    findings: list[dict[str, Any]] = []

    for item in raw_findings:

        rid = str(item.get("rule_id") or item.get("id") or "").strip()
        if rid not in rule_map:
            continue

        severity = str(item.get("severity") or "").strip().lower()
        if severity not in {"fatal", "major"}:
            continue

        if "confidence" in item:
            try:
                item_confidence = (
                    _finite_confidence(
                        item.get("confidence"),
                        (
                            "findings."
                            f"{rid}.confidence"
                        ),
                    )
                )
            except ValueError as error:
                return _diagnostic_finding(
                    "invalid_item_confidence",
                    error,
                )
        else:
            item_confidence = (
                global_confidence
            )

        confidence = max(
            global_confidence,
            item_confidence,
        )

        # Never apply fatal cap on low-confidence semantic interpretation.
        if severity == "fatal" and confidence < fatal_threshold:
            severity = "major"

        # If the LLM selected one of this topic's fatal rules with high
        # confidence, keep the source rule's fatal policy. This is not regex
        # matching; the LLM has already semantically mapped the answer to a
        # fatal rule. Keep it as major only when the LLM explicitly says the
        # answer did not directly assert the misconception or is merely vague.
        elif severity == "major" and confidence >= fatal_threshold:
            combined = " ".join(
                str(x or "")
                for x in [
                    item.get("message"),
                    item.get("evidence"),
                    item.get("reason"),
                ]
            )
            ambiguity_markers = [
                "직접적으로 없",
                "직접 주장은 없",
                "직접 주장하지",
                "오해를 줄 수",
                "오해를 유발",
                "설명 부족",
                "추가 설명",
                "애매",
                "불명확",
                "부족하여",
                "가능성",
            ]
            if not any(marker in combined for marker in ambiguity_markers):
                severity = "fatal"

        source_rule = rule_map[rid]
        message = str(item.get("message") or source_rule.get("message") or "핵심 이론 오류").strip()
        correct_rule = str(item.get("correct_rule") or source_rule.get("correct_rule") or "").strip()
        evidence = str(item.get("evidence") or "").strip()

        if _semantic_evidence_is_corrective_context(
            text,
            evidence,
        ):
            continue

        finding = {
            "id": f"llm_semantic_{rid}",
            "source_rule_id": rid,
            "severity": severity,
            "message": message,
            "correct_rule": correct_rule,
            "affected_layers": source_rule.get("affected_layers", ["C"]),
            "evidence": evidence,
            "engine": "topic_fatal_semantic_llm_v1",
            "confidence": confidence,
        }

        ceiling = source_rule.get("recommended_ceiling")
        if severity == "fatal":
            finding["recommended_ceiling"] = float(ceiling) if isinstance(ceiling, (int, float)) else 10.0

        findings.append(finding)

    # Keep this step focused; avoid flooding the user with many LLM findings.
    fatal_findings = [f for f in findings if f.get("severity") == "fatal"]
    major_findings = [f for f in findings if f.get("severity") == "major"]

    if fatal_findings:
        return fatal_findings[:3] + major_findings[:2]

    return major_findings[:3]

def _logic_normalize_layer_id(value: Any) -> str | None:
    text = str(value or "").strip().upper()

    if text in {"A", "B", "C", "D", "E"}:
        return text

    for separator in (
        ".",
        ":",
        "-",
        "_",
        " ",
    ):
        for layer_id in (
            "A",
            "B",
            "C",
            "D",
            "E",
        ):
            if text.startswith(
                layer_id + separator
            ):
                return layer_id

    return None


def _logic_finite_score(value: Any) -> float | None:
    import math

    if isinstance(value, bool):
        return None

    try:
        score = float(value)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(score):
        return None

    return score


def _logic_entry_score_field(
    entry: dict[str, Any],
) -> str | None:
    preferred_fields = [
        "final_score",
        "score",
        "adjusted_score",
        "weighted_score",
        "layer_score",
        "earned_points",
        "earned",
        "points",
        "obtained",
        "value",
    ]

    for field_name in preferred_fields:
        if (
            field_name in entry
            and _logic_finite_score(
                entry.get(field_name)
            )
            is not None
        ):
            return field_name

    for field_name, value in entry.items():
        lowered = str(field_name).lower()

        if (
            "score" not in lowered
            and "point" not in lowered
            and "earned" not in lowered
        ):
            continue

        if any(
            token in lowered
            for token in [
                "max",
                "maximum",
                "cap",
                "limit",
                "before",
                "base",
                "raw",
                "possible",
                "total",
            ]
        ):
            continue

        if _logic_finite_score(value) is not None:
            return str(field_name)

    return None


def _logic_find_layer_targets(
    breakdown: Any,
) -> dict[str, tuple[Any, Any]]:
    targets: dict[str, tuple[Any, Any]] = {}

    def visit(
        value: Any,
        inherited_layer: str | None = None,
    ) -> None:
        if isinstance(value, dict):
            explicit_layer = None

            for identity_field in [
                "id",
                "layer",
                "layer_id",
                "code",
                "category",
                "name",
                "label",
                "title",
            ]:
                candidate = _logic_normalize_layer_id(
                    value.get(identity_field)
                )

                if candidate:
                    explicit_layer = candidate
                    break

            active_layer = (
                explicit_layer
                or inherited_layer
            )

            if (
                active_layer
                and active_layer not in targets
            ):
                score_field = (
                    _logic_entry_score_field(value)
                )

                if score_field:
                    targets[active_layer] = (
                        value,
                        score_field,
                    )

            for key, child in value.items():
                key_layer = (
                    _logic_normalize_layer_id(key)
                )

                if (
                    key_layer
                    and key_layer not in targets
                ):
                    if (
                        _logic_finite_score(child)
                        is not None
                    ):
                        targets[key_layer] = (
                            value,
                            key,
                        )

                    elif isinstance(child, dict):
                        score_field = (
                            _logic_entry_score_field(
                                child
                            )
                        )

                        if score_field:
                            targets[key_layer] = (
                                child,
                                score_field,
                            )

                visit(
                    child,
                    key_layer or active_layer,
                )

        elif isinstance(value, list):
            for child in value:
                visit(
                    child,
                    inherited_layer,
                )

    visit(breakdown)

    return targets


def _logic_layer_score_snapshot(
    grade: dict[str, Any],
) -> dict[str, float | None]:
    breakdown = grade.get("breakdown")
    targets = _logic_find_layer_targets(
        breakdown
    )

    snapshot: dict[str, float | None] = {}

    for layer_id in [
        "A",
        "B",
        "C",
        "D",
        "E",
    ]:
        target = targets.get(layer_id)

        if not target:
            snapshot[layer_id] = None
            continue

        container, key = target
        snapshot[layer_id] = (
            _logic_finite_score(
                container.get(key)
            )
        )

    return snapshot


def _logic_preserve_score_range_width(
    previous_range: Any,
    total_score: float,
) -> str:
    import re

    text = str(previous_range or "").strip()

    match = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)\s*~\s*"
        r"(-?\d+(?:\.\d+)?)\s*",
        text,
    )

    if match:
        lower = float(match.group(1))
        upper = float(match.group(2))
        half_width = max(
            0.0,
            (upper - lower) / 2.0,
        )
    else:
        half_width = 0.5

    new_lower = max(
        0.0,
        total_score - half_width,
    )
    new_upper = total_score + half_width

    return (
        f"{new_lower:.1f}~"
        f"{new_upper:.1f}"
    )


def _logic_apply_fatal_bc_score_policy(
    grade: dict[str, Any],
    logic_eval: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(grade, dict):
        return grade

    if not isinstance(logic_eval, dict):
        return grade

    fatal = bool(
        logic_eval.get(
            "fatal_error_detected"
        )
    ) or (
        str(
            logic_eval.get("verdict")
            or logic_eval.get("mode")
            or ""
        )
        .strip()
        .lower()
        == "fatal"
    )

    score_policy = logic_eval.get(
        "score_policy"
    )

    if not isinstance(score_policy, dict):
        score_policy = {}
    else:
        score_policy = dict(score_policy)

    logic_eval["score_policy"] = (
        score_policy
    )

    score_effect = str(
        score_policy.get("score_effect")
        or ""
    ).strip()

    diagnostic_only = (
        score_effect == "diagnostic_only"
        or score_policy.get(
            "direct_score_application"
        )
        is False
    )

    if diagnostic_only:
        score_policy["score_effect"] = (
            "diagnostic_only"
        )
        score_policy[
            "direct_score_application"
        ] = False
        score_policy["layer_caps"] = {}
        score_policy[
            "recommended_ceiling"
        ] = None

        logic_eval["score_policy"] = (
            score_policy
        )

        grade[
            "logic_score_adjustment"
        ] = {
            "applied": False,
            "policy": "diagnostic_only",
            "status": score_policy.get(
                "status",
                "provisional",
            ),
            "reason": (
                score_policy.get("reason")
                or (
                    "Logic 오류는 진단에만 사용하며 "
                    "calibration 전에는 점수를 변경하지 않는다."
                )
            ),
            "affected_layers": [],
            "diagnostic_focus_layers": [
                "B",
                "C",
            ],
            "preserved_layers": [
                "A",
                "B",
                "C",
                "D",
                "E",
            ],
            "direct_score_application": False,
            "direct_d_e_effect": "none",
        }

        if fatal:
            grade["grade_confidence"] = (
                "low"
            )
            grade["logic_trust_status"] = (
                "limited"
            )

        return grade

    scope = str(
        score_policy.get("scope")
        or ""
    ).strip()

    score_effect = str(
        score_policy.get("score_effect")
        or ""
    ).strip()

    theory_core_fatal = bool(
        score_policy.get(
            "theory_core_fatal_error"
        )
    )

    raw_caps = score_policy.get(
        "layer_caps"
    )

    configured_caps: dict[
        str,
        float,
    ] = {}

    if isinstance(raw_caps, dict):
        for layer_id in ("B", "C"):
            value = _logic_finite_score(
                raw_caps.get(layer_id)
            )

            if value is not None and value >= 0.0:
                configured_caps[layer_id] = value

    applicable = (
        fatal
        and theory_core_fatal
        and scope
        == "theory_core_topic_profile"
        and score_effect == "B_C_only"
        and set(configured_caps)
        == {"B", "C"}
    )

    if not applicable:
        grade[
            "logic_score_adjustment"
        ] = {
            "applied": False,
            "reason": (
                "Topic Profile에 명시된 THEORY_CORE "
                "fatal B/C cap이 없어 점수를 변경하지 않았다."
            ),
            "affected_layers": [],
            "preserved_layers": [
                "A",
                "B",
                "C",
                "D",
                "E",
            ],
            "scope": scope or "unscoped",
            "direct_d_e_effect": "none",
        }

        return grade

    targets = _logic_find_layer_targets(
        grade.get("breakdown")
    )

    before = _logic_layer_score_snapshot(
        grade
    )

    required_layers = {
        "A",
        "B",
        "C",
        "D",
        "E",
    }

    if not required_layers.issubset(
        targets
    ):
        missing = sorted(
            required_layers - set(targets)
        )

        grade[
            "logic_score_adjustment"
        ] = {
            "applied": False,
            "reason": (
                "B/C cap 적용에 필요한 layer "
                "score path를 찾지 못했다."
            ),
            "missing_layers": missing,
            "affected_layers": [],
            "preserved_layers": [
                "A",
                "D",
                "E",
            ],
            "scope": scope,
            "direct_d_e_effect": "none",
        }

        return grade

    applied_caps: dict[
        str,
        dict[str, float],
    ] = {}

    for layer_id in ("B", "C"):
        cap = configured_caps[layer_id]
        container, key = targets[layer_id]
        current = _logic_finite_score(
            container.get(key)
        )

        if current is None:
            continue

        adjusted = min(
            current,
            cap,
        )

        container[key] = round(
            adjusted,
            2,
        )

        applied_caps[layer_id] = {
            "before": round(
                current,
                2,
            ),
            "cap": round(
                cap,
                2,
            ),
            "after": round(
                adjusted,
                2,
            ),
        }

    after = _logic_layer_score_snapshot(
        grade
    )

    if any(
        after.get(layer_id) is None
        for layer_id in required_layers
    ):
        grade[
            "logic_score_adjustment"
        ] = {
            "applied": False,
            "reason": (
                "B/C cap 적용 후 layer score "
                "snapshot이 불완전하다."
            ),
            "affected_layers": [],
            "preserved_layers": [
                "A",
                "D",
                "E",
            ],
            "before": before,
            "after": after,
            "scope": scope,
            "direct_d_e_effect": "none",
        }

        return grade

    total_before = _logic_finite_score(
        grade.get("total_score")
    )

    recalculated_total = round(
        sum(
            float(after[layer_id])
            for layer_id in [
                "A",
                "B",
                "C",
                "D",
                "E",
            ]
        ),
        2,
    )

    grade["total_score"] = (
        recalculated_total
    )

    applied_cap_record = {
        "id": (
            "logic_theory_core_fatal_bc_caps"
        ),
        "reason": (
            score_policy.get("reason")
            or (
                "THEORY_CORE fatal 오류로 "
                "B/C layer cap을 적용함."
            )
        ),
        "affected_layers": [
            "B",
            "C",
        ],
        "layer_caps": {
            layer_id: round(
                configured_caps[layer_id],
                2,
            )
            for layer_id in ("B", "C")
        },
        "direct_d_e_effect": "none",
    }

    applied_caps = grade.get(
        "applied_caps"
    )

    if not isinstance(applied_caps, list):
        applied_caps = []

    applied_caps = [
        item
        for item in applied_caps
        if not (
            isinstance(item, dict)
            and item.get("id")
            == applied_cap_record["id"]
        )
    ]

    applied_caps.append(
        applied_cap_record
    )
    grade["applied_caps"] = applied_caps

    adjustment = {
        "applied": True,
        "policy": (
            "topic_profile_theory_core_fatal_B_C"
        ),
        "scope": scope,
        "reason": (
            score_policy.get("reason")
            or (
                "THEORY_CORE fatal 오류가 문제 요구의 "
                "정확한 이해와 Fact 정확성을 훼손했다."
            )
        ),
        "affected_layers": [
            "B",
            "C",
        ],
        "preserved_layers": [
            "A",
            "D",
            "E",
        ],
        "layer_caps": applied_caps
        and applied_caps[-1].get(
            "layer_caps"
        ),
        "layer_adjustments": applied_caps
        and applied_caps[-1].get(
            "layer_caps"
        ),
        "before": before,
        "after": after,
        "total_before": total_before,
        "total_after": recalculated_total,
        "recommended_ceiling": (
            score_policy.get(
                "recommended_ceiling"
            )
        ),
        "direct_d_e_effect": "none",
    }

    grade[
        "logic_score_adjustment"
    ] = adjustment

    # Canonical final writer synchronizes total_score, final_total_score,
    # score_range and every threshold flag.
    from grade_score_reconciler import (
        _apply_numeric_flags,
    )

    grade = _apply_numeric_flags(grade)

    adjustment[
        "total_after"
    ] = grade.get("total_score")
    adjustment[
        "final_total_after"
    ] = grade.get(
        "final_total_score"
    )
    adjustment[
        "score_range_after"
    ] = grade.get("score_range")

    grade[
        "logic_score_adjustment"
    ] = adjustment

    return grade


def attach_logic_check_to_grade(
    grade: dict[str, Any],
    answer_text: str,
) -> dict[str, Any]:
    # phase3b can run before final difficulty_strategy is attached.
    # Bridge the best known upstream topic into difficulty_strategy.
    if isinstance(grade, dict):
        difficulty_strategy = grade.get(
            "difficulty_strategy"
        )

        if not isinstance(
            difficulty_strategy,
            dict,
        ):
            difficulty_strategy = {}
        else:
            difficulty_strategy = dict(
                difficulty_strategy
            )

        topic_id = (
            difficulty_strategy.get(
                "topic_id"
            )
            or grade.get("topic_id")
            or grade.get(
                "inferred_topic_id"
            )
            or grade.get(
                "logic_check_topic_id"
            )
            or grade.get(
                "rubric_topic_id"
            )
        )

        if not topic_id:
            question_analysis = grade.get(
                "question_analysis"
            )

            if isinstance(
                question_analysis,
                dict,
            ):
                topic_id = (
                    question_analysis.get(
                        "topic_id"
                    )
                    or question_analysis.get(
                        "inferred_topic_id"
                    )
                    or question_analysis.get(
                        "logic_check_topic_id"
                    )
                )

        if not topic_id:
            metadata = grade.get(
                "metadata"
            )

            if isinstance(metadata, dict):
                topic_id = (
                    metadata.get(
                        "topic_id"
                    )
                    or metadata.get(
                        "inferred_topic_id"
                    )
                    or metadata.get(
                        "logic_check_topic_id"
                    )
                )

        if (
            topic_id
            and not difficulty_strategy.get(
                "topic_id"
            )
        ):
            difficulty_strategy[
                "topic_id"
            ] = str(topic_id)
            grade[
                "difficulty_strategy"
            ] = difficulty_strategy

    logic_eval = evaluate_logic_checks(
        answer_text=answer_text,
        grade=grade,
    )

    if not logic_eval.get("applicable"):
        return grade

    grade["logic_check_evaluation"] = (
        logic_eval
    )

    weaknesses = grade.get("weaknesses")

    if isinstance(weaknesses, list):
        weakness_items = [
            str(item)
            for item in weaknesses
            if str(item).strip()
        ]
    elif (
        isinstance(weaknesses, str)
        and weaknesses.strip()
    ):
        weakness_items = [
            weaknesses.strip()
        ]
    else:
        weakness_items = []

    for finding in logic_eval.get(
        "findings",
        [],
    ):
        if not isinstance(finding, dict):
            continue

        severity = finding.get(
            "severity",
            "warn",
        )
        message = finding.get("message")

        if message:
            _append_unique(
                weakness_items,
                (
                    f"[Logic Check/{severity}] "
                    f"{message}"
                ),
            )

    grade["weaknesses"] = weakness_items

    advice = grade.get("rewrite_advice")

    if isinstance(advice, list):
        advice_items = [
            str(item)
            for item in advice
            if str(item).strip()
        ]
    elif (
        isinstance(advice, str)
        and advice.strip()
    ):
        advice_items = [
            advice.strip()
        ]
    else:
        advice_items = []

    for point in logic_eval.get(
        "next_practice_points",
        [],
    )[:3]:
        _append_unique(
            advice_items,
            f"[Logic Check] {point}",
        )

    grade["rewrite_advice"] = (
        advice_items
    )

    grade = (
        _logic_apply_fatal_bc_score_policy(
            grade,
            logic_eval,
        )
    )

    return grade
