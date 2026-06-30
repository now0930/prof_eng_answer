#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rubric_content.model_answers import (  # type: ignore
    load_model_answer_bank,
    question_type_ids,
    save_model_answer_bank,
    upsert_model_answer,
    validate_model_answer_bank,
)
from rubric_content.fact_anchors import (  # type: ignore
    load_fact_anchor_bank,
    save_fact_anchor_bank,
    upsert_fact_anchor_topic,
    validate_fact_anchor_bank_data,
)

MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "backups"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{path.stem}.before_relation_fix.{stamp}{path.suffix}"
    shutil.copy2(path, out)
    return out


def model_entry(
    topic_id: str,
    question_type: str,
    title: str,
    aliases: list[str],
    questions: list[str],
    expected_structure: list[str],
    outline: list[str],
    high_score: list[str],
    low_score: list[str],
    field_points: list[str],
) -> dict[str, Any]:
    return {
        "id": f"{topic_id}_{question_type}_v1",
        "topic_id": topic_id,
        "question_type": question_type,
        "title": title,
        "topic_aliases": aliases,
        "question_examples": questions,
        "expected_structure": expected_structure,
        "model_answer_outline": outline,
        "high_score_features": high_score,
        "low_score_patterns": low_score,
        "field_connection_points": field_points,
        "revision_notes": [
            "Added to align model_answers with existing fact_anchors topic_id relationship.",
            "Created by scripts/apply_relation_completion_patch.py",
        ],
    }


