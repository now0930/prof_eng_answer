#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "scripts" else Path.cwd()

MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

OUT_MD = ROOT / "reports/model_fact_relationship_audit.md"
OUT_CSV = ROOT / "reports/model_fact_relationship_audit.csv"

QUESTION_TYPE_HINTS = {
    "PRINCIPLE_INTERPRETATION": ["정의", "원리", "메커니즘", "관계", "해석", "특성", "표현", "식"],
    "COMPARE_SELECTION": ["비교", "선정", "장단점", "적용", "조건", "기준", "분류"],
    "DIAGNOSIS_ACTION": ["원인", "문제", "진단", "대책", "개선", "고장", "조치"],
    "IMPLEMENTATION_EVALUATION": ["절차", "적용", "구축", "운영", "평가", "검증", "유지보수", "기록"],
}

GENERIC_FIELD_POINTS = {
    "정격",
    "손실",
    "발열",
    "파형",
    "보호회로",
    "효율",
}

MOJIBAKE_PATTERNS = [
    chr(0x00C3), chr(0x00C2), chr(0x00ED), chr(0x00EC), chr(0x00EB), chr(0x00F0), chr(0xFFFD),
]

MARKDOWN_LEAK_PATTERNS = [
    r"^#{1,6}\s+",
    r"```",
    r"^\s*[-*]\s*$",
]

BROAD_TRIGGER_WARNINGS = {
    "flowmeter_dp_orifice": ["초음파유량계", "초음파 유량계", "도플러", "도플러 유량계", "Doppler", "doppler", "ultrasonic flowmeter"],
    "pressure_dp_transmitter": ["압력", "pressure"],
    "industrial_communication_protocol": ["통신", "산업통신", "무선통신"],
}

