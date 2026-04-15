# Valuation Reconciler Templates

Templates for reconciliation tables, implied assumption analysis, catalyst identification, recommendations, and investment thesis construction.

## Table of Contents
- [Reconciliation Table](#reconciliation-table)
- [Implied Assumptions Worksheet](#implied-assumptions-worksheet)
- [Catalyst Identification Template](#catalyst-identification-template)
- [Recommendation Template](#recommendation-template)
- [Investment Thesis Template](#investment-thesis-template)
- [Sensitivity Matrix Template](#sensitivity-matrix-template)

---

## Reconciliation Table

Assemble all valuation estimates side by side. Assign confidence weights based on method appropriateness for the company type.

### Valuation Summary

| Method | Value/Share | Key Assumptions | Confidence Weight |
|--------|------------|-----------------|-------------------|
| DCF (FCFF) | $ | Growth: %, Margin: %, WACC: % | % |
| DCF (FCFE) | $ | Growth: %, ke: % | % |
| PE Regression | $ | Predicted PE: x, R-squared: | % |
| PE Peer Median | $ | Peer median PE: x, applied to EPS: $ | % |
| EV/EBITDA Peers | $ | Peer median: x, applied to EBITDA/share: $ | % |
| EV/Sales | $ | Peer median: x, applied to Rev/share: $ | % |
| PBV | $ | Peer median: x, applied to BV/share: $ | % |
| Special Situations | $ | Adjustment: (failure prob, liquidity, etc.) | % |
| **Weighted Estimate** | **$** | | **100%** |

### Confidence Weight Guidelines

**When to weight DCF more heavily (50-70%)**:
- Unique business with few true comparables
- Company at different life cycle stage than peers
- Significant growth/margin trajectory change underway
- Financial services or capital-intensive firms where accounting distorts multiples

**When to weight relative valuation more heavily (50-70%)**:
- Commodity business in well-defined peer group (airlines, banks, REITs)
- Mature, stable company with predictable cash flows
- Industry where market pricing anchors on specific multiples (e.g., EV/EBITDA for telecom)
- Limited visibility into long-term growth trajectory

**When to weight special-situations adjustment heavily**:
- Negative earnings (failure-probability adjustment dominates)
- Distressed company (equity-as-option model provides floor)
- Private company (liquidity discount material)

### Divergence Analysis

**Highest estimate**: $ [method]
**Lowest estimate**: $ [method]
**Spread**: $ (%) -- is spread > 20%?

**Source of divergence** (check applicable):
- [ ] Growth rate assumptions differ between methods
- [ ] Discount rate / risk assessment differs
- [ ] Peer universe selection drives relative value higher/lower
- [ ] Terminal value dominates DCF (>80%) -- flag for review
- [ ] Accounting differences (e.g., R&D capitalization affects PE vs EV/EBITDA differently)
- [ ] Market pricing of sector broadly differs from fundamentals (whole sector may be over/undervalued)

**Resolution**: [Which estimate do you trust more, and why?]

---

## Implied Assumptions Worksheet

Reverse-engineer the growth rate and ROIC that make DCF value equal to market price.

### Implied Growth Rate

**Objective**: Find growth rate g* such that DCF(g*) = Market Price

**Method**: Hold all DCF inputs constant except revenue growth rate. Iterate until DCF output matches current market price.

| Iteration | Growth Rate | DCF Value | vs Market Price |
|-----------|------------|-----------|-----------------|
| Your estimate | % | $ | +/- $ |
| Market implied (trial 1) | % | $ | +/- $ |
| Market implied (trial 2) | % | $ | +/- $ |
| Market implied (converged) | **%** | **$** | **~$0** |

**Implied growth rate**: %
**Your narrative growth rate**: %
**Gap**: percentage points

**Plausibility check**:
- [ ] Implied growth consistent with company's historical growth?
- [ ] Implied growth consistent with industry growth rate?
- [ ] Implied growth achievable given TAM and current market share?
- [ ] Base rate: What fraction of companies sustain this growth for the assumed period?

### Implied ROIC

**Objective**: Find ROIC* such that DCF(ROIC*) = Market Price

**Method**: Hold all DCF inputs constant except return on capital (which affects reinvestment rate via g = ROIC x reinvestment rate). Iterate until DCF output matches current market price.

| Iteration | ROIC | Reinvestment Rate | DCF Value | vs Market Price |
|-----------|------|-------------------|-----------|-----------------|
| Your estimate | % | % | $ | +/- $ |
| Market implied (trial 1) | % | % | $ | +/- $ |
| Market implied (converged) | **%** | **%** | **$** | **~$0** |

**Implied ROIC**: %
**Your narrative ROIC**: %
**Industry median ROIC**: %
**Company historical ROIC (5-year avg)**: %

**Interpretation**:
- [ ] Market implies ROIC below historical average -- market expects deterioration
- [ ] Market implies ROIC near historical average -- market prices continuation
- [ ] Market implies ROIC above historical average -- market expects improvement
- [ ] Market implies ROIC below WACC -- market prices value destruction (no growth premium)

### EVA Value Decomposition

**Invested Capital**: $
**PV of Future EVA**: $
**Total Firm Value**: $

**Growth premium** = (Firm Value - Invested Capital) / Firm Value = %

**Interpretation**: The market is paying % of total value for expected growth. If growth premium > 50%, the valuation is highly sensitive to growth assumptions.

---

## Catalyst Identification Template

Catalysts are specific events that could cause the gap between value and price to close.

### Catalyst Assessment

| Catalyst | Expected Timing | Value Impact | Probability | Weighted Impact |
|----------|----------------|-------------|-------------|-----------------|
| [Event 1] | [Quarter/Date] | [$/share or %] | [%] | [$ x prob] |
| [Event 2] | [Quarter/Date] | [$/share or %] | [%] | [$ x prob] |
| [Event 3] | [Quarter/Date] | [$/share or %] | [%] | [$ x prob] |
| **Total expected catalyst impact** | | | | **$** |

### Catalyst Categories

**Earnings-related**:
- Next earnings report showing margin expansion or revenue acceleration
- Guidance revision (upward/downward)
- Beat/miss relative to consensus expectations

**Operational**:
- Restructuring completion (cost savings realization)
- New product or service launch
- Geographic expansion into new markets
- Capacity expansion coming online

**Financial**:
- Share buyback announcement or acceleration
- Dividend initiation or increase
- Debt refinancing at lower rate
- Capital structure optimization (moving toward optimal debt ratio)

**External**:
- Regulatory approval or change
- Industry consolidation (M&A activity)
- Competitor exit or market share shift
- Macroeconomic tailwind (rate cuts, demand recovery)

**Management**:
- New CEO or key executive appointment
- Strategic review or investor day
- Spin-off or divestiture of non-core assets

### Catalyst Quality Checklist

- [ ] Each catalyst has a specific "what" (not vague)
- [ ] Each catalyst has an estimated "when" (quarter or date, not "eventually")
- [ ] Each catalyst has a quantified impact estimate ($/share or %)
- [ ] Each catalyst has a probability assessment (not assumed certain)
- [ ] At least one catalyst is within 6 months (for actionability)
- [ ] Catalysts are independent of each other (not double-counting)

---

## Recommendation Template

### Recommendation Summary

**Company**: [Name]
**Ticker**: [Symbol]
**Current Price**: $
**Weighted Intrinsic Value**: $
**Margin of Safety**: %
**Value-to-Price Ratio**: x

**Recommendation**: [Buy / Sell / Hold]
**Conviction Level**: [High / Moderate / Low]
**Price Target**: $
**Time Horizon**: [6 months / 12 months / 24 months]

### Recommendation Rationale

**Why this recommendation** (2-3 sentences):
[Link the business narrative to the valuation gap. State the core thesis concisely.]

**What the market is missing** (1-2 sentences):
[Identify the specific assumption where your view diverges from market consensus.]

**What would change this recommendation**:
- Upgrade trigger: [What would make you more bullish?]
- Downgrade trigger: [What would make you more bearish?]
- Stop-loss: [At what price or event would you exit?]

### Risk Factors

| Risk | Probability | Impact if Realized | Mitigation |
|------|------------|-------------------|------------|
| [Risk 1] | [Low/Med/High] | [Effect on thesis] | [How partially addressed] |
| [Risk 2] | [Low/Med/High] | [Effect on thesis] | [How partially addressed] |
| [Risk 3] | [Low/Med/High] | [Effect on thesis] | [How partially addressed] |

### Margin of Safety Calibration

**Required margin by company type**:

| Company Type | Minimum Margin of Safety | Rationale |
|--------------|-------------------------|-----------|
| Stable, predictable (utilities, staples) | 10-15% | Low cash flow volatility, narrow forecast range |
| Moderate growth (industrials, healthcare) | 15-25% | Moderate uncertainty in growth trajectory |
| High growth (tech, biotech) | 25-40% | Wide range of outcomes, high terminal value dependence |
| Distressed / turnaround | 30-50% | Binary risk, high failure probability |
| Private / illiquid | 25-40% | Additional liquidity risk, less price discovery |

**Actual margin of safety**: %
**Required margin for this company type**: %
**Margin adequate?**: [Yes / No -- adjust recommendation if insufficient]

---

## Investment Thesis Template

One-page synthesis linking business narrative to valuation to recommendation.

### Investment Thesis: [Company Name]

**The Story**: [2-3 sentences describing the business narrative -- what does this company do, where is it in its life cycle, and how does it evolve over the next 5-10 years?]

**The Numbers**:
- Revenue growth: % (current) converging to % (stable)
- Operating margin: % (current) converging to % (target)
- ROIC: % vs WACC: % -- value [creating / neutral / destroying]
- DCF intrinsic value: $/share

**The Market View**:
- Current price: $/share
- Market implies: % growth and % ROIC
- Our view differs because: [1-2 sentences]

**The Gap**:
- Margin of safety: %
- Primary catalyst: [Event, timing, expected impact]
- Secondary catalyst: [Event, timing, expected impact]

**The Risks**:
1. [Primary risk and how it would affect the thesis]
2. [Secondary risk and how it would affect the thesis]

**The Recommendation**:
- Action: [Buy / Sell / Hold]
- Price target: $
- Time horizon: [months]
- Exit trigger: [What would invalidate the thesis]

---

## Sensitivity Matrix Template

Show how the per-share value changes across key assumption ranges.

### Value Sensitivity: Growth Rate vs WACC

| | WACC -1% | WACC Base | WACC +1% |
|---------|----------|-----------|----------|
| **Growth +2%** | $ | $ | $ |
| **Growth Base** | $ | $ | $ |
| **Growth -2%** | $ | $ | $ |

### Value Sensitivity: Operating Margin vs Growth Rate

| | Growth -2% | Growth Base | Growth +2% |
|---------|------------|-------------|------------|
| **Margin +2%** | $ | $ | $ |
| **Margin Base** | $ | $ | $ |
| **Margin -2%** | $ | $ | $ |

### Breakeven Analysis

- Growth rate that makes value = price: %
- WACC that makes value = price: %
- Operating margin that makes value = price: %

**Decision sensitivity**: Does the recommendation (buy/sell/hold) change within the plausible range of assumptions?
- [ ] Recommendation holds across all scenarios -- high conviction
- [ ] Recommendation flips in 1-2 extreme scenarios -- moderate conviction
- [ ] Recommendation flips in base-case variations -- low conviction, consider Hold
