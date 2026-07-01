from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Claim:
    slot: str
    value: str
    evidence: str
    claim_type: str = "definition"


def normalize_text(text: str) -> str:
    value = str(text or "")

    # Preserve LaTeX fractions before stripping braces/slashes.
    value = re.sub(
        r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}",
        r"\1/\2",
        value,
    )

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
        ("ω_d", "ωd"),
        ("ω_n", "ωn"),
        ("zeta", "ζ"),
        ("Zeta", "ζ"),
        ("sigma", "σ"),
        ("theta", "θ"),
        ("≤", "<="),
        ("≥", ">="),
        ("^2", "²"),
    ]

    for old, new in replacements:
        value = value.replace(old, new)

    value = value.replace("{", "").replace("}", "")
    value = value.replace("\\", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalized_lines(text: str) -> list[str]:
    return [
        normalize_text(line)
        for line in str(text or "").splitlines()
        if normalize_text(line)
    ]


REGION_LABELS = {
    "undamped": [
        r"무\s*감쇠",
        r"un[-\s]*damped",
        r"undamped",
    ],
    "underdamped": [
        r"부족\s*감쇠",
        r"under[-\s]*damped",
        r"under\s*damp",
    ],
    "critical": [
        r"임계\s*감쇠",
        r"critically[-\s]*damped",
        r"critical\s*damp",
    ],
    "overdamped": [
        r"과\s*감쇠",
        r"over[-\s]*damped",
        r"over\s*damp",
    ],
    "unstable": [
        r"불안정",
        r"unstable",
    ],
}


def _label_regex(region: str) -> str:
    return r"(?:" + "|".join(REGION_LABELS[region]) + r")"


def _detect_region_label(text: str) -> str | None:
    for region, patterns in REGION_LABELS.items():
        for pat in patterns:
            if re.search(pat, text, flags=re.IGNORECASE):
                return region
    return None


def _range_value(raw: str) -> str | None:
    t = normalize_text(raw)
    t = t.replace(" ", "")

    # Keep the order from specific to broad.
    if re.search(r"0<ζ<1", t):
        return "0<zeta<1"
    if re.search(r"0\.70?7?<=ζ<1", t) or re.search(r"0\.70?7?≤ζ<1", t):
        return "0.7<=zeta<1"
    if re.search(r"ζ<0\.70?7?", t):
        return "zeta<0.7"
    if re.search(r"ζ=0\.70?7?", t) or re.search(r"0\.70?7?", t) and "ζ" in t and "=" in t:
        return "zeta==0.7"
    if re.search(r"ζ=1", t):
        return "zeta==1"
    if re.search(r"ζ>1", t):
        return "zeta>1"
    if re.search(r"ζ=0", t):
        return "zeta==0"
    if re.search(r"ζ<0", t):
        return "zeta<0"

    return None


def _split_table_cells(line: str) -> list[str]:
    if "|" not in line:
        return []
    cells = [normalize_text(c).strip() for c in line.strip().strip("|").split("|")]
    return [c for c in cells if c and not re.fullmatch(r"[-:\s]+", c)]


def _extract_table_region_claims(lines: list[str]) -> list[Claim]:
    claims: list[Claim] = []

    table_rows = [_split_table_cells(line) for line in lines if "|" in line]
    table_rows = [row for row in table_rows if row]

    for i, row in enumerate(table_rows):
        regions_by_index: dict[int, str] = {}
        for idx, cell in enumerate(row):
            region = _detect_region_label(cell)
            if region in {"undamped", "underdamped", "critical", "overdamped", "unstable"}:
                regions_by_index[idx] = region

        if not regions_by_index:
            continue

        # Search nearby rows for a zeta/range row.
        for nearby in table_rows[i + 1 : i + 4]:
            if not any("ζ" in cell or "zeta" in cell.lower() for cell in nearby):
                continue

            for idx, region in regions_by_index.items():
                if idx >= len(nearby):
                    continue
                value = _range_value(nearby[idx])
                if value:
                    claims.append(
                        Claim(
                            slot=f"{region}.zeta_range",
                            value=value,
                            evidence=f"{row[idx]} | {nearby[idx]}",
                            claim_type="definition",
                        )
                    )
            break

    return claims


def _extract_compact_header_region_claims(lines: list[str]) -> list[Claim]:
    claims: list[Claim] = []

    for i, line in enumerate(lines[:-1]):
        labels: list[tuple[int, str]] = []
        for region in ["undamped", "underdamped", "critical", "overdamped", "unstable"]:
            m = re.search(_label_regex(region), line, flags=re.IGNORECASE)
            if m:
                labels.append((m.start(), region))

        if len(labels) < 2:
            continue

        labels = sorted(labels)
        next_line = lines[i + 1]
        ranges = []
        for m in re.finditer(
            r"(?:0\s*<\s*ζ\s*<\s*1|0\.70?7?\s*<=\s*ζ\s*<\s*1|ζ\s*<\s*0\.70?7?|ζ\s*=\s*0\.70?7?|ζ\s*=\s*1|ζ\s*>\s*1|ζ\s*=\s*0|ζ\s*<\s*0)",
            next_line,
            flags=re.IGNORECASE,
        ):
            ranges.append((m.start(), m.group(0)))

        if len(ranges) < len(labels):
            continue

        # Pair by order. This catches compact text/table summaries:
        # "Under damp Critical damp over damp"
        # "ζ < 0.7 ζ = 0.7 0.7 <= ζ < 1"
        for (_, region), (_, raw_range) in zip(labels, ranges):
            value = _range_value(raw_range)
            if value:
                claims.append(
                    Claim(
                        slot=f"{region}.zeta_range",
                        value=value,
                        evidence=f"{line} / {next_line}",
                        claim_type="definition",
                    )
                )

    return claims


def _range_matches(text: str) -> list[tuple[int, str, str]]:
    patterns = [
        r"0\s*<\s*ζ\s*<\s*1",
        r"0\.70?7?\s*<=\s*ζ\s*<\s*1",
        r"ζ\s*<\s*0\.70?7?",
        r"ζ\s*=\s*0\.70?7?",
        r"ζ\s*=\s*1",
        r"ζ\s*>\s*1",
        r"ζ\s*=\s*0",
        r"ζ\s*<\s*0",
    ]

    matches: list[tuple[int, str, str]] = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            value = _range_value(m.group(0))
            if value:
                matches.append((m.start(), m.group(0), value))

    matches.sort(key=lambda x: x[0])
    return matches


def _region_matches(text: str) -> list[tuple[int, str, str]]:
    matches: list[tuple[int, str, str]] = []

    for region in ["undamped", "underdamped", "critical", "overdamped", "unstable"]:
        for pat in REGION_LABELS[region]:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                matches.append((m.start(), m.group(0), region))

    matches.sort(key=lambda x: x[0])
    return matches


def _split_claim_segments(line: str) -> list[str]:
    """
    Split only at claim-level separators. Do not split on '.' because decimals
    such as 0.707 are common in this topic.
    """
    normalized = normalize_text(line)

    # Markdown/table rows are handled elsewhere.
    normalized = normalized.replace("|", ",")

    raw_segments = re.split(r"[,，;；]|(?:\s*/\s*)", normalized)
    segments = [seg.strip() for seg in raw_segments if seg.strip()]
    return segments or [normalized]


def _segment_to_region_claim(segment: str) -> Claim | None:
    ranges = _range_matches(segment)
    regions = _region_matches(segment)

    if len(ranges) != 1 or len(regions) != 1:
        return None

    _, raw_range, value = ranges[0]
    _, raw_region, region = regions[0]

    return Claim(
        slot=f"{region}.zeta_range",
        value=value,
        evidence=segment,
        claim_type="definition",
    )


def _extract_sentence_region_claims(lines: list[str]) -> list[Claim]:
    """
    Extract definition claims from local clauses only.

    This intentionally avoids broad patterns like:
        range .{0,80} label
    because a correct compact sentence can contain multiple definitions:
        ζ=0은 무감쇠, 0<ζ<1은 부족감쇠, ζ=1은 임계감쇠, ζ>1은 과감쇠
    Broad window matching would incorrectly pair ζ=0 with 임계감쇠.
    """
    claims: list[Claim] = []

    for line in lines:
        for segment in _split_claim_segments(line):
            claim = _segment_to_region_claim(segment)
            if claim is not None:
                claims.append(claim)

    return claims


def extract_zeta_region_claims(text: str) -> list[Claim]:
    lines = normalized_lines(text)
    claims: list[Claim] = []

    claims.extend(_extract_table_region_claims(lines))
    claims.extend(_extract_compact_header_region_claims(lines))
    claims.extend(_extract_sentence_region_claims(lines))

    # De-duplicate while preserving evidence diversity.
    seen: set[tuple[str, str, str]] = set()
    unique: list[Claim] = []
    for claim in claims:
        key = (claim.slot, claim.value, claim.evidence)
        if key in seen:
            continue
        seen.add(key)
        unique.append(claim)

    return unique


def extract_step_response_claim_findings(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lines = normalized_lines(text)

    critical = _label_regex("critical")
    over = _label_regex("overdamped")

    # Fatal only for explicit wrong assignments in the same row/clause.
    critical_wrong = re.compile(
        critical
        + r"\s*(?:[:|\-]|은|는)?\s*.{0,35}"
        + r"(진동\s*있|진동\s*발생|진동\s*함|오버\s*슈트\s*있|오버\s*슈트\s*발생|overshot|overshoot\s*exists|충돌\s*위험)",
        flags=re.IGNORECASE,
    )

    over_wrong = re.compile(
        over
        + r"\s*(?:[:|\-]|은|는)?\s*.{0,35}"
        + r"(오버\s*슈트\s*있|오버\s*슈트\s*발생|overshot|overshoot\s*exists|충돌\s*위험|빠른\s*제어|최속)",
        flags=re.IGNORECASE,
    )

    for line in lines:
        if critical_wrong.search(line):
            findings.append(
                {
                    "id": "claim_critical_step_response_conflict",
                    "severity": "fatal",
                    "message": "임계감쇠 응답을 진동 또는 오버슈트 응답으로 명시하여 표준 응답 특성과 충돌한다.",
                    "correct_rule": "임계감쇠는 오버슈트와 진동 없이 가장 빠르게 수렴하는 응답이다.",
                    "affected_layers": ["C"],
                    "recommended_ceiling": 10.0,
                    "evidence": line,
                }
            )

        if over_wrong.search(line):
            findings.append(
                {
                    "id": "claim_overdamped_step_response_conflict",
                    "severity": "fatal",
                    "message": "과감쇠 응답을 오버슈트, 충돌 위험 또는 최속 응답으로 명시하여 표준 응답 특성과 충돌한다.",
                    "correct_rule": "과감쇠는 오버슈트 없이 느리게 수렴하는 응답이다.",
                    "affected_layers": ["C"],
                    "recommended_ceiling": 10.0,
                    "evidence": line,
                }
            )

    return findings


def extract_angle_claim_findings(text: str) -> list[dict[str, Any]]:
    n = normalize_text(text)

    # Direct contradiction:
    # If theta is explicitly defined from the negative real axis, zeta must be cos(theta).
    if re.search(
        r"(음의\s*실수축|negative\s*real\s*axis|실수축).{0,180}sin\s*θ\s*=.{0,100}(σ\s*/\s*ωn|ζ)",
        n,
        flags=re.IGNORECASE,
    ):
        return [
            {
                "id": "claim_angle_reference_conflict",
                "severity": "fatal",
                "message": "θ를 음의 실수축 기준 각도로 정의한 뒤 sinθ=σ/ωn=ζ로 표현하여 기하학적 관계가 충돌한다.",
                "correct_rule": "θ를 음의 실수축 기준으로 정의하면 ζ=cosθ이다. sinθ 관계는 허수축 기준 각도일 때 사용해야 한다.",
                "affected_layers": ["C", "E"],
                "recommended_ceiling": 10.0,
                "evidence": n[:260],
            }
        ]

    return []


EXPECTED = {
    "undamped.zeta_range": {"zeta==0"},
    "underdamped.zeta_range": {"0<zeta<1"},
    "critical.zeta_range": {"zeta==1"},
    "overdamped.zeta_range": {"zeta>1"},
    "unstable.zeta_range": {"zeta<0"},
}


FATAL_MESSAGES = {
    "underdamped.zeta_range": (
        "부족감쇠 영역을 표준 정의와 다르게 명시했다.",
        "부족감쇠는 0<ζ<1 전체 영역이다.",
    ),
    "critical.zeta_range": (
        "임계감쇠의 ζ 범위를 표준 정의와 다르게 명시했다.",
        "임계감쇠는 ζ=1이다.",
    ),
    "overdamped.zeta_range": (
        "과감쇠의 ζ 범위를 표준 정의와 다르게 명시했다.",
        "과감쇠는 ζ>1이다.",
    ),
    "undamped.zeta_range": (
        "무감쇠의 ζ 범위를 표준 정의와 다르게 명시했다.",
        "무감쇠는 ζ=0이다.",
    ),
}


def compare_zeta_claims(claims: list[Claim]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for claim in claims:
        expected = EXPECTED.get(claim.slot)
        if not expected:
            continue

        if claim.value in expected:
            continue

        # Unstable can be described as zeta < 0 or RHP pole; don't over-penalize partial forms.
        if claim.slot == "unstable.zeta_range":
            continue

        msg, correct_rule = FATAL_MESSAGES.get(
            claim.slot,
            ("감쇠비 구간 정의가 표준 정의와 충돌한다.", "표준 감쇠비 구간 정의를 따르세요."),
        )

        findings.append(
            {
                "id": f"claim_{claim.slot.replace('.', '_')}_conflict",
                "severity": "fatal",
                "message": msg,
                "correct_rule": correct_rule,
                "affected_layers": ["C"],
                "recommended_ceiling": 10.0,
                "evidence": claim.evidence,
                "claim": asdict(claim),
            }
        )

    return findings


def evaluate_second_order_claims(text: str) -> dict[str, Any]:
    claims = extract_zeta_region_claims(text)
    findings: list[dict[str, Any]] = []

    findings.extend(compare_zeta_claims(claims))
    findings.extend(extract_step_response_claim_findings(text))
    findings.extend(extract_angle_claim_findings(text))

    # De-duplicate findings by id + evidence.
    seen: set[tuple[str, str]] = set()
    unique_findings: list[dict[str, Any]] = []
    for finding in findings:
        key = (str(finding.get("id")), str(finding.get("evidence", "")))
        if key in seen:
            continue
        seen.add(key)
        unique_findings.append(finding)

    fatal = any(f.get("severity") == "fatal" for f in unique_findings)
    recommended_ceiling = 10.0 if fatal else None

    return {
        "applicable": True,
        "engine": "claim_schema_v1",
        "claims": [asdict(c) for c in claims],
        "findings": unique_findings,
        "fatal_error_detected": fatal,
        "recommended_ceiling": recommended_ceiling,
        "mode": "fatal" if fatal else "pass",
    }
