#!/usr/bin/env python3
"""Read-only pending Fact sentence proposal vs canonical/generated audit.

Confirm 48 historical proposals and fail closed if an unreviewed candidate
replaces its canonical statement. Explicitly reviewed representation changes
are checked against their recorded wording and preserved scoring reference. Does not
regenerate banks, approve claims, or alter scoring.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grading.evidence.fact_anchor_compatibility import validate_sentence_compatibility

MANIFEST_REL = "calibration/fact_anchor_simplification_review_20261114.json"
GENERATED_REL = "rubrics/generated/fact_anchors.generated.json"

# A correction to the old canonical statement is not approval of the 48
# shortened candidates. Only this exactly documented Fact may differ from its
# historical previous_statement; unrelated source changes still fail closed.
PRECISION_CORRECTION_ID = (
    "speed_rotation_measurement_encoder_proximity_tachometer_selection_error",
    "encoder_frequency_limit_selection",
)
PRECISION_CORRECTION_REPORT = (
    "reports/pr38_encoder_frequency_canonical_precision_review_20261115.md"
)

# Exact review-approved *wording*, not just a collection of keywords. Any
# future edit requires a separate source review and test/manifest update.
PRECISION_CORRECTION_STATEMENT = "증분형 A/B 엔코더의 채널별 출력 주기수 PPR[cycle/rev]와 최고 회전속도 n_max[rpm]로 채널 주파수 f_ch=n_max·PPR/60[Hz]를 계산해 엔코더 최대 응답 주파수 및 수신기의 복호모드별 입력 주파수 한계와 비교한다. 수신기 내부의 x1/x2/x4 유효 계수율 f_count=n_max·N_eff/60[count/s]은 별도의 처리율 한계가 명시된 경우 그 사양과 비교하며, 고해상도일수록 같은 회전속도에서 주파수가 증가한다."

# Exact independently reviewed legacy wording is enabled below for the
# representation-only compatibility path. Other candidates remain pending.
REVIEWED_SENTENCE_ID = (
    "humidity_measurement_capacitive_resistive_dew_point_selection_compensation",
    "relative_humidity_definition",
)
REVIEWED_SENTENCE = "Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다."
REVIEWED_SENTENCE_REPORT = "reports/pr38_humidity_token_neutral_review_20261116.md"
REVIEWED_SENTENCES = {
    REVIEWED_SENTENCE_ID: REVIEWED_SENTENCE,
    (REVIEWED_SENTENCE_ID[0], "dew_point_definition"): "Dew point T_d는 현재 수증기 함량과 압력조건에서 기체를 냉각할 때 liquid water condensation이 시작되는 온도다.",
    (REVIEWED_SENTENCE_ID[0], "frost_point_distinction"): "0°C 이하의 매우 건조한 조건에서는 응축상이 ice인지 liquid water인지에 따라 frost point와 dew point를 구분할 수 있다.",
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "counting_window_speed_equation"): '고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다.',
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "gear_tooth_speed_equation"): '회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 n = 60f/Z이다.',
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "quadrature_direction_principle"): 'Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다.',
    ("speed_rotation_measurement_encoder_proximity_tachometer_selection_error", "tachogenerator_voltage_speed_principle"): 'Permanent-magnet DC tachogenerator는 회전에 의해 생성되는 DC voltage가 정상 동작범위에서 회전속도에 대체로 비례하도록 설계된 analog speed transducer다.',
    ('humidity_measurement_capacitive_resistive_dew_point_selection_compensation', 'absolute_humidity_definition'): 'Absolute humidity는 단위 체적당 수증기 질량 ρ_v = m_v/V로 정의할 수 있으며 이상기체 근사에서는 ρ_v = P_w/(R_v T)로 연결된다.',
    ('humidity_measurement_capacitive_resistive_dew_point_selection_compensation', 'pressure_dew_point_effect'): 'Dew point는 pressure condition의 영향을 받으므로 compressed gas에서는 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다.',
    ('humidity_measurement_capacitive_resistive_dew_point_selection_compensation', 'capacitive_polymer_principle'): 'Capacitive humidity sensor는 porous electrode 사이의 hygroscopic polymer dielectric이 수분을 흡수·방출하면 dielectric constant가 변하고 이에 따라 capacitance가 변하는 원리를 이용한다.',
    ('pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error', 'diaphragm_deflection_principle'): 'Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다.',
    ('pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error', 'diaphragm_sensor_vs_seal'): '압력을 직접 감지하는 diaphragm sensing element와 공정유체를 계기에서 격리하는 diaphragm seal은 목적이 다르다.',
    ('pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error', 'dp_transmitter_two_port_principle'): 'DP transmitter는 high-side와 low-side 두 입력의 압력차를 sensing element에 전달하여 차압을 전기신호로 변환한다.',
    ('speed_rotation_measurement_encoder_proximity_tachometer_selection_error', 'period_measurement_low_speed'): '저속에서는 연속 유효 pulse 사이의 시간 T_c를 측정하여 n = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다.',
    ('speed_rotation_measurement_encoder_proximity_tachometer_selection_error', 'inductive_proximity_principle'): 'Inductive proximity sensor는 sensing face의 교번 전자기장에 금속 target이 접근할 때 발생하는 eddy-current loss 또는 oscillator 변화로 target 존재를 검출한다.',
    ('speed_rotation_measurement_encoder_proximity_tachometer_selection_error', 'digital_tachometer_instrument_boundary'): 'Digital tachometer는 encoder·proximity·optical pickup 등의 pulse를 계수하거나 period를 측정해 RPM을 표시하는 instrument일 수 있다.',
    ('thermocouple_temperature_sensor_seebeck_reference_junction_compensation', 'thermocouple_law_of_intermediate_metals'): '열전대 회로에 제3의 금속이 삽입되더라도 그 금속과 열전대 재료 사이에 형성된 두 접점이 동일한 온도에 있으면 순 열기전력은 변하지 않는다.',
    ('thermocouple_temperature_sensor_seebeck_reference_junction_compensation', 'thermocouple_thermowell_installation_dynamic_error'): '보호관, 삽입길이, 유속, 배관 벽면과의 열전도, 복사, 접촉상태는 측정접점이 실제 공정 온도에 도달하는 과정에 영향을 준다.',
}

REVIEWED_ADDITIONAL_REPORTS = {'absolute_humidity_definition': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'pressure_dew_point_effect': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'capacitive_polymer_principle': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'diaphragm_deflection_principle': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'diaphragm_sensor_vs_seal': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'dp_transmitter_two_port_principle': 'reports/pr38_humidity_pressure_feedback_first_sentence_review_20261116.md', 'period_measurement_low_speed': 'reports/pr38_rotation_thermocouple_first_sentence_review_20261116.md', 'inductive_proximity_principle': 'reports/pr38_rotation_thermocouple_first_sentence_review_20261116.md', 'digital_tachometer_instrument_boundary': 'reports/pr38_rotation_thermocouple_first_sentence_review_20261116.md', 'thermocouple_law_of_intermediate_metals': 'reports/pr38_rotation_thermocouple_first_sentence_review_20261116.md', 'thermocouple_thermowell_installation_dynamic_error': 'reports/pr38_rotation_thermocouple_first_sentence_review_20261116.md'}


def _read(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected JSON object")
    return data


def audit_source_generated(root: Path = ROOT) -> dict[str, Any]:
    manifest = _read(root / MANIFEST_REL)
    if (manifest.get("schema_version") != "fact_anchor_simplification_review.v1"
            or manifest.get("score_effect") != "none"
            or manifest.get("application_status") != "CANDIDATE_ONLY_NOT_APPLIED"
            or manifest.get("applied_anchor_count") != 0
            or manifest.get("review_status") != "PENDING_TECHNICAL_REVIEW"
            or not isinstance(manifest.get("entries"), list)
            or len(manifest["entries"]) != manifest.get("changed_anchor_count")):
        raise ValueError("invalid Fact sentence review manifest")
    generated = _read(root / GENERATED_REL)
    topics = generated.get("topics")
    if not isinstance(topics, list):
        raise ValueError("generated Fact Bank topic list missing")
    bank_index: dict[str, dict[str, dict]] = {}
    for topic in topics:
        if not isinstance(topic, dict) or not isinstance(topic.get("anchors"), list):
            raise ValueError("invalid generated topic")
        tid = topic.get("topic_id")
        if not isinstance(tid, str) or tid in bank_index:
            raise ValueError("duplicate or invalid generated Topic")
        anchors = {}
        for anchor in topic["anchors"]:
            if not isinstance(anchor, dict):
                raise ValueError("invalid generated Fact Anchor")
            aid = anchor.get("anchor_id") or anchor.get("id")
            if not isinstance(aid, str) or aid in anchors:
                raise ValueError("duplicate or invalid generated Fact ID")
            anchors[aid] = anchor
        bank_index[tid] = anchors
    source_cache: dict[str, dict[str, dict]] = {}
    counts: Counter[str] = Counter()
    changed_topics: Counter[str] = Counter()
    precision_corrections = 0
    reviewed_sentences = 0
    seen: set[tuple[str, str]] = set()
    cases: list[dict[str, Any]] = []
    for item in manifest["entries"]:
        if not isinstance(item, dict):
            raise ValueError("invalid review entry")
        topic = item.get("topic_id")
        aid = item.get("anchor_id")
        previous = item.get("previous_statement")
        new = item.get("simplified_statement")
        if (not all(isinstance(x, str) and x for x in (topic, aid, previous, new))
                or item.get("review_status") != "PENDING_TECHNICAL_REVIEW"
                or (topic, aid) in seen):
            raise ValueError("invalid or repeated review identity")
        seen.add((topic, aid))
        canonical_statement = previous
        precision_corrected = False
        correction = item.get("canonical_precision_correction")
        if correction is not None:
            expected_metadata = {
                "review_report": PRECISION_CORRECTION_REPORT,
                "review_method": "ai",
                "application_scope": "CANONICAL_PRECISION_ONLY_NOT_SIMPLIFICATION",
                "release_status": "PENDING_VALIDATION",
                "score_effect": "none",
            }
            if ((topic, aid) != PRECISION_CORRECTION_ID
                    or not isinstance(correction, dict)
                    or set(correction) != set(expected_metadata) | {"statement"}
                    or any(correction.get(k) != v for k, v in expected_metadata.items())
                    or not isinstance(correction.get("statement"), str)
                    or correction["statement"] in (previous, new)):
                raise ValueError("unauthorized canonical precision correction")
            canonical_statement = correction["statement"]
            if canonical_statement != PRECISION_CORRECTION_STATEMENT:
                raise ValueError("canonical precision correction differs from reviewed wording")
            report = (root / PRECISION_CORRECTION_REPORT).read_text(encoding="utf-8")
            if previous not in report or canonical_statement not in report:
                raise ValueError("canonical precision correction evidence mismatch")
            precision_corrected = True
            precision_corrections += 1
        if topic not in source_cache:
            path = root / "rubrics/topic_packs" / topic / "fact_anchor.json"
            if path.resolve().parent.name != topic or "/" in topic or ".." in topic:
                raise ValueError("unsafe Topic ID")
            raw = _read(path)
            if raw.get("topic_id") != topic or not isinstance(raw.get("anchors"), list):
                raise ValueError("invalid source Topic ownership")
            d = {}
            for a in raw["anchors"]:
                key = a.get("anchor_id") or a.get("id")
                if not isinstance(key, str) or key in d:
                    raise ValueError("duplicate or invalid source Fact")
                d[key] = a
            source_cache[topic] = d
        source = source_cache[topic].get(aid)
        reviewed_sentence = False
        if (topic, aid) in REVIEWED_SENTENCES and isinstance(source, dict):
            reviewed_text = REVIEWED_SENTENCES[(topic, aid)]
            reference = validate_sentence_compatibility(source)
            report_path = REVIEWED_ADDITIONAL_REPORTS.get(aid) or (
                "reports/pr38_rotation_token_neutral_review_20261116.md"
                if topic == "speed_rotation_measurement_encoder_proximity_tachometer_selection_error"
                else REVIEWED_SENTENCE_REPORT)
            report = (root / report_path).read_text(encoding="utf-8")
            if (source.get("statement") != reviewed_text or reference != previous
                    or previous not in report or reviewed_text not in report
                    or "gpt-6-luna" not in report):
                raise ValueError("reviewed sentence compatibility mismatch")
            canonical_statement = reviewed_text
            reviewed_sentence = True
            reviewed_sentences += 1
        if (not isinstance(source, dict) or source.get("statement") != canonical_statement):
            raise ValueError("source text drifted from pending-review canonical snapshot")
        if precision_corrected:
            if (any(source.get(k) != canonical_statement
                    for k in ("claim", "description"))
                    or not source.get("accepted_explanations")
                    or source["accepted_explanations"][0] != canonical_statement):
                raise ValueError("canonical precision correction aliases out of sync")
        changed_topics[topic] += 1
        anchor = bank_index.get(topic, {}).get(aid)
        if anchor is None:
            state = "GENERATED_ANCHOR_MISSING"
        elif reviewed_sentence:
            if (anchor.get("statement") == canonical_statement
                    and anchor.get("expected") == previous
                    and anchor.get("sentence_compatibility") == source.get("sentence_compatibility")):
                state = "GENERATED_CANONICAL_WITH_PRESERVED_SCORING_REFERENCE"
            else:
                state = "GENERATED_WORDING_OTHER"
        else:
            generated_text = (
                anchor.get("expected") or anchor.get("fact")
                or anchor.get("statement") or anchor.get("description")
            )
            if generated_text == new:
                state = "GENERATED_WORDING_MATCHES_CANDIDATE"
            elif generated_text == canonical_statement:
                state = "GENERATED_WORDING_MATCHES_CANONICAL"
            elif precision_corrected and generated_text == previous:
                state = "GENERATED_WORDING_MATCHES_SUPERSEDED_CANONICAL"
            else:
                state = "GENERATED_WORDING_OTHER"
        counts[state] += 1
        cases.append({
            "topic_id": topic, "anchor_id": aid, "generated_wording_status": state,
            "canonical_wording_status": (
                "SOURCE_REVIEWED_SENTENCE_WITH_SCORING_REFERENCE" if reviewed_sentence
                else "SOURCE_REVIEWED_PRECISION_CORRECTION" if precision_corrected
                else "SOURCE_ORIGINAL_NOT_PROMOTED"
            ),
            "technical_equivalence_reviewed": False,
            "score_effect": "none",
        })
    return {
        "schema_version": "fact_anchor_sentence_sync_audit.v1",
        "status": "AUDIT_ONLY",
        "score_effect": "none",
        "score_admission": "DISABLED",
        "application_status": "PARTIALLY_APPLIED" if reviewed_sentences else "CANDIDATE_ONLY_NOT_APPLIED",
        "applied_anchor_count": reviewed_sentences,
        "canonical_wording_status": (
            "HAS_REVIEWED_PRECISION_CORRECTION" if precision_corrections
            else "SOURCE_ORIGINAL_NOT_PROMOTED"
        ),
        "precision_corrected_anchor_count": precision_corrections,
        "anchor_count": len(cases),
        "topic_count": len(changed_topics),
        "generated_wording_counts": dict(sorted(counts.items())),
        "cases": sorted(cases, key=lambda x: (x["topic_id"], x["anchor_id"])),
        "generated_wording_match_is_not_routing_equivalence": True,
        "technical_equivalence_reviewed": False,
        "safe_to_promote_automatically": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    result = audit_source_generated()
    if args.summary_only:
        result.pop("cases")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
