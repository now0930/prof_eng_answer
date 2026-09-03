from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from pathlib import Path
from rubric_bank_paths import resolve_rubric_bank_path
from typing import Any
import math


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_PROFILE_PATH = resolve_rubric_bank_path("logic_check_profiles")
# LOGIC_CHECK_PROFILE_PATH remains a manual override; otherwise follow RUBRIC_BANK_MODE.

LOGIC_CHECK_PROFILE_PATH = Path(
    os.getenv("LOGIC_CHECK_PROFILE_PATH", str(DEFAULT_PROFILE_PATH))
)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip("/")
LOGIC_LLM_MODEL = os.getenv(
    "LOGIC_LLM_VERIFIER_MODEL",
    os.getenv("OLLAMA_MODEL", "gemma4:e4b"),
)
LOGIC_LLM_TIMEOUT = int(os.getenv("LOGIC_LLM_VERIFIER_TIMEOUT", "90"))
# STAGE22E21S14_ENV_BACKED_NUM_CTX_V1
LOGIC_LLM_NUM_CTX = int(os.getenv('LOGIC_LLM_VERIFIER_NUM_CTX', '8192'))
OLLAMA_ENDPOINT_PROBE_TIMEOUT = float(
    os.getenv(
        "LOGIC_LLM_ENDPOINT_PROBE_TIMEOUT",
        "1.5",
    )
)
OLLAMA_ENDPOINT_RETRY_SECONDS = float(
    os.getenv(
        "LOGIC_LLM_ENDPOINT_RETRY_SECONDS",
        "15",
    )
)

_OLLAMA_SELECTED_BASE_URL: str | None = None
_OLLAMA_LAST_SELECTION_ATTEMPT = 0.0


def _ollama_url_candidates() -> list[str]:
    urls: list[str] = []

    env_url = os.getenv("OLLAMA_URL")
    if env_url:
        urls.append(env_url.rstrip("/"))

    urls.extend(
        [
            OLLAMA_URL,
            "http://localhost:11434",
            "http://127.0.0.1:11434",
            "http://ollama:11434"
        ]
    )

    deduped: list[str] = []
    for url in urls:
        url = str(url or "").rstrip("/")
        if url and url not in deduped:
            deduped.append(url)

    return deduped


def _probe_ollama_endpoint(
    base_url: str,
) -> bool:
    request = urllib.request.Request(
        base_url.rstrip("/") + "/api/tags",
        method="GET",
    )

    with urllib.request.urlopen(
        request,
        timeout=OLLAMA_ENDPOINT_PROBE_TIMEOUT,
    ) as response:
        status = int(
            getattr(response, "status", 200)
            or 200
        )
        response.read(1)

    return 200 <= status < 300


def _select_ollama_base_url() -> str | None:
    global _OLLAMA_LAST_SELECTION_ATTEMPT
    global _OLLAMA_SELECTED_BASE_URL

    if _OLLAMA_SELECTED_BASE_URL:
        return _OLLAMA_SELECTED_BASE_URL

    now = time.monotonic()

    if (
        _OLLAMA_LAST_SELECTION_ATTEMPT > 0.0
        and now - _OLLAMA_LAST_SELECTION_ATTEMPT
        < max(0.0, OLLAMA_ENDPOINT_RETRY_SECONDS)
    ):
        return None

    _OLLAMA_LAST_SELECTION_ATTEMPT = now

    for base_url in _ollama_url_candidates():
        try:
            if _probe_ollama_endpoint(base_url):
                _OLLAMA_SELECTED_BASE_URL = base_url
                return base_url
        except Exception:
            continue

    return None


def _ordered_ollama_url_candidates() -> list[str]:
    candidates = _ollama_url_candidates()
    selected = _select_ollama_base_url()

    if selected and selected in candidates:
        return [
            selected,
            *[
                candidate
                for candidate in candidates
                if candidate != selected
            ],
        ]

    return candidates


def _remember_ollama_base_url(
    base_url: str,
) -> None:
    global _OLLAMA_SELECTED_BASE_URL

    normalized = str(base_url or "").rstrip("/")

    if normalized:
        _OLLAMA_SELECTED_BASE_URL = normalized


def _forget_ollama_base_url(
    base_url: str,
) -> None:
    global _OLLAMA_SELECTED_BASE_URL

    normalized = str(base_url or "").rstrip("/")

    if _OLLAMA_SELECTED_BASE_URL == normalized:
        _OLLAMA_SELECTED_BASE_URL = None


def _reset_ollama_endpoint_selection_for_tests() -> None:
    global _OLLAMA_LAST_SELECTION_ATTEMPT
    global _OLLAMA_SELECTED_BASE_URL

    _OLLAMA_SELECTED_BASE_URL = None
    _OLLAMA_LAST_SELECTION_ATTEMPT = 0.0


def _normalize_text(text: str) -> str:
    value = str(text or "")

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


def _lines(text: str) -> list[str]:
    return [
        _normalize_text(line)
        for line in str(text or "").splitlines()
        if _normalize_text(line)
    ]


def _candidate_text(items: list[str]) -> str:
    return " ".join(x for x in items if x).strip()


def _load_profile_bank() -> dict[str, Any]:
    if not LOGIC_CHECK_PROFILE_PATH.exists():
        raise FileNotFoundError(f"logic check profile not found: {LOGIC_CHECK_PROFILE_PATH}")

    with LOGIC_CHECK_PROFILE_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("logic check profile root must be object")

    return data


def load_logic_check_profile(topic_id: str) -> dict[str, Any]:
    bank = _load_profile_bank()
    profiles = bank.get("profiles") or []

    for profile in profiles:
        if isinstance(profile, dict) and profile.get("topic_id") == topic_id:
            return profile

    raise KeyError(f"logic check profile not found for topic_id={topic_id}")


