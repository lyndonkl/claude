---
name: financial-statement-analyzer
description: Reads and normalizes a company's financial statements to extract clean valuation inputs. Performs accounting adjustments including R&D capitalization, operating lease conversion to debt, stock-based compensation treatment, and one-time item normalization. Computes FCFF, FCFE, and key financial ratios. Use when preparing financials for valuation, cleaning accounting data, computing free cash flows, analyzing financial ratios, or when user mentions financial statements, FCFF, FCFE, ROIC, R&D capitalization, or operating lease adjustment.
---
# Financial Statement Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Technology company -- $2B revenue, $500M R&D, $100M annual operating lease payments

**Raw financials (as reported)**:
- Revenue: $2,000M
- COGS: $600M
- R&D expense: $500M (expensed entirely)
- SG&A: $300M
- Operating income (EBIT): $600M
- Interest expense: $40M
- Tax rate (marginal): 25%
- CapEx: $150M, Depreciation: $100M
- Change in working capital: +$30M
- Operating lease commitments: $100M/year for 5 years

**Adjustment 1 -- R&D capitalization** (5-year asset life):

| Year | R&D Spend | Amortization (1/5) |
|------|-----------|-------------------|
| Current | $500M | $100M |
| Year -1 | $450M | $90M |
| Year -2 | $400M | $80M |
| Year -3 | $350M | $70M |
| Year -4 | $300M | $60M |

- Total amortization of past R&D: $300M (sum of years -1 through -4)
- Research asset created: unamortized R&D on balance sheet = $1,100M
- Adjusted operating income: $600M + $500M (add back current R&D) - $400M (total amortization) = **$700M**
- Tax adjustment: additional tax on $100M uplift = $25M

**Adjustment 2 -- Operating lease conversion**:
- PV of lease commitments at 5% pre-tax cost of debt: ~$432M debt equivalent
- Reclassify $432M from operating expense to debt on balance sheet
- Adjusted operating income: add back lease expense ($100M), subtract depreciation of lease asset ($86M) = net +$14M
- Adjusted EBIT: $700M + $14M = **$714M**

**Adjusted financials**:
- Adjusted EBIT: $714M
- After-tax operating income: $714M x (1 - 0.25) = $536M
- Adjusted CapEx (including R&D CapEx): $150M + $500M = $650M
- Adjusted depreciation (including R&D amortization): $100M + $400M = $500M
- FCFF: $536M - ($650M - $500M) - $30M = **$356M**
- Adjusted debt: original debt + $432M lease debt
- ROIC: $536M / ($3,500M book capital + $1,100M research asset + $432M lease asset) = **10.6%**
- FCFE: $356M - $40M x (1 - 0.25) + ($200M net debt issued) = **$526M**

**Ratio dashboard**:

| Ratio | Reported | Adjusted |
|-------|----------|----------|
| Operating margin | 30.0% | 35.7% |
| ROIC | 12.9% | 10.6% |
| Debt-to-capital | 20.0% | 28.5% |
| Reinvestment rate | 14.9% | 28.0% |

The adjustments reveal that the company reinvests more heavily than reported figures suggest (R&D is investment, not expense) and carries more leverage once lease obligations are recognized as debt.

## Workflow

Copy this checklist and track progress:

```
Financial Statement Analysis Progress:
- [ ] Step 1: Collect raw financial statements
- [ ] Step 2: Identify and apply accounting adjustments
- [ ] Step 3: Compute free cash flows (FCFF and FCFE)
- [ ] Step 4: Calculate key financial ratios
- [ ] Step 5: Compare to industry benchmarks
- [ ] Step 6: Validate and document
```

**Step 1: Collect raw financial statements**

