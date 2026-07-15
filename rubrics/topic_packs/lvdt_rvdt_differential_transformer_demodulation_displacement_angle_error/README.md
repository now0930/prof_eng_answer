# LVDT·RVDT의 차동변압기 원리, 위상민감 복조, 변위·각도 측정 및 오차

## Topic Pack 개요

- Topic ID: `lvdt_rvdt_differential_transformer_demodulation_displacement_angle_error`
- 문제유형: `PRINCIPLE_INTERPRETATION`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 의미평가: `LLM_ONLY`
- deterministic check: disabled
- candidate extraction: empty

## 평가 범위

이 Topic Pack은 LVDT의 교류 여자, 직렬 역접속, 차동출력, 영점 평형, 진폭·위상 해석, 위상민감 복조와 저역통과필터를 평가한다.

또한 규정 선형범위, 영점 잔류전압, 철심 정렬, 온도, 여자조건, 자기포화, 케이블·차폐·접지, 동특성, 교정과 RVDT 회전각 측정을 평가한다.

## Source 계약

- 핵심 사실 Anchor: 20개
- Fatal Wrong Claim: 10개
- Routing Alias: 32개
- Routing Field Point: 5개
- Question Example: 14개
- Expected Question Pattern: 14개

## 라우팅 경계

- 일반 저항형·용량형·유도형 센서 비교는 기존 수동센서 일반 Topic을 유지한다.
- 게이지율, Wheatstone bridge와 탄성체 변형은 스트레인 게이지·로드셀 Topic을 유지한다.
- 전하출력, 전하증폭기, IEPE와 동적 힘·압력·가속도는 압전식 센서 Topic을 유지한다.
- LVDT의 차동변압기 구조, 위치·변위, 영점, 출력 위상과 복조가 중심이면 이 Topic을 우선한다.
- RVDT의 회전각 측정 질문은 이 Topic을 우선한다.
- 단독 약어 `LVDT`는 기존 수동센서 일반 Topic의 Alias와 중복되므로 신규 Routing Alias에는 등록하지 않는다.

## 검증 정책

ChatGPT가 요구사항 Markdown과 현대형 Topic Pack 스키마를 바탕으로 Source JSON을 직접 작성한다.

독립 LLM 의미평가, Gemini, 로컬 Ollama와 컨테이너 E2E는 실행하지 않는다.

## LVDT·RVDT 적용조건

- 두 2차 전압은 페이저 또는 동일 기준의 순간신호로 비교한다. 이상적인 전기적 영점에서는 두 2차 전압의 크기와 위상이 같아 E_s1=E_s2가 되고 직렬 역접속 차동출력 E_o=E_s1-E_s2는 0이 된다. 두 2차 전압 각각이 0이 되는 것은 아니다.
- 실제 LVDT의 전기적 영점에서는 권선 불균형, 기생 정전용량, 누설자속, 여자 고조파와 자기회로 비대칭 때문에 원시 차동 AC 출력에 null residual voltage가 남을 수 있다.
- 복조 후 DC zero offset은 기준위상 오차, 위상보상 불량, 증폭기 오프셋과 온도 드리프트 때문에 발생할 수 있다. 이는 센서 원시 AC null residual voltage와 구분하여 교정하고 진단한다.
- 위상민감 복조와 저역통과필터는 대표적인 부호 변위 복원 방식이다. 두 2차 신호를 개별 취득하여 정류·필터링한 뒤 V_A-V_B 또는 (V_A-V_B)/(V_A+V_B)를 계산하는 방식도 합 신호가 유효하고 적용조건을 설명하면 정답으로 인정한다.
- 두 이동 방향의 차동출력은 영점을 기준으로 약 180도의 상대 위상반전을 보인다. 실제 방향 판별은 센서, 케이블과 신호조절기의 위상지연을 고려한 기준위상 또는 동등한 극성 판별 방식으로 수행한다.
- LVDT 변위정보는 여자 반송파의 포락선에 실리므로 여자주파수는 요구 기계적 측정대역보다 충분히 높아야 한다. 구체적인 비율과 여자전압은 센서 및 신호조절기의 허용 주파수, 감도, 발열과 자기포화 사양을 함께 확인하여 선정한다.
- 복조 후 필터 대역폭을 높이면 응답은 빨라지지만 반송파 리플과 잡음이 증가할 수 있다. 대역폭을 낮추면 리플은 감소하지만 응답지연이 증가하므로 요구 동특성과 출력 리플을 함께 검증한다.
- RVDT는 회전각을 차동출력으로 변환하지만 선형 각도범위와 허용 비선형은 제품의 자기회로, 권선과 기구 설계에 따라 달라진다. 특정 각도값을 모든 RVDT에 일반화하지 않고 제조사 교정범위와 데이터시트를 확인한다.
- Fatal의 직접 점수 영향은 B/C에 한정한다. D/E 점수는 직접 변경하지 않고 관련 현장 적용·제언의 claim trust만 limited로 표시한다.

## Fact verification references

- TE Connectivity `LVDT Tutorial`
- NewTek LVDT technical guidance
- Analog Devices AD598 data sheet
- United Electronic Industries LVDT/RVDT tutorial
- Manufacturer RVDT product data
