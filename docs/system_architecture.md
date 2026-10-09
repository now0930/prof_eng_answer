# 시스템 구조와 데이터 권한

이 문서는 프로젝트 전체의 연결 관계를 설명합니다. 알고리즘·필드·운영 명령의 정본을 복제하지 않고 해당 문서와 코드로 연결합니다.

## 1. 두 경로를 구분한다

```text
채점 경로
Topic Pack JSON ─► builder ─► generated bank ─► Grader ─► grade.json/결과
       ▲                                            │
       └──── 검토된 콘텐츠 변경 제안 ◄───────────────┘ (오류 발견 시 별도 검토)

학습·출처 경로
WordPress 원문/HTML·자사 PDF·이미지 ─► 비공개 출처 카탈로그
          │ URL·버전·해시·위치·검토 상태    │ 승인된 참조
          └───────────────────────────────► Master Topic Pack
                                               ├─ Grading View: 기존 source 호환 projection
                                               ├─ Training View ─► /review
                                               └─ Diagnosis View + 확정 grade ─► 피드백
                                                                    │
                                                      학습 이력·Review Queue
```

운영 Grader는 `study/topic_views.py`의 `grading_view()`를 호출해 채점하지 않습니다. 기본 `RUBRIC_BANK_MODE=generated`에서 `grading/rubrics/rubric_bank_paths.py`가 생성 bank 경로를 선택합니다. Grading View는 기존 source와의 호환성을 검증하는 읽기 전용 adapter입니다. 이를 실제 채점 경로로 전환하려면 별도 parity·회귀 검증이 필요합니다.

## 2. 계층별 소유권

| 계층 | 정본·입력 | 허용되는 출력 | 금지되는 승격 |
|---|---|---|---|
| WordPress Source Pack | 게시글·첨부 원문, 추출/OCR, 출처 메타데이터 | 원문 참조와 변경 제안 | OCR/HTML을 즉시 정답·감점 규칙으로 사용 |
| Topic Pack source | `rubrics/topic_packs/<topic_id>/`의 Fact·Model·Logic·Importance 등 | 검토된 채점 규칙 | 승인·검증을 우회한 변경 |
| Generated bank | Topic Pack source의 builder 출력 6개 | 운영 Grader가 읽는 bank | 수동 편집 |
| Master Topic Pack | `master_topic_packs/<topic_id>.json`의 식별자·revision·source 참조·projection 계약 | 세 View의 입력 | 별도 채점 규칙 DB로 중복 관리 |
| Grading View | 기존 채점 source의 호환 projection | adapter·계약 검증 | 현재 운영 Grader의 직접 판정권을 주장 |
| Training View | Topic 자료·검토된 학습 구성·출처 자료 | `/review` 학습 화면 | 점수·fatal 변경 |
| Diagnosis/Feedback View | 진단 안내와 확정 채점 결과 | 부족점·복습 자료 안내 | 점수·판정 재계산 |
| 학습 이력·Review Queue | 사용자별 시도·진단·복습 상태 | 다음 학습 대상 후보·이력 | Master 또는 Topic Pack에 개인 상태 저장 |

채점 배점 A/B/C/D/E와 Question Type·routing·fatal의 실제 권한은 [채점 아키텍처](grading_architecture.md), [Question Type](question_type_taxonomy.md), 관련 코드·회귀 테스트가 소유합니다. Master와 학습 계층을 추가해도 이 권한은 이동하지 않습니다.

## 3. Topic과 콘텐츠의 연결

`topic_id`는 채점 source, Master, 세 View를 연결합니다. Topic Pack은 공식 기출문항 1개와 동의어가 아닙니다. 예상 가능한 문항 범위와 단위 지식을 정리한 자료이며, 대표 질문·Fact Anchor의 정확성과 경계는 개별 검토가 필요합니다. 현재 생성 manifest의 Topic 86개와 Fact Anchor 2,073개라는 수치는 해당 커밋의 스냅샷이지 영구 계약이 아닙니다.

