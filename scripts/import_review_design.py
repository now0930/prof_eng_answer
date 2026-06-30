#!/usr/bin/env python3
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(".").resolve()
MODEL_BANK = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_BANK = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"

META = {
    "dc_dc_chopper_buck_converter": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "DC-DC 초퍼와 Buck/Boost 컨버터의 동작 원리",
        "questions": [
            "DC-DC 초퍼의 동작 원리와 Buck/Boost 컨버터에서 PWM 듀티비가 출력전압에 미치는 영향을 설명하시오."
        ],
        "aliases": ["DC-DC 초퍼", "Chopper", "Buck 컨버터", "Boost 컨버터", "PWM 듀티비"],
    },
    "power_semiconductor_switching_device_characteristics": {
        "question_type": "COMPARE_SELECTION",
        "title": "전력반도체 스위칭 소자의 특성과 선정 기준",
        "questions": [
            "전력반도체 스위칭 소자의 주요 특성과 선정 시 고려사항을 설명하시오."
        ],
        "aliases": ["전력반도체 소자", "스위칭 소자", "다이오드 역회복", "SCR", "MOSFET", "IGBT", "SOA"],
    },
    "induction_motor_dq_reference_frame_equivalent_circuit": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "유도전동기의 d-q 좌표변환과 회전좌표계 등가회로",
        "questions": [
            "유도전동기의 d-q 좌표변환과 회전좌표계 등가회로의 전압방정식 및 토크식을 설명하시오."
        ],
        "aliases": [
            "d-q 좌표변환",
            "회전좌표계",
            "유도전동기 등가회로",
            "벡터제어",
            "토크 방정식"
        ],
    },
    "control_valve_positioner_ip_converter": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "Control valve positioner와 I/P converter",
        "questions": [
            "Control valve positioner와 I/P converter의 동작 원리 및 피드백에 의한 밸브 위치 제어 과정을 설명하시오."
        ],
        "aliases": [
            "positioner",
            "I/P converter",
            "control valve",
            "pilot valve",
            "feedback spring",
        ],
    },
    "reference_tracking_prefilter_steady_state_error_control": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "상태피드백 기준입력 추종과 정상상태 오차 보상",
        "questions": [
            "상태피드백 제어에서 기준입력 추종 시 정상상태 오차가 발생하는 이유와 prefilter, feedforward, 적분 제어에 의한 보상 방법을 설명하시오."
        ],
        "aliases": [
            "reference tracking",
            "prefilter",
            "feedforward",
            "steady-state error",
            "integral control",
        ],
    },
    "thermopile_noncontact_ir_temperature_sensor": {
        "question_type": "COMPARE_SELECTION",
        "title": "써모파일 비접촉 적외선 온도센서",
        "questions": [
            "써모파일의 비접촉 적외선 온도측정 원리와 열전대, RTD 등 접촉식 온도센서와의 차이 및 선정 기준을 설명하시오."
        ],
        "aliases": [
            "thermopile",
            "IR temperature sensor",
            "noncontact temperature",
            "radiation",
            "emissivity",
        ],
    },
    "psd_position_sensitive_detector_optical_sensor": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "PSD 선형 광학 위치검출 센서",
        "questions": [
            "PSD(Position Sensitive Detector) 선형 광학 센서의 위치 검출 원리와 전류비를 이용한 위치 산출 방법을 설명하시오."
        ],
        "aliases": [
            "PSD",
            "position sensitive detector",
            "optical sensor",
            "current ratio",
            "position measurement",
        ],
    },
    "wheatstone_bridge_null_balance_measurement": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "Wheatstone bridge와 null balance 측정",
        "questions": [
            "Wheatstone bridge의 평형 조건과 null balance 측정 원리 및 센서 계측에서의 적용 방법을 설명하시오."
        ],
        "aliases": [
            "Wheatstone bridge",
            "null balance",
            "bridge balance",
            "strain gage",
            "RTD",
        ],
    },
    "photodiode_light_sensor_operation_modes": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "포토다이오드 광센서 동작 모드",
        "questions": [
            "포토다이오드의 동작 원리와 광전지 모드, 광전도 모드의 차이 및 적용 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "포토다이오드",
            "photodiode",
            "광전지 모드",
            "광전도 모드",
            "광전류",
            "암전류",
            "접합 커패시턴스"
        ],
    },
    "classification_model_precision_recall_f1_evaluation": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "분류 모델 Precision, Recall, F1-score 성능평가",
        "questions": [
            "분류 모델 성능평가에서 Precision, Recall, F1-score의 의미와 불균형 데이터에서의 적용 기준을 설명하시오."
        ],
        "aliases": [
            "Precision",
            "Recall",
            "F1-score",
            "혼동행렬",
            "confusion matrix",
            "분류 모델 성능평가",
            "불균형 데이터"
        ],
    },
    "mems_comb_drive_electrostatic_actuator": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "MEMS comb-drive 정전기 액추에이터",
        "questions": [
            "MEMS electrostatic actuator와 comb-drive actuator의 동작 원리, 장단점 및 적용 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "MEMS actuator",
            "electrostatic actuator",
            "comb-drive actuator",
            "정전기 액추에이터",
            "컴브 드라이브",
            "pull-in",
            "stiction"
        ],
    },
    "control_valve_body_trim_selection": {
        "question_type": "COMPARE_SELECTION",
        "title": "제어밸브 body와 trim 구조 선정",
        "questions": [
            "제어밸브의 body 형식과 trim 구조를 비교하고, balanced trim, unbalanced trim, butterfly valve 선정 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "control valve body",
            "valve trim",
            "balanced trim",
            "unbalanced trim",
            "globe valve",
            "butterfly valve",
            "plug profile",
            "seat leakage"
        ],
    },
    "sensor_linearization_transfer_function_approximation": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "센서 전달함수와 선형화 근사 방법",
        "questions": [
            "센서의 입력-출력 전달함수와 선형화, 구간별 선형근사, 다항식 근사, spline 근사 방법을 설명하시오."
        ],
        "aliases": [
            "sensor linearization",
            "센서 선형화",
            "static transfer function",
            "dynamic transfer function",
            "linear regression",
            "piecewise linear approximation",
            "lookup table",
            "spline approximation"
        ],
    },
    "sensor_static_dynamic_performance_characteristics": {
        "question_type": "COMPARE_SELECTION",
        "title": "센서 정특성·동특성과 선정 기준",
        "questions": [
            "센서에 요구되는 정특성 및 동특성을 설명하고, 센서 선정 시 감도, 분해능, 선형성, 안정도, 응답시간 등을 어떻게 고려해야 하는지 설명하시오."
        ],
        "aliases": [
            "센서 특성",
            "sensor characteristics",
            "감도",
            "분해능",
            "선형성",
            "안정도",
            "응답시간",
            "정특성",
            "동특성"
        ],
    },
    "smart_mcc_motor_control_center_monitoring": {
        "question_type": "IMPLEMENTATION_EVALUATION",
        "title": "스마트 MCC 전동기 제어반 감시와 진단",
        "questions": [
            "스마트 전동기 제어반(Smart MCC)의 구성, 특징, 장단점 및 도입 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "Smart MCC",
            "스마트 MCC",
            "Motor Control Center",
            "전동기 제어반",
            "전동기 상태감시",
            "예지보전",
            "전력품질 감시",
            "motor monitoring"
        ],
    },
    "industrial_robot_degrees_of_freedom": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "산업용 로봇 자유도와 작업 능력",
        "questions": [
            "산업용 로봇에서 자유도(DOF)의 의미를 설명하고, 3자유도, 6자유도, 7자유도 이상 로봇의 특징과 선정 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "산업용 로봇 자유도",
            "robot degree of freedom",
            "DOF",
            "3자유도",
            "6자유도",
            "7자유도",
            "위치 자유도",
            "자세 자유도"
        ],
    },
    "frame_grounding_shielding_noise_control": {
        "question_type": "DIAGNOSIS_ACTION",
        "title": "프레임 그라운드와 전자기파 차폐 대책",
        "questions": [
            "제어기 설계에서 프레임 그라운드의 목적을 설명하고, 전자기파 차폐와 노이즈 저감을 위한 적용 방법 및 주의사항을 설명하시오."
        ],
        "aliases": [
            "프레임 그라운드",
            "frame ground",
            "chassis ground",
            "전자기파 차폐",
            "EMI",
            "EMC",
            "shield grounding",
            "ground loop",
            "노이즈 접지"
        ],
    },
    "measurement_repeatability_reproducibility": {
        "question_type": "COMPARE_SELECTION",
        "title": "측정 반복성과 재현성 비교",
        "questions": [
            "측정에서 반복성(Repeatability)과 재현성(Reproducibility)을 비교하고, 품질관리 및 계측 시스템 평가에서의 의미를 설명하시오."
        ],
        "aliases": [
            "반복성",
            "재현성",
            "repeatability",
            "reproducibility",
            "Gage R&R",
            "측정 시스템 분석",
            "측정 일관성",
            "measurement variation"
        ],
    },
    "energy_harvesting_wireless_sensor_power": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "에너지 하베스팅과 무선 센서 전원",
        "questions": [
            "에너지 하베스팅(Energy Harvesting) 기술의 원리, 에너지 소스, 응용 분야 및 적용 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "에너지 하베스팅",
            "Energy Harvesting",
            "무선 센서 전원",
            "self powered sensor",
            "태양광 하베스팅",
            "열전 발전",
            "진동 에너지",
            "RF energy harvesting"
        ],
    },
    "gpib_scpi_instrumentation_communication": {
        "question_type": "PRINCIPLE_INTERPRETATION",
        "title": "GPIB와 SCPI 계측 장비 통신",
        "questions": [
            "GPIB와 SCPI의 개념, 구성, 동작 방식 및 계측 장비 자동화에서의 활용과 한계를 설명하시오."
        ],
        "aliases": [
            "GPIB",
            "SCPI",
            "IEEE 488",
            "계측 장비 통신",
            "instrumentation communication",
            "Talker",
            "Listener",
            "Controller",
            "자동시험장비"
        ],
    },
    "pressure_gauge_accessories_installation": {
        "question_type": "COMPARE_SELECTION",
        "title": "공정용 압력계 액세서리와 설치 기준",
        "questions": [
            "공정용 압력계 설치 시 사용하는 주요 액세서리의 종류, 기능, 선정 기준 및 설치 시 주의사항을 설명하시오."
        ],
        "aliases": [
            "압력계 액세서리",
            "pressure gauge accessory",
            "snubber",
            "pressure dampener",
            "overpressure protector",
            "isolating valve",
            "siphon",
            "diaphragm seal",
            "chemical seal"
        ],
    },
    "control_valve_actuator_types_selection": {
        "question_type": "COMPARE_SELECTION",
        "title": "밸브 액추에이터 종류와 선정 기준",
        "questions": [
            "밸브 액추에이터의 종류와 특징을 비교하고, 전기식, 공압식, 유압식, 수동식 액추에이터 선정 시 고려사항을 설명하시오."
        ],
        "aliases": [
            "밸브 액추에이터",
            "valve actuator",
            "electric actuator",
            "pneumatic actuator",
            "hydraulic actuator",
            "manual actuator",
            "fail open",
            "fail close"
        ],
    },
}

