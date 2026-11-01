# Independent primary-source review — 35 OT security, lifecycle and acceptance claims

2026-11-01. Reviewer GPT-6. Exact original 35 Fact IDs in four canonical Topic Pack `fact_anchor.json` sources, prior status PENDING in 1,290-unique-ID source audit. **31 KEEP_BOUNDED; 3 REVISE_REQUIRED; 1 SOURCE_CHECKED_VENDOR_APPLICATION_HOLD.** Oracle ZDM exact documented condition is manufacturer/version specific and held from general technical scoring. NIST Rev.3 specifically, not the 2026 Rev.4 public draft. Statements compared individually; this is not managed pack hash approval.

## First-party original sources and access restrictions
- **NIST SP 800-82 Rev3**: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf — Issuer original official full PDF §6.1.1, §6.2.1, §6.2.4, §6.3–6.5, App.E.2.3/5, App.F CM-3 & PL-11; screenshot PDF index124 visually inspected. Rev4 remains only initial public draft as of 2026-11-01.
- **NIST IR8179**: https://csrc.nist.gov/pubs/ir/8179/final — Issuer original publicly accessible abstract, not all printed report pages.
- **IEC 62402:2019**: https://webstore.iec.ch/en/publication/59531 — Issuer catalogue publicly describes lifecycle obsolescence policy, planning, avoidance and resolution; paid normative clauses NOT accessed.
- **ISO 10007:2017**: https://committee.iso.org/sites/tc176/home/projects/published/iso-10007-2017.html — Public TC176 committee summary, carries explicit third-party maintenance disclaimer; no paid normative clauses accessed.
- **Oracle ZDM21.2**: https://docs.oracle.com/en/database/oracle/zero-downtime-migration/21.2/zdmug/introduction-to-zero-downtime-migration.html — Original 'Physical Online Migration' lines60–67, explicit SQL*Net/redo/manual role reversal and source-side TDE caveat.
- **NASA SWE-066**: https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604537/SWE-066%2B-%2BPerform%2BTesting — Original NASA handbook §1.1 testing levels (NASA obligations not generic PLC mandates).
- **NASA STP**: https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604427/STP%2B-%2BSoftware%2BTest%2BPlan — Original publisher §1 test plans, unit/integration/requirements verification matrix; recommended NASA document not universal artifact list.
- **ISA ISA-105**: https://www.isa.org/standards-and-publications/isa-standards/isa-105-standards — Original public issuer summary ANSI/ISA‑62381‑2026 adoption IEC62381:2024, IEC62382:2024 loop check; detailed paid clauses not accessed.

## Exact claim-by-claim adjudication

### configuration_change_release_backup_rollback_migration_obsolescence_management (13 statements)

| Exact Fact ID | Verdict | Original-source locator | Engineering claim-to-source interpretation and limitation |
|---|---|---|---|
| `nist_sp80082_ot_inventory_for_migration_discovery` | `KEEP_BOUNDED` | NIST SP800-82r3 §6.1.1 pp.90–92 | Inventory vendor/model/location/version and connectivity is supported; license/spare and custom control logic are site-specific additions. |
| `obsolescence_management_is_lifecycle_process` | `KEEP_BOUNDED` | IEC 62402:2019 publisher summary | Managing obsolescence starts during design and continues over the life cycle, not just procurement after discontinuation. |
| `oracle_zdm_post_switchover_fallback_condition_example` | `SOURCE_CHECKED_VENDOR_APPLICATION_HOLD` | Oracle ZDM21.2 §Physical Online Migration | Original explicitly conditions fallback on ongoing redo synchronization and manual action; also TDE/encrypted redo limitation. Proprietary mechanism, not generic industrial scoring. |
| `ot_backup_restore_scope_includes_recovery_dependencies` | `KEEP_BOUNDED` | NIST SP800-82r3 §6.2.4.3; App.E.2.5 | Backup must be recoverable with needed dependencies/tools; product/version lists vary. |
| `restore_testing_and_recovery_evidence` | `KEEP_BOUNDED` | NIST §6.2.4.3–5, §6.5 | Backup and response/recovery plans should be tested; record outcomes and gaps. Interval is determined by risk. |
| `sw06_configuration_identification_tracks_ci_attributes_and_relationships` | `KEEP_BOUNDED` | ISO 10007:2017 issuer committee public overview; NIST §6.1.1 | Identification/status and relationships matter, but the exact columns are local implementation. |
| `sw06_legacy_system_risk_based_management` | `KEEP_BOUNDED` | NIST §1.1 and §6.1.1; IEC62402 | Risk, availability and obsolescence inform maintain/replace/segregate tradeoffs; not a universal replace schedule. |
| `sw06_ot_backup_scope_is_asset_and_recovery_objective_specific` | `KEEP_BOUNDED` | NIST §6.2.4.3 and App.E.2.5 | Recoverable OT contents can include logic, firmware, VM, documents and licenses when applicable, not mandatory all every device. |
| `sw06_restore_and_rollback_are_distinct_recovery_concepts` | `KEEP_BOUNDED` | NIST §6.2.4.3–5; Oracle ZDM §Physical Online Migration | Restore is copy/data return; rollback reverses a change and may require coordinated cutover. Methods overlap but not synonymous. |
| `version_control_is_not_complete_configuration_management` | `KEEP_BOUNDED` | ISO10007 public overview | Version tracking alone does not establish approved baseline, configuration control and status audit. |
| `backup_integrity_separation_and_retention_controls` | `KEEP_BOUNDED` | NIST App.E.2.5, §6.2.4.3 | Backup protection, integrity and geographically/operationally appropriate separation are risk-based; not a fixed retention/copy count. |
| `configuration_baseline_is_approved_point_in_time_reference` | `KEEP_BOUNDED` | NIST §6.2.4.2; ISO 10007 | Approved configuration reference, not simply latest source revision or last backup. |
| `disaster_recovery_objectives_and_resources` | `KEEP_BOUNDED` | NIST §6.2.4.5, §6.5 | Recovery objectives consider acceptable service interruption and lost data, staffing and continuity. Numeric limits are site dependent. |

