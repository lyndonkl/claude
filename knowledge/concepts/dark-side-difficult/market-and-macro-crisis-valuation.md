# Valuing the market, and revaluing companies in a macro shock

**Core idea:** Intrinsic value is not a fixed anchor that the market wanders around. It moves too, because it is built from macro inputs — the riskfree rate, the equity risk premium, base earnings — and those inputs move violently in a crisis. The same discipline that values a company values the whole market: base earnings, an expected growth path, the share of earnings returned as dividends and buybacks, and a required return equal to the riskfree rate plus the equity risk premium. Doing this in a crisis forces you to convert fear and hope into numbers, and it gives you a benchmark for judging whether a market that looks disconnected from the economy actually is.

**Formulas:**
- Value of the index: `Value = Σ_{t=1..5} E(CF_t)/(1 + r)^t + E(CF_6)/[(r_stable − g)(1 + r)^5]`, where `E(CF_t)` = expected aggregate dividends plus buybacks in year `t`, `r` = riskfree rate + equity risk premium, and `g` = perpetual growth, capped at the riskfree rate.
- Augmented dividends: `Cash returned = Dividends + Buybacks`. `Cash payout ratio = Cash returned / Earnings`.
- Sustainable payout in stable growth: `Payout = 1 − g / ROE`.
- Implied equity risk premium: solve for the `r` that sets the present value of expected index cash flows equal to the current index level, then subtract the riskfree rate.
- Company revaluation in a shock, one term at a time: `Cost of equity = riskfree + β × ERP`; `After-tax cost of debt = (riskfree + default spread) × (1 − t)`; `Expected growth = Reinvestment rate × Return on capital`; `TV_n = FCFF_{n+1}/(WACC_stable − g)`.
- Tax-change decomposition: a lower effective tax rate raises the after-tax return on capital and so growth; a lower marginal rate raises the after-tax cost of debt and so the cost of capital. Net value change = the two effects combined.

**Procedure (valuing the index):**
1. Take base-year aggregate earnings and base-year cash returned (dividends plus buybacks).
2. Forecast the earnings path. In a crisis, split the shock into a transitory part and a permanent part, and say what fraction is recovered by which year.
3. Forecast the cash payout ratio path. Companies cut dividends and, far more sharply, buybacks in a downturn; the payout then recovers toward the long-run level.
4. Set the required return: current riskfree rate plus an equity risk premium anchored on the historical average of the **implied** premium over a stated window.
5. Decide what happens to both after year 5 — the riskfree rate may normalize upward and the premium may revert to its long-run average.
6. Cap perpetual growth at the riskfree rate.
7. Discount, compare with the index level, and then simulate the whole thing ([[scenario-analysis-and-simulation]]).

**Procedure (revaluing a company in a shock):**
1. Change the base earnings if the shock hits current operations.
2. Change the growth inputs — usually a lower reinvestment rate, a lower return on capital, or both.
3. Change the equity risk premium and the default spread, which both spike in a crisis.
4. Change the capital-structure path if the firm can no longer move to its target debt ratio.
5. Rerun and attribute the change in value to each input, so the story is auditable.

**Reference data (1):** S&P 500 cash returned, 2001–2019 — the base for any index valuation.

| Year | Earnings | Dividends | Buybacks | Cash returned as % of earnings | Cash returned as % of market cap |
|---|---|---|---|---|---|
| 2007 | 82.54 | 28.14 | 67.22 | 115.53% | 6.49% |
| 2008 | 49.51 | 28.45 | 39.07 | 136.37% | 7.47% |
| 2009 | 56.86 | 21.97 | 15.46 | 65.82% | 3.36% |
| 2015 | 100.48 | 43.41 | 64.94 | 107.83% | 5.30% |
| 2018 | 152.78 | 54.39 | 96.11 | 98.51% | 6.00% |
| 2019 | 163.00 | 58.50 | 87.81 | 89.76% | 4.53% |
| **Median 2001–2019** | | | | **83.40%** | **4.82%** |
| High / Low | | | | 136.37% / 57.74% | 7.47% / 2.84% |

