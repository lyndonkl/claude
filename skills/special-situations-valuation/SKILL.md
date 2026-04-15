---
name: special-situations-valuation
description: Adapts the standard DCF framework for companies that break normal valuation assumptions. Handles four sub-frameworks: high-growth firms with negative earnings (revenue-based approach with failure probability), distressed firms (equity-as-call-option via Black-Scholes), private companies (total beta and liquidity discount), and financial services firms (excess return model on book equity). Use when valuing unprofitable startups, distressed companies, private firms, banks, insurance companies, or when user mentions negative earnings valuation, distress valuation, private company discount, equity as call option, total beta, liquidity discount, excess return model, or financial services valuation.
---
# Special Situations Valuation

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: High-growth SaaS company with negative earnings

**Inputs**: Revenue $500M, operating loss -$100M (margin -20%), cash $300M, burn rate $80M/year, WACC 10%

**Revenue-based DCF approach**:
1. Target operating margin: 15% (median of mature SaaS peers -- Salesforce, Adobe, ServiceNow)
2. Revenue growth: 30% years 1-3, declining to 3% by year 10
3. Sales-to-capital ratio: 2.0 (each $1 of capital generates $2 of revenue)
4. Year-by-year margin convergence: -20% to +15% linearly over 8 years

**Projected year-by-year summary**:

| Year | Revenue | Op. Margin | EBIT(1-t) | Reinvestment | FCFF |
|------|---------|-----------|-----------|--------------|------|
| 0 | $500M | -20% | -$75M | $163M | -$238M |
| 3 | $1,099M | -6.9% | -$57M | $187M | -$244M |
| 5 | $1,592M | +1.9% | $23M | $163M | -$140M |
| 8 | $2,015M | +11.9% | $180M | $65M | +$115M |
| 10 | $2,139M | +15.0% | $241M | $19M | +$222M |

**Terminal value**: $241M x (1.03) / (0.085 - 0.03) = $4,512M (WACC converges to 8.5% in stable growth)

**DCF value of firm**: $3,200M (PV of cash flows + PV of terminal value)

**Failure adjustment**:
- Cash runway: $300M / $80M = 3.75 years
- Probability of failure: 15% (based on cash runway, industry base rates for SaaS at this stage)
- Distress sale value: $200M (assets in liquidation)

**Adjusted value**: $3,200M x 0.85 + $200M x 0.15 = **$2,750M**

Subtract debt $150M, add cash $300M, subtract options $100M = **equity value $2,800M**

Compare: standard DCF (if earnings were positive) would value firm at $3,200M, so the failure adjustment reduces value by ~14%.

## Workflow

Copy this checklist and track your progress:

```
Special Situations Valuation Progress:
- [ ] Step 1: Classify the special situation
- [ ] Step 2: Select and apply the sub-framework
- [ ] Step 3: Make model-specific adjustments
- [ ] Step 4: Apply probability weighting or discounts
- [ ] Step 5: Compare to standard DCF result
- [ ] Step 6: Validate and document
```

**Step 1: Classify the special situation**

