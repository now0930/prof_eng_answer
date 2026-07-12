# 저항·정전용량·인덕턴스형 센서의 물성·기하 변환 원리

## 1. Topic 기본정보

- Topic ID: `passive_sensor_resistive_capacitive_inductive_transduction`
- 문제 유형: `PRINCIPLE`
- 난이도: `THEORY_CORE`
- 선택 중요도: `CORE_MUST_PREPARE`
- 평가 방식: `LLM_ONLY`
- 결정론적 검사: 비활성화
- 작성 기준일: 2026-07-12

## 2. 출제 범위

저항형, 정전용량형, 인덕턴스형 센서가 외부 측정량을 전기적
파라미터 변화로 변환하는 원리를 다룬다.

외부 힘, 압력, 변위, 온도, 습도 또는 대상체의 재료 특성은 센서의
기하학적 치수 또는 재료 물성을 변화시킨다. 이 변화는 각각 저항
`R`, 정전용량 `C`, 인덕턴스 `L`의 변화로 나타난다.

센서 자체의 `R`, `C`, `L` 변화는 외부 여기회로와 신호조절회로를
통해 전압, 전류, 위상, 전하, 임피던스 또는 주파수 신호로 변환된다.

다음 세 가지 재료 물성을 중심으로 정리한다.

- 저항형 센서: 도전율 `kappa` 또는 비저항 `rho`
- 정전용량형 센서: 유전율 `epsilon`
- 인덕턴스형 센서: 투자율 `mu`

Young's modulus `E`는 전기적 물성이 아니라 외부 힘이나 압력과
기하학적 변형을 연결하는 기계적 물성으로 다룬다.

## 3. 통합 변환 사슬

수동형 파라미터 센서의 기본 변환 사슬은 다음과 같다.

    측정량
    -> 응력·변위·온도·재료 상태 변화
    -> 기하학적 변화 또는 재료 물성 변화
    -> Delta R, Delta C, Delta L
    -> 여기 및 신호조절
    -> 전압, 전류, 임피던스, 위상, 주파수

핵심 원칙은 다음과 같다.

- 센서는 측정량을 먼저 `R`, `C`, `L` 변화로 변환한다.
- 수동형 센서는 일반적으로 외부 전기적 여기가 필요하다.
- 출력 전압이나 전류는 센서소자와 신호조절회로의 결합 결과다.
- 센서 감도는 기계적 감도, 파라미터 감도와 회로 감도의 곱으로
  해석할 수 있다.
- 기하학적 변화와 재료 물성 변화를 구분해야 한다.

## 4. 기본 기계 관계

기계적 응력과 변형률은 다음과 같다.

    sigma_m = F / A_m

    epsilon_m = Delta l / l

선형 탄성영역에서 Young's modulus는 다음과 같다.

    E = sigma_m / epsilon_m

따라서 다음 관계가 성립한다.

    epsilon_m = sigma_m / E

- `sigma_m`: 기계적 응력
- `epsilon_m`: 변형률
- `E`: Young's modulus
- `F`: 힘
- `A_m`: 힘이 작용하는 단면적
- `l`: 초기 길이
- `Delta l`: 길이 변화

Young's modulus가 크면 같은 응력에서 변형률이 작다. Young's
modulus가 작으면 같은 응력에서 변형률이 크다.

Young's modulus는 다음 변환 단계에 관여한다.

    힘·압력
    -> 응력
    -> 변형률·변위
    -> Delta l, Delta A, Delta d, Delta g
    -> Delta R, Delta C, Delta L

## 5. Fact Anchor 요구사항

### A01 — `sensor_passive_transduction_chain`

저항형, 정전용량형, 인덕턴스형 센서는 측정량을 직접 디지털 값으로
변환하는 것이 아니라 먼저 `R`, `C`, `L`의 파라미터 변화로 변환하고,
외부 여기 및 신호조절회로를 통해 전압·전류·주파수 등의 신호로
검출한다.

필수 내용:

- 측정량과 전기적 출력 사이에 기계적 또는 재료적 변환단계가 있다.
- 센서소자와 신호조절회로의 역할을 구분한다.
- 수동형 파라미터 센서는 일반적으로 외부 여기가 필요하다.
- 출력은 전압뿐 아니라 전류, 위상, 임피던스, 전하 또는 주파수일 수
  있다.

