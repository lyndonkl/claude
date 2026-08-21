# The enhanced cost of capital approach (indirect bankruptcy costs)

**Core idea:** The standard schedule holds operating income fixed while the rating falls from AAA to C. That is not how distress works. Customers defer purchases, suppliers tighten terms, employees leave, and operating income drops — the indirect costs of bankruptcy. The enhanced approach builds these in: at each debt ratio, after inferring the rating, haircut EBITDA by an amount tied to that rating, then compute the cost of capital and firm value on the reduced income. The optimum is now chosen on **maximum firm value**, not minimum cost of capital, because the cash flows themselves vary with the debt ratio. In practice the optimum often barely moves; what changes dramatically is the penalty for overshooting it. The value cliff past the optimum becomes far steeper, which is the real lesson.

**Formulas:**
- `EBITDA(d) = EBITDA_base × (1 + drop(rating(d)))`, where `drop` is a negative fraction from the distress table.
- `EBIT(d) = EBITDA(d) − Depreciation` (depreciation is held constant).
- The rest of the schedule follows [[cost-of-capital-approach]], but with EBIT(d) feeding both the coverage ratio and the value.
- Firm value with distress on: `V(d) = [EBIT(d) × (1 − t) − (Capex − Depreciation)] × (1 + g) / (WACC(d) − g)`, with g the growth rate implied by the current price.
- Normalization of the base: if the firm is *already* distressed at its current rating, gross up the base — `EBITDA_base = Current EBITDA / (1 + drop(current rating))`.
- Optimal `d* = argmax_d V(d)`.

**Procedure:**
1. Choose a distress severity: Low, Medium or High indirect bankruptcy costs. Base it on how much the firm's business depends on customer confidence in its survival. Durable goods, long-service products, and intangible/people-based businesses take High; immediate-consumption businesses take Low.
2. Normalize current EBITDA up to a no-distress level if the firm's current rating already carries a haircut.
3. Run the schedule as usual, but after the rating is determined at each debt ratio, apply the EBITDA drop for that rating before computing EBIT, coverage, taxes and value. Note the added circularity: the haircut depends on the rating, and the rating depends on EBIT.
4. Select the debt ratio with the highest firm value.
5. Report the value profile, not just the optimum. Show how fast value falls one and two steps past the optimum.
6. Consider the dynamic variant as an alternative: instead of a single operating income, draw from a distribution of operating income outcomes and evaluate the debt ratio across the distribution.

**Reference data:** Drop in EBITDA by rating, under Low / Medium / High indirect bankruptcy cost assumptions. (The lecture version is keyed to the rating the firm falls *to*; the capstru.xlsx version is wired to the full rating ladder, with the Medium column being the one hard-wired into the ratings tables.)

*capstru.xlsx table (current vintage, full ladder):*

| Rating | Low | Medium | High |
|---|---|---|---|
| Aaa/AAA | 0 | 0 | 0 |
| Aa2/AA | 0 | 0 | 0 |
| A1/A+ | 0 | 0 | 0 |
| A2/A | 0 | 0 | −2% |
| A3/A- | 0 | −2% | −5% |
| Baa2/BBB | −5% | −10% | −15% |
| Ba1/BB+ | −10% | −20% | −25% |
| Ba2/BB | −10% | −20% | −25% |
| B1/B+ | −10% | −20% | −25% |
| B2/B | −10% | −20% | −25% |
| B3/B- | −15% | −25% | −30% |
| Caa/CCC | −25% | −40% | −50% |
| Ca2/CC | −25% | −40% | −50% |
| C2/C | −25% | −40% | −50% |
| D2/D | −30% | −50% | −100% |

*Lecture version (Disney), keyed to the rating the firm falls to:* To A: 0 / 0 / 2%; To A-: 0 / 2% / 5%; To BBB: 5% / 10% / 15%; To BB+: 10% / 20% / 25%; To B-: 15% / 25% / 30%; To C: 25% / 40% / 50%; To D: 30% / 50% / 100%.

**Worked example:** Disney's schedule re-run with distress-adjusted operating income:

| d | Beta | ke | Rating | kd pre-tax | Tax rate | kd after-tax | WACC | Enterprise value |
|---|---|---|---|---|---|---|---|---|
| 0% | 0.9239 | 8.07% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 8.07% | $122,633m |
| 10% | 0.9895 | 8.45% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 7.81% | $134,020m |
| 20% | 1.0715 | 8.92% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 7.54% | $147,739m |
| 30% | 1.1769 | 9.53% | Aa2/AA | 3.45% | 36.10% | 2.20% | 7.33% | $160,625m |
| **40%** | **1.3175** | **10.34%** | **A2/A** | **3.75%** | **36.10%** | **2.40%** | **7.16%** | **$172,933m** |
| 50% | 1.5573 | 11.72% | C2/C | 11.50% | 31.44% | 7.88% | 9.80% | $35,782m |
| 60% | 1.9946 | 14.24% | Caa/CCC | 13.25% | 22.74% | 10.24% | 11.84% | $25,219m |
| 70% | 2.6594 | 18.07% | Caa/CCC | 13.25% | 19.49% | 10.67% | 12.89% | $21,886m |
| 80% | 3.9892 | 25.73% | Caa/CCC | 13.25% | 17.05% | 10.99% | 13.94% | $19,331m |
| 90% | 7.9783 | 48.72% | Caa/CCC | 13.25% | 15.16% | 11.24% | 14.99% | $17,311m |

The optimum stays at 40%. But enterprise value collapses from $172,933m at 40% to $35,782m at 50%, because the rating falls all the way to C2/C and the distress haircut guts EBITDA. Under the standard approach the same step cost far less. The message to management is not "borrow to 40%" but "40% is fine and 50% is catastrophic."

**Determinism:**
- DETERMINISTIC: given a distress table and the standard inputs, the whole schedule and the value-maximizing ratio. The added rating-to-haircut lookup is another fixed-point loop.
- JUDGMENT: choosing Low/Medium/High severity — this is a pure assumption about how much customers, suppliers and employees would punish a distressed firm; deciding whether the firm's current income is already distress-impaired; specifying an operating income distribution for the dynamic variant.

**Pitfalls:**
- Selecting on minimum WACC when distress costs are on. Once operating income varies with the debt ratio, only firm value is a valid objective.
- Assuming the optimum will shift. Often it does not; the value profile is where the information is.
- Applying High severity to a grocery-style business or Low severity to an aircraft manufacturer. Match the haircut to how much the customer's purchase depends on the firm surviving.
- Double-counting: layering a rating constraint on top of a distress-adjusted schedule ([[downside-risk-and-rating-constraints]]).
- Forgetting to gross up a currently distressed firm's EBITDA before running the schedule, which double-penalizes it.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.75-78
- corpfin-capital-structure — capstru.xlsx, `Input choices page` (indirect bankruptcy cost table), `Optimal Capital Structure` rows 51-52, F44, row 77

**Related:** [[cost-of-capital-approach]], [[synthetic-rating-and-cost-of-debt]], [[apv-approach]], [[downside-risk-and-rating-constraints]], [[debt-equity-tradeoff]], [[pathways-to-the-optimal-debt-ratio]]
