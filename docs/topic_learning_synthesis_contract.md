# Topic 공통 지식·학습 구성·평가 연결 계약

상태: Stage 2 설계 확정. 아래 계약은 Stage 3 구현 대상으로, 현재 런타임이
이미 지원하는 필드나 승인된 기술 내용으로 취급하지 않는다.

## 저장 및 호환 경계

새 문서 형식은 `topic-learning-synthesis-v1`로 한다. 기존
`master-topic-pack-v1`, `training-projection-v1`, `topic-learning-material-v1`
파일은 수정 없이 읽을 수 있어야 한다. 기존 `learning_materials`에는 새
형식의 파일을 넣지 않는다. 해당 로더는 기존 학습자료 필드를 엄격히 검사한다.

Stage 3에서는 Master에 선택적 `learning_synthesis` 참조를 추가한다.
이 변경은 additive schema 확장이므로 schema와 Python validator를 함께
배포한다. 확장 전의 엄격한 로더가 새 필드를 읽을 수 있다고 가정하지 않는다.
참조를 추가하지 않은 기존 Master는 그대로 지원한다.

참조는 `{path, revision, content_sha256}`이며 경로는 repository 내부의
상대 JSON 경로다. 해시는 파일 원본 바이트의 SHA-256이다. Topic ID, revision,
해시가 모두 맞을 때만 새 자료를 읽는다. 기본 내용 저장 위치는 비공개
`data/topic_learning_synthesis/<topic_id>.json`으로 한다. 공개 테스트는
가상 출처와 합성 문장을 사용하고, 실제 WordPress 본문을 fixture에 넣지 않는다.

Master 참조 갱신은 기존 source/content proposal과 구별되는 학습 구성 변경이다.
기존 content proposal의 legacy source 편집 대상을 억지로 확장하지 않는다.
Stage 3은 검증과 읽기만 구현하고, 참조 적용은 Stage 4~7에서 별도의
revision·before hash 검사 및 명시적 적용 경로로 제공한다.

## 공통 규칙

- root 필드: `schema_version`, `topic_id`, `revision`, `evidence`, `knowledge`,
  `relations`, `conflicts`, `learning_path`, `grading_links`, `score_effect`.
- `schema_version`은 `topic-learning-synthesis-v1`, revision은 1 이상의 정수,
  `score_effect`는 `none`이다. 알 수 없는 필드는 거부한다.
- 내부 ID는 비어 있지 않은 ASCII 영문·숫자·밑줄·하이픈 문자열이다.
  외부에서 참조할 때 `(topic_id, ID)`로 식별한다.
- ID는 내용의 동일성을 나타낸다. 문구 수정 시 ID를 유지하고 revision을
  올린다. 의미가 다른 개념으로 교체하면 새 ID를 부여한다.
- 이 v1은 Topic 내부 관계를 지원한다. Topic 간 선수지식 연결은 후속 확장이다.
- review 객체는 `status`, `reviewed_by`, `reviewed_at`, `note`를 가진다.
  status는 `draft`, `llm_reviewed_human_pending`, `human_verified`, `rejected`다.
  draft에서는 검토자·시각을 null로 허용한다. 나머지는 검토자 ID와 timezone이
  포함된 시각이 필요하다. LLM이 human_verified로 자기 승인하지 않는다.
- 출처 연결 승인 상태는 기존 Master가 소유한다. knowledge와 learning_path,
  grading_links의 review는 각각 지식·교육 구성·매핑 검토로 별도 관리한다.
  매핑 검토가 기존 채점 규칙 승인 절차를 대체하지 않는다.

## 출처 근거: evidence[]

필드: `evidence_id`, `source_id`, `source_url`, `source_version`,
`source_content_sha256`, `locator`, `excerpt`.

기존 WordPress claim의 evidence 의미를 재사용한다. source_version은 기존
Master와 호환되도록 문자열 또는 정수이며 타입을 포함해 정확히 비교한다.
해시는 정규화하지 않은 추출 텍스트를 UTF-8로 인코딩한 SHA-256이다.
URL은 정확한 asset URL이며 Master에 없으면 wordpress_url로 비교한다.
excerpt는 그 추출 텍스트의 실제 부분 문자열이어야 한다.

구조 검증과 자료 확인을 구분한다. 파일 형식만 맞으면 구조 검증은 통과할 수
있지만 자료를 확인할 수 없으면 verified라고 표시하지 않는다. 로더는 원본을
변경하지 않고 `matching`, `stale`, `unavailable` 확인 결과를 별도 반환한다.
연결되지 않은 출처는 오류다. stale/unavailable 근거에 의존하는 설명은
일반 학습 본문에서 제외하고 검토 화면에 이유와 함께 보존한다.

## 지식: knowledge[]와 relations[]

knowledge 필드: `knowledge_id`, `kind`, `title`, `statement`, `conditions`,
`units`, `exceptions`, `evidence_ids`, `origin`, `review`.

kind는 `concept`, `formula`, `condition`, `application`, `boundary`다.
origin은 `source_excerpt`, `synthesis`, `authored`로 나눈다. source_excerpt는
인용과 일치해야 하고, synthesis는 근거를 종합한 설명임을 표시한다.
authored는 연결 설명·예제 등 작성자가 추가한 내용으로 표시한다.
모든 항목은 적어도 하나의 evidence를 참조한다. 출처가 설명 전체를 직접
주장한다고 간주하지 않으며 origin과 review를 함께 보여준다.

