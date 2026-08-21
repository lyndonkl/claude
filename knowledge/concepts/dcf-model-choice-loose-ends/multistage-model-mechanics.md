# Multi-stage model mechanics (how 1-, 2- and 3-stage models are actually built)

**Core idea:** Once you have chosen a stage count, the model's wiring is largely fixed. A one-stage model is a growing perpetuity. A two-stage model projects a constant-parameter high-growth phase, then jumps to a terminal value. A three-stage model interpolates linearly between the two ends: growth, payout, beta, debt ratio and cost of debt each step from their high-growth value to their stable value over the transition years. Two mechanical details separate a correct implementation from a wrong one. When the discount rate varies by year, discount with the cumulative product of `(1 + r_t)`, never with a single rate raised to a power. And the terminal cash flow must be forced consistent with the stable growth rate through `Reinvestment Rate = g/ROC` (or `payout = 1 − g/ROE`).

**Formulas:**
- One stage: `Value = CF₀(1+g)/(r − g)`. Requires `g < r`.
- Two stages: `Value = Σ_{t=1..n} CF_t/(1+r_hg)^t + TV_n/(1+r_hg)^n`, `TV_n = CF_{n+1}/(r_stable − g_stable)`.
- Three stages: high-growth years 1..n₁ at constant `g_hg`; transition years j = 1..n₂ with
  `g_j = g_hg − (g_hg − g_stable) × j/n₂`,
  `payout_j = payout_hg + (payout_stable − payout_hg) × j/n₂`,
  `beta_j = beta_hg − (beta_hg − beta_stable) × j/n₂`, and `r_j = riskfree + beta_j × ERP`.
- Cumulative discounting: `PV of a transition-year flow = CF_j / [ (1+r_hg)^{n₁} × Π_{k≤j}(1+r_k) ]`.
- Terminal consistency: `FCFF_T = EBIT(1−t)_T × (1 − g/ROC)`; `FCFE_T = Net Income_T × (1 − g/ROE)`; `DPS_T = EPS_T × (1 − g/ROE)`.
- Blended high-growth rate (used in the focussed spreadsheets): `g_hg = w_hist × g_hist + w_outside × g_outside + w_fund × g_fund`, with `g_hist = (EPS₀/EPS_{−5})^{1/5} − 1`.
- Fundamental growth, equity version: `g_fund = b × [ ROC + (D/E)(ROC − i(1−t)) ]`, b = retention ratio, i = interest rate on debt.
- Working-capital drag: `ΔWC_t = WC% of revenues × (Revenue_t − Revenue_{t−1}) × (1 − debt financing ratio)`.

