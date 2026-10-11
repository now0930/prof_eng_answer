# DP transmitter manifold Anchor 근거 재검토 (2026-10-11)

## 결과

`dp_transmitter_manifold_bleed_pressure_test_pulsation_isolation`의 아래 두 Anchor는
이전 200건 배치 감사에서 `확인`으로 분류되어 있었지만, 해당 분류만으로 기술 검증 완료로
보지 않는다. 현행 문구는 제조사·구성별 절차를 보편적인 단일 순서로 일반화하므로
approved fact registry에 등록하지 않고 미검증 상태로 유지한다.

| Anchor | 현행 주장 요약 | 판정 |
|---|---|---|
| `manifold_isolation_sequence` | “3-valve”에서 H close → equalizing open → L close → bleed open | 미승인. 제조사 문서는 3-valve와 5-valve의 구조를 구분한다. 3-valve에는 통상 H/L isolation 2개와 equalize 1개가 있으며 전용 bleed valve가 포함되지 않을 수 있다. 격리 순서도 장치·작업 절차별로 확정해야 한다. |
| `manifold_return_sequence` | bleed close → L open → equalizing close → H open | 미승인. 일반 복귀 절차로 확인되지 않았다. Rosemount 절차는 해당 모델 및 작업 조건에 따라 zero trim 이후 equalize를 닫고 LP isolation을 다시 여는 식으로 설명하며, 다른 구성에는 별도 도식·순서가 있다. |

## 확인 근거와 범위

- Emerson, *Rosemount 2051 Reference Manual*, Table 2-7, “Three-valve configuration” (2024), pp. 32–34: 정상 운전 시 두 isolation valve open / equalizing valve closed. Zero trim 절차는 LP-side isolation valve를 먼저 닫고 equalize valve를 열어 압력을 같게 한 뒤, zero trim 후 equalize를 닫고 LP isolation을 다시 연다. 이는 **zero trim 절차**이지 일반적인 전 공정 격리·bleed 절차로 전용할 수 없다.
- Emerson, *Rosemount 3051 Reference Manual* (2018), pp. 60–64: 3-valve arrangement, 5-valve natural-gas arrangement 및 in-line/block-and-bleed arrangement를 구분하고 서로 다른 순서를 제시한다. 별도 bleed screw는 block-and-bleed 방식의 기능으로 설명한다.
- Emerson, *Rosemount Manifold Solutions* (October 2024), pp. 4–6: 3-valve는 2 isolation + 1 equalize; 5-valve는 여기에 controlled vent를 위한 drain/vent valve 2개를 추가하는 구성을 설명한다.
- Yokogawa FAQ, “Can I use a 2-valve gauge manifold on a DP transmitter?”: 3/5-valve equalizing valve의 연결 기능과 적용 경계를 설명한다. 안전한 manifold 조작 순서를 일반화하는 근거로 사용하지 않는다.

## 후속 조치

운전 순서를 Anchor로 유지하려면 적용 manifold의 실제 valve arrangement, transmitter 모델, 작업 목적
(격리·zero trim·calibration·venting·복귀), 공정 압력 및 위험물 배출 경로를 명시하고 해당 제조사
manual 절차와 대조해야 한다. 그 전까지는 exact sequence를 정답·오답 판정에 쓰지 않고,
기능적 원칙(제조사 절차 준수, 허용 차압 초과 방지, trapped pressure의 통제된 배출)만 별도 검토한다.

검토는 근거 기록만 수행했다. Fact Anchor 본문 및 점수 영향은 변경하지 않았다.

