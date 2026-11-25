# PR #46 관계 인식 구조 재평가

기준 `c8f21e8ece3e71b51394d8c75b25e70d8173a4fd`. 관계 비교기는 여러 Topic에서 재사용할 수 있다. 현재 자연어 추출과 Machine Contract 적용 범위로 정본 2,096개 전체에 확장할 근거는 확보되지 않았다. 채점 변경은 적용하지 않았다. Registry 11건의 검토 결과와 승인 대상 5개 문장은 [별도 검토 문서](pr46_registry_source_review_proposals.md)에 있다.

## 실제 실행 경로

`deterministic_primary_grader`는 질문 라우팅 후 canonical extractor와 수량 차원 및 공학 검증을 실행한다. Fact Anchor adapter는 제외 Overlay와 질문 범위를 거쳐 근거를 계산한다. 속도·습도 등 9개 Topic/Anchor 키는 개별 관계표에서 다루고, 엔코더 주파수는 별도 guard, 열전대 비교는 cross-topic 계약에서 평가한다. Machine Contract evaluator의 판정과 Anchor 근거를 합치기 전후로 상태를 따로 확인했다. 미인정 20건 모두 해당 대상 Machine Contract 규칙이 없었고, canonical extractor가 생성한 관계 claim은 0건이었다. 17건의 Anchor adapter 대상 상태가 `MISSING`, 열전대 3건은 cross-topic 경로의 대상 상태가 `MISSING`이었다. 따라서 대상 관계를 이미 인식한 뒤 점수 투영에서 잃은 사례는 확인되지 않았다.

### 신규 미인정 20건의 전수 분류

ID의 숫자는 고정된 신규 55건에서 해당 Anchor의 답안 순서다. 아래 판정은 개발용 사례의 기술적·문항 범위 검토다. 3개 PST 사례는 명시적 질문과 내부 선택의 범위가 다르므로 기대 정답 집계에 그대로 사용하기 어렵다. 기존 기대값과 143건의 입력은 보존했다.

| Anchor / 사례 | 주 원인 | 기술 내용과 문항 범위 판단 |
|---|---|---|
| encoder_frequency_limit_selection / 1 | 수식·수치 | 채널 출력, 수신·송신 한계, 체배 처리를 분리한다. 식의 계수와 단위는 생략했으므로 개념 인정 가능. |
| encoder_frequency_limit_selection / 2 | 수식·수치 | 1,800 rpm × 200주기/회전 ÷ 60 = 6 kHz, x4 계수율 24,000/s가 맞다. 사양 대조까지 서술하지 않아 부분 인정 가능. |
| encoder_frequency_limit_selection / 3 | 비례·반비례 | 같은 속도에서 회전당 채널 주기 증가와 두 한계 구분은 관련 있다. ‘신호 대역’은 채널 펄스 주파수 자체인지 불분명해 완전 인정 보류. |
| counting_window_speed_equation / 3 | 수식·수치 | 60/(600×0.5) = 0.2 rpm/계수와 저속 상대 효과가 타당하다. 고정 설정 수치를 관계 조건으로 인식하지 못했다. |
| gear_tooth_speed_equation / 3 | 수식·수치 | 정규 피치에서 연속 두 치가 빠진 구간은 세 피치로 환산한다. 한 바퀴 평균 관계는 없으므로 국부 관계만 인정 가능. |
| absolute_humidity_definition / 1 | 개념·동의어 | 1 m³ 안의 기체 상태 물 질량은 정의를 충족한다. RH·이슬점 비교는 다른 요구사항이다. |
| absolute_humidity_definition / 3 | 수식·수치 | 12 g/2 m³ = 6 g/m³가 타당하다. 단위 표기 정규화와 질량/체적 바인딩이 필요하며 단위 환산 자체는 없다. |
| sw04_hil / 1 | 개념·동의어 | 실제 보드에 모의 센서 입력을 공급하고 출력을 플랜트 모델에 돌려주는 폐루프 관계가 맞다. |
| sw04_hil / 2 | 개념·동의어 | 현물 제어기와 실시간 모의 공정의 I/O는 첫 문장에 있다. 뒤 문장의 시운전은 별개 적용 근거다. 주 관계에 문장 간 조건 결합은 불필요하다. |
| sw04_hil / 3 | 개념·동의어 | 실시간 모델 중심 어순에서도 실제 PLC와 폐루프가 확인된다. 파서는 PLC 개념만 표시했다. |
| thermocouple_measures_temperature_difference / 1 | 개념·동의어 | 형식에 따른 재료쌍과 두 온도의 관계가 맞다. ‘제벡 전압’ 및 ‘접합부’ 서술이 cross-topic 요구 패턴에 맞지 않았다. |
| thermocouple_measures_temperature_difference / 2 | 적용범위·조건 | 같은 종류와 고정된 기준 접합부를 명시했다. 유효 변환범위에서 의미 있는 조건부 설명이다. |
| thermocouple_measures_temperature_difference / 3 | 개념·동의어 | 제벡 기전력과 두 접합점의 설명은 기본 원리의 부분 진술이다. 모든 기준온도에서 같은 온도차의 전압이 같다고 주장하지 않았다. |
| imperfect_test_residual_risk / 3 | 적용범위·조건 | 교체 전까지 드러나지 않는다고 한 고장에 한정해 노출을 모델에 남기는 설명이다. 부분시험의 검출 범위는 명시되지 않아 부분 진술이다. |
| response_time_process_safety_time / 1 | 적용범위·기대값 | 전체 SIF와 최종요소 시간 구분은 타당하다. 질문 자체는 Safe State, fail action, de-energize 철학의 일치성을 요구한다. |
| response_time_process_safety_time / 2 | 적용범위·기대값 | 전체 5초와 최종요소 1초 예시는 올바른 별도 시간 한계다. 위 질문의 명시적 요구범위와는 다르다. |
| response_time_process_safety_time / 3 | 적용범위·기대값 | 센서 및 논리 시간을 포함한 비교와 밸브 시간 예산은 타당하다. 위 질문의 명시적 요구범위와는 다르다. |
| redundancy_independence_boundary / 1 | 인과관계 | 공용 공기원 상실이 복수 최종요소의 종속 실패를 일으킬 수 있음을 설명했다. 위험감소 평가와 직접 연결된다. |
| redundancy_independence_boundary / 2 | 인과관계 | 공유 환경에 의한 동시 고장과 독립 고장의 모델 분리가 타당하다. |
| incremental_encoder_principle / 3 | 적용범위·조건 | 정전 중 정지와 저장 무결성, 미계측 이동 시 기준 재확립을 올바르게 분리한다. 누적 원리와 A/B/Z 전체 설명으로는 부족하다. |

