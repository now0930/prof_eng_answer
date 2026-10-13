# 운영 우선: 채점 품질 체크시트와 Topic별 수정 순서

갱신: 2026-10-13. 목적은 **현재 결정론적 채점 경로를 먼저 가동하고**, 확인된 문제를
세션별로 축적하면서 Topic Pack을 하나씩 보완하는 것이다. WordPress Fact와 LLM 제안은
자동으로 채점 권한을 얻지 않는다.

## 가동 범위

- 현재 브랜치의 실제 `grading_agents.run_agent_pipeline` 결정론 경로가 작동한다.
  세션에는 기존 `deterministic_grade.json`과 별도 `quality_checksheet.json`이 저장된다.
- 체크시트는 `score_effect=none`이고 질문·답안 원문을 복사하지 않는다. 권한 0600으로
  세션 폴더에 저장하며 `data/sessions/`는 Git에서 제외된다.
- 기존 운영 봇은 다른 체크아웃을 사용한다. 이 브랜치의 체크시트가 운영 봇에 적용됐다는
  뜻이 아니며, 운영 적용은 브랜치 병합·릴리스·배포 확인 후 별도로 수행한다.
- 미해결 의미 보조는 비공개 파일럿만 실행됐고, LLM의 동의는 점수에 반영하지 않는다.

## 자동 점검 항목

| check_id | 의미 | 실패/보류 시 최초 판단 |
|---|---|---|
| `score_authority` | 기존 점수 엔진과 출력 점수·LLM 권한 일치 | 시스템 결함 P0 |
| `fatal_verdict_consistency` | fatal이 있는데 합격으로 표시되지 않음 | 시스템 결함 P0 |
| `question_scope` | 기존 채점기의 명시적 질문 계약 선택 여부 | 요구·routing 점검 P1 |
| `evidence_recall` | 낮은 근거 회수 경고 없음 | 표현·Fact·Pack 대조 P1 |
| `unresolved_claims` | parser가 보류한 문장 없음 | 구절별 의미 검토 P2 |

`question_scope=pass`도 승인 Fact의 전체 범위가 확정됐다는 뜻은 아니다. 자동 점검
`pass`는 답안 사실 정확성의 증명이 아니다. 답안 내용이 부족하거나 기준 라벨이
틀렸을 수 있으므로, 전문가 점수 범위와의 차이는 `benchmark_conflict`로만 기록한다.
`false_low`/`false_high`는 답안·라벨·요구 범위를 독립 대조한 뒤에만 확정한다.

## 체크시트 생명주기

```text
open → triaged → fix_pending_retest → retested → closed
   ↘ deferred ↗                    ↘ triaged
```

수정 대기는 Pack·코드·라벨의 변경 참조가 있어야 한다. 자동 점검 항목의 재시험은 **다른
채점 snapshot에서 같은 check가 pass**일 때만 인정한다. 수동 문제는 새 snapshot과
수정 참조·담당자의 재시험 기록이 필요하다. `retested`는 특정 점검의 재실행 통과이지
모든 기술 사실의 독립 검증 완료가 아니다. 확정 점수 파일은 이 명령으로 수정할 수 없다.

## 사용

저장소 루트에서 승인된 과거 사례 세 건을 실제 결정론적 진입점으로 실행한다. 결과는
`data/sessions/quality_pilot_*`에 남는다. 재실행 때마다 새 세션을 만들므로 기존
검토 기록을 덮지 않는다.

```bash
python3 -B scripts/run_quality_pilot.py
python3 -B scripts/quality_checksheet.py list --sessions-root data/sessions
python3 -B scripts/quality_checksheet.py export --sessions-root data/sessions \
  --output /tmp/grading_quality_checksheet.csv
python3 -B scripts/quality_checksheet.py show --session data/sessions/<session_id>
python3 -B scripts/quality_checksheet.py add --session data/sessions/<session_id> \
  --category benchmark_conflict --priority P2 --note "답안과 기준 범위 재검토 필요"
python3 -B scripts/quality_checksheet.py advance --session data/sessions/<session_id> \
  --issue-id manual_001 --status triaged --note "답안·라벨을 대조함"
```

수정 후에는 `fix_pending_retest`에 `--fix-reference <commit-or-source-hash>`를 넣고,
새 세션으로 다시 채점한 뒤 `retested`에 `--retest-session <new-session>`을 지정한다.
잘못 분류한 문제는 `reclassify`로 근거와 함께 고치며 이전 분류는 audit에 남는다.
CSV에는 검토 메모가 들어가므로 저장소 밖 새 경로에 권한 0600으로만 내보내고 공개
커밋·공유 전에 개인정보를 확인한다.

