# Special Situations Valuation Templates

Templates for situation classification, model-specific inputs, and comparison across sub-frameworks.

## Table of Contents
- [Situation Classification Guide](#situation-classification-guide)
- [High-Growth / Negative Earnings Template](#high-growth--negative-earnings-template)
- [Distressed Firm Template](#distressed-firm-template)
- [Private Company Template](#private-company-template)
- [Financial Services Template](#financial-services-template)
- [Standard vs Adjusted Comparison](#standard-vs-adjusted-comparison)

---

## Situation Classification Guide

Use this decision tree to determine which sub-framework applies.

### Step 1: Is the firm a financial services company?

**Indicators**:
- [ ] Primary business is banking, lending, insurance, or financial intermediation
- [ ] Deposits, insurance reserves, or trading liabilities constitute majority of balance sheet
- [ ] Regulated by banking/insurance authorities (OCC, Fed, FDIC, state insurance commissions)
- [ ] Revenue comes from net interest income, premiums, fees, or trading gains

If 2+ indicators are checked: **Use Pattern 4 (Financial Services)**. Proceed to [Financial Services Template](#financial-services-template).

### Step 2: Does the firm have negative or near-zero operating income?

**Indicators**:
- [ ] Operating income (EBIT) is negative in the most recent period
- [ ] Operating margin is below -5%
- [ ] Revenue is growing at >20% annually
- [ ] Company is in Young Growth or Start-up life cycle stage
- [ ] Company has not yet reached target operating margins for its industry

If operating income is negative and revenue is growing: **Use Pattern 1 (High-Growth / Negative Earnings)**. Proceed to [High-Growth Template](#high-growth--negative-earnings-template).

### Step 3: Is the firm in financial distress?

**Indicators**:
- [ ] Interest coverage ratio < 1.5
- [ ] Book value of equity is negative
- [ ] Altman Z-score < 1.8 (distress zone)
- [ ] Credit rating is CCC or below
- [ ] Market value of assets may be below face value of debt
- [ ] CDS spread > 500 basis points

If 2+ indicators are checked: **Use Pattern 2 (Distressed)**. Proceed to [Distressed Firm Template](#distressed-firm-template).

### Step 4: Is the firm private?

**Indicators**:
- [ ] No publicly traded equity
- [ ] Owner is undiversified (majority of wealth in this company)
- [ ] No active secondary market for shares
- [ ] Valuation is for estate, acquisition, or venture purposes

If the firm is private: **Use Pattern 3 (Private Company)**. Proceed to [Private Company Template](#private-company-template).

### Multiple classifications

A company may fall into more than one category:
- **Private + high-growth**: Apply revenue-based DCF (Pattern 1), then add total beta adjustment and liquidity discount (Pattern 3)
- **Private + financial services**: Apply excess return model (Pattern 4), then add total beta and liquidity discount (Pattern 3)
- **Distressed + private**: Apply equity-as-call-option (Pattern 2), then apply liquidity discount (Pattern 3)

---

## High-Growth / Negative Earnings Template

### Base Year Data

| Item | Value | Source |
|------|-------|--------|
| Current revenue | $ | |
| Revenue growth rate (TTM) | % | |
| Operating income (EBIT) | $ | |
| Operating margin | % | |
| Tax rate (marginal) | % | |
| Cash and equivalents | $ | |
| Annual cash burn rate | $ | |
| Invested capital | $ | |
| Current sales-to-capital ratio | | Revenue / Invested Capital |

### Target Operating Margin

| Mature Peer Company | Revenue | Operating Margin |
|---------------------|---------|-----------------|
| Peer 1 | $ | % |
| Peer 2 | $ | % |
| Peer 3 | $ | % |
| Peer 4 | $ | % |
| Peer 5 | $ | % |
| **25th percentile** | | **%** |
| **Median** | | **%** |
| **75th percentile** | | **%** |

**Selected target margin**: ___% (rationale: ___________________________)

**Convergence period**: ___ years (from current margin to target margin)

### Revenue Growth Trajectory

| Year | Revenue Growth | Revenue | Cumulative |
|------|---------------|---------|------------|
| 1 | % | $ | |
| 2 | % | $ | |
| 3 | % | $ | |
| 4 | % | $ | |
| 5 | % | $ | |
| 6-10 | declining to stable | | |
| Stable | % | $ | |

**Growth decline logic**: Revenue growth declines from ___% to ___% over ___ years because: _________________________

### Reinvestment via Sales-to-Capital

| Year | Revenue Change | Sales-to-Capital | Reinvestment |
|------|---------------|-----------------|--------------|
| 1 | $ | | $ |
| 2 | $ | | $ |
| ... | | | |

**Sales-to-capital ratio**: ___ (derived from: industry average / company history / comparable firms)

### Failure Probability Assessment

| Factor | Assessment |
|--------|-----------|
| Cash on hand | $ |
| Annual burn rate | $ |
| Cash runway (years) | |
| Altman Z-score (if applicable) | |
| Industry base failure rate | % |
| Company-specific factors | |
| **Estimated failure probability** | **%** |

**Distress sale value**: $___  (basis: liquidation of assets at ___% of book value)

### Final Calculation

| Component | Value |
|-----------|-------|
| PV of projected FCFF (years 1-n) | $ |
| PV of terminal value | $ |
| DCF value of firm (going concern) | $ |
| Failure-adjusted firm value | $ |
| Minus: Debt | $ |
| Plus: Cash | $ |
| Minus: Employee options | $ |
| **Equity value** | **$** |
| Shares outstanding (diluted) | |
| **Per-share value** | **$** |

---

## Distressed Firm Template

### Black-Scholes Inputs for Equity as Call Option

| Input | Symbol | Value | Source / Derivation |
|-------|--------|-------|---------------------|
| Firm value (PV of expected cash flows from assets) | S | $ | DCF of operating assets |
| Face value of debt | K | $ | Sum of all debt obligations |
| Weighted average debt maturity | t | years | Duration-weighted average |
| Riskfree rate (matching maturity) | r | % | Treasury rate for maturity t |
| Firm value volatility (annual std dev) | sigma | % | See methodology for estimation |
| Cash flow yield (annual CF as % of firm value) | y | % | FCFF / Firm value |

### Debt Structure

| Debt Tranche | Face Value | Maturity | Weight |
|--------------|-----------|----------|--------|
| Tranche 1 | $ | years | % |
| Tranche 2 | $ | years | % |
| Tranche 3 | $ | years | % |
| **Total** | **$** | **weighted avg** | **100%** |

### Firm Value Volatility Estimation

Choose one approach (see methodology for details):

- [ ] **Approach A**: Average of equity volatility (de-levered) and debt volatility (adjusted for leverage)
- [ ] **Approach B**: Comparable firm asset volatility (unlevered equity volatility of comparable non-distressed firms)
- [ ] **Approach C**: Operating income volatility scaled to asset level

**Estimated firm value volatility**: ___% (annual standard deviation)

### Black-Scholes Calculation

| Step | Calculation | Value |
|------|-------------|-------|
| d1 | [ln(S/K) + (r - y + sigma^2/2) x t] / (sigma x sqrt(t)) | |
| d2 | d1 - sigma x sqrt(t) | |
| N(d1) | Cumulative normal distribution of d1 | |
| N(d2) | Cumulative normal distribution of d2 | |
| Call value (equity) | S x e^(-yt) x N(d1) - K x e^(-rt) x N(d2) | $ |

### Final Values

| Component | Value |
|-----------|-------|
| Value of equity (Black-Scholes) | $ |
| Value of debt (Firm value - Equity value) | $ |
| Shares outstanding | |
| **Per-share equity value** | **$** |

---

## Private Company Template

### Total Beta Calculation

| Item | Value | Source |
|------|-------|--------|
| Market beta (from comparable public firms) | | Bottom-up unlevered beta, relevered |
| R-squared of comparable regression | | Average R of comparable firm regressions |
| Correlation with market (R) | | sqrt(R-squared) |
| **Total beta** | **Market beta / R** | |

**Context check**:
- [ ] Owner is undiversified (family business, sole owner, majority of wealth) -> Use total beta
- [ ] Owner is diversified (PE fund, public acquirer, well-diversified investor) -> Use market beta
- [ ] Mixed (partially diversified) -> Use value between market beta and total beta

### Liquidity Discount Estimation

Use restricted stock study regression to estimate discount based on company characteristics:

| Factor | Value | Impact on Discount |
|--------|-------|--------------------|
| Revenue | $ | Larger revenue -> smaller discount |
| Operating margin | % | Higher margin -> smaller discount |
| Positive earnings (yes/no) | | Positive -> smaller discount |
| Block size (% of firm) | % | Larger block -> larger discount |
| Industry | | Some industries more liquid |

**Estimated liquidity discount**: ___% (from regression or benchmark range 10-35%)

**Minority discount** (if applicable):
- [ ] Valuing a minority stake without control -> apply minority discount
- [ ] Valuing a controlling stake -> no minority discount
- Estimated minority discount: ___% (if applicable)

### Value Calculation

| Component | Value |
|-----------|-------|
| Standard DCF value (using market beta) | $ |
| Adjusted DCF value (using total beta, if undiversified) | $ |
| Liquidity discount applied | % |
| Value after liquidity discount | $ |
| Minority discount applied (if applicable) | % |
| **Final private company value** | **$** |

---

## Financial Services Template

### Excess Return Model Inputs

| Item | Value | Source |
|------|-------|--------|
| Book value of equity (current) | $ | Balance sheet |
| Current ROE | % | Net income / Book equity |
| Expected ROE (stable) | % | Peer median or target |
| Cost of equity (ke) | % | CAPM |
| Expected growth in book equity (high-growth period) | % | Retention x ROE |
| Length of high-growth period | years | |
| Stable growth rate | % | Constrained by risk-free rate |
| Payout ratio (high-growth) | % | 1 - (g / ROE) |
| Payout ratio (stable) | % | 1 - (g_stable / ROE_stable) |

### Regulatory Capital Check

| Item | Value |
|------|-------|
| Tier 1 capital ratio (actual) | % |
| Tier 1 capital ratio (required minimum) | % |
| Buffer above minimum | % |
| Constrained growth rate (if capital-constrained) | % |

### Year-by-Year Excess Return Projection

| Year | BV Equity | ROE | Net Income | Cost of Equity | Excess Return | PV of Excess Return |
|------|-----------|-----|------------|----------------|---------------|---------------------|
| 1 | $ | % | $ | $ | $ | $ |
| 2 | $ | % | $ | $ | $ | $ |
| ... | | | | | | |

### Terminal Value

| Component | Value |
|-----------|-------|
| BV equity at end of high-growth period | $ |
| ROE in stable period | % |
| Cost of equity in stable period | % |
| Stable growth rate | % |
| Terminal excess return value | $ |
| PV of terminal value | $ |

### Final Value

| Component | Value |
|-----------|-------|
| Book value of equity (current) | $ |
| PV of excess returns (high-growth) | $ |
| PV of terminal excess return value | $ |
| **Total equity value** | **$** |
| Shares outstanding | |
| **Per-share value** | **$** |

**Price-to-book implied**: Total equity value / Book value = ___x

**Interpretation**: If ROE > ke, P/BV > 1 (justified premium). If ROE < ke, P/BV < 1 (justified discount).

---

## Standard vs Adjusted Comparison

Use this template to show the impact of special-situation adjustments.

| Metric | Standard DCF | Special Situation Adjusted | Difference |
|--------|-------------|---------------------------|-----------|
| Discount rate used | % | % | |
| Growth assumptions | | | |
| Terminal value | $ | $ | |
| Firm / equity value (pre-adjustment) | $ | $ | |
| Probability weighting / discount applied | N/A | % | |
| **Final value** | **$** | **$** | **$** |
| **Per-share value** | **$** | **$** | **$** |

**Adjustment impact narrative**:
- What adjustments were made and why:
- Magnitude of each adjustment as % of standard value:
- Whether the adjustment increased or decreased value:
- Sensitivity of the adjustment to key assumptions:
