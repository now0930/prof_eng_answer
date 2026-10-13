# Stage 6 실행 연결과 검증 경계

> 이 문서는 이전 3경로 탐색 실험의 이력이다. 2026-10-13 사용자 승인으로
> 3경로 비교 의무를 종료했다. 현재 목표와 완료 기준은
> [미해결 의미 보완 실행 로드맵](semantic_assist_roadmap.md)을 따른다.

## 2026-10-13 확인 결과

- 샌드박스 밖의 읽기 전용 Docker 접근은 성공했다. 기존 `prof_eng_answer_bot`에
  Gemini·Clova·Ollama 설정이 있다. 키 값은 조회·출력·복사하지 않았다.
- 기존 컨테이너의 Gemini로 `Reply OK` 요청을 보내 HTTP 200 및 응답 존재를 확인했다.
  따라서 이전의 “provider 설정이 없어 실행 불가능” 설명은 정정한다.
- 사용자가 3개 사례 전송을 승인한 뒤 Gemini 요청을 실행했다. 최소 연결 검사는 HTTP 200이었다.
- `extract_fact_shadow_candidates.py`는 누락되어 있던 의미 후보 생성 경로다.
  운영 채점기, generated bank, 승인 상태는 변경하지 않는다.

## 후보 생성

외부 Gemini 전송 승인 후 저장소 루트에서 실행한다. 기존 컨테이너 환경의 키를
사용하며 키를 호스트나 파일로 가져오지 않는다. 사례별 출력 파일은 새 경로여야 한다.

```bash
python3 scripts/extract_fact_shadow_candidates.py \
  --case-id risk_nyquist_normal_01 \
  --output /tmp/stage6_nyquist_candidates.json
```

같은 방법으로 `sil_target_operations_issue1`, `mcdc_vmodel_sil_issue1`을 실행한다.
SIL은 Golden에 대응하는 원답안이며, V-Model은 연관된 세 Topic의 Fact를 함께 사용한다.
사용자 자료는 `--input private.json`으로 전달한다. JSON 필드는 `question`, `answer`,
`topic_ids`만 허용한다. 기준 정답 라벨은 모델 입력에 포함하지 않는다.

질문 요구 추출과 답안 주장 추출은 별도 요청이다. 질문 추출 요청에는 답안이 없다.
모델에는 원문과 해당 Topic의 승인 Fact 문장·관계가 전송된다. 반환된 인용문은
원문 내 유일한 일치 구간으로만 연결한다. 중복·없는 인용, 계약 외 필드 및 점수 권한은
거부한다. 추출 실패는 실패로 기록하며 빈 성공 결과로 바꾸지 않는다.

출력은 권한 0600인 비공개 JSON이며 원문 인용과 모델 응답을 포함한다.
공개 커밋 금지. 요청·질문·답안·Fact hash, 모델명, token 사용량, 지연 시간을 기록한다.
금액은 가격 근거가 없으므로 추정하지 않는다. `ok`는 provider 응답과 후보 형식 검증
성공만 의미하고, 답안 전체 추출 완료를 보증하지 않는다. 항상
`independently_verified=false`, `stage6_complete=false`, `score_effect=none`이다.

## 승인 후 탐색 실행 결과

초기 요청에서 SIL은 빈 후보를 반환했고, V-Model의 복합 한국어 작업구문은 task enum
불일치로 거부됐다. 프롬프트와 task 정규화를 보완한 뒤 V-Model 및 Nyquist 후보 형식은
통과했다. SIL은 세 번째 요청에서 질문 후보 1건만 통과했고 답안 후보는 0건이었다.
V-Model·Nyquist 답안도 일부 후보만 반환됐다. 각 재시도 사이 프롬프트/정규화 코드가
변경됐으므로 이 결과를 동일 조건의 3사례 집계로 취급하지 않는다. 후보는 모두
`independently_verified=false`다.

이 실행은 Gemini 전송·응답 처리·일부 원문 span 검증 경로만 확인했다. 세 경로의 같은
revision 결과, 독립 Fact ID 기준 라벨, Fact 일치율, 답안 추출 완전성은 산출하지 못했다.
따라서 Stage 6은 진행 중이며 PASS가 아니다.

