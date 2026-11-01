# IEC 60534-1 independent review — four anchors (2026-11-01)

Scope: independent comparison of four general engineering claims against accessible excerpts of IEC 60534-1:2023 (public standards preview). Status KEEP_BOUNDED explicitly restricts use to stated applicability and does not certify every sentence of a Topic Pack.

Primary excerpts:
- https://www.iteh.asia/catalog/standards/iec/7183ed93-2abc-4103-8bf4-054d6336808a/iec-60534-1-2023 — sections 3.3.11 to 3.3.13, definitions of installed characteristic, inherent and installed rangeability.
- https://www.iteh.eu/catalog/standards/iec/7183ed93-2abc-4103-8bf4-054d6336808a/iec-60534-1-2023 — clauses 3.3.7 and 3.3.11–3.3.13 (search-indexed preview).
- https://cdn.standards.iteh.ai/samples/21845/21743842f00d430f9d16513ab3301d37/IEC-60534-1-2023.pdf — preview, flow coefficient expressions and caveat: turbulent liquid flow, no cavitation/flashing, same nominal pipe/valve size for the simplified equation.

| fact_id | verdict | strict scope |
|---|---|---|
| inherent_rangeability_is_controllable_cv_ratio_under_stated_tolerance | KEEP_BOUNDED | Ratio of largest to smallest flow coefficients within specified deviation. Distinguish from installed flow ratio. |
| installed_rangeability_depends_on_installed_controllability_limits | KEEP_BOUNDED | Based on actual maximum/minimum flow in operating conditions where installed-characteristic slope remains within user-specified limits. |
| control_valve_liquid_flow_depends_on_cv_dp_and_specific_gravity | KEEP_BOUNDED | Simplified proportional relationship Q ∝ Cv sqrt(Δp/SG) only for units and liquid non-cavitating/non-flashing turbulent service where assumptions hold; not a universal phase-change or choked-flow equation. |
| control_valve_required_and_rated_coefficients_are_distinct | KEEP_BOUNDED | Required coefficient determined for specified process cases must be differentiated from manufacturer's rated capacity at rated travel and conditions (IEC 60534-1 clauses 3.3.7 and flow-coefficient definitions). |

**Limitations:** excerpts of the standard preview, not licensed access to every full IEC clause or inspection of the exact original Topic Pack sentences. No further pending items are marked independently checked in this batch.
