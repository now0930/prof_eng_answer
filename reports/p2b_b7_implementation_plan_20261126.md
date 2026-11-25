# P2-B7 — 비채점 Claim 근거 정합성 개선 실행계획

기준: 0338b7a7c72b333566b23ef448f6b032aeadfd00; Issue #40 / Draft PR #49. 원본 36건과 기존 111건은 보존. 이 커밋은 시험 명세 준비만 수행하고 Python 구현과 실행은 NOT_RUN이다.

## 작업 범위
- 별도 36건 fixture: GEN-18 C→U, GEN-20 U→R, GEN-21 C→U, GEN-35 U→R. R15/C6/U15. 독립 전문가 라벨 아님.
- 개선 대상은 기존 8건 + 신규 20건 = 28건. 신규 16개 나머지 사례도 방어 회귀로 실행한다.
- GEN-09의 기존 모순 판정은 원문 덧셈을 mass_flow=volumetric_flow로 오변환한 결과로 근거 실패이다. 최우선 재현/차단. 단순 판정 일치와 근거 정합성을 분리한다.
- GEN-26은 올바른 추출 이후 한국어 종결형 감사 제한으로 보류. 수식, 영어, 명사형 답안을 근거 기반으로 수용하되 단순 나열/인용은 제외한다.
- GEN-04/05/09/15는 잘못된 연산·무관성·비율 반전의 기술적 모순과 현 계약 표현 가능성을 구분한다. 동일한 subject/predicate/object의 반대 극성을 근거 없이 만들어 내지 않는다. 기존 표현으로 입증하지 못하면 보류 및 후보 기록.

## Codex 구현 지시
1. git status, branch, HEAD 확인. 기존 runner로 원본 111, 검토 111, 원본 36, 검토 36 기준 재생. 결과 파일 새 이름 사용. 실행 오류 0 확인.
2. 기존 추출기/ontology/수식 처리/감사 경로 및 기존 스키마 재사용. 문장 역할·연산·조건 귀속·부정/정정·절 단위 인용 처리를 기능 단위 개선. 시험 ID별 분기/문장 암기 금지. LLM 비교는 P2-B8으로 남긴다.
3. 연구용 근거 정합성 검사 및 테스트 추가. 정확한 source span/text, owner, scope, assertion_context, source meaning entailment, 연산 순서, polarity, conditions 확인. 단순 문자열 또는 schema 일치는 의미 정확성을 보장하지 않는다. 28건마다 technical expected / observed / fidelity PASS|FAIL|NOT_ESTABLISHED / reason / evidence span을 분리 기록. 명시적으로 채택되지 않은 주장, 근거 없는 메타데이터, 자기동일화, 다른 관계 오귀속 검증. 보류는 근거 PASS로 계수하지 않음. GEN-09 재현 반례는 질량유량 동일시와 덧셈을 구분하며, 기존 fatal/ceiling 정책에 연결하지 않는다.
4. 16개 방어 사례 및 새로운 비개발 반례(독립 전문가 라벨 아님)로 회귀. 실제 기술 오류와 계약 범위 밖을 별도 기록. 개발 자료와 holdout 구분. 원본 111건 일치 및 검토 111/36·신규 probe 별도 집계, fixture-relative false support/contradiction, fidelity failures, withheld, coverage 기록. 독립 accuracy NOT_ESTABLISHED 유지.
5. 기존 143개 비공개 답안 replay를 기준 SHA와 개선 최종 코드 SHA 각각 clean checkout에서 실행, 입력/출력 SHA256·code SHA/tree·명령·환경·행수 기록. 원문 공개 금지. 143행 변경 0 필요. 이전 snapshot의 불명확한 SHA 귀속을 새 증거로 대체.
6. focused pytest, validate-all, Generated freshness, Topic Pack Release Gate, 전체 offline RC, 최종 SHA Actions. 결과 전후 비교 및 보고서 기록. 정본 2,096개/Topic89/Registry/Generated/119 HOLD/D4/P1-C 후보/A~E/WRONG/Fatal/Ceiling/25점 정책 보존. score_admission=DISABLED, score_effect=none. main 병합·배포·봇 재시작 금지. Firecrawl 금지.
7. 기존 draft branch에 커밋/push, Issue #40/PR #49 갱신. P2-B7의 실행 및 근거 정합성 검증이 끝나도 P2-B 전체 완료나 P2-C 진입을 자동 선언하지 않는다. P2-B8~B10과 기존 게이트는 유지. 남은 제약/NOT_RUN을 사실대로 기록.

## 명령 예시
```bash
python3 -B reports/run_p2b_relation_diagnostic_20261125.py --cases reports/p2b_generalization_reviewed_cases_20261126.json --output /tmp/p2b_b7_reviewed36.json
VALIDATION_LIVE_API=0 QUALITATIVE_DE_MODE=off PROMOTE_GENERATED=0 python3 -B scripts/release_candidate.py validate
```
runner의 소스 해시 검사와 충돌 시 허용 경계를 임의 완화하지 말고 명시적으로 버전 및 변경 근거 기록. 출력 경로는 기존 파일과 중복 금지.
