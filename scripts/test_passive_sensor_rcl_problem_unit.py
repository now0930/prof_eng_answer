#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPIC_ID = "passive_sensor_resistive_capacitive_inductive_transduction"
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID


def read_json(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    fact = read_json("fact_anchor.json")
    logic = read_json("logic_check.json")
    model = read_json("model_answer.json")
    importance = read_json("topic_importance.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = (
        ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"
    ).read_text(encoding="utf-8")

    for name, obj in (
        ("fact", fact),
        ("logic", logic),
        ("model", model),
        ("importance", importance),
    ):
        require(obj["topic_id"] == TOPIC_ID, f"{name} topic id mismatch")

    anchors = {row["id"]: row for row in fact["anchors"]}
    require(len(anchors) == 14, "Fact Anchor count drift")
    patterns = model["expected_question_patterns"]
    require(len(patterns) == 5, "expected question pattern count drift")
    require(
        model.get("question_examples") == [row["pattern"] for row in patterns],
        "question_examples must mirror expected patterns in order",
    )

    required = set().union(*(set(row["required_anchor_ids"]) for row in patterns))
    outline = set().union(
        *(set(row.get("anchor_refs", [])) for row in model["recommended_outline"])
    )
    require(required <= anchors.keys(), "unknown required anchor")
    require(outline == anchors.keys(), "outline must trace every Fact Anchor")
    unrequired = anchors.keys() - required
    require(
        unrequired == {"sensor_resistive_strain_gauge_factor"}
        and anchors["sensor_resistive_strain_gauge_factor"]["importance"] == "optional",
        "only the explicitly optional strain-gauge detail may remain outside question requirements",
    )

    aliases = set(model["routing_aliases"])
    forbidden_specific_aliases = {"strain gauge", "Wheatstone bridge", "LVDT"}
    require(
        not (aliases & forbidden_specific_aliases),
        "dedicated strain-gauge or LVDT terms must not route to the broad RCL pack",
    )
    for layer, names in (
        ("deterministic", logic["deterministic_checks"]["topic_aliases"]),
        ("semantic", logic["llm_profile"]["candidate_extraction"]["key_terms"]),
    ):
        normalized = {str(name).casefold() for name in names}
        require(
            not (normalized & forbidden_specific_aliases),
            f"dedicated terms leaked into {layer} candidate aliases",
        )

    truth_schema = logic["llm_profile"]["truth_schema"]
    require(len(truth_schema) == len(fact["anchors"]), "truth schema cardinality mismatch")
    for anchor, truth in zip(fact["anchors"], truth_schema):
        require(
            truth == f"[{anchor['id']}] {anchor['statement']}",
            f"truth schema must preserve anchor identity and statement: {anchor['id']}",
        )
    require(logic["deterministic_checks"]["enabled"] is False, "deterministic checks changed")
    require(len(fact["fatal_wrong_claims"]) == 8, "fatal contract count changed")
    require(
        all(row["severity"] == "fatal" for row in fact["fatal_wrong_claims"]),
        "fatal severity contract changed",
    )
    require(
        "strain_gauge_load_cell_wheatstone_bridge_temperature_compensation_error" in readme + sheet
        and "lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error" in readme + sheet,
        "specific sensor topic handoffs must remain documented",
    )
    require(
        any("전용 strain-gauge Topic" in item for item in logic["llm_profile"]["false_positive_cautions"]),
        "strain-gauge detail must not be a false-positive omission on generic RCL questions",
    )
    require(
        "내부 지식·문항 분류" in readme + sheet,
        "internal classification boundary must be documented",
    )
    require(
        all("패턴 " in point or "명시적으로 묻는 경우" in point for point in model["high_score_points"]),
        "high-score criteria must state question applicability",
    )
    require(
        all("패턴 " in point or "명시적으로 묻는 경우" in point for point in model["common_missing_points"]),
        "missing-point criteria must state question applicability",
    )
    require(
        all("패턴 " in point for point in importance["high_band_unlock_conditions"]),
        "importance unlock conditions must state question applicability",
    )

    print("PASS: passive RCL problem-unit contract")
    print(f"topic_id={TOPIC_ID}")
    print(f"anchors={len(anchors)}")
    print(f"required_union={len(required)}")
    print(f"patterns={len(patterns)}")
    print(f"routing_aliases={len(aliases)}")
    print("strain_gauge_and_lvdt_handoff=PASS")
    print("question_scope_and_example_parity=PASS")


if __name__ == "__main__":
    main()
