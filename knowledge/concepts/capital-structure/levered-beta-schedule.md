# Relevering beta across the debt-ratio schedule

**Core idea:** Equity gets riskier as a firm borrows, because the fixed claim of debt sits ahead of it. The levered beta formula prices exactly that: it scales the business-risk beta up by the debt-equity ratio, dampened by the tax shield. To build an optimal-capital-structure schedule you first strip leverage out of the observed beta to get an unlevered (asset) beta, then add leverage back at each candidate debt ratio. The unlevered beta is the one number in the schedule that should be estimated with care, because every cost of equity in the column depends on it.

**Formulas:**
- `β_L = β_u × (1 + (1 − t) × D/E)` — β_L = levered (equity) beta, β_u = unlevered (asset) beta, t = marginal tax rate, D/E = debt-to-equity ratio in market values.
- Unlever a regression beta: `β_u = β_regression / (1 + (1 − t) × D/E_average over the regression period)`.
- Bottom-up unlevered beta: `β_u = Σ_i w_i × β_u,i`, where the weights `w_i` are business values and `β_u,i` are sector unlevered betas. Business value is usually estimated as `Revenues_i × (EV/Sales)_i`.
- `D/E at a debt ratio d = d / (1 − d)`.
- `Cost of equity = Riskfree rate + β_L × Equity risk premium`.
- Private-firm variant: replace the market beta with a **total beta** = `market beta / correlation of the firm with the market`, because the owner is undiversified.

**Procedure:**
1. Estimate β_u. Prefer bottom-up: value-weight the unlevered betas of the businesses the firm operates in. Fall back to unlevering the firm's own regression beta at the average D/E over the regression window.
2. Note that if the firm holds significant cash, a full treatment nets it out before relevering; the capstru.xlsx implementation unlevers the current beta at the current D/E and leaves it there.
3. For each debt ratio d in the grid, compute D/E = d/(1−d).
4. Relever with the tax rate **actually used at that debt ratio**. That is the capped rate `t_used = MIN(t_EBIT, t_cap)` from [[tax-benefit-of-debt]], not the headline marginal rate. Once interest exceeds EBIT the shield shrinks and beta rises faster.
5. Apply CAPM to get the cost of equity at each d.
6. Stop the grid at 90%. At d = 100% the D/E ratio is infinite and the formula breaks.
7. For a private firm, run the whole schedule with total betas; the cost of equity is higher at every level and the optimum shifts.

**Reference data:** Disney's bottom-up unlevered beta build (2013):

| Business | Revenues | EV/Sales | Business value | Weight | Unlevered beta |
|---|---|---|---|---|---|
| Media Networks | $20,356m | 3.27 | $66,580m | 49.27% | 1.03 |
| Parks & Resorts | $14,087m | 3.24 | $45,683m | 33.81% | 0.70 |
| Studio Entertainment | $5,979m | 3.05 | $18,234m | 13.49% | 1.10 |
| Consumer Products | $3,555m | 0.83 | $2,952m | 2.18% | 0.68 |
| Interactive | $1,064m | 1.58 | $1,684m | 1.25% | 1.22 |
| **Disney Operations** | **$45,041m** | | **$135,132m** | **100%** | **0.9239** |

Disney's levered beta schedule (β_u = 0.9239, t = 36.1%, riskfree 2.75%, ERP 5.76%):

| Debt ratio | D/E | Levered beta | Cost of equity |
|---|---|---|---|
| 0% | 0.00% | 0.9239 | 8.07% |
| 10% | 11.11% | 0.9895 | 8.45% |
| 20% | 25.00% | 1.0715 | 8.92% |
| 30% | 42.86% | 1.1770 | 9.53% |
| 40% | 66.67% | 1.3175 | 10.34% |
| 50% | 100.00% | 1.5143 | 11.48% |
| 60% | 150.00% | 1.8095 | 13.18% |
| 70% | 233.33% | 2.3016 | 16.01% |
| 80% | 400.00% | 3.2856 | 21.68% |
| 90% | 900.00% | 6.2376 | 38.69% |

(At 70–90% the schedule actually used in the WACC table shows higher betas — 2.3762, 3.6289, 7.4074 — because the tax rate applied in the relevering falls once interest exceeds EBIT.)

**Worked example:** Disney's regression route. Regression beta 1.25, average D/E over the regression period 19.44%, t = 36.1%. β_u = 1.25 / (1 + 0.639 × 0.1944) = 1.1119. The bottom-up estimate of 0.9239 is lower and is the number carried forward, because it has a much smaller standard error. Relevering at 40% debt: D/E = 0.6667, β_L = 0.9239 × (1 + 0.639 × 0.6667) = 1.3175, ke = 2.75% + 1.3175 × 5.76% = 10.34%.

A second worked case (levbeta.xls): regression beta 1.40, t = 36%, average D/E 0.14 → β_u = 1.40 / (1 + 0.64 × 0.14) = 1.284875. Market value of debt = 876.282 × [1 − 1.075^−5]/0.075 + 12,342/1.075^5 = 12,142.263 against equity of 50,889.038, so current D/E = 0.23862 and current β_L = 1.284875 × (1 + 0.64 × 0.23862) = 1.481083. The full 0–90% schedule from the same β_u runs 1.2849, 1.3762, 1.4905, 1.6373, 1.8331, 2.1072, 2.5184, 3.2036, 4.5742, 8.6858.

**Determinism:**
- DETERMINISTIC: β_u + t + D/E → β_L; β_L + riskfree + ERP → cost of equity; business revenues + EV/Sales multiples + sector unlevered betas → bottom-up β_u; regression beta + average D/E + t → unlevered beta. Fully scriptable.
- JUDGMENT: choosing the business breakdown and the comparable sector betas; choosing EV/Sales multiples to value the businesses; deciding between the regression and bottom-up beta; deciding to use total betas for a private or closely held firm; picking the equity risk premium and riskfree rate.

**Pitfalls:**
- Using the regression beta directly in the schedule. It already embeds the firm's historical leverage.
- Relevering with the headline tax rate at debt ratios where the tax benefit is capped.
- Unlevering at the *current* D/E when the regression period had a different average leverage.
- Ignoring cash: a cash-heavy firm's observed beta is diluted toward zero.
- Extending the grid to 100% debt.
- Using a market beta for an undiversified owner's firm, which understates the cost of equity badly.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.44
- corporate_finance--lecture_slides--cfpacket2spr20 p.46
- corporate_finance--lecture_slides--cfpacket2spr20 p.71 (total beta for a private firm)
- corpfin-capital-structure — levbeta.xls (unlever/relever utility) and capstru.xlsx `Optimal Capital Structure` rows 49-50

**Related:** [[cost-of-capital-approach]], [[tax-benefit-of-debt]], [[bottom-up-beta]], [[total-beta]], [[optimal-debt-ratio-by-firm-type]], [[synthetic-rating-and-cost-of-debt]]
