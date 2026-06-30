#!/usr/bin/env python3
"""
Apply rubric review fixes for industrial_instrumentation_control.

Run from the repository root:

  python3 scripts/apply_rubric_review_fixes.py
  python3 scripts/rubric_manager.py validate-all

This script intentionally uses the repository's rubric update functions:
- rubric_registry.upsert_model_answer
- rubric_content.fact_anchors.upsert_fact_anchor_topic
- save_model_answer_bank / save_fact_anchor_bank
- validate_model_answer_bank / validate_fact_anchor_bank_data
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from rubric_registry import (  # noqa: E402
    load_model_answer_bank,
    question_type_ids,
    save_model_answer_bank,
    upsert_model_answer,
    validate_model_answer_bank,
)
from rubric_content.common import (  # noqa: E402
    FACT_ANCHOR_BANK,
    MODEL_ANSWER_BANK,
    backup_file,
)
from rubric_content.fact_anchors import (  # noqa: E402
    load_fact_anchor_bank,
    save_fact_anchor_bank,
    upsert_fact_anchor_topic,
    validate_fact_anchor_bank_data,
)


def stamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


def model_answer(
    topic_id: str,
    question_type: str,
    title: str,
    question_examples: list[str],
    topic_aliases: list[str],
    expected_structure: list[str],
    model_answer_outline: list[str],
    high_score_features: list[str],
    low_score_patterns: list[str],
    field_connection_points: list[str],
) -> dict[str, Any]:
    return {
        "id": f"{topic_id}_{question_type}_v1",
        "topic_id": topic_id,
        "question_type": question_type,
        "title": title,
        "question_examples": question_examples,
        "topic_aliases": topic_aliases,
        "expected_structure": expected_structure,
        "model_answer_outline": model_answer_outline,
        "high_score_features": high_score_features,
        "low_score_patterns": low_score_patterns,
        "field_connection_points": field_connection_points,
        "revision_notes": [
            f"created_at={stamp()}",
            "review_fix: model_answers와 fact_anchors 동기화 보강",
        ],
    }


def anchor(
    topic_id: str,
    idx: int,
    name: str,
    expected: str,
    core_terms: list[str],
    support_terms: list[str],
) -> dict[str, Any]:
    return {
        "id": f"{topic_id}_anchor_{idx}",
        "name": name,
        "expected": expected,
        "core_terms": core_terms,
        "support_terms": support_terms,
    }


def fact_topic(
    topic_id: str,
    name: str,
    aliases: list[str],
    triggers: list[str],
    anchors: list[dict[str, Any]],
    priority: str = "high",
) -> dict[str, Any]:
    return {
        "topic_id": topic_id,
        "priority": priority,
        "name": name,
        "aliases": aliases,
        "triggers": triggers,
        "anchors": anchors,
    }


MODEL_ANSWERS: list[dict[str, Any]] = [
    model_answer(
        topic_id="vibration_measurement_condition_monitoring",
        question_type="COMPARE_SELECTION",
        title="진동 측정과 상태감시 센서 선정형 모범 답안",
        question_examples=[
            "진동 측정에서 변위, 속도, 가속도 센서의 적용 기준을 설명하시오.",
            "회전체 상태감시에서 shaft vibration, housing vibration, bearing fault 진단 방법을 비교하시오.",
            "진동 보호용 trip과 진단용 monitoring의 차이를 설명하시오.",
        ],
        topic_aliases=[
            "진동측정",
            "상태감시",
            "condition monitoring",
            "변위센서",
            "속도센서",
            "가속도센서",
            "shaft vibration",
            "bearing fault",
        ],
        expected_structure=[
            "진동 측정 목적과 보호·진단 목적 구분",
            "변위·속도·가속도 센서의 측정 대상과 주파수 대역 비교",
            "shaft vibration, housing vibration, bearing fault 적용 구분",
            "보호용 trip과 진단용 monitoring의 기능 차이",
            "설치 위치, 신호처리, alarm/trip 설정, 유지보수 고려사항",
        ],
        model_answer_outline=[
            "진동 측정은 회전체의 이상을 조기에 파악하고 설비 보호, 상태진단, 예방보전 기준을 확보하기 위한 계측이다.",
            "변위 센서는 축의 상대변위와 저주파·대진폭 진동, 속도 센서는 베어링 하우징의 중간 주파수 진동, 가속도 센서는 고주파 충격과 베어링 결함 진단에 주로 사용된다.",
            "shaft vibration은 비접촉 변위 probe로 축 중심 이동, unbalance, oil whirl 등을 감시하는 경우가 많고, housing vibration은 velocity pickup 또는 accelerometer로 구조물 전달 진동을 본다.",
            "bearing fault는 내륜·외륜·볼 결함에 의한 고주파 충격 성분이 중요하므로 accelerometer, FFT, envelope analysis, trend monitoring을 함께 적용한다.",
            "보호용 trip은 과진동 시 설비 손상을 막기 위한 신뢰성 높은 한계 동작이고, 진단용 monitoring은 spectrum, trend, phase, envelope 등으로 원인을 해석하는 기능이다.",
            "현장에서는 센서 설치 강성, 케이블 노이즈, 접지, alarm/trip setpoint, false trip 방지, 기존 보호계전·DCS 연계, 유지보수 접근성을 함께 고려해야 한다.",
        ],
        high_score_features=[
            "변위·속도·가속도 센서의 측정 대상과 주파수 대역을 구분한다.",
            "shaft vibration과 housing vibration의 계측 위치와 의미를 분리한다.",
            "bearing fault 진단에서 고주파 충격, FFT, envelope, trend를 언급한다.",
            "보호용 trip과 진단용 monitoring의 목적과 신뢰성 요구 차이를 설명한다.",
            "설치, 노이즈, setpoint, false trip, 유지보수까지 현장 적용으로 연결한다.",
        ],
        low_score_patterns=[
            "진동센서를 모두 같은 용도로 설명한다.",
            "가속도 센서가 항상 모든 진동 측정에 가장 좋다고 단정한다.",
            "변위, 속도, 가속도를 단순 미분·적분 관계로만 설명하고 실제 적용 위치를 구분하지 않는다.",
            "trip과 monitoring을 구분하지 않는다.",
        ],
        field_connection_points=[
            "proximity probe",
            "velocity pickup",
            "accelerometer",
            "FFT",
            "envelope analysis",
            "alarm setpoint",
            "trip setpoint",
            "false trip",
            "predictive maintenance",
        ],
    ),
    model_answer(
        topic_id="doppler_effect_velocity_flow_measurement",
        question_type="PRINCIPLE_INTERPRETATION",
        title="도플러 효과와 속도·유량 측정 원리 모범 답안",
        question_examples=[
            "도플러 효과와 이를 이용한 속도 측정 원리를 설명하시오.",
            "도플러 초음파 유량계의 원리와 적용 조건을 설명하시오.",
            "도플러 방식과 transit-time 초음파 유량계를 비교하시오.",
        ],
        topic_aliases=[
            "도플러",
            "Doppler",
            "도플러 유량계",
            "초음파 도플러",
            "Doppler flowmeter",
            "radar speed measurement",
        ],
        expected_structure=[
            "도플러 효과 정의",
            "접근·이격에 따른 주파수 변화",
            "반사파를 이용한 속도 산출 원리",
            "도플러 초음파 유량계의 적용 조건",
            "레이다·초음파·유량 측정 적용 구분과 한계",
        ],
        model_answer_outline=[
            "도플러 효과는 파원과 관측자 또는 반사체 사이의 상대속도 때문에 수신 주파수가 송신 주파수와 달라지는 현상이다.",
            "반사체가 송신기 또는 수신기에 접근하면 수신 주파수는 증가하고, 멀어지면 수신 주파수는 감소한다.",
            "도플러 속도 측정은 송신파와 반사파의 주파수 차이를 측정하여 반사체의 속도 성분을 계산하는 방식이다.",
            "도플러 초음파 유량계는 유체 내 입자, 기포, 슬러리 등 초음파를 산란·반사할 수 있는 반사체가 있어야 안정적으로 동작한다.",
            "깨끗한 액체에는 일반적으로 transit-time 방식이 더 적합하고, 도플러 방식은 오염수, 슬러리, 기포가 포함된 유체에 유리하다.",
            "레이다 속도계는 전자파 반사를 이용하고 초음파 유량계는 음파 전파를 이용하므로 매질, 반사 조건, 설치각, 유동 상태, 배관 충만 여부를 함께 검토해야 한다.",
        ],
        high_score_features=[
            "접근 시 주파수 증가, 이격 시 주파수 감소를 정확히 설명한다.",
            "송신파와 반사파의 주파수 차이를 속도와 연결한다.",
            "도플러 초음파 유량계의 반사체 조건을 명확히 제시한다.",
            "Doppler 방식과 transit-time 방식을 구분한다.",
            "레이다, 초음파, 유량 측정의 적용 조건과 한계를 구분한다.",
        ],
        low_score_patterns=[
            "접근과 이격의 주파수 변화를 반대로 설명한다.",
            "초음파 유량계를 모두 도플러 방식으로 설명한다.",
            "깨끗한 물에서도 도플러 방식이 항상 적합하다고 단정한다.",
            "반사체 조건, 설치각, 배관 충만 조건을 고려하지 않는다.",
        ],
        field_connection_points=[
            "송신 주파수",
            "수신 주파수",
            "주파수 편이",
            "반사체",
            "입자",
            "기포",
            "slurry",
            "transit-time",
            "radar",
            "초음파 센서 설치각",
        ],
    ),
    model_answer(
        topic_id="adc_dac_signal_conversion_interface",
        question_type="PRINCIPLE_INTERPRETATION",
        title="ADC/DAC 신호 변환 인터페이스 원리 모범 답안",
        question_examples=[
            "ADC와 DAC의 동작 원리와 오차 요인을 설명하시오.",
            "아날로그 계측 신호의 디지털 변환 과정과 주의사항을 설명하시오.",
        ],
        topic_aliases=[
            "ADC",
            "DAC",
            "A/D 변환",
            "D/A 변환",
            "표본화",
            "양자화",
            "부호화",
            "sampling",
            "quantization",
        ],
        expected_structure=[
            "계측 인터페이스에서 ADC/DAC의 역할",
            "ADC의 표본화·양자화·부호화 과정",
            "DAC의 디코딩·가중합성·필터링 과정",
            "해상도와 정확도의 차이",
            "주요 오차 요인과 현장 적용 고려사항",
        ],
        model_answer_outline=[
            "ADC는 센서 또는 transmitter의 아날로그 전압·전류 신호를 디지털 제어기나 DAQ가 처리할 수 있는 코드로 변환하는 장치이다.",
            "ADC 과정은 시간축에서 신호를 일정 주기로 취하는 표본화, 진폭축을 유한 단계로 나누는 양자화, 양자화된 값을 binary code로 표현하는 부호화로 설명할 수 있다.",
            "DAC는 디지털 코드를 디코딩하여 저항 ladder, current source, PWM 등으로 가중 합성하고, 필요 시 reconstruction filter로 아날로그 출력 리플을 줄인다.",
            "bit 수가 증가하면 LSB 크기가 작아져 해상도는 좋아지지만, 기준전압, noise, offset error, gain error, INL/DNL, jitter가 나쁘면 전체 정확도는 보장되지 않는다.",
            "샘플링 주기는 신호 대역폭보다 충분히 빨라야 하며 aliasing을 막기 위해 anti-aliasing filter와 적절한 grounding, shielding, isolation을 검토해야 한다.",
            "현장에서는 4~20mA, 1~5V, thermocouple/RTD 입력, 절연 모듈, 기준전압 안정도, PLC scan time, 제어 주기와의 정합성을 함께 검토한다.",
        ],
        high_score_features=[
            "ADC의 표본화, 양자화, 부호화를 순서대로 설명한다.",
            "DAC의 디코딩, 가중 합성, 필터링을 구분한다.",
            "해상도와 정확도가 다르다는 점을 명확히 설명한다.",
            "양자화 오차, offset, gain, INL/DNL, sampling jitter를 언급한다.",
            "anti-aliasing, 기준전압, 노이즈, 접지, 절연, scan time을 현장 조건과 연결한다.",
        ],
        low_score_patterns=[
            "ADC는 아날로그를 디지털로 바꾼다고만 설명한다.",
            "bit 수가 높으면 항상 정확하다고 설명한다.",
            "sampling과 quantization을 구분하지 않는다.",
            "aliasing, jitter, 기준전압, 노이즈 등 실제 오차 요인을 누락한다.",
        ],
        field_connection_points=[
            "4~20mA",
            "1~5V",
            "LSB",
            "anti-aliasing filter",
            "reference voltage",
            "offset error",
            "gain error",
            "INL",
            "DNL",
            "sampling jitter",
            "PLC scan time",
        ],
    ),
    model_answer(
        topic_id="temperature_sensor_thermowell_material_selection",
        question_type="COMPARE_SELECTION",
        title="온도센서 Thermowell 재질·형상 선정형 모범 답안",
        question_examples=[
            "Thermowell의 목적과 재질 선정 기준을 설명하시오.",
            "온도센서 보호관 선정 시 고려사항을 설명하시오.",
        ],
        topic_aliases=[
            "thermowell",
            "써모웰",
            "온도센서 보호관",
            "보호관",
            "wake frequency",
            "삽입길이",
        ],
        expected_structure=[
            "thermowell의 목적",
            "재질 선정 기준",
            "형상과 삽입 길이 선정",
            "진동·파손 위험과 wake frequency 검토",
            "응답 지연, 유지보수, 비용 고려",
        ],
        model_answer_outline=[
            "Thermowell은 온도센서를 공정 유체의 압력, 부식, 침식, 유속, 기계적 충격으로부터 보호하고 운전 중 센서 교체성을 확보하는 압력 경계 부품이다.",
            "재질은 온도, 압력, 유체 부식성, 침식성, 오염 가능성, 위생 요구, 기존 배관 재질과의 galvanic corrosion 가능성을 고려하여 선정한다.",
            "일반 수계·약부식 환경에는 SS304/316 계열이 쓰일 수 있으나, 고온·고압·염소·산·알칼리·해수 등에서는 Hastelloy, Inconel, Monel, Titanium 등 공정 조건에 맞는 재질 검토가 필요하다.",
            "형상은 직선형, 테이퍼형, 스텝형 등이 있으며 강도, 응답성, 압력손실, 유속 조건을 함께 고려해야 한다.",
            "삽입 길이는 대표 온도를 얻을 만큼 충분해야 하지만 너무 길면 응답 지연과 vortex shedding에 의한 진동·피로 파손 위험이 증가한다.",
            "현장에서는 wake frequency 계산, nozzle 위치, 유속, 보호관 강도, sensor 교체성, spare 표준화, 비용과 납기까지 함께 검토한다.",
        ],
        high_score_features=[
            "thermowell의 보호, 압력 경계, 운전 중 교체 목적을 설명한다.",
            "재질을 온도, 압력, 부식, 침식, 유체 조건과 연결한다.",
            "형상과 삽입 길이를 응답성, 강도, 대표성으로 비교한다.",
            "wake frequency, vortex shedding, 피로 파손 위험을 언급한다.",
            "응답 지연, 유지보수, 표준화, 비용을 실무 판단으로 연결한다.",
        ],
        low_score_patterns=[
            "thermowell을 단순한 센서 커버로만 설명한다.",
            "SS316이면 대부분 충분하다고 단정한다.",
            "삽입 길이는 길수록 좋다고 설명한다.",
            "진동, wake frequency, 응답 지연, 유지보수성을 누락한다.",
        ],
        field_connection_points=[
            "공정 유체",
            "부식",
            "침식",
            "SS316",
            "Hastelloy",
            "Inconel",
            "삽입 길이",
            "tapered thermowell",
            "wake frequency",
            "vortex shedding",
            "응답 지연",
            "센서 교체",
        ],
    ),
    model_answer(
        topic_id="level_measurement_sensor_selection",
        question_type="COMPARE_SELECTION",
        title="레벨 측정 센서 비교·선정형 모범 답안",
        question_examples=[
            "레벨 측정 센서의 종류와 선정 기준을 설명하시오.",
            "초음파, 플로트, GWR, 레이저, 정전용량식 레벨계의 특징을 비교하시오.",
        ],
        topic_aliases=[
            "레벨 측정",
            "level measurement",
            "초음파 레벨계",
            "플로트 레벨계",
            "가이드웨이브 레이더",
            "GWR",
            "레이저 레벨계",
            "정전용량식 레벨계",
        ],
        expected_structure=[
            "레벨 측정 목적과 선정 기준",
            "접촉식·비접촉식 분류",
            "초음파, 플로트, GWR, 레이저, 정전용량식 비교",
            "거품, 증기, 유전율, 점도, 부식성, 방폭 조건 영향",
            "유지보수, 비용, 기존 설비 연계 판단",
        ],
        model_answer_outline=[
            "레벨 측정은 탱크 재고, overflow 방지, pump 보호, 공정 안정화를 위해 액체 또는 고체의 높이를 계측하는 것이다.",
            "초음파와 레이저 레벨계는 비접촉식으로 설치·유지보수가 유리하나, 거품, 증기, 분진, 표면 난반사, 탱크 내부 구조물의 영향을 받을 수 있다.",
            "플로트 방식은 접촉식으로 원리가 단순하고 비용이 낮지만 점도, 고착, 부식, 슬러지, 기계적 마모에 취약하다.",
            "가이드웨이브 레이더는 probe를 따라 전자파가 진행하는 접촉식 계열로 볼 수 있으며 증기 영향은 비교적 작지만 유전율, probe 부착물, 설치 공간, 계면 조건을 검토해야 한다.",
            "정전용량식은 probe와 탱크 사이 정전용량 변화를 이용하므로 유전율, coating, 부착물, interface, 접지 조건의 영향이 크다.",
            "선정 시 측정 대상, 접촉 허용 여부, 압력·온도, 거품·증기·분진, 점도, 부식성, 방폭, 세정성, calibration, 기존 nozzle과 wiring, 비용을 종합 판단한다.",
        ],
        high_score_features=[
            "접촉식과 비접촉식 분류를 정확히 제시한다.",
            "각 센서의 원리와 취약 조건을 공정 조건과 연결한다.",
            "GWR을 일반 비접촉식 radar와 구분한다.",
            "거품, 증기, 유전율, 점도, 부식성, 방폭 조건을 선정 기준으로 사용한다.",
            "유지보수, 기존 nozzle, wiring, 비용까지 판단한다.",
        ],
        low_score_patterns=[
            "초음파가 모든 탱크에 범용 적용 가능하다고 설명한다.",
            "GWR을 비접촉식이라고 단정한다.",
            "정전용량식에서 유전율 영향을 누락한다.",
            "거품, 증기, 점도, 부식성, 방폭 조건을 고려하지 않는다.",
        ],
        field_connection_points=[
            "non-contact",
            "contact",
            "ultrasonic",
            "float",
            "guided wave radar",
            "laser",
            "capacitance",
            "foam",
            "vapor",
            "dielectric constant",
            "viscosity",
            "corrosion",
            "explosion proof",
        ],
    ),
    model_answer(
        topic_id="continuous_discrete_control_model_comparison",
        question_type="COMPARE_SELECTION",
        title="연속시간·이산시간·이산사건 제어모델 비교형 모범 답안",
        question_examples=[
            "연속시간 모델과 이산시간 모델, 이산사건 모델을 비교하시오.",
            "디지털 제어에서 이산시간 모델 적용 시 고려사항을 설명하시오.",
        ],
        topic_aliases=[
            "연속시간 모델",
            "이산시간 모델",
            "이산사건 모델",
            "z 변환",
            "차분방정식",
            "sampling period",
            "aliasing",
        ],
        expected_structure=[
            "모델 구분 목적",
            "연속시간 모델의 표현과 적용",
            "이산시간 모델의 표현과 적용",
            "이산사건 모델의 표현과 적용",
            "디지털 제어 적용 시 sampling, aliasing, 지연 고려",
        ],
        model_answer_outline=[
            "제어모델은 대상 시스템의 시간 특성과 사건 발생 방식을 어떻게 표현하는지에 따라 연속시간, 이산시간, 이산사건 모델로 구분할 수 있다.",
            "연속시간 모델은 시간 변수가 연속이고 미분방정식, 전달함수, Laplace 변환으로 표현되며 아날로그 공정, 물리계 동특성, 주파수응답 해석에 적합하다.",
            "이산시간 모델은 일정 sampling period마다 상태와 출력이 갱신되며 차분방정식, pulse transfer function, z 변환으로 표현되어 디지털 제어기와 DAQ 구현에 적합하다.",
            "이산사건 모델은 연속량보다 상태 전이와 이벤트 발생 순서가 중요하며 PLC sequence, interlock, batch process, discrete manufacturing 제어에 적합하다.",
            "디지털 제어에서는 sampling period, zero-order hold, computation delay, quantization, phase lag, aliasing, anti-aliasing filter가 제어 안정성과 응답성에 영향을 준다.",
            "따라서 연속시간 설계식을 그대로 코드화하는 것이 아니라 대상 bandwidth, scan time, actuator 응답, 통신 지연, 안전 logic과의 연계를 고려하여 모델을 선택해야 한다.",
        ],
        high_score_features=[
            "연속시간, 이산시간, 이산사건 모델의 수학적 표현을 구분한다.",
            "미분방정식/Laplace, 차분방정식/z 변환, 상태전이/이벤트를 정확히 연결한다.",
            "디지털 제어에서 sampling period와 zero-order hold 영향을 설명한다.",
            "aliasing, anti-aliasing, phase lag, computation delay를 언급한다.",
            "PLC sequence와 연속 제어 loop의 적용 차이를 구분한다.",
        ],
        low_score_patterns=[
            "연속 모델과 이산 모델을 단순히 아날로그/디지털 정도로만 설명한다.",
            "이산시간 모델과 이산사건 모델을 혼동한다.",
            "z 변환, sampling period, aliasing, phase lag를 누락한다.",
            "연속 제어식을 그대로 디지털 제어에 적용해도 된다고 설명한다.",
        ],
        field_connection_points=[
            "Laplace transform",
            "z transform",
            "difference equation",
            "sampling period",
            "zero-order hold",
            "aliasing",
            "anti-aliasing filter",
            "phase lag",
            "PLC sequence",
            "interlock",
            "scan time",
        ],
    ),
    model_answer(
        topic_id="second_order_system_resonance_frequency_response",
        question_type="PRINCIPLE_INTERPRETATION",
        title="2차 시스템 주파수응답과 공진주파수 해석형 모범 답안",
        question_examples=[
            "표준 2차 시스템의 주파수응답과 공진주파수를 설명하시오.",
            "2차계에서 감쇠비와 공진주파수의 관계를 설명하시오.",
            "시간응답 overshoot와 주파수응답 resonance의 차이를 설명하시오.",
        ],
        topic_aliases=[
            "2차 시스템",
            "second order system",
            "공진주파수",
            "resonance frequency",
            "frequency response",
            "감쇠비",
            "zeta",
            "omega r",
        ],
        expected_structure=[
            "표준 2차 전달함수",
            "주파수응답 크기식",
            "공진 발생 조건과 공진주파수",
            "감쇠비가 공진 peak에 미치는 영향",
            "시간응답 overshoot와 주파수응답 resonance 구분",
        ],
        model_answer_outline=[
            "표준 2차 시스템은 보통 G(s)=Kωn²/(s²+2ζωns+ωn²) 형태로 나타내며, ωn은 고유진동수, ζ는 감쇠비이다.",
            "주파수응답은 s=jω를 대입하여 얻고, 정규화하면 크기는 |G(jω)|/K = 1 / sqrt((1-(ω/ωn)²)² + (2ζω/ωn)²)로 표현할 수 있다.",
            "공진주파수는 주파수응답 크기가 최대가 되는 주파수이며, 표준 2차계에서는 ζ < 1/sqrt(2)일 때 ωr = ωn sqrt(1 - 2ζ²)로 주어진다.",
            "ζ가 작을수록 공진 peak가 커지고, ζ가 증가하면 peak가 감소하며 ζ ≥ 1/sqrt(2)에서는 뚜렷한 공진 peak가 나타나지 않는다.",
            "시간응답 overshoot는 step response에서 목표값을 초과하는 현상이고, 주파수응답 resonance는 특정 주파수 입력에서 이득이 커지는 현상이므로 서로 구분해야 한다.",
            "ζ=1은 임계감쇠로 시간응답에서 오버슈트 없이 빠르게 수렴하는 조건이지, 주파수응답 공진 조건이 아니다.",
        ],
        high_score_features=[
            "표준 2차 전달함수를 정확히 쓴다.",
            "주파수응답 크기식을 정규화 형태로 설명한다.",
            "ωr = ωn sqrt(1 - 2ζ²)와 조건 ζ < 1/sqrt(2)를 정확히 제시한다.",
            "감쇠비 증가에 따른 공진 peak 감소를 설명한다.",
            "시간응답 overshoot와 주파수응답 resonance를 명확히 구분한다.",
            "ζ=1 임계감쇠를 공진 조건처럼 오해하지 않는다.",
        ],
        low_score_patterns=[
            "ζ=1을 공진 조건처럼 설명한다.",
            "공진주파수 조건 ζ < 1/sqrt(2)를 누락한다.",
            "ωd = ωn sqrt(1-ζ²)와 ωr = ωn sqrt(1-2ζ²)를 혼동한다.",
            "step overshoot와 frequency resonance를 같은 개념으로 설명한다.",
            "2차 전달함수의 분모 감쇠항 2ζωn s를 잘못 쓴다.",
        ],
        field_connection_points=[
            "natural frequency",
            "damping ratio",
            "frequency response",
            "resonant peak",
            "resonance frequency",
            "overshoot",
            "critical damping",
            "servo system",
            "mechanical vibration",
            "control loop tuning",
        ],
    ),
]

FACT_TOPICS: list[dict[str, Any]] = [
    fact_topic(
        topic_id="vibration_measurement_condition_monitoring",
        name="진동 측정과 상태감시",
        aliases=["진동측정", "상태감시", "condition monitoring", "shaft vibration", "bearing fault"],
        triggers=["진동", "진동측정", "상태감시", "변위센서", "속도센서", "가속도센서", "shaft vibration", "bearing fault", "trip"],
        anchors=[
            anchor("vibration_measurement_condition_monitoring", 1, "센서별 측정 대상", "변위 센서는 축 상대변위와 저주파 대진폭 진동, 속도 센서는 housing의 중간 주파수 진동, 가속도 센서는 고주파 충격과 베어링 결함 진단에 주로 적용된다.", ["변위", "속도", "가속도", "주파수 대역"], ["저주파", "중간 주파수", "고주파", "상대변위", "충격"]),
            anchor("vibration_measurement_condition_monitoring", 2, "shaft vibration과 housing vibration", "shaft vibration은 주로 비접촉 변위 probe로 축의 상대 운동을 감시하고, housing vibration은 하우징에 부착한 속도 또는 가속도 센서로 구조물 전달 진동을 감시한다.", ["shaft vibration", "housing vibration", "비접촉 변위 probe"], ["proximity probe", "bearing housing", "velocity pickup", "accelerometer"]),
            anchor("vibration_measurement_condition_monitoring", 3, "베어링 결함 진단", "베어링 결함은 고주파 충격 성분과 반복 주파수 특성이 중요하므로 accelerometer, FFT, envelope analysis, trend를 이용해 진단한다.", ["베어링 결함", "고주파", "FFT", "envelope"], ["내륜", "외륜", "ball pass frequency", "trend"]),
            anchor("vibration_measurement_condition_monitoring", 4, "보호 trip과 진단 monitoring", "보호용 trip은 과진동 시 설비 손상을 방지하는 한계 동작이고, 진단용 monitoring은 spectrum과 trend로 원인을 분석하는 기능이다.", ["trip", "monitoring", "보호", "진단"], ["alarm", "setpoint", "false trip", "spectrum"]),
            anchor("vibration_measurement_condition_monitoring", 5, "현장 적용 조건", "진동 계측은 설치 강성, 센서 방향, 케이블 노이즈, 접지, alarm/trip 설정, 기존 DCS·보호시스템 연계를 함께 고려해야 한다.", ["설치", "노이즈", "접지", "setpoint"], ["mounting", "shield", "DCS", "protection system"]),
        ],
    ),
    fact_topic(
        topic_id="doppler_effect_velocity_flow_measurement",
        name="도플러 효과와 속도·유량 측정",
        aliases=["도플러", "Doppler", "도플러 유량계", "초음파 도플러"],
        triggers=["도플러", "Doppler", "도플러 유량계", "초음파 도플러", "주파수 편이", "속도 측정"],
        anchors=[
            anchor("doppler_effect_velocity_flow_measurement", 1, "도플러 효과 정의", "도플러 효과는 파원, 관측자 또는 반사체의 상대운동 때문에 수신 주파수가 송신 주파수와 달라지는 현상이다.", ["도플러 효과", "상대운동", "수신 주파수"], ["송신 주파수", "주파수 편이", "반사체"]),
            anchor("doppler_effect_velocity_flow_measurement", 2, "접근·이격 주파수 변화", "반사체가 접근하면 수신 주파수는 증가하고, 이격하면 수신 주파수는 감소한다.", ["접근", "주파수 증가", "이격", "주파수 감소"], ["approach", "recede", "frequency shift"]),
            anchor("doppler_effect_velocity_flow_measurement", 3, "속도 산출 원리", "도플러 측정은 송신파와 반사파의 주파수 차이를 이용하여 반사체의 속도 성분을 계산한다.", ["송신파", "반사파", "주파수 차이", "속도"], ["incident wave", "reflected wave", "velocity component"]),
            anchor("doppler_effect_velocity_flow_measurement", 4, "초음파 도플러 유량계 조건", "도플러 초음파 유량계는 유체 내 입자, 기포, 슬러리 등 초음파를 산란·반사하는 반사체가 있어야 안정적으로 동작한다.", ["초음파", "입자", "기포", "반사체"], ["slurry", "scatter", "dirty liquid"]),
            anchor("doppler_effect_velocity_flow_measurement", 5, "적용 구분", "깨끗한 액체에는 transit-time 방식이 유리한 경우가 많고, 도플러 방식은 반사체가 있는 유체에 적합하며 레이다는 전자파 반사를 이용한다.", ["transit-time", "도플러", "레이다", "초음파"], ["clean liquid", "radar", "매질", "설치각"]),
        ],
    ),
    fact_topic(
        topic_id="adc_dac_signal_conversion_interface",
        name="ADC/DAC 신호 변환 인터페이스",
        aliases=["ADC", "DAC", "A/D 변환", "D/A 변환", "표본화", "양자화"],
        triggers=["ADC", "DAC", "A/D", "D/A", "표본화", "양자화", "부호화", "샘플링", "sampling", "quantization"],
        anchors=[
            anchor("adc_dac_signal_conversion_interface", 1, "ADC 변환 과정", "ADC는 아날로그 신호를 표본화, 양자화, 부호화 과정을 거쳐 디지털 코드로 변환한다.", ["ADC", "표본화", "양자화", "부호화"], ["sample and hold", "binary code", "digital conversion"]),
            anchor("adc_dac_signal_conversion_interface", 2, "DAC 변환 과정", "DAC는 디지털 코드를 디코딩하고 가중 합성한 뒤 필터링을 통해 아날로그 출력으로 복원한다.", ["DAC", "디코딩", "가중 합성", "필터링"], ["R-2R ladder", "current source", "reconstruction filter"]),
            anchor("adc_dac_signal_conversion_interface", 3, "해상도와 정확도 구분", "bit 수 증가는 LSB를 작게 하여 해상도를 높이지만 기준전압, 노이즈, 선형성, offset/gain error가 나쁘면 정확도는 보장되지 않는다.", ["bit", "해상도", "정확도", "LSB"], ["reference voltage", "noise", "offset", "gain"]),
            anchor("adc_dac_signal_conversion_interface", 4, "오차 요인", "ADC/DAC 품질은 양자화 오차, 오프셋 오차, 이득 오차, INL/DNL, 샘플링 지터의 영향을 받는다.", ["양자화 오차", "오프셋 오차", "이득 오차", "INL", "DNL", "지터"], ["linearity", "sampling jitter", "error budget"]),
            anchor("adc_dac_signal_conversion_interface", 5, "현장 인터페이스 고려사항", "계측 인터페이스에서는 anti-aliasing filter, 기준전압 안정도, 접지, 차폐, 절연, PLC scan time, 제어 주기와의 정합성을 고려해야 한다.", ["anti-aliasing", "기준전압", "접지", "절연", "scan time"], ["shield", "grounding", "control period", "DAQ"]),
        ],
    ),
    fact_topic(
        topic_id="temperature_sensor_thermowell_material_selection",
        name="온도센서 Thermowell 재질·형상 선정",
        aliases=["thermowell", "써모웰", "온도센서 보호관", "보호관", "삽입길이"],
        triggers=["thermowell", "써모웰", "온도센서 보호관", "보호관", "삽입 길이", "wake frequency", "온도센서 재질"],
        anchors=[
            anchor("temperature_sensor_thermowell_material_selection", 1, "thermowell 목적", "Thermowell은 온도센서를 압력, 부식, 침식, 유속, 충격으로부터 보호하고 운전 중 센서 교체성을 확보하는 압력 경계 부품이다.", ["thermowell", "보호", "압력 경계", "센서 교체"], ["부식", "침식", "유속", "process connection"]),
            anchor("temperature_sensor_thermowell_material_selection", 2, "재질 선정", "재질은 온도, 압력, 부식성, 침식성, 유체 조성, 기존 배관 재질과의 적합성에 따라 SS316, Hastelloy, Inconel, Monel, Titanium 등을 검토한다.", ["재질", "온도", "압력", "부식", "SS316"], ["Hastelloy", "Inconel", "Monel", "Titanium", "galvanic corrosion"]),
            anchor("temperature_sensor_thermowell_material_selection", 3, "형상과 삽입 길이", "형상과 삽입 길이는 대표 온도 측정, 응답성, 강도, 압력손실, 설치 공간을 고려하여 결정한다.", ["형상", "삽입 길이", "응답성", "강도"], ["straight", "tapered", "stepped", "immersion length"]),
            anchor("temperature_sensor_thermowell_material_selection", 4, "진동·파손 위험", "유속이 큰 배관에서는 vortex shedding과 wake frequency가 thermowell 고유진동수와 근접하면 피로 파손 위험이 있으므로 진동 검토가 필요하다.", ["vortex shedding", "wake frequency", "고유진동수", "피로 파손"], ["유속", "resonance", "ASME PTC 19.3 TW"]),
            anchor("temperature_sensor_thermowell_material_selection", 5, "응답 지연과 유지보수", "Thermowell은 센서 보호와 교체성을 높이지만 열용량 증가로 응답 지연을 유발할 수 있어 보호성, 응답성, 유지보수, 비용을 함께 평가해야 한다.", ["응답 지연", "유지보수", "비용", "교체성"], ["thermal lag", "spare", "standardization", "shutdown"]),
        ],
    ),
    fact_topic(
        topic_id="level_measurement_sensor_selection",
        name="레벨 측정 센서 비교·선정",
        aliases=["레벨 측정", "level measurement", "GWR", "초음파 레벨계", "정전용량식 레벨계"],
        triggers=["레벨", "level", "초음파 레벨", "플로트", "GWR", "가이드웨이브 레이더", "레이저 레벨", "정전용량식", "액위"],
        anchors=[
            anchor("level_measurement_sensor_selection", 1, "접촉·비접촉 분류", "초음파와 레이저는 비접촉식, 플로트와 정전용량식은 접촉식이며, GWR은 probe를 따라 전자파가 진행하므로 접촉식 계열로 보는 것이 적절하다.", ["접촉식", "비접촉식", "초음파", "GWR", "플로트"], ["laser", "capacitance", "probe", "guided wave radar"]),
            anchor("level_measurement_sensor_selection", 2, "초음파·레이저 한계", "초음파와 레이저 레벨계는 비접촉 장점이 있으나 거품, 증기, 분진, 표면 난반사, 내부 구조물 영향을 받을 수 있다.", ["초음파", "레이저", "거품", "증기", "분진"], ["non-contact", "reflection", "false echo", "vapor"]),
            anchor("level_measurement_sensor_selection", 3, "플로트 방식 조건", "플로트 방식은 구조가 단순하고 저비용이나 점도, 고착, 슬러지, 부식, 기계적 마모에 취약하다.", ["플로트", "점도", "고착", "부식"], ["sludge", "mechanical wear", "maintenance"]),
            anchor("level_measurement_sensor_selection", 4, "GWR·정전용량식 조건", "GWR은 유전율, probe 부착물, 계면 조건을 고려해야 하고 정전용량식은 유전율, coating, 접지, interface 조건의 영향을 크게 받는다.", ["GWR", "정전용량식", "유전율", "부착물"], ["interface", "coating", "grounding", "dielectric constant"]),
            anchor("level_measurement_sensor_selection", 5, "현장 선정 기준", "레벨 센서는 압력·온도, 거품·증기·분진, 점도, 부식성, 방폭, 세정성, calibration, 기존 nozzle과 wiring, 비용을 종합해 선정한다.", ["압력", "온도", "방폭", "부식성", "비용"], ["nozzle", "wiring", "calibration", "cleaning"]),
        ],
    ),
    fact_topic(
        topic_id="continuous_discrete_control_model_comparison",
        name="연속시간·이산시간·이산사건 제어모델 비교",
        aliases=["연속시간 모델", "이산시간 모델", "이산사건 모델", "z 변환", "차분방정식"],
        triggers=["연속시간", "이산시간", "이산사건", "차분방정식", "z 변환", "sampling period", "aliasing", "디지털 제어 모델"],
        anchors=[
            anchor("continuous_discrete_control_model_comparison", 1, "연속시간 모델", "연속시간 모델은 시간 변수가 연속이고 미분방정식, 전달함수, Laplace 변환으로 표현되며 물리계 동특성 해석에 적합하다.", ["연속시간", "미분방정식", "전달함수", "Laplace"], ["continuous time", "frequency response", "analog"]),
            anchor("continuous_discrete_control_model_comparison", 2, "이산시간 모델", "이산시간 모델은 sampling period마다 값이 갱신되며 차분방정식과 z 변환으로 표현되어 디지털 제어기 구현에 적합하다.", ["이산시간", "sampling period", "차분방정식", "z 변환"], ["discrete time", "pulse transfer function", "digital control"]),
            anchor("continuous_discrete_control_model_comparison", 3, "이산사건 모델", "이산사건 모델은 연속량보다 이벤트 발생과 상태 전이가 중요하며 PLC sequence, interlock, batch process에 적합하다.", ["이산사건", "이벤트", "상태 전이", "PLC"], ["sequence", "interlock", "batch", "finite state"]),
            anchor("continuous_discrete_control_model_comparison", 4, "디지털 제어 영향", "디지털 제어에서는 zero-order hold, computation delay, quantization, phase lag가 안정성과 응답성에 영향을 준다.", ["zero-order hold", "계산 지연", "quantization", "phase lag"], ["scan time", "sampled-data", "stability"]),
            anchor("continuous_discrete_control_model_comparison", 5, "aliasing과 샘플링", "샘플링 주기가 부적절하면 aliasing이 발생하므로 신호 대역폭, anti-aliasing filter, 제어 주기, 통신 지연을 고려해야 한다.", ["aliasing", "anti-aliasing", "샘플링", "통신 지연"], ["bandwidth", "control period", "sampling theorem"]),
        ],
    ),
    fact_topic(
        topic_id="second_order_system_resonance_frequency_response",
        name="2차 시스템 주파수응답과 공진주파수",
        aliases=["2차 시스템", "공진주파수", "resonance frequency", "frequency response", "감쇠비"],
        triggers=["2차 시스템", "2차계", "공진주파수", "주파수응답", "resonance", "감쇠비", "zeta", "omega r"],
        anchors=[
            anchor("second_order_system_resonance_frequency_response", 1, "표준 2차 전달함수", "표준 2차 시스템은 G(s)=Kωn²/(s²+2ζωns+ωn²) 형태로 표현하며 ωn은 고유진동수, ζ는 감쇠비이다.", ["2차 전달함수", "ωn", "ζ", "감쇠비"], ["natural frequency", "standard second-order system"]),
            anchor("second_order_system_resonance_frequency_response", 2, "주파수응답 크기식", "s=jω를 대입하면 정규화 크기는 |G(jω)|/K = 1 / sqrt((1-(ω/ωn)²)² + (2ζω/ωn)²)로 표현된다.", ["주파수응답", "크기식", "s=jω"], ["normalized frequency", "magnitude response"]),
            anchor("second_order_system_resonance_frequency_response", 3, "공진주파수와 조건", "표준 2차계의 공진주파수는 ζ < 1/sqrt(2)일 때 ωr = ωn sqrt(1 - 2ζ²)로 주어진다.", ["공진주파수", "ωr", "ζ < 1/sqrt(2)"], ["resonant peak", "omega r"]),
            anchor("second_order_system_resonance_frequency_response", 4, "감쇠비와 공진 peak", "감쇠비가 작을수록 공진 peak가 커지고, ζ ≥ 1/sqrt(2)에서는 뚜렷한 공진 peak가 나타나지 않는다.", ["감쇠비", "공진 peak", "ζ"], ["resonant peak", "damping ratio"]),
            anchor("second_order_system_resonance_frequency_response", 5, "overshoot와 resonance 구분", "시간응답 overshoot는 step response에서 목표값을 초과하는 현상이고, 주파수응답 resonance는 특정 주파수 입력에서 이득이 커지는 현상이며 ζ=1 임계감쇠는 공진 조건이 아니다.", ["overshoot", "resonance", "ζ=1", "임계감쇠"], ["step response", "frequency response", "critical damping"]),
        ],
    ),
]


def apply_existing_topic_fixes(model_bank: dict[str, Any], fact_bank: dict[str, Any]) -> None:
    # 1) flowmeter_dp_orifice: remove ultrasonic/Doppler triggers from DP/orifice routing.
    for topic in fact_bank.get("topics", []):
        if not isinstance(topic, dict):
            continue
        if topic.get("topic_id") == "flowmeter_dp_orifice":
            topic["triggers"] = [
                "유량계",
                "오리피스",
                "위어",
                "차압식",
                "차압 유량계",
                "DP flowmeter",
                "orifice flowmeter",
                "유량측정",
            ]

    # 2) local instrument cabinet: installation/evaluation lens and law-number softening.
    for item in model_bank.get("answers", []):
        if not isinstance(item, dict):
            continue
        topic_id = item.get("topic_id")

        if topic_id == "local_instrument_cabinet_installation":
            item["question_type"] = "IMPLEMENTATION_EVALUATION"
            item["expected_structure"] = [
                "설치 목적과 적용 범위",
                "전원·접지·보호장치 검토",
                "방폭·충전부 방호·작업공간 등 안전 기준 검토",
                "배선, gland, shield, 접지, 노이즈 대책",
                "점검·유지보수·기존 설비 연계 조건",
            ]
            outline = []
            for line in item.get("model_answer_outline", []):
                text = str(line)
                if "70cm" in text or "70 cm" in text:
                    text = "계장반은 관계 법령과 전기설비 기준에 따른 조작·점검 작업공간을 확보하고, 설비 전압·위험도·점검 방식에 맞게 접근성을 검토해야 한다."
                outline.append(text)
            if outline:
                item["model_answer_outline"] = outline
            item["field_connection_points"] = [
                "panel grounding",
                "shield grounding",
                "cable gland",
                "IP 등급",
                "방폭",
                "작업공간",
                "ventilation",
                "condensation",
                "loop check",
                "maintenance access",
            ]

        # 3) control valve positioner expected structure completion.
        if topic_id == "control_valve_positioner_ip_converter":
            item["expected_structure"] = [
                "배경과 최종제어요소 역할",
                "I/P converter의 4~20mA to 3~15 psi 변환",
                "포지셔너 구성: diaphragm/capsule, pilot valve, actuator",
                "feedback spring/linkage에 의한 위치 피드백",
                "힘 평형과 목표 위치 정지",
                "마찰·히스테리시스·air supply·fail action 등 현장 문제",
            ]
            item["field_connection_points"] = [
                "I/P converter",
                "4~20mA",
                "3~15 psi",
                "pilot valve",
                "feedback spring",
                "linkage",
                "stiction",
                "dead band",
                "air supply",
                "fail open",
                "fail close",
                "smart positioner",
            ]

        # 4) d-q reference frame field points.
        if topic_id == "induction_motor_dq_reference_frame_equivalent_circuit":
            item["field_connection_points"] = [
                "벡터제어",
                "d축 자속 제어",
                "q축 토크 전류 제어",
                "좌표계 부호",
                "속도기전력 보상",
                "전류제어기 설계",
                "인버터 구동",
                "센서리스 제어",
            ]

        # 5) soften RTD temperature threshold expression.
        if topic_id == "temperature_sensor_thermocouple_rtd":
            new_outline = []
            changed = False
            for line in item.get("model_answer_outline", []):
                text = str(line)
                if "300℃ 이하" in text:
                    text = (
                        "따라서 중저온 정밀 온도 제어, 품질 관리, 저온 공정에는 RTD가 유리한 경우가 많고, "
                        "고온 furnace, 배관 표면 온도, 빠른 응답이 필요한 공정에는 열전대가 적합한 경우가 많다."
                    )
                    changed = True
                new_outline.append(text)
            if changed:
                item["model_answer_outline"] = new_outline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-backup", action="store_true", help="Do not create backup files")
    parser.add_argument("--skip-validate-all", action="store_true", help="Skip scripts/rubric_manager.py validate-all")
    args = parser.parse_args()

    model_bank = load_model_answer_bank(MODEL_ANSWER_BANK)
    fact_bank = load_fact_anchor_bank(FACT_ANCHOR_BANK)

    if not args.no_backup:
        print("backup:", backup_file(MODEL_ANSWER_BANK))
        print("backup:", backup_file(FACT_ANCHOR_BANK))

    for entry in MODEL_ANSWERS:
        model_bank = upsert_model_answer(model_bank, entry)
        print("upsert model_answer:", entry["id"])

    for topic in FACT_TOPICS:
        fact_bank = upsert_fact_anchor_topic(fact_bank, topic)
        print("upsert fact_anchor:", topic["topic_id"])

    apply_existing_topic_fixes(model_bank, fact_bank)

    model_errors = validate_model_answer_bank(model_bank, allowed_types=question_type_ids())
    fact_errors = validate_fact_anchor_bank_data(fact_bank)

    if model_errors:
        print("\nINVALID model_answer bank:")
        for err in model_errors:
            print("-", err)
        return 1

    if fact_errors:
        print("\nINVALID fact_anchor bank:")
        for err in fact_errors:
            print("-", err)
        return 1

    save_model_answer_bank(model_bank, MODEL_ANSWER_BANK)
    save_fact_anchor_bank(fact_bank, FACT_ANCHOR_BANK)

    print("\nSaved:")
    print("-", MODEL_ANSWER_BANK)
    print("-", FACT_ANCHOR_BANK)

    if not args.skip_validate_all:
        print("\nRUN: python3 scripts/rubric_manager.py validate-all")
        rc = subprocess.call([sys.executable, str(ROOT / "scripts" / "rubric_manager.py"), "validate-all"], cwd=str(ROOT))
        if rc != 0:
            print("\nvalidate-all failed:", rc)
            return rc

    print("\nDONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