### A02 — `sensor_mechanical_stress_strain_youngs_modulus`

Young's modulus는 외부 힘이나 압력에 의해 발생하는 응력과 변형률을
연결하는 기계적 물성이다.

    sigma_m = F / A_m
    epsilon_m = Delta l / l
    E = sigma_m / epsilon_m

필수 내용:

- `E`는 전기저항, 유전율 또는 투자율이 아니다.
- 같은 응력에서 `E`가 크면 변형이 작다.
- 기계적 변형이 전기적 파라미터 변화의 입력이 된다.
- 탄성영역과 선형 근사의 적용범위를 언급한다.
- 다이어프램과 빔에서는 형상, 두께와 경계조건도 변형을 결정한다.

### A03 — `sensor_resistive_geometry_conductivity_relation`

균일한 도체의 저항은 길이, 단면적과 재료의 비저항 또는 도전율에
의해 결정된다.

    R = rho l / A
    R = l / (kappa A)

- `rho`: 비저항
- `kappa`: 도전율
- `l`: 도체 길이
- `A`: 전류 통과 단면적

저항의 미소 변화율은 다음과 같이 표현할 수 있다.

    Delta R / R
    = Delta rho / rho
      + Delta l / l
      - Delta A / A

또는 다음과 같다.

    Delta R / R
    = -Delta kappa / kappa
      + Delta l / l
      - Delta A / A

필수 내용:

- 길이와 단면적 변화는 기하학적 효과다.
- 비저항 또는 도전율 변화는 재료 물성 효과다.
- 온도, 변형과 재료상태가 도전율에 영향을 줄 수 있다.
- 저항이 길이에만 의존한다고 설명하지 않는다.

### A04 — `sensor_resistive_strain_gauge_factor`

스트레인 게이지에서 축방향 변형률과 Poisson ratio를 고려하면 다음
근사를 사용할 수 있다.

    Delta l / l = epsilon_m

    Delta A / A
    approximately -2 nu epsilon_m

따라서 다음과 같다.

    Delta R / R
    approximately
    (1 + 2 nu) epsilon_m
    + Delta rho / rho

Gauge factor는 다음과 같다.

    GF = (Delta R / R) / epsilon_m

필수 내용:

- Gauge factor는 기하학적 효과와 압저항 효과를 함께 포함한다.
- 금속 게이지와 반도체 압저항 센서의 주요 효과가 다를 수 있다.
- 변형률이 작다는 전제에서 선형화한 관계임을 설명한다.
- 온도에 의한 저항 변화와 기계적 변형을 구분한다.

### A05 — `sensor_resistive_voltage_current_conversion`

저항 변화는 정전류, 정전압 또는 브리지 회로로 전압과 전류 변화로
변환한다.

정전류 여기에서는 다음과 같다.

    V = I R

    Delta V = I Delta R

정전압 여기에서는 다음과 같다.

    I = V / R

필수 내용:

- 작은 저항 변화에는 Wheatstone bridge가 널리 사용된다.
- quarter, half, full bridge는 감도와 온도보상 특성이 다르다.
- 여기전압 증가 시 출력은 증가하지만 자기발열도 증가할 수 있다.
- 리드선 저항, 접촉저항과 온도계수를 검토한다.

### A06 — `sensor_capacitive_geometry_permittivity_relation`

평행판 근사에서 정전용량은 유전율, 전극 중첩면적과 전극 간격에 의해
결정된다.

    C = epsilon A / d

    epsilon = epsilon_0 epsilon_r

- `epsilon`: 유전율 또는 permittivity
- `epsilon_0`: 진공 유전율
- `epsilon_r`: 비유전율
- `A`: 전극 중첩면적
- `d`: 전극 간격

정전용량 변화율은 다음과 같다.

    Delta C / C
    =
    Delta epsilon / epsilon
    + Delta A / A
    - Delta d / d

필수 내용:

- 면적과 간격 변화는 기하학적 효과다.
- 유전율 변화는 재료 물성 효과다.
- 압력센서는 다이어프램 변형에 따른 간격 변화를 이용할 수 있다.
- 습도와 액위센서는 유전율 또는 유전체 분포 변화를 이용할 수 있다.
- fringe field와 기생 정전용량을 검토한다.

