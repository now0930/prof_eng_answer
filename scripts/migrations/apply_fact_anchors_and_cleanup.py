#!/usr/bin/env python3
"""
Add missing fact_anchor topics and clean related model_answer entries for
rubrics/model_answers/industrial_instrumentation_control.json and
rubrics/fact_anchors/industrial_instrumentation_control.json.

Run from the repository root:
    python3 scripts/migrations/apply_fact_anchors_and_cleanup.py
    python3 scripts/rubric_manager.py validate-all

This script is idempotent: it upserts fact_anchor topics by topic_id and only
edits targeted model_answer fields for known topics.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "scripts" else Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rubric_content.common import (  # noqa: E402
    FACT_ANCHOR_BANK,
    MODEL_ANSWER_BANK,
    backup_file,
    read_json,
    write_json,
)
from rubric_content.fact_anchors import (  # noqa: E402
    load_fact_anchor_bank,
    save_fact_anchor_bank,
    upsert_fact_anchor_topic,
    validate_fact_anchor_bank_data,
)

try:
    from rubric_registry import (  # type: ignore  # noqa: E402
        load_model_answer_bank,
        save_model_answer_bank,
        validate_model_answer_bank,
        question_type_ids,
    )
except Exception:  # pragma: no cover - fallback for older repo layouts
    load_model_answer_bank = None
    save_model_answer_bank = None
    validate_model_answer_bank = None
    question_type_ids = None

REVISION_NOTE = "updated_by=apply_fact_anchors_and_cleanup.py; reason=align model_answers with fact_anchors and review cleanup"


def anchor(topic_id: str, num: int, name: str, expected: str, core: list[str], support: list[str]) -> dict[str, Any]:
    return {
        "id": f"{topic_id}_anchor_{num}",
        "name": name,
        "expected": expected,
        "core_terms": core,
        "support_terms": support,
    }


FACT_TOPICS: list[dict[str, Any]] = [
    {
        "topic_id": "vibration_measurement_condition_monitoring",
        "priority": "high",
        "name": "회전체 진동 측정과 상태감시",
        "aliases": [
            "진동 측정", "진동 감시", "vibration monitoring", "condition monitoring",
            "변위 센서", "속도 센서", "가속도 센서", "shaft vibration", "housing vibration", "bearing fault",
        ],
        "triggers": [
            "진동", "진동감시", "condition monitoring", "변위센서", "속도센서", "가속도센서",
            "shaft vibration", "housing vibration", "bearing", "trip relay",
        ],
        "anchors": [
            anchor(
                "vibration_measurement_condition_monitoring", 1,
                "센서별 측정 대상 구분",
                "변위 센서는 주로 축 상대변위와 저속 대형 회전체 shaft vibration 감시에, 속도 센서는 housing vibration의 진동 심각도 평가에, 가속도 센서는 고주파 bearing fault와 충격성 진동 진단에 적합하다고 구분해야 한다.",
                ["변위 센서", "속도 센서", "가속도 센서", "shaft vibration", "housing vibration", "bearing fault"],
                ["proximity probe", "velocity pickup", "accelerometer", "relative vibration", "absolute vibration"],
            ),
            anchor(
                "vibration_measurement_condition_monitoring", 2,
                "주파수 대역과 신호 특성",
                "저주파·대변위 영역은 변위, 중간 주파수 기계 진동 심각도는 속도, 고주파 결함과 충격 검출은 가속도가 유리하며 적분·미분 변환만으로 모든 센서를 대체할 수 없다고 설명해야 한다.",
                ["저주파", "중간 주파수", "고주파", "적분", "미분"],
                ["frequency range", "noise", "mounting", "signal conditioning", "filter"],
            ),
            anchor(
                "vibration_measurement_condition_monitoring", 3,
                "보호용 trip과 진단용 monitoring 구분",
                "보호용 trip은 설비 손상 방지를 위한 신뢰성 높은 alarm/trip 설정과 오동작 방지가 핵심이고, 진단용 monitoring은 trend, spectrum, FFT, envelope 등으로 원인 분석과 예방정비를 수행하는 기능이라고 구분해야 한다.",
                ["trip", "monitoring", "alarm", "trend", "FFT"],
                ["envelope", "spectrum", "setpoint", "relay", "preventive maintenance"],
            ),
            anchor(
                "vibration_measurement_condition_monitoring", 4,
                "설치와 계측 신뢰성",
                "센서 선정만이 아니라 설치 위치, mounting 강성, 케이블·접지·노이즈, 간극 조정, 온도 환경, 교정과 loop test가 진동 감시 신뢰도에 영향을 준다고 설명해야 한다.",
                ["설치 위치", "mounting", "노이즈", "간극", "교정"],
                ["grounding", "cable", "loop test", "temperature", "gap voltage"],
            ),
            anchor(
                "vibration_measurement_condition_monitoring", 5,
                "현장 적용과 유지보수 판단",
                "회전체 중요도, 운전 속도, 베어링 형식, 위험도, 기존 DCS/PLC/SIS 연계, 예비품과 유지보수 비용을 고려하여 보호와 진단의 목적에 맞게 센서와 시스템을 선정해야 한다.",
                ["회전체 중요도", "운전 속도", "베어링", "DCS", "PLC", "SIS"],
                ["예비품", "유지보수", "risk", "redundancy", "cost"],
            ),
        ],
    },
    {
        "topic_id": "doppler_effect_velocity_flow_measurement",
        "priority": "high",
        "name": "도플러 효과와 속도·유량 측정",
        "aliases": [
            "도플러 효과", "Doppler effect", "도플러 유량계", "Doppler flowmeter",
            "초음파 도플러", "레이더 속도계", "주파수 편이", "frequency shift",
        ],
        "triggers": [
            "도플러", "Doppler", "주파수 편이", "접근 시 주파수", "이격 시 주파수", "도플러 유량계", "초음파 도플러", "레이더 속도",
        ],
        "anchors": [
            anchor(
                "doppler_effect_velocity_flow_measurement", 1,
                "도플러 주파수 변화 방향",
                "송신원 또는 반사체가 관측자 쪽으로 접근하면 수신 주파수는 증가하고, 멀어지면 수신 주파수는 감소한다고 설명해야 한다.",
                ["접근", "주파수 증가", "이격", "주파수 감소", "Doppler shift"],
                ["상대속도", "파동", "반사파", "수신 주파수"],
            ),
            anchor(
                "doppler_effect_velocity_flow_measurement", 2,
                "반사파 기반 속도 산출",
                "도플러 속도 측정은 송신파와 이동 물체 또는 유체 내 산란체에서 돌아온 반사파의 주파수 차이를 이용해 속도 성분을 산출한다.",
                ["송신파", "반사파", "주파수 차", "속도"],
                ["입사각", "cosine", "radar", "ultrasonic", "scatterer"],
            ),
            anchor(
                "doppler_effect_velocity_flow_measurement", 3,
                "도플러 초음파 유량계의 반사체 조건",
                "도플러 초음파 유량계는 유체 내 입자, 기포, 슬러리 등 초음파를 산란시키는 반사체가 필요하며 깨끗한 단상 액체에는 transit-time 방식이 더 적합할 수 있다.",
                ["입자", "기포", "반사체", "산란체", "transit-time"],
                ["슬러리", "탁도", "single-phase", "ultrasonic flowmeter"],
            ),
            anchor(
                "doppler_effect_velocity_flow_measurement", 4,
                "적용 분야 구분",
                "레이다는 주로 비접촉 거리·속도 측정에, 초음파 도플러는 유체 속 산란체 속도 측정에, 유량계는 관 단면적과 평균 유속을 이용한 유량 산정에 적용된다고 구분해야 한다.",
                ["레이다", "초음파", "유량", "평균 유속", "관 단면적"],
                ["non-contact", "velocity", "flow rate", "profile", "installation"],
            ),
            anchor(
                "doppler_effect_velocity_flow_measurement", 5,
                "한계와 설치 조건",
                "도플러 측정은 입사각, 반사 신호 세기, 유속 분포, 배관 충만 상태, 기포·입자 농도, 직관거리, 노이즈에 영향을 받으므로 적용 조건 검토가 필요하다.",
                ["입사각", "신호 세기", "유속 분포", "직관거리", "노이즈"],
                ["SNR", "pipe full", "concentration", "alignment", "calibration"],
            ),
        ],
    },
    {
        "topic_id": "adc_dac_signal_conversion_interface",
        "priority": "high",
        "name": "ADC/DAC 신호 변환과 계측 인터페이스",
        "aliases": ["ADC", "DAC", "A/D 변환", "D/A 변환", "sampling", "quantization", "LSB", "샘플링 지터"],
        "triggers": ["ADC", "DAC", "A/D", "D/A", "표본화", "양자화", "부호화", "해상도", "샘플링", "jitter"],
        "anchors": [
            anchor(
                "adc_dac_signal_conversion_interface", 1,
                "ADC 변환 단계",
                "ADC는 아날로그 입력을 일정 주기로 표본화하고, 각 표본값을 유한한 단계로 양자화한 뒤, 디지털 코드로 부호화하는 과정이라고 설명해야 한다.",
                ["ADC", "표본화", "양자화", "부호화", "디지털 코드"],
                ["sample and hold", "sampling period", "LSB", "binary code"],
            ),
            anchor(
                "adc_dac_signal_conversion_interface", 2,
                "DAC 변환 단계",
                "DAC는 디지털 코드를 디코딩하고 저항 가중합, 전류 가중합 또는 스위치드 커패시터 방식 등으로 아날로그 값을 합성한 뒤, 필요 시 reconstruction filter로 계단파 성분을 완화한다.",
                ["DAC", "디코딩", "가중 합성", "필터링", "아날로그 출력"],
                ["R-2R", "current steering", "zero-order hold", "reconstruction filter"],
            ),
            anchor(
                "adc_dac_signal_conversion_interface", 3,
                "해상도와 정확도의 구분",
                "bit 수가 증가하면 LSB가 작아져 해상도는 좋아지지만, offset error, gain error, noise, 기준전압, 비선형성이 나쁘면 전체 정확도가 항상 좋아지는 것은 아니다.",
                ["bit 수", "해상도", "정확도", "LSB", "offset error", "gain error"],
                ["reference voltage", "noise", "accuracy", "resolution"],
            ),
            anchor(
                "adc_dac_signal_conversion_interface", 4,
                "오차 요인",
                "양자화 오차, 오프셋 오차, 이득 오차, INL/DNL, 샘플링 지터, 기준전압 불안정, 노이즈가 계측 신호 품질에 영향을 준다고 설명해야 한다.",
                ["양자화 오차", "오프셋 오차", "이득 오차", "INL", "DNL", "샘플링 지터"],
                ["reference", "noise", "linearity", "calibration"],
            ),
            anchor(
                "adc_dac_signal_conversion_interface", 5,
                "계측 인터페이스 적용 조건",
                "실제 PLC/DCS/DAQ 인터페이스에서는 anti-aliasing filter, 샘플링 주기, 입력 범위, 절연, 접지, shield, common-mode noise, 보정과 진단 기능을 함께 고려해야 한다.",
                ["anti-aliasing", "샘플링 주기", "입력 범위", "절연", "접지"],
                ["DCS", "PLC", "DAQ", "shield", "common-mode", "calibration"],
            ),
        ],
    },
    {
        "topic_id": "temperature_sensor_thermowell_material_selection",
        "priority": "high",
        "name": "온도센서 보호관 thermowell 재질·형상 선정",
        "aliases": ["thermowell", "보호관", "온도계 보호관", "wake frequency", "삽입 길이", "보호관 재질"],
        "triggers": ["thermowell", "보호관", "온도센서 보호", "삽입 길이", "wake frequency", "보호관 파손", "재질 선정"],
        "anchors": [
            anchor(
                "temperature_sensor_thermowell_material_selection", 1,
                "thermowell 목적",
                "Thermowell은 온도센서를 공정 유체의 압력, 부식, 침식, 유속, 충격으로부터 보호하고 압력 경계를 유지하면서 운전 중 센서 교체성을 확보하는 부품이라고 설명해야 한다.",
                ["thermowell", "센서 보호", "압력 경계", "센서 교체", "공정 유체"],
                ["RTD", "thermocouple", "maintenance", "process isolation"],
            ),
            anchor(
                "temperature_sensor_thermowell_material_selection", 2,
                "재질 선정 기준",
                "재질은 공정 온도, 압력, 부식성, 침식성, 유체 조성, 유속, 기계적 강도와 기존 배관 재질을 고려하여 선정해야 하며 SS316, Hastelloy, Monel, Inconel 등은 조건과 연결해 제시해야 한다.",
                ["재질", "온도", "압력", "부식성", "침식성", "SS316", "Hastelloy"],
                ["Monel", "Inconel", "compatibility", "wetted part", "pipe material"],
            ),
            anchor(
                "temperature_sensor_thermowell_material_selection", 3,
                "형상과 삽입 길이",
                "Straight, tapered, stepped 등 형상과 삽입 길이는 강도, 응답성, 유동 방해, 설치 공간, 센서 tip 위치와 연결되며 길수록 항상 좋은 것은 아니라고 설명해야 한다.",
                ["형상", "삽입 길이", "straight", "tapered", "stepped", "응답성"],
                ["tip position", "immersion", "strength", "flow disturbance"],
            ),
            anchor(
                "temperature_sensor_thermowell_material_selection", 4,
                "wake frequency와 진동 파손",
                "유속이 큰 배관에서는 vortex shedding에 따른 wake frequency가 thermowell 고유진동수와 가까워지면 공진과 피로 파손이 발생할 수 있으므로 진동 검토와 공진 회피가 필요하다.",
                ["wake frequency", "vortex shedding", "고유진동수", "공진", "피로 파손"],
                ["ASME PTC 19.3 TW", "flow velocity", "fatigue", "stress"],
            ),
            anchor(
                "temperature_sensor_thermowell_material_selection", 5,
                "응답 지연과 유지보수",
                "Thermowell은 센서를 보호하지만 열용량과 전도 경로 때문에 응답 지연을 증가시킬 수 있으므로 제어 루프 응답, 교정, 청소, 교체성, 예비품 표준화를 함께 고려해야 한다.",
                ["응답 지연", "열용량", "제어 루프", "교정", "유지보수"],
                ["response time", "cleaning", "replacement", "spare", "standardization"],
            ),
        ],
    },
    {
        "topic_id": "level_measurement_sensor_selection",
        "priority": "high",
        "name": "레벨 측정 센서 선정",
        "aliases": ["level measurement", "레벨계", "초음파 레벨", "플로트 레벨", "GWR", "가이드웨이브 레이더", "레이저 레벨", "정전용량식 레벨"],
        "triggers": ["레벨 측정", "레벨계", "초음파 레벨", "플로트", "GWR", "가이드웨이브", "레이저 레벨", "정전용량식", "level sensor"],
        "anchors": [
            anchor(
                "level_measurement_sensor_selection", 1,
                "접촉식·비접촉식 분류",
                "초음파와 비접촉 레이더·레이저는 비접촉식, 플로트와 정전용량식 및 GWR probe 방식은 공정과 접촉하는 방식으로 분류하고 각 방식의 설치 조건을 구분해야 한다.",
                ["접촉식", "비접촉식", "초음파", "플로트", "GWR", "정전용량식"],
                ["radar", "laser", "probe", "installation", "tank"],
            ),
            anchor(
                "level_measurement_sensor_selection", 2,
                "초음파·레이저·비접촉 레이더 한계",
                "비접촉식 계기는 탱크 상부 설치와 유지보수 장점이 있으나 거품, 증기, 분진, 난반사, 온도층, 압력 조건, 표면 상태에 의해 오차가 발생할 수 있다.",
                ["거품", "증기", "분진", "난반사", "비접촉식"],
                ["ultrasonic", "laser", "radar", "surface", "temperature gradient"],
            ),
            anchor(
                "level_measurement_sensor_selection", 3,
                "GWR와 정전용량식 조건",
                "GWR은 probe를 따라 전자파가 진행하므로 유전율, 부착물, probe 형상, 설치 간섭을 고려해야 하며, 정전용량식은 유전율 변화, coating, interface 측정 조건에 민감하다고 설명해야 한다.",
                ["GWR", "probe", "유전율", "부착물", "정전용량식"],
                ["guided wave radar", "coating", "interface", "dielectric constant"],
            ),
            anchor(
                "level_measurement_sensor_selection", 4,
                "플로트와 접촉식 한계",
                "플로트식은 구조가 단순하고 직관적이지만 점도, 고착, 부식성, 밀도 변화, 기계적 마모, 난류에 영향을 받으므로 공정 유체 조건을 확인해야 한다.",
                ["플로트", "점도", "고착", "부식성", "밀도"],
                ["mechanical wear", "turbulence", "float", "maintenance"],
            ),
            anchor(
                "level_measurement_sensor_selection", 5,
                "선정 기준과 안전 조건",
                "레벨 센서 선정은 측정 범위, 정확도, 탱크 형상, 거품·증기·유전율·점도·부식성, 방폭, SIL/인터록, 유지보수 접근성, 비용과 기존 DCS/PLC 연계를 함께 판단해야 한다.",
                ["측정 범위", "정확도", "방폭", "유지보수", "DCS", "PLC"],
                ["SIL", "interlock", "cost", "compatibility", "process condition"],
            ),
        ],
    },
    {
        "topic_id": "continuous_discrete_control_model_comparison",
        "priority": "high",
        "name": "연속시간·이산시간·이산사건 제어 모델 비교",
        "aliases": ["continuous model", "discrete model", "이산시간 모델", "이산사건 모델", "z 변환", "차분방정식", "sampling"],
        "triggers": ["연속시간", "이산시간", "이산사건", "차분방정식", "z 변환", "sampling", "aliasing", "digital control"],
        "anchors": [
            anchor(
                "continuous_discrete_control_model_comparison", 1,
                "연속시간 모델",
                "연속시간 모델은 시간 변수가 연속이며 미분방정식, Laplace 변환, 전달함수, 상태방정식으로 공정 동특성을 표현한다고 설명해야 한다.",
                ["연속시간", "미분방정식", "Laplace", "전달함수", "상태방정식"],
                ["s-domain", "dynamic system", "continuous control"],
            ),
            anchor(
                "continuous_discrete_control_model_comparison", 2,
                "이산시간 모델",
                "이산시간 모델은 샘플링 주기마다 갱신되는 신호를 차분방정식, z 변환, pulse transfer function 등으로 표현하며 디지털 제어기 구현과 직접 연결된다.",
                ["이산시간", "샘플링 주기", "차분방정식", "z 변환", "디지털 제어"],
                ["sampled-data", "pulse transfer", "ZOH", "controller implementation"],
            ),
            anchor(
                "continuous_discrete_control_model_comparison", 3,
                "이산사건 모델",
                "이산사건 모델은 연속 신호값보다 상태, 이벤트, 조건, 논리 전이를 중심으로 설비 sequence, interlock, PLC logic, batch process를 표현한다고 구분해야 한다.",
                ["이산사건", "상태", "이벤트", "논리 전이", "PLC"],
                ["sequence", "interlock", "batch", "state machine", "Petri net"],
            ),
            anchor(
                "continuous_discrete_control_model_comparison", 4,
                "샘플링과 aliasing",
                "아날로그 신호를 이산화할 때 샘플링 주기와 Nyquist 조건, anti-aliasing filter를 고려하지 않으면 aliasing과 정보 손실이 발생한다고 설명해야 한다.",
                ["샘플링", "Nyquist", "aliasing", "anti-aliasing"],
                ["sampling frequency", "filter", "information loss", "discretization"],
            ),
            anchor(
                "continuous_discrete_control_model_comparison", 5,
                "디지털 제어 적용 한계",
                "디지털 제어에서는 ZOH, 계산 지연, 통신 지연, quantization, sampling jitter가 위상 지연과 안정도 여유에 영향을 주므로 연속 제어식을 단순히 코드로 옮기는 것으로 보아서는 안 된다.",
                ["ZOH", "계산 지연", "위상 지연", "안정도 여유", "quantization"],
                ["communication delay", "jitter", "phase margin", "implementation"],
            ),
        ],
    },
    {
        "topic_id": "second_order_system_resonance_frequency_response",
        "priority": "high",
        "name": "2차 시스템 주파수응답과 공진",
        "aliases": ["2차 시스템", "second order system", "frequency response", "resonance", "공진 주파수", "감쇠비", "zeta", "omega_n"],
        "triggers": ["2차 시스템", "주파수응답", "공진", "공진 주파수", "resonant peak", "감쇠비", "zeta", "omega"],
        "anchors": [
            anchor(
                "second_order_system_resonance_frequency_response", 1,
                "표준 2차 전달함수",
                "표준 2차계는 보통 G(s)=Kωn²/(s²+2ζωn s+ωn²)로 표현하며, ωn은 고유진동수, ζ는 감쇠비라고 설명해야 한다.",
                ["G(s)", "ωn", "ζ", "고유진동수", "감쇠비"],
                ["second order", "transfer function", "natural frequency", "damping ratio"],
            ),
            anchor(
                "second_order_system_resonance_frequency_response", 2,
                "주파수응답 크기식",
                "s=jω를 대입하면 2차계 주파수응답 크기는 주파수비 r=ω/ωn에 대해 분모 √((1-r²)²+(2ζr)²)의 형태로 해석된다고 설명해야 한다.",
                ["s=jω", "주파수응답", "r=ω/ωn", "크기식", "분모"],
                ["magnitude", "frequency ratio", "Bode", "amplitude ratio"],
            ),
            anchor(
                "second_order_system_resonance_frequency_response", 3,
                "공진 주파수와 조건",
                "표준 2차 저역통과계의 공진 주파수는 ωr=ωn√(1−2ζ²)이며, 실수 공진 주파수가 존재하려면 ζ<1/√2 조건을 만족해야 한다.",
                ["ωr", "ωn√(1−2ζ²)", "ζ<1/√2", "공진 주파수"],
                ["resonance", "resonant frequency", "low-pass", "condition"],
            ),
            anchor(
                "second_order_system_resonance_frequency_response", 4,
                "시간응답과 주파수응답 구분",
                "시간응답의 overshoot와 주파수응답의 resonance는 관련은 있지만 같은 개념이 아니며, ζ=1은 임계감쇠 조건이지 공진 조건이 아니라고 명확히 구분해야 한다.",
                ["overshoot", "resonance", "ζ=1", "임계감쇠", "공진 조건"],
                ["time response", "frequency response", "critical damping", "confusion"],
            ),
            anchor(
                "second_order_system_resonance_frequency_response", 5,
                "제어·계측 적용 판단",
                "공진은 진동 증폭, 노이즈 증폭, 제어루프 불안정, 센서·기계 구조물 손상 위험과 연결되므로 감쇠비, bandwidth, loop tuning, mechanical resonance 회피를 함께 고려해야 한다.",
                ["진동 증폭", "노이즈 증폭", "제어루프", "bandwidth", "loop tuning"],
                ["mechanical resonance", "stability", "sensor", "damping", "design"],
            ),
        ],
    },
]

FIELD_POINTS: dict[str, list[str]] = {
    "vibration_measurement_condition_monitoring": [
        "shaft vibration과 housing vibration 측정 위치를 구분한다.",
        "bearing fault 진단에는 고주파 가속도, envelope, FFT, trend 분석을 검토한다.",
        "보호용 trip setpoint와 진단용 monitoring alarm을 분리해 관리한다.",
        "센서 mounting, cable, grounding, gap, 온도 환경과 loop test를 확인한다.",
    ],
    "doppler_effect_velocity_flow_measurement": [
        "입사각과 반사체 농도에 따른 Doppler shift 신뢰성을 확인한다.",
        "깨끗한 단상 액체에는 Doppler 방식보다 transit-time 방식이 적합할 수 있다.",
        "배관 충만 상태, 직관거리, SNR, 유속 분포와 설치 방향을 검토한다.",
        "레이다 속도 측정, 초음파 유량 측정, 일반 유량계 적용 범위를 구분한다.",
    ],
    "adc_dac_signal_conversion_interface": [
        "sampling period와 anti-aliasing filter를 함께 검토한다.",
        "resolution, accuracy, offset, gain, INL/DNL, jitter를 구분한다.",
        "reference voltage 안정도, isolation, grounding, shield, common-mode noise를 확인한다.",
        "PLC/DCS/DAQ 입력 범위와 기존 loop compatibility를 검토한다.",
    ],
    "temperature_sensor_thermowell_material_selection": [
        "공정 유체의 온도, 압력, 부식성, 침식성에 맞춰 wetted material을 선정한다.",
        "삽입 길이, 형상, wake frequency, vortex shedding, 피로 파손 위험을 검토한다.",
        "응답 지연이 온도 제어루프와 alarm 동작에 미치는 영향을 확인한다.",
        "운전 중 센서 교체성, 예비품 표준화, 청소·교정 접근성을 고려한다.",
    ],
    "level_measurement_sensor_selection": [
        "초음파, 비접촉 레이더, 레이저, 플로트, GWR, 정전용량식의 접촉 여부를 구분한다.",
        "거품, 증기, 분진, 유전율, 점도, 부식성, 부착물 조건을 확인한다.",
        "GWR probe 형상, tank 내부 간섭, interface 측정 가능성을 검토한다.",
        "방폭, SIL/interlock, 유지보수 접근성, 기존 DCS/PLC 연계를 고려한다.",
    ],
    "continuous_discrete_control_model_comparison": [
        "연속시간 모델은 미분방정식/Laplace, 이산시간 모델은 차분방정식/z 변환으로 구분한다.",
        "이산사건 모델은 sequence, interlock, PLC logic, batch process와 연결한다.",
        "sampling period, ZOH, aliasing, anti-aliasing filter, phase delay를 검토한다.",
        "계산 지연, 통신 지연, quantization, jitter가 안정도 여유에 미치는 영향을 확인한다.",
    ],
    "second_order_system_resonance_frequency_response": [
        "고유진동수 ωn, 감쇠비 ζ, 공진 주파수 ωr, resonant peak를 구분한다.",
        "ζ<1/√2에서 공진 peak가 존재한다는 조건을 확인한다.",
        "시간응답 overshoot와 주파수응답 resonance를 혼동하지 않는다.",
        "기계 공진, 센서 노이즈 증폭, 제어 loop tuning, bandwidth 설계와 연결한다.",
    ],
    "induction_motor_dq_reference_frame_equivalent_circuit": [
        "벡터제어", "d축 자속 제어", "q축 토크 전류 제어", "좌표계 부호",
        "속도기전력 보상", "전류제어기 설계", "인버터 구동", "센서리스 제어",
    ],
}

MODEL_PATCHES: dict[str, dict[str, Any]] = {
    "vibration_measurement_condition_monitoring": {
        "low_score_patterns": [
            "변위, 속도, 가속도 센서를 모두 같은 진동 센서로만 설명하면 안 된다.",
            "센서별 주파수 대역과 측정 위치를 구분하지 않으면 안 된다.",
            "shaft vibration, housing vibration, bearing fault 적용 차이를 빠뜨리면 안 된다.",
            "보호용 trip과 진단용 monitoring의 목적 차이를 빠뜨리면 안 된다.",
        ],
        "expected_structure": [
            "배경", "진동감시설비 구성", "변위 센서", "속도 센서", "가속도 센서", "보호용 trip과 진단용 monitoring 구분", "선정 및 유지보수 고려사항",
        ],
    },
    "doppler_effect_velocity_flow_measurement": {
        "expected_structure": ["배경", "도플러 효과 원리", "접근·이격 시 주파수 변화", "초음파 도플러 유량계", "적용 분야와 한계"],
    },
    "adc_dac_signal_conversion_interface": {
        "expected_structure": ["배경", "ADC 변환 과정", "DAC 변환 과정", "해상도와 정확도", "오차 요인", "계측 인터페이스 적용 고려사항"],
    },
    "temperature_sensor_thermowell_material_selection": {
        "expected_structure": ["배경", "thermowell 목적", "재질 선정", "형상과 삽입 길이", "wake frequency와 파손 위험", "응답 지연과 유지보수"],
    },
    "level_measurement_sensor_selection": {
        "expected_structure": ["배경", "접촉식·비접촉식 분류", "초음파·레이더·레이저", "플로트·GWR·정전용량식", "공정 조건별 선정", "방폭·유지보수·비용"],
    },
    "continuous_discrete_control_model_comparison": {
        "expected_structure": ["배경", "연속시간 모델", "이산시간 모델", "이산사건 모델", "샘플링·z 변환·aliasing", "디지털 제어 적용 기준"],
    },
    "second_order_system_resonance_frequency_response": {
        "expected_structure": ["배경", "표준 2차 전달함수", "주파수응답 크기식", "공진 주파수와 조건", "시간응답과 주파수응답 구분", "현장 적용"],
        "low_score_patterns": [
            "ζ=1 임계감쇠를 공진 조건처럼 설명하면 안 된다.",
            "시간응답 overshoot와 주파수응답 resonance를 같은 개념으로 쓰면 안 된다.",
            "ωr=ωn√(1−2ζ²)의 존재 조건 ζ<1/√2를 빠뜨리면 안 된다.",
            "수식만 쓰고 감쇠비, bandwidth, 제어루프 영향 등 해석을 빠뜨리면 안 된다.",
        ],
    },
    "local_instrument_cabinet_installation": {
        "question_type": "IMPLEMENTATION_EVALUATION",
    },
    "control_valve_positioner_ip_converter": {
        "expected_structure": [
            "배경과 최종제어요소 역할",
            "I/P converter의 4-20 mA to 3-15 psi 변환",
            "포지셔너 구성: diaphragm/capsule, pilot valve, actuator",
            "feedback spring/linkage에 의한 위치 피드백",
            "힘 평형과 목표 위치 정지",
            "마찰·히스테리시스·air supply·fail action 등 현장 문제",
        ],
    },
}

TOPIC_ALIASES_ADD: dict[str, list[str]] = {
    "level_measurement_sensor_selection": ["GWR", "가이드웨이브 레이더", "guided wave radar", "probe radar"],
    "temperature_sensor_thermowell_material_selection": ["wake frequency", "vortex shedding", "ASME PTC 19.3 TW"],
    "second_order_system_resonance_frequency_response": ["ωr", "ωn", "ζ", "resonant peak", "공진 peak"],
}


def unique_extend(values: list[Any], additions: list[Any]) -> list[Any]:
    out = list(values) if isinstance(values, list) else []
    for item in additions:
        if item not in out:
            out.append(item)
    return out


def load_model_bank() -> dict[str, Any]:
    if load_model_answer_bank is not None:
        return load_model_answer_bank(MODEL_ANSWER_BANK)
    return read_json(MODEL_ANSWER_BANK)


def save_model_bank(bank: dict[str, Any]) -> None:
    if save_model_answer_bank is not None:
        save_model_answer_bank(bank, MODEL_ANSWER_BANK)
    else:
        write_json(MODEL_ANSWER_BANK, bank)


def clean_model_answers() -> tuple[int, list[str]]:
    bank = load_model_bank()
    answers = bank.get("answers", [])
    if not isinstance(answers, list):
        raise SystemExit("model answer bank has no answers list")

    changed = 0
    notes: list[str] = []
    generic_phrases = [
        "현장 적용 시 정격, 손실, 발열, 파형, 보호회로를 함께 검토한다.",
        "측정 시 전압 파형과 전류 파형을 함께 확인한다.",
        "설계 변경 시 효율, 신뢰성, 비용, 유지보수성을 함께 판단한다.",
    ]

    for item in answers:
        if not isinstance(item, dict):
            continue
        tid = item.get("topic_id")
        before = json.dumps(item, ensure_ascii=False, sort_keys=True)

        if tid in MODEL_PATCHES:
            for key, value in MODEL_PATCHES[tid].items():
                item[key] = value

        if tid in FIELD_POINTS:
            item["field_connection_points"] = FIELD_POINTS[tid]
        elif isinstance(item.get("field_connection_points"), list):
            # Keep non-target topics as-is, except remove the clearly unrelated generic set
            # only when all field points are exactly the generic import defaults.
            fps = item["field_connection_points"]
            if fps == generic_phrases:
                # Do not invent replacement for unrelated topics. Leave them for a later topic-specific pass.
                pass

        if tid in TOPIC_ALIASES_ADD:
            item["topic_aliases"] = unique_extend(item.get("topic_aliases", []), TOPIC_ALIASES_ADD[tid])

        if tid == "flowmeter_dp_orifice":
            for key in ("topic_aliases", "question_examples", "expected_structure", "model_answer_outline", "high_score_features", "low_score_patterns", "field_connection_points"):
                if isinstance(item.get(key), list):
                    item[key] = [x for x in item[key] if not (isinstance(x, str) and ("초음파" in x or "도플러" in x or "Doppler" in x))]

        # Soft text cleanup for known risky fixed legal number expression.
        if tid == "local_instrument_cabinet_installation":
            for key in ("model_answer_outline", "high_score_features", "field_connection_points"):
                if isinstance(item.get(key), list):
                    item[key] = [
                        s.replace("70cm 작업공간", "관계 법령과 전기설비 기준에 따른 조작·점검 작업공간") if isinstance(s, str) else s
                        for s in item[key]
                    ]

        # Normalize common formula notation in second-order topic without disturbing JSON schema.
        if tid == "second_order_system_resonance_frequency_response":
            for key in ("model_answer_outline", "high_score_features", "low_score_patterns"):
                if isinstance(item.get(key), list):
                    repl = []
                    for s in item[key]:
                        if not isinstance(s, str):
                            repl.append(s)
                            continue
                        s = s.replace("wr = wnsqrt(1 - 2zeta^2)", "ωr = ωn√(1−2ζ²)")
                        s = s.replace("zeta < 1/sqrt(2)", "ζ < 1/√2")
                        s = s.replace("wn", "ωn")
                        s = s.replace("zeta", "ζ")
                        s = s.replace("jw", "jω")
                        repl.append(s)
                    item[key] = repl

        # Remove markdown section remnants accidentally captured by parser.
        for key in ("low_score_patterns", "model_answer_outline", "high_score_features", "field_connection_points"):
            if isinstance(item.get(key), list):
                item[key] = [
                    s for s in item[key]
                    if not (isinstance(s, str) and (s.strip().startswith("## ") or s.strip().startswith("### ")))
                ]

        item["revision_notes"] = unique_extend(item.get("revision_notes", []), [REVISION_NOTE])

        after = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if before != after:
            changed += 1
            notes.append(str(tid))

    # Validate before writing.
    if validate_model_answer_bank is not None and question_type_ids is not None:
        errors = validate_model_answer_bank(bank, allowed_types=question_type_ids())
        if errors:
            print("INVALID model answer bank after cleanup", file=sys.stderr)
            for e in errors:
                print("-", e, file=sys.stderr)
            raise SystemExit(1)

    save_model_bank(bank)
    return changed, notes


def upsert_fact_topics() -> tuple[int, list[str]]:
    bank = load_fact_anchor_bank(FACT_ANCHOR_BANK)
    changed: list[str] = []

    for topic in FACT_TOPICS:
        before = json.dumps(bank, ensure_ascii=False, sort_keys=True)
        upsert_fact_anchor_topic(bank, topic)
        after = json.dumps(bank, ensure_ascii=False, sort_keys=True)
        if before != after:
            changed.append(topic["topic_id"])

    # Also remove clear ultrasonic/Doppler misrouting from DP/orifice fact anchor triggers/aliases.
    for t in bank.get("topics", []):
        if not isinstance(t, dict):
            continue
        if t.get("topic_id") == "flowmeter_dp_orifice":
            for key in ("triggers", "aliases"):
                if isinstance(t.get(key), list):
                    old = list(t[key])
                    t[key] = [
                        x for x in t[key]
                        if not (isinstance(x, str) and ("초음파" in x or "도플러" in x or "Doppler" in x))
                    ]
                    if old != t[key] and "flowmeter_dp_orifice" not in changed:
                        changed.append("flowmeter_dp_orifice")

    errors = validate_fact_anchor_bank_data(bank)
    if errors:
        print("INVALID fact anchor bank after update", file=sys.stderr)
        for e in errors:
            print("-", e, file=sys.stderr)
        raise SystemExit(1)

    save_fact_anchor_bank(bank, FACT_ANCHOR_BANK)
    return len(changed), changed


def main() -> int:
    print("root:", ROOT)
    print("model bank:", MODEL_ANSWER_BANK)
    print("fact bank:", FACT_ANCHOR_BANK)

    print("backup model:", backup_file(MODEL_ANSWER_BANK))
    print("backup fact:", backup_file(FACT_ANCHOR_BANK))

    fact_count, fact_changed = upsert_fact_topics()
    model_count, model_changed = clean_model_answers()

    print("fact topics changed:", fact_count)
    for tid in fact_changed:
        print(" -", tid)

    print("model answers changed:", model_count)
    for tid in model_changed:
        print(" -", tid)

    print("\nRunning validate-all...")
    result = subprocess.run([sys.executable, "scripts/rubric_manager.py", "validate-all"], cwd=ROOT)
    if result.returncode != 0:
        print("validate-all failed", file=sys.stderr)
        return result.returncode

    print("\nCheck topic_id coverage:")
    for topic in FACT_TOPICS:
        tid = topic["topic_id"]
        print(f" - {tid}: fact_anchor upserted")

    print("\nDone. Review with:")
    print("  git diff -- rubrics/model_answers/industrial_instrumentation_control.json")
    print("  git diff -- rubrics/fact_anchors/industrial_instrumentation_control.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
