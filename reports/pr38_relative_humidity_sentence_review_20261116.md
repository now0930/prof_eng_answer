# Relative humidity definition: source-grounded sentence review

The proposed single sentence preserves the definition; temperature dependence remains a separate existing Anchor. This is an AI review of one legacy Anchor, not human review or a change to Registry admission. Release validation and generated synchronization are separately required.

- Topic: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation`
- Anchor: `relative_humidity_definition`
- Reviewer: `gpt-6-luna`, review method: `ai`, 2026-11-16.
- Previous: Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다. 포화수증기압은 온도함수이므로 RH는 온도에 강하게 의존한다.
- Reviewed sentence: 상대습도 RH[%]는 같은 온도의 실제 수증기 분압 P_w와 포화수증기압 P_ws(T)의 비율로, RH=100·P_w/P_ws(T)이다.
- Evidence: NOAA National Data Buoy Center, *Handbook of Automated Data Quality Control* (2023), §3.4 and Appendix A §A1, https://www.ndbc.noaa.gov/publications/NDBCHandbookofAutomatedDataQualityControl2023.pdf, accessed 2026-11-16; relative humidity is calculated from vapor and saturation vapor pressure, with temperature used for the latter. Vaisala, *Humidity measurement in test chambers*, FAQ 2, https://www.vaisala.com/en/application-note/humidity-measurement-test-chambers-questions-and-answers, accessed 2026-11-16, gives RH=100·Pw/Pws and identifies Pws as temperature dependent.
- Mapping: the ratio, factor 100, water-vapor partial pressure, and same-temperature saturation pressure are preserved. The separate `rh_temperature_dependence` Anchor retains temperature dependence at approximately constant water-vapor amount. The original complete sentence remains in `accepted_explanations` for provenance; the source reference, ID, weight, exclusions and Registry approval are unchanged.
- Scope: the formula states the existing industrial RH definition; temperature and phase reference remain those of the applicable measurement convention. This review does not independently verify other candidates, change scoring eligibility, or establish routing/score equivalence after regeneration.