def _compile(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, flags=re.IGNORECASE)


def _normalize_label(label: str, label_map: dict[str, str]) -> str:
    raw = str(label or "")
    lower = raw.lower()

    for key, normalized in label_map.items():
        if str(key).lower() in lower or str(key) in raw:
            return str(normalized)

    return raw


def _structured_mapping_candidate(lines: list[str], rule: dict[str, Any]) -> str | None:
    label_regex = _compile(str(rule.get("label_regex") or ""))
    range_regex = _compile(str(rule.get("range_regex") or ""))
    label_map = rule.get("label_map") or {}

    for i, line in enumerate(lines[:-1]):
        labels = [
            _normalize_label(m.group(0), label_map)
            for m in label_regex.finditer(line)
        ]

        if len(labels) < 2:
            continue

        nearby = " ".join(lines[i + 1 : i + 3])
        ranges = [m.group(0) for m in range_regex.finditer(nearby)]

        if len(ranges) < len(labels):
            continue

        pairs = [f"{label} => {rng}" for label, rng in zip(labels, ranges)]
        return " | ".join(pairs)

    collapsed = " ".join(lines)
    labels = [
        _normalize_label(m.group(0), label_map)
        for m in label_regex.finditer(collapsed)
    ]
    ranges = [m.group(0) for m in range_regex.finditer(collapsed)]

    if len(labels) >= 2 and len(ranges) >= len(labels):
        pairs = [f"{label} => {rng}" for label, rng in zip(labels[: len(ranges)], ranges)]
        return " | ".join(pairs)

    return None


def extract_logic_evidence_candidates(
    answer_text: str,
    profile: dict[str, Any],
) -> list[dict[str, str]]:
    extraction = profile.get("candidate_extraction") or {}
    max_candidates = int(extraction.get("max_candidates") or 12)
    nearby_window = int(extraction.get("nearby_window") or 1)
    rules = extraction.get("rules") or []
    key_terms = extraction.get("key_terms") or []

    lines = _lines(answer_text)
    candidates: list[dict[str, str]] = []

    def add(kind: str, text: str) -> None:
        text = _normalize_text(text)
        if not text:
            return
        if len(text) > 900:
            text = text[:900]
        if any(
            candidate["text"] == text
            and candidate["kind"] == kind
            for candidate in candidates
        ):
            return
        candidates.append(
            {
                "id": f"C{len(candidates) + 1}",
                "kind": kind,
                "text": text,
            }
        )

    # Preserve table semantics before nearby-line extraction flattens them.
    # This is topic-neutral: headers are bound to each row's cells and the
    # verifier still decides whether the resulting relationship is correct.
    normalized_key_terms = [
        _normalize_text(str(term)).casefold()
        for term in key_terms
        if _normalize_text(str(term))
    ]

    def table_cells(line: str) -> list[str]:
        stripped = str(line or "").strip()
        if stripped.count("|") < 2:
            return []
        return [cell.strip() for cell in stripped.strip("|").split("|")]

    raw_lines = str(answer_text or "").splitlines()
    table_header_hints = (
        "구분", "항목", "단계", "대상", "도구", "방법", "요소",
        "기준", "특성", "내용", "조건", "결과",
    )
    for index in range(len(raw_lines) - 2):
        headers = table_cells(raw_lines[index])
        following = table_cells(raw_lines[index + 1])
        if not headers or len(following) != len(headers):
            continue
        has_separator = all(
            re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))
            for cell in following
        )
        if not has_separator:
            normalized_headers = [_normalize_text(cell).casefold() for cell in headers]
            if not any(
                hint.casefold() in header
                for header in normalized_headers
                for hint in table_header_hints
            ):
                continue
        data_start = index + 2 if has_separator else index + 1
        for row_line in raw_lines[data_start:]:
            cells = table_cells(row_line)
            if len(cells) != len(headers):
                break
            rendered = " | ".join(
                f"{header}={cell}"
                for header, cell in zip(headers, cells)
                if header and cell
            )
            normalized_rendered = _normalize_text(rendered).casefold()
            if normalized_key_terms and not any(
                term in normalized_rendered for term in normalized_key_terms
            ):
                continue
            add("structured_table_relation", rendered)

    for rule in rules:
        if not isinstance(rule, dict):
            continue

        kind = str(rule.get("kind") or "candidate")
        rule_type = str(rule.get("type") or "")

        if rule_type == "structured_mapping":
            structured = _structured_mapping_candidate(
                lines,
                rule,
            )
            if structured:
                add(kind, structured)
            continue

        pattern = str(rule.get("regex") or "")
        if not pattern:
            continue

        regex = _compile(pattern)

        if rule_type == "line_regex":
            for line in lines:
                if regex.search(line):
                    add(kind, line)
            continue

        if rule_type == "nearby_regex":
            for index, line in enumerate(lines):
                if regex.search(line):
                    start = max(
                        0,
                        index - nearby_window,
                    )
                    end = min(
                        len(lines),
                        index + nearby_window + 1,
                    )
                    add(
                        kind,
                        _candidate_text(
                            lines[start:end]
                        ),
                    )
            continue

    # LLM-only profiles intentionally keep rules empty so that
    # deterministic regexes do not decide whether a claim is wrong.
    # In that configuration, key terms only select nearby evidence;
    # the LLM still performs the semantic verdict.
    if not candidates and not rules and key_terms:
        normalized_terms: list[str] = []

        for term in key_terms:
            normalized = _normalize_text(
                str(term)
            ).casefold()

            if (
                normalized
                and normalized
                not in normalized_terms
            ):
                normalized_terms.append(
                    normalized
                )

        for index, line in enumerate(lines):
            normalized_line = _normalize_text(
                line
            ).casefold()

            if not any(
                term in normalized_line
                for term in normalized_terms
            ):
                continue

            start = max(
                0,
                index - nearby_window,
            )
            end = min(
                len(lines),
                index + nearby_window + 1,
            )

            add(
                "key_term_context",
                _candidate_text(
                    lines[start:end]
                ),
            )

        # A matched expression may span line boundaries.
        if not candidates:
            collapsed = _candidate_text(lines)
            normalized_collapsed = _normalize_text(
                collapsed
            ).casefold()

            if any(
                term in normalized_collapsed
                for term in normalized_terms
            ):
                add(
                    "key_term_context",
                    collapsed,
                )

    return candidates[:max_candidates]