MODEL_ENTRIES: list[dict[str, Any]] = [
    model_entry(
        "explosion_safety_sil_sis",
        "IMPLEMENTATION_EVALUATION",
        "방폭, SIL, SIS 적용 평가",
        ["방폭", "SIL", "SIS", "안전계장시스템", "Explosion proof", "Safety Instrumented System"],
        [
            "방폭 설비와 SIL/SIS의 개념 및 적용 시 고려사항을 설명하시오.",
            "위험지역 계장설비에서 방폭과 SIS 적용 기준을 설명하시오.",
        ],
        [
            "위험지역과 방폭의 목적",
            "방폭 구조와 계장기기 선정 기준",
            "SIS, SIF, SIL의 역할",
            "위험도 분석과 SIL 할당",
            "설계, 검증, proof test, 유지보수 관점",
        ],
        [
            "방폭은 폭발위험 분위기에서 점화원을 격리하거나 점화 가능성을 낮추어 폭발을 방지하기 위한 설비 선정 원칙이다.",
            "방폭기기는 위험장소 구분, 가스그룹, 온도등급, 보호방식, 케이블 글랜드와 접지 조건을 함께 검토하여 선정한다.",
            "SIS는 공정 제어계와 독립적으로 위험 상태를 감지하고 안전상태로 전환하는 안전계장시스템이며, SIF와 SIL 단위로 설계·검증한다.",
            "SIL은 장비 품질 등급이 아니라 요구 위험저감 수준이며, LOPA, HAZOP, 고장률, proof test interval, 공통원인고장을 고려한다.",
            "현장 적용 시 방폭 인증, bypass 관리, proof test 기록, 변경관리, 예비품, 유지보수 접근성, 비용을 종합 평가해야 한다.",
        ],
        [
            "위험지역 등급, 가스그룹, 온도등급을 구체적으로 연결한다.",
            "BPCS와 SIS의 독립성, 진단, fail-safe, proof test를 설명한다.",
            "SIL을 단순 중요도 등급이 아니라 위험저감 성능으로 해석한다.",
        ],
        [
            "방폭과 SIS를 같은 개념으로 설명하면 안 된다.",
            "SIL을 장비 가격이나 품질 등급처럼 설명하면 안 된다.",
            "방폭 인증, 설치 방식, 케이블 글랜드, 접지를 빠뜨리면 현장성이 부족하다.",
        ],
        ["위험지역 구분", "Ex d/Ex i", "gas group", "temperature class", "SIS", "SIF", "SIL", "LOPA", "proof test", "bypass 관리"],
    ),
    model_entry(
        "flowmeter_dp_orifice",
        "PRINCIPLE_INTERPRETATION",
        "차압식 유량계와 오리피스 유량 측정",
        ["차압식 유량계", "오리피스", "orifice flowmeter", "DP flowmeter", "위어", "벤츄리"],
        [
            "오리피스 유량계의 원리와 설치상 주의사항을 설명하시오.",
            "차압식 유량계의 유량 산출 원리와 현장 적용 한계를 설명하시오.",
        ],
        [
            "차압식 유량 측정의 원리",
            "오리피스, 벤츄리, 노즐의 구성",
            "유량과 차압의 제곱근 관계",
            "설치 조건과 보정 요소",
            "장단점, 유지보수, 적용 한계",
        ],
        [
            "차압식 유량계는 유로에 조임부를 설치하여 유속 증가와 정압 감소를 만들고, 그 차압으로 유량을 추정한다.",
            "비압축성 유체의 기본 관계는 유량이 차압의 제곱근에 비례하며, 실제 적용에서는 유량계수, 밀도, beta ratio, Reynolds number를 고려한다.",
            "오리피스는 구조가 간단하고 표준화가 쉬우나 영구 압력손실이 크고 rangeability가 제한된다.",
            "정확한 측정을 위해 상·하류 직관거리, 탭 위치, 배관 충만, impulse line 막힘, square-root extraction을 검토해야 한다.",
            "가스·증기 유량에서는 압력·온도 보상, 밀도 보상, 응축수 처리와 동결·막힘 방지가 중요하다.",
        ],
        [
            "유량과 차압의 제곱근 관계를 명확히 설명한다.",
            "직관거리, beta ratio, 유량계수, 보상 조건을 함께 언급한다.",
            "오리피스의 경제성과 압력손실, 유지보수 한계를 균형 있게 쓴다.",
        ],
        [
            "차압과 유량이 선형 비례한다고 쓰면 안 된다.",
            "초음파, 코리올리, 전자유량계 원리를 차압식과 혼동하면 안 된다.",
            "직관거리와 impulse line 조건을 빠뜨리면 현장성이 부족하다.",
        ],
        ["orifice plate", "beta ratio", "differential pressure", "square-root extraction", "impulse line", "straight run", "pressure loss"],
    ),
    model_entry(
        "hmi_scada",
        "IMPLEMENTATION_EVALUATION",
        "HMI/SCADA 구성과 운영 평가",
        ["HMI", "SCADA", "감시제어", "운전 화면", "알람", "historian"],
        [
            "HMI와 SCADA의 기능 및 구축 시 고려사항을 설명하시오.",
            "공정 감시제어 시스템의 화면, 알람, 이력관리 설계 기준을 설명하시오.",
        ],
        [
            "HMI/SCADA의 목적",
            "시스템 구성 요소",
            "화면, 알람, trend, historian 기능",
            "PLC/DCS와 통신 연계",
            "보안, 이중화, 유지보수 평가",
        ],
        [
            "HMI는 운전자가 공정 상태를 인지하고 조작하는 인터페이스이며, SCADA는 원격 감시, 제어, 데이터 수집, 이력 관리를 포함하는 상위 감시제어 시스템이다.",
            "주요 구성은 operator station, engineering station, server, historian, alarm server, 통신 gateway, PLC/DCS/RTU 연계로 설명할 수 있다.",
            "좋은 HMI는 process overview, abnormal situation detection, alarm priority, trend, interlock 상태, manual/auto 상태를 명확히 제공해야 한다.",
            "SCADA 구축 시 통신 지연, time synchronization, redundancy, backup/restore, user authority, audit trail, cyber security를 고려한다.",
            "현장 적용에서는 화면 표준화, 알람 rationalization, 변경관리, 운영자 교육, 장애 시 수동운전 절차가 중요하다.",
        ],
        [
            "HMI와 SCADA의 범위 차이를 구분한다.",
            "알람 관리, historian, 사용자 권한, 보안을 포함한다.",
            "운전성, 유지보수성, 장애 대응성을 평가한다.",
        ],
        [
            "HMI를 단순 모니터 화면으로만 설명하면 부족하다.",
            "알람 flooding, 권한관리, 보안, 이력관리를 빠뜨리면 고득점이 어렵다.",
            "PLC/DCS와 SCADA의 역할을 혼동하면 안 된다.",
        ],
        ["operator station", "alarm management", "historian", "trend", "redundancy", "time sync", "user authority", "cyber security"],
    ),
    model_entry(
        "industrial_communication_protocol",
        "COMPARE_SELECTION",
        "산업용 통신 프로토콜 비교와 선정",
        ["산업용 통신", "Modbus", "Profibus", "Profinet", "EtherNet/IP", "HART", "Fieldbus", "OPC UA"],
        [
            "산업용 통신 프로토콜의 종류와 선정 기준을 설명하시오.",
            "계장 시스템에서 Modbus, HART, Fieldbus, Industrial Ethernet의 적용 차이를 설명하시오.",
        ],
        [
            "산업용 통신의 목적",
            "계층과 물리 매체",
            "주요 프로토콜 비교",
            "실시간성, 신뢰성, 확장성 평가",
            "OT 보안과 유지보수 고려",
        ],
        [
            "산업용 통신은 현장기기, PLC, DCS, SCADA, historian 사이에서 측정값, 상태, 진단, 제어 명령을 안정적으로 교환하기 위한 기반이다.",
            "Modbus는 단순성과 범용성이 장점이나 고급 진단과 실시간성이 제한될 수 있고, HART는 4~20mA 위에 디지털 진단 정보를 중첩한다.",
            "Profibus/Fieldbus 계열은 field device 통합과 진단에 강하고, Profinet/EtherNet/IP 같은 Industrial Ethernet은 고속·대용량·상위 연계에 유리하다.",
            "프로토콜 선정은 update time, determinism, topology, redundancy, cable distance, noise immunity, device support, vendor compatibility를 기준으로 한다.",
            "현장 적용에서는 network segmentation, firewall, account 관리, time synchronization, packet capture, spare module, 장애 진단 절차를 포함해야 한다.",
        ],
        [
            "프로토콜별 장단점과 적용 위치를 구체적으로 비교한다.",
            "실시간성, 결정성, 노이즈, 이중화, 보안을 함께 평가한다.",
            "4~20mA/HART와 Fieldbus/Ethernet 계열의 차이를 설명한다.",
        ],
        [
            "모든 통신을 Ethernet으로만 설명하면 부족하다.",
            "속도만으로 프로토콜을 선정하면 안 된다.",
            "OT 보안과 장애 진단 절차를 빠뜨리면 현장성이 낮다.",
        ],
        ["Modbus", "HART", "Profibus", "Profinet", "EtherNet/IP", "OPC UA", "determinism", "redundancy", "OT security"],
    ),
    model_entry(
        "motor_inverter_drive",
        "PRINCIPLE_INTERPRETATION",
        "전동기 인버터 구동 원리와 적용",
        ["인버터", "VFD", "전동기 구동", "motor drive", "PWM", "가변속"],
        [
            "인버터를 이용한 전동기 가변속 구동 원리와 적용 시 고려사항을 설명하시오.",
            "VFD의 구성과 전동기 제어 특성을 설명하시오.",
        ],
        [
            "인버터 구동의 목적",
            "정류부, DC link, 인버터부 구성",
            "V/f 제어와 벡터제어 개념",
            "전동기와 부하 특성",
            "보호, 고조파, EMC, 유지보수 고려",
        ],
        [
            "인버터는 전원 주파수와 전압을 가변하여 유도전동기 등의 속도와 토크를 제어하는 전력변환 장치이다.",
            "기본 구성은 정류부, DC link, 인버터부, 게이트 드라이브, 제어부, 보호회로로 이루어지며 PWM을 통해 출력 전압과 주파수를 합성한다.",
            "V/f 제어는 자속 유지를 위해 전압과 주파수 비를 관리하고, 벡터제어는 자속 전류와 토크 전류를 분리하여 응답성과 정밀도를 높인다.",
            "적용 시 부하 토크 특성, acceleration/deceleration time, regenerative energy, braking resistor, motor insulation, cable length를 검토한다.",
            "현장에서는 고조파, 누설전류, bearing current, EMC, 접지, 냉각, 파라미터 백업, 보호 설정과 spare policy가 중요하다.",
        ],
        [
            "전력변환 구조와 제어 방식의 차이를 설명한다.",
            "부하 특성, 가감속, 회생, 보호를 함께 고려한다.",
            "EMC, 접지, 베어링 전류, 절연 등 현장 문제를 언급한다.",
        ],
        [
            "인버터를 단순 속도조절기라고만 쓰면 부족하다.",
            "V/f와 벡터제어를 혼동하면 안 된다.",
            "고조파, EMC, motor insulation, cable length를 빠뜨리면 현장성이 낮다.",
        ],
        ["VFD", "PWM", "DC link", "V/f control", "vector control", "harmonics", "EMC", "bearing current", "braking resistor"],
    ),
    model_entry(
        "noise_grounding_surge",
        "DIAGNOSIS_ACTION",
        "노이즈, 접지, 서지 문제 진단과 대책",
        ["노이즈", "접지", "서지", "EMI", "RFI", "shield", "ground loop"],
        [
            "계장 신호에서 노이즈와 접지 문제의 원인 및 대책을 설명하시오.",
            "서지와 EMI가 계측제어 시스템에 미치는 영향과 방지 대책을 설명하시오.",
        ],
        [
            "노이즈와 서지의 영향",
            "발생 원인과 유입 경로",
            "접지와 차폐 원칙",
            "필터, 절연, SPD 적용",
            "진단과 유지보수 절차",
        ],
        [
            "계장 신호는 mV, 4~20mA, pulse, fieldbus 등 낮은 에너지 신호가 많아 전자기 노이즈, 접지 전위차, 서지에 의해 오동작할 수 있다.",
            "주요 원인은 전력선과 신호선 병행 포설, 인버터 스위칭, 낙뢰, 접지 루프, shield 양단 접지 오류, 절연 불량, 공통모드 전압이다.",
            "대책은 전력선·신호선 분리, twisted pair, shield 단일점 또는 설계 기준에 맞는 접지, 절연 amplifier, filter, surge protective device 적용이다.",
            "통신선과 아날로그 신호는 접지 기준, cable tray 분리, bonding, gland 처리, intrinsic safety 접지 조건을 함께 검토해야 한다.",
            "진단은 trend, oscilloscope, loop calibrator, insulation test, grounding resistance, event log, noise source on/off test로 원인을 좁힌다.",
        ],
        [
            "노이즈 유입 경로와 신호 종류별 영향 차이를 설명한다.",
            "shield, grounding, isolation, SPD, filtering을 목적별로 구분한다.",
            "진단 절차와 시공 기준을 함께 제시한다.",
        ],
        [
            "무조건 접지를 많이 하면 좋다고 쓰면 안 된다.",
            "shield 양단/단일점 접지 조건을 구분하지 않으면 위험하다.",
            "노이즈와 서지를 같은 현상으로만 설명하면 부족하다.",
        ],
        ["EMI", "RFI", "ground loop", "shield", "twisted pair", "SPD", "isolation", "common mode", "bonding"],
    ),
    model_entry(
        "pid_control",
        "PRINCIPLE_INTERPRETATION",
        "PID 제어 동작과 튜닝",
        ["PID", "비례적분미분", "P 제어", "I 제어", "D 제어", "튜닝", "제어루프"],
        [
            "PID 제어의 P, I, D 동작과 튜닝 시 고려사항을 설명하시오.",
            "공정 제어에서 PID 제어기의 역할과 현장 적용 문제를 설명하시오.",
        ],
        [
            "PID 제어의 목적",
            "P, I, D 동작의 의미",
            "응답 특성과 튜닝 영향",
            "windup, derivative kick, noise 문제",
            "현장 적용과 유지보수 기준",
        ],
        [
            "PID 제어는 설정값과 측정값의 오차를 이용하여 조작량을 계산하는 대표적 feedback 제어 방식이다.",
            "P 동작은 오차에 비례한 즉각적 조작을 제공하지만 단독으로는 offset이 남을 수 있다.",
            "I 동작은 오차를 누적하여 정상상태 offset을 제거하지만 과도하게 크면 overshoot와 hunting을 유발할 수 있다.",
            "D 동작은 오차 변화율에 반응하여 예측적 감쇠를 제공하지만 측정 노이즈와 derivative kick에 민감하다.",
            "현장 튜닝은 공정 dead time, time constant, valve stiction, sensor noise, sampling time, anti-windup, manual/auto 전환을 함께 고려해야 한다.",
        ],
        [
            "P/I/D 각각이 응답에 미치는 영향을 구분한다.",
            "offset, overshoot, hunting, settling time을 연결해 설명한다.",
            "anti-windup, derivative filtering, 현장 밸브 문제를 포함한다.",
        ],
        [
            "P, I, D를 단순 약어로만 나열하면 안 된다.",
            "I 동작이 항상 응답을 좋게 만든다고 쓰면 안 된다.",
            "D 동작의 노이즈 민감성을 빠뜨리면 부족하다.",
        ],
        ["offset", "overshoot", "hunting", "dead time", "anti-windup", "derivative kick", "sampling time", "valve stiction"],
    ),
    model_entry(
        "plc_dcs_remote_io",
        "COMPARE_SELECTION",
        "PLC, DCS, Remote I/O 구성 비교",
        ["PLC", "DCS", "Remote I/O", "분산제어", "제어시스템 구성"],
        [
            "PLC, DCS, Remote I/O의 특징과 적용 기준을 비교하시오.",
            "분산제어 시스템에서 Remote I/O를 적용할 때 고려사항을 설명하시오.",
        ],
        [
            "PLC, DCS, Remote I/O의 역할",
            "구성 요소와 적용 대상",
            "응답성, 확장성, 신뢰성 비교",
            "통신과 이중화 검토",
            "유지보수, 비용, migration 고려",
        ],
        [
            "PLC는 discrete logic, sequence, machine control에 강하고, DCS는 연속공정의 loop control, operation integration, alarm/historian 연계에 강하다.",
            "Remote I/O는 현장 가까이에 I/O를 배치하여 배선량과 panel 공간을 줄이고, controller와 통신망으로 연결하는 구조이다.",
            "시스템 선정은 I/O 수량, scan time, loop 수, batch/continuous 특성, redundancy, SIL 요구, vendor support, lifecycle cost를 기준으로 한다.",
            "Remote I/O 적용 시 통신 지연, network failure, power redundancy, environmental rating, spare channel, cable route, grounding을 검토해야 한다.",
            "기존 설비 migration에서는 downtime, cutover plan, loop check, FAT/SAT, operator training, spare strategy가 중요하다.",
        ],
        [
            "PLC와 DCS의 적용 영역을 공정 특성과 연결한다.",
            "Remote I/O의 배선 절감 장점과 통신 의존 리스크를 함께 쓴다.",
            "이중화, scan time, 유지보수, migration을 포함한다.",
        ],
        [
            "PLC와 DCS를 단순 크기 차이로만 설명하면 안 된다.",
            "Remote I/O를 단순 단자대처럼 설명하면 부족하다.",
            "통신 장애와 전원 이중화를 빠뜨리면 현장성이 낮다.",
        ],
        ["scan time", "remote I/O", "redundancy", "loop check", "FAT", "SAT", "migration", "network failure", "spare channel"],
    ),
    model_entry(
        "pressure_dp_transmitter",
        "PRINCIPLE_INTERPRETATION",
        "압력·차압 전송기 원리와 설치",
        ["압력전송기", "차압전송기", "DP transmitter", "pressure transmitter", "remote seal"],
        [
            "압력전송기와 차압전송기의 원리 및 설치 시 고려사항을 설명하시오.",
            "압력 계측에서 zero/span, impulse line, remote seal의 영향을 설명하시오.",
        ],
        [
            "압력 계측의 종류",
            "압력·차압 전송기 원리",
            "LRV/URV, zero/span 의미",
            "설치와 impulse line 고려",
            "오차, 보호, 유지보수 기준",
        ],
        [
            "압력전송기는 공정 압력을 센서 변형, 정전용량, piezoresistive 등의 방식으로 검출하여 표준 신호로 변환한다.",
            "차압전송기는 두 압력 포트의 차이를 측정하며 유량, 액위, 필터 막힘, 밀도 측정 등에 활용된다.",
            "LRV/URV는 측정 범위의 하한과 상한이고, zero/span 조정은 4~20mA 출력과 공정 압력의 대응을 맞추는 작업이다.",
            "설치 시 impulse line 기울기, 막힘, 기포·응축수, freezing, wet leg/dry leg, zero elevation/suppression을 검토해야 한다.",
            "고온·부식·점성 유체에는 diaphragm seal과 capillary를 적용할 수 있으나 응답 지연과 온도 영향을 함께 고려해야 한다.",
        ],
        [
            "게이지압, 절대압, 차압의 차이를 구분한다.",
            "차압전송기의 다양한 적용 예를 설명한다.",
            "impulse line, remote seal, static pressure effect, 유지보수를 포함한다.",
        ],
        [
            "압력과 차압을 같은 개념으로 설명하면 안 된다.",
            "4~20mA만 설명하고 sensing 원리와 설치 오차를 빠뜨리면 부족하다.",
            "remote seal의 응답 지연과 온도 영향을 무시하면 안 된다.",
        ],
        ["gauge pressure", "absolute pressure", "differential pressure", "LRV", "URV", "zero/span", "impulse line", "wet leg", "remote seal"],
    ),
    model_entry(
        "transfer_function_state_space",
        "COMPARE_SELECTION",
        "전달함수와 상태공간 모델 비교",
        ["전달함수", "상태공간", "state space", "transfer function", "제어모델"],
        [
            "전달함수와 상태공간 모델의 차이와 적용 기준을 설명하시오.",
            "제어 시스템 해석에서 전달함수와 상태방정식의 장단점을 비교하시오.",
        ],
        [
            "모델 표현의 목적",
            "전달함수의 정의와 특징",
            "상태공간 모델의 정의와 특징",
            "극점, 고유값, 안정도 해석",
            "SISO/MIMO, 현대제어 적용 기준",
        ],
        [
            "전달함수는 초기조건을 0으로 두고 입력과 출력의 Laplace 변환 비로 시스템 동특성을 표현하는 모델이다.",
            "전달함수는 SISO 시스템, 주파수응답, root locus, Bode plot, classic control 해석에 직관적이다.",
            "상태공간 모델은 내부 상태변수와 입력·출력 관계를 미분방정식 형태로 표현하며 MIMO 시스템과 현대제어 설계에 적합하다.",
            "전달함수의 극점은 상태행렬의 고유값과 연결되어 안정도와 동특성을 나타내지만, 상태공간은 controllability와 observability까지 평가할 수 있다.",
            "현장 적용에서는 모델 식별 정확도, 선형화 범위, 센서·actuator 제한, digital implementation, 유지보수자가 이해 가능한 표현을 고려한다.",
        ],
        [
            "전달함수와 상태공간의 수학적 정의를 구분한다.",
            "SISO/MIMO, 초기조건, 내부상태, 관측·제어 가능성을 비교한다.",
            "고전제어와 현대제어 적용 차이를 설명한다.",
        ],
        [
            "상태공간을 전달함수의 다른 표기라고만 설명하면 부족하다.",
            "초기조건, 내부상태, controllability/observability를 빠뜨리면 안 된다.",
            "모델이 실제 공정의 유효 범위를 가진다는 점을 무시하면 위험하다.",
        ],
        ["Laplace transform", "state equation", "A matrix", "pole", "eigenvalue", "controllability", "observability", "MIMO", "linearization"],
    ),
]


