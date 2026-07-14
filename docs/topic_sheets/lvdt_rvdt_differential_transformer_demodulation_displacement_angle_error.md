# LVDT·RVDT의 차동변압기 원리, 위상민감 복조, 변위·각도 측정 및 오차

## 1. 문서 목적

이 문서는 산업계측제어기술사 답안 채점 시스템에 다음 Topic Pack을 추가하기 위한 요구사항을 정의한다.

- Topic ID: `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`
- 한글 주제명: LVDT·RVDT의 차동변압기 원리, 위상민감 복조, 변위·각도 측정 및 오차
- 주요 측정량: 직선 변위, 위치, 간극, 스트로크, 회전각
- 주요 센서: LVDT, RVDT
- 주요 신호처리: 교류 여자, 차동출력, 위상민감 복조, 저역통과필터
- 주요 오차: 영점 잔류전압, 비선형, 정렬, 온도, 여자조건, 케이블, 자기포화

이 문서를 먼저 확정한 뒤 ChatGPT가 Source JSON을 직접 작성한다.

Gemini, Ollama 또는 다른 LLM이 JSON을 생성하지 않는다.

## 2. Topic 메타데이터

- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `THEORY_CORE`
- `selection_importance`: `CORE_MUST_PREPARE`
- `semantic_execution`: `LLM_ONLY`
- deterministic check: 비활성화
- deterministic fatal check: 빈 배열
- deterministic major check: 빈 배열
- candidate extraction: 빈 객체
- 독립 LLM 검증: 실행하지 않음
- 로컬 Ollama E2E: 실행하지 않음
- ChatGPT 수동 의미 검토: 필수

## 3. 핵심 평가 관점

고득점 답안은 다음 흐름을 논리적으로 연결해야 한다.

1. 1차 코일에 교류 전압을 인가한다.
2. 가동 철심 위치에 따라 두 2차 코일과의 상호인덕턴스가 달라진다.
3. 두 2차 코일은 직렬 역접속된다.
4. 차동출력은 두 2차 유도전압의 차로 결정된다.
5. 영점에서는 두 2차 전압의 크기가 같아 차동출력이 이상적으로 0이 된다.
6. 규정 선형범위에서는 출력 진폭이 변위량에 비례한다.
7. 기준 여자신호에 대한 출력 위상은 이동 방향을 나타낸다.
8. 위상민감 복조와 저역통과필터를 사용하면 부호가 있는 직류 변위신호를 얻을 수 있다.
9. 실제 측정에서는 영점 잔류전압, 정렬, 온도, 여자조건과 케이블 영향을 고려해야 한다.
10. RVDT는 동일한 차동변압기 개념을 회전각 측정에 적용한다.

## 4. LVDT 구조와 교류 여자

LVDT는 중앙의 1차 코일, 양쪽에 대칭으로 배치된 두 2차 코일과 코일 내부에서 이동하는 고투자율 가동 철심으로 구성된다.

가동 철심은 코일과 전기적으로 접속되지 않는다.

철심과 코일 보빈 사이에는 일반적으로 기계적 접촉이 없으므로 마찰과 전기 접점 마모가 작다.

1차 코일에는 교류 전압을 인가한다.

교류 자속은 가동 철심을 통해 두 2차 코일에 결합된다.

여자전압의 크기와 주파수는 다음 항목에 영향을 준다.

- 2차 유도전압
- 감도
- 위상
- 발열
- 자기포화
- 주파수응답
- 신호대잡음비

따라서 여자조건은 센서와 신호조절기의 사양에 맞게 유지해야 한다.

## 5. 차동출력과 영점

두 2차 코일은 직렬 역접속한다.

차동출력은 다음 관계로 표현한다.

\[
E_o=E_{s1}-E_{s2}
\]

여기서 \(E_o\)는 차동출력이고, \(E_{s1}\)과 \(E_{s2}\)는 각 2차 코일의 유도전압이다.

