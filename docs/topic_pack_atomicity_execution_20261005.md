# Topic Pack 원자성 재구성 실행 기록

## 기준과 현재 위치

- 기준 커밋: `29fcd661e7c671d38892c8be268a64af9e19352f`.
- 지침: `topic_pack_workflow.md`, `topic_pack_atomicity.md`,
  `topic_pack_atomicity_review_20261005.md`, `rubric_authoring_guide.md`.
- 현재: Stage 1 기준 검증과 Stage 2 P0 참조 영향 조사 완료. Stage 3 회귀 입력 준비 대기.
- 이 문서는 변경 제안이다. 기술 내용 승인 또는 canonical source 변경 기록이 아니다.
- WordPress 원문, private DB, 기존 검토 주석, 채점 정책과 generated bank는 변경하지 않는다.

## 단계별 계획

| 단계 | 작업 | 완료 조건 | 상태 |
|---|---|---|---|
| 1 | 최신 지침·inventory·release baseline 확인 | audit/release 결과 확보 | 완료 |
| 2 | 지정 P0 3건의 주장·조건·참조 영향 조사 | 출처, 기존 ID, 소비자, 미확인 사항 기록 | 완료 |
| 3 | 첫 Topic의 분리안과 replay fixture 준비 | 정상/부분/오답/fatal/인접 질문 비교 입력 확보 | 대기 |
| 4 | 의미 검토 후 첫 Topic source 변경 | 검토 기록, ID 호환, focused regression | 대기 |
| 5 | RRF Topic에 동일 절차 적용 | 출처·mirror·machine contract 일치 | 대기 |
| 6 | 광범위 Topic 및 나머지 경고 검토 | 유지/분리/보류와 근거 기록 | 대기 |
| 7 | generated 재생성·통합 회귀 | release, routing/score/fatal 전후 차이 설명 | 대기 |

경고 개수만으로 Topic을 분리하지 않는다. 관리 대상 Pack의 승인 hash는 재사용하지
않으며, legacy Pack에 임의로 승인 상태를 추가하지 않는다. 내용 변경은 실제 검토
기록과 source workflow에 따라 진행한다.

## Stage 1 결과

실행 환경: 로컬 checkout, 외부 LLM 요청 없이 실행.

| 명령 | 결과 |
|---|---|
| `python3 scripts/audit_topic_pack_atomicity.py` | PASS: 85 Topics, errors 0, warnings 38 |
| `python3 scripts/rubric_manager.py validate-topic-pack-release --all` | PASS: generated_pipeline, quality, release |

상세 로그는 `/tmp/topic_atomicity_baseline.log`, `/tmp/topic_atomicity_release.log`에
저장했다. 임시 로그는 영구 증빙이 아니며 위 명령으로 재현한다. release 검증 후
generated snapshot 복구와 tracked source 무변경을 확인했다. 전체 pytest와 live
LLM 10회 재현성은 이 단계 결과에 포함하지 않는다.

## Stage 2: P0 영향 조사

### 1. 감쇠비 Fact 분리 후보

- Topic: `second_order_lag_response_by_damping_ratio`.
- 원본 위치: `fact_anchor.json`, `so2_zero_negative_damping`.
- 기존 statement의 서로 다른 판정 대상: ζ=0의 극점·지속진동·안정성,
  ζ<0의 극점·발산·안정성. 한 쪽만 설명한 답안을 구별할 필요가 있다.
- 후보: 무감쇠 응답과 음의 감쇠 응답을 별도 ID로 구성한다. 최종 ID는 아직 미정.
- 보존할 조건: 표준 2차 모델의 적용범위, 기존 극점/안정성 해석 및 오탐 방지 조건.
  조건을 생략한 일반 명제로 확장하지 않는다.
- 직접 참조: 같은 Pack의 `model_answer.json`,
  `scripts/repair_topic_pack_atomicity.py`,
  `tests/test_telegram_export_grading_regression.py`.
