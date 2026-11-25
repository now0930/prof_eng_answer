"""Bounded relation evidence for selected source-owned Fact Anchors."""
from __future__ import annotations

import re
import unicodedata

SPEED = "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
FINAL = "final_control_element_sil_sis_esd_valve_partial_stroke_test"
HUMIDITY = "humidity_measurement_capacitive_resistive_dew_point_selection_compensation"
SOFTWARE = "instrumentation_control_software_lifecycle_v_model_traceability_verification_validation"

# Each component has its own accepted relation and, where supported, an
# explicit contrary relation. One component cannot stand in for another.
RULES = {
    (SPEED, "counting_window_speed_equation"): (
        (r"(?:고정|일정|그대로).{0,35}(?:측정창|측정\s*창|표본\s*구간|창)|(?:측정창|측정\s*창|표본\s*구간|창).{0,25}(?:고정|일정)|n_eff.{0,15}(?:δt|Δt|t\s*=)", ""),
        (r"(?:절대|한\s*(?:카운트|count|눈금)|한\s*count|1\s*카운트|눈금).{0,48}(?:일정|그대로|불변|변하지\s*않|\d+(?:\.\d+)?\s*rpm)|(?:rpm\s*(?:step|간격)|속도\s*간격).{0,12}(?:일정|불변)|60\s*/\s*\(\s*n_eff\s*[·*×]\s*(?:δt|t)\s*\)",
         r"(?:감소하면|낮아지면|저속).{0,40}(?:절대|한\s*카운트).{0,30}(?:증가|커진)"),
        (r"(?:저속|느릴수록|속도가\s*낮).{0,65}(?:상대|비율).{0,30}(?:커|증가|크다)", ""),
    ),
    (SPEED, "gear_tooth_speed_equation"): (
        (r"(?:평균|한\s*바퀴|전체\s*회전).{0,60}(?:유효\s*event|실측\s*펄스\s*수|실제로\s*들어온\s*펄스\s*개수|\d+\s*펄스|60\s*f\s*/\s*z)",
         r"(?:평균|전체\s*회전).{0,30}명목\s*치수.{0,15}그대로"),
        (r"(?:국부|period|결손치\s*구간|빈\s*이빨).{0,55}(?:실제\s*각도\s*간격.{0,12}(?:반영|적용|사용|환산)|정상\s*치간\s*주기로\s*쓰지\s*않|같은\s*각도로\s*계산하면\s*안)",
         r"(?:결손|missing.tooth).{0,55}(?:국부|주기).{0,35}정상\s*치간.{0,38}그대로"),
    ),
    (SPEED, "incremental_encoder_principle"): (
        (r"(?:펄스|pulse|카운트|count).{0,25}(?:누적|세며|수\s*또는\s*주파수).{0,28}(?:상대|위치|속도)|(?:증분형|incremental).{0,35}펄스를\s*세", ""),
        (r"(?:미계측|정전|차단|꺼진).{0,82}(?:복원할\s*수\s*없|복구할\s*수\s*없|변위는\s*알\s*수\s*없|(?:homing|기준점을\s*다시).{0,14}(?:필요|잡아야|한다))",
         r"(?:미계측|전원\s*차단).{0,65}(?:자동\s*복구|homing이\s*필요\s*없)"),
    ),
    (HUMIDITY, "absolute_humidity_definition"): (
        (r"(?:체적|부피|세제곱미터|m³).{0,32}(?:수증기.{0,12}(?:질량|그램))|수증기\s*질량.{0,20}(?:체적|부피)으로\s*나눈|m_v\s*/\s*v",
         r"절대습도.{0,25}건공기\s*질량당"),
    ),
    (SOFTWARE, "sw04_hil"): (
        (r"(?:실제|실물|물리).{0,23}(?:하드웨어|제어기|plc|i/o).{0,38}실시간.{0,28}(?:플랜트|공정|plant\s*model).{0,35}(?:연계|연결|입출력|폐루프|모의)",
         r"hil.{0,28}실제\s*생산설비.{0,12}반드시"),
        (r"가상\s*시운전.{0,35}(?:sil|hil).{0,20}(?:활용|적용)|virtual\s*commissioning.{0,40}(?:sil|hil).{0,20}(?:활용|적용)",
         r"(?:virtual\s*commissioning|가상\s*시운전).{0,25}hil.{0,25}상호배타적"),
    ),
    (FINAL, "fail_action_vs_safe_state"): (
        (r"(?:상실|고장|failure).{0,32}(?:개방|폐쇄|유지|위치)|고장\s*시\s*밸브\s*동작", ""),
        (r"(?:안전상태|안전한지|safe\s*state).{0,50}(?:위험\s*분석.{0,14}(?:정한|정한다|결정|기준)|hazard.based\s*process\s*requirement|별개|다르)|(?:위험\s*분석|hazard.based).{0,30}안전상태.{0,12}(?:정한|정한다|결정)|차단이\s*안전한\s*공정.{0,35}srs.{0,25}(?:선정|검증)",
         r"(?:fail\s*action.{0,25}safe\s*state.{0,20}같은\s*개념|모든\s*공정.{0,35}폐쇄.{0,18}안전상태로\s*간주)"),
    ),
    (FINAL, "imperfect_test_residual_risk"): (
        (r"(?:미검출|놓치는|검출되지\s*않|untested).{0,65}(?:제거되지\s*않|사라지지\s*않|주기를\s*그대로\s*적용하지\s*않|(?:검출[·ㆍ\s]*복구|정비|overhaul|mission\s*time|위험\s*기여).{0,30}(?:반영|평가|볼|본다|때까지|까지|사용))",
         r"(?:미검출|모든).{0,22}위험고장.{0,24}(?:매번\s*제거|pst\s*주기를\s*동일)"),
        (r"(?:실제로.{0,25}찾고\s*복구|검출[·ㆍ·\s]*복구|overhaul\s*/\s*mission\s*time).{0,35}(?:때까지|까지|반영|평가|주기를\s*사용)", ""),
    ),
    (FINAL, "response_time_process_safety_time"): (
        (r"(?:전체\s*sif|전체\s*안전기능).{0,65}(?:process\s*safety\s*time|pst|안전상태).{0,30}(?:달성|도달|이내|충족|만족)|(?:pst|process\s*safety\s*time).{0,28}전체\s*안전기능.{0,8}에\s*적용(?:하고|한다)|센서.{0,75}전체\s*시간.{0,25}허용\s*공정시간.{0,10}들어야",
         r"최종제어요소.{0,20}응답시간만.{0,75}전체\s*sif.{0,25}자동"),
        (r"(?:최종제어요소|최종요소|final.element|밸브).{0,55}(?:할당|배정).{0,22}(?:시간|allowable\s*time).{0,22}(?:비교|만족|충족|이내|검증)", ""),
    ),
    (FINAL, "redundancy_independence_boundary"): (
        (r"(?:공통\s*원인\s*고장|common\s*cause\s*failure|공통원인\s*기여|종속성|의존성).{0,45}(?:반영|고려|별도로\s*계산|모델.{0,18}평가)",
         r"(?:항상\s*완전\s*독립|공통\s*원인\s*고장.{0,30}무시|공유\s*유틸리티.{0,20}무시)"),
    ),
}

