# Advanced Chain Estimation → Decision → Storytelling Methodology

## Workflow

Copy this checklist and track your progress:

```
Advanced Analysis Progress:
- [ ] Step 1: Select appropriate advanced technique for complexity
- [ ] Step 2: Build model (decision tree, Monte Carlo, real options)
- [ ] Step 3: Run analysis and interpret results
- [ ] Step 4: Validate robustness across scenarios
- [ ] Step 5: Translate technical findings into narrative
```

**Step 1: Select appropriate advanced technique for complexity**

Choose technique based on decision characteristics: decision trees for sequential choices, Monte Carlo for multiple interacting uncertainties, real options for flexibility value, multi-criteria analysis for qualitative + quantitative factors. See [Technique Selection Guide](#technique-selection-guide) for decision flowchart.

**Step 2: Build model**

Structure problem using chosen technique: define states and branches for decision trees, specify probability distributions for Monte Carlo, identify options and decision points for real options analysis, establish criteria and weights for multi-criteria. See technique-specific sections below for modeling guidance.

**Step 3: Run analysis and interpret results**

Execute calculations (manually for small trees, with tools for complex simulations), interpret output distributions or decision paths, identify dominant strategies or highest-value options, and quantify value of information or flexibility where applicable.

**Step 4: Validate robustness across scenarios**

Test assumptions with stress testing, vary key parameters to check sensitivity, compare results across different modeling approaches, and identify conditions where conclusion changes. See [Sensitivity and Robustness Testing](#sensitivity-and-robustness-testing).

**Step 5: Translate technical findings into narrative**

Convert technical analysis into business language, highlight key insights without overwhelming with methodology, explain "so what" for decision-makers, and provide clear recommendation with confidence bounds. See [Communicating Complex Analysis](#communicating-complex-analysis).

---

## Technique Selection Guide

**Decision Trees** → Sequential decisions with discrete outcomes and known probabilities
- Use when: Clear sequence of choices, branching scenarios, need optimal path
- Example: Build vs buy with adoption uncertainty

**Monte Carlo Simulation** → Multiple interacting uncertainties with continuous distributions
- Use when: Many uncertain variables, complex interactions, need probability distributions
- Example: Project NPV with uncertain cost, revenue, timeline

**Real Options Analysis** → Decisions with flexibility value (defer, expand, abandon)
- Use when: Uncertainty resolves over time, value of waiting, staged commitments
- Example: Pilot before full launch, expand if successful

**Multi-Criteria Decision Analysis (MCDA)** → Mix of quantitative and qualitative factors
- Use when: Multiple objectives, stakeholder tradeoffs, subjective criteria
- Example: Vendor selection (cost + quality + relationship)

---

## Decision Trees

### Structure
- **Decision node (□)**: Your choice
- **Chance node (○)**: Uncertain outcome with probabilities
- **Terminal node**: Final payoff

### Method
1. Map all decisions and chance events
2. Assign probabilities to chance events
3. Work backward: calculate EV at chance nodes, choose best at decision nodes
4. Identify optimal path

### Example
```
□ Build vs Buy
├─ Build → ○ Success (60%) → $500k
│         └─ Fail (40%) → $100k
└─ Buy → ○ Fits (70%) → $400k
         └─ Doesn't (30%) → $150k

Build EV = (500 × 0.6) + (100 × 0.4) = $340k
Buy EV = (400 × 0.7) + (150 × 0.3) = $325k
Decision: Build (higher EV)
```

### Value of Information
- EVPI = EV with perfect info - EV without info
- Tells you how much to spend on reducing uncertainty

---

## Monte Carlo Simulation

### When to Use
- Multiple uncertain variables (>3)
- Complex interactions between variables
- Need full probability distribution of outcomes
- Continuous ranges (not discrete scenarios)

### Method
1. **Identify uncertain variables**: cost, revenue, timeline, adoption rate, etc.
2. **Define distributions**: normal, log-normal, triangular, uniform
3. **Specify correlations**: if variables move together
4. **Run simulation**: 10,000+ iterations
5. **Analyze output**: mean, median, percentiles, probability of success

### Distribution Types
- **Normal**: μ ± σ (height, measurement error)
- **Log-normal**: positively skewed (project duration, costs)
- **Triangular**: min/most likely/max (quick estimation)
- **Uniform**: all values equally likely (no information)

### Interpretation
- **P50 (median)**: 50% chance of exceeding
- **P10/P90**: 80% confidence interval
- **Probability of target**: P(NPV > $0), P(ROI > 20%)

### Tools
- Excel: =NORM.INV(RAND(), mean, stdev)
- Python: `numpy.random.normal(mean, stdev, size=10000)`
- @RISK, Crystal Ball: Monte Carlo add-ins

---

## Real Options Analysis

### Concept
Flexibility has value. Option to defer, expand, contract, or abandon is worth more than committing upfront.

### When to Use
- Uncertainty resolves over time (can learn before committing)
- Irreversible investments (can't easily reverse)
- Staged decisions (pilot → scale)

### Types of Options
- **Defer**: Wait for more information before committing
- **Expand**: Scale up if successful
- **Contract/Abandon**: Scale down or exit if unsuccessful
- **Switch**: Change approach mid-course

### Valuation Approach

**Simple NPV (no flexibility):**
- Commit now: EV = Σ(outcome × probability)

**With real option:**
- Value = NPV of commitment + Value of flexibility
- Flexibility value = Expected payoff from optimal future decision - Expected payoff from committing now

### Example
- **Commit to full launch now**: $1M investment, 60% success → $3M, 40% fail → $0
  - EV = (3M × 0.6) + (0 × 0.4) - 1M = $800K

- **Pilot first ($200K), then decide**:
  - Good pilot (60%) → full launch → EV $1.8M (0.6 × 3M - 1M)
  - Bad pilot (40%) → abandon → lose $200K
  - EV = (1.8M × 0.6) + (-0.2M × 0.4) = $1.0M

- **Real option value** = $1.0M - $800K = $200K (value of flexibility to learn first)

---

## Multi-Criteria Decision Analysis (MCDA)

### When to Use
- Multiple objectives that can't be reduced to single metric (not just NPV)
- Qualitative + quantitative factors
- Stakeholder tradeoffs (different groups value different things)

### Method

**1. Identify criteria** (from stakeholder perspectives)
- Cost, speed, quality, risk, strategic fit, customer impact, etc.

**2. Weight criteria** (based on priorities)
- Sum to 100%
- Finance might weight cost 40%, Product weights customer impact 30%

**3. Score alternatives** (1-5 or 1-10 scale on each criterion)
- Alternative A: Cost=4, Speed=2, Quality=5
- Alternative B: Cost=2, Speed=5, Quality=3

**4. Calculate weighted scores**
- A = (4 × 0.3) + (2 × 0.4) + (5 × 0.3) = 3.5
- B = (2 × 0.3) + (5 × 0.4) + (3 × 0.3) = 3.5

**5. Sensitivity analysis** on weights
- How much would weights need to change to flip the decision?

### Handling Qualitative Criteria
- **Scoring rubric**: Define what 1, 3, 5 means for "strategic fit"
- **Pairwise comparison**: Compare alternatives head-to-head on each criterion
- **Range**: Use min-max scaling to normalize disparate units

---

## Sensitivity and Robustness Testing

### One-Way Sensitivity
- Vary one parameter at a time (e.g., cost ±20%)
- Check if conclusion changes
- Identify which parameters matter most

### Two-Way Sensitivity
- Vary two parameters simultaneously
- Create sensitivity matrix or contour plot
- Example: Cost (rows) × Revenue (columns) → NPV

### Tornado Diagram
- Bar chart showing impact of each parameter
- Longest bars = most sensitive parameters
- Focus analysis on top 2-3 drivers

### Scenario Analysis
- Define coherent scenarios (pessimistic, base, optimistic)
- Not just parameter ranges, but plausible futures
- Calculate outcome for each complete scenario

### Break-Even Analysis
- At what value does conclusion change?
- "Need revenue >$500K to beat alternative"
- "If cost exceeds $300K, pivot to Plan B"

### Stress Testing
- Extreme scenarios (worst case everything goes wrong)
- Identify fragility: "Works unless X and Y both fail"
- Build contingency plans for stress scenarios

---

## Communicating Complex Analysis

### For Executives
**Focus**: Bottom line, confidence, risks
- Recommendation (1 sentence)
- Key numbers (EV, NPV, ROI)
- Confidence level (P10-P90 range)
- Top 2 risks + mitigations
- Decision criteria: "Proceed if X, pivot if Y"

### For Technical Teams
**Focus**: Methodology, assumptions, sensitivity
- Modeling approach and rationale
- Key assumptions with justification
- Sensitivity analysis results
- Robustness checks performed
- Limitations of analysis

### For Finance
**Focus**: Numbers, assumptions, financial metrics
- Cash flow timing
- Discount rate and rationale
- NPV, IRR, payback period
- Risk-adjusted returns
- Comparison to hurdle rate

### General Principles
- **Lead with conclusion**, then support with analysis
- **Show confidence bounds**, not just point estimates
- **Explain "so what"**, not just "what"
- **Use visuals**: probability distributions, decision trees, tornado charts
- **Be honest about limitations**: "Assumes X, sensitive to Y"

---

## Common Pitfalls in Advanced Analysis

### False Precision
- **Problem**: Reporting $1,234,567 when uncertainty is ±50%
- **Fix**: Round appropriately. Use ranges, not points.

### Ignoring Correlations
- **Problem**: Modeling all uncertainties as independent when they're linked
- **Fix**: Specify correlations in Monte Carlo (costs move together, revenue and volume linked)

### Overfit ting Models
- **Problem**: Building complex models with 20 parameters when data is thin
- **Fix**: Keep models simple. Complexity doesn't equal accuracy.

### Anchoring on Base Case
- **Problem**: Treating "most likely" as "expected value"
- **Fix**: Calculate probability-weighted EV. Assymetric distributions matter.

### Analysis Paralysis
- **Problem**: Endless modeling instead of deciding
- **Fix**: Set time limits. "Good enough" threshold. Decide with available info.

### Confirmation Bias
- **Problem**: Modeling to justify predetermined conclusion
- **Fix**: Model alternatives fairly. Seek disconfirming evidence. External review.

### Ignoring Soft Factors
- **Problem**: Optimizing NPV while ignoring strategic fit, team morale, brand impact
- **Fix**: Use MCDA for mixed quantitative + qualitative. Make tradeoffs explicit.

---

## Advanced Tools and Resources

### Spreadsheet Tools
- **Excel**: Data tables, Scenario Manager, Goal Seek
- **Google Sheets**: Same capabilities, collaborative

### Specialized Software
- **@RISK** (Palisade): Monte Carlo simulation add-in for Excel
- **Crystal Ball** (Oracle): Similar Monte Carlo tool
- **Python**: `numpy`, `scipy`, `simpy` for custom simulations
- **R**: Statistical analysis and simulation

### When to Use Tools vs. Manual
- **Manual** (small decision trees): < 10 branches, quick calculation
- **Spreadsheet** (medium complexity): Decision trees, simple Monte Carlo (< 5 variables)
- **Specialized tools** (high complexity): 10+ uncertain variables, complex correlations, sensitivity analysis

### Learning Resources
- Decision analysis: "Decision Analysis for the Professional" - Skinner
- Monte Carlo: "Risk Analysis in Engineering" - Modarres
- Real options: "Real Options" - Copeland & Antikarov
- MCDA: "Multi-Criteria Decision Analysis" - Belton & Stewart

---

## Summary

**Choose technique based on problem structure:**
- Sequential choices → Decision trees
- Multiple uncertainties → Monte Carlo
- Flexibility value → Real options
- Mixed criteria → MCDA

**Focus on:**
- Robust conclusions (stress test assumptions)
- Clear communication (translate technical to business language)
- Actionable insights (not just numbers)
- Honest limits (acknowledge what analysis can't tell you)

**Remember:**
- Models inform decisions, don't make them
- Simple model well-executed beats complex model poorly-executed
- Transparency about assumptions matters more than sophistication
- "All models are wrong, some are useful" - George Box
