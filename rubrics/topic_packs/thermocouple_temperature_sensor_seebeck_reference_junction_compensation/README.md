# 열전대 온도센서의 원리, 기준접점 보상 및 보상도선

## Topic 정보

- Topic ID: `thermocouple_temperature_sensor_seebeck_reference_junction_compensation`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Evaluation method: `LLM_ONLY`

## 목적

이 Topic Pack은 열전대의 Seebeck 효과, 측정접점과 기준접점,
냉접점 보상, 중간금속·중간온도 법칙, 연장도선·보상도선,
종류별 비선형 변환, 접점 구조, 설치, 교정 및 진단을 평가한다.

열전대는 측정접점의 절대온도를 직접 출력하지 않는다.
측정접점과 기준접점의 온도차에 대응하는 열기전력을 발생시키며,
절대온도 환산에는 기준접점 온도 측정과 종류별 보상이 필요하다.

## Topic 경계

- 열전대와 RTD의 비교·선정은
  `temperature_sensor_thermocouple_rtd` Topic에서 다룬다.
- Pt100과 2·3·4선식 보상은 RTD 독립 Topic에서 다룬다.
- NTC·PTC와 thermistor 식은 향후 독립 Topic에서 다룬다.
- 이 Topic은 열전대 원리·CJC·보상도선·설치·진단에 집중한다.

## Source 구성

- `fact_anchor.json`: Fact Anchor 14개와 Fatal Wrong Claim 8개
- `logic_check.json`: truth schema 14개와 fatal condition 8개
- `model_answer.json`: 답안 구조와 고득점 판단 기준
- `topic_importance.json`: FIELD_APPLICATION 전략과 high-band 조건

## 평가 방식

- deterministic checks는 비활성화한다.
- Candidate extraction rules는 비워 둔다.
- 문자열 일치가 아니라 원리·조건·인과관계·현장 적용성을 평가한다.
- Fatal Wrong Claim이 답안의 결론이면 high-band를 허용하지 않는다.

## 기준 문서

`docs/topic_sheets/thermocouple_temperature_sensor_seebeck_reference_junction_compensation.md`

이 Source Pack은 검토가 완료된 요구사항 Markdown에서 직접 생성했다.

## Data-driven 라우팅 필드

`routing_aliases`와 `routing_field_points`를 Source Pack에 명시하여 generated builder의 fallback 대신 열전대 전용 라우팅 메타데이터를 사용한다.
