---
name: intrinsic-valuation-dcf
description: Performs discounted cash flow valuation using the appropriate model variant (DDM, FCFE, or FCFF) with configurable growth stages. Produces year-by-year cash flow projections, terminal value, equity bridge (subtract debt, add cash, subtract option value), per-share intrinsic value, and sensitivity analysis. Use when valuing a company intrinsically, building a DCF model, estimating fair value, or when user mentions DCF, discounted cash flow, intrinsic value, terminal value, or free cash flow valuation.
---
# Intrinsic Valuation (DCF)

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Two-stage FCFF model for a mature growth company

**Inputs**:
- Base year EBIT: $500M, Tax rate: 25%, CapEx: $200M, Depreciation: $150M, WC change: $20M
- High-growth period: 5 years, revenue growth 12%, reinvestment rate 50%, WACC 9%
- Stable period: perpetual growth 3%, reinvestment rate 30%, WACC 8.5%

**Step-by-step**:

1. Base year after-tax operating income: $500M x (1 - 0.25) = $375M
2. Base year FCFF: $375M - ($200M - $150M) - $20M = $305M

3. Year-by-year projections (high-growth, 12% growth, 50% reinvestment):

| Year | After-tax EBIT | Reinvestment | FCFF    | PV Factor (9%) | PV of FCFF |
|------|---------------|-------------|---------|----------------|------------|
| 1    | $420.0M       | $210.0M     | $210.0M | 0.9174         | $192.7M    |
| 2    | $470.4M       | $235.2M     | $235.2M | 0.8417         | $198.0M    |
| 3    | $526.8M       | $263.4M     | $263.4M | 0.7722         | $203.4M    |
| 4    | $590.1M       | $295.0M     | $295.0M | 0.7084         | $208.9M    |
| 5    | $660.9M       | $330.4M     | $330.4M | 0.6499         | $214.8M    |

4. Terminal value (end of year 5):
   - Stable FCFF = $660.9M x (1.03) x (1 - 0.30) = $476.5M
   - Terminal value = $476.5M / (0.085 - 0.03) = $8,663M
   - PV of terminal value = $8,663M x 0.6499 = $5,631M

5. Firm value = $1,017.8M + $5,631M = $6,649M

6. Equity bridge:
   - Firm value: $6,649M
   - Minus debt: -$2,000M
   - Plus cash: +$500M
   - Minus employee options: -$200M
   - Equity value: $4,949M
   - Per share (100M shares): **$49.49**

7. Sensitivity grid (per-share value):

| WACC \ Growth | 2.0%  | 2.5%  | 3.0%  | 3.5%  | 4.0%  |
|---------------|-------|-------|-------|-------|-------|
| 7.5%          | $62   | $68   | $76   | $86   | $99   |
| 8.0%          | $53   | $57   | $62   | $69   | $78   |
| 8.5%          | $45   | $48   | $52   | $57   | $63   |
| 9.0%          | $39   | $41   | $44   | $48   | $52   |
| 9.5%          | $34   | $36   | $38   | $41   | $44   |

## Workflow

Copy this checklist and track your progress:

```
DCF Valuation Progress:
- [ ] Step 1: Select DCF model variant
- [ ] Step 2: Establish base year cash flows
- [ ] Step 3: Estimate growth rate and high-growth period length
- [ ] Step 4: Project year-by-year cash flows
- [ ] Step 5: Compute terminal value
- [ ] Step 6: Discount, bridge to equity, compute per-share value
- [ ] Step 7: Build sensitivity analysis
```

**Step 1: Select DCF model variant**

