# Forecasting future FCFE, dividends and buyback capacity

**Core idea:** Assessing the past payout is only half the job. The forward-looking half projects FCFE for the next five years, projects the dividend the firm is likely to keep paying given its stickiness, and takes the difference as the cash available for buybacks. That difference is the practical output of a payout analysis: it tells you how much repurchase capacity the firm has, or how large the funding gap will be if it keeps its dividend. The projection is deliberately simple — constant growth rates applied to the current year's net income, cap ex, depreciation and revenues, with working capital tied to revenues — because the point is to bound the payout capacity, not to build a full valuation.

**Formulas:**

For forecast years t = 1 to 5, with base-year (year 0) values from the most recent financial statements:
- Revenues_t = Revenues_0 × (1 + g_rev)^t
- Net Income_t = Net Income_0 × (1 + g_NI)^t
- Cap Ex_t = Cap Ex_0 × (1 + g_capex)^t
- Depreciation_t = Depreciation_0 × (1 + g_depr)^t
- ΔWorking Capital_t = WC% × (Revenues_t − Revenues_(t−1))  ← note this is the **change**, driven by the revenue increment, not the level
- Net cap ex funded by equity_t = (Cap Ex_t − Depreciation_t) × (1 − DR)
- Working capital funded by equity_t = ΔWorking Capital_t × (1 − DR)
- **FCFE_t = Net Income_t − (Cap Ex_t − Depreciation_t)(1 − DR) − ΔWorking Capital_t × (1 − DR)**
- Expected Dividends_t = Dividends_0 × (1 + g_div)^t
- **Cash available for buybacks_t = FCFE_t − Expected Dividends_t**

Symbols:
- g_rev, g_NI, g_capex, g_depr, g_div = expected annual growth rates in revenues, net income, capital expenditures, depreciation and dividends
- WC% = non-cash working capital as a percentage of revenues
- DR = debt ratio; use the target ratio if the firm is moving to one, otherwise the current debt-to-capital ratio

**Procedure:**
1. Set the base year. Use the most recent year's revenues, net income, cap ex, depreciation and dividends, or normalized values if the most recent year was unusual.
2. Choose growth rates. In the simplest version all of revenues, net income, cap ex and depreciation grow at the same rate — a firm in steady state. Depart from that only with a reason, and note that letting cap ex grow faster than depreciation permanently is an implicit claim about the reinvestment rate.
3. Set the working capital percentage from history: non-cash working capital divided by revenues, averaged over recent years.
4. Set the debt ratio. This is the same choice as in the historical analysis: current ratio, or target if you are moving the firm.
5. Project revenues first, take the year-over-year increments, and multiply by WC% to get the change in working capital. Do not multiply the revenue *level* by WC% — that is the working capital balance, not the change.
6. Compute FCFE each year.
7. Project dividends at the expected dividend growth rate. Be realistic: stickiness means the dividend will keep growing at roughly its historical rate unless management commits otherwise.
8. Subtract to get annual buyback capacity. Interpret:
   - Positive and growing → the firm can sustain a buyback programme of that size without leverage or asset sales.
   - Negative → the firm cannot fund its own dividend from FCFE, and the shortfall must come from cash reserves, new debt or new equity.
9. Feed the result into the recommendation. A firm with large projected buyback capacity and good projects can be left alone; a firm with negative capacity is heading for the cash-deficit quadrant of [[dividend-matrix]].

**Reference data — the model's default assumption set (dividends.xls, `Forecasted Dividends & FCFE`, Disney case):**

| Input | Value |
|---|---|
| Expected growth in revenues (next 5 years) | 5% |
| Expected growth in net income | 5% |
| Expected growth in capital expenditures | 5% |
| Expected growth in depreciation | 5% |
| Non-cash working capital as % of revenues | 6% |
| Expected growth in dividends | 5% |
| Revenues, most recent year | $42,278M |
| Net income, most recent year | $6,136M |
| Capital expenditures, most recent year | $2,796M |
| Depreciation, most recent year | $2,192M |
| Dividends paid, most recent year | $1,324M |
| Debt ratio (current) | 11.579% |

**Worked example — Disney, forecast year 1 ($ millions):**
- Revenues_1 = 42,278 × 1.05 = **44,391.9**
- Net Income_1 = 6,136 × 1.05 = **6,442.8**
- Cap Ex_1 = 2,796 × 1.05 = 2,935.8; Depreciation_1 = 2,192 × 1.05 = 2,301.6; so Cap Ex − Depreciation = 634.2
- ΔWorking Capital_1 = 0.06 × (44,391.9 − 42,278) = 0.06 × 2,113.9 = **126.83**
- Net cap ex funded by equity = 634.2 × (1 − 0.115793) = **560.76**
- Working capital funded by equity = 126.83 × (1 − 0.115793) = **112.15**
- **FCFE_1 = 6,442.8 − 560.76 − 112.15 = 5,769.89**
- Expected Dividends_1 = 1,324 × 1.05 = **1,390.2**
- **Cash available for buybacks_1 = 5,769.89 − 1,390.2 = 4,379.69**

Repeating through year 5, buyback capacity grows to about **5,323.54**. The reading: on these assumptions Disney can sustain a buyback programme of roughly $4.4–5.3 billion a year on top of a dividend growing at 5%, without borrowing beyond its current debt ratio. Compare that with the $4,087M it actually repurchased in the base year, and the current payout looks sustainable.

**Determinism:**
- DETERMINISTIC: the entire forecast table. Given the base-year values, the five growth rates, the working capital percentage and the debt ratio, a script produces revenues, net income, FCFE, expected dividends and buyback capacity for all five years.
- JUDGMENT: every input. The growth rates, whether cap ex and depreciation should grow at the same rate, the working capital intensity, whether the base year is representative, and which debt ratio applies. The forecast is only as good as these assumptions, and none of them is observable.

**Pitfalls:**
- Multiplying the revenue level by WC% and calling it the change in working capital. The formula uses the revenue *increment*; using the level overstates reinvestment by an order of magnitude.
- Forgetting that year 0 revenues are the base for the first year's increment.
- Growing cap ex faster than depreciation indefinitely without checking the implied reinvestment rate and return on capital.
- Using the historical dividend growth rate mechanically for a firm whose FCFE cannot support it. The output then shows negative buyback capacity, which is the finding — do not "fix" it by lowering the dividend growth assumption without saying so.
- Applying a target debt ratio in the forecast that differs from the one used in the historical analysis without flagging the change.
- Treating the five-year buyback capacity as a valuation. It is a capacity bound under simple growth assumptions, not a discounted cash flow.
- Ignoring that a base year with unusual cap ex or working capital propagates through all five forecast years.

**Sources:**
- corpfin-payout-projects — dividends.xls, sheets `Inputs` (section 3, cells E55–E64, D66) and `Forecasted Dividends & FCFE` (rows 6–14)
- corporate_finance--lecture_slides--cfpacket2spr20 p.193-194
- corporate_finance--lecture_slides--cfpacket2spr20 p.200

**Related:** [[fcfe-potential-dividends]], [[cash-trust-assessment]], [[cash-returned-dividends-and-buybacks]], [[buyback-value-and-eps-effect]], [[dividend-matrix]], [[dividend-life-cycle]]
