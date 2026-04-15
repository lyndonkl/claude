# Capital Structure Optimizer Methodology

Detailed mechanics for the cost of capital approach, trade-off framework, debt type matching, and the APV alternative.

## Table of Contents
- [Unlevering Beta](#unlevering-beta)
- [Cost of Capital Approach](#cost-of-capital-approach)
- [Synthetic Rating Table](#synthetic-rating-table)
- [Interpreting the Optimal](#interpreting-the-optimal)
- [Trade-Off Framework](#trade-off-framework)
- [Debt Type Matching](#debt-type-matching)
- [APV Alternative](#apv-alternative)
- [Industry Debt Ratio Benchmarks](#industry-debt-ratio-benchmarks)

---

## Unlevering Beta

The unlevered beta isolates the business risk of the company, removing the financial risk introduced by leverage. It serves as the starting point for the WACC schedule: at each hypothetical debt ratio, the unlevered beta is relevered to determine the cost of equity at that level.

### From the Company's Own Beta

If the company has a regression beta (or a well-estimated bottom-up beta at its current capital structure):

```
Unlevered Beta = Current Levered Beta / (1 + (1 - t) x (D/E_current))
```

Where:
- t = marginal tax rate
- D/E_current = current debt-to-equity ratio using market values

**Example**: Levered beta 1.2, marginal tax rate 25%, D/E 0.40
- Unlevered beta = 1.2 / (1 + 0.75 x 0.40) = 1.2 / 1.30 = 0.923

### From Comparable Firms (Bottom-Up Approach)

When the company's own beta is unreliable (private company, recent IPO, conglomerate):

1. Select 5-10 comparable firms in the same business.
2. Obtain each comparable's levered beta, debt-to-equity ratio, and marginal tax rate.
3. Unlever each comparable's beta using the formula above.
4. Take the median (or revenue-weighted average) of unlevered betas.

**Advantages of bottom-up over regression beta**:
- Lower standard error (averaging across firms reduces noise)
- Reflects current business mix (not historical)
- Can be applied to any company, including private firms

### Relevering at Each Debt Ratio

For each row in the WACC schedule, relever the unlevered beta at the hypothetical D/E:

```
Levered Beta at target D/E = Unlevered Beta x (1 + (1 - t) x (D/E_target))
```

At D/E = 0 (all equity), levered beta equals unlevered beta.
As D/E increases, levered beta increases proportionally.

---

## Cost of Capital Approach

This is the primary methodology for finding the optimal capital structure. For each debt ratio from 0% to 90%, compute the WACC. The optimal is where WACC reaches its minimum.

### Step-by-Step for Each Debt Ratio

**Given**: Unlevered beta, riskfree rate (Rf), equity risk premium (ERP), EBIT, marginal tax rate (t), firm value estimate (V).

**For debt ratio D% (where D% = D / (D+E))**:

**Step 1: Compute D/E ratio**
```
D/E = D% / (1 - D%)
```

**Step 2: Relever beta**
```
Levered Beta = Unlevered Beta x (1 + (1 - t) x D/E)
```

**Step 3: Compute cost of equity**
```
ke = Rf + Levered Beta x ERP
```

**Step 4: Estimate dollar debt and interest expense**
```
Dollar Debt = D% x V
Interest Expense = Dollar Debt x (Rf + Default Spread)
```

Note: This creates a circularity because the default spread depends on the interest coverage, which depends on the interest expense, which depends on the dollar debt, which depends on the firm value, which depends on WACC. For a first pass, use the current firm value. Iterate if precision matters.

**Step 5: Compute interest coverage**
```
Interest Coverage = EBIT / Interest Expense
```

**Step 6: Look up synthetic rating**

Use the interest coverage ratio to determine the synthetic credit rating from the lookup table below.

**Step 7: Determine default spread**

The default spread corresponds to the synthetic rating. Use the appropriate column (large firm or small firm) from the table below.

**Step 8: Compute cost of debt**
```
Cost of Debt (pre-tax) = Rf + Default Spread
Cost of Debt (after-tax) = Cost of Debt (pre-tax) x (1 - t)
```

If the company has NOLs or is not currently paying taxes, the after-tax cost of debt equals the pre-tax cost (no tax shield until NOLs are exhausted).

**Step 9: Compute WACC**
```
WACC = ke x (1 - D%) + kd(1-t) x D%
```

**Step 10: Record and move to next debt ratio**

After computing all 10 rows, identify the minimum WACC.

### Handling the Tax Shield at High Debt Ratios

When debt is very high relative to EBIT, the company may not generate enough taxable income to fully use the tax deduction on interest. In this case:

- If Interest Expense > EBIT, the effective tax rate on the marginal debt is zero (no tax shield on excess interest)
- Compute the tax-deductible portion: min(Interest Expense, EBIT)
- After-tax cost of debt = pre-tax cost of debt - (tax rate x tax-deductible interest / total interest)

This refinement matters primarily at debt ratios above 60-70% and prevents the model from overstating the attractiveness of extreme leverage.

---

## Synthetic Rating Table

Map interest coverage ratio to credit rating and default spread. Use the large-firm column for companies with market cap above $5B and the small-firm column for companies below.

### Interest Coverage to Rating (Large Firms, Market Cap > $5B)

| Interest Coverage Range  | Synthetic Rating | Typical Default Spread |
|--------------------------|-----------------|------------------------|
| > 8.50                   | AAA             | 0.60%                 |
| 6.50 - 8.50             | AA              | 0.80%                 |
| 5.50 - 6.50             | A+              | 1.00%                 |
| 4.25 - 5.50             | A               | 1.10%                 |
| 3.00 - 4.25             | A-              | 1.25%                 |
| 2.50 - 3.00             | BBB             | 1.60%                 |
| 2.25 - 2.50             | BB+             | 2.00%                 |
| 2.00 - 2.25             | BB              | 2.50%                 |
| 1.75 - 2.00             | B+              | 3.25%                 |
| 1.50 - 1.75             | B               | 4.00%                 |
| 1.25 - 1.50             | B-              | 5.00%                 |
| 0.80 - 1.25             | CCC             | 6.50%                 |
| 0.65 - 0.80             | CC              | 8.00%                 |
| 0.20 - 0.65             | C               | 10.50%                |
| < 0.20                  | D               | 14.00%                |

### Interest Coverage to Rating (Small Firms, Market Cap < $5B)

| Interest Coverage Range  | Synthetic Rating | Typical Default Spread |
|--------------------------|-----------------|------------------------|
| > 12.50                  | AAA             | 0.60%                 |
| 9.50 - 12.50            | AA              | 0.80%                 |
| 7.50 - 9.50             | A+              | 1.00%                 |
| 6.00 - 7.50             | A               | 1.10%                 |
| 4.50 - 6.00             | A-              | 1.25%                 |
| 4.00 - 4.50             | BBB             | 1.60%                 |
| 3.50 - 4.00             | BB+             | 2.00%                 |
| 3.00 - 3.50             | BB              | 2.50%                 |
| 2.50 - 3.00             | B+              | 3.25%                 |
| 2.00 - 2.50             | B               | 4.00%                 |
| 1.50 - 2.00             | B-              | 5.00%                 |
| 1.25 - 1.50             | CCC             | 6.50%                 |
| 0.80 - 1.25             | CC              | 8.00%                 |
| 0.50 - 0.80             | C               | 10.50%                |
| < 0.50                  | D               | 14.00%                |

**Note**: These spreads reflect typical market conditions. In periods of credit stress, spreads widen across all ratings. In benign environments, spreads compress. The relative ordering and the general magnitude are more important than the exact basis points.

The synthetic rating table is also used by the `cost-of-capital-estimator` skill. If a more recent or company-specific spread schedule is available, use it in place of these defaults.

---

## Interpreting the Optimal

### Reading the WACC Schedule

The WACC schedule typically shows this pattern:
1. **All-equity (0% debt)**: WACC equals the unlevered cost of equity. No tax shield benefit.
2. **Low debt (10-30%)**: WACC declines as low-cost after-tax debt replaces expensive equity. Credit rating remains high, so default spreads are modest.
3. **Moderate debt (30-50%)**: WACC reaches its minimum. The tax shield benefit is maximized relative to the increasing cost of financial distress.
4. **High debt (50-70%)**: WACC begins to rise. The credit rating drops, default spreads increase rapidly, and the cost of equity rises as beta increases.
5. **Very high debt (70-90%)**: WACC rises steeply. The company is below investment grade, default spreads dominate, and the tax shield may be impaired (not enough taxable income).

### Flat vs Steep Minimums

- **Flat minimum** (WACC changes less than 20 bps across a 20 pp range): The company has significant flexibility in choosing its debt ratio. Minor deviations from optimal are not costly.
- **Steep minimum** (WACC changes more than 50 bps across a 10 pp range): The optimal is well-defined and deviations are costly. The company should move toward the optimal.

### When the Optimal is at 0% Debt

This occurs when:
- Tax rate is very low (tax shield minimal)
- Business is very volatile (distress costs rise quickly)
- The company has significant indirect bankruptcy costs

In this case, the recommendation is to carry minimal or no debt. This is common for young growth companies, biotech firms, and companies with high human capital dependence.

### Value Enhancement Calculation

```
Value Enhancement = V_optimal - V_current
                  = EBIT(1-t) / WACC_optimal - EBIT(1-t) / WACC_current
```

**Example**: EBIT = $300M, t = 25%, WACC_current = 8.65%, WACC_optimal = 8.56%
- V_current = $225M / 0.0865 = $2,601M
- V_optimal = $225M / 0.0856 = $2,628M
- Enhancement = $27M (about 1% of firm value)

As a rule of thumb, if value enhancement is less than 2% of firm value, the transaction costs and management attention required for restructuring may not be justified.

---

## Trade-Off Framework

The optimal capital structure balances the benefits and costs of debt.

### Benefits of Debt

**Tax shield**: Interest payments are tax-deductible, reducing the effective cost of debt. The annual tax saving = Interest Expense x Marginal Tax Rate. Higher marginal tax rates increase debt capacity.

**Discipline**: Fixed debt payments force management to generate cash flows. This can reduce wasteful spending ("free cash flow problem"). Most beneficial for mature companies with high free cash flows and limited growth opportunities.

**Signaling**: Issuing debt can signal management's confidence in future cash flows (willingness to commit to fixed payments). More relevant for information-opaque companies.

### Costs of Debt

**Expected bankruptcy costs**: As debt increases, the probability of financial distress rises. Bankruptcy costs include direct costs (legal fees, court costs, typically 2-5% of firm value) and indirect costs (loss of customers, employees, and suppliers; reduced investment; fire sale of assets).

**Agency costs**: Conflicts between debt holders and equity holders. Equity holders may take excessive risk (asset substitution), avoid positive-NPV projects if gains accrue to debt holders (debt overhang), or pay excessive dividends.

**Loss of flexibility**: Committed debt payments reduce financial flexibility. The company may be unable to invest in attractive projects if cash flows decline unexpectedly. Most costly for companies facing uncertain growth opportunities.

### Three Propositions for Debt Capacity

From Damodaran's framework:

1. **Higher marginal tax rate leads to more debt capacity**: The tax shield is more valuable when the tax rate is higher.
2. **More stable and predictable cash flows support more debt**: Companies with volatile EBIT face higher distress risk at any given debt level.
3. **Higher indirect bankruptcy costs reduce debt capacity**: Companies where customers, employees, or suppliers are sensitive to financial health (airlines, warranty providers, professional services) should carry less debt than a pure WACC minimization suggests.

---

## Debt Type Matching

After determining the optimal debt ratio, match the type of debt to the company's asset and cash flow characteristics.

### Maturity Matching

**Principle**: Debt maturity should approximate the life of the assets being financed.

| Asset Type                    | Typical Life | Debt Maturity Match        |
|-------------------------------|-------------|----------------------------|
| Working capital               | < 1 year    | Revolving credit facility  |
| Equipment / Vehicles          | 3-7 years   | Medium-term loans or notes |
| Real estate / Buildings       | 10-30 years | Long-term bonds or mortgages|
| Infrastructure / Utilities    | 20-40 years | Very long-term bonds       |
| Intangibles / Goodwill        | Indefinite  | Mix of maturities          |

**Why maturity matching matters**: If debt matures before the asset generates cash, the company faces refinancing risk. If debt maturity far exceeds asset life, the company pays for duration it does not need.

**Weighted average asset life**: Compute the weighted average useful life of the asset base to determine the target maturity profile. See the template for the calculation worksheet.

### Currency Matching

**Principle**: Denominate debt in the currencies that match revenue streams.

**Method**:
1. Identify revenue breakdown by currency (e.g., 70% USD, 20% EUR, 10% GBP).
2. Target a similar distribution for debt denomination.
3. Natural hedging: if costs are also in a specific currency, net the revenue against costs before determining the debt currency.

**Example**: A company earning 60% of revenue in USD and 40% in EUR should target approximately 60% USD-denominated debt and 40% EUR-denominated debt. This creates a natural hedge: if the EUR weakens, both revenue and debt service decline in USD terms.

**When perfect matching is impractical**: If debt markets in the revenue currency are illiquid or expensive, use synthetic hedging (currency swaps) to convert the economic exposure of debt issued in a different currency.

### Fixed vs Floating Rate Decision

**Principle**: Match rate structure to cash flow sensitivity.

| Cash Flow Profile              | Recommended Rate Structure     | Rationale                                    |
|-------------------------------|-------------------------------|----------------------------------------------|
| Stable, predictable           | Primarily fixed rate          | Lock in costs; cash flows can support fixed payments |
| Cyclical, tied to economy     | Primarily floating rate       | Interest costs decline when revenue declines  |
| Commodity-linked              | Floating (often tracks rates) | Commodity prices and rates often co-move      |
| High growth, variable         | Mix of fixed and floating     | Balance certainty and flexibility             |

**Interest rate environment consideration**: In a low-rate environment, locking in fixed rates provides protection against future increases. In a high-rate environment, floating rates allow the company to benefit if rates decline.

### Debt Instrument Selection

| Instrument       | Best For                                  | Advantages                      | Limitations                      |
|-----------------|-------------------------------------------|---------------------------------|----------------------------------|
| Corporate bonds | Large, rated companies                    | Lower cost, long maturities     | Public disclosure, covenants     |
| Bank term loans | Mid-size companies, relationship banking  | Flexible terms, renegotiable    | Shorter maturity, variable rate  |
| Revolving credit| Working capital needs                     | Draw as needed, pay down        | Higher spread, commitment fees   |
| Private placement| Companies avoiding public markets         | Less disclosure, customizable   | Higher rate, limited size        |
| Convertible debt| Growth companies                          | Lower coupon, equity upside     | Dilution risk, complexity        |

---

## APV Alternative

The Adjusted Present Value (APV) approach provides an alternative to the WACC method for valuing the effect of capital structure changes. It is conceptually cleaner because it separates operating value from financing effects.

### APV Formula

```
Firm Value (APV) = Unlevered Firm Value + PV of Tax Shield - PV of Bankruptcy Costs
```

Where:
- **Unlevered Firm Value** = FCFF discounted at unlevered cost of equity (as if all-equity financed)
- **PV of Tax Shield** = Present value of interest tax deductions
- **PV of Bankruptcy Costs** = Probability of distress x Cost of distress

### When to Use APV Instead of WACC

- When the capital structure is changing over time (WACC assumes a constant D/E ratio)
- When the company is highly leveraged and may not fully use the tax shield
- When explicitly modeling the probability of distress is important (e.g., LBO analysis)
- When there are significant non-debt tax shields (NOLs, investment tax credits)

### APV Computation Steps

1. **Value the unlevered firm**: Discount FCFF at the unlevered cost of equity (Rf + Unlevered Beta x ERP).
2. **Value the tax shield**: If debt is permanent, PV of tax shield = t x D. If debt is time-limited, discount annual tax savings (Interest x t) at the cost of debt.
3. **Value the expected bankruptcy costs**: Estimate probability of distress (from bond rating or Altman Z-score) and multiply by estimated bankruptcy costs (10-25% of firm value for direct + indirect).
4. **Sum the components**: APV = Unlevered value + Tax shield - Expected bankruptcy costs.

### Comparing APV and WACC Results

Both methods should give the same answer at any given capital structure if assumptions are consistent. Discrepancies typically arise from:
- WACC assumes a fixed target debt ratio; APV allows the debt level to change.
- WACC bakes the tax shield into the discount rate; APV values it separately.
- APV makes bankruptcy cost assumptions explicit; WACC embeds them implicitly through the credit spread.

For most capital structure optimization exercises, the WACC approach (cost of capital approach) is more practical and is the primary methodology in this skill. Use APV as a cross-check or when the capital structure is expected to change materially over the projection period.

---

## Industry Debt Ratio Benchmarks

Typical debt-to-capital ratios by industry sector (based on market values). These serve as reasonableness checks for the computed optimal.

| Industry Sector              | Median Debt/Capital | Typical Range  | Key Drivers                           |
|------------------------------|---------------------|----------------|---------------------------------------|
| Technology (Software)        | 5-15%               | 0-25%          | Low tangible assets, high growth      |
| Technology (Hardware)        | 10-25%              | 5-35%          | Moderate tangible assets              |
| Pharmaceuticals              | 10-20%              | 0-30%          | High R&D, uncertain cash flows        |
| Consumer Staples             | 25-35%              | 15-45%         | Stable demand, predictable cash flows |
| Industrials / Manufacturing  | 20-35%              | 10-45%         | Tangible assets, moderate cyclicality |
| Utilities                    | 40-55%              | 30-65%         | Regulated, very stable cash flows     |
| Telecommunications           | 35-50%              | 25-60%         | Large infrastructure, stable revenue  |
| Real Estate (REITs)          | 35-50%              | 25-60%         | Asset-backed, tax-advantaged          |
| Retail                       | 20-35%              | 10-45%         | Working capital heavy, cyclical       |
| Airlines                     | 40-60%              | 30-70%         | Capital-intensive, lease-heavy        |
| Oil and Gas                  | 15-30%              | 5-45%          | Commodity volatility, asset-backed    |
| Financial Services           | N/A (debt is ops)   | N/A            | Debt is operating, not financial      |

**Important**: These are central tendencies. Individual companies deviate based on their specific growth profile, profitability, tax position, and strategic choices. The optimal for a specific company may reasonably differ from the sector median by 10-15 percentage points.

Financial services firms (banks, insurance, asset managers) use debt as a raw material, not as a financing choice. Capital structure optimization for these firms focuses on equity capital adequacy, not debt-equity trade-offs. This skill is not intended for financial services firms; see `special-situations-valuation` for bank and insurance valuation.
