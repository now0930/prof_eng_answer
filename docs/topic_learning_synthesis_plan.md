# WordPress 기반 Topic 지식·학습 구성 작업 계획

## 목표와 범위

여러 WordPress 게시글의 단편적인 내용을 Topic 기준으로 종합하고, 공통 지식에
학습 순서와 평가 연결을 부여한다. Training은 논리적인 설명 흐름을 제공하고
Grading은 기존 문제 요구사항과 승인된 평가 규칙을 유지한다. Feedback은
평가 결과에서 학습할 개념과 절로 연결한다.

기존 82개 Topic을 일괄 재작성하지 않는다. 대표 Topic 1개에서 검증한 다음
최대 3개로 확장한다. 비공개 DB·원문·개인 답안을 Git에 올리지 않는다.
WordPress 원문은 보존하며 변경 제안과 주석은 분리한다.

## 전체 단계와 현재 위치

| 단계 | 작업 및 산출물 | PASS 기준 | 상태 |
|---|---|---|---|
| 1 | 현재 Master/View·학습자료·승인 흐름 조사 | 실제 구현과 미구현 사항 기록 | 완료 |
| 2 | 공통 지식·학습 경로·채점 연결 계약 설계 | ID·revision·출처·검토 상태·호환 정책 명시 | 완료 |
| 3 | schema·validator·호환 adapter 구현 | 참조 무결성, 중복 ID, 순환 선수관계, 버전 불일치 테스트 | 완료 |
| 4 | 여러 WordPress 글을 종합하는 초안 생성 경로 | 다중 출처·중복 통합·충돌·추론 표시, 원문 보존 | 완료 |
| 5 | Training View와 /review 소비 경로 확장 | 학습 목표부터 자가 점검까지 순서대로 표시, 기존 v1 fallback | 완료 |
| 6 | 기존 채점 ID 및 Feedback 연결 | 미충족 요구사항→지식→학습 절 연결, 점수·판정 동일 | 완료 |
| 7 | 대표 Topic 1~3개 통합 검증 | 여러 글 종합·출처 추적·stale 처리·이력 격리 E2E | 완료 (1개) |
| 8 | 전체 회귀·release gate·문서·전달 | 필요한 gate PASS, 비공개 자료 제외, 단계별 commit | 검증 실행 완료 / 전체 pytest 11건 실패로 미완료 |

각 단계 PASS 후 해당 변경만 commit한다. 실패는 원인과 재현 명령을 기록하며
테스트 제외나 기대값 완화로 PASS 처리하지 않는다. push 시 실제 remote를
확인하고 성공한 목적지를 보고한다. 운영 재시작과 콘텐츠 승인은 별도 작업이다.

## Stage 1 조사 결과

- `schemas/master_topic_pack.schema.json`: Master는 기존 채점 source 참조,
  세 projection, 출처, 선택적 `learning_materials` 경로를 관리한다.
- `study/master_topic_pack.py::project_training`: 기존 fact/model/importance에서
  문제·목차·핵심 사실·누락 포인트를 읽고 WordPress HTML과 학습자료를 추가한다.
- `study/topic_views.py`: 세 View의 공개 읽기 인터페이스가 있다.
- `study/learning_materials/`: 현재 Nyquist 학습자료 예제가 있다. 별도 학습자료
  경로를 재사용할 수 있으므로 동일 역할의 저장소를 무조건 추가하지 않는다.
- `study/review_presentation.py`: 현재 원문·주석 발췌 표시가 중심이다.
- `study/learning_runtime.py`: 사용자가 선택한 Topic의 Training과 과거 진단을
  결합한다. 학습 진행 상태는 Master와 별도다.
- 원문 로더는 현재 연결된 WordPress post/page의 WXR/REST HTML을 지원한다.
  모든 PDF·이미지 OCR이 Training View에 직접 제공된다고 간주하면 안 된다.
- 현재 Master source reference schema에는 콘텐츠 해시 필드가 없다. HTML
  bundle의 자체 해시 검사와 학습자료의 근거 해시 고정은 서로 다른 검사다.
  새 계약은 어떤 버전·해시를 승인했는지 명확히 고정해야 한다.
- 직전 설명의 `content_sources: [learning_materials, wordpress_sources, ...]`는
  제안 예시이며 현재 v1 enum으로 유효하지 않다. v1에 그대로 적용하지 않는다.

아직 없는 핵심 기능은 안정적인 공통 지식 ID, 지식 간 관계, 다중 출처 기반
종합 설명, 학습 절 순서, 평가 요구사항에서 학습 절로 가는 명시적 매핑이다.

## Stage 2 계약

상세 필드·상태·호환 경계는 [확정 설계](topic_learning_synthesis_contract.md)에
기록했다. 구현 완료를 의미하지 않는다. 새 synthesis 문서는 기존 학습자료를
material ID로 재사용하고, Master의 선택적 참조로 연결한다.

