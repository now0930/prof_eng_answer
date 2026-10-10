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

이 세 문장은 이미 운영 중인 legacy Fact Anchor에 대응한다. 검토 후보 기록은
WordPress source ID·버전·DB 콘텐츠 해시·기존 Anchor ID를 묶고, 최종 승인본은
[approved Fact registry](../grading/evidence/approved_fact_registry.json)에 보관한다.
승인자는 사용자 요청으로 위임받은 Codex임을 명시했다. 여기에는 원문 발췌나 개인 DB가
없고 `score_effect=none`이다. Source의 hash는 DB가 보유한 값이며
원본 웹페이지에서 새로 계산한 hash라는 뜻이 아니다.

기술적 외부 교차확인은 [IEC 61511-1의 SIS 생명주기·요구사항](https://webstore.iec.ch/en/publication/24237),
[IEC 61508-3의 안전 관련 SW 요구사항](https://webstore.iec.ch/en/publication/5517),
[MathWorks의 Nyquist 설명](https://www.mathworks.com/help/control/ref/nyquistplot.html)을
참고했다. 이는 WordPress 본문과 별개의 기술 참고이며 사용자 source 승인 대체물이 아니다.

현재 남은 운영 반영 조건:

1. WordPress 추출 본문 신호와 source metadata는 대조했지만, 웹 원본을 새로 수집해
   해시를 다시 산출하지는 않았다.
2. Master는 verified로 갱신되었고 세 Fact는 approved registry에 들어갔지만,
   기존 A/B/C/D/E 점수에 반영하는 Grading View adapter는 아직 연결되지 않았다.
3. legacy Topic Pack 상태는 그대로 두었다. 승인된 Fact registry가 곧바로 기존
   generated bank에 들어가는 것은 아니다.

따라서 세 Fact는 **검토 승인되어 registry에 등록**됐지만, 점수 영향은 아직 없다.
다음은 이 registry를 기존 점수 계약 안에서 소비하는 Grading View adapter와
대표 3개 Topic의 동일 답안 비교 평가다.

Nyquist Master의 다른 이미지 source 17건은 Master 시간 버전과 DB ETag 버전이
달라 `stale`이다. 이 감사는 해당 이미지를 기술 Fact 근거로 사용하지 않았다.

같은 DB snapshot에서 다음 읽기 전용 검사를 재실행할 수 있다. 출력에는 본문과
DB 경로가 포함되지 않으며, 세 candidate의 URL·버전·DB 해시와 본문 신호 문구를
확인한다. 신호 문구 일치는 정량식·표준 해석의 완전한 사실 검증이나 사람 승인이 아니다.

```bash
python3 scripts/verify_representative_fact_sources.py --database /path/to/private/wordpress_sources.sqlite3
```
