# Spare-parts and KPI anchor evidence review — 2026-10-11

Topic: `control_system_operations_maintenance_calibration_inspection_spares_kpi`

## Disposition

The Topic has 26 canonical anchors. At the time of the initial review, twenty-one
had verified Fact registry mappings and five remained unresolved. After narrowing
and independently verifying `spares_criticality_classification` and
`spares_stock_policy_reorder_leadtime`, narrowing
`spares_preservation_shelf_life_rotation` to the directly supported NASA limited-
shelf-life lesson, and narrowing `spares_obsolescence_substitution_moc` to
vendor-specific lifecycle examples plus NIST OT change-control guidance, the
current count is 25 verified / 1 unresolved.
New/updated Facts have `score_effect=none`; generated artifacts must be rebuilt
through the rubric CLI after source-pack edits.

## Per-anchor findings

| Anchor | Finding | Evidence / unresolved scope |
|---|---|---|
| `spares_criticality_classification` | Verified after narrowing | Critical Spare is framed as asset-specific restoration-risk judgment: critical asset restoration need, failure consequences, redundancy/alternatives, procurement/repair lead time. NASA NPR 8831.2D Appendix G and NPR 8831.2E Chapter 7 support example risk factors; DOE OIG-24-30 supports critical-spare role and procurement lead-time context. The Pack explicitly disclaims a universal classification algorithm and treats frequency/cost alone as insufficient by themselves. |
| `spares_stock_policy_reorder_leadtime` | Verified after narrowing | GAO-09-103 pp. 7–8 documents a Navy inventory example: reorder-point requirements include operating and acquisition lead-time demand, safety level and repair-cycle stock; economic order quantity balances ordering and holding costs. DOE OIG-24-30 pp. 1–2 supports documenting critical-spare levels and locally based reorder points in the WAPA context. The Pack now disclaims universal plant formulas, MOQ, commonality and mandatory min/max methods. |
| `spares_preservation_shelf_life_rotation` | Verified after narrowing | NASA LLIS Lesson 724 directly says to identify limited-shelf-life spares, acquire them periodically, and remove/replace expired spares in its space-system context. The Pack no longer claims humidity/dust controls, periodic functional tests, firmware/license checks or FIFO/rotation as universal requirements. |
| `spares_obsolescence_substitution_moc` | Verified after narrowing | NI's hardware lifecycle policy distinguishes its own Mature/LTB/support/discontinued phases and product-specific replacement/repair-support availability. NIST SP 800-82 Rev. 3 §6.2.4.2 recommends approved OT baselines and documented, tested, approved changes before deployment. The Pack does not generalize NI phases to other vendors or claim a universal compatibility checklist or substitution sequence. |
| `kpi_gaming_single_metric_tradeoff` | Not verified as written | SMRP and DOE FEMP sources support defined KPI formulas and contextual metric boundaries, but do not substantiate this anchor's specific causal examples (under-reporting failures, premature work-order closeout, excessive PM) as general outcomes of single-KPI optimization. A 2025 industry-conference paper discusses work-order KPI manipulation but is insufficient to verify the broad causal bundle on its own. |

## Sources checked

- [NASA NPR 5900.1, Spare Parts Acquisition](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_5900_0001_&page_name=ALL), especially §§1.2, 2.3, 3.1.
- [DOE OIG-24-30, WAPA critical spares audit](https://www.energy.gov/ig/articles/audit-doe-oig-24-30).
- [GAO-09-103, Defense Inventory: Management Actions Needed to Improve the Cost Efficiency of the Navy's Spare Parts Inventory](https://www.gao.gov/assets/gao-09-103.pdf), pp. 7–8.
- [NASA Lessons Learned Information System, Lesson 724, Spares with Limited Shelf Life](https://llis.nasa.gov/lesson/724).
- [DoD PSM Workshop 2025, consolidated briefs](https://www.acq.osd.mil/asds/ps/docs/psm/PSM_WS_2025_Day3_Consolidated_Briefs.pdf); workshop material, not a universal regulation.
- [NIST SP 800-82 Rev. 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf), OT configuration change-control safeguards.
- [SMRP Best Practices Metrics MicroLearning](https://training.smrp.org/metrics-microlearning) and [DOE FEMP O&M Best Practices Guide](https://www.energy.gov/sites/default/files/2020/04/f74/omguide_complete_w-eo-disclaimer.pdf); these support metric definitions/formulas, not the claimed gaming examples.

These anchors should be narrowed or supported by additional evidence before being
promoted to verified status. This note is an audit disposition only and does not
change grading behavior.
