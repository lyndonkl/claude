# The cost of capital approach to the optimal debt ratio

**Core idea:** Firm value is the present value of expected cash flows to the firm, discounted at the cost of capital. Hold the cash flows fixed and the debt ratio that minimizes the cost of capital maximizes firm value. The whole method is one schedule: at each debt ratio from 0% to 90%, relever the beta to get a cost of equity, infer a bond rating from the interest coverage ratio to get a cost of debt, cap the tax benefit if interest outgrows earnings, weight the two, and read off the minimum. The curve is U-shaped because two forces fight. Substituting cheap debt for expensive equity pulls the cost of capital down; the rising cost of equity, the deteriorating rating and the dying tax shield push it back up.

**Formulas:**
- `Cost of capital = ke × E/(D+E) + kd_pretax × (1 − t_used) × D/(D+E)`, where ke = cost of equity, kd_pretax = riskfree rate + default spread (+ country default spread), t_used = the tax rate after the EBIT/deductibility caps ([[tax-benefit-of-debt]]).
- `ke = Riskfree rate + Levered beta × Equity risk premium`; `β_L = β_u × (1 + (1 − t_used) × D/E)` ([[levered-beta-schedule]]).
- `D/E = d / (1 − d)` where `d = D/(D+E)`.
- `$ Debt at d = d × (current MV equity + current total debt including leases)` — the capital base is held constant across the schedule.
- `Interest expense at d = kd_pretax(d) × $Debt(d)` (assuming all debt is refinanced at the new rate).
- `Interest coverage ratio = EBIT / Interest expense` → synthetic rating → default spread ([[synthetic-rating-and-cost-of-debt]]).
- Firm value at d, incremental form (capstru.xlsx): `V(d) = EV_current × [1 + (WACC_current − WACC_d) / (WACC_d − g)]`, with `g = min(implied growth, riskfree rate)`.
- Implied growth backed out of the current price: `g = (EV × WACC_current − FCFF) / (EV + FCFF)`, where `FCFF = EBIT(1 − t) + Depreciation − Capex − ΔNon-cash WC`.
- Textbook growing-perpetuity form: `V = CF_0 (1+g) / (WACC − g)`.

**Procedure:**
1. **Set the base.** Compute current market value of equity (shares × price) and market value of debt, including capitalized leases. Total capital = E + D; enterprise value = E + D − cash.
2. **Restate operations for leases.** Adjust EBITDA, depreciation, EBIT and interest expense for capitalized operating leases before anything else ([[debt-vs-equity-choices]]).
3. **Get the unlevered beta.** Prefer a bottom-up, business-value-weighted unlevered beta; the regression alternative is `β_u = regression beta / (1 + (1 − t) × average D/E over the regression period)` ([[levered-beta-schedule]]).
4. **Hold constant across the whole schedule:** EBITDA, depreciation, EBIT, capex, the riskfree rate, the ERP, the marginal tax rate, and total capital. Only the mix changes.
5. **For each d in {0%, 10%, …, 90%}:**
   a. D/E = d/(1−d); $Debt = d × total capital.
   b. Solve the circular rating problem: guess a rate, compute interest, compute coverage = EBIT/interest, look up the rating and rate, repeat until the rating implied equals the rating used ([[synthetic-rating-and-cost-of-debt]]).
   c. Compute `t_used = MIN(t_EBIT, t_cap)` ([[tax-benefit-of-debt]]).
   d. Relever beta with `t_used`; compute ke.
   e. After-tax cost of debt = kd_pretax × (1 − t_used).
   f. WACC = ke × (1 − d) + after-tax kd × d.
   g. Firm value at d, using the incremental formula above (or the distress-adjusted FCFF perpetuity if indirect bankruptcy costs are on).
6. **Pick the optimum.** With no indirect bankruptcy costs, the minimum-WACC ratio is also the maximum-value ratio. With them on, select on maximum firm value, since operating income now varies with d.
7. **Report the gap.** Excess debt capacity = optimal dollar debt − current debt. Then value the move ([[recapitalization-and-buyback-price]]) and stress-test it ([[downside-risk-and-rating-constraints]]).

**Reference data:** Disney's full schedule (November 2013 analysis; riskfree 2.75%, ERP 5.76%, β_u = 0.9239, marginal tax rate 36.1%, lease-adjusted EBIT $10,032m, total capital $137,839m):

| Debt ratio | Beta | Cost of equity | Rating | Pre-tax kd | Tax rate | After-tax kd | WACC |
|---|---|---|---|---|---|---|---|
| 0% | 0.9239 | 8.07% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 8.07% |
| 10% | 0.9895 | 8.45% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 7.81% |
| 20% | 1.0715 | 8.92% | Aaa/AAA | 3.15% | 36.10% | 2.01% | 7.54% |
| 30% | 1.1770 | 9.53% | Aa2/AA | 3.45% | 36.10% | 2.20% | 7.33% |
| **40%** | **1.3175** | **10.34%** | **A2/A** | **3.75%** | **36.10%** | **2.40%** | **7.16%** |
| 50% | 1.5143 | 11.48% | B3/B- | 10.00% | 36.10% | 6.39% | 8.93% |
| 60% | 1.8095 | 13.18% | Caa/CCC | 11.50% | 36.10% | 7.35% | 9.68% |
| 70% | 2.3762 | 16.44% | Caa/CCC | 11.50% | 32.64% | 7.75% | 10.35% |
| 80% | 3.6289 | 23.66% | Ca2/CC | 12.25% | 26.81% | 8.97% | 11.90% |
| 90% | 7.4074 | 45.43% | C2/C | 13.25% | 22.03% | 10.33% | 13.84% |

