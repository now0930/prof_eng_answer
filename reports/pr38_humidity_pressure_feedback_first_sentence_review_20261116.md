# Source-grounded first-sentence review: humidity, pressure and feedback

An independent AI review was requested with the `gpt-6-luna` agent configuration; the agent self-reported GPT-6 without exposing its exact deployment ID. Method: AI; 2026-11-16. This is bounded source-wording review, not human review, Fact admission or scoring promotion. Each previous full statement remains the scoring reference.

## `absolute_humidity_definition`

- Previous: Absolute humidity는 단위 체적당 수증기 질량 ρ_v = m_v/V로 정의할 수 있으며 이상기체 근사에서는 ρ_v = P_w/(R_v T)로 연결된다. RH와 달리 같은 수증기 상태라도 온도·압력과 체적변화의 영향을 받는다.
- Reviewed: Absolute humidity는 단위 체적당 수증기 질량 ρ_v = m_v/V로 정의할 수 있으며 이상기체 근사에서는 ρ_v = P_w/(R_v T)로 연결된다.
- Evidence: Vaisala HMP155 calculation formulas, Absolute humidity (3); https://docs.vaisala.com/r/M210912EN-J/en-US/GUID-8F8C9ECE-FFD9-4F6F-9F11-D94CF9122735 (accessed 2026-11-16).
- Boundary: Ideal-gas approximation is explicit; the density is water-vapor mass per volume.

## `pressure_dew_point_effect`

- Previous: Dew point는 pressure condition의 영향을 받으므로 compressed gas에서는 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다. 압력변화 시 같은 moisture content라도 condensation condition이 달라질 수 있다.
- Reviewed: Dew point는 pressure condition의 영향을 받으므로 compressed gas에서는 pressure dew point와 atmospheric-equivalent dew point를 혼동하지 않는다.
- Evidence: Vaisala, What Is Dew Point and How to Measure It, pressure effects; https://www.vaisala.com/en/blog/2019-09/what-dew-point-and-how-measure-it (accessed 2026-11-16).
- Boundary: Pressure condition and compressed-gas context remain explicit.

## `capacitive_polymer_principle`

- Previous: Capacitive humidity sensor는 porous electrode 사이의 hygroscopic polymer dielectric이 수분을 흡수·방출하면 dielectric constant가 변하고 이에 따라 capacitance가 변하는 원리를 이용한다. 이 capacitance를 전자회로가 RH 신호로 변환한다.
- Reviewed: Capacitive humidity sensor는 porous electrode 사이의 hygroscopic polymer dielectric이 수분을 흡수·방출하면 dielectric constant가 변하고 이에 따라 capacitance가 변하는 원리를 이용한다.
- Evidence: Sensirion, Technology: Humidity, capacitive measurement principle; https://sensirion.com/products/technology (accessed 2026-11-16).
- Boundary: The claim is limited to a hygroscopic polymer dielectric and capacitance mechanism.

## `feedback_disturbance_noise_paths`

- Previous: 단위 피드백의 표준 신호 위치에서 출력단 외란은 S를 통해 출력에 나타나고 측정 잡음은 -T를 통해 출력에 나타난다. 전달경로는 외란과 잡음의 주입 위치에 따라 달라지므로 신호 위치를 먼저 정의해야 한다.
- Reviewed: 단위 피드백의 표준 신호 위치에서 출력단 외란은 S를 통해 출력에 나타나고 측정 잡음은 -T를 통해 출력에 나타난다.
- Evidence: MathWorks, getCompSensitivity, More About and transfer-path derivation; https://www.mathworks.com/help/control/ref/genlti.getcompsensitivity.html (accessed 2026-11-16).
- Boundary: Unity feedback and standard disturbance/noise injection locations are essential; other positions need their own transfer paths.

## `diaphragm_deflection_principle`

- Previous: Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다. 얇고 유연한 diaphragm은 작은 압력차에 높은 감도를 얻을 수 있다.
- Reviewed: Diaphragm pressure element는 막 양측의 압력차가 만드는 탄성변형을 변위 또는 전기신호로 변환한다.
- Evidence: WIKA, Pressure & Temperature Measurement Handbook, §1.4.1, diaphragm elements; https://www.wika.com/media/Brochures-and-flyers/EN-UM/br_rfhandbook_en_um.pdf (accessed 2026-11-16).
- Boundary: Pressure difference across the diaphragm and elastic deflection are explicit.

## `diaphragm_sensor_vs_seal`

- Previous: 압력을 직접 감지하는 diaphragm sensing element와 공정유체를 계기에서 격리하는 diaphragm seal은 목적이 다르다. Seal은 fill fluid와 capillary를 포함할 수 있으며 자체로 모든 오차를 제거하지 않는다.
- Reviewed: 압력을 직접 감지하는 diaphragm sensing element와 공정유체를 계기에서 격리하는 diaphragm seal은 목적이 다르다.
- Evidence: Emerson Rosemount DP Level Transmitters and Diaphragm Seal Systems, §1 introduction; https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/dp-level/documents/doc-rosemount-dp-00825-0100-4016.pdf (accessed 2026-11-16).
- Boundary: Sensor element and process-isolating seal are distinguished; the previous scoring reference retains the fill-fluid and error caveat.

## `dp_transmitter_two_port_principle`

- Previous: DP transmitter는 high-side와 low-side 두 입력의 압력차를 sensing element에 전달하여 차압을 전기신호로 변환한다. 두 포트에 동일한 압력이 인가된 상태는 이상적으로 zero differential pressure 조건이다.
- Reviewed: DP transmitter는 high-side와 low-side 두 입력의 압력차를 sensing element에 전달하여 차압을 전기신호로 변환한다.
- Evidence: Emerson, differential-pressure measurement overview, instrument types; https://www.emerson.com/en/measurement-instrumentation/catalog/pressure-measurement/differential-pressure (accessed 2026-11-16).
- Boundary: High/low inputs and differential-pressure conversion are retained; equal-input zero is a separate implication.

Other candidates are not approved by this review. Constant vapor amount alone does not fully constrain pressure and volume; the relative-humidity temperature candidate remains pending clarification. Final-value theorem pole conditions, pressure sensing scope, and project-specific acceptance-test scope remain pending.

The feedback disturbance/noise sentence is **not applied**: its original first accepted explanation differs, so the existing compatibility contract cannot be used without a separate compatibility design.
