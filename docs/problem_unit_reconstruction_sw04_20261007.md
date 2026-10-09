# SW-04 계측제어 SW lifecycle Topic Pack 감사 — 2026-10-07

## 판정

`instrumentation_control_software_lifecycle_v_model_traceability_verification_validation`는
요구사항·V-Model·시험수준·V&V·RTM·분석·테스트 환경·변경/결함 증적을 다루는 SW-04 문제군이다.
13개 대표 질문을 유지하되 일반 lifecycle 질문과 SIL/MC/DC가 명시된 복합 질문의 평가범위를
분리한다.

## Coverage·연결 검사

- 33 Fact Anchor 중 최소 한 pattern의 required union에 연결된 수는 29/33 = 87.9% (screen 표기 88%).
- Union에서 빠진 4개는 `sw04_coding_standard`, `sw04_sw05_boundary`, `sw04_sw10_boundary`,
  `sw04_system_architecture`다. 현재 13개 질문은 별도로 coding standard, project acceptance
  handover, full system architecture를 필수 질문으로 묻지 않는다. 범위 경계 2개는 routing/context
  자료이므로 coverage 숫자를 위해 required anchor로 추가하지 않는다.
- 기존 outline은 32/33 Anchor를 참조했고 `sw04_mcdc_detailed_coverage_boundary`만 빠졌다.
  Simulation/HIL/Fault injection 및 V-model/SIL 경계와 연관된 학습 outline에 참조를 추가해
  33/33으로 만들었다.

## 패턴별 지식 보완

- Pattern 12 문항은 MC/DC를 직접 명시하지만 운영 MC/DC 복합문항 회귀의 원시 필수항목 13개를
  유지한다. `sw04_mcdc_detailed_coverage_boundary`와
  `vmodel_no_sil_guarantee__mcdc_adjacent_boundary`는 학습 outline과 범위 안내에 연결하고
  별도 필수 채점항목으로 추가하지 않는다. 이는 상세 MC/DC 책임의 차이를 학습할 수 있게 하면서
  기존 복합문항의 중복 채점을 막는다.
- Pattern 13은 generic V-Model/unit·integration·system test와 SIL 관련 SW verification을 묻고,
  `routing_exclusive_block_terms`에 MC/DC/정적·동적 분석 용어가 있다. 이 기존 차단조건은
  변경하지 않았고 Pattern 13에 상세 MC/DC 요구를 추가하지 않았다.
- 전체 required union은 여전히 29/33이다. 개선 지점은 union 퍼센트를 인위적으로 높이는 것이 아니라
  명시된 MC/DC 질문의 pattern-level 누락을 바로잡은 것이다.

## Scoring 범위·기존 topic overlap

19개 `high_score_points`, 17개 `common_missing_points`, 9개 high-band unlock 문구를 pattern 번호와
조건에 연결했다. 이에 따라 일반 lifecycle 문제에 HIL/Fault injection/MC/DC를 동시에 요구하지
않으며, 누락만으로 감점하지 않는다. MISRA와 xUnit/test harness의 차이는 기존 focused
overgrading regression이 소유하므로 관련 시험도구 문맥에서만 남겼다.

Pattern 12의 동일 문구는 SW-04, SW-05 및 전용 MC/DC Topic에 함께 있고, existing regression
fixture `MCDC-VMODEL-SIL-OVERGRADING-01`은 이 세 topic ID를 명시적으로 기대한다. 이는 기존
hybrid regression 범위이므로 변경하지 않았다. Pattern 13 문구도 SW-05에 중복되지만 SW-04의
pattern은 `routing_exclusive` block terms를 가지고 있다. Router, canonical ownership, Topic Type,
Golden expected topic set은 이번 작업에서 수정하지 않았다.

이 작업은 Topic Pack source와 문서의 scope clarification이며 runtime이 pattern별로 기계적 점수
gating을 한다고 주장하지 않는다.

## 검증 결과

- SW-04 focused regression `scripts/test_instrumentation_control_software_lifecycle_v_model.py`: PASS (32 tests)
- 복합 overgrading regression `scripts/test_mcdc_vmodel_sil_overgrading_regression.py`: PASS; hybrid fixture scope와 prior cap/evidence expectations 보존
- `validate_topic_packs.py --topic-id ...`: PASS; global uniqueness 포함 2,066 Anchor 검사
- `validate_topic_pack_quality.py --topic-id ... --require-logic-check`: PASS; errors 0, warnings 0
- `audit_topic_pack_atomicity.py --topic-id ...`: PASS; errors 0, warnings 0
- `validate_topic_pack_release.py --topic-id ... --require-logic-check`: PASS; generated pipeline PASS
- `git diff --check`: PASS
- Release validator가 임시 생성한 `rubrics/generated/` 파일은 사전 snapshot으로 복원했다.

## 변경 파일

- `rubrics/topic_packs/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation/model_answer.json`
- 동 topic `README.md`, `topic_importance.json`
- `docs/topic_sheets/instrumentation_control_software_lifecycle_v_model_traceability_verification_validation.md`
- `scripts/test_instrumentation_control_software_lifecycle_v_model.py`
- `docs/topic_pack_reorganization_progress_20261007.md`, `docs/README.md`

그 밖의 기존 dirty worktree 변경은 수정·stage하지 않았다. 기존 Grader A/B/C/D/E·deterministic
score, routing authority, fatal IDs, Golden/release gate와 generated output을 직접 수정하지 않았다.