철심이 전기적 중앙에 위치하면 두 2차 코일과의 결합이 대칭이 된다.

이상적인 영점에서는 다음 관계가 성립한다.

\[
|E_{s1}|=|E_{s2}|
\]

따라서,

\[
E_o\approx0
\]

영점에서 두 2차 전압이 각각 0이 되는 것은 아니다.

두 전압의 크기가 같고 직렬 역접속되어 상쇄되는 것이다.

두 2차 코일을 같은 극성으로 연결하면 공통성분이 더해지므로 정상적인 차동 위치검출 기능을 얻을 수 없다.

## 6. 변위량과 이동 방향

철심이 한쪽으로 이동하면 가까운 2차 코일과의 상호인덕턴스가 증가하고 반대쪽 코일과의 상호인덕턴스는 감소한다.

영점 부근의 규정 선형범위에서는 다음과 같이 표현할 수 있다.

\[
|E_o|\approx K_x|x|
\]

여기서 \(K_x\)는 변위 감도이고 \(x\)는 영점으로부터의 변위이다.

출력 진폭은 변위량을 나타낸다.

출력 위상은 기준 여자신호에 대한 이동 방향을 나타낸다.

한쪽 방향에서는 기준신호와 동상에 가까운 출력이 발생하고 반대 방향에서는 약 180도 반전된 출력이 발생한다.

따라서 절댓값 또는 단순 정류만으로는 방향정보가 손실될 수 있다.

## 7. 위상민감 복조와 저역통과필터

LVDT의 원시 출력은 교류 반송파에 변위정보가 실린 신호이다.

PLC, 데이터수집장치 또는 제어기가 사용하기 쉬운 직류 신호로 변환하려면 복조가 필요하다.

위상민감 복조기는 다음 두 정보를 함께 사용한다.

- LVDT 차동출력의 진폭
- 기준 여자신호에 대한 위상

위상민감 복조를 적용하면 영점을 기준으로 양수와 음수의 부호가 있는 변위신호를 얻을 수 있다.

개념적으로 다음과 같이 표현할 수 있다.

\[
V_{dc}\approx K_d x
\]

동기검파 후에는 반송파와 고조파 성분이 남을 수 있다.

저역통과필터는 다음 기능을 수행한다.

- 반송파 제거
- 고주파 잡음 억제
- 직류 변위성분 추출
- 출력 리플 감소

필터 차단주파수를 지나치게 낮게 설정하면 응답이 느려진다.

지나치게 높게 설정하면 반송파 리플과 잡음이 증가할 수 있다.

## 8. 신호조절 및 측정사슬

대표적인 측정사슬은 다음과 같다.

1. 교류 여자발생기
2. LVDT 1차 코일
3. 가동 철심과 두 2차 코일
4. 차동출력
5. 증폭기
6. 위상민감 복조기
7. 저역통과필터
8. 영점과 감도 조정
9. 전압 또는 전류 출력
10. ADC, PLC 또는 제어기

출력 형식은 다음과 같이 구성할 수 있다.

- 양·음 직류전압
- 0–10 V
- ±10 V
- 4–20 mA
- 디지털 변위값

## 9. 선형범위와 동특성

LVDT의 출력은 전체 철심 이동범위에서 완전히 선형이지 않다.

영점 부근의 규정 범위에서만 변위와 출력의 비례관계가 충분히 유지된다.

선형범위를 벗어나면 다음 영향이 커질 수 있다.

- 자기회로 비대칭
- 누설자속
- 결합계수 비선형
- 끝단효과
- 감도 변화
- 위상오차

LVDT의 동특성은 다음 요소의 영향을 받는다.

- 철심과 연결부의 질량
- 기계적 설치강성
- 이동기구의 마찰과 유격
- 여자주파수
- 복조기 대역폭
- 저역통과필터 차단주파수
- 출력 증폭기 대역폭
- 케이블과 입력회로

