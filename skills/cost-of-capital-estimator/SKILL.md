---
name: cost-of-capital-estimator
description: Computes cost of equity (CAPM), cost of debt (synthetic rating), and weighted average cost of capital (WACC) for any company in any currency. Handles emerging market risk premiums, bottom-up beta estimation, and multi-country operations. Use when estimating discount rates, computing WACC, determining hurdle rates, analyzing cost of equity or debt, or when user mentions cost of capital, WACC, beta, equity risk premium, country risk premium, or discount rate.
---
# Cost of Capital Estimator

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Company**: Ambev (Brazilian beverage company)
- Incorporated in Brazil; revenue split: Brazil 60%, Latin America 30%, US 10%
- Industry: Beverages (alcoholic and non-alcoholic)
- Current D/E ratio: 25% (market values); marginal tax rate: 34%

**Step 1 -- Riskfree rate (BRL analysis)**

US 10-year Treasury yield: 4.0%. Brazil government bond: 11.0%. Brazil sovereign default spread (Baa2 rating): 2.5%.

Option A -- Subtract default spread: 11.0% - 2.5% = 8.5% (riskfree rate in BRL, captures inflation differential).

Option B -- Build from US rate + inflation differential: (1.04) x (1.06)/(1.02) - 1 = 8.1% (using expected inflation: Brazil 6%, US 2%).

Use 8.5% for this analysis (Option A, simpler and directly observable).

**Step 2 -- Equity risk premium buildup**

Mature market ERP (implied, S&P 500): 5.0%.

Country risk premiums (CRP):
- Brazil: Default spread 2.5% x (equity vol / bond vol) = 2.5% x 1.5 = 3.75%
- Other LatAm (average): 3.0%
- US: 0%

Operation-weighted CRP = 0.60 x 3.75% + 0.30 x 3.0% + 0.10 x 0% = 3.15%.

Total ERP = 5.0% + 3.15% = 8.15%.

**Step 3 -- Bottom-up beta**

Comparable beverage firms (global, n=20): Median unlevered beta = 0.80.

Relever at Ambev's capital structure:
Levered Beta = 0.80 x (1 + (1 - 0.34) x 0.25) = 0.80 x 1.165 = 0.93.

**Step 4 -- Cost of equity**

Cost of Equity = 8.5% + 0.93 x 8.15% = 8.5% + 7.58% = **16.08%**.

**Step 5 -- Cost of debt (synthetic rating)**

EBIT: R$20B, Interest expense: R$2.5B. Interest coverage = 8.0x.

Lookup: Coverage of 8.0x maps to A rating for large firms, default spread = 1.00%.

Pre-tax cost of debt = 8.5% + 1.00% = 9.50%.

After-tax cost of debt = 9.50% x (1 - 0.34) = 6.27%.

**Step 6 -- WACC**

Capital structure weights (market values): E/(D+E) = 80%, D/(D+E) = 20%.

WACC = 16.08% x 0.80 + 6.27% x 0.20 = 12.86% + 1.25% = **14.12%**.

**Interpretation**: This is a BRL-denominated WACC. Use it to discount BRL-denominated cash flows. For USD-denominated analysis, rebuild using USD riskfree rate and adjust the ERP accordingly.

## Workflow

Copy this checklist and track your progress:

```
Cost of Capital Estimation Progress:
- [ ] Step 1: Determine riskfree rate for analysis currency
- [ ] Step 2: Estimate equity risk premium (mature market + country risk)
- [ ] Step 3: Estimate beta (regression or bottom-up)
- [ ] Step 4: Compute cost of equity
- [ ] Step 5: Compute cost of debt via synthetic rating
- [ ] Step 6: Compute WACC and validate
```

**Step 1: Determine riskfree rate for analysis currency**

The riskfree rate anchors the entire computation. It should be denominated in the same currency as projected cash flows.

- For USD or EUR analysis: use the 10-year government bond yield for the US or Germany.
- For emerging market currencies: subtract the sovereign default spread from the local government bond yield, or use the US rate adjusted by the inflation differential.

