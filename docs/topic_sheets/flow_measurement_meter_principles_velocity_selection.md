# Topic Sheet: 유량·유속 계측의 원리, 유량계 종류 및 선정

## 1. Topic metadata

- `topic_id`: `flow_measurement_meter_principles_velocity_selection`
- `title_ko`: `유량·유속 계측의 원리, 유량계 종류 및 선정`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `FIELD_APPLICATION`
- `selection_importance`: `NORMAL`
- `semantic_execution`: `DETERMINISTIC_PRIMARY_CANDIDATE`
- `deterministic_checks.enabled`: `false`

## 2. Scope and ownership

### Included

이 Topic은 밀폐 배관에서 체적유량·질량유량·유속을 계측하는 원리와
유량계의 비교·선정을 다룬다.

- 단면 유속분포와 단면 평균유속의 차이
- \(Q=\int_A v_n\,dA=A\bar v\) 관계와 질량유량의 밀도 관계
- 차압식 primary element(오리피스, 노즐, 벤투리 등), 피토관, 가변면적식
  (rotameter), 용적식 positive-displacement meter의 계측 원리 비교
- 터빈·와류·전자기·초음파 transit-time/Doppler·코리올리스·열식 유량계의
  측정원리와 주요 적용 경계
- 유체 상태·전도도·청정도·유량범위·압력손실·설치조건·정확도 요구에 따른
  계기 선택
- 유속분포·배관 교란·기포/고형물·온도/밀도/점도·펄세이션·오염·마모 및
  영점/교정 관련 오차의 진단 관점
- 실제 유체 조건과 출력량(체적·질량, 순간·적산)을 측정 요구에 맞게 정하는
  절차

### Excluded and hand-off

- 압력 기준, 압력센싱 소자, DP transmitter range/static-pressure effect,
  transmitter calibration 및 impulse line 상세:
  `pressure_measurement_sensor_bourdon_diaphragm_piezoresistive_dp_selection_error`
- 차압식 레벨, 밀도보상, wet/dry leg와 level remote seal:
  `differential_pressure_level_measurement_density_compensation_wet_leg_dry_leg_remote_seal_error`
- 비행시간 거리·레벨 측정, 초음파 에코·음속보상 일반:
  `ultrasonic_sensor_time_of_flight_distance_level_temperature_compensation_reflection_error`
- 제어밸브 Cv/Kv, 밸브 sizing 및 설치 유량특성:
  `control_valve_sizing_cv_kv_reynolds_liquid_selection`,
  `control_valve_gas_sizing_choked_flow_critical_pressure_ratio`,
  `control_valve_characteristics_inherent_installed_equal_percentage_linear_quick_opening`
- 공정 제어루프 설계, 펌프/배관망 유압설계와 CFD 상세
- 개수로 유량, 수문/웨어 계측, 의료·수중 음향 및 비파괴검사

초음파 원리가 겹쳐 보여도 이 Topic은 **배관 유속·유량 측정**을 소유한다.
기존 초음파 Topic은 거리·레벨 측정 원리와 에코 품질을 소유한다. DP flow
primary element의 유량-차압 변환은 이 Topic의 적용 범위이며, pressure
transmitter 자체의 측정 특성과 설치·교정은 압력 Topic으로 넘긴다.

## 3. Representative questions

1. 유속분포와 단면 평균유속의 관계를 설명하고, 체적유량 및 질량유량으로
   환산하는 방법을 설명하시오.
2. 차압식, 가변면적식, 용적식, 터빈식, 와류식, 전자기식, 초음파식 및
   코리올리스 유량계의 원리와 적용상 차이를 비교하시오.
3. 유량계 선정 시 유체 물성, 유량범위, 압력손실, 설치조건, 출력량과
   유지보수 요구를 검토하는 절차를 설명하시오.
4. 초음파 transit-time 방식과 Doppler 방식의 측정원리 및 적용 한계를
   구분하시오.