측정대역은 기계계와 전기 신호조절계의 대역폭을 함께 고려해야 한다.

## 10. 주요 오차

### 10.1 영점 잔류전압

실제 영점에서는 차동출력이 완전히 0이 되지 않을 수 있다.

주요 원인은 다음과 같다.

- 두 2차 코일의 권선 불균형
- 기생 정전용량
- 누설자속
- 여자파형의 고조파
- 철심과 코일의 비대칭
- 복조기 위상오차

영점 잔류전압은 단순 영점조정만으로 완전히 제거되지 않을 수 있다.

### 10.2 정렬과 편심

철심이 코일 축과 일치하지 않으면 다음 문제가 발생할 수 있다.

- 결합계수 비대칭
- 출력 비선형
- 반복성 저하
- 기계적 마찰
- 히스테리시스
- 영점 이동

센서 본체와 이동축의 동심도 및 축 정렬을 확보해야 한다.

### 10.3 온도

온도변화는 코일저항, 여자전류, 감도, 영점, 절연특성, 전자회로 오프셋과 기계구조의 열팽창에 영향을 준다.

온도보상은 센서, 신호조절기와 설치구조를 함께 고려해야 한다.

### 10.4 여자조건과 자기포화

여자전압 또는 주파수가 규정값에서 벗어나면 다음 문제가 발생할 수 있다.

- 감도 변화
- 위상 변화
- 발열
- 신호대잡음비 저하
- 자기포화
- 복조 기준 불일치

과도한 여자 또는 부적절한 자기회로 조건에서는 철심이나 자기회로가 포화될 수 있다.

자기포화는 파형 왜곡, 고조파 증가, 감도 비선형, 영점 잔류전압과 복조오차를 증가시킨다.

### 10.5 케이블, 차폐와 접지

장거리 케이블과 불완전한 배선은 다음 영향을 줄 수 있다.

- 케이블 정전용량
- 신호 감쇠
- 위상 변화
- 전자기 유도잡음
- 접지루프
- 공통모드 잡음
- 영점 불안정

센서 제조사가 지정한 케이블, 차폐와 접지방법을 적용해야 한다.

## 11. RVDT

RVDT는 차동변압기 원리를 회전각 측정에 적용한 센서이다.

주요 구성은 다음과 같다.

- 교류 여자되는 1차 권선
- 차동으로 연결된 2차 권선
- 회전하는 자성 로터 또는 코어
- 위상민감 복조기
- 각도 출력회로

영점 부근의 규정 각도범위에서는 출력이 회전각에 근사적으로 비례한다.

RVDT도 출력 진폭은 각도 크기, 출력 위상은 회전 방향과 관련된다.

RVDT는 전체 회전범위에서 완전 선형이지 않으며 규정 각도범위와 장착 정렬을 준수해야 한다.

RVDT는 직선 변위센서가 아니다.

## 12. 적용 사례

- 유압실린더 또는 공압실린더 스트로크 측정
- 제어밸브 스템 위치 피드백
- 프레스와 성형설비 변위 측정
- 서보시스템 위치 피드백
- 터빈 또는 대형기계의 밸브 위치
- 재료시험기의 변위 측정
- 치수와 간극 측정
- 로봇과 자동화설비의 위치 확인
- 항공·방산 액추에이터 위치
- RVDT를 이용한 회전축 또는 링크 각도 측정

## 13. 기존 Topic과의 라우팅 경계

### 13.1 수동센서 일반 Topic

다음 질문은 LVDT/RVDT Topic을 우선한다.

- LVDT의 원리를 설명하시오.
- 차동변압기식 변위센서를 설명하시오.
- LVDT의 영점과 차동출력을 설명하시오.
- LVDT의 위상민감 복조를 설명하시오.
- LVDT와 RVDT를 비교하시오.

다음 질문은 기존 수동센서 일반 Topic을 유지한다.