### A07 — `sensor_capacitive_dynamic_current_readout`

정전용량형 센서는 전하, 전류, 임피던스, 충·방전 시간 또는
발진주파수 변화로 읽을 수 있다.

    q = C V

시간에 따라 `C`와 `V`가 변하면 다음과 같다.

    i = dq / dt
      = C dV/dt + V dC/dt

정현파 여기에서 이상적 정전용량 임피던스는 다음과 같다.

    Z_C = 1 / (j omega C)

    |I| = omega C |V|

필수 내용:

- 정전용량 자체와 측정회로의 출력 전압을 구분한다.
- AC bridge, charge amplifier, capacitance-to-digital converter 또는
  oscillator를 사용할 수 있다.
- 기생 정전용량, 케이블과 차폐의 영향을 설명한다.
- 고임피던스 입력에서 누설과 오염의 영향을 고려한다.

### A08 — `sensor_inductive_magnetic_circuit_permeability_relation`

자기회로의 자기저항과 인덕턴스는 다음과 같이 표현할 수 있다.

    R_m = l_m / (mu A)

    L = N^2 / R_m

단순 자기회로에서는 다음과 같이 근사할 수 있다.

    L approximately mu N^2 A / l_m

- `R_m`: 자기저항
- `mu`: 투자율 또는 permeability
- `N`: 권수
- `A`: 자속 통과 단면적
- `l_m`: 자기회로 유효 길이

필수 내용:

- 투자율은 자속 형성과 자기저항에 영향을 준다.
- 면적과 자기회로 길이는 기하학적 변수다.
- 코어의 포화, 히스테리시스와 주파수 의존성을 검토한다.
- 인덕턴스가 권수만으로 결정된다고 설명하지 않는다.

### A09 — `sensor_inductive_gap_eddy_current_conductivity`

가변 릴럭턴스형 센서에서는 공극이 자기저항과 인덕턴스에 큰 영향을
준다.

    R_g = g / (mu_0 A)

- `g`: 공극 길이
- `R_g`: 공극 자기저항

공극이 증가하면 일반적으로 총 자기저항이 증가하고 인덕턴스가
감소한다.

와전류 센서에서는 대상체의 도전율, 투자율, 두께, 주파수와 코일 간
거리가 코일의 복소 임피던스에 영향을 준다.

    Z = R_loss + j omega L

필수 내용:

- 유도형 위치센서와 와전류 센서의 원리를 구분한다.
- 와전류가 반대 방향 자기장을 만들어 코일 임피던스를 변화시킨다.
- 대상체 도전율 `kappa`와 투자율 `mu`가 함께 작용할 수 있다.
- skin depth와 주파수의 영향을 고려한다.

### A10 — `sensor_inductive_voltage_impedance_readout`

자속쇄교량과 코일 전압은 다음과 같다.

    lambda = L i

    v = d lambda / dt

인덕턴스가 시간에 따라 변하면 다음과 같다.

    v = L di/dt + i dL/dt

정현파 정상상태에서 이상적 인덕터 임피던스는 다음과 같다.

    Z_L = j omega L

필수 내용:

- 인덕턴스 변화는 전압, 전류, 위상, 임피던스 또는 공진주파수로
  검출할 수 있다.
- LVDT는 상호인덕턴스와 차동 전압을 이용한다.
- 코일저항과 철손 때문에 실제 임피던스는 순수 `j omega L`이 아니다.
- AC excitation, demodulation과 phase-sensitive detection을
  설명한다.

### A11 — `sensor_material_property_geometry_separation`

세 센서의 기본 전기 파라미터는 재료 물성과 기하학적 변수의 조합으로
결정된다.

    R = l / (kappa A)

    C = epsilon A / d

    L approximately mu N^2 A / l_m

따라서 다음 대응이 성립한다.

- 저항 `R`과 도전율 `kappa`
- 정전용량 `C`와 유전율 `epsilon`
- 인덕턴스 `L`과 투자율 `mu`

필수 내용:

