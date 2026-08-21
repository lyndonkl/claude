# Natural resource options (undeveloped reserves)

**Core idea:** In a natural resource investment the underlying asset is the resource itself. Its value depends on two things: the quantity of the resource available and the resource's price. Developing it costs money, and the owner's profit is the difference between the value of the extracted resource and the development cost. So an undeveloped reserve is a call option, exercised by developing. This is the strongest real-option application in the material, because the underlying commodity is traded (giving observable prices and volatility), reserves trade, and development costs are known from past projects. Two features are specific to resources: a **development lag** between the exercise decision and first cash flow, and **net production revenue** acting as a dividend yield.

**Formulas:**
- Payoff on a natural resource investment: `max(V - X, 0)`, where `V` = estimated value of the resource and `X` = cost of development.
- Underlying asset value, adjusted for the development lag:
  - `S = Reserves x (Price per unit - Production cost per unit) / (1 + y)^(lag)`
  - `Reserves` in physical units; `y` = dividend yield (net production revenue as a fraction of developed-reserve value); `lag` = development lag in years.
- Strike: `K = Reserves x Development cost per unit`.
- Option value (dividend-adjusted Black-Scholes call): `C = S x e^(-y*t) x N(d1) - K x e^(-r*t) x N(d2)`, with `t` = relinquishment life, `sigma^2` = variance in the resource price, `r` = riskless rate.
- Firm value for a resource company: `Firm value = PV of developed (producing) reserves + Option value of undeveloped reserves`.
- Developed reserves as a finite annuity: `PV = FCFF x (1 - (1 + WACC)^(-n)) / WACC`, with `n` = remaining life of developed reserves.
- `Equity value = Firm value - Debt`; `Value per share = Equity value / shares`.

**Procedure:**
1. Separate reserves into **developed (producing)** and **undeveloped**. They are valued by different methods.
2. Value developed reserves with a DCF. Use the annual free cash flow to the firm from production, the remaining reserve life, and the WACC. A level annuity is usually adequate.
3. For undeveloped reserves, get expert estimates of the quantity available (geologists for oil, and equivalent specialists for other resources).
4. Compute the gross value per unit as `price - production cost (including taxes and royalties)`, then multiply by reserves.
5. Discount that value back over the **development lag**, because the firm receives no cash flows from reserves until they are developed. Use the dividend yield as the discount rate over the lag. This gives `S`.
6. Set `K` = reserves times development cost per unit, in present-value dollars.
7. Set `t` = the relinquishment period, if the asset must be given up at a point in time. Otherwise use the time to exhaust inventory, based on inventory and capacity output.
8. Set `sigma^2` from the variability of the resource price and the variability of available reserves.
9. Set `y` = net production revenue each year as a percent of the market value of developed reserves.
10. Set `r` = a government bond rate matching `t`.
11. Value the call. Add it to the developed-reserve DCF, subtract debt, divide by shares.
12. Compare the result with the market or offer price to reach a verdict.

**Reference data:**

Estimation process for each natural-resource option input (Damodaran's mapping table):

| # | Input | Estimation process |
|---|---|---|
| 1 | Value of available reserves | Expert estimates (geologists for oil, etc.); then PV of the after-tax cash flows from the resource |
| 2 | Cost of developing reserve (strike) | Past costs and the specifics of the investment |
| 3 | Time to expiration | Relinquishment period if the asset must be relinquished; or time to exhaust inventory, from inventory and capacity output |
| 4 | Variance in value of underlying asset | Variability of the price of the resource and variability of available reserves |
| 5 | Net production revenue (dividend yield) | Net production revenue each year as a percent of market value |
| 6 | Development lag | Discount the reserve value back over the lag period |

**Worked example:** Gulf Oil, a takeover target in early 1984 at $70 per share.

Inputs:

| Item | Value |
|---|---|
| Shares outstanding | 165.30 million |
| Total debt | $9.9 billion |
| Estimated reserves | 3,038 million barrels |
| Average development cost | $10/barrel (PV dollars) |
| Development lag | ~2 years |
| Average relinquishment life of reserves | 12 years |
| Oil price | $22.38/barrel |
| Production cost, taxes and royalties | $7/barrel |
| Bond rate | 9.00% |
| Net production revenue (dividend yield) | ~5% of value of developed reserves |
| Variance in oil prices | 0.03 |

*Undeveloped reserves as a call.*
`S = 3,038 x (22.38 - 7) / 1.05^2 = $42,380.44 million`
`K = 3,038 x 10 = $30,380 million`
`t` = 12 years, `sigma^2` = 0.03, `r` = 9%, `y` = 5%.
`d1` = 1.6548, `N(d1)` = 0.9510; `d2` = 1.0548, `N(d2)` = 0.8542.
`C = 42,380.44 x e^(-0.05 x 12) x 0.9510 - 30,380 x e^(-0.09 x 12) x 0.8542 = $13,306 million`.

*Developed reserves.* FCFF of $915 million per year for 10 years at a WACC of 12.5%:
`PV = 915 x (1 - 1.125^(-10)) / 0.125 = $5,065.83 million`.

*Firm and per share.*

| Component | $ millions |
|---|---|
| Value of undeveloped reserves | 13,306 |
| Value of production in place | 5,066 |
| **Total value of firm** | **18,372** |
| Less outstanding debt | 9,900 |
| **Value of equity** | **8,472** |
| Value per share (8,472 / 165.3) | **$51.25** |

Verdict: $51.25 per share against a $70 takeover offer. The bid was well above the option-inclusive value.

**Determinism:** **DETERMINISTIC**: the whole computation chain once the inputs are set. A script takes `(reserves, price, production cost, development cost, lag, relinquishment life, variance, riskless rate, yield, FCFF, WACC, developed-reserve life, debt, shares)` and returns `S`, `K`, `d1`, `d2`, the call value, the annuity value, firm value, equity value, and value per share. The lag adjustment and the annuity are closed-form. **JUDGMENT**: the reserve estimate itself, which comes from geologists and carries wide error bars. The development cost per barrel, drawn from past projects that may not resemble this one. The relinquishment life, or the inventory-exhaustion horizon if there is no relinquishment date. The variance input — whether to use oil-price variance alone (as here, 0.03) or to widen it for reserve uncertainty. The 5% net production revenue rate. And the split between developed and undeveloped reserves.

**Pitfalls:**
- Skipping the development lag adjustment. Cash flows do not start when you exercise; failing to discount `S` back over the lag overstates the option materially. Two years at 5% cut Gulf Oil's `S` by about 9%.
- Omitting the dividend yield in the option formula. Net production revenue is real value leakage over a 12-year option.
- Valuing all reserves as options. Reserves already in production are a DCF annuity, not an option; double-counting them inflates firm value.
- Using price variance where reserve quantity is also highly uncertain. The input should reflect both.
- Forgetting to subtract debt. Gulf Oil's $9.9 billion of debt is more than half the firm value; equity per share is meaningless without it.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.38-43
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.38-43

**Related:** [[option-to-delay]], [[black-scholes-model]], [[real-options-framework]], [[patent-valuation-as-option]], [[valuing-a-firm-with-patents]], [[dcf-valuation]], [[cost-of-capital]], [[value-per-share]]
