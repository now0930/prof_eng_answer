# Humidity sentence review with evidence-token preservation

The earlier Korean paraphrases added lexical tokens used by the deterministic Fact evidence adapter. This review replaces three with short original-wording statements while keeping each original `accepted_explanations` list and first entry unchanged. Source-grounded AI reviewer: `gpt-6-luna`, review method `ai`, 2026-11-16. This review is not a human approval, Registry approval, or automatic score admission.

## `relative_humidity_definition`

- Previous: Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다. 포화수증기압은 온도함수이므로 RH는 온도에 강하게 의존한다.
- Reviewed: Relative humidity는 같은 온도에서 실제 수증기 분압 P_w를 포화수증기압 P_ws(T)로 나눈 비이며 RH[%] = 100·P_w/P_ws(T)로 정의한다.
- Source: NOAA/NDBC, *Handbook of Automated Data Quality Control* (2023), §3.4 and Appendix A §A1, https://www.ndbc.noaa.gov/publications/NDBCHandbookofAutomatedDataQualityControl2023.pdf, accessed 2026-11-16. Same-temperature pressure ratio and percent remain explicit; the temperature-dependence explanation is preserved in the unchanged accepted explanation and separate `rh_temperature_dependence` Anchor.

## `dew_point_definition`

- Previous: Dew point T_d는 현재 수증기 함량과 압력조건에서 기체를 냉각할 때 liquid water condensation이 시작되는 온도다. Ambient temperature가 dew point에 가까워질수록 condensation risk가 증가한다.
- Reviewed: Dew point T_d는 현재 수증기 함량과 압력조건에서 기체를 냉각할 때 liquid water condensation이 시작되는 온도다.
- Source: NOAA/NWS Glossary, Dew Point, https://forecast.weather.gov/glossary.php?word=DEW; Vaisala HMDW110 User Guide, Output parameters explained, https://docs.vaisala.com/r/M211726EN-J/en-US/GUID-2EB36F26-0403-4E11-9710-1AF6B3BFD57D?contentId=YPrCE2ibM7ghmoVHFeZ8Sw; accessed 2026-11-16. Fixed moisture and pressure, cooling and liquid-water reference remain. The condensation-risk explanation remains in the unchanged accepted explanation.

## `frost_point_distinction`

- Previous: 0°C 이하의 매우 건조한 조건에서는 응축상이 ice인지 liquid water인지에 따라 frost point와 dew point를 구분할 수 있다. Subzero moisture specification에서는 사용한 정의와 계산 기준을 확인해야 한다.
- Reviewed: 0°C 이하의 매우 건조한 조건에서는 응축상이 ice인지 liquid water인지에 따라 frost point와 dew point를 구분할 수 있다.
- Source: Vaisala, *Dew Point/Frost Point Selection*, §§1–3, pp. 3–5, https://www.vaisala.com/sites/default/files/documents/Dew-point-frost-point-selection-B212716EN.pdf, accessed 2026-11-16. The water/ice reference distinction is preserved, with the previous dry/subzero scope; the prior definition/calculation-basis note remains in the unchanged accepted explanation.

The capacitive and resistive candidates were restored to their previous source wording pending further review of the adapter and sensor-technology scope. The technically reviewed frost-point shortening was also restored after a synthetic fallback-routing owner regression. The relative-humidity and dew-point shortenings were subsequently restored to their previous canonical wording as well, after the D/E canonical-axis projection produced an extra axis per shortened Anchor; see `pr38_fact_sentence_evidence_token_review_20261116.md`. All proposals above are now non-scoring and unapplied. Identical token sets do not establish routing, evidence-span, or overall score equivalence.


## Subsequent application (2026-11-16)

After the historical rollback described above, the relative-humidity, dew-point, and frost-point first sentences were applied as source representations using the explicit compatibility contract in `pr38_sentence_compatibility_20261116.md`. The full prior statements remain the scoring references; this update does not approve a new Fact or resolve the later Claim-separation work. The earlier routing regression and axis duplication are covered by focused compatibility comparisons, not assumed fixed by wording alone.
