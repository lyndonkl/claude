# Decomposing convertible debt

**Core idea:** A convertible bond is two securities in one wrapper: a plain bond, plus a call option on the company's stock. Treating the whole thing as debt overstates debt and understates equity; treating it as equity does the reverse. Damodaran's rule is to break it apart and eliminate "convertibles" as a third category entirely. The bond half goes into debt at its straight-debt value; the option half goes into market capitalization as equity. The split is easy because the market gives you the total: value the bond half by discounting its coupons and face value at the rate on straight bonds of the same rating, and the option half is whatever is left over.

**Formulas:**
- Straight debt value = Coupon × [1 − (1 + r)^(−n)] / r + Face value / (1 + r)^n
  - Coupon = stated coupon rate × face value (the annual cash coupon).
  - r = market interest rate on STRAIGHT bonds of the same rating and maturity (not the convertible's stated rate).
  - n = years to maturity.
  - The first term is the present value of an n-year coupon annuity; the second is the discounted face value.
- Equity (conversion option) portion = Market value of the convertible − Straight debt value.
- Then: Debt for the weights += Straight debt value. Market capitalization for the weights += Equity portion.

**Procedure:**
1. Collect the convertible's terms: face value, stated coupon rate, years to maturity, and its current MARKET value (price × number of bonds outstanding).
2. Determine the firm's rating and the current market yield on straight bonds of that rating and maturity. If the firm has no rating, use a synthetic rating ([[synthetic-rating]]).
3. Discount the convertible's coupons and face value at that straight-bond rate. That is the straight debt value — what the bond would be worth with the conversion right stripped out.
4. Subtract the straight debt value from the convertible's market value. The remainder is the conversion option's value.
5. Add the straight debt value to total debt. Add the option value to market capitalization.
6. Sanity-check: the option value must be positive. If the convertible trades BELOW its straight-debt value, either your straight-bond rate is too low, or the market is pricing distress the rating does not reflect.
7. Use the resulting debt and equity figures in the cost-of-capital weights ([[market-value-weights]]).
8. Apply the same logic to convertible preferred stock: a preferred component plus a conversion option counted as equity.

**Reference data:** No lookup table. The mapping:

| Component | Value | Goes into |
|---|---|---|
| Straight debt piece | Coupon annuity + discounted face, at the straight-bond rate | Debt |
| Conversion option piece | Market value of convertible − straight debt piece | Market capitalization (equity) |
| Whole convertible | Market value | Nothing — never used as a single category |

Model implementation (wacccalc.xls, `Cost of Capital worksheet`): inputs are book value of convertible debt (B42), interest expense on the convertible (B43), maturity in years (B44), and market value of the convertible (B45). The straight-debt value C56 = B43 × [1 − (1 + r_d)^(−B44)] / r_d + B42 / (1 + r_d)^B44, where r_d is the firm's pre-tax cost of debt (B37). The equity portion C58 = B45 − C56. C56 is added to the market value of debt (C62 = straight debt + convertible straight-debt piece + lease debt); C58 belongs with equity. If maturity is 0, skip the present-value formula and use the book and market values directly.

**Worked example:** A firm has $125 million face value of convertible debt with a 4% stated coupon and 10 years to maturity. The convertible trades at a market value of $140 million. The firm is rated A, and the market rate on A-rated straight bonds is 8%.

- Annual coupon = 4% × $125m = $5 million.
- Straight debt value = $5m × [1 − 1.08^(−10)] / 0.08 + $125m / 1.08^10 = $5m × 6.7101 + $125m × 0.46319 = $33.55m + $57.90m = $91.45 million.
- Equity (conversion option) portion = $140m − $91.45m = $48.55 million.
- In the cost-of-capital weights: add $91.45m to debt and $48.55m to market capitalization.

Note how large the error would be from the naive treatments. Counting the whole $140m as debt overstates debt by 53%. Counting it all as equity understates debt by $91m.

**Determinism:**
- DETERMINISTIC: face value, coupon rate, maturity, market value and the straight-bond rate → straight debt value and equity portion. Pure arithmetic.
- JUDGMENT: the straight-bond rate r. It requires the firm's rating (actual or synthetic), a current spread table, and a maturity-matched riskfree rate. Small errors in r move the split noticeably in a long-dated convertible.
- JUDGMENT: whether to use this simple bond-arithmetic split at all, versus a formal option-pricing model for the conversion right. The subtraction method is the packet's method and is adequate when the convertible trades.
- JUDGMENT: what to do when the convertible does not trade, so no market value is observable. Then both halves must be modelled, and the option needs an option-pricing input set (stock price, volatility, conversion ratio, time to maturity).

**Pitfalls:**
- Discounting the convertible's cash flows at the convertible's OWN low stated coupon rate. Convertibles carry below-market coupons precisely because of the option; using that rate makes the bond half look almost like par and shrinks the option to nothing.
- Putting the whole market value into debt because it is called a bond.
- Forgetting the equity half in the market capitalization, which understates the equity weight and, with it, the cost of capital.
- Using the convertible's book value instead of its market value when computing the option residual.
- Leaving the convertible's full coupon in the interest expense used for the interest coverage ratio while only the straight-debt piece sits in debt. Keep the numerator and denominator consistent.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.194
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.113-114
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.110-111
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls convertible block (B42-B45, C56, C58, C62)

**Related:** [[preferred-stock-cost]], [[what-counts-as-debt]], [[market-value-of-debt]], [[market-value-weights]], [[cost-of-capital-assembly]], [[synthetic-rating]], [[option-pricing]]
