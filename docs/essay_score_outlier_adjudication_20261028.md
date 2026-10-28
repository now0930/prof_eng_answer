# 15점 하한 제거 감사 — 범위 밖 8건

이 문서는 2026-10-28의 `expert_accuracy_golden.jsonl` 48건과 실제 fixture를
대조한 작업 기록이다. 사용자 승인 Golden 라벨은 변경하지 않았다. `reviewed`는
개별 점수의 독립적인 인간 재채점이 끝났다는 의미로 확대 해석하지 않는다.

| 사례 | 하한 제거 점수 / 허용 범위 | 주원인 | 이번 조치 / 남은 확인 |
| --- | ---: | --- | --- |
| `sil_target_operations_issue1` | 7.61 / 10–14.5 | 검증된 치명 오류 4건, 부분 근거와 운영 문장의 낮은 포착. 현재 점수와 허용 범위 하한의 차이는 사실 오류를 지워서 해결할 문제가 아니다. | Fatal 판정 유지. 이 답안에 10점 이상을 보장해야 하는지 독립 채점 필요. |
| `sis_lopa_architecture_issue1` | 7.84 / 9.5–13 | PFD와 고장률 비교 오류가 Fatal. 맞는 RRF 관계와 일부 아키텍처는 포착됐지만 여러 요구가 누락으로 판정됨. | Fatal 유지. 해당 부분 점수와 허용 범위의 독립 재판정 필요. |
| `mcdc_vmodel_sil_issue1` | 6.2 / 10.5–14.5 | MISRA·HFT·MC/DC·소프트웨어 무결성의 핵심 오류 4건. 구조 3점 외 정답 근거가 제한됨. | Fatal 유지. 현재 범위 하한을 기계적으로 맞추지 않음. |
| `qtype_qg-da-high-01` | 15.38 / 20–25 | 답안은 진단→조치→검증을 충분히 제시하나, 명시 계약에 질문과 직접 관계가 약한 `stiction_limit_cycle_path`·`oscillation_requires_differential_diagnosis`가 있고 증거 span도 엉뚱한 문장에 걸림. | Topic의 질문별 요구 ID와 근거 추출을 검토 제안. Pack 승인 전 운영 변경 금지. |
| `qtype_qg-ie-high-01` | 14.88 / 20–25 | 일치하는 질문 계약이 없어 `derived_question_contract`가 네 Anchor만 고르고, 그중 `sw06_sw04_boundary`는 질문 요구와 다름. | 질문별 계약 추가 제안. Pack 승인 전 운영 변경 금지. |
| `risk_nyquist_normal_01` | 11.83 / 14–19 | 질문은 임계점과 P·N·Z 관계만 요구하지만 더 넓은 ‘원리와 판별 절차’ 계약의 7개 Anchor를 적용. | 질문 범위 축소 계약 제안. 짧은 답안의 14점 하한은 별도 검토. |
| `risk_lead_lag_normal_01` | 12.5 / 15–19 | 질문은 진상·지상 설계인데 ‘결합보상기 상충관계’ 계약 4개 Anchor가 선택됨. | 질문별 계약 제안 및 15점 하한 재판정. |
| `risk_lqr_normal_01` | 12.5 / 14–19 | Q/R·Riccati는 포착되나 ‘단위 정규화와 포화 한계를 포함한 반복 조정’이라는 두 설계 제약을 D축이 0점 처리. | 서로 다른 두 설계 제약을 D축에 반영하도록 보완. 하한 없이 15.0으로 범위 진입. |

## 추가로 발견한 교차사례 결함

`evaluate_score_evidence`는 요구 근거 span이 한 개라도 있으면 D/E를 답안 **전체**에서
찾는다. 무관한 문단의 현장·시험·연결 표현도 점수화될 수 있다. 근거 span만
사용하는 엄격한 방식으로 시험하자 48건 중 범위 일치율은 0.666667으로
하락하고 범위 밖 사례가 16건이 됐다. 이는 과거 점수가 일부 답안 전체의
우연한 표현에 기대고 있었다는 신호다. 근거 span 추출 품질과 질문 계약을
보강하기 전에는 엄격한 방식을 운영 기본값으로 승격하지 않는다.

## 승인·출시 경계

- 기존 Golden과 release 기준 `0.85`는 유지한다. 점수 맞추기 위해 라벨이나
  gate 수치를 변경하지 않는다.
- 15점 하한은 기본 정책에서 제거한다. `ESSAY_LEGACY_15_FLOOR=1`은 이전
  결과 재현용이며 운영 컨테이너에는 설정하지 않는다.
- `ESSAY_STRICT_EVIDENCE_BINDING=1`은 비교 실험 전용이다. 근거 span 품질과
  질문 계약이 보강되기 전에는 운영 컨테이너에 설정하지 않는다.
- Topic Pack 변경은 `docs/topic_pack_workflow.md`의 사람 검토·승인/hash 절차를
  거쳐야 한다. 이 문서는 제안이지 승인 기록이 아니다.
- 하한 제거만의 점수 범위 일치율은 `0.854167`(41/48), 기준 `0.85` 통과다.
  기존 정책과 엄격 결합 정책의 일치율은 각각 `0.875`와 `0.666667`이다.
  치명 오류 3건과 질문 계약 불일치 4건은 여전히 허용 범위 밖이다.
- 남은 별도 과제: 질문별 범위 검토 → 근거 span 회귀 → 범위 밖 7건의 독립
  재판정 → 하한 제거·엄격 결합 **동시** 정책의 release gate 통과.

## 적용 검증

- 하한 제거를 기본값으로 바꾼 뒤 `test_deterministic_score_evidence.py`,
  `test_deterministic_score_engine.py`, `test_chapter22_dp_laminar_grading.py`
  23건 통과. 전문가 재현 감사 5건과 운영 진입점 집중 테스트 14건 통과.
- `python3 scripts/rubric_manager.py validate-all`: `ALL VALID`.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh`: 종료 코드 0.
- 전용 10회 채점 재현성 검사는 opt-in이라 실행하지 않았다.
