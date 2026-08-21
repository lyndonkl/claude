# Cost of capital build-up table (the hurdle-rate deliverable)

**Core idea:** Part III of the corporate finance project ends in one table: the firm's cost of equity, cost of debt and cost of capital, built from the ground up. Equity risk comes from a bottom-up unlevered beta relevered at the firm's own debt-to-equity ratio. Debt risk comes from a synthetic rating derived from interest coverage, not from an agency letter. The equity risk premium is weighted by where revenues come from, not where the firm is listed. The table is then produced twice — once on market values and once on net book values — because the market-value version drives valuation while the book/net version is the fair comparison against accounting returns like ROE and ROC.

**Formulas:**
- Levered beta = Unlevered beta × (1 + (1 − t) × D/E). t = marginal tax rate; D/E = debt-to-equity ratio.
- Cost of equity = Rf + Levered beta × ERP. Rf = risk-free rate; ERP = equity risk premium.
- Interest coverage ratio = EBIT / Interest expense.
- Cost of debt (pre-tax) = Rf + Default spread, where the spread comes from the synthetic rating implied by the coverage ratio.
- Debt ratio = D / (D + E). Net debt ratio uses (Debt − Cash) in place of Debt.
- WACC = (E/(D+E)) × Cost of equity + (D/(D+E)) × Cost of debt × (1 − t).
- Revenue-weighted ERP = Σ (revenue share in country i × ERP of country i).

**Procedure:**
1. **Unlevered beta.** Take the industry average unlevered beta for each business the firm operates in, and value-weight across businesses. A coffee retailer that is part restaurant and part beverage gets a blend.
2. **Debt and equity in market terms.** Equity = shares outstanding × price. Debt = market value of interest-bearing debt *plus the capitalized value of lease commitments*. Record cash separately.
3. **Relever.** Compute D/E at market values and apply the levering formula with the marginal tax rate.
4. **ERP by revenue geography.** Weight country ERPs by revenue exposure. A purely domestic US firm gets the mature-market premium; a firm with substantial emerging-market revenue gets a higher blended premium.
5. **Cost of equity** = Rf + levered beta × ERP.
6. **Synthetic rating for debt.** Compute EBIT / interest expense. Map the coverage ratio to a rating, the rating to a default spread, and add the spread to Rf. Where there is no interest expense at all, the coverage ratio is undefined and the rating must be assigned by judgment.
7. **WACC** with market-value weights and the after-tax cost of debt.
8. **Repeat the whole table on net book values** — book equity, book debt, book debt net of cash. This version is the one to compare against ROE and ROC in Part IV, because those returns are computed on book capital.
9. Hand the market WACC to the valuation and the book/net figures to the return-spread analysis.

**Reference data:** Spring 2015 build-up for four food companies. Rf = 2.17%, marginal tax rate 35% throughout.

| Cost of equity / capital | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Unlevered beta | 0.78 | 0.72 | 0.72 | 0.80 |
| Shares (m) | 753.10 | 961.12 | 31.00 | 304.57 |
| Stock price | $77.21 | $96.13 | $684.51 | $40.67 |
| Equity ($m, market) | 58,147 | 92,392 | 21,220 | 12,387 |
| Debt ($m, market) | 7,870 | 49,721 | 534 | 6,829 |
| Equity ($m, book) | 5,274 | 12,853 | 2,012 | 8,904 |
| Debt ($m, book) | 5,479 | 14,990 | 534 | 8,178 |
| Cash ($m) | 1,708 | 2,078 | 419 | 438 |
| Debt ratio (market) | 11.92% | 34.99% | 2.45% | 35.54% |
| Debt ratio (book) | 50.96% | 53.84% | 20.97% | 47.87% |
| Debt ratio (market, net) | 9.33% | 33.52% | 0.53% | 33.26% |
| Debt ratio (book, net) | 35.07% | 46.37% | 4.49% | 45.31% |
| Levered beta (market) | 0.85 | 0.97 | 0.73 | 1.09 |
| Levered beta (book, net) | 1.14 | 1.19 | 0.75 | 1.25 |
| Equity risk premium | 5.91% | 6.22% | 5.75% | 5.75% |
| Cost of equity (market) | 7.16% | 8.21% | 6.38% | 8.42% |
| Cost of equity (book, net) | 8.89% | 9.57% | 6.46% | 9.37% |
| Cost of capital (market) | 6.58% | 6.13% | 6.29% | 6.39% |
| Cost of capital (book, net) | 6.57% | 6.18% | 6.29% | 6.35% |

