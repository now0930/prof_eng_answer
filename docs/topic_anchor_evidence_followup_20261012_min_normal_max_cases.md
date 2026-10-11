# Minimum/normal/maximum valve sizing cases Anchor 근거 검토 (2026-10-12)

## 결과

`control_valve_selection_process_pressure_temperature_flow_media_lifecycle`의
`minimum_normal_maximum_cases`는 이번 검토에서 **미검증으로 유지**한다. Anchor는 minimum,
normal, maximum case를 각각의 동시 pressure drop, fluid property, required travel 및 control
objective와 함께 평가하라고 한다.

## 확인 근거와 한계

- Emerson Fisher Specification Manager Quick Start Guide D103533X012, Valve Sizing:
  Minimum/Normal/Maximum/Others를 service conditions로 구분하고, flow, inlet pressure,
  differential pressure, temperature, specific gravity/viscosity 및 compressible-flow 변수를
  조건별 입력으로 제시한다. 이는 sizing 입력을 여러 case로 관리하는 점은 지지한다.
  [원문](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/d103533x012.pdf)
- Emerson DVC7K-H instruction manual D104767X012의 Service Conditions는 maximum,
  normal 및 minimum flow rate를 각각 설명한다. 이 제품 설명만으로 전체 control-valve sizing
  방법이나 required travel 기준을 일반화할 수는 없다.
  [원문](https://www.emerson.com/is/content/emerson/en/final-control/flow-controls/documents/instruction-manual-fisher-fieldvue-dvc7k-h-digital-valve-controller-en.pdf)
- Emerson Control Valve Sizing guidance는 적절한 sizing을 위해 process condition과 fluid
  property 입력이 필요하다고 설명한다. 그러나 현재 확보한 자료는 Anchor가 결합한 모든 case에서
  required travel 및 control objective를 어떻게 산정·판정해야 하는지, 또는 특정 travel 목표가
  보편적인지 직접 정하지 않는다.
  [원문](https://www.emerson.com/en/final-control/catalog/products-and-software/valves/control-valves/control-valves-sizing)

## 판정 및 후속 조치

복수 운전조건을 sizing에 반영하는 부분은 제조사 자료로 확인되지만, Anchor 전체 문구의 required
travel·control objective 연결은 충분히 직접 입증되지 않았다. 이 부분을 보편 규칙으로 verified
하지 않는다. IEC 60534-2-1/ANSI-ISA-75.01.01의 적용 조항 또는 실제 project sizing procedure에서
case별 required travel과 control objective의 명시적 관계를 확인하거나, Anchor를 근거가 확인된
case별 sizing-input 사실로 축소한 뒤 다시 검토한다.

이번 검토는 근거와 미해결 사유만 기록했다. Topic Pack 문구와 점수 계약은 변경하지 않았다.
