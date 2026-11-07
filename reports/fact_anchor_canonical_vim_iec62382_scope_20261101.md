# Five canonical boundary adjudications — VIM, IEC 62382, SFC and field procedures (2026-11-01)

Reviewed and cross-checked exact canonical statements with the identified authoritative original publication. **2 KEEP_BOUNDED and 3 HOLD**. HOLD means not verified; stay `NOT_PERFORMED` in audit. Scope-only/jurisdictional edition requirements and niche fixed test procedures are ineligible for generic mandatory exam scoring without a separate reviewed scoring exclusion and runtime regression. Reviewer GPT-6 (AI); review date 2026-11-01.

## 1. vim_distinguishes_resolution_repeatability_and_accuracy

- Canonical topic/anchor: `optical_laser_photoelectric_noncontact_measurement_tof_triangulation` / `accuracy_resolution_repeatability_boundary`
- **Original statement:** VIM에서 분해능은 측정량의 최소 변화 중 지시값에 감지 가능한 변화를 일으키는 크기이고, 반복도는 반복성 조건에서의 측정정밀도이며, 정확도는 측정값과 참값의 일치도이다. 정확도는 수치량으로 직접 표현되지 않으며 precision·repeatability와 같은 개념이 아니므로 세 지표를 혼용해서는 안 된다.
- Primary publisher/document: JCGM 200:2012 International Vocabulary of Metrology (VIM), 3rd ed., original BIPM publication
- URL: https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf
- Locator and original inspection method: Definitions 2.13 (measurement accuracy), 2.21 (repeatability), 4.14 (resolution); p.24 PDF page index 39 screenshot verified; other terms cross-checked via original extracted text
- Verdict: **KEEP_BOUNDED**
- Detailed validity or deficiency: Resolution is smallest detectable change in indication, repeatability is measurement precision under repeatability conditions, accuracy is non-numeric closeness to true value. Do not substitute precision/accuracy or turn conceptual accuracy directly into an SI-valued scalar.

## 2. iec62382_loop_check_scope_and_boundaries

- Canonical topic/anchor: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` / `sw10_loop_test`
- **Original statement:** Loop test는 해당 Loop의 현장 입력 또는 출력 종단에서 배선·I/O·스케일링·제어기·HMI까지 신호의 방향, 범위와 동작을 종단 간 확인한다. 폐루프 제어 Loop는 센서부터 제어기와 최종요소까지 확인하며, 최종요소가 없는 정보·감시 Loop는 해당 입력 종단까지 확인한다.
- Primary publisher/document: IEC 62382:2024, 3rd ed. 2024-08, official publicly accessible excerpt; IEC publication description
- URL: https://cdn.standards.iteh.ai/samples/104569/954e455763a94f98b5f16dce4ef31098/IEC-62382-2024.pdf
- Locator and original inspection method: Clauses 1.1, 4, 5.1.1 (public preview p.12) indexed text; screenshot attempted but timeout; publication https://webstore.iec.ch/en/publication/67573
- Verdict: **KEEP_BOUNDED**
- Detailed validity or deficiency: Loop check verifies installed loop hardware, field connections, I/O and required functions after construction before commissioning. The full sensor-to-controller/final element boundary varies by loop type; HMI and active process demonstration are not universal for every loop. This standard is specific to IEC 62382:2024, not a universal mandated checklist.

## 3. sw02_sfc_transition_is_boolean_condition_enabling_next_step

- Canonical topic/anchor: `control_logic_sequence_interlock_permissive_trip_state_transition_fail_safe` / `sw02_transition_guard`
- **Original statement:** Transition guard는 상태변화를 허용하는 논리조건이다. 기동·명령 기반 전이의 대표식은 Command AND 모든 필수 Permissive AND 필요한 선행 Feedback AND NOT Trip AND NOT Inhibit로 나타낼 수 있다. 자동 진행, 시간 유지 완료 또는 공정조건 도달 전이는 Command 없이 성립할 수 있으며, Feedback은 전이의 선행조건 또는 동작 완료 확인조건으로 구분한다.
- Primary publisher/document: PLCopen IEC 61131-3 FAQ, When SFC actions executed?
- URL: https://www.plcopen.org/standards/logic/iec-61131-3/faqs/
- Locator and original inspection method: SFC POU invocation, active step, transition true condition
- Verdict: **HOLD_NEEDS_CLAIM_SPECIFIC_GUARD_SOURCE**
- Detailed validity or deficiency: True transitions move steps; source does not establish full original Command AND Permissive AND feedback NOT Trip / NOT Inhibit generalized Boolean guard or all automatic cases. No source-matched verdict yet.

## 4. four_to_twenty_milliamp_repair_requires_end_to_end_reverification

- Canonical topic/anchor: `analog_current_loop_4_20ma_two_wire_active_passive_troubleshooting` / `acl_closed_loop_verification`
- **Original statement:** 복구 후에는 4·12·20 mA 주입값과 0·50·100% 표시, engineering-unit scaling, alarm·trip 방향을 끝단까지 재검증하고 복구 상태를 기록한다.
- Primary publisher/document: NI, Fundamentals, System Design and Setup for 4–20mA Current Loop
- URL: https://www.ni.com/en/shop/data-acquisition/fundamentals--system-design--and-setup-for-the-4-to-20-ma-curren.html
- Locator and original inspection method: Current loop components and signal/connection fundamentals
- Verdict: **HOLD_NONCORE_FIXED_TEST_SCRIPT**
- Detailed validity or deficiency: Original demands exact 4,12,20 mA post-repair injection and alarm/trip verification; this is project-specific testing procedure, NOT a universally necessary three-point technical fact. Must not be admitted as mandatory general scoring anchor solely from NI circuit fundamentals.

## 5. commissioning_uses_site_procedures_to_verify_installed_function

- Canonical topic/anchor: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` / `sw10_commissioning`
- **Original statement:** Commissioning은 안전조건과 승인된 절차 아래 Energization, 정적점검, Loop·기능시험, 단계별 기동, Tuning, 부하시험과 안정화 순으로 수행한다.
- Primary publisher/document: IEC 62382:2024, sections 1/4 precommissioning loop checks
- URL: https://webstore.iec.ch/en/publication/67573
- Locator and original inspection method: IEC 62382 public scope separates construction loop check from cold commissioning
- Verdict: **HOLD_NONCORE_FIXED_SEQUENCE**
- Detailed validity or deficiency: Original lists Energization→static checks→loop tests→start-up→tuning→load test→stabilization as fixed sequence. Actual process commissioning follows risk/site/project plan and stages can overlap. Public scope does not certify exact universal sequence.


No changes to canonical Topic Pack facts or generated banks, no source-approval workflow/test run. Original overlay and revision holds remain independent; no final runtime score admission implied.