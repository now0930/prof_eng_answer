# Topic Sheet: 유공압 시스템·유압회로의 원리와 구성요소 선정

## 1. Topic metadata

- `topic_id`: `fluid_power_hydraulic_pneumatic_systems_circuit_principles_selection`
- `title_ko`: `유공압 시스템·유압회로의 원리와 구성요소 선정`
- `question_type`: `PRINCIPLE_INTERPRETATION`
- `difficulty`: `FIELD_APPLICATION`
- `selection_importance`: `NORMAL`
- `semantic_execution`: `DETERMINISTIC_PRIMARY_CANDIDATE`
- `deterministic_checks.enabled`: `false`

## 2. Scope and ownership

이 Topic은 유체를 이용해 동력을 생성·전달·제어하는 산업용 fluid power
시스템의 기본 구성과 회로 원리를 다룬다. 유압과 공압의 working-fluid
차이를 바탕으로 reservoir/air preparation, pump/compressor, valve,
actuator, piping 및 auxiliary components의 기능을 연결하고, 부하·속도·
압력·운전 요구에 맞는 기초 회로와 구성을 설명한다.

### Included

- Fluid power 구성 흐름: 동력원, 유체원, conditioning/storage, control valve,
  actuator, piping 및 return/exhaust
- 유압과 공압의 작동유체·압축성 및 적용 trade-off 비교
- 유압유 점도·밀도·bulk modulus와 온도·누설·마찰·윤활·냉각 영향의 기본 원리
- Pump의 displacement/유량 역할, positive-displacement 계열의 기본 구분,
  pump와 load·system pressure의 관계
- 유압 cylinder·hydraulic motor와 공압 actuator의 선형·회전 출력 원리
- Directional·pressure·flow control valve의 회로상 역할
- Relief/reducing/unloading/sequence/counterbalance 및 check valve의
  기본 회로 기능과 적용조건
- 유압 regenerative circuit, unloading circuit, accumulator 사용 목적과
  에너지·속도·압력 관계
- Accumulator, reservoir, filter/strainer, heat exchanger, seal, air receiver,
  cooler/dryer, FRL 등 auxiliary 장치의 기능
- Electrohydraulic servo/proportional valve의 command-to-flow 기본 원리,
  pilot stage, torque motor/flapper-nozzle/spool 역할 개관
- 압력·유량·속도·힘·동력의 기초 관계와 단위·전제 명시
- 오염·온도·점도·누설·cavitation/aeration·압력충격과 안전한 유지관리의
  기초 고려

### Excluded and hand-off

- 공정 제어밸브(body/trim), pneumatic actuator thrust·fail-safe spring sizing,
  positioner/I/P/booster calibration 및 process valve package selection:
  관련 `control_valve_*` Topic이 소유한다. 본 Topic은 구동원리/회로 수준에서
  유압·공압 작동기를 다룰 뿐 control valve package 선정으로 확장하지 않는다.
- 공정유체 계측기 및 flowmeter/pressure transmitter 원리·선정:
  해당 instrumentation Topic이 소유한다. 회로 해석에 필요한 압력·유량은
  상태량으로만 사용한다.
- 일반 제어이론, PID 설계, 주파수응답·상태공간:
  해당 control-theory Topic이 소유한다.
- 기계요소 설계, 상세 구조응력·피로·실린더 제작/실링 제조 규격,
  정량 배관 압력강하 설계 및 상세 열유체 해석
- 특정 제조사 servo-valve 성능곡선, 응답대역, contamination class 또는
  압력 등급의 보편 수치화

## 3. Representative questions

1. 유압 및 공압 시스템의 구성과 작동 원리를 비교하고 적용 시 장단점을
   설명하시오.
2. 유압 pump, valve 및 actuator의 기능과 압력·유량·힘·속도의 관계를
   설명하시오.
3. 유압의 방향·압력·유량 제어밸브 종류와 회로상 기능을 설명하시오.
4. 유압 regenerative circuit, unloading circuit 및 accumulator의 기능과
   적용조건을 설명하시오.
