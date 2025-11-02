# Chain Estimation → Decision → Storytelling Template

## Workflow

Copy this checklist and track your progress:

```
Analysis Progress:
- [ ] Step 1: Gather inputs and define decision scope
- [ ] Step 2: Estimate costs, benefits, and probabilities
- [ ] Step 3: Calculate expected value and compare alternatives
- [ ] Step 4: Structure narrative with clear recommendation
- [ ] Step 5: Validate completeness with quality checklist
```

**Step 1: Gather inputs and define decision scope**

Clarify what decision needs to be made, identify 2-5 alternatives to compare, list key uncertainties (costs, benefits, probabilities), determine audience (executives, technical team, finance), and note constraints (budget, timeline, requirements). Use [Quick Template](#quick-template) structure below.

**Step 2: Estimate costs, benefits, and probabilities**

For each alternative, quantify all relevant costs (development, operation, opportunity cost), estimate benefits (revenue, savings, productivity gains), assign probabilities to scenarios (best/base/worst case), and use ranges rather than point estimates. See [Estimation Guidelines](#estimation-guidelines) for techniques.

**Step 3: Calculate expected value and compare alternatives**

Compute probability-weighted outcomes for each alternative, compare using appropriate decision criteria (NPV, IRR, payback, utility), identify which option has best risk-adjusted return, and test sensitivity to key assumptions. See [Decision Analysis](#decision-analysis) section.

**Step 4: Structure narrative with clear recommendation**

Follow storytelling framework: problem statement, alternatives considered, analysis summary, clear recommendation with reasoning, and next steps. Tailor level of detail to audience. See [Narrative Structure](#narrative-structure) for guidance.

**Step 5: Validate completeness with quality checklist**

Use [Quality Checklist](#quality-checklist) to verify: all alternatives considered, estimates are justified, probabilities are reasonable, expected value is calculated correctly, sensitivity analysis performed, narrative is clear and persuasive, assumptions stated explicitly.

## Quick Template

Copy this structure to create your analysis:

```markdown
# Decision: {Decision Question}

## 1. Decision Context

**What we're deciding:** {Clear statement of the choice}

**Why this matters:** {Business impact, urgency, strategic importance}

**Alternatives:**
1. {Option A}
2. {Option B}
3. {Option C}

**Key uncertainties:**
- {Variable 1}: {Range or distribution}
- {Variable 2}: {Range or distribution}
- {Variable 3}: {Range or distribution}

**Constraints:**
- Budget: {Available resources}
- Timeline: {Decision deadline, implementation timeline}
- Requirements: {Must-haves, non-negotiables}

**Audience:** {Who needs to approve this decision?}

---

## 2. Estimation

### Alternative 1: {Name}

**Costs:**
- Initial investment: ${Low}k - ${High}k (most likely: ${Base}k)
- Annual operational: ${Low}k - ${High}k per year
- Opportunity cost: {What we give up}

**Benefits:**
- Revenue impact: +${Low}k - ${High}k (most likely: ${Base}k)
- Cost savings: ${Low}k - ${High}k per year
- Strategic value: {Qualitative benefits}

**Probabilities:**
- Best case (30%): {Scenario description}
- Base case (50%): {Scenario description}
- Worst case (20%): {Scenario description}

**Key assumptions:**
- {Assumption 1}
- {Assumption 2}
- {Assumption 3}

### Alternative 2: {Name}
{Same structure}

### Alternative 3: {Name}
{Same structure}

---

## 3. Decision Analysis

### Expected Value Calculation

**Alternative 1: {Name}**
- Best case (30%): ${Amount} × 0.30 = ${Weighted}
- Base case (50%): ${Amount} × 0.50 = ${Weighted}
- Worst case (20%): ${Amount} × 0.20 = ${Weighted}
- **Expected value: ${Total}**

**Alternative 2: {Name}**
{Same calculation}
**Expected value: ${Total}**

**Alternative 3: {Name}**
{Same calculation}
**Expected value: ${Total}**

### Comparison

| Alternative | Expected Value | Risk Profile | Time to Value | Strategic Fit |
|-------------|----------------|--------------|---------------|---------------|
| {Alt 1}     | ${EV}          | {High/Med/Low} | {Timeline}    | {Score/10}    |
| {Alt 2}     | ${EV}          | {High/Med/Low} | {Timeline}    | {Score/10}    |
| {Alt 3}     | ${EV}          | {High/Med/Low} | {Timeline}    | {Score/10}    |

### Sensitivity Analysis

**What if {key variable} changes?**
- If {variable} is 20% higher: {Impact on decision}
- If {variable} is 20% lower: {Impact on decision}

**Most sensitive to:**
- {Variable 1}: {Explanation of impact}
- {Variable 2}: {Explanation of impact}

**Robustness check:**
- Conclusion holds if {conditions}
- Would change if {conditions}

---

## 4. Recommendation

**Recommended option: {Alternative X}**

**Reasoning:**
{1-2 paragraphs explaining why this is the best choice given the analysis}

**Key factors:**
- {Factor 1}: {Why it matters}
- {Factor 2}: {Why it matters}
- {Factor 3}: {Why it matters}

**Tradeoffs accepted:**
- We're accepting {downside} in exchange for {upside}
- We're prioritizing {value 1} over {value 2}

**Risks and mitigations:**
- **Risk**: {What could go wrong}
  - **Mitigation**: {How we'll address it}
- **Risk**: {What could go wrong}
  - **Mitigation**: {How we'll address it}

---

## 5. Next Steps

**If approved:**
1. {Immediate action 1} - {Owner} by {Date}
2. {Immediate action 2} - {Owner} by {Date}
3. {Immediate action 3} - {Owner} by {Date}

**Success metrics:**
- {Metric 1}: Target {value} by {date}
- {Metric 2}: Target {value} by {date}
- {Metric 3}: Target {value} by {date}

**Decision review:**
- Revisit this decision in {timeframe} to validate assumptions
- Key indicators to monitor: {metrics to track}

**What would change our mind:**
- If {condition}, we should reconsider
- If {condition}, we should accelerate
- If {condition}, we should pause
```

---

## Estimation Guidelines

### Cost Estimation

**Categories to consider:**
- **One-time costs**: Development, implementation, migration, training
- **Recurring costs**: Subscription fees, maintenance, support, infrastructure
- **Hidden costs**: Opportunity cost, technical debt, switching costs
- **Risk costs**: Probability-weighted downside scenarios

**Estimation techniques:**
- **Analogous**: Similar past projects (adjust for differences)
- **Parametric**: Cost per unit × quantity (e.g., $150k per engineer × 2 engineers)
- **Bottom-up**: Estimate components and sum
- **Three-point**: Best case, most likely, worst case → calculate expected value

**Expressing uncertainty:**
- Use ranges: $200k-$400k (not $300k)
- Assign probabilities: 60% likely $300k, 20% $200k, 20% $400k
- Show confidence: "High confidence" vs "Rough estimate"

### Benefit Estimation

**Categories to consider:**
- **Revenue impact**: New revenue, increased conversion, higher retention
- **Cost savings**: Reduced operational costs, avoided hiring, infrastructure savings
- **Productivity gains**: Time saved × value of time
- **Risk reduction**: Probability of bad outcome × cost of bad outcome
- **Strategic value**: Market positioning, competitive advantage, optionality

**Quantification approaches:**
- **Direct measurement**: Historical data, benchmarks, experiments
- **Proxy metrics**: Leading indicators that correlate with value
- **Scenario modeling**: Best/base/worst case with probabilities
- **Comparable analysis**: Similar initiatives at comparable companies

### Probability Assignment

**How to assign probabilities:**
- **Base rates**: Start with historical frequency (e.g., 70% of projects finish on time)
- **Adjustments**: Modify for specific circumstances (this project is simpler/more complex)
- **Expert judgment**: Multiple estimates, average or calibrated
- **Reference class forecasting**: Look at similar situations

**Common probability pitfalls:**
- **Overconfidence**: Ranges too narrow, probabilities too extreme (5% or 95%)
- **Anchoring**: First number becomes reference even if wrong
- **Optimism bias**: Best case feels more likely than it is
- **Planning fallacy**: Underestimating time and cost

**Calibration check:**
- If you say 70% confident, are you right 70% of the time?
- Test with past predictions if available
- Use wider ranges for higher uncertainty

---

## Decision Analysis

### Expected Value Calculation

**Formula:**
```
Expected Value = Σ (Outcome × Probability)
```

**Example:**
- Best case: $500k × 30% = $150k
- Base case: $300k × 50% = $150k
- Worst case: $100k × 20% = $20k
- Expected value = $150k + $150k + $20k = $320k

**Multi-year NPV:**
```
NPV = Σ (Cash Flow_t / (1 + discount_rate)^t)
```

**When to use:**
- **Expected value**: When outcomes are roughly linear with value (money, time)
- **Decision trees**: When sequence of choices matters
- **Monte Carlo**: When multiple uncertainties interact
- **Scoring/weighting**: When mix of quantitative and qualitative factors

### Comparison Methods

**1. Expected Value Ranking**
- Calculate EV for each alternative
- Rank by highest expected value
- **Best for**: Decisions with quantifiable outcomes

**2. NPV Comparison**
- Discount future cash flows to present value
- Compare NPV across alternatives
- **Best for**: Multi-year investments

**3. Payback Period**
- Time to recover initial investment
- Consider in addition to NPV (not instead of)
- **Best for**: When liquidity or fast ROI matters

**4. Weighted Scoring**
- Score each alternative on multiple criteria (1-10)
- Multiply by importance weight
- Sum weighted scores
- **Best for**: Mix of quantitative and qualitative factors

### Sensitivity Analysis

**One-way sensitivity:**
- Vary one input at a time (e.g., cost ±20%)
- Check if conclusion changes
- Identify which inputs matter most

**Tornado diagram:**
- Show impact of each variable on outcome
- Order by magnitude of impact
- Focus on top 2-3 drivers

**Scenario analysis:**
- Define coherent scenarios (pessimistic, base, optimistic)
- Calculate outcome for each complete scenario
- Assign probabilities to scenarios

**Break-even analysis:**
- At what value of {key variable} does decision change?
- Provides threshold for monitoring

---

## Narrative Structure

### Executive Summary (for executives)

**Format:**
1. **The decision** (1 sentence): What we're choosing between
2. **The recommendation** (1 sentence): What we should do
3. **The reasoning** (2-3 bullets): Key factors driving recommendation
4. **The ask** (1 sentence): What approval or resources needed
5. **The timeline** (1 sentence): When this happens

**Length:** 4-6 sentences, fits in one paragraph

**Example:**
> "We evaluated building custom analytics vs. buying a SaaS tool. Recommendation: Buy the SaaS solution. Key factors: (1) $130k lower expected cost due to build risk, (2) 6 months faster time-to-value, (3) proven reliability vs. custom development uncertainty. Requesting $20k implementation budget and $120k annual subscription approval. Implementation begins next month with value delivery in 8 weeks."

### Detailed Analysis (for stakeholders)

**Structure:**
1. **Problem statement**: Why this decision matters (1 paragraph)
2. **Alternatives considered**: Show you did the work (bullets)
3. **Analysis approach**: Methodology and assumptions (1 paragraph)
4. **Key findings**: Numbers, comparison, sensitivity (1-2 paragraphs)
5. **Recommendation**: Clear choice with reasoning (1-2 paragraphs)
6. **Risks and mitigations**: What could go wrong (bullets)
7. **Next steps**: Implementation plan (bullets)

**Length:** 1-2 pages

**Tone:** Professional, balanced, transparent about tradeoffs

### Technical Deep-Dive (for technical teams)

**Additional detail:**
- Estimation methodology and data sources
- Sensitivity analysis details
- Technical assumptions and constraints
- Implementation considerations
- Alternative approaches considered and why rejected

**Length:** 2-4 pages

**Tone:** Analytical, rigorous, shows technical depth

---

## Quality Checklist

Before finalizing, verify:

**Estimation quality:**
- [ ] All relevant costs included (one-time, recurring, opportunity, risk)
- [ ] All relevant benefits quantified or described
- [ ] Uncertainty expressed with ranges or probabilities
- [ ] Assumptions stated explicitly with justification
- [ ] Sources cited for estimates where applicable

**Decision analysis quality:**
- [ ] Expected value calculated correctly (probability × outcome)
- [ ] All alternatives compared fairly
- [ ] Sensitivity analysis performed on key variables
- [ ] Robustness tested (does conclusion hold across reasonable ranges?)
- [ ] Dominant option identified with clear rationale

**Narrative quality:**
- [ ] Clear recommendation stated upfront
- [ ] Problem statement explains why decision matters
- [ ] Alternatives shown (proves due diligence)
- [ ] Analysis summary appropriate for audience
- [ ] Tradeoffs acknowledged honestly
- [ ] Risks and mitigations addressed
- [ ] Next steps are actionable

**Communication quality:**
- [ ] Tailored to audience (exec vs technical vs finance)
- [ ] Jargon explained or avoided
- [ ] Key numbers highlighted
- [ ] Visual aids used where helpful (tables, charts)
- [ ] Length appropriate (not too long or too short)

**Integrity checks:**
- [ ] No cherry-picking of favorable data
- [ ] Downside scenarios included, not just upside
- [ ] Probabilities are calibrated (not overconfident)
- [ ] "What would change my mind" conditions stated
- [ ] Limitations and uncertainties acknowledged

---

## Common Decision Types

### Build vs Buy
- **Estimate**: Dev cost, maintenance, SaaS fees, implementation
- **Decision**: 3-5 year TCO with risk adjustment
- **Story**: Control vs. cost, speed vs. customization

### Market Entry
- **Estimate**: TAM/SAM/SOM, CAC, LTV, time to profitability
- **Decision**: NPV with market uncertainty scenarios
- **Story**: Growth opportunity vs. execution risk

### Hiring
- **Estimate**: Comp, recruiting, ramp time, productivity impact
- **Decision**: Cost per output vs. alternatives
- **Story**: Capacity constraints vs. efficiency gains

### Technology Migration
- **Estimate**: Migration cost, operational savings, risk reduction
- **Decision**: Multi-year TCO plus risk-adjusted benefits
- **Story**: Short-term pain for long-term gain

### Resource Allocation
- **Estimate**: Cost per initiative, expected impact
- **Decision**: Portfolio optimization or impact/effort ranking
- **Story**: Given constraints, maximize expected value