### ot_cybersecurity_defense_in_depth_allowlisting_supply_chain_incident_response (12 statements)

| Exact Fact ID | Verdict | Original-source locator | Engineering claim-to-source interpretation and limitation |
|---|---|---|---|
| `nist_80082r3_ot_baseline_configuration_and_predeployment_change_testing` | `KEEP_BOUNDED` | NIST SP800-82r3 §6.2.4.2 pp.111–112 | NIST advises baseline recording and documented, approved, tested changes; avoid disabling vital services without impact test. |
| `nist_80082r3_ot_compensating_controls_risk_documentation` | `KEEP_BOUNDED` | NIST SP800-82r3 App.F PL-11 pp.230+ | NIST requires documented alternative protection, rationale and residual risk, not assurance every substitute is equivalent in efficacy. |
| `nist_80082r3_ot_configuration_management_aligned_with_moc` | `KEEP_BOUNDED` | NIST App.F CM-3 p.244; §6.2.4.2 | Original explicitly calls for alignment with organization's Management of Change and predeployment authorization. |
| `nist_80082r3_ot_detection_process_and_network_baseline` | `KEEP_BOUNDED` | NIST §6.3 pp.128–132 | Anomaly detection and alerting benefit from traffic baselines and interpretation; no fixed alarm tooling required. |
| `nist_80082r3_ot_identity_management_credentials_and_lifecycle` | `KEEP_BOUNDED` | NIST §6.2.1 p.96, App.F IA | Manage identity and credentials for users, devices and services by authorized access; no mandatory IAM product. |
| `nist_80082r3_ot_ids_ips_monitoring_and_sensor_tuning` | `KEEP_BOUNDED` | NIST §6.3.1–2 pp.129–131 | IDS/IPS and behavioral tools support monitoring and require tuning and OT performance checks; are optional/case-specific. |
| `nist_80082r3_ot_incident_containment_with_process_risk_assessment` | `KEEP_BOUNDED` | NIST §6.4 and §6.2.4.5 | Containment/eradication/recovery must account for unsafe consequences of disconnection or shutdown. |
| `nist_80082r3_ot_mfa_remote_access_with_environmental_constraints` | `KEEP_BOUNDED` | NIST §6.2.1 p.102 | MFA is accepted best practice for remote OT; assess device capability and compensating controls for placement. |
| `nist_80082r3_ot_safety_system_separation_risk_and_control_impact` | `KEEP_BOUNDED` | NIST §2.3.7 p.25, §4.2.2 p.55 | Traditional separated SIS and integrated control/safety exist; adequate separation and security impact depend on risk. |
| `nist_80082r3_ot_security_requirements_prioritize_availability_safety_context` | `KEEP_BOUNDED` | NIST §1 OT risk and CIA | Availability/reliability/safety are often critical OT concerns, without declaring confidentiality never matters. |
| `nist_80082r3_ot_vulnerability_scanning_with_impact_controls` | `KEEP_BOUNDED` | NIST §6.3.2 and App.E.2.3 | Passive/active scanning must avoid impact to fragile live OT devices; offline rehearsal, maintenance windows. |
| `nist_ir8179_criticality_prioritizes_by_goal_importance_and_loss_impact` | `KEEP_BOUNDED` | NISTIR 8179 issuer abstract | Criticality uses mission/organizational goals and impact of loss or improper operation; not a universal numeric rank. |