| 계약 | 설계할 필드와 불변식 |
|---|---|
| 공통 지식 | `knowledge_id`, `topic_id`, revision, 개념/관계/수식, 적용 조건·예외, 여러 evidence 참조 |
| 출처 근거 | source ID, 정확한 URL, 버전, 해시, 위치, 인용; 원문과 종합 설명 구분 |
| 학습 경로 | path/section ID, 학습 목표, 선수관계, 순서, knowledge 참조, 설명·예제·자가 점검 |
| 평가 매핑 | 기존 source/record/requirement ID와 knowledge ID 연결; 문제 범위는 기존 demand authority가 결정 |
| 검토 | 출처 연결, 지식 정확성, 학습 구성, 채점 승인 상태를 별도 관리 |
| 충돌 | 상반된 근거와 적용 조건을 보존; 미해결 항목을 확정 지식으로 승격하지 않음 |
| 변경 | source 변경→영향받는 지식/절/평가 매핑 탐색→제안→승인; revision 고정 |

학습용 설명을 바꿔도 Grading payload가 변하지 않아야 한다. 지식 검토 승인은
새 채점 규칙 승인과 다르다. 교육 목적으로 생성한 연결 설명과 예시는 출처가
직접 주장하는 내용과 구분한다. LLM 작성·검토 결과는 검토자와 상태를 남긴다.

Master는 참조·버전의 중심으로 유지하며 별도 파일로 내용을 관리할 수 있다.
`learning_materials`와 기존 소비자를 재사용하는 additive 방식부터 검토하고,
v2가 필요하면 v1 adapter를 함께 정의한다. 이 문서의 필드는 아직 구현된
schema로 취급하지 않는다.

## 검증과 알려진 제약

Stage 8: 전체 pytest 723 passed / 11 failed / 1 warning. Stage 3 로그와 실패
node ID 집합이 동일하며 신규 실패는 0개다. non-promote release 스크립트는
exit 0이다. opt-in 재현성 검사와 live smoke는 실행하지 않았다. 전체 회귀 PASS
조건은 미충족이며 [실패 분류와 전달 상태](topic_learning_synthesis_validation.md)에
후속 작업을 기록했다. 실제 운영 반영·최종 push는 하지 않았다.

Stage 7: Nyquist의 WordPress 글 2개를 6개 지식·6절·5개 선수관계로 종합했다.
기존 계산 예제 material ID를 재사용하고 작성본·후보·검토 메모는 비공개
`data/topic_learning_authoring/`에 저장했다. 운영 Master는 변경하지 않았다.
실제 자료 E2E는 임시 복사본에서 draft 보류→LLM 검토 상태 표시→History 저장→
/review→복습 완료→출처 변경 감지를 확인했다. 원문·Master·canonical 파일 해시와
Grading payload 불변을 검사했다. 사람 검토 완료 상태는 부여하지 않았다.
question_demand_axes가 없는 Topic이므로 실제 요구사항 매핑은 비워 두었고,
무매핑 fallback을 확인했다. 정확한 매핑은 Stage 6의 합성 fixture에서 검증했다.
공개 checkout에 비공개 후보가 없으면 이 E2E는 skip한다.
실제 E2E 1 passed, 관련 합계 53 passed, release validation PASS.
로그: `/tmp/synthesis_stage7_e2e.log`, `/tmp/synthesis_stage7_tests.log`,
`/tmp/synthesis_stage7_release.log`.

Stage 6: `study/learning_feedback.py`를 Diagnosis projection과 확정 grade
feedback adapter, /review에 연결했다. `question_demand_axes.requirements`의
requirement_id와 canonical ledger row를 정확히 연결한다. Topic, source_file,
requirement_text까지 일치해야 하며 missing/partial/incorrect만 추천한다.
unknown/correct, 모호한 ID, 검토 대기 매핑은 추천하지 않는다. 매핑은
human_verified여야 하고 해당 학습 절은 현재 eligible이어야 한다.

snapshot에는 Master/synthesis revision과 지식·절 ID/제목만 추가하며 원문 본문을
복사하지 않는다. /review는 현재 버전과 다르면 이전 절 안내를 최신 자료로
표시하지 않는다. 원문 변경은 기존 source hash 검사에서 차단한다.
canonical source resolver는 실제 requirement_id와 nested deterministic check
컬렉션을 지원한다. 안정적인 ID 없는 topic_importance는 계속 거부한다.
Fact/Logic 레코드 참조 검증은 지원하지만 그 결과의 Feedback 소비는 별도
명시적 ID adapter가 필요하므로 이번 구현은 requirement ledger 경로에 한정한다.

관련 테스트 47 passed, 기존 통합·작성·표시 테스트 33 passed (기존 warning 1개),
release validation PASS. 실제 Topic 매핑은 아직 작성·승인하지 않았으며 기존
채점 점수·규칙은 수정하지 않았다. 전체 pytest 기존 실패는 여전히 미해결이다.
로그: `/tmp/synthesis_stage6_tests.log`, `/tmp/synthesis_stage6_integration.log`,
`/tmp/synthesis_stage6_release.log`.

