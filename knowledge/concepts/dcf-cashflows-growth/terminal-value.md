# Terminal value and the stable-growth phase

**Core idea:** A going concern potentially lives forever, but you cannot forecast cash flows forever. So you forecast explicitly for a finite growth period and capture everything beyond it in a terminal value. This one number typically carries the majority of a DCF's value, and it is where most valuations go wrong — not because the perpetuity formula is hard, but because the assumptions behind it are rarely made internally consistent. Four disciplines fix that: obey the growth cap (stable growth cannot exceed the growth rate of the economy, proxied by the riskfree rate), do not stretch the high-growth period, make the firm *earn* its terminal growth by reinvesting `g/ROC`, and make every stable-period input look like a mature firm.

**Formulas:**
- Structure: `Value = SUM over t=1..N of CF_t/(1+r)^t + Terminal value / (1+r)^N`, where `N` = the length of the explicit growth period.
- **Growing perpetuity:** `Terminal value_N = CF_(N+1) / (r − g)`, with `r` matched to the cash flow (cost of capital for FCFF, cost of equity for FCFE/dividends) and `g` the constant growth rate forever.
- **Firm version with reinvestment built in:** `Terminal value_N = EBIT_(N+1) × (1 − t) × (1 − g/ROC) / (Cost of capital − g)`
- **Stable-period reinvestment rate** `= g / ROC` (firm) and **stable-period payout ratio** `= 1 − g/ROE` (equity).
- Growth-rate decomposition and cap: `Riskfree rate = Expected inflation + Expected real interest rate`; `Nominal GDP growth = Expected inflation + Expected real growth`. Because the two share the inflation component and the real components converge in a mature economy, the **riskfree rate is a serviceable proxy and cap for nominal economy growth**, and hence for stable growth.
- Consistency check in reverse (see [[return-on-invested-capital]]): `Embedded reinvestment rate = 1 − FCFF_terminal/EBIT(1−t)_terminal`; `Implied perpetual ROC = g / embedded reinvestment rate`.

**Procedure:**
1. **Choose the length of the explicit growth period `N`.** Tie it to competitive advantages, not to convention. It is not growth that creates value but growth with excess returns, so the growth period is really the period over which the firm can keep competition at bay. Proposition 1: the stronger and more sustainable the moat, the longer value-creating growth lasts. Proposition 2: firms with strong, durable moats are rare. Practical drivers: larger firm -> shorter period; higher current growth -> longer; stronger barriers to entry -> longer. Analysts systematically assume periods that are too long.
2. **Set the stable growth rate `g`, obeying the cap.** `g <= growth rate of the economy`, proxied by the riskfree rate in the valuation currency. It can be set lower — a mature firm in an economy that also contains high-growth firms probably grows below the aggregate rate. It can even be negative, in which case the firm gradually shrinks and the terminal value falls accordingly. Match the convention: nominal cash flows require a nominal `g` in the valuation currency.
3. **Keep `g` consistent with the riskfree rate.** The riskfree rate embeds an implicit view about nominal economy growth. Pairing a high `g` with a low riskfree rate systematically **overvalues**; pairing a low `g` with a high riskfree rate **undervalues**. Capping `g` at the riskfree rate keeps numerator and denominator telling the same story.
4. **Choose the perpetual return on capital.** ROC = cost of capital makes growth value-neutral (see the sensitivity table). Allowing ROC > cost of capital forever asserts a permanent moat and must be argued. The empirical evidence supports fading *growth* toward the economy's rate faster than you fade *excess returns*: median ROIC of large US firms is sustained in roughly an 8–12% band over decades, while real revenue growth declines toward GDP growth.
5. **Make growth earned, not free.** Set the stable reinvestment rate to `g/ROC` (or the payout to `1 − g/ROE`). Efficiency growth cannot be assumed in stable growth, so reinvestment is the only source of growth left.
6. **Make every other stable-period input mature.** Beta moves toward 1.00. The debt ratio moves toward the industry or mature-company average. Country risk premiums (especially in emerging markets) fade over time. Excess returns approach zero. The cost of capital moves to a mature-firm level.
7. **Run the reverse check.** Back the implied perpetual ROC out of the terminal cash flow and ask whether it is defensible.
8. **Prefer the stable-growth model over the alternatives.** Liquidation value is right when assets are separable and marketable. An exit multiple is easiest but converts your intrinsic valuation into a relative valuation by importing market pricing.