### instrumentation_control_software_lifecycle_v_model_traceability_verification_validation (7 statements)

| Exact Fact ID | Verdict | Original-source locator | Engineering claim-to-source interpretation and limitation |
|---|---|---|---|
| `sw04_verification_and_validation_are_distinct_complementary_activities` | `KEEP_BOUNDED` | NASA SWE-066; STP | Verification vs defined specifications and validation vs intended needs are distinct questions. |
| `sw04_integration_test_verifies_software_interfaces` | `KEEP_BOUNDED` | NASA SWE-066; STP §Test levels | Integration tests module/communication interfaces; selected timing/failure-path criteria depend on contract. |
| `sw04_requirements_traceability_matrix_links_requirements_design_and_tests_bidirectionally` | `REVISE_REQUIRED` | NASA STP §1 #10; SWE-066 | Bidirectional requirements-test traceability warranted, but insisting one RTM include every Design/Code/Test/Result stage is not universal. |
| `sw04_unit_test_verifies_isolated_software_units` | `KEEP_BOUNDED` | NASA STP §1 #2; SWE-066 | Unit testing evaluates function/module under isolated or controlled dependencies; not all possible boundary cases universally mandatory. |
| `sw04_validation_definition_checks_intended_use_and_user_needs` | `KEEP_BOUNDED` | NASA SWE-066 | Validation evaluates intended use/user needs and practical operating environment. |
| `sw04_verification_definition_checks_work_product_conformance` | `KEEP_BOUNDED` | NASA SWE-066; NASA verification planning | Verification compares work product with its input/specified requirements. |
| `v_model_design_test_mapping` | `KEEP_BOUNDED` | NASA SWE-066; STP | Model maps lifecycle artifacts to corresponding verification activities; chosen process not universal and does not prove SIL. |

### control_software_project_engineering_documents_fat_sat_commissioning_acceptance (3 statements)

| Exact Fact ID | Verdict | Original-source locator | Engineering claim-to-source interpretation and limitation |
|---|---|---|---|
| `commissioning_uses_site_procedures_to_verify_installed_function` | `REVISE_REQUIRED` | ISA ISA‑105/IEC62381/62382 publisher summary | Canonical fixed ordering puts Energization before static inspection; pre-energization safety/readiness checks are indispensable. FAT/SAT/loop check and commissioning distinct. |
| `fat_checks_approved_automation_baseline_at_supplier_site` | `REVISE_REQUIRED` | ISA‑105 official IEC62381:2024 summary | Supplier FAT verifies agreed project-specific requirements, not every project necessarily has HMI/alarm/communication/recovery requirements. |
| `sat_checks_installed_site_interfaces_and_conditions` | `KEEP_BOUNDED` | ISA‑105 official IEC62381:2024 summary | SAT verifies installed equipment/site interfaces; multi-subsystem full integration is separately SIT. |

## Corrective actions required before Source Pack approval

- `commissioning_uses_site_procedures_to_verify_installed_function`: Current forced *energize then static checks* reading is unsafe as a universal sequence. Require suitable de-energized mechanical/electrical inspections, approved permissions, then staged energization and process testing, adapted to actual system and local rules.
- `fat_checks_approved_automation_baseline_at_supplier_site`: Restrict test checklist to agreed project requirements. Do not always demand HMI, alarm, interlock, communications and recovery on systems without them.
- `sw04_requirements_traceability_matrix_links_requirements_design_and_tests_bidirectionally`: Reword bidirectional traceability to applicable requirements↔verification evidence; other links may be separate managed artefacts rather than mandatory one RTM.
- `oracle_zdm_post_switchover_fallback_condition_example`: Vendor-specific fallback is not general OT rollback fact; preserve independent vendor hold. Oracle original additionally documents redo encryption/TDE constraint, so link health alone does not assure fallback.

**After reconciliation** ledger total 1290: 182 PENDING, 714 KEEP_BOUNDED, 67 REVISE_REQUIRED, 36 insufficient direct evidence holds, 7 standard-scoped, 8 vendor-scoped, 275 general-scoring excluded, 1 legacy scoped-only. Executable unresolved-source holds 233; independent revision holds 67. Original 276 screening exclusions unchanged. Original canonical Registry and Topic Packs/generation views not modified, no release gate PASS claimed, draft PR17 remains unmerged.
