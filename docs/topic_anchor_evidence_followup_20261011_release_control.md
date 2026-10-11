# Release-control anchor evidence review — 2026-10-11

## Disposition

Topic: `configuration_change_release_backup_rollback_migration_obsolescence_management`  
Anchor: `sw06_release_control_authorized_artifact`  
Fact: `sw06_release_control_identifies_approved_versioned_scope_and_checks_delivery_copy`  
Status: verified/approved; `score_effect=none`.

The anchor was narrowed to avoid treating one release process as a universal plant
requirement. It now covers identification of the approved release scope and
versions, verification of the master and delivery copies, and controlled delivery
history under the applicable project/site procedure. It does not require a
particular checksum utility, ban every rebuild or field edit in all contexts, or
claim that NASA project guidance is a plant regulation.

## Evidence and limits

- NASA's SWE-085 Version D guidance requires applicable project procedures for
  storage, handling, delivery, release, and maintenance; identifies release scope
  and configuration-item versions/revisions; and describes creating/verifying a
  master copy and checking delivery copies against it. Checksum validation is an
  example of a comparison technique, not the sole permitted method. [NASA SWE-085](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695469/SWE-085%2B-%2BRelease%2BManagement)
- NIST's baseline-configuration definition describes a formally reviewed and
  agreed configuration reference that changes through change-control procedures
  and supports future builds, releases, and changes. This corroborates the
  configuration-control concept but does not prescribe an OT release workflow.
  [NIST CSRC baseline configuration](https://csrc.nist.gov/glossary/term/baseline_configuration)

## Registry

The Fact is registered in `grading/evidence/approved_fact_registry.json`, with no
source-reference dependency and no runtime score effect. The generated rubric
banks were rebuilt using `scripts/rubric_manager.py build-generated-rubrics`.

## Additional verified anchor: as-built documentation and OT backup boundary

`sw06_as_built_consistency` previously implied that the approved repository, live
installation, backup, and related documentation must all be mutually identical.
That overstates the evidence: an OT backup is a recovery copy from a particular
time and need not be identical to the current online state. The anchor is narrowed
to two supported controls: compare/reconcile the as-built configuration against
approved technical documentation; and inventory OT backups including configuration
information, checking reliability/integrity when technically possible while
tracking backup version/time and differences from live state. NASA-HDBK-1004
describes PCA as checking that as-built configuration complies with its design
documentation. NIST SP 800-82 Rev. 3 recommends an OT backup inventory including
configuration information and reliability/integrity verification where technically
possible; NIST SP 1339 recommends integrating backups with change management,
creating and testing them regularly, and reviewing them in recovery exercises.
No universal live-backup equality or fixed backup cadence is claimed. `score_effect=none`.
[NASA-HDBK-1004, Appendix A.11](https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline/0/2020_04_01_nasa_hdbk_1004_approved.pdf),
[NIST SP 800-82 Rev. 3, §6.2.4.3 and Appendix E](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf),
[NIST SP 1339](https://csrc.nist.gov/pubs/sp/1339/final).

## Additional verified anchor: risk-based OT backup scope

`sw06_backup_scope_and_consistency` previously stated a broad fixed backup
inventory (including recipes, databases, certificates, drivers and other items)
for all control systems and required an internally consistent time point. NIST
SP 1339 instead says to identify the files, software, and spares required to
restore each selected environment; its examples include program/logic/config
files, I/O lists, firmware, HMI files, license keys, vendor tools, OS/VM images,
and supporting software. It calls for backup scope, frequency, media and location
to reflect information-change rate, system type, risk, and dependencies; labels
include system name/date/time. It also recommends integrity mechanisms and
recurring restoration tests on non-production systems. NIST SP 800-82 Rev. 3
corroborates OT-specific backup inventory and integrity checks when technically
possible. The Pack now treats the NIST items as examples, not a universal fixed
checklist, and leaves asset-specific contents and test feasibility to operational
context. `score_effect=none`.
[NIST SP 1339, pp. 1–2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1339.pdf),
[NIST SP 800-82 Rev. 3, §6.2.4.3 and Appendix E](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

## Additional verified anchor: MOC scope and legal/guidance distinction

`sw06_moc_trigger_and_scope` previously treated permanent, temporary, emergency,
quality, environmental, security, maintenance and regulatory-impact changes as
one universal MOC domain. That scope was not substantiated. The anchor is now
bounded to 29 CFR 1910.119(l): for OSHA PSM-covered processes, written MOC
procedures apply (except replacements in kind) to changes to process chemicals,
technology, equipment, procedures, and facility changes affecting the covered
process. Before the change, the rule specifies technical basis, safety/health
impact, operating-procedure modifications, time period and authorization;
affected operating, maintenance and contract employees must be informed/trained
before startup, and PSI/procedures updated when affected. OSHA Appendix C gives
nonmandatory additional context for temporary changes. Separately, NIST SP
800-82 Rev. 3 recommends documenting, testing and approving OT changes before
deployment. These sources do not establish one universal MOC legal scope for all
industries or every change category. `score_effect=none`.
[OSHA 29 CFR 1910.119(l)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119),
[OSHA Appendix C (nonmandatory)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119AppC),
[NIST SP 800-82 Rev. 3, §6.2.4.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

## Additional verified anchor: change impact review scope

`sw06_impact_analysis_multidisciplinary` formerly made a long set of domains
(logic, communications, HMI, historian, reports, alarms, safety functions,
procedures, training, spares, licenses, and recovery) a mandatory multidisciplinary
review for every change. The cited sources support scoped review, not that fixed
universal checklist. OSHA 29 CFR 1910.119(l)(2) specifies technical basis,
safety/health impact, operating-procedure modifications, change period and
authorization for covered PSM changes. Its nonmandatory Appendix C gives possible
change-form topics and differentiates review depth by complexity: minor,
well-understood changes may use an authorized checklist; complex/significant
changes may warrant operations, maintenance and safety participation. NIST SP
800-82 Rev. 3 recommends approved OT baselines and documenting/testing/approving
changes before deployment; it illustrates dependency impact, such as disabling
PLC communications also disabling associated HMI communications. Therefore the
Pack now treats connected functions as change-specific impact candidates and does
not claim all fields or disciplines are mandatory for each change. `score_effect=none`.
[OSHA 29 CFR 1910.119(l)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119),
[OSHA Appendix C (nonmandatory)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119AppC),
[NIST SP 800-82 Rev. 3, §§6.2.4.1–6.2.4.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

## Additional verified anchor: change implementation plan scope

`sw06_change_implementation_plan` previously required the same long list of
sequence, personnel, tools, operating conditions, outage window, communications,
backup, verification, abort, rollback, and owner fields for every change. The
sources support tailoring instead. For OSHA PSM-covered changes, 29 CFR
1910.119(l) sets the pre-change considerations (technical basis, safety/health
impact, procedure modifications, necessary time period, authorization) and
affected-employee information/training before startup. NIST SP 800-82 Rev. 3
recommends documenting, testing, and approving OT changes before deployment and
notes that many changes may need scheduled downtime to minimize impacts. NIST SP
1339 says backup/recovery procedures should be adapted to the operating
environment and safety requirements. The revised anchor therefore treats backup,
communications, rollback, abort criteria, and similar items as plan elements
selected when applicable, not as one universal checklist. `score_effect=none`.
[OSHA 29 CFR 1910.119(l)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119),
[NIST SP 800-82 Rev. 3, §6.2.4.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf),
[NIST SP 1339](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1339.pdf).

## Additional verified anchor: regression-test selection and scope

`sw06_risk_based_regression` now distinguishes the software-testing concept from
plant-specific operating procedure. NASA SWE-191 defines regression testing as
retesting previously integrated/tested software after changes to check prior
functionality and avoid introducing defects; it discusses choosing a subset based
on changed and potentially affected areas and balancing coverage, confidence, time,
and effort. NIST SP 800-82 Rev. 3 separately recommends testing devices before OT
deployment and documenting, testing, and approving OT changes before deployment;
its PLC/HMI example demonstrates why dependencies can matter. These sources support
change-impact- and risk-informed test selection, but do not impose a fixed test list
for every plant change. Actual OT test scope and operating scenarios remain tied to
system risk and applicable site procedures. `score_effect=none`.
[NASA SWE-191](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695526/SWE-191%2B-%2BSoftware%2BRegression%2BTesting),
[NIST SP 800-82 Rev. 3, §§6.2.4.1–6.2.4.2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf).

## Additional verified anchor: change-specific rollback requirements

`sw06_rollback_preplanned_criteria` previously presented a long, fixed set of
rollback fields (trigger, time limit, target baseline, data handling and decision
authority) as universally required. NIST SP 800-128 lists requirements for rollback
when problems occur as part of an organization's configuration change-control
procedures, while CISA's control-system patch guidance recommends a contingency
plan depending on the patch if it corrupts the stable environment. These sources
support requiring applicable change procedures to address rollback, and identifying
the conditions and stable recovery target where a change is reversible. They do not
establish the same detailed fields or rollback obligation for every plant change.
The revised Anchor therefore leaves timing, data reconciliation and authority to
system impact and applicable procedures. `score_effect=none`.
[NIST SP 800-128, §3.2.2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-128.pdf),
[CISA, Recommended Practice for Patch Management of Control Systems, p. 19](https://www.cisa.gov/sites/default/files/recommended_practices/RP_Patch_Management_S508C.pdf).

## Additional verified anchor: Restore and Rollback are related, not synonymous

`sw06_restore_rollback_distinction` was narrowed to the supported conceptual
boundary: Restore recovers selected data/configuration/system state from backup;
Rollback reverses a problematic change toward a prior approved or stable state;
a rollback may use a backup restore, but the operations are not synonyms. NIST SP
800-82 Rev. 3 describes OT backups as recovery resources and recommends testing
restoration from backup data. NIST SP 800-128 treats rollback requirements as part
of change-control procedures, separately from backup/recovery. Exact steps depend
on the recovery object and applicable procedure. `score_effect=none`.
[NIST SP 800-82 Rev. 3, §6.2.4.3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf),
[NIST SP 800-128, §3.2.2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-128.pdf).

## Additional verified anchor: vendor lock-in as a managed lifecycle trade-off

`sw06_vendor_lockin_lifecycle_risk` is verified score-neutrally as a balanced
value/portability and continuity review, not a ban on vendor-specific features or
single-supplier solutions. UK GDS guidance explicitly says that provider-specific
features may bring value and that lock-in risk should be judged against portability,
preparedness and exit cost; it also identifies data export, open formats/standards
and provider-switch planning. This is cloud guidance, so it supports the general
trade-off principle only. NIST SP 800-82 Rev. 3 supplies the OT-specific context:
proprietary protocols, vendor-constrained support and licensing, long asset lifetimes,
planned outages, and replacement-part availability can affect continuity. UK Open
Standards guidance illustrates data/API portability but is not an OT rule. The sources
do not require every plant to use open interfaces, obtain source code, retain a second
vendor, or impose identical contract clauses. Review only the data/config export,
interfaces, substitute options, service/IP/tool rights and switching cost relevant to
the asset and contract. `score_effect=none`.

- [UK GDS, Managing technical lock-in in the cloud](https://www.gov.uk/guidance/managing-technical-lock-in-in-the-cloud)
- [NIST SP 800-82 Rev. 3, §§2.2 and 6](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [UK Government, Open Standards Principles](https://www.gov.uk/government/publications/open-standards-principles/open-standards-principles)