**Reference data:**

Three ways to estimate terminal value:
| Approach | When it is right | Objection |
|---|---|---|
| Liquidation value | Assets separable and marketable | Not a going-concern value |
| Exit multiple | Easiest | Imports market pricing — your DCF becomes a relative valuation |
| Stable growth model | Technically soundest | Requires judgments on when stability arrives and what excess returns persist |

Terminal value sensitivity: EBIT(1−t) in year n+1 = $100m, cost of capital 10%. Each cell = `100 × (1 − g/ROC)/(0.10 − g)`:
| g forever \ ROC | 6% | 8% | 10% | 12% | 14% |
|---|---|---|---|---|---|
| 0.0% | $1,000 | $1,000 | $1,000 | $1,000 | $1,000 |
| 0.5% | $965 | $987 | $1,000 | $1,009 | $1,015 |
| 1.0% | $926 | $972 | $1,000 | $1,019 | $1,032 |
| 1.5% | $882 | $956 | $1,000 | $1,029 | $1,050 |
| 2.0% | $833 | $938 | $1,000 | $1,042 | $1,071 |
| 2.5% | $778 | $917 | $1,000 | $1,056 | $1,095 |
| 3.0% | $714 | $893 | $1,000 | $1,071 | $1,122 |

At ROC = cost of capital the terminal value is $1,000 whatever the growth rate. Below it, growth destroys value.

The riskfree rate tracks nominal GDP growth over long periods (US data):
| Period | 10-yr T.Bond rate | Inflation | Real GDP growth | Nominal GDP growth | Nominal GDP − T.Bond |
|---|---|---|---|---|---|
| 1954–2015 | 5.93% | 3.61% | 3.06% | 6.67% | 0.74% |
| 1954–1980 | 5.83% | 4.49% | 3.50% | 7.98% | 2.15% |
| 1981–2008 | 6.88% | 3.26% | 3.04% | 6.30% | −0.58% |
| 2009–2015 | 2.57% | 1.66% | 1.47% | 3.14% | 0.57% |

Growth-pattern selection (how many stages before stable growth):
| Firm profile | Model |
|---|---|
| Large and growing at or below the economy's rate; or regulated; or average risk and reinvestment | Stable growth (single stage) |
| Large and growing moderately (<= economy growth + 10%); or a single product with a finite-life moat (a patent) | 2-stage |
| Small and growing very fast (> economy growth + 10%); or strong barriers to entry; or characteristics far from the norm | 3-stage / n-stage |

**Worked examples:**

*Disney, stable-period inputs (November 2013).* All four disciplines in one place:
1. Growth cap — perpetual `g` = **2.5%**, deliberately set *below* the 2.75% riskfree rate.
2. Excess returns — ROC drops from 12.61% to **10%**, still above the 7.29% stable cost of capital, on the argument that Disney's brand advantages will not have fully dissipated by year 10.
3. Reinvest to grow — stable reinvestment rate `= g/ROC = 2.5%/10% = 25%`.
4. Mature risk — beta goes to 1.00 (cost of equity `2.75% + 1.00 × 5.76% = 8.51%`), the debt ratio rises to 20%, the cost of debt stays 3.75%, so the stable cost of capital `= 8.51% × 0.80 + 3.75% × (1 − 0.361) × 0.20 = 7.29%`.
Result: terminal-year `EBIT(1−t) = 10,639`, reinvestment `2,660`, `FCFF = 7,980`, `Terminal value = 7,980/(0.0729 − 0.025) = 165,323`.

*Heineken, September 2019 (Euros) — a negative stable growth rate.* With a **−0.5%** Euro riskfree rate, stable `g` is set to **−0.5%**, the stable cost of capital and stable ROC are both 5%, so the stable reinvestment rate is `−0.5%/5% = −10%` (the firm disinvests as it shrinks). Terminal value `= 2,972/(0.05 − (−0.005)) = 54,034`. PV(terminal value) 36,391 out of an operating-asset value of 51,691 — 70% of the value.

