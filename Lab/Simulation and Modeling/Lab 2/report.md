# Lab Report

## Title
**Generation of Random Numbers using Pseudo-Random Number Generator (LCG) and Validation using the Chi-Square Test**

---

## Objectives

1. To understand the concept of random numbers and conditions for statistical randomness.
2. To implement a **Linear Congruential Generator (LCG)** without using built-in random libraries.
3. To implement the **Chi-Square Test** manually to validate uniformity of generated numbers.
4. To scale up the generator and test it on a larger sample, comparing the result to a critical value.

---

## Theory

A random number is a sequence of numbers chosen by chance, satisfying two conditions: **uniformity** (values equally likely over an interval) and **unpredictability** (future values can't be guessed from past ones). Computers are deterministic, so they generate **pseudo-random numbers** using a fixed formula that statistically mimics randomness.

**Linear Congruential Generator (LCG):**
$$X_{n+1} = (a \cdot X_n + c) \bmod m$$
where `m` = modulus, `a` = multiplier, `c` = increment, `X₀` = seed.

**Chi-Square Test:** validates whether generated numbers are uniformly distributed by comparing observed (`Oᵢ`) vs expected (`Eᵢ`) frequencies across bins:
$$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$$
A small χ² (below the critical value for a chosen significance level and degrees of freedom) means the generator passes the uniformity test.

---

## Part A: Basic LCG (20 numbers)

**Source Code:**
```python
# Linear Congruential Generator
m = 16
a = 5
c = 3
seed = 7

x = seed
for i in range(20):
    x = (a * x + c) % m
    r = x / m
    print(f"{i+1:2d}: State={x:2d} Random={r:.4f}")
```

**Output:**
```
 1: State= 6 Random=0.3750
 2: State= 1 Random=0.0625
 3: State= 8 Random=0.5000
 4: State=11 Random=0.6875
 5: State=10 Random=0.6250
 6: State= 5 Random=0.3125
 7: State=12 Random=0.7500
 8: State=15 Random=0.9375
 9: State=14 Random=0.8750
10: State= 9 Random=0.5625
11: State= 0 Random=0.0000
12: State= 3 Random=0.1875
13: State= 2 Random=0.1250
14: State=13 Random=0.8125
15: State= 4 Random=0.2500
16: State= 7 Random=0.4375
17: State= 6 Random=0.3750   ← sequence repeats from here
18: State= 1 Random=0.0625
19: State= 8 Random=0.5000
20: State=11 Random=0.6875
```
With `m=16`, the generator has a period of 16 — the sequence repeats starting at step 17 (matching step 1).

---

## Part B: Chi-Square Test on the Same LCG (20 numbers, manual)

**Source Code:**
```python
# LCG parameters
m = 16   # modulus
a = 5    # multiplier
c = 3    # increment
x = 7    # seed (X0)

bins = [0] * 10
for _ in range(20):
    x = (a * x + c) % m
    r = x / m
    index = int(r * 10)
    if index == 10:
        index = 9
    bins[index] += 1

print("Observed (O_i):", bins)

# ---- Chi-Square Test (computed manually, no library) ----
n = 20
k = len(bins)
expected = n / k

chi_square = 0
for o in bins:
    chi_square += ((o - expected) ** 2) / expected

print("Expected (E_i) per bin:", expected)
print("Chi-square value:", chi_square)
```

**Output:**
```
Observed (O_i): [3, 2, 1, 3, 1, 3, 3, 1, 2, 1]
Expected (E_i) per bin: 2.0
Chi-square value: 4.0
```

---

## Part C: Scaled-Up Version (256 numbers, using `scipy` for the critical value)

To check randomness more robustly, the sample size was increased to 256, with 8 bins, and the result compared against a proper critical value.

**Source Code:**
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

iterator = 256   # numbers to generate
a, b, p = 29, 37, 256   # multiplier, increment, modulus
n = 8            # number of bins
x02 = 0
critical_value = chi2.ppf(1 - 0.05, df=n - 1)   # 95th percentile, df=7

r = np.ones(iterator, dtype=int)
ei = iterator / n
c = np.zeros(n, dtype=int)
r[0] = 17   # seed

for i in range(iterator - 1):
    r[i + 1] = (r[i] * a + b) % p

for i in range(iterator):
    c[min(r[i] // 32, n - 1)] += 1   # bin width = 32

for i in range(n):
    x02 += ((c[i] - ei) ** 2) / ei

print("Bin frequencies (c):", c)
print("Chi-square statistic:", x02)
print("Critical value:", critical_value)
print("Chi square test passed" if x02 <= critical_value else "Chi square test failed")

plt.plot(r)
plt.xlabel("Index"); plt.ylabel("Random Number")
plt.title("LCG Generated Sequence")
plt.show()
```

> **Note:** Two bugs from the original draft were corrected here: `chi2.pdf` → `chi2.ppf` (critical value needs the inverse CDF, not the density), and `(c[i]-ei)*2` → `(c[i]-ei)**2` (the formula requires squaring, not doubling).

**Output:**
```
Bin frequencies (c): [32 32 32 32 32 32 32 32]
Chi-square statistic: 0.0
Critical value: 14.067140449340169
Chi square test passed
```

The plot showed a jagged, non-repeating pattern across all 256 points, with no visible trend.

---

## Discussion

We learned that an LCG can be implemented entirely without external random libraries, using only the recurrence formula and a chosen seed. In Part A, with a small modulus (`m=16`), the sequence repeated after exactly 16 steps, showing that **period length is tied directly to `m`** — a generator can never produce more distinct values than its modulus allows. In Part B, applying the Chi-Square test manually on just 20 numbers gave χ² = 4.0, which is low relative to typical critical values, suggesting reasonable uniformity even at small sample size, though 20 numbers spread across 10 bins is too small a sample to draw a strong conclusion from. It was observed that scaling up to 256 numbers (Part C) with carefully chosen parameters produced a **full-period sequence**, giving perfectly equal bin frequencies and a Chi-Square statistic of exactly 0.0 — clearly passing against the critical value of 14.067. This showed us that larger samples give a much more reliable randomness check than smaller ones. We came to know that small coding errors, like confusing a density function with a percentile function, or multiplication with squaring, can silently give an incorrect statistic or critical value, so verifying each formula against its mathematical definition before trusting any output really matters.

## Conclusion

This lab showed that pseudo-random numbers can be generated and statistically validated without relying on built-in libraries. We concluded that the choice of `a`, `c`, and `m` strongly affects both the period and uniformity of an LCG, that larger sample sizes give more trustworthy Chi-Square results, and that the Chi-Square test overall is a reliable, simple way to confirm whether a generated sequence behaves uniformly.