5. 공기압축기, air receiver, dryer 및 FRL의 기능과 공압 시스템 운전 시
   고려사항을 설명하시오.
6. 전기-유압 서보밸브의 구성과 전기 입력에서 spool/유량 출력까지의 기본
   제어 원리를 설명하시오.
7. 제시된 작동 조건에 적합한 유공압 구성을 선정하고 압력·유량·오염·안전
   고려사항을 설명하시오.

## 4. Candidate core facts to verify during human review

- 유압은 액체를, 공압은 공기 등 기체를 working fluid로 이용한다. 액체도
  탄성·기포·배관 팽창 영향을 받으며 절대적으로 비압축성이라고 표현하지 않는다.
- Pump/compressor는 유량 또는 압축유체 공급을 만들며, 회로 압력은 부하와
  유로·제어 조건에 따라 형성된다. Pump가 언제나 독립적으로 고정 압력을
  생성한다고 단순화하지 않는다.
- 유압 actuator의 힘은 압력과 유효 면적, 선형 속도는 유량과 유효 면적에
  관련된다. 실린더의 cap/rod side 면적이 다르면 양방향 속도와 추력이 다르다.
- 유체 동력은 \(pQ\)이며 SI 단위로 \(p\,[Pa]\), \(Q\,[m^3/s]\)를 쓸 때 W다.
  단위환산, 효율과 압력강하는 실제 입력·출력 동력 계산에서 구분한다.
- Relief valve는 설정 조건에서 압력을 제한하는 보호/제어 경로다. 정상운전 중
  압력제어·열발생과 회로 구성 영향은 valve type에 따라 다르다.
- Pressure reducing valve는 하류 압력을 낮게 조절하며 relief valve와 동일한
  회로 기능이 아니다. Unloading valve는 조건에 따라 pump 유량을 낮은 압력
  경로로 전환한다. Counterbalance valve는 over-running load 제어 및 부하
  유지 목적을 회로 조건에 맞춰 설명한다.
- Accumulator는 압력에너지를 저장·방출하는 장치다. 보조유량, 누설 보상,
  비상 동작 또는 맥동 완화에 쓸 수 있으나 선정·충전·격리·방출은 시스템과
  안전 절차를 따라야 한다.
- Regenerative circuit은 차동 실린더의 rod-side 유량을 cap-side에 합류시켜
  전진 속도를 높일 수 있지만 유효 추력과 압력·유량 관계가 달라진다. 단순히
  어떤 회로에서든 유량이 합쳐진다고 일반화하지 않는다.
- 공압 기체의 압축성은 부하 변화에 따른 탄성·응답에 영향을 준다. 유압이 항상
  정밀하고 공압은 정밀제어가 불가능하다는 이분법 대신 설계·센서·제어와
  부하·속도 조건을 제시한다.
- FRL은 filter/regulator/lubricator의 일반 조합을 가리키지만 모든 공압기기에
  lubricator가 항상 필요하지는 않다. 제조사 요구와 downstream 기기를 확인한다.
- Air dryer는 압축공기 수분·이슬점 요구를 관리하며, receiver·cooler·배수와
  함께 시스템 품질을 결정한다. 압력과 온도 등급은 제품 및 설계 기준을 확인한다.
- Electrohydraulic servo valve는 전기 명령을 pilot/main stage의 유압 유량
  제어로 바꾼다. torque motor/flapper-nozzle/spool은 일반 구성 예이며 모든
  servo/proportional valve가 같은 구조는 아니다.
- 고속 유체 흐름, 급격한 valve 조작, 오염과 부적절한 흡입조건은 압력충격,
  cavitation/aeration, 마모와 응답저하를 유발할 수 있다. 현장 원인과 대응은
  회로·유체·제조사 조건으로 설명한다.

