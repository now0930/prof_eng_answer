# 제어밸브 가혹 운전: 고·저유량, 고온·저온·극저온 및 입자성 유체


## 1. Topic 정보

- Topic ID: `control_valve_severe_service_high_low_flow_temperature_cryogenic_particles`
- Primary: `COMPARE_SELECTION`
- Secondary: `IMPLEMENTATION_EVALUATION`
- Tertiary: `DIAGNOSIS_ACTION`
- Difficulty: `FIELD_APPLICATION`
- Importance: `CORE_MUST_PREPARE`

## 2. Severe-Service 정의

단일 threshold가 아니다.
Process condition, fluid property, valve geometry와 consequence의 복합 조건이다.
Minimum·normal·maximum과 transient case를 함께 검토한다.

## 3. High-Flow Service

Local velocity, kinetic energy와 hydraulic power를 확인한다.
Outlet jet와 downstream reducer·elbow를 포함한다.
Pressure staging은 energy concentration을 분산한다.

## 4. Flow와 Energy Proxy

$$v=\frac{Q}{A}$$
$$E_k=\frac{v^2}{2}$$
$$P_h=\Delta P\,Q$$
$$S_e=\rho v^3A$$
Hydraulic power와 erosive severity는 screening proxy이다.

## 5. Low-Flow·Micro-Flow

Catalog rangeability와 installed minimum controllable flow를 구분한다.
Small-orifice·needle·multi-hole trim의 resolution과 plugging을 비교한다.

## 6. Turndown과 Margin

$$R_i=\frac{Q_{\max}}{Q_{\min}}$$
$$M_m=\frac{Q_{\mathrm{available}}-Q_{\mathrm{required}}}{Q_{\mathrm{required}}}$$
분모는 양수이다.

## 7. High Temperature

Material strength, pressure derating, oxidation와 creep를 확인한다.
Packing·gasket·seat·coating compatibility를 별도 확인한다.
Thermal cycling과 heat soak를 포함한다.

## 8. Thermal Expansion

$$\Delta L=\alpha L\Delta T$$
$$\Delta L_{\mathrm{rel}}=(\alpha_1-\alpha_2)L\Delta T$$
Reference temperature, material coefficient와 sign convention을 명시한다.

## 9. Heat Leak

$$\dot Q=UA\Delta T$$
Steady-state approximation 조건을 명시한다.

## 10. Low Temperature·Cryogenic

Material toughness와 brittle fracture를 확인한다.
Thermal contraction, clearance와 sealing load를 확인한다.
Extended bonnet과 packing isolation을 검토한다.

## 11. Vaporization과 Cavity Pressure

$$x=\frac{\dot Q}{\dot m h_{fg}}$$
Heat leak, phase state와 approximation을 명시한다.
Trapped liquid warming과 relief path를 확인한다.

## 12. Icing·Insulation

Icing, condensation, cold-box와 insulation interface를 확인한다.

## 13. Particle Characterization

Size distribution, concentration, hardness, shape와 density를 확인한다.
Settling, agglomeration와 chemical behavior를 포함한다.

## 14. Stokes Settling Proxy

$$v_s=\frac{(\rho_p-\rho_f)gd^2}{18\mu}$$
Creeping-flow·dilute·spherical-particle 조건에서만 사용한다.

## 15. Slurry·Fibrous·Sticky Fluid

Slurry erosion과 impingement를 평가한다.
Fibrous bridging과 sticky·polymerizing deposit를 평가한다.

## 16. Geometry

| Geometry | 장점 | 주의점 |
|---|---|---|
| Full-port·rotary | Solids passage | Torque·shutoff trade-off |
| Angle·eccentric | Drainability·direction control | Installation 검토 |
| Cage·multi-hole | Staging·noise control | Particle blockage |

## 17. Material와 Surface

Hardfacing, coating, ceramic와 hardened alloy를 비교한다.
Impact, thermal shock, corrosion와 repairability를 확인한다.

## 18. Purge·Flushing

Purge medium, flow, pressure와 contamination을 정의한다.
Drain, vent와 clean-out access를 포함한다.

## 19. Corrosion와 Erosion

Corrosion은 chemical·electrochemical loss이다.
Erosion은 mechanical wear이다.
Erosion-corrosion은 상호작용이다.

## 20. Multiphase

Phase fraction, slip, compressibility와 vaporization uncertainty를 확인한다.
Single-phase prediction의 적용 한계를 명시한다.

## 21. Wear Trend

$$\Delta C=C_{\mathrm{current}}-C_{\mathrm{baseline}}$$
$$\dot C=\frac{C_2-C_1}{t_2-t_1}$$
같은 measurement method와 $t_2>t_1$을 사용한다.

## 22. Inspection·Maintenance

Wear point, clearance, coating, seat와 packing을 검사한다.
Diagnostics는 inspection을 대체하지 않는다.
Spare trim와 planned replacement를 준비한다.

## 23. Lifecycle Workflow

Specification → operating envelope → material review → sizing → geometry → vendor review → test → commissioning → maintenance → repair verification

## 24. Topic 경계

- Topic 1: Actuator thrust·fail-safe sizing
- Topic 3: Deadband·stiction·response
- Topic 4: General body·actuator type
- Topic 5: Authority·gain·rangeability
- Topic 6: Liquid Cv·Kv·Reynolds sizing
- Topic 7: Gas choked-flow sizing
- Topic 8: Cavitation·flashing
- Topic 9: Noise prediction·mitigation
- Topic 10: Balanced trim·seal mechanics
- Topic 12: Diagnostics·predictive maintenance
- Topic 13: Seat leakage·packing·emissions
- Topic 15: SIS·ESD·PST
- Topic 16: Full lifecycle·bid evaluation

## 25. 대표 오답

- Severe service는 하나의 threshold로 판정한다.
- Hydraulic power가 universal damage law이다.
- Catalog rangeability가 minimum controllable flow이다.
- Micro-flow trim은 plugging되지 않는다.
- Material strength는 temperature와 무관하다.
- Cryogenic은 viscosity만 고려한다.
- Hardfacing은 모든 erosion을 해결한다.
- Multi-hole trim은 모든 slurry에 최적이다.
- Stokes 식은 모든 particle에 적용된다.
- Diagnostics가 inspection을 대체한다.

## 26. 고득점 답안 기준

1. Combined operating envelope를 정의한다.
2. High-flow와 low-flow mechanism을 구분한다.
3. Velocity·power proxy와 적용 한계를 설명한다.
4. Micro-flow resolution·plugging trade-off를 설명한다.
5. High-temperature expansion·material·packing을 설명한다.
6. Cryogenic toughness·contraction·extended bonnet을 설명한다.
7. Particle·slurry·fibrous fluid를 구분한다.
8. Geometry·material·purge를 failure mechanism에 연결한다.
9. Inspection·spare·repair verification을 포함한다.
10. Topic 1·3·4·5·6·7·8·9·10·12·13·15·16 경계를 명시한다.
