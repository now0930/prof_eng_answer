#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

TOPIC_ID = "optical_laser_photoelectric_noncontact_measurement_tof_triangulation"
EXPECTED_QUESTION_TYPE = "PRINCIPLE_INTERPRETATION"
EXPECTED_DIFFICULTY = "FIELD_APPLICATION"
EXPECTED_SELECTION_IMPORTANCE = "NORMAL"

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "rubrics" / "topic_packs" / TOPIC_ID
SHEET = ROOT / "docs" / "topic_sheets" / f"{TOPIC_ID}.md"


def load(name: str) -> dict:
    return json.loads((PACK / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalized_alias(text: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", " ", text.casefold()).strip()


def main() -> None:
    fact = load("fact_anchor.json")
    logic = load("logic_check.json")
    model = load("model_answer.json")
    importance = load("topic_importance.json")
    readme = (PACK / "README.md").read_text(encoding="utf-8")
    sheet = SHEET.read_text(encoding="utf-8")

    # 1. File/schema/topic identity contract.
    require(fact["schema_version"] == "fact_anchor.v1", "fact schema")
    require(logic["schema_version"] == "topic_pack.logic_check.v1", "logic schema")
    require(model["schema_version"] == "topic_pack.model_answer.v1", "model schema")
    require(
        importance["schema_version"] == "topic_pack.topic_importance.v1",
        "importance schema",
    )
    for name, obj in (
        ("fact", fact),
        ("logic", logic),
        ("model", model),
        ("importance", importance),
    ):
        require(obj["topic_id"] == TOPIC_ID, f"{name} topic_id")

    # 2. Step-0 classification decision must stay consistent.
    require(
        fact["question_type_hint"] == EXPECTED_QUESTION_TYPE,
        "fact question type",
    )
    require(model["question_type"] == EXPECTED_QUESTION_TYPE, "model question type")
    require(
        importance["question_type"] == EXPECTED_QUESTION_TYPE,
        "importance question type",
    )
    require(
        importance["difficulty"] == EXPECTED_DIFFICULTY,
        "importance difficulty",
    )
    require(
        importance["selection_importance"] == EXPECTED_SELECTION_IMPORTANCE,
        "importance selection importance",
    )

    # 3. Fact Anchor cardinality and key mechanism coverage.
    anchors = fact["anchors"]
    require(len(anchors) == 26, "anchor count must remain 26")
    anchor_ids = [row["id"] for row in anchors]
    require(len(anchor_ids) == len(set(anchor_ids)), "anchor ids must be unique")
    anchor_by_id = {row["id"]: row for row in anchors}

    required_anchor_ids = {
        "optical_noncontact_measurement_chain",
        "photoelectric_conversion_principle",
        "photoelectric_through_beam_mode",
        "photoelectric_retroreflective_mode",
        "photoelectric_diffuse_reflective_mode",
        "photoelectric_intensity_boundary",
        "optical_direct_tof_round_trip",
        "optical_direct_tof_distance_equation",
        "optical_indirect_tof_phase_principle",
        "optical_itof_phase_ambiguity",
        "laser_triangulation_principle",
        "laser_triangulation_detector_coordinate",
        "laser_triangulation_calibration",
        "triangulation_range_resolution_tradeoff",
        "surface_reflectivity_color_effect",
        "specular_transparent_surface_error",
        "ambient_light_filtering",
        "laser_speckle_effect",
        "alignment_occlusion_geometry",
        "tof_timing_jitter_resolution",
        "detector_saturation_dynamic_range",
        "multipath_mixed_pixel_error",
        "calibration_reference_traceability",
        "accuracy_resolution_repeatability_boundary",
        "wavelength_material_selection",
        "optical_method_selection_tradeoff",
    }
    require(set(anchor_ids) == required_anchor_ids, "anchor set drift")

    dtof = anchor_by_id["optical_direct_tof_distance_equation"]["statement"]
    require("d=c·Δt/2" in dtof, "Direct ToF must preserve d=c·Δt/2")
    require("왕복" in dtof and "광" in dtof, "Direct ToF physical meaning missing")

    itof = anchor_by_id["optical_indirect_tof_phase_principle"]["statement"]
    require(
        "d=c·φ/(4πf_m)" in itof,
        "Indirect ToF representative phase equation missing",
    )
    ambiguity = anchor_by_id["optical_itof_phase_ambiguity"]["statement"]
    require("2π" in ambiguity and "비모호" in ambiguity, "iToF ambiguity missing")

    tri = anchor_by_id["laser_triangulation_principle"]["statement"]
    require(
        all(token in tri for token in ("기준선", "spot", "거리")),
        "triangulation geometry chain missing",
    )
    tri_cal = anchor_by_id["laser_triangulation_calibration"]["statement"]
    require("보정" in tri_cal and "기준선" in tri_cal, "triangulation calibration missing")

    # 4. Critical conceptual boundaries.
    photo_boundary = anchor_by_id["photoelectric_intensity_boundary"]["statement"]
    require("절대거리" in photo_boundary, "photoelectric absolute-distance boundary missing")
    surface = anchor_by_id["specular_transparent_surface_error"]["statement"]
    require(
        "투명" in surface and "다중" in surface,
        "transparent/specular optical error mechanism missing",
    )
    ambient = anchor_by_id["ambient_light_filtering"]["statement"]
    require(
        any(token in ambient for token in ("광학필터", "동기검파", "시간게이팅")),
        "ambient-light countermeasure missing",
    )
    perf = anchor_by_id["accuracy_resolution_repeatability_boundary"]["statement"]
    require(
        all(token in perf for token in ("분해능", "반복도", "정확도")),
        "performance-term boundary missing",
    )

    # 5. Fatal projection must remain exact-order and C-layer only.
    fatal = fact["fatal_wrong_claims"]
    require(len(fatal) == 14, "fatal count must remain 14")
    fatal_ids = [row["id"] for row in fatal]
    require(len(fatal_ids) == len(set(fatal_ids)), "fatal ids must be unique")
    require(
        all(row["severity"] == "fatal" for row in fatal),
        "all fact fatal rows must be fatal",
    )
    require(
        all(row["affected_layers"] == ["C"] for row in fatal),
        "fact fatal ownership must be C-only",
    )

    profile = logic["llm_profile"]
    require(
        profile["truth_schema"] == [row["statement"] for row in anchors],
        "truth_schema must be exact Fact Anchor projection",
    )
    require(
        len(profile["fatal_conditions"]) == len(fatal),
        "fatal projection cardinality mismatch",
    )
    for idx, row in enumerate(fatal):
        projected = profile["fatal_conditions"][idx]
        require(
            projected.startswith(f"[{row['id']}] "),
            f"fatal id/order projection mismatch at {row['id']}",
        )
        require(row["claim"] in projected, f"fatal claim projection missing: {row['id']}")
        require(
            row["correction"] in projected,
            f"fatal correction projection missing: {row['id']}",
        )

    fatal_text = "\n".join(row["claim"] for row in fatal)
    for required_wrong_claim in (
        "d=c·Δt",
        "음속",
        "거리 제한 없이",
        "삼각측량은 송신 펄스",
        "수광세기만 알면",
        "주변광의 영향을 전혀",
        "분해능 수치가 곧 절대 정확도",
        "다중경로 오차가 발생하지",
        "오염 점검이 필요 없다",
        "항상 최적",
    ):
        require(
            required_wrong_claim in fatal_text,
            f"missing fatal boundary: {required_wrong_claim}",
        )

    # 6. LLM-only semantic ownership contract.
    det = logic["deterministic_checks"]
    require(det["enabled"] is False, "deterministic semantic checks must stay disabled")
    require(det["fatal_checks"] == [], "deterministic fatal checks must stay empty")
    require(det["major_checks"] == [], "deterministic major checks must stay empty")
    require(
        det["question_type_checks"] == [],
        "deterministic question type checks must stay empty",
    )
    require(
        det["topic_aliases"] == [],
        "deterministic topic aliases intentionally remain empty for this LLM-only pack",
    )

    require(profile["enabled"] is True, "LLM profile must stay enabled")
    require(
        profile["candidate_extraction"]["rules"] == [],
        "candidate_extraction rules must stay empty",
    )
    require(
        profile["score_policy"]
        == {
            "direct_score_application": False,
            "direct_d_e_effect": "none",
            "affected_layers": ["C"],
        },
        "LLM score policy must remain C-only and non-direct",
    )
    require(len(profile["major_checks"]) == 10, "major check count drift")
    require(
        len(profile["false_positive_cautions"]) >= 10,
        "false-positive caution coverage too weak",
    )

    # 7. Model answer anchor reference integrity.
    anchor_set = set(anchor_ids)
    patterns = model["expected_question_patterns"]
    require(len(patterns) == 10, "question pattern count")
    for row in patterns:
        refs = set(row["required_anchor_ids"])
        require(refs, "question pattern without required anchors")
        require(refs <= anchor_set, f"unknown pattern anchor: {refs - anchor_set}")

    outline = model["recommended_outline"]
    require(len(outline) == 8, "outline section count")
    outline_union: set[str] = set()
    for row in outline:
        refs = set(row["anchor_refs"])
        require(refs <= anchor_set, f"unknown outline anchor: {refs - anchor_set}")
        outline_union |= refs
    require(outline_union == anchor_set, "outline must cover all Fact Anchors")

    # 8. Routing aliases must be specific enough and preserve ownership boundary.
    aliases = model["routing_aliases"]
    require(len(aliases) == 18, "routing alias count drift")
    forbidden_generic = {
        "laser",
        "광학",
        "센서",
        "sensor",
        "tof",
        "measurement",
        "측정",
        "비접촉",
    }
    normalized = [normalized_alias(alias) for alias in aliases]
    require(
        not (set(normalized) & forbidden_generic),
        "overly generic routing alias introduced",
    )
    require(
        any("triangulation" in alias.casefold() for alias in aliases),
        "triangulation alias coverage missing",
    )
    require(
        any("photoelectric" in alias.casefold() for alias in aliases),
        "photoelectric alias coverage missing",
    )
    require(
        any("tof" in alias.casefold() for alias in aliases),
        "optical ToF alias coverage missing",
    )

    # 9. Explicit cross-topic ownership handoff must remain in human-readable source.
    handoff_text = readme + "\n" + sheet
    require(
        "ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error"
        in handoff_text,
        "ultrasonic ownership handoff missing",
    )
    require(
        "radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error"
        in handoff_text,
        "radar ownership handoff missing",
    )
    require(
        "Laser triangulation" in handoff_text or "laser triangulation" in handoff_text,
        "laser triangulation human-readable scope missing",
    )

    # 10. Historical-frequency prohibition and no placeholder residue.
    all_text = "\n".join(
        [
            readme,
            sheet,
            json.dumps(fact, ensure_ascii=False),
            json.dumps(logic, ensure_ascii=False),
            json.dumps(model, ensure_ascii=False),
            json.dumps(importance, ensure_ascii=False),
        ]
    )
    require(
        "historical_frequency_used" in readme or "Historical frequency used" in readme,
        "historical-frequency policy not documented",
    )
    for forbidden in ("TODO", "TBD", "FIXME", "PLACEHOLDER"):
        require(forbidden not in all_text, f"placeholder residue: {forbidden}")

    print("PASS: optical/photoelectric/laser noncontact focused regression")
    print(f"topic_id={TOPIC_ID}")
    print(f"anchors={len(anchors)}")
    print(f"fatals={len(fatal)}")
    print(f"major_checks={len(profile['major_checks'])}")
    print(f"question_patterns={len(patterns)}")
    print(f"routing_aliases={len(aliases)}")
    print(f"question_type={importance['question_type']}")
    print(f"difficulty={importance['difficulty']}")
    print("semantic_execution=LLM_ONLY")
    print("deterministic_topic_aliases_empty=INTENTIONAL")
    print("historical_frequency_used=false")


if __name__ == "__main__":
    main()
