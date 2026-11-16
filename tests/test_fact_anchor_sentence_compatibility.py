"""Explicit, score-neutral compatibility for independently reviewed sentences."""

import copy
import hashlib
import json
from pathlib import Path

import pytest

import grading.evidence.cross_topic_question_contract as cross_topic
import grading.evidence.fact_anchor_evidence_adapter as adapter
from grading.evidence.fact_anchor_compatibility import (
    COMPATIBILITY_VERSION,
    scoring_anchor_view,
    scoring_topic_view,
    validate_sentence_compatibility,
)
from grading.evidence.logic_check_evaluator import _build_canonical_axis_context
from grading.evidence.fact_anchor_sentence_view import project_fact_anchor_sentences
from scripts.build_generated_rubrics import build_fact_anchors, load_topic_pack
from scripts.validate_topic_packs import validate_fact_anchor


TOPIC = "synthetic_compatibility_test"
REFERENCE = "센서 출력은 입력에 비례한다. 동작 범위와 입력 조건을 확인한다."
SHORT = "센서 출력은 입력에 비례한다."


def _anchors():
    legacy = {
        "id": "sensor_response", "anchor_id": "sensor_response",
        "statement": REFERENCE, "claim": REFERENCE, "description": REFERENCE,
        "expected": REFERENCE, "accepted_explanations": [REFERENCE, "별도 응답 근거를 확인한다."],
        "core_terms": ["센서 출력", "입력 비례"], "importance": "core",
    }
    concise = copy.deepcopy(legacy)
    for key in ("statement", "claim", "description"):
        concise[key] = SHORT
    concise["sentence_compatibility"] = {
        "version": COMPATIBILITY_VERSION,
        "reference_sha256": hashlib.sha256(REFERENCE.encode("utf-8")).hexdigest(),
    }
    return legacy, concise


def test_unmarked_anchor_is_unchanged_and_marked_view_preserves_baseline():
    old, short = _anchors()
    before = copy.deepcopy(short)
    assert scoring_anchor_view(old) is old
    assert scoring_anchor_view(short) == old
    assert short == before
    assert adapter._anchor_tokens(short) == adapter._anchor_tokens(old)


@pytest.mark.parametrize("mutation", ["reference", "digest", "prefix", "alias", "version", "shape"])
def test_invalid_compatibility_never_silently_restores_reference(mutation):
    _, anchor = _anchors()
    if mutation == "reference":
        anchor["expected"] = "다른 검증되지 않은 설명이다."
    elif mutation == "digest":
        anchor["sentence_compatibility"]["reference_sha256"] = "0" * 64
    elif mutation == "prefix":
        anchor["statement"] = "다른 사실이다."
    elif mutation == "alias":
        anchor["claim"] = "다른 주장이다."
    elif mutation == "version":
        anchor["sentence_compatibility"]["version"] = "other"
    else:
        anchor["sentence_compatibility"]["unreviewed"] = True
    # Invalid metadata never suppresses an axis or overrides its reference;
    # the existing Topic Pack validator rejects it before promotion.
    assert scoring_anchor_view(anchor) is anchor
    with pytest.raises(ValueError, match="Fact sentence compatibility"):
        validate_sentence_compatibility(anchor)
    unmarked = copy.deepcopy(anchor)
    unmarked.pop("sentence_compatibility")
    assert _build_canonical_axis_context({"fact_anchor": {"anchors": [anchor]}}) == (
        _build_canonical_axis_context({"fact_anchor": {"anchors": [unmarked]}})
    )


def test_scoring_context_keeps_legacy_axis_ids_and_distinct_claims():
    old, short = _anchors()
    independent = {
        "id": "sensor_limit", "anchor_id": "sensor_limit",
        "statement": "센서 허용 범위는 별도로 확인한다.",
        "accepted_explanations": ["센서 허용 범위는 별도로 확인한다."],
        "importance": "core",
    }
    old_axes = _build_canonical_axis_context({"fact_anchor": {"anchors": [old, independent]}})
    new_axes = _build_canonical_axis_context({"fact_anchor": {"anchors": [short, independent]}})
    assert old_axes == new_axes
    assert {axis["axis_id"] for axis in new_axes} >= {"sensor_response", "sensor_limit"}
    # A non-opted-in distinct statement must still produce its own axis.
    unmarked = copy.deepcopy(short)
    unmarked.pop("sentence_compatibility")
    assert len(_build_canonical_axis_context({"fact_anchor": {"anchors": [unmarked, independent]}})) > len(old_axes)