- 저항형·용량형·유도형 센서를 비교하시오.
- 수동센서의 변환원리를 설명하시오.
- 유도형 센서의 일반적인 원리를 설명하시오.

### 13.2 스트레인 게이지·로드셀 Topic

다음 요소가 중심이면 스트레인 게이지·로드셀 Topic이다.

- 게이지율
- Wheatstone bridge
- mV/V
- 탄성체
- 크리프
- 정하중 측정

다음 요소가 중심이면 LVDT/RVDT Topic이다.

- 차동변압기
- 가동 철심
- 직렬 역접속
- 교류 여자
- 위상민감 복조
- 직선 변위
- 회전각

### 13.3 압전식 센서 Topic

다음 요소가 중심이면 압전식 센서 Topic이다.

- 직접 압전효과
- 전하출력
- 전하증폭기
- IEPE
- 동적 힘
- 동압
- 가속도

다음 요소가 중심이면 LVDT/RVDT Topic이다.

- 위치와 변위
- 상호인덕턴스
- 차동출력
- 영점
- 출력 위상
- 동기검파

### 13.4 다른 변위센서와의 경계

- 와전류센서: 도전성 측정물, 고주파 코일, 표면 간극
- 정전용량형 센서: 전극면적, 전극간격, 유전율
- 포텐쇼미터: 접촉식 저항 분압
- 엔코더: 광학 또는 자기식 펄스와 디지털 위치
- 초음파센서: 전파시간
- 레이저 변위센서: 삼각측량 또는 시간비행

## 14. Fact Anchor 후보

다음 20개를 정확한 Source Anchor 계약으로 사용한다.

1. `lvdt_differential_transformer_structure` — 1차 코일, 두 2차 코일과 가동 철심으로 구성되는 차동변압기 구조
2. `lvdt_primary_ac_excitation` — 1차 코일 교류 여자와 교류 자속 발생
3. `lvdt_secondary_series_opposition` — 두 2차 코일의 직렬 역접속
4. `lvdt_core_position_mutual_inductance` — 철심 위치에 따른 상호인덕턴스와 결합계수 변화
5. `lvdt_differential_output_es1_es2` — 차동출력 \(E_o=E_{s1}-E_{s2}\)
6. `lvdt_null_position_voltage_balance` — 영점에서 두 2차 전압의 크기가 같아 차동출력이 상쇄되는 원리
7. `lvdt_output_amplitude_displacement` — 선형범위에서 출력 진폭과 변위량의 관계
8. `lvdt_output_phase_direction` — 기준 여자신호에 대한 출력 위상과 이동 방향의 관계
9. `lvdt_linear_measurement_range` — 영점 부근 규정 선형범위와 범위 초과 시 비선형
10. `lvdt_null_residual_voltage` — 권선 불균형, 기생성분과 고조파에 의한 영점 잔류전압
11. `lvdt_phase_sensitive_demodulation` — 위상민감 복조 또는 동기검파를 통한 방향 판별
12. `lvdt_low_pass_dc_output` — 저역통과필터에 의한 반송파 제거와 직류 출력 생성
13. `lvdt_excitation_frequency_voltage_sensitivity` — 여자전압·주파수가 감도, 위상과 발열에 미치는 영향
14. `lvdt_core_alignment_eccentricity_error` — 철심 편심, 축 정렬과 기계적 유격 오차
15. `lvdt_temperature_coil_resistance_error` — 온도에 따른 코일저항, 감도와 영점 변화
16. `lvdt_magnetic_saturation_nonlinearity` — 자기포화, 파형왜곡과 비선형
17. `lvdt_cable_shield_grounding_error` — 케이블, 차폐, 접지와 전자기 잡음 영향
18. `lvdt_dynamic_response_frequency_bandwidth` — 기계계, 여자, 복조기와 필터에 의한 동특성
19. `rvdt_rotary_angle_measurement` — RVDT의 회전각 측정원리와 제한 각도범위
20. `lvdt_calibration_traceability_diagnostics` — 영점, 감도, 선형성 교정과 추적성 및 상태진단

