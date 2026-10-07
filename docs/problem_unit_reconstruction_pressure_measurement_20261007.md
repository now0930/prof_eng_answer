# 압력계측 센서 문제 단위 감사

검토일: 2026-10-07
대상: `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
판정 범위: 대표 질문의 문제 단위, Anchor 연결·선택성, 공통 채점 기준의 적용범위 및 인접 Topic ownership. 과거 출제 여부나 공식 출제분류를 인증하는 감사는 아니다.

## 판정

- 하나의 포괄적인 압력계측 지식 Pack으로는 유지한다. 압력 기준, 센서 원리, transmitter 선정, 오차·설치 문제는 공통 pressure-measurement 맥락을 공유하고, 기존 Router·taxonomy 변경 근거는 확인되지 않았다.
- 10개 expected question pattern은 서로 다른 직접 요구를 표현하며 예시 질문도 대응한다. 질문 패턴 자체는 변경하지 않았다.
- 자동 Anchor 연결 그래프는 3개 군을 만든다: pattern 1(pressure reference) 단독, pattern 2–7 및 9–10(8개 sensing/selection/installation/retrofit 패턴), pattern 8(error/calibration) 단독. 이는 질문들이 무관하다는 증거가 아니라 required Anchor를 공유하지 않는다는 구조 신호다. 압력 기준 정의와 종합 성능·보정은 특정 하위문제에서 독립적으로 물을 수 있으므로, 억지 Anchor를 추가해 연결 그래프를 꾸미지 않았다.
- 전체 22개 Anchor는 outline에 모두 연결되고 required-anchor union은 21/22다. `dp_level_boundary` 하나는 DP level owner 경계 설명용이므로 `optional`로 두고 어떤 expected-question pattern에서도 필수 답안요소로 요구하지 않는다.

## 변경

1. README와 Topic Sheet의 `IC-2027-W-2-1`을 공식 criterion 표기에서 내부 planning reference로 정정했다. 이 ID는 repository-local mapping이며 공식 분류나 기출 식별자가 아니다. 역사적 출제 빈도도 근거 부족으로 계속 사용하지 않는다.
2. `high_score_points`, `common_missing_points`, `high_band_unlock_conditions`에 pattern별 적용범위를 적었다. pattern 1의 pressure reference, pattern 2–7/9의 원리·선정·설치, pattern 8의 performance/calibration, pattern 10의 retrofit 기준을 서로 무관한 문제에 전역 필수요건처럼 적용하지 않는다.
3. DP-level hydrostatic conversion, wet/dry leg, density compensation은 인접 DP-level Topic의 소유범위임을 재확인했다. 이 경계는 routing/불필요한 혼입 방지에 사용하며, 일반 pressure 또는 DP-transmitter 문제에서 언급하지 않은 것을 감점하지 않는다.
4. scoring contract, deterministic scoring, Question Type, Topic routing, fatal rules, generated projection 및 release gate 동작은 변경하지 않았다.

## 기술 근거 확인

- WIKA의 Bourdon 원리 설명은 oval cross-section이 압력에 따라 원형에 가까워지고 관 끝 변위가 movement/pointer를 구동한다는 기존 설명을 뒷받침한다: [WIKA Bourdon functional principle](https://blog.wika.com/en/knowhow/bourdon-tube-pressure-gauge-functional-principle/).
- Emerson의 특정 transmitter reference manual은 static line pressure에 따른 zero/span 효과와 보정이 model/range에 따라 다름을 보여준다. 문서의 기존 주의 문구처럼 제품별 수치를 보편식으로 일반화하지 않는다: [Rosemount reference manual](https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/technical/products/pressure/documents/doc-rosemount-3051s-00809-0200-4802.pdf).

## 검증

- Focused Topic Pack test: 10/10 PASS
- Topic Pack schema: PASS (22개 Anchor, 전역 Anchor uniqueness 확인)
- Topic Pack quality: PASS (errors 0, warnings 0)
- Atomicity: PASS, warning 1건 유지 (`DISCONNECTED_QUESTION_FAMILIES: 1, 8, 1`). 이 경고는 여러 하위문항을 인위적으로 연결하지 않은 구조 신호로 본문에 설명했다.
- Scoped release: PASS (generated projection은 검증 뒤 원래 상태로 복원; promote하지 않음)
- Full regression: 본 source-only 수정은 기존 전체 release suite를 대체하지 않으며, dirty worktree 상태와 관련된 별도 release 검토에서 수행

## 다음

다음 screen 순서의 인접 Pack은 `pressure_transmitter_force_balance_null_detection`이다. 이번 감사는 후보 Pack의 내용 검토를 통과시킨 것이며, 전체 82개 Pack의 사실 완전성이나 사람 승인을 의미하지 않는다.
