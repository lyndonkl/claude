---
name: dividend-buyback-analyzer
description: Determines how much cash a company can return to shareholders and whether to use dividends, buybacks, or retained earnings. Compares actual cash returns to FCFE capacity, identifies excess cash on the balance sheet, and recommends an optimal return policy. Use when analyzing dividend policy, evaluating share buybacks, assessing cash return capacity, or when user mentions dividend policy, buyback, share repurchase, FCFE, payout ratio, cash return, or excess cash.
---
# Dividend and Buyback Analysis

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Mature tech company -- assess whether it is returning enough cash to shareholders and in what form.

**Inputs**:
- Net income: $2.0B
- CapEx: $600M, Depreciation: $400M
- Change in working capital: $50M
- Debt repaid: $200M, Debt issued: $300M
- Current dividends: $400M, Current buybacks: $600M
- Cash on balance sheet: $8.0B, Revenue: $15B
- ROC: 12%, WACC: 10%

**Step 1 -- Compute FCFE**:
```
FCFE = Net Income - (CapEx - Depreciation) - Change in WC + (Debt Issued - Debt Repaid)
FCFE = $2.0B - ($600M - $400M) - $50M + ($300M - $200M)
FCFE = $2.0B - $200M - $50M + $100M = $1.85B
```

**Step 2 -- Compare to actual returns**:
```
Total cash returned  = Dividends + Buybacks = $400M + $600M = $1.0B
FCFE gap             = $1.85B - $1.0B = $850M (under-returning)
Cash return ratio    = $1.0B / $1.85B = 54% (returning only ~half of capacity)
```

**Step 3 -- Assess excess cash**:
```
Operating cash needs = Revenue x 3% = $15B x 0.03 = $450M
Excess cash          = $8.0B - $450M = $7.55B
```

**Step 4 -- Evaluate reinvestment quality**:
```
ROC (12%) > WACC (10%) -- still earning above cost of capital
But gap is narrowing and reinvestment opportunities are declining
```

**Step 5 -- Determine dividend vs buyback split**:
- Dividends create sticky expectations; maintain at $400M
- Buybacks offer flexibility; increase to $1.15B
- Return $2B of excess cash via special buyback program over 2 years

**Step 6 -- Recommendation**:
- Increase total annual return from $1.0B to $1.55B (84% of FCFE)
- Return $2B of excess cash via accelerated buyback over 24 months
- Retain $500M/year of FCFE for reinvestment (ROC > WACC, but selective)

## Workflow

Copy this checklist and track your progress:

```
Dividend & Buyback Analysis Progress:
- [ ] Step 1: Compute FCFE (what the company can afford to return)
- [ ] Step 2: Compare to actual cash returned (dividends + buybacks)
- [ ] Step 3: Assess excess cash on balance sheet
- [ ] Step 4: Evaluate reinvestment quality (ROC vs WACC)
- [ ] Step 5: Determine optimal split (dividends vs buybacks)
- [ ] Step 6: Make recommendation
```

**Step 1: Compute FCFE**