DIFF_PRESSURE_CAL_FACT = {
    "topic_id": "differential_pressure_transmitter_calibration",
    "name": "차압전송기 교정",
    "aliases": ["차압전송기 교정", "DP transmitter calibration", "zero span", "LRV URV", "as-found as-left"],
    "triggers": ["차압전송기 교정", "DP transmitter calibration", "zero 조정", "span 조정", "LRV", "URV", "4-20mA 교정"],
    "anchors": [
        {
            "id": "differential_pressure_transmitter_calibration_anchor_1",
            "name": "교정 목적과 출력 대응",
            "expected": "차압전송기 교정은 기준 차압 입력에 대해 LRV/URV와 4~20mA 출력 대응을 확인하고 허용오차 내로 조정하는 절차이다.",
            "core_terms": ["차압전송기", "LRV", "URV", "4~20mA", "허용오차"],
            "support_terms": ["calibration", "range", "output", "span"],
        },
        {
            "id": "differential_pressure_transmitter_calibration_anchor_2",
            "name": "zero/span 조정",
            "expected": "zero 조정은 하한 입력에서의 출력 오차를, span 조정은 상한 입력과 측정 범위 전체의 기울기 오차를 보정하는 작업이다.",
            "core_terms": ["zero", "span", "하한", "상한", "기울기 오차"],
            "support_terms": ["offset", "gain error", "adjustment"],
        },
        {
            "id": "differential_pressure_transmitter_calibration_anchor_3",
            "name": "다점 상승·하강 교정",
            "expected": "상승·하강 다점 교정을 수행하여 선형성, 히스테리시스, 반복성, 영점 복귀 상태를 확인해야 한다.",
            "core_terms": ["다점 교정", "상승", "하강", "선형성", "히스테리시스", "반복성"],
            "support_terms": ["linearity", "repeatability", "as-found"],
        },
        {
            "id": "differential_pressure_transmitter_calibration_anchor_4",
            "name": "현장 배관과 manifold 영향",
            "expected": "manifold의 equalizing, vent, drain 조작과 impulse line 막힘, 기포, 응축수, 누설은 현장 교정 오차에 직접 영향을 준다.",
            "core_terms": ["manifold", "equalizing valve", "vent", "drain", "impulse line"],
            "support_terms": ["막힘", "기포", "응축수", "누설", "현장오차"],
        },
        {
            "id": "differential_pressure_transmitter_calibration_anchor_5",
            "name": "기록과 유지보수",
            "expected": "as-found/as-left 결과, 기준기 추적성, 교정일자, 조정 내역, 허용오차 판정은 유지보수 이력과 품질 보증에 필요하다.",
            "core_terms": ["as-found", "as-left", "추적성", "교정 기록", "허용오차 판정"],
            "support_terms": ["traceability", "maintenance history", "quality assurance"],
        },
    ],
}


