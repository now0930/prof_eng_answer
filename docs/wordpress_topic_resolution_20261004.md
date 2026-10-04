# WordPress Topic resolution, 2026-10-04

The owner delegated remaining relationship decisions to Codex in this session.
The attached LLM CSV was treated as recommendation data. The frozen resolution
report records its hash, the original export hash, accepted post/Topic pairs,
post and Topic snapshots, and a disposition for every logical CSV record.
The reviewer is `codex:user-delegated-20261004`, not a human reviewer.

## Applied result

- Reviewed recommendation set: 686 records.
- New approved relationships: 66 (56 existing candidates, 10 new mappings).
- Existing approved relationships retained: 29; catalog approved total: 95.
- Deferred records: 591 (478 pending candidates and 113 unmatched records).
- Added Master envelopes for 30 existing Topics; Master inventory is now 49.
- Applied 316 first-party source-reference proposals, including 30 previously
  pending references; Master references total 390.
- External source proposals retained as pending: 13 (7 PDF, 6 HTML).
- All 368 first-party PDFs already had extracted text; no PDF was downloaded
  or re-OCRed during this batch. Extraction state remained identical.

The source batch includes WordPress post, first-party PDF and image references.
Image references are metadata; no new image OCR was performed. All newly
applied references remain `unverified`: relationship relevance is not a claim
that formulas, handwritten OCR or technical explanations are correct.
Technical content promotion remains a separate proposal workflow.

## Evidence and deferrals

Stored post questions/body and Topic ownership were compared for approval
recommendations. Seven high-confidence recommendations were deferred for sparse
article/video pointers, unreadable handwritten OCR, adjacent-topic scope,
title-only evidence or an already approved more precise Topic. Medium-confidence
rejection recommendations were not turned into rejected catalog links.

`reports/wordpress_topic_link_resolution_20261004.json` contains all record
dispositions. `reports/wordpress_topic_link_resolution_result_20261004.json`
contains application counts, the SQLite backup path, deferred external proposals
and validation log paths. The CSV remains unchanged. The catalog and its backup
are local data and are not committed; Master references and review audit reports
are committed. Reapplying an identical resolved link is a no-op; a different
decision cannot silently replace it.

## View and regression checks

Training and Diagnosis Views now expose copied source references, and Feedback
preserves them. Existing learning-history feedback snapshots are historical;
current sources can be read through Training View. Grading View remains the
same four legacy source payloads. New Masters may additionally retain an
optional question-demand-axes file reference without adding it to Grading View.

An initial integration run caught a fifth Grading View key in four newly
constructed Masters. Their projection configuration was corrected to preserve
the existing four-key contract; no test or release gate was weakened.

Validation completed:

- Review transaction rollback, duplicate attachment handling, reviewer identity,
  idempotent retry and resolved-decision preservation.
- All 49 Master schemas, three projections and learning integration.
- All 95 approved post links have their post reference in the related Master.
- Two-item daily queue loads current Training View source references using an
  isolated history database; actual learner history was not changed.
- Full non-promoting release suite and `validate-topic-pack-release --all`.
- SQLite integrity and foreign keys, unchanged PDF extraction snapshots and
  unchanged legacy Topic sources/generated banks.

Optional live LLM smoke and the dedicated 10-run reproducibility gate were not
run because this batch does not change scoring or model transport. No bot
deployment or external message was performed.

The batch is complete for supported relationships and provenance. Deferred
items are explicitly recorded work requiring better source evidence, not
implicitly approved links or completed content verification.
