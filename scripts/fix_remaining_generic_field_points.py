#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
BACKUP_DIR = ROOT / "reports" / "backups"

GENERIC = {
    "현장 적용 시 정격, 손실, 발열, 파형, 보호회로를 함께 검토한다.",
    "측정 시 전압 파형과 전류 파형을 함께 확인한다.",
    "설계 변경 시 효율, 신뢰성, 비용, 유지보수성을 함께 판단한다.",
}

REPLACEMENTS = {
    "rectifier_source_inductance_commutation_overlap": [
        "전원 인덕턴스",
        "commutation overlap angle",
        "평균 DC 출력전압 저하",
        "thyristor 정류기",
        "변압기 누설 리액턴스",
        "line current distortion",
        "전압 강하와 전류 중첩",
        "부하전류 변화에 따른 중첩 증가",
        "전원 용량과 단락 임피던스 검토",
    ],
    "dc_dc_chopper_buck_converter": [
        "duty ratio",
        "switching frequency",
        "inductor ripple current",
        "output capacitor ripple",
        "buck/boost topology",
        "MOSFET/diode conduction loss",
        "switching loss",
        "EMI filter",
        "thermal design",
        "over-current protection",
    ],
    "power_semiconductor_switching_device_characteristics": [
        "SCR, GTO, IGBT, MOSFET",
        "전압·전류 rating",
        "conduction loss",
        "switching loss",
        "gate drive",
        "safe operating area",
        "thermal impedance",
        "short-circuit protection",
        "dv/dt와 di/dt 제한",
    ],
    "reference_tracking_prefilter_steady_state_error_control": [
        "state feedback",
        "reference gain",
        "prefilter",
        "Nbar",
        "steady-state error",
        "model mismatch",
        "actuator saturation",
        "disturbance rejection",
        "servo control",
    ],
    "thermopile_noncontact_ir_temperature_sensor": [
        "infrared radiation",
        "Seebeck effect",
        "emissivity",
        "field of view",
        "ambient temperature compensation",
        "blackbody calibration",
        "lens contamination",
        "response time",
        "비접촉 온도 측정 거리",
    ],
    "psd_position_sensitive_detector_optical_sensor": [
        "light spot position",
        "photocurrent ratio",
        "position calculation circuit",
        "analog signal conditioning",
        "linearity",
        "light source alignment",
        "ambient light noise",
        "calibration",
        "측정 거리와 spot size",
    ],
    "wheatstone_bridge_null_balance_measurement": [
        "bridge balance",
        "null point",
        "strain gauge",
        "RTD bridge",
        "excitation voltage",
        "lead wire compensation",
        "instrumentation amplifier",
        "zero drift",
        "temperature compensation",
    ],
    "photodiode_light_sensor_operation_modes": [
        "photovoltaic mode",
        "photoconductive mode",
        "reverse bias",
        "responsivity",
        "dark current",
        "transimpedance amplifier",
        "bandwidth",
        "ambient light shielding",
        "optical filter",
    ],
    "industrial_robot_degrees_of_freedom": [
        "degree of freedom",
        "joint configuration",
        "workspace",
        "reach",
        "payload",
        "singularity",
        "repeatability",
        "path planning",
        "tool center point",
        "safety zone",
    ],
    "frame_grounding_shielding_noise_control": [
        "frame ground",
        "shield termination",
        "one-point grounding",
        "multi-point grounding",
        "ground loop",
        "EMC",
        "cable tray bonding",
        "surge protection",
        "isolation",
        "noise current return path",
    ],
    "measurement_repeatability_reproducibility": [
        "Gage R&R",
        "repeatability",
        "reproducibility",
        "operator variation",
        "equipment variation",
        "ANOVA",
        "%GRR",
        "calibration",
        "measurement system analysis",
        "품질검사 판정 신뢰성",
    ],
    "energy_harvesting_wireless_sensor_power": [
        "energy harvesting source",
        "solar, vibration, thermal gradient",
        "power budget",
        "duty cycle",
        "supercapacitor",
        "backup battery",
        "wireless sensor node",
        "low-power communication",
        "maintenance interval",
        "harvester 설치 위치",
    ],
    "hart_fims_field_instrument_management": [
        "HART device parameter",
        "DD/DTM",
        "FIMS",
        "asset management",
        "online diagnostics",
        "calibration history",
        "loop check",
        "commissioning",
        "preventive maintenance",
        "DCS asset management integration",
    ],
    "pressure_transmitter_datasheet_specification": [
        "range와 span",
        "maximum working pressure",
        "accuracy와 turndown",
        "wetted material",
        "process connection",
        "diaphragm seal",
        "output signal/protocol",
        "hazardous area certification",
        "IP/NEMA enclosure",
        "installation environment",
    ],
    "reliability_maintainability_availability_ram": [
        "MTBF",
        "MTTR",
        "availability",
        "redundancy",
        "modularization",
        "diagnostics",
        "spare parts",
        "preventive maintenance",
        "maintenance accessibility",
        "RAM KPI",
    ],
    "wirelesshart_isa100_wireless_instrument_network": [
        "WirelessHART",
        "ISA100.11a",
        "mesh network",
        "gateway",
        "channel hopping",
        "battery life",
        "security key",
        "latency",
        "coexistence with Wi-Fi",
        "DCS/PLC integration",
    ],
}

def has_generic(points):
    return isinstance(points, list) and any(x in GENERIC for x in points)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    answers = data.get("answers", [])

    changed = []
    remaining = []

    for answer in answers:
        tid = answer.get("topic_id")
        points = answer.get("field_connection_points")
        if not has_generic(points):
            continue

        if tid in REPLACEMENTS:
            before = list(points)
            answer["field_connection_points"] = REPLACEMENTS[tid]
            notes = answer.setdefault("revision_notes", [])
            notes.append(
                datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                + " content_fix_v2: replaced generic field_connection_points with topic-specific points."
            )
            changed.append((tid, before, answer["field_connection_points"]))
        else:
            remaining.append(tid)

    if args.dry_run:
        print("DRY RUN")
        for tid, before, after in changed:
            print("WOULD: patch field_connection_points:", tid)
        if remaining:
            print("remaining generic field_connection_points needing manual review:")
            for tid in sorted(set(remaining)):
                print("-", tid)
        else:
            print("remaining generic field_connection_points: 0")
        return

    if changed:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = BACKUP_DIR / f"industrial_instrumentation_control.model_answers.before_remaining_generic_fix.{stamp}.json"
        backup.write_text(MODEL_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        MODEL_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("backup:", backup.relative_to(ROOT))

    for tid, before, after in changed:
        print("patched field_connection_points:", tid)

    if remaining:
        print("WARN: remaining generic field_connection_points needing manual review:")
        for tid in sorted(set(remaining)):
            print("WARN:", tid)
    else:
        print("remaining generic field_connection_points: 0")

    print("DONE")

if __name__ == "__main__":
    main()
