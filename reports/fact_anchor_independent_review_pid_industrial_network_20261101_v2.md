# P&ID and industrial Ethernet deterministic timing — 23 exact original-source comparisons

2026-11-01; reviewer GPT-6. `b339f694` supplied origin; continuing existing branch `codex/essay-boundary-calibration-20261028`. Each exact Fact ID retrieved from its actual canonical `rubrics/topic_packs/<topic>/fact_anchor.json`; previous independent source state PENDING. **23 KEEP_BOUNDED, 0 REVISE or DROP**; no proprietary software checklists or universal vendor recovery numbers promoted. First-party ISA/IEC/IEEE/IETF public official original publisher description or full RFC, not purchased standard normative text.

## First-party original sources
- **ISA-5.1-2024** — https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5-1 — ISA original issuer public scope: symbols & IDs, P&ID functional schematic, organization-specific design alternatives.
- **ISA-5 official series** — https://www.isa.org/standards-and-publications/isa-standards/isa-5-standard — ISA official public summary of ANSI/ISA-5.1, ISA‑TR5.1.04-2026 PFD/P&ID, ISA-5.4 loop diagram interconnection/construction.
- **IEC 62439-2:2016** — https://webstore.iec.ch/en/publication/24434 — Original IEC issuer public scope, MRP ring, dedicated manager, single link/switch failure; no paid detailed profile clauses used.
- **IEC 62439-3:2021** — https://webstore.iec.ch/en/publication/64423 — Original IEC issuer summary, PRP two networks, HSR ring/mesh, seamless zero recovery when compliant.
- **IEEE TSN official** — https://www.ieee802.org/1/pages/tsn.html — IEEE 802.1Qbv scheduled queues relative known time, Qci policing and Qbu frame preemption listed among published standards.
- **IEEE 802.1Qbu** — https://www.ieee802.org/1/pages/802.1bu.html — Original IEEE amendment purpose and both-link-partners support condition.
- **IEEE 802.1Qci** — https://grouper.ieee.org/groups/802/1/pages/802.1ci.html — Original IEEE text filtering/policing stream disruptions and behavior limits.
- **IETF RFC7567** — https://datatracker.ietf.org/doc/html/rfc7567 — Original IETF Best Current Practice: queue delays grow with congestion; full buffers can drop, and raw buffers alone do not guarantee deterministic performance.
- **ISO10007 public summary** — https://committee.iso.org/sites/tc176/home/projects/published/iso-10007-2017.html — Public committee process overview change control/status audit, not private normative clauses.


## pid_piping_instrumentation_diagram_symbols_tags_loops_control_narrative (12)

| Exact original Fact ID | Decision | Original publisher section/standard | Exact claim verification and applicability boundary |
|---|---|---|---|
| `pid_line_list_spec_and_nozzle_relations_checked_when_project_uses_them` | `KEEP_BOUNDED` | ISA 5.1 issuer scope; ISO10628-1 diagrams | Line list and piping/nozzle cross-check is good when project requires it. Autodesk software-specific example is not general norm. |
| `pid_major_equipment_piping_and_field_instrumentation_content` | `KEEP_BOUNDED` | ISA 5.1 issuer scope; ISA TR5.1.04 summary | P&IDs depict relevant process equipment, line IDs, valves and functions, exact line size/spec format project-selected. |
| `pid_shows_selected_alarm_and_interlock_functions_not_full_logic_detail` | `KEEP_BOUNDED` | ISA 5.1; ISA-5.06.01 issuer functions | P&ID functional diagram can indicate trip/alarm, while Boolean logic and sequence normally documented separately; no universal mandatory symbol for each internal PLC rung. |
| `pid_walkdown_can_verify_as_found_configuration_and_feed_as_built_records` | `KEEP_BOUNDED` | ISA 5.1 purpose and ISA-5.4 application through commissioning | Physical walkdown can reconcile installed tags/valves vs drawings, with controlled as-built records; procedure local. |
| `process_change_requires_document_review_and_pid_revision_where_affected` | `KEEP_BOUNDED` | ISO 10007 configuration control; ISA 5.1 document purpose | Changed P&ID content is subject to controlled approved revision in applicable change process, not unapproved redlines indefinitely. |
| `pfd_and_pid_purpose_and_detail_distinction` | `KEEP_BOUNDED` | ISA-5 Series official PFD/P&ID overview | PFD depicts higher-level material/energy process than detailed P&ID; depth is a project convention. |
| `pid_measurement_loop_functional_path` | `KEEP_BOUNDED` | ISA 5.1 instrumentation systems and ISA-5.4 loops | Trace process sensor/transmitter and connected functional loop steps when present, not insist every loop has controller. |
| `loop_diagram_carries_installation_and_wiring_detail_beyond_pid` | `KEEP_BOUNDED` | ISA-5.4 instrument loop diagrams official description | Loop diagram details component interconnections, power and signal wiring, beyond P&ID functional mapping. |
| `pid_diagram_and_pid_controller_terms_require_contextual_disambiguation` | `KEEP_BOUNDED` | ISA 5.1 P&ID and engineering PID-control definitions | P&ID drawing vs proportional-integral-derivative controller abbreviations are separate subjects; terminology not scored twice. |
| `pid_diagram_scope_and_documentation_function` | `KEEP_BOUNDED` | ISA 5.1 issuer scope | P&ID communicates process piping, equipment and measurement/control relationships, not physical scale. |
| `pid_feedback_loop_measure_controller_final_element_chain` | `KEEP_BOUNDED` | ISA 5.1 loop depiction; feedback loop topology | Process measurement/controller/final element make feedback functional chain where used; tuning numerical details outside schematic. |
| `pid_is_functional_schematic_not_physical_location_drawing` | `KEEP_BOUNDED` | ISA 5.1 schematic purpose; ISA 5.4 | Functional schematic not spatial scale/actual routed pipe length; refer construction/layout drawings. |

