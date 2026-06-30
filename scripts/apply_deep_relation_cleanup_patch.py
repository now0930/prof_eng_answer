#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

try:
    from rubric_content.model_answers import (  # type: ignore
        load_model_answer_bank,
        save_model_answer_bank,
        question_type_ids,
        validate_model_answer_bank,
    )
    from rubric_content.fact_anchors import (  # type: ignore
        load_fact_anchor_bank,
        save_fact_anchor_bank,
        validate_fact_anchor_bank_data,
    )
except Exception as exc:
    print(f"ERROR: cannot import rubric_content modules: {exc}", file=sys.stderr)
    raise

MODEL_PATH = ROOT / "rubrics/model_answers/industrial_instrumentation_control.json"
FACT_PATH = ROOT / "rubrics/fact_anchors/industrial_instrumentation_control.json"


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "backups"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{path.stem}.before_deep_relation_cleanup.{stamp}{path.suffix}"
    shutil.copy2(path, out)
    return out


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def append_unique_list(obj: dict[str, Any], field: str, values: list[str]) -> bool:
    current = as_list(obj.get(field))
    changed = False
    for v in values:
        if v not in current:
            current.append(v)
            changed = True
    if changed:
        obj[field] = current
    return changed


def replace_list_exact(obj: dict[str, Any], field: str, remove_values: set[str], add_values: list[str] | None = None) -> bool:
    current = as_list(obj.get(field))
    new_list = [x for x in current if x not in remove_values]
    if add_values:
        for v in add_values:
            if v not in new_list:
                new_list.append(v)
    changed = new_list != current
    if changed:
        obj[field] = new_list
    return changed


def model_entries(bank: dict[str, Any], topic_id: str) -> list[dict[str, Any]]:
    return [a for a in bank.get("answers", []) if isinstance(a, dict) and a.get("topic_id") == topic_id]


def fact_topic(bank: dict[str, Any], topic_id: str) -> dict[str, Any] | None:
    return next((t for t in bank.get("topics", []) if isinstance(t, dict) and t.get("topic_id") == topic_id), None)


def append_support_terms_to_anchors(topic: dict[str, Any], terms: list[str], max_each: int | None = None) -> bool:
    changed = False
    anchors = topic.get("anchors", [])
    if not isinstance(anchors, list):
        return False
    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        support = as_list(anchor.get("support_terms"))
        before = list(support)
        candidate_terms = terms[:max_each] if max_each else terms
        for term in candidate_terms:
            if term not in support:
                support.append(term)
        if support != before:
            anchor["support_terms"] = support
            changed = True
    return changed


def append_terms_to_best_matching_anchor(topic: dict[str, Any], name_keywords: list[str], terms: list[str]) -> bool:
    anchors = topic.get("anchors", [])
    if not isinstance(anchors, list):
        return False

    selected: dict[str, Any] | None = None
    for anchor in anchors:
        if not isinstance(anchor, dict):
            continue
        text = " ".join(str(anchor.get(k, "")) for k in ["id", "name", "expected"])
        if any(k in text for k in name_keywords):
            selected = anchor
            break
    if selected is None and anchors and isinstance(anchors[-1], dict):
        selected = anchors[-1]

    if not selected:
        return False

    support = as_list(selected.get("support_terms"))
    before = list(support)
    for term in terms:
        if term not in support:
            support.append(term)
    if support != before:
        selected["support_terms"] = support
        return True
    return False


def mark_revision_model(entry: dict[str, Any], note: str) -> None:
    notes = as_list(entry.get("revision_notes"))
    if note not in notes:
        notes.append(note)
    entry["revision_notes"] = notes


def mark_revision_fact(topic: dict[str, Any], note: str) -> None:
    notes = as_list(topic.get("revision_notes"))
    if note not in notes:
        notes.append(note)
    topic["revision_notes"] = notes


