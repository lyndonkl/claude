# Valuing young companies with negative earnings (work backwards)

**Core idea:** A young company with tiny revenues and large operating losses cannot be valued forward from its own history, because there is no history and current earnings are meaningless. Instead you specify a **mature end-state** — the revenue scale, operating margin, return on capital and cost of capital the business will have when it grows up — and let the intermediate years converge to it. Value then comes almost entirely from the terminal years, early free cash flows are negative (which is where dilution shows up), and taxes are suppressed until net operating losses are used up. The discount rate matters far less than the revenue/margin path, so do not agonize over beta; agonize over the end-state and over the probability the firm never gets there.

**Formulas:**
- Revenue path: `Rev_t = Rev_{t−1} × (1 + g_t)`, with `g_1` set directly and years 2–5 at a compounded rate, then a linear fade over years 6–10 to the stable growth rate: `g_t = g_5 − (g_5 − g_stable) × (t − 5)/5`.
- Stable growth cap: `g_stable ≤ riskfree rate` (Damodaran's default in the Ginzu model sets `g_stable = riskfree rate`, optionally the post-year-10 riskfree rate).
- Margin convergence to a target by a chosen convergence year `T_c`: `margin_t = target` if `t > T_c`, else `margin_t = target − ((target − margin_1)/T_c) × (T_c − t)`.
- `EBIT_t = Rev_t × margin_t`.
- NOL / tax engine: `Taxes_t = tax rate × max(0, EBIT_t − NOL_{t−1})`; `NOL_t = NOL_{t−1} − min(NOL_{t−1}, max(EBIT_t, 0)) + max(−EBIT_t, 0)`; `EBIT(1−t)_t = EBIT_t − Taxes_t` (a loss year gets **no** tax refund). Effective tax rate for year t = `Taxes_t / EBIT_t` when EBIT_t > 0, else 0.
- Reinvestment from the sales-to-capital ratio: `Reinvestment_t = (Rev_t − Rev_{t−1}) / (Sales/Capital)` — see [[sales-to-capital-reinvestment]].
- `FCFF_t = EBIT(1−t)_t − Reinvestment_t`.
- Cost of equity: `k_e = riskfree + β_bottom-up × ERP`, with β fading toward 1.0 (or the mature sector beta) over the second half of the forecast. Pre-tax cost of debt fades to the stable value the same way. `WACC_t = k_e,t × E/(D+E)_t + k_d,t × (1 − effective tax rate_t) × D/(D+E)_t`. Discount with the cumulated factor `Cum_t = Π_{s≤t} (1 + WACC_s)`, `PV_t = FCFF_t / Cum_t`.
- Terminal value: `TV_n = FCFF_{n+1} / (WACC_stable − g_stable)`, with `FCFF_{n+1} = EBIT(1−t)_{n+1} × (1 − g_stable/ROC_stable)`. Terminal ROC defaults to the stable cost of capital (no excess returns forever) unless a durable moat is argued.
- Equity bridge: `Value of operating assets` (after any failure adjustment) `− debt (incl. lease debt) − minority interests + cash + cross holdings & non-operating assets = Equity`; `− value of employee options`; `÷ shares outstanding = value per share`. See [[dilution-and-employee-options]].

**Procedure:**
1. **Fix the base year.** Trailing-12-month revenues, adjusted operating income (add back R&D and lease adjustments if you capitalize them), effective and marginal tax rates, cash, debt, shares, options, and any NOL carryforward.
2. **Choose the end-state first.** Target pre-tax operating margin = the mature sector's margin (Amazon 2000: 10%, the retail-industry average; Boeing 2020: 5.47%, the global aerospace margin; JC Penney: 6.25%, US retail median). Terminal growth ≤ riskfree rate. Terminal ROC = stable cost of capital unless you can defend a moat.
3. **Set the revenue path backwards from that end-state.** Start with the year-1 growth you can defend, hold a compounded rate through year 5, fade linearly to stable growth in years 6–10. Cross-check: excess growth over the industry average dies within roughly **five years** of an IPO (the median post-IPO firm beats its industry by ~15% in year 1, ~7% year 2, ~3% year 3, ~0% by years 5–6, from Metrick's 1965–2005 new-issue data). Then check dollar revenues in year 10 against the **total addressable market** — if implied market share is implausible, the growth path is wrong.
4. **Ramp the margin** from the (usually negative) year-1 margin to the target by a stated convergence year.
5. **Run the NOL engine** so taxes stay at zero while losses are being absorbed, then step to the effective rate and let it converge to the marginal rate by the terminal year.
6. **Charge for growth**: reinvestment from the sales-to-capital ratio, and sanity-check the imputed ROC each year ([[sales-to-capital-reinvestment]]).
7. **Set discount rates loosely but sensibly**: bottom-up sector beta (never the regression beta), let the cost of capital fall as the firm matures, and if truly desperate use the **90th–95th percentile** of the cross-sectional distribution of costs of capital across all firms as the starting cost of capital. Do **not** put failure risk in the discount rate.
8. **Value the terminal year, discount everything**, and build the equity bridge.
9. **Adjust for failure** outside the DCF: `Value = Going-concern value × (1 − p_fail) + Distress proceeds × p_fail` ([[distress-and-failure-adjusted-value]]).
10. **Stress it**: two-way sensitivity on growth × target margin, then a simulation ([[scenario-analysis-and-simulation]]).

**Reference data:** Amazon, January 2000 — the canonical work-backwards path (revenue $1,117m and a −36.71% margin in the trailing year; sales-to-capital 3.00; target margin 10%).

| Year | Revenue growth | Sales | Operating margin | EBIT | EBIT(1−t) | Reinvestment | FCFF | Cost of capital |
|---|---|---|---|---|---|---|---|---|
| Tr 12 mths | — | $1,117 | −36.71% | −$410 | −$410 | — | — | — |
| 1 | 150.00% | $2,793 | −13.35% | −$373 | −$373 | $559 | −$931 | 12.84% |
| 2 | 100.00% | $5,585 | −1.68% | −$94 | −$94 | $931 | −$1,024 | 12.84% |
| 3 | 75.00% | $9,774 | 4.16% | $407 | $407 | $1,396 | −$989 | 12.84% |
| 4 | 50.00% | $14,661 | 7.08% | $1,038 | $871 | $1,629 | −$758 | 12.83% |
| 5 | 30.00% | $19,059 | 8.54% | $1,628 | $1,058 | $1,466 | −$408 | 12.81% |
| 6 | 25.20% | $23,862 | 9.27% | $2,212 | $1,438 | $1,601 | −$163 | 12.13% |
| 7 | 20.40% | $28,729 | 9.64% | $2,768 | $1,799 | $1,623 | $177 | 11.96% |
| 8 | 15.60% | $33,211 | 9.82% | $3,261 | $2,119 | $1,494 | $625 | 11.69% |
| 9 | 10.80% | $36,798 | 9.91% | $3,646 | $2,370 | $1,196 | $1,174 | 11.15% |
| 10 | 6.00% | $39,006 | 9.95% | $3,883 | $2,524 | $736 | $1,788 | 9.61% |
| TY | 6.00% | $41,346 | 10.00% | $4,135 | $2,688 | $807 | $1,881 | 9.61% |

Amazon's discount-rate inputs (Jan 2000): riskfree 6.5%; beta 1.60 (dot-com retailer bottom-up) fading to 1.00; ERP 4%; cost of equity 12.90% → 10.50%; synthetic BBB rating from average interest coverage over the next five years → pre-tax cost of debt 6.5% + 1.5% = 8.0%; debt ratio drifting from 1.2% to the 15% retail-industry average; tax rate 0% (NOL of $500m) → 35%.

Regression-beta uselessness (why rule 7 exists): Amazon's 2-year weekly regression beta vs the S&P 500 was raw 2.23 / adjusted 1.82, R² = 0.17, standard error of beta 0.50.

Later Amazon stories, same machinery, different end-states:

| Input | Amazon 2019 (price $1,970.19) | Amazon 2020 (price $3,260.48) |
|---|---|---|
| Base revenues | $208,125m | $321,782m |
| Revenue growth | 15% yrs 1–5 → 3% yrs 6–10 | 25% in 2020, 20% yrs 1–5 → 2% yrs 6–10 |
| Operating margin | 7.71% → 12.50% | 7.99% (7.5% in 2020) → 12.00% |
| Tax rate | 20.20% → 24.00% | 16.99% → 25.00% |
| Sales-to-capital | 5.95 (marginal ROIC 89.16%) | 1.95 (marginal ROIC 25.94%) |
| Terminal RIR / ROC | 30.00% / 10.00% | 16.67% / 12.00% |
| Cost of capital | 7.97% → 7.50% | 6.11% flat |
| Terminal value / PV(TV) | $925,287m / $435,438m | $2,396,245m / $1,323,967m |
| PV of 10-yr cash flows | $206,707m | $128,131m (FCFF negative yrs 1–5, e.g. yr 1 −$16,313m) |
| Operating assets | $642,144m | $1,452,098m |
| Failure probability | 0% | 0% |
| Equity bridge | − debt & MI $45,435m + cash $27,050m | − debt & MI $91,401m + cash $71,391m |
| Value / share | $1,255.05 (497.00 shares) | $2,827.42 (506.50 shares) |

Negative-earnings model schedule (fcffneg.xls, the n-stage model built for exactly this case) — a template for how the year-by-year inputs are entered and faded:

| Year | Rev growth | EBITDA/Revenue | Capex growth | Depreciation growth | WC % of revenue |
|---|---|---|---|---|---|
| 1 | 0.00 | 0.000 | −0.20 | 0.10 | 0.03 |
| 2 | 0.30 | 0.075 | −0.50 | 0.10 | 0.03 |
| 3 | 0.25 | 0.150 | −0.50 | 0.10 | 0.03 |
| 4 | 0.20 | 0.225 | −0.50 | 0.10 | 0.03 |
| 5 | 0.10 | 0.300 | 0.05 | −0.50 | 0.03 |
| 6 | 0.10 | 0.306 | 0.05 | −0.50 | 0.03 |
| 7 | 0.10 | 0.312 | 0.05 | 0.05 | 0.03 |
| 8 | 0.08 | 0.318 | 0.05 | 0.05 | 0.03 |
| 9 | 0.06 | 0.324 | 0.05 | 0.05 | 0.03 |
| 10 | 0.05 | 0.330 | 0.05 | 0.05 | 0.03 |

In that model beta and pre-tax cost of debt hold their high-growth values through year n/2 and then move **linearly** to their stable values: `x_t = x_high − (x_high − x_stable) × (t − n/2)/(n/2)` for t in (n/2, n]. With β 2.0 → 1.0 and k_d 8.9% → 8.0% over years 6–10, WACC runs 11.62% (years 1–5, no tax shield because the NOL kills it) → 7.74% stable.

**Worked example:** Amazon, January 2000. Terminal value = 1,881 / (0.0961 − 0.06) = $52,148m. Discounting the FCFF stream above at the year-specific costs of capital gives value of operating assets $15,170m; + cash $26m = firm $15,196m; − debt $349m = equity $14,847m; − equity options $2,892m (all outstanding options valued as options at the then-$84 stock price) = $11,955m; ÷ shares = **$35.08 per share** versus a market price of $84 — overvalued. (The Spring-2020 edition of the same slide carries operating assets of $14,910m and prints $34.32 per share; the difference is rounding in the operating-asset total, not a different model.)

Second worked example, fcffneg.xls end-to-end: revenues 3,789 → 11,821 by year 10, EBITDA margin 0% → 33%, EBIT negative through year 4 and positive from year 5; the NOL of 2,075 grows with early losses to 6,170 and is exhausted during year 7, so taxes are 0 for years 1–6, 8.84 in year 7 and full 35% after. FCFF runs −3,431, −1,380, +29, 1,197, 1,966, 2,238, 2,536, 1,804, 1,965, 2,113. PV of high-growth FCFF = 2,446.42; terminal FCFF = 2,243.06 × (1 − 0.05/0.09) = 996.92; TV = 996.92/(0.07742 − 0.05) = 36,362.96, PV 13,470.92. Firm 15,917.34 + cash 1,477 − debt 7,271 = equity 10,123.34; − options 299.73 = 9,823.61; ÷ 886.467 shares = **$11.08 per share** versus a $12.57 market price.

**Determinism:** DETERMINISTIC once the assumption set is fixed — (base revenues, growth path, year-1 margin, target margin, convergence year, tax rates, NOL, sales-to-capital, cost-of-capital path, terminal growth and ROC, cash, debt, shares, option value) → revenues, EBIT, taxes, reinvestment, FCFF, WACC path, terminal value, equity value, value per share. A script can reproduce every table above exactly. JUDGMENT: the target margin (needs the mature sector's margin distribution), the growth path (needs market size, competitive structure and post-IPO fade evidence), the sales-to-capital ratio (sector or own history), the convergence year, the terminal ROC, and the failure probability. Also judgment: whether the base-year numbers need R&D or lease restatement first.

**Pitfalls:**
- Using the regression beta of a young stock (Amazon's had an R² of 0.17 and a standard error of 0.50) instead of a bottom-up sector beta.
- Loading failure risk into the discount rate. Failure belongs in a probability-weighted value, not in `r`; doing both double-counts.
- Holding the cost of capital constant for ten years when the whole story is that the firm matures.
- Forgetting to pay for growth — revenue growth without reinvestment produces absurd imputed returns on capital.
- Believing your own margin forecast. Amazon's assumed 10% mature margin never arrived: actual operating margin peaked at 6.36% (2004) and fell to 1.00% (2013) and 0.11% (2014 LTM), while actual revenues eventually blew past the forecast ($85,247m actual vs $51,460m forecast in 2014). The direction call was right and nearly every line item was wrong.
- Letting revenue growth persist above the industry average for a decade after the IPO.
- Adding a separate dilution haircut on top of the DCF ([[dilution-and-employee-options]]).

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.297-303
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.311-312
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.288-294
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.302
- spreadsheet model doc: special-troubled.md — fcffneg.xls (n-stage FCFF model for negative-earnings firms)
- spreadsheet model doc: ginzu-fcff-corona.md — fcffsimpleginzuCorona.xlsx (margin convergence, NOL row, reinvestment, terminal ROC)

**Related:** [[sales-to-capital-reinvestment]], [[dilution-and-employee-options]], [[distress-and-failure-adjusted-value]], [[scenario-analysis-and-simulation]], [[difficult-company-taxonomy]], [[value-versus-price]], [[bottom-up-beta]], [[terminal-value]], [[synthetic-rating]], [[cost-of-capital]]
