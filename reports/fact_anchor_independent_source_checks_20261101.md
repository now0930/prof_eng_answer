# Independent primary-source spot checks — 2026-11-01

**Scope: 3 of the 1,290 currently queued Fact IDs**, NOT verification
of the full 1,290. No LLM agreement, historic Registry `verified` status,
or schema citation metadata alone was counted as an independent check.
Source material inspected: current publicly available HTML of the
issuing organization. Access date 2026-11-01.

## 1. multiple_and_absent_stability_crossings
- Topic/Anchor: `control_system_frequency_domain_stability_margins_bode_nyquist`
  (use the canonical Registry topic/Anchor for any automatic linkage).
- Source: MathWorks, [margin: Gain margin, phase margin, and crossover frequencies](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html), R2026b, sections “Margin Values,” “Tips” and “Output Arguments.”
- Primary material confirms: Gain and phase margins are defined at different
  crossing conditions; for several crossovers, `margin` returns the
  smallest/closest-to-zero margin, rather than blindly using the first.
  If the requested sampled frequency range has no 0-dB crossing, the
  relevant reported phase margin can be `Inf`. The API also warns that
  `margin(mag,phase,w)` may be less accurate because of interpolation.
- Decision: **KEEP with SISO/classical margin and frequency-range
  qualification**. The general concept is valid but do not infer a
  robust multivariable stability guarantee from these margins.
- New independent source check: YES (HTML). Do not claim review of every
  possible margin-return convention.

## 2. sw06_ci_identification_scope_and_examples
- Source: NASA, [Systems Engineering Handbook 6.5 Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/),
  §§6.5.1.1, 6.5.1.2.2, 6.5.1.3.
- Primary material confirms: the CM plan guides selection of items
  subject to configuration control; CI selection, associated documents,
  identifiers and baselines are defined as part of identification.
  NASA explicitly lists controlled items, documents, hardware, software
  and models as an output *when identified for control*. Not every
  possible asset is unconditionally a CI.
- Decision: **KEEP as project-scope-bounded general configuration
  management principle**; NASA's particular baseline taxonomy is not a
  mandatory universal implementation.
- New independent source check: YES (HTML).

## 3. osha_psm_scoped_management_of_change_requirements
- Source: U.S. OSHA, [29 CFR 1910.119](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119),
  §§(a)(1)-(2), (b) “Replacement in kind,” and (l)(1)-(5).
- Primary material confirms: PSM coverage applies to defined chemical
  processes and includes exclusions; MOC written procedures cover
  changes to specified process aspects affecting a **covered process**,
  except replacement in kind. Before change, assess technical basis,
  safety/health effect, procedure modifications, timing and authorization.
  Affected employees must be informed/trained before start-up.
- Decision: **KEEP as factually supported U.S.-specific regulation**,
  but **EXCLUDE from universal/generic professional-exam scoring
  references** because the scope is jurisdiction-specific.
- New independent source check: YES (HTML). No assertion that this
  regulation governs every plant or jurisdiction.

## Remaining limitations and next-review policy

- Queue size is 1,290 and current exclusion overlay contains 276.
- This report checks only 3 facts, **2 generally eligible (conditional)
  and 1 excluded/scoped**. The remaining 1,287 have *not* been
  independently compared with primary material in this new run.
- The separate full-Queue `fact_anchor_independent_verification_audit_20261101.csv`
  is a **metadata and identity reconciliation**, not external source
  reading. Previous Registry provenance remains unchanged.
- No complete `validate-all`, `validate_release.sh`, focused pytest,
  generated-bank rebuild or deployment was executed by this report.
