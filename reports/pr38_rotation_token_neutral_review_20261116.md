# Rotation sentence review with evidence-token preservation

Independent source-grounded AI reviewer: `gpt-6-luna`, review method `ai`, 2026-11-16. Review is limited to the exact four legacy Anchor statements; no Registry approval or scoring admission is implied. The original accepted-explanation lists remain unchanged.

## `quadrature_direction_principle`

- Previous: Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다. x1/x2/x4 decoding에 따라 유효 count/rev가 달라질 수 있다.
- Reviewed: Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다.
- Evidence: OMRON, Rotary Encoders, Output Phase Difference and CW, https://www.ia.omron.com/support/guide/34/explanation_of_terms.html; Operating Principles, https://www.ia.omron.com/support/guide/34/introduction.html. Accessed 2026-11-16.

## `counting_window_speed_equation`

- Previous: 고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다. 낮은 속도에서는 한 count가 만드는 속도 step이 커져 quantization 또는 resolution error가 증가할 수 있다.
- Reviewed: 고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다.
- Evidence: OMRON, Rotary Encoders, Operating Principles and Selection Guidelines [6], https://www.ia.omron.com/support/guide/34/introduction.html. The m/Δt count-rate equation is a dimensional derivation, not a source quotation. Accessed 2026-11-16.

## `gear_tooth_speed_equation`

- Previous: 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 n = 60f/Z이다. 실제 missing-tooth, multiple-edge counting 또는 target pattern이 있으면 Z 대신 회전당 유효 event 수를 사용한다.
- Reviewed: 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 n = 60f/Z이다.
- Evidence: OMRON, Rotary Encoders, Selection Guidelines [6], https://www.ia.omron.com/support/guide/34/introduction.html. The frequency-to-rpm relation is a dimensional derivation with Z effective events/rev and one pulse per event. Accessed 2026-11-16.

## `tachogenerator_voltage_speed_principle`

- Previous: Permanent-magnet DC tachogenerator는 회전에 의해 생성되는 DC voltage가 정상 동작범위에서 회전속도에 대체로 비례하도록 설계된 analog speed transducer다. V_t ≈ K_t·n의 sensitivity로 표현할 수 있다.
- Reviewed: Permanent-magnet DC tachogenerator는 회전에 의해 생성되는 DC voltage가 정상 동작범위에서 회전속도에 대체로 비례하도록 설계된 analog speed transducer다.
- Evidence: maxon, Motors as Generators, sections 1.1 and 1.2, https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators. Terminal loading, winding and brush resistance can affect measured output. Accessed 2026-11-16.

The unchanged original explanation retains decoding counts, sensitivity, low-speed quantization, and irregular-event corrections as applicable. The statement for gear events retains one pulse per identical event and must not be applied to an irregular physical tooth count without an effective event count. Original token sets are preserved through the unchanged first explanation; routing, evidence-span and score equivalence remain separate questions. Other candidates are not approved by this review.

Subsequent D/E canonical-axis projection exposed an additional axis for each shortened Anchor. The four original canonical wordings were restored pending a reviewed compatibility design; these short sentences remain non-scoring proposals. See `pr38_fact_sentence_evidence_token_review_20261116.md`.


## Subsequent application (2026-11-16)

After the historical rollback described above, the four reviewed first sentences were applied as source representations using `fact_anchor_sentence_compat_v1`. The previous statements remain the scoring references. This does not admit a new Fact or complete the later Claim separation. The source conditions on one pulse per event and uniform events remain explicit; irregular-event corrections remain in the preserved reference. Focused tests compare the combined Topic against its prior scoring projection and routing.
