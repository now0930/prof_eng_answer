from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path
from rubric_bank_paths import resolve_rubric_bank_path
from typing import Any


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

    lines = _lines(answer_text)
    candidates: list[dict[str, str]] = []

    def add(kind: str, text: str) -> None:
        text = _normalize_text(text)
        if not text:
            return
        if len(text) > 900:
            text = text[:900]
        if any(c["text"] == text and c["kind"] == kind for c in candidates):
            return
        candidates.append(
            {
                "id": f"C{len(candidates) + 1}",
                "kind": kind,
                "text": text,
            }
        )

    for rule in rules:
        if not isinstance(rule, dict):
            continue

        kind = str(rule.get("kind") or "candidate")
        rule_type = str(rule.get("type") or "")

        if rule_type == "structured_mapping":
            structured = _structured_mapping_candidate(lines, rule)
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
            for i, line in enumerate(lines):
                if regex.search(line):
                    start = max(0, i - nearby_window)
                    end = min(len(lines), i + nearby_window + 1)
                    add(kind, _candidate_text(lines[start:end]))
            continue

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
        return None

    try:
        return json.loads(cleaned[start : end + 1])
    except Exception:
        return None


def _call_ollama_json(prompt: str) -> dict[str, Any] | None:
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
        "options": {
            "temperature": 0,
            "top_p": 0.1,
        },
    }

    errors: list[str] = []

    for base_url in _ollama_url_candidates():
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
                return parsed

            errors.append(f"{base_url}: JSON parse failed")
        except Exception as exc:
            errors.append(f"{base_url}: {exc!r}")

    raise RuntimeError("all Ollama endpoints failed: " + " | ".join(errors))


def _numbered(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


def _build_logic_prompt(
    profile: dict[str, Any],
    candidates: list[dict[str, str]],
) -> str:
    display_name = profile.get("display_name") or profile.get("topic_id")
    truth_schema = profile.get("truth_schema") or []
    fatal_conditions = profile.get("fatal_conditions") or []
    safe_conditions = profile.get("safe_conditions") or []

    return f"""
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
  "findings": [
    {{
      "candidate_id": "C1",
      "severity": "fatal" | "major" | "minor",
      "message": "한국어 오류 설명",
      "correct_rule": "정답 기준"
    }}
  ]
}}

중요:
- fatal finding은 candidate_id가 반드시 있어야 한다.
- candidate_id는 아래 후보 목록의 id 중 하나만 사용한다.
- kind가 structured_damping_region_table인 후보는 "A => B" 형태의 수험생 주장 요약이다. 이 매핑이 정답 스키마와 직접 충돌하면 우선 검토하라.
- evidence가 정답 구분과 실무 튜닝점 구분을 모두 포함하면 fatal로 잡지 않는다.
- 확실하지 않으면 warn으로 둔다.

후보 evidence:
{json.dumps(candidates, ensure_ascii=False, indent=2)}
""".strip()



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


def verify_logic_with_llm(answer_text: str, topic_id: str) -> dict[str, Any]:
    profile = load_logic_check_profile(topic_id)
    cap_policy = profile.get("cap_policy") or {}
    fatal_threshold = float(cap_policy.get("fatal_confidence_threshold") or 0.75)
    fatal_ceiling = float(cap_policy.get("fatal_recommended_ceiling") or 10.0)

    candidates = extract_logic_evidence_candidates(answer_text, profile)

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

    prompt = _build_logic_prompt(profile, candidates)

    try:
        verdict = _call_ollama_json(prompt)
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

    candidate_map = {c["id"]: c for c in candidates}

    try:
        confidence = float(verdict.get("confidence", 0.0))
    except Exception:
        confidence = 0.0

    normalized_findings: list[dict[str, Any]] = []

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

        if severity == "fatal":
            finding["recommended_ceiling"] = fatal_ceiling

        normalized_findings.append(finding)

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
        "candidates": candidates,
        "fatal_error_detected": fatal,
        "recommended_ceiling": fatal_ceiling if fatal else None,
        "mode": mode,
    }


def verify_second_order_logic_with_llm(answer_text: str) -> dict[str, Any]:
    return verify_logic_with_llm(
        answer_text,
        "second_order_lag_response_by_damping_ratio",
    )
