# Backing the probability of distress out of bond prices

**Core idea:** Rating tables give an average default rate for a rating class. The market gives you this company's price today. If a firm has a traded bond, you can invert its price to recover the annual probability of distress the market is charging. You price the bond's promised coupons and principal, weight each payment by the probability the firm is still alive to make it, discount at the **riskfree** rate (so all the credit risk sits in the survival weights), and solve for the one probability that reproduces the observed price. The result is usually far more pessimistic than the rating table, and it is exactly the input the distress-adjusted DCF needs.

**Formulas:**
- Model price of the bond, with annual probability of distress `π` and zero recovery in distress:
  `Price = Σ_{t=1..T} [Coupon × (1 − π)^t / (1 + r_f)^t] + Face × (1 − π)^T / (1 + r_f)^T`
  where `Coupon = coupon rate × Face` (Face = 1000 by convention), `T` = years to maturity, `r_f` = riskfree rate, `π` = annual probability of distress (the unknown).
- Solve `f(π) = ModelPrice(π) − MarketPrice = 0`. `f` is monotonically decreasing in `π`, so the root is unique whenever the market price lies between zero and the riskfree-discounted value of the promised payments.
- Cumulative probabilities: `P(distress within n years) = 1 − (1 − π)^n`; `P(survive n years) = (1 − π)^n`.
- Feed into value: `Expected value per share = DCF value × (1 − P(distress over n years)) + Distress equity value × P(distress over n years)` — see [[distress-and-failure-adjusted-value]].

**Procedure:**
1. Pick a bond of the firm that actually trades, and record its coupon rate, remaining maturity, face value and market price (per 1000 of face).
2. Take the riskfree rate at the same maturity.
3. Build the promised cash-flow schedule: coupon in every year `t < T`, coupon plus face in year `T`, zero afterwards.
4. Multiply each year's promised cash flow by `(1 − π)^t` and discount at `r_f`.
5. Solve for `π` so the model price equals the market price. In Excel this is Solver on one cell; in code use bisection or Brent on `π ∈ [0, 1)`.
6. Convert to the horizon your DCF uses — the 10-year cumulative probability if the explicit forecast runs 10 years.
7. Estimate the distress-sale proceeds and compare them with the face value of debt. If proceeds fall short, equity is worth zero in the distress branch.
8. Blend the going-concern value with the distress value using the cumulative probability.
9. Sanity-check against the rating table. A big gap between the market-implied and rating-implied probability is information, not an error — the market is repricing the credit ahead of the agency.

**Reference data:** distress.xls — the model that implements this, with its stored example and outputs. Inputs: coupon rate 12%, maturity 8 years, riskfree rate 5%, market price 653 per 1000 face. Cash flows are 120 for years 1–7 and 1,120 in year 8; the schedule is built out to 25 years with zeros beyond maturity. Solver adjusts the annual distress probability so the model price equals 653.

| Output | Value |
|---|---|
| Annual probability of distress `π` | 13.5317% |
| Model bond value at that `π` | 653.00 |
| Cumulative probability of distress within 5 years | 51.66% |
| Cumulative probability of distress within 10 years | 76.63% |

Check on one year: year 1 promised 120 → survival-adjusted 120 × 0.8646829 = 103.7619 → PV 103.7619/1.05 = 98.8209. Year 8 promised 1,120 → 1,120 × 0.8646829^8 = 350.00 → PV 350.00/1.05^8 = 236.90. The 25 present values sum to 653.00.

Modelling assumptions baked into the sheet, and worth stating whenever you use it: discounting is at the riskfree rate, and recovery in distress is assumed to be **zero**. Both are choices, not bugs. A non-zero recovery assumption would lower the implied `π` for the same price.

**Worked example:** Las Vegas Sands, February 2009. S&P rated LVS B+, and historically 28.25% of B+ bonds default within 10 years. The market said worse. LVS had a 6.375% coupon bond maturing in 7 years trading at $529 per $1,000 of face, with a 3% riskfree rate:

`529 = Σ_{t=1..7} [63.75 × (1 − π)^t / 1.03^t] + 1000 × (1 − π)^7 / 1.03^7` → `π = 13.54%` per year.

Cumulative 10-year survival = (1 − 0.1354)^10 = 23.34%, so the cumulative 10-year probability of distress = **76.66%** — nearly three times the rating-table number. In distress, expected sale proceeds of $2,769m fall short of the face value of debt, so equity receives $0.00. The going-concern DCF gave $8.12 per share (revenues $4,390m growing to $9,974m by year 10, margin rising from 4.76% to the 17% industry average, beta 3.14 falling to 1.20, cost of capital 9.88% → 7.43%, terminal value 758/(0.0743 − 0.03) = $17,129m, equity $5,268m). Blending: `8.12 × (1 − 0.7666) + 0.00 × 0.7666 = $1.92 per share` — far closer to the $4.25 market price than the unadjusted $8.12.

**Determinism:** DETERMINISTIC — (coupon rate, maturity, face, riskfree rate, market price) → annual `π`, and (`π`, horizon) → cumulative probability; then (DCF value, distress equity value, cumulative probability) → expected value per share. A script can reproduce both the distress.xls example and the LVS number. JUDGMENT: which bond to use when several trade, whether to assume zero recovery, what the distress-sale proceeds would be, and whether the market price reflects distress or illiquidity.

**Pitfalls:**
- Discounting at the bond's yield instead of the riskfree rate. The survival weights already carry the credit risk; using the yield double counts it.
- Solving on an illiquid or stale bond price, which produces a probability that reflects the bid-ask spread rather than default risk.
- Forgetting that the sheet assumes zero recovery, then separately assuming a generous recovery in the equity valuation.
- Reporting the annual probability where the model needs the cumulative one over the forecast horizon (13.54% vs 76.66% for LVS is the difference between a $7 and a $2 stock).
- Trusting the rating-table probability when a traded bond disagrees with it.
- Expecting a root when the market price exceeds the riskfree-discounted value of the promised payments; there is none, and `π` should be reported as zero.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.323-324
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.322
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.313-315
- spreadsheet model doc: special-troubled.md — distress.xls

**Related:** [[distress-and-failure-adjusted-value]], [[declining-firm-valuation]], [[synthetic-rating]], [[default-spread]], [[cost-of-debt]], [[difficult-company-taxonomy]]