Determine which sub-framework applies based on company characteristics. A company may fall into multiple categories (e.g., a private financial services firm). See [resources/template.md](resources/template.md#situation-classification-guide) for the classification decision tree.

- **High-growth / negative earnings**: Revenue growing >20%, operating income negative or near-zero
- **Distressed**: Debt exceeds asset value or coverage ratios signal default risk
- **Private**: No public market for equity, owner may be undiversified
- **Financial services**: Bank, insurance company, or financial institution where debt is raw material

**Step 2: Select and apply the sub-framework**

Apply the methodology specific to the classified situation. See [resources/methodology.md](resources/methodology.md) for detailed formulas and step-by-step procedures for each sub-framework.

- High-growth: Revenue-based DCF with margin convergence. See [resources/methodology.md](resources/methodology.md#1-high-growth-firms-with-negative-earnings).
- Distressed: Equity-as-call-option (Black-Scholes). See [resources/methodology.md](resources/methodology.md#2-distressed-firms-equity-as-call-option).
- Private: Total beta and liquidity discount. See [resources/methodology.md](resources/methodology.md#3-private-companies).
- Financial services: Excess return model on book equity. See [resources/methodology.md](resources/methodology.md#4-financial-services-firms).

**Step 3: Make model-specific adjustments**

Each sub-framework requires specific adjustments beyond the standard DCF. See [resources/template.md](resources/template.md) for the relevant template with fill-in fields.

- High-growth: Set target margin from mature peers, use sales-to-capital for reinvestment
- Distressed: Estimate firm value volatility (asset-side, not equity-side)
- Private: Determine if owner is diversified (use market beta) or undiversified (use total beta)
- Financial services: Use equity cash flows only, compute ROE relative to cost of equity

**Step 4: Apply probability weighting or discounts**

Incorporate risk adjustments specific to the situation type. See [resources/methodology.md](resources/methodology.md) for estimation approaches.

- High-growth: Failure probability x distress value + (1 - failure probability) x DCF value
- Distressed: Black-Scholes directly prices the probability of recovery into equity value
- Private: Liquidity discount (typically 10-35%, varies with company characteristics)
- Financial services: No special discount, but regulatory capital constraints may limit growth

**Step 5: Compare to standard DCF result**

Show the standard DCF value alongside the adjusted value to make the impact of adjustments transparent. See [resources/template.md](resources/template.md#standard-vs-adjusted-comparison) for the comparison template.

**Step 6: Validate and document**

Validate using [resources/evaluators/rubric_special_situations_valuation.json](resources/evaluators/rubric_special_situations_valuation.json). **Minimum standard**: Average score of 3.5 or above.

## Common Patterns

**Pattern 1: High-Growth / Negative Earnings**
- **When**: Young companies with high revenue growth (>20%) and negative or minimal operating income
- **Approach**: Revenue-based DCF -- project revenue growth, converge margins to target (from mature industry peers), use sales-to-capital ratio for reinvestment, discount at WACC
- **Key inputs**: Current revenue, revenue growth trajectory, target operating margin (from mature peers), sales-to-capital ratio, failure probability
- **Adjustment**: Value = DCF value x (1 - P(failure)) + distress value x P(failure)
- **Typical companies**: Pre-profit SaaS, biotech pre-approval, marketplace platforms, early-stage tech

**Pattern 2: Distressed Firm**
- **When**: Firm value may be below face value of debt, significant probability of default
- **Approach**: Equity as a call option on the firm's assets using Black-Scholes. Equity holders have the right (not obligation) to pay off debt and claim residual value
- **Key inputs**: S = firm value (DCF of assets), K = face value of debt, t = weighted average debt maturity, sigma = std deviation of firm value, r = riskfree rate, y = cash flow yield
- **Adjustment**: Black-Scholes outputs equity value directly, incorporating default probability
- **Typical companies**: Highly leveraged firms, firms with negative book equity, companies in financial distress

**Pattern 3: Private Company**
- **When**: No public market for equity, typical in acquisitions, estate valuations, venture capital
- **Approach**: Standard DCF but with two modifications -- (a) total beta for undiversified owners, (b) liquidity discount for illiquid equity
- **Key inputs**: All standard DCF inputs plus owner diversification status, company size, profitability, industry
- **Adjustment**: Total beta = market beta / R (correlation with market); liquidity discount from restricted stock studies (10-35%)
- **Typical companies**: Family businesses, startups pre-IPO, professional practices, PE portfolio companies

**Pattern 4: Financial Services Firm**
- **When**: Banks, insurance companies, investment firms where debt is operational (deposits, insurance float, trading liabilities)
- **Approach**: Excess return model -- equity value = book value + PV of excess returns, where excess return = (ROE - cost of equity) x book value of equity
- **Key inputs**: Book value of equity, ROE (current and expected), cost of equity, expected growth in book equity, payout ratio
- **Adjustment**: Regulatory capital requirements constrain growth and payout; use equity models only (DDM or FCFE), never FCFF
- **Typical companies**: Commercial banks, investment banks, insurance companies, REITs, financial holding companies

## Guardrails

1. **Target margin sourcing**: For high-growth firms, target operating margin comes from mature industry peers, not from management projections or analyst optimism. Use the 25th-75th percentile range of mature companies in the same sector.

2. **Firm value volatility**: For the equity-as-call-option model, use asset-side volatility (firm value volatility), not equity volatility. Equity volatility overstates the underlying firm risk due to leverage amplification. Estimate from the unlevered firm or from comparable firms' asset volatility.

3. **Total beta applicability**: Total beta (market beta / correlation with market) applies only to undiversified owners who bear total risk. Diversified acquirers (PE funds, public companies) should use market beta. Specify the buyer context before choosing.

4. **Financial services debt treatment**: For banks and insurance companies, do not subtract debt from firm value to get equity value -- debt is operational, not financial. Use equity-only models (DDM, FCFE, or excess return model).

5. **Failure probability grounding**: Estimate failure probability from observable data -- cash burn rate vs. cash on hand, Altman Z-score, industry base failure rates, credit default swap spreads. Avoid round-number guesses without supporting evidence.

6. **Liquidity discount calibration**: The liquidity discount is not a flat percentage. It varies with company characteristics: larger, more profitable companies have smaller discounts. Use restricted stock study regression results that incorporate revenue, profitability, and block size as determinants.

7. **Transparency of adjustments**: Show the standard DCF value alongside the special-situation-adjusted value. This makes the magnitude and direction of each adjustment visible, and allows the reader to assess whether each adjustment is justified.

## Quick Reference

**Key formulas per sub-framework:**

```
HIGH-GROWTH (failure-adjusted value):
  Adjusted Value = DCF Value x (1 - P_failure) + Distress Value x P_failure
  Reinvestment = Change in Revenue / Sales-to-Capital Ratio
  Margin convergence: margin_t = current_margin + (target_margin - current_margin) x (t / T)

DISTRESSED (equity as call option):
  C = S x e^(-yt) x N(d1) - K x e^(-rt) x N(d2)
  d1 = [ln(S/K) + (r - y + sigma^2/2) x t] / (sigma x sqrt(t))
  d2 = d1 - sigma x sqrt(t)
  where S = firm value, K = face value of debt, t = debt maturity,
        sigma = firm value volatility, r = riskfree rate, y = cash flow yield

PRIVATE COMPANY:
  Total Beta = Market Beta / Correlation with Market
  Cost of Equity (undiversified) = Riskfree Rate + Total Beta x ERP
  Liquidity Discount: from restricted stock regression (f(revenue, profitability, block size))

FINANCIAL SERVICES (excess return model):
  Equity Value = BV_equity + sum[ (ROE_t - ke) x BV_equity_t / (1+ke)^t ] + Terminal
  Terminal = (ROE_stable - ke) x BV_equity_n+1 / ((ke - g) x (1+ke)^n)
  Growth in book equity = Retention Ratio x ROE
```

**Sub-framework selection decision tree:**

```
Is the firm a bank, insurer, or financial services company?
  Yes -> Pattern 4: Financial Services (excess return model)
  No  -> Does the firm have negative or near-zero operating income?
           Yes -> Pattern 1: High-Growth / Negative Earnings (revenue-based DCF)
           No  -> Is the firm facing significant distress or default risk?
                    Yes -> Pattern 2: Distressed (equity as call option)
                    No  -> Is the firm private (no public equity market)?
                             Yes -> Pattern 3: Private Company (total beta + liquidity discount)
                             No  -> Use standard DCF (intrinsic-valuation-dcf skill)
```

**Key resources:**

- **[resources/template.md](resources/template.md)**: Classification guide, templates for each situation type, standard vs adjusted comparison
- **[resources/methodology.md](resources/methodology.md)**: Revenue-based DCF, Black-Scholes for equity, total beta, liquidity discount, excess return model
- **[resources/evaluators/rubric_special_situations_valuation.json](resources/evaluators/rubric_special_situations_valuation.json)**: Quality criteria for situation classification, model selection, adjustments, and plausibility

**Cross-references to other skills:**

- `business-narrative-builder`: Life cycle stage determines which sub-framework applies
- `cost-of-capital-estimator`: Modified for private companies (total beta) and distressed firms
- `intrinsic-valuation-dcf`: Standard DCF for comparison; high-growth sub-framework builds on this
- `financial-statement-analyzer`: Provides cleaned base-year financials for all sub-frameworks

**Inputs required** (varies by situation type):

- **All**: Current financials, industry sector, company characteristics
- **High-growth**: Revenue, growth rate, mature peer margins, sales-to-capital, cash position, burn rate
- **Distressed**: Firm value estimate, face value of debt, debt maturity, firm value volatility
- **Private**: Standard DCF inputs + owner diversification status, company size, liquidity characteristics
- **Financial services**: Book value of equity, ROE, cost of equity, growth in book equity, payout ratio

**Outputs produced:**

- `special-situations-valuation.md`: Situation classification, sub-framework applied, model-specific adjustments, probability weighting or discounts, standard vs adjusted comparison, per-share value estimate