def patch_industrial_communication(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "industrial_communication_protocol"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "산업용 통신은 물리계층, 데이터링크, 응용계층 기능이 결합되어 현장 신호의 실시간성, 결정성, 진단성, 상호운용성을 확보해야 한다.",
            "프로토콜 비교 시 Modbus RTU/TCP, HART, Foundation Fieldbus, Profibus, Profinet, EtherNet/IP, OPC UA의 적용 위치와 update time, jitter, topology를 구분해야 한다.",
            "무선통신은 배선 절감 장점이 있으나 전원, 간섭, 지연, 보안, 신뢰성 조건이 다르므로 일반 유선 산업통신과 같은 trigger로 처리하지 않는 것이 안전하다.",
        ])
        changed += append_unique_list(entry, "high_score_features", [
            "OSI/TCP-IP 계층, 물리 매체, topology, update time, jitter, determinism을 비교한다.",
            "HART/Fieldbus 계열과 Industrial Ethernet 계열의 역할 차이를 설명한다.",
            "무선 통신은 별도 적용 조건과 보안·신뢰성 검토가 필요함을 구분한다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "OSI 계층", "TCP/IP", "physical layer", "topology", "Modbus RTU", "Modbus TCP",
            "HART", "Foundation Fieldbus", "Profibus", "Profinet", "EtherNet/IP",
            "OPC UA", "update time", "jitter", "determinism", "network segmentation",
            "redundancy", "OT 보안"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: strengthened communication protocol model/fact term alignment.")

    topic = fact_topic(fact, tid)
    if topic:
        changed += replace_list_exact(
            topic,
            "triggers",
            {"무선통신", "산업통신", "통신"},
            ["산업용 통신 프로토콜", "Modbus", "HART", "Fieldbus", "Profibus", "Profinet", "EtherNet/IP", "OPC UA"],
        )
        append_terms_to_best_matching_anchor(topic, ["실시간", "성능", "determinism", "jitter"], ["update time", "jitter", "determinism", "real-time"])
        append_terms_to_best_matching_anchor(topic, ["보안", "OT"], ["network segmentation", "firewall", "zone", "conduit", "OT security"])
        append_terms_to_best_matching_anchor(topic, ["계층", "OSI", "TCP"], ["OSI", "TCP/IP", "physical layer", "application layer"])
        mark_revision_fact(topic, "deep_relation_cleanup: narrowed broad triggers and added protocol support terms.")
    return changed


def patch_noise_grounding(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "noise_grounding_surge"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "노이즈는 차동모드와 공통모드로 유입될 수 있으며, 접지 전위차와 ground loop는 저준위 아날로그 신호와 통신 신호의 오동작 원인이 된다.",
            "차폐선은 cable shield, drain wire, gland 처리, 단일점 또는 다점 접지 원칙을 현장 주파수와 설비 기준에 맞게 적용해야 한다.",
            "서지는 낙뢰, 개폐, 대전력 부하 전환에서 발생할 수 있으므로 SPD, bonding, equipotential grounding, 절연, 필터를 조합해 보호한다.",
        ])
        changed += append_unique_list(entry, "high_score_features", [
            "차동모드 노이즈와 공통모드 노이즈를 구분한다.",
            "ground loop, shield 접지, SPD, isolation, filtering을 원인별 대책으로 연결한다.",
            "oscilloscope, trend, insulation test, 접지저항 측정 등 진단 방법을 포함한다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "differential mode", "common mode", "ground loop", "shield grounding", "drain wire",
            "single-point grounding", "multi-point grounding", "SPD", "surge", "bonding",
            "equipotential grounding", "isolation amplifier", "filter", "oscilloscope", "insulation test"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: strengthened noise/grounding/surge model-to-anchor alignment.")

    topic = fact_topic(fact, tid)
    if topic:
        append_terms_to_best_matching_anchor(topic, ["노이즈", "유입"], ["differential mode", "common mode", "EMI", "RFI"])
        append_terms_to_best_matching_anchor(topic, ["접지", "ground"], ["ground loop", "equipotential grounding", "bonding"])
        append_terms_to_best_matching_anchor(topic, ["차폐", "shield"], ["cable shield", "drain wire", "single-point grounding", "multi-point grounding"])
        append_terms_to_best_matching_anchor(topic, ["서지", "surge"], ["SPD", "surge protective device", "lightning", "switching surge"])
        append_terms_to_best_matching_anchor(topic, ["진단", "점검"], ["oscilloscope", "trend", "insulation test", "grounding resistance"])
        mark_revision_fact(topic, "deep_relation_cleanup: added support terms for noise/grounding/surge relation.")
    return changed


def patch_pid(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "pid_control"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "PID 파라미터는 gain 또는 proportional band, integral time/reset, derivative time/rate로 표현되며 공정 gain, time constant, dead time에 따라 튜닝한다.",
            "Ziegler-Nichols, Cohen-Coon, IMC tuning 등은 초기값 산정에 활용할 수 있으나 현장에서는 valve stiction, noise, actuator saturation을 반영해 보정해야 한다.",
            "anti-reset windup, bumpless transfer, derivative filtering, setpoint weighting은 실제 DCS/PLC PID 구현에서 안정 운전에 중요하다.",
        ])
        changed += append_unique_list(entry, "high_score_features", [
            "proportional band, integral time, derivative time의 현장 parameter 의미를 설명한다.",
            "Ziegler-Nichols, IMC 등 tuning 방법과 현장 보정 필요성을 구분한다.",
            "anti-reset windup, bumpless transfer, derivative filtering을 포함한다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "proportional band", "integral time", "reset", "derivative time", "rate",
            "Ziegler-Nichols", "Cohen-Coon", "IMC tuning", "anti-reset windup",
            "bumpless transfer", "derivative filter", "setpoint weighting", "actuator saturation",
            "valve stiction", "dead time", "process gain", "time constant"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: strengthened PID tuning and implementation alignment.")

    topic = fact_topic(fact, tid)
    if topic:
        append_terms_to_best_matching_anchor(topic, ["P", "비례"], ["proportional band", "gain", "process gain"])
        append_terms_to_best_matching_anchor(topic, ["I", "적분"], ["integral time", "reset", "anti-reset windup"])
        append_terms_to_best_matching_anchor(topic, ["D", "미분"], ["derivative time", "rate", "derivative filter"])
        append_terms_to_best_matching_anchor(topic, ["튜닝", "tuning"], ["Ziegler-Nichols", "Cohen-Coon", "IMC tuning"])
        append_terms_to_best_matching_anchor(topic, ["현장", "구현", "적용"], ["bumpless transfer", "setpoint weighting", "actuator saturation", "valve stiction"])
        mark_revision_fact(topic, "deep_relation_cleanup: added PID implementation/tuning support terms.")
    return changed


def patch_pressure_dp(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "pressure_dp_transmitter"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "압력전송기 topic은 일반 압력이라는 넓은 개념보다 압력·차압 전송기의 센싱 원리, range 설정, 설치 오차, impulse line 조건에 초점을 둔다.",
            "static pressure effect, overpressure protection, diaphragm seal, capillary temperature effect는 현장 선정과 오차 평가의 핵심이다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "static pressure effect", "overpressure protection", "diaphragm seal", "capillary temperature effect",
            "zero elevation", "zero suppression", "wet leg", "dry leg", "remote seal"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: clarified pressure transmitter scope and field points.")

    topic = fact_topic(fact, tid)
    if topic:
        changed += replace_list_exact(
            topic,
            "triggers",
            {"압력", "pressure"},
            ["압력전송기", "차압전송기", "DP transmitter", "pressure transmitter", "remote seal", "impulse line"],
        )
        append_terms_to_best_matching_anchor(topic, ["설치", "배관", "impulse"], ["wet leg", "dry leg", "zero elevation", "zero suppression"])
        append_terms_to_best_matching_anchor(topic, ["오차", "영향"], ["static pressure effect", "capillary temperature effect"])
        append_terms_to_best_matching_anchor(topic, ["보호", "과압"], ["overpressure protection", "diaphragm seal"])
        mark_revision_fact(topic, "deep_relation_cleanup: removed overly broad trigger and added transmitter support terms.")
    return changed


def patch_smart_factory(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "smart_factory_iiot_digital_twin"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "IIoT 기반 지능화는 sensor, edge gateway, PLC/DCS, historian, MES/ERP, analytics, digital twin으로 이어지는 데이터 흐름의 신뢰성이 전제되어야 한다.",
            "digital twin은 단순 3D 모델이 아니라 설비·공정 데이터를 이용해 상태 추정, 이상 감지, what-if 분석, 예지보전에 활용되는 모델이다.",
            "성과 평가는 OEE, availability, performance, quality, MTBF, MTTR, downtime, energy intensity, alarm response time, ROI로 정량화한다.",
            "데이터 품질, time synchronization, sensor calibration, cybersecurity, model drift, 운영자 수용성, 기존 PLC/DCS 변경 리스크를 함께 평가해야 한다.",
        ])
        changed += append_unique_list(entry, "high_score_features", [
            "sensor-edge-PLC/DCS-historian-analytics의 데이터 흐름을 설명한다.",
            "digital twin을 상태 추정, 예지보전, what-if 분석과 연결한다.",
            "OEE, MTBF, MTTR, downtime, energy, ROI 등 정량 지표를 사용한다.",
            "cybersecurity, data governance, model drift, 기존 제어계 영향까지 평가한다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "sensor reliability", "edge gateway", "PLC/DCS integration", "historian",
            "MES", "ERP", "digital twin", "predictive maintenance", "OEE",
            "availability", "performance", "quality", "MTBF", "MTTR", "downtime",
            "energy intensity", "ROI", "time synchronization", "data governance",
            "cybersecurity", "model drift"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: strengthened smart factory/IIoT/digital twin relationship.")

    topic = fact_topic(fact, tid)
    if topic:
        append_terms_to_best_matching_anchor(topic, ["데이터", "IIoT"], ["edge gateway", "historian", "time synchronization", "data governance"])
        append_terms_to_best_matching_anchor(topic, ["디지털", "twin", "트윈"], ["digital twin", "model drift", "what-if analysis"])
        append_terms_to_best_matching_anchor(topic, ["평가", "효과", "성과"], ["OEE", "MTBF", "MTTR", "downtime", "ROI", "energy intensity"])
        append_terms_to_best_matching_anchor(topic, ["기존", "PLC", "DCS"], ["PLC/DCS integration", "cybersecurity", "change management"])
        mark_revision_fact(topic, "deep_relation_cleanup: added smart factory support terms matching model answer.")
    return changed


def patch_transfer_function_state_space(model: dict[str, Any], fact: dict[str, Any]) -> int:
    changed = 0
    tid = "transfer_function_state_space"

    for entry in model_entries(model, tid):
        changed += append_unique_list(entry, "model_answer_outline", [
            "전달함수는 영초기조건에서 입력과 출력의 라플라스 변환 비로 정의되며, pole-zero, Bode, Nyquist, root locus 해석에 유리하다.",
            "상태공간은 xdot = Ax + Bu, y = Cx + Du 형태로 내부 상태를 표현하고 MIMO, 상태피드백, observer 설계에 적합하다.",
            "전달함수의 극점은 상태행렬 A의 고유값과 대응되지만, 상태공간은 controllability, observability, minimal realization 평가가 가능하다.",
            "비선형 공정에는 운전점 주변 선형화가 필요하며, 모델의 유효 범위와 parameter uncertainty를 함께 고려해야 한다.",
        ])
        changed += append_unique_list(entry, "high_score_features", [
            "zero initial condition, Laplace transform, pole-zero, frequency response를 전달함수 특징으로 제시한다.",
            "state variable, A/B/C/D matrix, MIMO, controllability, observability를 상태공간 특징으로 제시한다.",
            "고전제어와 현대제어 적용 차이, 선형화 범위와 모델 불확실성을 언급한다.",
        ])
        changed += append_unique_list(entry, "field_connection_points", [
            "zero initial condition", "Laplace transform", "pole-zero", "Bode plot",
            "Nyquist", "root locus", "state variable", "A matrix", "B matrix",
            "C matrix", "D matrix", "MIMO", "state feedback", "observer",
            "controllability", "observability", "minimal realization", "linearization",
            "parameter uncertainty"
        ])
        mark_revision_model(entry, "deep_relation_cleanup: strengthened transfer-function/state-space alignment.")

    topic = fact_topic(fact, tid)
    if topic:
        append_terms_to_best_matching_anchor(topic, ["전달함수", "Laplace", "라플라스"], ["zero initial condition", "Laplace transform", "pole-zero"])
        append_terms_to_best_matching_anchor(topic, ["상태", "state"], ["state variable", "A matrix", "B matrix", "C matrix", "D matrix"])
        append_terms_to_best_matching_anchor(topic, ["극점", "고유값"], ["pole", "eigenvalue", "A matrix"])
        append_terms_to_best_matching_anchor(topic, ["제어", "관측"], ["controllability", "observability", "observer", "state feedback"])
        append_terms_to_best_matching_anchor(topic, ["MIMO", "현대"], ["MIMO", "minimal realization", "linearization"])
        mark_revision_fact(topic, "deep_relation_cleanup: added transfer/state-space support terms.")
    return changed


PATCHERS = [
    patch_industrial_communication,
    patch_noise_grounding,
    patch_pid,
    patch_pressure_dp,
    patch_smart_factory,
    patch_transfer_function_state_space,
]


def main() -> int:
    if not MODEL_PATH.exists() or not FACT_PATH.exists():
        print("ERROR: run from prof_eng_answer repo root.", file=sys.stderr)
        return 2

    print("backup model:", backup(MODEL_PATH))
    print("backup fact :", backup(FACT_PATH))

    model = load_model_answer_bank(MODEL_PATH)
    fact = load_fact_anchor_bank(FACT_PATH)

    total_changes = 0
    for patcher in PATCHERS:
        changed = patcher(model, fact)
        total_changes += changed
        print(f"{patcher.__name__}: changed={changed}")

    model_errors = validate_model_answer_bank(model, allowed_types=question_type_ids())
    fact_errors = validate_fact_anchor_bank_data(fact)

    if model_errors or fact_errors:
        print("\nINVALID before save")
        for err in model_errors:
            print("model:", err)
        for err in fact_errors:
            print("fact :", err)
        return 1

    save_model_answer_bank(model, MODEL_PATH)
    save_fact_anchor_bank(fact, FACT_PATH)

    print(f"\nSaved. total_changes={total_changes}")

    print("\n=== validate-all ===")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rubric_manager.py"), "validate-all"],
        cwd=ROOT,
        text=True,
    )

    print("\n=== run deep relationship audit again ===")
    audit_path = ROOT / "scripts/deep_model_fact_relationship_audit.py"
    if audit_path.exists():
        subprocess.run([sys.executable, str(audit_path)], cwd=ROOT, text=True)
    else:
        print("SKIP: scripts/deep_model_fact_relationship_audit.py not found")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
