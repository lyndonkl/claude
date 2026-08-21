# Valuing a declining firm (negative growth, negative reinvestment)

**Core idea:** A declining firm has a long history that is worse than useless, because it describes a business that is shrinking. Revenues fall, margins are thin, and much of the invested capital earns less than the cost of capital. A well-managed declining firm does **not** fight the decline. It shuts or sells the investments that do not cover their cost of capital, which means depreciation exceeds capital spending, working capital shrinks, and the overall reinvestment rate turns negative. That asset shedding is a source of cash, and the surviving business can be both smaller and better. The investor's nightmare is management in denial, which grows revenues and operating income by making more sub-cost-of-capital investments and destroys value all the way.

**Formulas:**
- Negative growth path: `Rev_t = Rev_{t−1} × (1 + g_t)` with `g_t < 0` in early years, moderating toward a small positive or zero rate.
- Margin recovery: linear improvement from the depressed base margin to a sector-median margin by year 10.
- Reinvestment: `Reinvestment_t = (Rev_t − Rev_{t−1}) / (Sales/Capital)` — automatically negative when revenues fall. Net capex can be negative (depreciation > capex) as stores, plants or real estate are sold.
- `FCFF_t = EBIT(1−t)_t − Reinvestment_t`, so shrinking firms can show FCFF **above** after-tax operating income.
- Stable-phase reinvestment rate: `RIR = g/ROC`, which is negative when `g < 0`. (Heineken, Sept 2019: `g = −0.5%`, `ROC = 5%`, `RIR = −10%`.)
- Distress overlay: `Value of operating assets = (PV of FCFF + PV of terminal value) × (1 − P(failure)) + Distress proceeds × P(failure)` — see [[distress-and-failure-adjusted-value]].

**Procedure:**
1. Establish the base year honestly: current revenues, current (usually depressed) operating margin, current tax rate, and the invested capital.
2. Set a **negative** revenue growth path and a moderation schedule. JC Penney: −3% a year for five years, then −2%, −1%, 0%, +1%, +2% in years 6–10.
3. Set the margin target at the sector median rather than the firm's own better past. JC Penney used the US retail-sector median of 6.25%, reached in year 10 from a 1.32% base.
4. Let the tax rate rise toward the marginal rate as losses and shields run out (JC Penney: 35% → 40% by year 10).
5. Let reinvestment be negative while revenues shrink. Book the cash released from real estate and working capital as it comes.
6. Set the cost of capital high at the start if the cost of debt is high, and let it fall as leverage and risk normalize (JC Penney: 9.00% → 8.00% by year 10).
7. Value the terminal year on a much smaller, healthier business.
8. Ask whether survival is genuinely at risk. High debt plus weak earnings means the going-concern DCF overstates value; overlay a failure probability and a distress-sale value.
9. Test management's behaviour. If revenues and operating income are being grown by investing below the cost of capital, the "growth" is value destruction and the model should show it as such (reinvestment high, ROC below WACC, value falling).

**Reference data:** JC Penney, full declining-firm DCF (Figure 14.5). Base year: revenues $12,522m, EBIT margin 1.32%, EBIT $166m, tax rate 35%, EBIT(1−t) $108m.

| Year | Rev growth | Revenues | Op margin | EBIT | Tax rate | EBIT(1−t) | Reinvestment | FCFF | Cost of capital | PV(FCFF) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | −3.00% | $12,146 | 1.82% | $221 | 35% | $143 | −$188 | $331 | 9.00% | $304 |
| 2 | −3.00% | $11,782 | 2.31% | $272 | 35% | $177 | −$182 | $359 | 9.00% | $302 |
| 3 | −3.00% | $11,428 | 2.80% | $320 | 35% | $208 | −$177 | $385 | 9.00% | $297 |
| 4 | −3.00% | $11,086 | 3.29% | $365 | 35% | $237 | −$171 | $409 | 9.00% | $290 |
| 5 | −3.00% | $10,753 | 3.79% | $407 | 35% | $265 | −$166 | $431 | 9.00% | $280 |
| 6 | −2.00% | $10,538 | 4.28% | $451 | 36% | $289 | −$108 | $396 | 8.80% | $237 |
| 7 | −1.00% | $10,433 | 4.77% | $498 | 37% | $314 | −$53 | $366 | 8.60% | $201 |
| 8 | 0.00% | $10,433 | 5.26% | $549 | 38% | $341 | $0 | $341 | 8.40% | $173 |
| 9 | 1.00% | $10,537 | 5.76% | $607 | 39% | $370 | $52 | $318 | 8.20% | $149 |
| 10 | 2.00% | $10,748 | 6.25% | $672 | 40% | $403 | $105 | $298 | 8.00% | $129 |

