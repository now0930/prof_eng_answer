# Eight primary original-source claim checks — 2026-11-01

Reviewer GPT-6 (AI); actual canonical `rubrics/topic_packs/<topic_id>/fact_anchor.json` statements independently compared with original technical publications and the identified clauses/formulae. Decision KEEP_BOUNDED for each. This is an individual *claim* determination, not global acceptance for every exam scoring demand; use `docs/fact_anchor_eligibility_policy.md` and maintain excluded/revision overlays. Some PDF screenshots failed, as indicated at each locator. No Topic Pack / generated bank / runtime grading edits or tests were made.

## 1. steam_impulse_lines_use_condensate_and_balance_heads_per_device_design

- Canonical topic/anchor: `instrumentation_installation_wiring_impulse_tubing_inspection_codes` / `iiwic_steam_service_principle`
- **Actual canonical statement:** Steam service에서는 transmitter를 고온 steam에 직접 노출하지 않고 condensate를 이용한 pressure transmission과 양측 hydrostatic head의 일관성을 확보하도록 설치 철학을 적용한다.
- Primary technical authority: Emerson, The Engineer's Guide to DP Flow Measurement (2022)
- Original publisher URL: https://www.emerson.com/is/content/emerson/en/measurement-instrumentation/marketing/industries/oil-and-gas/documents/doc-rosemount-00805-0100-1041.pdf
- Exact section/evidence method: Chapter 6 §6.5 Maintaining Wet Legs, printed p.106; original indexed PDF text inspected, PDF screenshot attempted but failed due to file size
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: Steam impulse paths use condensed water to isolate transmitter from hot vapor and require matched hydrostatic heads for differential measurements. Details vary with process/elevation.

## 2. youngs_modulus_stress_strain_linear_elastic_relation

- Canonical topic/anchor: `passive_sensor_resistive_capacitive_inductive_transduction` / `sensor_mechanical_stress_strain_youngs_modulus`
- **Actual canonical statement:** Young's modulus E는 선형 탄성영역에서 기계적 응력 sigma_m과 변형률 epsilon_m을 연결하며, 같은 응력에서 E가 클수록 기하학적 변형은 작다.
- Primary technical authority: NIST Special Publication 260-177 (2013), User’s Guide for RM 8096/8097
- Original publisher URL: https://www.nist.gov/system/files/documents/srm/SP260-177.pdf
- Exact section/evidence method: §2 discussion of Young's modulus, printed p.31; original PDF text, screenshot attempted but timed out
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: In small-strain linear elastic domain, E=σ/ε so ε=σ/E for the same uniaxial stress; not valid beyond elastic/proportional limit or for all anisotropic tensor relations.

## 3. root_locus_asymptote_centroid

- Canonical topic/anchor: `root_locus_stability_gain_design` / `asymptote_centroid`
- **Actual canonical statement:** 점근선 중심은 σ_a=(Σp_i-Σz_i)/(n-m)로 계산한다.
- Primary technical authority: MIT OpenCourseWare, 16.06 Principles of Automatic Control, Lecture 12 (Fall 2012)
- Original publisher URL: https://ocw.mit.edu/courses/16-06-principles-of-automatic-control-fall-2012/2a107059e26df574559b1def4fa9e36d_MIT16_06F12_Lecture_12.pdf
- Exact section/evidence method: Rule 3, PDF page index 1 visually checked
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: Root locus asymptote centroid σa=(Σp−Σz)/(n−m) for n>m, open-loop poles/zeros counted with multiplicity. Not defined by this formula when n<=m.

## 4. root_locus_departure_and_arrival_angles

- Canonical topic/anchor: `root_locus_stability_gain_design` / `departure_and_arrival_angles`
- **Actual canonical statement:** 복소극 출발각과 복소영점 도착각은 대상 특이점을 제외한 나머지 극점과 영점의 각도 기여로 계산한다.
- Primary technical authority: MIT OpenCourseWare, 16.06 Principles of Automatic Control, Lecture 12 (Fall 2012)
- Original publisher URL: https://ocw.mit.edu/courses/16-06-principles-of-automatic-control-fall-2012/2a107059e26df574559b1def4fa9e36d_MIT16_06F12_Lecture_12.pdf
- Exact section/evidence method: Rule 4, PDF page index 2 visually checked
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: Departure/arrival angles follow root-locus angle condition by omitting singular target pole/zero and summing the remaining pole/zero angle contributions, modulo 360°; convention and multiplicity matter.

## 5. ackermann_formula_siso_controllability_and_conditioning_caveat

