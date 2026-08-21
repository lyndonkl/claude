# Assembling the cost of capital

**Core idea:** The cost of capital is the composite cost of all the financing a firm uses, weighted by how much of each it has. It is the hurdle rate for investments whose returns are measured to the whole firm, and the discount rate for free cash flow to the firm. Assembling it is the last step of the discount-rate chain: a bottom-up levered beta and an equity risk premium give the cost of equity; a rating and default spread give the pre-tax cost of debt; a marginal tax rate turns that into an after-tax cost; market values give the weights. Everything must share one currency and one date.

**Formulas:**
- Cost of capital = k_e × E/(D+E) + k_d × (1 − t) × D/(D+E)
  - k_e = cost of equity = Riskfree rate + Levered beta × Equity risk premium.
  - k_d = pre-tax cost of debt = Riskfree rate + Default spread.
  - t = marginal tax rate.
  - E, D = MARKET values of equity and debt (debt includes capitalized leases and the straight-debt half of convertibles).
- With preferred stock: add k_ps × PS/(D+E+PS) and expand the denominator ([[preferred-stock-cost]]).
- Levered beta = Unlevered beta × [1 + (1 − t) × D/E]. The D/E used here must be the same market ratio implied by the weights.
- Equivalent form seen in the packets: Cost of capital = k_e × (1 − D/(D+E)) + k_d × (1 − t) × (D/(D+E)).

**Procedure:**
1. Fix the currency and the valuation date. Every input must match both.
2. Riskfree rate: the long-term government bond rate in that currency, stripped of sovereign default risk if necessary.
3. Cost of equity: bottom-up unlevered beta from comparable firms, relevered at the firm's market D/E, times the equity risk premium (mature-market premium plus any country risk premium), plus the riskfree rate.
4. Pre-tax cost of debt: actual rating if available, otherwise a synthetic rating from interest coverage; add the default spread to the riskfree rate; add country risk if the rating does not already embed it ([[cost-of-debt-estimation-routes]], [[country-risk-in-cost-of-debt]]).
5. Marginal tax rate: statutory rate of the relevant jurisdiction. Apply (1 − t) to the cost of debt only ([[after-tax-cost-of-debt]]).
6. Market values: shares × price for equity; the bond-conversion method plus capitalized leases for debt; preferred separately if ≥ 5% of firm value ([[market-value-of-debt]], [[operating-leases-as-debt]], [[market-value-weights]]).
7. Weight and sum.
8. Consistency checks before using the number:
   - Same currency across cost of equity, cost of debt and cash flows.
   - Same D/E in the beta levering as in the weights.
   - Gross debt throughout, or net debt throughout — never mixed.
   - Tax shield in the discount rate only, never also in FCFF.
   - Match the hurdle rate to the claimholders: returns measured to equity → cost of equity; returns measured to the whole firm → cost of capital.
9. For a multi-business firm, compute a divisional cost of capital rather than applying the company rate everywhere ([[divisional-cost-of-capital]]).
10. If the valuation is in a different currency from the build-up, convert ([[currency-conversion-of-discount-rates]]).

**Reference data:** Assembled costs of capital for the packets' running companies.

| Company | Cost of equity | Pre-tax k_d | Tax rate | After-tax k_d | Debt ratio D/(D+E) | Cost of capital |
|---|---|---|---|---|---|---|
| Disney (US$) | 8.52% | 3.75% | 36.10% | 2.40% | 11.58% | 7.81% |
| Vale (US$) | 11.23% | 4.05% | 34.00% | 2.67% | 35.48% | 8.20% |
| Vale (nominal R$) | — | — | 34.00% | — | 35.48% | 15.62% |
| Tata Motors (Rupee) | 14.49% | 9.62% | 32.45% | 6.50% | 29.28% | 12.15% |
| Baidu (RMB) | 12.91% | 4.60% | 25.00% | 3.45% | 5.23% | 12.42% |
| Bookscape, market beta (US$) | 7.46% | 4.05% | 40.00% | 2.43% | 17.63% | 6.57% |
| Bookscape, total beta (US$) | 11.98% | 4.05% | 40.00% | 2.43% | 17.63% | 10.30% |
| Embraer 2004 (US$) | 10.70% | 9.29% | 34.00% | 6.13% | 16.00% | 9.97% |
| Embraer 2004 (nominal BR) | 18.41% | 13.00% | 34.00% | 8.58% | 16.00% | 16.44% |

Bookscape shows why the beta choice matters for a private firm: a market beta assumes a diversified owner, a total beta assumes an undiversified one, and the cost of capital moves from 6.57% to 10.30%.

