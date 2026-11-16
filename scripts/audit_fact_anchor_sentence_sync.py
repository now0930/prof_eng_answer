#!/usr/bin/env python3
"""Read-only pending Fact sentence proposal vs canonical/generated audit.

Pending simplifications remain outside canonical source and generated banks.
Separately reviewed wordings are explicitly pinned; all other changes
fail closed. This audit does not regenerate banks or grant scoring authority.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
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

# Each source-grounded AI review authorizes only its exact listed candidate.
REVIEWED_SIMPLIFICATION_ID = (
    "humidity_measurement_capacitive_resistive_dew_point_selection_compensation",
    "relative_humidity_definition",
)
REVIEWED_SIMPLIFICATION_STATEMENT = "상대습도 RH[%]는 같은 온도의 실제 수증기 분압 P_w와 포화수증기압 P_ws(T)의 비율로, RH=100·P_w/P_ws(T)이다."
REVIEWED_SIMPLIFICATION_REPORT = "reports/pr38_relative_humidity_sentence_review_20261116.md"
THERMOCOUPLE_TOPIC = "thermocouple_temperature_sensor_seebeck_reference_junction_compensation"
REVIEWED_SIMPLIFICATIONS = {
    REVIEWED_SIMPLIFICATION_ID: (REVIEWED_SIMPLIFICATION_STATEMENT, REVIEWED_SIMPLIFICATION_REPORT),
    (THERMOCOUPLE_TOPIC, "thermocouple_measures_temperature_difference"): (
        "열전대의 기전력은 측정접점뿐 아니라 기준접점 온도에도 의존하므로 측정접점의 절대온도 환산에는 기준접점 온도 정보가 필요하다.",
        "reports/pr38_thermocouple_sentence_review_20261116.md",
    ),
    (THERMOCOUPLE_TOPIC, "thermocouple_nonlinearity_reference_tables_polynomial_conversion"): (
        "열전대의 비선형 열기전력은 열전대 형식별 표준 열기전력표나 다항식의 유효 온도범위·단위에 맞춰 온도로 환산해야 한다.",
        "reports/pr38_thermocouple_sentence_review_20261116.md",
    ),
}


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
    reviewed_simplifications = 0
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
        simplification_reviewed = False
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
        reviewed = REVIEWED_SIMPLIFICATIONS.get((topic, aid))
        if reviewed and isinstance(source, dict) and source.get("statement") == new:
            reviewed_statement, reviewed_report = reviewed
            if new != reviewed_statement:
                raise ValueError("reviewed simplification differs from approved wording")
            report = (root / reviewed_report).read_text(encoding="utf-8")
            if previous not in report or new not in report or "gpt-6-luna" not in report:
                raise ValueError("reviewed simplification evidence mismatch")
            if (any(k in source and source[k] != new for k in ("claim", "description"))
                    or previous not in source.get("accepted_explanations", [])):
                raise ValueError("reviewed simplification aliases or original out of sync")
            canonical_statement = new
            simplification_reviewed = True
            reviewed_simplifications += 1
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
        else:
            generated_text = (
                anchor.get("expected") or anchor.get("fact")
                or anchor.get("statement") or anchor.get("description")
            )
            if generated_text == canonical_statement:
                state = "GENERATED_WORDING_MATCHES_CANONICAL"
            elif generated_text == new:
                state = "GENERATED_WORDING_MATCHES_CANDIDATE"
            elif (precision_corrected or simplification_reviewed) and generated_text == previous:
                state = "GENERATED_WORDING_MATCHES_SUPERSEDED_CANONICAL"
            else:
                state = "GENERATED_WORDING_OTHER"
        counts[state] += 1
        cases.append({
            "topic_id": topic, "anchor_id": aid, "generated_wording_status": state,
            "canonical_wording_status": (
                "SOURCE_REVIEWED_SIMPLIFICATION" if simplification_reviewed
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
        "application_status": "PARTIALLY_APPLIED" if reviewed_simplifications else "CANDIDATE_ONLY_NOT_APPLIED",
        "applied_anchor_count": reviewed_simplifications,
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