relation 필드: `relation_id`, `from_id`, `to_id`, `kind`, `explanation`,
`evidence_ids`, `review`. kind는 `prerequisite`, `derives_from`, `contrasts_with`,
`applies_to`다. 양 끝 knowledge ID가 존재해야 한다. prerequisite는
from이 to의 선수지식이라는 뜻이며 자기 참조와 순환을 금지한다.
다른 관계에 동일한 순서 제약을 강제하지 않는다.

## 충돌: conflicts[]

필드: `conflict_id`, `knowledge_ids`, `evidence_ids`, `description`, `status`,
`resolution`, `review`. status는 `unresolved`, `resolved`다.
서로 다른 주장을 하는 근거를 최소 2개 연결하고 적용 조건을 포함해 설명한다.
unresolved에서는 resolution이 null이며 관련 지식을 검토 대상으로 표시한다.
resolved는 해결 이유와 human_verified review가 필요하다. 원래 근거는 삭제하지 않는다.

## 학습 구성: learning_path

필드: `path_id`, `title`, `objectives`, `sections`, `review`.
sections는 순서가 있는 배열이며 각 절은 `section_id`, `kind`, `title`,
`knowledge_ids`, `body`, `origin`, `evidence_ids`, `material_ids`, `self_check`를 가진다.
kind는 `prerequisite`, `concept`, `derivation`, `worked_example`, `application`,
`boundary`, `self_check`다. 자료가 없는 단계를 빈 설명으로 채우지 않는다.
학습 목표와 적어도 하나의 절은 필요하다.

material_ids는 기존 `topic-learning-material-v1`의 같은 Topic 자료를 참조한다.
self_check는 `{question, answer}` 배열이다. body가 작성자의 설명이면 origin을
authored 또는 synthesis로 표시한다. 모든 절은 적어도 하나의 knowledge를
참조하고, 별도 인용이 있다면 evidence_ids를 추가한다.

prerequisite로 연결된 지식은 학습 경로에서 처음 소개되는 위치가 선행해야 한다.
같은 절에서 둘 다 소개하는 경우 허용하되 설명 순서는 구성 검토에서 확인한다.
모든 지식이 한 경로에 반드시 등장할 필요는 없다. unresolved/rejected 또는
자료 불일치 항목이 있으면 해당 절을 검토 대상으로 분리한다. LLM 검토만
완료한 설명은 그 상태를 표시하며 정답 확정 자료라고 표시하지 않는다.

## 평가 연결: grading_links[]

필드: `link_id`, `target`, `knowledge_ids`, `section_ids`, `review`.
target은 `source_key`, `record_id`, `source_content_sha256`이다. source_key는
기존 `fact_anchor`, `logic_check`, `model_answer`, `topic_importance`,
`question_demand_axes` 중 하나다. 해시는 해당 canonical source 파일 바이트다.
source별 기존 ID 규칙으로 record를 찾고 유일성을 검사한다. 안정적인 ID가
없는 source 항목은 추측으로 연결하지 않고 미지원 대상으로 보고한다.

이 연결은 평가 기준을 생성하거나 점수를 계산하지 않는다. 기존 Grading
Projection은 동일한 payload를 반환해야 한다. Feedback은 확정 결과에 정확한
source/record ID가 있을 때만 대응 학습 절을 안내한다. ID가 없으면 Topic
수준 안내로 fallback하고 문장 유사도로 임의 매핑하지 않는다.
학습 순서·분량·모든 학습 항목을 문제의 필수 채점 기준으로 사용하지 않는다.

## 소비·변경·검증 계약

Training은 기존 v1 필드를 유지하면서 검증된 `learning_synthesis` 결과를
선택적으로 제공한다. 새 참조가 없으면 기존 동작을 유지한다. 자료 손상은
명시적으로 보고하고 새 보조 자료만 사용할 수 없도록 한다. /review의 기존
문제 선택 및 확정 채점 결과 저장이 자료 오류 때문에 중단되지 않아야 한다.

Feedback은 학습 절 ID와 제목·출처 참조를 제공한다. 개인별 진단과 진행 상태는
History에만 저장하며 당시 Master/synthesis revision을 함께 기록한다.

변경 제안은 기준 Master revision과 대상 파일 before hash, 새 후보 파일 해시,
영향 knowledge/section/target 목록을 고정한다. source 변경으로 새 파일을
읽었다고 기존 검토 상태를 그대로 물려주지 않는다. 구조 검증과 검토 승인 후
명시적으로 적용한다. 채점 내용 변경은 기존 content proposal/release 절차다.

Stage 3 필수 검증: schema와 Python validator 일치, 중복·끊어진 참조,
다중 출처, 원문 인용·해시·URL 불일치, 선수관계 순환과 순서, conflict 상태,
잘못된 canonical target, 기존 학습자료 재사용, v1 fallback, 반환값 격리,
Training 수정 전후 Grading payload 동일성. synthetic fixture로 먼저 검증한다.
