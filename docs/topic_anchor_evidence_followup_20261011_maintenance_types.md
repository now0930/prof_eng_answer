# Maintenance-type terminology anchor review — 2026-10-11

## Disposition

Topic: `control_system_operations_maintenance_calibration_inspection_spares_kpi`  
Anchor: `maintenance_strategy_corrective_preventive_condition_predictive`  
Fact: `maintenance_types_distinguish_corrective_preventive_condition_based_and_predictive`  
Status: verified/approved; `score_effect=none`.

The original anchor incorrectly reduced preventive maintenance to time/usage
intervals, equated predictive maintenance with using a data model, and implied the
definitions themselves prescribe a strategy mix by asset risk. It has been
corrected to the standard's terminology and explicitly says that asset-specific
strategy selection and intervals are not determined by these definitions.

## Evidence and limits

ISO 14224:2016 §3.8 defines corrective maintenance as restoration after fault
detection; §3.78 defines preventive maintenance by its aim to limit degradation
and reduce failure probability; §3.7 defines condition-based maintenance as
preventive maintenance based on physical-condition assessment; §3.77 defines
predictive maintenance as future-state forecasting estimated/calculated from
defined historical data and known future operating parameters. ISO's catalogue
states the standard applies to petroleum, natural gas and petrochemical industries
and that the 2016 edition remains current. [ISO 14224:2016](https://www.iso.org/standard/64076.html)

This evidence verifies the terminology and relationship only. It does not establish
that every plant should use a particular mix of corrective, preventive, CBM, or
predictive tasks, nor does it set inspection or replacement intervals.

## Registry

The Fact is recorded in `grading/evidence/approved_fact_registry.json` with no
WordPress source dependency and no runtime scoring effect.

## Additional verified anchor: maintenance-plan definition

The related `maintenance_plan_task_interval_basis` anchor was narrowed to the
standard definition: a structured and documented set of maintenance tasks,
activities, procedures, resources, and duration. The long asset-specific list of
interval-selection inputs and work controls was removed from the asserted Fact;
those details remain site/regulatory decisions unless separately substantiated.
ISO 14224:2016 §3.54 supports this bounded definition. The Fact has no WordPress
source dependency and no runtime scoring effect.

## Additional verified anchor: OSHA-scoped maintenance work controls

`maintenance_roles_competence_permit_restoration` was too broad: its earlier
wording combined several departments, generic work permits, LOTO, SIS bypass,
functional testing, and restoration approval as if universally mandatory. It is
now limited to what OSHA directly states. Under 29 CFR 1910.147, a covered
hazardous-energy control program includes procedures, training, and periodic
inspections; authorized employees verify isolation before work, and release
checks equipment integrity and employee safety before affected employees are
notified prior to restart. For PSM-covered processes, 29 CFR 1910.119 separately
requires applicable safe-work practices, task-relevant training, and contractor
controls. These U.S. requirements do not establish one universal work-permit,
SIS-bypass-approval, or functional-test checklist for all plants. The Fact has
no WordPress dependency and `score_effect=none`.
[OSHA 29 CFR 1910.147](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147),
[OSHA 29 CFR 1910.119](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119).

## Additional verified anchor: PSM mechanical-integrity deficiency correction

`inspection_findings_defect_priority_closeout` originally bundled a generic
priority model, immediate/temporary measures, work-order handling, and retesting.
OSHA 29 CFR 1910.119(j) supports a narrower rule for mechanical-integrity
equipment in covered processes: inspections/tests use recognized and generally
accepted good engineering practices and are documented; a deficiency outside
acceptable limits defined by process safety information is corrected before
further use, or safely and timely while necessary measures assure safe operation.
It does not prescribe a universal risk-priority formula, work-order format, or
retest sequence across industries. The Fact has no WordPress dependency and
`score_effect=none`.
[OSHA 29 CFR 1910.119(j)(1)–(5)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119).

## Additional verified anchor: ISO 14224 failure-data scope

`failure_coding_rca_bad_actor_feedback` previously implied that one failure-code,
Bad Actor, RCA, and improvement-feedback workflow was universally prescribed.
ISO 14224:2016's official catalogue supports standardized reliability and
maintenance-data exchange for petroleum, natural-gas, and petrochemical
industries; failure data include cause and consequence, and the standard's
failure modes can be used as a reliability thesaurus for quantitative or
qualitative applications. The catalogue also explicitly excludes methods for
analyzing and applying RM data. The anchor therefore does not claim that ISO
sets site-wide Bad Actor thresholds, RCA triggers, or a corrective-action loop;
those remain organization/program-specific. The Fact has no WordPress dependency
and `score_effect=none`.
[ISO 14224:2016 official scope and abstract](https://www.iso.org/standard/64076.html).

## Additional verified anchor: offshore SIS maintenance deferral

`deferred_maintenance_risk_control` was overgeneralized as a universal
requirement for every deferred maintenance task to have interim safeguards,
approval, a new due date, and a named owner. UK HSE's Offshore Petroleum
Regulator Functional Safety Inspection Guide specifically recommends a defined
process for deferrals affecting offshore SIS maintenance, repairs, or tests;
review/approval roles; risk assessment and monitoring; and consideration of
anticipated duration and cumulative risk when several SIS components are
deferred. This is scoped guidance, not a universal legal workflow for all
industries or maintenance. The Fact has no WordPress dependency and
`score_effect=none`.
[HSE Functional Safety Inspection Guide, p. 30](https://www.hse.gov.uk/offshore/assets/docs/functional-safety-inspection-guide.pdf).

## Additional verified anchor: MTTR versus restoration-time definitions

`kpi_mttr_definition_boundary` previously described MTTR as a generic after-failure
restoration duration and allowed diagnosis, tests, approval, and delays to be
included without distinguishing standard conventions. ISO 14224:2016 and ISO/TR
12489 distinguish MTTR (expected repair time) from MTTRes (fault detection,
pre-repair delay, active repair, and time until available to return to operation).
For ISO 14224 data, fault-detection time may be zero or unknown; it must not be
silently treated as one fixed MTTR component. KPI comparisons therefore need the
selected convention and start/end boundary stated; the terms are not interchangeable.
The Fact has no WordPress dependency and `score_effect=none`.
[ISO/TR 12489:2013 §§3.1.31–3.1.35](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3Atr%3A12489%3Aed-1%3Av1%3Aen),
[ISO 14224:2016 §§3.63–3.64 preview](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A14224%3Aed-3%3Av1%3Afr).

## Additional verified anchor: calibration traceability and intervals

The `calibration_program_traceability` anchor is now limited to what NIST directly
supports: traceability is a property of a measurement result established through a
documented unbroken calibration chain, each link contributing uncertainty, and
traceability alone does not establish fitness for purpose. NIST states that it
generally sets no fixed recalibration interval; accuracy requirements,
contract/regulatory constraints, device stability, environment, and historical
measurement assurance can inform interval selection. This does not set universal
plant acceptance tolerances or calibration procedures. [NIST traceability policy](https://www.nist.gov/calibrations/traceability), [NIST calibration-interval guidance](https://www.nist.gov/calibrations/recommended-calibration-interval).

## Additional verified anchor: risk-informed maintenance criticality

`maintenance_criticality_risk_prioritization` was narrowed to the framework
supported by ISO 31000 and ISO 55001: risk analysis takes consequences and
likelihood into account, while asset-management decisions use defined criteria
and suitable methods. The standards do not provide one universal consequence
factor list or weighting for all instrumentation assets. The previously listed
safety, environment, production, quality, regulatory, recovery-time, and substitute
availability considerations are examples for context-specific analysis, not a
standardized mandatory checklist. [ISO 31000:2018](https://www.iso.org/standard/31000), [ISO 55001:2024](https://www.iso.org/standard/83054.html).

## Additional verified anchor: equipment identification and data scope

`om_asset_register_system_boundary` was limited to ISO 14224's applicable
reliability/maintenance data scope: the equipment identifier identifies function
and physical location, and equipment data includes taxonomy and relevant
attributes. ISO explicitly excludes complete equipment data sheets and
additional operator-specific on-service data from its scope; therefore it cannot
be used to assert a universal list containing firmware, spares, criticality, and
document references. [ISO 14224:2016 catalogue and scope](https://www.iso.org/standard/64076.html), [ISO 14224 §§3.91–3.92 preview](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A14224%3Aed-3%3Av1%3Afr).

## Additional verified anchor: maintenance and failure data categories

`work_order_history_closed_loop` was narrowed to the categories in ISO 14224's
official catalogue scope: failure cause/consequence and maintenance action,
resources, maintenance consequence, and downtime in standardized reliability
and maintenance data. The catalogue expressly excludes extra on-service data
an operator may consider useful. The Fact does not assert that ISO 14224
prescribes each site's work-order authorization, permit, testing, restoration,
closeout, or as-found/as-left workflow. [ISO 14224:2016 catalogue and scope](https://www.iso.org/standard/64076.html).

## Additional verified anchor: reliability-maintenance data quality

`maintenance_data_quality_cmms_taxonomy` was narrowed to ISO 14224:2016's
minimum RM-data categories and standardized exchange format: equipment taxonomy
and attributes, failure cause/consequence, and maintenance action/resources/
consequence/downtime, with data quality control and assurance guidance. The
claim is scoped to petroleum, natural gas and petrochemical industries. It does
not make CMMS/EAM a mandatory named product or imply all local work-order fields
are standardized, and the standard does not guarantee KPI/RCA analysis
reproducibility. ISO's catalogue also excludes methods for analyzing/applying RM
data. The ISO/TC67 OTC paper gives taxonomy, picklist, validation and quality
management as an implementation example, not a universal site workflow.
[ISO 14224:2016 catalogue](https://www.iso.org/standard/64076.html),
[ISO/TC67 OTC-28705-MS paper, pp. 11–12](https://committee.iso.org/files/live/sites/tc67/files/news/OTC-28705-MS%20paper%20about%20ISO%20TC67%20standards%20in%20Houston%203%20May%202018.pdf).

## Additional verified anchor: asset-management continual improvement

`om_continuous_improvement_pdca_lifecycle_cost` was narrowed to the current
ISO 55000/55001 framework. ISO 55001:2024 requires an asset-management system
to be established, implemented, maintained and improved for organization-chosen
assets; decision planning considers cost, risk and performance. ISO 55000:2024
frames asset management over the asset lifecycle to realize value aligned with
organizational objectives. These sources support a continual-improvement
management framework, not a universal instrument-specific list of KPI/OOT/spares
inputs, fixed review cadence, or prescribed follow-up action.
[ISO 55001:2024](https://www.iso.org/standard/83054.html),
[ISO/TC 251 ISO 55001 overview](https://committee.iso.org/sites/tc251/home/projects/published/iso-55001.html),
[ISO 55000:2024](https://www.iso.org/standard/83053.html).

## Additional verified anchor: OT configuration changes and backups

`maintenance_configuration_backup_change_handoff` was narrowed to published NIST
OT guidance. SP 800-82 Rev. 3 recommends documenting approved OT baselines,
documenting/testing/approving in-scope changes before deployment, tracking
changes, and considering OT operational impact; it also recommends maintaining,
testing and integrating backup procedures with configuration/change management.
SP 1339 (June 2026) explicitly recommends integrating OT backups into change
management, creating them regularly, testing them and reviewing them in recovery
exercises. Neither source establishes a universal pre/post baseline or backup
check for every maintenance task; applicability, coverage and cadence remain
organization/system defined.
[NIST SP 800-82 Rev. 3, §§6.2.4.2–6.2.4.3](https://doi.org/10.6028/NIST.SP.800-82r3),
[NIST SP 1339](https://csrc.nist.gov/pubs/sp/1339/final).
