# Six Canonical Fact Anchor primary-source reviews (2026-11-01)

Each original `fact_anchor.json` statement was fetched and compared to the issuing organization's official source. Five assertions use official HTML and one uses an actually screenshotted manufacturer PDF page. Decisions are **KEEP_BOUNDED** only for the indicated engineering propositions, not blanket certifications. No Topic Pack source, generated bank, or scoring overlay was changed.

## 1. choked_flow_vaporization_and_damage_are_distinct_assessments

- Topic/anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `choked_vapor_damage_axes_separated`
- Exact canonical statement: Choked 여부, vapor formation 여부와 physical damage severity는 서로 다른 판정축이다.
- Primary publisher source: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation
- Locator: Definition, different physical effects of flow choking/cavitation
- Determination: KEEP_BOUNDED
- Scope and exception: Choked condition means further pressure drop does not increase flow at fixed inlet, whereas vapor creation and trim damage depend on local Pv, recovery, and erosion; distinguish mechanism from damage severity.

## 2. control_valve_pressure_recovers_after_vena_contracta

- Topic/anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `downstream_pressure_recovery`
- Exact canonical statement: Vena contracta 이후 일부 kinetic energy가 static pressure로 회복되어 pressure가 P2까지 상승한다.
- Primary publisher source: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation
- Locator: Definition: downstream bubble collapse when line pressure increases
- Determination: KEEP_BOUNDED
- Scope and exception: After local minimum pressure, partially recovered static pressure can increase toward downstream P2; extent varies with geometry and irreversible loss.

## 3. multistage_trim_can_limit_per_stage_pressure_drop_conditionally

- Topic/anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `pressure_drop_staging_prevention`
- Exact canonical statement: Series restriction 또는 multi-stage trim으로 pressure drop을 분할하면 각 stage의 local pressure가 Pv 아래로 과도하게 떨어지는 것을 줄일 수 있다.
- Primary publisher source: https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/D103036X012.pdf
- Locator: Fisher NotchFlo DST March 2026 product bulletin, p.1 (PDF index 1) image checked
- Determination: KEEP_BOUNDED
- Scope and exception: Multistage pressure reduction distributes differential across stages, mitigating local cavitation in properly sized liquid service; vendor trim specifics and stated allowable stage pressure drops are not universal.

## 4. persistent_flashing_can_erode_downstream_valve_surfaces

- Topic/anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `flashing_damage_mechanism`
- Exact canonical statement: Flashing은 persistent two-phase high-velocity jet와 liquid-droplet impact에 의해 downstream erosion을 유발할 수 있다.
- Primary publisher source: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/valve-flashing
- Locator: Understanding Flashing and Damage Potential
- Determination: KEEP_BOUNDED
- Scope and exception: When P2<Pv and liquid remains vaporized, fast liquid-vapor stream may erode valve and downstream wetted material; specific droplet-impact micro-mechanism or erosion rate is not established by this page.

## 5. sub_vapor_pressure_at_vena_contracta_forms_vapor

- Topic/anchor: `control_valve_cavitation_flashing_choked_flow_damage_prevention` / `vapor_formation_condition`
- Exact canonical statement: Pvc가 Pv보다 낮으면 local vapor formation이 시작될 수 있다.
- Primary publisher source: https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/severe-service-control-valves/cavitation
- Locator: Definition: vapor bubbles near vapor pressure
- Determination: KEEP_BOUNDED
- Scope and exception: If local pressure reaches or falls below fluid vapor pressure, vapor formation can begin; temperature/composition and actual local pressure determine threshold, downstream recovery decides collapse.

## 6. fat_does_not_prove_actual_site_installation_and_process_load

- Topic/anchor: `control_software_project_engineering_documents_fat_sat_commissioning_acceptance` / `sw10_fat_limit`
- Exact canonical statement: FAT는 Simulation과 I/O 모사를 활용할 수 있으나 실제 현장 배선, 설치환경, 공정 부하와 최종 인터페이스를 완전히 증명하지 못한다.
- Primary publisher source: https://www.isa.org/standards-and-publications/isa-standards/isa-105-standards
- Locator: ISA-105: FAT at vendor site and SAT/SIT after local integration; IEC 62381:2024 adoption
- Determination: KEEP_BOUNDED
- Scope and exception: Pre-delivery FAT may use simulation and cannot alone certify installed field wiring/site environment/integrated live process loads. Site testing and commissioning need separate scope.


These remain claim-specific review results. Engineering terms with different test/service conditions must not be merged into one scoring demand. Full release tests and score-path admission checks have not been run.