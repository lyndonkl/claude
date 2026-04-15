# Dividend and Buyback Analysis Templates

Templates for computing FCFE, comparing cash returns, assessing excess cash, and formulating payout policy recommendations.

## Table of Contents
- [FCFE Calculation Template](#fcfe-calculation-template)
- [FCFE vs Actual Return Comparison](#fcfe-vs-actual-return-comparison)
- [Excess Cash Calculation](#excess-cash-calculation)
- [Peer Payout Comparison](#peer-payout-comparison)
- [Payout Policy Recommendation](#payout-policy-recommendation)
- [Cash Accumulation Projection](#cash-accumulation-projection)

---

## FCFE Calculation Template

Compute the maximum cash the company can sustainably return to equity holders.

### Single-Year FCFE

| Line Item | Amount | Source |
|-----------|--------|--------|
| Net Income | $ | Income statement |
| **Less: Net Capital Expenditure** | | |
| Capital Expenditure | ($ ) | Cash flow statement |
| Depreciation & Amortization | +$ | Cash flow statement |
| Net CapEx (CapEx - D&A) | ($ ) | |
| **Less: Working Capital Investment** | | |
| Change in Non-Cash Working Capital | ($ ) | Balance sheet delta |
| **Plus: Net Debt Change** | | |
| New Debt Issued | +$ | Cash flow statement |
| Debt Repaid | ($ ) | Cash flow statement |
| Net Debt Change | +/-($ ) | |
| **Free Cash Flow to Equity (FCFE)** | **$** | |

**Formula**:
```
FCFE = Net Income
     - (CapEx - Depreciation)
     - Change in Non-Cash Working Capital
     + (New Debt Issued - Debt Repaid)
```

### Multi-Year FCFE (for cyclical companies)

Use 3-5 year average to smooth cyclicality.

| Year | Net Income | Net CapEx | WC Change | Net Debt | FCFE |
|------|-----------|-----------|-----------|----------|------|
| Year 1 | $ | $ | $ | $ | $ |
| Year 2 | $ | $ | $ | $ | $ |
| Year 3 | $ | $ | $ | $ | $ |
| Year 4 | $ | $ | $ | $ | $ |
| Year 5 | $ | $ | $ | $ | $ |
| **Average** | **$** | **$** | **$** | **$** | **$** |

**Notes on FCFE computation**:
- Net income should be adjusted for non-recurring items (use normalized earnings for policy decisions)
- Working capital change should exclude cash and short-term debt (non-cash working capital only)
- Net debt change reflects the company's target capital structure -- if the company is maintaining a stable debt ratio, net debt issuance approximates the debt portion of new investment
- For financial services firms, FCFE = Net Income - Equity Reinvestment (change in regulatory capital requirements)

---

## FCFE vs Actual Return Comparison

Compare what the company can afford to return with what it actually returns.

### Annual Comparison

| Metric | Amount | Notes |
|--------|--------|-------|
| **FCFE (capacity)** | $ | From FCFE calculation above |
| **Actual Cash Returned** | | |
| Dividends Paid | $ | Cash flow statement |
| Shares Repurchased (net) | $ | Cash flow statement |
| Total Cash Returned | $ | Dividends + Buybacks |
| **Gap Analysis** | | |
| FCFE Gap (FCFE - Cash Returned) | $ | Positive = under-returning |
| Cash Return Ratio (Cash Returned / FCFE) | % | Target: 80-100% for mature firms |

### Multi-Year Trend

| Year | FCFE | Dividends | Buybacks | Total Returned | Cash Return Ratio | Cumulative Gap |
|------|------|-----------|----------|----------------|-------------------|----------------|
| Year 1 | $ | $ | $ | $ | % | $ |
| Year 2 | $ | $ | $ | $ | % | $ |
| Year 3 | $ | $ | $ | $ | % | $ |
| Year 4 | $ | $ | $ | $ | % | $ |
| Year 5 | $ | $ | $ | $ | % | $ |

**Interpretation guide**:
- Cash return ratio < 50%: Significant under-returning -- investigate whether retention is justified by reinvestment quality
- Cash return ratio 50-80%: Moderate under-returning -- may be appropriate if ROC > WACC with strong project pipeline
- Cash return ratio 80-100%: Healthy range for mature companies
- Cash return ratio 100-120%: Mild over-returning -- acceptable temporarily if FCFE is cyclically depressed
- Cash return ratio > 120%: Unsustainable over-distribution -- dividend cut or borrowing risk

---

## Excess Cash Calculation

Determine whether the balance sheet holds more cash than operations require.

### Excess Cash Worksheet

| Component | Amount | Methodology |
|-----------|--------|-------------|
| Cash and Marketable Securities | $ | Balance sheet |
| **Less: Operating Cash Needs** | | |
| Annual Revenue | $ | Income statement |
| Operating Cash % of Revenue | % | See industry norms below |
| Operating Cash Needs | $ | Revenue x Operating Cash % |
| **Excess Cash** | **$** | Cash - Operating Cash Needs |

### Industry Norms for Operating Cash as % of Revenue

| Industry | Typical Range | Rationale |
|----------|--------------|-----------|
| Technology (mature) | 2-3% | Low inventory, predictable billing cycles |
| Technology (growth) | 3-5% | Buffer for lumpy investments, acquisition optionality |
| Consumer Staples | 2-3% | Stable, predictable cash flow needs |
| Industrials / Manufacturing | 3-5% | Inventory and receivables cycles, seasonal variation |
| Retail | 3-5% | Seasonal inventory buildup, supplier payment timing |
| Healthcare / Pharma | 3-5% | R&D timing, regulatory uncertainty |
| Financial Services | N/A | Cash is operational -- do not apply this framework |
| Utilities | 1-2% | Regulated, highly predictable cash flows |
| Energy | 3-5% | Commodity price volatility, capital intensity |

### Excess Cash Context

| Metric | Value |
|--------|-------|
| Excess Cash as % of Market Cap | % |
| Excess Cash as % of Revenue | % |
| Excess Cash per Share | $ |
| Years of FCFE equivalent | X years |

If excess cash exceeds 1-2 years of FCFE, the company has a meaningful stockpile that should be addressed in the return policy.

---

## Peer Payout Comparison

Benchmark the company's return policy against comparable firms.

### Peer Table

| Company | Payout Ratio | Dividend Yield | Buyback Yield | Total Yield | Cash Return Ratio | Cash/Revenue |
|---------|-------------|----------------|---------------|-------------|-------------------|-------------|
| **Target** | % | % | % | % | % | % |
| Peer 1 | % | % | % | % | % | % |
| Peer 2 | % | % | % | % | % | % |
| Peer 3 | % | % | % | % | % | % |
| Peer 4 | % | % | % | % | % | % |
| **Peer Median** | **%** | **%** | **%** | **%** | **%** | **%** |

### Deviation Analysis

| Metric | Target | Peer Median | Deviation | Explanation |
|--------|--------|-------------|-----------|-------------|
| Payout Ratio | % | % | +/-pp | |
| Total Yield | % | % | +/-pp | |
| Cash Return Ratio | % | % | +/-pp | |
| Cash/Revenue | % | % | +/-pp | |

Significant deviations from peer norms should be explained by differences in growth rate, ROC, reinvestment opportunity, or life cycle stage.

---

## Payout Policy Recommendation

Synthesize findings into a concrete, actionable recommendation.

### Current State Summary

| Dimension | Finding |
|-----------|---------|
| FCFE | $ per year |
| Current cash returned | $ per year (% of FCFE) |
| Excess cash | $ (X years of FCFE) |
| ROC vs WACC | ROC = %, WACC = % (spread: +/- pp) |
| Reinvestment quality | [Improving / Stable / Declining] |
| Peer comparison | [Above / In line / Below] peer norms |

### Recommended Policy

| Component | Current | Recommended | Change | Rationale |
|-----------|---------|-------------|--------|-----------|
| Annual Dividends | $ | $ | +/-$ | |
| Annual Buybacks | $ | $ | +/-$ | |
| Total Annual Return | $ | $ | +/-$ | |
| Cash Return Ratio | % | % | +/-pp | |
| Excess Cash Return | N/A | $ over X years | | |

### Dividend vs Buyback Split Rationale

| Factor | Assessment | Implication |
|--------|-----------|-------------|
| Cash flow stability | [Stable/Variable/Cyclical] | [Supports/Limits] dividend capacity |
| Tax regime | [Dividends favored/Neutral/Capital gains favored] | Favors [dividends/buybacks] |
| Investor base | [Income-seeking/Mixed/Growth-oriented] | Favors [dividends/buybacks] |
| Stock valuation | [Undervalued/Fair/Overvalued] | Buybacks [accretive/neutral/dilutive] |
| Management confidence | [High/Moderate/Low] in sustainable FCFE | [Supports/Limits] dividend commitment |

### Implementation Path

- **Year 1**: [Specific actions -- dividend increase amount, buyback authorization size]
- **Year 2**: [Continuation or adjustment]
- **Year 3**: [Target steady-state policy]
- **Triggers for reassessment**: [ROC drops below WACC, major acquisition, debt maturity, regulatory change]

---

## Cash Accumulation Projection

Project cash balance under current vs recommended policy to illustrate the impact.

### Projection Table

| Year | FCFE | Current Policy Returns | Current Cash Balance | Recommended Returns | Recommended Cash Balance |
|------|------|----------------------|---------------------|--------------------|-----------------------|
| 0 (Now) | -- | -- | $ | -- | $ |
| 1 | $ | $ | $ | $ | $ |
| 2 | $ | $ | $ | $ | $ |
| 3 | $ | $ | $ | $ | $ |
| 4 | $ | $ | $ | $ | $ |
| 5 | $ | $ | $ | $ | $ |

**Assumptions**:
- FCFE growth rate: % per year
- Current policy: dividends grow at % per year, buybacks at $ per year
- Recommended policy: [describe changes]
- Excess cash return: $ distributed over [X] years

**Key takeaway**: Under current policy, cash balance grows to $[X] by Year 5 (equivalent to [Y] years of FCFE). Under recommended policy, cash stabilizes at $[Z] (operating needs plus modest buffer).