저장 글의 필기 OCR, 교재 요약 및 축약된 회로 설명은 출처 문맥이 제한적이다.
압력 한계, Reynolds 경계, 점도 등급, air composition, 고정 Cv/Q 식,
valve 성능 비교 및 servo 내부구조를 제품·조건 불문 canonical fact로 만들지
않는다.

## 5. Acceptable answer structure

1. 요구 동작·부하·속도·압력과 working fluid를 정의한다.
2. 동력원에서 conditioning, control valve, actuator 및 return/exhaust까지
   에너지/유체 흐름을 그린다.
3. 회로의 pressure·direction·flow 제어와 각 component의 역할을 설명한다.
4. 필요한 경우 actuator 관계식·유압 동력·회로 구성을 전제 및 단위와 함께 쓴다.
5. 유압/공압 또는 대안 회로를 응답·힘·속도·누설·효율·오염·유지관리로 비교한다.
6. 안전한 압력해제·저장에너지·배기·누유 및 commissioning 점검을 제시한다.

## 6. Fatal wrong-claim candidates

사람 검토 전까지 아래 항목은 검토용 후보이며, deterministic fatal 구현을
의미하지 않는다.

- 유압 시스템의 일반 작동유체를 압축공기라고 하거나, 공압 시스템이 액체 유압유를
  작동유체로 쓴다고 서로 바꾸어 설명한다.
- Pump가 회로 부하와 무관하게 압력을 단독으로 결정하며 항상 일정 압력을
  직접 공급한다고 설명한다.
- Relief valve가 하류 압력을 낮추고 조절하는 pressure reducing valve와 항상
  같은 기능이라고 설명한다.
- 유압 actuator의 출력이 유량만으로 힘을 결정한다고 하거나 \(pQ\)를 힘으로
  제시한다.
- Accumulator의 저장 에너지를 격리·방출 안전절차 없이 분해·정비해도 된다고
  설명한다.
- 모든 regenerative circuit에서 속도와 추력이 동시에 증가한다고 단정한다.
- 모든 공압 시스템이 항상 정밀제어 불가능하거나 모든 유압 시스템이 정밀제어를
  보장한다고 일반화한다.
- 모든 공압 actuator에서 lubricator를 반드시 사용해야 한다고 설명한다.

## 7. Warn-level and false-positive cautions

- 공압·유압의 비교는 시스템 압력·출력밀도·응답·부하 강성·누설 관리·환경,
  압축성 및 제어구조를 함께 다룬다. 단순 “저압/고압” 구분이나 source의
  특정 psi 숫자를 규격처럼 채점하지 않는다.
- \(pV/T=constant\), polytropic relation, viscosity 및 bulk-modulus 식은
  절대압/온도·정의·과정·단위와 가정을 구분한다. source OCR의 기호 오류를
  canonical 식으로 복사하지 않는다.
- 난류·층류 Reynolds 기준은 유로 형상·경계·운전 상태 의존성이 있으므로
  원형관 경계값을 유공압 모든 회로에 보편 적용하지 않는다.
- \(Q\propto\sqrt{\Delta p}\) 같은 orifice 관계는 유체·유동상태·계수 전제를
  명시한다. 점도·보정·압축성 영향이 있는 경우 고정 식만으로 완전 결정된다고
  하지 않는다.
- 7632 서보밸브 글에는 유압 방향/압력/유량 제어와 제어밸브 명칭이 함께 있다.
  유압 servo valve는 본 Topic에서 electrohydraulic stage 원리만 다루고
  공정 제어밸브 body/actuator/positioner 선정·교정은 해당 valve Topic으로
  인계한다.
- symbols-only post `7636`과 빈 post `7922`는 source evidence가 없으므로
  채점 anchor를 만들지 않는다. `7917`은 문제 요구만 제공하며 답변 근거가 아니다.

## 8. Cross-topic handoff

- 공정용 control valve의 본체·actuator 유형과 선정:
  `control_valve_types_globe_rotary_body_actuator_selection`
