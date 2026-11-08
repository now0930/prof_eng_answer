# PR #19 EMC Fact Anchor independent evidence review

- Review date: 2026-11-08
- Reviewer method: ChatGPT source-grounded technical comparison
- Status: REVIEW ONLY / NOT APPROVED
- Effect on scoring: NONE
- Original source and exclusions: UNCHANGED

## ipgse_scope_chain

- Current layer: `source_hold`
- Current reason: `insufficient_direct_primary_source_scope`
- Review decision: `KEEP_BOUNDED_CANDIDATE`
- Statement SHA256: `f019d484eec3fcce8f05e9e5661004fc0ecbc9842b61df68b7e87d8a90c5b145`
- Original statement: 계장 신호 간섭을 조사할 때는 가능한 간섭원(source), 결합경로(coupling path), 영향을 받는 신호·기기(victim)를 구분한다. 전원선, 기준전위·접지, 케이블·차폐 등은 현장에서 확인할 후보이며 실제 원인은 측정과 구성 확인으로 좁힌다.
- Source: NI Field Wiring, Minimizing Noise Coupling
- Source URL: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html
- Evidence locator: NI Field Wiring, Minimizing Noise Coupling
- Access date: 2026-11-08
- Supported scope: 간섭 경로와 실제 배선 구성 확인을 지지한다.
- Limitation: 특정 원인을 측정 없이 단정하지 않아야 한다.
- Candidate wording (not canonical): 간섭원, 결합경로, 피해 측정경로를 구분하고 실제 배선·접지·전원 구성과 측정으로 원인을 확인한다.
- Approval: PENDING

## ipgse_power_quality_scope

- Current layer: `source_hold`
- Current reason: `insufficient_direct_primary_source_scope`
- Review decision: `REVISE_SCOPE_CANDIDATE`
- Statement SHA256: `b97dd84dcd0de134afb442e86792ed03aaecc55ba3121524e1d92dfd723c7f8a`
- Original statement: 계장 전원 진단은 nominal voltage만 보지 않고 sag, swell, interruption, transient, harmonic/noise, frequency와 전원 source transfer 조건을 증상 시간대와 연계한다.
- Source: Fluke IEC 61000-4-30 Class A measurement overview
- Source URL: https://www.fluke.com/ko-kr/learn/blog/power-quality/what-does-the-iec-61000-4-30-class-a-standard-mean-to-me
- Evidence locator: Fluke IEC 61000-4-30 Class A measurement overview
- Access date: 2026-11-08
- Supported scope: 전압, 주파수, sag, swell, interruption, harmonic 측정 항목을 지지한다.
- Limitation: 계장 전원 전환과 증상 시점의 인과관계는 별도 현장 기록이 필요하다.
- Candidate wording (not canonical): 계장 전원 진단에서는 정격전압뿐 아니라 해당되는 전원품질 항목의 측정 기록을 증상 발생 시점 및 부하 운전조건과 비교한다.
- Approval: PENDING

## ipgse_emi_coupling_paths

- Current layer: `revision_hold`
- Current reason: `primary_source_revision_pending`
- Review decision: `KEEP_BOUNDED_REWORD_CANDIDATE`
- Statement SHA256: `09746202c9219cc4b954caa83581e8d0ebab0d0862e9107adced9b05b8743721`
- Original statement: EMI는 conducted, radiated, capacitive, inductive, common-impedance coupling으로 유입될 수 있으므로 source-path-victim 관점에서 경로를 식별한다.
- Source: NI Field Wiring, Noise Coupling Mechanisms
- Source URL: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html
- Evidence locator: NI Field Wiring, Noise Coupling Mechanisms
- Access date: 2026-11-08
- Supported scope: 전도성, 용량성, 유도성, 방사성 결합을 지지한다.
- Limitation: 공통 임피던스 결합은 전도성 결합과 중첩되는 분류이다.
- Candidate wording (not canonical): 대표적인 간섭 결합은 공통 임피던스를 통한 전도성, 전계를 통한 용량성, 자계를 통한 유도성 및 전자기 방사성 결합으로 설명할 수 있다.
- Approval: PENDING

## ipgse_diagnostic_workflow

- Current layer: `original_exclusion`
- Current reason: `noncore_detail`
- Review decision: `KEEP_NONCORE_EXCLUDED`
- Statement SHA256: `272da07e3d9c18c991a5aefe52213615cc972222678d9f1096226670b137c6f8`
- Original statement: 계장 신호 잡음의 원인을 찾을 때 FFT 등으로 주파수 특징을 살피고, 실제 배선·신호원·주변 설비를 조사한다. DAQ 단독 기준측정과 구성요소를 한 번에 하나씩 분리·비교하면 계측기·배선·신호원 후보를 구분하는 데 도움이 되며, 조치 후에는 원래 신호의 측정 조건과 성능을 다시 확인한다.
- Source: NI Diagnosing and Reducing Measurement Noise, Feb 4 2026
- Source URL: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/diagnosing-reducing-measurement-noise.html
- Evidence locator: NI Diagnosing and Reducing Measurement Noise, Feb 4 2026
- Access date: 2026-11-08
- Supported scope: FFT, 물리적 배선 조사, DAQ 기준 측정, 단계적 분리 진단을 지지한다.
- Limitation: FFT 및 특정 DAQ 시험이 모든 계장 문제의 필수 절차는 아니다.
- Candidate wording (not canonical): 증상과 신호 경로를 확인하고 필요에 따라 주파수 분석, 기준 측정 및 구성요소 분리 시험을 이용한다.
- Approval: PENDING

## ipgse_final_verification

- Current layer: `source_hold`
- Current reason: `insufficient_direct_primary_source_scope`
- Review decision: `REVISE_SCOPE_CANDIDATE`
- Statement SHA256: `7c12fdb514deee4dc66b08330596841345f58812d05f7c1aff185e415b0861fd`
- Original statement: 잡음 대책을 적용한 뒤에는 실제 적용에 적절하고 안전한 운전상태에서 신호 품질과 계측기 사양을 재확인하고, 변경 전 기준과 비교해 의도한 개선 및 부작용 여부를 점검한다. UPS transfer나 특정 noise-source on/off 시험은 설비 구성과 안전한 시험절차가 뒷받침될 때만 계획한다.
- Source: NI Field Wiring, Solving Noise Problems in Measurement Setups
- Source URL: https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/field-wiring-and-noise-considerations-for-analog-signals.html
- Evidence locator: NI Field Wiring, Solving Noise Problems in Measurement Setups
- Access date: 2026-11-08
- Supported scope: 기준 노이즈 측정과 계측기 사양 비교를 지지한다.
- Limitation: UPS 전환 및 노이즈 발생원 ON/OFF 시험은 별도의 위험평가와 절차가 필요하다.
- Candidate wording (not canonical): 조치 전후에 안전하고 비교 가능한 조건에서 신호 품질과 계측기 사양을 확인한다. 전원 전환 등 운전 시험은 별도 승인된 조건에서 수행한다.
- Approval: PENDING

## Release decision

- No Fact Anchor was promoted or unblocked.
- No Golden label or score range was changed.
- Existing EMC ABSTAIN remains required.
- Machine contract must not be created from excluded facts.
- Independent source review, canonical approval, and regression gates remain separate.
