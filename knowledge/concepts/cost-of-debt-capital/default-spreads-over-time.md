# Default spreads over time

**Core idea:** A default spread is the extra yield a bond of a given rating pays over the government bond of the same currency and maturity. Two facts govern its use. First, spreads rise steeply and non-linearly as ratings fall — under half a percent at Aaa/AAA, roughly 15-20% at D. Second, the whole spread structure shifts with the credit cycle. Between January 2008 and January 2009 spreads roughly doubled to tripled at every rating. In March 2020 they spiked again and mostly reverted by November. So a rating-based cost of debt is only as current as the spread table behind it. Refresh the table at the valuation date; never carry last year's spreads.

**Formulas:**
- Pre-tax cost of debt = Riskfree rate (same currency, long term) + Default spread(rating, date).
- Spread is a function of two arguments: the rating AND the date. Treat the date as a real input, not a footnote.
- Movements in default spreads and in the equity risk premium travel together. The ERP row in the crisis table below moved from 4.37% to 6.43% while spreads tripled, then fell back.

**Procedure:**
1. Fix the valuation date.
2. Get the firm's rating (actual or synthetic).
3. Pull the spread table AS OF the valuation date. Corporate bond spread data by rating is published by data services; Damodaran's spreadsheets note bondsonline.com as a refresh source and his own January updates as the annual vintage.
4. Read the spread for the rating. Add it to the riskfree rate in the valuation currency.
5. If the valuation date sits inside a credit dislocation (late 2008, March 2020), decide explicitly whether to use the crisis-date spread or a normalized one. Using the crisis-date spread is internally consistent if you also use the crisis-date ERP and crisis-date riskfree rate.
6. Re-check that the spread vintage matches the equity risk premium vintage used in the cost of equity. Mixing a 2020 ERP with 2013 spreads is inconsistent.

**Reference data:**

**(A) Through the 2008 crisis and aftermath.** Default spreads over treasuries by rating; bottom row is the equity risk premium at each date.

| Rating | 1-Jan-08 | 12-Sep-08 | 12-Nov-08 | 1-Jan-09 | 1-Jan-10 | 1-Jan-11 |
|---|---|---|---|---|---|---|
| Aaa/AAA | 0.99% | 1.40% | 2.15% | 2.00% | 0.50% | 0.55% |
| Aa1/AA+ | 1.15% | 1.45% | 2.30% | 2.25% | 0.55% | 0.60% |
| Aa2/AA | 1.25% | 1.50% | 2.55% | 2.50% | 0.65% | 0.65% |
| Aa3/AA− | 1.30% | 1.65% | 2.80% | 2.75% | 0.70% | 0.75% |
| A1/A+ | 1.35% | 1.85% | 3.25% | 3.25% | 0.85% | 0.85% |
| A2/A | 1.42% | 1.95% | 3.50% | 3.50% | 0.90% | 0.90% |
| A3/A− | 1.48% | 2.15% | 3.75% | 3.75% | 1.05% | 1.00% |
| Baa1/BBB+ | 1.73% | 2.65% | 4.50% | 5.25% | 1.65% | 1.40% |
| Baa2/BBB | 2.02% | 2.90% | 5.00% | 5.75% | 1.80% | 1.60% |
| Baa3/BBB− | 2.60% | 3.20% | 5.75% | 7.25% | 2.25% | 2.05% |
| Ba1/BB+ | 3.20% | 4.45% | 7.00% | 9.50% | 3.50% | 2.90% |
| Ba2/BB | 3.65% | 5.15% | 8.00% | 10.50% | 3.85% | 3.25% |
| Ba3/BB− | 4.00% | 5.30% | 9.00% | 11.00% | 4.00% | 3.50% |
| B1/B+ | 4.55% | 5.85% | 9.50% | 11.50% | 4.25% | 3.75% |
| B2/B | 5.65% | 6.10% | 10.50% | 12.50% | 5.25% | 5.00% |
| B3/B− | 6.45% | 9.40% | 13.50% | 15.50% | 5.50% | 6.00% |
| Caa/CCC+ | 7.15% | 9.80% | 14.00% | 16.50% | 7.75% | 7.75% |
| **ERP** | 4.37% | 4.52% | 6.30% | 6.43% | 4.36% | 5.20% |

**(B) The COVID spike and reversion, 2020.**