_CLAUSE = re.compile(r"[^.!?。;\n]+(?:\.[0-9]+[^.!?。;\n]*)?")
_QUOTED = re.compile(r'"[^"]*"|“[^”]*”|「[^」]*」|『[^』]*』')
_NON_ASSERTION = re.compile(
    r'["“”「」『』]|(?:라고|라는)\s*(?:주장|가정|인용)|틀린\s*(?:예|주장)|잘못된\s*(?:예|주장)|(?:아니라고|틀렸다|사실이\s*아니다)\s*$'
)


def relation_evidence(topic_id: str, anchor_id: str, answer: str):
    """Return None outside the allowlist, otherwise a status and evidence spans."""
    rules = RULES.get((topic_id, anchor_id))
    if rules is None:
        return None
    quoted = [m.span() for m in _QUOTED.finditer(answer)]
    clauses = [
        (unicodedata.normalize("NFKC", m.group()).casefold().strip(), m.span())
        for m in _CLAUSE.finditer(answer)
        if not any(m.start() < end and start < m.end() for start, end in quoted)
    ]
    clauses = [(text, span) for text, span in clauses if not _NON_ASSERTION.search(text)]
    matched = 0
    spans = set()
    for positive, negative in rules:
        if negative and any(re.search(negative, text) for text, _ in clauses):
            continue
        evidence = {span for text, span in clauses if re.search(positive, text)}
        if evidence:
            matched += 1
            spans.update(evidence)
    # A fixed window is a condition for interpreting the resolution claim,
    # not a positive claim by itself.
    if anchor_id == "counting_window_speed_equation" and not any(
        re.search(rules[0][0], text) for text, _ in clauses
    ):
        return "MISSING", []
    if anchor_id == "counting_window_speed_equation" and matched == 1:
        return "MISSING", []
    status = "SATISFIED" if matched == len(rules) else "PARTIAL" if matched else "MISSING"
    return status, [{"start": start, "end": end} for start, end in sorted(spans)]