## 15. Fatal Wrong Claim 후보

다음 10개를 정확한 Fatal 계약으로 사용한다.

1. `lvdt_fatal_dc_excitation`
   - 잘못된 주장: LVDT의 1차 코일은 직류로 여자한다.
   - 교정: LVDT는 교류 여자와 교류 자속을 이용한다.

2. `lvdt_fatal_secondary_same_polarity_series`
   - 잘못된 주장: 두 2차 코일은 같은 극성으로 직렬 연결한다.
   - 교정: 두 2차 코일은 차동출력을 얻기 위해 직렬 역접속한다.

3. `lvdt_fatal_each_secondary_zero_at_null`
   - 잘못된 주장: 영점에서 두 2차 코일의 전압이 각각 0이 된다.
   - 교정: 두 2차 전압의 크기가 같아 직렬 역접속 차동출력이 이상적으로 0이 된다.

4. `lvdt_fatal_amplitude_alone_direction`
   - 잘못된 주장: 출력 진폭만으로 변위량과 이동 방향을 모두 판별한다.
   - 교정: 진폭은 변위량을 나타내고 기준 여자신호에 대한 위상은 방향을 나타낸다.

5. `lvdt_fatal_output_always_dc`
   - 잘못된 주장: LVDT의 원시 출력은 항상 직류이다.
   - 교정: 원시 차동출력은 교류이며 직류 신호에는 복조와 필터가 필요하다.

6. `lvdt_fatal_full_range_perfect_linearity`
   - 잘못된 주장: LVDT는 철심의 전체 이동범위에서 완전히 선형이다.
   - 교정: 규정된 영점 부근 선형범위에서만 충분한 비례관계를 보장한다.

7. `lvdt_fatal_excitation_no_effect`
   - 잘못된 주장: 여자전압과 여자주파수는 감도와 동특성에 영향을 주지 않는다.
   - 교정: 여자조건은 감도, 위상, 발열, 포화와 주파수응답에 영향을 준다.

8. `lvdt_fatal_core_contact_required`
   - 잘못된 주장: LVDT 철심은 코일과 접촉해야 정상적으로 측정한다.
   - 교정: 철심은 자기결합을 변화시키며 일반적으로 코일과 접촉하지 않는다.

9. `lvdt_fatal_no_null_residual`
   - 잘못된 주장: 실제 LVDT에서는 영점 잔류전압이 발생하지 않는다.
   - 교정: 권선 불균형, 기생 정전용량, 고조파와 비대칭으로 영점 잔류전압이 발생할 수 있다.

10. `rvdt_fatal_linear_displacement_only`
    - 잘못된 주장: RVDT는 직선 변위만 측정한다.
    - 교정: RVDT는 차동변압기 원리를 이용하여 제한된 범위의 회전각을 측정한다.

## 16. Routing Alias 후보

다음 32개를 Routing Alias 후보로 사용한다.

기존 수동센서 일반 Topic이 단독 약어 `LVDT`를 이미 보유하므로 신규 Topic에서는 이를 중복 등록하지 않는다.

직접적인 LVDT 질문은 구체적인 복합 Alias, Question Example과 Expected Question Pattern으로 신규 Topic을 식별한다.