*Deutsche Bank (equity version).* At the end of year 5 the bank is in stable growth: cost of equity falls to 8.5% (beta -> 1) and ROE falls to 8.5% (**equal to** the cost of equity, i.e. zero excess returns). Stable payout `= 1 − g/ROE = 1 − 0.03/0.085 = 64.71%`. Year-6 dividend `= 5,143 × 1.03 × 0.6471 = 3,427`; `Terminal value = 3,427/(0.085 − 0.03) = 62,318`; `PV = 62,318/1.0923^5 = 40,079`.

*Baidu.* Stable `g` 3.5%, stable cost of capital 10%, stable ROC 15% -> reinvestment rate `3.5%/15% = 23.33%`; terminal-year `EBIT(1−t) 41,896 − reinvestment 9,776 = FCFF 32,120`; `Terminal value = 32,120/(0.10 − 0.035) = 494,159`.

**Determinism:**
- DETERMINISTIC: the perpetuity formula; the stable reinvestment rate `g/ROC` and payout `1 − g/ROE`; every cell of the sensitivity table; the discounting of the terminal value; the growth-pattern threshold screens (growth vs economy growth + 10%).
- JUDGMENT: `N`, the length of the growth period (needs an assessment of the moat's strength and durability); the stable growth rate within the cap; the perpetual ROC and whether any excess return survives; the stable beta, debt ratio and country risk premium; whether the firm ever reaches stability at all (Vale was valued with **no** high-growth period).

**Pitfalls:**
- **Growth without reinvestment.** The classic sleight of hand is assuming cap ex merely offsets depreciation and there are no working-capital needs in perpetuity, then applying a positive real growth rate. Zero net reinvestment is consistent only with roughly zero real growth. (Even purely inflationary growth generally needs working capital and replacement assets at inflated prices.)
- Letting `g` exceed the riskfree rate / nominal economy growth. In perpetuity the firm would eventually exceed the economy.
- Pairing a high `g` with a low riskfree rate (overvalues) or a low `g` with a high riskfree rate (undervalues).
- Setting `g` in one currency's terms and `r` in another's, or mixing real growth with nominal discount rates.
- Assuming a permanent ROC far above the cost of capital without an explicit moat argument — and never checking the implied perpetual ROC that your terminal FCFF embeds.
- Stretching the high-growth period to 10+ years with substantial excess returns because a spreadsheet template has ten columns.
- Leaving the stable-phase beta at 1.8 and the debt ratio at the current level. A mature firm should look mature on every dimension.
- Using an exit multiple and then describing the result as an intrinsic valuation.
- Forgetting that a negative `g` is legitimate and mechanically produces a negative reinvestment rate.

**Sources:**
- valpacket1spr21 p.197-210
- valpacket1spr20 p.194-206
- valpacket1spr21 p.216 / valpacket1spr20 p.212 (growth-pattern selection thresholds)
- valpacket1spr21 p.203 (Heineken DCF with negative stable growth)
- cfpacket2spr20 p.250-252, p.254 (closure; growth-period patterns; growth-period choice for Disney, Vale, Tata Motors, Baidu; Disney stable-period inputs), p.257, p.260-261, p.263
- spreadsheet:ImpliedROCROE.xls — the reverse consistency check on terminal assumptions
- spreadsheet:cpxest.xls — the three stable-growth cap-ex approaches and why "net cap ex = 0" is the dangerous one
- spreadsheet:fcffsimpleginzu.xlsx — terminal-year construction: terminal ROC defaults to terminal WACC, reinvestment = g/ROC, TV = FCFF/(WACC − g)

**Related:** [[value-of-growth]], [[return-on-invested-capital]], [[fundamental-growth-operating]], [[fundamental-growth-equity]], [[fcff]], [[fcff-forecast-engine]], [[dcf-model-choice-framework]], [[dcf-case-valuations]], [[riskfree-rate]], [[cost-of-capital]], [[competitive-advantage]]
