#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rubric_content.model_answers import (  # type: ignore
    load_model_answer_bank,
    save_model_answer_bank,
    question_type_ids,
    validate_model_answer_bank,
)
from rubric_content.fact_anchors import (  # type: ignore
    load_fact_anchor_bank,
    save_fact_anchor_bank,
    validate_fact_anchor_bank_data,
)

MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"
AUDIT_PATH = ROOT / "scripts/deep_model_fact_relationship_audit.py"

TARGET_COVERAGE_TOPICS = {
    "noise_grounding_surge",
    "smart_factory_iiot_digital_twin",
    "transfer_function_state_space",
}


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "backups"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{path.stem}.before_relationship_v2.{stamp}{path.suffix}"
    shutil.copy2(path, out)
    return out


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
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def count_terms(text: str, terms: list[str]) -> int:
    t = norm(text)
    return sum(1 for term in terms if term and norm(term) in t)


def topic_model_entries(model_bank: dict[str, Any], topic_id: str) -> list[dict[str, Any]]:
    return [
        a for a in model_bank.get("answers", [])
        if isinstance(a, dict) and a.get("topic_id") == topic_id
    ]


def topic_fact(fact_bank: dict[str, Any], topic_id: str) -> dict[str, Any] | None:
    return next(
        (
            t for t in fact_bank.get("topics", [])
            if isinstance(t, dict) and t.get("topic_id") == topic_id
        ),
        None,
    )


def model_text(entries: list[dict[str, Any]]) -> str:
    return flatten_text([
        [
            e.get("title"),
            e.get("expected_structure"),
            e.get("model_answer_outline"),
            e.get("high_score_features"),
            e.get("low_score_patterns"),
            e.get("field_connection_points"),
        ]
        for e in entries
    ])


def append_unique(entry: dict[str, Any], field: str, value: str) -> bool:
    arr = entry.get(field)
    if not isinstance(arr, list):
        arr = []
    if value not in arr:
        arr.append(value)
        entry[field] = arr
        return True
    return False


def append_unique_many(entry: dict[str, Any], field: str, values: list[str]) -> int:
    changed = 0
    for v in values:
        if v and append_unique(entry, field, v):
            changed += 1
    return changed


def support_terms(anchor: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    for k in ("core_terms", "support_terms"):
        v = anchor.get(k, [])
        if isinstance(v, list):
            terms.extend([str(x) for x in v if str(x).strip()])
    out = []
    for t in terms:
        if t not in out:
            out.append(t)
    return out


def reinforce_missing_anchor_coverage(model_bank: dict[str, Any], fact_bank: dict[str, Any]) -> int:
    changed = 0

    for tid in sorted(TARGET_COVERAGE_TOPICS):
        entries = topic_model_entries(model_bank, tid)
        fact = topic_fact(fact_bank, tid)
        if not entries or not fact:
            continue

        mtext = model_text(entries)
        anchors = fact.get("anchors", [])
        if not isinstance(anchors, list):
            continue

        missing_expected_sentences: list[str] = []
        missing_field_terms: list[str] = []

        for anchor in anchors:
            if not isinstance(anchor, dict):
                continue
            core = [str(x) for x in anchor.get("core_terms", []) if str(x).strip()]
            total_core = len(core)
            core_hit = count_terms(mtext, core)

            required = max(1, min(2, total_core)) if total_core else 0
            if total_core and core_hit < required:
                exp = str(anchor.get("expected", "")).strip()
                if exp:
                    missing_expected_sentences.append(exp)
                missing_field_terms.extend(support_terms(anchor))

        if missing_expected_sentences or missing_field_terms:
            for entry in entries:
                changed += append_unique_many(entry, "model_answer_outline", missing_expected_sentences)
                changed += append_unique_many(entry, "field_connection_points", missing_field_terms)
                changed += append_unique_many(entry, "revision_notes", [
                    "deep_relation_cleanup_v2: mirrored under-covered fact anchors into model answer outline/field points."
                ])

    return changed


def patch_audit_false_positive_rules() -> int:
    if not AUDIT_PATH.exists():
        print("SKIP: audit script not found:", AUDIT_PATH)
        return 0

    before = AUDIT_PATH.read_text(encoding="utf-8")
    after = before

    old = """            for tr in triggers:
                if contains_any(str(tr), bad_terms):
                    bad_triggers.append(str(tr))
"""
    new = """            broad_terms = {norm(x) for x in bad_terms}
            for tr in triggers:
                # Exact-match only: avoid false positives such as "압력전송기" matching broad term "압력",
                # or "산업용 통신 프로토콜" matching broad term "통신".
                if norm(str(tr)) in broad_terms:
                    bad_triggers.append(str(tr))
"""
    if old in after:
        after = after.replace(old, new)
    else:
        print("WARN: did not find old trigger-check block; audit script may already be patched.")

    old_dict = """BROAD_TRIGGER_WARNINGS = {
    "flowmeter_dp_orifice": ["초음파", "도플러", "Doppler", "ultrasonic"],
    "pressure_dp_transmitter": ["압력"],
    "industrial_communication_protocol": ["통신"],
}
"""
    new_dict = """BROAD_TRIGGER_WARNINGS = {
    "flowmeter_dp_orifice": ["초음파유량계", "초음파 유량계", "도플러", "도플러 유량계", "Doppler", "doppler", "ultrasonic flowmeter"],
    "pressure_dp_transmitter": ["압력", "pressure"],
    "industrial_communication_protocol": ["통신", "산업통신", "무선통신"],
}
"""
    if old_dict in after:
        after = after.replace(old_dict, new_dict)

    if after != before:
        backup(AUDIT_PATH)
        AUDIT_PATH.write_text(after, encoding="utf-8")
        return 1

    return 0


def main() -> int:
    if not MODEL_PATH.exists() or not FACT_PATH.exists():
        print("ERROR: run from repository root.", file=sys.stderr)
        return 2

    print("backup model:", backup(MODEL_PATH))
    print("backup fact :", backup(FACT_PATH))

    model_bank = load_model_answer_bank(MODEL_PATH)
    fact_bank = load_fact_anchor_bank(FACT_PATH)

    changed_model = reinforce_missing_anchor_coverage(model_bank, fact_bank)
    changed_audit = patch_audit_false_positive_rules()

    model_errors = validate_model_answer_bank(model_bank, allowed_types=question_type_ids())
    fact_errors = validate_fact_anchor_bank_data(fact_bank)

    if model_errors or fact_errors:
        print("\nINVALID before save")
        for err in model_errors:
            print("model:", err)
        for err in fact_errors:
            print("fact :", err)
        return 1

    save_model_answer_bank(model_bank, MODEL_PATH)
    save_fact_anchor_bank(fact_bank, FACT_PATH)

    print(f"changed_model_items={changed_model}")
    print(f"changed_audit_script={changed_audit}")

    print("\n=== validate-all ===")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rubric_manager.py"), "validate-all"],
        cwd=ROOT,
        text=True,
    )

    print("\n=== deep audit ===")
    audit = ROOT / "scripts/deep_model_fact_relationship_audit.py"
    if audit.exists():
        subprocess.run([sys.executable, str(audit)], cwd=ROOT, text=True)
    else:
        print("SKIP: no audit script")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