1. `linear variable differential transformer`
2. `linear differential transformer`
3. `LVDT sensor`
4. `LVDT displacement sensor`
5. `LVDT displacement transducer`
6. `LVDT position sensor`
7. `LVDT signal conditioner`
8. `LVDT demodulator`
9. `LVDT movable core`
10. `LVDT primary coil`
11. `LVDT secondary coils`
12. `LVDT series opposition`
13. `LVDT differential output`
14. `LVDT null position`
15. `LVDT null voltage`
16. `LVDT residual voltage`
17. `LVDT phase-sensitive demodulation`
18. `LVDT synchronous demodulation`
19. `LVDT carrier demodulation`
20. `차동변압기`
21. `차동 변압기`
22. `리니어 차동변압기`
23. `LVDT 변위센서`
24. `LVDT 위치센서`
25. `LVDT 가동 철심`
26. `LVDT 직렬 역접속`
27. `LVDT 차동 출력`
28. `LVDT 영점 잔류전압`
29. `LVDT 위상민감 복조`
30. `RVDT`
31. `rotary variable differential transformer`
32. `회전형 차동변압기`

## 17. Routing Field Point 후보

다음 5개를 Routing Field Point 후보로 사용한다.

1. 1차 코일의 교류 여자와 두 2차 코일의 직렬 역접속
2. 가동 철심 위치에 따른 상호인덕턴스와 차동출력 변화
3. 출력 진폭과 변위량, 출력 위상과 이동 방향의 구분
4. 위상민감 복조, 저역통과필터와 부호가 있는 직류 출력
5. 영점 잔류전압, 선형범위, 설치·온도·여자·케이블 오차와 RVDT 적용

## 18. Question Example 후보

다음 14개를 Question Example 후보로 사용한다.

1. LVDT의 원리와 특징을 설명하시오.
2. 차동변압기식 변위센서의 구조와 동작원리를 설명하시오.
3. LVDT의 영점과 차동출력 관계를 설명하시오.
4. LVDT 출력의 진폭과 위상이 나타내는 물리량을 설명하시오.
5. LVDT 신호조절에서 위상민감 복조가 필요한 이유를 설명하시오.
6. LVDT의 여자전압과 여자주파수가 측정에 미치는 영향을 설명하시오.
7. LVDT의 선형범위와 비선형 오차를 설명하시오.
8. LVDT의 영점 잔류전압 원인과 대책을 설명하시오.
9. LVDT 설치 시 철심 편심과 축 정렬 오차를 설명하시오.
10. LVDT의 온도, 케이블, 차폐와 접지 영향을 설명하시오.
11. LVDT의 동특성과 측정대역 결정요인을 설명하시오.
12. RVDT의 원리와 회전각 측정 특성을 설명하시오.
13. LVDT와 스트레인 게이지식 변위센서를 비교하시오.
14. LVDT와 RVDT의 공통점과 차이점을 설명하시오.

## 19. Expected Question Pattern 후보

다음 14개 패턴과 Anchor 연결을 Source 계약으로 사용한다.

1. LVDT 원리
   - `lvdt_differential_transformer_structure`
   - `lvdt_primary_ac_excitation`
   - `lvdt_secondary_series_opposition`
   - `lvdt_core_position_mutual_inductance`

2. 차동변압기식 변위센서 구조
   - `lvdt_differential_transformer_structure`
   - `lvdt_secondary_series_opposition`
   - `lvdt_differential_output_es1_es2`

3. 영점과 차동출력
   - `lvdt_differential_output_es1_es2`
   - `lvdt_null_position_voltage_balance`
   - `lvdt_null_residual_voltage`

4. 출력 진폭과 위상
   - `lvdt_output_amplitude_displacement`
   - `lvdt_output_phase_direction`

5. 위상민감 복조
   - `lvdt_output_phase_direction`
   - `lvdt_phase_sensitive_demodulation`
   - `lvdt_low_pass_dc_output`

6. 여자전압과 여자주파수
   - `lvdt_primary_ac_excitation`
   - `lvdt_excitation_frequency_voltage_sensitivity`
   - `lvdt_magnetic_saturation_nonlinearity`

7. 선형범위와 비선형
   - `lvdt_output_amplitude_displacement`
   - `lvdt_linear_measurement_range`
   - `lvdt_magnetic_saturation_nonlinearity`