## 첫 가동 결과와 다음 Topic 순서

| 사례 / Topic | 결정론 점수 | 승인 범위 | 기록 | 우선 확인할 것 |
|---|---:|---:|---|---|
| SIL 결정 / `sil_target_determination_risk_reduction_and_lifecycle` | 7.61 | 10.0–14.5 | `benchmark_conflict`, 낮은 근거 회수·미해결 12 | 네 핵심 오류와 기준 라벨의 벌점 범위, 정상 표현의 누락 여부 |
| V-Model / `instrumentation_control_software_lifecycle_v_model_traceability_verification_validation` 외 2 Topic | 6.20 | 10.5–14.5 | `benchmark_conflict`, 미해결 11 | Unit/Integration·MC/DC 오답 및 교차 Topic 중복 벌점 |
| Nyquist / `nyquist_stability_criterion_gain_phase_margin` | 11.83 | 14.0–19.0 | `benchmark_conflict`, 미해결 0 | 짧은 답안이 P·N·Z 관계식을 충분히 설명했는지 기준 라벨부터 확인 |

세 건의 `benchmark_conflict` 중 Nyquist 1건은 **triaged**로 옮겼다. 답안은 기준점과
안정 판정 방향은 언급하지만 `N=Z-P` 등 부호 규약을 포함한 명시적 관계 및 P·N·Z
정의가 부족하다. 그러므로 기준 라벨 자체도 대조 대상이다. SIL·V-Model의 2건은
**open**이다. 이를 과소채점으로 확정하거나 범위에 맞추기 위해 점수 규칙을 조정하지
않는다. 초기 세션에는 자동 보류 3건도 있다. 현재 전체 issue는 6건(열림 5,
분류 완료 1)이다. 우선순위는
Nyquist의 라벨/정답 범위 확인 → SIL의 fatal·정상 표현 대조 → V-Model 교차 Topic 중복
검토다. 각 문제는 한 번에 하나의 원인을 판정한다.

## Topic Pack 수정 게이트

1. 공개 커밋 밖 세션과 체크시트에서 한 문제를 선택한다. 질문·답안·전문가 라벨·출처
   Fact를 각각 대조해 **Pack 결함 / parser 결함 / scoring 결함 / 라벨 결함 / 정보 부족**
   중 하나로 판정한다.
2. Pack 결함으로 확인됐을 때만 `docs/topic_pack_workflow.md` 절차를 따른다.
   WordPress 원문은 출처이고 채점 기준 승격은 별도 사실 검증·승인 단계다.
3. 정상 답안과 의미가 비슷한 오답을 한 쌍의 회귀 사례로 추가한다. 기존 A/B/C/D/E,
   fatal, Question Type, routing 권한은 유지한다.
4. 집중 테스트, `rubric_manager.py validate-all`, non-promote 전체 release,
   `validate-topic-pack-release --all`을 실행한다. 실패는 체크시트에 기록하고 우회하지 않는다.
5. 새 세션 재시험과 기존 Golden 불변을 확인한 뒤에만 해당 issue를 종료한다.
   다음 Topic으로 이동할 때 해결·보류·남은 위험 수를 기록한다.

이 반복 절차로 전체 Topic을 순차 확장한다. 미해결 Fact나 질문 범위가 많은 Topic은
기존 채점 경로를 유지하고 LLM 결과를 점수에 자동 투입하지 않는다.

## 최초 가동 검증

- 실제 진입점 3사례 채점·체크시트 저장: 성공. 기존 운영 봇 자체에는 미배포.
- 관련 pytest **74 passed**; `rubric_manager.py validate-all` **ALL VALID**.
- `PROMOTE_GENERATED=0 scripts/validate_release.sh` **exit 0**;
  `validate-topic-pack-release --all` **PASS**; `git diff --check` 통과.
- 전체 release의 Topic content audit: 86 Topic / 86 Master / 749 question patterns /
  2,073 anchors PASS. 전용 10회 재현성 검사는 opt-in으로 SKIP.
- 공개 저장소 밖 상세 로그: `/tmp/quality_pilot_20261013.log`,
  `/tmp/quality_loop_release_20261013.log`,
  `/tmp/quality_loop_validate_all_20261013.log`,
  `/tmp/quality_loop_topic_release_20261013.log`.
