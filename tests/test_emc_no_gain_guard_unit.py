"""Pure no-gain protection checks, independent of repository data."""

from grading.scoring.emc_no_gain_guard import (
    EMC_TOPIC, cap_score_to_counterfactual, strip_detected_emc_error_units,
)


def violation(text, code="EMC_UPS_UNIVERSAL_FIX", offset=0):
    return {
        "code": code,
        "source_span": {"start": offset, "end": offset + len(text)},
        "source_text": text,
    }


def test_exact_bad_sentence_removed_and_newline_retained():
    good = "검증된 전원 품질을 확인한다."
    bad = "UPS로 모든 EMC 문제가 해결된다."
    answer = good + "\n\n" + bad
    result = strip_detected_emc_error_units(
        answer, [violation(bad, offset=len(good) + 2)],
        active_topic_ids=[EMC_TOPIC],
    )
    assert result == good


def test_other_topic_not_modified():
    bad = "UPS로 모든 EMC 문제가 해결된다."
    assert strip_detected_emc_error_units(
        bad, [violation(bad)], active_topic_ids=["other_topic"]
    ) is None


def test_wrong_or_corrupt_source_span_fails_closed():
    good = "검증된 전원 품질을 확인한다."
    bad = "UPS로 모든 EMC 문제가 해결된다."
    answer = good + bad
    fake = violation(bad, offset=0)
    assert strip_detected_emc_error_units(
        answer, [fake], active_topic_ids=[EMC_TOPIC]
    ) is None


def test_only_wrong_text_remains_no_counterfactual():
    bad = "UPS로 모든 EMC 문제가 해결된다."
    assert strip_detected_emc_error_units(
        bad, [violation(bad)], active_topic_ids=[EMC_TOPIC]
    ) is None


def test_invalid_finding_without_emc_is_ignored():
    text = "X"
    assert strip_detected_emc_error_units(
        text, [violation(text, "INVALID_OTHER")],
        active_topic_ids=[EMC_TOPIC]
    ) is None


def test_clamp_never_increases_total_and_preserves_requirement_fields():
    score = {
        "total_score": 13.63,
        "max_score": 25.0,
        "applied_ceiling": 14.5,
        "verdict": "NEEDS_CORRECTION",
        "official_pass_met": False,
        "high_score_met": False,
        "score_breakdown": {"A_structure": 3.0},
    }
    capped, changed = cap_score_to_counterfactual(
        score, clean_score_total=11.0, fatal_or_core_error=True,
    )
    assert changed and capped["total_score"] == 11.0
    assert capped["applied_ceiling"] == 11.0
    assert capped["verdict"] == "NEEDS_CORRECTION"
    assert capped["score_breakdown"] == score["score_breakdown"]
    assert score["total_score"] == 13.63


def test_major_capped_without_turning_into_fatal():
    score = {
        "total_score": 12.25, "max_score": 25.0,
        "applied_ceiling": 14.5, "verdict": "FAIL",
        "official_pass_met": False, "high_score_met": False,
    }
    capped, changed = cap_score_to_counterfactual(
        score, clean_score_total=11.0, fatal_or_core_error=False,
    )
    assert changed and capped["total_score"] == 11.0
    assert capped["verdict"] == "FAIL"


def test_no_cap_when_baseline_higher_or_equal():
    score = {
        "total_score": 9.17, "max_score": 25.0,
        "applied_ceiling": 14.5, "verdict": "FAIL",
    }
    same, changed = cap_score_to_counterfactual(
        score, clean_score_total=11.0, fatal_or_core_error=False,
    )
    assert not changed and same == score