## industrial_network_realtime_determinism_time_synchronization_fault_recovery_resilience (11)

| Exact original Fact ID | Decision | Original publisher section/standard | Exact claim verification and applicability boundary |
|---|---|---|---|
| `iec_62439_2_ring_recovery_is_single_failure_profile_dependent` | `KEEP_BOUNDED` | IEC 62439-2:2016 issuer summary | MRP deterministic designed for defined single switch/link failure; actual recovery profile/topology/device matter, no fixed universal millisecond. |
| `ieee_802_1qbv_gate_schedule_design_accounts_for_guard_band_cycle_and_clock_accuracy` | `KEEP_BOUNDED` | IEEE TSN official 802.1Qbv summary | Scheduled traffic queue gating relative common time needs schedule and clock accuracy; guard band is implementation/tradeoff, no universal size. |
| `industrial_cycle_time_distinguishes_periodic_application_and_network_cycles_from_frame_transfer` | `KEEP_BOUNDED` | IEEE TSN / periodic schedule definition | Application/communication cycle is recurrence interval, not duration of one frame transmission; phase and scheduling matter. |
| `throughput_is_a_rate_metric_distinct_from_latency_and_jitter` | `KEEP_BOUNDED` | IETF RFC7567 queue and rate-delay; IEEE TSN | Bitrate/throughput does not guarantee real-time latency/jitter bounds; need queue load and traffic shaping. |
| `clock_synchronization_alone_does_not_establish_deterministic_network_behavior` | `KEEP_BOUNDED` | IEEE TSN 802.1Qbv time-based schedule; IETF RFC7567 queue delay | Clocks are needed for certain shared schedules but uncontrolled queues and load still cause variable delay. |
| `frame_preemption_suspends_preemptable_frames_for_time_critical_traffic` | `KEEP_BOUNDED` | IEEE 802.1Qbu original amendment summary | Non-critical frame is suspended while critical transmits; both link partners must support preemption; overhead and validation relevant. |
| `iec_62439_2_mrp_ring_manager_controls_single_fault_recovery` | `KEEP_BOUNDED` | IEC 62439-2:2016 publisher statement | Dedicated media redundancy manager handles ring failover; time depends on selected single-failure profile and implementation. |
| `iec_62439_3_prp_hsr_provide_seamless_switchover_within_defined_protocol_scope` | `KEEP_BOUNDED` | IEC 62439-3:2021 issuer summary | Zero-recovery PRP/HSR claim for single applicable network-element failure and compliant duplicated path; common-cause not removed. |
| `ieee_802_1qci_filters_and_polices_traffic_per_stream` | `KEEP_BOUNDED` | IEEE 802.1Qci issuer amendment summary | Per-stream classification/policing can detect disruptive streams. Configurations can deny valid traffic, so must test. |
| `one_way_network_latency_accumulates_transmission_propagation_and_node_processing_delays` | `KEEP_BOUNDED` | Network timing dimensions + IETF RFC7567 | One-way delay is serialization, propagation, switch processing and queuing along route, under relevant protocol/clock measurement scope. |
| `rfc_7567_queue_overload_causes_delay_and_full_queue_loss` | `KEEP_BOUNDED` | IETF RFC7567 official BCP §2–4 | When offered load exceeds service, queues build then may overflow/drop, while buffering alone cannot guarantee deadline. |

**Release boundary:** No canonical Registry/topic pack generated-bank regeneration, no local pytest/PASS assertion, no direct main update. Explicitly inspect ISO/ISA/IEC paid normative clauses separately before treating exact clause language as required globally. Scores apply only to bounded cross-industry physics/standard descriptions. Expected audit total 1290: 159 remaining PENDING, 737 KEEP_BOUNDED, 67 REVISE_REQUIRED, 36 insufficient, 7 standard-scoped, 8 vendor-scoped, 275 scoring exclusions and 1 legacy scoped. Executable unresolved scoring holds 210 (=159+36+7+8), revision holds 67, original screening excluded 276 unchanged.
