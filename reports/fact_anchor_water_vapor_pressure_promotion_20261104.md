# Water vapor-pressure Fact: current-claim promotion review

Date: 2026-11-04. Independent technical reviewer: `gpt-6-luna`
(delegated agent model configured for this review). Deterministic contract
and source-hash validation owner: Codex. Decision: `KEEP_BOUNDED` for question-specific general
scoring eligibility, not automatic inclusion in every cavitation question.
This is AI review under the user's delegated approval; it is not human review.

| Fact ID | Exact current Topic Anchor statement | Disposition | Primary evidence and scope |
|---|---|---|---|
| `lower_temperature_reduces_water_vapor_pressure_at_fixed_composition` | 물의 액체-증기 평형 범위에서 온도를 낮추면 포화증기압 Pv가 낮아진다. 조성과 절대압력 분포가 동일하다면 Pvc·P2와 Pv 사이의 압력 여유가 커질 수 있지만, 이 사실만으로 캐비테이션·플래싱 또는 손상 방지를 보장하지 않는다. | `KEEP_BOUNDED` | IAPWS water saturation-pressure table supports the water-specific Pv trend. Pvc/P2 margin follows by subtraction only if those pressures stay fixed. No universal valve-damage prevention is claimed. |

Primary source: International Association for the Properties of Water and
Steam, [FAQs About Water and Steam](https://iapws.org/faqs/faq1), “What is the
effect of pressure on the boiling of water?” and adjacent water vapor-pressure
table: 25 °C / 0.00317 MPa; 100 °C / 0.1014 MPa (accessed 2026-11-04).
The [IAPWS saturation-properties release](https://www.iapws.org/relguide/Supp-sat.html)
confirms saturation pressure is a function of temperature for ordinary water.

For the valve boundary, [Emerson Control Valve Flashing](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/valve-flashing)
uses downstream pressure versus vapor pressure to identify flashing and
explicitly separates phase state from erosion severity. This is used only to
bound the valve inference, **not** to make a vendor-specific test result a
general scoring requirement.
The [Control Valve Handbook, 5th ed., ch. 5 §5.14.2](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d101881x012.pdf)
also identifies downstream pressure and operating-temperature vapor pressure
as application variables for flashing classification.

The Registry statement is already water-specific and includes unchanged
pressure/composition and no-damage-guarantee conditions. The Topic Anchor was
corrected on 2026-11-04 to match that scope. General scoring may credit this
fact only when cooling, water vapor pressure or applicable pressure margins
are within the actual question demand. It is not a mandatory answer element
for a generic valve sizing, cavitation diagnosis or flashing mitigation
question. Mixed fluids, non-equilibrium operation and a changed Pvc/P2
profile need separate analysis. The source does not support “cooling always
prevents cavitation or flashing.”

No scoring weight, fatal rule or A–E authority is changed by this admission.
The generic prevention question no longer requires this water-specific Fact;
a dedicated water-temperature question contract does. A focused regression
checks both selections. The promotion ledger pins the exact
current statement and Topic source hash; the executable source hold is removed
only through the reconciler and tested against the runtime exclusion API.

## Verification after admission

- Exact-ID promotion ledger: 104; remaining reviewed holds: 8.
- Executable overlays: 80 revision + 80 source/promotion + 276 original
  exclusions = 436 blocked; 2,092 - 436 = 1,656 non-blocked candidates.
- Focused Fact/reconciliation pytest: 13 passed; control-valve Topic
  regression: 27 passed. Both generic and water-specific question selections
  are asserted.
- Managed Topic promote, all-Topic integration, and `validate-all`: PASS.
- Full `PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0
  RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh`: exit 0 / PASS.
  The optional 10-run reproducibility gate was skipped by its existing
  opt-in contract. No live Telegram or container deployment was performed.