8. 영점 잔류전압
   - `lvdt_null_position_voltage_balance`
   - `lvdt_null_residual_voltage`
   - `lvdt_phase_sensitive_demodulation`

9. 설치와 정렬
   - `lvdt_core_alignment_eccentricity_error`
   - `lvdt_linear_measurement_range`
   - `lvdt_calibration_traceability_diagnostics`

10. 온도와 배선오차
    - `lvdt_temperature_coil_resistance_error`
    - `lvdt_cable_shield_grounding_error`
    - `lvdt_calibration_traceability_diagnostics`

11. 동특성과 대역폭
    - `lvdt_dynamic_response_frequency_bandwidth`
    - `lvdt_excitation_frequency_voltage_sensitivity`
    - `lvdt_low_pass_dc_output`

12. RVDT 원리
    - `rvdt_rotary_angle_measurement`
    - `lvdt_output_amplitude_displacement`
    - `lvdt_output_phase_direction`

13. LVDT와 스트레인 게이지식 변위센서 비교
    - `lvdt_differential_transformer_structure`
    - `lvdt_linear_measurement_range`
    - `lvdt_dynamic_response_frequency_bandwidth`
    - `lvdt_calibration_traceability_diagnostics`

14. LVDT와 RVDT 비교
    - `lvdt_differential_transformer_structure`
    - `rvdt_rotary_angle_measurement`
    - `lvdt_phase_sensitive_demodulation`

## 20. 권장 답안 구조

1. 배경과 적용 목적
2. LVDT 구조
3. 1차 코일 교류 여자
4. 가동 철심과 상호인덕턴스 변화
5. 두 2차 코일의 직렬 역접속
6. \(E_o=E_{s1}-E_{s2}\)
7. 영점의 전압 평형
8. 출력 진폭과 변위량
9. 출력 위상과 이동 방향
10. 위상민감 복조와 저역통과필터
11. 선형범위와 동특성
12. 영점·정렬·온도·여자·케이블 오차
13. RVDT 회전각 측정
14. 현장 적용과 교정

## 21. 고득점 요소

- 영점에서 두 2차 전압이 각각 0이 아니라 크기가 같아 상쇄된다고 설명한다.
- 두 2차 코일의 직렬 역접속 이유를 설명한다.
- 차동출력 \(E_o=E_{s1}-E_{s2}\)를 제시한다.
- 진폭과 위상이 각각 변위량과 방향을 나타낸다고 구분한다.
- 위상민감 복조의 필요성을 설명한다.
- 복조 후 저역통과필터의 반송파 제거 역할을 설명한다.
- 선형범위를 벗어나면 비선형이 증가한다고 설명한다.
- 영점 잔류전압의 실제 원인을 설명한다.
- 여자조건, 정렬, 온도와 케이블을 하나의 측정사슬 관점에서 설명한다.
- RVDT가 회전각 측정용임을 구분한다.
- 교정, 추적성과 상태진단을 현장 적용과 연결한다.

## 22. 공통 누락 요소

- 직렬 역접속 누락
- 영점 상쇄원리 누락
- 진폭과 위상의 역할 혼동
- 복조기 누락
- 저역통과필터 누락
- 선형범위 누락
- 영점 잔류전압 누락
- 정렬과 편심오차 누락
- 여자주파수 영향 누락
- RVDT와 LVDT 구분 누락
- 교정과 추적성 누락

## 23. 저득점 패턴

- LVDT를 단순 유도형 근접센서로만 설명
- 직류 여자라고 설명
- 두 2차 코일을 같은 극성으로 연결한다고 설명
- 영점에서 각 2차 전압이 0이라고 설명
- 출력 진폭만으로 방향까지 판단한다고 설명
- 원시 출력이 직류라고 설명
- 전체 이동범위가 완전 선형이라고 설명
- 여자조건은 영향이 없다고 설명
- 철심과 코일이 접촉해야 한다고 설명
- RVDT를 직선 변위센서라고 설명

