# S7 B7 — Three-context AI cross-review matrix (2026-11-19)

## Scope and limits

Three Codex subagents ran in separate contexts: Engineering, Semantics, and Adversarial. Each received only the 37-case anonymous reviewer export and its five source Fact records. They were instructed not to inspect the public correction proposal, author audit/key, source packet, private code map, Issue comments, or another agent's output. Each returned a disposition for all 37 blind case IDs.

These are **AI review opinions**, not independent human-expert labels, adjudication, or accuracy evidence. A source citation is evidence offered by an agent; unavailable source text remains unresolved. Risk dispositions are not answer labels. No result was written to the private `review_results.json`.

Engineering's whole-answer status and Semantics' whole-answer status agree on 22 of 37 rows. The 15 differing rows are listed explicitly in the final column. Their status vocabularies are preserved; they are not converted into a gold label. The Adversarial column is a separate risk dimension (13 false-acceptance risks, 5 false-rejection risks, 6 ambiguous-context holds, 13 no-major-risk observations).

## Case-by-case matrix

| Blind case | Engineering | Semantics: assertion / relation / whole answer | Adversarial risk | Disagreement or review note; evidence key |
|---|---|---|---|---|
| B7-0786F1D804A8 | CONTRADICTED | ASSERTED / MIXED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Same whole-answer outcome; correct construction dependence is mixed with an unsupported absolute equality. EHF §5.11.1.1. |
| B7-0815248398D4 | PARTIAL | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | Broad agreement; approval, identified configuration, and point-in-time qualifiers are incomplete. ISO §3.10.7; NIST 03.04.01. |
| B7-10213E991C99 | UNRESOLVED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | **Disagreement:** Engineering could not retrieve EHF; Semantics found the bounded claim supported. Primary-source check in this review session confirmed EHF describes flow-up port area and configuration-dependent stem/balanced-valve residual area. EHF §5.11.1.1. |
| B7-1426DE976954 | CONTRADICTED | ASSERTED / MIXED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Same whole-answer outcome; correspondence is followed by a counterclaim excluding design-stage relation. SEI, Traditional V Model. |
| B7-16332DE1FED5 | CONTRADICTED | ASSERTED / UNRESOLVED / UNRESOLVED | AMBIGUOUS_CONTEXT | **Disagreement:** Engineering treats equivalence to the complete contour as contradicted; Semantics and Adversarial hold because required representation/system context is underspecified. UW, complete RHP contour and mapped segments. |
| B7-168289E8E3CE | PARTIAL | ASSERTED / PARTIAL / PARTIAL | FALSE_REJECTION_RISK | Technical views agree on partial support; Adversarial cautions against rejecting solely because approval evidence is described as a separate check. ISO §3.10.7; NIST 03.04.01. |
| B7-1A5017D9F431 | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: reverses direction-reversal and no-observable-output-change behavior. McMillan §1.5, pp. 61–62. |
| B7-1CFEA6547D79 | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: recency alone does not establish approved-baseline status. ISO §3.10.7; NIST 03.04.01. |
| B7-1DD655E67FB5 | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | Agreement: describes an input interval after reversal with no observed output change. McMillan §1.5, pp. 61–62. |
| B7-24D02801A7BC | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | Agreement: a point-in-time configuration record is used as a reference for later change. ISO §3.10.7; NIST 03.04.01. |
| B7-2E764A13AF01 | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: deadband and stiction are not interchangeable definitions. McMillan §1.5, pp. 61–62; ISA InTech, Fig. 5 discussion. |
| B7-346601F43F72 | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | Agreement: development activities correspond to later verification/testing activities. SEI, Traditional V Model. |
| B7-35D530C17279 | UNRESOLVED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | **Disagreement:** Engineering could not retrieve EHF; Semantics treats categorical independence from nominal seat area as contradicted. Official EHF text accessed in this review session supports configuration dependence, but the agent's original unresolved disposition is retained. EHF §5.11.1.1. |
| B7-3C61E54EF624 | SUPPORTED | ASSERTED / PARTIAL / PARTIAL | AMBIGUOUS_CONTEXT | **Disagreement:** Engineering accepts the stated partial frequency-response relation; Semantics marks the whole answer partial, while Adversarial asks whether other contour segments/symmetry are accounted for. ETH L1809, pp. 17–20; UW, mapped contour segments. |
| B7-41C08292BB0F | PARTIAL | QUOTED / NO_ASSERTION / NO_ASSERTION | AMBIGUOUS_CONTEXT | **Disagreement:** technical content is not the issue; whether the row itself asserts the quoted proposition differs. Preserve assertion-context uncertainty. SEI, Traditional V Model. |
| B7-52EA69D345F1 | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | FALSE_REJECTION_RISK | Agreement on support; Adversarial flags risk of rejecting the valid distinction between an approved baseline and merely newest file. ISO §3.10.7; NIST 03.04.01. |
| B7-55A6CEDD74B9 | SUPPORTED | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | **Disagreement:** Engineering reads the reversal/no-response interval as sufficient; Semantics finds the input-range wording imprecise. McMillan §1.5, pp. 61–62; ISA InTech deadband diagnosis. |
| B7-5F8DFE1BE114 | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | Agreement: definition and test-condition-specific magnitude are bounded. McMillan §1.5, pp. 61–62. |
| B7-61D02AD6F2D9 | SUPPORTED | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | **Disagreement:** Engineering accepts correspondence with project-specific test detail; Semantics sees omitted scope as partial. SEI, Traditional V Model. |
| B7-6923C7A71EC8 | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: denies the reference role and equates baseline to newest file. ISO §3.10.7; NIST 03.04.01. |
| B7-7E55520CBD9E | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: replaces stage correspondence with a single-test claim. SEI, Traditional V Model. |
| B7-7EB5D3B9E2EB | SUPPORTED | QUOTED / NO_ASSERTION / NO_ASSERTION | AMBIGUOUS_CONTEXT | **Disagreement:** Engineering grades the quoted proposition's technical content; Semantics does not treat reported quotation as an asserted Claim. McMillan §1.5, pp. 61–62. |
| B7-8097B0A47C77 | SUPPORTED | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | **Disagreement:** Engineering considers the concise correspondence sufficient; Semantics expects more of the V-model scope. SEI, Traditional V Model. |
| B7-8C7072AB1D7C | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: reverses which half-plane the stated contour encloses. UW, complete RHP contour. |
| B7-9D3F8FE98AD2 | PARTIAL | ASSERTED / PARTIAL / PARTIAL | FALSE_REJECTION_RISK | Agreement on partial support; Adversarial warns not to reject the mapping claim solely for omitting the RHP qualifier. UW, contour and (L(s)) mapping. |
| B7-9F443D29ADB1 | SUPPORTED | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | Agreement: states the RHP enclosure and mapping into the complex plane. ETH L1809, pp. 17–20; UW, complete RHP contour. |
| B7-A5CA12F4F7BD | PARTIAL | QUOTED / NO_ASSERTION / NO_ASSERTION | AMBIGUOUS_CONTEXT | **Disagreement:** Engineering evaluates proposition content; Semantics finds no assertion; Adversarial holds on attribution/application context. UW, complete RHP contour. |
| B7-AEFD97346CE7 | PARTIAL | ASSERTED / SUPPORTED / SUPPORTED | NO_MAJOR_RISK | **Disagreement:** Engineering requires a test-condition or magnitude bound; Semantics finds the core definition supported. McMillan §1.5, pp. 61–62. |
| B7-C49B351137E3 | PARTIAL | MIXED / PARTIAL / PARTIAL | AMBIGUOUS_CONTEXT | Same broad partial outcome; whether the statement reports a claim or asserts approval remains unclear. ISO §3.10.7; NIST 03.04.01. |
| B7-C7B8B552DD47 | UNRESOLVED | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | **Disagreement:** Engineering withholds judgment because EHF retrieval failed; Semantics finds a partial geometry-dependent relation. Official EHF text accessed in this review session supports configuration-specific net unbalance area. EHF §5.11.1.1. |
| B7-D3228B9AE7D3 | UNRESOLVED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | **Disagreement:** Engineering could not retrieve EHF; Semantics finds the denial of construction dependence contradicted. Official EHF text accessed here describes port, stem, and balanced-valve configuration differences. EHF §5.11.1.1. |
| B7-DD278DE0AD3A | CONTRADICTED | ASSERTED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement: reverses the V-model mapping relation. SEI, Traditional V Model. |
| B7-E0700E2AF54D | CONTRADICTED | MIXED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement on whole answer: a supported definition is followed by its direct negation. McMillan §1.5, pp. 61–62. |
| B7-E731E3EC4526 | PARTIAL | ASSERTED / PARTIAL / PARTIAL | FALSE_REJECTION_RISK | Broad agreement on partial support; Adversarial warns against making every concise answer restate all definition qualifiers. ISO §3.10.7; NIST 03.04.01. |
| B7-EC19E434EBDD | CONTRADICTED | MIXED / CONTRADICTED / CONTRADICTED | FALSE_ACCEPTANCE_RISK | Agreement on whole answer: same contour is described and then denied. UW, complete RHP contour. |
| B7-EEA70A36D1BA | UNRESOLVED | QUOTED / NO_ASSERTION / NO_ASSERTION | FALSE_REJECTION_RISK | **Disagreement:** Engineering withholds technical judgment due EHF retrieval failure; Semantics says the answer reports an unconfirmed quote, not an asserted equality. Do not convert the quoted claim into an answer error. EHF §5.11.1.1. |
| B7-F57A3BF55B08 | UNRESOLVED | ASSERTED / PARTIAL / PARTIAL | NO_MAJOR_RISK | **Disagreement:** Engineering could not retrieve EHF; Semantics sees a partial net-area statement. Official EHF text accessed here supports net pressure differential × net unbalance area and construction dependence. EHF §5.11.1.1. |

