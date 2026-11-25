# P2-B3–B5 Claim–Fact 관계 인식 개선 기록

## 범위와 판정 한계

이 작업은 P2-B1/B2 기술 검토 메모를 반영해 비채점 Claim–Fact 감사 경로를 보완했다. Fact Anchor 정본, Registry, Topic Pack, Generated 데이터 및 채점 기준은 수정하지 않았다. 시험 문구의 기대값은 개발자가 마련한 기술 검토 결과이며 독립 전문가 라벨이 아니다. 따라서 아래 실행은 구현 동작과 fail-closed 위험을 확인한 것이며 의미 정확도, precision 또는 recall을 확정하지 않는다.

`score_admission=DISABLED`, `score_effect=none`을 유지한다.

## 구현한 변경

- 기존 `does_not_guarantee` 술어 자체의 부정 의미와 표면 Claim의 극성을 분리했다. “MC/DC가 SIL을 보장한다”와 “보장하지 않는다”의 표면 극성이 뒤집히지 않도록 했다.
- 기존 `distinct_from` 관계에서 “같지 않다/구분되지 않는다” 표현의 이중 부정 처리를 보완했다.
- 기존 `derived_by_ratio`에서 분자·분모의 순서와 비율 목적어를 원문 span에 결속했다. `residual frequency / tolerable frequency` 순서가 원문 근거에 있을 때만 관계 후보를 구성한다.
- ASCII/Unicode slash 및 띄어쓰기 alias 변형을 기존 용어 alias 처리에서 인식하도록 했다.
- 문장 간 주어 상속은 명시적 정정의 인접 문맥에 제한했다. 같은 관계의 기존 주장을 명시적으로 거부하고 정정한 경우에만 앞 문장의 주어를 이어받는다.
- 조건부 관계는 필수 조건의 원문 근거가 관계 주어보다 앞에 있고 Claim 조건으로 추출된 경우에만 감사기가 확정한다. 근거가 없거나 귀속이 불명확하면 보류한다.
- `condition_other` 구조화 Claim의 조건이 답안 원문에 근거하지 않으면 `RECOGNITION_UNCERTAIN`으로 둔다.
- 진단 runner는 JSON 사례 파일 입력을 지원하고 execution error가 있으면 비정상 종료한다.

바뀐 파일은 추출기, 기존 ontology alias 데이터, 비채점 관계 감사기, 그 runner, 관련 테스트 및 P2 연구 산출물이다. 새로운 Claim schema, predicate ID, Topic Pack 관계 또는 운영 채점 경로는 만들지 않았다.

## RRF 검토 처분

관계는 `RRF_required = F_residual / F_tolerable`이다. 정의형 답안에서 같은 위험 결과와 시간 기준을 반복하지 않은 것은 그 자체로 관계 오류가 아니다. 따라서 `hazop_lopa_required_rrf/condition_omitted`의 구조화 및 자연어 기대를 별도 수정 fixture에서 `CONFIRMED_RELATION`으로 기록했고, 원본 111개 fixture는 변경하지 않았다.

`condition_other`는 답안 문장이 동일 시나리오와 시간 기준을 말하는 반면 구조화 Claim이 원문에 없는 `different_condition`을 넣는다. 자연어 관계와 Claim 근거 정합성을 분리하고, 이 Claim은 근거 불일치로 `RECOGNITION_UNCERTAIN` 처리했다. 이는 답안 자체를 오답으로 판정한 결과가 아니다.

새로운 제한적인 반례에는 분자·분모 반전, 잘못된 RRF 관계, 조건 귀속 불일치가 포함된다. 현재 Machine Fact가 직접 표현하지 않는 위험(예: 서로 다른 위험 결과의 비교나 시간 단위 환산 오류)은 같은 관계 모순으로 추정하지 않고 미지원/보류로 남긴다.

## 결과 요약