- 질문계약 영향: 5개 expected question 중 2개가 기존 ID를 필수로 요구하고,
  첫 번째는 `pass_required_anchor_ids`에도 이를 둔다. 이를 두 신규 ID 모두
  필수로 바꾸면 합격 gate가 강화되므로 질문별 요구를 따로 결정해야 한다.
- 테스트 영향: `test_second_order_answer_missing_zero_and_negative_damping_is_not_high_score`
  가 기존 ID의 PARTIAL/MISSING을 검사한다. 새 ID로 재작성할 때 정상·부분 응답의
  요구 상태를 먼저 기록한다.
- 기존 주석 참조: `study/source_review_annotations/second_order_lag_response_by_damping_ratio.json`.
  이 파일은 미확정 원문 검토 의견이므로 새 ID로 덮어쓰지 않는다.
- 호환성: 과거 requirement 상태의 기존 ID를 삭제·치환하지 않는다. 새 schema/version
  또는 명시적 구/신 ID 매핑이 필요한지 resolver를 조사한 후 결정한다. 기존 하나의
  coverage가 두 개의 독립 가점으로 자동 증가하지 않게 전후 점수를 비교한다.
- 미확인: private Master의 실제 grading_links와 historical session 참조,
  원문 locator 및 외부 기술 근거의 충분성. 추적 파일 검색만으로 미사용을 선언하지 않는다.

### 2. 감쇠비 Logic 분리 후보

- 같은 Topic의 `logic_check.json / llm_profile.fatal_conditions`에서
  `표에서 Under damp => ζ<0.7, Critical damp => ζ=0.7, Over damp => 0.7≤ζ<1`
  문자열이 세 오개념을 함께 표현한다.
- 중요 발견: 같은 배열의 앞부분에 세 분류 오류가 이미 각각 별도 문자열로 존재한다.
  따라서 동일한 규칙 세 개를 추가하는 방식은 중복 검출/중복 페널티 위험이 있다.
- 후보: 기존 개별 규칙이 표 evidence에도 적용되는지 먼저 검사하고, 통합 문자열은
  회귀 fixture로 보존할지 검토한다. 별도 표 규칙이 필요하면 각 오개념의 owner를
  명확히 하되 severity/penalty 정책을 바꾸지 않는다.
- 필요한 fixture: 세 오류 각각, 혼합 표, 올바른 표, 반박 표현, 단순 누락,
  ζ≈0.707 실무 절충값의 정상 설명. 하나의 오류를 여러 rule이 중복 소유하지 않아야 한다.
- 결정: 분리 방향은 타당한 검토 후보이나 구현 방식은 미확정. fatal을 삭제하거나
  약화한 것으로 해석될 변경은 replay 없이 하지 않는다.

### 3. RRF Fact 분리 후보

- Topic: `hazop_lopa_ipl_risk_reduction_sil_target_allocation`.
- 위치: `fact_anchor.json / hazop_lopa_required_rrf`.
- 기존 statement의 판정 대상: RRF 비율 정의, 1 이하의 추가 위험감소 해석,
  demand mode별 PFDavg/PFH, SIL 약어. 요구 질문별 선택 가능한 주장으로 검토한다.
- 기존 `claim`, `description`, 첫 `accepted_explanations`에는 RRF 정의/해석만 있다.
  statement만 분리하지 말고 positive evidence mirror와 중복 Anchor를 함께 확인한다.
- source_basis: `docs/topic_sheets/hazop_lopa_ipl_risk_reduction_sil_target_allocation.md`.
  이것은 저장소의 authoring 출처이며 외부 표준 조항 검증 완료를 뜻하지 않는다.
- 직접 참조: `model_answer.json`의 여러 required_anchor_ids,
  `logic_check.json`의 requirement_id와
  `required_rrf_uses_residual_tolerable_ratio` machine fact,
  `tests/test_hazop_lopa_canonical_promotion.py`.
- 결정론적 연결: `tests/test_hazop_lopa_canonical_promotion.py`는 기존 ID를
  9개 canonical requirement 중 하나로 고정한다. 좁은 RRF/PFDavg/SIL 질문에서는
  정확히 기존 ID를 포함한 3개 requirement만 활성화한다. 새 Anchor를 질문계약에
  곧바로 추가하면 이 명시적 범위가 달라진다.
