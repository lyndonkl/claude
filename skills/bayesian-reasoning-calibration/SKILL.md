---
name: bayesian-reasoning-calibration
description: Applies Bayesian reasoning to systematically update probability estimates with new evidence, helping make better forecasts and avoid overconfidence. Use when making predictions or judgments under uncertainty, forecasting outcomes, evaluating probabilities, testing hypotheses, calibrating confidence, assessing risks with uncertain data, or when user mentions priors, likelihoods, Bayes theorem, probability updates, forecasting, calibration, or belief revision.
---

# Bayesian Reasoning & Calibration

## Table of Contents

- [Workflow](#workflow)
  - [1. Define the Question](#1--define-the-question)
  - [2. Establish Prior Beliefs](#2--establish-prior-beliefs)
  - [3. Identify Evidence & Likelihoods](#3--identify-evidence--likelihoods)
  - [4. Calculate Posterior](#4--calculate-posterior)
  - [5. Calibrate & Document](#5--calibrate--document)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Core formula:** P(H|E) = P(E|H) x P(H) / P(E), where P(H) = prior, P(E|H) = likelihood, P(H|E) = posterior.

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

Copy this checklist and track your progress:

```
Bayesian Reasoning Progress:
- [ ] Step 1: Define the question
- [ ] Step 2: Establish prior beliefs
- [ ] Step 3: Identify evidence and likelihoods
- [ ] Step 4: Calculate posterior
- [ ] Step 5: Calibrate and document
```

**Step 1: Define the question**

Clarify hypothesis (specific, testable claim), probability to estimate, timeframe (when outcome is known), success criteria, and why this matters (what decision depends on it). Example: "Product feature will achieve >20% adoption within 3 months" - matters for launch decision.

**Step 2: Establish prior beliefs**

Set initial probability using base rates (general frequency), reference class (similar situations), specific differences, and explicit probability assignment with justification. Good priors are based on base rates, account for differences, honest about uncertainty, and include ranges if unsure (e.g., 40-60%). Avoid purely intuitive priors, ignoring base rates, or extreme values without justification.

**Step 3: Identify evidence and likelihoods**

Assess evidence (specific observation/data), diagnostic power (does it distinguish hypotheses?), P(E|H) (probability if hypothesis TRUE), P(E|¬H) (probability if FALSE), and calculate likelihood ratio = P(E|H) / P(E|¬H). LR > 10 = very strong evidence, 3-10 = moderate, 1-3 = weak, ≈1 = not diagnostic, <1 = evidence against.

**Step 4: Calculate posterior**

Apply Bayes' Theorem: P(H|E) = [P(E|H) × P(H)] / P(E), or use odds form: Posterior Odds = Prior Odds × Likelihood Ratio. Calculate P(E) = P(E|H)×P(H) + P(E|¬H)×P(¬H), get posterior probability, and interpret change. For simple cases → Use `resources/template.md` calculator. For complex cases (multiple hypotheses) → Study `resources/methodology.md`.

**Step 5: Calibrate and document**

Check calibration (over/underconfident?), validate assumptions (are likelihoods reasonable?), perform sensitivity analysis, create `bayesian-reasoning-calibration.md`, and note limitations. Self-check using `resources/evaluators/rubric_bayesian_reasoning_calibration.json`: verify prior based on base rates, likelihoods justified, evidence diagnostic (LR ≠ 1), calculation correct, posterior calibrated, assumptions stated, sensitivity noted. Minimum standard: Score ≥ 3.5.

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
