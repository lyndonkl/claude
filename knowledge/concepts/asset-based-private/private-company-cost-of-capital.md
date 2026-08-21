# Estimating a private company's cost of capital

**Core idea:** A private firm has no beta, no bond rating, and no market debt-to-equity ratio, so every input has to be manufactured. The beta comes bottom-up from comparable public firms, then gets scaled to a total beta if the buyer is undiversified. The debt-to-equity ratio comes from the sector average, because using your own estimated values creates circular reasoning — you need the cost of capital to get values and the values to get the cost of capital. The cost of debt comes from a synthetic rating built off the interest coverage ratio, with lease commitments treated as interest. Then the pieces combine into an ordinary weighted average cost of capital.

**Formulas:**
- `Total unlevered beta = Unlevered market beta / ρ`, `ρ = sqrt(average R² of comparables)` — see [[total-beta]].
- `Levered beta = Unlevered beta × (1 + (1 − t) × D/E)`
- `Cost of equity = Riskfree rate + Levered beta × ERP`
- Alternative to total beta (offered in Damodaran's spreadsheet, not preferred): `Cost of equity = Riskfree rate + Levered market beta × ERP + Private company premium`. The premium is added flat, not scaled by beta.
- `Interest coverage ratio = Operating income / Interest expense`, where lease payments count as interest for a firm with no conventional debt.
- `Pre-tax cost of debt = Riskfree rate + Default spread(rating)`; `After-tax cost of debt = Pre-tax cost of debt × (1 − t)`
- Weight conversion from a D/E ratio: `D/(D+E) = (D/E) / (1 + D/E)` and `E/(D+E) = 1 / (1 + D/E)`. With D/E = 14.33%, the weights are 14.33/114.33 and 100/114.33.
- `Cost of capital = Cost of equity × E/(D+E) + After-tax cost of debt × D/(D+E)`
- Spreadsheet form when a debt-to-capital ratio is the input: `Total levered beta = (Unlevered beta / ρ) × (1 + (1 − t) × (D/C)/(1 − D/C))`.

**Procedure:**
1. Pick a comparable set of publicly traded firms on business economics, not industry label. Average their unlevered betas.
2. Decide the buyer's diversification. Undiversified → divide by `ρ = sqrt(average R²)` to get a total beta. Diversified → keep the market beta. Partially diversified → use that buyer's portfolio correlation.
3. Choose the debt-to-equity ratio. **Decision rule: use the industry-average market D/E of publicly traded firms in the sector.** The alternative — your own estimated debt and equity values — is circular. If you use it, you must iterate to convergence.
4. Lever the beta and compute the cost of equity with the current riskfree rate and ERP.
5. Compute the interest coverage ratio. For a private firm with no conventional debt but lease commitments, use the lease expense as the interest expense. If there is no interest expense at all, coverage is effectively infinite and the rating is AAA.
6. Look the coverage ratio up in the synthetic-rating table to get a rating and a default spread.
7. `Pre-tax cost of debt = riskfree + spread`, then multiply by `(1 − t)`.
8. Convert the D/E ratio to weights and take the weighted average.
9. Use the same D/E ratio in both the beta levering and the weighting. Consistency here is not optional.

**Reference data — synthetic rating table** (from `pvtdiscrate.xls`, "Synthetic ratings" sheet; a single legacy table with no large/small-firm split):

| Coverage ratio > | ≤ | Rating | Default spread |
|---|---|---|---|
| −100000 | 0.499999 | D | 14.00% |
| 0.5 | 0.799999 | C | 12.70% |
| 0.8 | 1.249999 | CC | 11.50% |
| 1.25 | 1.499999 | CCC | 10.00% |
| 1.5 | 1.999999 | B− | 8.00% |
| 2.0 | 2.499999 | B | 6.50% |
| 2.5 | 2.999999 | B+ | 4.75% |
| 3.0 | 3.499999 | BB | 3.50% |
| 3.5 | 4.499999 | BBB | 2.25% |
| 4.5 | 5.999999 | A− | 2.00% |
| 6.0 | 7.499999 | A | 1.80% |
| 7.5 | 9.499999 | A+ | 1.50% |
| 9.5 | 12.499999 | AA | 1.00% |
| 12.5 | 100000 | AAA | 0.75% |

Lookup is an approximate match on the lower bound. Negative EBIT with positive interest gives a negative coverage ratio, which falls into the first row (D, 14%). Later Damodaran tables split this by market cap and update the spreads; treat the table as a swappable parameter.

**Reference data — the restaurant's inputs, private buyer vs public buyer:**

| Input | Private (undiversified) | Public (diversified) |
|---|---|---|
| Unlevered beta | 2.36 (total) | 1.18 (market) |
| Debt-to-equity ratio | 14.33% | 14.33% |
| Tax rate | 40% | 40% |
| Riskfree rate | 4.25% | 4.25% |
| Equity risk premium | 4% | 4% |
| Levered beta | 2.56 | 1.28 |
| Cost of equity | 14.50% | 9.38% |
| Pre-tax cost of debt | 7.50% | 7.50% |
| After-tax cost of debt | 4.50% | 4.50% |
| **Cost of capital** | **13.25%** | **8.76%** |

**Worked example:** The restaurant. Coverage ratio = `$400,000 / $120,000 = 3.33`. The packet maps 3.33 to a **BB+** rating and a **3.25%** default spread, so the pre-tax cost of debt is `4.25% + 3.25% = 7.50%` and the after-tax cost is `7.50% × 0.60 = 4.50%`. Weights from D/E = 14.33%: equity `100/114.33 = 87.47%`, debt `14.33/114.33 = 12.53%`. Cost of capital = `14.50% × (100/114.33) + 4.50% × (14.33/114.33) = 13.25%`.

**Worked example — spreadsheet default (`pvtdiscrate.xls`):** unlevered beta 1.02, correlation 0.45, riskfree 6%, ERP 5.5%, tax 40%, industry debt-to-capital 15%, entered pre-tax cost of debt 7%. Total levered beta = `(1.02/0.45) × (1 + 0.6 × (0.15/0.85)) = 2.2667 × 1.10588 = 2.5067`. Cost of equity = `6% + 5.5% × 2.5067 = 19.79%`. After-tax cost of debt = `7% × 0.6 = 4.2%`. Cost of capital = `0.85 × 19.79% + 0.15 × 4.2% = 17.45%`. The synthetic route on the same sheet: EBIT 10,000, interest 2,500 → coverage 4.0 → BBB → spread 2.25% → pre-tax cost of debt 8.25%.

**Determinism:**
- DETERMINISTIC: `{unlevered beta, R², D/E, tax rate, riskfree, ERP} → cost of equity`. `{operating income, interest or lease expense} → coverage → rating → spread → cost of debt` via table lookup. `{cost of equity, after-tax cost of debt, D/E} → cost of capital`. A script does all of it, including the table lookup.
- JUDGMENT: the comparable set; whether the buyer is diversified; whether to use industry D/E or iterate on your own estimates; which vintage of the rating table applies; and whether the lease expense is the right proxy for interest. That judgment needs sector beta and D/E data, the firm's lease commitments, and a current spread table.

**Pitfalls:**
- Levering the beta at one D/E and weighting the cost of capital at another.
- Confusing D/E with D/(D+E). 14.33% D/E is a 12.53% debt weight, not 14.33%.
- Using your own estimated debt and equity values as weights without iterating. That is circular reasoning and the answer depends on where you started.
- Taking the "private company premium" route in the spreadsheet as equivalent to total beta. It adds a flat premium to a market-beta cost of equity and has no risk-model basis.
- Table drift: the packet's restaurant maps 3.33 to BB+ / 3.25%, while the legacy spreadsheet table maps 3.0–3.499 to BB / 3.50%. Different vintages, different answers. State which table you used.
- A correlation of 0 or a debt-to-capital of 1 divides by zero.
- Ignoring lease commitments when computing coverage. A restaurant with no bank debt is not a zero-leverage firm.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.125, p.132-133, p.136-137, p.151
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.123, p.130-131, p.134-135, p.149
- special-private.md — pvtdiscrate.xls, sheets "Total Beta approach" and "Synthetic ratings"

**Related:** [[total-beta]], [[private-company-valuation-framework]], [[private-company-statement-cleanup]], [[private-to-public-sale]], [[synthetic-rating]], [[bottom-up-beta]], [[cost-of-capital]], [[operating-lease-capitalization]]
