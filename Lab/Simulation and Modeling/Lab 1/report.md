# Lab Report

## Title
**Simulation and Modeling of Chemical Reaction Kinetics using Euler's Method**

**Name:** Manu Sharan Kumar
**Roll No:** ACE080BCT037

---

## Objectives

1. To simulate the time evolution of several reacting systems using numerical (Euler-method) integration of their rate equations.
2. To visualize how reactant and product concentrations change with time and approach equilibrium/steady state.
3. To apply the same numerical approach across different domains — chemistry, industrial process engineering, pharmacology, and astrophysics.

---

## Theory

**Chemical kinetics** studies the rate at which reactions occur. For an elementary reaction $aA + bB \rightarrow cC$, the rate law is $\text{Rate} = k[A]^a[B]^b$, where $k$ is the rate constant.

Most reacting systems are governed by coupled, non-linear ordinary differential equations (ODEs) with no closed-form solution. **Euler's Method** approximates the solution by discretizing time into small steps $\Delta t$ and updating each concentration as:

$$ y_{n+1} = y_n + \frac{dy}{dt}\Big|_{n} \cdot \Delta t $$

Four systems were simulated using this scheme:
1. A reversible second-order reaction $A + B \rightleftharpoons 2C$.
2. The Haber–Bosch ammonia synthesis, $N_2 + 3H_2 \rightleftharpoons 2NH_3$.
3. A two-compartment pharmacokinetic (drug absorption/elimination) model.
4. A simplified nuclear fusion (hydrogen → helium) model.

---

## Reaction 1: Reversible Reaction $A + B \rightleftharpoons 2C$

The net forward rate is $r = k_f[A][B] - k_b[C]^2$, giving $\frac{d[A]}{dt}=-r$, $\frac{d[B]}{dt}=-r$, $\frac{d[C]}{dt}=+2r$. Starting from $[A]_0=50$, $[B]_0=25$, $[C]_0=0$ mol, with $k_f=0.05$, $k_b=0.001$, $\Delta t=0.01$ s over 300 steps ($t=3$ s):

**Source Code (core update loop):**
```python
r = k_f * c1[i] * c2[i] - k_b * c3[i]**2
dc1 = -r
dc2 = -r
dc3 = 2 * r
c1_next = max(0.0, c1[i] + dc1 * dt)
c2_next = max(0.0, c2[i] + dc2 * dt)
c3_next = max(0.0, c3[i] + dc3 * dt)
```

**Output:**
```
Initial concentrations : [A]=50.0, [B]=25.0, [C]=0.0
Final concentrations   : [A]=26.75, [B]=1.75, [C]=46.50
```

The concentration-vs-time plot shows $[A]$ and $[B]$ falling while $[C]$ rises, flattening out as the system approaches equilibrium ($r \to 0$).

---

## Reaction 2: Haber–Bosch Ammonia Synthesis

$N_2 + 3H_2 \rightleftharpoons 2NH_3$, with $k_f=0.0002$, $k_b=0.005$, $\Delta t=0.1$ s, 150 steps. Starting concentrations: $N_2=40$, $H_2=100$, $NH_3=0$ mol/L. Per unit $N_2$ consumed, 3 units of $H_2$ are consumed and 2 units of $NH_3$ produced; the run is also logged to `industrial_reactor_log.txt`.

**Output:**
```
Final concentrations: N2=31.56 mol/L, H2=74.67 mol/L, NH3=16.89 mol/L
```

The plot shows $N_2$ and $H_2$ depleting while $NH_3$ climbs and levels off at the equilibrium yield (~16.9 mol/L).

---

## Reaction 3: Pharmacokinetic Simulation (Oral Single Dose)

A drug moves between the gut, bloodstream, and peripheral tissue:

$$ \frac{dA_{gut}}{dt} = -k_a A_{gut},\quad \frac{dA_{blood}}{dt} = k_a A_{gut} - k_{12}A_{blood} + k_{21}A_{peripheral} - k_e A_{blood},\quad \frac{dA_{peripheral}}{dt} = k_{12}A_{blood} - k_{21}A_{peripheral} $$

With $k_a=0.5$, $k_{12}=0.2$, $k_{21}=0.1$, $k_e=0.15$, a 100 mg oral dose, $\Delta t=0.1$ h over 24 h (240 steps):

**Output:**
```
Peak plasma concentration: 45.46 mg at t = 2.5 h
Final plasma concentration at 24h: 7.63 mg
Final peripheral concentration at 24h: 23.88 mg
```

The plot overlays the Minimum Effective Concentration (MEC = 15) and Toxic Threshold (46), showing plasma concentration entering the safe therapeutic band shortly after dosing and staying just under the toxic limit at its peak, before decaying below the MEC later in the day.

---

## Reaction 4: Nuclear Fusion (Hydrogen → Helium)

Fusion rate is modeled as strongly non-linear: $\text{fusion\_rate} = k_{fusion}[H]^2$, with $\Delta H = -4\cdot\text{fusion\_rate}\cdot\Delta t$ and $\Delta He = +1\cdot\text{fusion\_rate}\cdot\Delta t$. Using $k_{fusion}=0.0005$, $\Delta t=0.5$, 200 steps, starting at 100% hydrogen:

**Output:**
```
Final Hydrogen fuel remaining: 4.69%
Final Helium ash accumulated : 23.83%
```

The plot shows hydrogen fuel dropping sharply at first (rate $\propto [H]^2$) then tailing off slowly as fuel becomes scarce, while helium ash accumulates in a mirrored curve.

---

## Discussion

Four reacting systems were simulated numerically using Euler's method. Reaction 1 showed a simple reversible reaction settling into equilibrium ($[A]\approx27$, $[B]\approx2$, $[C]\approx47$ mol). Reaction 2 modeled industrial ammonia synthesis, with $N_2$ and $H_2$ being consumed while $NH_3$ accumulated toward an equilibrium yield. Reaction 3 modeled drug pharmacokinetics across gut, blood, and tissue compartments, highlighting the safe therapeutic range between the MEC and toxic threshold. Reaction 4 modeled stellar hydrogen fusion, showing highly non-linear fuel depletion since the rate scales with $[H]^2$. Across all four systems, using a sufficiently small time step $\Delta t$ was essential — too large a step would cause the linear (first-order) Euler approximation to overshoot and produce unstable or negative concentrations, which is why a `max(0.0, ...)` clamp was used defensively in each update.

## Conclusion

Euler-method numerical simulation provides a simple but effective way to study the time evolution of coupled, non-linear rate equations across very different domains — chemistry, industrial process engineering, pharmacology, and astrophysics — all using the same underlying approach: discretize time, compute instantaneous rates, and update concentrations step by step.
