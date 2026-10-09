# Topic Sheet: 전력전자 변환기와 전동기 구동의 원리 및 적용

## 1. Topic metadata

- `topic_id`: `power_electronics_converters_motor_drive_control`
- `title_ko`: `전력전자 변환기와 전동기 구동의 원리 및 적용`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `FIELD_APPLICATION`
- `selection_importance`: `NORMAL`
- `semantic_execution`: `DETERMINISTIC_PRIMARY_CANDIDATE`
- `deterministic_checks.enabled`: `false`

## 2. Scope and ownership

이 Topic은 전력반도체 스위칭으로 전기에너지의 형태를 변환하고, 변환기를
이용해 교류 전동기의 속도·토크를 제어하는 기본 원리와 산업 적용을 다룬다.
전력변환 단계와 제어목적, 주요 파형·손실·고조파 및 안전한 적용 판단을
서로 연결한다.

### Included

- 전력전자 변환의 기본 분류: AC-DC 정류, DC-DC 변환, DC-AC 인버터,
  AC-AC 위상제어/변환
- 다이오드·SCR·GTO/IGCT·MOSFET·IGBT의 제어성, 도통·차단 및 스위칭 역할
- 단상/3상 정류와 6-pulse 정류의 기본 도통·리플 원리
- SCR 점호각 위상제어, 강제/자연 commutation의 개념과 적용 경계
- Buck/Boost 등 PWM DC-DC 변환의 스위칭 상태, duty ratio와 평균 출력 관계
- 전압원 인버터(VSI)·전류원 인버터(CSI), 2-level leg, 상보 스위칭,
  dead time과 DC-link 개념
- 인버터 PWM의 평균 전압 합성, switching frequency, 파형·손실·고조파 trade-off
- 유도전동기 가변속 구동에서 주파수·전압 제어, V/f의 기본 취지와 운전 한계
- 자속기준/벡터제어의 d-q 기준좌표, 자속·토크 성분 분리, 자속각 추정,
  전류 지령 및 속도·토크 제어의 관계
- 변환기와 전동기 구동의 효율, 역률, 고조파, 열·과전류·과전압,
  EMC/절연, 회생 및 보호·시운전 고려사항

### Excluded and hand-off

- 전동기 권선·전자기 구조와 상세 등가회로/설계, 전자기장 해석:
  전기기기 설계 주제의 소유 범위
- PID, 주파수응답, 상태공간, 최적제어와 일반 제어기 설계:
  해당 process/control-theory Topic의 소유 범위. 이 Topic은 구동기와
  전력변환기 내부 제어의 목적·블록 역할만 설명한다.
- 회전수·각속도·pulse 계측, encoder/tachometer/proximity sensor 선정과
  오차: `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`