def test_existing_topic_validator_rejects_corrupt_opt_in_only(tmp_path):
    old, short = _anchors()
    pack = tmp_path / TOPIC
    pack.mkdir()
    path = pack / "fact_anchor.json"
    for anchor in (old, short):
        path.write_text(json.dumps({"topic_id": TOPIC, "anchors": [anchor]}, ensure_ascii=False), encoding="utf-8")
        assert validate_fact_anchor(pack, TOPIC, set()) == {"sensor_response"}
    short["sentence_compatibility"]["reference_sha256"] = "0" * 64
    path.write_text(json.dumps({"topic_id": TOPIC, "anchors": [short]}, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(SystemExit):
        validate_fact_anchor(pack, TOPIC, set())


def test_generated_topic_scoring_projection_keeps_original_context():
    old, short = _anchors()
    baseline = {"topic_id": TOPIC, "anchors": [old], "core_facts": [REFERENCE], "triggers": [REFERENCE]}
    concise = {"topic_id": TOPIC, "anchors": [short], "core_facts": [SHORT], "triggers": [REFERENCE]}
    snapshot = copy.deepcopy(concise)
    assert scoring_topic_view(concise) == baseline
    assert concise == snapshot


def test_question_demand_assets_keep_prior_anchor_text(tmp_path):
    from grading.routing.question_demand_evidence import _load_topic_assets

    old, short = _anchors()
    pack = tmp_path / "rubrics" / "topic_packs" / TOPIC
    pack.mkdir(parents=True)
    (pack / "model_answer.json").write_text("{}", encoding="utf-8")
    results = []
    for anchor in (old, short):
        (pack / "fact_anchor.json").write_text(
            json.dumps({"anchors": [anchor]}, ensure_ascii=False), encoding="utf-8"
        )
        results.append(_load_topic_assets(tmp_path, TOPIC))
    assert results[0] == results[1]


def test_duplicate_short_statement_is_rejected_before_promotion(tmp_path):
    _, short = _anchors()
    independent = {"id": "independent", "anchor_id": "independent", "statement": SHORT}
    topic = {"topic_id": TOPIC, "anchors": [short, independent], "core_facts": [SHORT]}
    assert scoring_topic_view(topic) is topic
    pack = tmp_path / TOPIC
    pack.mkdir()
    (pack / "fact_anchor.json").write_text(json.dumps(topic, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(SystemExit):
        validate_fact_anchor(pack, TOPIC, set())


def test_hybrid_and_multi_topic_contexts_keep_baseline_fact_evidence():
    from grading.evidence.hybrid_general_grading_context import build_hybrid_general_grading_context
    from grading.evidence.multi_topic_grading_context import build_multi_topic_grading_context
    from scripts.test_hybrid_general_grading_context import candidates, demands, semantic_hybrid, sources
    from scripts.test_multi_topic_grading_context import candidate_fixture, semantic_multi, source_fixture

    old, short = _anchors()
    hybrid = []
    multi = []
    for anchor in (old, short):
        hybrid_source = sources()
        hybrid_fact = hybrid_source["fact_anchor"]["topics"][0]
        hybrid_fact.update(anchors=[anchor], core_facts=[anchor["statement"]])
        hybrid.append(build_hybrid_general_grading_context(
            semantic_result=semantic_hybrid(), question_demand_result=demands(),
            shadow_candidate_result=candidates(), generated_sources=hybrid_source, enabled=True,
        ))
        multi_source = source_fixture()
        multi_fact = multi_source["fact_anchor"]["items"][0]
        multi_fact.update(anchors=[anchor], core_facts=[anchor["statement"]])
        multi.append(build_multi_topic_grading_context(
            semantic_result=semantic_multi(), shadow_candidate_result=candidate_fixture(),
            generated_sources=multi_source, enabled=True,
        ))
    assert hybrid[0]["applicable"] and multi[0]["applicable"]
    assert hybrid[0] == hybrid[1]
    assert multi[0] == multi[1]


def test_generated_routing_and_phase3_selection_match_baseline(monkeypatch):
    import grading_agents

    old, short = _anchors()
    old.pop("expected")  # The legacy source relied on generator fallback.
    base_pack = {
        "fact_anchor": {"topic_id": TOPIC, "title_ko": "센서 입력", "anchors": [old], "core_facts": [REFERENCE]},
        "model_answer": {"routing_aliases": ["센서 입력"]},
        "topic_importance": {},
    }
    new_pack = copy.deepcopy(base_pack)
    new_pack["fact_anchor"]["anchors"] = [short]
    new_pack["fact_anchor"]["core_facts"] = [SHORT]
    baseline = build_fact_anchors([base_pack], "test")
    concise = build_fact_anchors([new_pack], "test")
    original_topic, new_topic = baseline["topics"][0], concise["topics"][0]
    assert new_topic["triggers"] == original_topic["triggers"]
    assert new_topic["aliases"] == original_topic["aliases"]
    assert scoring_topic_view(new_topic) == original_topic
    question = "센서 입력 동작 범위와 입력 조건을 설명하시오."
    results = []
    for bank in (baseline, concise):
        monkeypatch.setattr(grading_agents, "_phase3_load_fact_anchor_bank", lambda *args, **kwargs: bank)
        results.append(grading_agents._phase3_select_fact_anchors_from_bank(question, ""))
    assert results[0] == results[1]


def test_all_reviewed_humidity_sentences_keep_original_scoring_projection(monkeypatch):
    import grading_agents
    from scripts.audit_fact_anchor_sentence_sync import REVIEWED_SENTENCES

    root = Path(__file__).resolve().parents[1]
    topic = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
    concise = load_topic_pack(root / "rubrics/topic_packs" / topic)
    baseline = copy.deepcopy(concise)
    for anchor in baseline["fact_anchor"]["anchors"]:
        if (topic, anchor.get("anchor_id")) not in REVIEWED_SENTENCES:
            continue
        short, reference = anchor["statement"], anchor.pop("expected")
        anchor.pop("sentence_compatibility")
        for key in ("statement", "claim", "description"):
            anchor[key] = reference
        core = baseline["fact_anchor"]["core_facts"]
        core[:] = [reference if value == short else value for value in core]
    banks = [build_fact_anchors([pack], "fixture") for pack in (baseline, concise)]
    assert scoring_topic_view(banks[0]["topics"][0]) == scoring_topic_view(banks[1]["topics"][0])
    results = []
    for bank in banks:
        monkeypatch.setattr(grading_agents, "_phase3_load_fact_anchor_bank", lambda *args, **kwargs: bank)
        results.append(grading_agents._phase3_select_fact_anchors_from_bank(
            "Subzero moisture specification에서 frost point 계산 기준을 설명하시오.", ""))
    assert results[0] == results[1]


def test_reviewed_relative_humidity_example_preserves_scoring_projection():
    root = Path(__file__).resolve().parents[1]
    topic = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
    original = load_topic_pack(root / "rubrics/topic_packs" / topic)
    manifest = json.loads((root / "calibration/fact_anchor_simplification_review_20261114.json").read_text(encoding="utf-8"))
    reference = next(row["previous_statement"] for row in manifest["entries"]
                     if (row["topic_id"], row["anchor_id"]) == (topic, "relative_humidity_definition"))
    original_anchor = next(row for row in original["fact_anchor"]["anchors"]
                           if row["anchor_id"] == "relative_humidity_definition")
    current_statement = original_anchor["statement"]
    for key in ("statement", "claim", "description"):
        original_anchor[key] = reference
    original_anchor.pop("expected", None)
    original_anchor.pop("sentence_compatibility", None)
    core = original["fact_anchor"]["core_facts"]
    core[core.index(current_statement)] = reference
    new = copy.deepcopy(original)
    anchor = next(row for row in new["fact_anchor"]["anchors"]
                  if row["anchor_id"] == "relative_humidity_definition")
    short = reference.split(". ", 1)[0] + "."
    assert anchor["accepted_explanations"][0] == reference
    for key in ("statement", "claim", "description"):
        anchor[key] = short
    anchor["expected"] = reference
    anchor["sentence_compatibility"] = {
        "version": COMPATIBILITY_VERSION,
        "reference_sha256": hashlib.sha256(reference.encode("utf-8")).hexdigest(),
    }
    core = new["fact_anchor"]["core_facts"]
    core[core.index(reference)] = short
    baseline_bank = build_fact_anchors([original], "fixture")
    concise_bank = build_fact_anchors([new], "fixture")
    baseline_topic, concise_topic = baseline_bank["topics"][0], concise_bank["topics"][0]
    assert concise_topic["triggers"] == baseline_topic["triggers"]
    assert concise_topic["aliases"] == baseline_topic["aliases"]
    assert scoring_topic_view(concise_topic) == scoring_topic_view(baseline_topic)
    original_anchor = next(row for row in original["fact_anchor"]["anchors"]
                           if row["anchor_id"] == anchor["anchor_id"])
    assert adapter._anchor_tokens(anchor) == adapter._anchor_tokens(original_anchor)
    assert _build_canonical_axis_context({"fact_anchor": {"anchors": [anchor]}}) == (
        _build_canonical_axis_context({"fact_anchor": {"anchors": [original_anchor]}})
    )


def test_evidence_scope_and_cross_topic_reference_match_legacy(tmp_path, monkeypatch):
    old, short = _anchors()
    path = tmp_path / "rubrics/topic_packs" / TOPIC / "fact_anchor.json"
    path.parent.mkdir(parents=True)
    monkeypatch.setattr(adapter, "ROOT", tmp_path)
    monkeypatch.setattr(cross_topic, "ROOT", tmp_path)
    question = "센서 동작 범위와 입력 조건을 설명하시오."
    answer = "센서 출력은 입력에 비례하고 동작 범위와 입력 조건을 확인한다."
    observed = []
    for anchor in (old, short):
        path.write_text(json.dumps({"topic_id": TOPIC, "anchors": [anchor]}, ensure_ascii=False), encoding="utf-8")
        scope = adapter._derived_anchor_scope(path.parent, question)
        evidence = adapter.evaluate_fact_anchor_requirements(answer_text=answer, topic_ids=[TOPIC])
        cross = cross_topic._anchor_statement(TOPIC, "sensor_response")
        observed.append((scope, evidence, cross))
    assert observed[0] == observed[1]
    # The human sentence projection remains concise and has no score authority.
    view = project_fact_anchor_sentences([TOPIC], root=tmp_path)
    assert view["rows"][0]["statement"] == SHORT
    assert view["score_effect"] == "none" and view["score_admission"] == "DISABLED"
