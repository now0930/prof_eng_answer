from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Any


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434").rstrip("/")
LOGIC_LLM_MODEL = os.getenv("LOGIC_LLM_VERIFIER_MODEL", os.getenv("OLLAMA_MODEL", "gemma4:e4b"))
LOGIC_LLM_TIMEOUT = int(os.getenv("LOGIC_LLM_VERIFIER_TIMEOUT", "90"))
FATAL_CONFIDENCE_THRESHOLD = float(os.getenv("LOGIC_LLM_FATAL_CONFIDENCE", "0.75"))


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



def _structured_damping_region_candidate(lines: list[str]) -> str | None:
    """
    Build a compact structured candidate from common copied table forms:
        Under damp Critical damp over damp
        zeta ζ < 0.7 ζ = 0.7 0.7 <= ζ < 1

    This does not decide correctness. It only presents the suspected mapping
    clearly to the LLM verifier.
    """
    label_re = re.compile(
        r"(under\s*damp(?:ed|ing)?|부족\s*감쇠|critical\s*damp(?:ed|ing)?|임계\s*감쇠|over\s*damp(?:ed|ing)?|과\s*감쇠)",
        flags=re.IGNORECASE,
    )

    range_re = re.compile(
        r"(ζ\s*<\s*0\.70?7?|ζ\s*=\s*0\.70?7?|0\.70?7?\s*<=\s*ζ\s*<\s*1|0\s*<\s*ζ\s*<\s*1|ζ\s*=\s*1|ζ\s*>\s*1)",
        flags=re.IGNORECASE,
    )

    def normalize_label(label: str) -> str:
        l = label.lower()
        if "under" in l or "부족" in label:
            return "Under damp"
        if "critical" in l or "임계" in label:
            return "Critical damp"
        if "over" in l or "과" in label:
            return "Over damp"
        return label

    for i, line in enumerate(lines[:-1]):
        labels = [normalize_label(m.group(0)) for m in label_re.finditer(line)]
        if len(labels) < 2:
            continue

        nearby = " ".join(lines[i + 1:i + 3])
        ranges = [m.group(0) for m in range_re.finditer(nearby)]

        if len(ranges) < len(labels):
            continue

        pairs = [f"{label} => {rng}" for label, rng in zip(labels, ranges)]
        return " | ".join(pairs)

    # Fallback for fully collapsed text.
    collapsed = " ".join(lines)
    labels = [normalize_label(m.group(0)) for m in label_re.finditer(collapsed)]
    ranges = [m.group(0) for m in range_re.finditer(collapsed)]

    if len(labels) >= 2 and len(ranges) >= len(labels):
        pairs = [f"{label} => {rng}" for label, rng in zip(labels[:len(ranges)], ranges)]
        return " | ".join(pairs)

    return None


def extract_second_order_evidence_candidates(answer_text: str, max_candidates: int = 12) -> list[dict[str, str]]:
    """
    Extract only high-value evidence candidates.
    This is NOT a full parser and should not decide correctness.
    LLM verifier decides whether a candidate is actually contradictory.
    """
    lines = _lines(answer_text)
    candidates: list[dict[str, str]] = []

    def add(kind: str, text: str) -> None:
        text = _normalize_text(text)
        if not text:
            return
        if len(text) > 700:
            text = text[:700]
        if any(c["text"] == text for c in candidates):
            return
        candidates.append(
            {
                "id": f"C{len(candidates) + 1}",
                "kind": kind,
                "text": text,
            }
        )

    structured_region = _structured_damping_region_candidate(lines)
    if structured_region:
        add("structured_damping_region_table", structured_region)

    damping_terms = re.compile(
        r"(무\s*감쇠|부족\s*감쇠|임계\s*감쇠|과\s*감쇠|under\s*damp|critical\s*damp|over\s*damp|un[-\s]*damped)",
        flags=re.IGNORECASE,
    )

    # 1) Compact header/table-like candidates.
    for i, line in enumerate(lines):
        has_many_damping_terms = len(damping_terms.findall(line)) >= 2
        has_zeta = "ζ" in line or "zeta" in line.lower()

        if has_many_damping_terms and has_zeta:
            add("damping_table_or_compact_row", line)
            continue

        if has_many_damping_terms and i + 1 < len(lines):
            nxt = lines[i + 1]
            if "ζ" in nxt or "zeta" in nxt.lower():
                add("damping_header_plus_zeta_row", _candidate_text([line, nxt]))

        if "|" in line and damping_terms.search(line):
            nearby = _candidate_text(lines[max(0, i - 1): min(len(lines), i + 3)])
            add("markdown_or_ascii_table", nearby)

    # 2) zeta 0.7 / 0.707 context.
    for i, line in enumerate(lines):
        if re.search(r"0\.70?7?", line):
            nearby = _candidate_text(lines[max(0, i - 1): min(len(lines), i + 2)])
            add("zeta_0_7_context", nearby)

    # 3) theta / sin / cos / angle context.
    for i, line in enumerate(lines):
        if re.search(r"(θ|theta|sin|cos|실수축|허수축|real\s*axis|imaginary\s*axis)", line, flags=re.IGNORECASE):
            nearby = _candidate_text(lines[max(0, i - 1): min(len(lines), i + 2)])
            add("angle_relation_context", nearby)

    # 4) Step response context.
    for i, line in enumerate(lines):
        if damping_terms.search(line) and re.search(
            r"(진동|오버\s*슈트|overshoot|overshot|충돌|최속|느리|수렴|발산)",
            line,
            flags=re.IGNORECASE,
        ):
            nearby = _candidate_text(lines[max(0, i - 1): min(len(lines), i + 2)])
            add("step_response_context", nearby)

    # 5) General classification line.
    for line in lines:
        if "ζ=0" in line and "0<ζ<1" in line and "ζ=1" in line and "ζ>1" in line:
            add("standard_zeta_classification", line)

    return candidates[:max_candidates]


