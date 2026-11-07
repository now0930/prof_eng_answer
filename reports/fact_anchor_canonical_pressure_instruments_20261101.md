# Canonical pressure-instrument primary-publisher verification — 2026-11-01

Scope: Seven independently inspected canonical statements. Five bounded validated propositions; two explicit HOLD for incomplete matching evidence. HOLD rows remain `NOT_PERFORMED` in the main audit and are not counted as completed primary source verifications.

No grade-source JSON, generated bank or runtime exclusion overlay was changed. Formal repository validation not run.

## 1. bourdon_tube_forms_and_ranges_are_design_specific

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `bourdon_forms_application`
- **Exact original statement:** Bourdon element는 C형, spiral, helical 등으로 구성할 수 있으며 형상·재질·두께에 따라 사용 압력범위가 달라진다. 일반적으로 견고한 현장 지시와 중·고압 측정에 널리 사용된다.
- Primary publisher: WIKA Bourdon tube pressure gauge
- Locator: Bourdon tube construction and C/spiral/helical ranges, HTML body
- URL: https://www.wika.com/en-us/lp_bourdon_tube_pressure_gauge.WIKA
- Verdict: **KEEP_BOUNDED**
- Precise verified scope or evidence gap: Different geometry/material/thickness provide different response and ranges. Manufacturer example 60 bar for C tube is NOT a universal dividing pressure; retain general structure/application principle.

## 2. piezoresistive_pressure_sensor_offset_and_sensitivity_are_temperature_dependent

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `piezoresistive_temperature_compensation`
- **Exact original statement:** Piezoresistive sensor의 offset과 sensitivity는 온도 영향을 받을 수 있으므로 bridge compensation, calibration coefficient, ASIC 보정 등 센서 구조에 맞는 temperature compensation이 중요하다.
- Primary publisher: Analog Devices, Demystifying Piezoresistive Pressure Sensors
- Locator: Pressure Sensor Signal Conditioning; Offset-Drift Compensation; equations 3–11
- URL: https://www.analog.com/en/resources/technical-articles/demystifying-piezoresistive-pressure-sensors.html
- Verdict: **KEEP_BOUNDED**
- Precise verified scope or evidence gap: Both zero offset and sensitivity can drift with T; particular compensation depends on sensor, bridge drive and ASIC. No guaranteed linear drift across arbitrary temperature.

## 3. pressure_pulsation_vibration_and_damping_affect_dynamic_indication

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `pulsation_vibration_dynamic_response`
- **Exact original statement:** 펌프·압축기·밸브 주변의 pulsation과 vibration은 기계식 gauge의 pointer flutter와 피로, transmitter의 dynamic error를 유발할 수 있어 damping, remote mounting, sampling/response-time 요구를 함께 검토한다.
- Primary publisher: WIKA How to Select a Pressure Gauge
- Locator: Section 3 Application, vibration/pulsation and snubber notes; WIKA 8 Common Reasons for Pressure Gauge Failure
- URL: https://blog.wika.com/us/knowhow/how-to-select-pressure-gauge/
- Verdict: **KEEP_BOUNDED**
- Precise verified scope or evidence gap: Mechanical gauge pointer instability/fatigue and damping are established. Pressure transmitter dynamic error depends on impulse line, filtering, sampling and bandwidth, not guaranteed by this mechanical gauge example.

## 4. pressure_range_overpressure_and_burst_limits_are_distinct_product_ratings

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `overrange_working_burst_pressure`
- **Exact original statement:** 측정 range와 maximum working pressure, overrange limit, proof/burst pressure는 서로 다른 개념이므로 정상 측정범위뿐 아니라 upset와 pressure spike에 대한 기계적 허용한계를 확인해야 한다.
- Primary publisher: WIKA Pressure sensor in the overload area
- Locator: First paragraph overload vs burst; supplementary DIN 16086 terms on WIKA page
- URL: https://blog.wika.com/en/products/pressure-products/pressure-sensor-overload/
- Verdict: **KEEP_BOUNDED**
- Precise verified scope or evidence gap: Rated measuring range carries stated error limits; overload survival does not guarantee accuracy; burst is destructive structural limit. Do not equate max working pressure with burst rating.

## 5. pressure_wetted_material_and_process_connection_selection_is_media_dependent

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `process_media_wetted_material_selection`
- **Exact original statement:** 공정유체의 부식성, 점도, 고형물, 위생성, 독성, 응축·결빙 가능성과 process temperature를 고려해 wetted material, process connection, seal/isolator와 flushing·drain 구조를 선정한다.
- Primary publisher: WIKA Chemical Compatibility: Wetted Parts of Pressure Sensors
- Locator: Chemical compatibility and wetted part material selection, paragraphs 1–6
- URL: https://blog.wika.com/us/products/pressure-products/chemical-compatibility/
- Verdict: **KEEP_BOUNDED**
- Precise verified scope or evidence gap: Fluid compatibility, temperature, pressure, phase, and contaminants affect wetted materials and isolator/connection. Exact flushing/draining layout and universal materials cannot be deduced from the source.

## 6. pressure_range_selection_checks_process_extremes_and_turndown_performance

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `range_turndown_resolution_selection`
- **Exact original statement:** 압력계기 선정에서는 정상·최소·최대 압력, calibration range, URL/LRL, turndown, resolution과 필요한 정확도를 함께 검토하여 정상 운전점이 지나치게 range 끝단에 몰리지 않도록 한다.
- Primary publisher: WIKA How to Select a Pressure Gauge
- Locator: Section 5 Pressure
- URL: https://blog.wika.com/us/knowhow/how-to-select-pressure-gauge/
- Verdict: **HOLD**
- Precise verified scope or evidence gap: WIKA describes normal range selection but does not prove full canonical mix of URL/LRL, electronic turndown, resolution, and accuracy requirements for every device.

## 7. pressure_reference_accuracy_and_operating_effects_are_distinct_specification_terms

- Canonical anchor: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error` / `accuracy_total_performance_terms`
- **Exact original statement:** 압력계기의 reference accuracy는 linearity, hysteresis, repeatability 등의 일부 또는 조합일 수 있고 제조사 정의가 다를 수 있다. 실제 성능은 온도·static pressure·installation·stability 영향까지 포함한 total performance 관점으로 평가한다.
- Primary publisher: Emerson Pressure Transmitters catalog
- Locator: Product comparison: reference accuracy and stability
- URL: https://www.emerson.com/en/measurement-instrumentation/catalog/pressure-measurement/pressure-transmitters
- Verdict: **HOLD**
- Precise verified scope or evidence gap: Catalog only distinguishes accuracy and stability; exact reference accuracy composition, static-pressure and ambient total performance require model-specific product data sheets; no full original-source proof here.


All checked technical documents were official HTML. Vendor examples do not themselves impose universal field-testing or compliance requirements. Current scoring eligibility overlays continue to apply.