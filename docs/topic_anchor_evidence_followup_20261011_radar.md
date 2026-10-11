# Radar/GWR Fact Anchor follow-up — 2026-10-11

## Scope and result

Independently re-reviewed the two previously unverified anchors in
`radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`.
Both are now represented by narrower, source-matched claims. The pack has 28 anchors;
all 28 now have verified Fact registry links. The new facts are score-neutral.

## `radar_upper_null_zone_overfill_coordination`

The old statement bundled transmit leakage, ringdown, nozzle reflection, receiver
saturation, operating maximum, and a universal independent-HH arrangement. Available
evidence did not justify that broad causal bundle or a universal safety requirement, so
the pack statement was replaced rather than approved as written.

The revised fact is model- and standard-scoped:

- Emerson Rosemount 5408 defines the configured Upper Null Zone as a near-transmitter
  region where echoes are ignored and measurement is not performed; its manual gives an
  Upper Range Value constraint relative to the zone.
- API Std 2350 5th edition §5.2.4.1 specifies ATG plus independent LAHH for Category 3
  petroleum tank overfill systems. It is not generalized to every tank or service.
- HSE HSG176 Fig. 9 independently illustrates a separate LAHH sensor for its
  flammable-liquid tank context.

Sources: [Rosemount 5408 Reference Manual, §7.5.3, p. 138](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/level/documents/dl-rmt-5408-non-contacting-radar-transmitter-202470.pdf), [API Std 2350 5th Edition](https://www.api.org/products-and-services/standards/important-standards-announcements/standard-2350), [HSE HSG176, Fig. 9, p. 33](https://www.hse.gov.uk/pubns/priced/hsg176.pdf).

## `gwr_quasi_tem_return_path`

The old `quasi-TEM`/universal return-path statement was not verified. The label and
generalized mode claim were removed; the stable anchor ID was retained to avoid changing
Topic routing contracts. The revised statement is limited to a documented product case:

- AMETEK/Magnetrol Eclipse Model 706 manual §3.3.5.2 says single-rod field behavior is
  installation/application dependent; nozzle impedance mismatch and nearby metallic
  objects can create extra reflections, false echoes, or measurement errors.
- The same manual contrasts this with the grounded coaxial outer tube for that product
  configuration. The contrast is not generalized to all GWR probe geometries.

Source: [Eclipse Model 706 HART I&O Manual BE 57-606, §§3.3.5.2, pp. 50–51](https://www.ametek-measurement.com/-/media/project/oneweb/oneweb/lms/documents/instruction-manuals/magnetrol/57-606_eclipse_model_706_hart_io.pdf?la=en&revision=3cc2fa2d-2023-4d70-8a74-8a74b6bebae0).

## Registry effect

Added two independently verified facts with `source_refs=[]`, explicit external
`verification_refs`, and `score_effect=none`. Registry totals are now 910 fact records,
909 unique canonical anchors, and 63 topics; 1,164 of 2,073 anchors remain unverified.
The 200-item batch administration counts are 444 confirmed-but-unregistered, 365
conditional-but-unregistered, and 355 without a current batch row.
