# Divisional cost of capital

**Core idea:** A multi-business firm has one cost of capital only by accident. Each division has its own business risk and, if you allocate debt sensibly, its own debt ratio. Using the company-wide rate as the hurdle for every division makes safe divisions look bad and risky divisions look good — safe businesses subsidize risky ones, and the firm drifts toward its riskiest activities. The fix is to compute a cost of capital per division: a bottom-up unlevered beta for that business, relevered at the division's own debt ratio, combined with the company's cost of debt and marginal tax rate. Disney's divisional rates span 5.69% to 8.96% around a company-wide 7.81%.

**Formulas:**
- Divisional allocated debt = Total firm debt × (division's identifiable assets / total identifiable assets).
- Divisional D/E = Allocated debt / (Estimated value of the division − Allocated debt).
- Divisional levered beta = Divisional unlevered beta × [1 + (1 − t) × Divisional D/E].
- Divisional cost of equity = Riskfree rate + Divisional levered beta × Equity risk premium.
- Divisional cost of capital = Divisional cost of equity × (1 − Debt ratio) + Pre-tax cost of debt × (1 − t) × Debt ratio, where Debt ratio = D/(D+E) for that division.
- Value of a division (for weights) = Division revenues × peer-group EV/Sales multiple.
- The pre-tax cost of debt and marginal tax rate are normally taken as company-wide, because debt is raised at the corporate level.

**Procedure:**
1. Identify the firm's businesses. Segment reporting is the usual starting point.
2. For each business, get an unlevered beta from comparable public firms in that business, cash-adjusted ([[bottom-up-beta]]).
3. Value each business. Apply the peer-group EV/Sales multiple to the division's revenues. Value weights are better than revenue or operating-income weights.
4. Allocate the firm's total debt across divisions. Damodaran's allocation key in the Disney case is identifiable assets. Any defensible key works, but state it — it drives the divisional debt ratios directly.
5. Divisional equity = division value − allocated debt. Divisional D/E = allocated debt / divisional equity.
6. Relever each division's unlevered beta at its own D/E. Compute the divisional cost of equity.
7. Combine with the company-wide after-tax cost of debt and the division's debt ratio to get the divisional cost of capital.
8. Adjust for geography. If the project or division sits in an emerging market, add a country risk premium to the ERP before computing the cost of equity ([[country-risk-in-cost-of-debt]]).
9. Use the divisional rate, not the corporate rate, to judge projects in that division.

**Reference data:**

*Disney, 2013: debt allocation by identifiable assets ($ millions), total debt $15,961.*

| Business | Identifiable assets | Share of debt | Value of business | Allocated debt | Estimated equity | D/E ratio |
|---|---|---|---|---|---|---|
| Media Networks | $28,627 | 38.04% | $66,580 | $6,072 | $60,508 | 10.03% |
| Parks & Resorts | $22,056 | 29.31% | $45,683 | $4,678 | $41,005 | 11.41% |
| Studio Entertainment | $14,750 | 19.60% | $18,234 | $3,129 | $15,106 | 20.71% |
| Consumer Products | $7,506 | 9.97% | $2,952 | $1,592 | $1,359 | 117.11% |
| Interactive | $2,311 | 3.07% | $1,684 | $490 | $1,194 | 41.07% |
| **Disney** | **$75,250** | **100%** | | **$15,961** | **$121,878** | **13.10%** |

*Disney: divisional betas, costs of equity and costs of capital.* Riskfree rate 2.75%; ERP 5.76%; pre-tax cost of debt 3.75%; marginal tax rate 36.10%; after-tax cost of debt 2.40% for every division.

| Business | Unlevered beta | D/E | Levered beta | Cost of equity | Debt ratio D/(D+E) | Cost of capital |
|---|---|---|---|---|---|---|
| Media Networks | 1.0313 | 10.03% | 1.0975 | 9.07% | 9.12% | 8.46% |
| Parks & Resorts | 0.7024 | 11.41% | 0.7537 | 7.09% | 10.24% | 6.61% |
| Studio Entertainment | 1.0993 | 20.71% | 1.2448 | 9.92% | 17.16% | 8.63% |
| Consumer Products | 0.6752 | 117.11% | 1.1805 | 9.55% | 53.94% | 5.69% |
| Interactive | 1.2187 | 41.07% | 1.5385 | 11.61% | 29.11% | 8.96% |
| **Disney Operations** | **0.9239** | **13.10%** | **1.0012** | **8.52%** | **11.58%** | **7.81%** |

*Vale: divisional costs of capital in two currencies.* After-tax cost of debt 2.67% and debt ratio 35.48% for every business; riskfree 2.75%; ERP 7.38%.

| Business | Unlevered beta | Levered beta at 54.99% D/E | Cost of equity | Cost of capital (US$) | Cost of capital (nominal R$) |
|---|---|---|---|---|---|
| Metals & Mining | 0.86 | 1.1657 | 11.35% | 8.27% | 15.70% |
| Iron Ore | 0.83 | 1.1358 | 11.13% | 8.13% | 15.55% |
| Fertilizers | 0.99 | 1.3493 | 12.70% | 9.14% | 16.63% |
| Logistics | 0.75 | 1.0222 | 10.29% | 7.59% | 14.97% |
| **Vale Operations** | **0.84** | **1.1503** | **11.23%** | **8.20%** | **15.62%** |

**Worked example:** Disney's Studio Entertainment division. Its comparable-firm unlevered beta is 1.0993. Identifiable assets of $14,750m out of $75,250m give it 19.60% of Disney's $15,961m debt, or $3,129m. The business is worth $18,234m (revenues $5,979m × peer EV/Sales of 3.05), so its equity is $15,106m and its D/E is 20.71%. Levered beta = 1.0993 × [1 + (1 − 0.361) × 0.2071] = 1.2448. Cost of equity = 2.75% + 1.2448 × 5.76% = 9.92%. Debt ratio = 3,129 / 18,234 = 17.16%. Cost of capital = 9.92% × 0.8284 + 2.40% × 0.1716 = **8.63%**.

The decision this changes: a big-budget movie projected to return 9.5% on equity clears Disney's company-wide 8.52% cost of equity but fails the movie business's 9.92%. Judged against the corporate average it looks like a good project; judged against its own business's risk it destroys value.

**Determinism:**
- DETERMINISTIC: given divisional unlevered betas, an allocation key, total debt, divisional values, the tax rate, the riskfree rate, the ERP and the cost of debt → allocated debt, divisional D/E, levered betas, costs of equity and costs of capital. Every number in the tables above is reproducible.
- JUDGMENT: how to define the divisions, which comparable firms belong to each, and which multiple to use for valuing each business.
- JUDGMENT: the debt-allocation key. Identifiable assets is Damodaran's choice for Disney, but sales, EBITDA or a division-specific target debt ratio are all defensible. This choice alone drives the striking 117% D/E for Consumer Products, whose asset base is large relative to its value.
- JUDGMENT: whether the company-wide cost of debt is right for a division. A standalone Consumer Products company with a 54% debt ratio would not borrow at Disney's A-rated 3.75%.

**Pitfalls:**
- Using one company-wide hurdle rate for all divisions. This is the error the whole concept exists to prevent.
- Allocating debt by a key that has no relationship to debt capacity, then treating the resulting divisional debt ratio as meaningful.
- Failing to notice when an allocation produces an implausible result — the 117% D/E and consequent 5.69% cost of capital for Consumer Products is an artifact of a large asset base against a small business value, and its low cost of capital would let weak projects clear.
- Using book asset values instead of estimated business values in the divisional weights.
- Forgetting the country risk adjustment when the division or project sits in an emerging market.
- Applying a divisional cost of CAPITAL to a return measured on EQUITY.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.165, p.172-174, p.201, p.204
- corporate_finance--lecture_slides--cfpacket1spr20 p.173 (the Disney movie hurdle-rate discussion)
- corporate_finance--lecture_slides--cfpacket1spr20 p.221, p.224 (project rate = divisional rate adjusted for country risk)
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.96 (Vale segment betas and costs of equity)
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.94 (same, 2020 edition)
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls Multi Business calculators (value-weighted unlevered beta from industry EV/Sales and unlevered beta lookups)

**Related:** [[cost-of-capital-assembly]], [[market-value-weights]], [[country-risk-in-cost-of-debt]], [[currency-conversion-of-discount-rates]], [[bottom-up-beta]], [[levered-beta]], [[hurdle-rate-choice]], [[ev-to-sales-multiple]]
