"""Pin source-reviewed Fact Anchor promotions to their current canonical text.

The allowlist is deliberately small: a KEEP_BOUNDED audit verdict alone does
not authorize general scoring. Add an ID only after checking its exact claim,
source-review caveat and general-scoring value.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "reports/fact_anchor_1290_latest_review_reconciliation_20261101.csv"
REGISTRY = ROOT / "grading/evidence/approved_fact_registry.json"
OUTPUT = ROOT / "reports/fact_anchor_keep_bounded_promotions_20261103.json"
SOURCE_HOLDS = ROOT / "grading/evidence/fact_anchor_unresolved_source_holds_20261101.json"
SECOND_BATCH_PENDING_SHA256 = "07f2d408bd66a3fe734181387b0b579777f1e8bff4b59704447473443a7377e2"
REPAIRED_PROMOTION_REVIEWS = {
    "lower_temperature_reduces_water_vapor_pressure_at_fixed_composition":
        "reports/fact_anchor_water_vapor_pressure_promotion_20261104.md",
    "sis_operational_maintenance_modification_records_and_review":
        "reports/topic_pack_stage8_moc_scope_review_20261112.md",
}
# These claims need a narrower canonical statement or are not general facts.
SECOND_BATCH_RETAINED_HOLDS = frozenset({
    "control_valve_vena_contracta_is_minimum_flow_area",
    "control_valve_guide_function_and_transverse_load_wear_relevance",
    "dp_level_radar_gwr_measurement_principle_comparison",
    "emerson_body_material_pressure_temperature_corrosion_erosion_tradeoff",
    "force_balance_null_position_error_detection",
    "pneumatic_force_balance_transmitter_chain",
    "srs_lifecycle_handoff_process_independently_verified",
    "temperature_sensor_thermal_resistance_model",
})

# Source-grounded, broadly applicable claims with an unchanged canonical text.
# Remaining KEEP_BOUNDED holds are intentionally not promoted by this batch.
PROMOTED_FACT_IDS = frozenset({
    "availability_readiness_and_time_fraction_measures",
    "bode_decibel_and_log_frequency_properties",
    "closed_seat_leakage_is_distinct_from_minimum_controllable_flow",
    "contact_temperature_error_controls_depend_on_immersion_gradients_and_use_conditions",
    "control_valve_cv_is_flow_capacity_not_travel_or_line_size",
    "diagnostic_coverage_and_proof_test_coverage_are_distinct_detection_mechanisms",
    "force_balance_pressure_area_equilibrium",
    "hazop_lopa_sif_allocation_boundary",
    "hazop_lopa_target_vs_achieved_sil",
    "proof_testing_targets_dangerous_failures_not_found_by_online_diagnostics",
})


def second_batch_fact_ids() -> frozenset[str]:
    holds = json.loads(SOURCE_HOLDS.read_text(encoding="utf-8"))["holds"]
    pending = frozenset(row["fact_id"] for row in holds
                        if row["reason"] == "reviewed_but_canonical_promotion_pending")
    if len(pending) != 102 or hashlib.sha256("\n".join(sorted(pending)).encode()).hexdigest() != SECOND_BATCH_PENDING_SHA256:
        # Once the hold manifest is reconciled, the first-batch ledger still
        # needs to be verifiable without reading the old 102-ID snapshot.
        recorded = json.loads(OUTPUT.read_text(encoding="utf-8"))
        pending = (frozenset(row["fact_id"] for row in recorded["entries"])
                   - PROMOTED_FACT_IDS - REPAIRED_PROMOTION_REVIEWS.keys())
        pending |= SECOND_BATCH_RETAINED_HOLDS | REPAIRED_PROMOTION_REVIEWS.keys()
    if len(pending) != 102 or hashlib.sha256("\n".join(sorted(pending)).encode()).hexdigest() != SECOND_BATCH_PENDING_SHA256:
        raise ValueError("Second-batch reviewed candidate set changed")
    return pending - SECOND_BATCH_RETAINED_HOLDS


def build() -> dict:
    with REVIEW.open(newline="", encoding="utf-8") as stream:
        review = {row["fact_id"]: row for row in csv.DictReader(stream)}
    registry = {
        row["fact_id"]: row
        for row in json.loads(REGISTRY.read_text(encoding="utf-8"))["facts"]
    }
    entries = []
    second_batch = second_batch_fact_ids()
    if len(second_batch) != 94 or PROMOTED_FACT_IDS & second_batch:
        raise ValueError("Unexpected second-batch promotion count or overlap")
    for fact_id in sorted(PROMOTED_FACT_IDS | second_batch):
        row = review[fact_id]
        fact = registry[fact_id]
        if row["latest_report_disposition"] != "KEEP_BOUNDED":
            raise ValueError(f"Not source-reviewed KEEP_BOUNDED: {fact_id}")
        if (fact["review_status"], fact["verification_status"]) != ("approved", "verified"):
            raise ValueError(f"Registry approval missing: {fact_id}")
        if (fact["topic_id"], fact["legacy_anchor_id"]) != (row["topic_id"], row["anchor_id"]):
            raise ValueError(f"Registry ownership mismatch: {fact_id}")
        refs = fact["verification_refs"]
        if not refs or any(not ref.get("locator") or
                           (not ref.get("url") and ref.get("authority_type") != "calculation")
                           for ref in refs):
            raise ValueError(f"Source locator missing: {fact_id}")
        source_path = ROOT / "rubrics/topic_packs" / row["topic_id"] / "fact_anchor.json"
        anchors = json.loads(source_path.read_text(encoding="utf-8"))["anchors"]
        anchor = next((item for item in anchors if item["anchor_id"] == row["anchor_id"]), None)
        if anchor is None:
            raise ValueError(f"Canonical Anchor missing: {fact_id}")
        statement = anchor["statement"]
        source_review = REPAIRED_PROMOTION_REVIEWS.get(fact_id, row["latest_review_source"])
        report_path = ROOT / source_review
        audit_line = next((line for line in report_path.read_text(encoding="utf-8").splitlines()
                           if line.startswith(f"| `{fact_id}` |")), None)
        if audit_line is None:
            raise ValueError(f"Individual source-review row missing: {fact_id}")
        audited_statement = audit_line.split(" | ")[1].strip()
        if fact_id == "bode_decibel_and_log_frequency_properties":
            # The Markdown table escaped the formula's absolute-value bars.
            audited_statement = audited_statement.replace("/L(jω)/", "|L(jω)|")
        if fact_id == "perpendicular_coriolis_force_instantaneous_rate_relation":
            audited_statement = (audited_statement
                                 .replace("2m/Ω//v(t)/", "2m|Ω||v(t)|")
                                 .replace("/v(t)/가", "|v(t)|가")
                                 .replace("/Ω/=/F_C(t)//(2m/v(t)/)", "|Ω|=|F_C(t)|/(2m|v(t)|)"))
        if " ".join(statement.split()) != " ".join(audited_statement.split()):
            raise ValueError(f"Source-reviewed and current claim differ: {fact_id}")
        if "`KEEP_BOUNDED`" not in audit_line:
            raise ValueError(f"Source-review verdict changed: {fact_id}")
        entries.append({
            "fact_id": fact_id,
            "topic_id": row["topic_id"],
            "anchor_id": row["anchor_id"],
            "statement_sha256": hashlib.sha256(statement.encode("utf-8")).hexdigest(),
            "topic_source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "source_review": source_review,
            "source_authorities": [ref["authority_id"] for ref in refs],
        })
    return {
        "version": "fact-anchor-canonical-promotion-v1",
        "promoted_on": "2026-11-04",
        "approval_basis": "103 previously reviewed claims remain pinned; one water-specific vapor-pressure claim was corrected, independently rechecked against IAPWS and the valve pressure-margin boundary, and user-directed for promotion on 2026-11-04. Eight second-batch claims remain held. No scoring weights, fatal rules, or previously promoted statements changed. Generated banks are maintained only through the managed builder.",
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = build()
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        OUTPUT.write_text(serialized, encoding="utf-8")
    elif OUTPUT.read_text(encoding="utf-8") != serialized:
        raise ValueError("Promotion ledger does not match current canonical sources")
    print(f"canonical_promotions={len(payload['entries'])} mode={'write' if args.write else 'check'}")


if __name__ == "__main__":
    main()