Buybacks are now as large as or larger than dividends, and total payout exceeds 100% of earnings in stress years.

**Reference data (2):** Implied equity risk premium averages, used to anchor the required return.

| Period | Average implied ERP |
|---|---|
| 1960–2019 | 4.20% |
| 2000–2019 | 4.86% |
| 2010–2019 | 5.58% |

The implied premium has ranged from about 2% at the 1999–2000 bubble peak to about 6.5% in the late 1970s and in 2008–09.

**Reference data (3):** Why the market can rise while the economy collapses. Correlation of quarterly US stock returns with real GDP growth, 1960–2020.

| Real GDP measure | Correlation with stock return |
|---|---|
| Same quarter | −0.0592 |
| One quarter ahead | 0.1201 |
| Two quarters ahead | 0.2320 |
| Three quarters ahead | 0.2626 |
| Four quarters ahead | 0.2633 |

Stocks correlate poorly with current GDP and better with future GDP. Markets are forward-looking, which explains the apparent 2020 disconnect.

**Worked example (1):** S&P 500, 1 November 2020. Base 2019 earnings 163, cash returned 146.30 (dividends 58.5 plus buybacks 87.8, a payout of about 89.75%). Story: earnings fall to 130 in 2020 and recover to 166 in 2021; 80% of the earnings drop is transitory and 20% permanent; dividends fall 20% and buybacks 50% in 2020, with cash returned staying depressed through 2024.

| Year | 2021 | 2022 | 2023 | 2024 | 2025 (terminal) |
|---|---|---|---|---|---|
| Expected earnings | 166.21 | 173.14 | 180.36 | 187.89 | 191.65 |
| Cash payout ratio | 78.16% | 81.33% | 84.49% | 87.65% | 87.65% |
| Expected cash returned | 129.92 | 140.81 | 152.39 | 164.69 | 167.99 |

Year-1 (2020) expected earnings 130.21 with a 75.00% payout, giving 97.66 of cash returned. Discount rate for years 1–5 = 0.88% riskfree (10-year T-bond) + 5.58% ERP (the 2010–19 average implied premium) = **6.46%**. After year 5 the riskfree rate rises to 2.00% and the ERP reverts to 4.82%, so the terminal required return is 6.82% and perpetual growth is capped at 2.00%.

Terminal value = 167.99/(0.0682 − 0.02) = **3,481.65**. Present values: 91.73, 114.63, 116.70, 118.64, and 2,666.40 (year-5 cash flow plus terminal value) → intrinsic value **3,108**. The index traded at 3,270, about 5% overvalued. The simulation put the median at 3,091.51 and the price between the 70th and 80th percentiles.

For contrast, the same index a year earlier (1 January 2020) with an augmented dividend discount model: base cash returned 150.50, analyst growth 3.96% for five years, stable growth 1.92% (the riskfree rate), cost of equity 1.92% + 1.00 × 5.00% = 6.92%. Projected augmented dividends 156.46, 162.65, 169.08, 175.77, 182.73; terminal value = (182.73 × 1.0192)/(0.0692 − 0.0192) = 3,274.75; intrinsic value **3,357.86** against an index level of 3,230.78. Redoing it with fundamentals rather than analyst growth — stable payout = 1 − 1.92%/18.44% ROE = 89.66%, payouts trending down from 92.33% — lowers the value to **3,268.95**. Making growth and payout consistent removes roughly 90 points of value.

**Worked example (2):** 3M, before and after the 2008 crisis. Same company, same model, five weeks apart.

