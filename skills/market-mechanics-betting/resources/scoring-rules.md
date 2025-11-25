# Scoring Rules and Calibration

Comprehensive guide to proper scoring rules, calibration measurement, and forecast accuracy improvement.

## Table of Contents

1. [Proper Scoring Rules](#1-proper-scoring-rules)
2. [Brier Score Deep Dive](#2-brier-score-deep-dive)
3. [Log Score](#3-log-score-logarithmic-scoring-rule)
4. [Calibration Curves](#4-calibration-curves)
5. [Resolution Analysis](#5-resolution-analysis)
6. [Sharpness](#6-sharpness)
7. [Practical Calibration Training](#7-practical-calibration-training)
8. [Comparison Table](#8-comparison-table-of-scoring-rules)

---

## 1. Proper Scoring Rules

### What is a Scoring Rule?

A **scoring rule** assigns a numerical score to a probabilistic forecast based on the forecast and actual outcome.

**Purpose:** Measure accuracy, incentivize honesty, enable comparison, track calibration over time.

### Strictly Proper vs Quasi-Proper

**Strictly Proper:** Reporting your true belief uniquely maximizes your expected score. No other probability gives better expected score.

**Why it matters:** Incentivizes honesty, eliminates gaming, optimizes for accurate beliefs.

**Quasi-Proper:** True belief maximizes score, but other probabilities might tie. Less desirable for forecasting.

### Common Proper Scoring Rules

**1. Brier Score** (strictly proper)
```
Score = -(p - o)²
p = Your probability (0 to 1)
o = Outcome (0 or 1)
```

**2. Logarithmic Score** (strictly proper)
```
Score = log(p) if outcome occurs
Score = log(1-p) if outcome doesn't occur
```

**3. Spherical Score** (strictly proper)
```
Score = p / √(p² + (1-p)²) if outcome occurs
```

### Common IMPROPER Scoring Rules (Avoid)

**Absolute Error:** `Score = -|p - o|` → Incentivizes extremes (NOT proper)

**Threshold Accuracy:** Binary right/wrong → Ignores calibration (NOT proper)

**Example of gaming improper rules:**
```
Using absolute error (improper):
True belief: 60% → Optimal report: 100% (dishonest)

Using Brier score (proper):
True belief: 60% → Optimal report: 60% (honest)
```

**Key Principle:** Only use strictly proper scoring rules for forecast evaluation.

---

## 2. Brier Score Deep Dive

### Formula

**Single forecast:** `Brier = (p - o)²`

**Multiple forecasts:** `Brier = (1/N) × Σ(pi - oi)²`

**Range:** 0.00 (perfect) to 1.00 (worst). Lower is better.

### Calculation Examples

```
90% Yes → (0.90-1)² = 0.01 (good) | 90% No → (0.90-0)² = 0.81 (bad)
60% Yes → (0.60-1)² = 0.16 (medium) | 50% Any → 0.25 (baseline)
```

### Brier Score Decomposition

**Murphy Decomposition:**
```
Brier Score = Reliability - Resolution + Uncertainty
```

**Reliability (Calibration Error):** Are your probabilities correct on average? (Lower is better)

**Resolution:** Do you assign different probabilities to different outcomes? (Higher is better)

**Uncertainty:** Base rate variance (uncontrollable, depends on problem)

**Improving Brier:**
1. Minimize reliability (fix calibration)
2. Maximize resolution (differentiate forecasts)

### Brier Score Interpretation

| Brier Score | Quality | Description |
|-------------|---------|-------------|
| 0.00 - 0.05 | Exceptional | Near-perfect |
| 0.05 - 0.10 | Excellent | Top tier |
| 0.10 - 0.15 | Good | Skilled |
| 0.15 - 0.20 | Average | Better than random |
| 0.20 - 0.25 | Below Average | Approaching random |
| 0.25+ | Poor | At or worse than random |

**Context matters:** Easy questions expect lower scores. Compare to baseline (0.25) and other forecasters.

### Improving Your Brier Score

**Path 1: Fix Calibration**

**If overconfident:** 80% predictions happen 60% → Be less extreme, widen intervals

**If underconfident:** 60% predictions happen 80% → Be more extreme when you have evidence

**Path 2: Improve Resolution**

**Problem:** All forecasts near 50% → Differentiate easy vs hard questions, research more, be bold when warranted

**Balance:** `Good Forecaster = Well-Calibrated + High Resolution`

### Brier Skill Score

```
BSS = 1 - (Your Brier / Baseline Brier)

Example:
Your Brier: 0.12, Baseline: 0.25
BSS = 1 - 0.48 = 0.52 (52% improvement over baseline)
```

**Interpretation:** BSS = 1.00 (perfect), 0.00 (same as baseline), <0 (worse than baseline)

---

## 3. Log Score (Logarithmic Scoring Rule)

### Formula

```
Log Score = log₂(p) if outcome occurs
Log Score = log₂(1-p) if outcome doesn't occur

Range: -∞ (worst) to 0 (perfect)
Higher (less negative) is better
```

### Calculation Examples

```
90% Yes → -0.15 | 90% No → -3.32 (severe) | 50% Yes → -1.00
99% No → -6.64 (catastrophic penalty for overconfidence)
```

### Relationship to Information Theory

**Log score measures bits of surprise:**
```
Surprise = -log₂(p)

p = 50% → 1 bit surprise
p = 25% → 2 bits surprise
p = 12.5% → 3 bits surprise
```

**Connection to entropy:** Log score equals cross-entropy between forecast distribution and true outcome.

### When to Use Log Score vs Brier

**Use Log Score when:**
- Severe penalty for overconfidence desired
- Tail risk matters (rare events important)
- Information-theoretic interpretation useful
- Comparing probabilistic models

**Use Brier Score when:**
- Human forecasters (less punishing)
- Easier interpretation (squared error)
- Standard benchmark (more common)
- Avoiding extreme penalties

**Key Difference:**

Brier: Quadratic penalty (grows with square)
```
Error: 10% → 0.01, 20% → 0.04, 30% → 0.09, 40% → 0.16
```

Log: Logarithmic penalty (grows faster for extremes)
```
Forecast: 90% wrong → -3.3, 95% wrong → -4.3, 99% wrong → -6.6
```

**Recommendation:** Default to Brier. Add Log for high-stakes or to penalize overconfidence. Track both for complete picture.

---

## 4. Calibration Curves

### What is a Calibration Curve?

**Visualization of forecast accuracy:**
```
Y-axis: Actual frequency (how often outcome occurred)
X-axis: Stated probability (your forecasts)
Perfect calibration: Diagonal line (y = x)
```

**Example:**
```
Actual %
   100 ┤                             ╱
    80 ┤                       ●
    60 ┤               ●
    40 ┤       ●               ← Perfect calibration line
    20 ┤ ●
     0 └───────────────────────
       0    20   40   60   80  100
            Stated probability %
```

### How to Create

**Step 1:** Collect 50+ forecasts and outcomes

**Step 2:** Bin by probability (0-10%, 10-20%, ..., 90-100%)

**Step 3:** For each bin, calculate actual frequency
```
Example: 60-70% bin
Forecasts: 15 total, Outcomes: 9 Yes, 6 No
Actual frequency: 9/15 = 60%
Plot point: (65, 60)
```

**Step 4:** Draw perfect calibration line (diagonal from (0,0) to (100,100))

**Step 5:** Compare points to line

### Over/Under Confidence Detection

**Overconfidence:** Points below diagonal (said 90%, happened 70%). Fix: Be less extreme, widen intervals.

**Underconfidence:** Points above diagonal (said 90%, happened 95%). Fix: Be more extreme when evidence is strong.

**Sample size:** <10/bin unreliable, 10-20 weak, 20-50 moderate, 50+ strong evidence

---

## 5. Resolution Analysis

### What is Resolution?

**Resolution** measures ability to assign different probabilities to outcomes that actually differ.

**High resolution:** Events you call 90% happen much more than events you call 10% (good)

**Low resolution:** All forecasts near 50%, can't discriminate (bad)

### Formula

```
Resolution = (1/N) × Σ nk(ok - ō)²

nk = Forecasts in bin k
ok = Actual frequency in bin k
ō = Overall base rate

Higher is better
```

### How to Improve Resolution

**Problem: Stuck at 50%**

Bad pattern: All forecasts 48-52% → Low resolution

Good pattern: Range from 20% to 90% → High resolution

**Strategies:**

1. **Gather discriminating information** - Find features that distinguish outcomes
2. **Use decomposition** - Fermi, causal models, scenarios
3. **Be bold when warranted** - If evidence strong → Say 85% not 65%
4. **Update with evidence** - Start with base rate, update with Bayesian reasoning

### Calibration vs Resolution Tradeoff

```
Perfect Calibration Only: Say 60% for everything when base rate is 60%
  → Calibration: Perfect
  → Resolution: Zero
  → Brier: 0.24 (bad)

High Resolution Only: Say 10% or 90% (extremes) incorrectly
  → Calibration: Poor
  → Resolution: High
  → Brier: Terrible

Optimal Balance: Well-calibrated AND high resolution
  → Calibration: Good
  → Resolution: High
  → Brier: Minimized
```

**Best forecasters:** Well-calibrated (low reliability error) + High resolution (discriminate events) = Low Brier

**Recommendation:** Don't sacrifice resolution for perfect calibration. Be bold when evidence warrants.

---

## 6. Sharpness

### What is Sharpness?

**Sharpness** = Tendency to make extreme predictions (away from 50%) when appropriate.

**Sharp:** Predicts 5% or 95% when evidence supports it (decisive)

**Unsharp:** Stays near 50% (plays it safe, indecisive)

### Why Sharpness Matters

```
Scenario: Base rate 60%

Unsharp forecaster: 50% for every event → Brier: 0.24, Usefulness: Low
Sharp forecaster: Range 20-90% → Brier: 0.12 (if calibrated), Usefulness: High
```

**Insight:** Extreme predictions (when accurate) improve Brier significantly. When wrong, hurt badly. Solution: Be sharp when you have evidence.

### Measuring Sharpness

```
Sharpness = Variance of forecast probabilities

Forecaster A: [0.45, 0.50, 0.48, 0.52, 0.49] → Var = 0.0007 (unsharp)
Forecaster B: [0.15, 0.85, 0.30, 0.90, 0.20] → Var = 0.1150 (sharp)
```

### When to Be Sharp

**Be sharp (extreme probabilities) when:**
- Strong discriminating evidence (multiple independent pieces align)
- Easy questions (outcome nearly certain)
- You have expertise (domain knowledge, track record)

**Stay moderate (near 50%) when:**
- High uncertainty (limited information, conflicting evidence)
- Hard questions (true probability near 50%)
- No expertise (unfamiliar domain)

**Goal:** Sharp AND well-calibrated (extreme when warranted, accurate probabilities)

---

## 7. Practical Calibration Training

### Calibration Exercises

**Exercise Set 1:** Make 10 forecasts on verifiable questions (fair coin 50%, Paris capital 99%, two heads 25%, die shows 6 at 16.67%). Check: Did 99% come true 9-10 times? Did 50% come true ~5 times?

**Exercise Set 2:** Make 20 "80% confident" predictions. Expected: 16/20 correct. Common: 12-14/20 (overconfident). What feels "80%" should be reported as "65%".

### Tracking Methods

**Method 1: Spreadsheet**
```
| Date | Question | Prob | Outcome | Brier | Notes |
Monthly: Calculate mean Brier
Quarterly: Generate calibration curve
```

**Method 2: Apps**
- PredictionBook.com (free, tracks calibration)
- Metaculus.com (forecasting platform)
- Good Judgment Open (tournament)

**Method 3: Focused Practice**
- Week 1: Make 20 predictions (focus on honesty)
- Week 2: Check calibration curve (identify bias)
- Week 3: Increase resolution (be bold)
- Week 4: Balance calibration + resolution

### Training Drills

**Drill 1:** Generate 10 "90% CIs" for unknowns. Target: 9/10 contain true value. Common mistake: Only 5-7 (overconfident). Fix: Widen by 1.5×.

**Drill 2:** Bayesian practice - State prior, observe evidence, update posterior, check calibration.

**Drill 3:** Make 10 predictions >80% or <20%. Force extremes when "pretty sure". Track: Are >80% happening >80%?

---

## 8. Comparison Table of Scoring Rules

### Summary

| Feature | Brier | Log | Spherical | Threshold |
|---------|-------|-----|-----------|-----------|
| **Proper** | Strictly | Strictly | Strictly | NO |
| **Range** | 0 to 1 | -∞ to 0 | 0 to 1 | 0 to 1 |
| **Penalty** | Quadratic | Logarithmic | Moderate | None |
| **Interpretation** | Squared error | Bits surprise | Geometric | Binary |
| **Usage** | Default | High-stakes | Rare | Avoid |
| **Human-friendly** | Yes | Somewhat | No | Yes (misleading) |

### Detailed Comparison

**Brier Score**

Pros: Easy to interpret, standard in competitions, moderate penalty, good for humans

Cons: Less severe penalty for overconfidence

Best for: General forecasting, calibration training, standard benchmarking

**Log Score**

Pros: Severe penalty for overconfidence, information-theoretic, strongly incentivizes honesty

Cons: Too punishing for humans, infinite at 0%/100%, less intuitive

Best for: High-stakes forecasting, penalizing overconfidence, ML models, tail risk

**Spherical Score**

Pros: Strictly proper, bounded, geometric interpretation

Cons: Uncommon, complex formula, rarely used

Best for: Theoretical analysis only

**Threshold / Binary Accuracy**

Pros: Very intuitive, easy to explain

Cons: NOT proper (incentivizes extremes), ignores calibration, can be gamed

Best for: Nothing (don't use for forecasting)

### When to Use Each

| Your Situation | Recommended |
|----------------|-------------|
| Starting out | **Brier** |
| Experienced forecaster | **Brier** or **Log** |
| High-stakes decisions | **Log** |
| Comparing to benchmarks | **Brier** |
| Building ML model | **Log** |
| Personal tracking | **Brier** |
| Teaching others | **Brier** |

**Recommendation:** Use **Brier** as default. Add **Log** for high-stakes or to penalize overconfidence.

### Conversion Example

**Forecast: 80%, Outcome: Yes**
```
Brier: (0.80-1)² = 0.04
Log (base 2): log₂(0.80) = -0.322
Spherical: 0.80/√(0.80²+0.20²) = 0.971
```

**Forecast: 80%, Outcome: No**
```
Brier: (0.80-0)² = 0.64
Log (base 2): log₂(0.20) = -2.322 (much worse penalty)
Spherical: 0.20/√(0.80²+0.20²) = 0.243
```

---

## Return to Main Skill

[← Back to Market Mechanics & Betting](../SKILL.md)

**Related Resources:**
- [Betting Theory Fundamentals](betting-theory.md)
- [Kelly Criterion Deep Dive](kelly-criterion.md)