| Rating | 14-Feb-20 | 20-Mar-20 | 1-Nov-20 |
|---|---|---|---|
| AAA | 0.69% | 1.43% | 0.73% |
| AA | 0.72% | 2.64% | 0.80% |
| A | 0.80% | 3.15% | 0.84% |
| BBB | 1.33% | 3.73% | 1.57% |
| BB | 1.93% | 7.45% | 3.49% |
| B | 3.40% | 10.74% | 5.24% |
| CCC or lower | 9.65% | 17.81% | 10.83% |

**(C) January vintages used in the packets.** The January 2021 and January 2020 slides plot spreads by rating class for each January from 2015 onward; exact values appear only graphically. Shape: well under 1% at Aaa/AAA rising to roughly 15-20% at D2/D, with 2016 the widest year at the low-grade end and 2017-2018 tighter. The January-2021 chart shows roughly 17.5% at D2/D.

**(D) Point-in-time spread columns embedded in the models** (useful as concrete defaults):

| Rating | wacccalc.xls (Jan 2020 vintage) | ratings.xls vintage | Nov 2013 slide | 2004 slide |
|---|---|---|---|---|
| Aaa/AAA | 0.40% | 0.69% | 0.40% | 0.35% |
| Aa2/AA | 0.70% | 0.85% | 0.70% | 0.50% |
| A1/A+ | 0.90% | 1.07% | 0.85% | 0.70% |
| A2/A | 1.00% | 1.18% | 1.00% | 0.85% |
| A3/A− | 1.20% | 1.33% | 1.30% | 1.00% |
| Baa2/BBB | 1.75% | 1.71% | 2.00% | 1.50% |
| Ba1/BB+ | 2.75% | 2.31% | 3.00% | 2.00% |
| Ba2/BB | 3.25% | 2.77% | 4.00% | 2.50% |
| B1/B+ | 4.00% | 4.05% | 5.50% | 3.25% |
| B2/B | 5.00% | 4.86% | 6.50% | 4.00% |
| B3/B− | 6.00% | 5.94% | 7.25% | 6.00% |
| Caa/CCC | 10.00% | 9.46% | 8.75% | 8.00% |
| Ca2/CC | 8.00% | 9.97% | 9.50% | 10.00% |
| C2/C | 7.00% | 13.09% | 10.50% | 12.00% |
| D2/D | 12.00% | 17.44% | 12.00% | 20.00% |

(The wacccalc rating labels below B3/B− are scrambled relative to spread monotonicity; see [[synthetic-rating]].)

**Worked example:** A Baa2/BBB-rated US industrial. On 1 January 2008 its default spread was 2.02%, so with a 4% riskfree rate its pre-tax cost of debt would have been 6.02%. One year later, on 1 January 2009, the same rating carried a 5.75% spread — a pre-tax cost of debt of 9.75% at the same riskfree rate, with nothing about the firm having changed. At a 30% debt ratio and a 35% tax rate, that spread move alone raises the cost of capital by 0.30 × 3.73% × 0.65 ≈ 0.73 percentage points.

**Determinism:**
- DETERMINISTIC: given a rating and a date, the spread is a table lookup; given a riskfree rate, the pre-tax cost of debt follows immediately.
- JUDGMENT: which date's spreads to use during a dislocation, and whether to normalize. The judgment needs the valuation's purpose (a mark-to-market transaction price argues for current spreads; a long-horizon intrinsic valuation may argue for a normalized level), plus the corresponding decision on the ERP and riskfree rate so all three are internally consistent.
- JUDGMENT: sourcing. The published spread series differ slightly between vendors and between Damodaran's vintages, as the table above shows.

**Pitfalls:**
- Reusing a spread table from a prior year because "spreads don't move much". They move a lot.
- Using current spreads with a stale ERP, or vice versa.
- Assuming spreads are proportional to ratings. They are convex — the jump from BB to B is far larger than from AA to A.
- Adding a corporate default spread on top of a riskfree rate drawn from a different currency.
- Confusing a corporate default spread (this concept) with a sovereign/country default spread (see [[country-risk-in-cost-of-debt]]). They are different numbers with different sources, and an emerging-market corporate may need both.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.192
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.106-108
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.104-105
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls spread columns and the "spreads can be updated from bondsonline.com" note
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Synthetic rating` spread columns and rating→spread map

**Related:** [[synthetic-rating]], [[cost-of-debt-estimation-routes]], [[country-risk-in-cost-of-debt]], [[synthetic-vs-actual-rating]], [[equity-risk-premium]], [[riskfree-rate]]
