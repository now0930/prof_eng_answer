#!/usr/bin/env python3
"""
Rubric Bank content validator.

Scope:
- run existing validators
- check A/B/C/D/E scoring layer consistency
- check rater weight consistency
- check topic_id references across Rubric Bank files
- check question_type references in Model Answer Bank
- check Logic Check D/E policy at data level

This does not judge technical truth quality of each fact or model answer.
"""

from __future__ import annotations

from typing import Any

from validators.rubric_bank.common import (
    RUBRIC_PATHS,
    collection,
    duplicates,
    item_id,
    load_json,
    run_script,
    write_report,
)


EXPECTED_LAYERS = ["A", "B", "C", "D", "E"]
EXPECTED_TOTAL_POINTS = 25.0
TOL = 1e-6


EXISTING_VALIDATORS = [
    ("format", ["scripts/validate_rubric_bank_format.py"]),
    ("config", ["scripts/validate_config.py"]),
    ("question_type_profile", ["scripts/validate_question_type_profile.py"]),
    ("model_answer_bank", ["scripts/validate_model_answer_bank.py"]),
    ("fact_anchor_bank", ["scripts/validate_fact_anchor_bank.py"]),
    ("model_fact_consistency", ["scripts/validate_model_fact_consistency.py"]),
    ("topic_importance", ["scripts/rubric_manager.py", "validate-topic-importance"]),
    ("logic_check_bank", ["scripts/validate_logic_check_bank.py"]),
    ("logic_check_de_policy", ["scripts/validate_logic_check_de_policy.py"]),
    (
        "logic_check_de_claim_trust_regression",
        ["scripts/check_logic_check_de_claim_trust_regression.py"],
    ),
]


def add_error(errors: list[str], code: str, message: str) -> None:
    errors.append(f"{code}: {message}")


def add_warning(warnings: list[str], code: str, message: str) -> None:
    warnings.append(f"{code}: {message}")


def validate_existing_scripts(errors: list[str]) -> list[dict[str, Any]]:
    results = []

    for name, args in EXISTING_VALIDATORS:
        result = run_script(name, args)
        results.append(result)

        if not result["ok"]:
            add_error(
                errors,
                "existing_validator",
                f"{name} failed with returncode={result['returncode']}",
            )

    return results


