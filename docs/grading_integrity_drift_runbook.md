# Grading Integrity Drift Runbook

이 문서는 Issue #1에서 확인된 과대채점 유형이 다시 발생하지 않도록 보정 corpus와 의미 기반 drift gate를 운영하는 절차를 정의한다. 점수 숫자의 재현성만 확인하지 않고 `문제 경계 → Topic·요구축 → 기술관계 검증 → 최종 JSON → Telegram 표현`의 의미 계약을 함께 확인한다.

## 1. 운영 목표

다음 조건을 릴리스 불변조건으로 관리한다.

1. SIL 결정·플랜트 운영 문항은 전용 Topic과 정확한 8개 요구축을 사용한다.
2. 원본 오답의 `PFDavg = 빈도 × 빈도` 관계는 fatal로 검출한다.
3. 교정 답안의 올바른 빈도비 관계는 fatal로 검출하지 않는다.
4. HAZOP/LOPA, PST 최종요소, MC/DC 안전 소프트웨어 문항에는 Issue #1 전용 Topic이 누출되지 않는다.
5. fatal이 있으면 `strong`, full credit, 합격 허용과 `high confidence`가 최종 출력에서 다시 살아나지 않는다.
6. 요구사항 언급률과 정확 충족률을 별도 지표로 유지한다.

점수 `13.52` 자체는 기준선의 핵심 진실값이 아니다. provider 점수는 참고값으로 유지할 수 있지만, 판정 근거와 상태 플래그는 검증된 기술 오류에 종속되어야 한다.

## 2. Source of truth

| 역할 | 파일 |
|---|---|
| 의미 기준선과 이웃 주제 목록 | `calibration/grading_integrity_drift_baseline.json` |
| Issue #1 원본·교정 답안 | `calibration/sil_target_operations_overgrading_regression.json` |
| HAZOP/LOPA 이웃 회귀 | `calibration/sis_lopa_architecture_overgrading_regression.json` |
| MC/DC·V-Model 이웃 회귀 | `calibration/mcdc_vmodel_sil_overgrading_regression.json` |
| 일반 교차 주제 최소 다양성 | `calibration/general_grading_cross_topic_cases.json` |
| drift 실행기 | `scripts/check_grading_integrity_drift.py` |
| 실제 세션 경계 재현 | `scripts/replay_sil_issue1_session.py` |

## 3. 실행 방법

릴리스 전 기본 gate:

```bash
python3 -B scripts/check_grading_integrity_drift.py
python3 -B tests/test_grading_integrity_drift.py
python3 -B tests/test_sil_runtime_replay.py
```

정상 출력은 `status=PASS`와 기준선의 `semantic_sha256` 일치다. 상세 증적이 필요하면 tracked 디렉터리가 아닌 임시 위치에 보고서를 생성한다.

```bash
python3 -B scripts/check_grading_integrity_drift.py \
  --report /tmp/grading_integrity_drift_report.json
```

실제 컨테이너 parity는 세션 재현 스크립트를 같은 commit과 mount에서 실행하고 호스트의 `core_sha256`과 비교한다. 외부 LLM과 실제 Telegram 전송은 deterministic drift gate에 포함하지 않는다.

## 4. 실패 해석

| 실패 영역 | 주된 의미 | 우선 확인 |
|---|---|---|
| `routing` | 질문 정규화, activation 또는 Topic 요구축 변경 | `question_demand_axes.json`, `question_demand_contract.py` |
| `relations` | SIL 수식 탐지 규칙 또는 원본·교정 fixture 변화 | `sil_relation_integrity.py` |
| `output` | fatal cap, confidence 또는 Telegram 표현 회귀 | `verdict_consistency.py`, `bot.py`, `grade_output_summarizer.py` |
| `cross_topic_domains` | corpus 다양성 축소 | `general_grading_cross_topic_cases.json` |
| 해시만 불일치 | 관찰값의 순서·내용이 변경됨 | 상세 report를 이전 기준선과 비교 |

이웃 문항이 Issue #1 Topic으로 바뀌면 activation 범위를 넓히지 말고 충돌하는 문구와 소유 Topic을 먼저 식별한다. 단순히 expected hash를 교체해서 통과시키지 않는다.

## 5. 기준선 변경 절차

의도적인 정책 변경일 때만 다음 순서로 기준선을 갱신한다.

1. 원본 fixture는 보존하고 새 사례 또는 corrected variant를 추가한다.
2. 전문가가 Topic, 기술관계, 요구상태와 금지 문구를 검토한다.
3. `--show-current-fingerprint`로 현재 fingerprint를 확인한다.
4. 상세 report에서 모든 의미 변경을 검토한 뒤 `expected_semantic_sha256`을 갱신한다.
5. focused regression, 전체 release validation과 컨테이너 parity를 다시 실행한다.
6. 변경 사유와 전후 fingerprint를 PR 또는 Issue에 기록한다.

해시 갱신만 있는 변경은 허용하지 않는다. 기준선의 기대값 또는 새로운 fixture와 그 판단 근거가 함께 변경되어야 한다.

## 6. Corpus 확장 기준

새 사례는 다음 중 하나를 추가로 검증할 때 포함한다.

- 기존 오답을 정답으로 칭찬한 실운영 회귀
- 정답을 fatal로 오인한 false positive
- Topic 간 activation 충돌
- 문제·답안 경계 손실 또는 OCR 표기 변형
- provider가 만든 `strong`, full credit, confidence를 Python 최종 경계가 차단하지 못한 사례

각 사례에는 원본 질문과 답안, 기대 Topic, 검증 가능한 오류 ID, 허용·금지 최종 상태를 둔다. D/E의 표현 깊이처럼 전문가 판단 편차가 큰 항목은 결정론적 fatal 규칙으로 만들지 않는다.

## 7. 운영 주기와 향후 방향

- 매 commit: focused drift 및 session replay 테스트
- 배포 전: 전체 release validation
- 배포 후: 실제 컨테이너에서 네트워크 없는 replay parity
- 실채점 오판 발견 시: 익명화된 fixture를 즉시 추가
- 정기 검토: 주제별 false positive·false negative와 언급률/정확률 차이를 집계

다음 확장 우선순위는 SIL 외 고위험 수식 주제의 original/corrected 쌍, Topic별 최소 이웃 음성 사례, 전문가 이중검토 표본과 provider별 점수 분포 감시다. 결정론적 gate와 통계적 score calibration은 분리해서 운영한다.
