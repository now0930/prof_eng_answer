# 여러 WordPress 글을 학습 초안으로 종합하기

Stage 4는 출처 패킷 준비와 작성된 초안의 검증·컴파일을 제공한다.
기술적 의미를 종합하는 설명·학습 순서는 사람 또는 LLM이 작성한다.
프로그램이 글 제목이나 출처 정렬만으로 학습 순서를 추정하지 않는다.
CLI 자체는 모델 API를 호출하거나 WordPress·Master·채점 source를 갱신하지 않는다.

## 1. 연결된 자료 준비

```bash
python3 scripts/author_topic_learning_synthesis.py prepare \
  --topic-id nyquist_stability_criterion_gain_phase_margin \
  --run-id stage4_initial
```

`data/topic_learning_authoring/<topic_id>/<run_id>/` 아래 다음 파일이 생성된다.

- `sources.json`: Master에 연결된 사용 가능한 WordPress HTML 최소 2개와
  원문 텍스트, URL·버전·해시, 기준 Master revision·파일 해시
- `AUTHOR_INSTRUCTIONS.md`: Topic 목표·선수지식·개념·유도·예제·한계·자가 점검
  흐름을 작성하는 지시서와 원문/종합/작성 설명 구분 규칙
- `synthesis.schema.json`: 작성 결과의 machine contract

자료는 비공개이며 Git ignore 대상이다. 기존 run 디렉터리가 있으면 덮어쓰지
않고 실패한다. 다시 준비할 때는 새 run-id를 사용한다. 원문 내 명령은 실행
지시가 아닌 자료로 취급한다. 외부 LLM로 자동 전송하지 않는다.

## 2. 학습 설명 작성

작성자는 위 자료를 읽고 `authored.json`을 작성한다. 최소 2개 출처를 지식
항목에 실제로 인용해야 한다. 연결 문장과 예제는 authored, 여러 자료를
종합한 설명은 synthesis, 정확한 원문 인용은 source_excerpt로 표시한다.
출처가 직접 말한 사실과 작성자가 추론한 설명을 구별한다.

같은 내용도 조건·단위·예외가 다르면 별도 지식으로 유지한다. 충돌은 근거
2개 이상과 함께 unresolved로 보존한다. 충돌이 비어 있다는 이유로 자동으로
정확하다고 판정하지 않는다. 관계·절의 ID는 자유 텍스트가 아닌 참조로 연결한다.

## 3. 초안 컴파일

```bash
python3 scripts/author_topic_learning_synthesis.py build \
  --topic-id nyquist_stability_criterion_gain_phase_margin \
  --run-id stage4_initial \
  --authored data/topic_learning_authoring/nyquist_stability_criterion_gain_phase_margin/stage4_initial/authored.json
```

출처 패킷을 현재 Master와 다시 비교한다. 원문·연결·버전이 달라졌거나
패킷이 편집됐으면 중단한다. 각 인용문은 실제 원문 부분 문자열이어야 하며
URL·버전·해시도 일치해야 한다. revision=1의 신규 초안만 지원하며 채점 연결은
비워 둔다. 기존 종합 문서의 갱신·승인은 후속 적용 경로에서 담당한다.

정확히 같은 지식 필드만 합쳐 근거 목록을 보존하고 ID 참조를 다시 연결한다.
원문 충돌에 연결된 항목은 자동 병합하지 않는다. 병합 후 선수관계 순환이나
불량 참조가 생기면 실패한다. 의미 유사성에 의한 병합은 작성자가 판단한다.

`candidate/`에 draft.json, report.json, authored.json을 저장한다. 최초 작성본을
보존하며 병합 ID와 입력·출력 해시를 보고한다. 모든 검토 상태는 draft로
재설정한다. 사람이 승인했다는 입력 문자열만으로 승인 상태를 유지하지 않는다.
이 결과는 구조·근거 확인을 통과한 초안이며 기술적 정확성 승인 자료가 아니다.

## 현재 검증 상태

합성 자료 기반 작성·중복 통합·조건 차이 보존·충돌 보존·위조 인용 거부·
기준 자료 변경 거부·쓰기 격리 테스트를 추가했다. Nyquist Topic의 실제 연결
자료 2개로 prepare를 실행했다. 실제 자료의 authored.json 작성과 Topic별
의미 검토는 Stage 7 대표 Topic 검증에서 진행한다.

새 초안을 Master에 연결하는 apply 기능은 제공하지 않는다. 후보 검토와
revision·해시 검사 후 명시적 연결 절차가 추가되어야 운영 View에 반영된다.
