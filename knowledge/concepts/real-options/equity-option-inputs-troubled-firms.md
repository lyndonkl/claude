# Estimating option inputs for equity in a troubled firm (Eurotunnel)

**Core idea:** The clean equity-as-a-call model assumes a firm with exactly two claim holders, one zero-coupon debt issue retirable at face value with no special features, and an observable firm value and variance. Real firms violate all four assumptions. This concept supplies the workarounds. How to build firm value. How to construct firm-value **variance** when only stock and bond volatilities are observable. How to collapse a whole debt schedule into one face value and one maturity. And how to match the riskless rate. The Eurotunnel case shows the full procedure on a firm whose DCF value was a quarter of its debt's face value — and whose equity was still worth something.

**Formulas:**
- Firm-value variance from traded stock and bonds:
  - `sigma^2_firm = w_E^2 x sigma_E^2 + w_D^2 x sigma_D^2 + 2 x w_E x w_D x rho_ED x sigma_E x sigma_D`
  - `w_E` = market-value weight of equity; `w_D` = market-value weight of debt; `sigma_E` = standard deviation of `ln(stock price)`; `sigma_D` = standard deviation of `ln(bond price)`; `rho_ED` = correlation between stock and bond price changes.
- Option life from a debt schedule: `t = face-value-weighted duration = sum(Face_i x Duration_i) / sum(Face_i)`. If durations are unavailable, use face-value-weighted maturity.
- Debt face value for the strike: short-term debt at face/book value; long-term coupon-bearing debt at `face value + cumulated nominal value of the coupons`.
- Equity: `E = S x N(d1) - K x e^(-r*t) x N(d2)`.
- Implied market value of debt: `D = S - E`. Implied interest rate: `r_debt = (Face value / Market value of debt)^(1/t) - 1`.

**Procedure:**
1. **Firm value `S`.** Choose one of three routes: cumulate the market values of equity and debt; value the assets in place using FCFF discounted at the WACC; or use the cumulated market value of assets if they are traded. For a deeply distressed firm the FCFF route is usually the only workable one, because the market value of debt is itself the thing you are trying to price.
2. **Variance in firm value `sigma^2`.** If stocks and bonds are both traded, apply the weighted-variance formula with the historical debt/equity weights over the estimation period. If they are not traded, use the variances of similarly rated bonds, or the average firm-value variance for the industry the company operates in.
3. **Value of the debt `K`.** For short-term debt use only the face or book value. For long-term coupon-bearing debt, add the cumulated nominal value of the coupons to the face value — the coupons are part of what the equity call must clear.
4. **Maturity `t`.** Compute the face-value-weighted duration of the bonds outstanding. Fall back to weighted maturity if durations are unavailable.
5. **Riskless rate `r`.** Match the instrument's duration to the option's life. A 15-year government bond with a duration around 11 years is the right instrument for an 11-year option, not a 15-year-maturity match.
6. Value the equity call, back out the market value of debt, and back out the implied interest rate on the debt.
7. Sanity-check the implied rate against traded bond yields. A wide gap points to an input problem, most often the variance or the firm value.

**Reference data:**

