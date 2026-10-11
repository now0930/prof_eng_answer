# Control-valve noise prediction method/source follow-up — 2026-10-11

## Scope

Verified the existing anchor `prediction_standard_vendor_method` in
`control_valve_noise_aerodynamic_hydrodynamic_low_noise_trim`. The anchor concerns
identifying the noise-prediction method, edition, vendor method where used, and
reported SPL observation/reference condition. Registration is technical evidence
only; `score_effect` remains `none` and existing grading authority is unchanged.

## Evidence and limits

- IEC 60534-8-3:2010 is an aerodynamic prediction method for compressible flow. Its
  stated scope is single-phase dry gases/vapours and it specifies valve applicability
  and downstream-pipe assumptions. This is evidence against treating the method as
  universal or omitting its edition/scope. [IEC publication page](https://webstore.iec.ch/en/publication/2474)
- ISA-75.17-1989 describes a compressible-fluid aerodynamic method and explicitly
  excludes mechanical vibration, unstable flow and other unpredictable behavior.
  This historic ISA document is not asserted to be equivalent to IEC 60534-8-3.
  [ISA product description](https://www.isa.org/products/isa-75-17-1989-control-valve-aerodynamic-noise-pre)
- Valmet's Flow Control Manual states that the noise calculation method presented
  in its sizing calculations is mainly based on VDMA 24422 (1979) and IEC 60534-8.
  Therefore a vendor calculation output should not be silently assumed to use a
  different standard or implementation. [Valmet manual](https://www.valmet.com/globalassets/sharepoint/imported/flowcontrol_manual.pdf)
- Valmet's gas/steam noise prediction material discusses atmospheric SPL and
  observation distance/direction. A reported SPL therefore needs its method-defined
  or selected reference/observation condition. [Valmet gas and steam flow](https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/)

## Interpretation

The approved Fact deliberately narrows the legacy wording: it requires identifying
the method/edition and scope, and the reference condition for the SPL result. It does
not claim IEC and ISA editions are interchangeable, that every manufacturer uses a
proprietary method, or that a prediction guarantees a field measurement.

## Registry

Fact ID: `control_valve_noise_prediction_method_and_reference_condition_must_be_identified`  
Legacy anchor: `prediction_standard_vendor_method`  
Status: `verified` / `approved` / `score_effect=none`

## Additional verified anchor: occupational exposure criterion

`occupational_limit_local_standard` is registered with explicit scope: the
criterion depends on jurisdiction and exposure duration/averaging, and employer or
project requirements apply only when relevant. NIOSH's 85 dBA 8-hour REL is a
recommendation, U.S. OSHA's permissible table uses duration-dependent values, and
UK HSE guidance uses its jurisdiction-specific daily/weekly action values. These
are different frameworks, not a single universal occupational limit. A point SPL
prediction for a valve must not be substituted for a worker's exposure assessment.

- [CDC/NIOSH occupational vs. environmental limits](https://www.cdc.gov/niosh/bulletin/2016/noise.html)
- [U.S. OSHA 29 CFR 1910.95](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.95)
- [UK HSE exposure assessment](https://www.hse.gov.uk/construction/healthrisks/physical-ill-health-risks/assessing-noise.htm)

## Additional verified anchor: sizing, velocity, and controllability trade-off

`valve_size_capacity_velocity_tradeoff` is supported with explicit operating
conditions. Baker Hughes' noise handbook identifies adequate valve sizing as one
means to keep outlet velocity appropriate; Emerson's Control Valve Handbook
describes the separate consequence of oversizing, including low-travel operation
and reduced usable turndown. The registered claim does not assert a universal
velocity reduction from nominal body size alone; it is conditioned on comparable
service/flow conditions and effective area, and it requires checking the full
operating range.

- [Baker Hughes, Masoneilan Noise Control Handbook](https://dam.bakerhughes.com/m/403871c7a460561b/original/Masoneilan-Noise-Control-Handbook-English.pdf), §3.1.1, pp. 9–10.
- [Emerson, Control Valve Handbook, 6th edition](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf), Chapter 2, Control Valve Performance.

## Additional verified anchor: pipe-wall transmission loss

`pipe_transmission_loss_dependency` is registered score-neutrally. IEC 60534-8-3:2010
calculates frequency-dependent pipe transmission loss, includes pipe-wall thickness,
pipe density and downstream-fluid density/sound-speed variables, and limits the
prediction method to steel and steel-alloy pipe. Emerson's Control Valve Handbook
explains that pipe-wall material, size and shape affect transmission and that the
external spectrum is estimated using the internal spectrum and frequency-dependent
transmission loss. The claim is therefore supported as a scoped prediction-model
dependency; it is not a universal formula for every material or service.

- [IEC 60534-8-3:2010, Introduction, Scope, and §5.5](https://preview.sist.si/sist-preview/16408/a97f3b244712460f9258b29366d3b0ae/IEC-60534-8-3-2010.pdf)
- [Emerson, Control Valve Handbook, 6th edition, Chapter 5](https://www.emerson.com/is/content/emerson/es/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf)

## Additional verified anchor: diffuser pressure-drop and service review

`diffuser_pressure_drop_distribution` is registered score-neutrally. Valmet's gas/
steam manual describes splitting pressure drop with a downstream fixed-area diffuser
for suitable high and relatively constant pressure-drop services; it calculates
diffuser capacity at maximum flow, treats valve and diffuser acoustic output
separately, and warns that excessive diffuser annular velocity can regenerate noise
or limit attenuation. The manual also requires lower velocities for impurity or wet-
steam cases to prevent erosion. Emerson/Fisher likewise describes an inline diffuser
as a fixed restriction that raises valve backpressure, while explicitly limiting
effectiveness to the sized condition and excluding throttling use. Therefore the
anchor is interpreted as a conditional design review, not a universal diffuser rule.

- [Valmet, Flow Control Manual, Gas and Steam Flow, “Diffusers” and velocity guidance](https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/)
- [Emerson/Fisher D103540X012 Reference Manual, Fig. 6-2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf)

## Additional verified anchor: integrated assessment scope

`control_valve_noise_scope` is registered as an engineering assessment framework,
not a fixed workflow mandated by one standard. The separate IEC methods support
the acoustic-quantity/source-mechanism distinction: Parts 8-1 and 8-2 define lab
measurement methods for aerodynamic and hydrodynamic flow respectively; Parts 8-3
and 8-4 provide distinct prediction methods and scopes. ISA75.07's committee scope
includes lab/field measurement and prediction or verification, while Valmet
describes source treatment separately from transmission-path treatment. Together
these sources justify connecting mechanism, path, mitigation and suitable field
verification in an application-specific evaluation. They do not mean every
prediction requires field measurement or that aero/hydrodynamic methods are
interchangeable. `score_effect=none`.

- [IEC 60534-8-1:2005](https://webstore.iec.ch/en/publication/2472)
- [IEC 60534-8-2:2011](https://webstore.iec.ch/en/publication/2473)
- [IEC 60534-8-3:2010](https://webstore.iec.ch/en/publication/2474)

## Unresolved anchor review: flashing noise and vibration

The legacy anchor `flashing_two_phase_noise` states that persistent flashing two-phase
flow and droplet impact can produce broadband noise and vibration. I did not register
it as verified. The evidence located is not sufficiently consistent to support that
combined general statement:

- Emerson's control-valve flashing guidance describes persistent vapor/liquid flow and
  droplet impact as erosion/damage mechanisms, but does not establish broadband noise
  or vibration as a necessary or generally expected result. Its Fisher technical
  sourcebook specifically reports that pure flashing applications did not create
  noise problems in the vendor's field experience. [Emerson flashing guidance](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/valve-flashing),
  [Fisher Sourcebook — Oil and Gas](https://www.emerson.com/is/content/emerson/en/final-control/pressure-management/jt-valves/documents/guide-control-valve-sourcebook-oil-gas-fisher-en-135836.pdf)
- A published pressure-reducing-valve case study identifies flashing noise from
  deceleration/expansion of two-phase flow, but its operating case also includes
  cavitation and does not establish a universal broadband spectrum or isolate vibration
  caused by flashing alone. [Ulanicki et al., Measurements and Analysis of Cavitation in a Pressure Reducing Valve During Operation — A Case Study](https://www.sciencedirect.com/science/article/pii/S1877705815024762)
- Emerson separately confirms that intense valve vibration can affect control and
  positioner performance, but that general statement does not attribute the vibration
  specifically to flashing. [Emerson, Control Valve Vibration](https://www.emerson.com/no-no/automation/valves/controlvalves/control-valve-vibration)

Disposition: remain unresolved. Do not treat erosion/droplet impact, acoustic noise,
and mechanical vibration as interchangeable consequences. Revisit only if the claim is
narrowed to a supported application or a primary study isolates flashing from cavitation
and other excitation mechanisms. `score_effect` remains `none`; no grading behavior or
anchor text was changed.

## Unresolved anchor review: operating-case noise matrix

The legacy anchor `operating_case_noise_matrix` requires noise prediction at minimum,
normal, maximum, startup, and shutdown conditions. There is direct support for part of
this requirement: IEC 60534-7's control-valve data sheet calls for predicted sound
pressure levels at minimum, normal, and maximum flow, calculated using IEC 60534-8-3
or IEC 60534-8-4. Emerson's Control Valve Handbook also says process conditions during
startup, normal operation, and shutdown should be supplied for the engineering review,
and calls for a maximum permissible noise level and reference point when pertinent.
[IEC 60534-7:2010](https://webstore.iec.ch/en/publication/2471), [public text excerpt](https://preview.sist.si/sist-preview/15859/c81f8fbf53c94f3eafd62560efa2e4ea/IEC-60534-7-2010.pdf),
[Emerson Control Valve Handbook, Chapter 5](https://www.emerson.kr/is/content/emerson/ko/final-control/isolation-valves/documents/control-valve-handbook-en-3661206.pdf).

The cited material does not explicitly require a separate noise prediction for every
startup and shutdown transient. As written, the anchor combines mandatory min/normal/max
flow reporting with transient-case prediction without stating that transient cases are
included when they are specified and relevant. I therefore leave this anchor unresolved
rather than infer the extra requirement. `score_effect` remains `none`; source anchor
text and grading behavior were not changed.

## Unresolved anchor: flashing two-phase noise

`flashing_two_phase_noise` remains **unverified** as worded. The persistent liquid-
vapor mixture and associated high-velocity flow can cause erosion and vibration,
but the stronger combined claim that flashing droplet impact produces broadband
noise is not established by the sources reviewed. The sources also disagree in
emphasis: Valmet says flashing flow can cause vibration/erosion, notes that no
flashing-valve noise prediction method is currently available, and reports typical
levels below 85 dB(A); Emerson/Fisher reports field investigations that did not
identify pure-flashing applications as noise problems and says an appropriate
two-phase prediction method does not exist; Samson discusses lower-level noise
excitation in two-phase flow and pipeline vibration from outlet shock waves.
These observations do not prove broadband spectral content. Do not infer that all
flashing services are acoustically quiet, but do not mark the present broadband
noise mechanism verified either. `score_effect` remains absent from the Fact
registry.

- [Valmet, Flow Control Manual, Liquid Flow, §3.3.3 and §3.4](https://www.valmet.com/flowcontrol/valves/flow-control-manual/liquid-flow/)
- [Emerson/Fisher D103540X012 Reference Manual, hydrodynamic-noise section](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103540x012.pdf)
- [Samson, Control Valves for Critical Applications, flashing/two-phase discussion](https://www.samsongroup.com/document/w01040en.pdf)

## Unresolved anchor: low-noise trim capacity/rangeability trade-off

`low_noise_trim_capacity_rangeability_tradeoff` remains **unverified as a combined
claim**. Emerson/Fisher's published engineering article documents that traditional
multi-flow-path/noise-attenuation trims often reduce maximum flow capacity and may
require a larger valve in the described applications. But it is not a universal
limit: Emerson's later Whisper NXG product material reports increased capacity
while retaining specified noise abatement. More importantly, the anchor joins
maximum `Cv` capacity and `rangeability` as though both necessarily trade against
noise reduction. Valmet defines inherent rangeability in terms of maximum and
minimum controllable `Cv`, and installed rangeability in terms of flow/gain limits;
that metric is not established by evidence that a particular trim reduces rated
capacity. Therefore only the capacity trade-off is supported for some traditional
designs. The full anchor should remain unresolved until narrowed to application-
and trim-specific capacity/control-range checks. No registry record was added.

- [Emerson/Fisher, Noise Abatement Selection](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d353361x012.pdf), pp. 2–3
- [Emerson, Fisher Whisper NXG noise-reduction product description](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/control-valve-noise-reduction)
- [Valmet, Rangeability—Ask the flow control expert](https://www.valmet.com/insights/articles/flow-control/flow-control-expert3/)

## Additional verified anchor: dirty-service compatibility review

`plugging_erosion_maintenance_tradeoff` is verified as a **selection review**, not
as a claim that all small-passage or multistage trims necessarily plug or erode.
Fisher's noise-attenuation brochure describes small-passage Whisper noise trims and
separately presents a large-open-area Dirty Service Trim that allows particulates
and is designed to limit plugging/erosion. The DST product bulletin documents
particle-size limits, reduced clearance-flow erosion, and in-line removal for
inspection. This supports checking actual particle size/type, passage geometry,
service erosion exposure and inspection access, while keeping dirty-service
ratings product-specific. It does not transfer the DST particle rating to a
noise-attenuation trim or define a universal maintenance interval. `score_effect=none`.

- [Emerson/Fisher, Noise-Attenuation Technologies for Control Valves, D351989X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d351989x012.pdf), pp. 12–13
- [Emerson/Fisher, Dirty Service Anti-Cavitation Trim Bulletin 80.2:021, D102310X012](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d102310x012.pdf), pp. 1, 3–5
- [Emerson, Fisher Dirty Service Trim product page](https://www.emerson.com/en/final-control/products/fisher-dst)

## Additional verified anchor: vendor prediction cross-check fields

`vendor_crosscheck_noise` is verified with conditions on method and operating
case. IEC 60534-8-3 defines an aerodynamic prediction method that relates internal
frequency-dependent noise and downstream pipe transmission to external SPL;
IEC 60534-8-2 is a distinct hydrodynamic laboratory-measurement method with
controlled test conditions including measured travel. Fisher's noise catalog
distinguishes octave-band levels from overall SPL and describes source/path
treatments and observation-distance correction. Therefore a reviewer should
cross-check the source-side quantity, spectrum, external SPL, travel and mitigation
against the method and case actually used. These are relevant cross-check fields,
not a claim that every vendor report must contain one universal set or that
aerodynamic prediction and hydrodynamic measurement are interchangeable.
`score_effect=none`.

- [IEC 60534-8-3:2010](https://webstore.iec.ch/en/publication/2474)
- [IEC 60534-8-2:2011](https://webstore.iec.ch/en/publication/2473)
- [Emerson/Fisher, Catalog 12, Section 3 (2018)](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/cat12_s3.pdf)
- [IEC 60534-8-4:2015](https://webstore.iec.ch/en/publication/23315)
- [ISA75.07 committee scope](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa75-07)
- [Valmet, source and path treatment](https://www.valmet.com/flowcontrol/valves/flow-control-manual/gas-and-steam-flow/)

## Additional verified anchor: prediction–measurement gap checklist

`prediction_measurement_gap_diagnosis` is registered as a score-neutral diagnostic
checklist, not as a mandated universal sequence or proof of a particular fault.
IEC 60534-8-3 defines a scoped prediction method with explicit fluid, valve and
downstream-pipe assumptions and calculates external sound pressure using pipe
transmission; applicability and input/regime/pipe mismatch are therefore sensible
checks before attributing a residual. ISA75.07 confirms that valve-noise measurement
and prediction/verification are distinct related activities. ISO 1996-2 provides a
general environmental sound-pressure determination framework, so observation
conditions, acoustic environment/reflection and background must be interpreted under
the measurement method actually used. These sources support checking the listed
factors, but do not prescribe the exact order or a control-valve-specific diagnostic
cause hierarchy. The order remains a practical checklist only. `score_effect=none`.

- [IEC 60534-8-3:2010](https://webstore.iec.ch/en/publication/2474)
- [ISA75.07 committee scope](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa75-07)
- [ISO 1996-2:2017](https://www.iso.org/standard/59766.html)

## Unresolved anchor: operating-case noise matrix

`operating_case_noise_matrix` remains unverified as stated. Evaluating minimum,
normal and maximum steady operating points can be an appropriate project design
practice when those cases are defined and the selected prediction method applies.
However, IEC 60534-8-3 specifies a theoretical method for single-phase dry gas/vapour
and listed valve/downstream-pipe configurations; it does not make a universal
minimum/normal/maximum plus startup/shutdown matrix mandatory, and a steady-state
method must not be assumed to model startup/shutdown transients. Keep this anchor
unpromoted unless narrowed to a project-specific case matrix and method-validity
check. `score_effect` remains absent from the Fact registry.

- [IEC 60534-8-3:2010, scope and method description](https://webstore.iec.ch/en/publication/2474)

## Additional verified anchor: source–path–receiver accounting

`source_path_receiver_hierarchy` is registered as a system-analysis framework.
ASHRAE explicitly models source, airborne/structureborne path, and receiver, and
states that received sound depends on observation point and room/acoustic context.
Valmet's control-valve material separates source treatment from attenuation of
already-generated sound along the path. IEC 60534-8-3 links generated aerodynamic
noise to downstream pipe transmission loss and external sound. This supports
keeping those terms distinct and preventing the same modeled attenuation from
being credited again as an independent treatment. It does not prescribe one
universal mitigation order, nor does it imply interacting treatments have
independent additive effects. `score_effect=none`.

- [ASHRAE Handbook—HVAC Applications (2019), Chapter 49, §§1–2 and 2.5](https://handbook.ashrae.org/Handbooks/A19/IP/a19_ch49/a19_ch49_ip.aspx?quantity=1)
- [Valmet, Finding the source of all that noise](https://www.valmet.com/insights/articles/flow-control/finding-the-source-of-all-that-noise/)
- [IEC 60534-8-3:2010](https://webstore.iec.ch/en/publication/2474)
