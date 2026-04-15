# Intrinsic Valuation (DCF) Templates

Templates for base year inputs, year-by-year projections, terminal value, equity bridge, sensitivity analysis, and value decomposition.

## Table of Contents
- [Base Year Inputs](#base-year-inputs)
- [Year-by-Year Projection Table](#year-by-year-projection-table)
- [Terminal Value Calculation](#terminal-value-calculation)
- [Equity Bridge](#equity-bridge)
- [Sensitivity Grid](#sensitivity-grid)
- [Value Decomposition](#value-decomposition)
- [Complete DCF Output Template](#complete-dcf-output-template)

---

## Base Year Inputs

### FCFF Model Inputs

**Company**: [Name]
**Currency**: [USD/EUR/etc.]
**Base Year**: [Fiscal year or TTM]

| Input | Value | Source / Notes |
|-------|-------|---------------|
| Revenue | $ | Financial statements |
| EBIT (Operating Income) | $ | Adjusted for one-time items |
| Tax rate (marginal) | % | Use marginal, not effective |
| After-tax EBIT | $ | EBIT x (1 - tax rate) |
| Capital expenditure | $ | Cash flow statement |
| Depreciation & amortization | $ | Cash flow statement |
| Net CapEx (CapEx - D&A) | $ | Computed |
| Change in non-cash working capital | $ | Balance sheet year-over-year |
| **Base year FCFF** | **$** | **After-tax EBIT - Net CapEx - WC change** |

**Derived metrics:**
| Metric | Value | Formula |
|--------|-------|---------|
| Reinvestment rate | % | (Net CapEx + WC change) / After-tax EBIT |
| Return on capital (ROC) | % | After-tax EBIT / Invested Capital |
| Sales-to-capital ratio | x | Revenue / Invested Capital |
| Operating margin | % | EBIT / Revenue |
| Invested capital | $ | BV of Equity + BV of Debt - Cash |

### FCFE Model Inputs

| Input | Value | Source / Notes |
|-------|-------|---------------|
| Net income | $ | Income statement |
| Capital expenditure | $ | Cash flow statement |
| Depreciation & amortization | $ | Cash flow statement |
| Change in non-cash working capital | $ | Balance sheet |
| Net debt issued (new - repaid) | $ | Cash flow statement |
| **Base year FCFE** | **$** | **NI - Net CapEx - WC change + Net debt** |

**Derived metrics:**
| Metric | Value | Formula |
|--------|-------|---------|
| Equity reinvestment rate | % | (Net CapEx + WC change - Net debt) / NI |
| Return on equity (ROE) | % | Net income / Book value of equity |
| Payout ratio | % | Dividends / Net income |

### DDM Model Inputs

| Input | Value | Source / Notes |
|-------|-------|---------------|
| Earnings per share (EPS) | $ | Diluted EPS |
| Dividends per share (DPS) | $ | Actual dividends paid |
| Payout ratio | % | DPS / EPS |
| Return on equity (ROE) | % | NI / Book equity |
| Cost of equity | % | From cost-of-capital-estimator |

---

## Year-by-Year Projection Table

### FCFF Projection (Two-Stage)

**Growth assumptions:**
- High-growth period: [X] years at [Y]% operating income growth
- Reinvestment rate (high-growth): [Z]%
- WACC (high-growth): [W]%
- Stable growth rate: [S]%
- Reinvestment rate (stable): [R]%
- WACC (stable): [V]%

| Year | Revenue | EBIT | After-tax EBIT | Reinvestment | FCFF | PV Factor | PV of FCFF |
|------|---------|------|---------------|-------------|------|-----------|------------|
| Base | $ | $ | $ | $ | $ | -- | -- |
| 1 | $ | $ | $ | $ | $ | 1/(1+WACC)^1 | $ |
| 2 | $ | $ | $ | $ | $ | 1/(1+WACC)^2 | $ |
| 3 | $ | $ | $ | $ | $ | 1/(1+WACC)^3 | $ |
| 4 | $ | $ | $ | $ | $ | 1/(1+WACC)^4 | $ |
| 5 | $ | $ | $ | $ | $ | 1/(1+WACC)^5 | $ |
| ... | | | | | | | |
| **Sum of PV (high-growth)** | | | | | | | **$** |

**Projection checklist:**
- [ ] Growth rate applied to after-tax operating income (or revenue with margin convergence)
- [ ] Reinvestment rate is consistent with growth (g = reinvestment rate x ROC)
- [ ] Revenue growth is bounded by TAM from business narrative
- [ ] Operating margin converges toward target (industry benchmark or narrative-based)
- [ ] Discount rate matches cash flow type (WACC for FCFF)

### FCFE Projection (Two-Stage)

| Year | Net Income | Equity Reinvestment | FCFE | PV Factor (ke) | PV of FCFE |
|------|-----------|-------------------|------|----------------|------------|
| Base | $ | $ | $ | -- | -- |
| 1 | $ | $ | $ | 1/(1+ke)^1 | $ |
| 2 | $ | $ | $ | 1/(1+ke)^2 | $ |
| ... | | | | | |
| **Sum of PV (high-growth)** | | | | | **$** |

### DDM Projection (Two-Stage)

| Year | EPS | Payout Ratio | DPS | PV Factor (ke) | PV of DPS |
|------|-----|-------------|-----|----------------|-----------|
| Base | $ | % | $ | -- | -- |
| 1 | $ | % | $ | 1/(1+ke)^1 | $ |
| 2 | $ | % | $ | 1/(1+ke)^2 | $ |
| ... | | | | | |
| **Sum of PV (high-growth)** | | | | | **$** |

---

## Terminal Value Calculation

### Growing Perpetuity Method (Primary)

**Step 1: Compute stable-period cash flow**

| Component | Value | Notes |
|-----------|-------|-------|
| Final year cash flow | $ | Last year of high-growth projection |
| Stable growth rate (g) | % | Should not exceed risk-free rate or nominal GDP |
| Cash flow in year n+1 | $ | Final year CF x (1 + g) |
| Stable reinvestment rate | % | g / stable ROC |
| Stable FCFF (or FCFE) | $ | After-tax income x (1 - reinvestment rate) |

**Step 2: Compute terminal value**

| Component | Value |
|-----------|-------|
| Stable cash flow (year n+1) | $ |
| Discount rate (stable WACC or ke) | % |
| Stable growth rate | % |
| **Terminal value** | **$ = CF / (r - g)** |

**Step 3: Discount terminal value to present**

| Component | Value |
|-----------|-------|
| Terminal value | $ |
| PV factor at year n | 1/(1+r)^n |
| **PV of terminal value** | **$** |

### Exit Multiple Cross-Check (Secondary)

| Metric | Value | Notes |
|--------|-------|-------|
| Terminal year EBITDA | $ | From projection |
| Industry EV/EBITDA multiple | x | Median of mature peers |
| Implied terminal value (multiple) | $ | EBITDA x multiple |
| Terminal value (perpetuity) | $ | From calculation above |
| Difference | % | Flag if > 25% divergence |

**Terminal value checklist:**
- [ ] Stable growth rate does not exceed risk-free rate or nominal GDP growth
- [ ] Reinvestment rate in stable period = g / ROC (internally consistent)
- [ ] Cost of capital in stable period reflects mature company (beta toward 1.0, industry-average leverage)
- [ ] Terminal value as % of total value is flagged if > 90%
- [ ] Exit multiple cross-check performed and reconciled

---

## Equity Bridge

### From Firm Value to Equity Value (FCFF Models)

| Component | Value | Notes |
|-----------|-------|-------|
| PV of high-growth cash flows | +$ | Sum from projection table |
| PV of terminal value | +$ | From terminal value calculation |
| **Operating asset value** | **=$** | Sum of above |
| Cash and marketable securities | +$ | Non-operating cash |
| Value of cross-holdings | +$ | Market value of equity stakes in other firms |
| Other non-operating assets | +$ | Overfunded pension, excess real estate |
| **Total firm value** | **=$** | |
| Market value of debt | -$ | All debt included in WACC |
| Value of employee stock options | -$ | Treasury stock method or Black-Scholes |
| Minority interests | -$ | Market value (or book x multiple) |
| **Equity value** | **=$** | |
| Diluted shares outstanding | | Treasury stock method for in-the-money options |
| **Per-share intrinsic value** | **=$** | Equity value / diluted shares |

### Employee Stock Option Valuation

**Treasury stock method (simpler):**
- Options outstanding: [N]
- Weighted average strike price: $[X]
- Current stock price (or estimated value): $[P]
- Diluted shares = Basic shares + (Options x (P - X) / P) for in-the-money options

**Black-Scholes method (more precise):**

| Input | Value |
|-------|-------|
| Number of options | N |
| Weighted average strike price (K) | $ |
| Estimated stock value (S) | $ |
| Weighted average maturity (t) | years |
| Risk-free rate (r) | % |
| Stock price volatility (sigma) | % |
| Dividend yield (y) | % |
| **Option value per option** | $ |
| **Total option value (N x per-option value)** | **$** |

### Equity Value Direct (FCFE / DDM Models)

| Component | Value | Notes |
|-----------|-------|-------|
| PV of high-growth cash flows (FCFE or DPS) | +$ | Sum from projection |
| PV of terminal value | +$ | Terminal value calculation |
| **Equity value (operating)** | **=$** | |
| Cash allocated to equity (net of debt-financed cash) | +$ | If not already in FCFE |
| Value of employee stock options | -$ | Treasury stock or Black-Scholes |
| **Equity value** | **=$** | |
| Diluted shares outstanding | | |
| **Per-share intrinsic value** | **=$** | |

---

## Sensitivity Grid

### Two-Way Sensitivity: Growth Rate vs. Discount Rate

Construct a grid showing per-share value at each combination. Highlight the base case cell.

| WACC \ Stable Growth | g - 1% | g - 0.5% | **g (base)** | g + 0.5% | g + 1% |
|---------------------|--------|----------|-------------|----------|--------|
| WACC + 1.0% | $ | $ | $ | $ | $ |
| WACC + 0.5% | $ | $ | $ | $ | $ |
| **WACC (base)** | $ | $ | **$** | $ | $ |
| WACC - 0.5% | $ | $ | $ | $ | $ |
| WACC - 1.0% | $ | $ | $ | $ | $ |

### Additional Sensitivity Dimensions

**Revenue growth sensitivity:**

| Growth Rate (high period) | Per-Share Value | % Change from Base |
|--------------------------|----------------|-------------------|
| Base - 4% | $ | % |
| Base - 2% | $ | % |
| Base (X%) | $ | -- |
| Base + 2% | $ | % |
| Base + 4% | $ | % |

**Operating margin sensitivity:**

| Target Margin | Per-Share Value | % Change from Base |
|--------------|----------------|-------------------|
| Base - 3% | $ | % |
| Base - 1.5% | $ | % |
| Base (X%) | $ | -- |
| Base + 1.5% | $ | % |
| Base + 3% | $ | % |

**Sensitivity checklist:**
- [ ] Growth rate and discount rate varied (minimum requirement)
- [ ] Base case clearly marked in grid
- [ ] Range of outcomes documented (bull/bear/base)
- [ ] Key assumptions identified as high-sensitivity (value changes >10% for small input change)

---

## Value Decomposition

Break total value into components to show where value comes from.

| Component | Value | % of Total | Interpretation |
|-----------|-------|-----------|---------------|
| PV of cash flows (high-growth) | $ | % | Value from near-term operations |
| PV of terminal value | $ | % | Value from long-term steady state |
| **Operating asset value** | **$** | **100%** | |
| Cash and non-operating assets | $ | | Margin of safety component |
| Minus: Debt, options, minorities | -$ | | Claims ahead of common equity |
| **Equity value** | **$** | | |

**Interpretation guide:**
- Terminal value > 80%: Most value depends on long-run assumptions. Stress-test stable growth and WACC.
- Terminal value < 50%: Near-term cash flows dominate. Focus on accuracy of 5-year projections.
- Cash > 15% of firm value: Company is cash-rich. Assess whether cash is being deployed productively.
- Options > 5% of equity: Dilution is material. Verify option count and valuation method.

---

## Complete DCF Output Template

Structure for the full valuation document:

1. **Model Selection**: Variant chosen (FCFF/FCFE/DDM), rationale for choice
2. **Base Year**: Cleaned financials, base year cash flow calculation, derived metrics (ROC, reinvestment rate, margin)
3. **Growth Assumptions**: Growth rate, period length, source (fundamental, historical, consensus), narrative link
4. **Year-by-Year Projections**: Full projection table with all line items
5. **Terminal Value**: Perpetuity calculation, exit multiple cross-check, terminal value as % of total
6. **Equity Bridge**: Firm value to equity (FCFF) or direct equity (FCFE/DDM), option adjustment, per-share value
7. **Sensitivity Analysis**: Two-way grid (growth vs WACC), additional dimensions as appropriate
8. **Value Decomposition**: Where value comes from, terminal value proportion assessment
9. **Key Risks and Assumptions**: What would change the valuation most, narrative dependencies
10. **Comparison to Market Price**: Current price, margin of safety, implied assumptions in market price
