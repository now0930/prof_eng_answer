# 대표 3개 Topic 출처·Fact 대조 (2026-10-10)

이 문서는 비공개 WordPress DB를 **읽기 전용**으로 대조한 결과다. DB나 OCR 전문,
답안 이력은 공개 저장소에 복사하지 않았다. 실시간 블로그 재수집·원본 HTML 해시
재계산은 수행하지 않았으므로, 아래 `일치`는 DB snapshot과 Master metadata 및
추출 본문 사이의 일치만 뜻한다.

| Topic | 기존 Anchor | WordPress source | 확인한 내용 | 상태 |
|---|---|---|---|---|
| 목표 SIL 결정 | `sil_band_mapping` | `wp-post:9398` | DB의 URL·버전이 Master와 일치하고 추출 본문에 목표 PFD/PFH 뒤 SIL 구간 판정이라는 순서가 존재 | 기술 의미 대조 완료, Master `unverified` |
| SW V-Model | `sw04_v_model_definition` | `wp-post:9364` | URL·버전 일치; 추출 본문에 설계 단계와 시험 단계의 대응 및 추적성이 설명됨 | 기술 의미 대조 완료, Master `unverified` |
| Nyquist | `critical_point_minus_one` | `wp-post:6134` | URL·버전 일치; 추출 본문에 Nyquist 임계점 -1+j0이 기재됨 | 기술 의미 대조 완료, Master `unverified` |

이 세 문장은 이미 운영 중인 legacy Fact Anchor에 대응한다. 별도
[`candidate` 기록](../reports/fact_grounded_representative_candidates_20261010.json)은
WordPress source ID·버전·DB 콘텐츠 해시·기존 Anchor ID를 묶는다. 여기에는 원문
발췌나 개인 DB가 없고 `score_effect=none`이다. Source의 hash는 DB가 보유한 값이며
원본 웹페이지에서 새로 계산한 hash라는 뜻이 아니다.

기술적 외부 교차확인은 [IEC 61511-1의 SIS 생명주기·요구사항](https://webstore.iec.ch/en/publication/24237),
[IEC 61508-3의 안전 관련 SW 요구사항](https://webstore.iec.ch/en/publication/5517),
[MathWorks의 Nyquist 설명](https://www.mathworks.com/help/control/ref/nyquistplot.html)을
참고했다. 이는 WordPress 본문과 별개의 기술 참고이며 사용자 source 승인 대체물이 아니다.

현재 승격 불가 사유:

1. 세 Master source의 `verification_status`가 모두 `unverified`이고 승인된
   `content_sha256` 기준선이 없다.
2. WordPress claim의 사람 콘텐츠 승인과 Fact 관계 binding 승인 기록이 없다.
3. legacy Topic Pack은 `legacy_unmanaged`이며, 이 기록을 `approve-topic`의 사람
   검토 이력으로 위장하거나 generated bank를 직접 수정할 수 없다.

따라서 candidate는 **새 채점 권한이 없다**. 기존 Anchor의 운영 동작도 변경하지 않았다.
실제 승격은 WordPress 원문·본문·수식과 candidate 세 건을 사람 검토한 뒤,
기존 content proposal/승인 절차로 Master source 기준선과 Fact의 `approved`
상태를 기록하고, 그 snapshot으로 독립 평가와 release를 통과했을 때만 가능하다.

Nyquist Master의 다른 이미지 source 17건은 Master 시간 버전과 DB ETag 버전이
달라 `stale`이다. 이 감사는 해당 이미지를 기술 Fact 근거로 사용하지 않았다.

같은 DB snapshot에서 다음 읽기 전용 검사를 재실행할 수 있다. 출력에는 본문과
DB 경로가 포함되지 않으며, 세 candidate의 URL·버전·DB 해시와 본문 신호 문구를
확인한다. 신호 문구 일치는 정량식·표준 해석의 완전한 사실 검증이나 사람 승인이 아니다.

```bash
python3 scripts/verify_representative_fact_sources.py --database /path/to/private/wordpress_sources.sqlite3
```
