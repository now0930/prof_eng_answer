# PR #19 — EMC 미연결 오류 규칙 6건 개별 심사

- 기준 브랜치: `codex/pr19-ready-20261108`
- 기준 커밋: `3b8833ec62ec03b33f3d0274a953e3fa11c6fe3e`
- 범위: `instrumentation_power_grounding_shielding_ups_ground_loop_emc`
- 상태: **검증 후보 / scoring HOLD 유지**
- 변경 성격: **기존 9개 오류 정의 중 미연결 6개의 실행 분류를 명시적으로 결정**. 신규 Fact Anchor 승인, 합격선 변경 및 Golden 재채점이 아니다.

## 1. 개별 판정

| 기존 rule_id | 실행 invariant | 이전 source severity | 이번 실행 분류 | 기술적 판단 |
|---|---|---|---|---|
| `ipgse_single_point_always_best` | `EMC_SINGLE_POINT_UNIVERSAL` | fatal | **major** | 단일점 접지의 보편적 우월성은 주파수, 장치, 등전위 본딩 조건을 누락한 과도한 일반화다. 범용 기술사 채점에서는 중요 사실 오류이나 이 단정만으로 인명안전 위험을 확정하지 않는다. |
| `ipgse_shield_replaces_pe` | `EMC_SHIELD_REPLACES_PE` | fatal | **fatal** | 일반 신호용 차폐층을 검증된 보호도체 없이 PE 대신 사용하겠다는 무조건적 주장은 전기안전을 저해할 수 있다. 단, 규격에 맞춰 보호도체로 설계·검증된 금속 차폐 도체는 별개다. |
| `ipgse_redundancy_no_common_cause` | `EMC_REDUNDANCY_IGNORES_CCF` | fatal | **major** | 두 전원의 병렬 연결만으로 공통고장점이 제거되지는 않는다. 분리 모듈·공통 입력·보호·출력분배 검토가 필요하다. |
| `ipgse_ground_loop_only_resistance` | `EMC_GROUND_LOOP_RESISTANCE_ONLY` | fatal | **major** | 다중 접지 귀로/전위차 및 공통 임피던스 등을 무시하고 도체 저항만으로 항상 해결된다고 단정한다. |
| `ipgse_emc_single_countermeasure` | `EMC_SINGLE_COUNTERMEASURE_UNIVERSAL` | fatal | **major** | 하나의 필터·접지 변경으로 모든 EMC 문제를 해결한다고 단정하는 것은 소스·전달경로·피해기기 구분을 생략한 오류다. |
| `ipgse_rewire_without_evidence` | `EMC_REWIRE_BEFORE_EVIDENCE` | fatal | **major** | 측정 또는 원인확인 없이 재결선을 보편적 표준 절차로 제시하는 것은 공학적 진단·검증 절차 오류다. 별도 절연·안전 조치를 무시하라는 주장일 때만 추가 안전 검토가 필요하다. |

**Severity는 산업표준에서 일률적으로 정의한 등급이 아니라 현 프로젝트의 기술사 채점 정책 판정이다.** 기존 `fatal_wrong_claims` 키는 과거 포맷의 이름으로 유지하지만 위 5개 항목의 실제 `severity`를 `major`로 변경한다. 동일 5건은 `llm_profile.fatal_conditions`에서 제외한다. 나머지 기존 3건 및 신규 1건의 `fatal`은 유지한다. `machine_contract.invariant_bindings`와 source severity의 일치 여부를 정식 회귀로 확인한다.

## 2. 근거 범위

실제 공식 원문 전체를 직접 대조한 표준 적합성 증명서가 아니며, 제조사 기술문서로 **공학적 방향성을 대조**하였다.

- Schneider Electric, *Grounding and Electromagnetic Compatibility of PLC Systems* (manual 33002439K01000): 접지·EMC 설계 및 적용조건. https://www.se.com/in/en/download/document/33002439K01000/
- Rockwell Automation, *System Design for Control of Electrical Noise*, GMC-RM001A-EN-P: 결합경로, 배선 분리, 차폐, 보호접지와 EMC 설계 구분. https://literature.rockwellautomation.com/idc/groups/literature/documents/rm/gmc-rm001_-en-p.pdf
- NI, *Field Wiring and Noise Considerations for Analog Signals*: 도전·용량·유도·복사 결합, 접지 루프, 단일 해법 부재. https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html
- Schneider Electric, *Why consider power supply redundancy?*: 병렬 직결 시 한 전원 출력단의 단락이 전체 출력을 잃게 하는 문제 및 분리 모듈 요구. https://www.se.com/uk/en/faqs/FA22823/
- Siemens, *EMC in Practice*, Reference Manual: 케이블 차폐, 저임피던스 본딩, 양단 접지 시 전위차·등전위 본딩 고려. https://cache.industry.siemens.com/dl/files/796/109739796/att_889889/v1/practice_of_emc_directive_2014_30_EU_en-US.pdf

주의: 전용 보호도체로 설계된 케이블 스크린/금속 차폐층의 적합성은 재질·단면적·고장전류·연속성 등 적용 규격 확인이 필요하다. 정규표현식으로 적합성 승인을 추론하지 않는다.

## 3. 실행 정책·경계

1. 전역 invariant 규칙은 변경하지 않는다. 새 6종은 기존 EMC Topic의 `owner_topic_id`가 활성화된 경우에만 판단한다.
2. 각 규칙은 제한된 **직접 단정 패턴**에만 적용한다. 표현이 모호하거나 인용·반박·조건부 설치인 경우 자동 오류를 확정하지 않는다.
3. 이전 `EMC_UNSAFE_PE_DISCONNECTION`, `EMC_SHIELD_ONE_END_UNIVERSAL`, `EMC_UPS_UNIVERSAL_FIX` 3종은 제거하지 않는다.
4. 6개 추가 규칙은 기존 보류 중인 핵심 Anchor 요구사항을 참조한다. **정규 Anchor 만족(SATISFIED)은 채점 제외 유지**하고, 확인된 부정적 오류(WRONG)만 기록한다.
5. Major는 Fatal에 의한 `passing_score_allowed=False`를 자동으로 유발하지 않는다. Major의 C-차원 처리와 추가 점수는 기존 채점 엔진 정책에 따른다.
6. Golden 점수·합격선·A–E 가중치는 변경하지 않는다. EMC 모범답안의 `ABSTAIN`은 그대로 유지되어야 한다.
7. Source span은 현재 기존 평가기 사양상 **검출된 문장을 가리키며**, 술어의 정확한 부분 구문 span 보증은 아니다.

## 4. 테스트와 릴리스 제약

`tests/test_emc_remaining_six_rules.py`에는 각 규칙당 명확한 오답 2건, 안전·반박·조건부 3건(총 30개 문장), 비EMC Topic 제한, 분류 일치, 5개 Anchor exclusion, Golden ABSTAIN 검증이 포함된다. 기존 `tests/test_emc_fatal_scope.py`도 그대로 통과해야 한다.

로컬 소스 묶음은 **채점 제외 원본 JSON 및 Golden calibration 파일 등 전체 저장소가 없으므로** 통합 테스트는 서버에서 수행한다. `validate-topic-pack-release`, `validate-all`, 관련 결정론적 채점 테스트를 모두 통과하기 전까지 PR #19 및 EMC Anchor의 HOLD는 해제하지 않는다.

검증 실패하면 변경을 커밋하지 않고 실패 사례를 누락·오검출·적용범위 오류로 분류해 재검토한다. 정규표현식 판정만으로 모든 한국어/영어 자유서술을 완벽하게 판별했다고 주장하지 않는다.