- Canonical topic/anchor: `state_space_controllability_observability_pole_placement` / `ackermann_and_numerical_limits`
- **Actual canonical statement:** SISO 완전 제어가능 시스템에서 Ackermann 공식으로 K를 계산할 수 있지만 고차 또는 ill-conditioned 시스템에서는 수치적으로 민감할 수 있다.
- Primary technical authority: Python Control Systems Library stable documentation, place_acker; MathWorks place
- Original publisher URL: https://python-control.readthedocs.io/en/stable/generated/control.place_acker.html
- Exact section/evidence method: place_acker: Ackermann pole-placement method and K output; supporting MathWorks https://www.mathworks.com/help/control/ref/place.html
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: For completely controllable SISO (A,B), Ackermann computes feedback K; controllability-matrix inversion and clustered/high-order poles can lead to numerical ill-conditioning. Not universally stable for all A,B.

## 6. psychrometric_wet_bulb_is_not_dew_point_except_at_saturation

- Canonical topic/anchor: `humidity_measurement_capacitive_resistive_dew_point_selection_compensation` / `psychrometric_wet_dry_bulb`
- **Actual canonical statement:** Psychrometric method는 dry-bulb와 wetted wet-bulb의 증발냉각 차이를 이용하고, airflow·wick·water purity·pressure를 고려한 psychrometric relation으로 humidity를 구한다. Wet-bulb temperature를 dew point와 동일시하지 않는다.
- Primary technical authority: WMO Guide to Meteorological Instruments and Methods of Observation, WMO-No. 8, 7th ed. (2008), hosted by US NWS
- Original publisher URL: https://www.weather.gov/media/epz/mesonet/CWOP-WMO8.pdf
- Exact section/evidence method: Chapter 4 §4.2.1 Psychrometers, PDF page index 95 visually checked, equation e'=e'w(p,Tw)−A p(T−Tw)
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: Psychrometric dry/wet bulb and psychrometer coefficient depend on airflow, wick and pressure; wet bulb is not generally dew point. All coincide at saturated equilibrium RH=100%.

## 7. lag_compensator_dc_to_high_frequency_gain_ratio

- Canonical topic/anchor: `lead_lag_compensator_phase_margin_steady_state_error` / `lead_lag_lag_gain_ratio_error_constant`
- **Actual canonical statement:** 표준 지상보상기에서 저주파 이득은 Kc, 고주파 이득은 Kc/β이므로 상대 이득비는 β이다. 요구 오차상수 개선비와 목표 교차주파수의 크기 조건을 함께 만족하도록 설계한다.
- Primary technical authority: Aditya Mahajan, Linear Systems and Control, §14.2 Lag Compensator; MathWorks Compensator Dynamics
- Original publisher URL: https://adityam.github.io/linear-systems/lag-lead-compensators.html
- Exact section/evidence method: §14.2, G(s)=K(1+sT)/(1+sαT), α>1; supplemental https://www.mathworks.com/help/control/ug/edit-compensator-dynamics.html
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: For normalized lag form DC gain Kc and high-frequency gain Kc/β (β=α>1); crossover and negative phase must be rechecked. A different normalization changes absolute gain names.

## 8. hazop_lopa_sil_band_mapping

- Canonical topic/anchor: `hazop_lopa_ipl_risk_reduction_sil_target_allocation` / `hazop_lopa_sil_band_mapping`
- **Actual canonical statement:** Low-demand mode에서 목표 PFDavg를 표준의 SIL 구간에 대응시켜 목표 SIL을 정하며 SIL 1, 2, 3의 PFDavg 범위는 각각 10^-2 이상 10^-1 미만, 10^-3 이상 10^-2 미만, 10^-4 이상 10^-3 미만이다.
- Primary technical authority: Schneider Electric, Altivar Process Embedded Safety Function Manual EAV64334 (2019)
- Original publisher URL: https://iportal2.schneider-electric.com/Contents/docs/SQD-ATV630D15Y6_User%20guide.pdf
- Exact section/evidence method: SIL low demand PFDavg table, printed p.18; original indexed publisher PDF text, screenshot attempted but timed out
- Verdict: **KEEP_BOUNDED**
- Scope, assumptions and counterexample: IEC 61508 low-demand SIL1 PFDavg in [10^-2,10^-1), SIL2 [10^-3,10^-2), SIL3 [10^-4,10^-3), within relevant standard editions. PFDavg band alone does not establish overall SIL or high-demand PFH.


These checks complete 100 claim-level source comparisons in the present interactive response, but do not certify the remaining Queue, any source outside recorded limits, or full formal release validation. No physical source text is substituted by a model-generated version.