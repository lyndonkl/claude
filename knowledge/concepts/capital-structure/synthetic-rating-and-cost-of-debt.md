# Synthetic ratings and the cost of debt at each debt ratio

**Core idea:** You cannot ask a ratings agency what a firm would be rated at a hypothetical 60% debt ratio, so you infer it. The interest coverage ratio (EBIT/interest expense) maps to a bond rating through a lookup table; the rating maps to a default spread; the spread plus the riskfree rate gives the pre-tax cost of debt. The calculation is circular: the rate determines the interest expense, the interest expense determines coverage, and coverage determines the rate. Solve it by fixed-point iteration at each debt ratio. This synthetic rating machinery is also how the model prices default risk for an unrated firm at its *current* leverage.

**Formulas:**
- `Interest coverage ratio = EBIT / Interest expense` (use lease-adjusted EBIT and lease-adjusted interest). If interest = 0, set coverage to a very large number (the spreadsheet uses 10,000,000) so the top rating applies.
- `Pre-tax cost of debt = Riskfree rate + Default spread(rating) + Country default spread`.
- `Interest expense at debt ratio d = Pre-tax cost of debt(d) × $Debt(d)` when all debt is refinanced at the new rate.
- If existing debt is *not* refinanced: `Interest = Old interest + rate(d) × ($Debt(d) − current debt)` for d above the current ratio, and `Interest = (Old interest / Book debt) × $Debt(d)` below it.
- `After-tax cost of debt = Pre-tax cost of debt × (1 − t_used)`.
- Alternative coverage-style metric reported alongside: `Funds from operations / Debt = (Net income + Depreciation) / $Debt`.

**Procedure:**
1. Choose the ratings table. Table 1 is for large, stable (manufacturing-type) firms; table 2 applies stricter coverage thresholds for smaller and riskier firms. Financial service firms need their own spreads entirely ([[financial-firm-capital-structure]]).
2. Compute lease-adjusted EBIT once, and hold it fixed across the schedule (unless indirect bankruptcy costs are on).
3. At each debt ratio: start from a guessed rate (the top-rating rate works).
4. Interest = rate × $Debt. Coverage = EBIT / Interest.
5. Look up the rating: the matching row is the last one whose lower bound is ≤ coverage (Excel approximate-match VLOOKUP semantics).
6. Read the default spread, add the riskfree rate and any country default spread, and get a new rate.
7. If the new rate differs from the guess, repeat. Stop when the rating implied equals the rating used. Watch for a two-cycle between adjacent ratings; if it oscillates, take the worse rating (or dampen the iteration).
8. Negative EBIT gives negative coverage, which falls in the bottom band → D rating.
9. Apply the tax cap, then compute the after-tax cost of debt ([[tax-benefit-of-debt]]).

**Reference data:**

*Current-vintage table shipped with capstru.xlsx — Table 1, "large/stable firms"* (spreads in %, applied as riskfree + spread + country spread):

| Coverage > | Coverage ≤ | Rating | Default spread |
|---|---|---|---|
| −100000 | 0.199999 | D2/D | 14.34% |
| 0.20 | 0.649999 | C2/C | 10.76% |
| 0.65 | 0.799999 | Ca2/CC | 8.80% |
| 0.80 | 1.249999 | Caa/CCC | 7.78% |
| 1.25 | 1.499999 | B3/B- | 4.62% |
| 1.50 | 1.749999 | B2/B | 3.78% |
| 1.75 | 1.999999 | B1/B+ | 3.15% |
| 2.00 | 2.249999 | Ba2/BB | 2.15% |
| 2.25 | 2.49999 | Ba1/BB+ | 1.93% |
| 2.50 | 2.999999 | Baa2/BBB | 1.59% |
| 3.00 | 4.249999 | A3/A- | 1.29% |
| 4.25 | 5.499999 | A2/A | 1.14% |
| 5.50 | 6.499999 | A1/A+ | 1.03% |
| 6.50 | 8.499999 | Aa2/AA | 0.82% |
| 8.50 | 100000 | Aaa/AAA | 0.67% |

