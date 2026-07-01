#!/usr/bin/env python3
"""
Fix known model-answer content issues found in the current rubric bank.

This script intentionally changes only content fields that were found to be
inconsistent with the current question_type taxonomy or with the topic itself.

Targets:
1) Cv CALC_DESIGN answer
   - CALC_DESIGN is absorbed into PRINCIPLE_INTERPRETATION.
   - Keep legacy_question_type=CALC_DESIGN so DEFINE and CALC_DESIGN can coexist.

2) Contaminated field_connection_points
   - Some non-power-electronics topics inherited generic points such as
     "정격, 손실, 발열, 파형, 보호회로".
   - Replace them with topic-specific field points.

3) Smart factory answer scope
   - Keep the topic as implementation/evaluation.
   - Reduce over-merged digital twin/cybersecurity material to supporting points.

Run from repo root:
  python3 scripts/fix_model_answer_content_issues.py
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"

BAD_GENERIC_FIELD_POINTS = [
    "현장 적용 시 정격, 손실, 발열, 파형, 보호회로를 함께 검토한다.",
    "측정 시 전압 파형과 전류 파형을 함께 확인한다.",
    "설계 변경 시 효율, 신뢰성, 비용, 유지보수성을 함께 판단한다.",
]

POWER_RELATED_TOPIC_TOKENS = (
    "dc_dc",
    "power_semiconductor",
    "solar_cell",
    "inverter",
    "converter",
    "switching_device",
)

FIELD_POINT_PATCHES: dict[str, list[str]] = {
    "camera_lidar_radar_sensor_comparison": [
        "탐지 거리와 해상도 요구",
        "조명 조건, 역광, 야간 환경",
        "비, 안개, 눈, 먼지 등 악천후 영향",
        "거리 측정 정확도와 상대 속도 측정",
        "3D point cloud와 객체 분류 성능",
        "센서 융합 시 시간 동기화",
        "좌표계 정합과 extrinsic calibration",
        "연산량, 비용, 실시간성, 안전 요구수준",
    ],
    "industrial_ethernet_realtime_network": [
        "cycle time",
        "latency",
        "jitter",
        "time synchronization",
        "determinism",
        "network load",
        "PLC, drive, remote I/O 연계",
        "EtherCAT, PROFINET, EtherNet/IP, TSN 선정",
        "기존 장비 호환성과 유지보수 인력",
    ],
    "induction_motor_dq_reference_frame_equivalent_circuit": [
        "d-q 좌표변환",
        "정지좌표계와 회전좌표계",
        "Park/Clarke 변환",
        "자속축과 토크축 분리",
        "슬립 주파수",
        "벡터제어",
        "인버터 구동",
        "전동기 파라미터 추정",
    ],
    "classification_model_precision_recall_f1_evaluation": [
        "confusion matrix",
        "TP, FP, FN, TN",
        "precision",
        "recall",
        "F1-score",
        "불균형 데이터",
        "설비 이상진단 false alarm",
        "품질검사 missed detection",
        "threshold 조정",
        "업무 리스크별 지표 선정",
    ],
    "mems_comb_drive_electrostatic_actuator": [
        "정전기력",
        "comb finger 구조",
        "전극 gap",
        "구동 전압",
        "변위와 capacitance 변화",
        "pull-in",
        "stiction",
        "공진 주파수",
        "제작 공차와 패키징",
    ],
    "control_valve_body_trim_selection": [
        "globe valve",
        "butterfly valve",
        "balanced trim",
        "unbalanced trim",
        "actuator thrust",
        "seat leakage",
        "rangeability",
        "cavitation과 flashing",
        "오염 유체와 trim 막힘",
        "유지보수 비용",
    ],
    "sensor_linearization_transfer_function_approximation": [
        "static transfer function",
        "dynamic transfer function",
        "calibration data",
        "piecewise linear approximation",
        "lookup table",
        "polynomial fitting",
        "spline approximation",
        "외삽 오차",
        "과적합",
        "보정 데이터 품질",
    ],
    "sensor_static_dynamic_performance_characteristics": [
        "sensitivity",
        "resolution",
        "linearity",
        "hysteresis",
        "repeatability",
        "stability",
        "response time",
        "bandwidth",
        "noise",
        "비용과 성능 trade-off",
    ],
    "smart_mcc_motor_control_center_monitoring": [
        "motor current",
        "thermal overload",
        "전력품질",
        "전동기 상태감시",
        "trip 이력",
        "보호계전",
        "통신 연계",
        "예지보전",
        "기존 MCC retrofit",
        "정비 접근성과 비용",
    ],
    "gpib_scpi_instrumentation_communication": [
        "IEEE 488",
        "SCPI command",
        "Talker, Listener, Controller",
        "계측 장비 자동화",
        "test sequence",
        "장비별 명령 호환성",
        "timeout과 응답 지연",
        "remote calibration",
        "legacy 장비 연계",
    ],
    "pressure_gauge_accessories_installation": [
        "isolating valve",
        "block and vent valve",
        "snubber",
        "pressure dampener",
        "overpressure protector",
        "siphon",
        "diaphragm seal",
        "맥동과 진동",
        "부식성·점성 유체",
        "응답 지연과 누설점 증가",
    ],
    "control_valve_actuator_types_selection": [
        "required torque",
        "valve size와 차압",
        "electric actuator",
        "pneumatic actuator",
        "hydraulic actuator",
        "fail-open, fail-close, fail-last",
        "positioner",
        "limit switch와 feedback signal",
        "방폭과 동력원 availability",
        "PLC/DCS 인터페이스",
    ],
}

SMART_FACTORY_PATCH = {
    "model_answer_outline": [
        "스마트팩토리 도입 효과 평가는 생산, 품질, 설비, 에너지, 안전, 운영 관리 측면에서 도입 전후 성과를 비교하는 것이다.",
        "평가 전에는 동일 제품, 동일 공정, 동일 기간, 동일 집계 기준으로 baseline을 확보해야 한다.",
        "핵심 지표는 OEE, 가동률, 불량률, 재작업률, MTBF, MTTR, 돌발정지 시간, 에너지 사용량, 작업자 개입 시간, ROI로 설정할 수 있다.",
        "정량 효과는 불량률 감소, 정지시간 감소, 생산성 향상, 에너지 절감, 유지보수 비용 절감으로 분석한다.",
        "정성 효과는 이상 조기 감지, 의사결정 속도 향상, 작업 표준화, 데이터 기반 개선 문화 형성으로 평가한다.",
        "IIoT 데이터 흐름은 sensor, edge gateway, PLC/DCS, historian, MES/ERP, analytics로 이어지며, 데이터 품질과 시간 동기화가 중요하다.",
        "digital twin은 상태 추정, what-if 분석, 예지보전에 활용할 수 있으나 도입 효과 평가의 보조 수단으로 다룬다.",
        "기존 PLC/DCS 연계 안정성, 사이버보안, 망분리, 접근제어, 운영 인력 숙련도, model drift를 도입 리스크로 검토한다.",
        "전면 도입보다 손실이 큰 공정에 pilot 적용 후 KPI와 ROI를 확인하고 단계적으로 확대하는 것이 현실적이다.",
    ],
    "high_score_features": [
        "평가 대상과 baseline 조건을 명확히 설정한다.",
        "OEE, 불량률, MTBF, MTTR, downtime, energy, ROI 등 정량 지표를 사용한다.",
        "정량 효과와 정성 효과를 구분한다.",
        "IIoT 데이터 흐름과 기존 PLC/DCS 연계 조건을 설명한다.",
        "투자비, 데이터 품질, 사이버보안, 운영 인력, model drift 등 한계를 설명한다.",
        "pilot 적용과 단계적 확대 같은 현실적 후속 조치를 제시한다.",
    ],
    "field_connection_points": [
        "OEE",
        "baseline",
        "불량률",
        "MTBF",
        "MTTR",
        "downtime",
        "energy intensity",
        "ROI",
        "pilot 적용",
        "edge gateway",
        "historian",
        "MES/ERP",
        "기존 PLC/DCS 연계",
        "cybersecurity",
        "model drift",
    ],
}

def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"ERROR: cannot read {path}: {exc}") from exc

def save_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def note(item: dict[str, Any], message: str) -> None:
    notes = item.setdefault("revision_notes", [])
    if not isinstance(notes, list):
        notes = [str(notes)]
        item["revision_notes"] = notes
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    full = f"{stamp} {message}"
    if full not in notes:
        notes.append(full)

def has_bad_generic(points: Any) -> bool:
    if not isinstance(points, list):
        return False
    joined = "\n".join(str(x) for x in points)
    return any(x in joined for x in BAD_GENERIC_FIELD_POINTS)

def is_power_related(topic_id: str) -> bool:
    return any(tok in topic_id for tok in POWER_RELATED_TOPIC_TOKENS)

def patch_cv(answers: list[dict[str, Any]], dry_run: bool) -> list[str]:
    changes: list[str] = []

    for a in answers:
        if a.get("topic_id") != "cv_valve_flow_coefficient":
            continue

        old = (a.get("id"), a.get("question_type"), a.get("legacy_question_type"), a.get("title"))

        if a.get("legacy_question_type") == "DEFINE" or a.get("id") == "cv_valve_flow_coefficient_DEFINE_v1":
            a["id"] = "cv_valve_flow_coefficient_DEFINE_v1"
            a["question_type"] = "PRINCIPLE_INTERPRETATION"
            a["legacy_question_type"] = "DEFINE"
            a["title"] = "Cv 밸브 유량계수 정의형 모범 답안"

        is_calc = (
            a.get("legacy_question_type") == "CALC_DESIGN"
            or "CALC_DESIGN" in str(a.get("id", ""))
            or "계산" in str(a.get("title", ""))
            or "설계형" in str(a.get("title", ""))
        )
        if is_calc and a.get("id") != "cv_valve_flow_coefficient_DEFINE_v1":
            a["id"] = "cv_valve_flow_coefficient_CALC_DESIGN_v1"
            a["question_type"] = "PRINCIPLE_INTERPRETATION"
            a["legacy_question_type"] = "CALC_DESIGN"
            a["title"] = "Cv 밸브 유량계수 계산·설계형 모범 답안"
            note(a, "content_fix: CALC_DESIGN is mapped to PRINCIPLE_INTERPRETATION by question_type v2.")

        if a.get("legacy_question_type") == "COMPARE" or "COMPARE" in str(a.get("id", "")):
            a["id"] = "cv_valve_flow_coefficient_COMPARE_v1"
            a["question_type"] = "COMPARE_SELECTION"
            a["legacy_question_type"] = "COMPARE"
            a["title"] = "Cv 밸브 유량계수 비교·선정형 모범 답안"

        new = (a.get("id"), a.get("question_type"), a.get("legacy_question_type"), a.get("title"))
        if old != new:
            changes.append(f"patched Cv mapping: {old} -> {new}")

    return changes

def patch_field_points(answers: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    changes: list[str] = []
    remaining_bad: list[str] = []

    for a in answers:
        tid = str(a.get("topic_id", ""))
        if tid in FIELD_POINT_PATCHES:
            old_points = a.get("field_connection_points")
            if old_points != FIELD_POINT_PATCHES[tid]:
                a["field_connection_points"] = FIELD_POINT_PATCHES[tid]
                note(a, "content_fix: replaced topic-mismatched field_connection_points.")
                changes.append(f"patched field_connection_points: {tid}")
            continue

        if has_bad_generic(a.get("field_connection_points")) and not is_power_related(tid):
            remaining_bad.append(tid)

    return changes, sorted(set(remaining_bad))

def patch_smart_factory(answers: list[dict[str, Any]]) -> list[str]:
    changes: list[str] = []
    for a in answers:
        if a.get("topic_id") != "smart_factory_iiot_digital_twin":
            continue
        touched = False
        for key, value in SMART_FACTORY_PATCH.items():
            if a.get(key) != value:
                a[key] = value
                touched = True
        if touched:
            note(a, "content_fix: narrowed over-merged smart factory answer to implementation/evaluation scope.")
            changes.append("patched smart_factory_iiot_digital_twin scope")
    return changes

def validate_pairs(answers: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for a in answers:
        key = (
            str(a.get("topic_id", "")),
            str(a.get("question_type", "")),
            str(a.get("legacy_question_type", "")),
        )
        if key in seen:
            errors.append("duplicate model answer triple: " + " | ".join(key))
        seen.add(key)
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
    args = parser.parse_args()

    data = load_json(MODEL_PATH)
    answers = data.get("answers")
    if not isinstance(answers, list):
        raise SystemExit("ERROR: model answer bank must contain list field: answers")

    before = json.dumps(data, ensure_ascii=False, sort_keys=True)

    changes: list[str] = []
    changes += patch_cv(answers, args.dry_run)
    field_changes, remaining_bad = patch_field_points(answers)
    changes += field_changes
    changes += patch_smart_factory(answers)

    pair_errors = validate_pairs(answers)

    after = json.dumps(data, ensure_ascii=False, sort_keys=True)
    changed = before != after

    if args.dry_run:
        print("DRY RUN")
        for c in changes:
            print("WOULD:", c)
        if not changes:
            print("no changes")
        if remaining_bad:
            print("remaining generic field_connection_points needing manual review:")
            for tid in remaining_bad:
                print("-", tid)
        for e in pair_errors:
            print("ERROR:", e)
        return 1 if pair_errors else 0

    if changed:
        backup_dir = ROOT / "reports" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = backup_dir / f"industrial_instrumentation_control.model_answers.before_content_fix.{stamp}.json"
        backup.write_text(MODEL_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        save_json(MODEL_PATH, data)
        print("backup:", backup.relative_to(ROOT))
        for c in changes:
            print("patched:", c)
    else:
        print("no changes")

    if remaining_bad:
        print("WARN: remaining generic field_connection_points needing manual review:")
        for tid in remaining_bad:
            print("WARN:", tid)

    if pair_errors:
        print("INVALID")
        for e in pair_errors:
            print("ERROR:", e)
        return 1

    print("DONE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
