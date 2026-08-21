# Value of control: status quo versus optimally run

**Core idea:** A mature company is easy to value on its own history. The hard case is when you expect that history to be abandoned — because management changes, an activist arrives, or an acquirer forces change. The fix is to value the same company **twice**: once with existing policies (status quo) and once as it would be run optimally. The gap between the two is the value of control. What you actually pay for is that gap multiplied by the probability that change happens. Optimal management has two levers: operating restructuring (invest more, and at higher returns) and financial restructuring (move to the debt ratio that minimizes the cost of capital). Both are easy to write down and hard to execute, so the probability weight matters as much as the gap.

**Formulas:**
- `Expected growth in EBIT(1−t) = Reinvestment rate × Return on capital`.
- `Cost of capital = Cost of equity × (1 − Debt ratio) + Pre-tax cost of debt × (1 − tax rate) × Debt ratio`.
- `Value of control per share = Optimally-managed value per share − Status-quo value per share`.
- `Expected value per share = Status-quo value × (1 − P(change)) + Optimal value × P(change)`.
- Optimal debt ratio = the debt ratio that **minimizes** the cost of capital, which (holding operating cash flows fixed) **maximizes** firm value. Firm value at each debt ratio is the same cash-flow stream discounted at that ratio's WACC.
- Value-creation test: growth adds value only when `ROIC > Cost of capital`. If `ROIC < Cost of capital`, growth destroys value.
- Levered beta at each candidate debt ratio: `β_L = β_U × (1 + (1 − t) × D/E)`; the rating (and so the pre-tax cost of debt) is reset from the interest coverage ratio at that debt level — see [[synthetic-rating]].

**Procedure:**
1. **Value the status quo.** Use the company's actual reinvestment rate, actual return on capital, actual debt ratio. Hormel 2008: RIR 19.14%, ROC 14.34%, growth 2.75% for 3 years, debt ratio 10.4%, cost of capital 6.79%.
2. **Diagnose the three failures.** Does it invest too little or too much? Does it earn less than its cost of capital on what it invests? Is the financing mix wrong?
3. **Build the operating restructuring.** Raise the reinvestment rate to what the opportunity set supports and set the return on new capital at a defensible level. Recompute growth as RIR × ROC and extend the growth period if the improvement is durable. Hormel: RIR 40%, ROC 14.00% → growth 5.60% for 5 years.
4. **Build the financial restructuring.** Run the cost of capital across debt ratios from 0% to 90% in 10-point steps. At each step relever the beta, reset the rating and the pre-tax cost of debt from interest coverage, and recompute WACC and firm value. Pick the minimum-WACC ratio. Above roughly **80% debt**, operating income no longer covers interest, so the effective tax rate must be cut to reflect the lost tax benefit.
5. **Value the optimally-run firm** with the new growth and the new cost of capital.
6. **Estimate P(change).** Consider the ownership structure, voting rights, activist presence, takeover defenses, board composition and age or tenure of management. Hormel used 10%.
7. **Blend**: expected value = status-quo × (1 − p) + optimal × p.
8. **Discount the restructuring story for execution risk.** Cost-cutting targets are met only when top management backs them and the targets are explicit; without that evidence, haircut the assumed improvement.

**Reference data (1):** Hormel Foods, January 2009 — cost of capital and firm value by debt ratio. Current ratio 10.39%; optimum lies between 20% and 30%.

| Debt ratio | Beta | Cost of equity | Bond rating | Interest rate on debt | Tax rate | After-tax cost of debt | WACC | Firm value |
|---|---|---|---|---|---|---|---|---|
| 0% | 0.78 | 7.00% | AAA | 3.60% | 40.00% | 2.16% | 7.00% | $4,523 |
| 10% | 0.83 | 7.31% | AAA | 3.60% | 40.00% | 2.16% | 6.80% | $4,665 |
| 10.39% (current) | 0.83 | 7.33% | AAA | 3.60% | 40.00% | 2.16% | 6.79% | $4,680 |
| 20% | 0.89 | 7.70% | AAA | 3.60% | 40.00% | 2.16% | 6.59% | $4,815 |
| 30% | 0.97 | 8.20% | A+ | 4.60% | 40.00% | 2.76% | 6.57% | $4,834 |
| 40% | 1.09 | 8.86% | A− | 5.35% | 40.00% | 3.21% | 6.60% | $4,808 |
| 50% | 1.24 | 9.79% | B+ | 8.35% | 40.00% | 5.01% | 7.40% | $4,271 |
| 60% | 1.47 | 11.19% | B− | 10.85% | 40.00% | 6.51% | 8.38% | $3,757 |
| 70% | 1.86 | 13.52% | CCC | 12.35% | 40.00% | 7.41% | 9.24% | $3,398 |
| 80% | 2.70 | 18.53% | CC | 14.35% | 38.07% | 8.89% | 10.81% | $2,892 |
| 90% | 5.39 | 34.70% | CC | 14.35% | 33.84% | 9.49% | 12.01% | $2,597 |