Cost of debt via synthetic rating, same date:

| Cost of debt | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Risk-free rate | 2.17% | 2.17% | 2.17% | 2.17% |
| Interest expense ($m) | 64 | 551 | 0 | 132 |
| EBIT ($m) | 3,081 | 7,968 | 711 | 1,430 |
| Interest coverage ratio | 48.07 | 14.47 | N/A | 10.83 |
| Synthetic rating | AAA | AAA | BBB | BBB |
| Default spread | 1.30% | 1.30% | 2.00% | 2.00% |
| Cost of debt | 3.47% | 3.47% | 4.17% | 4.17% |

ERP by revenue mix (2015 instance): CMG and TSN are essentially all-US and get 5.75%. SBUX gets 5.91% and MCD 6.22%, revenue-weighted across their top markets because both carry substantial emerging-market exposure.

Published data sets for this part: betas by industry; cost of debt and cost of capital by industry.

**Worked example:** Starbucks, 2015. Unlevered beta 0.78 from the restaurant/beverage blend. Market equity = 753.10m shares × $77.21 = $58,147m; market debt $7,870m, so D/E = 7,870/58,147 = 13.5%. Levered beta = 0.78 × (1 + 0.65 × 0.135) ≈ 0.85. Cost of equity = 2.17% + 0.85 × 5.91% = 7.16%. Coverage ratio = 3,081/64 = 48.07 → AAA → spread 1.30% → cost of debt 3.47%. WACC = 0.8808 × 7.16% + 0.1192 × 3.47% × 0.65 = 6.58%. On book-net values the same firm has a 35.07% debt ratio, a levered beta of 1.14 and a cost of equity of 8.89% — the figure used against its 39.22% ROE.

**Determinism:** DETERMINISTIC — given unlevered beta, share count, price, market and book debt, cash, tax rate, Rf, ERP and a coverage-to-spread table, a script produces every row: D/E, levered betas, costs of equity, coverage ratio, rating, spread, cost of debt, and both WACCs. JUDGMENT — the business mix used to blend the unlevered beta, the revenue-geography weights behind the ERP, how leases are capitalized into debt, and the rating assigned when coverage is undefined. Chipotle's BBB is explicitly a judgment call: it has no interest expense and no agency rating.

**Pitfalls:**
- Ignoring lease commitments. McDonald's market debt of $49,721m dwarfs its $14,990m book debt almost entirely because of capitalized leases and minimum rent obligations. Using book debt would badly understate leverage and overstate the equity weight.
- Setting the ERP by country of listing rather than by revenue geography.
- Comparing a market-value cost of equity to a book-value ROE. The two tables exist so that Part IV compares like with like.
- Treating the synthetic rating as safe because coverage is high. Interest coverage is the only criterion in the mechanical mapping, and it can understate rating risk.
- Assigning a rating to a firm with zero interest expense by formula. The ratio is undefined; state the assumption.

**Sources:**
- corporate_finance--project--cfproj p.6
- corporate_finance--project--food2015 p.7-8, p.2

**Related:** [[regression-performance-diagnostics]], [[return-spread-and-eva-analysis]], [[optimal-debt-ratio-wacc-schedule]], [[stockholder-analysis-marginal-investor]], [[two-stage-fcff-company-valuation]], [[corporate-finance-project-blueprint]]
