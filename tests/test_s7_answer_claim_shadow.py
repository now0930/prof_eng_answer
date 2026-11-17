from copy import deepcopy
import json
from pathlib import Path

from grading.evidence.approved_fact_registry import load_approved_fact_registry
from grading.evidence.s7_answer_claim_shadow import (
    compare_claim_to_registry, evaluate_answer_shadow, extract_answer_claims,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_REGISTRY = load_approved_fact_registry(REPOSITORY_ROOT)
FACTS_BY_ANCHOR = {
    fact["legacy_anchor_id"]: fact
    for fact in _REGISTRY["facts"]
    if fact.get("legacy_anchor_id") in {
        "effective_unbalanced_area", "sw06_baseline_approved_reference",
        "deadband_definition_direction_reversal", "sw04_v_model_definition",
        "nyquist_contour_and_mapping",
    }
}


CASES = [
    ("제어밸브 데드밴드는 입력 방향을 반전할 때 출력 변화가 없는 입력 구간이다.", "제어밸브 데드밴드", "출력 변화가 없는", "입력 구간"),
    ("승인된 기준선은 변경 관리의 기준으로 사용된다.", "승인된 기준선", "으로 사용된다", "변경 관리의 기준"),
    ("실효 불평형 면적은 압력 작용면과 밸브 구조에 따라 결정된다.", "실효 불평형 면적", "에 따라 결정된다", "압력 작용면과 밸브 구조"),
    ("개발 단계는 시험 단계에 대응한다.", "개발 단계", "에 대응한다", "시험 단계"),
]


def _one(answer):
    claims = extract_answer_claims(answer)["claims"]
    assert len(claims) == 1
    return claims[0]


def test_supported_five_fact_claims_have_observed_fields_and_spans():
    for answer, subject, relation, obj in CASES:
        claim = _one(answer)
        assert claim["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"
        for key, expected in (("subject", subject), ("relation", relation), ("object", obj)):
            field = claim[key]
            assert field["text"] == expected
            start, end = field["span"]["start"], field["span"]["end"]
            assert answer[start:end] == expected
        assert claim["polarity"] == "POSITIVE"


def test_nyquist_sentence_yields_two_answer_derived_relations():
    answer = "Nyquist 경로는 우반평면을 둘러싸고 L(s)의 복소평면 사상으로 이어진다."
    claims = extract_answer_claims(answer)["claims"]
    assert len(claims) == 2
    assert [(c["subject"]["text"], c["relation"]["text"], c["object"]["text"])
            for c in claims] == [
        ("Nyquist 경로", "둘러싸고", "우반평면"),
        ("L(s)", "사상", "복소평면"),
    ]
    for claim in claims:
        assert claim["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"
        for field in (claim["subject"], claim["relation"], claim["object"]):
            start, end = field["span"]["start"], field["span"]["end"]
            assert answer[start:end] == field["text"]


def test_case_mixed_nyquist_fallback_keeps_exact_original_spans():
    for answer, expected in (
        ("nyquist 경로에 대한 설명이다.", "nyquist 경로"),
        ("NYQUIST contour를 검토한다.", "NYQUIST contour"),
        ("Nyquist 경로 주변의 우반평면 응답을 확인한다.", "Nyquist 경로"),
    ):
        claims = extract_answer_claims(answer)["claims"]
        assert claims
        claim = claims[0]
        assert claim["extraction_status"] == "ABSTAIN"
        subject = claim["subject"]
        assert subject["text"] == expected
        start, end = subject["span"]["start"], subject["span"]["end"]
        assert 0 <= start < end <= len(answer)
        assert answer[start:end] == subject["text"]


def test_every_emitted_claim_span_is_an_exact_source_slice():
    examples = [answer for answer, *_ in CASES] + [
        "Nyquist 경로는 우반평면을 둘러싸고 L(s)의 복소평면 사상으로 이어진다.",
        "nyquist 경로에 대한 설명이다.",
        "NYQUIST contour를 검토한다.",
    ]
    for answer in examples:
        for claim in extract_answer_claims(answer)["claims"]:
            for field_name in ("subject", "relation", "object"):
                field = claim.get(field_name)
                if field is None:
                    continue
                start, end = field["span"]["start"], field["span"]["end"]
                assert 0 <= start < end <= len(answer)
                assert answer[start:end] == field["text"]
            start, end = claim["evidence_span"]["start"], claim["evidence_span"]["end"]
            assert 0 <= start < end <= len(answer)


def test_deadband_zero_output_change_is_positive_definition_not_negation():
    claim = _one(CASES[0][0])
    assert claim["relation"]["text"] == "출력 변화가 없는"
    assert claim["polarity"] == "POSITIVE"
    contrary = _one("데드밴드는 입력 방향 반전과 무관하다.")
    assert contrary["extraction_status"] == "ABSTAIN"
    assert contrary["polarity"] == "NEGATIVE_OR_AMBIGUOUS"


def test_registry_free_and_independent_stage_a():
    answer = CASES[3][0]
    first = extract_answer_claims(answer)
    fake_registry = [{"fact_id": "FAKE", "relation": {"subject": "X", "predicate": "Y", "object": "Z"}}]
    evaluate_answer_shadow(answer, fake_registry)
    assert extract_answer_claims(answer) == first
    claim = first["claims"][0]
    assert "candidate_fact_hint" not in claim
    assert not any(k.endswith("_id") for k in claim)


def test_stage_b_never_claims_semantic_match_without_crosswalk():
    claim = _one(CASES[3][0])
    fact = FACTS_BY_ANCHOR["sw04_v_model_definition"]
    result = compare_claim_to_registry(claim, fact, scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT)
    assert result["status"] == "NOT_ESTABLISHED"
    assert result["source_match_proven"] is False
    claim["extraction_status"] = "ABSTAIN"
    assert compare_claim_to_registry(claim, fact, scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT)["status"] == "ABSTAIN"


def test_negation_quotes_direction_and_partial_claims_fail_closed():
    for answer in (
        '"개발 단계는 시험 단계에 대응한다"고 말했다.',
        "개발 단계는 시험 단계와 대응하지 않는다.",
        "개발 단계만 설명한다.",
        "Nyquist 경로는 우반평면을 둘러싸지 않는다.",
    ):
        claim = _one(answer)
        assert claim["extraction_status"] == "ABSTAIN"


def test_registry_values_cannot_fill_unsupported_relation():
    result = extract_answer_claims("개발 단계만 언급했다.")
    assert result["claims"][0]["relation"] is None
    out = evaluate_answer_shadow(
        "개발 단계만 언급했다.", [FACTS_BY_ANCHOR["sw04_v_model_definition"]],
        scope_topic_id=FACTS_BY_ANCHOR["sw04_v_model_definition"]["topic_id"],
        repository_root=REPOSITORY_ROOT,
    )
    assert out["claims"][0]["relation"] is None
    assert out["comparisons"][0]["relation_comparison_status"] == "ABSTAIN"
    assert out["comparisons"][0]["reason"] == "ANSWER_CLAIM_NOT_ESTABLISHED_BY_STAGE_A"


def test_multiple_claims_are_separate_and_conditions_are_not_inferred():
    answer = CASES[0][0] + " " + CASES[3][0]
    claims = extract_answer_claims(answer)["claims"]
    assert len(claims) == 2
    assert claims[0]["evidence_span"]["end"] <= claims[1]["evidence_span"]["start"]
    assert all(c["conditions"] == [] and c["condition_status"] == "NOT_EXTRACTED" for c in claims)


def test_accuracy_and_score_admission_remain_disabled():
    result = evaluate_answer_shadow(CASES[0][0], [])
    assert result["accuracy"] is None
    assert result["accuracy_status"] == "NOT_ESTABLISHED"
    assert result["score_admission"] == "DISABLED"
    assert result["score_effect"] == "none"
    assert result["comparison_status"] == "NO_COMPARISON_TARGET"
    assert result["comparisons"][0]["reason"] == "NO_COMPARISON_TARGET"


def test_keyword_only_sentence_does_not_create_a_relation():
    answer = "데드밴드와 입력 방향 반전은 함께 설명되는 용어다."
    claims = extract_answer_claims(answer)["claims"]
    assert claims
    assert all(c["extraction_status"] == "ABSTAIN" for c in claims)
    assert all(c["relation"] is None and c["object"] is None for c in claims)


def test_reversed_relation_direction_is_not_normalized_to_supported_claim():
    answer = "시험 단계는 개발 단계에 대응한다."
    claims = extract_answer_claims(answer)["claims"]
    assert claims
    assert all(c["extraction_status"] == "ABSTAIN" for c in claims)


def test_each_supported_fact_has_an_unsupported_relation_abstention():
    unsupported = (
        "최신 파일은 승인된 기준선이다.",
        "실효 불평형 면적은 공칭 시트 면적과 항상 같다.",
        "시험 단계는 개발 단계에 대응한다.",
        "Nyquist 경로는 우반평면을 둘러싸지 않는다.",
    )
    for answer in unsupported:
        claims = extract_answer_claims(answer)["claims"]
        assert claims, answer
        assert all(c["extraction_status"] == "ABSTAIN" for c in claims), answer


def test_scoped_negation_does_not_promote_a_positive_subspan():
    answer = "개발 단계는 시험 단계에 대응하지만, 설계 단계는 시험 단계와 무관하다."
    claims = extract_answer_claims(answer)["claims"]
    assert claims
    assert all(c["extraction_status"] == "ABSTAIN" for c in claims)
    assert all(answer[c["evidence_span"]["start"]:c["evidence_span"]["end"]]
               for c in claims)


def test_quoted_claim_and_authors_own_claim_are_not_conflated():
    answer = '“개발 단계는 시험 단계에 대응한다”는 주장이 있다. 개발 단계는 시험 단계에 대응한다.'
    claims = extract_answer_claims(answer)["claims"]
    assert len(claims) == 2
    assert claims[0]["extraction_status"] == "ABSTAIN"
    assert claims[1]["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"
    for claim in claims:
        for key in ("subject", "relation", "object"):
            field = claim[key]
            start, end = field["span"]["start"], field["span"]["end"]
            assert answer[start:end] == field["text"]


def test_partially_true_statement_remains_surface_review_only():
    answer = "개발 단계는 시험 단계에 대응하지만 세부 시험 항목은 프로젝트마다 다르다."
    claim = _one(answer)
    assert (claim["subject"]["text"], claim["relation"]["text"], claim["object"]["text"]) == (
        "개발 단계", "에 대응", "시험 단계")
    assert claim["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"
    assert claim["conditions"] == []
    assert claim["condition_status"] == "NOT_EXTRACTED"


def test_contradictory_claims_in_one_sentence_fail_closed():
    answer = "개발 단계는 시험 단계에 대응하지만 설계 단계는 시험 단계와 무관하다."
    claims = extract_answer_claims(answer)["claims"]
    assert claims
    assert all(c["extraction_status"] == "ABSTAIN" for c in claims)


def test_missing_conditions_are_never_invented_and_v_model_has_none_required():
    claim = _one("개발 단계는 시험 단계에 대응한다.")
    assert claim["conditions"] == []
    assert claim["condition_status"] == "NOT_EXTRACTED"
    assert claim["extraction_status"] == "SURFACE_CLAIM_REVIEW_ONLY"


STAGE_B_CASES = (
    ("effective_unbalanced_area", CASES[2][0]),
    ("sw06_baseline_approved_reference", CASES[1][0]),
    ("deadband_definition_direction_reversal", CASES[0][0]),
    ("sw04_v_model_definition", CASES[3][0]),
    ("nyquist_contour_and_mapping", "Nyquist 경로는 우반평면을 둘러싸고 L(s)의 복소평면 사상으로 이어진다."),
)


def test_stage_b_generates_explicit_pair_audits_for_all_five_facts():
    for anchor_id, answer in STAGE_B_CASES:
        fact = FACTS_BY_ANCHOR[anchor_id]
        result = evaluate_answer_shadow(
            answer, [fact], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
        )
        assert result["comparison_status"] == "COMPARISONS_GENERATED"
        expected_pairs = 2 if anchor_id == "nyquist_contour_and_mapping" else 1
        assert len(result["comparisons"]) == expected_pairs
        assert all(row["comparison_fact_id"] == fact["fact_id"] for row in result["comparisons"])
        assert all(row["registry_validation_status"] == "APPROVED_VERIFIED" for row in result["comparisons"])
        assert all(row["registry_relation_ids"] == {
            key: fact["relation"][key] for key in ("subject", "predicate", "object")
        } for row in result["comparisons"])
        assert all(row["requested_comparison_fact_id"] == fact["fact_id"] for row in result["comparisons"])
        assert all(row["relation_comparison_status"] == "NOT_ESTABLISHED" for row in result["comparisons"])
        assert all(row["crosswalk_status"] == "MISSING_REVIEWED_CROSSWALK" for row in result["comparisons"])
        assert all(row["source_match_proven"] is False for row in result["comparisons"])
        assert all(row["score_admission"] == "DISABLED" and row["score_effect"] == "none"
                   for row in result["comparisons"])
        assert all("fact_id" not in claim and "candidate_fact_hint" not in claim
                   for claim in result["claims"])
        assert all(fact["fact_id"] not in str(claim) for claim in result["claims"])
        assert all("claim_evidence_span" in row for row in result["comparisons"])


def test_v_model_has_zero_required_conditions_and_nyquist_claims_stay_separate():
    vmodel = FACTS_BY_ANCHOR["sw04_v_model_definition"]
    answer = evaluate_answer_shadow(
        CASES[3][0], [vmodel], scope_topic_id=vmodel["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert vmodel["relation"]["conditions"] == []
    assert answer["comparisons"][0]["condition_comparison_status"] == "NO_REGISTRY_REQUIRED_CONDITIONS"

    nyquist = FACTS_BY_ANCHOR["nyquist_contour_and_mapping"]
    answer = evaluate_answer_shadow(
        STAGE_B_CASES[-1][1], [nyquist], scope_topic_id=nyquist["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert [row["claim_index"] for row in answer["comparisons"]] == [0, 1]
    assert len({row["claim_evidence_span"]["start"] for row in answer["comparisons"]}) == 2
    assert all(row["condition_comparison_status"] == "NOT_ASSESSED_ANSWER_CONDITIONS_NOT_EXTRACTED"
               for row in answer["comparisons"])


def test_stage_a_is_unchanged_when_registry_scope_changes():
    answer = CASES[3][0]
    first = evaluate_answer_shadow(
        answer, [FACTS_BY_ANCHOR["sw04_v_model_definition"]],
        scope_topic_id=FACTS_BY_ANCHOR["sw04_v_model_definition"]["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    second = evaluate_answer_shadow(
        answer, [FACTS_BY_ANCHOR["effective_unbalanced_area"]],
        scope_topic_id=FACTS_BY_ANCHOR["effective_unbalanced_area"]["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert first["claims"] == second["claims"] == extract_answer_claims(answer)["claims"]
    assert first["comparisons"][0]["comparison_fact_id"] != second["comparisons"][0]["comparison_fact_id"]


def test_stage_b_abstains_without_topic_scope_or_comparison_target():
    fact = FACTS_BY_ANCHOR["sw04_v_model_definition"]
    missing_topic = evaluate_answer_shadow(CASES[3][0], [fact], repository_root=REPOSITORY_ROOT)
    assert missing_topic["comparison_status"] == "SCOPE_REJECTED"
    assert missing_topic["comparisons"][0]["reason"] == "TOPIC_SCOPE_REQUIRED"
    no_target = evaluate_answer_shadow(CASES[3][0], [], repository_root=REPOSITORY_ROOT)
    assert no_target["comparison_status"] == "NO_COMPARISON_TARGET"
    assert no_target["comparisons"][0]["relation_comparison_status"] == "ABSTAIN"


def test_duplicate_forged_unverified_and_wrong_topic_registry_inputs_are_rejected():
    fact = FACTS_BY_ANCHOR["sw04_v_model_definition"]
    duplicate = evaluate_answer_shadow(
        CASES[3][0], [fact, fact], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert duplicate["comparison_scope"]["rejection_reason"] == "DUPLICATE_FACT_ID_IN_SCOPE"
    assert duplicate["comparisons"][0]["registry_validation_status"] == "REJECTED"

    forged = deepcopy(fact)
    forged["verification_refs"] = []
    forged["verification_status"] = "unverified"
    rejected = evaluate_answer_shadow(
        CASES[3][0], [forged], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert rejected["comparison_scope"]["rejection_reason"] == "FACT_NOT_IDENTICAL_TO_APPROVED_REGISTRY"

    unapproved = deepcopy(fact)
    unapproved["review_status"] = "candidate"
    rejected = evaluate_answer_shadow(
        CASES[3][0], [unapproved], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert rejected["comparison_scope"]["rejection_reason"] == "FACT_NOT_IDENTICAL_TO_APPROVED_REGISTRY"

    forged_source = deepcopy(fact)
    forged_source["verification_refs"][0]["supports_claim"] = "unrelated claim"
    rejected = evaluate_answer_shadow(
        CASES[3][0], [forged_source], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert rejected["comparison_scope"]["rejection_reason"] == "FACT_NOT_IDENTICAL_TO_APPROVED_REGISTRY"

    wrong_topic = evaluate_answer_shadow(
        CASES[3][0], [fact], scope_topic_id="another_topic", repository_root=REPOSITORY_ROOT,
    )
    assert wrong_topic["comparison_scope"]["rejection_reason"] == "FACT_TOPIC_SCOPE_MISMATCH"

    malformed = evaluate_answer_shadow(
        CASES[3][0], [{"fact_id": fact["fact_id"]}], scope_topic_id=fact["topic_id"],
        repository_root=REPOSITORY_ROOT,
    )
    assert malformed["comparison_scope"]["rejection_reason"] == "FACT_NOT_IDENTICAL_TO_APPROVED_REGISTRY"


def test_invalid_registry_root_and_abstained_claim_never_compare_as_match(tmp_path):
    fact = FACTS_BY_ANCHOR["sw04_v_model_definition"]
    invalid_root = evaluate_answer_shadow(
        CASES[3][0], [fact], scope_topic_id=fact["topic_id"], repository_root=tmp_path,
    )
    assert invalid_root["comparisons"][0]["relation_comparison_status"] == "ABSTAIN"
    assert invalid_root["comparisons"][0]["reason"] == "APPROVED_REGISTRY_INVALID_OR_UNAVAILABLE"

    abstained = evaluate_answer_shadow(
        "개발 단계만 언급했다.", [fact], scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert abstained["comparisons"][0]["relation_comparison_status"] == "ABSTAIN"
    assert abstained["comparisons"][0]["reason"] == "ANSWER_CLAIM_NOT_ESTABLISHED_BY_STAGE_A"

    malformed_claim = compare_claim_to_registry(
        [], fact, scope_topic_id=fact["topic_id"], repository_root=REPOSITORY_ROOT,
    )
    assert malformed_claim["status"] == "ABSTAIN"
    assert malformed_claim["claim_extraction_status"] == "ABSTAIN"


def test_b7_review_packet_is_complete_but_unlabeled_and_score_neutral():
    packet_path = REPOSITORY_ROOT / "calibration" / "s7_b7_expert_review_packet_v1.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["schema_version"] == "s7_b7_expert_review_packet.v1"
    assert packet["status"] == "PENDING_INDEPENDENT_REVIEW"
    assert packet["scope"] == {"topic_count": 5, "fact_count": 5, "case_count": 40, "cases_per_fact": 8}
    assert packet["policy"]["accuracy_status"] == "NOT_ESTABLISHED"
    assert packet["policy"]["score_admission"] == "DISABLED"
    assert packet["policy"]["author_authored_cases_are_ground_truth"] is False

    ids = set()
    for case in packet["cases"]:
        assert case["case_id"] not in ids
        ids.add(case["case_id"])
        assert case["review_status"] == "PENDING"
        assert case["data_origin"] == "AUTHOR_AUTHORED_PROBE_NOT_GOLD"
        assert case["independent_reviewer_label"] is None
        assert case["reviewer_evidence"] is None
        assert case["source_reference"]["registry_fact_verification_refs"]
        assert case["stage_b_comparison_status"]["overall"] in {"COMPARISONS_GENERATED", "NO_CLAIMS"}
        assert case["score_effect"] == "none"
        for claim in case["stage_a_extracted_claims"]:
            for key in ("subject", "relation", "object"):
                field = claim.get(key)
                if field is not None:
                    start, end = field["span"]["start"], field["span"]["end"]
                    assert case["answer_text"][start:end] == field["text"]
        for audit in case["stage_b_comparison_status"]["audits"]:
            assert audit["relation_comparison_status"] in {"NOT_ESTABLISHED", "ABSTAIN"}
            assert audit["source_match_proven"] is False
            assert audit["score_admission"] == "DISABLED"
            assert audit["score_effect"] == "none"
    assert len(ids) == 40