## Primary-source key

- **ISO** — [ISO/TC 176 Standards Alphabetical Listing (PDF)](https://committee.iso.org/files/live/sites/tc176sc1/files/Terms%20in%20TC%20176%20Standards%20Alphabetical%20Listing%20V1%202022%2009%2029.pdf), p. 8, configuration baseline, ISO 9000:2015 §3.10.7.
- **NIST** — [SP 800-171 Rev. 3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP-800-171r3.html), §03.04.01 and glossary entry “baseline configuration.”
- **EHF** — [Emerson Fisher Control Valve Handbook, 6th ed. (PDF)](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/valves/documents/control-valve-handbook-en-3661206.pdf), §5.11.1.1, “Unbalance Force.” The Engineering agent could not retrieve it; the primary review session accessed the official Emerson PDF search excerpt supporting net pressure differential × net unbalance area, flow-up port area, and configuration-dependent stem/balanced-valve area.
- **SEI** — [CMU Software Engineering Institute, “Using V Models for Testing”](https://www.sei.cmu.edu/blog/using-v-models-for-testing/), “The Traditional V Model.”
- **MCM** — [ISA-hosted McMillan excerpt, *Essentials of Modern Measurements and Final Elements* (PDF)](https://www.isa.org/getmedia/eb76a613-3961-4db0-8efe-a91dc308ec68/Essentials-of-Modern-Measurements_McMillan_Chapter-1-Essentials.pdf), §1.5, printed pp. 61–62.
- **IEC** — [IEC 60534-9:2007 official publication page](https://webstore.iec.ch/en/publication/2477), response-measurement scope; cited alongside MCM for deadband context, not as the only evidence for the definition.
- **ETH** — [ETH Zürich, Control Systems I Lecture 9: The Nyquist Condition (PDF)](https://ethz.ch/content/dam/ethz/special-interest/mavt/dynamic-systems-n-control/idsc-dam/Lectures/Control-Systems-1/Lectures/L1809_Nyquist.pdf), Nyquist contour and mapped segments, pp. 17–20.
- **UW** — [University of Washington, Nyquist Stability](https://faculty.washington.edu/chx/teaching/fbintro/lec24-nyquist-criterion/), “The complete right-half-plane contour” and mapped contour segments.
- **NIST/SEI/ETH/UW/IEC/ISO/EHF/MCM references above** are source pointers for the AI opinions only. They do not establish reviewer independence or constitute adjudicated labels.

## Outcome and boundaries

- No technical correction was applied to the existing proposal document from this cross-review alone. Its cited source claims were not shown to be false by the three assessments; where agents differed, the matrix records the difference and official-source boundary rather than silently choosing a label.
- Six effective-area dispositions were unresolved for Engineering only because its retrieval failed; official Emerson source text was accessible in the integrating session. Those agent opinions remain recorded as returned, with source-access disagreement explicit.
- Case-level differences are review leads, not labels. All 37 remain `PENDING`; independent human review remains absent. `accuracy_status=NOT_ESTABLISHED`, `source_match_proven=false`, `score_admission=DISABLED`, and `score_effect=none`.
- The original synthetic negative cases, source packet, private reviewer bundle, Registry, Topic Packs, Generated files, and grading policy are unchanged. B7 remains OPEN; 119 Facts remain HOLD; PR remains Draft and unmerged.
