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
