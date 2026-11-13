# WordPress URL → Topic Pack 지속 운영 정책

**기준 (2026-11-13): 서버에서 OCR과 PDF 파일 읽기는 하지 않습니다.** WordPress에 이미 준비된 본문 텍스트와 그림 참조를 자료로 사용합니다. PDF는 파일 원문 대신 URL·제목 등 참조 메타데이터만 남깁니다.

**AI/Codex 실행 세부 계약:** [URL 실행 지침](wordpress_url_continuous_ai_runbook.md) · [Topic 링크 검토](wordpress_topic_pack_linking_policy.md) · [Fact 적격성](fact_anchor_eligibility_policy.md)

## 목표

기존 WordPress 본문 텍스트와 그림 설명을 먼저 기존 Topic Pack과 연결하고, 독립 검증된 기술적 사실만 별도로 채점 기준에 반영합니다. 새 Topic/Fact/프로그램을 먼저 만들지 않습니다.

## URL별 작업

| 순서 | 작업 | 완료 기준 |
| --- | --- | --- |
| 1 | URL, post ID, 본문 해시 확인 | 신규·변경·미변경 판정 |
| 2 | WordPress 본문 텍스트와 그림/PDF 링크 메타데이터 수집 | 원본 텍스트 보존·링크 기록 |
| 3 | 기존 Topic 범위와 비교 | 후보 및 실제 본문 근거 확인 |
| 4 | 링크 승인·보류·거절 | 검토자·근거·상태 기록 |
| 5 | Master 출처 별도 승인 및 학습 bundle 연결 | 승인된 본문 source만 유효성 검사 |
| 6 | 필요할 때 기존 Fact와 대조 | 중복·오류·보완·보류 구분 |
| 7 | 필요한 채점 내용만 별도 승인·검증 후 변경 | 근거·해시·회귀 결과 확인 |

**Topic 링크 승인 ≠ Master 출처 승인 ≠ Fact 진위 검증 ≠ 채점 반영 승인**입니다.

## 입력과 제외 대상

- **본문 텍스트:** 원문을 변경하지 않고 수집합니다. 게시된 수식·그림 설명은 그 텍스트를 사용합니다.
- **그림:** URL·alt 텍스트 등 참조만 저장합니다. 서버에서 그림 속 기술 내용을 자동 판독하지 않습니다. 의미 분석은 사전에 작성된 설명 또는 별도 검토를 사용합니다.
- **PDF:** 원본 다운로드, 텍스트 추출, PDF 렌더링, OCR을 수행하지 않습니다. 준비된 내용이 본문에 텍스트와 그림 설명으로 제공될 때만 사용합니다.
- **과거 OCR 자료:** 비공개 카탈로그에 보존하며 URL 실행기의 검색과 학습 bundle에는 사용하지 않습니다. 독립 OCR 도구는 [레거시 문서](wordpress_topic_pack_ocr.md)를 참조하세요.

## 안전과 방향 이탈 방지

본문과 그림 링크만으로 새로운 채점 Fact를 임의 승인하지 않습니다. Topic 소유 범위·중복 검토를 선행하고, 출처 해시·검토자·근거·비공개 DB 백업을 보존합니다. 서버 OCR/PDF 처리 재도입은 별도의 명시적 요청이 있어야 합니다.

## URL 실행 및 보고

~~~bash
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/"
python3 scripts/wordpress_url_workflow.py "https://now0930.pe.kr/wordpress/자기회로/" --offline
~~~

매 실행마다 URL, 변경 상태, 본문 수집 여부, 그림/PDF 참조, 후보 Topic·승인 상태, Master·학습 bundle 상태, 독립 Fact 검토 필요 여부, 다음 작업 1순위를 보고합니다.

서버 OCR/PDF 원본 읽기 없이 처리된 것이 정상이며, 운영 DB 배포·채점 반영은 별도 단계입니다.