Gather the three statements: income statement, balance sheet, and cash flow statement. Record at least two years for trend analysis. See [resources/template.md](resources/template.md#financial-data-input-template) for data input fields.

- [ ] Income statement: revenue, COGS, operating expenses, R&D, SG&A, interest, taxes, net income
- [ ] Balance sheet: total assets, debt (short + long term), equity, cash, current assets/liabilities
- [ ] Cash flow statement: operating, investing, financing cash flows
- [ ] Supplemental: R&D expense history (5+ years), operating lease commitments, stock-based compensation

**Step 2: Identify and apply accounting adjustments**

Determine which adjustments apply based on company characteristics. See [resources/methodology.md](resources/methodology.md) for step-by-step procedures for each adjustment type.

- [ ] R&D capitalization: if R&D > 5% of revenue, capitalize and amortize over industry-appropriate life
- [ ] Operating lease conversion: if material lease commitments exist, convert to debt equivalent
- [ ] Stock-based compensation: treat as real operating expense (do not add back)
- [ ] One-time items: identify and normalize genuinely non-recurring charges
- [ ] Document each adjustment with before/after values and rationale

See [resources/template.md](resources/template.md#adjustment-documentation-template) for adjustment documentation format.

**Step 3: Compute free cash flows**

Calculate both FCFF and FCFE from adjusted figures. Verify they reconcile. See [resources/methodology.md](resources/methodology.md#free-cash-flow-computation) for detailed formulas and reconciliation.

- [ ] FCFF = After-tax operating income - (CapEx - Depreciation) - Change in non-cash working capital
- [ ] FCFE = Net income - (CapEx - Depreciation) - Change in WC - (Debt repaid - Debt issued)
- [ ] Reconciliation check: FCFE = FCFF - Interest(1-t) + Net debt change

**Step 4: Calculate key financial ratios**

Compute ratios from adjusted financials for a consistent picture. See [resources/template.md](resources/template.md#ratio-dashboard-template) for the full ratio dashboard.

- [ ] Profitability: operating margin, net margin, ROIC, ROE
- [ ] Leverage: debt-to-capital, interest coverage, debt-to-EBITDA
- [ ] Efficiency: reinvestment rate, sales-to-capital, asset turnover
- [ ] Liquidity: current ratio, quick ratio

**Step 5: Compare to industry benchmarks**

Place the company's adjusted ratios in context. See [Quick Reference](#quick-reference) for benchmark ranges by sector.

- [ ] Compare operating margin to sector quartiles
- [ ] Compare ROIC to sector median and to the company's own WACC
- [ ] Compare debt-to-capital to sector norm
- [ ] Flag ratios that are outliers (above 75th or below 25th percentile)

**Step 6: Validate and document**

Review completeness and consistency. Validate using [resources/evaluators/rubric_financial_statement_analyzer.json](resources/evaluators/rubric_financial_statement_analyzer.json). Minimum standard: average score of 3.5 or above.

- [ ] All adjustments documented with rationale
- [ ] FCFF and FCFE reconcile
- [ ] Ratios computed from adjusted (not raw) figures
- [ ] Industry comparison included

## Common Patterns

**Pattern 1: Tech Company (Heavy R&D)**
- **Key adjustments**: Capitalize R&D (asset life 2-3 years for software, 5-10 for biotech/pharma), treat SBC as real expense, capitalize software development costs
- **Typical profile**: High R&D-to-revenue (15-30%), low tangible assets, negative or low FCFF due to heavy reinvestment, high operating margins once R&D is capitalized
- **Watch for**: SBC that inflates cash flow from operations if added back, R&D history needed for capitalization schedule
- **Example sectors**: Software, semiconductors, pharmaceuticals, biotechnology

**Pattern 2: Capital-Heavy Company (Leases and CapEx)**
- **Key adjustments**: Convert operating leases to debt, separate maintenance CapEx from growth CapEx, analyze depreciation schedules
- **Typical profile**: Large fixed asset base, significant lease commitments (pre- or post-ASC 842), high depreciation, moderate margins
- **Watch for**: Accelerated vs straight-line depreciation effects, sale-leaseback transactions, capital vs operating lease classification under ASC 842
- **Example sectors**: Airlines, retail, telecom, real estate, shipping

**Pattern 3: Financial Services Company**
- **Key adjustments**: Debt is operational (raw material, not financing), use equity-only valuation (no FCFF), focus on book value and ROE, regulatory capital requirements
- **Typical profile**: High leverage by design, net interest margin as key metric, ROE rather than ROIC, provision for credit losses as major expense
- **Watch for**: Do not subtract debt from firm value (debt is not financial for banks). The `special-situations-valuation` skill handles this in depth.
- **Example sectors**: Banks, insurance, asset management, REITs

**Pattern 4: Cyclical Company (Earnings Normalization)**
- **Key adjustments**: Average earnings over full business cycle (5-10 years), separate cyclical from secular trends, normalize margins to mid-cycle levels
- **Typical profile**: Revenue and earnings swing with economic cycle, peak margins are not sustainable, trough margins are not permanent
- **Watch for**: Using peak-year earnings as "normal" (overstates value), restructuring charges that recur every downturn (these are not truly one-time)
- **Example sectors**: Automotive, construction, steel, mining, luxury goods

## Guardrails

1. **R&D capitalization asset life**: Use industry-appropriate asset lives. Software and internet: 2-3 years. Consumer products: 5-7 years. Pharmaceuticals: 8-10 years. Using the wrong life distorts both the research asset and adjusted income.

2. **Operating lease discount rate**: Discount future lease commitments at the pre-tax cost of debt, not WACC. The lease obligation is debt-like, so the discount rate should reflect the company's borrowing cost.

3. **Separate operating from non-operating items**: Cash and marketable securities are non-operating assets. Minority interests and cross-holdings need separate treatment. Do not mix operating and financial assets when computing invested capital.

4. **Tax rate selection**: Use marginal tax rate for FCFF computation (forward-looking). Use effective tax rate for historical ratio analysis. If the two diverge significantly, investigate why (tax loss carryforwards, foreign income, tax credits).

5. **FCFF and FCFE reconciliation**: FCFE should equal FCFF minus after-tax interest expense plus net debt issuance. If the two do not reconcile, there is an error in the computation. Check for missed items.

6. **Stock-based compensation is a real cost**: SBC reduces the value of existing shares through dilution. Do not add it back to compute "adjusted" earnings or cash flow. Treat it as an operating expense in the income statement.

7. **Recurring "non-recurring" items**: If a company reports restructuring charges in three of the past five years, these are not genuinely one-time. Normalize by averaging rather than excluding. Truly non-recurring items include asset write-downs from specific events, litigation settlements, and natural disaster impacts.

8. **Document every adjustment**: Each adjustment should include the pre-adjustment value, the post-adjustment value, and the rationale. This makes the analysis reproducible and allows others to disagree with specific adjustments without discarding the entire analysis.

## Quick Reference

**Key formulas:**

```
FCFF = After-tax Operating Income - (CapEx - Depreciation) - Change in Non-cash WC

FCFE = Net Income - (CapEx - Depreciation) - Change in WC - (Debt Repaid - Debt Issued)

Reinvestment Rate = (Net CapEx + Change in WC) / After-tax Operating Income

ROIC = After-tax Operating Income / Invested Capital

ROE = Net Income / Book Value of Equity

Debt-to-Capital = Total Debt / (Total Debt + Market Value of Equity)

Interest Coverage = EBIT / Interest Expense

Sales-to-Capital = Revenue / Invested Capital

R&D Capitalization:
  Research Asset = Sum of unamortized R&D from past N years
  Adjusted Operating Income = Reported OI + Current R&D - Total Amortization

Operating Lease Conversion:
  Lease Debt = PV of future lease commitments at pre-tax cost of debt
  Adjusted EBIT = Reported EBIT + Lease Expense - Depreciation of Lease Asset
```

**Ratio benchmarks by sector (approximate medians):**

| Metric | Tech | Industrial | Consumer | Healthcare |
|--------|------|-----------|----------|------------|
| Operating margin | 20-25% | 10-15% | 8-12% | 15-20% |
| ROIC | 15-25% | 10-15% | 12-18% | 12-20% |
| Debt-to-capital | 10-20% | 25-35% | 20-30% | 15-25% |
| Reinvestment rate | 40-60% | 30-50% | 25-40% | 35-55% |
| Sales-to-capital | 1.5-2.5 | 1.0-1.5 | 1.5-2.0 | 1.0-1.5 |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Financial data input template, adjustment documentation template, ratio dashboard, FCFF/FCFE worksheet
- **[resources/methodology.md](resources/methodology.md)**: R&D capitalization procedure, operating lease conversion, SBC treatment, normalization techniques, cash flow reconciliation
- **[resources/evaluators/rubric_financial_statement_analyzer.json](resources/evaluators/rubric_financial_statement_analyzer.json)**: Quality criteria for data completeness, adjustment accuracy, cash flow computation, ratio analysis

**Inputs required:**

- Income statement (revenue, COGS, R&D, SG&A, interest, taxes, net income)
- Balance sheet (total assets, current assets, fixed assets, debt, equity, cash)
- Cash flow statement (operating, investing, financing cash flows)
- R&D expense history (5+ years if capitalizing)
- Operating lease commitments schedule
- Effective and marginal tax rates

**Outputs produced:**

- Cleaned financials with all adjustments documented (before/after)
- FCFF and FCFE calculations with reconciliation
- Ratio dashboard (profitability, leverage, efficiency, liquidity)
- Industry comparison with sector benchmarks
