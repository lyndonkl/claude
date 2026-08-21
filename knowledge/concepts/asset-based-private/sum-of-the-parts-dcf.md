# Sum of the parts with DCF (valuing the parts intrinsically)

**Core idea:** Value each division as if it were a standalone company, with its own cost of capital, its own return on capital and its own growth. Then add the divisions, subtract the capitalized value of unallocated corporate expenses, and bridge to equity. The discipline that makes this work is that every division gets its own risk: a business with an unlevered beta of 1.19 does not deserve the same discount rate as one with 0.65. The second discipline is that growth must be earned. A division whose return on capital sits below its cost of capital gets no high-growth period at all, because growth there destroys value.

**Formulas:**
- Division cost of capital:
  - `Levered beta_i = Unlevered beta_i × (1 + (1 − t) × D/E)` — company-wide D/E used for every division unless a division's own financing is known.
  - `Cost of equity_i = Riskfree rate + Levered beta_i × ERP`
  - `Cost of capital_i = Cost of equity_i × (1 − D/(D+E)) + After-tax cost of debt × D/(D+E)`
- Division fundamentals:
  - `Return on capital_i (ROC) = After-tax operating income_i / Capital invested_i`
  - `Reinvestment rate_i (RIR) = Allocated reinvestment_i / After-tax operating income_i`, where allocated reinvestment = net cap ex + change in working capital assigned to the division.
  - `Expected growth_i = RIR_i × ROC_i`
- Division value:
  - `Value(Division_i) = PV of FCFF over the high-growth period + PV of terminal value`, discounted at `Cost of capital_i`
  - `FCFF_i,t = EBIT_i,t × (1 − t) × (1 − RIR_i)`
  - `Terminal value_i = FCFF_i,n+1 / (Cost of capital_i − g_stable)`, with `RIR_stable = g_stable / ROC_stable`
- Corporate expense drag:
  - `Value of corporate expenses = Corporate expenses_current × (1 − t) × (1 + g) / (Cost of capital_company − g)`
- Totals:
  - `Value of operating assets = Σ_i Value(Division_i) − Value of corporate expenses`
  - `Equity = Value of operating assets + Cash − Debt − Financing-arm debt − Minority interests`; `Per share = (Equity − Options) / Shares`
- Symbols: `t` = marginal tax rate; `ERP` = equity risk premium; `g_stable` = stable-period growth; `ROC_stable` = return on capital assumed in perpetuity.

