# Optimal debt ratio via the cost-of-capital schedule

**Core idea:** Part VI of the corporate finance project computes the financing mix that minimises the cost of capital. The method is a grid search. Step the debt ratio from 10% to 90%, and at each level recompute three things: the levered beta and cost of equity, the synthetic rating and cost of debt implied by the resulting interest coverage, and the weighted cost of capital. The debt ratio with the lowest WACC is the optimum. The deliverable is two tables — the full schedule, and the hurdle-rate build-up at the optimum. The project then asks a separate question: with reasonable constraints imposed, what would you actually recommend?

**Formulas:**
- At each trial debt ratio D/(D+E):
  - Levered beta = Unlevered beta × (1 + (1 − t) × D/E).
  - Cost of equity = Rf + Levered beta × ERP.
  - Interest expense at that ratio = Debt × pre-tax cost of debt; coverage = EBIT / interest expense.
  - Coverage → synthetic rating → default spread → pre-tax cost of debt = Rf + spread. (This is circular and is solved iteratively.)
  - WACC = (E/(D+E)) × Cost of equity + (D/(D+E)) × Cost of debt × (1 − t).
- Optimal debt ratio = argmin over the grid of WACC.

**Procedure:**
1. Fix the unlevered beta, marginal tax rate, Rf, ERP and current EBIT.
2. For each debt ratio on the grid (10%, 20%, … 90%), relever the beta, recompute the cost of equity, solve for the coverage-implied rating and spread, and compute WACC.
3. Pick the minimum-WACC row as the mechanical optimum.
4. Rebuild the full hurdle-rate table at that optimum: relevered beta, cost of equity, bond rating, pre-tax interest rate on debt, marginal tax rate, after-tax cost of debt, and the minimised WACC.
5. Compare the optimum to the current debt ratio. Under-levered or over-levered, and by how much?
6. Cross-check against the qualitative prediction from Part V. The firm with the highest EBITDA/value should show the highest optimum. See [[qualitative-debt-tradeoff]].
7. Benchmark the *current* ratio against the industry average and against a cross-sectional regression prediction. See [[recapitalization-value-and-stress-test]].
8. Impose constraints and state the recommendation separately from the mechanical answer.
9. Feed the optimum forward. It becomes the growth-phase capital structure in the valuation and the target of the transition plan.

**Reference data:** Spring 2015 WACC schedule; optimum marked with an asterisk.

| Debt ratio | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| 10% | 6.55% | 6.22% | 6.12% | 6.59% |
| 20% | 6.34% | 6.02% | 6.00% | 6.37% |
| 30% | 6.25% | 5.91% | 5.90%* | 6.16% |
| 40% | 6.15%* | 5.78% | 8.55% | 6.07% |
| 50% | 8.81% | 5.72%* | 10.03% | 5.93% |
| 60% | 10.18% | 8.95% | 11.08% | 5.88%* |
| 70% | 11.88% | 10.39% | 12.13% | 9.45% |
| 80% | 12.93% | 12.20% | 13.18% | 11.00% |
| 90% | 13.98% | 13.25% | 14.23% | 11.95% |

Hurdle rates at the optimal debt ratio:

| Item | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Optimal debt ratio | 40% | 50% | 30% | 60% |
| Relevered beta | 1.11 | 1.19 | 0.92 | 1.59 |
| Cost of equity | 8.75% | 9.19% | 7.46% | 11.31% |
| Bond rating at optimum | A− | A− | A− | BBB |
| Pre-tax interest rate on debt | 3.47% | 3.47% | 3.47% | 3.47% |
| Marginal tax rate | 35% | 35% | 35% | 35% |
| After-tax cost of debt | 2.26% | 2.26% | 2.26% | 2.26% |
| Minimised WACC | 6.15% | 5.72% | 5.90% | 5.88% |

Current versus optimal (2015): SBUX 11.92% → 40%; MCD 34.99% → 50%; CMG 2.45% → 30%; TSN 35.54% → 60%. All four are under-levered.

Spreadsheets referenced by the course for this part: capstru.xls, capstruo.xls. Published data sets: earnings variance by industry; market debt ratio regression.

**Worked example:** Chipotle, 2015. Unlevered beta 0.72, no existing debt, market debt ratio 2.45%. Stepping the grid, WACC falls from 6.12% at 10% debt to 5.90% at 30% debt, then jumps sharply to 8.55% at 40%. The jump is the rating cliff: past 30% the coverage ratio deteriorates enough that the synthetic rating and spread deteriorate faster than the tax shield gains. Optimum = 30%, with a relevered beta of 0.92, a cost of equity of 7.46%, an A− rating and a minimised WACC of 5.90%. This matches the Part V prediction exactly — Chipotle had the lowest EBITDA/value in the group (3.90%) and therefore the lowest optimum.

**Determinism:** DETERMINISTIC — given unlevered beta, tax rate, Rf, ERP, EBIT and a coverage-to-rating-to-spread table, a script produces the entire schedule and picks the minimum. The hurdle-rate table at the optimum follows mechanically. JUDGMENT — the constraints layered on top: rating floors the firm will not breach, how fast to move, pending acquisitions, and management's own tolerance. The recommended ratio can and often should differ from the argmin.

**Pitfalls:**
- Reporting the argmin as the recommendation. The project explicitly asks for the constrained recommendation as a separate answer.
- Treating the WACC curve as smooth. It is a step function with cliffs where the synthetic rating changes; the minimum can sit right at the edge of a cliff.
- Relying on interest coverage as the only rating criterion. This is the acknowledged weakness of the whole exercise and can understate rating risk.
- Using a single EBIT figure without testing what happens if earnings fall. See the stress test in [[recapitalization-value-and-stress-test]].
- Forgetting the circularity: the debt level sets the interest expense, which sets the coverage, which sets the rate, which sets the interest expense. It must be solved iteratively.

**Sources:**
- corporate_finance--project--cfproj p.9
- corporate_finance--project--food2015 p.11, p.2

**Related:** [[qualitative-debt-tradeoff]], [[recapitalization-value-and-stress-test]], [[cost-of-capital-buildup-deliverable]], [[debt-design-deliverable]], [[two-stage-fcff-company-valuation]]
