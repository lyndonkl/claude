# Design of Experiments - Advanced Methodology

## Workflow

Copy this checklist for advanced DOE cases:

```
Advanced DOE Progress:
- [ ] Step 1: Assess complexity and choose advanced technique
- [ ] Step 2: Design experiment using specialized method
- [ ] Step 3: Plan execution with advanced considerations
- [ ] Step 4: Analyze with appropriate statistical methods
- [ ] Step 5: Iterate or confirm findings
```

**Step 1: Assess complexity**

Identify which advanced technique applies: screening 8+ factors, response surface with curvature, robust design, mixture constraints, hard-to-change factors, or irregular factor space. See technique selection criteria below.

**Step 2: Design experiment**

Apply specialized design method from sections: [Screening Designs](#1-screening-designs), [Response Surface Methodology](#2-response-surface-methodology), [Taguchi Methods](#3-taguchi-methods-robust-parameter-design), [Optimal Designs](#4-optimal-designs), [Mixture Experiments](#5-mixture-experiments), or [Split-Plot Designs](#6-split-plot-designs).

**Step 3: Plan execution**

Address advanced considerations: blocking for nuisance variables, replication for variance estimation, center points for curvature detection, and sequential strategies. See [Sequential Experimentation](#7-sequential-experimentation) for iterative approaches.

**Step 4: Analyze**

Use appropriate analysis for design type: effect estimation, ANOVA, regression modeling, response surface equations, contour plots, and residual diagnostics. See [Analysis Techniques](#8-analysis-techniques).

**Step 5: Iterate or confirm**

Based on findings, run confirmation experiments, refine factor ranges, add center/axial points for RSM, or screen additional factors. See [Sequential Experimentation](#7-sequential-experimentation).

---

## 1. Screening Designs

**When to use**: 8-30 candidate factors, limited experimental budget, goal is to identify 3-5 vital factors for follow-up optimization.

### Plackett-Burman Designs

**Structure**: Orthogonal designs with runs = multiple of 4. Screens k factors in k+1 runs.

**Standard designs**:
- 12 runs → screen up to 11 factors
- 16 runs → screen up to 15 factors
- 20 runs → screen up to 19 factors
- 24 runs → screen up to 23 factors

**Example: 12-run Plackett-Burman generator matrix**:
```
Run 1: + + - + + + - - - + -
Subsequent runs: Cycle previous row left, last run is all minus
```

**Analysis**: Fit linear model Y = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ. Rank factors by |βᵢ|. Select top 3-5 for optimization. Pareto chart: cumulative % variance explained.

**Limitation**: Main effects confounded with 2-way interactions. Only valid if interactions negligible (sparsity-of-effects principle).

### Fractional Factorial Screening

**When to use**: 5-8 factors, need to estimate some 2-way interactions, Resolution IV or V required.

**Common designs**:
- **2⁵⁻¹ (Resolution V)**: 16 runs, 5 factors. Main effects and 2-way interactions clear. Generator: I = ABCDE.
- **2⁶⁻² (Resolution IV)**: 16 runs, 6 factors. Main effects clear, 2-way confounded with 2-way. Generators: I = ABCE, I = BCDF.
- **2⁷⁻³ (Resolution IV)**: 16 runs, 7 factors. Generators: I = ABCD, I = ABEF, I = ACEG.

**Confounding analysis**: Use defining relation to determine alias structure. Example for 2⁵⁻¹ with I = ABCDE:
- A aliased with BCDE
- AB aliased with CDE
- ABC aliased with DE

**Fold-over technique**: If screening reveals ambiguous confounding, run fold-over design (flip all signs) to de-alias. 16 runs + 16 fold-over = 32 runs = full 2⁵ factorial.

---

## 2. Response Surface Methodology

**When to use**: 2-5 factors already identified as important, need to find optimum, expect curvature (quadratic relationship).

### Central Composite Design (CCD)

**Structure**: Factorial points + axial points + center points

**Components**:
- **Factorial points**: 2^k corner points (±1 for all factors)
- **Axial points**: 2k points on axes (±α, 0, 0, ...) where α determines rotatability
- **Center points**: 3-5 replicates at origin (0, 0, ..., 0)

**Total runs**: 2^k + 2k + nc (nc = number of center points)

**Example: CCD for 3 factors** (8 + 6 + 5 = 19 runs):

| Type | X₁ | X₂ | X₃ |
|------|----|----|-----|
| Factorial | -1 | -1 | -1 |
| ... | ... | ... | ... | (8 factorial points)
| Axial | -α | 0 | 0 |
| Axial | +α | 0 | 0 |
| Axial | 0 | -α | 0 |
| Axial | 0 | +α | 0 |
| Axial | 0 | 0 | -α |
| Axial | 0 | 0 | +α |
| Center | 0 | 0 | 0 | (replicate 5 times)

**Rotatability**: Choose α = (2^k)^(1/4) for equal prediction variance at equal distance from center. For 3 factors: α = 1.682.

**Model**: Fit quadratic: Y = β₀ + Σβᵢxᵢ + Σβᵢᵢxᵢ² + Σβᵢⱼxᵢxⱼ

**Analysis**: Canonical analysis to find stationary point (maximum, minimum, or saddle). Ridge analysis if optimum outside design region.

### Box-Behnken Design

**Structure**: 3-level design that avoids extreme corners (all factors at ±1 simultaneously).

**Advantages**: Fewer runs than CCD, safer when extreme combinations may damage equipment or produce out-of-spec product.

**Example: Box-Behnken for 3 factors** (12 + 3 = 15 runs):

| X₁ | X₂ | X₃ |
|----|----|----|
| -1 | -1 | 0 |
| +1 | -1 | 0 |
| -1 | +1 | 0 |
| +1 | +1 | 0 |
| -1 | 0 | -1 |
| +1 | 0 | -1 |
| -1 | 0 | +1 |
| +1 | 0 | +1 |
| 0 | -1 | -1 |
| 0 | +1 | -1 |
| 0 | -1 | +1 |
| 0 | +1 | +1 |
| 0 | 0 | 0 | (center, replicate 3 times)

**Model**: Same quadratic as CCD.

**Trade-off**: Slightly less efficient than CCD for prediction, but avoids extreme points.

---

## 3. Taguchi Methods (Robust Parameter Design)

**When to use**: Product/process must perform well despite uncontrollable variation (noise factors). Goal: Find control factor settings that minimize sensitivity to noise.

### Inner-Outer Array Structure

**Inner array**: Control factors (factors you can set in production)
**Outer array**: Noise factors (environmental conditions, material variation, user variation)

**Approach**: Cross inner array with outer array. Each inner array run is repeated at all outer array conditions.

**Example: L₈ inner × L₄ outer** (8 control combinations × 4 noise conditions = 32 runs):

**Inner array (control factors A, B, C)**:

| Run | A | B | C |
|-----|---|---|---|
| 1 | -1 | -1 | -1 |
| 2 | -1 | -1 | +1 |
| ... | ... | ... | ... |
| 8 | +1 | +1 | +1 |

**Outer array (noise factors N₁, N₂)**:

| Noise | N₁ | N₂ |
|-------|----|----|
| 1 | -1 | -1 |
| 2 | -1 | +1 |
| 3 | +1 | -1 |
| 4 | +1 | +1 |

**Data collection**: For each inner run, measure response Y at all 4 noise conditions. Calculate mean (Ȳ) and variance (s²) or signal-to-noise ratio (SNR).

**Signal-to-Noise Ratios**:
- **Larger-is-better**: SNR = -10 log₁₀(Σ(1/Y²)/n)
- **Smaller-is-better**: SNR = -10 log₁₀(ΣY²/n)
- **Target-is-best**: SNR = 10 log₁₀(Ȳ²/s²)

**Analysis**: Choose control factor settings that maximize SNR (robust to noise) while achieving target mean.

**Two-step optimization**:
1. Maximize SNR to reduce variability
2. Adjust mean to target using control factors that don't affect SNR

---

## 4. Optimal Designs

**When to use**: Irregular factor space (constraints, categorical factors, unequal ranges), custom run budget, or standard designs don't fit.

### D-Optimal Designs

**Criterion**: Minimize determinant of (X'X)⁻¹ (maximize information, minimize variance of coefficient estimates).

**Algorithm**: Computer-generated. Start with candidate set of all feasible runs, select subset that maximizes |X'X|.

**Use cases**:
- Mixture experiments with additional process variables
- Constrained factor spaces (e.g., temperature + pressure can't both be high)
- Irregular grids (e.g., existing data points + new runs)
- Unequal factor ranges

**Software**: Use R (AlgDesign package), JMP, Design-Expert, or Python (pyDOE).

### A-Optimal and G-Optimal

**A-optimal**: Minimize average variance of predictions (trace of (X'X)⁻¹).
**G-optimal**: Minimize maximum variance across design space (minimax criterion).

**Choice**: D-optimal for parameter estimation, G-optimal for prediction across entire space, A-optimal for average prediction quality.

---

## 5. Mixture Experiments

**When to use**: Factors are proportions that must sum to 100% (e.g., chemical formulations, blend compositions, budget allocations).

### Simplex-Lattice Designs

**Constraints**: x₁ + x₂ + ... + xₖ = 1, all xᵢ ≥ 0

**{q,k} designs**: q = number of levels for each component, k = number of components

**Example: {2,3} simplex-lattice** (3 components at 0%, 50%, 100%):

| Run | x₁ | x₂ | x₃ |
|-----|----|----|-----|
| 1 | 1.0 | 0.0 | 0.0 |
| 2 | 0.0 | 1.0 | 0.0 |
| 3 | 0.0 | 0.0 | 1.0 |
| 4 | 0.5 | 0.5 | 0.0 |
| 5 | 0.5 | 0.0 | 0.5 |
| 6 | 0.0 | 0.5 | 0.5 |

**Model**: Scheffé canonical polynomials. Linear: Y = β₁x₁ + β₂x₂ + β₃x₃. Quadratic: Y = Σβᵢxᵢ + Σβᵢⱼxᵢxⱼ.

### Simplex-Centroid Designs

**Structure**: Pure components + binary blends + ternary blends + overall centroid.

**Example: 3-component simplex-centroid** (7 runs):

| Run | x₁ | x₂ | x₃ |
|-----|----|----|-----|
| 1 | 1.0 | 0 | 0 | (pure components)
| 2 | 0 | 1.0 | 0 |
| 3 | 0 | 0 | 1.0 |
| 4 | 0.5 | 0.5 | 0 | (binary blends)
| 5 | 0.5 | 0 | 0.5 |
| 6 | 0 | 0.5 | 0.5 |
| 7 | 0.33 | 0.33 | 0.33 | (centroid)

**Constraints**: Add lower/upper bounds if components have minimum/maximum limits. Use D-optimal design for constrained mixture space.

---

## 6. Split-Plot Designs

**When to use**: Some factors are hard to change (e.g., temperature requires hours to stabilize), others are easy to change. Randomizing all factors fully is impractical or expensive.

### Structure

**Whole-plot factors**: Hard to change (temperature, batch, supplier)
**Subplot factors**: Easy to change (concentration, time, operator)

**Design**: Randomize whole-plot factors at top level, randomize subplot factors within each whole-plot level.

**Example: 2² split-plot** (Temperature = whole-plot, Time = subplot, 2 replicates):

| Whole-plot | Temp | Subplot | Time | Run order |
|------------|------|---------|------|-----------|
| 1 | Low | 1 | Short | 1 |
| 1 | Low | 2 | Long | 2 |
| 2 | High | 3 | Short | 4 |
| 2 | High | 4 | Long | 3 |
| (Replicate block 2)

**Analysis**: Mixed model with whole-plot error and subplot error terms. Whole-plot factors tested with lower precision (fewer degrees of freedom).

**Trade-off**: Allows practical execution when full randomization impossible, but reduces statistical power for hard-to-change factors.

---

## 7. Sequential Experimentation

**Philosophy**: Learn iteratively, adapt design based on results. Minimize total runs while maximizing information.

### Stage 1: Screening

**Objective**: Reduce 10-20 candidates to 3-5 critical factors.
**Design**: Plackett-Burman or 2^(k-p) fractional factorial (Resolution III-IV).
**Runs**: 12-20.
**Output**: Ranked factor list, effect sizes with uncertainty.

### Stage 2: Steepest Ascent/Descent

**Objective**: Move quickly toward optimal region using main effects from screening.
**Method**: Calculate path of steepest ascent (gradient = effect estimates). Run experiments along this path until response stops improving.
**Example**: If screening finds temp effect = +10, pressure effect = +5, move in direction (temp: +2, pressure: +1).

### Stage 3: Factorial Optimization

**Objective**: Explore region around best settings from steepest ascent, estimate interactions.
**Design**: 2^k full factorial or Resolution V fractional factorial with 3-5 factors.
**Runs**: 16-32.
**Output**: Optimal settings, interaction effects, linear model.

### Stage 4: Response Surface Refinement

**Objective**: Fit curvature, find true optimum.
**Design**: CCD or Box-Behnken centered at best settings from Stage 3.
**Runs**: 15-20.
**Output**: Quadratic model, stationary point (optimum), contour plots.

### Stage 5: Confirmation

**Objective**: Validate predicted optimum.
**Design**: 3-5 replication runs at predicted optimal settings.
**Output**: Confidence interval for response at optimum. If prediction interval contains observed mean, model validated.

**Total runs example**: Screening (16) + Steepest ascent (4) + Factorial (16) + RSM (15) + Confirmation (3) = 54 runs. Compare to one-shot full factorial for 10 factors = 1024 runs.

---

## 8. Analysis Techniques

### Effect Estimation

**Factorial designs**: Estimate main effect of factor A as: Effect(A) = (Ȳ₊ - Ȳ₋) where Ȳ₊ = mean response when A is high, Ȳ₋ = mean when A is low.

**Interaction effect**: Effect(AB) = [(Ȳ₊₊ + Ȳ₋₋) - (Ȳ₊₋ + Ȳ₋₊)] / 2

**Standard error**: SE(effect) = 2σ/√n, where σ estimated from replicates or center points.

### ANOVA

**Purpose**: Test statistical significance of effects.
**Null hypothesis**: Effect = 0.
**Test statistic**: F = MS(effect) / MS(error), compare to F-distribution.
**Significance**: p < 0.05 (or chosen α level) → reject H₀, effect is significant.

### Regression Modeling

**Linear model**: Y = β₀ + β₁x₁ + β₂x₂ + β₁₂x₁x₂ + ε
**Quadratic model** (RSM): Y = β₀ + Σβᵢxᵢ + Σβᵢᵢxᵢ² + Σβᵢⱼxᵢxⱼ + ε

**Fit**: Least squares (minimize Σ(Yᵢ - Ŷᵢ)²).
**Assessment**: R², adjusted R², RMSE, residual plots.

### Residual Diagnostics

**Check assumptions**:
1. **Normal probability plot**: Residuals should fall on straight line. Non-normality indicates transformation needed.
2. **Residuals vs fitted**: Random scatter around zero. Funnel shape indicates non-constant variance (transform Y).
3. **Residuals vs run order**: Random. Trend indicates time drift, lack of randomization.
4. **Residuals vs factors**: Random. Pattern indicates missing interaction or curvature.

**Transformations**: Log(Y) for multiplicative effects, √Y for count data, 1/Y for rate data, Box-Cox for data-driven choice.

### Optimization

**Contour plots**: Visualize response surface, identify optimal region, assess tradeoffs.
**Desirability functions**: Multi-response optimization. Convert each response to 0-1 scale (0 = unacceptable, 1 = ideal). Maximize geometric mean of desirabilities.
**Canonical analysis**: Find stationary point (∂Y/∂xᵢ = 0), classify as maximum, minimum, or saddle point based on eigenvalues of Hessian matrix.

---

## 9. Sample Size and Power Analysis

**Before designing experiment, determine required runs**:

**Power**: Probability of detecting true effect if it exists (1 - β). Standard: power ≥ 0.80.

**Effect size (δ)**: Minimum meaningful difference. Example: "Must detect 10% yield improvement."

**Noise (σ)**: Process variability. Estimate from historical data, pilot runs, or engineering judgment.

**Formula for factorial designs**: n ≥ 2(Zα/2 + Zβ)²σ² / δ² per cell.

**Example**: Detect δ = 5 units, σ = 3 units, α = 0.05, power = 0.80.
- n ≥ 2(1.96 + 0.84)²(3²) / 5² = 2(7.84)(9) / 25 ≈ 6 replicates per factor level combination.

**For screening**: Use effect sparsity assumption. If testing 10 factors, expect 2-3 active. Size design to detect large effects (1-2σ).

**Software**: Use G*Power, R (pwr package), JMP, or online calculators.

---

## 10. Common Pitfalls and Solutions

**Pitfall 1: Ignoring confounding in screening designs**
- **Problem**: Plackett-Burman confounds main effects with 2-way interactions. If interactions exist, main effect estimates are biased.
- **Solution**: Use only when sparsity-of-effects applies (most interactions negligible). Follow up ambiguous results with Resolution IV/V design or fold-over.

**Pitfall 2: Extrapolating beyond design region**
- **Problem**: Response surface models are local approximations. Predicting outside tested factor ranges is unreliable.
- **Solution**: Expand design if optimum appears outside current region. Run steepest ascent, then new RSM centered on improved region.

**Pitfall 3: Inadequate replication**
- **Problem**: Without replicates, cannot estimate pure error or test lack-of-fit.
- **Solution**: Always include 3-5 center point replicates. For critical experiments, replicate entire design (2-3 times).

**Pitfall 4: Changing protocols mid-experiment**
- **Problem**: Breaks orthogonality, confounds design structure with time.
- **Solution**: Complete design as planned. If protocol change necessary, analyze before/after separately or treat as blocking factor.

**Pitfall 5: Treating categorical factors as continuous**
- **Problem**: Assigning arbitrary numeric codes (-1, 0, +1) to unordered categories (e.g., Supplier A/B/C) implies ordering that doesn't exist.
- **Solution**: Use indicator variables (dummy coding) or separate experiments for each category level.