**Worked examples:**

*Disney, 2013 ($ millions).*
- Cost of equity = 2.75% + 1.0013 × 5.76% = 8.52%. (Bottom-up levered beta 1.0013; riskfree 2.75%; ERP 5.76%.)
- After-tax cost of debt = (2.75% + 1.00%) × (1 − 0.361) = 3.75% × 0.639 = 2.40%.
- Market value of debt = $13,028 (converted from $14,288 book) + $2,933 (capitalized leases) = $15,961. Market value of equity = $121,878.
- Weights: equity 121,878 / 137,839 = 88.42%; debt 11.58%.
- **Cost of capital = 8.52% × 0.8842 + 2.40% × 0.1158 = 7.81%.**

*Embraer, 2004 (millions of BR).*
- Cost of equity = 4.29% + 1.07 × 4% + 0.27 × 7.89% = 10.70%. (Riskfree 4.29%; levered beta 1.07; mature-market premium 4%; lambda 0.27 applied to Brazil's 7.89% country risk premium.)
- Cost of debt = 4.29% + 4.00% (two-thirds of Brazil's country default spread) + 1.00% (company spread) = 9.29%.
- Market value of equity 11,042; market value of debt 2,083 (from book debt 1,953, interest 222, 4-year maturity, discounted at 9.29%).
- Weights: 84% equity, 16% debt. Marginal tax rate 34%.
- **Cost of capital = 10.70% × 0.84 + 9.29% × 0.66 × 0.16 = 9.97%.**

*Facebook, as configured in wacccalc.xls.*
- Market equity = 2,407 shares × $37.53 = 90,334.71. Market debt = 1,058.83 straight + 0 convertible + 1,127.92 leases = 2,186.75. Preferred = 0. Total capital = 92,521.47.
- Unlevered beta 1.0965 (global Advertising industry average) relevered: 1.0965 × [1 + (1 − 0.40) × 2,186.75 / 90,334.71] = 1.1124.
- ERP 7.127% (revenue-weighted across operating regions). Cost of equity = 2.5% + 1.1124 × 7.127% = 10.43%.
- After-tax cost of debt = 3.5% × 0.60 = 2.10%.
- Weights: equity 97.64%, debt 2.36%.
- **Cost of capital = 0.976365 × 10.4288% + 0.023635 × 2.10% = 10.23%.**

**Determinism:**
- DETERMINISTIC: given cost of equity, pre-tax cost of debt, tax rate and market values of each component, the weighted average is pure arithmetic. So is every intermediate step — levering the beta, converting book debt to market, capitalizing leases, splitting the convertible, looking up the rating spread.
- JUDGMENT lives upstream: choosing comparable firms for the unlevered beta, choosing the equity risk premium approach, setting the marginal tax rate, setting lambda for country risk, deciding gross versus net debt, and deciding whether to use the current or a target capital structure.
- JUDGMENT: whether to use one company-wide rate or divisional rates.
- JUDGMENT: for a private firm, whether the owner is diversified (market beta) or not (total beta).

**Pitfalls:**
- Currency mismatch between the cost of equity, the cost of debt and the cash flows.
- Applying (1 − t) to the whole cost of capital instead of only to the cost of debt.
- Adding the interest tax shield to FCFF as well as taking it in the discount rate.
- Using book weights ([[market-value-weights]]).
- Using a company-wide cost of capital as the hurdle rate for every division, which lets safe divisions subsidize risky ones and tilts the firm toward its riskiest businesses.
- Comparing a return on EQUITY to a cost of CAPITAL, or a return on capital to a cost of equity. Match the hurdle rate to the claimholders whose returns you measure.
- Levering the beta at a different D/E from the one in the weights.
- Leaving preferred stock or capitalized leases out of the capital base.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.184, p.194-195, p.200, p.202-205
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.111, p.115
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.108, p.112
- corporate_finance--lecture_slides--cfpacket1spr20 p.226 (cost of capital as the benchmark for return on capital)
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Cost of Capital worksheet` (B62-E64, WACC E64 = 0.1023193)

**Related:** [[market-value-weights]], [[market-value-of-debt]], [[after-tax-cost-of-debt]], [[cost-of-debt-estimation-routes]], [[divisional-cost-of-capital]], [[currency-conversion-of-discount-rates]], [[wacc-calculator-workflow]], [[preferred-stock-cost]], [[operating-leases-as-debt]], [[bottom-up-beta]], [[equity-risk-premium]], [[hurdle-rate-choice]], [[total-beta]]