## 24. 구현 대상 파일

요구사항 검토가 끝나면 다음 Source 파일을 작성한다.

- `rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/README.md`
- `rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/fact_anchor.json`
- `rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/logic_check.json`
- `rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/model_answer.json`
- `rubrics/topic_packs/lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error/topic_importance.json`

Source JSON은 ChatGPT가 기존 스키마와 생산 빌더 계약을 확인한 뒤 직접 작성한다.

## 25. Generated 반영 원칙

Source 파일이 검증되면 생산 빌더로 다음 파일을 재생성한다.

- `rubrics/generated/fact_anchors.generated.json`
- `rubrics/generated/logic_check_profiles.generated.json`
- `rubrics/generated/logic_checks.generated.json`
- `rubrics/generated/model_answers.generated.json`
- `rubrics/generated/topic_importance.generated.json`
- `rubrics/generated/topic_pack_manifest.generated.json`

기존 Topic 레코드는 변경하지 않는다.

신규 Topic은 Topic ID 기준 정렬 위치에 삽입한다.

## 26. Router 회귀 테스트 요구사항

최소 다음 경계를 검증한다.

1. LVDT 직접 질문은 LVDT/RVDT Topic을 선택한다.
2. 차동변압기식 변위센서 질문은 LVDT/RVDT Topic을 선택한다.
3. 위상민감 복조 질문은 LVDT/RVDT Topic을 선택한다.
4. RVDT 회전각 질문은 LVDT/RVDT Topic을 선택한다.
5. 일반 수동센서 비교 질문은 기존 수동센서 Topic을 유지한다.
6. 스트레인 게이지 중심 질문은 스트레인 게이지 Topic을 유지한다.
7. 압전식 힘·압력·가속도 질문은 압전식 Topic을 유지한다.
8. LVDT 중심 비교 질문은 LVDT/RVDT Topic을 Primary로 유지한다.
9. LVDT 답안에 strain 또는 piezo 키워드가 있어도 중심 Topic이 누출되지 않아야 한다.
10. 직접 실행과 module discovery의 테스트 수가 일치해야 한다.

## 27. 검증 범위

이번 Topic Pack은 다음 검증만 수행한다.

- Source JSON schema와 필드 검증
- 정확히 20개 Fact Anchor
- 정확히 10개 Fatal Wrong Claim
- Source/Generated 일치
- 기존 Topic 레코드 불변성
- 생산 빌더 의미적 멱등성
- Router focused regression
- Router 전체 테스트 파일
- direct 실행과 module discovery 일치
- `git diff --check`
- 정확한 변경 파일 경계
- ChatGPT 수동 의미 검토

다음 검증은 수행하지 않는다.

- 독립 LLM 의미 평가
- Gemini 평가
- 로컬 Ollama 호출
- 컨테이너 E2E
- 전체 저장소 회귀 테스트

## 28. 완료 조건

다음 조건을 모두 만족해야 한다.

- 요구사항 Markdown에 정확히 20개 Anchor ID가 명시된다.
- Source에 정확히 같은 20개 Anchor ID가 작성된다.
- Generated에 정확히 같은 20개 Anchor ID가 반영된다.
- Fatal Wrong Claim은 정확히 10개이다.
- deterministic check는 비활성화된다.
- candidate extraction은 빈 객체이다.
- LVDT와 일반 수동센서의 라우팅 경계가 유지된다.
- LVDT와 스트레인 게이지의 라우팅 경계가 유지된다.
- LVDT와 압전식 센서의 라우팅 경계가 유지된다.
- RVDT 회전각 질문이 신규 Topic으로 라우팅된다.
- 생산 빌더와 생산 Router는 수정하지 않는다.
- 테스트 수는 하드코딩하지 않고 동적으로 검증한다.
- 최종 변경 파일만 정확히 stage, commit, push한다.