STOP = {"설명", "한다", "해야", "있다", "있는", "통해", "경우", "고려", "주요", "핵심"}

def grab_section(md, topic_id):
    m = re.search(rf"\n##\s+\d+\.\s+{re.escape(topic_id)}\n(.*?)(?=\n---\n|\Z)", md, re.S)
    return m.group(1).strip() if m else ""

def grab_sub(sec, title):
    m = re.search(rf"\n###\s+{re.escape(title)}\n(.*?)(?=\n###\s+|\Z)", "\n" + sec, re.S)
    return m.group(1).strip() if m else ""

def clean_line(s):
    return re.sub(r"\s+", " ", s.strip(" -\t")).strip()

def parse_outline(sec):
    txt = grab_sub(sec, "Model Answer 핵심 구조")
    out = []
    for line in txt.splitlines():
        s = clean_line(line)
        if s:
            out.append(s)
    return out[:20]

def parse_risk(sec):
    txt = grab_sub(sec, "risk")
    return [clean_line(x) for x in txt.splitlines() if clean_line(x)][:8]

def parse_anchors(sec, topic_id):
    txt = grab_sub(sec, "Fact Anchor 후보")
    anchors = []
    cur = None
    for line in txt.splitlines():
        s = clean_line(line)
        m = re.match(r"^(\d+)\.\s*(.+)", s)
        if m:
            cur = {"name": m.group(2), "expected": ""}
            anchors.append(cur)
        elif cur and s:
            cur["expected"] = s
    result = []
    for i, a in enumerate(anchors[:5], 1):
        expected = a["expected"] or f"{a['name']}을 설명해야 한다."
        result.append({
            "id": f"{topic_id}_anchor_{i}",
            "name": a["name"],
            "expected": expected,
            "core_terms": terms(a["name"] + " " + expected, 5),
            "support_terms": terms(expected, 8),
        })
    return result

