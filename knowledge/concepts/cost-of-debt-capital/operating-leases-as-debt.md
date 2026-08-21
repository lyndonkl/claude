# Operating leases as debt

**Core idea:** An operating lease commits the firm to fixed, tax-deductible payments, and non-payment costs it the asset. That is debt by every test Damodaran uses. Before 2019 accountants kept these commitments off the balance sheet and buried the rent in operating expenses. The fix is mechanical: discount the future lease commitments from the footnote at the firm's pre-tax cost of debt, add the present value to debt, and restate operating income by adding back the rent and subtracting depreciation on the newly created leased asset. This changes four things at once — debt goes up, operating income goes up, the interest coverage ratio changes, and invested capital goes up. Since 2019 IFRS 16 and ASC 842 require capitalization, but the accounting rules are far more complicated than this present-value calculation, so the manual conversion remains the reference method.

**Formulas:**
Let commitments for years 1-5 be C₁…C₅, the lump-sum commitment for "year 6 and beyond" be L, the current-year lease expense be R, and the pre-tax cost of debt be k_d.

1. Years embedded in the lump: n₆ = ROUND(L / mean(C₁…C₅), 0).
2. Annualized year-6+ payment: A = L / n₆.
3. Present value of explicit years: PV_t = C_t / (1 + k_d)^t for t = 1…5.
4. Present value of the year-6+ block, an n₆-year annuity starting at year 6:
   PV_beyond = A × [1 − (1 + k_d)^(−n₆)] / k_d × (1 + k_d)^(−5).
5. Debt value of leases = PV₁ + PV₂ + PV₃ + PV₄ + PV₅ + PV_beyond.
6. Lease life = 5 + n₆. Depreciation on the leased asset = Debt value of leases / Lease life (straight line).
7. Adjusted operating income (full method) = Reported EBIT + R − Depreciation on the leased asset.
8. Adjusted operating income (short-cut) = Reported EBIT + k_d × Debt value of leases.
9. Adjusted debt = Reported interest-bearing debt + Debt value of leases.
10. Adjusted interest expense (for coverage) = Reported interest expense + k_d × Debt value of leases.

**Procedure:**
1. Open the lease footnote. Pull the current-year operating-lease expense and the schedule of minimum commitments for years 1-5 plus the "thereafter" lump sum.
2. Choose the discount rate. Use the firm's PRE-TAX cost of debt, because lease payments carry the same default risk as the firm's other fixed commitments.
3. Estimate n₆ = round(lump / average of the first five commitments). This spreads the thereafter lump over a plausible number of years rather than pretending it all arrives in year 6.
4. Discount each of years 1-5, then the year-6+ annuity, and sum. That is the debt value of leases.
5. Add the debt value to both book and market value of debt.
6. Restate operating income. The full method adds back the whole rent and subtracts straight-line depreciation on the capitalized asset. The short-cut adds back only the implied interest. The full method is what the packet uses for Disney and the ratings spreadsheet; the short-cut is a fast approximation.
7. Restate interest expense by adding the imputed lease interest, then recompute the interest coverage ratio.
8. Recognize the circularity: the discount rate depends on the rating, the rating depends on lease-adjusted coverage, and lease-adjusted coverage depends on the discount rate. Iterate to a fixed point (Excel calls this iterative calculation; the spreadsheets require it to be enabled).
9. Add the capitalized lease value to invested capital when computing return on capital, so the numerator and denominator stay consistent.

Edge cases and implementation rules:
- Lump = 0 → set n₆ = 0, skip the annuity, and use lease life 5.
- All five commitments zero → mean is 0 and n₆ divides by zero. Guard it.
- ROUND here is half-away-from-zero (Excel), not banker's rounding. Use floor(x + 0.5) semantics.
- n₆ rounds to 0 for a small lump → treat the lump as a single year-6 payment or as zero; set lease life 5.
- k_d = 0 breaks the annuity formula → use n₆ × A undiscounted.
- The five-year footnote format is US GAAP-specific. Generalize the "5" constants if the disclosure differs.
- Timing convention when computing returns on capital: income adjustments use THIS year's lease schedule; capital adjustments use LAST year's lease debt, to match a beginning-of-period capital base.

**Reference data:** No lookup table. Two canonical parameter sets from the models:

*oplease.xls saved example:* current lease expense 2,500; commitments 2,000 / 2,000 / 2,000 / 1,800 / 1,600; thereafter 8,000; k_d 5.48%; reported EBIT 10,000; reported debt 25,000.

*wacccalc.xls saved example (Facebook):* current lease expense 180; commitments 156 / 150 / 145 / 143 / 140; thereafter 600; k_d 3.5%.

