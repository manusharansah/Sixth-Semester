# Lab 2: Generation of Random Numbers using Pseudo-Random Number Generators and the Chi-Square Test

---

## 1. Objective

To understand how computers generate random numbers using **Pseudo-Random Number Generators (PRNGs)**, implement a generator algorithm from scratch (without using built-in library functions), and statistically validate the output using the **Chi-Square Test**.

---

## 2. What is a Random Number?

A random number is **a sequence of numbers chosen by chance**, such that no number is more predictable than any other.

### 2.1 Two Conditions for True Randomness

For a sequence to be considered statistically random, it must satisfy:

1. **Uniformity** — Values are uniformly distributed over a defined interval (every value in the range is equally likely to occur).
2. **Unpredictability** — It is impossible to predict a future value based on past or present values in the sequence.

> **Note:** Computers are deterministic machines, so they cannot generate *truly* random numbers from nothing. Instead, they generate **pseudo-random numbers** — numbers that *appear* random and pass statistical randomness tests, but are actually produced by a fixed, repeatable mathematical formula.

---

## 3. Algorithms to Generate Random Numbers

Three common categories of algorithms were introduced:

| Algorithm | Brief Description |
|---|---|
| **Linear Congruential Generator (LCG)** | Generates numbers using a simple linear recurrence relation (modulo arithmetic) |
| **XOR Shift Generator** | Uses bitwise XOR and shift operations on a binary seed value |
| **Mersenne Twister** | A more advanced, high-quality generator with a very long period (used in many modern libraries, e.g., Python's `random` module) |

The lab focuses primarily on the **Linear Congruential Generator (LCG)**.

---

## 4. Linear Congruential Generator (LCG)

### 4.1 Why LCG?

- **Simple to implement**
- **Minimal memory usage**
- **Faster** computation compared to more complex generators

### 4.2 Formula

The LCG recurrence relation is defined as:

$$X_{n+1} = (a \cdot X_n + c) \bmod m$$

### 4.3 Parameter Definitions

| Symbol | Constraint | Meaning |
|---|---|---|
| `m` | `0 < m` | The **modulus** — defines the range of generated values |
| `a` | `0 < a < m` | The **multiplier** |
| `c` | `0 ≤ c < m` | The **increment** |
| `X₀` | `0 ≤ X₀ < m` | The **seed** / starting value |
| `Xₙ₊₁` | — | The next generated value in the sequence |

### 4.4 How It Works (Explanation)

1. You pick a **seed** (`X₀`) — this is the starting point of the sequence.
2. Each new number `Xₙ₊₁` is calculated using the **previous number** `Xₙ`, multiplied by `a`, plus `c`, then taken modulo `m`.
3. Because the formula only depends on the previous value, the entire sequence is **fully determined by the seed**. The same seed will always reproduce the exact same sequence — this is why it's called *pseudo*-random rather than truly random.
4. The choice of `a`, `c`, and `m` strongly affects the **period** (how many numbers are generated before the sequence repeats) and the statistical quality of the output.

---

## 5. Validating Randomness: The Chi-Square Test

Since PRNGs generate numbers through a deterministic formula, we need a statistical test to check whether the output sequence still **behaves like a uniformly distributed random sample**. The **Chi-Square Test** is used for this validation.

### 5.1 Formula

$$\chi^2 = \sum_{i=0}^{n} \frac{(O_i - E_i)^2}{E_i}$$

### 5.2 Variable Definitions

| Symbol | Meaning |
|---|---|
| `Oᵢ` | **Observed** frequency — how many times a value/interval actually occurred in the generated data |
| `Eᵢ` | **Expected** frequency — how many times a value/interval should occur if the distribution were perfectly uniform |
| `n` | The number of categories/intervals being compared |

### 5.3 How It Works (Explanation)

1. Divide the range of generated numbers into equal intervals (bins).
2. Count how many generated numbers actually fall into each bin → this is `Oᵢ`.
3. Calculate how many numbers *should* fall into each bin if the distribution were perfectly uniform → this is `Eᵢ`.
4. For each bin, compute `(Oᵢ - Eᵢ)² / Eᵢ`, then sum across all bins to get `χ²`.
5. **Interpretation:**
   - A **small χ² value** → observed data closely matches expected uniform distribution → generator is statistically good.
   - A **large χ² value** → significant deviation from uniformity → generator may be biased or flawed.
   - The calculated χ² is typically compared against a **critical value** from chi-square distribution tables (based on degrees of freedom and chosen significance level, e.g., 0.05) to formally accept or reject the "randomness" hypothesis.

---

## 6. Real-World Applications of Random Number Generation

* **Cryptography** — generating keys, nonces, and salts that must be unpredictable to ensure security
* **Machine Learning** — random initialization of weights, shuffling datasets, train/test splitting
* **Simulation** — modeling stochastic/probabilistic real-world systems (e.g., queueing, Monte Carlo methods)

---

## 7. Task for Today (Lab Assignment)

**Goal:** Build a simulation of a random number generator.

**Requirements:**

1. Implement **random state / seed generation**:
   - Clearly document the **methodology** used to compute the seed.
   - Do **NOT** use any built-in random number library functions — implement the logic manually.
   - **Show the computation of the seed in full detail** (step-by-step), not just the final value.
2. Use the seed in your own implementation of an algorithm (e.g., LCG) to generate a sequence of pseudo-random numbers.
3. (Implied next step) Apply the **Chi-Square Test** to statistically validate that your generated sequence is uniformly distributed.

---

## 8. Summary

| Concept | Key Takeaway |
|---|---|
| Random Number | Must be uniformly distributed and unpredictable |
| PRNG | Deterministic formula that mimics randomness; same seed → same sequence |
| LCG | Simple, fast, low-memory; `Xₙ₊₁ = (aXₙ + c) mod m` |
| Chi-Square Test | Statistical check comparing observed vs. expected frequencies to validate uniformity |
| Today's Task | Manually implement seed generation + PRNG algorithm without libraries |