- sliding-stem valve actuator 힘·마찰·fail-safe sizing:
  `control_valve_fluid_forces_unbalance_friction_actuator_sizing_fail_safe`
- positioner, I/P, pneumatic booster, calibration:
  `control_valve_positioner_ip_converter_booster_accessories_calibration`
- process control valve sizing, characteristics, cavitation, trim, leakage,
  diagnostics, lifecycle and SIS final element: corresponding `control_valve_*`
  specialist Topic
- pressure/flow instrument measurement and selection: relevant instrumentation
  Topic Packs
- general PID and dynamic control theory: relevant control-theory Topic Packs

## 9. Local WordPress evidence and quality concerns

- `post_id=7567`, “유공압시스템 강의 정리” (8,475 chars): multi-lecture
  overview across fluid properties, piping, hydraulic power, pump, actuator,
  valves and circuits. OCR/notes include possible formula and symbol uncertainty;
  strongest broad-coverage source, but details require fact-by-fact review.
- `post_id=7621`, “공압 시스템” (5,385 chars): pneumatic/hydraulic comparison,
  ideal-gas examples, compressor, FRL, dryer, receiver and valves. Specific
  pressure figures and simplified comparisons are source-specific, not universal.
- `post_id=7626`, “보조 유압장치” (5,824 chars): reservoir, accumulators,
  intensifier, seals, filters/strainers, heat exchanger and contamination control.
  Accumulator application diagrams require circuit-specific verification.
- `post_id=7632`, “서보 밸브” (6,449 chars): directional/pressure/flow valve
  concepts and electrohydraulic servo valve details. Separate servo principles
  from process control valve ownership and verify spool/port descriptions.
- `post_id=7636`, “유공압기호” (0 chars): no stored article text; exclude as
  factual evidence pending source recovery.
- `post_id=7641`, “유압 회로” (6,866 chars): regenerative/unloading/accumulator
  circuits and pressure/direction/flow control. Check circuit porting and
  cylinder area assumptions before asserting speed, force or flow sums.
- `post_id=7917`, “133회 2교시 4번” (74 chars): authentic prompt asks about
  hydraulic-fluid characteristics, pressure generation/use and five advantages/
  disadvantages; useful as question evidence only.
- `post_id=7922`, “133회 2교시 2번” (0 chars): empty source; do not infer question
  or answer content.

The eight-post cluster is only partially substantive: 7567, 7621, 7626, 7632 and
7641 provide main coverage; 7917 contributes question wording; 7636 and 7922
need source recovery. This supports a managed draft candidate, not claims of
fully covered exam scope or blog-link approval.

## 10. Deterministic ontology grading direction

The managed draft can add a small machine contract for the working-fluid
distinction (hydraulic system -> liquid; pneumatic system -> gas). It must be
additive and downstream deterministic only; do not encode the many conditional
equations, valve functions, or unverified OCR claims as machine facts. The
provider-free regression must include normal and reversed relations and verify
exclusive topic routing against valve-actuator and instrumentation topics.
Neither a Topic-local contract nor a passing regression means whole-service
DETERMINISTIC_PRIMARY Authority Gate approval.

## 11. Human review checklist

- Is the Topic focused on generic industrial fluid power systems/circuits rather
  than duplicating process control-valve packs?
- Are pressure, flow, force, speed and power equations dimensionally correct and
  qualified by operating condition?
- Are pneumatic/hydraulic comparisons free of universal pressure figures and
  unsupported categorical claims?
- Are accumulator, regenerative, unloading and servo-valve descriptions checked
  against diagrams and correct topology?
- Are blank/symbol-only source posts excluded from factual anchors?
- Does provider-free routing select this Topic for representative fluid-power
  questions and hand off explicit process-valve sizing/positioner topics?
- Do ontology facts remain limited to reviewed relations with safe mutation cases?
- Do README, Topic Sheet, anchors, requirements and route question IDs agree?
- Is managed state still `draft / human_review_required` until human approval?
