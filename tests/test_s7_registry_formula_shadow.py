"""S7 formula shadow guards. Six authored pairs are NOT precision/recall ground truth."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from grading.evidence.s7_registry_formula_shadow import (
    SPECS, _literal_formula, evaluate_formula_shadow,
)


def _sample():
    source = {
        "schema_version": "s7_alias_registry_source_review.v1",
        "status": "EVIDENCE_COLLECTED_ALL_CANDIDATES_HOLD",
        "score_admission": "DISABLED",
        "inventory_execution_sha": "synthetic-only",
        "projection_count_with_duplicates": 179,
        "unique_topic_fact_count": 119,
        "rows": [],
    }
    challenge = {
        "schema_version": "s7_negative_claim_challenge.v1",
        "score_admission": "DISABLED",
        "adjudication_status": "AUTHOR_DRAFT_NOT_INDEPENDENTLY_LABELED",
        "cases": [],
    }
    path = (Path(__file__).resolve().parents[1]
            / "calibration/s7_alias_negative_claim_challenge_v1.json")
    real_cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    for case in real_cases:
        if case["fact_id"] not in SPECS:
            continue
        spec = SPECS[case["fact_id"]]
        source["rows"].append({
            "owner_topic_id": spec["owner"],
            "fact_id": case["fact_id"],
            "source_fact_id": spec["source"],
            "review_decision": "HOLD",
            "relation": {
                "subject": spec["subject"],
                "predicate": spec["predicate"],
                "object": spec["object"],
                "polarity": "positive",
                "conditions": spec["conditions"],
            },
        })
        challenge["cases"].append(case)
    return source, challenge


def test_six_draft_formulas_only_produce_shadow_candidates():
    source, challenge = _sample()
    result = evaluate_formula_shadow(source, challenge, strict=False)
    assert result["status"] == "SHADOW_FORMULA_PATTERNS_REVIEW_ONLY"
    assert result["formula_fact_pairs"] == 6
    assert result["positive_expected_formula_pattern_count"] == 6
    assert result["adversarial_expected_formula_pattern_count"] == 0
    assert result["adversarial_inverted_formula_pattern_count"] == 6
    assert result["measured_precision"] is None
    assert result["measured_recall"] is None
    assert result["measured_accuracy"] is None
    assert result["automatic_alias_admission"] is False
    assert result["score_admission"] == "DISABLED"
    assert all(row["score_effect"] == "none" for row in result["rows"])
    exported = json.dumps(result, ensure_ascii=False)
    assert "정적 기준과 일관된 단위" not in exported
    assert "PFDavg_target ≤" not in exported


@pytest.mark.parametrize(("family", "positive", "inverted"), [
    ("rrf_ratio", "동일 사건과 시간 기준에서 RRF_required = F_residual/F_tolerable",
     "동일 사건과 시간 기준에서 RRF_required = F_tolerable/F_residual"),
    ("pfd_bound", "저요구 PFDavg_target ≤ 1/RRF_required",
     "저요구 PFDavg_target ≥ 1/RRF_required"),
    ("nyquist_sign", "시계방향 양수 N_cw=Z−P", "시계방향 양수 N_cw=P−Z"),
    ("force_product", "정적 기준, 일관된 단위: ΔP × Au",
     "정적 기준, 일관된 단위: ΔP / Au"),
])
def test_formula_direction_is_not_synonymous(family, positive, inverted):
    assert _literal_formula(family, positive)[0] == "EXPECTED_FORMULA_SYNTAX"
    assert _literal_formula(family, inverted)[0] == "INVERTED_FORMULA_SYNTAX"


def test_no_generic_equal_alias_admitted():
    assert _literal_formula("rrf_ratio", "위험감소율은 비율과 같다") == (
        "NO_LITERAL_PATTERN", False,
    )
    assert _literal_formula("pfd_bound", "저요구 조건에서 PFD가 맞다") == (
        "NO_LITERAL_PATTERN", True,
    )
    assert _literal_formula(
        "nyquist_sign", "시계방향 양수일 때 Nyquist 관계는 같다",
    )[0] == "NO_LITERAL_PATTERN"


def test_formula_match_without_conditions_never_infers_conditions():
    assert _literal_formula("rrf_ratio", "RRF_required=F_residual/F_tolerable") == (
        "EXPECTED_FORMULA_SYNTAX", False,
    )
    assert _literal_formula("nyquist_sign", "N_cw=Z-P") == (
        "EXPECTED_FORMULA_SYNTAX", False,
    )


def test_source_identity_and_conditions_fail_closed():
    for field, value in (
        ("review_decision", "ACCEPT"),
        ("source_fact_id", "some_other_fact"),
    ):
        source, challenge = _sample()
        source["rows"][0][field] = value
        with pytest.raises(ValueError):
            evaluate_formula_shadow(source, challenge, strict=False)
    source, challenge = _sample()
    source["rows"][0]["relation"]["object"] = "invented"
    with pytest.raises(ValueError, match="relation"):
        evaluate_formula_shadow(source, challenge, strict=False)
    source, challenge = _sample()
    source["rows"][0]["relation"]["conditions"] = []
    with pytest.raises(ValueError, match="relation"):
        evaluate_formula_shadow(source, challenge, strict=False)


def test_score_admission_and_swapped_owner_blocked():
    source, challenge = _sample()
    challenge["cases"][0]["score_effect"] = "credit"
    with pytest.raises(ValueError, match="grade effect"):
        evaluate_formula_shadow(source, challenge, strict=False)
    source, challenge = _sample()
    challenge["cases"][0]["owner_topic_id"] = "wrong_owner"
    with pytest.raises(ValueError, match="owner"):
        evaluate_formula_shadow(source, challenge, strict=False)
    source, challenge = _sample()
    source["score_admission"] = "ENABLED"
    with pytest.raises(ValueError):
        evaluate_formula_shadow(source, challenge, strict=False)


def test_adversarial_pattern_collision_forces_hold():
    source, challenge = _sample()
    target = next(c for c in challenge["cases"]
                  if c["fact_id"] == "required_rrf_relation")
    target["adversarial_answer"] = target["positive_answer"]
    result = evaluate_formula_shadow(source, challenge, strict=False)
    assert result["status"] == "COUNTEREXAMPLE_PATTERN_COLLISION_REVIEW"
    assert result["adversarial_expected_formula_pattern_count"] == 1
    assert result["measured_accuracy"] is None


def test_existing_verified_registry_owns_all_six_relations():
    from grading.evidence.fact_claim_adapter import project_fact_claims

    topics = {spec["owner"] for spec in SPECS.values()}
    required = {
        topic: {fid for fid, spec in SPECS.items() if spec["owner"] == topic}
        for topic in topics
    }
    projected = project_fact_claims(sorted(topics), required_by_topic=required)
    by_key = {(r["owner_topic_id"], r["fact_id"]): r for r in projected}
    assert len(by_key) == len(SPECS)
    for fid, spec in SPECS.items():
        row = by_key[(spec["owner"], fid)]
        assert row["projection_status"] == "VERIFIED_REGISTRY_RELATION"
        assert row["source_fact_id"] == spec["source"]
        for field in ("subject", "predicate", "object", "conditions"):
            assert row["relation"][field] == spec[field]


def test_rejected_equation_is_not_counted_as_positive_pattern():
    phrase = "RRF_required = F_residual/F_tolerable가 맞다는 주장은 틀리다."
    result, _ = _literal_formula("rrf_ratio", phrase)
    assert result == "ASSERTION_CONTEXT_UNVERIFIED"
