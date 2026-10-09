# Radar Level / GWR 문제 단위와 owner 경계 검토

검토일: 2026-10-07
기존 Pack: `radar_level_gauge_fmcw_pulse_distance_level_dielectric_constant_false_echo_installation_error`
새 후보: `guided_wave_radar_level_measurement_tdr_interface_application`
상태: 신규 owner는 managed draft; 기존 Pack 내용·라우팅은 미이관

## 기존 Pack 검토

기존 Pack은 자유공간 pulse 왕복시간, FMCW chirp/beat frequency, 변조 bandwidth, 유전율,
blocking distance, false echo, 설치, echo mapping 및 방식 selection을 연결한다. 그 안의
GWR Anchor 4개는 TDR probe propagation, surface/interface layer path, probe return path,
process limitation을 다룬다. 현재 14개 expected patterns 중 GWR 고유 원리를 실제로 요구하는
pattern은 없으며, 마지막 방식선정 패턴만 GWR을 비교대상으로 언급한다.

따라서 구조 이슈는 단순 수치 coverage가 아니다. Free-space antenna/echo chain과 GWR의
probe-guided TDR/interface path는 답안 backbone이 다르고, 기존 제목·patterns와 GWR fact
bank 사이에 실질적인 scope mismatch가 있다.

## 분리 후보

> **GWR 레벨계의 TDR 측정원리와 프로브 구조에 따른 전파경로를 설명하고, 상부 액면 및
> 계면 측정 시 유전율·공정조건이 미치는 영향과 적용상 한계를 설명하시오.**

제안 owner는 TDR/probe propagation, surface와 interface path, probe geometry/return path,
probe-specific process·mechanical limitations로 제한했다. 일반 free-space FMCW 식, 안테나
beam/false-echo handling, device commissioning은 기존 owner 또는 handoff로 둔다.

| 요구 | 신규 draft anchor |
|---|---|
| Guided pulse와 reflection round-trip | `gwr_tdr_probe_guided_reflection` |
| Surface/interface propagation path | `gwr_surface_interface_permittivity_path` |
| Probe/return-path modeling boundary | `gwr_probe_return_path_quasi_tem_boundary` |
| Process/mechanical application limits | `gwr_process_probe_application_limits` |

기존 source Pack은 지우거나 수정하지 않았다. 새 owner는 unique IDs로 managed draft에만
복사했고 `routing_aliases`는 활성화되지 않았다. 승인되기 전 두 소스를 동시에 운영 채점하는
것은 방지한다.

## Coverage 및 주장 한계

- source pack은 현재 28 Anchors와 14 patterns를 가진다. 기존 required-anchor union은 20/28
  (71.4%)다. 미연결 8개는 GWR 고유 4개와 advanced radar nuance 4개로, coverage 수치를
  인위적으로 높이지 않고 owner/선택 범위를 따로 기록했다.
- 새 draft는 대표 질문 하나에 4개 고유 Anchor를 모두 연결했고 answer outline에도 각 참조를
  기록했다. 이것은 자동 schema/quality completeness일 뿐 기술 사실의 독립 검증은 아니다.
- 기존 pack README의 제조사/handbook source names는 이어받았으나 실제 manual edition,
  page, drawing 및 본문은 확인하지 않았다. 기술 approval이나 과거 출제 증거를 주장하지 않는다.
- deterministic checks는 disabled, fatal/major checks는 비어 있으며 grading weights,
  Question Type, fatal treatment, router authority는 바꾸지 않았다.

## 2026-10-07 추가 pattern-scope 검토

- 14개 pattern의 요구를 기준으로 `high_score_points`, `common_missing_points`, `high_band_unlock_conditions`를 문항별로 제한했다. Pulse, FMCW, resolution, level conversion, dielectric/echo, blocking, installation, false-echo diagnostics, method selection을 서로 다른 문항에 전역 필수요건처럼 적용하지 않는다.
- 8개 orphan nuance/GWR anchors를 `optional`로 바꿨다. 특히 GWR 네 anchor는 별도 draft가 승인·owner migration되기 전까지 legacy context일 뿐, 자유공간 radar answer의 필수 점수가 아니다.
- Model Answer pattern 14 intent를 보완해 GWR을 고수준 비교 대안으로 한정하고, 상세 TDR/probe/interface 지식은 이 Pack에서 감점요건으로 쓰지 않도록 명시했다.
- Internal scorer scope only: question type, fatal claims, deterministic scoring, aliases/routing, GWR draft status 및 generated runtime bank를 변경하지 않았다.
- Coverage check: 28 total anchors, 20 required union, 8 optional. Focused regression, schema/quality, atomicity, and scoped release results are recorded after execution.

## Validation state

- Focused pattern-scope regression: 4/4 PASS.
- Topic schema/global-anchor validation: PASS (87 packs, 2,068 anchors checked).
- Topic quality: PASS, 0 errors, 1 non-blocking warning (`logic_check.deterministic_checks.topic_aliases` empty).
- Atomicity audit: PASS, 0 errors, 0 warnings.
- Scoped release: PASS; generated outputs were restored to their pre-validation snapshot; LLM smoke was skipped.
- Pack status remains `legacy / legacy_unmanaged`; no approval or status promotion was fabricated.

이 결과는 해당 Pack의 구조·범위 회귀 검증이며 기술 사실의 독립 검증이나 전체 `--all` release 승인을 뜻하지 않는다.
전체 release gate는 다른 managed drafts의 reviewer approval 없이 승격하지 않는다.
