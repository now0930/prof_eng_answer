#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "calibration" / "qtype_golden"
MANIFEST_PATH = ROOT / "manifest.json"
SCHEMA_PATH = ROOT / "golden_case.schema.json"

ACTIVE_QTYPES = {
    "PRINCIPLE_INTERPRETATION": ("A", "PI", "cases/principle_interpretation.json"),
    "COMPARE_SELECTION": ("B", "CS", "cases/compare_selection.json"),
    "DIAGNOSIS_ACTION": ("C", "DA", "cases/diagnosis_action.json"),
    "IMPLEMENTATION_EVALUATION": ("D", "IE", "cases/implementation_evaluation.json"),
}
LEVELS = ("LOW", "PASS", "HIGH")
ROUTING_MODES = {"SINGLE_TOPIC", "MULTI_TOPIC", "GENERAL", "AMBIGUOUS"}
EVIDENCE_SCOPES = {
    "TOPIC_ONLY", "MULTI_TOPIC", "GENERAL_ONLY",
    "HYBRID_TOPIC_GENERAL", "AMBIGUOUS_FALLBACK",
}
DEMAND_STATUSES = {"present", "partial", "incorrect", "missing"}
ORIGINALITY_AXES = {"O1", "O2", "O3", "O4", "O5"}
LAYER_MAX = {"A": 3.0, "B": 6.0, "C": 8.0, "D": 6.0, "E": 2.0}


