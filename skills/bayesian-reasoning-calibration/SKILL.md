---
name: bayesian-reasoning-calibration
description: Use when making predictions or judgments under uncertainty and need to explicitly update beliefs with new evidence. Invoke when forecasting outcomes, evaluating probabilities, testing hypotheses, calibrating confidence, assessing risks with uncertain data, or avoiding overconfidence bias. Use when user mentions priors, likelihoods, Bayes theorem, probability updates, forecasting, calibration, or belief revision.
---

# Bayesian Reasoning & Calibration

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Bayesian Reasoning?](#what-is-bayesian-reasoning)
- [Workflow](#workflow)
  - [1. Define the Question](#1--define-the-question)
  - [2. Establish Prior Beliefs](#2--establish-prior-beliefs)
  - [3. Identify Evidence & Likelihoods](#3--identify-evidence--likelihoods)
  - [4. Calculate Posterior](#4--calculate-posterior)
  - [5. Calibrate & Document](#5--calibrate--document)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Apply Bayesian reasoning to systematically update probability estimates as new evidence arrives. This helps make better forecasts, avoid overconfidence, and explicitly show how beliefs should change with data.

## When to Use This Skill

- Making forecasts or predictions with uncertainty
- Updating beliefs when new evidence emerges
- Calibrating confidence in estimates
- Testing hypotheses with imperfect data
- Evaluating risks with incomplete information
- Avoiding anchoring and overconfidence biases
- Making decisions under uncertainty
- Comparing multiple competing explanations
- Assessing diagnostic test results
- Forecasting project outcomes with new data

**Trigger phrases:** "What's the probability", "update my belief", "how confident", "forecast", "prior probability", "likelihood", "Bayes", "calibration", "base rate", "posterior probability"

## What is Bayesian Reasoning?

A systematic way to update probability estimates using Bayes' Theorem:

**P(H|E) = P(E|H) × P(H) / P(E)**

Where:
- **P(H)** = Prior: Probability of hypothesis before seeing evidence
- **P(E|H)** = Likelihood: Probability of evidence if hypothesis is true
- **P(E|¬H)** = Probability of evidence if hypothesis is false
- **P(H|E)** = Posterior: Updated probability after seeing evidence

**Quick Example:**

```markdown
# Should we launch Feature X?

## Prior Belief
Before beta testing: 60% chance of adoption >20%
- Base rate: Similar features get 15-25% adoption
- Our feature seems stronger than average
- Prior: 60%

## New Evidence
Beta test: 35% of users adopted (70 of 200 users)

## Likelihoods
If true adoption is >20%:
- P(seeing 35% in beta | adoption >20%) = 75% (likely to see high beta if true)

If true adoption is ≤20%:
- P(seeing 35% in beta | adoption ≤20%) = 15% (unlikely to see high beta if false)

## Bayesian Update
Posterior = (75% × 60%) / [(75% × 60%) + (15% × 40%)]
Posterior = 45% / (45% + 6%) = 88%

## Conclusion
Updated belief: 88% confident adoption will exceed 20%
Evidence strongly supports launch, but not certain.
```

## Workflow

Follow these steps in order:

### 1. [ ] Define the Question

Clarify what you're forecasting:
- [ ] **What hypothesis?** (specific, testable claim)
- [ ] **What probability?** (what are you estimating?)
- [ ] **What timeframe?** (when will outcome be known?)
- [ ] **What counts as success?** (clear success criteria)
- [ ] **Why does this matter?** (what decision depends on this?)

**Example:**
- Hypothesis: "Product feature will achieve >20% adoption within 3 months"
- Probability to estimate: P(adoption >20%)
- Timeframe: 3 months post-launch
- Success: ≥20% of active users use feature weekly
- Matters for: Launch decision and resource allocation

### 2. [ ] Establish Prior Beliefs

Set initial probability before new evidence:
- [ ] **Identify base rates**: What's the general frequency?
- [ ] **Consider reference class**: What similar situations exist?
- [ ] **Account for specifics**: How is this case different?
- [ ] **State prior explicitly**: Assign probability (avoid vague "likely")
- [ ] **Justify prior**: Explain reasoning

**Good priors:**
- Based on base rates and reference classes
- Account for known differences
- Honest about uncertainty
- Range provided if unsure (e.g., 40-60%)

**Bad priors:**
- Purely intuitive ("feels like 50%")
- Ignoring base rates
- Extreme (1% or 99%) without justification
- Hidden or unstated

### 3. [ ] Identify Evidence & Likelihoods

Assess how evidence relates to hypothesis:
- [ ] **What evidence?** (specific observation or data)
- [ ] **How diagnostic?** (does it distinguish hypotheses?)
- [ ] **Estimate P(E|H)**: Probability of evidence if hypothesis TRUE
- [ ] **Estimate P(E|¬H)**: Probability of evidence if hypothesis FALSE
- [ ] **Calculate likelihood ratio**: P(E|H) / P(E|¬H)

**Likelihood ratio interpretation:**
- LR > 10: Very strong evidence for H
- LR = 3-10: Moderate evidence for H
- LR = 1-3: Weak evidence for H
- LR ≈ 1: Evidence is not diagnostic
- LR < 1: Evidence against H

### 4. [ ] Calculate Posterior

Update probability using Bayes' Theorem:
- [ ] **Apply formula**: P(H|E) = [P(E|H) × P(H)] / P(E)
- [ ] **Or use odds form**: Posterior Odds = Prior Odds × Likelihood Ratio
- [ ] **Calculate P(E)**: P(E|H)×P(H) + P(E|¬H)×P(¬H)
- [ ] **Get posterior probability**: Final updated belief
- [ ] **Interpret change**: How much did belief shift?

**For simple cases:**
Use resources/template.md calculator

**For complex cases:**
Study resources/methodology.md for multiple hypothesis updates

### 5. [ ] Calibrate & Document

Validate and record reasoning:
- [ ] **Check calibration**: Am I over/underconfident?
- [ ] **Validate assumptions**: Are likelihoods reasonable?
- [ ] **Perform sensitivity analysis**: How sensitive to inputs?
- [ ] **Document reasoning**: Create bayesian-reasoning-calibration.md
- [ ] **Note limitations**: What could invalidate this?

**Self-check using** `resources/evaluators/rubric_bayesian_reasoning_calibration.json`:

**Quality checks:**
- [ ] Prior is based on base rates, not just intuition
- [ ] Likelihoods are estimated with justification
- [ ] Evidence is actually diagnostic (LR ≠ 1)
- [ ] Calculation is correct
- [ ] Posterior is calibrated (not overconfident)
- [ ] Assumptions are stated explicitly
- [ ] Sensitivity to inputs is noted

**Minimum standard**: Score ≥ 3.5 across all criteria

**Output file**: Create `bayesian-reasoning-calibration.md` in current directory

## Common Patterns

**For forecasting:**
- Use base rates as starting point
- Update incrementally as evidence arrives
- Track forecast accuracy over time
- Calibrate by comparing predictions to outcomes

**For hypothesis testing:**
- State competing hypotheses explicitly
- Calculate likelihood ratio for evidence
- Update belief proportionally to evidence strength
- Don't claim certainty unless LR is extreme

**For risk assessment:**
- Consider multiple scenarios (not just binary)
- Update risks as new data arrives
- Use ranges when uncertain about likelihoods
- Perform sensitivity analysis

**For avoiding bias:**
- Force explicit priors (prevents anchoring to evidence)
- Use reference classes (prevents ignoring base rates)
- Calculate mathematically (prevents motivated reasoning)
- Document before seeing outcome (enables calibration)

## Guardrails

**Do:**
- State priors explicitly before seeing all evidence
- Use base rates and reference classes
- Estimate likelihoods with justification
- Update incrementally as evidence arrives
- Be honest about uncertainty
- Perform sensitivity analysis
- Track forecasts for calibration
- Acknowledge limits of the model

**Don't:**
- Use extreme priors (1%, 99%) without exceptional justification
- Ignore base rates (common bias)
- Treat all evidence as equally diagnostic
- Update to 100% certainty (almost never justified)
- Cherry-pick evidence
- Skip documenting reasoning
- Forget to calibrate (compare predictions to outcomes)
- Apply to questions where probability is meaningless

## Quick Reference

- **Standard template**: `resources/template.md`
- **Multiple hypotheses**: `resources/methodology.md`
- **Examples**: `resources/examples/product-launch.md`, `resources/examples/medical-diagnosis.md`
- **Quality rubric**: `resources/evaluators/rubric_bayesian_reasoning_calibration.json`

**Bayesian Formula (Odds Form)**:
```
Posterior Odds = Prior Odds × Likelihood Ratio
```

**Likelihood Ratio**:
```
LR = P(Evidence | Hypothesis True) / P(Evidence | Hypothesis False)
```

**Output naming**: `bayesian-reasoning-calibration.md` or `{topic}-forecast.md`