Stage 5: `learning_review_messages()`를 `/review`에 연결했다. 기존 개요 뒤에
학습 목표와 순서 있는 절을 표시하고 마지막에 복습 완료 명령을 안내한다.
기존 v1 Topic은 기존 단일 응답을 유지한다. 새 자료가 unavailable이면 내부
경로·오류 원문을 노출하지 않고 기존 자료 사용을 안내한다.
eligible section만 본문을 표시하고 draft 경로는 보류한다. LLM 검토와 사람
검토 상태, 원문/종합/작성 설명을 명시한다. 조건·단위·예외·자가 점검·출처를
보존하며 UTF-16 3000단위 이내로 분할해 긴 수식을 자르거나 누락하지 않는다.
연결 학습자료는 현재 ID만 안내하며 별도 자료 본문 화면은 후속 확장 대상이다.

검증: 관련 47 passed, 기존 History/View/비공개 E2E 15 passed (기존 return-value
warning 1개), release validation PASS. 실제 Telegram 전송은 mock으로 검사했고
운영 bot을 재시작하거나 실제 Topic에 후보를 연결하지 않았다. 전체 pytest의
기존 11개 실패는 이번 단계에서 수정하지 않았다. 로그는
`/tmp/synthesis_stage5_tests.log`, `/tmp/synthesis_stage5_integration.log`,
`/tmp/synthesis_stage5_release.log`다.

Stage 4: `study/synthesis_authoring.py`와
`scripts/author_topic_learning_synthesis.py`에 prepare/build 경로를 구현했다.
[작성 절차](topic_learning_authoring.md)에 LLM/사람의 설명 작성 책임과 자동 검증
범위를 구분했다. 관련 42 tests PASS, release validation PASS. 실제 Nyquist
자료 2개 prepare PASS. 실제 본문 종합은 Stage 7에서 수행한다. 검토·적용은
자동 승인하지 않으며 이 단계에서는 어떠한 Master 참조도 변경하지 않았다.
로그는 `/tmp/synthesis_stage4_tests.log`, `/tmp/synthesis_stage4_release.log`다.

Stage 3 구현: `schemas/topic_learning_synthesis.schema.json`,
`study/learning_synthesis.py`, Master 선택적 참조와 Training의 선택적 출력.
기존 Master 파일과 실제 학습·채점 콘텐츠는 변경하지 않았다. 새 자료의 오류는
`unavailable`로 반환하고 기존 Training 필드를 유지한다. 원문 확인 결과와
`eligible_section_ids`를 별도로 반환하며 전체 문서는 검토용이다. 일반 화면이
전체 document를 그대로 표시하면 안 된다. 화면 적용은 Stage 5 작업이다.

추가 의존성 없이 bundled schema에 사용한 키워드를 검사한다. 지원하지 않는
키워드 추가는 명시적으로 거부한다. schema는 구조를, Python은 참조·순환·근거
일치 검증을 추가로 담당한다. 검토자 문자열만으로 사람 신원을 인증할 수는
없으므로 human_verified 권한 확인은 향후 명시적 적용 경로가 담당해야 한다.

Canonical 연결은 현재 알려진 배열의 `id`를 엄격하게 찾는다. 기존 source가
중첩 객체이거나 안정적인 ID가 없으면 unsupported 오류를 반환한다. 전 source
종류의 실제 ID resolver 확대와 Feedback 소비는 Stage 6에서 수행한다.

검증: focused 59 passed, release validation PASS. 전체 pytest 첫 실행은
688 passed / 기존과 같은 11 failed / 1 warning이었다. 이후 경로·snapshot·순환
테스트 6개를 추가하여 focused 결과에 포함했다. 전체 회귀 PASS로 간주하지 않는다.
로그: `/tmp/synthesis_stage3_focused.log`, `/tmp/synthesis_stage3_full_pytest.log`,
`/tmp/synthesis_stage3_release.log` (로컬 임시 로그, Git 미포함).

구조 검증은 다중 출처, 끊어진 참조, 중복 지식 ID, 잘못된 Topic 연결,
선수관계 순환, stale 자료, 반환값 격리, 보조 자료 실패 시 채점 보존을 포함한다.
통합 검증은 요구사항에서 학습 절로 이동하는 경로와 학습 수정 전후 Grading
payload 동일성을 확인한다. 내용의 최종 정확성 승인은 사용자 검토로 남긴다.

직전 실행에서 관련 테스트 30개가 통과했고 `pytest tests`는 670 passed /
11 failed였다. 전체 scripts 포함 실행은 2423 passed / 13 failed / 4 errors였다.
이 수치는 이번 문서 작업에서 재실행한 결과가 아닌 이전 실행 기록이다.
`pytest.ini`는 기본 검색 대상을 tests로 제한하므로 전체 회귀 검증은 scripts의
기존 runner와 Golden/release gate도 포함해야 한다. 기존 실패의 원인을 확인해
기준선을 기록하고, 해소되지 않은 상태를 전체 회귀 PASS로 표현하지 않는다.

원격 `origin`은 현재 로컬 경로 저장소를 가리키며 직전 push는 임시 object
디렉터리 생성 오류로 실패했다. 이 원격으로의 push 성공도 GitHub 게시와
동일하다고 보고하지 않는다.
