# Intrinsic Valuation (DCF) Methodology

Deep reference for model selection, growth estimation, terminal value computation, option adjustment, three-stage mechanics, and discounting conventions.

## Table of Contents
- [Model Selection Decision Tree](#model-selection-decision-tree)
- [Growth Estimation](#growth-estimation)
- [Terminal Value](#terminal-value)
- [Three-Stage Model Mechanics](#three-stage-model-mechanics)
- [Employee Stock Option Adjustment](#employee-stock-option-adjustment)
- [Handling Negative Earnings](#handling-negative-earnings)
- [Discounting Mechanics and Conventions](#discounting-mechanics-and-conventions)
- [Linking Narrative to DCF Inputs](#linking-narrative-to-dcf-inputs)

---

## Model Selection Decision Tree

Use the following decision sequence to choose the DCF variant.

**Question 1: Is the company a financial services firm (bank, insurance, investment firm)?**
- Yes: Use FCFE or DDM. Debt is operational for financial firms, so FCFF and WACC are not meaningful. If the company pays stable dividends, use DDM. If dividends are irregular or payout is low, use FCFE with excess return model (see special-situations-valuation skill).
- No: Continue to Question 2.

**Question 2: Is the company's capital structure expected to change significantly?**
- Yes (leverage changing, M&A planned, recapitalization): Use FCFF. The WACC adjusts naturally as capital structure changes in the stable period, while FCFE requires explicit debt scheduling that introduces additional estimation error.
- No (stable debt ratio, predictable borrowing): Either FCFF or FCFE works. Continue to Question 3.

**Question 3: Is the company a mature, stable dividend payer?**
- Yes (long dividend track record, payout ratio > 50%, utility/REIT/consumer staple): Consider DDM. If buybacks are significant, use augmented DDM (dividends + buybacks as the cash flow).
- No: Use FCFF (default recommendation) or FCFE.

**Question 4: For FCFE, can you reliably estimate debt issuance and repayment?**
- Yes: FCFE is appropriate.
- No: Use FCFF. Estimating net debt flows adds noise that FCFF avoids.

**Summary decision rules:**
- Default for non-financial companies: FCFF two-stage
- Financial services: FCFE or DDM
- Mature dividend payers: DDM
- Changing capital structure: FCFF
- Stable structure, predictable debt: FCFF or FCFE (analyst preference)

---

## Growth Estimation

### Method 1: Fundamental Growth (Preferred)

Growth in operating income (for FCFF):
```
g = Reinvestment Rate x Return on Capital (ROC)

where:
  Reinvestment Rate = (Net CapEx + Change in WC) / After-tax EBIT
  ROC = After-tax EBIT / Invested Capital
  Invested Capital = Book Value of Equity + Book Value of Debt - Cash
```

Growth in net income (for FCFE / DDM):
```
g = Retention Ratio x Return on Equity (ROE)

where:
  Retention Ratio = 1 - Payout Ratio = 1 - (Dividends / Net Income)
  ROE = Net Income / Book Value of Equity
```

**Why fundamental growth is preferred:**
- It ties growth directly to reinvestment, ensuring internal consistency
- It makes explicit the trade-off: higher growth requires higher reinvestment, which reduces free cash flow
- It prevents the common error of projecting high growth without the reinvestment needed to support it

**Adjustments to consider:**
- If current ROC is unusually high or low (cyclical peak/trough), use normalized ROC
- If the company is improving efficiency, ROC can increase over the projection period (efficiency growth component)
- For young companies, sales-to-capital ratio may be more stable than ROC. Use: Reinvestment = Revenue change / Sales-to-capital ratio

### Method 2: Historical Growth (Cross-Check)

- Compute CAGR of revenue and operating income over 3, 5, and 10 years
- Use geometric mean, not arithmetic mean (avoids upward bias)
- Check whether historical growth rate is sustainable given current size and market conditions
- Historical growth is most useful when the company is mature and the past is a reasonable guide to the future
- For young or rapidly changing companies, historical growth may be misleading

### Method 3: Analyst Consensus (Cross-Check)

- Collect consensus revenue and EPS growth estimates for the next 2-5 years
- Use as a sanity check against fundamental and historical estimates
- Be aware of known biases: analysts tend to be optimistic on growth and slow to revise downward
- Weight analyst estimates more when the company has broad coverage (10+ analysts)

### Estimating the Length of the High-Growth Period

The high-growth period should reflect how long the company can earn returns above its cost of capital. Factors that extend the period:
- Strong competitive advantages (network effects, switching costs, patents, brands)
- Large addressable market with low current penetration
- High barriers to entry in the industry
- Management track record of sustained value creation

Factors that shorten the period:
- Commodity business with low differentiation
- Rapid technological change that erodes advantages
- Small addressable market nearing saturation
- Regulatory risk or competitive threats

**Typical ranges by company type:**
| Company Type | High-Growth Period | Rationale |
|-------------|-------------------|-----------|
| Mature stable | 0 years (stable model) | Already at steady state |
| Mature growth | 5 years | Advantages eroding, growth slowing |
| High growth | 5-10 years | Strong position, large TAM |
| Young growth | 10-15 years (three-stage) | Long runway, needs transition period |

---

## Terminal Value

### Growing Perpetuity (Primary Method)

The growing perpetuity formula assumes cash flows grow at a constant rate forever:

```
Terminal Value = CF(n+1) / (r - g_stable)

where:
  CF(n+1) = Cash flow in the first year of stable growth
  r = Discount rate in stable period (WACC for FCFF, ke for FCFE)
  g_stable = Stable growth rate (perpetuity)
```

**Computing the stable-period cash flow:**

For FCFF:
```
Stable FCFF = After-tax EBIT(n) x (1 + g_stable) x (1 - Stable Reinvestment Rate)

Stable Reinvestment Rate = g_stable / Stable ROC
```

For FCFE:
```
Stable FCFE = Net Income(n) x (1 + g_stable) x (1 - Stable Equity Reinvestment Rate)

Stable Equity Reinvestment Rate = g_stable / Stable ROE
```

For DDM:
```
Terminal Value = DPS(n) x (1 + g_stable) / (ke_stable - g_stable)
```

### Stable Growth Rate Constraints

The stable growth rate is the single most sensitive input in a DCF. Apply these constraints:

1. **Upper bound**: The stable growth rate should not exceed the risk-free rate (for real cash flows) or the nominal GDP growth rate of the economy. A company that grows faster than the economy forever would eventually become the economy.

2. **Practical range**: For companies operating in developed markets, 1-3% (real) or 2-4% (nominal) is typical. For companies with significant emerging market exposure, slightly higher (up to 5% nominal) may be justified.

3. **Consistency with reinvestment**: If g_stable = 3% and stable ROC = 10%, then reinvestment rate must be 30%. The remaining 70% of after-tax income is free cash flow. If ROC in stable period is only 8%, reinvestment rate must be 37.5%, leaving less free cash flow.

4. **Risk-free rate anchor**: In practice, setting g_stable equal to the risk-free rate is a common and defensible default. This implies the company grows with the economy.

### Exit Multiple Cross-Check (Secondary Method)

Apply an industry-average EV/EBITDA or PE multiple to terminal year financials:

```
Terminal Value (multiple) = Terminal Year EBITDA x Industry EV/EBITDA
```

This is a cross-check, not the primary approach, for two reasons:
- It introduces relative valuation assumptions into an intrinsic model, which defeats the purpose
- The multiple itself is driven by the same growth and risk assumptions that the perpetuity captures

If the perpetuity-based terminal value and the multiple-based terminal value differ by more than 25%, investigate:
- Is the stable growth rate too high or low relative to industry norms?
- Is the stable WACC inconsistent with the implied multiple?
- Is the industry multiple distorted by temporary conditions?

### Terminal Value as Percentage of Total Value

| Terminal Value % | Interpretation | Action |
|-----------------|---------------|--------|
| < 50% | Near-term cash flows dominate | Focus on accuracy of projections |
| 50-80% | Normal range for growth firms | Standard sensitivity analysis |
| 80-90% | High dependence on terminal | Stress-test g and WACC carefully |
| > 90% | Extreme dependence on terminal | Consider extending growth period or questioning model assumptions |

---

## Three-Stage Model Mechanics

Use when the company needs a transition period between high growth and stable growth.

**Stage 1: High Growth (Years 1 through n1)**
- Growth rate: g_high (constant)
- Reinvestment rate: high (consistent with g_high and current ROC)
- Discount rate: current WACC or ke

**Stage 2: Transition (Years n1+1 through n2)**
- Growth rate: declining linearly from g_high to g_stable
- Reinvestment rate: declining linearly from high to stable
- Discount rate: converging from current to stable levels
- Beta: converging toward 1.0
- Debt ratio: converging toward industry average

Linear interpolation for year t in the transition:
```
g(t) = g_high - (g_high - g_stable) x (t - n1) / (n2 - n1)
Reinvestment(t) = RR_high - (RR_high - RR_stable) x (t - n1) / (n2 - n1)
Beta(t) = Beta_high - (Beta_high - Beta_stable) x (t - n1) / (n2 - n1)
```

**Stage 3: Stable Growth (Year n2+1 onward)**
- Growth rate: g_stable (perpetuity)
- Reinvestment rate: g_stable / ROC_stable
- Discount rate: stable WACC or ke
- Terminal value computed at end of year n2

**When to use three-stage vs two-stage:**
- Two-stage: Company has 5-10 year growth period, then abrupt shift to stable. Works when the company is already in mature growth or approaching it.
- Three-stage: Company is in young growth or early high growth with a long runway. The transition period (5 years) captures the gradual deceleration of growth and convergence of risk and reinvestment characteristics.

---

## Employee Stock Option Adjustment

Employee stock options represent a claim on equity that must be subtracted before computing per-share value.

### Treasury Stock Method (Simpler)

Used when options are in the money (stock price > strike price):

```
Additional shares from options = Options x (Stock Price - Strike Price) / Stock Price

Diluted shares = Basic shares + Additional shares from in-the-money options

Per-share value = Equity value / Diluted shares
```

This method underestimates the option value because it ignores time value. Use for quick estimates.

### Black-Scholes Method (More Precise)

Value each tranche of options using modified Black-Scholes:

```
C = S x e^(-yt) x N(d1) - K x e^(-rt) x N(d2)

d1 = [ln(S/K) + (r - y + sigma^2/2) x t] / (sigma x sqrt(t))
d2 = d1 - sigma x sqrt(t)

where:
  S = Estimated stock value (use iterative approach: start with value per share
      ignoring options, compute option value, subtract, recompute per share, iterate)
  K = Weighted average exercise price
  t = Weighted average time to expiration
  r = Risk-free rate
  y = Dividend yield (expected)
  sigma = Stock price volatility (historical or implied)
  N() = Cumulative normal distribution function
```

**Total option value = Number of options x Value per option**

**Subtract total option value from equity value before dividing by basic shares.**

When using Black-Scholes:
- Group options by tranche if strike prices and maturities differ significantly
- Use estimated intrinsic value (not market price) as S when valuing the company
- For companies with very large option grants (tech), the option value can be 5-15% of equity value

---

## Handling Negative Earnings

When the company has negative operating income, the standard FCFF model cannot be directly applied. Options:

**Approach 1: Revenue-based DCF (preferred for high-growth firms)**
- Project revenue growth based on TAM and market share trajectory
- Converge operating margin from current (negative) to target (positive, based on mature industry peers)
- Use sales-to-capital ratio to determine reinvestment (Reinvestment = Revenue change / Sales-to-capital)
- Compute FCFF once margins turn positive
- Apply failure probability adjustment: Value = DCF value x (1 - P_failure) + Distress value x P_failure
- See special-situations-valuation skill for detailed negative-earnings methodology

**Approach 2: Normalize earnings**
- If earnings are temporarily depressed (cyclical trough, one-time restructuring), use normalized EBIT
- Average operating margin over a full cycle (5-10 years) and apply to current revenue
- Appropriate for cyclical companies, not for structurally unprofitable firms

**Approach 3: Start from revenue, build to earnings**
- Project revenue with growth rates
- Apply a target operating margin that converges over the high-growth period
- The company becomes profitable in year 2-4 of the projection
- Terminal value is computed on the normalized, mature-period earnings

---

## Discounting Mechanics and Conventions

### End-of-Year Convention (Standard)

Cash flows occur at the end of each year and are discounted accordingly:

```
PV of CF(t) = CF(t) / (1 + r)^t
```

### Mid-Year Convention (Alternative)

If cash flows occur relatively evenly throughout the year, the mid-year convention is more accurate:

```
PV of CF(t) = CF(t) / (1 + r)^(t - 0.5)
```

This increases the present value by approximately (1 + r)^0.5 relative to end-of-year. Use when:
- Cash flows are roughly uniform throughout the year (not lumpy)
- Precision matters and the discount rate is high

### Present Value of Terminal Value

The terminal value is computed at the end of year n and must be discounted back to the present:

```
PV of Terminal Value = Terminal Value / (1 + r)^n
```

If using mid-year convention for operating cash flows, still discount the terminal value at the full year n (it represents a perpetuity starting at the end of year n, not in the middle).

### Multi-Currency Considerations

When the company operates in multiple currencies:
- Project cash flows in the currency of operation
- Discount at a rate appropriate for that currency (using inflation-differential-adjusted risk-free rate)
- Convert terminal values to the reporting currency at the forward exchange rate (implied by interest rate differential)
- Alternatively, project all cash flows in a single currency and use a single consistent discount rate

The key consistency rule: cash flows and discount rate must be in the same currency. Mixing dollar cash flows with a rupee discount rate produces meaningless results.

---

## Linking Narrative to DCF Inputs

Each DCF input should trace back to the business narrative (from business-narrative-builder):

| DCF Input | Narrative Source |
|-----------|-----------------|
| Revenue growth rate | TAM sizing, market share trajectory, competitive position |
| Target operating margin | Industry structure, pricing power, cost advantages |
| Reinvestment rate (or sales-to-capital) | Capital intensity of growth, efficiency of deployment |
| Length of high-growth period | Competitive advantage magnitude and sustainability |
| Stable growth rate | Long-term industry growth, GDP linkage |
| Cost of capital | Risk profile from life cycle stage, geographic exposure |
| Failure probability | Life cycle stage (young/distressed), cash runway |

This linkage ensures that every number in the model is supported by a business reason, and changes to the narrative flow through to the valuation in a traceable way. If you cannot articulate why a growth rate is 12% rather than 8%, the input is not well-grounded.