def sanitize_flowmeter_triggers(fact_bank: dict[str, Any]) -> bool:
    changed = False
    banned = {
        "초음파유량계",
        "초음파 유량계",
        "도플러",
        "도플러 유량계",
        "Doppler",
        "doppler",
        "ultrasonic flowmeter",
    }
    for topic in fact_bank.get("topics", []):
        if not isinstance(topic, dict) or topic.get("topic_id") != "flowmeter_dp_orifice":
            continue
        triggers = topic.get("triggers")
        if isinstance(triggers, list):
            new_triggers = [x for x in triggers if x not in banned]
            if new_triggers != triggers:
                topic["triggers"] = new_triggers
                changed = True
    return changed


def relationship_report(model_bank: dict[str, Any], fact_bank: dict[str, Any]) -> None:
    answers = model_bank.get("answers", [])
    topics = fact_bank.get("topics", [])

    model_ids = [a.get("topic_id") for a in answers if isinstance(a, dict) and a.get("topic_id")]
    fact_ids = [t.get("topic_id") for t in topics if isinstance(t, dict) and t.get("topic_id")]

    model_counter = Counter(model_ids)
    fact_counter = Counter(fact_ids)
    model_set = set(model_ids)
    fact_set = set(fact_ids)

    only_in_model = sorted(model_set - fact_set)
    only_in_fact = sorted(fact_set - model_set)
    bad_anchor_count = [
        (t.get("topic_id"), len(t.get("anchors", [])))
        for t in topics
        if isinstance(t, dict) and len(t.get("anchors", [])) != 5
    ]

    print("\n=== Relationship report ===")
    print(f"model_answers answers 수        : {len(answers)}")
    print(f"model_answers unique topic_id 수: {len(model_set)}")
    print(f"fact_anchors topics 수          : {len(topics)}")
    print(f"fact_anchors unique topic_id 수 : {len(fact_set)}")
    print(f"양쪽 모두 존재하는 topic_id 수  : {len(model_set & fact_set)}")
    print(f"model에만 있는 topic_id 수      : {len(only_in_model)}")
    print(f"fact에만 있는 topic_id 수       : {len(only_in_fact)}")

    print("\nmodel_answers에만 있는 topic_id:")
    if only_in_model:
        for tid in only_in_model:
            print(f"- {tid} | variants={model_counter[tid]}")
    else:
        print("OK: 없음")

    print("\nfact_anchors에만 있는 topic_id:")
    if only_in_fact:
        for tid in only_in_fact:
            print(f"- {tid} | topics={fact_counter[tid]}")
    else:
        print("OK: 없음")

    print("\nanchor 개수가 5개가 아닌 topic:")
    if bad_anchor_count:
        for tid, n in bad_anchor_count:
            print(f"- {tid}: anchors={n}")
    else:
        print("OK: 없음")

    if not only_in_model and not only_in_fact and not bad_anchor_count:
        print("\nOK: topic_id 기준 관계가 정합합니다.")
    else:
        print("\nWARN: 아직 관계 불일치가 남아 있습니다.")


