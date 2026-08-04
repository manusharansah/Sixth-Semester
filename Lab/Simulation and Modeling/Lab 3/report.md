# Lab Report

## Title
**Simulation and Modeling — Monte Carlo Simulation (Estimating π and an Average)**

**Name:** Manu Sharan Kumar
**Roll No:** ACE080BCT037

---

## Objectives

1. To use the Monte Carlo method to estimate the value of $\pi$ using random sampling.
2. To use the Monte Carlo method to estimate the average of a set of random numbers.
3. To observe how both estimates converge as the number of random samples increases (Law of Large Numbers).

---

## Theory

**Monte Carlo simulation** relies on repeated random sampling to obtain numerical results for problems that are difficult to solve analytically: define a domain of inputs, generate random samples from a distribution over it, perform a deterministic computation on each sample, then aggregate the results. By the **Law of Large Numbers**, as the number of samples $n \to \infty$, the sample average converges to the true expected value.

**Task 1 — Estimating π:** A circle of radius $r$ inscribed in a square of side $2r$ has area ratio $\frac{\pi r^2}{4r^2}=\frac{\pi}{4}$. Dropping $N$ random points uniformly in the square and counting $N_{in}$ that fall inside the circle gives $\pi \approx 4\times\frac{N_{in}}{N}$.

**Task 2 — Estimating an average:** For $n$ independent uniform random numbers, the sample mean $\bar{x}$ converges to the true expected value $\mathbb{E}[X]$ as $n$ increases.

---

## Task 1: Monte Carlo Estimation of π

"Raindrops" are dropped uniformly inside a $1\times1$ square ($x,y\in[-0.5,0.5]$) circumscribing a circle of radius $0.5$; a drop is "inside" if $x^2+y^2\le0.5^2$.

**Source Code (core logic):**
```python
def monte_carlo_pi(number_of_drops):
    count_in = 0
    for i in range(number_of_drops):
        x = random.uniform(-0.5, 0.5)
        y = random.uniform(-0.5, 0.5)
        if x**2 + y**2 <= 0.5**2:
            count_in += 1
        pi_history.append(4 * count_in / (i + 1))
    return count_in, ...
```

**Output** (with `random.seed(42)`, at increasing sample sizes):
```
N=1000    : pi estimated = 3.180000
N=10000   : pi estimated = 3.139200
N=100000  : pi estimated = 3.140280
Actual π  = 3.141593
```

A scatter plot marks in-circle drops in blue and out-of-circle drops in black, forming a visible circular boundary. A second plot of the running π-estimate against the number of drops shows the curve oscillating widely at first and settling closer to the true value of $\pi$ (dashed reference line) as more drops are added.

---

## Task 2: Monte Carlo Estimation of an Average

Random integers in $[1,9]$ are generated via `np.random.randint(1, 10)` (true expected average $=5.0$). For epoch $i$, $i+1$ random numbers are drawn and their running average recorded, over 10,000 epochs.

**Source Code (core logic):**
```python
for i in range(EPOCH):
    add = [np.random.randint(1, 10) for j in range(i + 1)]
    avg = np.mean(add)
    AVG.append(avg)
```

**Output** (representative run):
```
Running average at epoch 10   : 5.50
Running average at epoch 100  : 4.78
Running average at epoch 10000: 4.98
```

The plot of running average vs. epoch number shows large fluctuations for small sample sizes, which damp out and converge tightly around the true expected value of $5.0$ (dashed reference line) as the epoch count grows.

---

## Discussion

Task 1 used the Monte Carlo method to estimate π from the ratio of points landing inside a circle inscribed in a square. As the number of dropped points increased from 1,000 to 100,000, the estimate moved noticeably closer to the true value of π, and the running-estimate plot visibly stabilized rather than oscillating widely, matching the expected $1/\sqrt{N}$ reduction in sampling error. Task 2 used the same principle to estimate the mean of a discrete uniform distribution over $[1,9]$; the running average was volatile for the first few dozen epochs but converged tightly to 5.0 well before the 10,000th epoch. In both tasks, the underlying computation is deterministic (just averaging), but the *inputs* are randomly generated — this is the defining feature of a Monte Carlo method.

## Conclusion

Both experiments verify the **Law of Large Numbers**: increasing the sample size improves the accuracy and reliability of statistical estimates obtained purely from random sampling. The estimated π became increasingly stable, and the estimated average converged to its expected value, as more samples were used in each case.
