# Source-grounded review: rotation and thermocouple first-sentence representations

Independent AI review used a subagent configured as `gpt-6-luna`; its self-identification exposed only GPT-6, not an independently confirmable deployment ID. Review method: AI, 2026-11-16. Exact sentence review only; not human review, Fact admission, source approval, or scoring promotion. The prior full statement remains the scoring reference.

Only the five bounded propositions below are applied.

## `period_measurement_low_speed`

- Previous: 저속에서는 연속 유효 pulse 사이의 시간 T_c를 측정하여 n = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다. 단, timer resolution과 jitter의 영향을 검토해야 한다.
- Reviewed: 저속에서는 연속 유효 pulse 사이의 시간 T_c를 측정하여 n = 60/(N_eff·T_c)로 계산하는 reciprocal/period 방식이 fixed-window count 방식보다 유리할 수 있다.
- Evidence: NI, Choosing a Counter Frequency Measurement Method, Low Frequency with 1 Counter; https://www.ni.com/en/support/documentation/supplemental/21/choosing-counter-frequency-measurement-method0.html (accessed 2026-11-16).
- Boundary: The effective pulse period and count/revolution refer to the same event stream; the possibility of an advantage is conditional. Timer resolution and jitter remain in the prior scoring reference.

## `inductive_proximity_principle`

- Previous: Inductive proximity sensor는 sensing face의 교번 전자기장에 금속 target이 접근할 때 발생하는 eddy-current loss 또는 oscillator 변화로 target 존재를 검출한다. Gear tooth나 flag를 반복 검출하면 passage frequency에서 회전속도를 계산할 수 있다.
- Reviewed: Inductive proximity sensor는 sensing face의 교번 전자기장에 금속 target이 접근할 때 발생하는 eddy-current loss 또는 oscillator 변화로 target 존재를 검출한다.
- Evidence: Pepperl+Fuchs, Inductive Sensors, pp. 7–9; https://pfdcpus.pepperl-fuchs.com/netpartner/portlets/training/online-classes/presentations_fa/inductive/downloads/inductive.pdf (accessed 2026-11-16).
- Boundary: The target is metallic; range and response depend on the sensor and target.

## `digital_tachometer_instrument_boundary`

- Previous: Digital tachometer는 encoder·proximity·optical pickup 등의 pulse를 계수하거나 period를 측정해 RPM을 표시하는 instrument일 수 있다. Tachometer라는 명칭만으로 sensing principle이 tachogenerator라고 단정하지 않는다.
- Reviewed: Digital tachometer는 encoder·proximity·optical pickup 등의 pulse를 계수하거나 period를 측정해 RPM을 표시하는 instrument일 수 있다.
- Evidence: NI, Hardware Encoder Measurements: How-To Guide, How an Encoder Makes a Measurement; https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x1riCAA (accessed 2026-11-16).
- Boundary: Pulse counting or period measurement is one possible architecture, not the only meaning of tachometer; the naming boundary remains in the prior scoring reference.

## `thermocouple_law_of_intermediate_metals`

- Previous: 열전대 회로에 제3의 금속이 삽입되더라도 그 금속과 열전대 재료 사이에 형성된 두 접점이 동일한 온도에 있으면 순 열기전력은 변하지 않는다. 따라서 단자대, 커넥터와 계측기 내부 도체를 사용할 수 있다. 다만 두 접점의 온도가 다르거나 등온 조건이 깨지면 추가 오차가 발생할 수 있다.
- Reviewed: 열전대 회로에 제3의 금속이 삽입되더라도 그 금속과 열전대 재료 사이에 형성된 두 접점이 동일한 온도에 있으면 순 열기전력은 변하지 않는다.
- Evidence: Analog Devices AN-274, Law of Intermediate Metals, Fig. 1c; https://www.analog.com/media/en/technical-documentation/application-notes/an-274.pdf (accessed 2026-11-16).
- Boundary: The two inserted-metal junctions must be at the same temperature.

## `thermocouple_thermowell_installation_dynamic_error`

- Previous: 보호관, 삽입길이, 유속, 배관 벽면과의 열전도, 복사, 접촉상태는 측정접점이 실제 공정 온도에 도달하는 과정에 영향을 준다. 열전대 자체의 전기적 원리가 정확해도 설치가 부적절하면 열전달 오차와 응답지연이 발생한다. 보호관의 열용량이 증가하면 일반적으로 응답이 느려진다.
- Reviewed: 보호관, 삽입길이, 유속, 배관 벽면과의 열전도, 복사, 접촉상태는 측정접점이 실제 공정 온도에 도달하는 과정에 영향을 준다.
- Evidence: Analog Devices AN-28, Error Sources in Thermocouple Systems; https://www.analog.com/en/resources/app-notes/an-28f.html (accessed 2026-11-16).
- Boundary: Installation and heat transfer can affect the measuring junction; no universal direction or magnitude of error is asserted.

Other remaining candidates are not approved by this report. Absolute encoder continuous-position uniqueness is held pending resolution/quantization clarification; channel frequency vs decoded event rate, index-only multi-turn boundary, thermocouple endpoint-temperature dependence, and intermediate-temperature sign conventions remain pending.
