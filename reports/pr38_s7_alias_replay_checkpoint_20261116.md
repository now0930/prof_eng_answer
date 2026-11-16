# PR #38 / S7 B7: 47 Golden Alias inventory root-cause replay checkpoint (2026-11-16)

> **Status: IMPLEMENTED_NOT_EXECUTED — B7 remains OPEN.** The user-provided numbers are a **baseline expectation**, NOT values recreated in this commit. Do not label an ontology cause for any of the 179 projections until the ID-level replay artifact passes all baseline checks.

## Revision and privacy

- User-requested reference commit: `5e4fc40e8925ce147d6d08c838f993b12a563f18`; at start the remote PR HEAD equaled this exact SHA. PR #38 was Draft, Issue #39 open. The GitHub API exposes committed tree state but **cannot show uncommitted files in a user's separate local checkout**. Container `git ls-remote` failed due to `Could not resolve host: github.com`; existing `prof_eng_answer` directories and private data have not been touched.
- Implemented research-only tracing in `grading/evidence/s7_alias_root_cause_audit.py`; optional observer in `scripts/evaluate_claim_alignment_s7.py`; `scripts/diagnose_s7_alias_inventory.py`; focused synthetic guardrail tests; optional manual Action input `run_s7_alias_diagnostics` (default OFF). Normal scoring, Fact Registry, Golden, ontology, Topic Pack and generated banks unchanged.
- The observer receives the **same** actual 47 Golden grading/requirements/canonical-parser/alignment/surface-audit path; each row retains `case_id`, `owner_topic_id`, `fact_id`, `source_fact_id` and canonical relation Subject/Predicate/Object IDs, polarity, condition IDs. It never writes question or answer text.

## Gate to reproduce before candidate review

Use Actions → `validation` → PR feature branch → check **Run S7 Alias root-cause replay**. The required offline pytest step runs first. Optional alias analysis executes separately, with `continue-on-error: true` solely because it is a **non-gating research experiment**; the alias script itself exits `2` on baseline mismatch and does not modify ontology.

Alternatively, in a disposable CLEAN checkout at the current HEAD:

```bash
python3 -B scripts/diagnose_s7_alias_inventory.py \
  --output /tmp/s7_alias_inventory.json \
  --baseline-output /tmp/s7_baseline_same_run.json
```

All output files are new, must be outside the repository, and are created with mode 0600. The Action uploads **only** the ID-level `s7_alias_inventory.json` artifact for 7 days, **not** the Golden answer text or baseline full report. Artifact may be missing if the script aborts before recording evidence.

### User-specified EXPECTED baseline (must be newly observed)

| Field | Expected | Newly measured here |
|---|---:|---|
| Graded cases | 47 | NOT_RUN |
| Expected policy abstentions | 1 | NOT_RUN |
| ALIAS_INVENTORY_INCOMPLETE projections, with duplicates | 179 | NOT_RUN |
| Subject+Predicate+Object | 162 | NOT_RUN |
| Predicate+Object | 9 | NOT_RUN |
| Subject only | 6 | NOT_RUN |
| Subject+Object | 2 | NOT_RUN |
| Missing subject / predicate / object occurrences | 170 / 171 / 173 | NOT_RUN |
| Registry literal candidates / EXACT_RELATION | 0 / 0 | NOT_RUN |
| Unexpected baseline failures / alignment failures | 0 / 0 | NOT_RUN |
| score_admission | DISABLED | Code contract, runtime NOT_RUN |

## Diagnostics data contract

- `primary_cause_projection_counts` is an **exclusive** per-projection partition using a documented deterministic precedence among `INVALID_ALIAS_FORMAT`, `UNSUPPORTED_RELATION`, `ID_NOT_FOUND`, `EMPTY_ALIAS`, `OTHER`. Its five values must sum to exactly 179 when the baseline is reproduced.
- `component_cause_counts_non_partition` is **not** an exclusive projection count: one missing projection may contribute 1-3 reasons. The stated 170+171+173 missing components must not be mistaken for 179 unique Facts.
- `_load_aliases`: Subject/Object keys come from engineering concepts plus quantities; a default ID-derived alias is included even when explicit aliases are empty. `_load_predicates`: predicate keys come only from canonical_predicates and do not receive the same default. Diagnosis checks the **actual runtime lookup lists**, original raw ontology definition, and namespace/format separately.
- Row-level evidence includes `case_id`, owner, legacy Fact, verified Registry `source_fact_id`, relation identifiers, missing combination, original ontology alias definition and computed reason. Global unique Subject/Predicate/Object IDs and unique `(topic_id,fact_id)` are separately counted. Repeated Golden projections are preserved, not incorrectly deduplicated.
- The listed ontology IDs and raw aliases are an **inventory audit**, not validated engineering meanings. **No automatic aliases or SUPPORTED promotions.**

## Completion gate / stop condition

1. Await actual run; if `BASELINE_MISMATCH`, review mismatch differences and stop before any candidate or ontology edits. Do not back-fill `179` from aggregate historic reports.
2. Once `REPRODUCED_BASELINE` is actually observed with saved ID rows, independently review missing causes and per-ID source evidence, recognize ambiguity/false-positive risk, and assign explicit `ACCEPT/REVISE/REJECT/HOLD` recommendations.
3. Only independently supported minimal alias changes may be submitted in a separate commit with new negative tests. Compare baseline and after focused pytest, full offline pytest/Release Validation, S7 duplicate/unique alias counts, literal review candidates, actual Claim–Fact precision and false-positive risk separately. No accuracy gain claim from raw count increase.
4. Record actual run SHA, action URL, exit status, 47/179 comparison, artifact identifier, and remaining blockers on PR #38 and Issue #39. Keep PR Draft; do not merge, deploy, restart, create Fact, weaken tests, edit Generated by hand, or change scoring authority.

**Current stop:** ID-level 179 replay has not run. Step 4 technical classification and step 5/6 alias edits must NOT be marked complete.
