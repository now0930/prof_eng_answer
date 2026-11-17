# S7 B7 — AI 작성 20개 연구 후보의 출처·구조 검증 및 격리 (2026-11-17)

## 기준과 목적

이전 독립 검토 준비 단계의 마지막 검증 실행은 [Actions #44007376507](https://github.com/now0930/prof_eng_answer/actions/runs/44007376507), HEAD `7409e045c6837b818cafc110b507679b896d06ab`, `1973 passed, 2 skipped`, `VALIDATION=PASS`. 해당 실행의 Source Review는 고유 Fact 119개 HOLD 및 179건 parser ID 누락, 채점 사용 DISABLED를 확인한다. 독립 인간 전문가 판정 건수는 0이다.

그 뒤 단일 AI가 두 관점으로 10개 작성자 초안을 점검하고, 5개 Fact × 4개 유형 = 20개의 추가 문장을 작성했다. 이는 별도 모델/전문가가 만든 독립 검증 데이터가 아니다. AI가 작성한 예시는 **자기출처 오염 위험이 있는 연구용 probe pool**일 뿐이다. 이 후보의 작성자 의도 유형을 정답 라벨로 취급하지 않는다.

## 실제 입력

- `s7_alias_source_review.json`: 기존 Actions #44007376507의 Registry source review (source SHA `7409e045...`, 119 HOLD)
- `calibration/s7_alias_negative_claim_challenge_v1.json`: 기존 작성자 초안 20쌍; 단지 원문 복사/출처 오염을 확인하는 기준
- **비공개** `ai_generated_holdout_candidates.json`: AI가 만든 20개 후보 (schema `s7_ai_authored_holdout_candidates.v1`, source SHA `7409e045...`). 이 파일에는 기술적 정답 인증이나 독립 라벨이 없다. GitHub/PR/Actions에 답안 원문을 업로드하지 않는다.

원본 5개 Fact의 실제 소스 조건 수는 각각 다음과 같다.

| Fact | 조건 ID 수 | AI 후보 유형에서 검토할 오류 |
|---|---:|---|
| `effective_unbalanced_area` | 2 | 실제 압력 작용면과 구조조건 누락 |
| `sw06_baseline_approved_reference` | 2 | 형상정보 식별, 공식 승인·합의 |
| `deadband_definition_direction_reversal` | 3 | 방향 반전/무응답 및 조립체·시험 조건 |
| `sw04_v_model_definition` | **0** | 조건 누락 유형 자체가 불가능 — 관계 설명 부족과 혼동 |
| `nyquist_contour_and_mapping` | 1 | 우반평면 안정도 분석 목적 |

**확정된 구조적 문제 1건:** `sw04_v_model_definition`의 AI 후보 case_no 3은 `omitted_conditions`라고 표기됐으나, 구조화된 Registry 소스 관계에는 조건 ID가 0개다. 이를 "필수 조건 누락" 정답 반례로 사용할 수 없다. `RELATION_UNDERSPECIFIED` 등 새로운 **제안 유형으로 사람이 재분류하거나 문장을 수정**해야 한다. 기존 Registry에 임의로 조건을 추가하여 문제를 해결해서는 안 된다.

다른 19건도 독립 기술검증을 통과한 것이 아니다. 단지 이 **특정 구조 충돌**이 발견되지 않았다는 뜻이다. 독립 전문가가 관계·필수 조건·인용 문맥·과도한 일반화 및 답안 자체의 기술적 타당성을 별도로 평가해야 한다.

## 구현 및 검증 게이트

- `grading/evidence/s7_ai_candidate_integrity_gate.py`: 정확한 5 × 4 후보 identity, AI 출처, 기존 119 HOLD 및 원본 Registry 관계·조건 8개, source SHA 일치 확인. 원문과 정확히 중복되는 문장, AI 후보 내부 중복, 원본 조건 수 0인데 조건 누락 유형으로 분류한 사례를 플래그 처리. **실제 뜻이나 진위 판정은 하지 않음**.
- `scripts/audit_s7_private_ai_candidates.py`: 수동 비공개 실행만 허용. source SHA는 원본 자료에 보존하며 새로운 commit의 HEAD로 바꿔치기하지 않는다. 결과 JSON에는 문장·소스 진술·검토자 정보 없이 ID/기술적 조건 개수/안전 상태만 기록.
- `tests/test_s7_ai_candidate_integrity_gate.py`: 20개 synthetic 예시, 0개 조건 구조 오류, 원문·후보 중복, 출처 위변조, Score 활성화/Fact Registry 관계 변경/검증 출처 누락 등 방어 시험.
- 기존 `validation.yml`에는 새 private CLI를 추가하지 않는다. 따라서 연구 Artifact 8개와 Grade 결과에는 변경이 없어야 한다.

원본의 AI 후보 JSON과 Source Review JSON을 **동일 SOURCE SHA**에 맞게 비공개 작업 디렉터리에 추출한 뒤 실행한다.

```bash
python3 -B scripts/audit_s7_private_ai_candidates.py \
  --source-review /private/s7_alias_source_review.json \
  --ai-candidates /private/ai_generated_holdout_candidates.json \
  --report /private/s7_ai_candidate_integrity_report.json
```

기대 보고: 후보 20개, 구성 유형 5/5/5/5, 검토 필요한 구조 불일치 최소 1개, 독립 검토 완료 0개, `independent_test_set_admission=PROHIBITED`, `score_admission=DISABLED`. 이 값은 **실제 입력을 읽어 확인하기 전에는 CI 성공으로 주장하지 않는다**.

## 다음 연구로 넘어가는 기준

1. 인간 검토자가 20건의 문장 원문을 사실·조건·범위 관점에서 각각 검증하며, 충돌 후보는 REWRITE/RETAG/REJECT/HOLD로 판정한다.
2. AI 작성 후보는 독립 모델 성능 평가의 홀드아웃으로 사용하지 않는다. 외부에서 신규 작성하거나 출처 분리된 사례를 별도로 수집한다.
3. 승인된 전문가 기준과 테스트 집합이 확보된 후에만, 운영 프로그램과 **별도 Research Shadow** 환경에서 입력 답안으로부터 Subject/Predicate/Object 및 조건을 실제 추출해 성능을 평가한다.
4. 향후 어느 단계도 Source의 Fact Anchor, Registry, Ontology, Topic Pack, canonical Claim parser, Golden, scoring rule을 자동 변경하지 않는다.

**보존:** 119 HOLD, B7/D2/D3 OPEN, `score_admission=DISABLED`, PR #38 Draft, main 병합·배포 금지.