TECHNICAL_MUST_TERMS = {
    "vibration_measurement_condition_monitoring": [
        ["변위", "shaft"],
        ["속도", "housing"],
        ["가속도", "bearing"],
        ["trip", "monitoring"],
    ],
    "doppler_effect_velocity_flow_measurement": [
        ["접근", "증가"],
        ["이격", "감소"],
        ["입자", "기포"],
        ["transit", "Doppler"],
    ],
    "adc_dac_signal_conversion_interface": [
        ["표본화", "양자화", "부호화"],
        ["디코딩", "가중", "필터"],
        ["해상도", "정확도"],
        ["오프셋", "이득", "비선형", "지터"],
    ],
    "temperature_sensor_thermowell_material_selection": [
        ["thermowell", "보호관"],
        ["재질", "부식"],
        ["삽입", "응답"],
        ["wake", "진동"],
    ],
    "level_measurement_sensor_selection": [
        ["초음파", "플로트"],
        ["GWR", "가이드"],
        ["정전용량", "유전율"],
        ["거품", "증기", "방폭"],
    ],
    "continuous_discrete_control_model_comparison": [
        ["연속", "미분"],
        ["이산시간", "차분", "z"],
        ["이산사건", "event"],
        ["sampling", "aliasing", "위상"],
    ],
    "second_order_system_resonance_frequency_response": [
        ["전달함수", "2차"],
        ["주파수응답", "크기"],
        ["ωr", "wr", "공진"],
        ["ζ", "zeta", "1/√2", "1/sqrt"],
        ["overshoot", "resonance"],
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(flatten_text(x) for x in value)
    if isinstance(value, dict):
        return "\n".join(flatten_text(v) for v in value.values())
    return str(value)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def contains_any(text: str, terms: list[str]) -> bool:
    t = norm(text)
    return any(norm(term) in t for term in terms if term)


def count_terms(text: str, terms: list[str]) -> int:
    t = norm(text)
    return sum(1 for term in terms if term and norm(term) in t)


def text_fields_model(a: dict[str, Any]) -> str:
    parts = [
        a.get("title"),
        a.get("question_type"),
        a.get("topic_aliases"),
        a.get("question_examples"),
        a.get("expected_structure"),
        a.get("model_answer_outline"),
        a.get("high_score_features"),
        a.get("low_score_patterns"),
        a.get("field_connection_points"),
    ]
    return flatten_text(parts)


def text_fields_fact(t: dict[str, Any]) -> str:
    parts = [
        t.get("name"),
        t.get("aliases"),
        t.get("triggers"),
        t.get("anchors"),
    ]
    return flatten_text(parts)


def anchor_text(anchor: dict[str, Any]) -> str:
    return flatten_text([
        anchor.get("name"),
        anchor.get("expected"),
        anchor.get("core_terms"),
        anchor.get("support_terms"),
    ])


def has_mojibake(text: str) -> bool:
    return any(x in text for x in MOJIBAKE_PATTERNS)


def has_markdown_leak(value: Any) -> bool:
    if isinstance(value, str):
        return any(re.search(p, value) for p in MARKDOWN_LEAK_PATTERNS)
    if isinstance(value, list):
        return any(has_markdown_leak(v) for v in value)
    if isinstance(value, dict):
        return any(has_markdown_leak(v) for v in value.values())
    return False


def model_variants_by_topic(answers: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for a in answers:
        tid = a.get("topic_id")
        if tid:
            out[tid].append(a)
    return out


def fact_by_topic(topics: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {t.get("topic_id"): t for t in topics if t.get("topic_id")}


def classify_question_type_alignment(question_type: str, fact_topic_text: str, model_text: str) -> str:
    hints = QUESTION_TYPE_HINTS.get(question_type, [])
    if not hints:
        return "WARN: unknown question_type"
    score_fact = count_terms(fact_topic_text, hints)
    score_model = count_terms(model_text, hints)
    if score_fact >= 1 or score_model >= 1:
        return "OK"
    return "REVIEW: question_type lens not obvious from text"


def audit_topic(tid: str, models: list[dict[str, Any]], fact: dict[str, Any] | None) -> dict[str, Any]:
    row: dict[str, Any] = {
        "topic_id": tid,
        "model_variants": len(models),
        "fact_exists": bool(fact),
        "anchor_count": len(fact.get("anchors", [])) if fact else 0,
        "severity": "OK",
        "issues": [],
        "coverage_score": "",
        "anchor_coverage": "",
    }

    if not models:
        row["severity"] = "BLOCKER"
        row["issues"].append("model_answer 없음")
        return row
    if not fact:
        row["severity"] = "BLOCKER"
        row["issues"].append("fact_anchor 없음")
        return row

    model_text = flatten_text([text_fields_model(m) for m in models])
    fact_text = text_fields_fact(fact)
    combined = model_text + "\n" + fact_text

    if has_mojibake(combined):
        row["severity"] = "BLOCKER"
        row["issues"].append("mojibake 의심 문자 존재")

    if any(has_markdown_leak(m) for m in models) or has_markdown_leak(fact):
        row["severity"] = max_sev(row["severity"], "MAJOR")
        row["issues"].append("markdown heading/code fence 파싱 잔재 의심")

    anchors = fact.get("anchors", [])
    if len(anchors) != 5:
        row["severity"] = max_sev(row["severity"], "BLOCKER")
        row["issues"].append(f"anchor 개수 {len(anchors)}개")

    missing_anchor_fields = []
    for i, anchor in enumerate(anchors, start=1):
        for key in ["id", "name", "expected", "core_terms", "support_terms"]:
            if key not in anchor:
                missing_anchor_fields.append(f"F{i}.{key}")
    if missing_anchor_fields:
        row["severity"] = max_sev(row["severity"], "BLOCKER")
        row["issues"].append("anchor 필수 field 누락: " + ", ".join(missing_anchor_fields))

    short_expected = []
    keywordy_expected = []
    for i, anchor in enumerate(anchors, start=1):
        exp = str(anchor.get("expected", "")).strip()
        if len(exp) < 25:
            short_expected.append(f"F{i}")
        # comma/term-only style: too few Korean particles/sentence endings
        if exp and not any(x in exp for x in ["다.", "한다", "이다", "된다", "해야", "있다"]):
            keywordy_expected.append(f"F{i}")
    if short_expected:
        row["severity"] = max_sev(row["severity"], "MAJOR")
        row["issues"].append("expected가 너무 짧음: " + ", ".join(short_expected))
    if keywordy_expected:
        row["severity"] = max_sev(row["severity"], "MINOR")
        row["issues"].append("expected가 fact 문장보다 키워드 나열에 가까움: " + ", ".join(keywordy_expected))

    # Anchor coverage in model answer: core terms/support terms should appear in model text at least partially.
    covered = 0
    cover_details = []
    for i, anchor in enumerate(anchors, start=1):
        core_terms = anchor.get("core_terms", []) or []
        support_terms = anchor.get("support_terms", []) or []
        core_hit = count_terms(model_text, core_terms)
        support_hit = count_terms(model_text, support_terms)
        total_core = len([x for x in core_terms if x])
        ok = (total_core == 0 and support_hit > 0) or (total_core > 0 and core_hit >= max(1, min(2, total_core)))
        if ok:
            covered += 1
            cover_details.append(f"F{i}:OK")
        else:
            cover_details.append(f"F{i}:LOW(core {core_hit}/{total_core}, support {support_hit})")
    row["coverage_score"] = f"{covered}/{len(anchors)}" if anchors else "0/0"
    row["anchor_coverage"] = "; ".join(cover_details)

    if anchors and covered < len(anchors):
        row["severity"] = max_sev(row["severity"], "MAJOR" if covered <= 3 else "MINOR")
        row["issues"].append("model_answer에서 일부 anchor core_terms 반영 약함")

    # Model high-score / field connection points should be represented by facts/triggers/anchors.
    model_points = []
    for m in models:
        model_points.extend(m.get("field_connection_points", []) or [])
        model_points.extend(m.get("high_score_features", []) or [])
    weak_points = []
    fact_text_norm = norm(fact_text)
    for p in model_points:
        p = str(p).strip()
        if len(p) < 2:
            continue
        # long full sentence high_score_features should not require exact match.
        # Use key nouns only by splitting.
        tokens = [x for x in re.split(r"[\s,·/()]+", p) if len(x) >= 2]
        tokens = tokens[:4]
        if tokens and not any(norm(tok) in fact_text_norm for tok in tokens):
            weak_points.append(p[:35])
    if len(weak_points) >= 5:
        row["severity"] = max_sev(row["severity"], "MINOR")
        row["issues"].append("model high_score/field point 일부가 anchor에 약하게 반영됨")

    # Generic field point warning.
    for m in models:
        fps = set(map(str, m.get("field_connection_points", []) or []))
        generic_hits = sorted(fps & GENERIC_FIELD_POINTS)
        if generic_hits and not any(key in tid for key in ["motor", "inverter", "semiconductor", "converter", "rectifier", "chopper"]):
            row["severity"] = max_sev(row["severity"], "MAJOR")
            row["issues"].append("비전력전자 topic에 generic field_connection_points 존재: " + ", ".join(generic_hits))

    # Broad trigger warnings.
    bad_triggers = []
    triggers = fact.get("triggers", []) or []
    for warning_topic, bad_terms in BROAD_TRIGGER_WARNINGS.items():
        if tid == warning_topic:
            broad_terms = {norm(x) for x in bad_terms}
            for tr in triggers:
                # Exact-match only: avoid false positives such as "압력전송기" matching broad term "압력",
                # or "산업용 통신 프로토콜" matching broad term "통신".
                if norm(str(tr)) in broad_terms:
                    bad_triggers.append(str(tr))
    if bad_triggers:
        row["severity"] = max_sev(row["severity"], "MAJOR")
        row["issues"].append("오라우팅 위험 trigger: " + ", ".join(sorted(set(bad_triggers))))

    # Question type relation.
    qtypes = sorted(set(str(m.get("question_type")) for m in models if m.get("question_type")))
    qtype_notes = []
    for q in qtypes:
        note = classify_question_type_alignment(q, fact_text, model_text)
        if note != "OK":
            qtype_notes.append(f"{q}: {note}")
    if qtype_notes:
        row["severity"] = max_sev(row["severity"], "MINOR")
        row["issues"].append("question_type/anchor lens 점검 필요: " + "; ".join(qtype_notes))

    # Technical must-term audit for high-risk topics.
    must_groups = TECHNICAL_MUST_TERMS.get(tid, [])
    missing_groups = []
    for group in must_groups:
        # Each group is satisfied if any term in group appears in combined text.
        if not contains_any(combined, group):
            missing_groups.append("/".join(group))
    if missing_groups:
        row["severity"] = max_sev(row["severity"], "MAJOR")
        row["issues"].append("중점 기술 개념 누락 의심: " + ", ".join(missing_groups))

    if not row["issues"]:
        row["issues"].append("OK")

    return row


SEV_RANK = {"OK": 0, "MINOR": 1, "MAJOR": 2, "BLOCKER": 3}


def max_sev(a: str, b: str) -> str:
    return a if SEV_RANK.get(a, 0) >= SEV_RANK.get(b, 0) else b


def write_reports(rows: list[dict[str, Any]]) -> None:
    OUT_MD.parent.mkdir(exist_ok=True)
    OUT_CSV.parent.mkdir(exist_ok=True)

    fieldnames = [
        "severity",
        "topic_id",
        "model_variants",
        "fact_exists",
        "anchor_count",
        "coverage_score",
        "anchor_coverage",
        "issues",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            rr = dict(r)
            rr["issues"] = " | ".join(rr.get("issues", []))
            w.writerow({k: rr.get(k, "") for k in fieldnames})

    counts = Counter(r["severity"] for r in rows)
    md = []
    md.append("# Model Answer ↔ Fact Anchor Relationship Audit\n")
    md.append("## Summary\n")
    for sev in ["BLOCKER", "MAJOR", "MINOR", "OK"]:
        md.append(f"- {sev}: {counts.get(sev, 0)}")
    md.append("\n## Issues\n")
    md.append("| severity | topic_id | coverage | anchor_count | issues |")
    md.append("|---|---|---:|---:|---|")
    for r in sorted(rows, key=lambda x: (-SEV_RANK.get(x["severity"], 0), x["topic_id"])):
        issues = "<br>".join(r.get("issues", []))
        md.append(
            f"| {r['severity']} | `{r['topic_id']}` | {r.get('coverage_score','')} | {r.get('anchor_count','')} | {issues} |"
        )
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    model = load_json(MODEL_PATH)
    fact = load_json(FACT_PATH)

    answers = model.get("answers", [])
    topics = fact.get("topics", [])

    models = model_variants_by_topic(answers)
    facts = fact_by_topic(topics)

    all_topic_ids = sorted(set(models) | set(facts))
    rows = []
    for tid in all_topic_ids:
        rows.append(audit_topic(tid, models.get(tid, []), facts.get(tid)))

    write_reports(rows)

    print("=== Deep relationship audit ===")
    print(f"model topics: {len(models)}")
    print(f"fact topics : {len(facts)}")
    print(f"all topics  : {len(all_topic_ids)}")
    for sev in ["BLOCKER", "MAJOR", "MINOR", "OK"]:
        print(f"{sev}: {sum(1 for r in rows if r['severity'] == sev)}")

    print(f"\nWrote: {OUT_MD}")
    print(f"Wrote: {OUT_CSV}")

    print("\nTop issues:")
    for r in sorted(rows, key=lambda x: (-SEV_RANK.get(x["severity"], 0), x["topic_id"]))[:30]:
        if r["severity"] == "OK":
            continue
        print(f"- {r['severity']} {r['topic_id']} coverage={r.get('coverage_score')} :: " + " | ".join(r.get("issues", [])))

    if any(r["severity"] in {"BLOCKER", "MAJOR"} for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
