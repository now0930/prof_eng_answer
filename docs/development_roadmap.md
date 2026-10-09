# 개발 로드맵과 검토 이력

이 문서는 최상위 README에서 분리한 개발 단계, WordPress 콘텐츠 승격 절차와 남은 일을 기록한다. 수치와 상태는 작성 당시의 증거를 가리키며, 현재 운영 상태는 코드·생성 manifest·CI·운영 환경을 다시 확인해야 한다.

## 1. 현재 구조와 확인 기준

- Topic Pack source에서 generated bank 6개를 만들고, 기본 Grader는 그 bank를 읽는다. Master의 Grading View는 호환 projection이다.
- Master의 Training/Diagnosis View와 학습 이력·Review Queue는 채점 이후의 학습 경로다. WordPress 원문·OCR이 자동으로 채점 기준이 되지 않는다.
- 이 문서 작성 시점의 커밋 기준 generated manifest는 Topic 86개다. [Topic 내용 감사](topic_pack_content_completion_20261007.md)는 747개 대표 예상문항·2,073개 Fact Anchor를 기록하지만, 그 질문을 공식 기출이나 모든 기술 사실의 최종 승인으로 간주하지 않는다.
- 실제 배포 판정에는 GitHub `main`, 서버 checkout, 컨테이너가 읽는 파일, 운영 smoke를 각각 확인한다. [운영 절차](operation_runbook.md)를 따른다.

## 2. Topic 학습 구성 단계

WordPress의 여러 단편 글을 Topic 기준의 목표 → 선수지식 → 개념·조건 → 예제 → 자가 점검으로 구성하고, 확정 채점 결과에서 필요한 학습 절로 안내하는 것이 목적이다. 학습 순서와 채점 항목은 동일하지 않다.

| 단계 | 산출물·판정 | 기록된 상태 |
|---|---|---|
| 1 | Master/View·출처·학습자료 조사 | 완료 |
| 2 | 공통 지식·학습 경로·평가 연결 계약 | 완료 |
| 3 | Schema·validator·호환 adapter | 완료 |
| 4 | 다중 WordPress 출처의 초안 준비·충돌 보존 | 완료 |
| 5 | Training View와 `/review` 표시 경로 | 완료 |
| 6 | 확정 진단→학습 절 연결, 점수 중립성 | 완료 |
| 7 | 대표 Topic의 출처·버전·이력 격리 검증 | 대표 1개 기록 |
| 8 | 로컬 회귀·release·문서·전달 | [당시 검증 기록](topic_learning_synthesis_validation.md)에 완료로 기록 |

이 표는 구조 구현 이력이다. 모든 Topic의 학습 콘텐츠가 완성·승인됐거나 운영 봇에 배포됐다는 뜻은 아니다. Nyquist 대표 학습 구성과 개정·평가 매핑 흐름은 [상세 계획](topic_learning_synthesis_plan.md), [작성 절차](topic_learning_authoring.md)에 있다. 승인되지 않은 절·불확실한 근거는 보류한다.

## 3. WordPress 출처와 채점 내용 승격

WordPress 글·HTML·자사 PDF·이미지/OCR은 비공개 출처 카탈로그에서 관리한다. 기존 README에 있던 승격 계획은 다음과 같이 분리한다.

1. 출처의 URL, version/hash, 페이지·절 등 locator와 원문을 식별한다.
2. Topic 연결 후보를 작성하고 직접 근거와 범위가 맞는지 검토한다. 불확실한 후보는 거절로 바꾸지 않고 보류한다.
3. 채점용 기술 주장이라면 `wordpress-claim-v1`로 claim·발췌·위치·대상 Fact/Logic/Model ID를 기록한다.
4. 기술 사실과 Topic 경계·적용 조건을 검토한다. 연결 승인과 정답 승인은 별개다.
5. `content-update-proposal-v1` 후보를 만들고 대상 source의 변경 전·후 및 영향 View를 확인한다.
6. 필요한 사람 승인과 후보 hash·revision 검증 후 canonical Topic Pack source에 적용한다.
7. generated 재생성, Golden/focused 회귀, 전체 release 및 재생성 일치 검사를 수행한다.

승인 전 WordPress Claim의 `score_effect`는 `none`이며, OCR 원문을 Grader 입력으로 직접 사용하지 않는다. 세부 계약은 [WordPress/View 계약](wordpress_topic_pack_view_contract.md), [Master 계약](master_topic_pack_contract.md), [Topic Pack 승인 절차](topic_pack_workflow.md)에 있다.

2026-10-05의 수동 링크 검토 문서는 직접 근거 후보 **13건**, 보류 후보 **166건**을 기록한다([결정 적용 절차](wordpress_topic_link_decision_application_workflow.md)). 이는 당시 분류 수치이며 현재 Catalog/Master의 승인·적용 건수와 같다고 간주하지 않는다. 비공개 DB·원문·OCR 본문은 Git에 싣지 않는다.

## 4. 남은 일과 게이트

| 작업 | 완료 판정 |
|---|---|
| 보류된 출처·Topic 후보 검토 | 근거와 범위가 명확한 결정만 승인; 불확실한 후보는 보류 유지 |
| Topic별 내용 정확성 보완 | 원문·독립 근거·반례 확인 후 source와 관련 테스트 수정 |
| 학습 절과 평가 매핑 확대 | 출처·ID·revision 고정, 미확정 절 격리, Grading payload 불변 |
| 실제 운영 반영 | 깨끗한 배포 대상·비공개 자료 백업, 컨테이너 파일/프로세스 parity 및 실제 smoke 확인 |

새 룰브릭 또는 채점 코드 변경은 `AGENTS.md`의 guardrail과 [검증·배포 절차](topic_pack_workflow.md)를 따른다. 과거의 `pytest 747 passed` 같은 수치는 성공 조건의 고정값이 아니다. 당시 실행 결과는 [검증 보고서](topic_learning_synthesis_validation.md)에 남기고 현재 회귀의 실제 건수·실패·건너뜀을 새로 보고한다.
