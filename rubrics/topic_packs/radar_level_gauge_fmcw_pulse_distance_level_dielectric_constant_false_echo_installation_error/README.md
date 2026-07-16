# 레이더식 레벨계의 FMCW·펄스 방식, 거리·레벨 측정원리, 유전율 영향 및 허위에코·설치오차

## Topic metadata

- Topic ID: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Semantic execution: `LLM_ONLY`
- Deterministic checks: disabled
- Candidate extraction: `{}`

## Source files

- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

## Core contracts

- 20 Fact Anchors
- 10 Fatal Wrong Claims
- 32 Routing Aliases
- 5 Routing Field Points
- 14 Question Examples
- 14 Expected Question Patterns
- 펄스식 왕복시간과 `D=cτ/2`
- FMCW 처프·비트주파수와 `D=cf_b/(2S)`
- 반송주파수의 빔 특성과 유효 변조 대역폭의 거리 분해능 역할 구분
- 상대유전율과 반사에코
- 블로킹 거리, 허위에코와 다중반사
- 액체의 수직 정렬과 분체의 표면방향 정렬조건
- 노즐·안테나 부착물·응축 및 설치오차

## Fact verification references

- Emerson FMCW Technology and Rosemount manuals
- Emerson Rosemount 5300 GWR manuals
- Siemens SITRANS radar manuals
- Texas Instruments FMCW radar fundamentals
- Endress+Hauser Levelflex technical information
- VEGA radar and guided-radar guidance## Validation policy

Source JSON은 Requirements Markdown을 기준으로 직접 관리한다.
Generated bank는 Source 검토 완료 후 재빌드한다.
LLM 의미검증은 ChatGPT가 직접 수행한다.
컨테이너 전용 실행경로를 변경하지 않으므로 컨테이너 E2E는 생략한다.

## 기존 Radar Topic Pack 통합 확장

### 1. 자유공간 Pulse·FMCW

- 펄스식 자유공간 레이더에서 기준점부터 표면까지의 편도거리는 D=v_g·τ/2로 계산한다. v_g는 실제 전파경로인 기체공간의 전파속도이며 일반 공기에서는 c_0에 가깝다. 고압가스나 고밀도 증기에서는 전파속도 보정 가능성을 검토한다.
- 정지표면과 이상적인 선형 처프에서 스윕 기울기 S=B/T_s, 비트주파수 f_b=Sτ이며 거리는 D=v_g·f_b/(2S)=v_g·f_b·T_s/(2B)이다. 실제 계기는 스윕 비선형, 신호처리와 기체공간 전파속도 영향을 함께 고려한다.
- FMCW의 이상적 거리 분해능은 ΔR≈v_g/(2B)이다. 이는 두 인접 반사면을 분리하는 능력이며 단일 표면의 측정 정확도, 반복성 또는 FFT bin 간격과 동일하지 않다. 정확도는 S/N비, 주파수·위상 추정, 보간, 스윕 선형성, 교정과 설치조건의 영향을 함께 받는다.

### 2. 반사·에코 신호

- 단일 점표적 monostatic radar equation의 R⁻⁴ 관계는 링크 예산의 참고식이다. 탱크 액면과 분체표면은 안테나 빔 footprint를 가진 확장 반사면이므로 R⁻⁴를 레벨계의 보편 지배식으로 적용하지 않고 안테나 패턴, 표면 거칠기·기울기, 유전율과 수신처리를 함께 평가한다.
- 공기에서 비자성 고유전율 매질로 수직입사할 때 전기장 반사계수 Γ=(1-√ε_r)/(1+√ε_r)는 음수이므로 이상적 전기장 반사에는 위상반전이 있다. 다만 계기가 표시하는 에코곡선의 부호와 극성은 수신기·복조·표시 규약에 따라 달라질 수 있으므로 피크 부호만으로 제품표면과 구조물을 보편적으로 판정하지 않는다.
- 에코 임계값은 거리별 잡음과 감쇠를 고려하여 유효 에코를 선별하는 진폭 기준이다. 고정 또는 적응형 임계곡선, false-echo map, 거리창, 에코 이력과 추적 알고리즘을 함께 사용하며 단일 최대피크만으로 실제 표면을 확정하지 않는다.

### 3. 근거리 불감영역

- 안테나 근처에는 송신누설, 링다운, 노즐반사와 수신기 포화로 blocking distance 또는 upper null zone이 생길 수 있다. 과도한 마스킹은 실제 고레벨을 숨길 수 있으므로 최대 운전레벨과 독립 HH 과충전 방호가 불감영역 밖에서 성립하도록 조정한다.

### 4. Guided Wave Radar

- 일반적인 산업용 GWR은 TDR 원리에 따라 저전력 나노초 마이크로파 펄스를 rod, cable 또는 coaxial probe를 따라 전송하고 임피던스가 변하는 제품표면의 반사 왕복시간으로 거리를 계산한다. 이를 자유공간 FMCW와 동일한 구조로 일반화하지 않는다.
- GWR의 상부 액면 레벨은 기준점부터 표면까지의 기체·증기 구간 왕복시간으로 계산하므로 제품 액체의 √ε_r를 거리식 전체에 일률적으로 나누지 않는다. 계면 측정에서는 펄스가 상부 액체층을 통과하므로 그 구간의 전파속도 c_0/√ε_r,upper와 상부층 두께를 반영한다.
- 동축 또는 2선식 프로브는 이상적 TEM 전파를 근사할 수 있다. 단일 rod·cable probe는 탱크벽, 노즐과 주변 구조가 귀환경로를 형성하는 실용적 guided 또는 quasi-TEM 구조이므로 항상 완전한 무분산 TEM이라고 단정하지 않는다. 연결부, 프로브 형상과 부착물은 링잉·감쇠·허위에코를 발생시킬 수 있다.
- GWR은 자유공간 레이더보다 좁은 공간, 내부구조물, 난류와 일부 거품 조건에 유리할 수 있지만 공정 영향에 면역인 것은 아니다. 저유전율, 두꺼운 거품·에멀전, 프로브 부착물, 인장하중, 휨·접촉, 고압증기와 상·하부 매질의 유전율 차이를 검토한다.

### 5. 기술사 답안 논리 위계

1. 자유공간 Pulse·FMCW와 GWR TDR을 구분한다.
2. 왕복거리식과 FMCW beat-frequency 식을 제시한다.
3. 유전율, 반사계수와 에코마진을 연결한다.
4. 노즐·내부구조·응축·부착물의 false echo를 분석한다.
5. threshold, false-echo map, echo tracking과 불감영역을 설명한다.
6. GWR의 전파경로·계면조건·프로브 기계조건을 설명한다.
7. 최대레벨과 독립 HH 과충전 방호를 연계한다.
