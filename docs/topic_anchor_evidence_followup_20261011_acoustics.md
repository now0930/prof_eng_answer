# Acoustic quantity and decibel fact verification (2026-10-11)

Scope: twenty-two declarative anchors in `control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`. All are score-neutral and are registered only within their stated physical, mathematical or measurement assumptions.

| Anchor | Verification and boundary |
|---|---|
| `sound_power_level_definition` | ISO 3747 §3.17 defines sound power level as 10 log10 of source sound power over reference sound power, with reference 1 pW. It is a source quantity, not point SPL. |
| `sound_pressure_level_definition` | ISO 3747 §3.2 defines SPL as 10 log10(p²/p0²), equivalently 20 log10(p/p0), and gives p0=20 μPa for airborne sound. The statement is limited to RMS pressure and a stated measurement/weighting convention. |
| `decibel_logarithmic_scale` | Direct consequence of ISO's logarithmic level definitions: add the underlying linear mean-square pressure/power ratios, then convert back to dB. Arithmetic addition of dB levels is not generally valid. |
| `independent_source_logarithmic_sum` | Derivation: for each level Li, the linear power ratio is 10^(Li/10); independent/uncorrelated source powers add, so Ltotal=10 log10(Σ10^(Li/10)). Correlated coherent pressures may require phase-aware treatment. |
| `identical_source_doubling` | Under the same uncorrelated-source assumption, equal levels L yield L+10 log10(2)=L+3.0103 dB. |
| `pressure_amplitude_doubling` | From the SPL definition, doubling the same RMS pressure yields 20 log10(2)=6.0206 dB when reference and weighting remain unchanged. |
| `sound_power_pressure_boundary` | ISO 3747 obtains source sound power from sound-pressure measurements under a defined acoustic method/environment; NIST Handbook 122's pressure-to-power relation includes reverberation, room volume, absorption and atmospheric conditions. Thus source power and point pressure cannot be equated without propagation and measurement conditions. |
| `a_weighting_dba_meaning` | OSHA describes A-weighting as an approximation of human-ear frequency response around a specified reference loudness; ISO requires the A-weighting indicator to be identified. This is a measurement weighting, not an unweighted dB value and not an occupational exposure limit by itself. |
| `multiple_source_parallel_bypass_combination` | The same linear-domain derivation applies to parallel-valve and bypass sources only when they are mutually uncorrelated and share a common reference/weighting; correlated or coherent sources require suitable phase-aware treatment. |
| `overall_spectrum_octave_distinction` | ISO defines total and octave-band sound power/pressure levels separately and requires frequency-band or weighting notation to be reported. Overall level and spectrum therefore convey different information. |
| `acoustic_power_pipe_radiation_path` | Emerson/Fisher describes a closed-system path in which in-fluid sound excites the valve-adjacent pipe boundary and its vibration radiates external sound. This does not imply a fixed transmission efficiency or make internal power equal external SPL. |
| `multi_hole_jet_division` | Emerson/Fisher's noise-attenuation brochure and Whisper Trim I product documentation describe model-specific multi-path/drilled-hole trim splitting a large turbulent flow into multiple smaller jets or sources. This does not establish a universal noise reduction for every multi-hole trim. |
| `silencer_insulation_enclosure_path_treatment` | Emerson/Fisher separates source from path treatment and lists inline silencers, pipe treatment/insulation and insulated boxes/buildings as distinct options. Effectiveness depends on the transmission path and installation. |
| `multi_stage_pressure_ratio_velocity_control` | Emerson/Fisher documents multistage pressure reduction that divides stream power between stages and expansion areas for velocity management. Stage pressure ratios and velocity targets remain trim- and service-specific; no universal numeric limit is claimed. |
| `aerodynamic_turbulent_jet_noise` | Emerson/Fisher identifies turbulent gas/steam flow as aerodynamic noise source; Valmet further distinguishes lower-pressure-ratio turbulence from high-pressure-ratio/choked shock-wave interactions. The latter is not asserted for all service. |
| `cavitation_bubble_collapse_noise` | Emerson/Fisher documents liquid-only cavitation as vapor-bubble formation and collapse, with noise, vibration, and damage possible; persistent vapor in flashing is distinguished from collapse-driven cavitation noise. |
| `aerodynamic_expansion_shock_noise` | Valmet identifies shock-wave/turbulence interaction as a major source in high-pressure-ratio or choked gas/steam flow. No universal ratio or noise value is claimed. |
| `gas_choked_regime_noise_input` | Gas/steam choking is sonic flow at the vena contracta and, after the full-choke limit at fixed opening/inlet pressure, further pressure drop does not increase flow. It is a finite flow regime, not zero flow; applicable noise regime is selected from service conditions. |
| `gas_outlet_velocity_mach_geometry` | Valmet and Fisher support dependence on velocity/sonic regime, measurable valve geometry, service conditions, and downstream pipe transmission. No generic velocity/Mach limit is asserted. |
| `external_spl_observation_condition` | Fisher estimates SPL at an observer location and accounts for distance and pipe/path attenuation; Valmet describes directional effects; ISO 3744:2025 specifies measurement surfaces and reflecting-environment corrections. No fixed enclosure attenuation is claimed. |
| `process_flow_vs_accessory_noise` | Fisher distinguishes process-flow mechanical/aerodynamic/hydrodynamic noise; Foxboro VBS200 and SMC IP8001 documentation identify configuration-specific pneumatic exhaust noise. This does not imply every actuator or positioner has an independently audible exhaust source. |
| `field_measurement_background_correction` | OSHA and ISO 9612:2025 support recording source/location/distance, weighting, duration and representative exposure conditions; ISO 3744:2025 adds method-specific environment corrections. Apply/report background correction only where required by the selected method. |