Terminal value $5,710m; PV of terminal value $2,479m; PV of the 10-year cash flows $2,362m; sum of PV $4,841m.

A second declining-firm pattern, with a negative riskfree rate: Heineken in euros, September 2019. Base revenues €23,119m, operating margin 14.86%, sales-to-invested-capital 0.71 (5-year average 0.79), ROIC 7.46%, effective tax rate 29.70%. Revenues grow 3.22% a year for five years and then taper to −0.5% by year 10, matching the euro riskfree rate of −0.50%. Margin drifts down to 14.00%; the tax rate goes to 25%. Cost of equity = −0.50% + 1.20 × 6.83% = 7.66%; after-tax cost of debt = (−0.5% + 2%) × (1 − 0.25) = 1.13%; WACC = 7.66% × 0.599 + 1.13% × 0.401 = 5.04%. Stable phase: `g = −0.5%`, cost of capital 5%, ROC 5%, `RIR = −10%`, terminal reinvestment −€297m. Terminal value = 2,972/(0.05 − (−0.005)) = €54,034m. Operating assets €51,691.19m; − debt €19,709.52m − minority interests €1,069m + cash €1,751.60m + non-operating assets €1,401m = equity €34,065.26m; ÷ 571.10 shares = **€59.65 per share** versus a €93.25 price.

**Worked example:** JC Penney. The going-concern DCF sums to $4,841m. The high debt load and weak earnings put survival at risk, so the bond rating implies a **20% probability of failure**, with liquidation recovering **50% of book value**, i.e. $2,421m. Value of operating assets = 4,841 × 0.80 + 2,421 × 0.20 = **$4,357m**. Note the shape of the cash flows: FCFF of $331m in year 1 exceeds EBIT(1−t) of $143m precisely because reinvestment is −$188m.

**Determinism:** DETERMINISTIC — (base revenues and margin, negative growth path, margin-recovery path, tax path, sales-to-capital or explicit reinvestment path, cost-of-capital path, terminal inputs, failure probability, distress proceeds) → FCFF, PVs, terminal value, distress-weighted operating assets. JUDGMENT: how fast revenues decline and when the decline moderates, the sector-median margin target and whether the firm can reach it, how much cash the asset sales release, the failure probability, and the liquidation recovery percentage.

**Pitfalls:**
- Forecasting positive growth because the model template assumes it. A declining business needs negative growth and negative reinvestment.
- Blocking negative reinvestment, which throws away the real cash released by shutting stores or selling real estate.
- Anchoring the margin target on the company's own historical best rather than the sector median.
- Valuing a declining, highly levered firm as a pure going concern. Without the distress overlay the DCF overstates value.
- Cheering revenue growth at a declining firm. If new investments earn below the cost of capital, revenue and operating income can rise while value falls.
- Forgetting the equity-side claims that decline exposes: underfunded pension obligations, litigation claims, and liquidation preferences all reduce what common equity receives.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.319-321
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.310-312
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.320

**Related:** [[distress-and-failure-adjusted-value]], [[bond-implied-distress-probability]], [[sales-to-capital-reinvestment]], [[value-of-control-and-restructuring]], [[currency-consistency-and-invariance]], [[difficult-company-taxonomy]], [[terminal-value]]
