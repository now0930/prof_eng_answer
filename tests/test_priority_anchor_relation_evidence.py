"""Check the scoped relation evidence and the owning question contract."""
import pytest

from grading.evidence.priority_anchor_relations import FINAL, HUMIDITY, SOFTWARE, SPEED, relation_evidence
from grading.routing.deterministic_topic_router import route_question_topics
from grading.scoring.deterministic_primary_grader import grade_deterministically


@pytest.mark.parametrize("topic,anchor,answer,status", [
    (SPEED, "counting_window_speed_equation",
     "측정창을 고정하면 절대 RPM 간격은 일정하다. 저속일수록 상대 양자화 영향이 커진다.", "SATISFIED"),
    (SPEED, "counting_window_speed_equation",
     "측정창 고정, 절대 RPM 간격, 상대 양자화.", "MISSING"),
    (SPEED, "gear_tooth_speed_equation",
     "전체 회전 평균에는 실측 펄스 수를 넣는다. 국부 주기는 실제 각도 간격을 반영한다.", "SATISFIED"),
    (SPEED, "gear_tooth_speed_equation",
     "결손 구간 국부 주기에 정상 치간 각도를 그대로 적용한다.", "MISSING"),
    (SPEED, "incremental_encoder_principle",
     "증분형 엔코더는 펄스를 세며 전원 차단 중 미계측 이동을 복원할 수 없다.", "SATISFIED"),
    (HUMIDITY, "absolute_humidity_definition", "부피당 수증기의 질량으로 절대습도를 나타낸다.", "SATISFIED"),
    (HUMIDITY, "absolute_humidity_definition", "절대습도, 수증기, 체적, 포화 수증기압.", "MISSING"),
    (SOFTWARE, "sw04_hil", "실물 제어기를 실시간 공정 모델과 연결한다.", "PARTIAL"),
    (SOFTWARE, "sw04_hil", "“먼저 시작한다. 실물 제어기를 실시간 공정 모델과 연결한다. 끝이다.”", "MISSING"),
    (FINAL, "fail_action_vs_safe_state", "고장 시 밸브 동작과 공정 안전상태는 별개다.", "SATISFIED"),
    (FINAL, "fail_action_vs_safe_state", "Fail action, safe state, 위험분석, SRS.", "MISSING"),
    (FINAL, "imperfect_test_residual_risk", "미검출 고장은 실제 검출·복구까지 평가한다.", "SATISFIED"),
    (FINAL, "imperfect_test_residual_risk", "PST, 미검출 고장, overhaul/mission time.", "MISSING"),
    (FINAL, "response_time_process_safety_time",
     "전체 SIF는 PST 내 안전상태에 도달해야 한다. 최종제어요소는 할당 응답시간을 만족한다.", "SATISFIED"),
    (FINAL, "response_time_process_safety_time", "전체 SIF, PST, 최종제어요소, 할당 응답시간.", "MISSING"),
    (FINAL, "redundancy_independence_boundary", "항상 완전 독립이다. 공통원인고장은 무시한다.", "MISSING"),
])
def test_scoped_relation_requires_asserted_evidence(topic, anchor, answer, status):
    actual, spans = relation_evidence(topic, anchor, answer)
    assert actual == status
    assert bool(spans) == (status != "MISSING")
    assert all(answer[s["start"]:s["end"]].strip() for s in spans)
    assert relation_evidence("unrelated", anchor, answer) is None


REDUNDANCY = "redundancy_independence_boundary"
REDUNDANCY_QUESTION = (
    "SIS 최종제어요소 이중화에서 1oo2 또는 2oo3 ESD 밸브의 "
    "공통원인고장과 종속성을 고려하여 위험감소를 평가하시오."
)


def test_redundancy_question_routes_and_changes_final_score():
    route = route_question_topics(REDUNDANCY_QUESTION)
    assert route["topic_ids"] == [FINAL]
    totals = []
    for answer, expected in (
        ("공유 공기원의 종속성을 반영하여 이중화의 위험감소를 평가한다.", "SATISFIED"),
        ("채널은 항상 완전 독립이며 공통원인고장을 무시한다.", "MISSING"),
    ):
        result = grade_deterministically(
            question_text=REDUNDANCY_QUESTION, answer_text=answer, qualitative_de_mode="off"
        )
        assert result["provider_calls"] == 0
        target = [r for r in result["requirements"] if r["requirement_id"] == REDUNDANCY]
        assert [r["status"] for r in target] == [expected]
        totals.append(result["total_score"])
    assert totals[0] > totals[1]

    old_question = "SIF bypass, override, impairment와 restoration 관리 기준을 설명하시오."
    result = grade_deterministically(question_text=old_question, answer_text="변경을 승인한다.")
    assert REDUNDANCY not in {r["requirement_id"] for r in result["requirements"]}


@pytest.mark.parametrize("topic,anchor,answer,recognized", [
    (SPEED, "counting_window_speed_equation",
     "계수 게이트 폭이 일정할 때 환산 속도 증분은 운전점에 따라 바뀌지 않는다.", True),
    (SPEED, "gear_tooth_speed_equation",
     "빠진 치의 앞뒤 펄스를 비교할 때 실제 회전각을 사용한다.", True),
    (SPEED, "gear_tooth_speed_equation",
     '“빠진 치의 앞뒤 펄스에는 실제 회전각을 사용한다”를 인용한다.', False),
    (HUMIDITY, "absolute_humidity_definition",
     "수증기의 질량을 습공기 부피로 나누면 절대습도가 된다.", True),
    (HUMIDITY, "absolute_humidity_definition",
     "수증기의 질량을 건조한 공기의 질량으로 나누면 절대습도가 된다.", False),
    (FINAL, "imperfect_test_residual_risk",
     "부분 시험에서 포착되지 않은 고장은 유지된다.", True),
    (FINAL, "imperfect_test_residual_risk",
     "부분 시험에서 포착되지 않은 고장도 수리 없이 제거된다.", False),
    (SPEED, "incremental_encoder_principle",
     "기준 신호 이후의 에지를 누적해 상대 변위를 얻는다.", True),
])
def test_relation_paraphrases_preserve_assertion_and_evidence(topic, anchor, answer, recognized):
    status, spans = relation_evidence(topic, anchor, answer)
    assert (status in {"SATISFIED", "PARTIAL"}) is recognized
    assert [answer[s["start"]:s["end"]] for s in spans] == (
        [answer.removesuffix(".")] if recognized else []
    )


def test_equating_fail_position_with_process_safe_state_earns_no_credit():
    # A bare equivalence has no independently asserted device movement.
    false_claim = "압력 상실 시 위치와 공정 안전 상태는 항상 일치한다."
    topic, anchor = FINAL, "fail_action_vs_safe_state"
    assert relation_evidence(topic, anchor, false_claim) == ("MISSING", [])
    valid = "동력 상실 시 밸브는 폐쇄된다."
    status, spans = relation_evidence(topic, anchor, f"{false_claim} {valid}")
    assert status == "PARTIAL"
    assert [f"{false_claim} {valid}"[span["start"]:span["end"]].strip() for span in spans] == [
        valid.removesuffix(".")
    ]
