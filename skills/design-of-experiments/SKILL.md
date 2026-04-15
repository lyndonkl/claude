---
name: design-of-experiments
description: Generates structured experimental designs (factorial, response surface, Taguchi) to systematically discover how multiple factors affect outcomes while minimizing experimental runs. Use when optimizing multi-factor systems with limited experimental budget, screening many variables to find the vital few, discovering interactions between parameters, mapping response surfaces for peak performance, validating robustness to noise factors, or when users mention factorial designs, A/B/n testing, parameter tuning, or process optimization.
---
# Design of Experiments

## Table of Contents
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Design of Experiments Progress:
- [ ] Step 1: Define objectives and constraints
- [ ] Step 2: Identify factors, levels, and responses
- [ ] Step 3: Choose experimental design
- [ ] Step 4: Plan execution details
- [ ] Step 5: Create experiment plan document
- [ ] Step 6: Validate quality
```

**Step 1: Define objectives and constraints**

Clarify the experiment goal (screening vs optimization), response metric(s), experimental budget (max runs), time/cost constraints, and success criteria. See [Common Patterns](#common-patterns) for typical objectives.

**Step 2: Identify factors, levels, and responses**

List all candidate factors (controllable inputs), specify levels for each factor (low/high or discrete values), categorize factors (control vs noise), and define response variables (measurable outputs). For screening many factors (8+), see [resources/methodology.md](resources/methodology.md#screening-designs) for Plackett-Burman and fractional factorial approaches.

**Step 3: Choose experimental design**

Based on objective and constraints:
- **For screening 5+ factors with limited runs** → Use [resources/methodology.md](resources/methodology.md#screening-designs) for fractional factorial or Plackett-Burman
- **For optimizing 2-5 factors** → Use [resources/template.md](resources/template.md#factorial-designs) for full or fractional factorial
- **For response surface mapping** → Use [resources/methodology.md](resources/methodology.md#response-surface-methodology) for central composite or Box-Behnken
- **For robust design against noise** → Use [resources/methodology.md](resources/methodology.md#taguchi-methods) for parameter vs noise factor arrays

**Step 4: Plan execution details**

Specify randomization order (eliminate time trends), blocking strategy (control nuisance variables), replication plan (estimate error), sample size justification (power analysis), and measurement protocols. See [Guardrails](#guardrails) for critical requirements.

**Step 5: Create experiment plan document**

Create `design-of-experiments.md` with sections: objective, factors table, design matrix (run order with factor settings), response variables, execution protocol, and analysis plan. Use [resources/template.md](resources/template.md) for structure.

**Step 6: Validate quality**

Self-assess using [resources/evaluators/rubric_design_of_experiments.json](resources/evaluators/rubric_design_of_experiments.json). Check: objective clarity, factor completeness, design appropriateness, randomization plan, measurement protocol, statistical power, analysis plan, and deliverable quality. **Minimum standard**: Average score ≥ 3.5 before delivering.

## Common Patterns

**Pattern 1: Screening (many factors → vital few)**
- **Context**: 10-30 candidate factors, limited budget, want to identify 3-5 critical factors
- **Approach**: Plackett-Burman or fractional factorial (Resolution III/IV)
- **Output**: Pareto chart of effect sizes, shortlist for follow-up optimization
- **Example**: Software performance tuning with 15 configuration parameters

**Pattern 2: Optimization (find best settings)**
- **Context**: 2-5 factors already identified as important, want to find optimal levels
- **Approach**: Full factorial (2^k) or fractional factorial + steepest ascent
- **Output**: Main effects plot, interaction plots, recommended settings
- **Example**: Manufacturing process with temperature, pressure, time factors

**Pattern 3: Response Surface (map the landscape)**
- **Context**: Need to understand curvature, find maximum/minimum, quantify tradeoffs
- **Approach**: Central Composite Design (CCD) or Box-Behnken
- **Output**: Response surface equation, contour plots, optimal region
- **Example**: Chemical formulation with ingredient ratios

**Pattern 4: Robust Design (work despite noise)**
- **Context**: Product/process must perform well despite uncontrollable variation
- **Approach**: Taguchi inner-outer array (control × noise factors)
- **Output**: Settings that minimize sensitivity to noise factors
- **Example**: Consumer product that must work across temperature/humidity ranges

**Pattern 5: Sequential Experimentation (learn then refine)**
- **Context**: High uncertainty, want to learn iteratively with minimal waste
- **Approach**: Screening → Steepest ascent → Response surface → Confirmation
- **Output**: Progressively refined understanding and settings
- **Example**: New product development with unknown factor relationships

## Guardrails

**Design requirements:**

1. **Randomize run order**: Eliminates time-order bias and confounding with lurking variables. Use random number generator, not "convenient" sequences.

2. **Replicate center points**: For designs with continuous factors, replicate center point runs (3-5 times) to estimate pure error and detect curvature.

3. **Preserve critical interactions**: In fractional factorials, avoid confounding important 2-way interactions with main effects. Choose Resolution IV or higher if interactions matter.

4. **Check design balance**: Ensure orthogonality (factors are uncorrelated in design matrix). Correlation > 0.3 reduces precision and interpretability.

5. **Define response precisely**: Use objective, quantitative, repeatable measurements. Avoid subjective scoring unless calibrated with multiple raters.

6. **Justify sample size**: Run power analysis to ensure design can detect meaningful effect sizes with acceptable Type II error risk (beta at most 0.20).

7. **Document assumptions**: State expected effect magnitudes, interaction assumptions, noise variance estimates. Design validity depends on these.

8. **Plan for analysis before running**: Specify statistical tests, significance level (alpha), effect size metrics before data collection to prevent p-hacking.

**Common pitfalls:**

- ❌ **One-factor-at-a-time (OFAT)**: Misses interactions, requires more runs than factorial designs
- ❌ **Ignoring blocking**: If runs span days/batches/operators, block accordingly or confound results with time trends
- ❌ **Too many levels**: Use 2-3 levels initially. More levels increase runs exponentially.
- ❌ **Unmeasured factors**: If an important factor isn't controlled/measured, it becomes noise
- ❌ **Changing protocols mid-experiment**: Breaks design structure. If necessary, restart or analyze separately.

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Quick-start templates for common designs (factorial, screening, response surface)
- **[resources/methodology.md](resources/methodology.md)**: Advanced techniques (optimal designs, Taguchi, mixture experiments, sequential strategies)
- **[resources/evaluators/rubric_design_of_experiments.json](resources/evaluators/rubric_design_of_experiments.json)**: Quality criteria for experiment plans

**Typical workflow time:**

- Simple factorial (2-4 factors): 15-30 minutes
- Screening design (8+ factors): 30-45 minutes
- Response surface design: 45-60 minutes
- Robust design (Taguchi): 60-90 minutes

**When to escalate:**

- User needs mixture experiments (factors must sum to 100%)
- Split-plot designs required (hard-to-change factors)
- Optimal designs for irregular constraints
- Bayesian adaptive designs
→ Use [resources/methodology.md](resources/methodology.md) for these advanced cases

**Inputs required:**

- **Process/System**: What you're experimenting on
- **Factors**: List of controllable inputs with candidate levels
- **Responses**: Measurable outputs (KPIs, metrics)
- **Constraints**: Budget (max runs), time, resources
- **Objective**: Screening, optimization, response surface, or robust design

**Outputs produced:**

- `design-of-experiments.md`: Complete experiment plan with design matrix, randomization, protocols, analysis approach
