# Guided Wave Radar (GWR) 레벨 측정원리와 적용

## Status and evidence

- Topic ID: `guided_wave_radar_level_measurement_tdr_interface_application`
- Question Type: `PRINCIPLE_INTERPRETATION`
- State: managed `draft / human_review_required`; not an active routing or grading owner.
- The prompt below is a knowledge-based plausible question. No past-exam instance, frequency,
  or official syllabus classification has been verified.
- Facts were reorganized from the existing Radar Pack. Its named manufacturer sources and exact
  manual edition/page/diagram have not been independently checked here.

## Representative problem unit

> Guided Wave Radar (GWR) 레벨계의 TDR 측정원리와 프로브 구조에 따른 전파경로를 설명하고,
> 상부 액면 및 계면 측정 시 유전율·공정조건이 미치는 영향과 적용상 한계를 설명하시오.

This is one answer unit organized around pulse propagation along a probe, reflection/round-trip
time, distinct propagation paths for surface and interface measurement, and probe-specific limits.
It is not the free-space pulse/FMCW carrier, chirp, beat-frequency, or antenna beam problem.

## Required answer chain

1. State that GWR sends a low-power microwave pulse along a rod, cable, or coaxial probe.
2. Explain reflection at an impedance discontinuity and TDR range inference from round-trip time.
3. Distinguish upper-surface measurement through the gas/vapor path from an interface echo that
   traverses an upper liquid layer; do not apply the liquid dielectric factor to the entire gas gap.
4. Explain that probe geometry and the surrounding tank/return path affect practical propagation;
   avoid universal TEM/no-dispersion claims for every probe type.
5. Bound applicability by dielectric contrast, foam/emulsion, buildup, probe deformation/contact,
   vapor/process conditions, installation and the selected device's rated envelope.

## Anchor-to-demand map

| Demand | Fact Anchor |
|---|---|
| TDR principle and guided pulse path | `gwr_tdr_probe_guided_reflection` |
| Surface vs interface propagation path | `gwr_surface_interface_permittivity_path` |
| Probe geometry and return path | `gwr_probe_return_path_quasi_tem_boundary` |
| Process and mechanical limitations | `gwr_process_probe_application_limits` |

## Owner boundary

- Existing free-space Radar Pack retains pulse time-of-flight, FMCW/chirp/beat-frequency,
  range resolution, antenna beam/false echo, and its existing aliases until a reviewed migration.
- This draft candidate is limited to probe-guided TDR structure/path, upper-surface/interface
  propagation, and probe-specific application limitations.
- General instrument installation, vendor specification, commissioning acceptance, and safety
  function/SIL claims remain with their existing owners.
- The original Radar Pack retains its GWR anchors and pattern #14 for now. The new draft is not
  promoted; simultaneous runtime grading/routing ownership is not enabled.

## Technical cautions

- Do not describe free-space FMCW and GWR probe-guided TDR as one identical transmitter structure.
- Do not divide the full gas-space surface distance by `sqrt(epsilon_r, product)`.
- Do not claim every single-rod/cable probe is an ideal, dispersion-free TEM line.
- Do not claim that GWR is immune to low dielectric contrast, foam/emulsion, buildup, bending,
  contact, high-pressure vapor, or product-specific constraints.
- Confirm all details against the selected manufacturer's manual before operational use.

## Source provenance

Existing source candidate:
`radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
Fact Anchors `gwr_tdr_guided_wave_principle`,
`gwr_effective_permittivity_propagation_path`, `gwr_quasi_tem_return_path`, and
`gwr_interface_and_process_limitations`. The existing Radar README lists Emerson Rosemount 5300,
Siemens SITRANS, Endress+Hauser Levelflex, and other radar manuals as verification references;
exact editions/pages and the underlying documents remain unchecked.

## Review checklist

- [ ] Confirm the TDR/probe and reflection description against primary manufacturer documentation.
- [ ] Confirm which parts of the level/interface dielectric path are general and which are device-specific.
- [ ] Confirm rod/cable/coaxial distinctions and avoid unsupported universal propagation claims.
- [ ] Check whether process/mechanical limitation anchors are sufficient for the representative demand.
- [ ] Resolve alias conflict and single-owner migration with the existing free-space Radar Pack.
- [ ] Human review is recorded before approval, generated promotion, or router activation.
