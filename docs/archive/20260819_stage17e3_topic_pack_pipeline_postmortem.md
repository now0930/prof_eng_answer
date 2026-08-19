# Stage17E3 Topic Pack Pipeline Postmortem

## 1. 문서 상태

| 항목 | 값 |
|---|---|
| 작업일 | 2026-08-19 |
| 저장소 | `now0930/prof_eng_answer` |
| Branch | `main` |
| 시작 HEAD | `91d4c71b4e7629f3efa019ccf727cab15ee9ad48` |
| 완료 HEAD | `7b441d003da69584056d8a44b3c8dc96da015733` |
| 완료 tree | `ea1285efc25a778389accf3edc19160255a21e2c` |
| Commit | `fix(topic-pack): stabilize generated contract pipeline` |
| Commit 범위 | 수정 8개, 신규 4개, 총 12개 |
| 제외한 기존 dirty | `scripts/validate_release.sh` |
| 최종 상태 | local/remote 일치, ahead/behind `0/0` |

이 문서는 Stage17E3의 시행착오와 복구 과정을 기록한다. 현재 운영 절차는 [`../topic_pack_workflow.md`](../topic_pack_workflow.md)를 따른다.

## 2. 목표

Stage17E3의 목표는 Topic Pack 확장 과정에서 발견된 generated version, classification policy, schema/profile contract와 검증 경계를 안정화하는 것이었다.

최종 변경은 다음을 포함했다.

- generated version의 결정성 확보
- 75개 Topic classification 정합성 확보
- Topic Pack schema와 implementation evaluation profile 추가
- Topic Pack contract test와 tool test 추가
- generated bank 6개 재생성
- 기존 dirty 파일을 제외한 선택적 commit과 push

## 3. 최종 변경 범위

### 3.1 수정 8개

```text
rubrics/generated/fact_anchors.generated.json
rubrics/generated/logic_check_profiles.generated.json
rubrics/generated/logic_checks.generated.json
rubrics/generated/model_answers.generated.json
rubrics/generated/topic_importance.generated.json
rubrics/generated/topic_pack_manifest.generated.json
scripts/build_generated_rubrics.py
scripts/test_topic_classification_policy.py
```

### 3.2 신규 4개

```text
rubrics/topic_profiles/implementation_evaluation_v1.json
schemas/topic_pack_spec.schema.json
scripts/test_topic_pack_contract.py
scripts/test_topic_pack_tool.py
```

### 3.3 명시적 제외

```text
scripts/validate_release.sh
```

이 파일은 Stage17E3 시작 전부터 dirty였다. Stage17E3 commit에는 포함하지 않았다.

## 4. 시간순 경과

### 4.1 결정성 및 classification 수리

`build_generated_rubrics.py`의 wall-clock version 생성을 제거했다. Builder source와 canonical sorted Topic Pack input을 SHA-256으로 계산하도록 변경했다.

공유 version prefix:

```text
sha256-b5e77b4dd281a108961741ed5eaf0a1188d365e21b97918daa6b779fe067ac31
```

새 Topic:

```text
control_valve_maintenance_inspection_troubleshooting_overhaul_reassembly_testing
```

이 Topic을 `FIELD_APPLICATION`에 등록했다.

최종 classification:

```text
THEORY_CORE=22
FIELD_APPLICATION=37
DESIGN_EVALUATION=16
TOTAL=75
```

별도로 고정되어 있던 과거 전체 수 `74`는 제거했다.

결과:

```text
SOURCE_CONTRACT_CHECKS=106_OF_106_PASS
FOCUSED_TESTS=PASS
FULL_VALIDATION=PASS
GENERATED_IDEMPOTENCE=6_OF_6_PASS
```

### 4.2 Post-repair 검토

수리 직후 다음을 확인했다.

- tracked diff 9개
- index diff 0개
- Stage 소유 tracked 8개
- Stage 소유 untracked 4개
- 제외 파일 1개
- generated 의미 검토 6/6
- classification `22/37/16_TOTAL_75`

결과:

```text
REVIEW_CHECKS=60_OF_60_PASS
```

### 4.3 Pre-commit audit V1의 감사 도구 오류

첫 pre-commit audit는 repository 문제가 아닌 감사 코드 문제로 실패했다.

원인:

```python
status_for(...).strip()
```

Git porcelain status의 선행 공백을 제거하여 다음 상태를 잘못 비교했다.

```text
실제: " M scripts/validate_release.sh"
변환: "M scripts/validate_release.sh"
```

교훈:

- Git porcelain status의 공백은 의미가 있다.
- 문자열 전체에 `.strip()`을 적용하지 않는다.
- path와 XY status를 구조적으로 파싱한다.
- audit 실패와 product failure를 구분한다.

수정한 V2 결과:

```text
AUDIT_CHECKS=86_OF_86_PASS
```

### 4.4 Selective staging V1의 trailing whitespace 발견

첫 selective staging은 정확한 12개 파일을 index에 올렸다. 그러나 다음 검사에서 실패했다.

