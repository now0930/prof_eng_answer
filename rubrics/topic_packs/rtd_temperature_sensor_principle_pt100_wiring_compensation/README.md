# RTD 온도센서의 측정원리와 Pt100·측정전류·2선식·3선식·4선식 배선보상

## Topic ID

`rtd_temperature_sensor_principle_pt100_wiring_compensation`

이 Topic은 기존 `rtd_pt100_wire_connection_compensation`를 배선 중심 Topic에서 RTD
측정원리·결선·자기발열을 연결한 지식 단위로 확장한 대체 Topic이다. 다만 아래 세 대표
질문은 서로의 전체 내용을 요구하지 않는다. 채점 시 `model_answer.json`의 패턴별
`required_anchor_ids`만 해당 질문의 필수 범위로 적용한다.

## RTD 측정 사슬

    공정온도
    → 감온부 온도
    → 금속 저항 변화
    → 여기전류에 의한 전압 변화
    → 배선보상·증폭·선형화
    → 표시·제어용 온도값

핵심 관계는 다음과 같다.

    R = ρl/A
    V_RTD = I_exc R_RTD
    R_RTD = V_RTD/I_exc
    P_self = I_exc² R_RTD

Pt100은 0℃에서 공칭저항이 100 Ω인 백금 RTD이다.

정밀한 저항-온도 변환에는 Callendar–Van Dusen 관계 또는
표준 저항-온도표를 사용한다.

## 2선식

    R_measured = R_RTD + R_L1 + R_L2

두 리드선 저항이 측정값에 직렬로 포함된다.

## 3선식

    R_L1 ≈ R_L2

동일 리드저항 가정에서 bridge 또는 차동측정으로 리드선 영향의
1차 성분을 상쇄한다. 불평형이 있으면 잔류오차가 발생한다.

## 4선식

force lead와 sense lead를 분리하는 Kelvin 방식이다.

리드선 전압강하 영향을 크게 줄이지만 자기발열, 설치오차,
노이즈와 drift까지 제거하는 것은 아니다.

## Topic 경계

- Thermocouple: Seebeck effect, 기준접점, 냉접점 보상, 보상도선
- Thermistor: NTC/PTC, Beta 식, Steinhart–Hart 식, 비선형화

위 두 센서는 별도 Topic으로 작성한다.

## 평가 계약

- 문제 유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `FIELD_APPLICATION`
- 중요도: `NORMAL`
- 평가 방식: `LLM_ONLY`
- Fact Anchor: 14개
- Fatal Wrong Claim: 8개
- 권장 답안 구조: 8개
- 고득점 해제조건: 8개
- 결정론적 검사: 비활성화
- candidate extraction rule: 없음

### 대표 질문별 필수 범위

1. 측정원리·Pt100: 측정 사슬, 금속 저항원리, Pt100 기준특성, 저항-온도 특성
2. 결선·리드선 보상: 2선식, 3선식, 4선식과 결선 선정
3. 측정전류·자기발열·선정: 여기전류, 자기발열, 배선 선정

Transmitter 상세, thermowell·동적응답, 교정·불확도·진단은 유용한 확장 지식이지만 위
질문들이 명시적으로 요구하지 않는 한 고득점 필수조건이나 누락 감점으로 사용하지 않는다.
