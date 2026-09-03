from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from rubric_bank_paths import resolve_rubric_bank_path

from generic_grading_contract import (
    AlignmentStatus,
    ClaimRelationAssessment,
    ClaimRelationType,
    EvidenceTrustTier,
    evidence_credit_weight,
    normalize_alignment_status,
    normalize_evidence_trust_tier,
    normalize_relation_type,
)


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
    # STAGE22E20I_ROUTER_OWNED_LOGIC_TOPIC_APPLICABILITY_V1
    # Explicit router selection is authoritative. Text aliases
    # remain a fallback only when no logic-check route exists.
    routed_logic_topic_id = str(
        grade.get("logic_check_topic_id") or ""
    ).strip()
    if routed_logic_topic_id:
        current_logic_topic_id = str(
            topic_check.get("topic_id") or ""
        ).strip()
        return bool(
            current_logic_topic_id
            and current_logic_topic_id
            == routed_logic_topic_id
        )

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




def _filter_second_order_legacy_fatal_findings(
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
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
    return filtered


def _apply_second_order_claim_evaluator(text: str, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Second-order damping topic uses JSON-profile LLM verification:
    - JSON profile defines truth_schema, fatal_conditions, safe_conditions, and candidate rules.
    - Python extracts only candidate evidence from the profile.
    - LLM verifies whether the candidate contains a direct contradiction.
    - Legacy hard-coded fatal findings are removed to prevent false caps.
    - Non-fatal major/minor findings remain as supplemental feedback.
    """
    filtered = _filter_second_order_legacy_fatal_findings(findings)

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





# STAGE22D_GLOBAL_CANONICAL_AXIS_COMPARISON_V1
_STAGE22_AXIS_STATUSES = {
    "ALIGNED",
    "PARTIAL",
    "OFF_AXIS",
    "UNSUPPORTED",
    "CONTRADICTED",
    "FATAL_CONTRADICTION",
}
_STAGE22_FATAL_CONFIDENCE = 0.80


def _stage22_clean_refs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str):
            item = item.strip()
            if item and item not in result:
                result.append(item)
    return result


def _stage22_confidence(value: Any) -> float:
    if isinstance(value, bool):
        return 0.0
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return 0.0
    if not math.isfinite(number):
        return 0.0
    return max(0.0, min(1.0, number))


def _stage22_tokens(value: Any) -> set[str]:
    normalized = _normalize_text(str(value or "")).casefold()
    return {
        token
        for token in re.findall(r"[0-9a-zA-Z가-힣_]{2,}", normalized)
        if token not in {
            "한다", "이다", "대한", "위한", "설명", "기준",
            "단계", "경우", "the", "and", "for", "with",
            "from", "this", "that",
        }
    }


def _stage22_axis_id(value: Any, index: int) -> str:
    raw = str(value or "").strip()
    if raw:
        safe = re.sub(
            r"[^0-9a-zA-Z가-힣_.:-]+",
            "_",
            raw,
        ).strip("_")
        if safe:
            return safe[:160]
    return f"canonical_axis_{index:03d}"


def _build_canonical_axis_context(
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    if not isinstance(context, dict):
        return []

    roots: list[tuple[str, Any]] = []
    embedded = context.get("_stage22_canonical_context")
    if isinstance(embedded, dict):
        roots.extend(
            (f"stage22_context.{key}", value)
            for key, value in embedded.items()
            if value is not None
        )
    for key in (
        "model_answer", "fact_anchor", "logic_check",
        "topic_importance", "topic_check",
        "model_answer_reference", "question_demand_evidence",
        "question_demand_evidence_for_score", "question_analysis",
    ):
        value = context.get(key)
        if value is not None:
            roots.append((key, value))
    roots.append(("context", context))

    demands: dict[str, dict[str, Any]] = {}

    def collect_demands(value: Any, path: str) -> None:
        if isinstance(value, dict):
            lower = path.casefold()
            demand_id = str(
                value.get("demand_id")
                or (value.get("id") if "demand" in lower else "")
                or ""
            ).strip()
            demand_text = str(
                value.get("text")
                or value.get("demand")
                or value.get("requirement")
                or value.get("description")
                or ""
            ).strip()
            if demand_id and demand_text:
                demands[demand_id] = {
                    "text": demand_text,
                    "anchor_refs": _stage22_clean_refs(
                        value.get("anchor_refs")
                        or value.get("required_anchor_ids")
                    ),
                }
            for key, child in value.items():
                collect_demands(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                collect_demands(child, f"{path}[{index}]")

    for root_name, root_value in roots:
        collect_demands(root_value, root_name)

    axes: list[dict[str, Any]] = []
    seen_claims: set[str] = set()
    skip_tokens = (
        "wrong_claim", "wrong_pattern", "rejected_explanation",
        "fatal_condition", "common_missing",
    )
    scalar_keys = (
        "statement", "content", "correct_rule", "correction",
        "expected", "truth", "canonical_claim", "intent",
    )
    list_keys = (
        "high_score_points", "accepted_explanations",
        "truth_schema",
    )

    def add_axis(claim: Any, node: Any, path: str) -> None:
        claim_text = str(claim or "").strip()
        normalized = _normalize_text(claim_text).casefold()
        if len(normalized) < 12 or normalized in seen_claims:
            return
        if any(token in path.casefold() for token in skip_tokens):
            return
        node = node if isinstance(node, dict) else {}
        raw_id = (
            node.get("axis_id") or node.get("anchor_id")
            or node.get("id") or node.get("rule_id")
        )
        axis_id = _stage22_axis_id(raw_id, len(axes) + 1)
        anchor_refs = _stage22_clean_refs(
            node.get("anchor_refs") or node.get("anchor_ids")
        )
        if (
            not anchor_refs
            and raw_id
            and ("anchor" in path.casefold() or node.get("anchor_id"))
        ):
            anchor_refs = [str(raw_id).strip()]
        demand_refs = _stage22_clean_refs(node.get("demand_refs"))
        importance = str(
            node.get("importance") or node.get("criticality")
            or node.get("selection_importance") or ""
        ).strip().casefold()
        severity = str(node.get("severity") or "").strip().casefold()
        grading_notes = str(
            node.get("grading_notes") or ""
        ).strip().casefold()
        source_marks_direct_fatal = (
            importance in {
                "must", "core", "high", "critical", "required",
            }
            and "fatal" in grading_notes
            and any(
                marker in grading_notes
                for marker in (
                    "direct", "직접", "opposite", "반대",
                    "contradiction", "충돌",
                )
            )
        )
        fatal_core = bool(
            node.get("fatal") is True
            or node.get("fatal_if_opposite") is True
            or node.get("fatal_requires_direct_opposite_claim") is True
            or node.get("fatal_requires_explicit_contradiction") is True
            or source_marks_direct_fatal
            or (
                severity == "fatal"
                and str(
                    node.get("correct_rule")
                    or node.get("correction") or ""
                ).strip()
            )
        )
        if fatal_core:
            criticality = "fatal_core"
        elif importance in {
            "must", "core", "high", "critical", "required",
        }:
            criticality = "core"
        else:
            criticality = "supporting"
        keywords = _stage22_clean_refs(
            node.get("keywords") or node.get("core_terms")
        )
        token_set = _stage22_tokens(claim_text)
        for keyword in keywords:
            token_set |= _stage22_tokens(keyword)
        axes.append(
            {
                "axis_id": axis_id,
                "axis_name": str(
                    node.get("axis_name") or node.get("title")
                    or node.get("section") or raw_id or path
                ).strip(),
                "canonical_claim": claim_text,
                "criticality": criticality,
                "source_fields": [path],
                "anchor_refs": anchor_refs,
                "demand_refs": demand_refs,
                "_tokens": token_set,
            }
        )
        seen_claims.add(normalized)

    def walk(value: Any, path: str, parent_key: str = "") -> None:
        if any(token in path.casefold() for token in skip_tokens):
            return
        if isinstance(value, dict):
            for key in scalar_keys:
                candidate = value.get(key)
                if isinstance(candidate, str):
                    add_axis(candidate, value, f"{path}.{key}")
            for key in list_keys:
                candidates = value.get(key)
                if isinstance(candidates, list):
                    for index, candidate in enumerate(candidates):
                        if isinstance(candidate, str):
                            add_axis(
                                candidate,
                                value,
                                f"{path}.{key}[{index}]",
                            )
            for key, child in value.items():
                walk(child, f"{path}.{key}", str(key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                if isinstance(child, str) and parent_key in list_keys:
                    add_axis(child, {}, f"{path}[{index}]")
                else:
                    walk(child, f"{path}[{index}]", parent_key)

    for root_name, root_value in roots:
        walk(root_value, root_name)

    for axis in axes:
        if not axis["demand_refs"]:
            axis_tokens = set(axis.get("_tokens") or set())
            axis_anchor_refs = set(axis.get("anchor_refs") or [])
            matched: list[str] = []
            for demand_id, demand in demands.items():
                if axis_anchor_refs & set(demand.get("anchor_refs") or []):
                    matched.append(demand_id)
                    continue
                overlap = axis_tokens & _stage22_tokens(demand.get("text"))
                if len(overlap) >= 2 or any(
                    len(token) >= 6 for token in overlap
                ):
                    matched.append(demand_id)
            axis["demand_refs"] = matched[:8]

    priority = {"fatal_core": 0, "core": 1, "supporting": 2}
    axes.sort(
        key=lambda row: (
            priority.get(str(row.get("criticality")), 9),
            0 if row.get("demand_refs") else 1,
            str(row.get("axis_id")),
        )
    )
    output: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for axis in axes:
        axis_id = str(axis.get("axis_id") or "").strip()
        if not axis_id:
            continue
        if axis_id in used_ids:
            axis_id = _stage22_axis_id(
                f"{axis_id}_{len(output) + 1}",
                len(output) + 1,
            )
            axis["axis_id"] = axis_id
        used_ids.add(axis_id)
        axis.pop("_tokens", None)
        output.append(axis)
        if len(output) >= 64:
            break
    return output


# STAGE22E_SOURCE_OWNED_AXIS_PROVENANCE_V1

def _rebind_exclusive_relation_rows_to_source_owner(
    value: Any,
    *,
    canonical_axes: list[dict[str, Any]] | None,
    answer_text: str | None,
) -> Any:
    if isinstance(value, dict):
        prepared: Any = dict(value)
        raw_rows = value.get("alignments")
    elif isinstance(value, list):
        prepared = list(value)
        raw_rows = value
    else:
        return value

    if not isinstance(raw_rows, list):
        return prepared

    def normalize_token(item: Any) -> str:
        return re.sub(
            r"[^0-9a-z가-힣]+",
            "",
            str(item or "").casefold(),
        )

    def leading_subject(item: Any) -> str:
        text = str(item or "").strip()
        if not text:
            return ""
        korean = re.match(
            r"^\s*([0-9A-Za-z가-힣_./()\-]+?)"
            r"(?:은|는|이|가|을|를)(?=\s|$)",
            text,
        )
        if korean:
            return korean.group(1)
        english = re.match(
            r"^\s*([0-9A-Za-z_./()\- ]{2,80}?)"
            r"\s+(?:is|are|verifies|validates|checks)\b",
            text,
            re.I,
        )
        return english.group(1) if english else ""

    def identifier_suffix_alias(item: Any) -> str:
        tokens = [
            token
            for token in re.split(
                r"[_:.\-/]+",
                str(item or "").casefold(),
            )
            if token
        ]
        while tokens and re.fullmatch(r"[a-z]+\d+", tokens[0]):
            tokens.pop(0)
        return "_".join(tokens)

    def owner_aliases(axis: dict[str, Any]) -> list[str]:
        raw: list[str] = []
        axis_name = str(axis.get("axis_name") or "").strip()
        if axis_name:
            raw.append(axis_name)
            subject = leading_subject(axis_name)
            if subject:
                raw.append(subject)

        subject = leading_subject(axis.get("canonical_claim"))
        if subject:
            raw.append(subject)

        suffix = identifier_suffix_alias(axis.get("axis_id"))
        if suffix:
            raw.append(suffix)
        for ref in axis.get("anchor_refs") or []:
            suffix = identifier_suffix_alias(ref)
            if suffix:
                raw.append(suffix)

        result: list[str] = []
        for item in raw:
            token = normalize_token(item)
            if token and token not in result:
                result.append(token)
        return result

    def source_identity_ready(axis: dict[str, Any]) -> bool:
        axis_id = str(axis.get("axis_id") or "").strip()
        anchors = [
            str(item).strip()
            for item in axis.get("anchor_refs") or []
            if str(item).strip()
        ]
        demands = [
            str(item).strip()
            for item in axis.get("demand_refs") or []
            if str(item).strip()
        ]
        return bool(
            axis_id
            and str(
                axis.get("criticality") or "supporting"
            ).strip().casefold() == "fatal_core"
            and len(anchors) == 1
            and anchors[0] == axis_id
            and demands
        )

    active_axes = [
        dict(axis)
        for axis in (canonical_axes or [])
        if isinstance(axis, dict)
        and str(axis.get("axis_id") or "").strip()
    ]
    axis_by_id = {
        str(axis.get("axis_id") or "").strip(): axis
        for axis in active_axes
    }
    normalized_answer = normalize_token(answer_text or "")
    exclusive_pattern = re.compile(
        r"^\s*(.+?)\.exclusively_establishes\.(.+?)\s*$",
        re.I,
    )
    exclusive_markers = (
        "독점",
        "전담",
        "단독",
        "exclusive",
        "exclusively",
        "sole",
        "only",
    )

    prepared_rows: list[Any] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            prepared_rows.append(raw)
            continue

        row = dict(raw)
        signature = str(
            row.get("claim_signature") or ""
        ).strip()
        match = exclusive_pattern.match(signature)
        status = str(
            row.get("status") or ""
        ).strip().upper()
        error_class = str(
            row.get("error_class") or ""
        ).strip().upper()
        if (
            status == "CANONICAL_RELATION_CONTRADICTION"
            and error_class
            == "CANONICAL_RELATION_CONTRADICTION"
        ):
            status = "CONTRADICTED"
        answer_claim = str(
            row.get("answer_claim")
            or row.get("evidence")
            or ""
        ).strip()
        try:
            confidence = float(row.get("confidence"))
        except (TypeError, ValueError, OverflowError):
            confidence = 0.0

        eligible = bool(
            match
            and status in {
                "CONTRADICTED",
                "FATAL_CONTRADICTION",
            }
            and error_class
            == "CANONICAL_RELATION_CONTRADICTION"
            and confidence >= 0.80
        )
        if eligible:
            subject_token = normalize_token(match.group(1))
            target_token = normalize_token(match.group(2))
            normalized_claim = normalize_token(answer_claim)
            eligible = bool(
                subject_token
                and target_token
                and normalized_claim
                and normalized_claim in normalized_answer
                and subject_token in normalized_claim
                and any(
                    marker in answer_claim.casefold()
                    for marker in exclusive_markers
                )
            )

        if eligible:
            candidates = [
                axis
                for axis in active_axes
                if (
                    subject_token in owner_aliases(axis)
                    and source_identity_ready(axis)
                )
            ]
            if len(candidates) == 1:
                resolved = candidates[0]
                resolved_axis_id = str(
                    resolved.get("axis_id") or ""
                ).strip()
                selected_axis_id = str(
                    row.get("axis_id") or ""
                ).strip()
                selected_axis = axis_by_id.get(selected_axis_id)
                selected_conflicts = bool(
                    selected_axis
                    and selected_axis_id != resolved_axis_id
                    and source_identity_ready(selected_axis)
                )
                if not selected_conflicts:
                    row["axis_id"] = resolved_axis_id
                    row["status"] = "FATAL_CONTRADICTION"

        prepared_rows.append(row)

    if isinstance(prepared, dict):
        prepared["alignments"] = prepared_rows
        return prepared
    return prepared_rows


def _normalize_canonical_axis_alignment_response(
    value: Any,
    *,
    canonical_axes: list[dict[str, Any]] | None = None,
    answer_text: str | None = None,
) -> dict[str, Any]:
    value = _rebind_exclusive_relation_rows_to_source_owner(
        value,
        canonical_axes=canonical_axes,
        answer_text=answer_text,
    )
    axes = canonical_axes if isinstance(canonical_axes, list) else []
    axis_map = {
        str(axis.get("axis_id") or "").strip(): axis
        for axis in axes
        if isinstance(axis, dict)
        and str(axis.get("axis_id") or "").strip()
    }
    if isinstance(value, dict):
        raw_rows = value.get("alignments")
    elif isinstance(value, list):
        raw_rows = value
    else:
        raw_rows = []
    if not isinstance(raw_rows, list):
        raw_rows = []

    aliases = {
        "MATCH": "ALIGNED",
        "MATCHED": "ALIGNED",
        "INCOMPLETE": "PARTIAL",
        "IRRELEVANT": "OFF_AXIS",
        "NOT_SUPPORTED": "UNSUPPORTED",
        "CONTRADICTION": "CONTRADICTED",
        "FATAL": "FATAL_CONTRADICTION",
    }
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        axis_id = str(raw.get("axis_id") or "").strip()
        axis = axis_map.get(axis_id, {})
        axis_known = bool(axis)
        raw_status = str(raw.get("status") or "").strip().upper()
        status = aliases.get(raw_status, raw_status)
        if status not in _STAGE22_AXIS_STATUSES:
            status = "UNSUPPORTED"
        if axis_id and not axis_known:
            status = "UNSUPPORTED"
        answer_claim = str(
            raw.get("answer_claim") or raw.get("evidence") or ""
        ).strip()
        if axis_known:
            canonical_claim = str(
                axis.get("canonical_claim") or ""
            ).strip()
            anchor_refs = _stage22_clean_refs(axis.get("anchor_refs"))
            demand_refs = _stage22_clean_refs(axis.get("demand_refs"))
            criticality = str(
                axis.get("criticality") or "supporting"
            ).strip().casefold()
        else:
            canonical_claim = str(
                raw.get("canonical_claim")
                or raw.get("correct_rule") or ""
            ).strip()
            anchor_refs = _stage22_clean_refs(raw.get("anchor_refs"))
            demand_refs = _stage22_clean_refs(raw.get("demand_refs"))
            criticality = str(
                raw.get("criticality") or "supporting"
            ).strip().casefold()
        signature = str(raw.get("claim_signature") or "").strip()
        if not signature:
            signature = re.sub(
                r"[^0-9a-zA-Z가-힣_.:-]+",
                ".",
                _normalize_text(
                    answer_claim or canonical_claim or axis_id
                ).casefold(),
            ).strip(".")[:240]
        if (
            status in {"CONTRADICTED", "FATAL_CONTRADICTION"}
            and answer_text is not None
        ):
            normalized_answer = _normalize_text(answer_text).casefold()
            normalized_claim = _normalize_text(answer_claim).casefold()
            if not normalized_claim or normalized_claim not in normalized_answer:
                status = "UNSUPPORTED"
        confidence = _stage22_confidence(raw.get("confidence"))
        fatal_allowed = (
            status == "FATAL_CONTRADICTION"
            and criticality == "fatal_core"
            and confidence >= _STAGE22_FATAL_CONFIDENCE
            and bool(anchor_refs)
            and bool(demand_refs)
        )
        if status == "FATAL_CONTRADICTION" and not fatal_allowed:
            status = "CONTRADICTED"
        rows.append(
            {
                "axis_id": axis_id,
                "status": status,
                "answer_claim": answer_claim,
                "canonical_claim": canonical_claim,
                "claim_signature": signature,
                "error_class": str(
                    raw.get("error_class")
                    or (
                        "CANONICAL_RELATION_CONTRADICTION"
                        if status in {
                            "CONTRADICTED", "FATAL_CONTRADICTION",
                        }
                        else "CANONICAL_AXIS_ALIGNMENT"
                    )
                ).strip(),
                "anchor_refs": anchor_refs,
                "demand_refs": demand_refs,
                "criticality": criticality,
                "confidence": confidence,
                "reason": str(raw.get("reason") or "").strip(),
                "fatal": fatal_allowed,
            }
        )
    counts = {
        status: sum(row["status"] == status for row in rows)
        for status in sorted(_STAGE22_AXIS_STATUSES)
    }
    return {
        "version": "canonical_axis_alignment_v1",
        "score_effect": "none",
        "direct_score_application": False,
        "alignments": rows,
        "summary": {
            "alignment_count": len(rows),
            "status_counts": counts,
            "fatal_count": counts.get("FATAL_CONTRADICTION", 0),
        },
    }


def _canonical_axis_alignment_to_findings(
    value: Any,
) -> list[dict[str, Any]]:
    normalized = (
        value
        if (
            isinstance(value, dict)
            and value.get("version") == "canonical_axis_alignment_v1"
            and isinstance(value.get("alignments"), list)
        )
        else _normalize_canonical_axis_alignment_response(value)
    )
    findings: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[str, ...]]] = set()
    for row in normalized.get("alignments", []):
        if not isinstance(row, dict):
            continue
        status = str(row.get("status") or "").strip().upper()
        if status not in {"CONTRADICTED", "FATAL_CONTRADICTION"}:
            continue
        signature = str(row.get("claim_signature") or "").strip()
        if not signature:
            continue
        anchor_refs = _stage22_clean_refs(row.get("anchor_refs"))
        demand_refs = _stage22_clean_refs(row.get("demand_refs"))
        dedup_key = (signature, tuple(demand_refs))
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        confidence = _stage22_confidence(row.get("confidence"))
        criticality = str(
            row.get("criticality") or "supporting"
        ).strip().casefold()
        fatal = (
            status == "FATAL_CONTRADICTION"
            and criticality == "fatal_core"
            and confidence >= _STAGE22_FATAL_CONFIDENCE
            and bool(anchor_refs)
            and bool(demand_refs)
        )
        severity = "fatal" if fatal else "major"
        axis_id = str(row.get("axis_id") or "").strip()
        source_rule_id = "canonical_axis::" + (axis_id or signature)
        findings.append(
            {
                "id": f"canonical_axis_{len(findings) + 1}",
                "candidate_id": axis_id or signature,
                "rule_id": source_rule_id,
                "source_rule_id": source_rule_id,
                "severity": severity,
                "message": str(
                    row.get("reason")
                    or "답안의 주장이 활성 정답 축과 직접 충돌한다."
                ).strip(),
                "correct_rule": str(
                    row.get("canonical_claim") or ""
                ).strip(),
                "affected_layers": ["B", "C"],
                "evidence": str(
                    row.get("answer_claim") or ""
                ).strip(),
                "engine": "canonical_axis_alignment_v1",
                "confidence": confidence,
                "error_class": str(
                    row.get("error_class")
                    or "CANONICAL_RELATION_CONTRADICTION"
                ).strip(),
                "claim_signature": signature,
                "anchor_refs": anchor_refs,
                "demand_refs": demand_refs,
                "alignment_status": status,
                "score_effect": "none",
                "direct_score_application": False,
            }
        )
    return findings


def _stage22_extend_batch_schema(
    schema: dict[str, Any],
    canonical_axes: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return schema
    axis_ids = [
        str(axis.get("axis_id") or "").strip()
        for axis in canonical_axes
        if isinstance(axis, dict)
        and str(axis.get("axis_id") or "").strip()
    ]
    if not axis_ids:
        return schema
    extended = dict(schema)
    properties = dict(extended.get("properties") or {})
    properties["alignments"] = {
        "type": "array",
        "maxItems": min(12, len(axis_ids)),
        "items": {
            "type": "object",
            "properties": {
                "axis_id": {"type": "string", "enum": axis_ids},
                "status": {
                    "type": "string",
                    "enum": sorted(_STAGE22_AXIS_STATUSES),
                },
                "answer_claim": {"type": "string"},
                "canonical_claim": {"type": "string"},
                "claim_signature": {"type": "string"},
                "error_class": {"type": "string"},
                "anchor_refs": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "demand_refs": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "criticality": {
                    "type": "string",
                    "enum": ["supporting", "core", "fatal_core"],
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "reason": {"type": "string"},
            },
            "required": [
                "axis_id", "status", "answer_claim", "canonical_claim",
                "claim_signature", "error_class", "anchor_refs",
                "demand_refs", "criticality", "confidence", "reason",
            ],
            "additionalProperties": False,
        },
    }
    extended["properties"] = properties
    return extended


def _stage22_extend_batch_prompt(
    prompt: str,
    canonical_axes: list[dict[str, Any]],
) -> str:
    axes = [
        {
            "axis_id": axis.get("axis_id"),
            "canonical_claim": axis.get("canonical_claim"),
            "criticality": axis.get("criticality"),
            "anchor_refs": axis.get("anchor_refs"),
            "demand_refs": axis.get("demand_refs"),
        }
        for axis in canonical_axes[:48]
        if isinstance(axis, dict)
    ]
    if not axes:
        return prompt
    return (
        str(prompt)
        + "\n\n[GLOBAL_CANONICAL_AXIS_COMPARISON_V1]\n"
        + "기존 fatal rule 확인과 같은 LLM 호출 안에서 답안 전체의 "
        + "명시적 주장을 아래 활성 정답 축과 비교하라.\n"
        + "문구 유사도가 아니라 개념, 관계 방향, 소유 범위와 조건을 비교한다.\n"
        + "ALIGNED는 같은 의미, PARTIAL은 같은 축의 불완전 설명, "
        + "OFF_AXIS는 다른 축, UNSUPPORTED는 근거 부족이다.\n"
        + "CONTRADICTED는 정답 관계와 직접 충돌하는 주장이다.\n"
        + "FATAL_CONTRADICTION은 fatal_core 축을 답안이 명시적으로 "
        + "반대로 주장하고 confidence>=0.80이며 anchor_refs와 "
        + "demand_refs가 모두 있을 때만 사용한다.\n"
        + "누락, 애매함, 단순 관련성 부족, 다른 유효 축은 오답 또는 "
        + "fatal로 판정하지 않는다.\n"
        + "findings는 기존 사전 정의 rule 전용으로 유지한다. 전역 비교는 "
        + "같은 JSON object의 alignments에만 기록한다.\n"
        + "정답 축이나 기술 기준을 새로 만들지 않는다.\n"
        + "canonical axes:\n"
        + json.dumps(axes, ensure_ascii=False, indent=2)
    )

_GENERIC_ALIGNMENT_ALIASES = {
    "MATCH": AlignmentStatus.ALIGNED,
    "MATCHED": AlignmentStatus.ALIGNED,
    "ALIGNED": AlignmentStatus.ALIGNED,
    "PRESENT": AlignmentStatus.ALIGNED,
    "CORRECT": AlignmentStatus.ALIGNED,
    "PARTIAL": AlignmentStatus.PARTIAL,
    "INCOMPLETE": AlignmentStatus.PARTIAL,
    "CONTRADICTED": AlignmentStatus.CONTRADICTED,
    "CONTRADICTION": AlignmentStatus.CONTRADICTED,
    "FATAL_CONTRADICTION": AlignmentStatus.CONTRADICTED,
    "CANONICAL_RELATION_CONTRADICTION": (
        AlignmentStatus.CONTRADICTED
    ),
    "UNSUPPORTED": AlignmentStatus.UNSUPPORTED,
    "NOT_SUPPORTED": AlignmentStatus.UNSUPPORTED,
    "OFF_AXIS": AlignmentStatus.NOT_APPLICABLE,
    "IRRELEVANT": AlignmentStatus.NOT_APPLICABLE,
    "NOT_APPLICABLE": AlignmentStatus.NOT_APPLICABLE,
}


def _generic_alignment_status(value: Any) -> AlignmentStatus:
    normalized = str(value or "").strip().upper()
    if normalized in _GENERIC_ALIGNMENT_ALIASES:
        return _GENERIC_ALIGNMENT_ALIASES[normalized]
    return normalize_alignment_status(value)


def _generic_relation_type(row: dict[str, Any]) -> ClaimRelationType:
    explicit = (
        row.get("relation_type")
        or row.get("claim_relation_type")
    )
    if explicit:
        return normalize_relation_type(explicit)

    signature = str(
        row.get("claim_signature")
        or row.get("error_class")
        or ""
    ).strip().upper()

    token_map = (
        ("DEFINITION", ClaimRelationType.DEFINITION),
        ("CLASSIFICATION", ClaimRelationType.CLASSIFICATION),
        ("PURPOSE", ClaimRelationType.PURPOSE),
        ("MAPPING", ClaimRelationType.MAPPING),
        ("CAUSE_EFFECT", ClaimRelationType.CAUSE_EFFECT),
        ("CAUSE", ClaimRelationType.CAUSE_EFFECT),
        ("CONDITION", ClaimRelationType.CONDITION),
        ("SEQUENCE", ClaimRelationType.SEQUENCE),
        ("METRIC_SCOPE", ClaimRelationType.METRIC_SCOPE),
        ("SCOPE", ClaimRelationType.METRIC_SCOPE),
        ("COMPONENT", ClaimRelationType.COMPONENT),
        ("EQUIVALENCE", ClaimRelationType.EQUIVALENCE),
    )
    for token, relation_type in token_map:
        if token in signature:
            return relation_type
    return ClaimRelationType.EQUIVALENCE


def _generic_evidence_trust_tier(
    row: dict[str, Any],
) -> EvidenceTrustTier:
    explicit = (
        row.get("evidence_trust_tier")
        or row.get("trust_tier")
    )
    if explicit:
        return normalize_evidence_trust_tier(explicit)

    engine = str(
        row.get("engine")
        or row.get("evidence_source")
        or ""
    ).strip().upper()
    if "DETERMINISTIC" in engine:
        return EvidenceTrustTier.DETERMINISTIC

    anchor_refs = row.get("anchor_refs")
    demand_refs = row.get("demand_refs")
    source_rule = (
        row.get("source_rule_id")
        or row.get("rule_id")
    )
    if (
        isinstance(anchor_refs, list)
        and anchor_refs
        and isinstance(demand_refs, list)
        and demand_refs
    ) or source_rule:
        return EvidenceTrustTier.VERIFIED_STRUCTURED

    evidence = str(
        row.get("evidence")
        or row.get("answer_claim")
        or ""
    ).strip()
    try:
        confidence = float(row.get("confidence") or 0.0)
    except (TypeError, ValueError, OverflowError):
        confidence = 0.0

    if evidence and confidence > 0.0:
        return EvidenceTrustTier.SEMANTIC_INFERRED
    return EvidenceTrustTier.UNSUPPORTED


def normalize_generic_claim_relations(
    value: Any,
) -> dict[str, Any]:
    if isinstance(value, dict):
        raw_rows = (
            value.get("claim_relations")
            or value.get("relations")
            or value.get("alignments")
            or []
        )
    elif isinstance(value, list):
        raw_rows = value
    else:
        raw_rows = []

    if not isinstance(raw_rows, list):
        raw_rows = []

    rows: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_rows, start=1):
        if not isinstance(raw, dict):
            continue

        relation_type = _generic_relation_type(raw)
        alignment_status = _generic_alignment_status(
            raw.get("alignment_status")
            or raw.get("status")
        )
        trust_tier = _generic_evidence_trust_tier(raw)

        claim_id = str(
            raw.get("claim_id")
            or raw.get("id")
            or raw.get("axis_id")
            or raw.get("claim_signature")
            or raw.get("candidate_id")
            or f"claim_relation_{index:03d}"
        ).strip()

        assessment = ClaimRelationAssessment(
            claim_id=claim_id,
            relation_type=relation_type,
            alignment_status=alignment_status,
            evidence_trust_tier=trust_tier,
            source_claim=str(
                raw.get("source_claim")
                or raw.get("answer_claim")
                or raw.get("evidence")
                or ""
            ).strip(),
            target_claim=str(
                raw.get("target_claim")
                or raw.get("canonical_claim")
                or raw.get("correct_rule")
                or ""
            ).strip(),
            evidence=str(
                raw.get("evidence")
                or raw.get("answer_claim")
                or ""
            ).strip(),
        )
        normalized = assessment.to_dict()
        normalized["credit_weight"] = evidence_credit_weight(
            trust_tier,
            alignment_status,
        )
        normalized["confidence"] = raw.get("confidence")
        normalized["anchor_refs"] = (
            list(raw.get("anchor_refs"))
            if isinstance(raw.get("anchor_refs"), list)
            else []
        )
        normalized["demand_refs"] = (
            list(raw.get("demand_refs"))
            if isinstance(raw.get("demand_refs"), list)
            else []
        )
        normalized["source_rule_id"] = str(
            raw.get("source_rule_id")
            or raw.get("rule_id")
            or ""
        ).strip()
        rows.append(normalized)

    relation_counts = {
        item.value: sum(
            row["relation_type"] == item.value
            for row in rows
        )
        for item in ClaimRelationType
    }
    alignment_counts = {
        item.value: sum(
            row["alignment_status"] == item.value
            for row in rows
        )
        for item in AlignmentStatus
    }
    trust_counts = {
        item.value: sum(
            row["evidence_trust_tier"] == item.value
            for row in rows
        )
        for item in EvidenceTrustTier
    }

    return {
        "version": "generic_claim_relation_v1",
        "score_effect": "none",
        "direct_score_application": False,
        "claim_relations": rows,
        "summary": {
            "relation_count": len(rows),
            "relation_type_counts": relation_counts,
            "alignment_status_counts": alignment_counts,
            "evidence_trust_tier_counts": trust_counts,
            "aligned_count": alignment_counts[
                AlignmentStatus.ALIGNED.value
            ],
            "partial_count": alignment_counts[
                AlignmentStatus.PARTIAL.value
            ],
            "contradicted_count": alignment_counts[
                AlignmentStatus.CONTRADICTED.value
            ],
            "unsupported_count": alignment_counts[
                AlignmentStatus.UNSUPPORTED.value
            ],
            "not_applicable_count": alignment_counts[
                AlignmentStatus.NOT_APPLICABLE.value
            ],
            "credited_relation_weight": round(
                sum(
                    float(row["credit_weight"])
                    for row in rows
                ),
                2,
            ),
        },
    }


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


_OPTIONAL_FATAL_RULE_METADATA_FIELDS = (
    "error_class",
    "claim_signature",
    "anchor_refs",
    "demand_refs",
)


def _copy_optional_fatal_rule_metadata(
    finding: dict[str, Any],
    source_rule: dict[str, Any],
) -> dict[str, Any]:
    # Source-owned metadata is copied only when explicitly present.
    if not isinstance(finding, dict) or not isinstance(source_rule, dict):
        return finding

    for field_name in ("error_class", "claim_signature"):
        value = source_rule.get(field_name)
        if isinstance(value, str) and value.strip():
            finding[field_name] = value.strip()

    for field_name in ("anchor_refs", "demand_refs"):
        raw_values = source_rule.get(field_name)
        if not isinstance(raw_values, list):
            continue

        cleaned: list[str] = []
        for raw_value in raw_values:
            if not isinstance(raw_value, str):
                continue
            value = raw_value.strip()
            if value and value not in cleaned:
                cleaned.append(value)

        if cleaned:
            finding[field_name] = cleaned

    return finding



# STAGE25G3_FAIL_CLOSED_SECONDARY_PROFILE_SELECTION_V1
_SECONDARY_PROFILE_ACTIVATION_SCOPE = (
    "claim_triggered_secondary_profile_v1"
)


def _logic_answer_segment(value: str) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    marker = re.search(
        r"\[\s*답안\s*\]\s*",
        text,
        flags=re.IGNORECASE,
    )
    if marker:
        return text[marker.end():].strip()

    marker = re.search(
        r"^/grade\b.*$",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if marker:
        return text[marker.end():].strip()

    return text.strip()


def _secondary_profile_group_matches(
    answer_text: str,
    groups: Any,
) -> list[str]:
    if not isinstance(groups, list):
        return []

    matched: list[str] = []
    for index, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            continue
        group_id = str(group.get("id") or f"group_{index}").strip()
        patterns = group.get("patterns")
        if not group_id or not isinstance(patterns, list):
            continue

        for raw_pattern in patterns:
            pattern = str(raw_pattern or "").strip()
            if not pattern:
                continue
            try:
                found = re.search(
                    pattern,
                    answer_text,
                    flags=re.IGNORECASE,
                )
            except re.error:
                found = None
            if found:
                matched.append(group_id)
                break

    return matched


def _secondary_profile_rule_match(
    answer_text: str,
    rule: Any,
) -> dict[str, Any]:
    if (
        not isinstance(rule, dict)
        or str(rule.get("activation_scope") or "").strip()
        != _SECONDARY_PROFILE_ACTIVATION_SCOPE
    ):
        return {"matched": False}

    strong = _secondary_profile_group_matches(
        answer_text,
        rule.get("strong_pattern_groups"),
    )
    relation = _secondary_profile_group_matches(
        answer_text,
        rule.get("relation_pattern_groups"),
    )
    try:
        minimum = max(
            1,
            int(rule.get("min_strong_groups") or 2),
        )
    except (TypeError, ValueError, OverflowError):
        minimum = 2

    matched = len(strong) >= minimum
    if (
        not matched
        and bool(
            rule.get(
                "single_strong_requires_relation_group",
                True,
            )
        )
        and len(strong) >= 1
        and len(relation) >= 1
    ):
        matched = True

    return {
        "matched": matched,
        "rule_id": str(rule.get("id") or "").strip(),
        "strong_groups": strong,
        "relation_groups": relation,
        "strong_count": len(strong),
        "relation_count": len(relation),
    }


def _select_claim_triggered_secondary_profiles(
    answer_text: str,
    primary_topic_id: str | None,
    topic_checks: Any,
) -> list[dict[str, Any]]:
    if not isinstance(topic_checks, list):
        return []

    allowed = {
        str(row.get("topic_id") or "").strip()
        for row in topic_checks
        if isinstance(row, dict)
        and str(row.get("topic_id") or "").strip()
    }
    if not allowed:
        return []

    try:
        from logic_llm_verifier import LOGIC_CHECK_PROFILE_PATH

        profile_bank = _load_json(Path(LOGIC_CHECK_PROFILE_PATH))
    except Exception:
        return []

    profiles = profile_bank.get("profiles")
    if not isinstance(profiles, list):
        return []

    answer = _logic_answer_segment(answer_text)
    if not answer:
        return []

    selected: list[dict[str, Any]] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        current_topic_id = str(profile.get("topic_id") or "").strip()
        if (
            not current_topic_id
            or current_topic_id == str(primary_topic_id or "").strip()
            or current_topic_id not in allowed
            or not bool(profile.get("enabled", True))
        ):
            continue

        extraction = profile.get("secondary_profile_activation")
        rules = (
            extraction.get("rules")
            if isinstance(extraction, dict)
            else None
        )
        if not isinstance(rules, list):
            continue

        # The activation rule is the authority for secondary diagnostic
        # execution. The profile's primary score policy is not imported.
        eligible_rules = [
            rule
            for rule in rules
            if isinstance(rule, dict)
            and str(
                rule.get("score_effect_requirement")
                or ""
            ).strip()
            == "diagnostic_only"
        ]
        if not eligible_rules:
            continue

        matches = [
            _secondary_profile_rule_match(answer, rule)
            for rule in eligible_rules
        ]
        matches = [
            match
            for match in matches
            if match.get("matched")
        ]
        if not matches:
            continue

        matches.sort(
            key=lambda row: (
                -int(row.get("strong_count") or 0),
                -int(row.get("relation_count") or 0),
                str(row.get("rule_id") or ""),
            )
        )
        selected.append(
            {
                "topic_id": current_topic_id,
                "activation": matches[0],
                "score_effect": "diagnostic_only",
            }
        )

    selected.sort(
        key=lambda row: (
            -int(
                row.get("activation", {}).get("strong_count")
                or 0
            ),
            -int(
                row.get("activation", {}).get("relation_count")
                or 0
            ),
            str(row.get("topic_id") or ""),
        )
    )
    return selected[:1]


def _merge_secondary_logic_evaluations(
    primary_result: dict[str, Any],
    secondary_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    result = dict(primary_result)
    primary_topic_id = str(result.get("topic_id") or "").strip()
    findings = [
        dict(row)
        for row in result.get("findings", [])
        if isinstance(row, dict)
    ]

    def identity(row: dict[str, Any], fallback: str) -> tuple[str, str]:
        return (
            str(row.get("source_topic_id") or fallback or "").strip(),
            str(
                row.get("source_rule_id")
                or row.get("rule_id")
                or row.get("id")
                or ""
            ).strip(),
        )

    seen = {
        identity(row, primary_topic_id)
        for row in findings
    }
    deductions = [
        str(value)
        for value in result.get("deduction_elements", [])
        if str(value or "").strip()
    ]
    practice = [
        str(value)
        for value in result.get("next_practice_points", [])
        if str(value or "").strip()
    ]
    evaluated = [primary_topic_id] if primary_topic_id else []
    summaries: list[dict[str, Any]] = []

    for item in secondary_rows:
        topic_id = str(item.get("topic_id") or "").strip()
        evaluation = item.get("evaluation")
        if not topic_id or not isinstance(evaluation, dict):
            continue

        if topic_id not in evaluated:
            evaluated.append(topic_id)

        merged_ids: list[str] = []
        for raw in evaluation.get("findings", []):
            if not isinstance(raw, dict):
                continue
            row = dict(raw)
            row["source_topic_id"] = topic_id
            row["secondary_profile"] = True
            key = identity(row, topic_id)
            if not key[1] or key in seen:
                continue
            seen.add(key)
            findings.append(row)
            merged_ids.append(key[1])

        for value in evaluation.get("deduction_elements", []):
            _append_unique(deductions, str(value or ""))
        for value in evaluation.get("next_practice_points", []):
            _append_unique(practice, str(value or ""))

        summaries.append(
            {
                "topic_id": topic_id,
                "mode": evaluation.get("mode"),
                "fatal_error_detected": evaluation.get(
                    "fatal_error_detected"
                ),
                "finding_count": len(
                    [
                        row
                        for row in evaluation.get("findings", [])
                        if isinstance(row, dict)
                    ]
                ),
                "merged_finding_ids": merged_ids,
                "activation": item.get("activation"),
                "score_effect": "diagnostic_only",
            }
        )

    result["findings"] = findings
    result["deduction_elements"] = deductions
    result["next_practice_points"] = practice
    result["evaluated_topic_ids"] = evaluated
    result["secondary_profile_evaluations"] = summaries
    result["secondary_profile_selection"] = {
        "version": _SECONDARY_PROFILE_ACTIVATION_SCOPE,
        "score_effect": "diagnostic_only",
        "selected_topic_ids": [
            row["topic_id"]
            for row in summaries
        ],
        "selected_count": len(summaries),
    }
    result["mode"] = _mode_from_findings(findings)

    fatal = any(
        row.get("severity") == "fatal"
        for row in findings
        if isinstance(row, dict)
    )
    major = any(
        row.get("severity") == "major"
        for row in findings
        if isinstance(row, dict)
    )
    minor = any(
        row.get("severity") in {"minor", "warn", "warning"}
        for row in findings
        if isinstance(row, dict)
    )
    result["fatal_error_detected"] = fatal

    score_policy = result.get("score_policy")
    if isinstance(score_policy, dict):
        score_policy = dict(score_policy)
        score_policy["secondary_profile_score_effect"] = "diagnostic_only"
        score_policy[
            "secondary_profile_direct_score_application"
        ] = False
        result["score_policy"] = score_policy

    if fatal:
        status = "limited"
        message = (
            "Primary 또는 진단 전용 secondary Logic Check에서 "
            "fatal이 감지되어 D/E 주장은 제한적으로 신뢰합니다."
        )
    elif major:
        status = "not_invalidated"
        message = (
            "Logic Check major gap이 있어 D/E 주장을 "
            "충분히 입증된 것으로 보지 않습니다."
        )
    elif minor:
        status = "trusted_with_notes"
        message = "Logic Check 보완 지점이 남아 있습니다."
    else:
        status = "trusted"
        message = "Logic Check finding이 없습니다."

    result["de_claim_trust_evaluation"] = {
        "enabled": bool(evaluated),
        "target_layers": ["D", "E"],
        "score_effect": "none",
        "status": status,
        "message": message,
        "rule": (
            "D/E 점수는 A/B/C/D/E scoring model에서만 산정하며 "
            "Logic Check는 D/E claim trust만 제공합니다."
        ),
    }
    return result

# STAGE25G3E_SINGLE_CALL_FULL_LOGIC_OWNER_V1
_STAGE25G3E_INTERNAL_COMPACT_SECONDARY_KEY = (
    "_stage25g3e_compact_secondary_internal_topic_id"
)


# STAGE25G3E2_INTERNAL_TRANSPORT_KEYS_FAIL_SAFE_V1
def _stage25g3e2_read_internal_transport_value(
    grade: Any,
    key: str,
    default: Any = None,
    *,
    normalize_string: bool = False,
) -> Any:
    if not isinstance(grade, dict):
        return default

    try:
        # Internal transport keys are implementation details. Bypass an
        # overridden dict-subclass get() so they cannot consume or alter
        # the public topic-routing failure boundary.
        value = dict.get(
            grade,
            key,
            default,
        )
    except Exception:
        return default

    if not normalize_string:
        return value

    try:
        return str(value or "").strip()
    except Exception:
        return default


def _stage25g3e_candidate_topic_id(
    value: Any,
    *,
    _depth: int = 0,
) -> str:
    if _depth > 8:
        return ""

    if isinstance(value, dict):
        for key in (
            "logic_check_topic_id",
            "topic_id",
            "primary_topic_id",
            "inferred_topic_id",
        ):
            candidate = value.get(key)
            if (
                isinstance(candidate, str)
                and candidate.strip()
            ):
                return candidate.strip()

        for key in (
            "topic_check",
            "profile",
            "candidate",
            "answer",
            "primary_reference",
        ):
            if key not in value:
                continue
            nested = _stage25g3e_candidate_topic_id(
                value.get(key),
                _depth=_depth + 1,
            )
            if nested:
                return nested

        for nested_value in value.values():
            nested = _stage25g3e_candidate_topic_id(
                nested_value,
                _depth=_depth + 1,
            )
            if nested:
                return nested

    elif isinstance(value, (list, tuple)):
        for item in value:
            nested = _stage25g3e_candidate_topic_id(
                item,
                _depth=_depth + 1,
            )
            if nested:
                return nested

    return ""


def _stage25g3e_compact_profile_v2(
    topic_id: str,
) -> dict[str, Any] | None:
    normalized_topic_id = str(
        topic_id or ""
    ).strip()
    if not normalized_topic_id:
        return None

    try:
        from logic_llm_verifier import (
            load_logic_check_profile,
        )

        profile = load_logic_check_profile(
            normalized_topic_id
        )
    except Exception:
        return None

    if not isinstance(profile, dict):
        return None

    compact_config = profile.get(
        "compact_batch_verification"
    )
    if not isinstance(compact_config, dict):
        return None
    if compact_config.get("enabled", True) is not True:
        return None
    if compact_config.get("version") != 2:
        return None
    if compact_config.get("max_llm_calls") != 1:
        return None

    return profile


def _stage25g3e_preselect_compact_secondary(
    answer_text: str,
    primary_topic_id: str,
    topic_logic_checks: Any,
) -> tuple[list[Any], str]:
    raw_candidates = (
        _select_claim_triggered_secondary_profiles(
            answer_text,
            str(primary_topic_id or "").strip(),
            topic_logic_checks,
        )
    )
    if not isinstance(raw_candidates, list):
        return [], ""

    candidates = list(raw_candidates)
    for candidate in candidates:
        candidate_topic_id = (
            _stage25g3e_candidate_topic_id(
                candidate
            )
        )
        if (
            _stage25g3e_compact_profile_v2(
                candidate_topic_id
            )
            is None
        ):
            continue

        # One activated compact secondary owns the sole semantic LLM call.
        return [candidate], candidate_topic_id

    return candidates, ""


def _stage25g3e_multi_topic_batch_ids(
    grade: dict[str, Any],
    answer_text: str,
    primary_topic_id: str,
    topic_logic_checks: Any,
) -> list[str]:
    try:
        contract = grade.get("question_contract") if isinstance(grade, dict) else None
    except Exception:
        return []
    summary = (
        contract.get("multi_topic_grading_context_summary")
        if isinstance(contract, dict)
        else None
    )
    if not isinstance(summary, dict) or summary.get("routing_mode") != "MULTI_TOPIC":
        return []
    topic_ids = [
        str(value).strip()
        for value in summary.get("primary_topic_ids") or []
        if str(value or "").strip()
    ]
    for candidate in _select_claim_triggered_secondary_profiles(
        answer_text,
        str(primary_topic_id or "").strip(),
        topic_logic_checks,
    ):
        topic_id = _stage25g3e_candidate_topic_id(candidate)
        if topic_id and topic_id not in topic_ids:
            topic_ids.append(topic_id)
    return list(dict.fromkeys(topic_ids)) if len(set(topic_ids)) >= 2 else []


def _stage25g3e_pass_profile_evaluation() -> dict[str, Any]:
    return {
        "verdict": "pass",
        "confidence": "high",
        "reason": (
            "Primary generic semantic verifier skipped because "
            "an activated compact secondary owns the single LLM call."
        ),
        "checks": [],
        "findings": [],
        "alignments": [],
    }


# STAGE25G3F_SECONDARY_FATAL_CEILING_MERGE_V1
def _stage25g3f_merge_secondary_fatal_ceiling(
    parent_result: dict[str, Any],
    secondary_evaluation: Any,
    secondary_topic_id: str,
) -> dict[str, Any]:
    if not isinstance(parent_result, dict):
        return parent_result
    if not isinstance(secondary_evaluation, dict):
        return parent_result

    raw_findings = secondary_evaluation.get(
        "findings"
    )
    if not isinstance(raw_findings, list):
        raw_findings = []

    fatal_findings = [
        row
        for row in raw_findings
        if isinstance(row, dict)
        and str(
            row.get("severity") or ""
        ).strip().lower()
        == "fatal"
    ]
    if not fatal_findings:
        return parent_result

    candidate_ceilings: list[float] = []
    fatal_finding_ids: list[str] = []

    for row in fatal_findings:
        finding_id = str(
            row.get("id") or ""
        ).strip()
        if (
            finding_id
            and finding_id
            not in fatal_finding_ids
        ):
            fatal_finding_ids.append(
                finding_id
            )

        value = row.get(
            "recommended_ceiling"
        )
        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and float(value) >= 0.0
        ):
            candidate_ceilings.append(
                float(value)
            )

    secondary_policy = secondary_evaluation.get(
        "score_policy"
    )
    if not isinstance(secondary_policy, dict):
        secondary_policy = {}

    secondary_policy_ceiling = (
        secondary_policy.get(
            "recommended_ceiling"
        )
    )
    if (
        secondary_policy.get(
            "theory_core_fatal_error"
        )
        is True
        and isinstance(
            secondary_policy_ceiling,
            (int, float),
        )
        and not isinstance(
            secondary_policy_ceiling,
            bool,
        )
        and float(
            secondary_policy_ceiling
        )
        >= 0.0
    ):
        candidate_ceilings.append(
            float(
                secondary_policy_ceiling
            )
        )

    distinct_ceilings = sorted(
        set(candidate_ceilings)
    )
    if not distinct_ceilings:
        return parent_result

    secondary_ceiling = min(
        distinct_ceilings
    )

    parent_policy = parent_result.get(
        "score_policy"
    )
    if not isinstance(parent_policy, dict):
        parent_policy = {}
    else:
        parent_policy = dict(
            parent_policy
        )

    existing_ceiling = parent_policy.get(
        "recommended_ceiling"
    )
    if (
        isinstance(existing_ceiling, (int, float))
        and not isinstance(existing_ceiling, bool)
        and float(existing_ceiling) >= 0.0
    ):
        applied_ceiling = min(
            float(existing_ceiling),
            secondary_ceiling,
        )
    else:
        applied_ceiling = secondary_ceiling

    preserve_existing_direct_caps = bool(
        parent_policy.get(
            "direct_score_application"
        )
    ) and str(
        parent_policy.get(
            "score_effect"
        )
        or ""
    ).strip() == "B_C_only"

    parent_policy[
        "theory_core_fatal_error"
    ] = True
    parent_policy[
        "recommended_ceiling"
    ] = applied_ceiling
    parent_policy["reason"] = (
        str(
            parent_policy.get("reason")
            or secondary_policy.get("reason")
            or (
                "Secondary Logic Check fatal이 "
                "감지되어 총점 ceiling을 적용합니다."
            )
        ).strip()
    )
    parent_policy[
        "direct_d_e_effect"
    ] = "none"

    if not preserve_existing_direct_caps:
        parent_policy[
            "score_effect"
        ] = "none"
        parent_policy[
            "direct_score_application"
        ] = False
        parent_policy[
            "layer_caps"
        ] = {}

    previous_merge = parent_policy.get(
        "secondary_fatal_ceiling_merge"
    )
    previous_ids: list[str] = []
    previous_ceilings: list[float] = []
    previous_count = 0

    if isinstance(previous_merge, dict):
        raw_previous_ids = previous_merge.get(
            "fatal_finding_ids"
        )
        if isinstance(raw_previous_ids, list):
            previous_ids = [
                str(value)
                for value in raw_previous_ids
                if str(value).strip()
            ]

        raw_previous_ceilings = (
            previous_merge.get(
                "distinct_candidate_ceilings"
            )
        )
        if isinstance(
            raw_previous_ceilings,
            list,
        ):
            previous_ceilings = [
                float(value)
                for value in raw_previous_ceilings
                if (
                    isinstance(
                        value,
                        (int, float),
                    )
                    and not isinstance(
                        value,
                        bool,
                    )
                )
            ]

        raw_count = previous_merge.get(
            "merge_count"
        )
        if (
            isinstance(raw_count, int)
            and not isinstance(raw_count, bool)
            and raw_count >= 0
        ):
            previous_count = raw_count

    merged_ids = list(previous_ids)
    for finding_id in fatal_finding_ids:
        if finding_id not in merged_ids:
            merged_ids.append(finding_id)

    merged_candidate_ceilings = sorted(
        set(
            previous_ceilings
            + distinct_ceilings
        )
    )

    parent_policy[
        "secondary_fatal_ceiling_merge"
    ] = {
        "version": (
            "stage25g3f_secondary_fatal_"
            "ceiling_merge_v1"
        ),
        "secondary_topic_id": str(
            secondary_topic_id or ""
        ).strip(),
        "fatal_finding_ids": merged_ids,
        "fatal_finding_count": len(
            merged_ids
        ),
        "distinct_candidate_ceilings": (
            merged_candidate_ceilings
        ),
        "applied_ceiling": (
            applied_ceiling
        ),
        "applied_once_per_secondary_evaluation": (
            True
        ),
        "merge_count": previous_count + 1,
        "secondary_score_effect": str(
            secondary_policy.get(
                "score_effect"
            )
            or ""
        ).strip(),
        "secondary_direct_score_application": (
            bool(
                secondary_policy.get(
                    "direct_score_application"
                )
            )
        ),
        "parent_direct_score_application": (
            bool(
                parent_policy.get(
                    "direct_score_application"
                )
            )
        ),
        "direct_d_e_effect": "none",
    }

    parent_result[
        "score_policy"
    ] = parent_policy
    return parent_result


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
    canonical_axis_alignment_evaluation = {
        "version": "canonical_axis_alignment_v1",
        "score_effect": "none",
        "direct_score_application": False,
        "alignments": [],
        "summary": {
            "alignment_count": 0,
            "status_counts": {},
            "fatal_count": 0,
        },
    }
    sil_relation_integrity_evaluation = {
        "version": "sil_relation_integrity_v1",
        "marker": "SIL_RELATION_INTEGRITY_V1",
        "applicable": False,
        "status": "not_applicable",
        "fatal_error_detected": False,
        "findings": [],
    }


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

    llm_profile_enabled = False

    _stage25g3e_internal_compact_secondary_topic_id = (
        _stage25g3e2_read_internal_transport_value(
            grade,
            _STAGE25G3E_INTERNAL_COMPACT_SECONDARY_KEY,
            "",
            normalize_string=True,
        )
    )

    _stage25g3e_preselected_secondary_candidates: list[Any] = []
    _stage25g3e_compact_secondary_topic_id = (
        _stage25g3e_internal_compact_secondary_topic_id
    )
    _stage25g3e_multi_topic_ids = _stage25g3e_multi_topic_batch_ids(
        grade,
        answer_text,
        str(_preferred_logic_topic_id or "").strip(),
        bank.get("topic_logic_checks", []),
    )

    if _stage25g3e_multi_topic_ids:
        _stage25g3e_compact_secondary_topic_id = ""
    elif not _stage25g3e_internal_compact_secondary_topic_id:
        (
            _stage25g3e_preselected_secondary_candidates,
            _stage25g3e_compact_secondary_topic_id,
        ) = _stage25g3e_preselect_compact_secondary(
            answer_text,
            str(_preferred_logic_topic_id or "").strip(),
            bank.get("topic_logic_checks", []),
        )

    for topic_check in _topic_logic_checks_for_evaluation:
        topic_check_enabled = bool(
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
        llm_profile_enabled = False
        try:
            from logic_llm_verifier import (
                load_logic_check_profile,
                verify_logic_with_llm,
            )

            profile = load_logic_check_profile(
                str(topic_id)
            )

            # STAGE22E3_PROFILE_ONLY_CANONICAL_AXIS_RUNTIME_V1
            llm_profile_enabled = (
                isinstance(profile, dict)
                and bool(profile.get("enabled", True))
            )
            if llm_profile_enabled:
                profile_topic_context = dict(topic_check)
                profile_topic_context[
                    "_stage22_canonical_context"
                ] = {
                    "topic_check": topic_check,
                    "model_answer_reference": grade.get(
                        "model_answer_reference"
                    ),
                    "question_demand_evidence": (
                        grade.get(
                            "question_demand_evidence_for_score"
                        )
                        or grade.get(
                            "question_demand_evidence"
                        )
                    ),
                    "question_analysis": grade.get(
                        "question_analysis"
                    ),
                }
                canonical_axes = (
                    _build_canonical_axis_context(
                        profile_topic_context
                    )
                )
                demand_bound_axes = [
                    axis
                    for axis in canonical_axes
                    if isinstance(axis, dict)
                    and axis.get("demand_refs")
                ]
                canonical_axes = (
                    demand_bound_axes[:24]
                    if demand_bound_axes
                    else canonical_axes[:24]
                )

                if _stage25g3e_multi_topic_ids:
                    from logic_llm_verifier import (
                        verify_logic_topics_with_llm,
                    )

                    profile_evaluation = verify_logic_topics_with_llm(
                        answer_text,
                        _stage25g3e_multi_topic_ids,
                    )
                    llm_profile_enabled = True
                elif (
                    _stage25g3e_internal_compact_secondary_topic_id
                    and str(topic_id or '').strip()
                    == _stage25g3e_internal_compact_secondary_topic_id
                ):
                    semantic_topic_check = dict(topic_check)
                    semantic_topic_check['llm_profile'] = profile
                    semantic_topic_check[
                        '_stage22_canonical_context'
                    ] = {
                        'topic_check': topic_check,
                        'model_answer_reference': grade.get(
                            'model_answer_reference'
                        ),
                        'question_demand_evidence': (
                            grade.get(
                                'question_demand_evidence_for_score'
                            )
                            or grade.get(
                                'question_demand_evidence'
                            )
                        ),
                        'question_analysis': grade.get(
                            'question_analysis'
                        ),
                    }
                    semantic_result = (
                        _evaluate_topic_fatal_checks_with_llm(
                            text,
                            semantic_topic_check,
                        )
                    )
                    returned_alignment = (
                        semantic_topic_check.get(
                            '_stage22_axis_alignment_evaluation'
                        )
                    )
                    if isinstance(semantic_result, dict):
                        profile_evaluation = dict(
                            semantic_result
                        )
                    elif isinstance(semantic_result, list):
                        profile_evaluation = {
                            'findings': list(semantic_result),
                        }
                    else:
                        profile_evaluation = {
                            'findings': [],
                        }
                    if isinstance(returned_alignment, dict):
                        profile_evaluation.setdefault(
                            'canonical_axis_alignment_evaluation',
                            returned_alignment,
                        )
                    llm_profile_enabled = True
                elif _stage25g3e_compact_secondary_topic_id:
                    profile_evaluation = (
                        _stage25g3e_pass_profile_evaluation()
                    )
                else:
                    profile_evaluation = (
                        verify_logic_with_llm(
                        answer_text,
                        str(topic_id),
                        canonical_axes=canonical_axes,
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
            if llm_profile_enabled:
                if not isinstance(
                    profile_evaluation,
                    dict,
                ):
                    profile_evaluation = {}

                # STAGE22E10_PROFILE_ALIGNMENT_ENVELOPE_MERGE_V1
                profile_alignment_payload = (
                    profile_evaluation.get(
                        "canonical_axis_alignment_evaluation"
                    )
                    if isinstance(
                        profile_evaluation.get(
                            "canonical_axis_alignment_evaluation"
                        ),
                        dict,
                    )
                    else profile_evaluation
                )
                canonical_axis_alignment_evaluation = (
                    _normalize_canonical_axis_alignment_response(
                        profile_alignment_payload,
                        canonical_axes=canonical_axes,
                        answer_text=text,
                    )
                )
                existing_claim_signatures = {
                    str(
                        existing.get("claim_signature")
                        or ""
                    ).strip()
                    for existing in findings
                    if isinstance(existing, dict)
                }
                for axis_finding in (
                    _canonical_axis_alignment_to_findings(
                        canonical_axis_alignment_evaluation
                    )
                ):
                    claim_signature = str(
                        axis_finding.get("claim_signature")
                        or ""
                    ).strip()
                    if (
                        claim_signature
                        and claim_signature
                        in existing_claim_signatures
                    ):
                        continue
                    findings.append(axis_finding)
                    if claim_signature:
                        existing_claim_signatures.add(
                            claim_signature
                        )

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

            # Profile-owned deterministic rules must not disappear merely
            # because compact multi-topic routing already consumed the single
            # LLM call.  Merge them independently of the LLM branch.
            if isinstance(profile, dict):
                try:
                    from logic_llm_verifier import (
                        _authoritative_structured_findings,
                    )
                    cap_policy = profile.get("cap_policy")
                    default_ceiling = (
                        cap_policy.get("fatal_recommended_ceiling")
                        if isinstance(cap_policy, dict)
                        else None
                    )
                    if not isinstance(default_ceiling, (int, float)):
                        default_ceiling = 10.0
                    deterministic_findings = (
                        _authoritative_structured_findings(
                            answer_text,
                            profile,
                            float(default_ceiling),
                        )
                    )
                except Exception:
                    deterministic_findings = []
                for deterministic_finding in deterministic_findings:
                    identity = str(
                        deterministic_finding.get("source_rule_id")
                        or deterministic_finding.get("rule_id")
                        or deterministic_finding.get("id")
                        or ""
                    )
                    if any(
                        isinstance(existing, dict)
                        and identity
                        and identity == str(
                            existing.get("source_rule_id")
                            or existing.get("rule_id")
                            or existing.get("id")
                            or ""
                        )
                        for existing in findings
                    ):
                        continue
                    findings.append(deterministic_finding)

        if llm_profile_enabled:
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

        if (
            str(topic_id or "").strip()
            == "sil_target_determination_risk_reduction_and_lifecycle"
        ):
            from sil_relation_integrity import (
                evaluate_sil_relation_integrity,
            )

            sil_relation_integrity_evaluation = (
                evaluate_sil_relation_integrity(
                    answer_text
                )
            )
            for relation_finding in (
                sil_relation_integrity_evaluation.get(
                    "findings"
                )
                or []
            ):
                if not isinstance(
                    relation_finding,
                    dict,
                ):
                    continue
                relation_finding = dict(
                    relation_finding
                )
                rule_id = str(
                    relation_finding.get("rule_id")
                    or relation_finding.get(
                        "source_rule_id"
                    )
                    or ""
                ).strip()
                if any(
                    isinstance(existing, dict)
                    and rule_id
                    and rule_id
                    in {
                        str(
                            existing.get("rule_id")
                            or ""
                        ).strip(),
                        str(
                            existing.get(
                                "source_rule_id"
                            )
                            or ""
                        ).strip(),
                    }
                    for existing in findings
                ):
                    continue
                findings.append(relation_finding)

        if not topic_check_enabled:
            break

        for check in topic_check.get("fatal_checks", []):
            for pattern in check.get("wrong_patterns", []):
                # Multiline/table rules depend on row boundaries.  Try the
                # immutable answer first; use normalized text only as a
                # compatibility fallback for symbol normalization.
                matched, ctx = _find_wrong_pattern(answer_text, pattern)
                if not matched:
                    matched, ctx = _find_wrong_pattern(text, pattern)
                if not matched:
                    continue

                if (
                    check.get("id") == "underdamped_as_divergence"
                    and _has_good_underdamped_divergence_separation(text)
                ):
                    continue

                finding = {
                    "id": check.get("id"),
                    "severity": check.get("severity", "fatal"),
                    "message": check.get("message"),
                    "correct_rule": check.get("correct_rule"),
                    "affected_layers": check.get("affected_layers", []),
                    "evidence": ctx,
                    "matched_pattern": pattern,
                }
                _copy_optional_fatal_rule_metadata(
                    finding,
                    check,
                )
                findings.append(finding)
                _append_unique(deduction_elements, check.get("message", "핵심 이론 오류"))
                ceiling = check.get("recommended_ceiling")
                if isinstance(ceiling, (int, float)):
                    recommended_ceiling = ceiling if recommended_ceiling is None else min(recommended_ceiling, float(ceiling))
                break

        # Semantic fatal fallback:
        # wrong_patterns are only a fast deterministic aid. If they do not catch
        # a fatal misconception, ask the LLM verifier to interpret the answer
        # against this topic's fatal rules in context.
        if not llm_profile_enabled and (not any(f.get("severity") == "fatal" for f in findings)):
            semantic_topic_check = dict(topic_check)
            semantic_topic_check["_stage22_canonical_context"] = {
                "topic_check": topic_check,
                "model_answer_reference": grade.get("model_answer_reference"),
                "question_demand_evidence": (
                    grade.get("question_demand_evidence_for_score")
                    or grade.get("question_demand_evidence")
                ),
                "question_analysis": grade.get("question_analysis"),
            }
            semantic_findings = _evaluate_topic_fatal_checks_with_llm(
                text,
                semantic_topic_check,
            )
            returned_alignment = semantic_topic_check.get(
                "_stage22_axis_alignment_evaluation"
            )
            if isinstance(returned_alignment, dict):
                canonical_axis_alignment_evaluation = returned_alignment

            for semantic_finding in semantic_findings:
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
        if llm_profile_enabled:
            findings = (
                _filter_second_order_legacy_fatal_findings(
                    findings
                )
            )
        else:
            findings = (
                _apply_second_order_claim_evaluator(
                    text,
                    findings,
                )
            )
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
        "sil_relation_integrity_evaluation": (
            sil_relation_integrity_evaluation
        ),
        "canonical_axis_alignment_evaluation": (
            canonical_axis_alignment_evaluation
        ),
        "generic_claim_relation_evaluation": (
            normalize_generic_claim_relations(
                canonical_axis_alignment_evaluation
            )
        ),
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

    # STAGE25G3_FAIL_CLOSED_SECONDARY_PROFILE_COMPOSITION_V1
    if (
        isinstance(grade, dict)
        and not bool(
            _stage25g3e2_read_internal_transport_value(
        grade,
        "_logic_check_secondary_replay",
        False,
    )
        )
    ):
        if _stage25g3e_internal_compact_secondary_topic_id:
            candidates = []
        else:
            candidates = list(
                _stage25g3e_preselected_secondary_candidates
            )
        secondary_rows: list[dict[str, Any]] = []

        for candidate in candidates:
            secondary_topic_id = str(
                candidate.get("topic_id") or ""
            ).strip()
            if not secondary_topic_id:
                continue

            secondary_grade = dict(grade)
            secondary_grade["_logic_check_secondary_replay"] = True
            for key in (
                "logic_check_topic_id",
                "topic_id",
                "inferred_topic_id",
                "primary_topic_id",
            ):
                secondary_grade[key] = secondary_topic_id

            _stage25g3e_secondary_topic_id = (
                _stage25g3e_candidate_topic_id(
                    secondary_grade
                )
            )
            if (
                _stage25g3e_compact_secondary_topic_id
                and _stage25g3e_secondary_topic_id
                == _stage25g3e_compact_secondary_topic_id
            ):
                secondary_grade[
                    _STAGE25G3E_INTERNAL_COMPACT_SECONDARY_KEY
                ] = _stage25g3e_compact_secondary_topic_id
            evaluation = evaluate_logic_checks(
                answer_text,
                secondary_grade,
                path,
            )
            result = (
                _stage25g3f_merge_secondary_fatal_ceiling(
                    result,
                    evaluation,
                    _stage25g3e_secondary_topic_id,
                )
            )
            if (
                isinstance(evaluation, dict)
                and evaluation.get("applicable") is True
            ):
                secondary_rows.append(
                    {
                        "topic_id": secondary_topic_id,
                        "activation": candidate.get("activation"),
                        "evaluation": evaluation,
                    }
                )

        if secondary_rows:
            result = _merge_secondary_logic_evaluations(
                result,
                secondary_rows,
            )

    result['single_llm_owner_evaluation'] = {
        'version': 'stage25g3e_single_call_owner_v7',
        'compact_secondary_topic_id': (
            _stage25g3e_compact_secondary_topic_id
        ),
        'internal_compact_secondary': bool(
            _stage25g3e_internal_compact_secondary_topic_id
        ),
        'primary_profile_verifier_skipped': bool(
            _stage25g3e_compact_secondary_topic_id
            and not _stage25g3e_internal_compact_secondary_topic_id
        ),
        'semantic_llm_owner': (
            'multi_topic_batch'
            if _stage25g3e_multi_topic_ids
            else (
                'secondary_compact_helper'
                if _stage25g3e_compact_secondary_topic_id
                else 'primary_profile_verifier'
            )
        ),
        'multi_topic_ids': _stage25g3e_multi_topic_ids,
        'max_llm_calls': 1,
    }
    return result




# STAGE19B2_EXISTING_SEMANTIC_RESPONSE_NORMALIZATION_V2
def _normalize_topic_fatal_semantic_response(
    value: Any,
) -> Any:
    # No new technical judgement is created here.
    # Only explicit asserted major/fatal checks become findings.
    if not isinstance(value, dict):
        return value

    normalized = dict(value)

    for container_key in (
        "result",
        "output",
        "analysis",
    ):
        nested = normalized.get(container_key)

        if not isinstance(nested, dict):
            continue

        if not any(
            key in nested
            for key in (
                "findings",
                "checks",
                "verdict",
                "confidence",
                "reason",
            )
        ):
            continue

        for key in (
            "findings",
            "checks",
            "verdict",
            "confidence",
            "reason",
        ):
            if key not in normalized and key in nested:
                normalized[key] = nested[key]

    if isinstance(normalized.get("findings"), list):
        return normalized

    checks = normalized.get("checks")

    if not isinstance(checks, list):
        return normalized

    findings = []

    for row in checks:
        if not isinstance(row, dict):
            continue

        if row.get("asserted") is not True:
            continue

        severity = str(
            row.get("severity")
            or row.get("status")
            or ""
        ).strip().lower()

        if severity not in {"major", "fatal"}:
            continue

        rule_id = str(
            row.get("rule_id")
            or row.get("id")
            or ""
        ).strip()

        if not rule_id:
            continue

        finding = {
            "rule_id": rule_id,
            "severity": severity,
            "candidate_id": str(
                row.get("candidate_id") or ""
            ).strip(),
            "evidence": str(
                row.get("evidence") or ""
            ).strip(),
            "message": str(
                row.get("message")
                or row.get("reason")
                or ""
            ).strip(),
            "correct_rule": str(
                row.get("correct_rule")
                or row.get("correction")
                or ""
            ).strip(),
        }

        confidence = row.get(
            "confidence",
            normalized.get("confidence"),
        )

        if confidence is not None:
            finding["confidence"] = confidence

        findings.append(finding)

    normalized["findings"] = findings
    normalized["semantic_response_normalization"] = {
        "marker": (
            "STAGE19B2_EXISTING_SEMANTIC_"
            "RESPONSE_NORMALIZATION_V2"
        ),
        "source": "existing_checks",
        "asserted_required": True,
        "allowed_statuses": ["major", "fatal"],
        "new_rule_owner_created": False,
        "score_effect": "none",
    }
    return normalized



# STAGE19D_EXISTING_SEMANTIC_SCHEMA_REPAIR_V1

# STAGE19F_EXISTING_FATAL_RULE_JSON_SCHEMA_V1
def _topic_fatal_semantic_json_schema(
    topic_check: dict[str, Any],
) -> dict[str, Any]:
    # The enum comes only from the existing Topic Profile rule IDs.
    fatal_checks = topic_check.get("fatal_checks")

    if not isinstance(fatal_checks, list):
        fatal_checks = []

    rule_ids = []

    for row in fatal_checks:
        if not isinstance(row, dict):
            continue

        rule_id = str(
            row.get("id")
            or row.get("rule_id")
            or ""
        ).strip()

        if rule_id and rule_id not in rule_ids:
            rule_ids.append(rule_id)

    rule_id_schema: dict[str, Any] = {
        "type": "string",
    }

    if rule_ids:
        rule_id_schema["enum"] = rule_ids

    check_schema = {
        "type": "object",
        "properties": {
            "rule_id": rule_id_schema,
            "status": {
                "type": "string",
                "enum": [
                    "pass",
                    "major",
                    "fatal",
                ],
            },
            "asserted": {
                "type": "boolean",
            },
            "candidate_id": {
                "type": "string",
            },
            "evidence": {
                "type": "string",
            },
            "reason": {
                "type": "string",
            },
            "correction": {
                "type": "string",
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
        },
        "required": [
            "rule_id",
            "status",
            "asserted",
            "candidate_id",
            "evidence",
            "reason",
            "correction",
            "confidence",
        ],
        "additionalProperties": False,
    }

    finding_schema = {
        "type": "object",
        "properties": {
            "candidate_id": {
                "type": "string",
            },
            "rule_id": rule_id_schema,
            "severity": {
                "type": "string",
                "enum": [
                    "major",
                    "fatal",
                ],
            },
            "message": {
                "type": "string",
            },
            "correct_rule": {
                "type": "string",
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
        },
        "required": [
            "candidate_id",
            "rule_id",
            "severity",
            "message",
            "correct_rule",
            "confidence",
        ],
        "additionalProperties": False,
    }

    return {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "enum": [
                    "pass",
                    "warn",
                    "fatal",
                ],
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "reason": {
                "type": "string",
            },
            "checks": {
                "type": "array",
                "items": check_schema,
            },
            "findings": {
                "type": "array",
                "items": finding_schema,
            },
        },
        "required": [
            "verdict",
            "confidence",
            "reason",
            "checks",
            "findings",
        ],
        "additionalProperties": False,
    }


def _repair_topic_fatal_semantic_schema_once(
    *,
    prompt: str,
    initial_response: Any,
    topic_check: dict[str, Any],
) -> Any:
    # Retry once only when the existing verifier omitted its schema.
    normalized = (
        _normalize_topic_fatal_semantic_response(
            initial_response
        )
    )

    if (
        isinstance(normalized, dict)
        and isinstance(
            normalized.get("findings"),
            list,
        )
    ):
        return normalized

    if not isinstance(normalized, dict):
        return normalized

    fatal_checks = topic_check.get(
        "fatal_checks"
    )

    if not isinstance(fatal_checks, list):
        return normalized

    existing_rules = []

    for row in fatal_checks:
        if not isinstance(row, dict):
            continue

        rule_id = str(
            row.get("id")
            or row.get("rule_id")
            or ""
        ).strip()

        if not rule_id:
            continue

        existing_rules.append(
            {
                "rule_id": rule_id,
                "condition": str(
                    row.get("message")
                    or row.get("condition")
                    or ""
                ).strip(),
                "correct_rule": str(
                    row.get("correct_rule")
                    or ""
                ).strip(),
            }
        )

    if not existing_rules:
        return normalized

    import json
    from logic_llm_verifier import (
        _call_ollama_json,
    )

    repair_prompt = (
        "이전 기술 검증 응답은 필수 schema를 누락했다.\n"
        "새로운 기술 판단이나 새로운 rule id를 만들지 말고, "
        "아래 기존 rule id만 사용하여 이전 판정을 구조화하라.\n"
        "각 rule을 checks에 정확히 한 번 포함한다.\n"
        "답안이 해당 오개념을 직접 주장한 경우에만 "
        "asserted=true 및 status=major 또는 fatal로 기록한다.\n"
        "직접 주장하지 않았거나 근거가 불충분하면 "
        "asserted=false 및 status=pass로 기록한다.\n"
        "findings에는 asserted=true인 major/fatal만 포함한다.\n"
        "반드시 JSON 객체만 반환한다.\n\n"
        "기존 rule 목록:\n"
        + json.dumps(
            existing_rules,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n\n이전 응답:\n"
        + json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n\n원래 검증 지시:\n"
        + str(prompt)
        + "\n\n필수 출력 필드: "
        "verdict, confidence, reason, checks, findings"
    )

    repaired = (
        _normalize_topic_fatal_semantic_response(
            _call_ollama_json(
                repair_prompt,
                format_schema=(
                    _topic_fatal_semantic_json_schema(
                        topic_check
                    )
                ),
            )
        )
    )

    if not (
        isinstance(repaired, dict)
        and isinstance(
            repaired.get("findings"),
            list,
        )
    ):
        return normalized

    repaired[
        "semantic_schema_repair"
    ] = {
        "marker": (
            "STAGE19D_EXISTING_SEMANTIC_"
            "SCHEMA_REPAIR_V1"
        ),
        "attempt_count": 1,
        "rule_source": (
            "existing_topic_fatal_checks"
        ),
        "new_rule_owner_created": False,
        "direct_reason_to_rule_inference": False,
        "score_effect": "none",
    }
    return repaired


# STAGE19J_EXISTING_FATAL_PER_RULE_EVALUATION_V1
def _single_topic_fatal_finding_schema(
    rule_id: str,
) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "maxItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": {
                            "type": "string",
                            "const": rule_id,
                        },
                        "severity": {
                            "type": "string",
                            "enum": [
                                "major",
                                "fatal",
                            ],
                        },
                        "evidence": {
                            "type": "string",
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                        },
                    },
                    "required": [
                        "rule_id",
                        "severity",
                        "evidence",
                        "confidence",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "findings",
        ],
        "additionalProperties": False,
    }


def _single_topic_fatal_prompt(
    text: str,
    check: dict[str, Any],
) -> str:
    rule_id = str(
        check.get("id")
        or check.get("rule_id")
        or ""
    ).strip()
    condition = str(
        check.get("message")
        or check.get("condition")
        or ""
    ).strip()
    correct_rule = str(
        check.get("correct_rule")
        or ""
    ).strip()

    return (
        "다음 답안이 아래 기존 fatal rule 하나를 "
        "직접 위반하는지만 판정하라.\n"
        "새로운 rule id 또는 새로운 기술 기준을 만들지 않는다.\n"
        "답안에 오개념이 직접 주장된 경우에만 findings에 "
        "항목 하나를 기록한다.\n"
        "누락, 애매함, 설명 부족 또는 추론만으로는 "
        "findings를 만들지 않는다.\n"
        "evidence는 답안에서 공백을 포함해 직접 복사한 "
        "짧은 원문이어야 한다.\n"
        "답안이 잘못된 표현을 부정하거나 정정하는 문맥이면 "
        "findings를 만들지 않는다.\n"
        "반드시 제공된 JSON schema만 반환한다.\n\n"
        f"rule_id: {rule_id}\n"
        f"오류 조건: {condition}\n"
        f"정정 기준: {correct_rule}\n\n"
        "답안:\n"
        + str(text)
    )


def _evaluate_topic_fatal_checks_with_llm_legacy_contract(text: str, topic_check: dict[str, Any]) -> list[dict[str, Any]]:
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

        _copy_optional_fatal_rule_metadata(
            finding,
            source_rule,
        )
        findings.append(finding)

    # Keep this step focused; avoid flooding the user with many LLM findings.
    fatal_findings = [f for f in findings if f.get("severity") == "fatal"]
    major_findings = [f for f in findings if f.get("severity") == "major"]

    if fatal_findings:
        return fatal_findings[:3] + major_findings[:2]

    return major_findings[:3]


def _topic_fatal_batch_finding_schema(
    eligible_checks: list[dict[str, Any]],
) -> dict[str, Any]:
    rule_ids = [
        str(
            check.get("id")
            or check.get("rule_id")
            or ""
        ).strip()
        for check in eligible_checks
    ]
    rule_ids = [
        rule_id
        for rule_id in rule_ids
        if rule_id
    ]

    return {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "maxItems": len(rule_ids),
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": {
                            "type": "string",
                            "enum": rule_ids,
                        },
                        "severity": {
                            "type": "string",
                            "enum": [
                                "major",
                                "fatal",
                            ],
                        },
                        "evidence": {
                            "type": "string",
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                        },
                    },
                    "required": [
                        "rule_id",
                        "severity",
                        "evidence",
                        "confidence",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "findings",
        ],
        "additionalProperties": False,
    }


def _topic_fatal_batch_prompt(
    text: str,
    eligible_checks: list[dict[str, Any]],
) -> str:
    rules = []

    for check in eligible_checks:
        rule_id = str(
            check.get("id")
            or check.get("rule_id")
            or ""
        ).strip()

        if not rule_id:
            continue

        rules.append(
            {
                "rule_id": rule_id,
                "error_condition": str(
                    check.get("message")
                    or check.get("condition")
                    or ""
                ).strip(),
                "correct_rule": str(
                    check.get("correct_rule")
                    or ""
                ).strip(),
            }
        )

    return (
        "다음 답안이 아래 기존 fatal rule들을 직접 "
        "위반하는지 한 번에 판정하라.\n"
        "새로운 rule id 또는 새로운 기술 기준을 만들지 않는다.\n"
        "각 rule은 서로 독립적으로 판정한다.\n"
        "답안에 오개념이 직접 주장된 rule만 findings에 기록한다.\n"
        "한 rule_id당 findings 항목은 최대 하나이다.\n"
        "누락, 애매함, 설명 부족 또는 추론만으로는 "
        "findings를 만들지 않는다.\n"
        "evidence는 답안에서 공백을 포함해 직접 복사한 "
        "짧은 원문이어야 한다.\n"
        "답안이 잘못된 표현을 부정하거나 정정하는 문맥이면 "
        "findings를 만들지 않는다.\n"
        "반드시 제공된 JSON schema만 반환한다.\n\n"
        "기존 fatal rules:\n"
        + json.dumps(
            rules,
            ensure_ascii=False,
            indent=2,
        )
        + "\n\n답안:\n"
        + str(text)
    )



# STAGE25G3C_COMPACT_ONE_CALL_SECONDARY_V1
def _stage25g3c_compact_batch_config(
    local_values: dict[str, Any],
) -> dict[str, Any] | None:
    for value in local_values.values():
        if not isinstance(value, dict):
            continue

        direct = value.get("compact_batch_verification")
        if isinstance(direct, dict):
            return direct

        nested = value.get("llm_profile")
        if isinstance(nested, dict):
            direct = nested.get("compact_batch_verification")
            if isinstance(direct, dict):
                return direct

    return None


def _stage25g3c_extract_compact_evidence(
    text: str,
    selectors: list[dict[str, Any]],
) -> str:
    normalized_text = str(text or "")
    chunks: list[str] = []

    for selector in selectors:
        if not isinstance(selector, dict):
            continue

        pattern = str(selector.get("pattern") or "").strip()
        if not pattern:
            continue

        window = max(
            0,
            min(int(selector.get("window") or 300), 1200),
        )
        max_matches = max(
            1,
            min(int(selector.get("max_matches") or 1), 4),
        )

        try:
            matches = list(
                re.finditer(
                    pattern,
                    normalized_text,
                    flags=re.IGNORECASE | re.DOTALL,
                )
            )
        except re.error:
            matches = list(
                re.finditer(
                    re.escape(pattern),
                    normalized_text,
                    flags=re.IGNORECASE,
                )
            )

        for match in matches[:max_matches]:
            start = max(0, match.start() - window)
            end = min(
                len(normalized_text),
                match.end() + window,
            )
            chunk = re.sub(
                r"\s+",
                " ",
                normalized_text[start:end],
            ).strip()
            if chunk and chunk not in chunks:
                chunks.append(chunk)

    return "\n\n".join(chunks)[:5000]


def _stage25g3c_compact_rule_record(
    raw: Any,
) -> dict[str, Any] | None:
    if isinstance(raw, dict):
        rule_id = str(
            raw.get("id")
            or raw.get("rule_id")
            or raw.get("check_id")
            or ""
        ).strip()
        if not rule_id:
            return None

        return {
            "id": rule_id,
            "wrong_claim": str(
                raw.get("wrong_claim")
                or raw.get("claim")
                or raw.get("description")
                or ""
            ).strip(),
            "correct_rule": str(
                raw.get("correct_rule")
                or raw.get("correction")
                or raw.get("message")
                or ""
            ).strip(),
            "severity": str(
                raw.get("severity") or "fatal"
            ).strip().lower(),
            "affected_layers": list(
                raw.get("affected_layers") or ["C"]
            ),
            "recommended_ceiling": raw.get(
                "recommended_ceiling"
            ),
        }

    if not isinstance(raw, str):
        return None

    text = re.sub(r"\s+", " ", raw).strip()
    match = re.match(
        r"^\[([^\]]+)\]\s*(.*)$",
        text,
    )
    if not match:
        return None

    rule_id = match.group(1).strip()
    body = match.group(2).strip()
    wrong_claim = body
    correct_rule = ""

    if "정답은" in body:
        left, right = body.split("정답은", 1)
        wrong_claim = left.strip()
        correct_rule = "정답은 " + right.strip()
    else:
        sentence_match = re.match(
            r"^(.+?[.!?])\s*(.+)$",
            body,
        )
        if sentence_match:
            wrong_claim = sentence_match.group(1).strip()
            correct_rule = sentence_match.group(2).strip()

    return {
        "id": rule_id,
        "wrong_claim": wrong_claim,
        "correct_rule": correct_rule,
        "severity": "fatal",
        "affected_layers": ["C", "D"],
        "recommended_ceiling": 14.5,
    }


def _stage25g3c_compact_diagnostic(
    reason: str,
    detail: str = "",
) -> dict[str, Any]:
    return {
        "mode": "warn",
        "fatal_error_detected": False,
        "findings": [],
        "diagnostics": [
            {
                "id": "stage25g3c_compact_batch_diagnostic",
                "severity": "warn",
                "reason": reason,
                "message": detail.strip() or reason,
                "affected_layers": [],
            }
        ],
        "compact_batch_verification": {
            "status": "invalid",
            "reason": reason,
            "llm_call_count": 1,
        },
    }


# STAGE25G3D_COMPACT_STRUCTURED_EVIDENCE_ARBITRATION_V1
def _stage25g3d_extract_structured_relation(
    text: str,
    spec: Any,
) -> str:
    if not isinstance(spec, dict):
        return ""

    pattern = str(
        spec.get("combined_pattern") or ""
    ).strip()
    rendered = str(
        spec.get("render") or ""
    ).strip()
    if not pattern or not rendered:
        return ""

    try:
        matched = re.search(
            pattern,
            str(text or ""),
            flags=re.IGNORECASE | re.DOTALL,
        )
    except re.error:
        matched = re.search(
            re.escape(pattern),
            str(text or ""),
            flags=re.IGNORECASE,
        )

    return rendered if matched else ""


def _stage25g3c_compact_batch_secondary_once(
    text: str,
    eligible_checks: list[Any],
    local_values: dict[str, Any],
) -> dict[str, Any] | None:
    from logic_llm_verifier import (
        _call_ollama_json,
    )

    config = _stage25g3c_compact_batch_config(
        local_values
    )
    if not isinstance(config, dict):
        return None

    if not bool(config.get("enabled", True)):
        return None

    if int(config.get("max_llm_calls") or 1) != 1:
        return _stage25g3c_compact_diagnostic(
            "compact_batch_invalid_max_llm_calls",
            "max_llm_calls must be 1",
        )

    fields = config.get("fields")
    if not isinstance(fields, list) or not fields:
        return _stage25g3c_compact_diagnostic(
            "compact_batch_missing_fields"
        )

    rule_records: dict[str, dict[str, Any]] = {}
    for raw in eligible_checks:
        record = _stage25g3c_compact_rule_record(raw)
        if record is not None:
            rule_records[record["id"]] = record

    field_ids: list[str] = []
    field_evidence: dict[str, str] = {}
    structured_evidence: dict[str, str] = {}

    for field in fields:
        if not isinstance(field, dict):
            return _stage25g3c_compact_diagnostic(
                "compact_batch_invalid_field"
            )

        field_id = str(
            field.get("field_id") or ""
        ).strip()
        if (
            not field_id
            or field_id in field_ids
            or re.fullmatch(
                r"[a-z][a-z0-9_]*",
                field_id,
            )
            is None
        ):
            return _stage25g3c_compact_diagnostic(
                "compact_batch_invalid_field_id",
                field_id,
            )

        selectors = field.get("evidence_selectors")
        if not isinstance(selectors, list):
            selectors = []

        raw_evidence = (
            _stage25g3c_extract_compact_evidence(
                text,
                selectors,
            )
        )
        structured = (
            _stage25g3d_extract_structured_relation(
                text,
                field.get("structured_relation"),
            )
        )

        evidence_parts: list[str] = []
        if structured:
            evidence_parts.extend(
                [
                    "[STRUCTURED_TABLE_RELATION]",
                    structured,
                ]
            )
        if raw_evidence:
            evidence_parts.extend(
                [
                    "[RAW_EVIDENCE]",
                    raw_evidence,
                ]
            )

        field_ids.append(field_id)
        structured_evidence[field_id] = structured
        field_evidence[field_id] = "\n".join(
            evidence_parts
        ).strip()

        if "control_expected" in field:
            continue

        rule_id = str(
            field.get("rule_id") or ""
        ).strip()
        if not rule_id:
            return _stage25g3c_compact_diagnostic(
                "compact_batch_missing_rule_id",
                field_id,
            )
        if rule_id not in rule_records:
            return _stage25g3c_compact_diagnostic(
                "compact_batch_rule_not_found",
                rule_id,
            )

    schema = {
        "type": "object",
        "properties": {
            field_id: {"type": "boolean"}
            for field_id in field_ids
        },
        "required": list(field_ids),
        "additionalProperties": False,
    }

    prompt_lines = [
        str(
            config.get("prompt_intro")
            or (
                "각 field를 전용 evidence만 보고 "
                "독립적으로 판정한다."
            )
        ).strip(),
        "",
        "판정 기준:",
    ]

    for index, field in enumerate(fields, start=1):
        field_id = str(field["field_id"])
        prompt_lines.append(
            f"{index}. field_id={field_id}"
        )

        if "control_expected" not in field:
            rule_id = str(
                field.get("rule_id") or ""
            ).strip()
            record = rule_records[rule_id]
            prompt_lines.extend(
                [
                    f"   rule_id={rule_id}",
                    (
                        "   오류 조건="
                        + str(
                            record.get("wrong_claim")
                            or ""
                        ).strip()
                    ),
                    (
                        "   정답 기준="
                        + str(
                            record.get("correct_rule")
                            or ""
                        ).strip()
                    ),
                ]
            )

        prompt_lines.append(
            "   field criterion="
            + str(
                field.get("criterion") or ""
            ).strip()
        )

        relation_hint = str(
            field.get("relation_hint") or ""
        ).strip()
        if relation_hint:
            prompt_lines.append(
                f"   판정 보조={relation_hint}"
            )

        exclusion_hint = str(
            field.get("exclusion_hint") or ""
        ).strip()
        if exclusion_hint:
            prompt_lines.append(
                f"   제외 조건={exclusion_hint}"
            )

    notes = config.get("global_notes")
    if isinstance(notes, list) and notes:
        prompt_lines.extend(["", "중요:"])
        for note in notes:
            prompt_lines.append(
                "- " + str(note).strip()
            )

    prompt_lines.extend(
        ["", "Field-specific Evidence:"]
    )
    for field_id in field_ids:
        prompt_lines.extend(
            [
                f"[{field_id}]",
                field_evidence[field_id]
                or "(matching evidence 없음)",
                "",
            ]
        )

    prompt = "\n".join(prompt_lines).strip()

    try:
        response = _call_ollama_json(
            prompt,
            format_schema=schema,
        )
    except Exception as exc:
        return _stage25g3c_compact_diagnostic(
            "compact_batch_llm_call_failed",
            repr(exc),
        )

    if (
        not isinstance(response, dict)
        or set(response) != set(field_ids)
        or any(
            not isinstance(response.get(field_id), bool)
            for field_id in field_ids
        )
    ):
        return _stage25g3c_compact_diagnostic(
            "compact_batch_invalid_boolean_schema",
            json.dumps(
                response,
                ensure_ascii=False,
                default=str,
            )[:1200],
        )

    for field in fields:
        if "control_expected" not in field:
            continue

        field_id = str(field["field_id"])
        expected = field.get("control_expected")
        if not isinstance(expected, bool):
            return _stage25g3c_compact_diagnostic(
                "compact_batch_invalid_control_contract",
                field_id,
            )
        if response[field_id] is not expected:
            return _stage25g3c_compact_diagnostic(
                "compact_batch_control_mismatch",
                field_id,
            )

    effective_response = {
        field_id: response[field_id]
        for field_id in field_ids
    }
    arbitration: list[dict[str, Any]] = []

    for field in fields:
        if "control_expected" in field:
            continue

        field_id = str(field["field_id"])
        raw_value = response[field_id]
        evidence_present = bool(
            field_evidence.get(field_id)
        )
        structured_spec = field.get(
            "structured_relation"
        )
        authoritative_true = (
            isinstance(structured_spec, dict)
            and bool(
                structured_spec.get(
                    "authoritative_true"
                )
            )
            and bool(
                structured_evidence.get(field_id)
            )
        )

        if authoritative_true:
            effective_response[field_id] = True
            if raw_value is not True:
                arbitration.append(
                    {
                        "field_id": field_id,
                        "action": (
                            "structured_relation_"
                            "false_negative_override"
                        ),
                        "raw_value": raw_value,
                        "effective_value": True,
                    }
                )
            continue

        requires_evidence = bool(
            field.get(
                "require_nonempty_evidence_for_true",
                True,
            )
        )
        if (
            raw_value is True
            and requires_evidence
            and not evidence_present
        ):
            effective_response[field_id] = False
            arbitration.append(
                {
                    "field_id": field_id,
                    "action": (
                        "true_without_field_evidence_"
                        "suppressed"
                    ),
                    "raw_value": True,
                    "effective_value": False,
                }
            )

    findings: list[dict[str, Any]] = []

    for field in fields:
        field_id = str(field["field_id"])
        if "control_expected" in field:
            continue
        if effective_response[field_id] is not True:
            continue

        rule_id = str(
            field.get("rule_id") or ""
        ).strip()
        record = rule_records[rule_id]

        wrong_claim = str(
            record.get("wrong_claim") or ""
        ).strip()
        finding = {
            "id": rule_id,
            "severity": str(
                record.get("severity") or "fatal"
            ).strip().lower(),
            "message": (
                "오류 주장 탐지: " + wrong_claim
                if wrong_claim
                else rule_id
            ),
            "correct_rule": str(
                record.get("correct_rule") or ""
            ).strip(),
            "affected_layers": list(
                record.get("affected_layers") or ["C"]
            ),
            "evidence": field_evidence.get(
                field_id,
                "",
            ),
            "source": (
                "stage25g3d_compact_structured_"
                "evidence_arbitration"
            ),
        }

        ceiling = record.get("recommended_ceiling")
        if ceiling is not None:
            finding["recommended_ceiling"] = ceiling

        findings.append(finding)

    fatal_error_detected = any(
        str(finding.get("severity") or "").lower()
        == "fatal"
        for finding in findings
    )

    return {
        "mode": _mode_from_findings(findings),
        "fatal_error_detected": fatal_error_detected,
        "findings": findings,
        "diagnostics": [],
        "compact_batch_verification": {
            "status": "accepted",
            "llm_call_count": 1,
            "raw_field_values": {
                field_id: response[field_id]
                for field_id in field_ids
            },
            "field_values": {
                field_id: effective_response[field_id]
                for field_id in field_ids
            },
            "field_evidence_present": {
                field_id: bool(
                    field_evidence.get(field_id)
                )
                for field_id in field_ids
            },
            "structured_true_fields": [
                field_id
                for field_id in field_ids
                if bool(
                    structured_evidence.get(field_id)
                )
            ],
            "arbitration": arbitration,
            "diagnostic_only": bool(
                config.get("diagnostic_only", True)
            ),
        },
    }


def _evaluate_topic_fatal_checks_with_llm_stage19_contract(
    text: str,
    topic_check: dict[str, Any],
) -> list[dict[str, Any]]:
    from logic_llm_verifier import (
        _call_ollama_json,
    )

    fatal_checks = topic_check.get(
        "fatal_checks"
    )

    # STAGE34C_V4_PROFILE_FATAL_RULE_RECORD_BRIDGE_V1
    # Internal compact secondary replay attaches the active profile under
    # llm_profile. Profile fatal_conditions are source-owned strings, while
    # the stage19 evaluator accepts only dict rule records. Convert them with
    # the existing compact rule parser before eligible_checks filtering.
    if not isinstance(fatal_checks, list) or not fatal_checks:
        attached_profile = topic_check.get(
            "llm_profile"
        )
        profile_fatal_checks = (
            attached_profile.get(
                "fatal_conditions"
            )
            if isinstance(
                attached_profile,
                dict,
            )
            else None
        )
        if isinstance(
            profile_fatal_checks,
            list,
        ):
            bridged_fatal_checks = []
            for raw_profile_rule in (
                profile_fatal_checks
            ):
                rule_record = (
                    _stage25g3c_compact_rule_record(
                        raw_profile_rule
                    )
                )
                if rule_record is not None:
                    bridged_fatal_checks.append(
                        rule_record
                    )
            fatal_checks = bridged_fatal_checks

    if not isinstance(fatal_checks, list) or not fatal_checks:
        return []

    eligible_checks = [
        row
        for row in fatal_checks
        if isinstance(row, dict)
        and str(
            row.get("id")
            or row.get("rule_id")
            or ""
        ).strip()
    ]

    if not eligible_checks:
        return []

    canonical_axes = _build_canonical_axis_context(topic_check)

    rule_map = {
        str(
            check.get("id")
            or check.get("rule_id")
            or ""
        ).strip(): check
        for check in eligible_checks
    }
    rule_ids = list(rule_map)
    batch_size = len(rule_ids)
    compact_result = (
        _stage25g3c_compact_batch_secondary_once(
            text,
            eligible_checks,
            locals(),
        )
    )
    if compact_result is not None:
        return compact_result

    schema = _stage22_extend_batch_schema(
        _topic_fatal_batch_finding_schema(
            eligible_checks
        ),
        canonical_axes,
    )
    prompt = _stage22_extend_batch_prompt(
        _topic_fatal_batch_prompt(
            text,
            eligible_checks,
        ),
        canonical_axes,
    )

    diagnostics: list[dict[str, str]] = []
    normalized_answer = _normalize_text(
        text
    ).casefold()

    normalized_response: Any = None

    try:
        normalized_response = (
            _normalize_topic_fatal_semantic_response(
                _call_ollama_json(
                    prompt,
                    format_schema=schema,
                )
            )
        )
    except Exception as error:
        diagnostics.extend(
            {
                "rule_id": rule_id,
                "reason": "verifier_call_failed",
                "error": repr(error),
            }
            for rule_id in rule_ids
        )

    if not (
        isinstance(
            normalized_response,
            dict,
        )
        and isinstance(
            normalized_response.get(
                "findings"
            ),
            list,
        )
    ) and not diagnostics:
        repair_prompt = (
            "이전 응답은 필수 findings schema를 "
            "누락했다.\n"
            "새로운 rule id를 만들지 말고 아래 기존 "
            "rule들만 다시 판정하라.\n"
            "각 rule은 서로 독립적으로 판정한다.\n"
            "직접 위반한 답안 원문이 있을 때만 해당 "
            "rule_id의 findings 항목을 반환하고, "
            "아니면 빈 배열을 반환한다.\n"
            "한 rule_id당 항목은 최대 하나이다.\n"
            "evidence는 답안에서 직접 복사한다.\n\n"
            "허용 rule ids:\n"
            + json.dumps(
                rule_ids,
                ensure_ascii=False,
            )
            + "\n\n"
            + prompt
        )

        try:
            normalized_response = (
                _normalize_topic_fatal_semantic_response(
                    _call_ollama_json(
                        repair_prompt,
                        format_schema=schema,
                    )
                )
            )
        except Exception as error:
            diagnostics.extend(
                {
                    "rule_id": rule_id,
                    "reason": (
                        "schema_repair_call_failed"
                    ),
                    "error": repr(error),
                }
                for rule_id in rule_ids
            )

    if not (
        isinstance(
            normalized_response,
            dict,
        )
        and isinstance(
            normalized_response.get(
                "findings"
            ),
            list,
        )
    ) and not diagnostics:
        diagnostics.extend(
            {
                "rule_id": rule_id,
                "reason": "findings_field_missing",
                "error": (
                    "batch response did not "
                    "contain findings"
                ),
            }
            for rule_id in rule_ids
        )

    findings: list[dict[str, Any]] = []
    seen_rule_ids: set[str] = set()

    raw_findings = (
        normalized_response.get("findings")
        if isinstance(
            normalized_response,
            dict,
        )
        else []
    )

    if not isinstance(raw_findings, list):
        raw_findings = []

    for raw_finding in raw_findings:
        if not isinstance(
            raw_finding,
            dict,
        ):
            continue

        returned_rule_id = str(
            raw_finding.get("rule_id")
            or raw_finding.get(
                "source_rule_id"
            )
            or ""
        ).strip()

        if (
            returned_rule_id not in rule_map
            or returned_rule_id in seen_rule_ids
        ):
            diagnostics.append(
                {
                    "rule_id": returned_rule_id,
                    "reason": (
                        "unexpected_or_duplicate_rule_id"
                    ),
                    "error": returned_rule_id,
                }
            )
            continue

        seen_rule_ids.add(returned_rule_id)
        check = rule_map[returned_rule_id]

        severity = str(
            raw_finding.get("severity")
            or ""
        ).strip().lower()

        if severity not in {
            "major",
            "fatal",
        }:
            continue

        confidence_raw = raw_finding.get(
            "confidence"
        )

        try:
            confidence = float(
                confidence_raw
            )
        except (
            TypeError,
            ValueError,
        ):
            confidence = 0.0

        if confidence < 0.80:
            diagnostics.append(
                {
                    "rule_id": returned_rule_id,
                    "reason": (
                        "confidence_below_threshold"
                    ),
                    "error": str(
                        confidence_raw
                    ),
                }
            )
            continue

        evidence = str(
            raw_finding.get("evidence")
            or ""
        ).strip()
        normalized_evidence = _normalize_text(
            evidence
        ).casefold()

        if (
            not normalized_evidence
            or normalized_evidence
            not in normalized_answer
        ):
            diagnostics.append(
                {
                    "rule_id": returned_rule_id,
                    "reason": (
                        "evidence_not_in_answer"
                    ),
                    "error": evidence[:240],
                }
            )
            continue

        if _semantic_evidence_is_corrective_context(
            text,
            evidence,
        ):
            diagnostics.append(
                {
                    "rule_id": returned_rule_id,
                    "reason": (
                        "corrective_context_excluded"
                    ),
                    "error": evidence[:240],
                }
            )
            continue

        compatibility_single_rule = (
            batch_size == 1
        )
        finding = {
            "id": (
                "llm_semantic_"
                + returned_rule_id
            ),
            "source_rule_id": (
                returned_rule_id
            ),
            "severity": severity,
            "message": str(
                check.get("message")
                or check.get("condition")
                or "핵심 이론 오류"
            ).strip(),
            "correct_rule": str(
                check.get("correct_rule")
                or ""
            ).strip(),
            "affected_layers": (
                check.get(
                    "affected_layers"
                )
                or ["C"]
            ),
            "evidence": evidence,
            "engine": (
                "topic_fatal_semantic_"
                "llm_per_rule_v1"
                if compatibility_single_rule
                else
                "topic_fatal_semantic_"
                "llm_batch_v1"
            ),
            "confidence": confidence,
            "semantic_rule_evaluation": {
                "mode": (
                    "single_rule"
                    if compatibility_single_rule
                    else "batch"
                ),
                "batch_size": batch_size,
                "schema_kind": (
                    "findings_only"
                ),
                "rule_source": (
                    "existing_topic_fatal_checks"
                ),
                "new_rule_owner_created": False,
                "primary_call_count": 1,
                "max_repair_call_count": 1,
            },
        }

        ceiling = check.get(
            "recommended_ceiling"
        )

        if isinstance(
            ceiling,
            (int, float),
        ) and not isinstance(
            ceiling,
            bool,
        ):
            finding[
                "recommended_ceiling"
            ] = float(ceiling)

        _copy_optional_fatal_rule_metadata(
            finding,
            check,
        )
        findings.append(finding)

    axis_evaluation = _normalize_canonical_axis_alignment_response(
        normalized_response,
        canonical_axes=canonical_axes,
        answer_text=text,
    )
    topic_check["_stage22_axis_alignment_evaluation"] = axis_evaluation
    existing_signatures = {
        str(finding.get("claim_signature") or "").strip()
        for finding in findings
        if isinstance(finding, dict)
    }
    for axis_finding in _canonical_axis_alignment_to_findings(
        axis_evaluation
    ):
        signature = str(
            axis_finding.get("claim_signature") or ""
        ).strip()
        if signature and signature in existing_signatures:
            continue
        findings.append(axis_finding)
        if signature:
            existing_signatures.add(signature)

    diagnostics = [
        diagnostic
        for diagnostic in diagnostics
        if str(
            diagnostic.get("reason") or ""
        ) != "corrective_context_excluded"
    ]

    if diagnostics:
        diagnostic_reasons = {
            row.get("reason")
            for row in diagnostics
            if isinstance(row, dict)
        }
        diagnostic_reason = (
            "findings_field_missing"
            if diagnostic_reasons
            == {"findings_field_missing"}
            else (
                "per_rule_evaluation_partial"
                if batch_size == 1
                else "batch_evaluation_partial"
            )
        )

        findings.append(
            {
                "id": (
                    "topic_fatal_semantic_"
                    "llm_error"
                ),
                "severity": "minor",
                "message": (
                    "일부 기존 fatal rule의 "
                    "batch semantic 검증이 "
                    "fail-open 처리되었습니다."
                ),
                "correct_rule": (
                    "semantic verifier 실패 또는 "
                    "불충분한 evidence에는 fatal "
                    "판정을 적용하지 않습니다."
                ),
                "affected_layers": ["C"],
                "engine": (
                    "topic_fatal_semantic_"
                    "llm_batch_v1"
                    if batch_size > 1
                    else
                    "topic_fatal_semantic_"
                    "llm_per_rule_v1"
                ),
                "diagnostic": {
                    "ok": False,
                    "reason": diagnostic_reason,
                    "rule_failure_count": len(
                        diagnostics
                    ),
                    "details": diagnostics,
                    "batch_size": batch_size,
                    "primary_call_count": 1,
                    "max_repair_call_count": 1,
                },
            }
        )

    return findings


def _evaluate_topic_fatal_checks_with_llm(
    text: str,
    topic_check: dict[str, Any],
) -> list[dict[str, Any]]:
    try:
        import logic_llm_verifier as verifier_module
    except Exception:
        return _evaluate_topic_fatal_checks_with_llm_legacy_contract(
            text,
            topic_check,
        )

    stage19_capable = (
        callable(
            getattr(
                verifier_module,
                "verify_logic_with_llm",
                None,
            )
        )
        and callable(
            getattr(
                verifier_module,
                "_call_ollama_json",
                None,
            )
        )
    )

    if stage19_capable:
        return _evaluate_topic_fatal_checks_with_llm_stage19_contract(
            text,
            topic_check,
        )

    return _evaluate_topic_fatal_checks_with_llm_legacy_contract(
        text,
        topic_check,
    )
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
