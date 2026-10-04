# Master → 채점·학습·피드백 View

## 구조와 권한

```text
WordPress 원문·HTML·PDF·이미지 (비공개 수집 자료)
    │ 출처 연결 / 변경 제안 → 승인 후 참조 갱신
    ↓
Master Topic Pack (topic_id, revision, 출처·버전, 콘텐츠 참조)
    ├── 채점 View → 기존 Grader → 확정 점수
    ├── 학습 View → 학습 자료·문제·원문·검토 주석
    └── 피드백 View + 확정 채점 결과 → 부족점·복습 안내
                                      ↓
                           별도 학습 이력 → Review Queue → 재작성
```

Master는 모든 본문을 중복 저장하는 파일이 아니라 Topic 단위의 참조·버전
관리 중심이다. 기존 Topic Pack은 승인된 채점 기준의 권한을 유지한다.
WordPress 원문은 학습 참고자료이며, 연결만으로 채점 사실이 되지 않는다.
검토 주석은 원문과 분리하고 미확정 상태로 유지한다. 이번 구조 정리는
원문 수정, 기술적 검토 승인, 전체 Topic 재작성 작업을 포함하지 않는다.

## 코드의 공통 진입점

`study/topic_views.py`를 새 소비자의 공개 읽기 인터페이스로 사용한다.

| View 함수 | 제공 데이터 | 소비자 / 권한 |
|---|---|---|
| `grading_view(root, master)` | 기존 채점 소스 호환 projection | 기존 Grader와의 호환 경계. 새 채점 엔진 아님 |
| `training_view(root, master)` | 문제·목차·기존 사실·출처 원문·학습자료·주석 | 학습·복습 화면, 점수 변경 없음 |
| `feedback_view(root, master)` | 진단 차원·기존 검사 참조·보완점·추천자료·주석 | 확정 점수 이후 피드백, `score_effect: none` |

세 함수는 필요한 View만 독립적으로 생성한다. 모든 View를 한꺼번에
만드는 필수 로더를 두지 않아 학습 원문 오류가 채점 View를 막지 않는다.
반환값 수정은 Master나 원문을 갱신하는 수단이 아니다.

기존 `study/master_topic_pack.py`는 검증·projection 구현을 유지한다.
기존 `project_grading`, `project_training`, `project_diagnosis`도 호환된다.
피드백의 저장 계약은 `diagnosis-projection-v1`, Master 설정 키는
`projections.diagnosis`로 유지한다. 피드백이라는 사용자 용어를 맞추기
위해 기존 파일·DB를 일괄 rename하거나 별도 네 번째 View를 만들지 않는다.

## 실제 소비 경로와 한계

- `study/learning_runtime.py`는 공개 View 인터페이스를 통해 학습·피드백을
  읽는다. `feedback_from_view`가 확정 채점 결과와 피드백 View를 결합한다.
- 기존 Grader 실행 경로와 라우팅은 그대로다. 채점 View는 호환 projection이며
  전체 Grader가 Master 로더를 통해 실행되도록 전환한 것은 아니다.
- `review_material_for_topic`의 `wordpress_topic_pack` 반환은 기존 비공개
  자료 호환 필드다. 새 소비자는 Master 연결·버전 검사를 거친
  `training.source_materials`를 사용한다. 원시 bundle을 승인된 지식으로
  취급하지 않는다.
- `/review`는 `study/review_presentation.py`로 Training View의 원문 발췌와
  미확정 주석을 표시한다. 원시 OCR bundle은 표시 입력으로 사용하지 않는다.
  자료와 주석은 각각 최대 2건 요약하며 전체 원문은 변경하지 않는다.
  주석은 검토 대기·점수 영향 없음 및 현재/이전 원문 여부를 명시한다.
  저장된 피드백은 이전 채점 시점의 안내로 표시한다. 다른 화면의 확장은
  별도 작업이며 이 변경만으로 운영 중 프로세스가 자동 재시작되지는 않는다.
- 학습 이력, 확정 채점 결과, Queue는 사용자 상태이며 Master에 넣지 않는다.
  오래된 피드백은 당시 snapshot이고 최신 Master와 같다고 가정하지 않는다.

## 변경 흐름과 검증

출처 변경은 제안과 승인 과정을 거친다. 채점 기준 변경은 별도의 콘텐츠
검토·승인이 필요하다. 미확정 주석은 두 승인 절차를 대체하지 않는다.
출처 버전·URL·해시 불일치는 명시적 projection 오류로 처리하며, 기존
runtime의 보조 안내 실패 처리는 확정 점수 저장을 보호한다.

공개 진입점 테스트는 기존 projection과의 동일성, 독립 호출, 반환값 격리를
확인한다. 기존 릴리스 회귀 검증과 Topic release gate는 그대로 유지한다.
