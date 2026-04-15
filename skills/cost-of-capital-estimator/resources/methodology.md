# Cost of Capital Estimation Methodology

Detailed procedures, formulas, and reference tables for computing the cost of equity, cost of debt, and WACC.

## Table of Contents
- [Riskfree Rate Derivation](#riskfree-rate-derivation)
- [Four-Step ERP Procedure](#four-step-erp-procedure)
- [Country Risk Premium Approaches](#country-risk-premium-approaches)
- [Bottom-Up Beta Estimation](#bottom-up-beta-estimation)
- [Synthetic Rating Table](#synthetic-rating-table)
- [Special Cases](#special-cases)

---

## Riskfree Rate Derivation

The riskfree rate is the foundation of every cost of capital computation. It represents the return on an investment with zero default risk and zero reinvestment risk.

### Requirements for a Riskfree Rate

1. No default risk -- the entity issuing the security should have no chance of default.
2. No reinvestment risk -- there should be no uncertainty about reinvestment rates. In practice, this means matching the bond duration to the cash flow duration.
3. Currency match -- the riskfree rate should be in the same currency as the cash flows being discounted.

### Method A: Local Government Bond Minus Sovereign Default Spread

Use this when the country has a liquid, long-term government bond market.

```
Riskfree Rate (local currency) = Local Government Bond Yield - Sovereign Default Spread
```

The sovereign default spread is derived from the country's Moody's (or equivalent) credit rating. For example:
- Baa2 sovereign rating corresponds to approximately 2.0-2.5% default spread.
- Ba1 sovereign rating corresponds to approximately 3.0-3.5% default spread.

This method assumes the local bond yield is composed of: true riskfree rate + default premium + expected inflation.

### Method B: Inflation Differential from US Riskfree Rate

Use this when local government bonds are illiquid, unavailable, or the sovereign default spread is uncertain.

```
Riskfree Rate (local) = (1 + US Riskfree Rate) x (1 + Expected Inflation_local) / (1 + Expected Inflation_US) - 1
```

Example: US 10-year = 4%, India expected inflation = 5%, US expected inflation = 2%.
Riskfree rate in INR = (1.04)(1.05)/(1.02) - 1 = 7.06%.

### When to Use Each Method

| Situation | Recommended Method |
|-----------|-------------------|
| Developed market (US, Germany, Japan) | Government bond yield directly (it is the riskfree rate) |
| Emerging market with rated sovereign debt | Method A: Local bond minus default spread |
| Country with thin or unreliable bond market | Method B: Inflation differential |
| Cross-check for any emerging market | Compute both, they should be within 50bps |

### Common Pitfall: Using a Defaultable Bond as Riskfree

Many emerging market government bonds carry default risk. Using the raw yield as the riskfree rate overstates the true riskfree rate and then understates the equity risk premium when it is added back.

---

## Four-Step ERP Procedure

This procedure follows Damodaran's framework for estimating the equity risk premium for any country.

### Step 1: Estimate the Implied ERP for the S&P 500

The implied ERP is the premium that makes the present value of expected cash flows on the S&P 500 equal to its current level. It is forward-looking and market-derived.

Procedure:
1. Take the current S&P 500 level and the aggregate dividends + buybacks (total cash yield).
2. Project cash flows growing at consensus earnings growth for the next 5 years, then at the riskfree rate in perpetuity.
3. Solve for the discount rate that makes PV of cash flows = current index level.
4. Implied ERP = Solved discount rate - Riskfree rate.

The implied ERP for the S&P 500 historically ranges from 4% to 6%. Damodaran publishes an updated estimate annually on his website.

Why implied over historical: Historical ERPs vary from 3% to 8% depending on whether you use arithmetic vs. geometric returns, the time period (1928-present vs. 1960-present), and T-bills vs. T-bonds as the riskfree benchmark. The implied ERP eliminates these choices by being derived from current market prices.

### Step 2: Assess Sovereign Country Risk via Credit Rating

For the country or countries where the company operates, obtain the sovereign credit rating from Moody's (or S&P equivalent).

Map the rating to a sovereign default spread:

| Moody's Rating | S&P Equivalent | Sovereign Default Spread |
|---------------|----------------|------------------------|
| Aaa | AAA | 0.00% |
| Aa1 | AA+ | 0.40% |
| Aa2 | AA | 0.50% |
| Aa3 | AA- | 0.60% |
| A1 | A+ | 0.75% |
| A2 | A | 0.85% |
| A3 | A- | 1.00% |
| Baa1 | BBB+ | 1.50% |
| Baa2 | BBB | 2.00% |
| Baa3 | BBB- | 2.50% |
| Ba1 | BB+ | 3.00% |
| Ba2 | BB | 3.50% |
| Ba3 | BB- | 4.00% |
| B1 | B+ | 5.00% |
| B2 | B | 6.00% |
| B3 | B- | 7.00% |
| Caa1 | CCC+ | 8.50% |
| Caa2 | CCC | 10.00% |
| Caa3 | CCC- | 12.00% |

These spreads are approximate and should be updated with current market data when available. Use CDS spreads as an alternative market-based measure.

### Step 3: Convert Sovereign Risk to Equity Risk Premium

Equity markets are more volatile than bond markets. To convert a bond-based default spread into an additional equity risk premium, multiply by the relative volatility:

```
Country Equity Risk Premium = Sovereign Default Spread x (Std Dev of Country Equity Index / Std Dev of Country Bond)
```

The equity/bond volatility ratio is typically between 1.3x and 1.7x. When country-specific data is unavailable, use 1.5x as a default.

Example: Brazil sovereign default spread = 2.5%, equity/bond volatility ratio = 1.5.
Brazil Country ERP = 2.5% x 1.5 = 3.75%.

### Step 4: Compute Total ERP for the Country

```
Total ERP for Country = Mature Market Implied ERP + Country Equity Risk Premium
```

Example: Implied S&P 500 ERP = 5.0%, Brazil Country ERP = 3.75%.
Total ERP for Brazil = 5.0% + 3.75% = 8.75%.

For a company operating across multiple countries, compute a blended ERP using the country risk premium approaches described in the next section.

---

## Country Risk Premium Approaches

A company's exposure to country risk depends on where it does business, not just where it is incorporated. Three approaches measure this exposure.

### Approach 1: Location-Based (Simplest)

Assign the full country risk premium of the country of incorporation to the company.

```
CRP = Country ERP of incorporation country
```

**Pros**: Simple, no data required beyond country of incorporation.
**Cons**: Ignores that many companies earn revenue globally. A Brazilian company with 80% US revenue faces less Brazilian country risk than a purely domestic Brazilian firm.

Use this as a quick first pass or when geographic revenue data is unavailable.

### Approach 2: Operation-Based Revenue Weighting (Recommended)

Weight the country risk premium by the proportion of revenue earned in each country or region.

```
Operation-weighted CRP = Sum of (Revenue_i% x CRP_i) for each country i
```

Example for Ambev:
- Brazil (60% revenue): CRP = 3.75% -> 0.60 x 3.75% = 2.25%
- Other LatAm (30% revenue): CRP = 3.00% -> 0.30 x 3.00% = 0.90%
- US (10% revenue): CRP = 0% -> 0.10 x 0% = 0.00%
- Total operation-weighted CRP = 3.15%

**Pros**: Reflects actual risk exposure, straightforward to compute from annual report geographic segments.
**Cons**: Revenue may not perfectly capture risk (e.g., a company may face supply chain risk in a country where it has production but no revenue).

### Approach 3: Lambda-Based (Most Precise)

Estimate a company-specific lambda that measures its sensitivity to country risk, analogous to how beta measures market risk sensitivity.

```
Cost of Equity = Riskfree Rate + Beta x Mature ERP + Lambda x CRP
```

Lambda can be estimated from a regression of the company's returns against a country risk index, or approximated using the ratio of the company's revenue from the country to the average company's revenue from that country.

In practice, lambda is difficult to estimate reliably. The operation-based approach (Approach 2) is recommended for most analyses.

---

## Bottom-Up Beta Estimation

Bottom-up betas are preferred over regression betas for three reasons:
1. **Lower standard error**: Averaging across 15-20 firms reduces noise.
2. **Forward-looking**: Reflects the current industry risk, not the historical average.
3. **Allows capital structure targeting**: You relever at the desired or current D/E, not the historical average.

### Procedure

**Step 1: Select comparable firms**

Identify 15-20 publicly traded firms in the same industry as the target company. "Same industry" means similar products/services and similar risk profile, not necessarily the same country.

For a multi-business company, select comparables for each business segment separately.

**Step 2: Collect levered betas and capital structure for each comparable**

For each firm, obtain:
- Equity beta (from a regression of stock returns against market returns, typically 2-5 years of weekly or monthly data)
- Market D/E ratio (market cap for equity, book or market value for debt)
- Marginal tax rate

**Step 3: Unlever each beta**

```
Unlevered Beta = Levered Beta / (1 + (1 - Tax Rate) x (D/E))
```

This formula (the Hamada equation) assumes debt is riskless and the tax benefit of debt is proportional to the amount of debt. For firms with very high leverage or risky debt, a more general form exists:

```
Unlevered Beta = (Levered Beta + Beta_debt x (1-t) x (D/E)) / (1 + (1-t) x (D/E))
```

In most cases, Beta_debt is assumed to be zero (or close to it), simplifying to the standard formula.

**Step 4: Compute the median unlevered beta**

Use the median (not the mean) to reduce the influence of outliers. If the sample is large enough (20+), the mean and median should be close.

| Statistic | Value |
|-----------|-------|
| Number of firms | ___ |
| Median unlevered beta | ___ |
| Mean unlevered beta | ___ |
| Std deviation | ___ |

**Step 5: Relever at the target company's capital structure**

```
Levered Beta = Unlevered Beta x (1 + (1 - Tax Rate) x (D/E))
```

Use the target company's current market D/E ratio and marginal tax rate. If the company plans to change its capital structure, use the target D/E.

### Multi-Business Companies

For conglomerates or diversified firms:

1. Identify comparable firms for each business segment.
2. Compute the unlevered beta for each segment.
3. Weight by the proportion of firm value (or revenue, if value is unknown) in each segment.
4. The weighted average unlevered beta becomes the firm's unlevered beta.
5. Relever at the firm's overall capital structure.

```
Firm Unlevered Beta = Sum of (Segment_i Value Weight x Segment_i Unlevered Beta)
```

---

## Synthetic Rating Table

When a company does not have a public credit rating (most private firms, many smaller public firms), estimate a synthetic rating from the interest coverage ratio. The interest coverage ratio is the single best predictor of credit ratings.

```
Interest Coverage Ratio = EBIT / Interest Expense
```

### Large Firms (Revenue > $5B)

| Interest Coverage | Rating | Default Spread |
|------------------|--------|---------------|
| > 12.5 | AAA | 0.40% |
| 9.50 - 12.50 | AA | 0.70% |
| 7.50 - 9.50 | A+ | 0.85% |
| 6.00 - 7.50 | A | 1.00% |
| 4.50 - 6.00 | A- | 1.20% |
| 4.00 - 4.50 | BBB | 1.60% |
| 3.50 - 4.00 | BB+ | 2.00% |
| 3.00 - 3.50 | BB | 2.50% |
| 2.50 - 3.00 | BB- | 3.00% |
| 2.00 - 2.50 | B+ | 3.75% |
| 1.50 - 2.00 | B | 5.00% |
| 1.25 - 1.50 | B- | 6.00% |
| 0.80 - 1.25 | CCC | 8.00% |
| 0.50 - 0.80 | CC | 10.00% |
| < 0.50 | C/D | 12.00% |

### Small Firms (Revenue < $5B)

Small firms face tighter thresholds because their cash flows are less diversified and more volatile.

| Interest Coverage | Rating | Default Spread |
|------------------|--------|---------------|
| > 12.5 | AAA | 0.40% |
| 9.50 - 12.50 | AA | 0.70% |
| 7.50 - 9.50 | A+ | 0.85% |
| 6.00 - 7.50 | A | 1.00% |
| 4.50 - 6.00 | A- | 1.20% |
| 3.50 - 4.50 | BBB | 1.75% |
| 2.50 - 3.50 | BB | 3.00% |
| 2.00 - 2.50 | B+ | 4.00% |
| 1.50 - 2.00 | B | 5.50% |
| 1.00 - 1.50 | B- | 6.50% |
| 0.80 - 1.00 | CCC | 8.50% |
| 0.50 - 0.80 | CC | 11.00% |
| < 0.50 | C/D | 13.50% |

### Notes on Using the Synthetic Rating Table

1. **EBIT should be normalized**: If the current year EBIT is unusually high or low (one-time gains/losses, cyclical peak/trough), use a normalized EBIT that reflects sustainable operating income.

2. **If interest expense is zero**: The company has no debt. Assign the highest rating (AAA). When computing the WACC sensitivity table across debt ratios, estimate interest expense at each level as: Interest = Debt x Pre-tax cost of debt.

3. **Cross-check with actual rating**: If the company has a public credit rating from Moody's or S&P, compare it to the synthetic rating. They should be within 1-2 notches. Significant divergence may indicate factors the interest coverage ratio does not capture (e.g., pending litigation, industry headwinds, governance concerns).

4. **Updating default spreads**: The default spreads in this table are baseline estimates. For current spreads, consult market data on corporate bond yields by rating. The spread over the riskfree rate (not the spread over Treasuries, which may include a liquidity premium) is what matters.

---

## Special Cases

### Negative Operating Income

If EBIT is negative, the interest coverage ratio is negative. In this case:
- Assign a CCC or lower rating (high default risk).
- Consider whether the firm is temporarily or permanently in distress.
- For young growth companies burning cash by choice (investing in growth), the cost of capital should reflect the business risk of the target state, not current distress. Use the industry average unlevered beta and a low debt ratio.

### No Debt

If the company has zero debt:
- Levered beta = Unlevered beta (D/E = 0).
- WACC = Cost of equity (100% equity-funded).
- No cost of debt computation needed.
- Sensitivity table still useful to show what WACC would be at different leverage levels.

### Financial Services Firms

Banks and insurance companies use debt as operational raw material, not as financing. Standard WACC analysis does not apply.

- Use cost of equity only (not WACC) to discount cash flows to equity (FCFE or dividends).
- Beta should reflect the equity risk of the financial institution.
- Do not separate operating and financing debt; all debt is operational.
- The excess return model (value = book equity + PV of (ROE - ke) x book equity) is the standard approach. This is covered in detail in the special-situations-valuation skill.

### Currency Conversion of WACC

If cash flows and WACC are in different currencies, convert the WACC using the inflation differential:

```
WACC_local = (1 + WACC_USD) x (1 + Inflation_local) / (1 + Inflation_USD) - 1
```

This preserves the real cost of capital while adjusting for the nominal currency denomination. The resulting valuation should be identical regardless of which currency is used, as long as cash flows and discount rates are in the same currency.