**Reference data — canonical model variants (Damodaran's focussed spreadsheets, 2020 archive):**

| Model | Stages | Structure |
|---|---|---|
| `ddmst`, `fcfest`, `fcffst` | 1 | Gordon growth on DPS, FCFE or FCFF |
| `ddm2st`, `fcfe2st`, `fcff2st` | 2 | Constant high growth (≤10 yrs), abrupt drop to stable |
| `ddm3st`, `fcfe3st`, `fcff3st` | 3 | High growth, linear transition, stable; year-specific betas/WACC |
| `fcffgen` | n (≤10) | Fully year-specific growth, margin, cap-ex, depreciation and WC%; NOL carryforward tax logic |

Structural conventions worth reproducing:
- Historical growth is a 5-year CAGR from earnings five years ago.
- If a growth-source toggle is switched off, that estimate is treated as **0** while its weight is still applied. This silently lowers the blended growth rate.
- ROC/ROE for fundamental growth uses **prior-year** book values of debt and equity; the D/E ratio and interest rate use current-year values.
- In `fcff3st` and `fcffeva`, cap ex in the transition glides in **dollars** (linear interpolation to the year-10 target), not at a growth rate; the year-10 cap ex is back-solved from the stable reinvestment rule.
- The stable-phase reinvestment branch is three-way: from fundamentals (`g/ROC`), or cap ex offset by depreciation (net cap ex = 0), or cap ex = a stated multiple of depreciation.

**Procedure:**
1. Set the phase lengths: n₁ high-growth years and, for three stages, n₂ transition years.
2. Estimate the high-growth rate. Blend historical, analyst and fundamental estimates with explicit weights, or set it directly from a narrative.
3. Project the cash flow year by year through the high-growth phase, keeping cap ex, depreciation, revenues and working capital consistent with earnings growth (or on their own stated paths).
4. For a three-stage model, step every changing parameter linearly across the transition, ending exactly at the stable value in the final transition year.
5. Recompute the discount rate each year that beta, debt ratio or cost of debt changes, and accumulate discount factors as a running product.
6. Build the terminal year: grow the last projected flow at `g_stable`, then override reinvestment with `g/ROC` (or payout with `1 − g/ROE`).
7. Compute `TV = CF_T/(r_stable − g_stable)` and discount it through the **end of the transition**, using the same cumulative factor.
8. Sum the phase present values, then run the equity bridge ([[equity-value-bridge]]).

**Worked example (`fcff3st`, a 5 + 5 model):** Revenues start at 12,406 and grow 30% for five years; growth then declines linearly to the 6% stable rate (25.2%, 20.4%, 15.6%, 10.8%, 6.0%). The pre-tax operating margin climbs from 6.89% to a 30% target in year 5, then eases to the 25% perpetual margin (operating expense ratio steps 0.71, 0.72, 0.73, 0.74, 0.75). Beta glides 1.25 → 1.10 and the debt ratio 0% → 5%, so WACC falls from 13.375% to 12.1625%. Stable reinvestment is set from fundamentals: `RR = 6%/12% = 0.5`, giving `FCFF₁₀ = 15,083.52 × 0.5 = 7,541.76`, and year-10 cap ex is back-solved at 9,406.02. `TV = 7,541.76 × 1.06/(0.121625 − 0.06) = 129,724`. Discounting with the cumulative WACC product (3.3975 by year 10) gives a firm value of **66,667**; plus cash 850, minus debt 0, minus options 1,500, over 1,500 shares = **$44.01 per share**.

**Determinism:**
- DETERMINISTIC: the entire projection given the input set — linear ramps, cumulative discount factors, terminal cash flow from `g/ROC`, terminal value, present values, and the per-share bridge. A script can reproduce every number.
- JUDGMENT: phase lengths, the high-growth rate and its weights, target margins, the stable ROC/ROE, and the beta and leverage endpoints. These need the competitive analysis behind [[growth-pattern-and-stage-count]].

**Pitfalls:**
- Discounting transition-year flows at a single average rate when the cost of capital changes each year.
- Discounting the terminal value at the high-growth discount rate instead of through the whole transition.
- Growing terminal cap ex from the prior year rather than back-solving it from the stable reinvestment rate. The two disagree, and only the second is internally consistent.
- Leaving a growth-source toggle off while keeping its weight, which quietly drags the blended growth rate down.
- Requiring `g_stable < r_stable`; the sheets have no guard, and a violation returns a nonsense value.
- Using current-year book capital for the fundamental ROC when the convention is prior-year.

**Sources:**
- valpacket1spr21 p.216-217
- valpacket1spr20 p.212-213
- focussed-ddm (ddmst, ddm2st, ddm3st: transition ramps for growth, payout and beta)
- focussed-fcfe (fcfest, fcfe2st, fcfe3st: cumulative discounting, negative early FCFE)
- focussed-fcff (fcffst, fcff2st, fcff3st, fcffgen: margin paths, WACC glide, NOL logic, back-solved cap ex)
- reconciliation (fcffeva.xls: linear dollar interpolation of cap ex in transition)

**Related:** [[growth-pattern-and-stage-count]], [[dcf-model-choice-framework]], [[equity-value-bridge]], [[terminal-value]], [[fundamental-growth-rate]], [[net-operating-loss-carryforward]], [[valuing-employee-options]]
