# Release-blocking Fact source triage — 2026-11-02

This is a **claim/source gap map**, not ChatGPT content approval and not an
instruction to remove any scoring hold. The existing 540 exact-ID blocks are
unchanged. Public primary-publisher pages were inspected on 2026-11-02; where
the cited standard text was unavailable, its content was **not** inferred from
the bibliographic preview.

| Anchor | First-party source and locator | What it establishes / remaining gap | Action |
|---|---|---|---|
| `sw04_rtm_bidirectional` | [NASA SWE-052](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052%2B-%2BBidirectional%2BTraceability), §1 and §2 | Bidirectional links among applicable requirements, design, code and verification are supported. The Pack's implication that one RTM universally contains every stage/result needs narrowing; NASA's table is also software-class scoped. | ChatGPT review proposed narrower wording; keep revision hold. |
| `hazop_lopa_initiating_event_frequency` | [AIChE/CCPS LOPA Data](https://ccps.aiche.org/resources/tools/lopa), Basic LOPA Steps and Initiating Events | Initiating event and frequency are defined for a scenario. This page does not prescribe the Pack's specific equipment-history/reliability-data basis in all cases. | Review source-specific clause or narrow. |
| `hazop_lopa_no_additional_sif_when_ratio_below_one` | [AIChE/CCPS LOPA Data](https://ccps.aiche.org/resources/tools/lopa), Basic LOPA Steps | Risk is evaluated against criteria to decide if another IPL is needed. It does not explicitly state a universal `required RRF <= 1` no-SIF rule or the Pack's ALARP qualifier. | Preserve hold until exact formula/decision conditions are established. |
| `operations_moc_revalidation` | [UK HSE COMAH C&I guidance](https://www.hse.gov.uk/comah/sragtech/discguidciindex.htm), criteria 5.2.4.3–5.2.5.1 | Supports proof-test/maintenance records and a modification procedure in the COMAH context. Does not prove every listed trend field must be logged universally. | Preserve promotion hold; bound to applicability. |
| `sis_sif_sil_scope`, `achieved_sil_verification`, `hazop_lopa_sif_allocation_boundary`, `demand_mode_metric_selection` | IEC 61508/61511 preview links in Registry; [HSE functional safety overview](https://www.hse.gov.uk/eci/functional.htm), SIS and lifecycle sections | HSE supports the high-level SIS and lifecycle concepts. IEC preview URLs did not yield inspectable clauses in this check, so precise IEC-derived assertion boundaries remain unconfirmed here. | Do not promote on overview alone; obtain inspectable normative/official text or another direct primary source. |
| `mcdc_definition` | [NASA/TM-2001-210876](https://ntrs.nasa.gov/api/citations/20010057789/downloads/20010057789.pdf), Abstract and §§1–2 | Tutorial is specifically framed around DO-178B Level A aviation software. It is not a universal industrial-control scoring requirement. | Preserve general-scoring exclusion; separately decide explicitly scoped-question behavior without weakening the exclusion. |

The Release Gate failures include missing requirement rows for these anchors;
that is expected while the current overlays block them. A green gate cannot
be manufactured by merely changing test expectations or declaring existing
Registry `verified` values sufficient. Review the exact source/claim mapping,
then either repair approved canonical sources through the managed workflow or
record a deliberate protected-test/policy conflict for separate adjudication.
