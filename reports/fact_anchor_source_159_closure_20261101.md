# Fact Anchor original-source verification reconciliation — baseline 2629eb95 — 159 IDs

Date: 2026-11-01. Existing branch: `codex/essay-boundary-calibration-20261028`. Review author: GPT-6. This is an evidence-review reconciliation. **Do not interpret `KEEP_BOUNDED` as complete canonical approval, nor HOLD as claim falsehood.**

## Exact set audit

- Original baseline `2629eb95` 159 `independent_primary_source_check_pending` entries, not 150 approximately.
- Previously completed 14 manufacturing entries (13 KEEP, 1 source insufficient hold) on work branch before this review.
- Five independent claim-evidence reports added 145 new individual adjudications (39 + 36 + 20 + 27 + 23).
- Union of six reports = **159 distinct exact `fact_id` values**, overlaps = **zero**, ID coverage = **159/159**. The work branch's pre-existing pending manifest of 145 held records is entirely covered by the five reports; the manifest is **not** automatically revised by evidence reports.
- Ledger: [`fact_anchor_source_159_decision_ledger_20261101.csv`](fact_anchor_source_159_decision_ledger_20261101.csv) with `general_scoring_promotion=NOT_AUTHORIZED` and `release_gate=NOT_RUN` on every row.

## Technical adjudication of the 159 originally-pending IDs

- `KEEP_BOUNDED`: **125** (original claim principally supported only with explicitly defined conditions; requires canonical claim/score ownership reconciliation).
- `REVISE_REQUIRED`: **13** (claim part invalid, ambiguous, internally routed, or overly mandatory; revise and reverify before scoring).
- `HOLD_INSUFFICIENT_DIRECT_SOURCE_SCOPE`: **14** (individual source claim remains unverified, must not score).
- `SOURCE_CHECKED_SCOPED_STANDARD_HOLD`: **4** (some issuer or standard/edition scope identified; full exact normative clauses may remain unreviewed, so remains non-general mandatory scoring).
- `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD`: **3** (specific manufacturer model/application only, ineligible as universally mandatory fact).
- 159 sum exactly. The count of **not technically admitted as generic scoring references** here is not zero: holds/scoped/revision statuses are retained; KEEP is not operationally promoted.

## Key substantive corrections needed in canonical source

- `flashing_persists_when_outlet_pressure_below_vapor_pressure`: strict flashing downstream **P2 < Pv**, not current `P2 ≤ Pv`; transition/boundary state cannot be treated as guaranteed persistent two-phase flow.
- `simple_series_valve_authority_ratio_requires_fixed_boundary` and `valve_authority_is_defined_for_declared_operating_condition`: Valve Authority has manufacturer/model-dependent ratio definitions; identify numerator, denominator and design point before grading.
- `device_description_formats_support_ecosystem_specific_engineering_integration`: GSDML, EDD, EDS and ESI differ in what each file can express; do not mandate menus, diagnostics and methods for all formats.
- `feedback_field_design_and_validation_checklist`: replace blanket every-plant requirement with scope-appropriate engineering verification items.
- `force_balance_transmitter_tradeoffs_are_architecture_dependent`: electrical power burden not universal for pneumatic force balance; insufficient original evidence.
- Vendor-specific Fisher calibration and FIELDVUE diagnostic tiers must remain product-scoped, not general technical-exam mandatory scoring.

## What is NOT concluded

- No claim that all 159 are scientifically correct, that the older 1,290 Fact Queue or the 1,520 approved Registry records have each been re-certified in this pass.
- No auto-promotion of the current legacy `verified` Registry flag. No source-hash approval, score rules, Topic Pack canonical changes, generated banks, exclusion manifest, test baselines or release-gate state changed by this report.
- No `pytest`, `rubric_manager.py validate-all`, full `validate_release.sh`, and no full release gate run. Existing branch-only GitHub report commits cannot execute the local checks. Treat deployment / merge as blocked.

## Report index
- [39 new source comparisons](../reports/fact_anchor_independent_review_control_valve_39_20261101.md)
- [36 new source comparisons](../reports/fact_anchor_independent_review_other_36_20261101.md)
- [20 new source comparisons](../reports/fact_anchor_independent_review_safety_20_20261101.md)
- [27 new source comparisons](../reports/fact_anchor_independent_review_remaining_27_20261101.md)
- [23 new source comparisons](../reports/fact_anchor_independent_review_remaining_23_20261101.md)
- [Manufacturing prior 14](../reports/fact_anchor_independent_review_manufacturing_20261101_v2.md)

## Required before scoring promotion

Use exact claim-to-evidence statements and affected source revision to correct or narrow canonical Topic Packs, then reconcile the independent source audit CSV and temporary runtime holds atomically, regenerate managed views using repository CLI and run regression/validation/release gates. Do not manipulate generated banks manually or weaken A/B/C/D/E authority and fatal rules.
