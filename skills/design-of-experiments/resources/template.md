# Design of Experiments - Template

## Workflow

Copy this checklist and track your progress:

```
DOE Template Progress:
- [ ] Step 1: Define experiment objective
- [ ] Step 2: List factors and levels
- [ ] Step 3: Select design type
- [ ] Step 4: Generate design matrix
- [ ] Step 5: Randomize and document protocol
- [ ] Step 6: Finalize experiment plan
```

**Step 1: Define experiment objective**

Specify what you're trying to learn (screening, optimization, response surface, robust design), primary response metric(s), and success criteria. See [Objective Definition](#objective-definition) for examples.

**Step 2: List factors and levels**

Identify all factors (controllable inputs), specify levels for each (2-3 initially), distinguish control vs noise factors, and define measurable responses. See [Factor Table Template](#factor-table-template) for structure.

**Step 3: Select design type**

Based on objective:
- **2-5 factors, want all combinations** → [Full Factorial](#full-factorial-designs)
- **5+ factors, limited runs** → [Fractional Factorial](#fractional-factorial-designs)
- **Screening 8+ factors** → [Plackett-Burman](#plackett-burman-screening)

**Step 4: Generate design matrix**

Create run-by-run table with factor settings for each experimental run. See [Design Matrix Examples](#design-matrix-examples) for format.

**Step 5: Randomize and document protocol**

Randomize run order, specify blocking if needed, detail measurement procedures, and plan replication strategy. See [Execution Details](#execution-details) for guidance.

**Step 6: Finalize experiment plan**

Create complete `design-of-experiments.md` document using [Document Structure Template](#document-structure-template). Self-check with quality criteria in [Quality Checklist](#quality-checklist).

---

## Document Structure Template

Use this structure for the final `design-of-experiments.md` file:

```markdown
# Design of Experiments: [Experiment Name]

## 1. Objective

**Goal**: [Screening | Optimization | Response Surface | Robust Design]

**Context**: [1-2 sentences describing the system/process being studied]

**Success Criteria**: [What constitutes a successful experiment? Measurable outcomes.]

**Constraints**:
- Budget: [Maximum number of runs allowed]
- Time: [Deadline or duration per run]
- Resources: [Equipment, personnel, materials]

## 2. Factors and Levels

| Factor | Type | Low Level (-1) | High Level (+1) | Center (0) | Units | Rationale |
|--------|------|----------------|-----------------|------------|-------|-----------|
| A: [Name] | Control | [value] | [value] | [value] | [units] | [Why this factor?] |
| B: [Name] | Control | [value] | [value] | [value] | [units] | [Why this factor?] |
| C: [Name] | Noise | [value] | [value] | - | [units] | [Uncontrollable variation] |

**Factor Selection Rationale**: [Why these factors? Any excluded? Assumptions?]

## 3. Response Variables

| Response | Description | Measurement Method | Target | Units |
|----------|-------------|-------------------|---------|-------|
| Y1: [Name] | [What it measures] | [How measured] | [Maximize/Minimize/Target value] | [units] |
| Y2: [Name] | [What it measures] | [How measured] | [Maximize/Minimize/Target value] | [units] |

**Response Selection Rationale**: [Why these responses? Any tradeoffs?]

## 4. Experimental Design

**Design Type**: [Full Factorial 2^k | Fractional Factorial 2^(k-p) | Plackett-Burman | Central Composite | Box-Behnken]

**Resolution**: [For fractional factorials: III, IV, or V]

**Runs**:
- Design points: [number]
- Center points: [number of replicates at center]
- Total runs: [design + center]

**Design Rationale**: [Why this design? What can/can't it detect?]

## 5. Design Matrix

| Run | Order | Block | A | B | C | Y1 | Y2 | Notes |
|-----|-------|-------|---|---|---|----|----|-------|
| 1 | 5 | 1 | -1 | -1 | -1 | | | |
| 2 | 12 | 1 | +1 | -1 | -1 | | | |
| 3 | 3 | 1 | -1 | +1 | -1 | | | |
| 4 | 8 | 1 | +1 | +1 | -1 | | | |
| 5 | 1 | 2 | -1 | -1 | +1 | | | |
| ... | ... | ... | ... | ... | ... | | | |

**Randomization**: Run order randomized using [method]. Original design point order preserved in "Run" column.

**Blocking**: [If used] Runs blocked by [day/batch/operator/etc.] to control for [nuisance variable].

## 6. Execution Protocol

**Preparation**:
- [ ] [Equipment setup/calibration steps]
- [ ] [Material preparation]
- [ ] [Personnel training]

**Run Procedure**:
1. [Step-by-step protocol for each run]
2. [Factor settings to apply]
3. [Wait/equilibration time]
4. [Response measurement procedure]
5. [Recording method]

**Quality Controls**:
- [Measurement calibration checks]
- [Process stability verification]
- [Outlier detection procedure]

**Timeline**: [Start date, duration per run, expected completion]

## 7. Analysis Plan

**Primary Analysis**:
- Calculate main effects for factors A, B, C
- Calculate 2-way interaction effects (AB, AC, BC)
- Fit linear model: Y = β0 + β1·A + β2·B + β3·C + β12·AB + ...
- ANOVA to test significance (α = 0.05)
- Residual diagnostics (normality, constant variance, independence)

**Graphical Analysis**:
- Main effects plot
- Interaction plot
- Pareto chart of standardized effects
- Residual plots (normal probability, vs fitted, vs order)

**Decision Criteria**:
- Effects significant at p < 0.05 are considered important
- Interaction present if p(interaction) < 0.05
- Optimal settings chosen to [maximize/minimize] Y1 while [constraint on Y2]

**Follow-up**:
- If curvature detected → Run [response surface design]
- If additional factors identified → Run [screening design]
- Confirmation runs: [Number] at predicted optimum settings

## 8. Assumptions and Limitations

**Assumptions**:
- [Linear relationship between factors and response]
- [No strong higher-order interactions]
- [Homogeneous variance across factor space]
- [Errors are independent and normally distributed]
- [Process is stable during experiment]

**Limitations**:
- [Design resolution limits – e.g., 2-way interactions confounded]
- [Factor range restrictions]
- [Measurement precision limits]
- [External validity – generalization beyond tested region]

**Risks**:
- [What could invalidate results?]
- [Mitigation strategies]

## 9. Expected Outcomes

**If screening design**:
- Pareto chart identifying 3-5 critical factors from [N] candidates
- Effect size estimates with confidence intervals
- Shortlist for follow-up optimization experiment

**If optimization design**:
- Optimal factor settings: A = [value], B = [value], C = [value]
- Predicted response at optimum: Y1 = [value] ± [CI]
- Interaction insights: [Which factors interact? How?]

**If response surface**:
- Response surface equation: Y = [polynomial model]
- Contour/surface plots showing optimal region
- Sensitivity analysis showing robustness

**Deliverables**:
- This experiment plan document
- Completed design matrix with results (after execution)
- Analysis report with plots and recommendations
```

---

## Objective Definition

**Screening**: Screen 12 software config parameters to identify 3-5 affecting API response time. Success: Reduce candidates 60%+. Constraint: Max 16 runs.

**Optimization**: Optimize injection molding (temp, pressure, time) to minimize defect rate while cycle time < 45s. Success: < 2% defects (currently 8%). Constraint: Max 20 runs, 2 days.

**Response Surface**: Map yield vs temperature/pH, find maximum, model curvature. Success: R² > 0.90, optimal region. Constraint: Max 15 runs.

---

## Factor Table Template

| Factor | Type | Low (-1) | High (+1) | Center (0) | Units | Rationale |
|--------|------|----------|-----------|------------|-------|-----------|
| A: Temperature | Control | 150°C | 200°C | 175°C | °C | Literature suggests 150-200 range optimal |
| B: Pressure | Control | 50 psi | 100 psi | 75 psi | psi | Equipment operates 50-100, nonlinear expected |
| C: Time | Control | 10 min | 30 min | 20 min | min | Longer times may improve but cost increases |
| D: Humidity | Noise | 30% | 70% | - | %RH | Uncontrollable environmental variation |

**Type definitions**:
- **Control**: Factors you can set deliberately in the experiment
- **Noise**: Factors that vary but can't be controlled (for robust design)
- **Held constant**: Factors fixed at one level (not in design)

**Level selection guidance**:
- **2 levels**: Start here for screening/optimization. Detects linear effects and interactions.
- **3 levels**: Add center point to detect curvature. Required for response surface designs.
- **Categorical**: Use coded values (-1, +1) for categories (e.g., Supplier A = -1, Supplier B = +1)

---

## Full Factorial Designs

**When to use**: 2-5 factors, want to estimate all main effects and interactions, budget allows 2^k runs.

**Design structure**: Test all combinations of factor levels.

**Example: 2³ factorial (3 factors, 2 levels each = 8 runs)**

| Run | A | B | C |
|-----|---|---|---|
| 1 | - | - | - |
| 2 | + | - | - |
| 3 | - | + | - |
| 4 | + | + | - |
| 5 | - | - | + |
| 6 | + | - | + |
| 7 | - | + | + |
| 8 | + | + | + |

**Advantages**:
- Estimates all main effects and 2-way/3-way interactions
- No confounding
- Maximum precision for given number of factors

**Limitations**:
- Runs grow exponentially: 2³ = 8, 2⁴ = 16, 2⁵ = 32, 2⁶ = 64
- Inefficient for screening (wastes runs on unimportant factors)

**Add center points**: Replicate 3-5 runs at center (0, 0, 0) to detect curvature and estimate pure error.

---

## Fractional Factorial Designs

**When to use**: 5+ factors, limited budget, willing to sacrifice some interaction information.

**Design structure**: Test a fraction (1/2, 1/4, 1/8) of full factorial, deliberately confounding higher-order interactions.

**Example: 2⁵⁻¹ design (5 factors, 16 runs instead of 32)**

**Resolution IV**: Main effects clear, 2-way interactions confounded with each other.

| Run | A | B | C | D | E |
|-----|---|---|---|---|---|
| 1 | - | - | - | - | + |
| 2 | + | - | - | - | - |
| 3 | - | + | - | - | - |
| 4 | + | + | - | - | + |
| 5 | - | - | + | - | - |
| ... | ... | ... | ... | ... | ... |

**Generator**: E = ABCD (defining relation: I = ABCDE)

**Confounding structure**:
- A confounded with BCDE
- AB confounded with CDE
- ABC confounded with DE

**Resolution levels**:
- **Resolution III**: Main effects confounded with 2-way interactions. Use for screening only.
- **Resolution IV**: Main effects clear, 2-way confounded with 2-way. Good for screening + some optimization.
- **Resolution V**: Main effects and 2-way clear, 2-way confounded with 3-way. Preferred for optimization.

**Choosing fraction**: Use standard designs (tables available) or design software to ensure desired resolution.

---

## Plackett-Burman Screening

**When to use**: Screen 8-15 factors with minimal runs, only care about main effects.

**Design structure**: Orthogonal design with runs = next multiple of 4 above number of factors.

**Example: 12-run Plackett-Burman for up to 11 factors**

| Run | A | B | C | D | E | F | G | H | J | K | L |
|-----|---|---|---|---|---|---|---|---|---|---|---|
| 1 | + | + | - | + | + | + | - | - | - | + | - |
| 2 | + | - | + | + | + | - | - | - | + | - | + |
| 3 | - | + | + | + | - | - | - | + | - | + | + |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Advantages**:
- Very efficient: Screen 11 factors in 12 runs (vs 2048 for full factorial)
- Main effects estimated independently

**Limitations**:
- 2-way interactions completely confounded with main effects
- Only use when interactions unlikely or unimportant
- Cannot estimate interactions

**Use case**: Early-stage screening to reduce 15 candidates to 4-5 for follow-up factorial design.

---

## Design Matrix Examples

**Format**: Each row = one run. **Columns**: Run (design point #), Order (randomized sequence), Block (if used), Factors (coded -1/0/+1 or actual values), Responses (blank until execution), Notes (observations).

| Run | Order | A: Temp (°C) | B: Press (psi) | C: Time (min) | Y1: Yield (%) | Y2: Cost ($) |
|-----|-------|--------------|----------------|---------------|---------------|--------------|
| 1 | 3 | 150 | 50 | 10 | | |
| 2 | 7 | 200 | 50 | 10 | | |
| 3 | 1 | 150 | 100 | 10 | | |
| 4 | 5 | 200 | 100 | 10 | | |

---

## Execution Details

**Randomization**: Eliminates bias from time trends/drift. Method: (1) List runs, (2) Assign random numbers, (3) Sort by random number = execution order, (4) Document both orders. Exception: Don't randomize hard-to-change factors (use split-plot design, see methodology.md).

**Blocking**: Use when runs span days/batches/operators. Method: Divide into 2-4 balanced blocks, randomize within each, analyze with block as factor. Example: 16 runs over 2 days → 2 blocks of 8.

**Replication**: True replication (repeat entire run), repeated measures (multiple measurements per run), or center points (3-5 replicates at center for pure error). Guidance: Always include 3-5 center points for continuous factors.

---

## Quality Checklist

Before finalizing the experiment plan, verify:

**Objective & Scope**:
- [ ] Goal clearly stated (screening | optimization | response surface | robust)
- [ ] Success criteria are measurable and realistic
- [ ] Constraints documented (runs, time, cost)

**Factors**:
- [ ] All important factors included
- [ ] Levels span meaningful range (not too narrow, not outside feasible region)
- [ ] Factor types identified (control vs noise)
- [ ] Rationale for each factor documented

**Responses**:
- [ ] Responses are objective and quantitative
- [ ] Measurement method specified and validated
- [ ] Target direction clear (maximize | minimize | hit target)

**Design**:
- [ ] Design type appropriate for objective and budget
- [ ] Design resolution adequate (e.g., Resolution IV+ if interactions matter)
- [ ] Run count justified (power analysis or practical limit)
- [ ] Design matrix correct (orthogonal, balanced)

**Execution**:
- [ ] Randomization method specified
- [ ] Blocking used if runs span nuisance variable levels
- [ ] Replication plan documented (center points, full replicates)
- [ ] Protocol detailed enough for independent execution
- [ ] Timeline realistic

**Analysis**:
- [ ] Analysis plan specified before data collection
- [ ] Significance level (α) stated
- [ ] Decision criteria clear
- [ ] Residual diagnostics planned
- [ ] Follow-up strategy identified

**Assumptions & Risks**:
- [ ] Key assumptions stated explicitly
- [ ] Limitations acknowledged (resolution, range, measurement)
- [ ] Risks identified with mitigation plans