```text
git diff --cached --check
```

발견된 위치:

```text
scripts/test_topic_pack_contract.py:132
scripts/test_topic_pack_tool.py:135
```

두 줄 모두 공백만 있는 blank line이었다.

Rollback 결과:

```text
ROLLBACK=PASS
INDEX=CLEAN
WORKTREE=UNCHANGED
```

이 실패는 중요한 경계 문제를 드러냈다.

- `git diff --check`는 untracked 신규 파일을 검사하지 않는다.
- 신규 파일의 whitespace 오류는 staging 전에는 놓칠 수 있다.
- commit 전에 `git diff --cached --check`가 필요하다.

### 4.5 Whitespace 수리

Repository와 candidate의 두 파일에서 같은 줄의 trailing whitespace만 제거했다.

결과:

```text
REPAIR_TYPE=TRAILING_WHITESPACE_ONLY
EXACT_REPAIR=2_OF_2_PASS
TARGET_CANDIDATE_MATCH=4_OF_4
TARGET_WHITESPACE_CLEAN=4_OF_4
FOCUSED_UNITTEST_RC=0
FULL_VALIDATION_RC=0
GENERATED_STABILITY=6_OF_6
REPAIR_CHECKS=65_OF_65_PASS
```

### 4.6 수리 후 scope 재고정

Whitespace 수리로 파일 hash가 바뀌었으므로 이전 pre-commit manifest를 재사용하지 않았다.

새 기준선으로 다시 수행했다.

```text
POST_WHITESPACE_REVIEW=66_OF_66_PASS
PRECOMMIT_SCOPE_AUDIT_V3=71_OF_71_PASS
COMMIT_SCOPE_WHITESPACE_CLEAN=12_OF_12_PASS
```

### 4.7 Selective staging V2

새 manifest의 12개 경로만 staging했다.

결과:

```text
STAGED_PATH_COUNT=12
STAGED_TRACKED_MODIFIED_COUNT=8
STAGED_NEW_FILE_COUNT=4
UNSTAGED_PATHS=scripts/validate_release.sh
STAGE_CHECKS=109_OF_109_PASS
```

검증된 index tree:

```text
ea1285efc25a778389accf3edc19160255a21e2c
```

### 4.8 Staged audit

현재 index를 저장된 patch, scope manifest, candidate, generated 의미 계약과 교차 검증했다.

결과:

```text
STAGED_WHITESPACE_CLEAN=12_OF_12_PASS
TARGET_CANDIDATE_MATCH=4_OF_4_PASS
GENERATED_STAGED_REVIEW=6_OF_6_PASS
POLICY_TEST_RC=0
FOCUSED_UNITTEST_RC=0
AUDIT_CHECKS=125_OF_125_PASS
```

### 4.9 Local commit

검증된 index tree만 commit했다.

```text
COMMIT_SHA=7b441d003da69584056d8a44b3c8dc96da015733
COMMIT_PARENT=91d4c71b4e7629f3efa019ccf727cab15ee9ad48
COMMIT_TREE=ea1285efc25a778389accf3edc19160255a21e2c
COMMITTED_PATH_COUNT=12
COMMIT_CHECKS=69_OF_69_PASS
```

Commit 후에도 `scripts/validate_release.sh`는 unstaged로 남았다.

### 4.10 Pre-push audit와 push

Push 직전 원격 lineage를 다시 확인했다.

```text
REMOTE_HEAD=91d4c71b4e7629f3efa019ccf727cab15ee9ad48
LOCAL_HEAD=7b441d003da69584056d8a44b3c8dc96da015733
LOCAL_AHEAD=1
LOCAL_BEHIND=0
PRE_PUSH_AUDIT=85_OF_85_PASS
```

Force 없이 한 번 push했다.

```text
git push origin HEAD:refs/heads/main
```

Push 결과:

```text
POST_REMOTE_HEAD=7b441d003da69584056d8a44b3c8dc96da015733
POST_PUSH_AHEAD=0
POST_PUSH_BEHIND=0
PUSH_CHECKS=51_OF_51_PASS
```

### 4.11 Post-push audit

최종 read-only 감사 결과:

```text
LOCAL_HEAD=7b441d003da69584056d8a44b3c8dc96da015733
REMOTE_HEAD=7b441d003da69584056d8a44b3c8dc96da015733
LOCAL_AHEAD=0
LOCAL_BEHIND=0
INDEX_DIFF_COUNT=0
UNSTAGED_PATHS=scripts/validate_release.sh
POLICY_TEST_RC=0
FOCUSED_UNITTEST_RC=0
AUDIT_CHECKS=85_OF_85_PASS
CLASSIFICATION=STAGE17E3_COMPLETE
```

## 5. 직접 원인

### 5.1 Generated version이 시간에 의존

같은 source로 rebuild해도 version이 달라질 수 있었다. 이는 idempotence와 clean checkout 재현성을 깨뜨린다.

수정:

- wall clock 제거
- canonical input 기반 SHA-256 version
- generated 6개 공유 prefix 검증