def _extract_json_object(text: str) -> dict[str, Any] | None:
    if not text:
        return None

    # Remove code fences if present.
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
        return json.loads(cleaned[start:end + 1])
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

    req = urllib.request.Request(
        OLLAMA_URL + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=LOGIC_LLM_TIMEOUT) as resp:
        raw = resp.read().decode("utf-8", errors="replace")

    data = json.loads(raw)
    content = (data.get("message") or {}).get("content") or data.get("response") or ""
    return _extract_json_object(content)


def _build_second_order_prompt(candidates: list[dict[str, str]]) -> str:
    return f"""
다음은 산업계측제어기술사 답안 중 2차 표준형 시스템/감쇠비 문항의 Logic Check 후보 evidence이다.

너의 임무:
- candidate evidence 안에서 수험생이 실제로 한 주장을 판단한다.
- 정답 스키마와 직접 충돌하는 경우만 fatal로 판정한다.
- 단순 누락, 애매함, 설명 부족은 fatal이 아니다.
- candidate evidence에 없는 내용을 만들어내면 안 된다.
- ζ≈0.707 언급 자체는 fatal이 아니다.
- ζ≈0.707을 '부족감쇠 영역의 실무적 타협점/45도 극점/튜닝점'으로 설명하면 정상이다.
- ζ≈0.707을 '임계감쇠의 정의'라고 명시한 경우만 fatal이다.

정답 스키마:
1. ζ=0: 무감쇠
2. 0<ζ<1: 부족감쇠
3. ζ=1: 임계감쇠
4. ζ>1: 과감쇠
5. 부족감쇠는 오버슈트와 감쇠진동을 동반할 수 있으나 좌반면 극점이면 안정 수렴한다.
6. 임계감쇠는 오버슈트 없이 가장 빠른 무진동 수렴이다.
7. 과감쇠는 오버슈트 없이 느리게 수렴한다.
8. θ를 음의 실수축 기준으로 정의하면 ζ=cosθ이다. sinθ 관계는 허수축 기준 각도일 때 가능하다.
9. 시간지연은 위상여유를 줄여 불안정을 유발할 수 있으나, 부족감쇠 자체와 발산은 구분해야 한다.

fatal 판정 조건:
- 명시적으로 임계감쇠=ζ=0.7 또는 0.707이라고 정의함
- 명시적으로 과감쇠=0.7≤ζ<1이라고 정의함
- 명시적으로 부족감쇠=ζ<0.7로 제한함
- 명시적으로 임계감쇠가 진동/오버슈트 응답이라고 함
- 명시적으로 과감쇠가 오버슈트/충돌위험/최속 응답이라고 함
- θ를 음의 실수축 기준으로 정의하고 sinθ=ζ 또는 sinθ=σ/ωn이라고 함

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


def verify_second_order_logic_with_llm(answer_text: str) -> dict[str, Any]:
    candidates = extract_second_order_evidence_candidates(answer_text)

    if not candidates:
        return {
            "applicable": True,
            "engine": "llm_verifier_v1",
            "verdict": "pass",
            "confidence": 1.0,
            "findings": [],
            "candidates": [],
            "fatal_error_detected": False,
            "recommended_ceiling": None,
            "mode": "pass",
            "reason": "검증할 핵심 후보 evidence가 없습니다.",
        }

    prompt = _build_second_order_prompt(candidates)

    try:
        verdict = _call_ollama_json(prompt)
    except Exception as exc:
        return {
            "applicable": True,
            "engine": "llm_verifier_v1",
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
    confidence = verdict.get("confidence", 0.0)
    try:
        confidence = float(confidence)
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

        # Guardrail: low-confidence fatal is downgraded.
        if severity == "fatal" and confidence < FATAL_CONFIDENCE_THRESHOLD:
            severity = "major"

        evidence = candidate_map[cid]["text"]
        message = str(item.get("message") or "").strip()
        correct_rule = str(item.get("correct_rule") or "").strip()

        if not message:
            continue

        finding = {
            "id": f"llm_second_order_{cid}_{severity}",
            "severity": severity,
            "message": message,
            "correct_rule": correct_rule,
            "affected_layers": ["C"],
            "candidate_id": cid,
            "evidence": evidence,
            "engine": "llm_verifier_v1",
        }

        if severity == "fatal":
            finding["recommended_ceiling"] = 10.0

        normalized_findings.append(finding)

    fatal = any(f.get("severity") == "fatal" for f in normalized_findings)

    mode = "fatal" if fatal else ("warn" if normalized_findings else "pass")

    return {
        "applicable": True,
        "engine": "llm_verifier_v1",
        "verdict": verdict.get("verdict", mode),
        "confidence": confidence,
        "reason": verdict.get("reason", ""),
        "findings": normalized_findings,
        "candidates": candidates,
        "fatal_error_detected": fatal,
        "recommended_ceiling": 10.0 if fatal else None,
        "mode": mode,
    }
