# Valuation Reconciler Methodology

Advanced techniques for reconciling multiple valuations, reverse-engineering market assumptions, analyzing catalysts, and calibrating margin of safety.

## Table of Contents
- [Three-Lens Reconciliation Framework](#three-lens-reconciliation-framework)
- [Implied Growth and ROIC Reverse Engineering](#implied-growth-and-roic-reverse-engineering)
- [Catalyst Analysis Framework](#catalyst-analysis-framework)
- [Margin of Safety Calibration](#margin-of-safety-calibration)
- [EVA Value Decomposition](#eva-value-decomposition)
- [Common Divergence Patterns](#common-divergence-patterns)

---

## Three-Lens Reconciliation Framework

Reconciliation examines the company through three lenses. Each lens answers a different question. The goal is to identify where the lenses agree (convergence) and where they disagree (divergence), then understand why.

### Lens 1: Intrinsic Value (DCF)

**Question**: What is this company worth based on its expected future cash flows?

**Strengths**:
- Grounded in fundamentals (cash flows, growth, risk)
- Independent of current market sentiment
- Forces explicit assumptions about future trajectory
- Most appropriate for unique businesses with few peers

**Weaknesses**:
- Sensitive to terminal value assumptions (often 50-80% of total value)
- Requires estimates of growth rate, margins, and discount rate far into the future
- Small changes in WACC or stable growth rate produce large value swings
- Garbage in, garbage out -- quality depends entirely on input assumptions

**When to anchor on DCF**:
- Company is unique (few meaningful comparables)
- Significant operational transformation underway (margins or growth changing)
- Company is at a different life cycle stage than peers
- User has high confidence in the business narrative and cash flow projections

### Lens 2: Relative Value (Multiples vs Peers)

**Question**: Is this company cheap or expensive relative to similar companies?

**Two sub-approaches**:

**Simple peer comparison**: Compare target's multiple (PE, EV/EBITDA) to peer median. Adjust qualitatively for differences in growth, risk, and margins.
- Advantage: Simple, intuitive, fast
- Limitation: Does not control for differences systematically

**Sector regression**: Regress the multiple against its fundamental drivers (growth, risk, margin) across the peer universe. Use predicted multiple for target company.
- Advantage: Controls for multiple differences simultaneously
- Limitation: Requires 15-20+ data points; regression may have low R-squared

**When to anchor on relative valuation**:
- Company is a commodity business in a well-defined industry
- Many true comparables exist (same industry, similar size, similar stage)
- Market is efficiently pricing the peer group
- Quick assessment needed; DCF input quality is low

### Lens 3: Relative Value (vs Market Regression)

**Question**: Is this company cheap or expensive relative to the entire market, controlling for fundamentals?

**Approach**: Run the regression across the entire market (not just sector) using fundamental drivers. This tests whether the company is mispriced relative to all companies, not just its narrow peer group.

**When this lens adds value**:
- Sector itself may be over/undervalued (all tech stocks expensive, all energy stocks cheap)
- Company straddles multiple sectors (conglomerate)
- Peer universe is too small for a meaningful sector regression

### Reconciliation Process

**Step 1: Tabulate results from all three lenses**

Record DCF value, simple peer value, regression value, and (if applicable) market regression value. Note the spread between highest and lowest.

**Step 2: Diagnose divergences**

If spread is < 15%, the methods converge. The weighted average is a reasonable estimate with moderate confidence.

If spread is > 30%, significant divergence exists. Diagnose the source:

| Divergence Pattern | Likely Cause | Resolution |
|-------------------|-------------|------------|
| DCF >> Relative | Your growth/margin assumptions are more optimistic than what peers achieve | Review if narrative is too bullish; check if peers are temporarily depressed |
| DCF << Relative | Your DCF inputs are conservative, or peers are overvalued by the market | Check if WACC is too high or growth too low; consider whether sector is in a bubble |
| Peer median >> Regression | Target has weaker fundamentals than peer average | Regression is more reliable; peer median overstates value |
| Peer median << Regression | Target has stronger fundamentals than peer average | Regression captures this; peer median understates value |

**Step 3: Assign weights and compute final estimate**

Weights should reflect method appropriateness (see template.md confidence weight guidelines) and input quality. A DCF built on 5 years of stable cash flows deserves more weight than one built on speculative growth assumptions.

---

## Implied Growth and ROIC Reverse Engineering

Instead of asking "what is the stock worth?", flip the question: "what does the market believe about this company's future?"

### Implied Growth Rate Calculation

**Concept**: Hold all DCF inputs constant except revenue growth. Find the growth rate g* that produces a DCF value exactly equal to the current market price.

**Iterative procedure**:

1. Start with your base case DCF model (growth = your narrative assumption)
2. Note the DCF value vs market price
3. Adjust growth rate:
   - If DCF > market price, the market implies lower growth. Decrease g.
   - If DCF < market price, the market implies higher growth. Increase g.
4. Repeat until DCF value converges to within 1% of market price
5. The converged growth rate is the market's implied growth rate

**Practical approach for manual calculation**:

Compute DCF at three growth rates (e.g., 0%, your estimate, 2x your estimate). Plot value vs growth. Interpolate to find growth rate at market price.

**Interpretation guide**:

| Implied Growth vs Your Estimate | Interpretation |
|-------------------------------|----------------|
| Implied much lower (> 3pp gap) | Market is skeptical of growth story; potential buy if you have conviction |
| Implied slightly lower (1-3pp gap) | Modest disagreement; may reflect normal estimation difference |
| Implied approximately equal (< 1pp gap) | Market agrees with your growth view; no mispricing on growth dimension |
| Implied higher (> 1pp above yours) | Market is more optimistic; potential sell if you believe market is wrong |

### Implied ROIC Calculation

**Concept**: ROIC determines how much reinvestment is needed to achieve a given growth rate (g = ROIC x reinvestment rate). A higher ROIC means less reinvestment is needed for the same growth, producing higher free cash flows.

**Procedure**:

1. Hold growth rate constant at your estimate
2. Vary ROIC (which changes reinvestment rate and therefore FCFF)
3. Find ROIC* such that DCF(ROIC*) = market price

**Combined interpretation**:

The most revealing analysis varies both growth and ROIC together, constructing an "implied assumptions map":

| | Low ROIC (10%) | Mid ROIC (15%) | High ROIC (20%) |
|------|---------------|----------------|-----------------|
| **Low growth (3%)** | $ | $ | $ |
| **Mid growth (6%)** | $ | $ | $ |
| **High growth (9%)** | $ | $ | $ |

Shade the cell(s) closest to market price. This reveals the growth/quality combination the market is pricing in.

---

## Catalyst Analysis Framework

A catalyst is a specific event that causes the market to reprice the stock toward intrinsic value. Without catalysts, even correctly identified mispricing may persist indefinitely.

### Catalyst Classification

**Type 1: Information catalysts** -- New information changes market perception
- Earnings surprises (beat or miss)
- Guidance revisions
- Analyst initiations or upgrades
- Conference presentations revealing strategy details

**Type 2: Operational catalysts** -- Business events change fundamentals
- Product launch or FDA approval
- Restructuring completion
- Contract win or loss
- Capacity expansion
- Management change

**Type 3: Financial catalysts** -- Capital allocation events signal value
- Share buyback (signals management believes stock is cheap)
- Dividend initiation or increase
- Debt reduction or refinancing
- Spin-off or divestiture (unlocks sum-of-parts value)

**Type 4: External catalysts** -- Events outside company control
- Regulatory change (favorable or adverse)
- Industry consolidation (acquisition target potential)
- Macroeconomic shift (rate cuts benefiting rate-sensitive sectors)
- Competitor stumble (market share opportunity)

### Catalyst Evaluation Criteria

For each catalyst, assess:

**Specificity**: Is the event clearly defined? ("Q3 earnings report" is specific; "market will realize value" is not)

**Timing**: Is the expected date identifiable? Events within 6 months have more weight than those 18+ months away.

**Magnitude**: How much of the value gap could this catalyst close? Quantify in dollars per share or percentage of gap.

**Probability**: How likely is the catalyst to occur? Use historical base rates where possible.

**Independence**: Are catalysts independent of each other, or does catalyst B depend on catalyst A occurring first?

### Gap Closure Estimation

**Expected gap closure** = Sum of (catalyst impact x probability) for all identified catalysts

If expected gap closure < 30% of the total value gap within 12 months, the investment thesis depends on patience and multiple catalysts compounding. This increases the risk of thesis fatigue and should lower conviction.

If expected gap closure > 50% within 12 months, one or two high-probability catalysts could drive meaningful repricing. This supports a higher-conviction recommendation.

---

## Margin of Safety Calibration

Margin of safety protects against estimation error, not against being fundamentally wrong about the business. A 30% margin does not help if the narrative itself is incorrect.

### Calibration by Uncertainty Dimension

**Cash flow predictability**:
- Subscription revenue with 95%+ retention: low uncertainty, 10-15% margin
- Cyclical industrial with volatile demand: moderate uncertainty, 20-30% margin
- Pre-revenue biotech with binary outcomes: high uncertainty, 35-50% margin

**Forecast horizon sensitivity**:
- Terminal value < 50% of total DCF value: lower margin needed
- Terminal value 50-70%: standard margin
- Terminal value > 80%: higher margin needed (value depends on distant, uncertain cash flows)

**Information quality**:
- Public company with 10+ years of clean financials: lower margin
- Recently IPO'd with limited track record: higher margin
- Private company with limited disclosure: higher margin

**Model complexity**:
- Standard two-stage FCFF: lower margin
- Three-stage with multiple transitions: higher margin
- Special situations (failure probability, option pricing): higher margin

### Margin of Safety Decision Matrix

| Predictability | Forecast Horizon | Info Quality | Suggested Margin |
|---------------|-----------------|-------------|-----------------|
| High | Short (TV < 50%) | Good (10yr+ history) | 10-15% |
| High | Medium (TV 50-70%) | Good | 15-20% |
| Moderate | Medium | Moderate (3-10yr history) | 20-30% |
| Low | Long (TV > 70%) | Moderate | 25-35% |
| Low | Long | Poor (< 3yr history) | 35-50% |

### Adjusting Recommendations for Insufficient Margin

If the actual margin of safety falls below the suggested range:
- Reduce conviction level (high to moderate, moderate to low)
- Widen the price target range (reflecting greater uncertainty)
- Require stronger catalysts to justify the position
- Consider a Hold instead of Buy, waiting for a better entry point

---

## EVA Value Decomposition

EVA (Economic Value Added) decomposition reveals how much of the firm's value comes from existing assets versus expected growth.

### Decomposition Formula

```
Firm Value = Invested Capital + PV of Future EVA

Where:
  EVA in year t = (ROIC_t - WACC) x Invested Capital_t
  PV of Future EVA = Sum of [EVA_t / (1 + WACC)^t]

Growth Premium = (Firm Value - Invested Capital) / Firm Value
```

### Interpretation

**Growth premium near 0%**: Market pays only for assets in place. Either the company earns ROIC approximately equal to WACC (no excess returns), or the market expects no growth. This is typical of mature commodity businesses.

**Growth premium 20-40%**: Market prices in moderate excess returns and growth. Common for established companies with competitive advantages.

**Growth premium 50-70%**: Market prices in significant excess returns sustained over many years. Common for high-quality growth companies (strong brands, network effects). Valuation is moderately sensitive to growth assumptions.

**Growth premium > 70%**: Market pays mostly for future growth. Valuation is highly sensitive to growth and competitive advantage assumptions. Small changes in narrative can produce large value swings. This is typical of high-growth tech, biotech, and young companies.

### Using EVA Decomposition in Reconciliation

Compare your EVA decomposition (based on your narrative) with the market's implied decomposition (using market price as firm value):

| Component | Your Narrative | Market Implied |
|-----------|---------------|----------------|
| Invested Capital | $ | $ |
| PV of Future EVA | $ | $ |
| Growth Premium | % | % |

If the market's implied growth premium is much lower than yours, the market is skeptical about the company's ability to earn excess returns (ROIC > WACC) going forward. This is the core disagreement driving the value gap.

---

## Common Divergence Patterns

### Pattern A: DCF High, Relative Low

**Diagnosis**: Your DCF assumptions (growth, margin, or risk) are more optimistic than what comparable companies achieve.

**Questions to resolve**:
- Is the target genuinely different from peers (better competitive position, unique catalyst)?
- Are your growth projections anchored in a specific, testable narrative?
- Could you be suffering from narrative bias (falling in love with the story)?

**Resolution**: If differences are justified by company-specific factors, weight DCF more. If not, revise DCF inputs downward toward peer-implied levels.

### Pattern B: DCF Low, Relative High

**Diagnosis**: Your DCF is conservative, or the entire peer group is overvalued.

**Questions to resolve**:
- Is your WACC too high (unreasonably pessimistic risk assessment)?
- Are your growth/margin assumptions below the company's historical performance?
- Is the peer group in a sentiment-driven bubble?

**Resolution**: If DCF inputs are genuinely conservative, consider that peers may be overvalued. Relative valuation says "cheap relative to peers" not "undervalued in absolute terms." If the whole sector is expensive, the relative value estimate is misleading.

### Pattern C: PE High, EV/EBITDA Low

**Diagnosis**: The two multiples disagree. This often reflects capital structure differences.

**Questions to resolve**:
- Does the company have significantly more or less debt than peers?
- Are there large non-cash charges (depreciation, amortization) distorting PE?
- Is interest expense unusually high or low?

**Resolution**: EV/EBITDA is capital-structure neutral, making it more reliable for cross-company comparison when leverage differs. If capital structure is the driver, weight EV/EBITDA more heavily.

### Pattern D: All Methods Agree, but Different from Price

**Diagnosis**: Strong convergence among valuation methods, but market price diverges. This is either a clear mispricing opportunity or a sign that you are missing information the market has.

**Questions to resolve**:
- Is there pending news (M&A rumor, regulatory action, earnings warning) driving the price?
- Has the stock price moved recently on information not yet reflected in your model?
- Is there a structural reason for mispricing (index rebalancing, forced selling, tax-loss harvesting)?

**Resolution**: Convergence across methods increases confidence, but verify that your information set is current. Check recent news, insider transactions, and short interest before committing to a strong recommendation.
