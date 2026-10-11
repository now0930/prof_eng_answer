# Fail-open gas control-valve flow anchor — evidence review, 2026-10-11

## Anchor and disposition

Topic: `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`  
Anchor: `fail_open_maximum_flow_case`  
Fact: `fail_open_gas_valve_flow_uses_credible_case_pressures_and_choke_check`  
Status: verified/approved; `score_effect=none`.

The anchor is registered with a deliberate condition: maximum upstream pressure
and minimum downstream pressure may be paired only if they are credible and can
coincide in the same process/relief scenario. Independent extrema from unrelated
cases must not be combined mechanically.

## Evidence

- Fisher/Rosemount's *Control Valve Primer*, Chapter 5, pp. 24–26, gives gas flow
  equations in terms of absolute `P1`, `P2`, temperature, gas properties and valve
  coefficient. It distinguishes subcritical from critical flow and explicitly asks
  whether a fail-open valve's resulting flow could exceed downstream relief
  capacity. It also cautions that the correct process inlet pressure must account
  for pump head at the maximum flow being passed, static head, equipment pressure
  losses and line losses. [ISA chapter PDF](https://www.isa.org/getmedia/c37b8eb0-dbf9-4cb8-a29a-aac88db297a0/Baumann-ControlValvePrimer_Chapter5.pdf)
- IEC 60534-2-1:2011 provides installed-condition equations to predict compressible
  and incompressible flow through control valves. This supports using valve sizing
  equations and applicable gas/choke parameters; it does not prescribe one
  universal pair of high/low pressures for every failure scenario.
  [IEC publication page](https://webstore.iec.ch/en/publication/2461)
- API 521 is the applicable standard family for pressure-relieving/depressuring
  system design; the actual relief scenario, coincident relieving conditions,
  permitted outlet credit and required relieving rate remain subject to the
  governing edition and plant-specific relief basis.
  [API Standard 521 scope](https://www.api.org/products-and-services/standards/important-standards-announcements/standard521)

## Limits

This Fact does not claim that the valve flow alone equals the complete relief load,
that a single valve failure always governs the relief case, or that unrelated
maximum/minimum pressures can be combined. `score_effect` remains `none`.