def main() -> int:
    if not MODEL_PATH.exists() or not FACT_PATH.exists():
        print("ERROR: run this script from the prof_eng_answer repository root.", file=sys.stderr)
        return 2

    print("backup model:", backup(MODEL_PATH))
    print("backup fact :", backup(FACT_PATH))

    model_bank = load_model_answer_bank(MODEL_PATH)
    fact_bank = load_fact_anchor_bank(FACT_PATH)

    for entry in MODEL_ENTRIES:
        model_bank = upsert_model_answer(model_bank, entry)
        print("upsert model_answer:", entry["topic_id"])

    fact_bank = upsert_fact_anchor_topic(fact_bank, DIFF_PRESSURE_CAL_FACT)
    print("upsert fact_anchor :", DIFF_PRESSURE_CAL_FACT["topic_id"])

    if sanitize_flowmeter_triggers(fact_bank):
        print("cleanup fact_anchor: flowmeter_dp_orifice triggers sanitized")

    model_errors = validate_model_answer_bank(model_bank, allowed_types=question_type_ids())
    fact_errors = validate_fact_anchor_bank_data(fact_bank)

    if model_errors or fact_errors:
        print("\nINVALID before save")
        for err in model_errors:
            print("model:", err)
        for err in fact_errors:
            print("fact :", err)
        return 1

    save_model_answer_bank(model_bank, MODEL_PATH)
    save_fact_anchor_bank(fact_bank, FACT_PATH)

    print("\nSaved:")
    print("-", MODEL_PATH)
    print("-", FACT_PATH)

    relationship_report(model_bank, fact_bank)

    print("\n=== validate-all ===")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rubric_manager.py"), "validate-all"],
        cwd=ROOT,
        text=True,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