| 집합 | 건수 | 관측 일치 | 해석 |
|---|---:|---:|---|
| 원본 111, 기존 B3 이전 기록 | 111 | 83 (56/64 구조화, 27/47 자연어) | SHA `57197b6` 기준 역사적 결과 |
| 변경되지 않은 원본 111 재생 | 111 | 95 (57/64, 38/47) | 현재 B3 작업 트리 결과. 원본 입력은 동일 |
| 기술 검토 반영 별도 fixture | 111 | 97 (58/64, 39/47) | 원본 대비 +2 추가 일치 |
| 새 개발 일반화 probe | 36 | 17/36 provisional labels | 34 uncertain, 1 contradiction, 1 relation. 정확도 지표 아님 |

모든 runner 실행에서 `EXECUTION_ERROR=0`이었다. 원본 입력 111건 기준 B3 작업 트리의 정확 일치는 직전의 역사적 83/111에서 95/111로 늘었다. 다만 원본/별도 검토 fixture를 사용한 수치이며 전문가 평가가 아니다. 기술 검토 반영 fixture의 97/111 중 구조화 mixed 6건은 기존 관계 비교기가 명시적 모순을 내는 동작과 새 참조 정책 사이의 차이로 남겼다. 이를 evaluator 오류로 세지 않았고 기존 WRONG 우선 동작을 바꾸지 않았다.

기술 검토 fixture의 자연어 기대 관계 16건 중 일부 표현은 인식됐고, 8개 paraphrase/formula 관계가 여전히 `RECOGNITION_UNCERTAIN`이다. 사례별 목록은 `p2b_remaining_mismatch_analysis_20261125.json`에 기록했다. 새 36건 probe에서도 19개 provisional 관계/모순 기대는 보류됐다. 잘못된 SUPPORT를 줄이는 fail-closed 동작은 유지됐지만 표현 일반화가 충분하다는 증거는 아니다.

## 검증 자료와 해시

- 원본 111 input: `p2b_relation_cases_20261125.json`, SHA-256 `bf75899e302c5cb9736332fe230a914d0cd0d57d09c8d59e6328910267e60ee9`
- 수정 111 input: `p2b_revised_relation_cases_20261125.json`, SHA-256 `bb605893aa7d16b13a58bc6b8ac18454302d3a7cd51a4a3cea2de56edea6db34`
- 일반화 36 input: `p2b_generalization_cases_20261125.json`, SHA-256 `098c6e4e1819bc7c332babf166b41764b3dd9b2dd26084a19152b7fae17cdb2c`
- 건별 실행, 결과 SHA, confusion 및 실행 오류: `p2b_recognition_improvement_results_20261125.json`
- 사례별 처분: `p2b_technical_case_dispositions_20261125.json`
- 잔여 차이: `p2b_remaining_mismatch_analysis_20261125.json`

보호 답안 143건의 로컬 replay snapshot 2개는 비공개 `/tmp` 경로에 두었고 공개 저장소에는 답안 원문/근거 span을 복사하지 않았다. 두 파일은 각각 143행이며 SHA-256이 모두 `a2825370ef80f61b2d5c3fa55a765ad811f7a8401e6e8590a41e9d663ab16693`; 행 비교 결과 변경 0건, 필드 차이 0건이다. 실행 SHA 메타데이터가 snapshot 내부에 없으므로 이 결과의 정확한 코드 SHA 귀속은 제한적으로 기록한다.

## 남은 위험

- 8개 자연어 paraphrase/formula 관계가 미인식 상태다.
- 새 일반화 probe의 19개 관계/모순 기대가 보류된다. 이는 특정 입력을 추가 등록하는 식으로 해결하지 않았다.
- 조건 alias의 순서 기반 적용은 제한된 언어 패턴이다. 복합문, 장거리 조건 귀속, 다중 관계에서는 계속 보류할 수 있다.
- 구조화 mixed 6건은 기존 정책과 참조 정책이 다르다. 운영 정책은 변경하지 않았다.
- 독립 전문가 검토가 없으므로 실제 의미 정확도는 `NOT_ESTABLISHED`다.

## 상태

기능 수정 및 개발자 작성 회귀 실행은 완료했다. 그러나 자연어 일반화 범위가 제한되고 독립 검증이 없으므로 P2-B 완료 게이트는 통과하지 못했다. P2-B는 `PARTIAL_OR_UNRESOLVED`; 기존 workplan에 따라 P2-C 진입은 차단 상태다.