class ContractError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError(f"missing file: {path.relative_to(REPO)}") from exc
    except json.JSONDecodeError as exc:
        raise ContractError(
            f"invalid JSON: {path.relative_to(REPO)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        ) from exc


def validate_range(value: Any, minimum: float, maximum: float, label: str) -> tuple[float, float]:
    require(isinstance(value, dict), f"{label}: range must be object")
    require(set(value) == {"min", "max"}, f"{label}: range keys must be min/max")
    lo, hi = value["min"], value["max"]
    require(isinstance(lo, (int, float)) and not isinstance(lo, bool), f"{label}.min must be number")
    require(isinstance(hi, (int, float)) and not isinstance(hi, bool), f"{label}.max must be number")
    lo, hi = float(lo), float(hi)
    require(minimum <= lo <= hi <= maximum, f"{label}: invalid range {lo}..{hi}")
    return lo, hi


def validate_manifest() -> None:
    manifest = load_json(MANIFEST_PATH)
    require(manifest.get("version") == "qtype_golden_manifest_v1", "manifest version mismatch")
    require(manifest.get("state") == "COMPLETE_12_CASES", "manifest state mismatch")
    require(manifest.get("case_contract_version") == "qtype_golden_case_v1", "case contract mismatch")
    require(manifest.get("required_answer_levels") == list(LEVELS), "answer level mismatch")
    configured = manifest.get("question_types", {})
    require(set(configured) == set(ACTIVE_QTYPES), "manifest must define exactly 4 active QTypes")

    for qtype, (lane, short, rel_path) in ACTIVE_QTYPES.items():
        item = configured[qtype]
        require(item.get("lane") == lane, f"{qtype}: lane mismatch")
        require(item.get("short_code") == short, f"{qtype}: short code mismatch")
        require(item.get("case_file") == rel_path, f"{qtype}: case file mismatch")
        require(item.get("required_case_count") == 3, f"{qtype}: required count mismatch")

    require(manifest["score_policy"]["layer_max"] == LAYER_MAX, "layer max mismatch")
    require(float(manifest["score_policy"]["total_max"]) == 25.0, "total max mismatch")
    lanes = manifest["parallel_plan"]["lanes"]
    require(set(lanes) == {"A", "B", "C", "D", "E"}, "parallel lanes must be A~E")
    require(lanes["E"]["role"] == "REGRESSION_RUNNER", "Lane E role mismatch")


def validate_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    require(schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema", "schema draft mismatch")
    require(schema.get("title") == "4-QType Production Golden Case", "schema title mismatch")
    require(set(schema["properties"]["question_type"]["enum"]) == set(ACTIVE_QTYPES), "schema QType mismatch")


def validate_case(case: Any, qtype: str, short: str) -> None:
    top = {
        "case_id", "version", "question_type", "answer_level",
        "topic_id_basis", "question", "answer", "expected",
    }
    require(isinstance(case, dict) and set(case) == top, f"{qtype}: case keys mismatch")
    require(case["version"] == "qtype_golden_case_v1", "case version mismatch")
    require(case["question_type"] == qtype, "case QType mismatch")

    level = case["answer_level"]
    require(level in LEVELS, f"invalid answer level: {level}")
    case_id = case["case_id"]
    require(isinstance(case_id, str) and case_id.startswith(f"QG-{short}-{level}-"), "case id prefix mismatch")
    suffix = case_id.rsplit("-", 1)[-1]
    require(len(suffix) == 2 and suffix.isdigit(), "case id suffix must be two digits")

    for field in ("topic_id_basis", "question", "answer"):
        require(isinstance(case[field], str) and case[field].strip(), f"{case_id}: empty {field}")

    expected = case["expected"]
    keys = {
        "question_demands", "demand_status", "expected_topic_ids",
        "routing_mode", "evidence_scope", "layer_ranges", "total_range",
        "coverage_range", "fact_cap_behavior", "critical_fact_expectation",
        "fatal_logic_expectation", "originality_scope", "feedback_scope",
        "required_feedback_characteristics", "forbidden_feedback",
    }
    require(isinstance(expected, dict) and set(expected) == keys, f"{case_id}: expected keys mismatch")

    demands = expected["question_demands"]
    require(isinstance(demands, list) and demands, f"{case_id}: demands required")
    demand_ids = []
    for demand in demands:
        require(isinstance(demand, dict) and set(demand) == {"id", "text", "is_core"}, f"{case_id}: demand keys")
        require(isinstance(demand["id"], str) and demand["id"].strip(), f"{case_id}: demand id")
        require(isinstance(demand["text"], str) and demand["text"].strip(), f"{case_id}: demand text")
        require(isinstance(demand["is_core"], bool), f"{case_id}: demand is_core")
        demand_ids.append(demand["id"])
    require(len(demand_ids) == len(set(demand_ids)), f"{case_id}: duplicate demand id")

    statuses = expected["demand_status"]
    require(isinstance(statuses, dict) and set(statuses) == set(demand_ids), f"{case_id}: demand status keys")
    require(set(statuses.values()) <= DEMAND_STATUSES, f"{case_id}: invalid demand status")

    topics = expected["expected_topic_ids"]
    require(isinstance(topics, list), f"{case_id}: topics must be list")
    require(all(isinstance(x, str) and x.strip() for x in topics), f"{case_id}: invalid topic id")
    require(len(topics) == len(set(topics)), f"{case_id}: duplicate topic id")

    routing = expected["routing_mode"]
    evidence = expected["evidence_scope"]
    require(routing in ROUTING_MODES, f"{case_id}: invalid routing")
    require(evidence in EVIDENCE_SCOPES, f"{case_id}: invalid evidence scope")

    if routing == "SINGLE_TOPIC":
        require(len(topics) == 1, f"{case_id}: SINGLE_TOPIC requires one topic")
        require(evidence in {"TOPIC_ONLY", "HYBRID_TOPIC_GENERAL"}, f"{case_id}: SINGLE_TOPIC evidence")
    elif routing == "MULTI_TOPIC":
        require(len(topics) >= 2, f"{case_id}: MULTI_TOPIC requires >=2 topics")
        require(evidence in {"MULTI_TOPIC", "HYBRID_TOPIC_GENERAL"}, f"{case_id}: MULTI_TOPIC evidence")
    elif routing == "GENERAL":
        require(not topics and evidence == "GENERAL_ONLY", f"{case_id}: GENERAL contract")
    else:
        require(evidence == "AMBIGUOUS_FALLBACK", f"{case_id}: AMBIGUOUS contract")

    layers = expected["layer_ranges"]
    require(isinstance(layers, dict) and set(layers) == set(LAYER_MAX), f"{case_id}: layer ranges")
    min_sum = max_sum = 0.0
    for layer, maximum in LAYER_MAX.items():
        lo, hi = validate_range(layers[layer], 0.0, maximum, f"{case_id}.{layer}")
        min_sum += lo
        max_sum += hi

    total_lo, total_hi = validate_range(expected["total_range"], 0.0, 25.0, f"{case_id}.total")
    require(min_sum <= total_lo <= total_hi <= max_sum, f"{case_id}: total/layer range mismatch")

    if level == "LOW":
        require(total_hi < 15.0, f"{case_id}: LOW must be <15")
    elif level == "PASS":
        require(total_lo >= 15.0 and total_hi < 20.0, f"{case_id}: PASS must be [15,20)")
    else:
        require(total_lo >= 20.0 and total_hi <= 25.0, f"{case_id}: HIGH must be [20,25]")

    validate_range(expected["coverage_range"], 0.0, 100.0, f"{case_id}.coverage")

    require(expected["fact_cap_behavior"] in {"NO_CAP_EXPECTED", "CAP_EXPECTED", "NOT_APPLICABLE"}, "fact cap")
    require(expected["critical_fact_expectation"] in {"NO_CRITICAL_ERROR", "CRITICAL_ERROR_EXPECTED", "NOT_APPLICABLE"}, "critical fact")
    require(expected["fatal_logic_expectation"] in {"NO_FATAL", "FATAL_EXPECTED", "NOT_APPLICABLE"}, "fatal logic")

    originality = expected["originality_scope"]
    require(isinstance(originality, dict) and set(originality) == {"eligible_axes", "forbidden_axes"}, "originality scope")
    eligible = set(originality["eligible_axes"])
    forbidden = set(originality["forbidden_axes"])
    require(eligible <= ORIGINALITY_AXES and forbidden <= ORIGINALITY_AXES, "originality axes")
    require(eligible.isdisjoint(forbidden), "originality overlap")
    require(eligible | forbidden == ORIGINALITY_AXES, "O1~O5 must all be classified")

    feedback = expected["feedback_scope"]
    require(isinstance(feedback, dict) and set(feedback) == {"required_elements", "forbidden_elements"}, "feedback scope")
    for field in ("required_elements", "forbidden_elements"):
        values = feedback[field]
        require(isinstance(values, list), f"{case_id}: feedback {field}")
        require(all(isinstance(x, str) and x.strip() for x in values), f"{case_id}: feedback {field} value")

    for field in ("required_feedback_characteristics", "forbidden_feedback"):
        values = expected[field]
        require(isinstance(values, list) and values, f"{case_id}: {field} must be non-empty")
        require(all(isinstance(x, str) and x.strip() for x in values), f"{case_id}: {field} value")


def validate_collection(qtype: str, require_complete: bool) -> int:
    lane, short, rel_path = ACTIVE_QTYPES[qtype]
    data = load_json(ROOT / rel_path)
    require(set(data) == {"version", "question_type", "lane", "cases"}, f"{qtype}: collection keys")
    require(data["version"] == "qtype_golden_collection_v1", f"{qtype}: collection version")
    require(data["question_type"] == qtype, f"{qtype}: collection QType")
    require(data["lane"] == lane, f"{qtype}: collection lane")
    cases = data["cases"]
    require(isinstance(cases, list), f"{qtype}: cases list")

    if require_complete:
        require(len(cases) == 3, f"{qtype}: complete Golden Set requires exactly 3 cases")
    else:
        require(len(cases) in {0, 3}, f"{qtype}: G0 empty or atomic 3-case result required")

    if cases:
        levels = [x.get("answer_level") if isinstance(x, dict) else None for x in cases]
        require(sorted(levels) == sorted(LEVELS), f"{qtype}: LOW/PASS/HIGH exactly once")
        seen = set()
        for case in cases:
            validate_case(case, qtype, short)
            require(case["case_id"] not in seen, f"{qtype}: duplicate case id")
            seen.add(case["case_id"])
    return len(cases)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--qtype", choices=sorted(ACTIVE_QTYPES))
    args = parser.parse_args()

    try:
        validate_manifest()
        validate_schema()
        selected = [args.qtype] if args.qtype else list(ACTIVE_QTYPES)
        counts = {q: validate_collection(q, args.require_complete) for q in selected}
    except ContractError as exc:
        print(f"QTYPE_GOLDEN_VALIDATION=FAIL: {exc}", file=sys.stderr)
        return 1

    print("QTYPE_GOLDEN_CONTRACT=PASS")
    print(f"REQUIRE_COMPLETE={'true' if args.require_complete else 'false'}")
    for q in selected:
        print(f"{q}_CASE_COUNT={counts[q]}")
    print("QTYPE_GOLDEN_COMPLETE=PASS" if args.require_complete else "QTYPE_GOLDEN_COLLECTION_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
