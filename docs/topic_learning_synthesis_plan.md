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
| 4 | 여러 WordPress 글을 종합하는 초안 생성 경로 | 다중 출처·중복 통합·충돌·추론 표시, 원문 보존 | 다음 작업 |
| 5 | Training View와 /review 소비 경로 확장 | 학습 목표부터 자가 점검까지 순서대로 표시, 기존 v1 fallback | 대기 |
| 6 | 기존 채점 ID 및 Feedback 연결 | 미충족 요구사항→지식→학습 절 연결, 점수·판정 동일 | 대기 |
| 7 | 대표 Topic 1~3개 통합 검증 | 여러 글 종합·출처 추적·stale 처리·이력 격리 E2E | 대기 |
| 8 | 전체 회귀·release gate·문서·전달 | 필요한 gate PASS, 비공개 자료 제외, 단계별 commit | 대기 |

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
