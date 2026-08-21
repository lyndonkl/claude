# Time Value of Money and the Discount Rate

**Core idea:** A dollar tomorrow is worth less than a dollar today, for exactly three reasons. People prefer current consumption and must be paid to defer it. Monetary inflation erodes what a dollar buys. And uncertainty in a future cash flow makes it less valuable. The discount rate packages all three. It is the rate at which present and future cash flows are traded off, and it is also an opportunity cost — the return available on the next best alternative of equivalent risk. Everything downstream follows. A stronger preference for current consumption, higher expected inflation, or higher risk all raise the discount rate, and a higher discount rate lowers the value of any future cash flow. Discounting converts future cash flows to present ones; compounding does the reverse.

**Formulas:**
- Discount rate decomposition (conceptual): `r = (compensation for deferring consumption) + (expected inflation) + (risk premium)`. Operationally the first two together are the riskfree rate, so `r = riskfree rate + risk premium`.
- Present value of a cash flow at time t: `PV = CF_t / (1 + r)^t` where `CF_t` = cash flow at time t, `r` = discount rate per period, `t` = number of periods.
- Future value: `FV = CF_0 × (1 + r)^t` where `CF_0` = cash flow today.
- Principle 1 (aggregation): cash flows at different points in time may not be compared or added until they are all moved to a common date, either today (present value) or a chosen future date (future value).
- Principle 2 (decision rules): any investment rule must weigh both *how much* cash arrives and *when* it arrives.

**Procedure:**
1. Draw the time line. Mark today as time 0 and place every cash flow at the period it occurs. Adopt the end-of-period convention unless told otherwise: a cash flow "in year 1" arrives at the end of year 1.
2. Fix the currency and the nominal/real basis of the cash flows, because the discount rate must match on both dimensions (nominal cash flows → nominal rate; euro cash flows → euro rate).
3. Build the discount rate from its three drivers. Start with the riskfree rate in that currency (which already carries consumption preference and expected inflation), then add a risk premium sized to the uncertainty in the cash flows.
4. Cross-check the rate as an opportunity cost. Ask: what return could this investor earn on an alternative of *equivalent risk*? If the discount rate is materially below that, it is too low.
5. Move every cash flow to the common date using `CF_t/(1+r)^t` (or `× (1+r)^t` to go forward), then sum. Only now may you add them.
6. Sanity-check the compounding. If the analysis extrapolates a high growth rate for 5, 8 or 10 years, compute the implied out-year revenue or market share and ask whether it is plausible. If a large fraction of the total value sits in a heavily discounted terminal value, note that the discounting has already shrunk it substantially and check the terminal assumptions rather than the near-term ones.

**Reference data:** No lookup table is required for the concept itself. The one directional table that matters:

| Driver rises | Effect on discount rate | Effect on value of future cash flows |
|---|---|---|
| Preference for current consumption | Higher | Lower |
| Expected inflation | Higher | Lower |
| Uncertainty (risk) in cash flows | Higher | Lower |

**Worked example:** A time line showing $100 received at the end of each of the next four years (points 0, 1, 2, 3, 4 with $100 at years 1 through 4). At a 10% discount rate the four cash flows are worth 100/1.10 = $90.91, 100/1.10² = $82.64, 100/1.10³ = $75.13 and 100/1.10⁴ = $68.30, summing to $316.99 today. Note that the fourth-year dollar is worth only 68% of the first-day dollar — that gap *is* the time value of money, and at a 20% rate the same year-4 cash flow would be worth only $48.23. (Source: Damodaran, Foundations of Finance Session 6, Figure 3.1.)

**Determinism:**
- DETERMINISTIC: given `{CF_t}`, `r` and `t`, all discounting and compounding is pure arithmetic. A script takes cash flows, dates, and a rate and returns PV or FV exactly.
- JUDGMENT: choosing `r`. That requires an estimate of the riskfree rate in the right currency, a view on the risk of the cash flows, and knowledge of returns available on equivalent-risk alternatives. Also judgment: how long a high growth rate can be extrapolated before the compounded values become implausible.

**Pitfalls:**
- Adding or comparing cash flows from different periods without discounting them first — the single most common error.
- Using a decision rule based only on total cash received, ignoring timing (this is what makes payback and undiscounted accounting measures unreliable).
- Underestimating compounding: extrapolating a small company's recent growth rate for 8-10 years produces out-year revenues that are often absurd once you compute them.
- Underestimating discounting in the other direction and then being surprised at how little a 10-year-out terminal value contributes.
- Mismatching the discount rate to the cash flows on currency, on nominal-vs-real, or on risk.

**Sources:**
- `foundations_of_finance--introduction p.7`
- `foundations_of_finance--time_value_of_money p.2-5, p.8`

**Related:** [[present-value-of-the-five-cash-flow-types]], [[compounding-frequency-and-effective-rates]], [[real-vs-nominal-conversion]], [[fisher-equation-and-intrinsic-riskfree-rate]], [[currency-consistent-valuation]], [[marginal-investor-and-beta]], [[finance-first-principles]]