마지막 동일 코드 revision 실행에서 provider 요청은 세 사례 모두 응답했지만 구조적으로
성공한 전체 묶음은 Nyquist 1/3뿐이었다. 질문 후보 출력은 SIL 빈 목록, V-Model 1건,
Nyquist 1건이었다. 답안 후보 출력은 SIL 7건, V-Model 빈 목록, Nyquist 2건이었다.
SIL·V-Model은 적어도 한 쪽 요청이 유효하지 않아 묶음 실패다. 인용 span·schema만
확인한 수치이며 의미상 Fact 일치율이 아니다.

기존 3인 LLM 채점 경로도 같은 checkout revision에서 세 fixture로 실행했다. Snapshot의
`engine_commit`은 `bc375b02c7e51a5eba28971e24ccf3bcb62409ee`, evaluator SHA는
`9f448ffc761702169a54ec57fd81479e80bafdf15cf9366c695ec8f7013dfe2d`로 세 실행이 같다.

| 사례 | 결정론 점수 | 기존 LLM 점수 | LLM−결정론 | 의미 후보 경로 |
|---|---:|---:|---:|---|
| SIL target | 7.61 | 19.00 | +11.39 | 묶음 실패: 질문 후보 빈 목록, 답안 후보 7건 |
| V-Model/SIL | 6.20 | 19.00 | +12.80 | 묶음 실패: 질문 후보 1건, 답안 후보 빈 목록 |
| Nyquist 정상 답안 | 11.83 | 18.00 | +6.17 | 구조 통과: 질문 1건, 답안 2건 |

이 점수차는 정확도 판정이 아니다. Gemini 후보 검증 완료는 0건이고, 독립 기준 Fact ID/span
라벨도 없다. 비교 가능한 3경로 사례는 `0/3`이다. SIL 후보를 에이전트가 대조한 결과
`R_max` 문장을 위험수용 정책 Fact로, 곱셈형 `PFD_avg` 문장을 비율 경계 Fact로 투영한
의미 불일치를 확인했다. 이를 바탕으로 LLM 또는 결정론 점수 어느 쪽이 과대/과소인지
확정하지 않는다. 승인된 후보 검증기와 기준 라벨이 있어야 판정할 수 있다.

동일 revision의 후보 추출 6회 중 schema/span 검증 성공은 4회, 전체 사용량은 31,522
tokens, 요청 합산 지연은 10.127초였다. 이는 후보 추출만의 측정이며 경로 비용 평균이나
금액 추정에 사용하지 않는다. 같은 Nyquist 사례의 별도 LLM 반복은 13.0점과 18.0점으로
달라 단일 실행 수치의 변동성도 확인됐다. 이는 지정된 재현성 gate를 수행했다는 뜻은 아니다.

추가 한계: 위 기존 LLM 실행에는 `phase2 skipped: session_dir not found`가 기록됐다.
따라서 표의 LLM 점수는 기본 3인 채점 경로 결과이며 전체 운영 후처리를 완료한 Gemini
채점 결과가 아니다. 전체 운영 경로와의 정확도 비교 자료로 사용할 수 없다.

## 과거 비교 계획의 미완료 항목 (현재 완료 조건에서 제외)

1. 답안을 보지 않고 질문 scope와 요구 Fact를 독립 검토한다.
2. 후보 생성 출력과 분리된 기준 Fact ID 및 원문 span 라벨을 확정한다.
3. 모델 후보의 관계·부정·조건·인용 해석을 독립 검증한다. 후보를 그대로 승인 ID로
   복사하거나 다른 LLM의 동의를 결정론적 증명으로 간주하지 않는다.
4. 같은 코드·입력·지식 snapshot에서 규칙 전용, 의미 보조 shadow, 기존 LLM 경로를
   실행한다. 의미 보조 경로의 점수 정책이 미승인인 동안 점수는 N/A로 기록한다.
5. 전체 및 비교 가능한 사례 수, 보류율, Fact 일치율, 기존 두 채점 경로의 점수 차이,
   token·지연을 보고한다. 재사용 회귀 사례의 pilot과 독립 holdout 평가는 구분한다.

현재 compiler는 semantic 요구 후보를 자동 resolved로 승격하지 않는다. 이는 승인 경계이며
provider 연결을 고쳤다는 이유로 완화하지 않는다. 위 절차와 Stage 6 기준이 충족되기 전에는
3경로 평가 완료나 운영 승격을 선언하지 않는다.
