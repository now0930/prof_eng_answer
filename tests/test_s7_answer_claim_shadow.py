from grading.evidence.s7_answer_claim_shadow import (
    compare_claim_to_registry, evaluate_answer_shadow, extract_answer_claims,
)


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
    verified = {"review_status": "approved", "verification_status": "verified",
                "relation": {"subject": "s", "predicate": "p", "object": "o"}}
    assert compare_claim_to_registry(claim, verified)["status"] == "NOT_ESTABLISHED"
    claim["extraction_status"] = "ABSTAIN"
    assert compare_claim_to_registry(claim, verified)["status"] == "ABSTAIN"


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
    out = evaluate_answer_shadow("개발 단계만 언급했다.", [{"relation": {"subject": "s", "predicate": "p", "object": "o"}}])
    assert out["claims"][0]["relation"] is None
    assert out["comparisons"] == []


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