Underlying debt/interest schedule: $Debt runs $0 / $13,784 / $27,568 / $41,352 / $55,136 / $68,919 / $82,703 / $96,487 / $110,271 / $124,055m; interest $0 / $434 / $868 / $1,427 / $2,068 / $6,892 / $9,511 / $11,096 / $13,508 / $16,437m; coverage ∞ / 23.10 / 11.55 / 7.03 / 4.85 / 1.46 / 1.05 / 0.90 / 0.74 / 0.61.

Disney's current (pre-move) cost of capital: ke = 2.75% + 1.0013 × 5.76% = 8.52%; after-tax kd = 3.75% × (1 − 0.361) = 2.40%; weights E = $121,878m, D = $15,961m → WACC = 7.81%.

Disney's lease-adjusted financials used in the schedule: revenues $45,041m; EBITDA $12,517m; depreciation $2,485m; EBIT $10,032m; interest $459m (unadjusted: EBITDA $10,642m, D&A $2,192m, EBIT $9,450m, interest $349m).

Stylized textbook illustration of the same shape (firm with $200m cash flow growing 3% forever):

| d | Cost of equity | After-tax kd | WACC | Firm value |
|---|---|---|---|---|
| 0% | 10.50% | 4.80% | 10.50% | $2,747 |
| 20% | 11.60% | 5.40% | 10.36% | $2,799 |
| **40%** | **13.10%** | **5.70%** | **10.14%** | **$2,885** |
| 60% | 15.00% | 7.20% | 10.32% | $2,814 |
| 80% | 17.20% | 9.00% | 10.64% | $2,696 |
| 100% | 19.70% | 11.40% | 11.40% | $2,452 |

**Worked example:** Disney at 40%. $Debt = 0.40 × 137,839 = $55,136m. Iterating the rating: at an A2/A rate of 3.75%, interest = $2,068m, coverage = 10,032/2,068 = 4.85, which falls in the 4.25–5.5 band → A2/A. The guess is consistent, so stop. D/E = 40/60 = 66.67%, so β_L = 0.9239 × (1 + 0.639 × 0.6667) = 1.3175 and ke = 2.75% + 1.3175 × 5.76% = 10.34%. Interest ($2,068m) is far below EBIT ($10,032m), so t stays 36.1% and after-tax kd = 2.40%. WACC = 10.34% × 0.60 + 2.40% × 0.40 = 7.16% — the minimum across the schedule. Disney's optimal dollar debt is $55.1B against $15.96B outstanding, so excess debt capacity is about $39.14B.

**Determinism:**
- DETERMINISTIC: given β_u, riskfree rate, ERP, marginal tax rate, EBIT, EBITDA, depreciation, capex, current equity and debt values, cash, and a ratings table → the entire schedule (D/E, $debt, interest, coverage, rating, kd, t_used, β_L, ke, WACC, firm value) and the argmin/argmax. The only subtlety is the fixed-point iteration inside step 5b.
- JUDGMENT: which EBIT to use (current vs. normalized), which unlevered beta, which ratings table (large/stable vs. small/risky), the marginal tax rate, whether existing debt is refinanced at the new rate, whether to turn on indirect bankruptcy costs, and whether the growth rate implied by the current price is credible.

**Pitfalls:**
- **It is static.** Operating income is the single most critical number, and it is held fixed. If EBIT changes, the optimum changes ([[downside-risk-and-rating-constraints]]).
- **It ignores indirect bankruptcy costs.** Operating income is assumed unaffected by a collapse in the rating, which is false for firms selling durable goods or services ([[enhanced-cost-of-capital-approach]]).
- **Rigid risk assumptions.** The method assumes market risk scales exactly with the levered-beta formula and default risk exactly with coverage-based ratings.
- Forgetting to hold total capital constant, or letting EBIT drift with the debt ratio in the standard version.
- Forgetting the tax cap at high debt ratios; without it the curve keeps falling and the optimum runs to 90%.
- Forgetting to relever beta with the *reduced* tax rate once the cap binds. This is why Disney's 70–90% betas differ from a constant-t calculation.
- Reading the kink in the curve as an error. Disney's 1997 analysis dips slightly at 70% after rising at 60%; that comes from the interaction of the rating-driven cost of debt with the capped tax benefit.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.37-38
- corporate_finance--lecture_slides--cfpacket2spr20 p.40-43
- corporate_finance--lecture_slides--cfpacket2spr20 p.45
- corporate_finance--lecture_slides--cfpacket2spr20 p.50-54
- corporate_finance--lecture_slides--cfpacket2spr20 p.75
- corpfin-capital-structure — capstru.xlsx, sheets `Inputs`, `Optimal Capital Structure` (rows 46-77), `Summary Table`

**Related:** [[levered-beta-schedule]], [[synthetic-rating-and-cost-of-debt]], [[tax-benefit-of-debt]], [[recapitalization-and-buyback-price]], [[downside-risk-and-rating-constraints]], [[enhanced-cost-of-capital-approach]], [[apv-approach]], [[optimal-debt-ratio-by-firm-type]], [[determinants-of-optimal-debt-ratio]], [[bottom-up-beta]], [[fcff]]
