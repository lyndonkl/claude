# Bayesian Reasoning Template

## Workflow

Copy this checklist and track your progress:

```
Bayesian Update Progress:
- [ ] Step 1: State question and establish prior from base rates
- [ ] Step 2: Estimate likelihoods for evidence
- [ ] Step 3: Calculate posterior using Bayes' theorem
- [ ] Step 4: Perform sensitivity analysis
- [ ] Step 5: Calibrate and validate with quality checklist
```

**Step 1: State question and establish prior from base rates**

Define specific, testable hypothesis with timeframe and success criteria. Identify reference class and base rate, adjust for specific differences, and state prior explicitly with justification. See [Step 1: State the Question](#step-1-state-the-question) and [Step 2: Find Base Rates](#step-2-find-base-rates) for guidance.

**Step 2: Estimate likelihoods for evidence**

Assess P(E|H) (probability of evidence if hypothesis TRUE) and P(E|¬H) (probability if FALSE), calculate likelihood ratio = P(E|H) / P(E|¬H), and interpret diagnostic strength. See [Step 3: Estimate Likelihoods](#step-3-estimate-likelihoods) for examples and common mistakes.

**Step 3: Calculate posterior using Bayes' theorem**

Apply P(H|E) = [P(E|H) × P(H)] / P(E) or use simpler odds form: Posterior Odds = Prior Odds × LR. Interpret change in belief (prior → posterior) and strength of evidence. See [Step 4: Calculate Posterior](#step-4-calculate-posterior) for calculation methods.

**Step 4: Perform sensitivity analysis**

Test how posterior changes with different prior values and likelihoods to assess robustness of conclusion. See [Sensitivity Analysis](#sensitivity-analysis) section in template structure.

**Step 5: Calibrate and validate with quality checklist**

Check for overconfidence, base rate neglect, and extreme posteriors. Use [Calibration Check](#calibration-check) and [Quality Checklist](#quality-checklist) to verify prior is justified, likelihoods have reasoning, evidence is diagnostic (LR ≠ 1), calculation correct, and assumptions stated.

## Quick Template

```markdown
# Bayesian Analysis: {Topic}

## Question
**Hypothesis**: {What are you testing?}
**Estimating**: P({specific outcome})
**Timeframe**: {When will outcome be known?}
**Matters because**: {What decision depends on this?}

---

## Prior Belief (Before Evidence)

### Base Rate
{What's the general frequency in similar cases?}
- Reference class: {Similar situations}
- Base rate: {X%}

### Adjustments
{How is this case different from base rate?}
- Factor 1: {Increases/decreases probability because...}
- Factor 2: {Increases/decreases probability because...}

### Prior Probability
**P(H) = {X%}**

**Justification**: {Why this prior?}

**Range if uncertain**: {min%} to {max%}

---

## Evidence

**What was observed**: {Specific evidence or data}

**How diagnostic**: {Does this distinguish hypothesis true vs false?}

### Likelihoods

**P(E|H) = {X%}** - Probability of seeing this evidence IF hypothesis is TRUE
- Reasoning: {Why this likelihood?}

**P(E|¬H) = {Y%}** - Probability of seeing this evidence IF hypothesis is FALSE
- Reasoning: {Why this likelihood?}

**Likelihood Ratio = {X/Y} = {ratio}**
- Interpretation: Evidence is {very strong / moderate / weak / not diagnostic}

---

## Bayesian Update

### Calculation

**Using probability form**:
```
P(H|E) = [P(E|H) × P(H)] / P(E)

where P(E) = [P(E|H) × P(H)] + [P(E|¬H) × P(¬H)]

P(E) = [{X%} × {Prior%}] + [{Y%} × {100-Prior%}]
P(E) = {calculation}

P(H|E) = [{X%} × {Prior%}] / {P(E)}
P(H|E) = {result%}
```

**Or using odds form** (often simpler):
```
Prior Odds = P(H) / P(¬H) = {Prior%} / {100-Prior%} = {odds}
Likelihood Ratio = {LR}
Posterior Odds = Prior Odds × LR = {odds} × {LR} = {result}
Posterior Probability = Posterior Odds / (1 + Posterior Odds) = {result%}
```

### Posterior Probability
**P(H|E) = {result%}**

### Change in Belief
- Prior: {X%}
- Posterior: {Y%}
- Change: {+/- Z percentage points}
- Interpretation: Evidence {strongly supports / moderately supports / weakly supports / contradicts} hypothesis

---

## Sensitivity Analysis

**How sensitive is posterior to inputs?**

If Prior was {different value}:
- Posterior would be: {recalculated value}

If P(E|H) was {different value}:
- Posterior would be: {recalculated value}

**Robustness**: Conclusion is {robust / somewhat robust / sensitive} to assumptions

---

## Calibration Check

**Am I overconfident?**
- Did I anchor on initial belief? {yes/no - reasoning}
- Did I ignore base rates? {yes/no - reasoning}
- Is my posterior extreme (>90% or <10%)? {If yes, is evidence truly that strong?}
- Would an outside observer agree with my likelihoods? {check}

**Red flags**:
- ✗ Posterior is 100% or 0% (almost never justified)
- ✗ Large update from weak evidence (check LR)
- ✗ Prior ignores base rate entirely
- ✗ Likelihoods are guesses without reasoning

---

## Limitations & Assumptions

**Key assumptions**:
1. {Assumption 1}
2. {Assumption 2}

**What could invalidate this analysis**:
- {Condition that would change conclusion}
- {Different interpretation of evidence}

**Uncertainty**:
- Most uncertain about: {which input?}
- Could be wrong if: {what scenario?}

---

## Decision Implications

**Given posterior of {X%}**:

Recommended action: {what to do}

**If decision threshold is**:
- High confidence needed (>80%): {action}
- Medium confidence (>60%): {action}
- Low bar (>40%): {action}

**Next evidence to gather**: {What would further update belief?}
```

## Step-by-Step Guide

### Step 1: State the Question

Be specific and testable.

**Good**: "Will our product achieve >1000 DAU within 6 months?"
**Bad**: "Will the product succeed?"

Define success criteria numerically when possible.

### Step 2: Find Base Rates

**Method**:
1. Identify reference class (similar situations)
2. Look up historical frequency
3. Adjust for known differences

**Example**:
- Question: Will our SaaS startup raise Series A?
- Reference class: B2B SaaS startups, seed stage, similar market
- Base rate: ~30% raise Series A within 2 years
- Adjustments: Strong traction (+), competitive market (-), experienced team (+)
- Adjusted prior: 45%

**Common mistake**: Ignoring base rates entirely ("inside view" bias)

### Step 3: Estimate Likelihoods

Ask: "If hypothesis were true, how likely is this evidence?"
Then: "If hypothesis were false, how likely is this evidence?"

**Example - Medical test**:
- Hypothesis: Patient has disease (prevalence 1%)
- Evidence: Positive test result
- P(positive test | has disease) = 90% (test sensitivity)
- P(positive test | no disease) = 5% (false positive rate)
- LR = 90% / 5% = 18 (strong evidence)

**Common mistake**: Confusing P(E|H) with P(H|E) - the "prosecutor's fallacy"

### Step 4: Calculate Posterior

**Odds form is often easier**:

1. Convert prior to odds: Odds = P / (1-P)
2. Multiply by LR: Posterior Odds = Prior Odds × LR
3. Convert back to probability: P = Odds / (1 + Odds)

**Example**:
- Prior: 30% → Odds = 0.3/0.7 = 0.43
- LR = 5
- Posterior Odds = 0.43 × 5 = 2.15
- Posterior Probability = 2.15 / 3.15 = 68%

### Step 5: Calibrate

**Calibration questions**:
- If you made 100 predictions at X% confidence, would X actually occur?
- Are you systematically over/underconfident?
- Does your posterior pass the "outside view" test?

**Calibration tips**:
- Track your forecasts and outcomes
- Be especially skeptical of extreme probabilities (>95%, <5%)
- Consider opposite evidence (confirmation bias check)

## Common Pitfalls

**Ignoring base rates** ("base rate neglect"):
- Bad: "Test is 90% accurate, so positive test means 90% chance of disease"
- Good: "Disease is rare (1%), so even with positive test, probability is only ~15%"

**Confusing conditional probabilities**:
- P(positive test | disease) ≠ P(disease | positive test)
- These can be very different!

**Overconfident likelihoods**:
- Claiming P(E|H) = 99% when evidence is ambiguous
- Not considering alternative explanations

**Anchoring on prior**:
- Weak evidence + starting at 50% = staying near 50%
- Solution: Use base rates, not 50% default

**Treating all evidence as equally strong**:
- Check likelihood ratio (LR)
- LR ≈ 1 means evidence is not diagnostic

## Worked Example

**Question**: Will project finish on time?

**Prior**:
- Base rate: 60% of our projects finish on time
- This project: More complex than average (-), experienced team (+)
- Prior: 55%

**Evidence**: At 50% milestone, we're 1 week behind schedule

**Likelihoods**:
- P(behind at 50% | finish on time) = 30% (can recover)
- P(behind at 50% | miss deadline) = 80% (usually signals trouble)
- LR = 30% / 80% = 0.375 (evidence against on-time)

**Calculation**:
- Prior odds = 0.55 / 0.45 = 1.22
- Posterior odds = 1.22 × 0.375 = 0.46
- Posterior probability = 0.46 / 1.46 = 32%

**Conclusion**: Updated from 55% to 32% probability of on-time finish. Being behind at 50% is meaningful evidence of delay.

**Decision**: If deadline is flexible, continue. If hard deadline, consider descoping or adding resources.

## Quality Checklist

- [ ] Prior is justified (base rate + adjustments)
- [ ] Likelihoods have reasoning (not just guesses)
- [ ] Evidence is diagnostic (LR significantly different from 1)
- [ ] Calculation is correct
- [ ] Posterior is in reasonable range (not 0% or 100%)
- [ ] Assumptions are stated
- [ ] Sensitivity analysis performed
- [ ] Decision implications clear