def extract_second_order_evidence_candidates(
    answer_text: str,
    max_candidates: int | None = None,
) -> list[dict[str, str]]:
    profile = load_logic_check_profile("second_order_lag_response_by_damping_ratio")

    if max_candidates is not None:
        profile = dict(profile)
        extraction = dict(profile.get("candidate_extraction") or {})
        extraction["max_candidates"] = max_candidates
        profile["candidate_extraction"] = extraction

    return extract_logic_evidence_candidates(answer_text, profile)



def _repair_single_missing_top_level_object_brace(text: str) -> dict[str, Any] | None:
    # Repair only one missing top-level JSON object closing brace.
    # This fallback is fail-closed and inserts no other token.
    if not text:
        return None

    stack: list[str] = []
    in_string = False
    escape = False
    matching_open = {"}": "{", "]": "["}

    for character in text:
        if in_string:
            if escape:
                escape = False
            elif character == "\\":
                escape = True
            elif character == '"':
                in_string = False
            continue

        if character == '"':
            in_string = True
        elif character in ("{", "["):
            stack.append(character)
        elif character in ("}", "]"):
            expected = matching_open[character]
            if not stack or stack[-1] != expected:
                return None
            stack.pop()

    if in_string or escape or stack != ["{"]:
        return None

    try:
        parsed = json.loads(text + "}")
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _extract_json_object(text: str) -> dict[str, Any] | None:
    if not text:
        return None

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:
        return _repair_single_missing_top_level_object_brace(cleaned)

    try:
        return json.loads(cleaned[start : end + 1])
    except Exception:
        return _repair_single_missing_top_level_object_brace(cleaned)