*Table 2, "smaller and riskier firms"* — same ratings and spreads, higher coverage thresholds: D2/D < 0.5; C2/C 0.5–0.8; Ca2/CC 0.8–1.25; Caa/CCC 1.25–1.5; B3/B- 1.5–2; B2/B 2–2.5; B1/B+ 2.5–3; Ba2/BB 3–3.5; Ba1/BB+ 3.5–4; Baa2/BBB 4–4.5; A3/A- 4.5–6; A2/A 6–7.5; A1/A+ 7.5–9.5; Aa2/AA 9.5–12.5; Aaa/AAA > 12.5.

*The lecture-packet version of table 1 (2013 vintage, T.Bond rate 2.75%)*, showing the resulting interest rates directly:

| Coverage | Rating | Spread | Interest rate |
|---|---|---|---|
| > 8.50 | Aaa/AAA | 0.40% | 3.15% |
| 6.5 – 8.5 | Aa2/AA | 0.70% | 3.45% |
| 5.5 – 6.5 | A1/A+ | 0.85% | 3.60% |
| 4.25 – 5.5 | A2/A | 1.00% | 3.75% |
| 3 – 4.25 | A3/A- | 1.30% | 4.05% |
| 2.5 – 3 | Baa2/BBB | 2.00% | 4.75% |
| 2.25 – 2.5 | Ba1/BB+ | 3.00% | 5.75% |
| 2 – 2.25 | Ba2/BB | 4.00% | 6.75% |
| 1.75 – 2 | B1/B+ | 5.50% | 8.25% |
| 1.5 – 1.75 | B2/B | 6.50% | 9.25% |
| 1.25 – 1.5 | B3/B- | 7.25% | 10.00% |
| 0.8 – 1.25 | Caa/CCC | 8.75% | 11.50% |
| 0.65 – 0.8 | Ca2/CC | 9.50% | 12.25% |
| 0.2 – 0.65 | C2/C | 10.50% | 13.25% |
| < 0.2 | D2/D | 12.00% | 14.75% |

**Worked example:** Disney at a 30% debt ratio (2013 inputs: total capital $137,839m, lease-adjusted EBIT $10,032m, T.Bond 2.75%). $Debt = 0.30 × 137,839 = $41,352m. *Iteration 1*: price it at the AAA rate of 3.15% → interest = $1,303m → coverage = 10,032/1,303 = 7.70, which falls in the 6.5–8.5 band → Aa2/AA, not AAA. *Iteration 2*: reprice at the AA rate of 3.45% → interest = $1,427m → coverage = 10,032/1,427 = 7.03 → still Aa2/AA. Consistent, so stop: rating AA, pre-tax kd 3.45%, after-tax kd = 3.45% × (1 − 0.361) = 2.20%. Compare 20%: $Debt $27,568m, interest $868m, coverage 11.55 → AAA at 3.15%. And 50%: $Debt $68,919m, interest $6,892m, coverage 1.46 → B3/B- at 10.00% — the collapse from A to B- between 40% and 50% is what turns the cost of capital curve upward.

**Determinism:**
- DETERMINISTIC: EBIT + $Debt + riskfree rate + country spread + ratings table → rating, default spread, pre-tax and after-tax cost of debt at every debt ratio, via fixed-point iteration. A script reproduces this exactly.
- JUDGMENT: which ratings table applies (large/stable vs. small/risky vs. financial); whether to override the synthetic rating with an actual agency rating; whether to assume existing debt is refinanced at the new rate; what country default spread to add; whether the EBIT used is representative.

**Pitfalls:**
- Ignoring the circularity and pricing all debt levels at the current rate. That understates the cost of debt badly at high leverage.
- Using an unadjusted EBIT and interest expense when the firm has large operating leases.
- Applying the manufacturing-firm table to a bank. Even the safest banks come out with absurdly low ratings and near-zero optimal debt ratios.
- Letting a two-cycle in the iteration silently pick the more favorable rating.
- Treating the synthetic rating as an agency rating. It is a coverage-based proxy that ignores everything else agencies weigh.
- Forgetting the country default spread for firms in risky markets; it shifts the whole cost-of-debt column up.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.47-50
- corpfin-capital-structure — capstru.xlsx, sheets `Default Spreads and Ratios` and `Optimal Capital Structure` (rows 55, 62-65, lookup block D82:H96)

**Related:** [[cost-of-capital-approach]], [[tax-benefit-of-debt]], [[levered-beta-schedule]], [[enhanced-cost-of-capital-approach]], [[apv-approach]], [[financial-firm-capital-structure]], [[downside-risk-and-rating-constraints]]