- `kappa`, `epsilon`, `mu`는 서로 다른 물리량이다.
- 길이, 면적, 간격과 공극은 기하학적 변수다.
- Young's modulus는 기계적 변형을 결정하는 물성이다.
- 하나의 센서에서는 물성과 기하 변화가 동시에 발생할 수 있다.
- 온도와 환경변수에 의한 교차감도를 고려한다.

### A12 — `sensor_rcl_excitation_signal_conditioning`

수동형 `R`, `C`, `L` 센서는 외부 여기를 사용하여 파라미터 변화를
측정 가능한 전기신호로 변환한다.

대표 여기와 신호조절 방식은 다음과 같다.

- 저항형: DC 또는 AC bridge, 정전류, instrumentation amplifier
- 정전용량형: AC bridge, charge amplifier, oscillator, CDC
- 인덕턴스형: AC bridge, oscillator, synchronous demodulator

필수 내용:

- 여기원 안정도가 측정 정확도에 영향을 준다.
- ratiometric 측정은 여기변동 영향을 줄일 수 있다.
- 증폭, 필터링, 복조, 선형화와 A/D 변환이 필요할 수 있다.
- 센서소자와 전체 계측채널의 전달특성을 구분한다.
- 접지, 차폐, 절연과 EMC를 검토한다.

### A13 — `sensor_rcl_sensitivity_linearity_environment`

센서의 전체 감도는 측정량에서 기계적 변형, 전기 파라미터와 출력
신호로 이어지는 각 단계의 감도를 곱하여 해석할 수 있다.

    S_total
    =
    d(output) / d(measurand)

또는 다음과 같이 분해할 수 있다.

    S_total
    =
    d(output) / d(parameter)
    *
    d(parameter) / d(geometry or property)
    *
    d(geometry or property) / d(measurand)

필수 내용:

- 감도와 정확도, 분해능, 선형성은 동일하지 않다.
- 지나치게 높은 감도는 범위, 포화, 잡음과 안정성을 악화시킬 수 있다.
- 온도, 습도, 주파수, 재료 aging과 설치조건을 검토한다.
- 히스테리시스, creep, 반복성과 영점변화를 평가한다.
- Young's modulus와 구조강성은 감도와 측정범위의 상충관계에
  영향을 준다.

### A14 — `sensor_rcl_calibration_implementation_validation`

최종 센서 시스템은 `R`, `C`, `L` 변화만 계산하는 것이 아니라
기계구조, 물성, 여기회로와 신호처리를 포함하여 교정하고 검증해야
한다.

필수 내용:

- 입력 측정량과 출력 전압·전류·주파수 사이의 교정곡선을 구한다.
- 영점, span, 선형성, 반복성, 히스테리시스와 온도특성을 검증한다.
- 기준기와 추적성을 확보한다.
- 다점교정과 불확도 평가를 수행한다.
- 설치 후 배선, 기생성분, 차폐와 접지를 확인한다.
- 정적 특성과 동적 응답을 모두 검증한다.
- 장기 drift, 재교정 주기와 고장진단을 고려한다.

## 6. 세 센서의 통합 비교

| 구분 | 저항형 | 정전용량형 | 인덕턴스형 |
|---|---|---|---|
| 기본 파라미터 | `R` | `C` | `L` 또는 복소 임피던스 |
| 기본식 | `R=l/(kappa A)` | `C=epsilon A/d` | `L approximately mu N^2A/l_m` |
| 핵심 물성 | 도전율 `kappa` | 유전율 `epsilon` | 투자율 `mu` |
| 핵심 기하 | 길이·단면적 | 면적·간격 | 면적·자기회로 길이·공극 |
| 주요 출력 | 전압·전류 | 전하·전류·주파수 | 전압·전류·위상·임피던스 |
| 주요 여기 | DC·AC bridge | AC·charge excitation | AC excitation |
| 대표 센서 | strain gauge, RTD | 압력·변위·습도 | LVDT, 근접·와전류 |
| 주요 오차 | 자기발열·리드선 | 기생용량·누설 | 히스테리시스·철손·공극 |

## 7. Fatal Wrong Claim 요구사항

### F01 — `sensor_fatal_direct_voltage_without_excitation`

잘못된 주장:

저항형, 정전용량형, 인덕턴스형 수동센서는 외부 여기나
신호조절회로 없이 측정량에 비례한 전압을 스스로 직접 발생한다.

정확한 기준:

수동형 파라미터 센서는 먼저 `R`, `C`, `L`을 변화시키며, 일반적으로
외부 여기와 신호조절회로를 통해 전압, 전류 또는 주파수로 읽는다.

### F02 — `sensor_fatal_youngs_modulus_electrical_property`

잘못된 주장:

Young's modulus는 도전율, 유전율 또는 투자율과 같은 전기적 물성으로
`R`, `C`, `L`을 직접 결정한다.

정확한 기준:

Young's modulus는 응력과 변형률을 연결하는 기계적 물성이며,
기하학적 변형을 통해 간접적으로 `R`, `C`, `L` 변화에 영향을 준다.

### F03 — `sensor_fatal_resistance_length_only`

잘못된 주장:

도체의 저항은 길이에만 의존하며 단면적과 도전율 또는 비저항은
영향을 주지 않는다.

정확한 기준:

저항은 `R=l/(kappa A)=rho l/A`로 표현되며 길이, 단면적과 재료의
도전율 또는 비저항에 의해 결정된다.

### F04 — `sensor_fatal_capacitance_ignores_permittivity_gap`

잘못된 주장:

정전용량은 전극면적만으로 결정되며 유전율과 전극 간격은 영향을
주지 않는다.

정확한 기준:

평행판 근사에서 `C=epsilon A/d`이므로 유전율, 중첩면적과 간격이
모두 정전용량을 결정한다.

### F05 — `sensor_fatal_inductance_ignores_gap_permeability`

잘못된 주장:

인덕턴스는 코일 권수만으로 결정되며 코어 투자율, 자속면적,
자기회로 길이와 공극은 영향을 주지 않는다.

정확한 기준:

인덕턴스는 자기저항의 역수에 비례하며 투자율, 권수, 자속면적,
자기회로 길이와 공극의 영향을 받는다.

### F06 — `sensor_fatal_material_properties_identical`

잘못된 주장:

도전율, 유전율과 투자율은 이름만 다른 동일한 물리량이므로
`R`, `C`, `L` 식에서 서로 바꾸어 사용할 수 있다.

정확한 기준:

도전율은 전하전도, 유전율은 전기장 에너지 저장, 투자율은 자기장
형성과 관련된 서로 다른 물리량이다.

### F07 — `sensor_fatal_sensitivity_always_better`

잘못된 주장:

센서의 기계적 또는 전기적 감도는 높을수록 측정범위, 선형성, 잡음,
안정성과 관계없이 항상 우수하다.

정확한 기준:

감도 증가는 작은 입력 검출에 유리하지만 범위, 포화, 잡음,
비선형성, 구조강도와 안정성 사이의 상충관계를 가진다.

### F08 — `sensor_fatal_parameter_change_equals_measurand`

잘못된 주장:

`Delta R`, `Delta C`, `Delta L`은 교정, 여기회로와 환경보상 없이
항상 외부 측정량과 동일한 값이다.

정확한 기준:

파라미터 변화는 물성, 기하, 온도와 회로특성의 영향을 받으므로
측정량과 출력 사이의 전달관계를 교정하고 보상해야 한다.

## 8. 권장 답안 구조

### O01 — 수동형 센서의 통합 변환 사슬

측정량이 기계적 변형 또는 재료 물성 변화를 거쳐 `R`, `C`, `L`로
변환되고, 여기회로를 통해 전기신호로 출력되는 전체 구조를 설명한다.

참조 Anchor:

- `sensor_passive_transduction_chain`
- `sensor_mechanical_stress_strain_youngs_modulus`

### O02 — 저항형 센서의 물성과 기하학

`R=l/(kappa A)`를 기준으로 길이, 단면적, 도전율과 비저항 변화를
설명한다.

참조 Anchor:

- `sensor_resistive_geometry_conductivity_relation`
- `sensor_resistive_strain_gauge_factor`

### O03 — 저항 변화의 전압·전류 변환

정전류·정전압 여기와 Wheatstone bridge를 이용한 저항 변화 검출을
설명한다.

참조 Anchor:

- `sensor_resistive_voltage_current_conversion`

### O04 — 정전용량형 센서의 물성과 기하학

`C=epsilon A/d`를 기준으로 유전율, 전극면적과 간격 변화를 설명한다.

참조 Anchor:

- `sensor_capacitive_geometry_permittivity_relation`
- `sensor_capacitive_dynamic_current_readout`

### O05 — 인덕턴스형 센서의 자기회로

자기저항, 투자율, 권수, 자속면적, 자기회로 길이와 공극이
인덕턴스에 미치는 영향을 설명한다.

참조 Anchor:

- `sensor_inductive_magnetic_circuit_permeability_relation`
- `sensor_inductive_gap_eddy_current_conductivity`

### O06 — 인덕턴스 변화의 전기적 검출

코일 전압, 임피던스, 위상, 공진주파수와 LVDT·와전류 신호검출을
설명한다.

참조 Anchor:

- `sensor_inductive_voltage_impedance_readout`

### O07 — 재료 물성·기하·신호조절의 통합

도전율, 유전율, 투자율과 Young's modulus의 역할을 구분하고
여기·증폭·복조·필터링을 설명한다.

참조 Anchor:

- `sensor_material_property_geometry_separation`
- `sensor_rcl_excitation_signal_conditioning`

### O08 — 감도·오차·교정과 현장 검증

감도, 선형성, 환경영향, 교정, 설치와 동적응답을 종합 평가한다.

참조 Anchor:

- `sensor_rcl_sensitivity_linearity_environment`
- `sensor_rcl_calibration_implementation_validation`

## 9. 고득점 해제조건

### H01 — 통합 변환 사슬

측정량에서 기계변형·물성변화, `R·C·L`, 여기회로와 전기출력까지의
단계를 명확히 구분한다.

### H02 — Young's modulus의 정확한 위치

Young's modulus를 전기적 물성이 아니라 응력과 변형을 연결하는
기계적 물성으로 설명한다.

### H03 — 저항형 센서의 물성·기하 분해

`R=l/(kappa A)`와 저항 변화율을 사용하여 길이, 단면적과 도전율
변화를 분리한다.

### H04 — 정전용량형 센서의 세 변화요소

`C=epsilon A/d`를 기준으로 유전율, 면적과 간격 변화의 역할을
설명한다.

### H05 — 인덕턴스형 센서의 자기회로

자기저항, 투자율, 공극과 와전류 대상체의 도전율 영향을 설명한다.

### H06 — 전압·전류·임피던스 변환

각 센서 파라미터 변화가 여기 및 신호조절을 통해 전압, 전류,
위상 또는 주파수로 변환되는 원리를 설명한다.

### H07 — 감도와 실제 성능의 상충관계

감도, 측정범위, 선형성, 잡음, 포화, 온도와 구조강성의 상충관계를
설명한다.

### H08 — 교정과 구현 검증

다점교정, 불확도, 기생성분, 설치환경, 동적응답과 장기 drift를
종합 검증한다.

## 10. Source Topic Pack 작성 계약

후속 Source Topic Pack은 다음 파일로 구성한다.

- `README.md`
- `fact_anchor.json`
- `logic_check.json`
- `model_answer.json`
- `topic_importance.json`

필수 수량:

- Fact Anchor: 14개
- Fatal Wrong Claim: 8개
- 권장 답안 구조: 8개
- 고득점 해제조건: 8개

추가 원칙:

- 모든 ID는 이 문서에 정의된 전역 고유 ID를 사용한다.
- 결정론적 검사는 비활성화한다.
- candidate extraction rule은 비워 둔다.
- 공식의 단순 누락이나 기호 차이만으로 Fatal 처리하지 않는다.
- 물성, 기하와 회로의 역할을 조건 없이 반대로 설명한 경우를 Fatal
  후보로 판정한다.
- `dielectricity`보다 공학적으로 표준적인 `permittivity`, 즉 유전율을
  사용한다.
- 기계적 응력 기호와 전기전도도 기호가 혼동되지 않도록 응력은
  `sigma_m`, 도전율은 `kappa`로 구분한다.
- 이상적인 `R`, `C`, `L` 식과 실제 센서의 기생성분·비선형성을
  구분한다.