5. 차압식 유량계에서 유량과 차압의 관계가 성립하는 전제와 대표 오차를
   설명하시오.

## 4. Candidate core facts to verify during human review

- 체적유량은 측정 단면에 수직인 국소 유속 성분의 면적 적분으로 정의되며,
  평균유속을 쓰면 \(Q=A\bar v\)로 나타낼 수 있다.
- 질량유량은 밀도와 체적유량의 관계를 사용한다. 밀도가 변하면 체적유량과
  질량유량을 동일한 수치 또는 동일한 계측량으로 취급할 수 없다.
- 차압식 primary element의 유량 환산은 유동상태, 형상, 밀도·압축성 및
  적용 표준이 정한 보정조건에 종속된다. primary-element 종류·beta ratio,
  discharge coefficient와 기체 팽창 보정 등 계기 구성과 유체 상태에 따른
  환산을 고려한다. 단순 \(Q\propto\sqrt{\Delta P}\) 관계를 모든 유체·
  유량범위에 무조건 적용하지 않는다.
- 피토관은 정압과 전압(정체압)의 차이를 이용해 국소 유속을 추정한다.
  비압축성·저속 등 적용 전제에서 \(v=\sqrt{2\Delta p/\rho}\)로 나타낼 수
  있다. 단일 지점 유속을 배관 전체 평균유속으로 간주하려면 별도의
  profile/traverse 전제가 필요하다.
- 오리피스, 노즐, 벤투리 등 차압 primary element는 형상, beta ratio,
  방출계수, 압축성 보정과 설치조건이 다르므로 해당 계기·적용 표준의
  산정방법을 확인한다. 압력손실과 성능은 형식별 조건으로 비교한다.
- 터빈 유량계는 유동에 의해 회전하는 rotor의 회전응답을 이용한다.
  유체 점도, 유동 profile, bearing/rotor condition 및 설치조건이 성능에
  영향을 줄 수 있다.
- 와류 유량계는 bluff body 후류의 vortex shedding과 유속 사이의 관계를
  이용한다. 적용 가능한 Reynolds 범위, 형상, 진동과 신호 검출조건을
  확인하며 모든 유체·저유량에 동일한 성능을 가정하지 않는다.
- 전자기 유량계는 도전성 유체에서 유동에 의한 유도전압을 이용한다.
  유체 전도도, 전극 접촉, 접지/라이닝 조건과 완전 충만 여부가 적용에
  중요하다. 비전도성 유체에 일반적으로 적용할 수 있다고 서술하지 않는다.
- 초음파 transit-time은 흐름 방향과 역방향의 전파시간 차이를 이용하고,
  Doppler는 유체 내 반사체에서 발생한 주파수 이동을 이용한다. 두 방식의
  반사체 요구와 유체 적합성을 혼동하지 않는다.
- 코리올리스 유량계는 진동 튜브를 통과하는 질량유량에 따른 운동학적
  응답을 측정해 질량유량을 산출한다. 측정기 구조·설치 및 유체 조건을
  고려하고, 모든 코리올리스 계기가 같은 출력/불확도를 가진다고 단정하지
  않는다.
- 열식 유량계는 열전달과 유동에 따른 냉각/온도 응답을 이용한다. 가스
  조성·열물성·교정 조건 변화가 환산에 영향을 줄 수 있다.
- 가변면적식 유량계는 유량에 따라 float와 유체력 평형 위치가 변하고,
  float 위치에서의 유효 유로 면적 변화로 유량을 표시한다. 설치방향과
  유체 물성·기종의 교정조건을 확인한다.
- 용적식 유량계는 측정실에 포획·이송되는 일정 체적의 반복 횟수 또는
  회전/행정 응답으로 유량을 산출한다. 점도, 누설, 마모 및 기포 등 실제
  구조·운전조건에 따른 영향을 검토한다.
