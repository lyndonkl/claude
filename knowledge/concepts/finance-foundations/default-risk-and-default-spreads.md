# Default Risk and Default Spreads

**Core idea:** A contractual claim promises cash flows, but the promisor may not deliver. That risk of not being paid what is contractually due is default risk, or credit risk. Lenders respond by charging more than the riskfree rate, and the excess is the default spread. Pricing a risky bond therefore needs one extra step over pricing a Treasury: discount the *promised* cash flows at the riskfree rate plus the spread that matches the issuer's credit rating. Because riskier bonds trade at lower prices, a firm sliding into distress will see its bond prices fall even if market interest rates do not move at all. Default risk is an independent driver of bond prices.

**Formulas:**
- Default-risk adjusted discount rate: `r = Riskfree rate + Default spread`. `Default spread` is read off a rating-to-spread table for the issuer's rating and the relevant period.
- Price of a bond with default risk: `Price = C × PV(A, n, r_f + s) + F / (1 + r_f + s)^n`. `C` = annual coupon; `n` = years to maturity; `r_f` = riskfree rate; `s` = default spread for the bond's rating; `F` = face value; `PV(A, n, r) = [1 − (1+r)^(−n)]/r`.
- Implied spread from a market price: solve for `YTM` from the price, then `s = YTM − r_f`.

**Procedure:**
1. Establish the issuer's credit rating. Use the agency rating if one exists (Moody's, S&P, Fitch). If the issuer is unrated, estimate a synthetic rating from its interest coverage ratio and then proceed.
2. Look up the default spread for that rating in the table below, using the year closest to your valuation date. Spreads for the same rating move over time, so the year matters.
3. Add the spread to the riskfree rate for the same maturity and currency. That is the discount rate.
4. Discount the *promised* coupons and face value at that rate. Do not haircut the cash flows and also raise the rate; that double-counts the default risk.
5. Check the investment-grade line. A rating below BBB is below investment grade, and the lower rating classes are "high yield" bonds. That threshold matters because many institutions cannot hold below-investment-grade paper, which thins the market and widens spreads further.
6. When the firm's credit deteriorates, reprice with the new rating's spread rather than the old. The price change comes entirely from the spread, with market rates unchanged.
7. Going the other way, extract the market's view. Take a traded bond's price, solve for its yield to maturity, subtract the riskfree rate, and you have the market-implied default spread. Compare it with the table to see whether the market agrees with the rating.

**Reference data:** Default spreads for 10-year corporate bonds by rating (Damodaran, Foundations of Finance Session 7). Use the most recent column, 2017, unless you are valuing as of an earlier date:

| Rating (Moody's/S&P) | Spread 2017 | Spread 2016 | Spread 2015 |
|---|---|---|---|
| Aaa/AAA | 0.60% | 0.75% | 0.40% |
| Aa2/AA | 0.80% | 1.00% | 0.70% |
| A1/A+ | 1.00% | 1.10% | 0.90% |
| A2/A | 1.10% | 1.25% | 1.00% |
| A3/A- | 1.25% | 1.75% | 1.20% |
| Baa2/BBB | 1.60% | 2.25% | 1.75% |
| Ba1/BB+ | 2.50% | 3.25% | 2.75% |
| Ba2/BB | 3.00% | 4.25% | 3.25% |
| B1/B+ | 3.75% | 5.50% | 4.00% |
| B2/B | 4.50% | 6.50% | 5.00% |
| B3/B- | 5.50% | 7.50% | 6.00% |
| Caa/CCC | 6.50% | 9.00% | 7.00% |
| Ca2/CC | 8.00% | 12.00% | 8.00% |
| C2/C | 10.50% | 16.00% | 10.00% |
| D2/D | 14.00% | 20.00% | 12.00% |

Two features to note. Spreads rise steeply, not linearly, as ratings fall: the gap from AAA to BBB is 1.00 percentage point in 2017, while the gap from BBB to D is 12.40 points. And the whole curve shifts with market conditions — 2016 spreads were higher than both 2015 and 2017 at almost every rating, so using the wrong year's column can be a larger error than misjudging the rating by a notch.

**Worked example:** A BBB-rated, 3% coupon, 10-year corporate bond in January 2017, with $1,000 face value. The riskfree rate is 2.5%. The BBB spread for that period is 1.75%, so the discount rate is `2.5% + 1.75% = 4.25%`.

`PV(A, 10, 4.25%) = [1 − 1.0425^(−10)] / 0.0425 = 7.9877`
`Price = 30 × 7.9877 + 1000 / 1.0425^10 = 239.63 + 660.52 = $899.87`

Compare this with the same bond from a default-free issuer at 2.5%, which prices at $1,043.76. The 175-basis-point spread costs $143.89, or 13.8% of the risk-free price. If the issuer were then downgraded to B, the 2017 spread of 4.50% would push the discount rate to 7.0% and the price down again — with no change whatsoever in market interest rates. (Source: Damodaran, Foundations of Finance Session 7.)

**Determinism:**
- DETERMINISTIC: the discount rate, given a riskfree rate and a spread. The bond price, given coupon, maturity, face value, riskfree rate, and spread. The table lookup from `(rating, year)` to spread. The implied spread from a market price via IRR.
- JUDGMENT: assigning the credit rating, especially for an unrated issuer where you must build a synthetic rating. Choosing which year's spread table applies. Judging whether a firm is sliding into distress before the agencies act. Deciding whether the market-implied spread or the rating-based spread is the better estimate when they diverge. These need the issuer's financials, its interest coverage, its traded bond prices, and the state of the credit cycle.

**Pitfalls:**
- Using last year's spread table. Spreads for a single rating moved by more than a full percentage point between 2015 and 2016 at the BBB level, and by 8 points at the D level.
- Reducing the promised cash flows *and* adding the default spread to the discount rate. Pick one; doing both double-counts.
- Treating the rating as fixed. Ratings lag reality, and prices move before downgrades.
- Assuming spreads scale linearly with rating notches. They accelerate sharply below investment grade.
- Forgetting the investment-grade cliff at BBB. Crossing it triggers forced selling by institutions, so the spread widens by more than the credit deterioration alone would justify.
- Applying a corporate spread table to a sovereign issuer without adjustment.

**Sources:**
- `foundations_of_finance--vauing_bonds p.3, p.9-12`

**Related:** [[bond-valuation-and-yield-to-maturity]], [[interest-rate-risk-and-bond-propositions]], [[currency-consistent-valuation]], [[cost-of-capital]], [[synthetic-rating]], [[yield-curve-and-growth-signals]]
