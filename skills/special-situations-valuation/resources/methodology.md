# Special Situations Valuation Methodology

Detailed formulas, derivations, and step-by-step procedures for each of the four sub-frameworks.

## Table of Contents
- [1. High-Growth Firms with Negative Earnings](#1-high-growth-firms-with-negative-earnings)
- [2. Distressed Firms: Equity as Call Option](#2-distressed-firms-equity-as-call-option)
- [3. Private Companies](#3-private-companies)
- [4. Financial Services Firms](#4-financial-services-firms)
- [5. Cross-Cutting Techniques](#5-cross-cutting-techniques)

---

## 1. High-Growth Firms with Negative Earnings

### The Problem

Standard DCF requires positive base-year cash flows to project forward. When operating income is negative, the typical approach of applying a growth rate to current earnings produces meaningless results (growing a negative number makes it more negative). The solution is to start from revenue and project a path to profitability.

### Revenue-Based DCF: Step by Step

**Step 1: Establish current revenue and growth trajectory**

Start with trailing twelve-month revenue. Project revenue growth using one of:
- Historical revenue CAGR, adjusted for maturation (growth rate should decline as revenue base grows)
- TAM-based approach: target market share x market size, solved backward for implied CAGR
- Analyst consensus as a cross-check (not as the primary input)

Revenue growth should decline over time. A typical pattern:
- Years 1-3: Current high growth rate (30-50%)
- Years 4-6: Decelerating (15-25%)
- Years 7-10: Approaching stable growth (5-10%)
- Terminal: Risk-free rate or GDP growth (2-4%)

**Step 2: Set target operating margin from mature peers**

The critical assumption. Target margin should come from:
1. Identify 5-10 mature companies in the same industry
2. Compute their operating margins
3. Use the 25th-75th percentile range as the plausible target
4. Select a point estimate with justification (e.g., median if the company has average competitive position)

Do not use management guidance or "industry potential" -- use observed margins from companies that have already matured.

**Step 3: Define the margin convergence path**

Operating margin converges from current (negative) to target over the growth period:

```
Margin_t = Current_Margin + (Target_Margin - Current_Margin) x (t / T)
```

Where T = number of years to reach target margin. Linear convergence is the default. Use front-loaded convergence if the company has already demonstrated improving margins, or back-loaded if the company is still investing heavily.

**Step 4: Compute reinvestment using sales-to-capital ratio**

Instead of estimating CapEx and working capital separately (difficult for negative-earnings firms), use:

```
Reinvestment_t = Change_in_Revenue_t / Sales_to_Capital_Ratio
```

The sales-to-capital ratio represents how much revenue each dollar of invested capital generates. Estimate from:
- Company's own historical ratio (revenue change / capital change over trailing 3 years)
- Industry median for comparable companies
- Typical range: 1.0-3.0 (higher for asset-light businesses like SaaS, lower for capital-intensive)

**Step 5: Compute FCFF year by year**

```
Revenue_t = Revenue_(t-1) x (1 + g_t)
EBIT_t = Revenue_t x Margin_t
After_tax_EBIT_t = EBIT_t x (1 - Tax_Rate)
Reinvestment_t = (Revenue_t - Revenue_(t-1)) / Sales_to_Capital
FCFF_t = After_tax_EBIT_t - Reinvestment_t
```

Note: For years where EBIT is negative, the tax rate effect is zero (no tax benefit assumed unless the company has NOL carryforwards). If NOLs exist, they shelter future income -- the effective tax rate is zero until NOLs are exhausted, then rises to marginal rate.

**Step 6: Compute terminal value**

At the end of the projection period, the company should be at stable growth:

```
Terminal_Value = FCFF_(n+1) / (WACC_stable - g_stable)
```

Where:
- FCFF_(n+1) = stable-year after-tax operating income x (1 - reinvestment rate)
- Reinvestment rate in stable period = g_stable / ROC_stable
- WACC_stable converges toward mature company levels (typically lower than current WACC)
- g_stable is constrained to the risk-free rate or nominal GDP growth

**Step 7: Apply failure probability adjustment**

```
Adjusted_Value = DCF_Value x (1 - P_failure) + Distress_Value x P_failure
```

Estimate P_failure from:
- **Cash runway**: Cash / Annual Burn Rate. If < 2 years and no clear path to profitability, failure probability is substantial (20-40%)
- **Industry base rates**: Historical failure rates for companies at similar stage and sector
- **Altman Z-score**: If applicable (more suited to manufacturing firms)
- **Market signals**: CDS spreads, bond yields, credit rating

Estimate distress value from:
- Liquidation value of tangible assets
- Sale value of IP, customer base, or brand (if any)
- Typically 10-30% of going-concern DCF value for young tech firms

---

## 2. Distressed Firms: Equity as Call Option

### The Intuition

In a distressed firm, equity holders have limited liability. If firm value exceeds debt at maturity, equity holders pay off debt and keep the residual. If firm value falls below debt, equity holders walk away and lose nothing more than their investment. This payoff structure -- upside participation with downside protection -- is identical to a call option.

### Black-Scholes Applied to Equity

The equity of a levered firm is a call option on the firm's assets:

```
C = S x e^(-yt) x N(d1) - K x e^(-rt) x N(d2)

d1 = [ln(S/K) + (r - y + sigma^2 / 2) x t] / (sigma x sqrt(t))
d2 = d1 - sigma x sqrt(t)
```

**Variable mapping**:

| Option Variable | Firm Equivalent | How to Estimate |
|----------------|-----------------|-----------------|
| S (stock price) | Value of the firm (assets) | DCF of operating assets or asset-based valuation |
| K (strike price) | Face value of all debt | Sum of all debt obligations (book value) |
| t (time to expiration) | Weighted average debt maturity | Duration-weighted average of debt maturities |
| r (riskfree rate) | Riskfree rate | Treasury rate matching maturity t |
| sigma (volatility) | Std deviation of firm value | See estimation approaches below |
| y (dividend yield) | Cash flow yield | Annual FCFF / Firm Value |

### Estimating Firm Value Volatility

This is the most challenging input. Three approaches:

**Approach A: De-lever equity volatility**

```
Sigma_firm = Sigma_equity x (E / (D + E)) + Sigma_debt x (D / (D + E))
```

Where Sigma_equity is observed from stock price returns, and Sigma_debt is estimated from bond return volatility or credit spread volatility. This approach works when both equity and debt are traded.

**Approach B: Comparable firm asset volatility**

Use unlevered equity volatility of comparable non-distressed firms in the same industry:

```
Sigma_firm_unlevered = Sigma_equity_comparable x (E / (D + E))_comparable
```

Average across 5-10 comparable firms. This avoids the problem that the distressed firm's own equity volatility is amplified by leverage.

**Approach C: Operating income volatility**

Estimate the standard deviation of the firm's operating income over 5-10 years, then scale:

```
Sigma_firm ≈ Coefficient_of_Variation(EBIT) x (1 + D/E)^(-1)
```

This approach is rougher but useful when market data is unavailable.

### Interpretation of Results

- **N(d2)** = risk-neutral probability that firm value exceeds debt at maturity (probability of solvency)
- **1 - N(d2)** = probability of default
- If firm value << debt (deeply distressed), equity may still have value because of volatility and time
- Higher volatility increases equity value (more upside potential), even though it increases default risk
- Longer debt maturity increases equity value (more time for recovery)

### Limitations

- Assumes a single debt maturity (real firms have multiple tranches with different maturities)
- Does not account for debt covenants that may force earlier liquidation
- Black-Scholes assumes log-normal distribution of firm value (may underestimate tail risk)
- Firm value itself must be estimated, introducing circularity

---

## 3. Private Companies

### Two Key Adjustments

Private companies differ from public companies in two ways that affect valuation:
1. **Risk**: If the owner is undiversified, they bear total risk (not just market risk)
2. **Liquidity**: There is no ready market to sell shares, creating a liquidity cost

### Total Beta for Undiversified Owners

In CAPM, beta measures only systematic (market) risk because diversified investors can eliminate unsystematic risk. An undiversified owner cannot diversify, so they bear the total risk of the firm.

```
Total Beta = Market Beta / Correlation with Market

Where:
  Market Beta = from regression of comparable public firm returns on market returns
  Correlation = R (not R-squared) from that regression
  R = sqrt(R-squared)
```

**Example**:
- Comparable public firm beta: 1.2
- R-squared from regression: 0.25
- Correlation R: sqrt(0.25) = 0.50
- Total beta: 1.2 / 0.50 = 2.40

**Cost of equity comparison**:
- Diversified owner: ke = 4% + 1.2 x 5.5% = 10.6%
- Undiversified owner: ke = 4% + 2.4 x 5.5% = 17.2%

**When to use total beta**:
- Sole proprietor whose wealth is concentrated in the business
- Family business where owners have limited outside investments
- Startup founder with majority of net worth in the company

**When to use market beta**:
- Private equity fund with diversified portfolio of companies
- Public company acquiring a private target
- Venture capital fund

### Liquidity Discount

Private company shares cannot be sold quickly or cheaply. This illiquidity warrants a discount from the value computed using public market assumptions.

**Sources for estimating the discount**:

**Restricted stock studies**: Compare prices of restricted (unregistered) shares to freely traded shares of the same company. Key findings:
- Average discount: 20-25% (varies significantly)
- Discount varies with company characteristics:
  - Larger revenue -> smaller discount (more information, more potential buyers)
  - Higher profitability -> smaller discount
  - Larger block size -> larger discount (harder to sell large block)

**Regression approach** (preferred over flat discount):

```
Liquidity_Discount = a - b1 x ln(Revenue) - b2 x (Dummy: Positive_Earnings) + b3 x (Block_Size%)
```

Typical coefficients from restricted stock research:
- Base discount: ~30-35%
- Revenue effect: -2% to -4% per doubling of revenue
- Profitability effect: -5% to -8% if earnings are positive
- Block size effect: +1% to +2% per 10% increase in block size

**Bid-ask spread approach**: Use the bid-ask spread as a measure of liquidity cost. For private firms, estimate the implicit spread from transaction frequency and information asymmetry.

### Minority Discount (If Applicable)

If valuing a minority stake without control:
- Minority shareholders cannot set dividends, strategy, or capital allocation
- Minority discount typically 15-25% (depends on governance protections)
- Do not double-count: if using DCF that already reflects current management decisions (which minority holders cannot change), a minority discount may be appropriate
- If acquirer will gain control, no minority discount

### Private Company Valuation Sequence

1. Run standard DCF using market beta (as if the firm were public)
2. If owner is undiversified, re-run DCF with total beta -> higher cost of equity -> lower value
3. Apply liquidity discount (10-35% based on company characteristics)
4. If valuing minority stake, apply minority discount (15-25%)
5. Final value = DCF value (at total beta) x (1 - liquidity discount) x (1 - minority discount)

---

## 4. Financial Services Firms

### Why Standard DCF Fails

For banks and insurance companies:
- **Debt is operational**: Deposits and insurance reserves are raw materials, not financing. Subtracting debt from firm value would destroy the valuation.
- **Capital expenditure is ambiguous**: Banks invest in loans, not factories. Traditional CapEx and working capital definitions do not apply.
- **Regulation constrains capital**: Regulatory capital requirements (Basel III, Solvency II) limit how much a bank can pay out or grow.

### The Excess Return Model

Value equity directly as:

```
Equity Value = Book Value of Equity + PV of Future Excess Returns

Excess Return in year t = (ROE_t - ke) x Book Value of Equity_(t-1)
```

**Intuition**: If a bank earns ROE of 15% and its cost of equity is 10%, the excess return is 5% of book equity each year. The present value of these excess returns, plus book value, equals the fair value of equity.

### Step-by-Step Procedure

**Step 1: Determine current book value of equity**

Use the latest balance sheet. For banks, book value is meaningful because assets (loans, securities) are marked to market or carried at amortized cost. Book value of equity = Total Assets - Total Liabilities.

**Step 2: Estimate ROE**

- Current ROE = Net Income / Average Book Equity
- Normalize for one-time items (loan loss provisions in recession years, trading gains/losses)
- Project ROE for high-growth period and stable period
- ROE should converge toward cost of equity over time as competitive advantages erode (unless the bank has a durable franchise)

**Step 3: Estimate cost of equity**

Use CAPM: ke = Riskfree Rate + Beta x ERP

For financial services firms:
- Beta: Use bottom-up beta from comparable financial firms (regression betas are volatile for financials)
- Typical bank betas: 0.8-1.2 (developed market), higher for investment banks and emerging markets
- Do not compute WACC -- use cost of equity only

**Step 4: Estimate growth in book equity**

```
Growth in Book Equity = Retention Ratio x ROE
Retention Ratio = 1 - Payout Ratio
Payout Ratio = (Dividends + Buybacks) / Net Income
```

**Regulatory constraint**: Growth in book equity is limited by the need to maintain capital ratios:

```
Maximum Sustainable Growth = ROE x (1 - Minimum_Payout)
Minimum_Payout = 1 - (Required_Capital_Ratio_Increase / ROE)
```

If the bank needs to build capital (e.g., to meet Basel III buffers), payout falls and growth in book equity is constrained.

**Step 5: Project excess returns**

For each year of the high-growth period:

```
BV_Equity_t = BV_Equity_(t-1) x (1 + g)
Net_Income_t = ROE_t x BV_Equity_(t-1)
Cost_of_Equity_t = ke x BV_Equity_(t-1)
Excess_Return_t = Net_Income_t - Cost_of_Equity_t = (ROE_t - ke) x BV_Equity_(t-1)
```

**Step 6: Compute terminal value**

In stable growth:

```
Terminal_Excess_Return = (ROE_stable - ke_stable) x BV_Equity_n
Terminal_Value = Terminal_Excess_Return / (ke_stable - g_stable)
```

Where g_stable is the stable growth rate in book equity (constrained by GDP growth and capital requirements).

**Step 7: Sum to get equity value**

```
Equity Value = BV_Equity_0 + sum[PV(Excess_Return_t)] + PV(Terminal_Value)
```

### Price-to-Book Interpretation

The excess return model directly implies a price-to-book ratio:

```
P/BV = 1 + PV(Excess Returns) / BV_Equity
```

- ROE > ke -> P/BV > 1 (bank earns more than its cost of equity, deserves premium)
- ROE = ke -> P/BV = 1 (bank earns exactly its cost of equity, worth book value)
- ROE < ke -> P/BV < 1 (bank destroys value, worth less than book value)

### Alternative: Dividend Discount Model for Banks

If preferred over the excess return model:

```
Value = sum[Expected_DPS_t / (1 + ke)^t] + Terminal_Value / (1 + ke)^n
Terminal_Value = DPS_(n+1) / (ke - g_stable)
Expected_DPS = Net_Income x Payout_Ratio
```

DDM works well for banks because:
- Dividends are well-defined and observable
- Regulatory requirements constrain payout ratios, making forecasting more predictable
- Reinvestment in a bank (making loans) is hard to separate from operations

---

## 5. Cross-Cutting Techniques

### NOL (Net Operating Loss) Carryforward Treatment

For high-growth firms with accumulated losses:

1. Calculate cumulative NOLs from prior years
2. In projection years where EBIT turns positive, set effective tax rate to 0% until NOLs are exhausted
3. Once NOLs are fully used, tax rate jumps to marginal rate
4. The value of NOLs is captured automatically in higher after-tax cash flows during the sheltered years

### Sensitivity Analysis for Special Situations

Special-situation valuations are highly sensitive to key assumptions. Run sensitivity on:

**High-growth**: Target operating margin (+/- 3 percentage points), failure probability (+/- 10 percentage points)

**Distressed**: Firm value volatility (+/- 10 percentage points), debt maturity (+/- 2 years)

**Private**: Total beta vs. market beta (show both values), liquidity discount (+/- 10 percentage points)

**Financial services**: ROE (+/- 2 percentage points), cost of equity (+/- 1 percentage point)

### Reconciling Multiple Sub-Frameworks

When a company triggers multiple classifications (e.g., private + high-growth), apply adjustments in this order:

1. Start with the primary valuation model (revenue-based DCF, excess return model, etc.)
2. Apply probability weighting or distress adjustments (failure probability)
3. Apply discount rate adjustments (total beta for private)
4. Apply value discounts (liquidity discount, minority discount)

This ordering prevents double-counting of risk adjustments.