**Reference data (2):** Global excess-return distribution, January 2017, roughly 32,000 firms — the empirical base for "growth is not automatically good".

| ROIC − cost of capital | Firms | Share |
|---|---|---|
| −6% or worse | ~5,200 | — |
| −6% to −2% | ~5,750 | — |
| **At least 2% below cost of capital (laggards)** | **10,961** | **33.96%** |
| −2% to 0% | ~2,150 | — |
| 0% to +2% | ~8,900 | — |
| **Within ±2% (running in place)** | **11,049** | **34.23%** |
| +2% to +6% | ~2,600 | — |
| +6% to +10% | ~1,800 | — |
| Above +10% (super winners) | 5,865 | — |
| **At least 2% above cost of capital (value creators)** | **10,264** | **31.80%** |

**Reference data (3):** Why cost-cutting assumptions need evidence. Survey of 178 companies that met their cost-reduction targets, ranked by the share of respondents naming each factor in their top two: top-management support 44%; clear targets 39%; clear, well-planned approach 31%; necessary talent and capabilities 22%; sufficient accountability 19%; fact base for decisions 15%; sufficient communication 8%; smaller-than-expected financial-crisis impact 7%; investment in critical functional capabilities 3%; union support 3%; incentives in place 2%; supportive regulations 0%.

**Worked example:** Hormel Foods, 2008 (after-tax operating income $315m, 5% compounded growth over the prior five years).
- *Status quo:* growth = 14.34% × 19.14% = 2.75% for 3 years; cost of capital = 7.33% × (1 − 0.104) + 3.60% × (1 − 0.40) × 0.104 = 6.79%; beyond year 3, growth 2.35%, ROC 7.23%, RIR 32.52%, cost of capital 7.23%. Operating assets $4,682m; + cash $155m − debt $491m − management options $53m = equity $4,293m → **$31.91 per share**.
- *Optimally run:* operating restructuring gives growth = 14.00% × 40% = 5.60% for 5 years; financial restructuring moves the debt ratio to 20%, so cost of capital = 7.75% × (1 − 0.20) + 3.60% × (1 − 0.40) × 0.20 = 6.63% (the cost of equity rises, the WACC falls). Beyond year 5: growth 2.35%, ROC 6.74%, RIR 34.87%, cost of capital 6.74%. Operating assets $5,475m → equity $5,085m → **$37.80 per share**.
- *Value of control:* $37.80 − $31.91 = **$5.89 per share**. With a 10% probability of management change, expected value = 31.91 × 0.90 + 37.80 × 0.10 = **$32.50 per share**.

**Determinism:** DETERMINISTIC — (reinvestment rate, ROC, growth period, cost-of-equity and cost-of-debt inputs, debt ratio) → growth, WACC, firm value, per-share value for each scenario; and (status-quo value, optimal value, P(change)) → expected value. The whole optimal-capital-structure table is deterministic given the levered-beta mechanics and a rating/spread schedule. JUDGMENT: the optimal reinvestment rate and return on new capital (needs the sector's ROC distribution and the firm's project pipeline), the rating assigned at each debt level, the probability of management change (needs ownership, voting rights, activist activity, takeover market), and how much of the promised cost cutting to believe.

**Pitfalls:**
- Valuing the optimally-run firm and quoting that as *the* value. Without a probability of change you are valuing a company that does not exist yet.
- Assuming margin improvement with no evidence of top-management commitment or clear targets.
- Assuming that more growth is always better. Roughly two-thirds of global firms earn a return within 2% of, or below, their cost of capital, so their growth adds little or destroys value.
- Forgetting that raising the debt ratio raises the cost of equity; only the weighted average may fall, and only up to a point.
- Ignoring the tax-benefit cutoff at very high leverage, which flatters the WACC of an over-levered structure.
- Treating weak corporate governance as a flat valuation discount instead of as a low probability of the optimal scenario — see [[return-improvement-and-governance-drag]].

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.313-318
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.304-309

**Related:** [[return-improvement-and-governance-drag]], [[difficult-company-taxonomy]], [[declining-firm-valuation]], [[synthetic-rating]], [[cost-of-capital]], [[optimal-capital-structure]], [[bottom-up-beta]], [[value-versus-price]]
