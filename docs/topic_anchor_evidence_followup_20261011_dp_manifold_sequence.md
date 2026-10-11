# DP transmitter manifold sequence follow-up — 2026-10-11

## Unresolved: isolation and return valve sequences

The anchors `manifold_isolation_sequence` and `manifold_return_sequence` remain
unverified as universal procedures. Their sequence includes a separate bleed/vent
operation while describing a “3-valve” manifold; a conventional 3-valve block has
two block valves and one equalizing valve, while bleed/vent capability may be a
separate fitting or part of a different 5-valve assembly. The exact valve names,
arrangement and pressure-retaining cavities therefore need to be identified before
prescribing a sequence.

Emerson's Rosemount 3051 reference manual gives a model/configuration-specific
procedure: its zeroing sequence closes the low-pressure isolate before opening the
equalize valve, and the return-to-service procedure opens the low-side isolate under
the stated equalized/isolated conditions. The 3051S manual also provides 3- and
5-valve-specific arrangements. These manufacturer procedures do not establish one
mandatory H-first shutdown or return order for every manifold, transmitter, process,
or vent arrangement. In particular, the anchor's `H close → equalizing open → L
close → bleed open` and `bleed close → L open → equalizing close → H open` are not
promoted without matching the exact installed equipment manual and safe handling of
trapped process pressure.

This is an evidence/disposition record, not an instruction to operate a live
installation. Do not alter a field valve sequence from this note. `score_effect`
remains absent from the Fact registry.

- [Emerson, Rosemount 3051 Pressure Transmitter Reference Manual, July 2020](https://www.emerson.com/content/dam/emerson/en/measurement-instrumentation/technical/products/pressure/documents/dl-rmt-3051-pressure-transmitter-76002.pdf), manifold operation and zeroing procedure
- [Emerson, Rosemount 3051S Reference Manual, December 2025](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051s-00809-0100-4801.pdf), 3-valve and 5-valve operation procedures
- [Emerson, Instrument Manifolds](https://www.emerson.com/en/measurement-instrumentation/catalog/pressure-measurement/instrument-manifolds), manifold functions and configuration families