- 계장 전원·접지·UPS·ground loop와 일반 EMC 설계:
  `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- 위험장소 인증, 방폭·본질안전 기기 선정:
  `hazardous_area_explosion_protection_intrinsic_safety_equipment_selection`
- 전력계통 보호·차단기 협조, 고압 송배전·계통 안정도와 발전기 설계
- 전력반도체 소자 물리·공정·패키지 신뢰성의 상세 반도체공학
- 변압기·배전반·모터의 제조 및 정비 절차 세부

## 3. Representative questions

1. 전력변환기의 AC-DC, DC-DC, DC-AC 및 AC-AC 변환 원리와 적용을 설명하시오.
2. 다이오드, SCR, IGBT 및 MOSFET의 제어 특성과 전력변환기 내 역할을
   비교하시오.
3. 정류기의 위상제어와 PWM DC-DC 변환의 출력제어 원리 및 파형·손실 특성을
   설명하시오.
4. 전압원 인버터와 전류원 인버터의 차이, PWM의 기능 및 주요 설계 고려사항을
   설명하시오.
5. 유도전동기의 가변속 구동에서 V/f 제어와 자속기준 벡터제어의 목적·원리·
   적용상 차이를 설명하시오.
6. 전력변환기 및 전동기 구동설비의 고조파, 효율, 열, EMC·보호와 시운전
   고려사항을 설명하시오.

## 4. Candidate core facts to verify during human review

- 전력변환기는 전력반도체의 스위칭을 이용해 입력 전력의 형태 또는 크기를
  부하 요구에 맞게 변환·제어한다.
- 기본 converter 분류는 AC-DC 정류기, DC-DC converter, DC-AC inverter,
  AC-AC converter다. 양방향 전력 흐름·회생 여부는 토폴로지와 제어·보호
  설계에 따라 다르므로 converter 이름만으로 단방향이라고 단정하지 않는다.
- 다이오드는 외부 gate 명령으로 turn-on/off 시점을 모두 제어하는 소자가
  아니다. SCR은 gate로 주로 turn-on을 제어하며, turn-off는 전류가 holding
  조건 아래로 떨어지고 소자 회복조건을 만족하도록 commutation해야 한다.
  MOSFET·IGBT 등 완전제어 소자의 실제 switching도 구동·부하·회로 조건과
  switching loss의 영향을 받는다.
- 이상적인 buck converter의 연속전류모드 정상상태에서만 이상소자·무손실 등
  전제하에 \(V_o/V_i=D\)로 단순화할 수 있다. Boost의 이상식 및 discontinuous
  conduction, 부하·기생성분·폐루프 제어는 별도 조건이므로 무조건 일반화하지
  않는다.
- 인버터는 DC-link 입력으로 교류 전압/전류를 합성한다. VSI/CSI 명칭과 출력
  특성, 소자·수동소자 선택은 실제 topology 및 운전조건에 따라 설명한다.
- PWM은 스위칭 상태·시간비로 출력의 평균/기본파 성분을 제어한다. 스위칭
  주파수 상승은 필터 요구·고조파·소음과 스위칭 손실·열·EMI 사이 trade-off를
  만든다. “duty가 높으면 언제나 부하 평균전압이 증가한다”는 문장은 topology와
  정의 없이 일반화하지 않는다.
- 유도전동기의 자속기준 벡터제어는 회전자 자속 기준 d-q 좌표에서 자속 성분과
  토크 성분을 분리 제어하려는 방법이다. 성능은 자속각 추정, 파라미터,
  좌표변환, 전류제어기와 inverter 한계 등에 영향을 받는다.
- V/f 제어는 운전 주파수 변화에 따라 전압을 조정해 자속을 적정하게 유지하려는
  기본 접근이다. 저속 전압강하, field weakening, 부하·구동기 제한과 과도응답을
  고려하며 vector control과 동일한 동특성이라고 단정하지 않는다.
- 전력변환기 적용은 입력/출력 전압·전류, 전력·부하 범위, switching 및
  conduction loss, 열설계, 고조파·역률, 보호, 회생 요구, EMC·절연, 환경 및
  유지관리를 함께 검토한다.
- 장치의 계측제어 경계에서 전력변환기 내부 current/speed loop의 역할은 설명할
  수 있지만, 일반 제어기 설계·안정도 분석 및 실제 회전속도 센서 selection은
  해당 인접 Topic에 넘긴다.

저장 WordPress 문서는 그림의 OCR 및 개인 강의 메모를 포함한다. 아래 자료의
수식·도식·전력방향·손실 설명은 canonical Fact로 확정하기 전 신뢰할 수 있는
기술 자료와 실제 topology 조건으로 검증한다.

## 5. Acceptable answer structure

1. 요구 출력과 변환 방향: AC/DC, 전압·전류·주파수 및 부하/회생 요구를 정의한다.
2. 주회로: 정류/DC link/DC-DC/inverter 단계와 소자 역할을 제시한다.
3. 제어 원리: 점호각 또는 switching state/PWM과 출력 제어 관계를 설명한다.
4. 전동기 구동: 운전 요구에 맞는 V/f 또는 vector control의 자속·토크 제어를
   설명한다.
5. 성능·제약: 효율·손실·열·고조파·EMC·보호·응답을 조건부로 비교한다.
6. 적용 결론: topology와 제어방식을 실제 부하·운전·유지관리 요구로 정당화한다.

## 6. Fatal wrong-claim candidates

사람 검토 전까지 아래 항목은 검토용 후보이며, deterministic fatal로 모두
구현되었다고 간주하지 않는다.

- 정류기는 AC를 DC로, inverter는 DC를 AC로 변환하는 일반적인 역할을 완전히
  서로 바꾸어 설명한다.
- SCR은 gate 신호만으로 임의의 순간에 turn-off할 수 있다고 일반화한다.
- 다이오드는 gate 신호로 turn-on/off를 명령하는 완전제어 소자라고 설명한다.
- topology·운전모드·전도모드 전제 없이 모든 buck/boost에서 같은 duty-output
  식이 성립한다고 주장한다.
- 모든 PWM 변환기에서 duty ratio가 증가하면 부하 평균전압이 반드시 같은
  방향으로 증가한다고 단정한다.
- V/f 제어가 모든 속도범위와 부하조건에서 일정 자속·일정 토크를 보장한다고
  주장한다.
- vector control이 encoder가 반드시 있어야만 가능하거나, 반대로 자속각 추정과
  피드백이 전혀 필요 없다고 보편적으로 단정한다.
- switching frequency 증가는 효율·고조파·EMI를 모두 동시에 개선한다고 주장한다.

## 7. Warn-level and false-positive cautions

- 보조 그림의 OCR로 얻은 \(V_{RM}\), 역회복·commutation 파형 기호는 실제
  기호 정의와 소자/회로 조건을 확인한다.
- single-phase와 three-phase, diode와 phase-controlled rectifier,
  VSI와 CSI, hard/soft switching의 조건을 섞지 않는다.
- 산업용 VFD 제품 기능(회생, sensorless/vector control, 보호·통신)은 제조사와
  제품군별 차이가 있으므로 일반 기능으로 가정하지 않는다.
- 효율·역률·THD 식은 정의와 파형/측정조건을 밝히고, fundamental displacement
  factor와 true power factor를 혼동하지 않는다.
- motor speed control 원리의 설명과 shaft speed 센서의 계측·선정을 혼동하지
  않는다.
- 글 제목, retrieval 순위, OCR 키워드만으로 source fact 또는 WordPress link
  approval을 만들지 않는다.

## 8. Cross-topic handoff

- 회전수·각속도 센서, encoder pulse와 속도계측 오차:
  `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`
- PID/상태공간/주파수응답/제어기 안정도: 해당 control theory Topic
- 전력변환기 설치 시 계장 접지·차폐·UPS·ground loop: 계장 전원·접지 Topic
- 위험장소 인증·방폭: hazardous area Topic

## 9. Local WordPress evidence and quality concerns

- `post_id=7905`, “전력용 반도체”: uncontrolled/semi-controlled/fully-controlled
  분류와 SCR/GTO/IGCT/BJT/MOSFET/IGBT 메모. turn-off, loss와 특정 소자의
  우열은 단순화될 수 있어 소자별 source 검증이 필요하다.
- `post_id=8071`, “유도 전동기 순시 토크 제어 정리”: rotor-flux d-q 정렬,
  자속/토크 전류 분리와 vector control을 다룬다. OCR 수식 첨자·좌표계가
  깨졌을 수 있으므로 원식·전제 검증 전 수식을 고정하지 않는다.
- `post_id=8123`, “인버터 설명”: 2-level inverter leg, DC link, switching
  states와 powering/regeneration을 다룬다. 회생 전력흐름은 회로구성과
  DC-link/전원부 조건을 확인한다.
- `post_id=8399`, “현대전력전자공학 1장”: 전력전자·SCR 개관. 저자 메모와
  OCR 문장을 표준 정의나 역사적 단독 근거로 취급하지 않는다.
- `post_id=8407`, “현대전력전자공학, 2장”: diode reverse recovery와 SCR
  메모가 섞여 있다. 역회복 전압 기호와 회로 인덕턴스 효과는 파형과
  소자 표기법을 대조한다.
- `post_id=8420`, “현대전력전자공학, 4장”: PWM, buck/boost, 정류, switching
  변수 메모. “buck은 전류, boost는 전압” 등 축약 표현은 보편 원리로
  승격하지 않는다.
- `post_id=8426`, “현대전력전자공학, 5장”: AC-AC 위상제어와 SCR/Triac,
  고조파·역률 메모. 부하와 firing angle 조건을 확인한다.
- `post_id=8446`, “현대전력전자공학, 6장”: DC-DC 회로 동작을 대화체로
  풀어쓴 설명으로, topology/전도모드·인덕터 전압 극성·상태구간을 원그림과
  대조한다.
- `post_id=8599`, “현대전력전자공학, 7장”: DC-AC, inverter, VSI/CSI와
  switching 메모. 입력/출력 필터, 전류 경로 및 회생조건 검증이 필요하다.
- `post_id=9040`, “인버터, DC to AC”: 정류기 commutation overlap 내용을
  포함한다. 출력전류가 “두 배”라는 표현은 구간·전류 기준·회로를 확인하기
  전에는 채점 Fact로 쓰지 않는다.
- `post_id=9101`, “유도전동기, 교류 전동기”: AC induction motor 특성과
  motor-control 교재 메모. 모터 상세 이론 중 구동기 설명에 필요한 내용만
  포함하고 일반 전기기기 범위는 분리한다.

## 10. Deterministic ontology grading direction

이 Topic은 flow Topic과 마찬가지로 `grading_ontology`의 canonical concept/
predicate와 `logic_check.json`의 additive `machine_contract`를 통해
deterministic-primary 경로에 연결하는 것을 목표로 한다. 계약은 검증된 converter
방향 등 명확한 관계만 다룬다. provider-free 채점은 LLM 없이 동작할 수 있으나,
이 Topic 단독 추가가 전체 운영의 Authority Gate를 만족시키지는 않는다.
질문 라우팅·정상/오답 표현·fatal 경계·회귀 정확도를 검증하고 전역
DETERMINISTIC_PRIMARY Gate에 포함하기 전까지는 managed draft 상태로 둔다.

## 11. Human review checklist

- 기존 속도계측, 계장 전원/EMC, 일반 제어이론 및 전기기기 Topic의 소유 범위를
  침범하지 않는가?
- 변환기 분류·전력흐름을 topology와 operating mode에 맞춰 설명했는가?
- buck/boost, SCR commutation, vector control 수식과 적용조건을 검증했는가?
- OCR/강의 노트의 잘못된 수식·보편화 주장을 canonical fact로 승격하지 않았는가?
- machine contract가 안전한 canonical claim 관계만 검사하고 일반 문장을
  잘못 fatal로 처리하지 않는가?
- source JSON 네 개와 Topic Sheet의 ID, pattern, anchor reference가 일치하는가?
- 승인 전까지 managed 상태를 `draft / human_review_required`로 유지했는가?