See [resources/methodology.md](resources/methodology.md#riskfree-rate-derivation) for the inflation-differential approach and when each method is appropriate.

**Step 2: Estimate equity risk premium (mature market + country risk)**

Build the ERP in two layers:

1. Start with the implied ERP for a mature market (S&P 500). This is the baseline premium investors demand above the riskfree rate for holding equities.
2. Add the country risk premium (CRP) appropriate for where the company operates. Weight the CRP by revenue geography, not by country of incorporation.

See [resources/methodology.md](resources/methodology.md#four-step-erp-procedure) for the four-step ERP estimation and [resources/methodology.md](resources/methodology.md#country-risk-premium-approaches) for the three approaches to corporate country risk exposure.

**Step 3: Estimate beta (regression or bottom-up)**

Bottom-up beta is preferred over regression beta because it uses a larger sample, reflects the current business mix, and allows you to set the capital structure to the target rather than historical average.

1. Identify comparable firms in the same industry (15-20 minimum).
2. Find their equity betas, unlever each using its own D/E and tax rate.
3. Take the median unlevered beta.
4. Relever at the target company's D/E ratio and marginal tax rate.

See [resources/methodology.md](resources/methodology.md#bottom-up-beta-estimation) for the complete procedure and the relevering formula.

**Step 4: Compute cost of equity**

Apply the CAPM formula. For emerging market companies, incorporate the country risk premium into the expected return calculation. See [resources/template.md](resources/template.md#cost-of-equity-calculation) for the calculation worksheet.

**Step 5: Compute cost of debt via synthetic rating**

Estimate what rating the company would receive based on its interest coverage ratio, then look up the corresponding default spread.

1. Compute interest coverage = EBIT / Interest Expense.
2. Map to a synthetic rating using the lookup table (separate tables for large and small firms).
3. Cost of debt = Riskfree rate + Default spread for that rating.
4. After-tax cost of debt = Cost of debt x (1 - Marginal tax rate).

See [resources/methodology.md](resources/methodology.md#synthetic-rating-table) for the complete interest-coverage-to-rating-to-spread lookup table.

**Step 6: Compute WACC and validate**

Combine cost of equity and after-tax cost of debt using market value weights.

See [resources/template.md](resources/template.md#wacc-computation-worksheet) for the complete worksheet. Validate using [resources/evaluators/rubric_cost_of_capital_estimator.json](resources/evaluators/rubric_cost_of_capital_estimator.json). Minimum standard: Average score of 3.5 or higher.

## Common Patterns

**Pattern 1: US / Developed Market Company**

- **Riskfree rate**: US 10-year Treasury yield (or equivalent government bond in the analysis currency).
- **ERP**: Implied mature market premium only (no country risk premium).
- **Beta**: Regression beta available from financial data providers; bottom-up beta still preferred for stability.
- **Cost of debt**: Actual credit rating from Moody's/S&P if available; synthetic rating as cross-check.
- **Simplifications**: No currency conversion needed, no CRP weighting, no inflation differential.
- **When**: Large-cap US/European/Japanese companies with primarily domestic operations.

**Pattern 2: Emerging Market Company**

- **Riskfree rate**: Derived from local government bond minus sovereign default spread, or built from US riskfree rate plus inflation differential.
- **ERP**: Mature market premium + operation-weighted country risk premium.
- **Beta**: Bottom-up from global industry peers (emerging market betas from regression are noisy due to thin trading).
- **Cost of debt**: Synthetic rating preferred (local credit ratings may not be comparable).
- **Key decisions**: Currency of analysis, CRP weighting method, whether to add country risk to cost of debt or only to cost of equity.
- **When**: Companies incorporated in or with significant operations in Brazil, India, China, South Africa, Turkey, etc.

**Pattern 3: Private Company**

- **Riskfree rate**: Same as public company in same currency.
- **ERP**: Same as public company in same geography.
- **Beta**: Bottom-up from public peers, but consider total beta adjustment if the owner is undiversified. Total beta = market beta / correlation with market, resulting in a higher cost of equity.
- **Cost of debt**: Synthetic rating using the small-firm lookup table (tighter interest coverage thresholds).
- **Key decision**: Is the buyer/owner diversified (use market beta) or undiversified (use total beta)?
- **When**: Private companies, PE-owned firms, family businesses, startups.

**Pattern 4: Multi-Division Conglomerate**

- **Approach**: Estimate a separate cost of capital for each division using division-appropriate unlevered beta and country risk.
- **Beta**: Use industry-specific unlevered beta for each division (not the conglomerate's blended beta).
- **CRP**: Weight by each division's geographic revenue mix.
- **WACC**: Compute divisional WACCs separately; the corporate WACC is the value-weighted average across divisions.
- **When**: Diversified conglomerates operating across multiple industries and/or geographies.

## Guardrails

1. **Currency consistency**: The riskfree rate, cash flows, and WACC should all be denominated in the same currency. Mixing a USD riskfree rate with BRL cash flows produces meaningless results.

2. **Implied ERP over historical**: Use the implied equity risk premium derived from current market levels rather than long-run historical averages. The implied ERP reflects what investors are demanding today; historical averages are backward-looking and vary widely depending on the time period chosen.

3. **Bottom-up beta preferred**: Regression betas have high standard errors (often 0.20+), reflect historical business mix, and use historical capital structure. Bottom-up betas from 15-20 comparable firms produce a more stable and forward-looking estimate.

4. **Relevering formula**: Levered Beta = Unlevered Beta x (1 + (1 - Tax Rate) x (Debt/Equity)). Use market values for debt and equity, not book values. The tax rate should be the marginal rate.

5. **Synthetic rating from interest coverage**: Map current interest coverage (EBIT / Interest Expense) to a credit rating using the appropriate table (large firm vs. small firm). Do not rely on assigned ratings for companies that may not be rated.

6. **Market value weights**: WACC uses market value of equity (not book) and market value of debt (approximate with book if trading data unavailable). Book value weights systematically underweight equity for profitable firms.

7. **WACC matches cash flow currency**: If cash flows are in BRL, the WACC should be in BRL. If cash flows are in USD, the WACC should be in USD. Converting a WACC across currencies requires adjusting for the inflation differential between the two currencies.

## Quick Reference

**Key formulas:**

```
Cost of Equity (CAPM) = Riskfree Rate + Beta x Equity Risk Premium

For emerging markets:
  Cost of Equity = Riskfree Rate + Beta x Mature ERP + lambda x CRP
  (Simplified: lambda = 1, so CRP is added directly)

Riskfree Rate (local currency) = Local Govt Bond Yield - Sovereign Default Spread
  OR = (1 + US Rf) x (1 + Inflation_local) / (1 + Inflation_US) - 1

Country ERP = Sovereign Default Spread x (Equity Volatility / Bond Volatility)
  Typical ratio: 1.5x

Operation-weighted CRP = Sum of (Revenue_i% x CRP_i) for each country i

Levered Beta = Unlevered Beta x (1 + (1 - Tax Rate) x (D/E))
Unlevered Beta = Levered Beta / (1 + (1 - Tax Rate) x (D/E))

Total Beta (private, undiversified) = Market Beta / Correlation with Market

Cost of Debt (pre-tax) = Riskfree Rate + Default Spread (from synthetic rating)
Cost of Debt (after-tax) = Pre-tax Cost of Debt x (1 - Marginal Tax Rate)

WACC = ke x (E / (D+E)) + kd(1-t) x (D / (D+E))
```

**Current estimates (update periodically):**

| Parameter | Typical Range | Source |
|-----------|--------------|--------|
| US 10-year Treasury | 3.5% - 5.0% | Federal Reserve |
| Implied ERP (S&P 500) | 4.5% - 6.0% | Damodaran annual update |
| Equity/Bond volatility ratio | 1.3x - 1.7x | Use 1.5x as default |
| Unlevered beta (typical ranges) | 0.5 - 1.5 | By industry sector |

**Key resources:**

- **[resources/template.md](resources/template.md)**: WACC calculation worksheet, ERP buildup template, synthetic rating worksheet, sensitivity table
- **[resources/methodology.md](resources/methodology.md)**: 4-step ERP procedure, country risk premium approaches, bottom-up beta method, synthetic rating lookup table, riskfree rate derivation
- **[resources/evaluators/rubric_cost_of_capital_estimator.json](resources/evaluators/rubric_cost_of_capital_estimator.json)**: Quality criteria for riskfree rate, ERP, beta, cost of debt, WACC

**Inputs required:**

- Company country of incorporation and geographic revenue breakdown
- Industry sector (for comparable firm selection)
- Current debt-to-equity ratio (market values)
- Operating income (EBIT) and interest expense (for interest coverage)
- Marginal tax rate
- Currency for analysis
- Comparable firm betas (or access to financial data providers)

**Outputs produced:**

- `cost-of-capital.md`: Complete WACC computation with riskfree rate derivation, ERP buildup, beta estimation, synthetic rating, cost of equity, cost of debt, and final WACC with sensitivity analysis
