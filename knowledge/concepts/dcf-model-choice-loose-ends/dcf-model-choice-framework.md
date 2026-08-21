# DCF model choice framework (the three building blocks)

**Core idea:** Every DCF model is one combination of three choices. First, *which cash flow* you discount: dividends, free cash flow to equity (FCFE), or free cash flow to the firm (FCFF). Second, *which discount rate* matches it: cost of equity for equity flows, cost of capital (WACC) for firm flows. Third, *which growth pattern* you assume: one stage (stable growth forever), two stages (high growth then stable), or three stages (high growth, transition, stable). The choices are not free-floating. Cash flow fixes the discount rate, and firm characteristics fix the growth pattern. A wrong combination makes numerator and denominator inconsistent, and no amount of input precision repairs that.

**Formulas:**
- Dividends: cash flow = expected dividends per share (DPS). Buybacks should be added to dividends when treating them as cash returned.
- `FCFE = Net Income − (1 − δ)(Capital Expenditures − Depreciation) − (1 − δ)(Change in Non-cash Working Capital)`
  where δ = debt ratio (the fraction of reinvestment financed with debt), Net Income = after-tax income to equity holders.
  Equivalent long form: `FCFE = Net Income − (CapEx − Depreciation) − ΔWorking Capital + (New Debt Issued − Debt Repaid)`.
- `FCFF = EBIT(1 − t) − (Capital Expenditures − Depreciation) − Change in Non-cash Working Capital`
  where EBIT = earnings before interest and taxes, t = tax rate. Equivalently `FCFF = EBIT(1−t) + Depreciation − CapEx − ΔWC`.
- Cost of equity, CAPM: `k_e = Riskfree Rate + Beta × Equity Risk Premium`.
- Cost of equity, arbitrage pricing (APM): `k_e = Riskfree Rate + Σ_{j=1..n} Beta_j × Risk Premium_j` over n factors.
- Cost of capital: `WACC = k_e × E/(D+E) + k_d × D/(D+E)`, with `k_d = current pre-tax borrowing rate × (1 − t)` and E, D at **market** values.
- Value (generic): `Value = Σ_t CF_t / (1 + r)^t + Terminal Value_n / (1 + r)^n`, with CF and r drawn from the same column of the table below.

**Reference data — the building-block matrix:**

| Choice | Options | Consequence |
|---|---|---|
| Cash flow | Dividends → equity value per share; FCFE → equity value; FCFF → firm (enterprise) value | Fixes what the output *is* |
| Discount rate | Cost of equity (dividends, FCFE); cost of capital (FCFF) | Must match the cash flow's claimholder |
| Growth pattern | Stable (1-stage); two-stage (high then stable); three-stage (high, transition, stable) | Fixes model complexity and terminal-value timing |

Canonical spreadsheet implementations of every cell of that matrix (Damodaran's "focussed" model set): `ddmst`, `ddm2st`, `ddm3st`; `fcfest`, `fcfe2st`, `fcfe3st`; `fcffst`, `fcff2st`, `fcff3st`, `fcffgen` (n-stage, year-specific inputs, with net-operating-loss tax logic).

**Procedure:**
1. Inventory what you have: current dividends and buybacks, current FCFE, current FCFF; cost of equity and cost of capital; growth estimates from history, analysts and fundamentals.
2. Decide equity vs. firm valuation (see [[equity-versus-firm-valuation]]). Stable leverage or you are explicitly valuing the stock → equity; leverage changing, or leverage data incomplete, or you want firm value → firm.
3. If equity: choose dividends vs. FCFE with the 80%/110% screen (see [[dividends-versus-fcfe]]).
4. Attach the matching discount rate and currency (see [[discount-rate-cash-flow-matching]]).
5. Choose the number of stages from firm size, growth relative to the economy, and barriers to entry (see [[growth-pattern-and-stage-count]]).
6. Build the model with the stage mechanics in [[multistage-model-mechanics]], then bridge from the model output to value per share with [[equity-value-bridge]].
7. Sanity-check by reconciling variants: an FCFF and an FCFE valuation of the same firm should agree under constant market-value leverage ([[fcff-fcfe-reconciliation]]); a DDM and an FCFE valuation agree only if the retained cash earns the cost of equity ([[ddm-fcfe-reconciliation]]).

**Worked example (Con Ed, August 2008 — a fully justified model choice):** Con Ed is valued with a *stable-growth dividend discount model*. Each block is justified. Growth pattern: stable. Con Ed is a regulated utility barred from new growth markets, and its New York service area grows about 2% a year. Cash flow: equity, not firm. The capital structure has sat near 70% equity / 30% debt for decades. Measure: dividends, not FCFE. Con Ed paid out about 97% of FCFE as dividends over the prior five years. Inputs: trailing-12-month EPS $3.17, DPS $2.32 (payout 73%), beta 0.80, riskfree 4.10%, ERP 4.5%. Then `k_e = 4.1% + 0.8 × 4.5% = 7.70%` and `g = retention 27% × ROE 7.7% = 2.1%`. Value = 2.32 × 1.021 / (0.077 − 0.021) = **$42.30**, versus a market price of $40.76 on 12 August 2008.

**Determinism:**
- DETERMINISTIC: given the accounting inputs, each cash-flow definition (FCFE, FCFF), each discount-rate formula (CAPM, APM, WACC) and the discounting arithmetic compute exactly. Also deterministic: the 80%/110% dividend screen, the inflation ≥/<10% real-vs-nominal switch, and the "firm growth vs. economy growth + 10%" stage screen.
- JUDGMENT: whether leverage is "stable", whether FCFE is estimable (banks), whether barriers to entry justify a longer high-growth phase, and every forecast input (growth, margin, stable ROC/ROE, beta path). These need industry structure, regulatory context, and management/ownership information.

**Pitfalls:**
- Mixing blocks: discounting FCFF at the cost of equity, or discounting dividends at the cost of capital, produces a number that means nothing.
- Treating model complexity as rigor: adding a third stage to a mature regulated utility adds parameters, not accuracy.
- Estimating inputs first and choosing the model afterwards to fit the answer you want.
- Forgetting that the FCFE formula's δ (debt ratio) is the *financing* mix for reinvestment, not the firm's total debt ratio if those differ.

**Sources:**
- valpacket1spr21 p.212, p.217
- valpacket1spr20 p.208, p.213
- valpacket1spr21 p.279 (Con Ed model-choice tests)
- valpacket1spr20 p.275 (Con Ed model-choice tests)
- focussed-ddm (ddmst, ddm2st, ddm3st)
- focussed-fcfe (fcfest, fcfe2st, fcfe3st)
- focussed-fcff (fcffst, fcff2st, fcff3st, fcffgen)

**Related:** [[equity-versus-firm-valuation]], [[dividends-versus-fcfe]], [[discount-rate-cash-flow-matching]], [[growth-pattern-and-stage-count]], [[multistage-model-mechanics]], [[equity-value-bridge]], [[terminal-value]], [[cost-of-equity-capm]], [[bottom-up-beta]], [[fundamental-growth-rate]]
