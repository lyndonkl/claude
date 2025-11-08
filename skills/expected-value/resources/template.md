# Expected Value Templates

Quick-start templates for decision framing, outcome identification, probability estimation, payoff quantification, EV calculation, and sensitivity analysis.

## Workflow

```
Expected Value Analysis Progress:
- [ ] Step 1: Define decision and alternatives
- [ ] Step 2: Identify possible outcomes
- [ ] Step 3: Estimate probabilities
- [ ] Step 4: Estimate payoffs (values)
- [ ] Step 5: Calculate expected values
- [ ] Step 6: Interpret and adjust for risk preferences
```

**Step 1: Define decision and alternatives** → Use [Decision Framing Template](#decision-framing-template)

**Step 2: Identify possible outcomes** → Use [Outcome Identification Template](#outcome-identification-template)

**Step 3: Estimate probabilities** → Use [Probability Estimation Template](#probability-estimation-template)

**Step 4: Estimate payoffs** → Use [Payoff Quantification Template](#payoff-quantification-template)

**Step 5: Calculate expected values** → Use [EV Calculation Template](#ev-calculation-template)

**Step 6: Interpret and adjust for risk** → Use [Risk Adjustment Template](#risk-adjustment-template) and [Sensitivity Analysis Template](#sensitivity-analysis-template)

---

## Decision Framing Template

**Decision to be made**: [Clear statement of the choice]

**Context**: [Why are you making this decision? What's the deadline? What constraints exist?]

**Alternatives** (mutually exclusive options):
1. **[Alternative 1]**: [Brief description]
2. **[Alternative 2]**: [Brief description]
3. **[Alternative 3]**: [Brief description, if applicable]
4. **Do nothing / status quo**: [Always consider baseline]

**Success criteria**: [How will you know if this was a good decision? What are you optimizing for?]

**Assumptions**:
- [Key assumption 1]
- [Key assumption 2]
- [Key assumption 3]

**Out of scope** (not considering):
- [Factor 1 you're explicitly not modeling]
- [Factor 2]

---

## Outcome Identification Template

For each alternative, identify 3-5 possible outcomes (scenarios).

### Alternative: [Name]

**Outcome 1: Best case**
- **Description**: [What happens in optimistic scenario?]
- **Key drivers**: [What needs to go right?]
- **Likelihood indicator**: [Rough sense: common, uncommon, rare?]

**Outcome 2: Base case**
- **Description**: [What happens in most likely scenario?]
- **Key drivers**: [What's the typical path?]
- **Likelihood indicator**: [Should be most probable]

**Outcome 3: Worst case**
- **Description**: [What happens in pessimistic scenario?]
- **Key drivers**: [What needs to go wrong?]
- **Likelihood indicator**: [How bad could it get?]

**Outcome 4: [Other scenario, if needed]**
- **Description**:
- **Key drivers**:
- **Likelihood indicator**:

**Check**: Do these outcomes cover the full range of possibilities? Are they mutually exclusive (no overlap)?

---

## Probability Estimation Template

Estimate probability for each outcome using multiple methods, then reconcile.

### Outcome: [Name]

| Method | Estimate | Notes |
|--------|----------|-------|
| **Base rates** (reference class) | [X%] | [Similar situations: N cases, frequency] |
| **Inside view** (causal model) | [Y%] | [Key factors: p_A × p_B × p_C] |
| **Expert judgment** | [Z%] | [Average of expert estimates] |
| **Data/model** | [W%] | [Forecast, confidence interval] |

**Final estimate**: [Weighted average] **Confidence**: [Range if uncertain]

**All outcomes** (must sum to 1.0):
- Outcome 1: [p₁], Outcome 2: [p₂], Outcome 3: [p₃]. **Total**: [p₁+p₂+p₃ = 1.0 ✓]

---

## Payoff Quantification Template

### Outcome: [Name]

**Monetary**: Revenue [+$X], Cost [-$Y], Savings [+$Z], Opp. cost [-$W]. **Net**: [Sum]

**Non-monetary** (convert to $ or utility): Time [X hrs × $rate], Reputation [$Z], Learning [$W], Strategic [qualitative or $], Morale [qualitative or $]

**Time horizon**: [When?] **Discount rate**: [r%/yr if multi-period]

**NPV** (if multi-period): Yr0 [$X/(1+r)⁰], Yr1 [$Y/(1+r)¹], Yr2 [$Z/(1+r)²]. **Total NPV**: [Sum]

**Total Payoff**: [$ or utility] **Uncertainty**: [Point estimate or range: low-high]

---

## EV Calculation Template

Calculate expected value for each alternative.

### Alternative: [Name]

| Outcome | Probability (p) | Payoff (v) | p × v |
|---------|----------------|-----------|-------|
| [Outcome 1] | [p₁] | [v₁] | [p₁ × v₁] |
| [Outcome 2] | [p₂] | [v₂] | [p₂ × v₂] |
| [Outcome 3] | [p₃] | [v₃] | [p₃ × v₃] |
| **Total** | **1.0** | | **EV = Σ (p × v)** |

**Expected Value**: [EV = p₁×v₁ + p₂×v₂ + p₃×v₃]

**Variance**: Var = Σ (pᵢ × (vᵢ - EV)²)
- (v₁ - EV)² × p₁ = [X]
- (v₂ - EV)² × p₂ = [Y]
- (v₃ - EV)² × p₃ = [Z]
- **Variance** = [X + Y + Z]

**Standard Deviation**: σ = √Var = [σ]

**Coefficient of Variation**: CV = σ / EV = [CV] (lower = better risk-adjusted return)

### Comparison Across Alternatives

| Alternative | EV | σ (risk) | CV | Rank by EV |
|-------------|-------|----------|-----|------------|
| [Alt 1] | [EV₁] | [σ₁] | [CV₁] | [1] |
| [Alt 2] | [EV₂] | [σ₂] | [CV₂] | [2] |
| [Alt 3] | [EV₃] | [σ₃] | [CV₃] | [3] |

**Preliminary recommendation** (based on EV): [Highest EV alternative]

---

## Sensitivity Analysis Template

Test how sensitive the decision is to changes in key assumptions.

### One-Way Sensitivity (vary one variable at a time)

**Variable**: Probability of [Outcome X]

| p(Outcome X) | EV(Alt 1) | EV(Alt 2) | Best choice |
|-------------|-----------|-----------|-------------|
| [Low: p-20%] | [EV] | [EV] | [Alt] |
| [Base: p] | [EV] | [EV] | [Alt] |
| [High: p+20%] | [EV] | [EV] | [Alt] |

**Breakeven**: At what probability does decision flip? Solve: EV(Alt 1) = EV(Alt 2).

**Variable**: Payoff of [Outcome Y]

| v(Outcome Y) | EV(Alt 1) | EV(Alt 2) | Best choice |
|-------------|-----------|-----------|-------------|
| [Low: v-30%] | [EV] | [EV] | [Alt] |
| [Base: v] | [EV] | [EV] | [Alt] |
| [High: v+30%] | [EV] | [EV] | [Alt] |

### Tornado Diagram (which variables have most impact on EV?)

| Variable | Range tested | Impact on EV (swing) | Rank |
|----------|-------------|---------------------|------|
| [Var 1] | [low-high] | [±$X] | [1 (highest impact)] |
| [Var 2] | [low-high] | [±$Y] | [2] |
| [Var 3] | [low-high] | [±$Z] | [3] |

**Interpretation**: Focus on high-impact variables. Get better estimates for top 2-3.

### Scenario Analysis (vary multiple variables together)

| Scenario | Assumptions | EV(Alt 1) | EV(Alt 2) | Best |
|----------|------------|-----------|-----------|------|
| **Optimistic** | [High demand, low cost, no delays] | [EV] | [EV] | [Alt] |
| **Base** | [Expected values] | [EV] | [EV] | [Alt] |
| **Pessimistic** | [Low demand, high cost, delays] | [EV] | [EV] | [Alt] |

**Robustness**: Does the decision hold across scenarios? If different winners in different scenarios → decision is fragile, more info needed.

---

## Risk Adjustment Template

**Risk profile**: Risk-neutral / Risk-averse / Risk-seeking? One-shot or repeated decision?

**Utility function** (if risk-averse): U(x) = x (neutral), √x (moderate aversion), log(x) (strong aversion)

### Expected Utility (if risk-averse)

| Outcome | p | v | U(v) | p × U(v) |
|---------|---|---|------|----------|
| [Out 1] | [p₁] | [v₁] | [U(v₁)] | [p₁ × U(v₁)] |
| [Out 2] | [p₂] | [v₂] | [U(v₂)] | [p₂ × U(v₂)] |
| **Total** | **1.0** | | | **EU = Σ** |

**Certainty Equivalent**: CE = U⁻¹(EU). **Risk Premium**: EV - CE.

**Non-monetary factors**: Strategic value [$/qualitative], Alignment with mission [score 1-5], Regret [low/med/high]

**Recommendation**: Highest EV [Alt X], Highest EU [Alt Y], **Final choice**: [Alt Z with rationale]

---

## Decision Tree Template

For sequential decisions (make choice, observe outcome, make another choice).

### Tree Structure

```
[Decision 1] → [Outcome A] → [Decision 2a] → [Outcome C]
                                           → [Outcome D]
             → [Outcome B] → [Decision 2b] → [Outcome E]
                                           → [Outcome F]
```

### Fold-Back Induction (work backwards from end)

**Step 1: Calculate EV at terminal nodes** (final outcomes)
- Outcome C: [payoff = $X]
- Outcome D: [payoff = $Y]
- Outcome E: [payoff = $Z]
- Outcome F: [payoff = $W]

**Step 2: Calculate EV at Decision 2a**
- If choose path to C: [p(C) × $X]
- If choose path to D: [p(D) × $Y]
- **Optimal Decision 2a**: [Choose whichever has higher EV]
- **EV(Decision 2a)**: [max of the two]

**Step 3: Calculate EV at Decision 2b**
- If choose path to E: [p(E) × $Z]
- If choose path to F: [p(F) × $W]
- **Optimal Decision 2b**: [Choose whichever has higher EV]
- **EV(Decision 2b)**: [max of the two]

**Step 4: Calculate EV at Decision 1**
- If choose path to A: [p(A) × EV(Decision 2a)]
- If choose path to B: [p(B) × EV(Decision 2b)]
- **Optimal Decision 1**: [Choose whichever has higher EV]
- **Overall EV**: [max of the two]

**Optimal Strategy**:
1. At Decision 1: [Choose A or B]
2. If A occurs, at Decision 2a: [Choose path to C or D]
3. If B occurs, at Decision 2b: [Choose path to E or F]

**Value of Information**: If you could know outcome before Decision 1, how much would that be worth?
- EVPI = EV(with perfect info) - EV(current decision)

---

## Complete EV Analysis Template

**Decision**: [Name]

**Date**: [Date]

**Decision maker**: [Name/Team]

### 1. Decision Framing

**Alternatives**:
1. [Alt 1]
2. [Alt 2]
3. [Alt 3]

**Success criteria**: [What are you optimizing for?]

### 2. Outcomes and Probabilities

| Alternative | Outcome | Probability | Payoff | p × v |
|-------------|---------|------------|--------|-------|
| **[Alt 1]** | [Outcome 1] | [p₁] | [v₁] | [p₁ × v₁] |
|  | [Outcome 2] | [p₂] | [v₂] | [p₂ × v₂] |
|  | [Outcome 3] | [p₃] | [v₃] | [p₃ × v₃] |
|  | **EV(Alt 1)** | | | **[EV₁]** |
| **[Alt 2]** | [Outcome 1] | [p₁] | [v₁] | [p₁ × v₁] |
|  | [Outcome 2] | [p₂] | [v₂] | [p₂ × v₂] |
|  | [Outcome 3] | [p₃] | [v₃] | [p₃ × v₃] |
|  | **EV(Alt 2)** | | | **[EV₂]** |

### 3. Comparison

| Alternative | EV | σ (risk) | CV |
|-------------|-------|----------|-----|
| [Alt 1] | [EV₁] | [σ₁] | [CV₁] |
| [Alt 2] | [EV₂] | [σ₂] | [CV₂] |

**Highest EV**: [Alt X with EV = $Y]

### 4. Sensitivity Analysis

**Key assumptions**:
- [Assumption 1]: [If this changes by X%, decision flips? Yes/No]
- [Assumption 2]: [Breakeven value = ?]

**Robustness**: [Is decision robust across scenarios?]

### 5. Risk Adjustment

**Risk profile**: [One-shot or repeated? Risk-averse or neutral?]

**Recommendation**: [Alt X]

**Rationale**: [Why this choice given EV, risk, strategic factors?]

### 6. Action Plan

**Next steps**:
1. [Immediate action]
2. [Follow-up in X days/weeks]
3. [Decision review date]

**Contingencies**: [If Outcome Y occurs, we will...]
