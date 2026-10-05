# 유량·유속 계측의 원리, 유량계 종류 및 선정

- Topic ID: `flow_measurement_meter_principles_velocity_selection`
- Question type: `PRINCIPLE_INTERPRETATION`
- Difficulty: `FIELD_APPLICATION`
- Selection importance: `NORMAL`
- Semantic execution: `DETERMINISTIC_PRIMARY_CANDIDATE`
- Regex deterministic checks: disabled
- Ontology machine contract: enabled
- Workflow state: see `topic_status.json`. Human approval is recorded; repository-wide integration and commit gates remain separate.

Deterministic-primary 경로에서는 전역 engineering ontology와 아래
`machine_contract`가 canonical claim evidence를 평가하며 LLM을 호출하지
않는다. 실제 운영 적용은 전역 `DETERMINISTIC_GRADING_PRIMARY` flag와
Authority Gate가 `READY`인 경우에만 가능하다. 기존 `llm_profile`은
legacy/보조 경로 호환용이며 deterministic 점수·verdict를 만들지 않는다.

## Ownership

밀폐 배관의 국소·평균 유속, 체적유량·질량유량 환산, 유량계의 측정원리
비교와 계기 선정을 다룬다. 유량계 원리를 유체 조건과 설치·성능 요인에
연결하여 설명하는 답안을 평가한다.

이 Topic은 유량 측정 primary element와 유량-신호 변환 원리를 소유한다.
차압 transmitter 자체의 압력센싱·범위·교정·impulse line은 압력계측
Topic으로, 차압식 레벨은 DP 레벨 Topic으로 넘긴다. 배관 유량을 재는
초음파 방식은 이 Topic의 범위이며, 거리·레벨 초음파의 펄스 에코 원리와
에코 진단은 초음파 거리·레벨 Topic의 범위다. 제어밸브 Cv/Kv sizing은
유량계측과 별개다. 상세 경계와 hand-off 목록은
`docs/topic_sheets/flow_measurement_meter_principles_velocity_selection.md`를
참조한다.

## Core contract

1. 체적유량은 단면에 수직인 유속 성분의 면적 적분이며,
   \(Q=\int_A v_n\,dA=A\bar v\)는 단면 평균유속으로 표현한 관계다.
2. 질량유량은 \(\dot m=\int_A \rho v_n\,dA\)이며, 밀도가 균일할 때
   \(\dot m=\rho Q\)로 단순화된다. 체적유량과 질량유량은 구분한다.
3. 차압식(오리피스·노즐·벤투리 등), 피토관, 가변면적식(rotameter),
   용적식(positive displacement), 터빈, 와류, 전자기, 초음파,
   코리올리스 및 열식 계기의 물리 입력과 측정 대상을 구분한다.
   가변면적식은 유량에 따른 float 평형위치와 유효 유로면적을 이용하고,
   용적식은 반복 포획·이송되는 체적을 센다.
4. 차압과 유량의 제곱근 관계는 primary-element 형상·beta ratio,
   discharge coefficient, 유체 물성·유동과 보정조건을 전제로 설명한다.
   기체 유량에서는 압축성에 따른 팽창 보정 등 적용 기준을 확인하며,
   이를 무조건적인 보편식으로 취급하지 않는다.
5. 유량계 선정은 측정 대상, 유체상·물성·청정도, 유량범위, 정확도,
   압력손실, 배관·설치, 출력, 교정 및 유지보수 요구를 함께 비교한다.
6. 유동 profile, swirl, 배관 교란, 기포·고형물, 점도·밀도 변화,
   펄세이션, 오염·마모, 영점과 교정이 성능에 미치는 영향을 고려한다.
7. 현장 적용 시 유량계 본체와 별도로 압력 transmitter, 제어밸브,
   압력·레벨 계측 또는 거리·레벨 초음파의 소유 범위를 혼동하지 않는다.

## Grading direction

고득점 답안은 유량·유속 정의에서 출발해 측정 원리와 실제 선택 근거를
연결한다. 단일 지점 속도와 단면 평균속도, 체적과 질량 유량을 구별하고,
각 방식이 무엇을 감지해 어떤 조건으로 유량을 산출하는지 설명한다. 정확도
명목값만 비교하지 않고 공정 유체, 운전범위, 배관·설치, 압력손실과
수명주기 요구를 결론에 반영한다.

특정 기종의 교정식·보정계수·성능값은 계기 형식, 표준, 공정 조건과
제조사 사양에 종속된다. 별도 근거 없이 보편값으로 일반화하지 않는다.
primary element별 beta ratio, discharge coefficient, 압축성 보정은 적용
규격과 실제 계기 형상·운전조건에 맞춰 검증한다.
피토관의 \(v=\sqrt{2\Delta p/\rho}\)는 비압축성·저속 등 적용조건에서
국소속도를 나타내는 관계로만 사용하고, 배관 평균유속으로 바로 간주하지 않는다.

## Local evidence and review limits

- WordPress `post_id=6428` (“와류 유량계”)는 저장 본문이 매우 짧아 와류
  유량계의 상세 설명에 대한 독립 근거로 충분하지 않다.
- `post_id=6497` (“유속 측정”)에는 초음파 transit-time/Doppler와
  \(Q=A\bar v\) 관련 메모가 있으나, 전달시간 역수의 용어 혼동과 물성
  영향의 과도한 일반화 가능성을 재검증해야 한다.
- `post_id=7317` (“베르누이 방정식 유도”)는 일반 유체역학 보조 근거이며,
  유량계 원리나 primary element 설명을 단독으로 뒷받침하지 않는다.
- `post_id=7886` (“유량 측정 센서”)에는 유량 정의와 여러 센서 방식이
  함께 정리되어 있으나, 무관한 감쇠 내용 및 단순화·불완전한 식이 섞여
  있어 claim별 검증이 필요하다.

따라서 이 Pack의 source JSON은 사람이 검토한 채점 기준이다. 블로그 메모만으로
수치·보정식·규격 요구를 확정하지 않았다. 승인 여부와 source hash는
`topic_status.json`이 정본이며, repository-wide integration gate 및 runtime
Authority Gate와는 별도로 관리한다.

## Files

- `fact_anchor.json`: 기본 정의, 계측 원리, 적용 및 선정 기준
- `model_answer.json`: 대표 문제 유형, 답안 구조와 라우팅
- `logic_check.json`: ontology `machine_contract`와 legacy/보조 LLM profile
- `topic_importance.json`: 난이도와 고득점 조건
- `topic_status.json`: 관리 workflow 상태 및 source hash
