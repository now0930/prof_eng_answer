# Rotation measurement: two sentence reviews

Independent source-grounded AI reviewer: `gpt-6-luna`, review method `ai`, 2026-11-16. These are individual legacy Anchor reviews, not human review, Registry approval or automatic scoring admission. Each previous statement remains in accepted explanations.

## `quadrature_direction_principle`

- Previous: Quadrature incremental encoder는 A와 B 두 channel을 약 90 electrical degree 위상차로 출력하며 어느 channel이 선행하는지로 회전방향을 판별한다. x1/x2/x4 decoding에 따라 유효 count/rev가 달라질 수 있다.
- Reviewed: 증분형 엔코더의 A·B 직교 채널은 약 90° 전기각 위상차와 선행 채널로 방향을 판별하며, 유효 계수 수는 x1/x2/x4 복호화 방식에 따라 달라진다.
- Evidence: OMRON, *Rotary Encoders: Explanation of Terms*, Output Phase Difference and CW, https://www.ia.omron.com/support/guide/34/explanation_of_terms.html; *Introduction*, Operating Principles, https://www.ia.omron.com/support/guide/34/introduction.html; accessed 2026-11-16. The 90° electrical phase, lead/lag direction and decoding-dependent count are retained; A/B are the encoder's output channels.

## `tachogenerator_voltage_speed_principle`

- Previous: Permanent-magnet DC tachogenerator는 회전에 의해 생성되는 DC voltage가 정상 동작범위에서 회전속도에 대체로 비례하도록 설계된 analog speed transducer다. V_t ≈ K_t·n의 sensitivity로 표현할 수 있다.
- Reviewed: 영구자석형 DC 타코제너레이터의 출력전압은 규정 동작범위에서 회전속도에 대체로 비례하여 V_t≈K_t·n으로 표현할 수 있다.
- Evidence: maxon, *Motors as Generators*, §§1.1 and 1.2, https://support.maxongroup.com/hc/en-us/articles/360004496254-maxon-Motors-as-Generators, accessed 2026-11-16. Approximate proportionality is retained within the operating range; loading and brush/winding resistance can affect terminal voltage. The prior explanation retains the analog transducer classification and the sensitivity meaning of K_t.

## `counting_window_speed_equation`

- Previous: 고정 측정창 Δt 동안 m개의 유효 count를 세면 n = 60m/(N_eff·Δt)로 계산할 수 있다. 낮은 속도에서는 한 count가 만드는 속도 step이 커져 quantization 또는 resolution error가 증가할 수 있다.
- Reviewed: 측정창 Δt에 수신한 유효 펄스 수가 m이면 n[rpm]=60m/(N_eff·Δt)이며, 저속에서는 펄스 양자화에 의한 속도 분해능 한계가 커질 수 있다.
- Evidence: OMRON, *Rotary Encoders*, Operating Principles and Resolution, https://www.ia.omron.com/support/guide/34/introduction.html and https://www.ia.omron.com/support/guide/34/explanation_of_terms.html. The equation is a dimensional derivation: m/Δt counts/s divided by N_eff counts/rev, then multiplied by 60 s/min; it is not claimed as a quotation from OMRON. Low-speed quantization and the effective count convention remain explicit.

## `gear_tooth_speed_equation`

- Previous: 회전당 Z개의 동일한 tooth 또는 target event가 있고 각 event당 1 pulse를 얻는다면 n = 60f/Z이다. 실제 missing-tooth, multiple-edge counting 또는 target pattern이 있으면 Z 대신 회전당 유효 event 수를 사용한다.
- Reviewed: 회전당 검출 이벤트가 Z개이고 이벤트당 펄스가 하나이면 회전속도 n[rpm]=60f/Z이며, 누락 톱니나 다중 에지 계수 시 실제 유효 이벤트 수로 보정한다.
- Evidence: OMRON, *Rotary Encoders*, Selection Guidelines [6], https://www.ia.omron.com/support/guide/34/introduction.html; Pepperl+Fuchs, *Inductive Sensors*, pp. 7–9, https://pfdcpus.pepperl-fuchs.com/netpartner/portlets/training/online-classes/presentations_fa/inductive/downloads/inductive.pdf. The equation follows from f=(n/60)·Z; it is a dimensional derivation, not a quotation from the sensor training. Z must be the effective events/rev and f the event frequency. Missing-tooth, multi-edge and target-pattern differences are represented by the effective event count.

The Z/index candidate remains pending because its count-verification application needs to be retained explicitly. The old encoder-frequency simplification remains pending: physical channel frequency and decoder event rate are distinct. The pulse-frequency candidate must retain the encoder PPR definition; period measurement must retain its fixed-window comparison; and inductive sensing must retain the flag-target scope. No scoring weights, exclusions, source ownership or Registry approval are changed. Generated routing and score effects require their own validation.
