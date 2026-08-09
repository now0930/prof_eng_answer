#!/usr/bin/env python3
"""Compare normalized grading results with the 4-QType Production Golden contract.

This module intentionally does NOT execute Production grading.

Normalized result contract (one object per Golden case):
{
  "case_id": "QG-...",
  "question_type": "PRINCIPLE_INTERPRETATION",
  "topic_ids": ["topic_id"],
  "routing_mode": "SINGLE_TOPIC",
  "evidence_scope": "TOPIC_ONLY",
  "layer_scores": {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0},
  "total_score": 0.0,
  "coverage": 0.0,
  "fact_cap_applied": false,
  "critical_fact_error": false,
  "fatal_logic_error": false,
  "originality_axes": [],
  "feedback_elements": [],
  "feedback_characteristics": []
}

The input file may be a list of result objects, {"results": [...]}, a single
result object, or a mapping from case_id to result object.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

LAYER_NAMES = ("A", "B", "C", "D", "E")


class RunnerError(ValueError):
    """Golden inventory or normalized-result contract error."""


@dataclass(frozen=True)
class GoldenInventory:
    root: Path
    manifest: dict[str, Any]
    cases: dict[str, dict[str, Any]]
    qtype_counts: dict[str, int]
    expected_case_count: int
    missing_case_files: tuple[str, ...]


@dataclass(frozen=True)
class ComparisonReport:
    passed: bool
    golden_case_count: int
    result_case_count: int
    checked_case_count: int
    failures: tuple[str, ...]


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RunnerError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RunnerError(f"invalid JSON: {path}: {exc}") from exc


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RunnerError(f"{label}: expected object")
    return value


def load_golden_inventory(golden_root: Path, require_complete: bool = False) -> GoldenInventory:
    """Load manifest-driven Golden collections.

    Missing collection files are treated as empty only in inventory mode.
    Existing collections must be atomic: either 0 cases or required_case_count.
    """
    golden_root = Path(golden_root)
    manifest_obj = _load_json(golden_root / "manifest.json")
    manifest = dict(_require_mapping(manifest_obj, "manifest"))
    qtypes_obj = manifest.get("question_types")
    qtypes = _require_mapping(qtypes_obj, "manifest.question_types")

    cases: dict[str, dict[str, Any]] = {}
    counts: dict[str, int] = {}
    missing_files: list[str] = []
    expected_total = 0

    for qtype in sorted(qtypes):
        meta = _require_mapping(qtypes[qtype], f"manifest.question_types.{qtype}")
        case_file = meta.get("case_file")
        lane = meta.get("lane")
        required_count = meta.get("required_case_count")

        if not isinstance(case_file, str) or not case_file.strip():
            raise RunnerError(f"{qtype}: invalid case_file")
        if not isinstance(lane, str) or not lane.strip():
            raise RunnerError(f"{qtype}: invalid lane")
        if not isinstance(required_count, int) or isinstance(required_count, bool) or required_count <= 0:
            raise RunnerError(f"{qtype}: invalid required_case_count")

        expected_total += required_count
        path = golden_root / case_file
        if not path.is_file():
            counts[qtype] = 0
            missing_files.append(case_file)
            if require_complete:
                raise RunnerError(f"{qtype}: required case file missing: {case_file}")
            continue

        collection = _require_mapping(_load_json(path), f"{qtype} collection")
        if collection.get("question_type") != qtype:
            raise RunnerError(f"{qtype}: collection question_type mismatch")
        if collection.get("lane") != lane:
            raise RunnerError(f"{qtype}: collection lane mismatch")
        collection_cases = collection.get("cases")
        if not isinstance(collection_cases, list):
            raise RunnerError(f"{qtype}: collection cases must be list")

        count = len(collection_cases)
        counts[qtype] = count
        if require_complete:
            if count != required_count:
                raise RunnerError(f"{qtype}: expected {required_count} cases, found {count}")
        elif count not in {0, required_count}:
            raise RunnerError(
                f"{qtype}: inventory must be empty or atomic {required_count}-case collection, found {count}"
            )

        for index, raw_case in enumerate(collection_cases):
            case = dict(_require_mapping(raw_case, f"{qtype}.cases[{index}]"))
            case_id = case.get("case_id")
            if not isinstance(case_id, str) or not case_id.strip():
                raise RunnerError(f"{qtype}.cases[{index}]: invalid case_id")
            if case_id in cases:
                raise RunnerError(f"duplicate Golden case_id: {case_id}")
            if case.get("question_type") != qtype:
                raise RunnerError(f"{case_id}: Golden question_type mismatch")
            cases[case_id] = case

    if require_complete and len(cases) != expected_total:
        raise RunnerError(f"complete Golden Set requires {expected_total} cases, found {len(cases)}")

    return GoldenInventory(
        root=golden_root,
        manifest=manifest,
        cases=cases,
        qtype_counts=counts,
        expected_case_count=expected_total,
        missing_case_files=tuple(missing_files),
    )


def _normalize_result_sequence(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        raw_results = payload
    elif isinstance(payload, Mapping) and "results" in payload:
        raw_results = payload["results"]
        if not isinstance(raw_results, list):
            raise RunnerError("results: expected list")
    elif isinstance(payload, Mapping) and "case_id" in payload:
        raw_results = [payload]
    elif isinstance(payload, Mapping):
        raw_results = []
        for key, value in payload.items():
            item = dict(_require_mapping(value, f"result[{key}]"))
            embedded = item.get("case_id")
            if embedded is None:
                item["case_id"] = key
            elif embedded != key:
                raise RunnerError(f"result mapping key/case_id mismatch: {key} != {embedded}")
            raw_results.append(item)
    else:
        raise RunnerError("normalized result payload must be list or object")

    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_results):
        item = dict(_require_mapping(raw, f"results[{index}]"))
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise RunnerError(f"results[{index}]: invalid case_id")
        if case_id in seen:
            raise RunnerError(f"duplicate normalized result case_id: {case_id}")
        seen.add(case_id)
        results.append(item)
    return results


def load_normalized_results(path: Path) -> list[dict[str, Any]]:
    return _normalize_result_sequence(_load_json(Path(path)))


def _add_missing(failures: list[str], case_id: str, result: Mapping[str, Any], field: str) -> bool:
    if field not in result:
        failures.append(f"{case_id}:{field}:missing")
        return True
    return False


def _compare_scalar(
    failures: list[str],
    case_id: str,
    field: str,
    actual: Any,
    expected: Any,
) -> None:
    if actual != expected:
        failures.append(f"{case_id}:{field}:expected={expected!r}:actual={actual!r}")


def _compare_range(
    failures: list[str],
    case_id: str,
    field: str,
    actual: Any,
    expected_range: Any,
) -> None:
    if not _is_number(actual):
        failures.append(f"{case_id}:{field}:not-finite-number")
        return
    if not isinstance(expected_range, Mapping):
        failures.append(f"{case_id}:{field}:invalid-golden-range")
        return
    lo = expected_range.get("min")
    hi = expected_range.get("max")
    if not _is_number(lo) or not _is_number(hi):
        failures.append(f"{case_id}:{field}:invalid-golden-range")
        return
    value = float(actual)
    if not float(lo) <= value <= float(hi):
        failures.append(f"{case_id}:{field}:outside={float(lo)}..{float(hi)}:actual={value}")


def _as_string_set(
    failures: list[str],
    case_id: str,
    field: str,
    value: Any,
) -> set[str] | None:
    if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
        failures.append(f"{case_id}:{field}:expected-string-list")
        return None
    if len(value) != len(set(value)):
        failures.append(f"{case_id}:{field}:duplicate-values")
        return None
    return set(value)


def _compare_expectation_bool(
    failures: list[str],
    case_id: str,
    field: str,
    actual: Any,
    expectation: Any,
    positive_token: str,
    negative_token: str,
) -> None:
    if expectation == "NOT_APPLICABLE":
        return
    if not isinstance(actual, bool):
        failures.append(f"{case_id}:{field}:expected-bool")
        return
    if expectation == positive_token:
        expected_bool = True
    elif expectation == negative_token:
        expected_bool = False
    else:
        failures.append(f"{case_id}:{field}:unknown-golden-expectation={expectation!r}")
        return
    if actual is not expected_bool:
        failures.append(f"{case_id}:{field}:expected={expected_bool}:actual={actual}")


def compare_case(case: Mapping[str, Any], result: Mapping[str, Any]) -> list[str]:
    failures: list[str] = []
    case_id = str(case["case_id"])
    expected = case.get("expected")
    if not isinstance(expected, Mapping):
        return [f"{case_id}:expected:invalid-golden-object"]

    required_fields = (
        "question_type",
        "topic_ids",
        "routing_mode",
        "evidence_scope",
        "layer_scores",
        "total_score",
        "coverage",
        "originality_axes",
        "feedback_elements",
        "feedback_characteristics",
    )
    missing = {field for field in required_fields if _add_missing(failures, case_id, result, field)}

    if "question_type" not in missing:
        _compare_scalar(failures, case_id, "question_type", result["question_type"], case.get("question_type"))

    if "topic_ids" not in missing:
        actual_topics = _as_string_set(failures, case_id, "topic_ids", result["topic_ids"])
        golden_topics_raw = expected.get("expected_topic_ids")
        if actual_topics is not None:
            if not isinstance(golden_topics_raw, list) or not all(isinstance(x, str) for x in golden_topics_raw):
                failures.append(f"{case_id}:topic_ids:invalid-golden-topics")
            elif actual_topics != set(golden_topics_raw):
                failures.append(
                    f"{case_id}:topic_ids:expected={sorted(golden_topics_raw)!r}:actual={sorted(actual_topics)!r}"
                )

    if "routing_mode" not in missing:
        _compare_scalar(
            failures, case_id, "routing_mode", result["routing_mode"], expected.get("routing_mode")
        )
    if "evidence_scope" not in missing:
        _compare_scalar(
            failures, case_id, "evidence_scope", result["evidence_scope"], expected.get("evidence_scope")
        )

    if "layer_scores" not in missing:
        scores = result["layer_scores"]
        if not isinstance(scores, Mapping) or set(scores) != set(LAYER_NAMES):
            failures.append(f"{case_id}:layer_scores:must-have-exact-A-B-C-D-E")
        else:
            ranges = expected.get("layer_ranges")
            if not isinstance(ranges, Mapping):
                failures.append(f"{case_id}:layer_scores:invalid-golden-layer_ranges")
            else:
                for layer in LAYER_NAMES:
                    _compare_range(
                        failures, case_id, f"layer_scores.{layer}", scores[layer], ranges.get(layer)
                    )

    if "total_score" not in missing:
        _compare_range(failures, case_id, "total_score", result["total_score"], expected.get("total_range"))
    if "coverage" not in missing:
        _compare_range(failures, case_id, "coverage", result["coverage"], expected.get("coverage_range"))

    fact_expectation = expected.get("fact_cap_behavior")
    if fact_expectation != "NOT_APPLICABLE":
        if not _add_missing(failures, case_id, result, "fact_cap_applied"):
            _compare_expectation_bool(
                failures,
                case_id,
                "fact_cap_applied",
                result["fact_cap_applied"],
                fact_expectation,
                "CAP_EXPECTED",
                "NO_CAP_EXPECTED",
            )

    critical_expectation = expected.get("critical_fact_expectation")
    if critical_expectation != "NOT_APPLICABLE":
        if not _add_missing(failures, case_id, result, "critical_fact_error"):
            _compare_expectation_bool(
                failures,
                case_id,
                "critical_fact_error",
                result["critical_fact_error"],
                critical_expectation,
                "CRITICAL_ERROR_EXPECTED",
                "NO_CRITICAL_ERROR",
            )

    fatal_expectation = expected.get("fatal_logic_expectation")
    if fatal_expectation != "NOT_APPLICABLE":
        if not _add_missing(failures, case_id, result, "fatal_logic_error"):
            _compare_expectation_bool(
                failures,
                case_id,
                "fatal_logic_error",
                result["fatal_logic_error"],
                fatal_expectation,
                "FATAL_EXPECTED",
                "NO_FATAL",
            )

    if "originality_axes" not in missing:
        observed_axes = _as_string_set(failures, case_id, "originality_axes", result["originality_axes"])
        scope = expected.get("originality_scope")
        if observed_axes is not None:
            if not isinstance(scope, Mapping):
                failures.append(f"{case_id}:originality_axes:invalid-golden-scope")
            else:
                eligible = set(scope.get("eligible_axes", []))
                forbidden = set(scope.get("forbidden_axes", []))
                illegal = observed_axes - eligible
                forbidden_hits = observed_axes & forbidden
                if illegal:
                    failures.append(f"{case_id}:originality_axes:not-eligible={sorted(illegal)!r}")
                if forbidden_hits:
                    failures.append(f"{case_id}:originality_axes:forbidden={sorted(forbidden_hits)!r}")

    if "feedback_elements" not in missing:
        actual_elements = _as_string_set(
            failures, case_id, "feedback_elements", result["feedback_elements"]
        )
        scope = expected.get("feedback_scope")
        if actual_elements is not None:
            if not isinstance(scope, Mapping):
                failures.append(f"{case_id}:feedback_elements:invalid-golden-scope")
            else:
                required = set(scope.get("required_elements", []))
                forbidden = set(scope.get("forbidden_elements", []))
                absent = required - actual_elements
                hits = forbidden & actual_elements
                if absent:
                    failures.append(f"{case_id}:feedback_elements:missing-required={sorted(absent)!r}")
                if hits:
                    failures.append(f"{case_id}:feedback_elements:forbidden={sorted(hits)!r}")

    if "feedback_characteristics" not in missing:
        actual_chars = _as_string_set(
            failures, case_id, "feedback_characteristics", result["feedback_characteristics"]
        )
        if actual_chars is not None:
            required = set(expected.get("required_feedback_characteristics", []))
            forbidden = set(expected.get("forbidden_feedback", []))
            absent = required - actual_chars
            hits = forbidden & actual_chars
            if absent:
                failures.append(
                    f"{case_id}:feedback_characteristics:missing-required={sorted(absent)!r}"
                )
            if hits:
                failures.append(
                    f"{case_id}:feedback_characteristics:forbidden={sorted(hits)!r}"
                )

    return failures


def compare_inventory(
    inventory: GoldenInventory,
    normalized_results: Sequence[Mapping[str, Any]],
) -> ComparisonReport:
    failures: list[str] = []
    result_map: dict[str, Mapping[str, Any]] = {}

    for result in normalized_results:
        case_id = result.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            failures.append("<result>:case_id:missing-or-invalid")
            continue
        if case_id in result_map:
            failures.append(f"{case_id}:duplicate-result")
            continue
        result_map[case_id] = result

    golden_ids = set(inventory.cases)
    result_ids = set(result_map)

    for case_id in sorted(golden_ids - result_ids):
        failures.append(f"{case_id}:missing-result")
    for case_id in sorted(result_ids - golden_ids):
        failures.append(f"{case_id}:unexpected-result")

    checked = 0
    for case_id in sorted(golden_ids & result_ids):
        checked += 1
        failures.extend(compare_case(inventory.cases[case_id], result_map[case_id]))

    return ComparisonReport(
        passed=not failures,
        golden_case_count=len(golden_ids),
        result_case_count=len(result_ids),
        checked_case_count=checked,
        failures=tuple(failures),
    )


def _default_golden_root() -> Path:
    return Path(__file__).resolve().parents[1] / "calibration" / "qtype_golden"


def _print_inventory(inventory: GoldenInventory) -> None:
    print("MODE=INVENTORY")
    print(f"GOLDEN_CASES={len(inventory.cases)}")
    print(f"EXPECTED_CASES={inventory.expected_case_count}")
    counts = ",".join(f"{qtype}:{inventory.qtype_counts.get(qtype, 0)}" for qtype in sorted(inventory.qtype_counts))
    print(f"QTYPE_COUNTS={counts}")
    print(f"MISSING_CASE_FILES={len(inventory.missing_case_files)}")


def _write_json_report(path: Path, mode: str, inventory: GoldenInventory, report: ComparisonReport | None) -> None:
    payload: dict[str, Any] = {
        "mode": mode,
        "golden_case_count": len(inventory.cases),
        "expected_case_count": inventory.expected_case_count,
        "qtype_counts": inventory.qtype_counts,
        "missing_case_files": list(inventory.missing_case_files),
    }
    if report is not None:
        payload.update(
            {
                "passed": report.passed,
                "result_case_count": report.result_case_count,
                "checked_case_count": report.checked_case_count,
                "failures": list(report.failures),
            }
        )
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--golden-root",
        type=Path,
        default=_default_golden_root(),
        help="Golden contract directory (default: calibration/qtype_golden)",
    )
    parser.add_argument(
        "--results",
        type=Path,
        help="JSON file containing normalized grading result(s); omit for inventory mode",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="require every manifest QType collection to contain its full case count",
    )
    parser.add_argument("--json-report", type=Path, help="optional machine-readable report path")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        inventory = load_golden_inventory(args.golden_root, require_complete=args.require_complete)
        if args.results is None:
            _print_inventory(inventory)
            if args.json_report:
                _write_json_report(args.json_report, "INVENTORY", inventory, None)
            print("RESULT=PASS")
            return 0

        results = load_normalized_results(args.results)
        report = compare_inventory(inventory, results)
        print("MODE=COMPARE")
        print(f"GOLDEN_CASES={report.golden_case_count}")
        print(f"RESULT_CASES={report.result_case_count}")
        print(f"CHECKED_CASES={report.checked_case_count}")
        print(f"FAILURES={len(report.failures)}")
        for failure in report.failures:
            print(f"FAIL={failure}")
        if args.json_report:
            _write_json_report(args.json_report, "COMPARE", inventory, report)
        print(f"RESULT={'PASS' if report.passed else 'FAIL'}")
        return 0 if report.passed else 1
    except RunnerError as exc:
        print("RESULT=FAIL")
        print(f"ERROR={exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
