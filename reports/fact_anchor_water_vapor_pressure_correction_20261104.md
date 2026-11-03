# Water vapor-pressure Topic Anchor correction (held)

Date: 2026-11-04. Reviewer method: Codex source-to-claim comparison. This is
not a human approval, and the Fact is **not promoted to general scoring**.

- Fact ID: `lower_temperature_reduces_water_vapor_pressure_at_fixed_composition`
- Topic/Anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` /
  `reduce_liquid_temperature_prevention`
- Primary source: International Association for the Properties of Water and
  Steam, [FAQs About Water and Steam](https://iapws.org/faqs/faq1), section
  “What is the effect of pressure on the boiling of water?” and its
  water saturation-pressure table (checked 2026-11-04). The same site's
  [IAPWS-IF97 industrial formulation](https://www.iapws.org/relguide/IF97-Rev.html)
  identifies the saturation-curve domain.
- Source-to-claim mapping: the table rises from 0.00317 MPa at 25 °C to
  0.1014 MPa at 100 °C, supporting a lower saturation pressure when **water**
  is cooled within the liquid-vapor equilibrium range. At fixed absolute
  Pvc/P2 and composition, the difference between those pressures and Pv
  increases algebraically. This does not establish a changed valve pressure
  profile or damage-free operation.
- Previous Topic wording: “Liquid temperature를 낮추면 Pv가 감소하여
  cavitation·flashing margin을 늘릴 수 있다.” This was broader than the Registry's
  water-specific reviewed statement and omitted unchanged-pressure and
  no-guarantee qualifications.
- Change: narrow `statement`, `claim`, `accepted_explanations` and
  `source_basis` in the Topic source; add the same boundary to its README.
  The Registry's already-bounded statement remains unchanged. No scoring
  weight, requirement mapping, fatal rule or original-source review row changed.
- Hold: the original-source review refers to the prior Topic claim; this
  held Fact has no entry in the promotion ledger. A separate
  exact-current-claim admission review is still needed
  before removing the executable hold. The Topic correction is not itself
  evidence of successful grading calibration.

## Verification

- Focused Fact-hold/reconciliation pytest: 13 passed.
- Reconciliation: 1,290 reviewed; 103 promoted; 80 revision + 81
  source/promotion + 276 excluded = 437 blocked; unchanged.
- Managed single-Topic generated promotion and all-Topic integration: PASS.
  The 103 promoted statements stayed unchanged; the ledger's containing
  Topic-source hash was refreshed after this held Anchor changed.
- `rubric_manager.py validate-all`: PASS.
- `PROMOTE_GENERATED=0 RUN_SMOKE_TOPIC_PACKS=0
  RUN_GRADING_REPRODUCIBILITY=0 scripts/validate_release.sh`: exit 0 / PASS.
  The optional 10-run reproducibility gate was skipped by its opt-in contract.
- An exploratory full `pytest -q` run was interrupted after a long-running
  section at 34%; **do not represent that run as a full pytest PASS**. The
  complete repository Release Gate above did finish successfully.