**Procedure:**
1. Get an unlevered beta per division from that division's sector (bottom-up). Lever each at the company's debt-to-equity ratio, unless the division would carry different debt on its own.
2. Compute each division's cost of equity and cost of capital. Use the same after-tax cost of debt and debt weight for all divisions when the debt is raised at the parent.
3. Build each division's ROC from after-tax operating income over capital invested, and its reinvestment rate from allocated reinvestment over after-tax operating income.
4. Set expected growth = RIR × ROC. This ties growth to reinvestment and stops you assuming free growth.
5. Set the length of the high-growth period per division. **Decision rule: if a division's ROC is at or below its cost of capital, give it a zero-year growth period.** Growth adds nothing there. Otherwise 5 years is the packet's default.
6. Set the stable-period growth rate (3% for UTC, applied uniformly) and the stable ROC. **Decision rule: stable ROC = cost of capital, unless a durable competitive advantage justifies more.** UTC's exceptions: Pratt & Whitney 12% and Otis 14%.
7. Discount each division's FCFF and terminal value at its own cost of capital.
8. Sum the divisions.
9. Capitalize unallocated corporate expenses as a growing perpetuity, after tax, at the *company-wide* cost of capital, and subtract.
10. Bridge to equity: add cash, subtract all debt (including a captive finance arm's), subtract minority interests, subtract option value, divide by shares.
11. Compare to the pricing sum of the parts, to the whole-company DCF, and to the market.

**Reference data — United Technologies, 2009.** Company-wide inputs: D/E 30.44%, debt/capital 23.33%, after-tax cost of debt 2.95%, tax rate 38%, company cost of capital 8.68%, stable growth 3%, unallocated corporate expenses $408M.

| Division | Unlevered beta | Levered beta | Cost of equity | Cost of capital | ROC | RIR | Growth | Growth yrs | Stable ROC |
|---|---|---|---|---|---|---|---|---|---|
| Carrier | 0.83 | 0.97 | 9.32% | 7.84% | 13.57% | 43.28% | 5.87% | 5 | 7.84% |
| Pratt & Whitney | 0.81 | 0.95 | 9.17% | 7.72% | 24.51% | 57.90% | 14.19% | 5 | 12.00% |
| Otis | 1.19 | 1.39 | 12.07% | 9.94% | 35.71% | 18.06% | 6.45% | 5 | 14.00% |
| UTC Fire & Security | 0.65 | 0.76 | 7.95% | 6.78% | 6.03% | 52.27% | 3.15% | 0 | 6.78% |
| Hamilton Sundstrand | 1.04 | 1.22 | 10.93% | 9.06% | 14.16% | 38.26% | 5.42% | 5 | 9.06% |
| Sikorsky | 1.17 | 1.37 | 11.92% | 9.82% | 13.37% | 102.95% | 13.76% | 5 | 9.82% |

Resulting values ($ millions):

| Division | PV of FCFF | PV of terminal value | Value of operating assets |
|---|---|---|---|
| Carrier | 2,190 | 9,498 | 11,688 |
| Pratt & Whitney | 3,310 | 27,989 | 31,299 |
| Otis | 5,717 | 14,798 | 20,515 |
| UTC Fire & Security | 0 | 4,953 | 4,953 |
| Hamilton Sundstrand | 1,902 | 6,343 | 8,245 |
| Sikorsky | −49 | 3,598 | 3,550 |
| **Sum** | | | **80,250** |

**Reference data — GE segments (2018 analysis, 2017 data).** Each segment's ROIC compared to its own cost of capital drives the growth assumptions:

| Business | Revenues 2017 ($B) | EBIT after G&A ($B) | Invested capital | ROIC 2017 | ROIC 2013–17 | Cost of capital |
|---|---|---|---|---|---|---|
| Power | 36.00 | 1.69 | 328.34 | 3.85% | 9.28% | 4.91% |
| Renewable Energy | 10.30 | 0.41 | 49.91 | 6.19% | 8.00% | 6.88% |
| Oil & Gas | 17.20 | (0.31) | 275.95 | −0.83% | 3.71% | 8.82% |
| Aviation | 27.40 | 5.80 | 192.73 | 22.59% | 20.27% | 8.52% |
| Healthcare | 19.10 | 2.86 | 132.81 | 16.18% | 15.07% | 7.97% |
| Transportation | 4.20 | 0.70 | 20.73 | 25.17% | 26.67% | 7.49% |
| Lighting | 2.00 | 0.03 | 3.34 | 7.16% | 9.66% | 8.50% |
| Capital | 9.10 | (7.04) | 723.38 | −7.30% | −2.81% | 3.64% |
| Total | 125.30 | 4.15 | 1,727.18 | 1.80% | 4.50% | 6.23% |

**Worked example — UTC corporate expense drag and final comparison:**
`Value of corporate expenses = 408 × (1 − 0.38) × 1.03 / (0.0868 − 0.03) = $4,587M`.
`Value of operating assets = 80,250 − 4,587 = $75,663M`.
Against $74,230M from the pricing route, $71,410M from a whole-company DCF, and $52,261M of enterprise value at market prices. UTC traded roughly 30% below every estimate of the value of its parts.

**Worked example — GE, 2017 data ($ millions):** Each segment's EBIT is normalized at its 2013–17 average margin, corporate expense is allocated, and the after-tax figure is grown at `ROIC × reinvestment` and discounted at the segment's own cost of capital. Power: normalized EBIT before G&A 5,161.92, after allocation 4,061.80, after tax 3,046.35, cost of capital 4.91%, growth 6.10% → value 73,138.18. Non-capital segments total 176,957.62; GE Capital adds 27,080.96; value of businesses = 204,038.59. Bridge: − GE debt 83,568.00 − GE Capital debt 51,023.00 − minority interests 17,723.00 + cash 43,299.00 = equity 95,023.59; − options 218.94 = 94,804.65; **$10.92 per share**.

**Determinism:**
- DETERMINISTIC: `{unlevered betas, D/E, tax rate, riskfree, ERP, cost of debt, weights} → division costs of capital`. `{after-tax operating income, capital invested, allocated reinvestment} → ROC, RIR, growth`. `{EBIT, RIR, growth, growth-period length, cost of capital, stable inputs} → division value`. `{corporate expenses, tax rate, g, company cost of capital} → capitalized drag`. The whole equity bridge and per-share division.
- JUDGMENT: which sector each division belongs to and therefore its unlevered beta; whether the division would carry the parent's leverage standalone; how reinvestment and corporate G&A are allocated across divisions; the length of the high-growth period; the stable ROC and whether a competitive advantage justifies excess returns forever; and whether the latest year's earnings need normalizing. That judgment needs segment disclosures, sector beta data, the company's margin and ROIC history, and a view on each division's competitive position.

**Pitfalls:**
- One cost of capital for all divisions. UTC's range was 6.78% to 9.94% — a spread that changes division values by tens of percent.
- Granting a high-growth period to a division earning below its cost of capital. UTC Fire & Security earns 6.03% against a 6.78% cost of capital, so it gets zero growth years and its entire value is terminal.
- Assuming a stable ROC above cost of capital by default. That builds a perpetual competitive advantage into the terminal value without arguing for one.
- Dropping unallocated corporate expenses. For UTC they are worth −$4,587M, about 6% of the total.
- Missing that a very high reinvestment rate makes near-term FCFF negative. Sikorsky's PV of FCFF is −$49M with a 102.95% reinvestment rate; that is arithmetic, not an error.
- Forgetting a captive finance arm's debt in the bridge.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.111, p.115-121
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.109, p.113-119

**Related:** [[sum-of-the-parts-framework]], [[sum-of-the-parts-pricing]], [[asset-based-valuation-overview]], [[bottom-up-beta]], [[cost-of-capital]], [[terminal-value]], [[expected-growth-reinvestment]], [[fcff-valuation]]
