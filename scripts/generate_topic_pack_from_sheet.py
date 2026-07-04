#!/usr/bin/env python3
"""Generate topic_pack JSON drafts from a human-written Topic Sheet.

This script is an authoring tool, not a runtime grading component.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from topic_review_llm import extract_json_object, gemini_generate
except Exception as exc:  # pragma: no cover
    extract_json_object = None  # type: ignore[assignment]
    gemini_generate = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DEFAULT_GENERATION_MODEL = "gemini-2.5-flash"


SYSTEM_PROMPT = '너는 산업계측제어기술사 채점 Bot의 topic pack authoring agent다.\n\n가장 중요한 원칙:\n- 새 schema를 설계하지 않는다.\n- 제공된 EXISTING SOURCE JSON의 schema, top-level keys, nested keys, list item shape를 유지한다.\n- Topic Sheet는 내용 보강에만 사용한다.\n- 기존 schema에 없는 필드를 임의로 추가하지 않는다.\n- 기존 schema에 있는 필드를 삭제하지 않는다.\n- 기존 runtime과 호환되지 않는 pseudo field를 만들지 않는다.\n- 특히 logic_check에서는 "condition" 같은 pseudo-code 필드를 만들지 않는다.\n\n역할:\n- 사람이 작성한 Topic Sheet를 읽고 기존 topic pack source JSON과 같은 schema의 candidate JSON을 만든다.\n- runtime generated 파일을 직접 만들지 않는다.\n- candidate는 사람이 diff로 검토할 수 있어야 한다.\n\n공통 원칙:\n1. 기존 source JSON schema를 template으로 삼는다.\n2. Topic Sheet의 새 내용은 기존 schema 안에 맞춰 넣는다.\n3. 확실하지 않은 내용은 기존 schema에 review_notes 또는 needs_human_review 같은 필드가 있을 때만 넣는다.\n4. 그런 필드가 기존 schema에 없으면 새 필드를 만들지 말고 기존 설명 필드에 보수적으로 반영한다.\n5. ASCII 표와 다이어그램은 claim 추출 관점으로 설명하되, 기존 schema가 허용하는 위치에만 넣는다.\n6. fatal rule은 정답 기준과 명시적으로 충돌하는 경우에만 만든다.\n7. 단순 누락과 애매한 표현은 fatal이 아니라 major/minor 또는 보완점으로 둔다.\n8. 출력은 JSON object 하나만 한다. markdown fence를 쓰지 않는다.'

FACT_ANCHOR_PROMPT = '아래 Topic Sheet와 EXISTING fact_anchor.json을 기준으로 fact_anchor candidate를 작성하라.\n\n핵심:\n- schema lock이 최우선이다.\n- EXISTING fact_anchor.json의 top-level keys, nested structure, item shape를 유지하라.\n- 새 schema_version, canonical_tables, diagram_facts 같은 새 구조를 만들지 마라. 단, EXISTING에 이미 있으면 유지한다.\n- 기존 필드명과 배열 구조를 그대로 사용하라.\n- Topic Sheet의 내용은 기존 schema 안의 적절한 필드에만 반영하라.\n- 기존 파일에 없는 새 최상위 필드는 만들지 마라.\n- 기존 파일보다 과도하게 짧은 축약본을 만들지 마라.\n\n반영해야 할 내용:\n1. ζ=1은 임계감쇠이고 중근이다.\n2. ζ>1은 과감쇠이고 서로 다른 두 실근이다.\n3. 0<ζ<1은 부족감쇠이고 좌반평면 복소켤레근, 감쇠진동, 오버슈트 가능이다.\n4. 안정 표준 2차계 극점 실수부는 -ζωn이다.\n5. s = +ζωn ± jωd 또는 minus sign 없는 안정 극점 공식은 wrong form으로 감시해야 한다.\n6. ASCII 표와 다이어그램은 직접 정답표를 복사하는 것이 아니라, 답안 claim을 평가할 근거로 설명되어야 한다.\n7. dead time/e^{-Ls}는 보조 설명이며, 이 topic의 핵심을 대체하면 안 된다.\n\n금지:\n- 기존 schema에 없는 canonical_tables 구조를 새로 만들지 마라.\n- 기존 schema에 없는 diagram_facts 구조를 새로 만들지 마라.\n- 기존 schema에 없는 schema_version을 새로 만들지 마라.\n- existing JSON보다 작은 축약본으로 만들지 마라.\n\n출력:\n- EXISTING fact_anchor.json과 같은 schema의 JSON object 하나만 출력한다.\n\nEXISTING fact_anchor.json:\n<<<EXISTING_FACT_ANCHOR_JSON>>>\n{existing_fact_anchor_json}\n<<<END_EXISTING_FACT_ANCHOR_JSON>>>\n\nTopic Sheet:\n<<<TOPIC_SHEET>>>\n{topic_sheet}\n<<<END_TOPIC_SHEET>>>'

LOGIC_CHECK_PROMPT = '아래 Topic Sheet, fact_anchor candidate, EXISTING logic_check.json을 기준으로 logic_check candidate를 작성하라.\n\n핵심:\n- schema lock이 최우선이다.\n- EXISTING logic_check.json의 top-level keys, nested structure, item shape를 유지하라.\n- 새 schema를 만들지 마라.\n- "condition" 필드를 쓰지 마라.\n- pseudo code rule을 쓰지 마라.\n- EXISTING logic_check.json이 wrong_patterns 기반이면 새 fatal rule도 반드시 wrong_patterns 기반으로 작성하라.\n- EXISTING logic_check.json이 truth_schema, fatal_conditions, safe_conditions, major_checks 구조를 갖고 있으면 그 구조를 유지하라.\n- 기존 파일보다 과도하게 짧은 축약본을 만들지 마라.\n\n반드시 보강해야 할 fatal/warn 대상:\n1. ζ=1을 over damped, overdamped, 과감쇠, 과대감쇠로 분류\n2. ζ>1을 critical, critically damped, 임계감쇠로 분류\n3. overdamped, over damped, 과감쇠, 과대감쇠를 중근, repeated root, double root로 설명\n4. 임계감쇠를 서로 다른 두 실근으로 설명\n5. 0<ζ<1을 불안정, 발산 조건으로 설명\n6. ζ=0.707을 임계감쇠 정의로 설명\n7. 안정 표준 2차계 극점 실수부를 +ζωn으로 설명\n8. s = ζωn ± jωd처럼 minus sign 없이 안정 극점으로 해석\n9. 좌반평면 극점을 불안정으로 설명\n10. 우반평면 극점을 안정으로 설명\n11. θ를 음의 실수축 기준으로 정의하고 sinθ=ζ라고 설명\n\n반드시 safe condition으로 보호해야 할 것:\n1. ζ=1 → 중근은 정상이다.\n2. 임계감쇠 → 중근은 정상이다.\n3. 과감쇠 → 서로 다른 두 실근은 정상이다.\n4. θ를 허수축 기준으로 정의하면 ζ=sinθ 표현은 허용한다.\n5. ζ≈0.707을 실무 타협점으로 설명하면 정상이다.\n6. 단순 누락은 fatal이 아니다.\n7. ASCII 그림 위치만으로 fatal 처리하지 않는다.\n\n금지:\n- 다음 같은 rule을 만들지 마라: "ζ == 1 && (name == \'overdamped\' || pole_type == \'중근\')"\n- "ζ=1 && pole_type=중근"을 fatal로 만들지 마라. 이것은 정답이다.\n- 여러 오류를 하나의 ambiguous condition으로 묶지 마라.\n- condition, expression, pseudo_condition 같은 새 필드를 만들지 마라.\n- 기존 logic_check.json보다 훨씬 작은 축약본으로 만들지 마라.\n\n출력:\n- EXISTING logic_check.json과 같은 schema의 JSON object 하나만 출력한다.\n\nEXISTING logic_check.json:\n<<<EXISTING_LOGIC_CHECK_JSON>>>\n{existing_logic_check_json}\n<<<END_EXISTING_LOGIC_CHECK_JSON>>>\n\nfact_anchor candidate:\n<<<FACT_ANCHOR_JSON>>>\n{fact_anchor_json}\n<<<END_FACT_ANCHOR_JSON>>>\n\nTopic Sheet:\n<<<TOPIC_SHEET>>>\n{topic_sheet}\n<<<END_TOPIC_SHEET>>>'

MODEL_ANSWER_PROMPT = '아래 Topic Sheet, fact_anchor candidate, EXISTING model_answer.json을 기준으로 model_answer candidate를 작성하라.\n\n핵심:\n- schema lock이 최우선이다.\n- EXISTING model_answer.json의 top-level keys, nested structure, item shape를 유지하라.\n- 새 schema를 만들지 마라.\n- routing_aliases는 과도하게 넓히지 마라.\n- resonance frequency topic과 겹치는 alias를 새로 추가하지 마라.\n\n반영하면 좋은 내용:\n1. 대표 문제: 2차 지연시스템의 응답 특성을 감쇠비에 따라 구분하고 비교\n2. common mistakes에 다음을 보강\n   - ζ=1을 과감쇠로 분류\n   - 과감쇠를 중근으로 설명\n   - s = +ζωn ± jωd 부호 오류\n   - 2차 지연계와 dead time 혼동\n3. high score에는 극점, 오버슈트, 상승시간, 정착시간, 현장 trade-off를 포함\n4. ASCII 표/다이어그램은 답안 구성 요소로 허용하되, 의미 claim이 맞아야 한다고 설명\n\n출력:\n- EXISTING model_answer.json과 같은 schema의 JSON object 하나만 출력한다.\n\nEXISTING model_answer.json:\n<<<EXISTING_MODEL_ANSWER_JSON>>>\n{existing_model_answer_json}\n<<<END_EXISTING_MODEL_ANSWER_JSON>>>\n\nfact_anchor candidate:\n<<<FACT_ANCHOR_JSON>>>\n{fact_anchor_json}\n<<<END_FACT_ANCHOR_JSON>>>\n\nTopic Sheet:\n<<<TOPIC_SHEET>>>\n{topic_sheet}\n<<<END_TOPIC_SHEET>>>'

TOPIC_IMPORTANCE_PROMPT = '아래 Topic Sheet와 EXISTING topic_importance.json을 기준으로 topic_importance candidate를 작성하라.\n\n핵심:\n- schema lock이 최우선이다.\n- EXISTING topic_importance.json의 top-level keys, nested structure, item shape를 유지하라.\n- 새 schema를 만들지 마라.\n- 기존이 한국어 중심이면 한국어로 작성하라.\n- 기존 difficulty, importance, selection policy 필드명을 유지하라.\n\n반영할 내용:\n1. 이 topic은 THEORY_CORE 성격이다.\n2. 감쇠비별 응답 특성은 핵심 변별 영역이다.\n3. ζ=1/ζ>1/극점 부호 오류는 고위험 오류이다.\n4. 고득점은 정답표 암기가 아니라 극점-응답-현장 trade-off 연결에서 열린다.\n\n출력:\n- EXISTING topic_importance.json과 같은 schema의 JSON object 하나만 출력한다.\n\nEXISTING topic_importance.json:\n<<<EXISTING_TOPIC_IMPORTANCE_JSON>>>\n{existing_topic_importance_json}\n<<<END_EXISTING_TOPIC_IMPORTANCE_JSON>>>\n\nTopic Sheet:\n<<<TOPIC_SHEET>>>\n{topic_sheet}\n<<<END_TOPIC_SHEET>>>'

CONSISTENCY_REVIEW_PROMPT = '아래 Topic Sheet, EXISTING source JSON, 생성된 candidate JSON들이 schema lock을 잘 지켰는지 검토하라.\n\n검토 기준:\n1. candidate가 existing source JSON의 top-level keys를 유지했는가?\n2. candidate가 existing source JSON의 nested structure를 유지했는가?\n3. candidate가 새 schema_version이나 새 top-level schema를 만들지 않았는가?\n4. logic_check에 pseudo "condition" 필드가 없는가?\n5. logic_check fatal rule이 existing schema의 wrong_patterns/fatal_conditions 구조를 따르는가?\n6. ζ=1 → 중근을 fatal로 잘못 잡지 않는가?\n7. ζ=1 → overdamped, overdamped → 중근은 분리된 오류로 잡는가?\n8. candidate가 existing보다 과도하게 축약되지 않았는가?\n9. ASCII 표/다이어그램 평가 내용이 기존 schema 안에 안전하게 들어갔는가?\n\n출력 JSON 형식:\n{\n  "review_level": "pass | minor | major | blocker",\n  "summary": "...",\n  "schema_lock_violations": [],\n  "unsafe_logic_rules": [],\n  "missing_required_rules": [],\n  "over_strict_rules": [],\n  "candidate_shrinkage_risk": [],\n  "recommended_actions": []\n}\n\nEXISTING fact_anchor.json:\n<<<EXISTING_FACT_ANCHOR_JSON>>>\n{existing_fact_anchor_json}\n<<<END_EXISTING_FACT_ANCHOR_JSON>>>\n\nEXISTING logic_check.json:\n<<<EXISTING_LOGIC_CHECK_JSON>>>\n{existing_logic_check_json}\n<<<END_EXISTING_LOGIC_CHECK_JSON>>>\n\nEXISTING model_answer.json:\n<<<EXISTING_MODEL_ANSWER_JSON>>>\n{existing_model_answer_json}\n<<<END_EXISTING_MODEL_ANSWER_JSON>>>\n\nEXISTING topic_importance.json:\n<<<EXISTING_TOPIC_IMPORTANCE_JSON>>>\n{existing_topic_importance_json}\n<<<END_EXISTING_TOPIC_IMPORTANCE_JSON>>>\n\nfact_anchor candidate:\n<<<FACT_ANCHOR_JSON>>>\n{fact_anchor_json}\n<<<END_FACT_ANCHOR_JSON>>>\n\nlogic_check candidate:\n<<<LOGIC_CHECK_JSON>>>\n{logic_check_json}\n<<<END_LOGIC_CHECK_JSON>>>\n\nmodel_answer candidate:\n<<<MODEL_ANSWER_JSON>>>\n{model_answer_json}\n<<<END_MODEL_ANSWER_JSON>>>\n\ntopic_importance candidate:\n<<<TOPIC_IMPORTANCE_JSON>>>\n{topic_importance_json}\n<<<END_TOPIC_IMPORTANCE_JSON>>>'

PROMPT_ORDER = [
    "fact_anchor",
    "logic_check",
    "model_answer",
    "topic_importance",
    "consistency_review",
]


def project_root() -> Path:
    for candidate in [ROOT, Path.cwd(), Path("/workspace/prof_eng_answer")]:
        if (candidate / "rubrics" / "topic_packs").exists():
            return candidate
    raise SystemExit("ERROR: project root not found. Run inside prof_eng_answer repo.")


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def ensure_json_object(text: str, label: str) -> dict[str, Any]:
    """Return the first JSON object from an LLM response.

    Some Gemini responses contain a valid JSON object followed by extra text.
    The previous parser rejected that as "Extra data". For generation drafts,
    we want to accept the first complete JSON object and ignore trailing prose.
    """
    import json as _json

    raw = str(text or "").strip()

    # Remove a leading markdown fence if the model used one.
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()

    decoder = _json.JSONDecoder()

    # Fast path: exact JSON.
    try:
        data = _json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Robust path: parse the first complete object and ignore trailing text.
    start = raw.find("{")
    while start >= 0:
        try:
            data, _end = decoder.raw_decode(raw[start:])
            if isinstance(data, dict):
                return data
        except Exception:
            start = raw.find("{", start + 1)
            continue
        start = raw.find("{", start + 1)

    # Fallback to existing helper if available.
    if extract_json_object is not None:
        data, error = extract_json_object(text)
        if data is not None:
            return data
        raise SystemExit(f"ERROR: {label} did not return a JSON object: {error}\n{str(text)[:2000]}")

    raise SystemExit(f"ERROR: {label} did not return a JSON object\n{str(text)[:2000]}")


def call_llm(prompt: str, *, model: str | None, timeout: int | None, max_output_tokens: int | None) -> dict[str, Any]:
    if gemini_generate is None:
        raise SystemExit(f"ERROR: topic_review_llm import failed: {_IMPORT_ERROR}")
    response = gemini_generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        model=model,
        timeout=timeout,
        temperature=0.1,
        max_output_tokens=max_output_tokens,
    )
    content = str(response.get("content") or "")
    data = ensure_json_object(content, "LLM response")
    return {
        "provider": response.get("provider"),
        "model": response.get("model"),
        "content": content,
        "json": data,
    }


def load_existing_templates(pack_dir: Path) -> dict[str, str]:
    """Load existing topic pack JSON files as schema-lock templates."""
    mapping = {
        "existing_fact_anchor_json": "fact_anchor.json",
        "existing_logic_check_json": "logic_check.json",
        "existing_model_answer_json": "model_answer.json",
        "existing_topic_importance_json": "topic_importance.json",
    }
    templates: dict[str, str] = {}
    for key, filename in mapping.items():
        path = pack_dir / filename
        if path.exists():
            templates[key] = path.read_text(encoding="utf-8")
        else:
            templates[key] = "{}"
    return templates


def render_prompts(
    topic_sheet: str,
    drafts: dict[str, dict[str, Any]] | None = None,
    templates: dict[str, str] | None = None,
) -> dict[str, str]:
    """Render LLM prompts with schema-lock templates.

    Do not use str.format because prompt templates contain literal JSON examples.
    Only explicit placeholder replacement is allowed.
    """
    drafts = drafts or {}
    templates = templates or {}
    values = {
        "topic_sheet": topic_sheet,
        "fact_anchor_json": json_dumps(drafts.get("fact_anchor", {})),
        "logic_check_json": json_dumps(drafts.get("logic_check", {})),
        "model_answer_json": json_dumps(drafts.get("model_answer", {})),
        "topic_importance_json": json_dumps(drafts.get("topic_importance", {})),
        "existing_fact_anchor_json": templates.get("existing_fact_anchor_json", "{}"),
        "existing_logic_check_json": templates.get("existing_logic_check_json", "{}"),
        "existing_model_answer_json": templates.get("existing_model_answer_json", "{}"),
        "existing_topic_importance_json": templates.get("existing_topic_importance_json", "{}"),
    }

    def fill(template: str) -> str:
        out = template
        for key, value in values.items():
            out = out.replace("{" + key + "}", value)
        return out

    return {
        "fact_anchor": fill(FACT_ANCHOR_PROMPT),
        "logic_check": fill(LOGIC_CHECK_PROMPT),
        "model_answer": fill(MODEL_ANSWER_PROMPT),
        "topic_importance": fill(TOPIC_IMPORTANCE_PROMPT),
        "consistency_review": fill(CONSISTENCY_REVIEW_PROMPT),
    }


TOPIC_PACK_SOURCE_FILENAMES = {
    "fact_anchor": "fact_anchor.json",
    "logic_check": "logic_check.json",
    "model_answer": "model_answer.json",
    "topic_importance": "topic_importance.json",
}


def load_existing_json_template(pack_dir: Path, name: str) -> dict[str, Any]:
    """Load existing source JSON as the schema-lock merge template."""
    filename = TOPIC_PACK_SOURCE_FILENAMES.get(name)
    if not filename:
        return {}
    path = pack_dir / filename
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def schema_locked_merge(existing: Any, candidate: Any) -> Any:
    """Preserve existing schema while accepting candidate content.

    Dict:
      - keep only keys that already exist in the existing template
      - if candidate omits an existing key, restore the existing value

    List:
      - keep the candidate list when the LLM supplied one
      - otherwise restore the existing list

    Scalar:
      - keep candidate value unless it is None

    This prevents LLM shrinkage such as dropping llm_profile or de_claim_trust.
    """
    if isinstance(existing, dict):
        candidate_dict = candidate if isinstance(candidate, dict) else {}
        merged: dict[str, Any] = {}
        for key, old_value in existing.items():
            if key in candidate_dict:
                merged[key] = schema_locked_merge(old_value, candidate_dict[key])
            else:
                merged[key] = old_value
        return merged

    if isinstance(existing, list):
        if isinstance(candidate, list) and candidate:
            return candidate
        return existing

    if candidate is None:
        return existing
    return candidate



def append_required_logic_rules(data: dict[str, Any]) -> dict[str, Any]:
    """Append mandatory v1 fatal checks that the LLM often omits.

    This does not change schema. It only appends objects with the same shape as
    deterministic_checks.fatal_checks in the existing v1 logic_check.json.
    """
    dc = data.setdefault("deterministic_checks", {})
    fatal_checks = dc.setdefault("fatal_checks", [])
    if not isinstance(fatal_checks, list):
        return data

    existing_ids = {
        rule.get("id")
        for rule in fatal_checks
        if isinstance(rule, dict)
    }

    required = [
        {
            "id": "zeta_one_as_overdamped",
            "severity": "fatal",
            "wrong_patterns": [
                "ζ\\s*=\\s*1.{0,40}과\\s*감쇠",
                "ζ\\s*=\\s*1.{0,40}과대\\s*감쇠",
                "ζ\\s*=\\s*1.{0,40}over\\s*damp",
                "zeta\\s*=\\s*1.{0,40}over\\s*damp",
                "임계\\s*감쇠.{0,40}과\\s*감쇠",
                "critically\\s*damped.{0,40}over\\s*damped"
            ],
            "message": "임계감쇠(ζ=1)를 과감쇠로 잘못 분류하였다.",
            "correct_rule": "임계감쇠는 ζ=1이며 중근을 갖고, 과감쇠는 ζ>1이며 서로 다른 두 실근을 갖는다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "zeta_greater_than_one_as_critical",
            "severity": "fatal",
            "wrong_patterns": [
                "ζ\\s*>\\s*1.{0,40}임계\\s*감쇠",
                "ζ\\s*>\\s*1.{0,40}critical\\s*damp",
                "zeta\\s*>\\s*1.{0,40}critical\\s*damp",
                "과\\s*감쇠.{0,40}임계\\s*감쇠",
                "over\\s*damped.{0,40}critically\\s*damped"
            ],
            "message": "과감쇠(ζ>1)를 임계감쇠로 잘못 분류하였다.",
            "correct_rule": "임계감쇠는 ζ=1이고, 과감쇠는 ζ>1이다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "overdamped_as_repeated_root",
            "severity": "fatal",
            "wrong_patterns": [
                "과\\s*감쇠.{0,60}중근",
                "과대\\s*감쇠.{0,60}중근",
                "과\\s*감쇠.{0,60}반복\\s*실근",
                "over\\s*damped.{0,60}repeated\\s*root",
                "over\\s*damped.{0,60}double\\s*root"
            ],
            "message": "과감쇠를 중근 조건으로 잘못 설명하였다.",
            "correct_rule": "과감쇠는 서로 다른 두 실근을 가지며, 중근은 임계감쇠 조건이다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "critical_damping_as_distinct_roots",
            "severity": "fatal",
            "wrong_patterns": [
                "임계\\s*감쇠.{0,60}서로\\s*다른\\s*두\\s*실근",
                "임계\\s*감쇠.{0,60}상이한\\s*두\\s*실근",
                "critical\\s*damp.{0,60}distinct\\s*roots",
                "critically\\s*damped.{0,60}two\\s*real\\s*roots"
            ],
            "message": "임계감쇠를 서로 다른 두 실근으로 잘못 설명하였다.",
            "correct_rule": "임계감쇠는 중근을 가지며, 서로 다른 두 실근은 과감쇠 조건이다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "stable_pole_formula_missing_negative_sign",
            "severity": "fatal",
            "wrong_patterns": [
                "s\\s*=\\s*ζ\\s*(?:·|\\*)?\\s*ωn\\s*(?:±|\\+/-)\\s*j\\s*(?:·|\\*)?\\s*ωd",
                "s\\s*=\\s*zeta\\s*(?:·|\\*)?\\s*w[nN]\\s*(?:±|\\+/-)\\s*j\\s*(?:·|\\*)?\\s*w[dD]",
                "극점.{0,60}\\+\\s*ζ\\s*(?:·|\\*)?\\s*ωn",
                "pole.{0,60}\\+\\s*zeta\\s*(?:·|\\*)?\\s*w[nN]"
            ],
            "message": "안정한 표준 2차계 극점의 실수부 부호를 음수가 아닌 양수로 표기하였다.",
            "correct_rule": "표준 2차 시스템의 부족감쇠 극점은 s=-ζωn±jωd이며 안정 극점의 실수부는 음수이다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "left_right_half_plane_stability_inversion",
            "severity": "fatal",
            "wrong_patterns": [
                "좌반\\s*평면.{0,50}불\\s*안정",
                "left[-\\s]*half[-\\s]*plane.{0,50}unstable",
                "LHP.{0,50}unstable",
                "우반\\s*평면.{0,50}(?<!불)안정",
                "right[-\\s]*half[-\\s]*plane.{0,50}stable",
                "RHP.{0,50}stable"
            ],
            "message": "s-평면 좌반평면/우반평면 안정성 관계를 반대로 설명하였다.",
            "correct_rule": "연속시간 시스템에서 좌반평면 극점은 안정, 우반평면 극점은 불안정이다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "zeta_negative_as_stable",
            "severity": "fatal",
            "wrong_patterns": [
                "ζ\\s*<\\s*0.{0,50}(?<!불)안정",
                "zeta\\s*<\\s*0.{0,50}stable",
                "음의\\s*감쇠.{0,50}(?<!불)안정",
                "negative\\s*damping.{0,50}stable"
            ],
            "message": "음의 감쇠비(ζ<0)를 안정 조건으로 잘못 설명하였다.",
            "correct_rule": "ζ<0은 극점 실수부가 양수가 되어 우반평면 극점과 불안정 응답을 유발한다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        },
        {
            "id": "zeta_zero_as_asymptotically_stable",
            "severity": "fatal",
            "wrong_patterns": [
                "ζ\\s*=\\s*0.{0,50}점근\\s*안정",
                "zeta\\s*=\\s*0.{0,50}asymptotically\\s*stable",
                "무\\s*감쇠.{0,50}점근\\s*안정"
            ],
            "message": "무감쇠(ζ=0)를 점근 안정으로 잘못 설명하였다.",
            "correct_rule": "ζ=0은 순허수근에 의한 지속진동 상태이며 임계 안정 또는 marginal stability로 본다.",
            "affected_layers": ["C"],
            "recommended_ceiling": 10.0
        }
    ]

    for rule in required:
        if rule["id"] not in existing_ids:
            fatal_checks.append(rule)
            existing_ids.add(rule["id"])

    return data

def enforce_schema_lock(name: str, data: dict[str, Any], pack_dir: Path) -> dict[str, Any]:
    """Post-process LLM output against the existing source schema."""
    existing = load_existing_json_template(pack_dir, name)
    if not existing:
        return data

    merged = schema_locked_merge(existing, data)
    if not isinstance(merged, dict):
        return data

    if name == "logic_check":
        merged = append_required_logic_rules(merged)
        text = json.dumps(merged, ensure_ascii=False)
        forbidden_fragments = [
            '"condition"',
            "ζ == 1 &&",
            "pole_type == '중근'",
            'pole_type == "중근"',
        ]
        hits = [frag for frag in forbidden_fragments if frag in text]
        if hits:
            raise SystemExit(
                "ERROR: schema-lock guard rejected logic_check candidate; "
                f"forbidden fragments found: {hits}"
            )

        required_paths = [
            ("deterministic_checks", "de_claim_trust"),
            ("deterministic_checks", "next_practice_points"),
            ("llm_profile",),
        ]
        for path in required_paths:
            cur: Any = merged
            for key in path:
                if not isinstance(cur, dict) or key not in cur:
                    raise SystemExit(
                        "ERROR: schema-lock merge failed; missing required path: "
                        + ".".join(path)
                    )
                cur = cur[key]

    return merged

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    write_text(path, json_dumps(data) + "\n")


def output_path(pack_dir: Path, name: str, overwrite: bool) -> Path:
    mapping = {
        "fact_anchor": "fact_anchor.json",
        "logic_check": "logic_check.json",
        "model_answer": "model_answer.json",
        "topic_importance": "topic_importance.json",
    }
    filename = mapping[name]
    path = pack_dir / filename
    if overwrite or not path.exists():
        return path
    return pack_dir / filename.replace(".json", ".candidate.json")


def save_prompt_report(report_dir: Path, stamp: str, topic_id: str, prompts: dict[str, str]) -> Path:
    lines: list[str] = [
        f"# Topic Pack Generation Prompts: {topic_id}",
        "",
        f"timestamp: {stamp}",
        "",
    ]
    for name in PROMPT_ORDER:
        prompt = prompts.get(name, "")
        lines.extend([
            f"## {name}",
            "",
            "```text",
            prompt,
            "```",
            "",
        ])
    path = report_dir / f"topic_pack_generation_{topic_id}_{stamp}_prompts.md"
    write_text(path, "\n".join(lines))
    return path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate topic_pack JSON drafts from a human-written Topic Sheet."
    )
    p.add_argument("--topic-id", required=True)
    p.add_argument("--sheet", required=True, help="Path to Topic Sheet markdown.")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing topic pack JSON files.")
    p.add_argument("--dry-run", action="store_true", help="Only render prompts; do not call LLM.")
    p.add_argument(
        "--model",
        default=DEFAULT_GENERATION_MODEL,
        help=(
            "Gemini model for topic-pack generation. "
            "Default: env TOPIC_PACK_GENERATION_GEMINI_MODEL, "
            "then TOPIC_REVIEW_GEMINI_MODEL, then GEMINI_MODEL, "
            "then gemini-2.5-flash."
        ),
    )
    p.add_argument("--timeout", type=int, default=None)
    p.add_argument("--max-output-tokens", type=int, default=8192)
    p.add_argument(
        "--only",
        choices=["all", "fact_anchor", "logic_check", "model_answer", "topic_importance", "consistency_review"],
        default="all",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = project_root()
    sheet_path = Path(args.sheet)
    if not sheet_path.is_absolute():
        sheet_path = root / sheet_path
    if not sheet_path.exists():
        raise SystemExit(f"ERROR: sheet not found: {sheet_path}")

    topic_sheet = sheet_path.read_text(encoding="utf-8")
    if args.topic_id not in topic_sheet:
        print(f"WARN: topic_id {args.topic_id!r} not found in sheet text", file=sys.stderr)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = root / "reports"
    pack_dir = root / "rubrics" / "topic_packs" / args.topic_id
    pack_dir.mkdir(parents=True, exist_ok=True)
    templates = load_existing_templates(pack_dir)

    prompts = render_prompts(topic_sheet, templates=templates)
    prompt_report = save_prompt_report(report_dir, stamp, args.topic_id, prompts)
    print(f"prompts: {prompt_report.relative_to(root)}")
    print(f"model: {args.model}")

    if args.dry_run:
        print("dry-run: LLM call skipped")
        return 0

    drafts: dict[str, dict[str, Any]] = {}
    raw_report: dict[str, Any] = {
        "topic_id": args.topic_id,
        "sheet": str(sheet_path),
        "timestamp": stamp,
        "outputs": {},
    }

    for name in ["fact_anchor", "logic_check", "model_answer", "topic_importance"]:
        if args.only not in ("all", name):
            continue
        prompts = render_prompts(topic_sheet, drafts, templates)
        print(f"generating: {name}")
        result = call_llm(
            prompts[name],
            model=args.model,
            timeout=args.timeout,
            max_output_tokens=args.max_output_tokens,
        )
        data = result["json"]
        data = enforce_schema_lock(name, data, pack_dir)
        drafts[name] = data
        raw_report["outputs"][name] = {
            "provider": result.get("provider"),
            "model": result.get("model"),
            "content": result.get("content"),
            "json": data,
        }
        path = output_path(pack_dir, name, args.overwrite)
        write_json(path, data)
        print(f"wrote: {path.relative_to(root)}")

    if args.only in ("all", "consistency_review"):
        for name, filename in [
            ("fact_anchor", "fact_anchor.json"),
            ("logic_check", "logic_check.json"),
            ("model_answer", "model_answer.json"),
            ("topic_importance", "topic_importance.json"),
        ]:
            if name not in drafts:
                candidate = pack_dir / filename
                if candidate.exists():
                    try:
                        drafts[name] = json.loads(candidate.read_text(encoding="utf-8"))
                    except json.JSONDecodeError:
                        pass

        prompts = render_prompts(topic_sheet, drafts, templates)
        print("generating: consistency_review")
        result = call_llm(
            prompts["consistency_review"],
            model=args.model,
            timeout=args.timeout,
            max_output_tokens=args.max_output_tokens,
        )
        review_data = result["json"]
        raw_report["outputs"]["consistency_review"] = {
            "provider": result.get("provider"),
            "model": result.get("model"),
            "content": result.get("content"),
            "json": review_data,
        }
        review_path = report_dir / f"topic_pack_generation_{args.topic_id}_{stamp}_consistency_review.json"
        write_json(review_path, review_data)
        print(f"review: {review_path.relative_to(root)}")

    raw_path = report_dir / f"topic_pack_generation_{args.topic_id}_{stamp}_raw.json"
    write_json(raw_path, raw_report)
    print(f"raw: {raw_path.relative_to(root)}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
