# Thermocouple sentence review

Two exact legacy Anchor wordings were independently reviewed by `gpt-6-luna` using AI review on 2026-11-16. This is not human review, Registry approval, or a grant of scoring eligibility. The old statements remain in accepted explanations. Other candidates remain pending.

## `thermocouple_measures_temperature_difference`

- Previous: 열전대 전압은 측정접점 온도만의 함수가 아니다. 기준접점의 온도가 변하면 동일한 측정접점 온도에서도 측정 전압이 달라진다. 따라서 열전대는 본질적으로 두 접점의 온도차에 대응하는 센서이며, 절대온도를 얻으려면 기준접점 온도를 알아야 한다.
- Reviewed: 열전대의 기전력은 측정접점뿐 아니라 기준접점 온도에도 의존하므로 측정접점의 절대온도 환산에는 기준접점 온도 정보가 필요하다.
- Evidence: Analog Devices AN-274, *Practical Thermocouple Measurement*, Fig. 1, https://www.analog.com/media/en/technical-documentation/application-notes/an-274.pdf; NIST, *Thermocouples*, https://www.nist.gov/pml/sensor-science/thermodynamic-metrology/mercury-thermometer-alternatives/mercury-thermometer-5; accessed 2026-11-16. The sentence retains dependence on both junction temperatures and the need for a reference. It avoids implying that nonlinear emf is determined by the temperature difference alone.

## `thermocouple_nonlinearity_reference_tables_polynomial_conversion`

- Previous: 열전대 열기전력과 온도의 관계는 비선형이다. 따라서 열전대 종류별 표준 열기전력표 또는 표준 다항식을 사용하여 전압을 온도로 환산한다. 열전대 종류가 다르면 동일한 전압-온도 변환식을 사용할 수 없다. 다항식 적용 범위와 단위를 확인해야 하며, 범위 밖 외삽은 제한해야 한다.
- Reviewed: 열전대의 비선형 열기전력은 열전대 형식별 표준 열기전력표나 다항식의 유효 온도범위·단위에 맞춰 온도로 환산해야 한다.
- Evidence: NIST Monograph 175, ITS-90 thermocouple reference functions, e.g. §3.3, https://nvlpubs.nist.gov/nistpubs/Legacy/MONO/nistmonograph175.pdf, accessed 2026-11-16. Per-type equations, valid ranges and units remain explicit; out-of-range extrapolation is not implied to be valid. The sentence does not claim a reference table alone guarantees calibration accuracy.

Neither review authorizes other candidate statements. The electronic cold-junction candidate remains pending because a known-temperature reference is another implementation. Intermediate-temperature relations need same-pair and sign convention; measurement-chain and thermowell candidates may omit separate scoring demands. IDs, source references, weights, Registry and exclusions remain unchanged. Rebuild, routing impact and regression results are separate from this source review.
