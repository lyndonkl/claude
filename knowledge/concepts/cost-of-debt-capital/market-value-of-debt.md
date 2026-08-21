# Converting book debt to market value

**Core idea:** The cost of capital needs the MARKET value of debt, but balance sheets report book value. Most corporate debt does not trade, so you cannot look the market value up. Damodaran's workaround is to treat the entire book debt as if it were one coupon bond: the annual coupon is the firm's total interest expense, the face value is the book value of debt, the maturity is the weighted-average maturity from the debt footnote, and the discount rate is the firm's CURRENT pre-tax cost of debt. Discount the coupons and face value at that rate and you get an estimated market value. When rates or credit quality have moved since the debt was issued, this number differs materially from book. Add the debt value of operating leases on top.

**Formulas:**
- Estimated market value of debt = Interest expense × [1 − (1 + r)^(−M)] / r + Book value of debt / (1 + r)^M
  - Interest expense = total annual interest on debt (the "coupon" of the synthetic bond).
  - Book value of debt = face value of the synthetic bond.
  - M = weighted-average maturity of the firm's debt, in years.
  - r = current PRE-TAX cost of debt (riskfree rate + default spread).
  - The first term is the present value of an M-year annuity of interest; the second is the discounted principal.
- Weighted-average maturity M = Σ over tranches of (tranche amount / total disclosed amount) × tranche maturity.
- Total debt for the weights = Estimated market value of interest-bearing debt + Debt value of operating leases + Straight-debt component of convertibles.
- Default when the maturity schedule is unavailable: M = 3 years.

**Procedure:**
1. Pull the book value of interest-bearing debt from the balance sheet and total interest expense from the income statement.
2. Find the debt maturity schedule in the footnotes. Compute the weighted-average maturity: weight each tranche by its share of the DISCLOSED total and multiply by its years to maturity.
3. If no maturity schedule is disclosed, use 3 years.
4. Set r = the firm's current pre-tax cost of debt ([[cost-of-debt-estimation-routes]]). Do not use the historical average coupon rate.
5. Apply the bond formula.
6. Capitalize operating leases and add the resulting debt value ([[operating-leases-as-debt]]).
7. If there are convertibles, add only their straight-debt component ([[convertible-debt-decomposition]]).
8. Use the total in the cost-of-capital weights.

Interpretation rules:
- If the current cost of debt exceeds the average coupon rate embedded in the interest expense, market value comes out BELOW book value. That is what happened to Disney.
- If rates or credit quality have improved since issuance, market value exceeds book.
- The footnoted maturity amounts often do not add to total book debt, because firms do not break down the maturity of every borrowing. Use the disclosed tranches to compute the weighted-average maturity, but use the FULL book debt as the face value.

**Reference data:** Disney's debt maturity schedule, 2013 ($ millions). Total disclosed $12,139 against book debt of $14,288 — the gap is debt whose maturity Disney does not break out.

| Years to maturity | Amount | Weight | Weight × maturity |
|---|---|---|---|
| 0.5 | $1,452 | 11.96% | 0.06 |
| 2 | $1,300 | 10.71% | 0.21 |
| 3 | $1,500 | 12.36% | 0.37 |
| 4 | $2,650 | 21.83% | 0.87 |
| 6 | $500 | 4.12% | 0.25 |
| 8 | $1,362 | 11.22% | 0.90 |
| 9 | $1,400 | 11.53% | 1.04 |
| 19 | $500 | 4.12% | 0.78 |
| 26 | $25 | 0.21% | 0.05 |
| 28 | $950 | 7.83% | 2.19 |
| 29 | $500 | 4.12% | 1.19 |
| **Total** | **$12,139** | **100%** | **7.92 years** |

Model implementation (wacccalc.xls): inputs are book value of straight debt (B29), interest expense on debt (B30) and average maturity in years (B31). Market value of straight debt C55 = B30 × [1 − (1 + r)^(−B31)] / r + B29 / (1 + r)^B31, with r = B37, the pre-tax cost of debt. In the saved Facebook example: 56 × 2.801637 + 1,000 / 1.035³ = 1,058.83 against book debt of 1,000, because the 5.6% embedded coupon rate exceeds the 3.5% current cost of debt.

**Worked examples:**

*Disney, 2013.* Book debt $14,288 million; interest expense $349 million; weighted-average maturity 7.92 years; current pre-tax cost of debt 3.75%.
Market value of debt = 349 × [1 − 1.0375^(−7.92)] / 0.0375 + 14,288 / 1.0375^7.92 = **$13,028 million**.
It sits below book because the $349m interest expense implies an average coupon of about 2.4% on $14,288m, and the debt is being discounted at a higher current rate of 3.75%. Adding capitalized operating leases of $2,933 million gives total debt of $15,961 million.

*Embraer, 2004 (millions of Brazilian reais).* Book debt 1,953; interest expense 222; average maturity 4 years; pre-tax cost of debt 9.29%.
Market value of debt = 222 × (present value of a 4-year annuity at 9.29%) + 1,953 / 1.0929⁴ = **2,083 million BR**.
Here market exceeds book, because the implied coupon (222 / 1,953 ≈ 11.4%) is above the 9.29% current rate. Note the contrast with book equity of 3,350m BR against a market equity of 11,042m BR — the equity gap is far larger than the debt gap, which is exactly why book-value weights distort the cost of capital.

**Determinism:**
- DETERMINISTIC: book debt, interest expense, weighted-average maturity and the pre-tax cost of debt → market value of debt. The weighted-average maturity itself is deterministic from the disclosed schedule.
- JUDGMENT: the maturity when the schedule is missing or lumpy. The 3-year default is a convention, not a measurement. Judgment needs the firm's disclosed tranches, its refinancing history, and whether a revolver is genuinely short-term or perpetually rolled.
- JUDGMENT: whether to treat undisclosed debt as having the same average maturity as the disclosed portion. The Disney example does exactly that.
- JUDGMENT: whether the interest expense in the income statement corresponds to the debt on the balance sheet (mid-year issuance, capitalized interest, and interest income netting all break the correspondence).

**Pitfalls:**
- Using book debt in the weights because "debt trades near par". It does not, once rates or credit quality move.
- Discounting at the historical coupon rate instead of the current cost of debt. That returns book value by construction and defeats the exercise.
- Forgetting to add capitalized operating leases to the market value of debt as well as the book value.
- Using the disclosed footnote total ($12,139m for Disney) as the face value instead of full book debt ($14,288m).
- Ignoring the short-maturity tranches when computing the weighted average, which biases M upward.
- Applying the after-tax cost of debt as the discount rate. Use the pre-tax rate; the bond's cash flows are pre-tax.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.196-197, p.199-200
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.111
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.108
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls straight-debt block (B29-B31, C55) and MV_debt aggregation (C62)

**Related:** [[market-value-weights]], [[operating-leases-as-debt]], [[what-counts-as-debt]], [[convertible-debt-decomposition]], [[cost-of-debt-estimation-routes]], [[cost-of-capital-assembly]]