*ratings.xls saved example:* current lease expense 25; commitments 24 / 22 / 22 / 21 / 20; thereafter 111; k_d 4.18%; reported EBIT 50; reported debt 92.97; reported interest 8.

**Worked examples:**

*Disney, 2013 ($ millions, k_d = 3.75%).* Commitments and present values: year 1 $507.00 → $488.67; year 2 $422.00 → $392.05; year 3 $342.00 → $306.24; year 4 $272.00 → $234.76; year 5 $217.00 → $180.52. The $1,784 million beyond year 5 is annuitized as 5 years at $356.80 each (the average commitment over the first five years), with a present value of $1,330.69. Debt value of leases = $2,932.93 million. Added to the $13,028 million market value of interest-bearing debt, total debt outstanding = $15,961 million — the figure that produces Disney's 11.58% debt weight and its 7.81% cost of capital.

*oplease.xls, full arithmetic.* Mean of the first five commitments = 9,400 / 5 = 1,880. n₆ = round(8,000 / 1,880) = round(4.255) = 4. A = 8,000 / 4 = 2,000. PVs at 5.48%: 1,896.09, 1,797.59, 1,704.20, 1,454.09, 1,225.38. PV_beyond = 2,000 × [1 − 1.0548^(−4)] / 0.0548 ÷ 1.0548^5 = 5,371.39. Debt value of leases = 13,448.73. Lease life = 5 + 4 = 9, so depreciation = 13,448.73 / 9 = 1,494.30. Adjusted EBIT (full) = 10,000 + 2,500 − 1,494.30 = 11,005.70. Adjusted EBIT (short-cut) = 10,000 + 0.0548 × 13,448.73 = 10,736.99. Adjusted debt = 25,000 + 13,448.73 = 38,448.73.

*ratings.xls, showing the coverage feedback.* n₆ = round(111 / 21.8) = 5. A = 22.2. Debt value of leases = 177.01. Lease life = 10, so depreciation = 17.70. Adjusted operating income = 50 + 25 − 17.70 = 57.30. Adjusted debt = 92.97 + 177.01 = 269.98. Both the numerator and denominator of the coverage ratio move, which is why the rating must be solved iteratively.

**Determinism:**
- DETERMINISTIC: commitments, current lease expense and k_d → n₆, per-year present values, debt value of leases, depreciation, adjusted EBIT (both methods), adjusted debt, adjusted interest expense. A single function computes all of it: `capitalize_leases(commitments_1_5, lump_6plus, lease_expense, k_d) -> (debt_value, depreciation, oi_adjustment)`. The fixed-point iteration with the rating table is also mechanical.
- JUDGMENT: the discount rate to use before you have a rating (the seed value for the iteration), and whether to use the firm's pre-tax cost of debt or a secured-borrowing rate for asset-backed leases.
- JUDGMENT: the n₆ estimate when the footnote's "thereafter" lump is very large relative to the near-term commitments (long ground leases, airport gates), where rounding the ratio can badly misstate the tail.
- JUDGMENT: whether the disclosed minimum commitments understate the real obligation (contingent rent, percentage-of-sales rent in retail).

**Pitfalls:**
- Ignoring operating leases entirely. This understates debt, overstates the equity weight, overstates operating income quality and inflates return on invested capital.
- Discounting lease commitments at the cost of capital or the cost of equity. They are debt; use the pre-tax cost of debt.
- Treating the "thereafter" lump as a single year-6 payment. That understates its present value materially.
- Adding lease debt to the balance sheet but forgetting to restate operating income and interest expense, which leaves the coverage ratio inconsistent.
- Adding lease debt to invested capital but not to the debt used in the cost-of-capital weights, or vice versa.
- Not enabling iteration, so the circular rating/lease loop returns a reference error or a stale value. The ratings spreadsheet's own troubleshooting note is: on a REF! error, set the "operating leases?" flag to No and back to Yes.
- Assuming the post-2019 accounting numbers are equivalent to this calculation. IFRS 16 and ASC 842 balance doing the right thing against continuity with legacy rules, and firms lobbied for sector-specific modifications, so the reported lease liability may not match the present value of the commitments.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.185, p.197-199
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.118, p.120
- spreadsheet doc `corpfin-payout-projects` — oplease.xls, full algorithm, outputs and edge cases
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls `Operating Leases` sheet and the circularity/iteration note; returncalculator.xls dual lease converters and the timing convention
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Operating lease converter` sheet (C28, F31, F32, F33)

**Related:** [[what-counts-as-debt]], [[interest-coverage-ratio]], [[synthetic-rating]], [[market-value-of-debt]], [[market-value-weights]], [[cost-of-capital-assembly]], [[return-on-invested-capital]], [[earnings-adjustments]]