- 유량계 선정에는 필요한 유량 범위, 측정 대상(체적/질량), 유체 상과
  물성, 요구 정확도/응답, 허용 압력손실, 배관·전원·출력 인터페이스,
  교정 및 유지보수 조건을 함께 고려한다.

위 사실은 신규 Topic의 검토 초안이다. 현재 WordPress 문서는 학습 메모이며
오류·OCR artifact가 있을 수 있다. Fact Anchor로 확정하기 전 source JSON과
적용조건을 사람이 검증한다.

## 5. Acceptable answer structure

1. 측정 대상과 단위: 유속, 체적유량, 질량유량 및 순간/적산을 정의한다.
2. 기본 환산: 단면 평균유속과 면적 또는 질량보존 관계를 적용한다.
3. 원리 분류: 각 유량계의 입력 물리량과 변환 신호를 설명한다.
4. 적용성 비교: 유체 특성, 운전범위, 압력손실, 설치조건과 유지관리를
   기준으로 적합성을 비교한다.
5. 오차·검증: profile, 설치, 물성, fouling, 신호/교정 요인을 확인한다.
6. 결론: 공정 요구와 계기 성능·수명주기의 절충을 제시한다.

## 6. Fatal wrong-claim candidates

아래는 기술근거로 검토해야 할 fatal 후보다. 현재 Topic machine contract는
체적유량/질량유량 혼동과 전자기 유량계의 비전도성 유체 적용 주장을 결정론적
fatal로 검사한다. 나머지 항목은 검토 기준 후보일 뿐 deterministic fatal로
모두 구현된 것은 아니며, provider-free 경로에서 자동 차단된다고 간주하지 않는다.

- 체적유량 \(Q\)와 질량유량 \(\dot m\)을 밀도 변화와 무관하게 같은 물리량으로
  취급한다.
- 단일 지점의 국소 유속은 항상 배관 단면 평균유속과 같다고 단정한다.
- 차압식 유량의 제곱근 관계에 유체·유동·기하·보정의 적용경계가 없다고
  주장한다.
- 전자기 유량계를 비전도성 유체에도 일반적으로 사용할 수 있다고 주장한다.
- Doppler 초음파 방식에 반사체가 필요 없다고 하거나 transit-time 방식과
  같은 원리라고 설명한다.
- 초음파 거리측정의 \(d=ct/2\)를 배관 유량의 직접 계산식으로 사용한다.
- 제어밸브의 Cv/Kv를 일반 유량계의 직접 측정 원리 또는 유량센서로 혼동한다.
- 가변면적식과 용적식의 측정원리를 서로 바꾸어 설명하거나,
  가변면적식의 float 위치와 유로면적 관계를 무시한다.
- 배관 직관부·유동 교란·설치조건이 모든 유량계에서 무관하다고 단정한다.

## 7. Warn-level and false-positive cautions

- 시험 문제에서 “유속”을 물으면 센서가 측정하는 국소/평균 유속과 적산·체적
  환산 단계를 구분한다.
- 차압 유량, 초음파 유량, 열식 유량의 특정 보정식을 조건 없이 일반화하지
  않는다.
- 센서 카탈로그의 최대 정확도만으로 설치된 계기의 total performance를
  단정하지 않는다.
- 하나의 게시글에 여러 유량계 이름이 열거되어도 각 원리를 모두 설명한
  것으로 인정하지 않는다.
- 게시글 제목, OCR, retrieval 점수만으로 source fact 또는 link approval을
  만들지 않는다.

## 8. Cross-topic handoff

- 압력 센서/DP transmitter 원리와 설치·교정: 압력계측 Topic
- 초음파 거리·레벨 및 에코 처리: 초음파 거리·레벨 Topic
- 제어밸브의 Cv/Kv 산정: 액체/가스 제어밸브 sizing Topic
- flow control loop의 제어기·cascade/ratio 구조: process-control Topic
- 온도센서·열물성 계측 일반: 해당 온도/센서 Topic

## 9. Local WordPress evidence and known quality concerns