def _call_ollama_json(
    prompt: str,
    *,
    format_schema: dict[str, Any] | str | None = None,
) -> dict[str, Any] | None:
    payload = {
        "model": LOGIC_LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict technical answer verification engine. "
                    "Return JSON only. Do not add markdown. "
                    "Do not infer contradictions unless candidate evidence explicitly states them."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
        "options": {'temperature': 0, 'top_p': 0.1, 'num_ctx': LOGIC_LLM_NUM_CTX},
    }

    # STAGE19F_OLLAMA_STRUCTURED_OUTPUT_ENFORCEMENT_V1
    if format_schema is not None:
        payload["format"] = format_schema

    errors: list[str] = []

    for base_url in _ordered_ollama_url_candidates():
        req = urllib.request.Request(
            base_url.rstrip("/") + "/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=LOGIC_LLM_TIMEOUT) as resp:
                raw = resp.read().decode("utf-8", errors="replace")

            data = json.loads(raw)
            content = (data.get("message") or {}).get("content") or data.get("response") or ""
            parsed = _extract_json_object(content)

            if parsed is not None:
                _remember_ollama_base_url(
                    base_url
                )
                return parsed

            errors.append(f"{base_url}: JSON parse failed")
        except Exception as exc:
            _forget_ollama_base_url(
                base_url
            )
            errors.append(f"{base_url}: {exc!r}")

    raise RuntimeError("all Ollama endpoints failed: " + " | ".join(errors))

def _numbered(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


# STAGE22E3_PROFILE_CANONICAL_AXIS_BRIDGE_V1
# STAGE22E21S36_GLOBAL_FALLBACK_PROMPT_CLAIMS_ARRAY_V1
def _compact_prompt_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    compact_candidates: list[dict[str, Any]] = []

    for candidate in candidates:
        compact_candidate: dict[str, Any] = {
            "id": candidate.get("id"),
            "kind": candidate.get("kind"),
        }
        text = str(candidate.get("text") or "")

        if compact_candidate["kind"] == "global_answer_context":
            compact_candidate["claims"] = _lines(text)
        else:
            compact_candidate["text"] = text

        compact_candidates.append(compact_candidate)

    return compact_candidates


def _build_logic_prompt(
    profile: dict[str, Any],
    candidates: list[dict[str, str]],
    canonical_axes: list[dict[str, Any]] | None = None,
) -> str:
    display_name = profile.get("display_name") or profile.get("topic_id")
    truth_schema = profile.get("truth_schema") or []
    fatal_conditions = profile.get("fatal_conditions") or []
    safe_conditions = profile.get("safe_conditions") or []
    # STAGE22E21R_COMPACT_CANONICAL_PROMPT_V1
    # Stage22 uses canonical axes as the problem-relevant truth source.
    # Keep the legacy prompt path unchanged when no canonical axes exist.
    if canonical_axes:
        compact_axes = [
            {
                key: value
                for key, value in axis.items()
                if value not in (None, "", [], {})
            }
            for axis in canonical_axes
            if isinstance(axis, dict)
            and str(axis.get("axis_id") or "").strip()
            and str(axis.get("canonical_claim") or "").strip()
        ]
        compact_candidates = _compact_prompt_candidates(candidates)
        fatal_payload = json.dumps(
            fatal_conditions,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        safe_payload = json.dumps(
            safe_conditions,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        candidate_payload = json.dumps(
            compact_candidates,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        axis_payload = json.dumps(
            compact_axes,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        return (
            "GLOBAL_CANONICAL_AXIS_COMPARISON_V1\n"
            f"topic={display_name}\n"
            "임무:\n"
            "- candidate evidence에 실제로 적힌 주장만 판단한다.\n"
            "- active canonical axes와 의미/관계를 비교한다.\n"
            "- 표현 차이만으로 오답 처리하지 않는다.\n"
            "- 단순 누락·애매함·설명 부족은 fatal이 아니다.\n"
            "- source-owned fatal_core/fatal_if_opposite와 명시적으로 반대되고 "
            "confidence>=0.80이며 anchor_refs와 demand_refs 근거가 있을 때만 "
            "FATAL_CONTRADICTION을 사용한다.\n"
            "- LLM이 criticality, canonical claim, anchor_refs, demand_refs를 "
            "새로 만들면 안 된다.\n"
            f"fatal_conditions={fatal_payload}\n"
            f"safe_conditions={safe_payload}\n"
            f"candidate evidence={candidate_payload}\n"
            # STAGE22E21R7_CANONICAL_AXES_SUFFIX_CONTRACT_V1
            # STAGE22E21S18_EXPLICIT_REQUIRED_OUTPUT_FIELDS_V1
            "STAGE22_COMPACT_OUTPUT_CONTRACT_V1\n"
            "supplied JSON Schema와 일치하는 JSON object만 반환한다.\n"
            "top-level 필수 key: "
            "verdict,confidence,reason,checks,findings,alignments.\n"
            "alignment 필수 key: "
            "axis_id,answer_claim,canonical_claim,claim_signature,status,"
            "criticality,confidence,reason,error_class,anchor_refs,demand_refs.\n"
            "필수 key는 생략하지 않는다. confidence는 0~1 finite number이고 "
            "reason,claim_signature,error_class는 문자열이다.\n"
            "checks,findings,alignments,anchor_refs,demand_refs는 JSON array다.\n"
            "answer/reasoning wrapper를 쓰지 않는다.\n"
            "status는 ALIGNED|PARTIAL|OFF_AXIS|UNSUPPORTED|CONTRADICTED|"
            "FATAL_CONTRADICTION 중 하나다.\n"
            "각 원자 주장마다 별도 alignment; "
            "직접 소유하는 가장 구체적 axis에 1:1; "
            "포괄 axis 병합 금지.\n"
            "axis_id는 아래 값; answer_claim은 해당 주장; "
            "source-owned 필드는 source 복사.\n"
            "checks에는 fatal 조건 평가를, findings에는 실제 major/fatal 오류만 "
            "기록한다.\n"
            # STAGE22E21S24_GENERIC_EXCLUSIVE_ROLE_CONTRADICTION_V1
            # STAGE22E21S27_EXPLICIT_GENERIC_RULE_FIELD_BINDINGS_V1
            # STAGE22E21S30_DIRECT_OWNER_NO_COLLAPSE_AXIS_SELECTION_V1
            "타 축 독점·전담·단독: "
            "error_class=CANONICAL_RELATION_CONTRADICTION; "
            "claim_signature=<subject>.exclusively_establishes.<target>.\n"
            "source fatal+confidence>=0.80만 "
            "status=FATAL_CONTRADICTION.\n"
            "JSON 외 설명·markdown을 출력하지 않는다.\n"
            "canonical axes:\n"
            f"{axis_payload}"
        )

    prompt = f"""
다음은 산업계측제어기술사 답안 중 '{display_name}' 문항의 Logic Check 후보 evidence이다.

너의 임무:
- candidate evidence 안에서 수험생이 실제로 한 주장을 판단한다.
- 정답 스키마와 직접 충돌하는 경우만 fatal로 판정한다.
- 단순 누락, 애매함, 설명 부족은 fatal이 아니다.
- candidate evidence에 없는 내용을 만들어내면 안 된다.

정답 스키마:
{_numbered([str(x) for x in truth_schema])}

fatal 판정 조건:
{_numbered([str(x) for x in fatal_conditions])}

정상/안전 조건:
{_numbered([str(x) for x in safe_conditions])}

반드시 아래 JSON 형식으로만 답하라:
{{
  "verdict": "pass" | "warn" | "fatal",
  "confidence": 0.0,
  "reason": "간단한 한국어 사유",
  "checks": [],
  "findings": [],
  "alignments": []
}}

중요:
- checks에는 fatal 판정 조건을 각각 한 번씩 모두 포함한다.
- 해당 오개념을 주장하지 않았더라도 status=pass로 기록한다.
- findings에는 실제 major 또는 fatal 항목만 포함한다.
- fatal finding은 candidate_id가 반드시 있어야 한다.
- candidate_id는 아래 후보 목록의 id 중 하나만 사용한다.
- evidence가 정답 구분과 실무 튜닝점 구분을 모두 포함하면 fatal로 잡지 않는다.
- 확실하지 않으면 warn으로 둔다.

후보 evidence:
{json.dumps(candidates, ensure_ascii=False, indent=2)}
""".strip()

    active_axes = [
        {
            "axis_id": str(axis.get("axis_id") or "").strip(),
            "canonical_claim": str(
                axis.get("canonical_claim") or ""
            ).strip(),
            "criticality": str(
                axis.get("criticality") or "supporting"
            ).strip(),
            "anchor_refs": axis.get("anchor_refs") or [],
            "demand_refs": axis.get("demand_refs") or [],
        }
        for axis in (canonical_axes or [])
        if isinstance(axis, dict)
        and str(axis.get("axis_id") or "").strip()
        and str(axis.get("canonical_claim") or "").strip()
    ]

    if not active_axes:
        return prompt

    return (
        prompt
        + "\n\n[GLOBAL_CANONICAL_AXIS_COMPARISON_V1]\n"
        + "같은 LLM 호출 안에서 답안 전체의 명시적 주장을 "
        + "활성 정답 축과 비교하라.\n"
        + "문구 유사도가 아니라 개념, 관계 방향, 소유 범위, "
        + "조건 및 배타적 표현의 의미를 비교한다.\n"
        + "ALIGNED는 같은 의미, PARTIAL은 같은 축의 불완전 설명, "
        + "OFF_AXIS는 다른 축, UNSUPPORTED는 근거 부족이다.\n"
        + "CONTRADICTED는 정답 관계와 직접 충돌하는 주장이다.\n"
        + "FATAL_CONTRADICTION은 제공된 source criticality가 "
        + "fatal_core이고 답안이 그 관계를 명시적으로 반대로 "
        + "주장하며 confidence>=0.80인 경우에만 사용한다.\n"
        + "누락, 애매함, 단순 관련성 부족과 다른 유효 축은 "
        + "오답 또는 fatal로 판정하지 않는다.\n"
        + "axis_id, canonical_claim, criticality, anchor_refs와 "
        + "demand_refs는 아래 source 값만 복사한다.\n"
        + "답안에 실제로 확인되는 핵심 주장만 최대 12개를 "
        + "alignments에 기록한다.\n"
        + "canonical axes:\n"
        + json.dumps(
            active_axes,
            ensure_ascii=False,
            indent=2,
        )
    )


def _stage22_profile_response_schema(
    profile: dict[str, Any],
    candidates: list[dict[str, str]],
    canonical_axes: list[dict[str, Any]],
) -> dict[str, Any]:
    candidate_ids = [
        str(row.get("id") or "").strip()
        for row in candidates
        if isinstance(row, dict)
        and str(row.get("id") or "").strip()
    ]
    axis_ids = [
        str(row.get("axis_id") or "").strip()
        for row in canonical_axes
        if isinstance(row, dict)
        and str(row.get("axis_id") or "").strip()
    ]

    raw_fatal_conditions = profile.get("fatal_conditions") or []
    rule_ids: list[str] = []
    for index, row in enumerate(raw_fatal_conditions, start=1):
        if isinstance(row, dict):
            rule_id = str(
                row.get("id") or row.get("rule_id") or ""
            ).strip()
        else:
            match = re.match(r"\s*\[([^\]]+)\]", str(row or ""))
            rule_id = match.group(1).strip() if match else ""
        if not rule_id:
            rule_id = f"profile_rule_{index:03d}"
        if rule_id not in rule_ids:
            rule_ids.append(rule_id)

    rule_id_schema: dict[str, Any] = {"type": "string"}
    if rule_ids:
        rule_id_schema["enum"] = rule_ids

    candidate_schema: dict[str, Any] = {"type": "string"}
    if candidate_ids:
        candidate_schema["enum"] = ["", *candidate_ids]

    return {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "enum": ["pass", "warn", "fatal"],
            },
            "confidence": {
                "type": "number",
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "reason": {"type": "string"},
            "checks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": rule_id_schema,
                        "status": {
                            "type": "string",
                            "enum": ["pass", "major", "fatal"],
                        },
                        "asserted": {"type": "boolean"},
                        "candidate_id": candidate_schema,
                        "evidence": {"type": "string"},
                        "reason": {"type": "string"},
                        "correction": {"type": "string"},
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
                },
            },
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "candidate_id": candidate_schema,
                        "rule_id": rule_id_schema,
                        "severity": {
                            "type": "string",
                            "enum": ["fatal", "major", "minor"],
                        },
                        "message": {"type": "string"},
                        "correct_rule": {"type": "string"},
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
                },
            },
            "alignments": {
                "type": "array",
                "maxItems": 12,
                "items": {
                    "type": "object",
                    "properties": {
                        "axis_id": {
                            "type": "string",
                            "enum": axis_ids,
                        },
                        "status": {
                            "type": "string",
                            "enum": [
                                "ALIGNED",
                                "PARTIAL",
                                "OFF_AXIS",
                                "UNSUPPORTED",
                                "CONTRADICTED",
                                "FATAL_CONTRADICTION",
                            ],
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
                            "enum": [
                                "supporting",
                                "core",
                                "fatal_core",
                            ],
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                        },
                        "reason": {"type": "string"},
                    },
                    "required": [
                        "axis_id",
                        "status",
                        "answer_claim",
                        "canonical_claim",
                        "claim_signature",
                        "error_class",
                        "anchor_refs",
                        "demand_refs",
                        "criticality",
                        "confidence",
                        "reason",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": [
            "verdict",
            "confidence",
            "reason",
            "checks",
            "findings",
            "alignments",
        ],
        "additionalProperties": False,
    }



def _canonical_logic_finding_key(finding: dict[str, Any]) -> tuple[str, str]:
    severity = str(finding.get("severity") or "").strip()
    message = re.sub(r"\s+", " ", str(finding.get("message") or "")).strip()
    evidence = re.sub(r"\s+", " ", str(finding.get("evidence") or "")).strip()

    combined = f"{message} {evidence}"

    # Same logical contradiction can be phrased multiple ways by the LLM.
    if (
        "Under damp =>" in combined
        and "Critical damp =>" in combined
        and "Over damp =>" in combined
    ):
        return (severity, "second_order_zeta_region_mapping_conflict")

    if "sinθ" in combined and ("음의 실수축" in combined or "negative real" in combined):
        return (severity, "second_order_angle_reference_conflict")

    if "임계감쇠" in combined and ("진동" in combined or "오버" in combined):
        return (severity, "second_order_critical_step_response_conflict")

    if "과감쇠" in combined and ("오버" in combined or "충돌" in combined or "최속" in combined):
        return (severity, "second_order_overdamped_step_response_conflict")

    return (severity, message)


def _fatal_condition_rule_ids(profile: dict[str, Any]) -> set[str]:
    rule_ids: set[str] = set()
    for row in profile.get("fatal_conditions") or []:
        if isinstance(row, dict):
            rule_id = str(row.get("id") or row.get("rule_id") or "").strip()
        else:
            match = re.match(r"\s*\[([^\]]+)\]", str(row or ""))
            rule_id = match.group(1).strip() if match else ""
        if rule_id:
            rule_ids.add(rule_id)
    return rule_ids


def _authoritative_structured_rules(
    profile: dict[str, Any],
) -> list[dict[str, Any]]:
    explicit = profile.get("authoritative_structured_rules")
    if isinstance(explicit, list):
        return [dict(row) for row in explicit if isinstance(row, dict)]

    fatal_by_id = {
        str(row.get("id") or row.get("rule_id") or "").strip(): row
        for row in (profile.get("fatal_conditions") or [])
        if isinstance(row, dict)
    }
    rules: list[dict[str, Any]] = []
    compact = profile.get("compact_batch_verification") or {}
    for field in compact.get("fields") or []:
        if not isinstance(field, dict):
            continue
        relation = field.get("structured_relation") or {}
        if not isinstance(relation, dict) or not relation.get("authoritative_true"):
            continue
        rule_id = str(field.get("rule_id") or "").strip()
        pattern = str(relation.get("combined_pattern") or "").strip()
        source = fatal_by_id.get(rule_id)
        if not rule_id or not pattern or not isinstance(source, dict):
            continue
        rules.append({
            "rule_id": rule_id,
            "pattern": pattern,
            "render": str(relation.get("render") or "").strip(),
            "message": str(
                source.get("wrong_claim")
                or source.get("claim")
                or source.get("message")
                or rule_id
            ).strip(),
            "correct_rule": str(
                source.get("correct_rule")
                or source.get("correction")
                or ""
            ).strip(),
            "affected_layers": source.get("affected_layers") or ["C"],
            "recommended_ceiling": source.get("recommended_ceiling"),
        })
    return rules


def _authoritative_structured_findings(
    answer_text: str,
    profile: dict[str, Any],
    default_ceiling: float,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rule in _authoritative_structured_rules(profile):
        try:
            matched = re.search(
                str(rule.get("pattern") or ""),
                str(answer_text or ""),
                flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
            )
        except re.error:
            continue
        if matched is None:
            continue
        rule_id = str(rule.get("rule_id") or "").strip()
        ceiling = rule.get("recommended_ceiling")
        if not isinstance(ceiling, (int, float)) or isinstance(ceiling, bool):
            ceiling = default_ceiling
        finding = {
            "id": f"structured_{rule_id}",
            "rule_id": rule_id,
            "source_rule_id": rule_id,
            "severity": "fatal",
            "message": str(rule.get("message") or rule_id),
            "correct_rule": str(rule.get("correct_rule") or ""),
            "affected_layers": list(rule.get("affected_layers") or ["C"]),
            "evidence": str(rule.get("render") or matched.group(0)).strip(),
            "engine": "authoritative_structured_relation_v1",
            "confidence": 1.0,
            "recommended_ceiling": float(ceiling),
        }
        for reference_key in ("anchor_refs", "demand_refs", "demand_ref_terms"):
            references = rule.get(reference_key)
            if isinstance(references, list):
                finding[reference_key] = [
                    str(value).strip()
                    for value in references
                    if str(value).strip()
                ]
        findings.append(finding)
    return findings


def _combined_logic_profile(
    topic_ids: list[str],
    answer_text: str,
) -> dict[str, Any]:
    profiles = [load_logic_check_profile(topic_id) for topic_id in topic_ids]
    answer = _normalize_text(answer_text).casefold()

    def unique(values: list[Any]) -> list[Any]:
        output: list[Any] = []
        seen: set[str] = set()
        for value in values:
            key = json.dumps(value, ensure_ascii=False, sort_keys=True)
            if key not in seen:
                seen.add(key)
                output.append(value)
        return output

    def relevance(value: Any) -> int:
        tokens = set(re.findall(r"[A-Za-z가-힣0-9/]+", str(value).casefold()))
        return sum(len(token) for token in tokens if len(token) >= 3 and token in answer)

    def relevant_rows(profile: dict[str, Any], key: str, limit: int) -> list[Any]:
        ranked = sorted(
            enumerate(profile.get(key) or []),
            key=lambda item: (-relevance(item[1]), item[0]),
        )
        positive = [row for _index, row in ranked if relevance(row) > 0]
        return positive[:limit]

    fatal_conditions = unique([
        row for profile in profiles
        for row in relevant_rows(profile, "fatal_conditions", 8)
    ])
    truth_schema = unique([
        row for profile in profiles
        for row in relevant_rows(profile, "truth_schema", 6)
    ])
    safe_conditions = unique([
        row for profile in profiles
        for row in relevant_rows(profile, "safe_conditions", 4)
    ])
    key_terms = unique([
        row
        for profile in profiles
        for row in ((profile.get("candidate_extraction") or {}).get("key_terms") or [])
        if _normalize_text(str(row)).casefold() in answer
    ])
    ceilings = [
        float(value)
        for profile in profiles
        for value in [(profile.get("cap_policy") or {}).get("fatal_recommended_ceiling")]
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    ]
    thresholds = [
        float(value)
        for profile in profiles
        for value in [(profile.get("cap_policy") or {}).get("fatal_confidence_threshold")]
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    ]
    authoritative_structured_rules = unique([
        row
        for profile in profiles
        for row in _authoritative_structured_rules(profile)
    ])
    return {
        "topic_id": "multi_topic_logic_batch",
        "display_name": " + ".join(topic_ids),
        "enabled": True,
        "cap_policy": {
            "enabled": True,
            "fatal_confidence_threshold": max(thresholds) if thresholds else 0.8,
            "fatal_recommended_ceiling": min(ceilings) if ceilings else 10.0,
        },
        "candidate_extraction": {
            "max_candidates": 20,
            "nearby_window": 1,
            "rules": [],
            "key_terms": key_terms,
        },
        "truth_schema": truth_schema,
        "fatal_conditions": fatal_conditions,
        "safe_conditions": safe_conditions,
        "authoritative_structured_rules": authoritative_structured_rules,
    }


def verify_logic_with_llm(
    answer_text: str,
    topic_id: str,
    canonical_axes: list[dict[str, Any]] | None = None,
    *,
    _profile_override: dict[str, Any] | None = None,
    _force_schema: bool = False,
) -> dict[str, Any]:
    profile = (
        dict(_profile_override)
        if isinstance(_profile_override, dict)
        else load_logic_check_profile(topic_id)
    )
    cap_policy = profile.get("cap_policy") or {}
    fatal_threshold = float(cap_policy.get("fatal_confidence_threshold") or 0.75)
    fatal_ceiling = float(cap_policy.get("fatal_recommended_ceiling") or 10.0)

    active_axes = [
        dict(axis)
        for axis in (canonical_axes or [])
        if isinstance(axis, dict)
        and str(axis.get("axis_id") or "").strip()
        and str(axis.get("canonical_claim") or "").strip()
    ][:24]

    candidates = extract_logic_evidence_candidates(answer_text, profile)

    # STAGE22E7_GLOBAL_AXIS_EMPTY_CANDIDATE_FALLBACK_V1
    if not candidates and active_axes:
        global_answer = _normalize_text(answer_text)
        if global_answer:
            candidates = [
                {
                    "id": "C1",
                    "kind": "global_answer_context",
                    "text": answer_text[:4000],
                }
            ]

    if not candidates:
        return {
            "applicable": True,
            "engine": "llm_verifier_profile_v1",
            "topic_id": topic_id,
            "verdict": "pass",
            "confidence": 1.0,
            "findings": [],
            "candidates": [],
            "fatal_error_detected": False,
            "recommended_ceiling": None,
            "mode": "pass",
            "reason": "검증할 핵심 후보 evidence가 없습니다.",
        }

    prompt = _build_logic_prompt(
        profile,
        candidates,
        canonical_axes=active_axes,
    )
    response_schema = (
        _stage22_profile_response_schema(
            profile,
            candidates,
            active_axes,
        )
        if active_axes or _force_schema
        else None
    )
    call_kwargs = (
        {"format_schema": response_schema}
        if response_schema is not None
        else {}
    )

    try:
        verdict = _call_ollama_json(
            prompt,
            **call_kwargs,
        )
    except Exception as exc:
        return {
            "applicable": True,
            "engine": "llm_verifier_profile_v1",
            "topic_id": topic_id,
            "verdict": "warn",
            "confidence": 0.0,
            "findings": [
                {
                    "id": "llm_verifier_unavailable",
                    "severity": "minor",
                    "message": f"LLM logic verifier를 실행하지 못했습니다: {exc}",
                    "correct_rule": "LLM verifier 실패 시 fatal cap을 적용하지 않습니다.",
                    "affected_layers": ["C"],
                }
            ],
            "candidates": candidates,
            "fatal_error_detected": False,
            "recommended_ceiling": None,
            "mode": "warn",
            "reason": "LLM verifier unavailable",
        }

    if not isinstance(verdict, dict):
        verdict = {}

    raw_alignments = verdict.get("alignments")
    if not isinstance(raw_alignments, list):
        raw_alignments = []

    # STAGE22E10_PROFILE_ALIGNMENT_RETURN_ENVELOPE_V1
    alignment_rows = [
        row
        for row in raw_alignments
        if isinstance(row, dict)
    ]
    alignment_status_counts = {
        status: sum(
            str(row.get("status") or "").strip().upper()
            == status
            for row in alignment_rows
        )
        for status in (
            "ALIGNED",
            "PARTIAL",
            "OFF_AXIS",
            "UNSUPPORTED",
            "CONTRADICTED",
            "FATAL_CONTRADICTION",
        )
    }
    canonical_axis_alignment_evaluation = {
        "version": "canonical_axis_alignment_transport_v1",
        "score_effect": "none",
        "direct_score_application": False,
        "alignments": alignment_rows,
        "summary": {
            "alignment_count": len(alignment_rows),
            "status_counts": alignment_status_counts,
            "fatal_count": alignment_status_counts.get(
                "FATAL_CONTRADICTION",
                0,
            ),
        },
    }

    candidate_map = {c["id"]: c for c in candidates}

    confidence_value = verdict.get(
        "confidence"
    )
    confidence_error = None

    if isinstance(confidence_value, bool):
        confidence_error = (
            "confidence must be a finite "
            "numeric value, not bool"
        )
    else:
        try:
            confidence_candidate = float(
                confidence_value
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
        ) as error:
            confidence_error = (
                "confidence conversion failed: "
                f"{error!r}"
            )
        else:
            if math.isfinite(
                confidence_candidate
            ):
                confidence = (
                    confidence_candidate
                )
            else:
                confidence_error = (
                    "confidence must be finite"
                )

    if confidence_error is not None:
        return {
            "applicable": True,
            "engine": (
                "llm_verifier_profile_v1"
            ),
            "topic_id": topic_id,
            "verdict": "warn",
            "confidence": None,
            "findings": [
                {
                    "id": (
                        "llm_verifier_"
                        "invalid_confidence"
                    ),
                    "severity": "minor",
                    "message": (
                        "LLM logic verifier가 "
                        "유효하지 않은 confidence를 "
                        "반환했습니다: "
                        f"{confidence_error}; "
                        "value="
                        f"{confidence_value!r}"
                    ),
                    "correct_rule": (
                        "유한한 수치 confidence가 "
                        "없으면 fatal cap을 "
                        "적용하지 않습니다."
                    ),
                    "affected_layers": ["C"],
                }
            ],
            "candidates": candidates,
            "fatal_error_detected": False,
            "recommended_ceiling": None,
            "mode": "warn",
            "reason": (
                "LLM verifier invalid "
                "confidence"
            ),
            "confidence_diagnostic": {
                "ok": False,
                "error": confidence_error,
                "value_repr": repr(
                    confidence_value
                ),
            },
        }

    normalized_findings: list[dict[str, Any]] = []
    allowed_rule_ids = _fatal_condition_rule_ids(profile)

    for item in verdict.get("findings") or []:
        if not isinstance(item, dict):
            continue

        cid = str(item.get("candidate_id") or "").strip()
        if cid not in candidate_map:
            continue

        severity = str(item.get("severity") or "minor").strip().lower()
        if severity not in {"fatal", "major", "minor"}:
            severity = "minor"

        if severity == "fatal" and confidence < fatal_threshold:
            severity = "major"

        message = str(item.get("message") or "").strip()
        correct_rule = str(item.get("correct_rule") or "").strip()

        if not message:
            continue

        finding = {
            "id": f"llm_{topic_id}_{cid}_{severity}",
            "severity": severity,
            "message": message,
            "correct_rule": correct_rule,
            "affected_layers": ["C"],
            "candidate_id": cid,
            "evidence": candidate_map[cid]["text"],
            "engine": "llm_verifier_profile_v1",
        }
        rule_id = str(item.get("rule_id") or "").strip()
        if rule_id in allowed_rule_ids:
            finding["rule_id"] = rule_id
            finding["source_rule_id"] = rule_id

        if severity == "fatal":
            finding["recommended_ceiling"] = fatal_ceiling

        normalized_findings.append(finding)

    # Profile-owned, structurally reconstructed relations are deterministic
    # evidence. They do not depend on the semantic model noticing the same
    # table mapping, but remain limited to explicit authoritative_true rules.
    normalized_findings.extend(
        _authoritative_structured_findings(
            answer_text,
            profile,
            fatal_ceiling,
        )
    )

    # De-duplicate LLM verifier findings.
    # The LLM may return the same contradiction for multiple nearby candidates.
    deduped_findings: list[dict[str, Any]] = []
    seen_finding_keys: set[tuple[str, str, str]] = set()

    for finding in normalized_findings:
        key = _canonical_logic_finding_key(finding)

        if key in seen_finding_keys:
            continue

        seen_finding_keys.add(key)
        deduped_findings.append(finding)

    # Keep fatal feedback focused.
    fatal_findings = [f for f in deduped_findings if f.get("severity") == "fatal"]
    nonfatal_findings = [f for f in deduped_findings if f.get("severity") != "fatal"]

    if fatal_findings:
        deduped_findings = fatal_findings[:3] + nonfatal_findings[:2]
    else:
        deduped_findings = deduped_findings[:5]

    normalized_findings = deduped_findings

    fatal = any(f.get("severity") == "fatal" for f in normalized_findings)
    mode = "fatal" if fatal else ("warn" if normalized_findings else "pass")

    return {
        "applicable": True,
        "engine": "llm_verifier_profile_v1",
        "topic_id": topic_id,
        "verdict": verdict.get("verdict", mode),
        "confidence": confidence,
        "reason": verdict.get("reason", ""),
        "findings": normalized_findings,
        "alignments": raw_alignments,
        "canonical_axis_alignment_evaluation": (
            canonical_axis_alignment_evaluation
        ),
        "candidates": candidates,
        "fatal_error_detected": fatal,
        "recommended_ceiling": fatal_ceiling if fatal else None,
        "mode": mode,
    }


def verify_logic_topics_with_llm(
    answer_text: str,
    topic_ids: list[str],
) -> dict[str, Any]:
    unique_topic_ids = list(dict.fromkeys(
        str(topic_id or "").strip()
        for topic_id in topic_ids
        if str(topic_id or "").strip()
    ))
    if len(unique_topic_ids) < 2:
        raise ValueError("multi-topic logic batch requires at least two topics")
    profile = _combined_logic_profile(unique_topic_ids, answer_text)
    result = verify_logic_with_llm(
        answer_text,
        "multi_topic_logic_batch",
        _profile_override=profile,
        _force_schema=True,
    )
    result["topic_ids"] = unique_topic_ids
    result["engine"] = "multi_topic_logic_batch_v1"
    result["llm_call_count"] = 1
    return result


def verify_second_order_logic_with_llm(answer_text: str) -> dict[str, Any]:
    return verify_logic_with_llm(
        answer_text,
        "second_order_lag_response_by_damping_ratio",
    )
