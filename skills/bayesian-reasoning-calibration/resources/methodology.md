# Bayesian Reasoning & Calibration Methodology

## Table of Contents

- [When to Use This Methodology](#when-to-use-this-methodology)
- [Multiple Hypothesis Updates](#multiple-hypothesis-updates)
- [Sequential Evidence Updates](#sequential-evidence-updates)
- [Handling Dependent Evidence](#handling-dependent-evidence)
- [Calibration Techniques](#calibration-techniques)
- [Advanced Applications](#advanced-applications)

---

## When to Use This Methodology

Use this methodology for complex Bayesian reasoning cases:
- **Multiple competing hypotheses** (>2 hypotheses to update)
- **Sequential evidence** (multiple pieces of evidence over time)
- **Dependent evidence** (evidence items not independent)
- **Complex priors** (hierarchical or uncertain priors)
- **Calibration challenges** (checking for systematic biases)

For simple single-hypothesis updates, use `template.md` calculator.

---

## Multiple Hypothesis Updates

### Problem: Choosing Among Many Hypotheses

Often you have 3+ competing hypotheses and need to update all simultaneously.

**Example:**
- H1: Bug in payment processor code
- H2: Database connection timeout
- H3: Third-party API outage
- H4: DDoS attack

### Approach: Compute Posterior for Each Hypothesis

**Step 1: Assign prior probabilities** (must sum to 1)

| Hypothesis | Prior P(H) | Justification |
|------------|-----------|---------------|
| H1: Payment bug | 0.30 | Common issue, recent deploy |
| H2: DB timeout | 0.25 | Has happened before |
| H3: API outage | 0.20 | Dependency on external service |
| H4: DDoS | 0.10 | Rare but possible |
| H5: Other | 0.15 | Catch-all for unknowns |
| **Total** | **1.00** | Must sum to 1 |

**Step 2: Define likelihood for each hypothesis**

Evidence E: "500 errors only on payment endpoint"

| Hypothesis | P(E\|H) | Justification |
|------------|---------|---------------|
| H1: Payment bug | 0.80 | Bug would affect payment specifically |
| H2: DB timeout | 0.30 | Would affect multiple endpoints |
| H3: API outage | 0.70 | Payment uses external API |
| H4: DDoS | 0.50 | Could target any endpoint |
| H5: Other | 0.20 | Generic catch-all |

**Step 3: Compute P(E)** (marginal probability)

```
P(E) = Σ [P(E|Hi) × P(Hi)] for all hypotheses

P(E) = (0.80 × 0.30) + (0.30 × 0.25) + (0.70 × 0.20) + (0.50 × 0.10) + (0.20 × 0.15)
P(E) = 0.24 + 0.075 + 0.14 + 0.05 + 0.03
P(E) = 0.535
```

**Step 4: Compute posterior for each hypothesis**

```
P(Hi|E) = [P(E|Hi) × P(Hi)] / P(E)

P(H1|E) = (0.80 × 0.30) / 0.535 = 0.24 / 0.535 = 0.449 (44.9%)
P(H2|E) = (0.30 × 0.25) / 0.535 = 0.075 / 0.535 = 0.140 (14.0%)
P(H3|E) = (0.70 × 0.20) / 0.535 = 0.14 / 0.535 = 0.262 (26.2%)
P(H4|E) = (0.50 × 0.10) / 0.535 = 0.05 / 0.535 = 0.093 (9.3%)
P(H5|E) = (0.20 × 0.15) / 0.535 = 0.03 / 0.535 = 0.056 (5.6%)

Total: 100% (check: posteriors must sum to 1)
```

**Interpretation:**
- H1 (Payment bug): 30% → 44.9% (increased 15 pp)
- H3 (API outage): 20% → 26.2% (increased 6 pp)
- H2 (DB timeout): 25% → 14.0% (decreased 11 pp)
- H4 (DDoS): 10% → 9.3% (barely changed)

**Decision**: Investigate H1 (payment bug) first, then H3 (API outage) as backup.

---

## Sequential Evidence Updates

### Problem: Multiple Pieces of Evidence Over Time

Evidence comes in stages, need to update belief sequentially.

**Example:**
- Evidence 1: "500 errors on payment endpoint" (t=0)
- Evidence 2: "External API status page shows outage" (t+5 min)
- Evidence 3: "Our other services using same API also failing" (t+10 min)

### Approach: Chain Updates (Prior → E1 → E2 → E3)

**Step 1: Update with E1** (as above)
```
Prior → P(H|E1)
P(H1|E1) = 44.9% (payment bug)
P(H3|E1) = 26.2% (API outage)
```

**Step 2: Use posterior as new prior, update with E2**

Evidence E2: "External API status page shows outage"

New prior (from E1 posterior):
- P(H1) = 0.449 (payment bug)
- P(H3) = 0.262 (API outage)

Likelihoods given E2:
- P(E2|H1) = 0.20 (bug wouldn't cause external API status change)
- P(E2|H3) = 0.95 (API outage would definitely show on status page)

```
P(E2) = (0.20 × 0.449) + (0.95 × 0.262) = 0.0898 + 0.2489 = 0.3387

P(H1|E1,E2) = (0.20 × 0.449) / 0.3387 = 0.265 (26.5%)
P(H3|E1,E2) = (0.95 × 0.262) / 0.3387 = 0.698 (69.8%)
```

**Interpretation**: E2 strongly favors H3 (API outage). H1 dropped from 44.9% → 26.5%.

**Step 3: Update with E3**

Evidence E3: "Other services using same API also failing"

New prior:
- P(H1) = 0.265
- P(H3) = 0.698

Likelihoods:
- P(E3|H1) = 0.10 (payment bug wouldn't affect other services)
- P(E3|H3) = 0.99 (API outage would affect all services)

```
P(E3) = (0.10 × 0.265) + (0.99 × 0.698) = 0.0265 + 0.6910 = 0.7175

P(H1|E1,E2,E3) = (0.10 × 0.265) / 0.7175 = 0.037 (3.7%)
P(H3|E1,E2,E3) = (0.99 × 0.698) / 0.7175 = 0.963 (96.3%)
```

**Final conclusion**: 96.3% confidence it's API outage, not payment bug.

**Summary of belief evolution:**
```
        Prior   After E1   After E2   After E3
H1 (Bug):  30%  →  44.9%  →  26.5%  →   3.7%
H3 (API):  20%  →  26.2%  →  69.8%  →  96.3%
```

---

## Handling Dependent Evidence

### Problem: Evidence Items Not Independent

**Naive approach fails when**:
- E1 and E2 are correlated (not independent)
- Updating twice with same information

**Example of dependent evidence:**
- E1: "User reports payment failing"
- E2: "Another user reports payment failing"

If E1 and E2 are from same incident, they're not independent evidence!

### Solution 1: Treat as Single Evidence

If evidence is dependent, combine into one update:

**Instead of:**
- Update with E1: "User reports payment failing"
- Update with E2: "Another user reports payment failing"

**Do:**
- Single update with E: "Multiple users report payment failing"

Likelihood:
- P(E|Bug) = 0.90 (if bug exists, multiple users affected)
- P(E|No bug) = 0.05 (false reports rare)

### Solution 2: Conditional Likelihoods

If evidence is conditionally dependent (E2 depends on E1), use:

```
P(H|E1,E2) ∝ P(E2|E1,H) × P(E1|H) × P(H)
```

Not:
```
P(H|E1,E2) ≠ P(E2|H) × P(E1|H) × P(H)  ← Assumes independence
```

**Example:**
- E1: "Test fails on staging"
- E2: "Test fails on production" (same test, likely same cause)

Conditional:
- P(E2|E1, Bug) = 0.95 (if staging failed due to bug, production likely fails too)
- P(E2|E1, Env) = 0.20 (if staging failed due to environment, production different environment)

### Red Flags for Dependent Evidence

Watch out for:
- Multiple reports of same incident (count as one)
- Cascading failures (downstream failure caused by upstream)
- Repeated measurements of same thing (not new info)
- Evidence from same source (correlated errors)

**Principle**: Each update should provide **new information**. If E2 is predictable from E1, it's not independent.

---

## Calibration Techniques

### Problem: Over/Underconfidence Bias

Common patterns:
- **Overconfidence**: Stating 90% when true rate is 70%
- **Underconfidence**: Stating 60% when true rate is 80%

### Calibration Check: Track Predictions Over Time

**Method**:
1. Make many probabilistic forecasts (P=70%, P=40%, etc.)
2. Track outcomes
3. Group by confidence level
4. Compare stated probability to actual frequency

**Example calibration check:**

| Your Confidence | # Predictions | # Correct | Actual % | Calibration |
|-----------------|---------------|-----------|----------|-------------|
| 90-100% | 20 | 16 | 80% | Overconfident |
| 70-89% | 30 | 24 | 80% | Good |
| 50-69% | 25 | 14 | 56% | Good |
| 30-49% | 15 | 5 | 33% | Good |
| 0-29% | 10 | 2 | 20% | Good |

**Interpretation**: Overconfident at high confidence levels (saying 90% but only 80% correct).

### Calibration Curve

Plot stated probability vs actual frequency:

```
Actual %
    100 ┤                                    ●
        │                              ●
     80 ┤                        ●          (overconfident)
        │                  ●
     60 ┤            ●
        │      ●
     40 ┤ ●
        │
     20 ┤
        │
      0 └─────────────────────────────────
        0    20   40   60   80   100
              Stated probability %

Perfect calibration = diagonal line
Above line = overconfident
Below line = underconfident
```

### Debiasing Techniques

**For overconfidence:**
- Consider alternative explanations (how could I be wrong?)
- Base rate check (what's the typical success rate?)
- Pre-mortem: "It's 6 months from now and we failed. Why?"
- Confidence intervals: State range, not point estimate

**For underconfidence:**
- Review past successes (build evidence for confidence)
- Test predictions: Am I systematically too cautious?
- Cost of inaction: What's the cost of waiting for certainty?

### Brier Score (Calibration Metric)

**Formula**:
```
Brier Score = (1/n) × Σ (pi - oi)²

pi = stated probability for outcome i
oi = actual outcome (1 if happened, 0 if not)
```

**Example:**
```
Prediction 1: P=0.8, Outcome=1 → (0.8-1)² = 0.04
Prediction 2: P=0.6, Outcome=0 → (0.6-0)² = 0.36
Prediction 3: P=0.9, Outcome=1 → (0.9-1)² = 0.01

Brier Score = (0.04 + 0.36 + 0.01) / 3 = 0.137
```

**Interpretation:**
- 0.00 = perfect calibration
- 0.25 = random guessing
- Lower is better

**Typical scores:**
- Expert forecasters: 0.10-0.15
- Average people: 0.20-0.25
- Aim for: <0.15

---

## Advanced Applications

### Application 1: Hierarchical Priors

When you're uncertain about the prior itself.

**Example:**
- Question: "Will project finish on time?"
- Uncertain about base rate: "Do similar projects finish on time 30% or 60% of the time?"

**Approach**: Model uncertainty in prior

```
P(On time) = Weighted average of different base rates

Scenario 1: Base rate = 30% (if similar to past failures), Weight = 40%
Scenario 2: Base rate = 50% (if average project), Weight = 30%
Scenario 3: Base rate = 70% (if similar to past successes), Weight = 30%

Prior P(On time) = (0.30 × 0.40) + (0.50 × 0.30) + (0.70 × 0.30)
                  = 0.12 + 0.15 + 0.21
                  = 0.48 (48%)
```

Then update this 48% prior with evidence.

### Application 2: Bayesian Model Comparison

Compare which model/theory better explains data.

**Example:**
- Model A: "Bug in feature X"
- Model B: "Infrastructure issue"

Evidence: 10 data points

```
P(Model A|Data) / P(Model B|Data) = [P(Data|Model A) × P(Model A)] / [P(Data|Model B) × P(Model B)]
```

**Bayes Factor** = P(Data|Model A) / P(Data|Model B)

- BF > 10: Strong evidence for Model A
- BF = 3-10: Moderate evidence for Model A
- BF = 1: Equal evidence
- BF < 0.33: Evidence against Model A

### Application 3: Forecasting with Bayesian Updates

Use for repeated forecasting (elections, product launches, project timelines).

**Process:**
1. Start with base rate prior
2. Update weekly as new evidence arrives
3. Track belief evolution over time
4. Compare final forecast to outcome (calibration check)

**Example: Product launch success**

```
Week -8: Prior = 60% (base rate for similar launches)
Week -6: Beta feedback positive → Update to 70%
Week -4: Competitor launches similar product → Update to 55%
Week -2: Pre-orders exceed target → Update to 75%
Week 0: Launch → Actual success: Yes ✓

Forecast evolution: 60% → 70% → 55% → 75% → (Outcome: Yes)
```

**Calibration**: 75% final forecast, outcome=Yes. Good calibration if 7-8 out of 10 forecasts at 75% are correct.

---

## Quality Checklist for Complex Cases

**Multiple Hypotheses**:
- [ ] All hypotheses listed (including catch-all "Other")
- [ ] Priors sum to 1.0
- [ ] Likelihoods defined for all hypothesis-evidence pairs
- [ ] Posteriors sum to 1.0 (math check)
- [ ] Interpretation provided (which hypothesis favored? by how much?)

**Sequential Updates**:
- [ ] Evidence items clearly independent or conditional dependence noted
- [ ] Each update uses previous posterior as new prior
- [ ] Belief evolution tracked (how beliefs changed over time)
- [ ] Final conclusion integrates all evidence
- [ ] Timeline shows when each piece of evidence arrived

**Calibration**:
- [ ] Considered alternative explanations (not overconfident?)
- [ ] Checked against base rates (not ignoring priors?)
- [ ] Stated confidence interval or range (not just point estimate)
- [ ] Identified assumptions that could make forecast wrong
- [ ] Planned follow-up to track calibration (compare forecast to outcome)

**Minimum Standard for Complex Cases**:
- Multiple hypotheses: Score ≥ 4.0 on rubric
- High-stakes forecasts: Track calibration over 10+ predictions