- `post_id=6428`, “와류 유량계”: 제목과 시험문제 표현은 구체적이나 저장
  본문은 187자로 짧다. 첨부 원문/OCR을 확인하기 전까지 vortex 관련 세부
  Fact의 단독 근거로 쓰지 않는다.
- `post_id=6497`, “유속 측정”: 초음파 transit-time/Doppler 구성과 \(Q=A\bar v\)
  환산을 다룬다. 저장 내용에는 전달시간 역수와 주파수 표현을 혼동하는 전개,
  물성 영향에 대한 과도한 일반화 가능성이 있어 재검증이 필요하다.
- `post_id=7317`, “베르누이 방정식 유도”: 압력·속도·위치에너지 관계를
  유도하지만 유량계의 독립적 원리 설명은 아니다. 유량계 적용의 전제와
  primary element를 추가 설명할 때만 제한적으로 참고한다.
- `post_id=7886`, “유량 측정 센서”: \(Q=\int_A v_n\,dA\), 평균유속 환산과
  차압·열전달·초음파·전자기·코리올리스 등 측정방식 메모가 있다. 같은 자료에
  별개 2차 시스템 감쇠 내용과 단순화된/불완전한 식이 섞여 있어 claim별
  검증이 필요하다.

## 11. LLM review resolution

별도 LLM 검토에서 가변면적식·용적식의 범위는 있으나 명시적 Fact Anchor와
답안 구조가 빠진 점, 차압식 환산에서 primary-element 형상·beta ratio·
계수·기체 보정 검토가 충분히 구체적이지 않은 점을 확인했다. Topic Sheet와
README, Fact Anchor, model answer 및 LLM logic profile에 해당 내용을 보강했다.
추가 자체 검토에서는 차압 primary element의 대표 형식(오리피스·노즐·벤투리)을
명시하고, 피토관 속도압 식의 밀도·비압축성·저속 전제를 기록하여 국소속도와
단면 평균속도를 혼동하지 않도록 보강했다. 결정론 검사를 새로 활성화하지
않았으며, technical facts의 최종 승인은 사람 검토 단계에 남긴다.

## 12. Deterministic ontology execution boundary

이 Topic은 전역 `grading_ontology` canonical concept/predicate와
`logic_check.json`의 `machine_contract`를 사용해 deterministic-primary 평가
경로의 후보로 연결한다. `scripts/test_flow_measurement_ontology_contract.py`는
질문 라우팅, canonical claim 추출, 제한된 Topic 요구사항 및 2개 fatal을
provider-free로 테스트한다. 이는 모든 유량계 오개념의 완전한 deterministic
coverage를 입증하지 않는다. 실제 운영에서 기본 채점기로 쓰려면 이 Topic의
회귀·정확도 자료를 전역 calibration/Authority Gate에 추가하고, 전역
`DETERMINISTIC_GRADING_PRIMARY` feature flag와 전체 Gate가 `READY`여야 한다.
이 Topic source만 추가했다고 시스템 전체 운영 경로가 자동 전환되는 것은
아니다. LLM profile은 legacy/보조 경로 호환을 위해 유지하며,
deterministic-primary의 score/verdict 권한에는 관여하지 않는다.

## 10. Human review checklist

- Topic 범위가 기존 압력, 차압 레벨, 초음파 거리·레벨, 제어밸브 sizing
  Topic과 충돌하지 않는가?
- 유량계별 측정원리와 적용조건을 신뢰할 수 있는 기술 근거로 재검증했는가?
- 현 WordPress 원문의 오류·OCR artifact를 그대로 canonical Fact로 승격하지
  않았는가?
- Question pattern이 실제 유량·유속 계측 요구에 한정되어 있는가?
- README와 네 source JSON의 Topic ID·question type·ownership이 일치하는가?
- false-positive 및 adjacent-topic handoff가 충분한가?
- managed 상태가 `draft / human_review_required`이며, 승인 명령을 실행하지
  않았는가?
