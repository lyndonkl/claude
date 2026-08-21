# Reconciling the dividend discount model with FCFE

**Core idea:** A dividend discount model and an FCFE model applied to the same firm give different values whenever dividends differ from FCFE. The gap is not a mystery; it is exactly the value of the cash that piles up inside the firm, plus or minus what that cash earns relative to the cost of equity. If the retained cash is reinvested at the cost of equity, the two models agree to the penny. If it earns less — the usual case for cash sitting in low-yield securities under weak governance — the DDM value falls short of the FCFE value by the present value of that shortfall. This reconciliation turns "which model is right?" into a measurable question about the quality of retention.

**Formulas:**
- `Cash buildup: CB₁ = FCFE₁ − Div₁`; `CB_t = CB_{t−1}(1 + r_cash) + (FCFE_t − Div_t)`, where r_cash = the return earned on accumulated cash.
- FCFE value: `V_FCFE = Σ_{t=1..n} FCFE_t/(1+k_e)^t + P_n/(1+k_e)^n`.
- DDM value including the accumulated cash asset: `V_DDM = Σ_{t=1..n} Div_t/(1+k_e)^t + P_n/(1+k_e)^n + CB_n/(1+k_e)^n`.
- Terminal price (shared by both models): `P_n = FCFE_T/(k_e,stable − g_stable)`, with `FCFE_T = Net Income_T × (1 − g_stable/ROE_stable)`. In steady state dividends are assumed to equal FCFE, so the payout adjusts and both models use the same terminal price.
- Difference: `V_FCFE − V_DDM = 0` when `r_cash = k_e`; the difference grows as `r_cash` falls below `k_e`.

**Reference data — reconciliation model conventions (`fcfevsddm.xls`):**

| Element | Rule |
|---|---|
| Cash-buildup return | User choice: cost of equity (models reconcile) or a stated rate such as 7% |
| Terminal FCFE | `Net Income_T × (1 − g/ROE_stable)` — forced consistent with stable ROE |
| Terminal net cap ex | A **plug**: `NI_T − FCFE_T − ΔWC_T + Net Debt CF_T`. Not grown from year n |
| Terminal price | Identical in both models; the DDM assumes dividends equal FCFE in steady state |
| Working capital % | Derived as current WC / current revenues, not entered separately |

**Procedure:**
1. Build the FCFE stream for the high-growth years: `FCFE_t = Net Income_t − (CapEx − Depreciation)_t − ΔWC_t + Net Debt Cash Flow_t`.
2. Build the dividend stream over the same years by growing current dividends.
3. Compute the year-by-year cash buildup with the recursion above, using your assumed reinvestment rate on accumulated cash.
4. Set the terminal year: grow net income at `g_stable`, then set `FCFE_T = NI_T(1 − g/ROE_stable)`. Compute the terminal price once and use it in both models.
5. Value the FCFE stream at the cost of equity. Value the dividend stream at the cost of equity, then add the present value of the terminal cash balance.
6. Compare. If you want a pure test of dividend policy, rerun with `r_cash = k_e`; the two values should now be identical, confirming your arithmetic.
7. Interpret the residual difference as the value cost of the retention policy, and decide whether it should be a discount (see [[marginal-value-of-cash]]).

**Worked example (`fcfevsddm.xls`):** Net income 100, dividends 30, cap ex 75, depreciation 50, revenues 1,000, working capital 50, net debt cash flow 10. High growth is 10% for 5 years, then 4% forever with a stable ROE of 12%. Beta 1.0, riskfree 5%, ERP 4%, so `k_e = 9%`. Accumulated cash earns 7%.
- Year 1: net income 110; net cap ex 27.5; ΔWC = 0.05 × 100 = 5; net debt 11 → FCFE = 88.5. Dividend = 33. Cash buildup = 55.5.
- By year 5 the cash balance is 384.723.
- Terminal: `NI_T = 167.493`; `FCFE_T = 167.493 × (1 − 0.04/0.12) = 111.662`; `P₅ = 111.662/0.05 = 2,233.24`.
- FCFE value = 413.481 + 1,451.453 = **1,864.934**.
- DDM value = 154.179 + 1,451.453 + 250.043 = **1,855.676**.
- Difference = **9.258**, purely the cost of earning 7% instead of 9% on the retained cash. Set the cash return to 9% and the difference goes to zero.

**Determinism:**
- DETERMINISTIC: both valuations, the cash-buildup recursion, and the difference, given the inputs. A script computes all of it.
- JUDGMENT: the return the firm will actually earn on retained cash. That is a governance and capital-allocation question — look at the firm's acquisition history, its return on incremental capital, and its cash-holding policy. The stable ROE that sets terminal payout is also a judgment call.

**Pitfalls:**
- Concluding a cash-rich firm is overvalued because a naive DDM (with no cash-buildup term) gives a low value.
- Growing terminal net cap ex from the prior year instead of treating it as the plug that makes terminal reinvestment consistent with `g/ROE`.
- Letting dividends exceed FCFE without noticing that the "cash buildup" has gone negative — that is a drawdown, funded by debt or reserves, and it is not sustainable.
- Setting `ROE_stable < g_stable`, which makes terminal retention exceed 1 and terminal FCFE negative.

**Sources:**
- reconciliation (fcfevsddm.xls)
- valpacket1spr21 p.214
- valpacket1spr20 p.210

**Related:** [[dividends-versus-fcfe]], [[fcff-fcfe-reconciliation]], [[marginal-value-of-cash]], [[cash-in-valuation]], [[dcf-model-choice-framework]], [[stable-growth-inputs]]