| Input | 12 September 2008 | 16 October 2008 |
|---|---|---|
| Base EBIT(1−t) | 5,344 × (1 − 0.35) = 3,474 | 4,810 × 0.65 = 3,180 (base income cut 10%) |
| FCFF (base) | 2,433 | 2,139 |
| Reinvestment rate / ROC | 29.97% / 25.19% | 33% / 23.06% |
| Expected growth | 0.30 × 0.25 = 7.5% | 0.25 × 0.20 = 5% |
| Equity risk premium | 4% | 6% |
| Cost of equity | 3.72% + 1.15 × 4% = 8.32% | 3.96% + 1.15 × 6% = 10.86% |
| After-tax cost of debt | (3.72% + 0.75%)(1 − 0.35) = 2.91% | (3.96% + 1.5%)(1 − 0.35) = 3.55% |
| Cost of capital | 7.88% | 10.27% |
| Stable phase | g 3%, beta 1.10, debt ratio 20%, WACC 6.76%, ROC 6.76%, RIR 44% | g 3%, beta 1.00, ERP 4%, debt ratio stays 8%, WACC 7.55%, ROC 7.55%, RIR 40% |
| Terminal value | 2,645/(0.0676 − 0.03) = 70,409 | 2,434/(0.0755 − 0.03) = 53,481 |
| Operating assets | 60,607 | 43,975 |
| Equity (+cash 3,253 − debt 4,920) | 58,400 | 42,308 |
| **Value per share** | **$83.55** (price $70) | **$60.53** (price $57) |

A $23 drop in intrinsic value in five weeks, caused by a higher equity risk premium, a wider default spread, lower base earnings and lower growth. Value is not a constant.

**Worked example (3):** The 2017 US tax reform, valued on aggregate US equities as at 1 January 2018. The federal rate fell from 35% to 21%, the overall marginal rate from 38% to 24%, and the effective rate from 25.19% to 20%. Three channels: a lower effective rate raised the after-tax return on capital from 12.76% to 13.65% and, with reinvestment rising from 59.27% to 65%, lifted expected growth from 7.56% to 8.87%; a lower marginal rate raised the after-tax cost of debt from 2.42% to 2.97% and the cost of capital from 6.57% to 6.70%; the net effect lifted the aggregate value of US equities from $24,750bn to $27,151bn, a gain of **$2,400bn, or 9.70%**. Macro inputs: T-bond rate 2.41%, ERP 5.08%, beta 1.07, debt-to-capital 23.51%.

**Determinism:** DETERMINISTIC — (base earnings, earnings path, payout path, riskfree rate, ERP, terminal riskfree rate and ERP, perpetual growth) → index value; (index level, expected cash flows) → implied ERP; and every company revaluation once the changed inputs are set. All three worked examples reproduce exactly. JUDGMENT: the earnings path and the split between transitory and permanent damage, the payout cuts and their recovery, the equity risk premium and the averaging window that anchors it, whether and when the riskfree rate normalizes, and how much of a crisis to build into a single company's base earnings.

**Pitfalls:**
- Reading a stock-market rally against terrible current macro data as proof of irrationality. Stock returns correlate negatively with current-quarter GDP and positively with GDP three to four quarters ahead.
- Valuing the index off dividends alone. Buybacks are now as large as dividends and total payout regularly exceeds 100% of earnings.
- Using analyst growth with an unadjusted payout ratio. Growth and payout are linked by `payout = 1 − g/ROE`; ignoring that inflates value.
- Assuming the crisis-level riskfree rate and the crisis-level equity risk premium both persist forever. They usually revert, in opposite directions, and the terminal value is where that matters.
- Letting perpetual growth exceed the riskfree rate.
- Treating a fall in your own intrinsic value estimate during a crisis as a mistake. If base earnings, the equity risk premium and default spreads have all moved, value has moved.
- Changing several macro inputs at once without attributing the value change to each. The 3M example is instructive precisely because each change is separable.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.282-292
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.281-283

**Related:** [[scenario-analysis-and-simulation]], [[value-versus-price]], [[commodity-and-cyclical-valuation]], [[distress-and-failure-adjusted-value]], [[difficult-company-taxonomy]], [[implied-equity-risk-premium]], [[equity-risk-premium]], [[riskfree-rate]], [[terminal-value]]