## Primary references

- [ISO 3747:2010, Acoustics](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A3747%3Aed-3%3Av1%3Aen), §§3.2, 3.17 and method scope.
- [NIST Handbook 122, Noise Emission Measurements for Regulatory Purposes](https://nvlpubs.nist.gov/nistpubs/Legacy/hb/nbshandbook122.pdf), equations (15)–(16).
- [OSHA Technical Manual, Section III, Chapter 5](https://www.osha.gov/otm/section-3-health-hazards/chapter-5), A-weighting definition and measurement discussion.
- [ISO 13348:2019, Fans — Tolerances, methods of conversion and technical data presentation](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso%3A13348%3Aed-3%3Av1%3Aen), §§3.26–3.30, definitions of total and octave-band quantities.
- [Emerson/Fisher, Control Valve Sourcebook—Oil and Gas, Chapter 5](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), closed-system pipe transmission and noise path treatments.
- [Emerson/Fisher, Noise-Attenuation Technologies for Control Valves](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351989x012.pdf) and [Whisper Trim I product documentation](https://www.emerson.com/en/final-control/products/fisher-whisper-trim-i), model-specific multi-jet trim design.
- [Emerson/Fisher Control Valve Handbook §5.16](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf) and [Control Valve Sourcebook Chapter 5](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf), multi-stage pressure reduction and velocity-management examples.
- [Emerson/Fisher Whisper Trim III](https://www.emerson.com/en/final-control/products/fisher-whisper-trim-iii), aerodynamic noise mechanism for gas, vapor, and steam control-valve flows.
- [Emerson, Cavitation in Control Valves](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation) and [Fisher Catalog 12, Section 3](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s3.pdf), liquid bubble formation/collapse, noise, vibration, damage, and distinction from flashing.
- [Valmet Flow Control Manual, Gas and Steam Flow](https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/), §§4.1, 4.3–4.5, gas choking, aerodynamic-noise regimes, shock/turbulence interactions, velocity control and observation-point effects.
- [ISO 3744:2025](https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/08/08/80866.html?browse=tc), §§1.1, 1.3, sound-power estimation from specified sound-pressure measurement surfaces and reflecting-environment correction.
- [OSHA Technical Manual, Noise](https://www.osha.gov/otm/section-3-health-hazards/chapter-5), field survey records and instrumentation; [ISO 9612:2025](https://www.iso.org/standard/81317.html), noise exposure weighting and condition analysis; [CDC/NIOSH, Eliminate or Reduce Noise](https://www.cdc.gov/niosh/noise/prevent/eliminate.html), comparative microphone distance/time consistency.
- [Foxboro VBS200 Volume Booster Quick Guide](https://d38005r3ny6olb.cloudfront.net/images/data_sheets/Schneider/QG_EVE0602_A-EN_VBS200_Series.pdf), §§2.2.4 and 3.2, booster exhaust noise/silencing; [SMC IP8001 Operation Manual](https://static.smc.eu/binaries/content/assets/smc_global/product-documentation/operation-manuals/en/om_ip8001_om00013en-a.pdf), p. 19, positioner exhaust-noise adjustment cue.

The registered Facts have `score_effect=none`. No occupational exposure limit, universal valve-noise prediction method, fixed attenuation, or site acceptance criterion is inferred from these definitions and derivations. Remaining noise anchors—including pipe transmission-loss conditions, selection tradeoffs, multi-phase noise prediction, and hand-off boundaries—remain unregistered until their full wording and scope can be supported.

Additional verified anchor: `hydrodynamic_turbulence_noise`. IEC 60534-8-4:2015
describes prediction of noise generated by liquid flow through a control valve and
identifies normal turbulence and liquid cavitation as possible generation
mechanisms. The registered claim is limited to normal turbulence and does not
conflate it with cavitation or flashing. [IEC publication page](https://webstore.iec.ch/en/publication/23315).

## Pending anchors retained as unresolved

The following current Topic Pack anchors were reviewed against the sources above.
They remain absent from the approved registry because the available evidence does
not support every clause or the implied universal/ordered rule:

| Anchor | Reason it remains unresolved |
|---|---|
| `control_valve_noise_scope` | A useful learning-scope synthesis, but no single independent technical source establishes all listed components as a required integrated evaluation procedure. |
| `source_path_receiver_hierarchy` | NIOSH supports the source/path/receiver framework and preferred control order; the separate prohibition on double-counting combined effects needs a defined calculation/evaluation basis. |
| `topic7_aerodynamic_noise_handoff`, `topic8_hydrodynamic_noise_handoff` | The repository topics contain related variables, but internal routing alone is not independent technical evidence for every listed term and its boundary. |
| `flashing_two_phase_noise` | Vendor material lists flashing as a hydrodynamic noise source, while IEC 60534-8-4 excludes flashing from its prediction scope; the specific persistent two-phase/droplet-impact broadband claim is not established by the reviewed authoritative evidence. |
| `pipe_transmission_loss_dependency` | Pipe geometry/material/frequency are supported as transmission-loss factors; the anchor's additional “service condition” wording mixes process generation conditions with pipe transmission loss and has not been validated as written. |
| `diffuser_pressure_drop_distribution` | Sources support splitting pressure drop as a possible noise measure, but not the entire bundled claim about capacity, erosion, and diffuser-generated noise across applications. |
| `low_noise_trim_capacity_rangeability_tradeoff` | Emerson describes a capacity/noise trade-off for traditional complex low-noise trims, but the anchor generalizes this to rangeability and all low-noise trims; newer designs demonstrate the trade-off is not universal. |
| `plugging_erosion_maintenance_tradeoff` | The combined claims about small passages, plugging, erosion, particle tolerance, and maintenance are design-specific; a complete source set for this conjunction has not been established. |
| `operating_case_noise_matrix` | Multiple process conditions affect calculation inputs, but the exact required matrix (including startup/shutdown) is a workflow recommendation, not a verified universal prediction rule; transient cases may be outside steady-state method scope. |
| `prediction_measurement_gap_diagnosis` | Input, flow regime, pipe, observation point, reflections, and background can affect comparison, but the prescribed diagnostic order is not established as a standard sequence. |
| `vendor_crosscheck_noise` | The listed source level, octave spectrum, travel, external SPL, and mitigation fields are not demonstrated to be universally available or required in every vendor output. |

These eleven rows include twelve anchor IDs because the two hand-off anchors share a
row. They remain part of the overall unverified count; this table does not exclude
them from the 2,069 technical Fact-anchor population.
