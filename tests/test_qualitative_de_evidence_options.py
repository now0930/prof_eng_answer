"""Provider evidence IDs may only resolve to exact deterministic excerpts."""

from grading.qualitative.evidence_options import build_evidence_options, resolve_evidence_id


def test_literal_options_and_resolution():
    answer = "열전대는 고온에 적합하다.\nRTD는 정밀도가 높지만 범위가 좁다."
    requirements = [
        {"status": "SATISFIED", "owner_topic_id": "tc", "source_span": {"start": 0, "end": 16}},
        {"status": "PARTIAL", "owner_topic_id": "rtd", "source_span": {"start": 17, "end": len(answer)}},
    ]
    options = build_evidence_options(answer, requirements)
    assert len(options) == 2
    for option in options:
        assert answer[option["start"]:option["end"]] == option["quote"]
    by_id = {option["evidence_id"]: option for option in options}
    first = resolve_evidence_id({"criterion_id": "D1", "score": 1,
                                 "topic_id": "tc", "evidence_id": options[0]["evidence_id"]}, by_id)
    assert first["quote"] == options[0]["quote"]
    assert "evidence_id" not in first


def test_wrong_claim_and_wrong_topic_are_rejected():
    answer = "허용되는 기술적 근거이다.\n틀린 기술적 판단이다."
    cutoff = answer.index("\n")
    rows = [
        {"status": "SATISFIED", "owner_topic_id": "safe",
         "source_span": {"start": 0, "end": len(answer)}},
        {"status": "WRONG", "owner_topic_id": "safe",
         "source_span": {"start": cutoff + 1, "end": len(answer)}},
    ]
    options = build_evidence_options(answer, rows)
    assert len(options) == 1
    by_id = {option["evidence_id"]: option for option in options}
    try:
        resolve_evidence_id({"topic_id": "other", "evidence_id": options[0]["evidence_id"]}, by_id)
    except ValueError as error:
        assert str(error) == "invalid_evidence_id"
    else:
        raise AssertionError("wrong topic was accepted")


def test_duplicate_literal_is_bound_by_distinct_offsets():
    answer = "같은 근거를 쓴다.\n같은 근거를 쓴다."
    rows = [{"status": "SATISFIED", "owner_topic_id": "topic",
             "source_span": {"start": 0, "end": len(answer)}}]
    options = build_evidence_options(answer, rows)
    assert len(options) == 2
    assert options[0]["quote"] == options[1]["quote"]
    assert options[0]["start"] != options[1]["start"]
    assert all(answer[row["start"]:row["end"]] == row["quote"] for row in options)


def test_later_requirement_span_can_support_judgment_without_wrong_claim():
    answer = (
        "밸브는 유량을 조절한다.\n"
        "최대 차압에서 스프링 힘과 마찰력을 비교해 닫힘 여유를 확인한다.\n"
        "시트 하중은 언제나 필요 없다고 단정한다."
    )
    first_end = answer.index("\n")
    second_start = first_end + 1
    second_end = answer.index("\n", second_start)
    rows = [
        {"status": "SATISFIED", "owner_topic_id": "valve",
         "source_span": {"start": 0, "end": first_end},
         "source_spans": [{"start": 0, "end": first_end},
                          {"start": second_start, "end": second_end}]},
        {"status": "WRONG", "owner_topic_id": "valve",
         "source_span": {"start": second_end + 1, "end": len(answer)}},
    ]
    options = build_evidence_options(answer, rows)
    assert any("닫힘 여유" in row["quote"] for row in options)
    assert all("필요 없다고" not in row["quote"] for row in options)