Calculate free cash flow to equity -- the maximum sustainable cash return to shareholders. See [resources/template.md](resources/template.md#fcfe-calculation-template) for the computation worksheet and [resources/methodology.md](resources/methodology.md#fcfe-based-cash-return-framework) for the conceptual framework.

```
FCFE = Net Income - (CapEx - Depreciation) - Change in WC + (Debt Issued - Debt Repaid)
```

If FCFE is negative, the company cannot sustainably return cash and should be retaining or raising capital instead. Use multi-year average FCFE for cyclical companies.

**Step 2: Compare to actual cash returned**

Compute total cash returned (dividends + buybacks) and compare to FCFE. See [resources/template.md](resources/template.md#fcfe-vs-actual-return-comparison) for the comparison table.

Three outcomes:
- Cash returned < FCFE: Company is under-returning (accumulating cash)
- Cash returned approximately equal to FCFE: Company is returning what it can afford
- Cash returned > FCFE: Company is over-returning (borrowing to pay dividends or depleting cash -- unsustainable)

**Step 3: Assess excess cash on balance sheet**

Determine how much cash exceeds operating needs. See [resources/methodology.md](resources/methodology.md#excess-cash-methodology) for industry norms on operating cash requirements.

```
Excess Cash = Cash on Hand - Operating Cash Needs
Operating Cash Needs typically = 2-5% of Revenue (varies by industry)
```

Large excess cash indicates accumulated under-returning. This is a stock of past under-distribution, separate from the flow (FCFE vs returns).

**Step 4: Evaluate reinvestment quality**

Assess whether the company has profitable uses for retained cash. See [resources/methodology.md](resources/methodology.md#reinvestment-quality-assessment) for the ROC vs WACC framework.

- ROC > WACC with growing opportunities: retention is justified
- ROC > WACC but declining: return more, reinvest selectively
- ROC < WACC: return all FCFE; the company is destroying value by reinvesting

**Step 5: Determine optimal split (dividends vs buybacks)**

Choose the return mechanism based on cash flow predictability, tax regime, and investor base. See [resources/methodology.md](resources/methodology.md#dividend-vs-buyback-decision-framework) for the full decision framework.

Key considerations:
- Dividends are sticky -- once initiated, cutting them signals distress
- Buybacks are flexible -- can be scaled up or down with cash flow
- Tax regime: if capital gains are taxed lower than dividends, favor buybacks
- Signaling: dividends signal confidence in stable future cash flows

**Step 6: Make recommendation**

Synthesize findings into a concrete policy recommendation. See [resources/template.md](resources/template.md#payout-policy-recommendation) for the recommendation template. Validate using [resources/evaluators/rubric_dividend_buyback_analyzer.json](resources/evaluators/rubric_dividend_buyback_analyzer.json). Minimum standard: average score of 3.5 or higher.

## Common Patterns

**Pattern 1: Cash Hoarder**
- **Profile**: FCFE substantially exceeds cash returned; large and growing cash balance; ROC declining toward WACC
- **Signals**: Cash/Revenue ratio > 20%, cash return ratio < 50%, cash balance growing year-over-year
- **Typical companies**: Mature tech, pharma with expired patents, conglomerates
- **Recommendation**: Increase total return toward 80-100% of FCFE; return excess cash via special buyback or special dividend; shift composition toward buybacks for flexibility
- **Risk if unaddressed**: Activist pressure, value-destroying acquisitions with excess cash, agency costs

**Pattern 2: Dividend Stretcher**
- **Profile**: Dividends exceed FCFE; company borrowing or depleting cash to maintain dividend
- **Signals**: Cash return ratio > 120% of FCFE, rising debt with flat earnings, declining cash reserves
- **Typical companies**: Mature utilities post-regulation change, cyclical industrials in downturn, companies with legacy high-dividend culture
- **Recommendation**: Reduce dividend to sustainable level (70-80% of normalized FCFE); communicate reset clearly to investors; consider replacing part of dividend with buyback for flexibility
- **Risk if unaddressed**: Credit downgrade, forced dividend cut under duress (worse market reaction than proactive cut)

**Pattern 3: High-Growth Retainer**
- **Profile**: Low or zero cash returns; high reinvestment rate; ROC well above WACC
- **Signals**: Cash return ratio near 0%, reinvestment rate > 70%, ROC 2x+ WACC, revenue growing > 15%/year
- **Typical companies**: Young tech, biotech with pipeline, high-growth retail expanding
- **Recommendation**: Retention is appropriate if reinvestment opportunities remain; initiate modest buyback when growth moderates; avoid dividends until cash flows stabilize
- **Risk if unaddressed**: None if ROC stays high; reassess annually as growth decelerates

**Pattern 4: Mature Returner**
- **Profile**: Stable FCFE; balanced dividend and buyback program; cash return ratio 80-100%
- **Signals**: Steady payout ratio 40-60%, total yield 3-5%, cash balance stable
- **Typical companies**: Consumer staples, large-cap industrials, mature financials
- **Recommendation**: Maintain current policy; grow dividends in line with earnings growth; use buybacks as residual (absorb cyclical FCFE variation); optimize tax efficiency of split
- **Risk if unaddressed**: Low risk; periodic review to ensure ROC still exceeds WACC on retained portion

## Guardrails

1. **FCFE sets the ceiling on sustainable cash returns.** Dividends plus buybacks cannot exceed FCFE indefinitely without depleting cash or increasing debt. Short-term over-distribution is acceptable if FCFE is temporarily depressed, but multi-year over-distribution is unsustainable.

2. **Dividends create expectations; buybacks are flexible.** Match the return mechanism to cash flow predictability. Stable, predictable cash flows support dividends. Variable or cyclical cash flows favor buybacks as the primary return vehicle.

3. **Tax regime affects the optimal split.** If capital gains are taxed at a lower rate than ordinary income (dividends), buybacks are more tax-efficient for shareholders. Consider the investor base: tax-exempt institutions are indifferent; taxable individuals prefer the lower-taxed form.

4. **Excess cash calculation requires estimating operating cash needs.** Operating cash needs typically range from 2% of revenue (stable, predictable businesses) to 5% of revenue (cyclical or seasonal businesses). Cash beyond this threshold is excess and should be evaluated for return to shareholders.

5. **If ROC exceeds WACC and the company has good projects, retention is appropriate.** A high FCFE does not automatically mean the company should return it all. The quality of reinvestment opportunities matters -- but hold management accountable for delivering returns above cost of capital.

6. **Compare payout policy to peers.** Check the company's payout ratio, dividend yield, and total yield against industry norms. Significant deviations should be explained by differences in growth, risk, or reinvestment opportunity.

**Common pitfalls:**

- Treating dividends as a fixed obligation when the company's cash flows have become volatile -- dividends should be reset to a sustainable level
- Using book value of equity instead of market value when computing yields -- always use market-based metrics for investor-facing ratios
- Ignoring the stock of excess cash when focusing only on the flow (FCFE) -- both dimensions matter
- Assuming buybacks are always value-creating -- buybacks at overvalued prices destroy value; repurchasing at fair value or below creates value
- Not adjusting FCFE for one-time items -- use normalized or multi-year average FCFE for policy decisions

## Quick Reference

**Key formulas:**

```
FCFE = Net Income - (CapEx - Depreciation) - Change in WC + (Debt Issued - Debt Repaid)

Cash Returned = Dividends + Share Buybacks

Cash Return Ratio = Cash Returned / FCFE

Payout Ratio = Dividends / Net Income

Excess Cash = Cash on Hand - Operating Cash Needs

Dividend Yield = Dividends per Share / Price per Share

Buyback Yield = Value of Shares Repurchased / Market Cap

Total Shareholder Yield = Dividend Yield + Buyback Yield

Operating Cash Needs = Revenue x Operating Cash % (typically 2-5%)
```

**Decision framework:**

| Cash Return Ratio | ROC vs WACC | Excess Cash | Recommendation |
|-------------------|-------------|-------------|----------------|
| < 50% of FCFE | ROC < WACC | Large | Increase returns substantially; return excess cash |
| < 50% of FCFE | ROC > WACC | Moderate | Retain for reinvestment if projects are strong |
| 50-80% of FCFE | ROC > WACC | Low | Reasonable balance; fine-tune split |
| 80-100% of FCFE | ROC near WACC | Low | Optimal range for mature companies |
| > 100% of FCFE | Any | Declining | Unsustainable; reduce returns to FCFE level |

**Dividend vs buyback selection:**

| Factor | Favors Dividends | Favors Buybacks |
|--------|-----------------|-----------------|
| Cash flow stability | Stable, predictable | Variable, cyclical |
| Tax regime | Dividends taxed same or lower | Capital gains taxed lower |
| Investor base | Income-seeking (retirees, funds) | Growth-oriented, tax-sensitive |
| Stock valuation | N/A | Undervalued (accretive) |
| Signaling intent | Commitment to ongoing returns | Flexibility, opportunistic |
| Management confidence | High confidence in sustainability | Uncertainty about future cash flows |

**Key resources:**

- **[resources/template.md](resources/template.md)**: FCFE calculation worksheet, FCFE vs actual return comparison, excess cash calculation, payout policy recommendation template, peer comparison table
- **[resources/methodology.md](resources/methodology.md)**: FCFE-based cash return framework, dividend vs buyback decision framework, excess cash methodology, reinvestment quality assessment, tax considerations
- **[resources/evaluators/rubric_dividend_buyback_analyzer.json](resources/evaluators/rubric_dividend_buyback_analyzer.json)**: Quality criteria for FCFE accuracy, cash return comparison, excess cash assessment, recommendation quality

**Inputs required:**

- **Financial data**: Net income, CapEx, depreciation, working capital change, debt issued/repaid
- **Cash return data**: Dividends paid, shares repurchased (value)
- **Balance sheet**: Cash and marketable securities, total revenue
- **Valuation data**: ROC, WACC, market capitalization, share price
- **Context**: Industry norms, tax regime, investor base composition, management guidance

**Outputs produced:**

- `dividend-buyback-analysis.md`: Complete analysis with FCFE computation, cash return comparison, excess cash assessment, reinvestment quality evaluation, dividend vs buyback recommendation, peer comparison, projected cash accumulation under current vs recommended policy