def validate_scoring_model(
    scoring_model: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    layers = scoring_model.get("layers")

    if not isinstance(layers, list):
        add_error(errors, "scoring.layers", "layers must be list")
        return {}

    layer_ids = []
    total = 0.0

    for index, layer in enumerate(layers):
        if not isinstance(layer, dict):
            add_error(errors, "scoring.layers.item", f"layers[{index}] must be object")
            continue

        layer_id = item_id(layer, "id")
        if not layer_id:
            add_error(errors, "scoring.layers.id", f"layers[{index}] missing id")
            continue

        layer_ids.append(layer_id)

        points = layer.get("points")
        if not isinstance(points, (int, float)):
            add_error(errors, "scoring.layers.points", f"{layer_id} points must be numeric")
            continue

        total += float(points)

    if layer_ids != EXPECTED_LAYERS:
        add_error(
            errors,
            "scoring.layers.order",
            f"expected {EXPECTED_LAYERS}, got {layer_ids}",
        )

    if abs(total - EXPECTED_TOTAL_POINTS) > TOL:
        add_error(
            errors,
            "scoring.layers.total",
            f"layer points must sum to {EXPECTED_TOTAL_POINTS}, got {total}",
        )

    total_points = scoring_model.get("total_points")
    if not isinstance(total_points, (int, float)):
        add_error(errors, "scoring.total_points", "total_points must be numeric")
    elif abs(float(total_points) - EXPECTED_TOTAL_POINTS) > TOL:
        add_error(
            errors,
            "scoring.total_points",
            f"expected {EXPECTED_TOTAL_POINTS}, got {total_points}",
        )

    return {
        "layer_ids": layer_ids,
        "layer_points_total": total,
        "total_points": total_points,
    }


def validate_raters(
    scoring_model: dict[str, Any],
    rater_profile: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    raters = collection(rater_profile, "raters")
    rater_ids = []

    for index, rater in enumerate(raters):
        rater_id = item_id(rater, "id")
        if not rater_id:
            add_error(errors, "raters.id", f"raters[{index}] missing id")
            continue

        rater_ids.append(rater_id)

        primary_layers = rater.get("primary_layers") if isinstance(rater, dict) else None
        if not isinstance(primary_layers, list) or not primary_layers:
            add_error(
                errors,
                "raters.primary_layers",
                f"{rater_id} primary_layers must be non-empty list",
            )
        else:
            bad_layers = [x for x in primary_layers if x not in EXPECTED_LAYERS]
            if bad_layers:
                add_error(
                    errors,
                    "raters.primary_layers",
                    f"{rater_id} has unknown primary_layers: {bad_layers}",
                )

    weights_by_layer = scoring_model.get("rater_weights_by_layer")
    if not isinstance(weights_by_layer, dict):
        add_error(errors, "rater_weights", "rater_weights_by_layer must be object")
        return {"rater_ids": rater_ids}

    for layer_id in EXPECTED_LAYERS:
        weights = weights_by_layer.get(layer_id)
        if not isinstance(weights, dict):
            add_error(errors, "rater_weights.layer", f"{layer_id} weights missing")
            continue

        total = 0.0
        for rater_id, weight in weights.items():
            if rater_id not in rater_ids:
                add_error(
                    errors,
                    "rater_weights.rater",
                    f"{layer_id} has unknown rater {rater_id}",
                )

            if not isinstance(weight, (int, float)):
                add_error(
                    errors,
                    "rater_weights.value",
                    f"{layer_id}.{rater_id} must be numeric",
                )
                continue

            total += float(weight)

        if abs(total - 1.0) > TOL:
            add_error(
                errors,
                "rater_weights.sum",
                f"{layer_id} weights sum must be 1.0, got {total}",
            )

    return {"rater_ids": rater_ids}


def validate_question_types(
    question_type_profile: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    types = question_type_profile.get("types")
    if not isinstance(types, dict) or not types:
        add_error(errors, "question_types.types", "types must be non-empty object")
        active_types = set()
    else:
        active_types = set(types.keys())

    fallback_type = question_type_profile.get("fallback_type")
    if isinstance(fallback_type, str) and fallback_type not in active_types:
        add_error(
            errors,
            "question_types.fallback_type",
            f"unknown fallback_type {fallback_type}",
        )

    legacy_mapping = question_type_profile.get("legacy_mapping")
    legacy_types = set()

    if isinstance(legacy_mapping, dict):
        legacy_types = set(legacy_mapping.keys())

        for legacy, target in legacy_mapping.items():
            if isinstance(target, str) and target not in active_types:
                add_error(
                    errors,
                    "question_types.legacy_mapping",
                    f"{legacy} maps to unknown active type {target}",
                )
    else:
        add_error(errors, "question_types.legacy_mapping", "legacy_mapping must be object")

    return {
        "active_types": sorted(active_types),
        "legacy_types": sorted(legacy_types),
    }


def validate_fact_topics(
    fact_anchor_bank: dict[str, Any],
    errors: list[str],
) -> set[str]:
    topics = collection(fact_anchor_bank, "topics")
    topic_ids = []

    for index, topic in enumerate(topics):
        topic_id = item_id(topic, "topic_id")
        if not topic_id:
            add_error(errors, "fact_topics.topic_id", f"topics[{index}] missing topic_id")
            continue

        topic_ids.append(topic_id)

    dup = duplicates(topic_ids)
    if dup:
        add_error(errors, "fact_topics.duplicate", f"duplicate topic_id: {dup}")

    return set(topic_ids)


def validate_model_answers(
    model_answer_bank: dict[str, Any],
    fact_topic_ids: set[str],
    active_types: set[str],
    legacy_types: set[str],
    errors: list[str],
) -> dict[str, Any]:
    answers = collection(model_answer_bank, "answers")
    answer_ids = []
    used_topics = []
    used_question_types = []

    for index, answer in enumerate(answers):
        answer_id = item_id(answer, "id") or f"answers[{index}]"
        answer_ids.append(answer_id)

        topic_id = item_id(answer, "topic_id")
        if not topic_id:
            add_error(errors, "model_answers.topic_id", f"{answer_id} missing topic_id")
        elif topic_id not in fact_topic_ids:
            add_error(errors, "model_answers.topic_id", f"{answer_id} unknown topic_id {topic_id}")
        else:
            used_topics.append(topic_id)

        question_type = item_id(answer, "question_type")
        if not question_type:
            add_error(errors, "model_answers.question_type", f"{answer_id} missing question_type")
        elif question_type not in active_types and question_type not in legacy_types:
            add_error(
                errors,
                "model_answers.question_type",
                f"{answer_id} unknown question_type {question_type}",
            )
        else:
            used_question_types.append(question_type)

    dup = duplicates(answer_ids)
    if dup:
        add_error(errors, "model_answers.duplicate_id", f"duplicate id: {dup}")

    return {
        "answers": len(answers),
        "unique_topics": len(set(used_topics)),
        "question_types": sorted(set(used_question_types)),
    }


def validate_topic_importance(
    topic_importance: dict[str, Any],
    fact_topic_ids: set[str],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    topics = collection(topic_importance, "topics")
    topic_ids = []
    umbrella_topics = []

    for index, topic in enumerate(topics):
        topic_id = item_id(topic, "topic_id")
        if not topic_id:
            add_error(errors, "topic_importance.topic_id", f"topics[{index}] missing topic_id")
            continue

        topic_ids.append(topic_id)

        # Topic Importance may contain umbrella/strategy topics that are broader
        # than a single Fact Anchor topic. Existing validate-topic-importance
        # allows this, so content validation reports it as a warning only.
        if topic_id not in fact_topic_ids:
            umbrella_topics.append(topic_id)
            add_warning(
                warnings,
                "topic_importance.topic_id",
                f"{topic_id} is not a fact_anchor topic_id; treated as umbrella/strategy topic",
            )

    dup = duplicates(topic_ids)
    if dup:
        add_error(errors, "topic_importance.duplicate", f"duplicate topic_id: {dup}")

    return {
        "topics": len(topics),
        "unique_topics": len(set(topic_ids)),
        "umbrella_topics": sorted(set(umbrella_topics)),
    }


def count_de_affected_layers(value: Any) -> int:
    count = 0

    if isinstance(value, dict):
        layers = value.get("affected_layers")
        if isinstance(layers, list) and ("D" in layers or "E" in layers):
            count += 1

        for child in value.values():
            count += count_de_affected_layers(child)

    elif isinstance(value, list):
        for child in value:
            count += count_de_affected_layers(child)

    return count


def validate_logic_checks(
    logic_check_bank: dict[str, Any],
    fact_topic_ids: set[str],
    errors: list[str],
) -> tuple[dict[str, Any], set[str]]:
    checks = collection(logic_check_bank, "topic_logic_checks")
    topic_ids = []
    de_affected_count = count_de_affected_layers(logic_check_bank)

    for index, check in enumerate(checks):
        topic_id = item_id(check, "topic_id")
        if not topic_id:
            add_error(
                errors,
                "logic_checks.topic_id",
                f"topic_logic_checks[{index}] missing topic_id",
            )
            continue

        topic_ids.append(topic_id)

        if topic_id not in fact_topic_ids:
            add_error(errors, "logic_checks.topic_id", f"unknown topic_id {topic_id}")

        trust = check.get("de_claim_trust") if isinstance(check, dict) else None
        if not isinstance(trust, dict):
            add_error(errors, "logic_checks.de_claim_trust", f"{topic_id} missing de_claim_trust")
        else:
            if trust.get("score_effect") != "none":
                add_error(
                    errors,
                    "logic_checks.de_claim_trust.score_effect",
                    f"{topic_id} score_effect must be none",
                )
            if trust.get("target_layers") != ["D", "E"]:
                add_error(
                    errors,
                    "logic_checks.de_claim_trust.target_layers",
                    f"{topic_id} target_layers must be ['D', 'E']",
                )

    dup = duplicates(topic_ids)
    if dup:
        add_error(errors, "logic_checks.duplicate", f"duplicate topic_id: {dup}")

    if de_affected_count:
        add_error(
            errors,
            "logic_checks.affected_layers",
            f"D/E affected_layers count={de_affected_count}",
        )

    return {
        "topics": len(checks),
        "unique_topics": len(set(topic_ids)),
        "affected_de_count": de_affected_count,
    }, set(topic_ids)


def validate_logic_profiles(
    logic_check_profile: dict[str, Any],
    fact_topic_ids: set[str],
    logic_topic_ids: set[str],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    profiles = collection(logic_check_profile, "profiles")
    topic_ids = []

    for index, profile in enumerate(profiles):
        topic_id = item_id(profile, "topic_id")
        if not topic_id:
            add_error(
                errors,
                "logic_profiles.topic_id",
                f"profiles[{index}] missing topic_id",
            )
            continue

        topic_ids.append(topic_id)

        if topic_id not in fact_topic_ids:
            add_error(errors, "logic_profiles.topic_id", f"unknown topic_id {topic_id}")

        if logic_topic_ids and topic_id not in logic_topic_ids:
            add_warning(
                warnings,
                "logic_profiles.topic_id",
                f"{topic_id} has profile but no matching logic_check_bank topic",
            )

    dup = duplicates(topic_ids)
    if dup:
        add_error(errors, "logic_profiles.duplicate", f"duplicate topic_id: {dup}")

    return {
        "profiles": len(profiles),
        "unique_topics": len(set(topic_ids)),
    }


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    data = {
        name: load_json(path)
        for name, path in RUBRIC_PATHS.items()
    }

    existing_results = validate_existing_scripts(errors)

    scoring_summary = validate_scoring_model(data["scoring_model"], errors)
    rater_summary = validate_raters(
        data["scoring_model"],
        data["rater_profile"],
        errors,
    )
    qtype_summary = validate_question_types(data["question_type_profile"], errors)

    fact_topic_ids = validate_fact_topics(data["fact_anchor_bank"], errors)

    model_summary = validate_model_answers(
        data["model_answer_bank"],
        fact_topic_ids,
        set(qtype_summary["active_types"]),
        set(qtype_summary["legacy_types"]),
        errors,
    )

    topic_importance_summary = validate_topic_importance(
        data["topic_importance"],
        fact_topic_ids,
        errors,
        warnings,
    )

    logic_summary, logic_topic_ids = validate_logic_checks(
        data["logic_check_bank"],
        fact_topic_ids,
        errors,
    )

    profile_summary = validate_logic_profiles(
        data["logic_check_profile"],
        fact_topic_ids,
        logic_topic_ids,
        errors,
        warnings,
    )

    report = {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "existing_validators": existing_results,
        "summaries": {
            "scoring_model": scoring_summary,
            "rater_profile": rater_summary,
            "question_type_profile": qtype_summary,
            "fact_anchor_bank": {
                "topics": len(fact_topic_ids),
            },
            "model_answer_bank": model_summary,
            "topic_importance": topic_importance_summary,
            "logic_check_bank": logic_summary,
            "logic_check_profile": profile_summary,
        },
    }

    report_path = write_report("content_validation.json", report)

    if errors:
        print("INVALID: Rubric Bank content")
        for error in errors:
            print(f"- {error}")

        if warnings:
            print()
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")

        print(f"Wrote: {report_path}")
        return 1

    print("VALID: Rubric Bank content")
    print(f"- layers={scoring_summary.get('layer_ids')}")
    print(f"- total_points={scoring_summary.get('total_points')}")
    print(f"- raters={rater_summary.get('rater_ids')}")
    print(f"- question_types={qtype_summary.get('active_types')}")
    print(f"- fact_topics={len(fact_topic_ids)}")
    print(
        "- model_answers="
        f"{model_summary.get('answers')} "
        f"unique_topics={model_summary.get('unique_topics')}"
    )
    print(
        "- topic_importance="
        f"{topic_importance_summary.get('topics')} "
        f"unique_topics={topic_importance_summary.get('unique_topics')}"
    )
    print(
        "- logic_check_bank="
        f"{logic_summary.get('topics')} "
        f"affected_de_count={logic_summary.get('affected_de_count')}"
    )
    print(
        "- logic_check_profile="
        f"{profile_summary.get('profiles')} "
        f"unique_topics={profile_summary.get('unique_topics')}"
    )

    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")

    print(f"Wrote: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