주 원인 집계는 개념·동의어 6, 수식·수치 5, 비례관계 1, 인과관계 2, 적용범위·조건 6이다. 마지막 6건 중 3건은 평가 기대값과 문항 범위가 어긋난 PST 사례다. 단위 환산, 복수 문장에 필수 조건이 흩어진 경우, 부정·반대 방향이 단독 주 원인인 사례는 없었다.

## 다른 Topic에서 실행한 비교

정본 2,096개 중 기존 Machine Contract의 양성 조건 규칙과 소유 Topic·Anchor ID가 정확히 맞는 것은 54개였다. 이 중 제외 Overlay를 통과한 것은 45개(2.15%)다. 전체 Machine Contract는 16개 Topic, 113개 관계 Fact, 양성 식별 규칙 72개이며 일부 규칙은 Anchor와 다른 ID를 쓴다. 이 수치는 데이터 적용 범위다.

11개 밖의 6개 Anchor에서 30개 합성 자연어와 별도 구조화 주입 12개를 실행했다. 대상은 체적유량, Verification, 보호접지, 직사각형 위어, MC/DC, 요구 RRF다. 실제 계약의 `equivalent_to`, `checks`, `distinct_from`, `proportional_to`, `derived_by_ratio` 등 5개 술어를 공통 진단으로 비교했다. 실험용 Anchor별 구현 코드 추가는 0줄이며, 비교 로직은 6/6에 재사용됐다. 인과, 복합 조건 결합, 임의 단위·수식 해석은 이 재사용률에 포함하지 않는다.

| 유형 | 기존 실제 채점 | 별도 진단 |
|---|---|---|
| 명시적 정상 관계 6 | 6 SATISFIED | 6 관계 일치 |
| 같은 뜻을 다른 말로 표현한 정상·부분 답안 6 | 3 UNRESOLVED, 2 MISSING, 1 WRONG. 인정 0 | 6 인식 불확실 |
| 명시적 반대 주장 6 | 6 WRONG | 6 명시 반대 |
| 단순 용어열 6 | 2 SATISFIED, 4 UNRESOLVED | 6 인식 불확실 |
| 기술 내용 부족 대조 6 | 1 PARTIAL, 5 MISSING | 6 인식 불확실 |
| 계약의 구조화 Claim 주입 12 | 6 정상 SATISFIED, 6 반대 WRONG | 답안 추출을 거치지 않은 비교기 시험 |

오답 인정은 명시적 반대 0/6이었다. 별도의 용어열에서 Verification과 RRF 2건에 기존 채점의 과인정이 관측됐다. 체적유량의 면적분 표기는 평면을 통과하는 법선 속도 성분의 적분을 뜻하는 정상 표현이며 기존 경로는 이 사례를 WRONG으로 분류했다. 확인된 별도 Topic 사례는 이번 PR에서 채점 변경 없이 증거로 기록했다. 30개 자연어를 독립 정확도 표본으로 사용하지 않는다.

## 진단 구현과 다음 범위

[`audit_relation_recognition`](../scripts/audit_relation_recognition.py)은 기존 질문 범위, 제외 Overlay, canonical extraction 및 Machine Contract를 사용한다. 원문 위치가 확인된 완결 한국어 주장에 대해서만 일치나 명시적 반대 상태를 기록한다. 인용, 용어열, 조건 미결, 상충 증거, 관계 데이터 부재는 `RECOGNITION_UNCERTAIN`이다. `CONTENT_INSUFFICIENT`는 공백 답안처럼 부족을 직접 확인할 수 있는 경우로 제한했다. 이 진단은 채점기에 연결되지 않으며 점수 권한은 없다.

구조화된 Claim의 방향·극성·적용 범위 비교와 단위 차원 일치 확인은 재사용할 수 있다. 조건의 적용 대상 연결, 산술로 드러낸 비례식, 의미가 동등한 자연어 표현은 별도의 추출 검증이 필요하다. 특히 quantity evaluator의 차원 일치는 단위 환산이나 수식 동치까지 보증하지 않는다. 45개와 6개 표본의 결과를 전체 배점 경로로 외삽할 수 없다. 현재 지원되지 않는 대표 관계 유형에서 근거와 조건을 먼저 구조화·검증하는 것이 적절하다. 신규 사례 문구의 등록은 중단했다.

입력 고정본 SHA-256은 신규 55건 `a600f88cd1b6524dd00b58415173354c7af1b96f75e7f9e85f79bb8fef3dead9`, 143건 결과 기준선 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`이다. 사례 원문은 이 보고서에 싣지 않았다.
