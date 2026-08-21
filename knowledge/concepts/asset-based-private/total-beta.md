# Total beta and the undiversified buyer

**Core idea:** Standard risk-and-return models assume the marginal investor is diversified. Such an investor holds many assets, so firm-specific risk washes out, and only market risk gets priced. That is measured by beta. A private owner who has every dollar of wealth in one business is exposed to *all* of the risk, not just the market part. Total beta scales the market beta up by the share of risk that is actually market risk. Since betas are built from standard deviations rather than variances, that share is the **correlation** with the market, which is the square root of the regression R², not R² itself. The effect is large: a market beta of 1.18 with an average R² of 25% becomes a total beta of 2.36.

**Formulas:**
- `Total beta = Market beta / (Portion of total risk that is market risk)`
- `Portion of total risk that is market risk = Correlation with the market (ρ) = sqrt(R²)`, where `R²` is the average R-squared of the comparable public firms' beta regressions against the market index.
- Therefore: `Total unlevered beta = Unlevered market beta / ρ`
- Levering: `Levered total beta = Total unlevered beta × (1 + (1 − t) × D/E)`
- `Cost of equity = Riskfree rate + Levered total beta × ERP`
- Equivalently, the total beta is the beta of a portfolio whose only holding is this firm: `β_total = σ_firm / σ_market`, versus `β_market = ρ × σ_firm / σ_market`.
- Symbols: `t` = marginal tax rate; `D/E` = debt-to-equity ratio; `ERP` = equity risk premium; `σ` = standard deviation of returns.

**Procedure:**
1. Establish who the marginal investor is. This is the whole question. If the buyer will hold this business alongside a diversified portfolio, stop — use the market beta.
2. Get an unlevered market beta from comparable publicly traded firms (bottom-up). Choose the comparable set on business economics, not the industry label.
3. From the *same* regressions that produced those betas, take the average R².
4. Compute `ρ = sqrt(R²)`.
5. `Total unlevered beta = Unlevered market beta / ρ`.
6. Lever the total beta at the debt-to-equity ratio you will use for the private firm.
7. Compute the cost of equity from the levered total beta.
8. If the buyer is only *partially* diversified — a venture capital fund, a private equity fund, a family office with other holdings — use the correlation of **that buyer's portfolio** with the market, not the correlation of a single-asset holder. The result sits between the market-beta and total-beta answers.

**Reference data:** Diversification and perceived risk, using the packet's illustrative decomposition (80 units firm-specific risk, 20 units market risk) and the staged example (sector market beta 1, riskfree 4%, ERP 5%):

| Holder of the business | Correlation of holder's portfolio with market (ρ) | Perceived beta | Cost of equity |
|---|---|---|---|
| Fully invested private owner | 0.25 | 1 / 0.25 = 4 | 4% + 4(5%) = 24% |
| Specialized VC with several tech holdings | 0.50 | 1 / 0.50 = 2 | 4% + 2(5%) = 14% |
| Diversified public investors | 1.00 | 1 | 4% + 1(5%) = 9% |

Restaurant comparable sets (packet data):

| Comparable group | N firms | Average unlevered market beta | Average R² | ρ | Total unlevered beta |
|---|---|---|---|---|---|
| US publicly traded restaurants | 75 | 0.86 | — | — | — |
| High-end specialty retailers | 45 | 1.18 | 25% | 0.50 | 2.36 |

**Worked example:** The upscale French restaurant. Most listed restaurants are fast-food or mass chains (McDonald's, Burger King, Applebee's, TGIF), so their 0.86 unlevered beta is a poor match for an upscale establishment. Damodaran uses high-end specialty retailers instead: unlevered market beta 1.18, average regression R² of 25%. Then `ρ = sqrt(0.25) = 0.50` and `total unlevered beta = 1.18 / 0.50 = 2.36`. Levered at D/E 14.33% with a 40% tax rate: `2.36 × (1 + 0.6 × 0.1433) = 2.56`. With a 4.25% riskfree rate and a 4% ERP, `cost of equity = 4.25% + 2.56 × 4% = 14.50%`. The same business valued for a diversified public buyer uses the market beta: levered beta 1.28, cost of equity 9.38%.

**Determinism:**
- DETERMINISTIC: `{unlevered market beta, R²} → ρ → total unlevered beta`. Then `{total unlevered beta, D/E, tax rate, riskfree, ERP} → levered total beta → cost of equity`. A script computes all of it.
- JUDGMENT: which comparable firms define the sector (the restaurant case turns on this and moves the beta from 0.86 to 1.18); whether the buyer is undiversified, partially diversified, or diversified; and what correlation to assign a partially diversified buyer. That judgment needs the buyer's other holdings, the comparable firms' regression statistics, and a view on which peers share the business's economics.

**Pitfalls:**
- Dividing by R² instead of by the correlation. R² is a variance share; betas run on standard deviations, so the square root is the right adjustment. Dividing by 0.25 rather than 0.50 would have doubled the beta again.
- Using an R² from a different regression than the one that produced the beta.
- Applying total beta to a diversified buyer. That systematically undervalues the business and hands the surplus to the buyer.
- Applying total beta to a partially diversified buyer at full strength. A VC fund is not a single-asset holder.
- Picking comparables by industry label. Fast-food chains are the wrong peers for an upscale French restaurant even though both are "restaurants".
- Correlation of exactly zero breaks the formula. Require ρ > 0.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.129, p.132-136, p.151, p.153, p.167
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.127, p.130-134, p.149, p.151, p.164
- special-private.md — pvtdiscrate.xls, sheet "Total Beta approach" (`B22 = (B3/B6) × (1 + (1−t)·(D/C)/(1−D/C))`)

**Related:** [[private-company-cost-of-capital]], [[private-company-valuation-framework]], [[private-to-public-sale]], [[vc-stage-varying-cost-of-equity]], [[bottom-up-beta]], [[cost-of-equity]], [[diversification-and-risk]]
