# Humidity sentence review: dew point and sensing principles

Independent source-grounded AI reviewer: `gpt-6-luna`, review method `ai`, 2026-11-16. The following reviews concern only the exact four legacy Anchor statements, not Registry admission or a new scoring gate. Previous text remains in accepted explanations.

## `dew_point_definition`

- Previous: Dew point T_d는 현재 수증기 함량과 압력조건에서 기체를 냉각할 때 liquid water condensation이 시작되는 온도다. Ambient temperature가 dew point에 가까워질수록 condensation risk가 증가한다.
- Reviewed: 이슬점 T_d는 주어진 수증기 함량과 압력에서 기체를 냉각할 때 액체 물의 응축이 시작되는 온도이다.
- Evidence: NOAA NWS, Glossary: Dew Point (constant pressure and moisture); https://forecast.weather.gov/glossary.php?word=DEW (accessed 2026-11-16).

## `frost_point_distinction`

- Previous: 0°C 이하의 매우 건조한 조건에서는 응축상이 ice인지 liquid water인지에 따라 frost point와 dew point를 구분할 수 있다. Subzero moisture specification에서는 사용한 정의와 계산 기준을 확인해야 한다.
- Reviewed: 영하 조건에서는 얼음 형성을 기준으로 하는 서리점과 액체 물 응축을 기준으로 하는 이슬점의 정의를 구분해야 한다.
- Evidence: WMO Guide to Meteorological Instruments and Methods of Observation, Chapter 4, Annex 4.B, saturation over water and ice; https://www.weather.gov/media/epz/mesonet/CWOP-WMO8.pdf (accessed 2026-11-16).

## `capacitive_polymer_principle`

- Previous: Capacitive humidity sensor는 porous electrode 사이의 hygroscopic polymer dielectric이 수분을 흡수·방출하면 dielectric constant가 변하고 이에 따라 capacitance가 변하는 원리를 이용한다. 이 capacitance를 전자회로가 RH 신호로 변환한다.
- Reviewed: 고분자 정전용량식 습도센서는 흡습성 고분자 유전체의 수분 흡수·방출에 따른 유전율·정전용량 변화를 상대습도 신호로 변환한다.
- Evidence: Texas Instruments SNAA427, abstract and section 2, polymer dielectric and capacitance; https://www.ti.com/lit/an/snaa427/snaa427.pdf (accessed 2026-11-16).

## `resistive_humidity_principle`

- Previous: Resistive humidity sensor는 습기에 민감한 sensing element의 resistance 또는 impedance 변화를 측정한다. 제조사·기술 자료의 polymer 또는 conductive-salt 구조에서는 수증기 흡수에 따른 ionic conduction 변화가 저항성 응답을 만든다. 재료별 구조와 응답특성을 모든 resistive sensor에 일반화하지 않는다.
- Reviewed: 저항식 습도센서는 감지소자의 습도에 따른 저항 또는 임피던스 변화를 이용하며, 전도 메커니즘은 재료·구조에 따라 다르다.
- Evidence: ASHRAE Handbook 2025, Chapter 38, Section 4.4 Resistive Sensor; https://handbook.ashrae.org/handbooks/F25/SI/f25_ch38/F25_Ch38_si.aspx (accessed 2026-11-16).

Dew point retains fixed moisture and pressure; condensation risk remains elsewhere in the Topic. Frost point refers to saturation over ice and dew point to liquid water, including supercooled water. The capacitive claim applies to polymer-dielectric sensors; the resistive claim retains material/structure dependence and does not generalize an ionic mechanism to all devices. No existing Registry, weight, source reference or exclusion is altered. Other candidates remain pending.