def terms(text, n):
    words = re.findall(r"[A-Za-z0-9가-힣·/-]{2,}", text)
    out = []
    for w in words:
        if w in STOP:
            continue
        if w not in out:
            out.append(w)
    return out[:n] or ["핵심용어"]

def upsert_model(entry):
    data = json.loads(MODEL_BANK.read_text(encoding="utf-8"))
    items = data["answers"] if isinstance(data, dict) else data
    items[:] = [x for x in items if x.get("topic_id") != entry["topic_id"]]
    items.append(entry)
    MODEL_BANK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("model upserted:", entry["id"])

def upsert_fact(entry):
    data = json.loads(FACT_BANK.read_text(encoding="utf-8"))
    items = data["topics"] if isinstance(data, dict) else data
    items[:] = [x for x in items if x.get("topic_id") != entry["topic_id"]]
    items.append(entry)
    FACT_BANK.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("fact upserted:", entry["topic_id"])

def build(md, topic_id):
    sec = grab_section(md, topic_id)
    if not sec:
        print("skip, section not found:", topic_id)
        return

    meta = META[topic_id]
    qtype = meta["question_type"]
    outline = parse_outline(sec)
    anchors = parse_anchors(sec, topic_id)
    risk = parse_risk(sec)
    now = datetime.now().isoformat(timespec="seconds")

    model = {
        "id": f"{topic_id}_{qtype}_v1",
        "topic_id": topic_id,
        "question_type": qtype,
        "title": meta["title"],
        "question_examples": meta["questions"],
        "topic_aliases": meta["aliases"],
        "expected_structure": outline[:5],
        "model_answer_outline": outline,
        "high_score_features": [a["expected"] for a in anchors],
        "low_score_patterns": risk or ["핵심 원리와 선정 기준 없이 용어만 나열한다."],
        "field_connection_points": [
            "현장 적용 시 정격, 손실, 발열, 파형, 보호회로를 함께 검토한다.",
            "측정 시 전압 파형과 전류 파형을 함께 확인한다.",
            "설계 변경 시 효율, 신뢰성, 비용, 유지보수성을 함께 판단한다."
        ],
        "revision_notes": [
            f"created_at={now}",
            f"imported_from={sys.argv[1]}",
            "review design markdown에서 Model Answer와 Fact Anchor를 생성했다."
        ]
    }

    fact = {
        "topic_id": topic_id,
        "name": meta["title"],
        "aliases": meta["aliases"],
        "anchors": anchors,
    }

    upsert_model(model)
    upsert_fact(fact)

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: import_review_design.py <design.md>")
    p = Path(sys.argv[1])
    md = p.read_text(encoding="utf-8")
    for topic_id in META:
        build(md, topic_id)

if __name__ == "__main__":
    main()