Choose the model that matches the company and context. See [resources/methodology.md](resources/methodology.md#model-selection-decision-tree) for the full decision tree.

Quick selection guide:
- **FCFF**: Default for most companies. Values the entire firm, discounts at WACC, subtracts debt for equity. Use when capital structure is expected to change or when the company has significant debt.
- **FCFE**: Values equity directly, discounts at cost of equity. Use when capital structure is stable and debt ratio is predictable.
- **DDM**: Values equity via dividends, discounts at cost of equity. Use for mature, stable dividend-paying companies (utilities, REITs, mature banks).

**Step 2: Establish base year cash flows**

Start from cleaned financials (ideally from financial-statement-analyzer output). See [resources/template.md](resources/template.md#base-year-inputs) for the base year input template.

For FCFF:
- After-tax operating income = EBIT x (1 - tax rate)
- FCFF = After-tax EBIT - (CapEx - Depreciation) - Change in non-cash working capital

For FCFE:
- FCFE = Net Income - (CapEx - Depreciation) - Change in WC + (New debt issued - Debt repaid)

For DDM:
- Current dividends per share, payout ratio, earnings per share

**Step 3: Estimate growth rate and high-growth period length**

See [resources/methodology.md](resources/methodology.md#growth-estimation) for growth estimation methods.

Three approaches to estimating growth:
- **Fundamental**: g = Reinvestment rate x Return on capital (for FCFF) or g = Retention ratio x ROE (for FCFE/DDM)
- **Historical**: Extrapolate recent growth with judgment about sustainability
- **Analyst consensus**: Use as cross-check, not primary source

High-growth period length depends on competitive advantage magnitude and sustainability (typically 5-10 years).

**Step 4: Project year-by-year cash flows**

Build the projection table for each year of the high-growth period. See [resources/template.md](resources/template.md#year-by-year-projection-table) for the projection template.

For each year, compute:
- Revenue (or operating income) based on growth rate
- Reinvestment (based on reinvestment rate or sales-to-capital ratio)
- Free cash flow = Income after tax - Reinvestment
- Present value factor = 1 / (1 + discount rate)^year
- Present value of cash flow

**Step 5: Compute terminal value**

See [resources/methodology.md](resources/methodology.md#terminal-value) for terminal value approaches and constraints.

Growing perpetuity (preferred):
- Terminal value = CF in year n+1 / (discount rate - stable growth rate)
- Stable growth rate should not exceed the risk-free rate or nominal GDP growth
- Reinvestment rate in stable period: g / ROC (so growth is consistent with reinvestment)
- Cost of capital should converge toward mature company levels

Exit multiple cross-check (secondary):
- Apply industry EV/EBITDA or PE multiple to terminal year financials
- Compare to perpetuity-based terminal value for reasonableness

**Step 6: Discount, bridge to equity, compute per-share value**

See [resources/template.md](resources/template.md#equity-bridge) for the equity bridge template.

1. Sum PV of high-growth cash flows + PV of terminal value = Operating asset value
2. Add: Value of cash and non-operating assets
3. Subtract: Market value of debt (all debt included in WACC calculation)
4. Subtract: Value of employee stock options (use treasury stock method or Black-Scholes)
5. Subtract: Minority interests (at market value if available)
6. Divide by diluted share count = Per-share intrinsic value

**Step 7: Build sensitivity analysis**

See [resources/template.md](resources/template.md#sensitivity-grid) for the sensitivity grid template.

At minimum, vary:
- Stable growth rate (rows)
- Discount rate / WACC (columns)

Additional sensitivity dimensions to consider:
- Revenue growth rate in high-growth period
- Target operating margin
- Length of high-growth period
- Reinvestment rate

Validate using [resources/evaluators/rubric_intrinsic_valuation_dcf.json](resources/evaluators/rubric_intrinsic_valuation_dcf.json). **Minimum standard**: Average score of 3.5 or higher.

## Common Patterns

**Pattern 1: FCFF Two-Stage (Most Common)**
- **When**: Company with identifiable high-growth period followed by stable growth. Changing or uncertain capital structure. Most non-financial companies.
- **Structure**: Project FCFF for 5-10 years at above-normal growth, then terminal value at stable growth. Discount at WACC.
- **Equity bridge**: Firm value - Debt + Cash - Options = Equity value
- **Key risk**: Terminal value dominance. If terminal value exceeds 85% of total value, consider whether the high-growth period is too short or growth too low.

**Pattern 2: FCFE Two-Stage**
- **When**: Stable, predictable capital structure. Company manages to a target debt ratio. Financial services firms where FCFF is not meaningful.
- **Structure**: Project FCFE for high-growth period, then terminal value. Discount at cost of equity.
- **Equity bridge**: Not needed -- result is equity value directly. Subtract option value, divide by shares.
- **Key risk**: Debt ratio assumption. If actual debt policy deviates from assumption, value will be wrong.

**Pattern 3: Dividend Discount Model (DDM)**
- **When**: Mature, stable companies with long dividend track records. Utilities, REITs, mature banks, consumer staples.
- **Structure**: Project dividends per share, discount at cost of equity. Terminal value uses stable dividend growth.
- **Equity bridge**: Not needed -- result is per-share equity value.
- **Key risk**: Dividends may not reflect capacity to pay. If payout ratio is very low, DDM underestimates value. Consider augmented DDM (dividends + buybacks).

**Pattern 4: Three-Stage Model**
- **When**: Companies with long growth runways needing a transition period (young growth transitioning through mature growth to stable).
- **Structure**: Stage 1 (high growth, 5 years), Stage 2 (transition, growth declining linearly, 5 years), Stage 3 (stable perpetuity).
- **Key risk**: More parameters to estimate. Transition assumptions (how fast growth declines, when margins stabilize) add uncertainty.

## Guardrails

1. **Discounting consistency**: Match cash flows to discount rates. FCFF at WACC, FCFE at cost of equity, dividends at cost of equity. Mixing them produces meaningless numbers.

2. **Stable growth rate ceiling**: The stable growth rate should not exceed the risk-free rate (for real cash flows) or nominal GDP growth (for nominal cash flows). A company cannot grow faster than the economy in perpetuity.

3. **Terminal value proportion**: Terminal value typically represents 50-80% of total value for growth firms. Flag if it exceeds 90% -- this may indicate that the high-growth assumptions are too conservative or the growth period too short.

4. **Reinvestment-growth consistency**: In the stable period, reinvestment rate should equal g / ROC. If stable growth is 3% and ROC is 10%, reinvestment rate should be 30%. Disconnect between growth and reinvestment implies value creation from thin air.

5. **Equity bridge completeness**: When using FCFF, bridge from firm value to equity by subtracting the market value of debt that was included in the cost of capital, adding cash and non-operating assets, and subtracting employee option value and minority interests.

6. **Diluted share count**: Use the diluted share count (treasury stock method for in-the-money options) rather than basic shares outstanding. For companies with large option grants, the difference is material.

7. **Cost of capital convergence**: In the stable period, beta should converge toward 1.0, debt ratio toward industry average, and WACC toward the weighted average of the market. A company cannot maintain an extremely high or low cost of capital in perpetuity.

8. **Sensitivity analysis breadth**: Vary at least the growth rate and discount rate. The interaction between these two drivers accounts for most of the valuation range. Report the value as a range, not a point estimate.

**Common pitfalls:**

- Projecting high growth for too long (10+ years is rare outside pharmaceutical or platform businesses)
- Using book value of debt instead of market value in the equity bridge
- Forgetting to subtract employee stock option value (material for tech companies)
- Double-counting growth: applying a high growth rate to income that already reflects growth spending
- Assuming current margins are sustainable without checking industry convergence
- Using the same WACC for both the high-growth and stable periods when capital structure is expected to change

## Quick Reference

**Key formulas:**

```
FCFF = After-tax EBIT - (CapEx - Depreciation) - Change in Non-cash WC
     = After-tax EBIT x (1 - Reinvestment Rate)

FCFE = Net Income - (CapEx - Depreciation) - Change in WC + Net Debt Issued
     = Net Income x (1 - Equity Reinvestment Rate)

DDM = Dividends per Share (growing at g, discounted at ke)

Terminal Value (perpetuity) = CF(n+1) / (r - g_stable)

Growth (fundamental):
  g_operating_income = Reinvestment Rate x Return on Capital
  g_net_income = Retention Ratio x Return on Equity

Reinvestment Rate = (CapEx - Depreciation + Change in WC) / After-tax EBIT

Equity Bridge:
  Equity Value = Firm Value - Debt + Cash - Options - Minority Interests
  Per Share = Equity Value / Diluted Shares
```

**Model selection quick guide:**

| Situation | Model | Discount Rate | Result |
|-----------|-------|---------------|--------|
| Most companies, changing capital structure | FCFF | WACC | Firm value (bridge to equity) |
| Stable capital structure, predictable debt | FCFE | Cost of equity | Equity value |
| Mature dividend payers | DDM | Cost of equity | Equity value per share |
| Financial services | FCFE or DDM | Cost of equity | Equity value |
| Long growth runway, transition needed | Three-stage | WACC or ke | Depends on variant |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Base year inputs, year-by-year projection table, terminal value template, equity bridge, sensitivity grid, value decomposition
- **[resources/methodology.md](resources/methodology.md)**: Model selection decision tree, growth estimation methods, terminal value approaches, option adjustment, three-stage mechanics, mid-year convention
- **[resources/evaluators/rubric_intrinsic_valuation_dcf.json](resources/evaluators/rubric_intrinsic_valuation_dcf.json)**: Quality criteria for model selection, projections, terminal value, equity bridge, sensitivity analysis

**Inputs required:**

- Current after-tax operating income (FCFF) or net income (FCFE/DDM)
- Current CapEx, depreciation, and working capital change
- Revenue growth rate for high-growth period
- Target operating margin and reinvestment rate (or sales-to-capital ratio)
- Length of high-growth period (years)
- Stable growth rate
- WACC and/or cost of equity (from cost-of-capital-estimator)
- Current debt, cash, minority interests
- Shares outstanding and employee options (number, strike, maturity)

**Outputs produced:**

- `dcf-valuation.md`: Complete DCF model with year-by-year projections, terminal value, equity bridge, per-share value, sensitivity grid, value decomposition