- 별도 `question_demand_axes.json`과 `logic_check.json / machine_contract`가
  존재한다. RRF의 기존 machine requirement는 빈도비 한 관계를 소유하므로
  demand mode·SIL 약어로 확장하지 않는다.
- 후보: 기존 ID를 RRF 정의 owner로 유지할지 먼저 검토한다. demand mode/용어의
  기존 owner가 있으면 재사용하고, 모든 RRF 질문에 새 Anchor를 일괄 필수화하지 않는다.
- 필요한 fixture: 비율 정상/역전/곱셈 오류, RRF만 묻는 질문, demand mode 질문,
  용어만 묻는 질문, 누락과 명시적 오답 구분, 인접 SIL Topic 라우팅.
- 미확인: 관련 source의 정확한 조항/locator, 분리 이후 importance 및 denominator 영향,
  private Master와 Feedback 링크. 확정 사실을 추가하는 대신 미확인으로 남긴다.

### 소비자·출처 점검 결과

| 소비 경로 | 감쇠비 ID | RRF ID | 변경 전 조치 |
|---|---|---|---|
| Fact source | 단일 복합 Anchor | 복합 statement, RRF 중심 mirror | 각 주장과 조건 분리 후보 작성 |
| Model question contract | 2개 질문 필수, 1개 pass 필수 | 복수 질문에서 필수 | 질문별 기존 범위와 gate 유지 기준 기록 |
| Logic/machine contract | 표 분류 fatal 문자열과 별도 규칙 | 비율 fact에 묶인 requirement ID | 의미 중복과 severity 확인 |
| Question demand axes | 별도 파일 없음 | 별도 파일 있음 | 기존 explicit demand를 먼저 대조 |
| 회귀 테스트 | Telegram export 관련 1개 직접 참조 | canonical promotion 직접 참조 | 동일 입력의 전후 요구 상태 확보 |
| Learning/Feedback | tracked source의 검토 주석에 감쇠비 ID 1개 | tracked source에서 직접 ID 참조 없음 | private Master/이력 DB 별도 확인 |

두 Topic 모두 `topic_status.json`이 없는 legacy unmanaged Pack이다. 이 사실은
기술 내용 승인 여부를 나타내지 않는다. 이 checkout의 `data/`에는 private Master와
과거 session이 없어 실제 저장 이력의 링크 부재를 검증할 수 없다. Source의 직접
참조 목록만 확인한 상태이며, 배포 전 private 환경에서 동일 ID 검색이 필요하다.

### Stage 2 판정

- `so2_zero_negative_damping`: 독립 판정 가능한 두 주장이다. 분리 후보 확정.
  기존 ID의 이력 호환 방식과 질문별 필수 범위는 Stage 3 replay 후 결정한다.
- 감쇠비 표 Logic: 세 오개념의 개별 규칙이 이미 있다. 기존 통합 문자열을 단순히
  세 번 복제하지 않는다. 표 문맥에서 개별 검출 가능한지 Stage 3에서 확인한다.
- `hazop_lopa_required_rrf`: RRF 비율·해석 외 추가 주장이 statement에 섞여 있다.
  기존 ID/machine contract를 비율 owner로 유지하는 후보가 가장 변경 범위가 작다.
  새 주장에 대한 source locator는 아직 불충분하므로 canonical 사실 추가는 보류한다.

## 다음 실행

감쇠비 Topic 하나부터 동일 입력 replay baseline을 준비한다. `model_answer`의
pass gate와 기존 requirement ID에 대한 상태를 정상·부분·오답·fatal·인접 질문별로
기록한다. private Master/이력 DB의 링크는 이 checkout에 없으므로 배포 전 별도
확인 항목으로 유지한다. generated 산출물, 원문 미확정 주석, 전체 Pack 경계는
이번 조사에서 변경하지 않았다.