Master는 본문 전체를 복제하는 저장소가 아닙니다. `schemas/master_topic_pack.schema.json`에 정의된 식별자·참조·projection 계약을 관리하고, `study/master_topic_pack.py`와 `study/topic_views.py`가 필요한 View를 독립적으로 구성합니다. Feedback은 저장 계약 `diagnosis-projection-v1`을 사용하는 사용자 화면 이름입니다. 별도 네 번째 채점 View가 아닙니다.

여러 WordPress 글을 하나의 Topic 학습 흐름으로 종합하는 문서는 원문과 구분합니다. 공통 지식·학습 절·평가 ID의 매핑은 [학습 구성 계약](topic_learning_synthesis_contract.md)에 따르며, 학습 절 전체가 모든 문제의 필수 채점 항목이 되지 않습니다. 확정 채점 결과에서 학습 절로 향하는 안내도 점수 중립입니다.

## 4. 출처에서 채점 기준까지

1. 게시글·첨부를 식별하고 URL, 버전·해시, 페이지/절, 추출 방법 및 검토 상태를 기록합니다. WordPress 원문 DB와 OCR 본문은 비공개로 보관합니다.
2. Topic 후보 링크와 변경 제안을 만들고 승인된 source reference만 Master에 반영합니다. 출처 연결은 그 내용의 기술적 정확성 승인과 다릅니다.
3. Training은 연결된 원문·검토 주석을 상태와 함께 보여줄 수 있습니다. 버전·해시 불일치 또는 범위 지정 오류는 해당 자료를 보류합니다.
4. 채점에 쓸 claim은 별도의 근거·적용 조건·Topic 경계 검토와 콘텐츠 제안·승인을 거쳐 Topic Pack source로 반영합니다.
5. builder가 generated bank를 다시 만들고, 회귀·재생성 일치 검사를 통과해야 운영 Grader의 기준이 바뀝니다.

세부 필드와 승인 상태는 [WordPress/View 계약](wordpress_topic_pack_view_contract.md), [Master 계약](master_topic_pack_contract.md), [Topic Pack 절차](topic_pack_workflow.md)가 소유합니다. 사람 승인이 필요한 채점 source 변경을 학습 콘텐츠의 LLM 검토 상태로 대체하지 않습니다.

## 5. 결과·복습 경계

`/grade`는 확정된 결과를 만든 뒤 학습 이력에 점수와 진단을 기록합니다. Diagnosis View는 그 결과를 설명·학습 자료에 연결하지만 채점 결과를 다시 쓰지 않습니다. `/review <topic_id 또는 주제명>`은 사용자가 고른 Topic을 표시합니다. Review Queue는 향후 추천에 사용할 수 있는 별도 계약으로, 날짜 기반 자동 선택이 Telegram 명령의 현재 동작은 아닙니다. 이전 피드백은 작성 시점의 snapshot이므로 최신 Master와 같은 revision이라고 단정하지 않습니다.

구현과 저장 계약은 [학습 계층](learning_layer.md), [Master/View 구조](master_view_architecture.md)를 참조합니다.

## 6. 생성·검증·운영 반영

Topic Pack source와 generated bank를 같은 파일로 취급하지 않습니다. source 변경 후 공식 절차로 생성하고, 임시 디렉터리에서 다시 생성한 6개 파일과 커밋된 파일이 바이트 단위로 같은지 검사합니다.

```bash
python3 scripts/rubric_manager.py validate-topic-pack-release --all --promote-generated
python3 -B scripts/check_generated_rubrics_freshness.py
PROMOTE_GENERATED=0 scripts/validate_release.sh
```

새 managed Topic은 사람 승인과 source hash 일치가 먼저 필요합니다. `--all --promote-generated`는 승인 누락을 우회하는 명령이 아닙니다. CI는 non-promote release, 재생성 일치, 의도치 않은 diff를 검사합니다. 10회 채점 재현성 gate는 opt-in이며 일반 CI PASS에 포함됐다고 주장하지 않습니다.

GitHub 병합, 서버 checkout 갱신, 컨테이너 재시작, 실제 요청 smoke는 서로 다른 단계입니다. 실행 중인 프로세스가 이전 코드를 마운트하거나 사용자 변경이 있는 checkout을 사용할 수 있으므로 CI 성공만으로 배포 완료를 선언하지 않습니다. 배포 절차와 증거는 [운영 runbook](operation_runbook.md)을 따릅니다.