### 5.2 Classification 총계가 중복 고정

분류 집합과 별도로 전체 수 `74`를 literal로 검사하고 있었다. Topic이 75개가 되면서 stale assertion이 됐다.

수정:

- 실제 Topic set과 세 classification set의 합집합을 비교
- 분류별 count를 집합에서 계산
- 전체 수 literal 중복 제거

### 5.3 새 Topic의 classification 누락

새 Topic은 source와 generated에는 존재했지만 difficulty classification에 등록되지 않았다.

수정:

- `FIELD_APPLICATION`에 등록
- actual set과 classified set equality 계약 추가

### 5.4 Untracked 신규 파일의 whitespace 사각지대

Tracked diff 검사만으로는 신규 untracked 파일의 trailing whitespace를 찾지 못했다.

수정:

- commit 대상 전체 직접 whitespace 검사
- selective staging 후 `git diff --cached --check`
- staged audit에서 index blob 재검사

### 5.5 Audit code가 Git status를 잘못 파싱

`.strip()`이 porcelain status의 의미 있는 선행 공백을 제거했다.

수정:

- XY status와 path를 분리
- audit failure를 repository failure와 구분
- read-only diagnostic 후 audit script만 수정

### 5.6 Audit artifact가 ignored-set 변화처럼 보임

작업 과정에서 생성한 `gemini_script/*.sh`는 ignored 파일이었다. 단순 set 비교는 이를 repository mutation처럼 오판할 수 있었다.

수정:

- 알려진 audit self-artifact를 정규화
- 정규화 전후 set을 모두 기록
- non-normalized delta가 0인지 검사

### 5.7 기존 dirty 파일 혼입 위험

`validate_release.sh`는 Stage 시작 전부터 dirty였다. 범용 staging을 사용하면 의도치 않게 commit될 수 있었다.

수정:

- include 12개와 exclude 1개 manifest
- selective staging
- commit 전후 hash와 patch 보존
- post-push까지 unstaged 상태 확인

## 6. 잘 작동한 통제

### 6.1 Read-only audit와 mutation 분리

각 mutation 전에 현재 상태와 범위를 고정했다. Audit code 오류가 발생해도 repository와 index는 보존됐다.

### 6.2 Candidate와 repository 동시 정규화

Whitespace 수리 시 repository와 candidate를 같은 방식으로 변경했다. 이후 4개 target의 hash 일치를 계속 검증했다.

### 6.3 Generated 의미 감사

Generated 파일의 전체 line diff만 보지 않았다.

각 generated bank에 대해 다음을 확인했다.

- 기존 Topic record 불변
- 새 Topic 하나만 추가
- top-level metadata 계약 유지
- manifest count 75
- shared deterministic version

### 6.4 Tree 기반 commit 검증

Commit 성공 여부를 메시지만으로 판정하지 않았다.

```text
commit tree == 검증된 index tree
commit parent == pre-commit HEAD
commit path set == include manifest
```

### 6.5 증거 chain

각 단계는 `summary.json`, check TSV, manifest, patch와 log를 남겼다. 다음 단계는 이전 단계 결과를 다시 검증했다.

## 7. 앞으로의 표준

Topic Pack을 추가할 때 다음 순서를 기본으로 한다.

```text
기존 문서와 validator discovery
→ source boundary 확정
→ focused authoring
→ classification 등록
→ deterministic generated rebuild
→ build 2회 idempotence
→ generated semantic delta
→ 신규 파일 직접 whitespace 검사
→ full validation
→ include/exclude manifest
→ selective staging
→ cached diff check
→ staged tree audit
→ local commit
→ pre-push remote lineage audit
→ non-force push
→ post-push audit
```

다음 행동은 금지한다.

- 기존 절차를 확인하지 않고 schema를 추정
- generated JSON 직접 수정
- time-based generated version
- 전체 Topic 수 literal 중복
- `git add .`
- untracked 파일을 제외한 diff check만 수행
- 기존 dirty 파일과 Topic 변경을 같은 commit에 포함
- audit script 실패를 즉시 product failure로 단정
- force push

## 8. 핵심 교훈

1. Validator 통과와 reproducibility는 다른 계약이다.
2. Generated output은 결정성, idempotence와 의미 delta를 함께 검사해야 한다.
3. 신규 파일은 tracked diff 검사만으로 보호되지 않는다.
4. Git porcelain의 공백은 데이터다.
5. Audit 도구도 test 대상이다.
6. Commit 범위는 경로 manifest와 tree로 증명해야 한다.
7. 기존 dirty 상태는 작업 범위 밖의 보호 대상이다.
8. Push 성공은 원격 HEAD와 ahead/behind로 확인해야 한다.

## 9. 최종 기준선

Stage17E3는 다음 commit에서 완료됐다.

```text
7b441d003da69584056d8a44b3c8dc96da015733
```

재실행하지 않는다. 이후 Topic Pack 작업은 이 commit과 `docs/topic_pack_workflow.md`의 실패 방지 Gate를 기준으로 시작한다.
