# Independent primary document comparison — Fisher actuator sizing, 2026-11-01

Manufacturer document: Fisher/Emerson, actuator sizing example, https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103428x012.pdf ; section with figure 6, force available and selection of spring. Public PDF search text inspected, not a visual page inspection.

1. `sliding_stem_actuator_force_includes_seat_load_unbalance_and_friction` — KEEP_BOUNDED. Worked force balance explicitly accounts for seat load, packing friction and fluid unbalance. Sign and load components depend on stroke direction, geometry and stated shutoff case. Not a universal sum of unsigned magnitudes for all conditions.
2. `fisher_actuator_force_depends_on_diagram_pressure_and_effective_area` — KEEP_BOUNDED. Available diaphragm thrust given by supply pressure times effective area (using pressure differential against its reference), then subtract spring forces. This is an ideal pressure force term, not total net force or stroke-invariant effective area.

Only the named propositions are confirmed against this original manufacturer example; the full canonical Topic Pack paragraphs were not inspected and no broader grading claims are authorized.