Estimation routes for each input (Damodaran's table):

| Input | Estimation process |
|---|---|
| Value of the firm | Cumulate market values of equity and debt; or value the assets in place using FCFF and WACC; or use cumulated market value of assets if traded. |
| Variance in firm value | If stocks and bonds are traded, use the weighted-variance formula. If not traded, use variances of similarly rated bonds, or the average firm-value variance from the company's industry. |
| Value of the debt | If short term, use only the face/book value of debt. If long term and coupon-bearing, add the cumulated nominal value of the coupons to the face value. |
| Maturity of the debt | Face-value-weighted duration of bonds outstanding; if unavailable, weighted maturity. |

Eurotunnel's debt schedule at the end of 1997:

| Debt type | Face value (£m) | Duration (years) |
|---|---|---|
| Short term | 935 | 0.50 |
| 10 year | 2,435 | 6.7 |
| 20 year | 3,555 | 12.6 |
| Longer | 1,940 | 18.2 |
| **Total** | **8,865** | **10.93 (face-value-weighted)** |

**Worked example:** Eurotunnel in early 1998.

*The situation.* Eurotunnel had been a financial disaster since opening. In 1997 it reported EBIT of **-£56 million** and net income of **-£685 million**. End-1997 book value of equity was **-£117 million**. Face value of debt outstanding: **£8,865 million**, with a face-value-weighted duration of **10.93 years**.

*Firm value from a DCF.* Projected FCFF discounted at the WACC gave a firm value of **£2,312 million** — roughly a quarter of the debt's face value. Assumptions behind that DCF:

- Revenues grow 5% a year in perpetuity.
- COGS, currently 85% of revenues, drops to 65% of revenues by year 5 and stays there.
- Capital spending and depreciation grow 5% a year in perpetuity.
- There are no working-capital requirements.
- The debt ratio, currently 95.35%, drops to 70% after year 5.
- Cost of debt is 10% in the high-growth period and 8% after.
- Stock beta is 1.10 for the next five years, then 0.8.
- The long-term bond rate is 6%.

*Firm-value variance.* Eurotunnel's stock on the London Exchange had an annualized standard deviation of `ln(prices)` of **41%**. Its traded bonds had an annualized standard deviation of `ln(price)` of **17%**. The correlation between stock and bond price changes was **0.5**. The average debt proportion over 1992-1996 was **85%**, so `w_D` = 0.85 and `w_E` = 0.15.

`sigma^2_firm = (0.15)^2 (0.41)^2 + (0.85)^2 (0.17)^2 + 2 (0.15)(0.85)(0.5)(0.41)(0.17) = 0.0335`

*Riskless rate.* A 15-year government bond yielding **6%**, chosen because its duration of roughly 11 years matches the option's 10.93-year life.

*Valuation.*

| Input | Value |
|---|---|
| `S` = value of the firm | £2,312 million |
| `K` = face value of outstanding debt | £8,865 million |
| `t` = weighted average duration of debt | 10.93 years |
| `sigma^2` = variance in firm value | 0.0335 |
| `r` = riskless rate | 6% |

`d1` = -0.8337, `N(d1)` = 0.2023; `d2` = -1.4392, `N(d2)` = 0.0751.

`Equity = 2,312 x 0.2023 - 8,865 x e^(-0.06 x 10.93) x 0.0751 = £122 million`

`Market value of debt = 2,312 - 122 = £2,190 million`

`Interest rate on debt = (8,865 / 2,190)^(1/10.93) - 1 = 13.65%`

Eurotunnel's equity was worth £122 million despite negative book equity, negative EBIT, and a firm value less than a quarter of the debt's face value. Every penny of it is option time value.

**Determinism:** **DETERMINISTIC**, and a script computes all of these from the inputs:
- The face-value-weighted duration. The £8,865m of face values and the four duration figures give 10.93 years.
- The firm-value variance of 0.0335, from the two volatilities, the correlation and the weights.
- The Black-Scholes equity value of £122 million.
- The residual debt value of £2,190 million and the implied 13.65% yield.
- The £2,312 million firm value, once the DCF assumptions are stated.

**JUDGMENT**: every DCF assumption behind that £2,312 million. The perpetual 5% revenue growth. The COGS fall from 85% to 65% of revenues by year 5. The debt ratio path from 95.35% to 70%. The beta path from 1.10 to 0.8. Also the choice of the 1992-1996 window for the debt/equity weights. Whether the historical stock-bond correlation of 0.5 will hold. Which estimation route to use for each input when several are available. And the decision to treat the whole debt schedule as a single zero-coupon claim maturing at its weighted duration.

**Pitfalls:**
- Using the equity's own volatility (41% for Eurotunnel) as the firm-value volatility. The correct firm-value variance was 0.0335, a standard deviation of about 18% — less than half. Using 41% would grossly overstate the equity value.
- Using weighted *maturity* when durations are available. Duration is the better match for the option's life; Eurotunnel's face-value-weighted duration of 10.93 years is well below its weighted maturity.
- Ignoring coupons on long-term debt when setting the strike. The cumulated nominal coupons belong in the face value.
- Matching the riskless rate to bond *maturity* rather than duration. The 15-year bond was chosen for its ~11-year duration.
- Treating the £122 million as a precise valuation. It rests on a DCF built from long-horizon assumptions about a firm losing money, and the four simplifying assumptions of the model are all violated.
- Concluding from the positive equity value that the firm was viable. It was not; the number is time value on a deeply out-of-the-money call.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.77-82
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.77-82

**Related:** [[equity-as-call-option]], [[distressed-equity-time-value]], [[risk-shifting-and-stockholder-bondholder-conflict]], [[black-scholes-model]], [[real-options-framework]], [[dcf-valuation]], [[cost-of-capital]], [[cost-of-debt]], [[financial-distress]], [[duration]]
