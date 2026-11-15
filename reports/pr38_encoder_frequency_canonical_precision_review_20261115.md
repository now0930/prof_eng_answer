# Encoder frequency-selection canonical precision correction — PR #38 (2026-11-15)

> **기술 사실의 단위·정의 정밀 교정. 채점 정책·Fact Registry/Promotion ledger/Generated 반영은 하지 않으며, 전체 pytest 및 release validation 전에는 PR을 Draft로 유지한다.**

## Identity and prior canonical source

- Topic ID: `speed_rotation_measurement_encoder_proximity_tachometer_selection_error`
- Anchor ID: `encoder_frequency_limit_selection`
- Old canonical: Encoder와 receiving counter/PLC에는 최대 output/input frequency가 있으므로 최고 회전속도와 N_eff의 곱이 허용 주파수를 넘지 않도록 선정한다. 해상도를 높이면 동일 속도에서 pulse frequency도 증가한다.
- Corrected canonical: 증분형 A/B 엔코더의 채널별 출력 주기수 PPR[cycle/rev]와 최고 회전속도 n_max[rpm]로 채널 주파수 f_ch=n_max·PPR/60[Hz]를 계산해 엔코더 최대 응답 주파수 및 수신기의 복호모드별 입력 주파수 한계와 비교한다. 수신기 내부의 x1/x2/x4 유효 계수율 f_count=n_max·N_eff/60[count/s]은 별도의 처리율 한계가 명시된 경우 그 사양과 비교하며, 고해상도일수록 같은 회전속도에서 주파수가 증가한다.
- Basis: [nine-candidate final disposition](../reports/pr38_fact_anchor_nine_canonical_dispositions_20261115.md). The simplification candidate in the historical 48-row calibration manifest remains **PENDING_TECHNICAL_REVIEW / NOT APPLIED**.

## Original engineering source-to-claim mapping

1. **OMRON Industrial Automation**, *Rotary Encoders — Introduction*, `Operating Principles` and `Selection Guidelines [6] Maximum Response Frequency`, web HTML consulted 2026-11-15: [official page](https://www.ia.omron.com/support/guide/34/introduction.html). Formula `Maximum response frequency = Revolutions(RPM)/60 × Resolution`, and separate x2/x4 multiplier circuit description. Formula uses the encoder's output cycles (resolution) as defined for the selected device; never silently substitute receiver-decoded x4 effective count for the physical signal frequency.
2. **NI**, *NI-DAQmx Counter Input: Position: Decoding Type*, X1/X2/X4 definitions, web documentation consulted 2026-11-15: [official page](https://www.ni.com/docs/es-PE/bundle/ni-daqmx-labview-api-ref/page/resource/objmgr/daqmx-rc/daqmx-channel/attr21e6.html). X1 counts one A-edge; X2 both A edges; X4 A/B rising/falling edges. Thus the count rate may be 4× the physical A-channel cycle rate while the input signal itself remains unchanged.
3. **Rockwell Automation**, *1769-UM006E-EN-P Compact High-speed Counter Module User Manual*, `Chapter 2 — Module Operation → Input Frequency`, specific 1769-HSC model: [official manual](https://literature.rockwellautomation.com/idc/groups/literature/documents/um/1769-um006_-en-p.pdf). Different x2/x4 configuration has different permitted **input frequency**. Example is model-specific, **not a universal grading threshold**. PDF screenshot recheck of this manual is not asserted here.

## Dimensional verification and counterexamples

- n_max=3,000 rpm, channel PPR=2,000 cycle/rev -> `f_ch=3000×2000/60=100,000 Hz`. Under ideal quadrature x4 `N_eff=8,000 count/rev`, internal `f_count=3000×8000/60=400,000 count/s`.
- WRONG: comparing `f_count=400 kcount/s` directly against `250 kHz x4 input frequency` without verifying whether the vendor limit means external physical signal Hz or the decoder's internal count-event/s. Both use inverse seconds dimensionally, but represent distinct physical/implementation specifications.
- WRONG: using `n_max×PPR` as frequency when n is rpm; conversion `/60` is mandatory.
- CONDITIONAL: if a device defines `CPR` or `PPR` differently, obtain actual cycles/rev from the product datasheet. x4 effective count is a receiver decoding mode, not a fourfold change in the encoder output waveform cycle frequency. Electrical channel limitations, I/O filter/edge bandwidth, and physical RPM limitations remain device-specific.

## Safe change boundary and verification debt

- Edit only source Anchor `statement`, `claim`, `description`, first `accepted_explanations` to exact corrected sentence; leave all other anchors, scoring importance, weights, fatal, exclusions and IDs untouched. Clarify the topic sheet at the frequency equation (source of the old ambiguity).
- Preserve the 2026-11-14 manifest's exact `previous_statement` and `simplified_statement` as historical facts. Attach a **single scoped `canonical_precision_correction`** record to its original entry, which must exactly match this report and be rejected if applied to another Topic/Anchor.
- Protect both paths in audit/tests: unapproved simplified candidate cannot replace source; an unrelated source edit or an ungrounded 'correction' fails closed. The correction does not authorize any automatic score admission.
- GitHub connector writes do not run repo-wide validation. Managed generated rebuild and full offline `python3 -B scripts/release_candidate.py validate`, along with approved Registry/source-hash compatibility, must be completed before declaring release PASS. No direct `rubrics/generated` write.

**Review method:** GPT-6, AI technical review. User explicitly requested this single canonical correction. Not a human reviewer or CI validation claim.
