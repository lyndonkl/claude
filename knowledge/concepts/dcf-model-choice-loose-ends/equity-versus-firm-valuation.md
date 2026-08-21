# Equity valuation versus firm valuation

**Core idea:** The first fork in any DCF is whether to value the equity directly (discount dividends or FCFE at the cost of equity) or to value the whole firm (discount FCFF at the cost of capital, then subtract debt). Both routes are correct and, under constant market-value leverage, give identical equity values; they differ in how much they force you to forecast. Equity valuation requires you to project debt issues and repayments explicitly inside the cash flows, which is easy when leverage is stable and treacherous when it is not. Firm valuation buries leverage in the cost of capital, where a changing debt ratio moves WACC only gradually, so it is the robust choice for firms whose capital structure is in transit or whose debt data are incomplete.

**Formulas:**
- Equity route: `Value of Equity = Σ_t FCFE_t/(1+k_e)^t + TV_n^equity/(1+k_e)^n`, where `FCFE = Net Income − (CapEx − Depreciation) − ΔWorking Capital + Net Debt Issued`, k_e = cost of equity.
- Firm route: `Value of Firm = Σ_t FCFF_t/(1+WACC)^t + TV_n^firm/(1+WACC)^n`, where `FCFF = EBIT(1−t) − (CapEx − Depreciation) − ΔWorking Capital`.
- Bridge: `Value of Equity = Value of Firm + Cash and marketable securities + Cross holdings + Other non-operating assets − Debt − Other claims` (see [[equity-value-bridge]]).
- Consistency identity (holds exactly when debt each year = debt ratio × that year's firm value): the two routes give the same equity value; see [[fcff-fcfe-reconciliation]].

**Reference data — decision rules:**

| Use EQUITY valuation when | Use FIRM valuation when |
|---|---|
| Leverage is stable (whether high or low) | Leverage is too high or too low and is expected to change over time |
| Equity (the stock) is what you are valuing | You have only partial information on leverage (e.g. interest expenses not broken out) |
| | You care about firm value rather than equity value (value consulting, whole-business transactions) |

**Procedure:**
1. Compute the firm's current market-value debt ratio, `D/(D+E)`, and compare it with the industry/sector average and with management's stated target.
2. If the current ratio is close to the target and has been stable historically → equity valuation is safe. Con Ed's roughly 70/30 equity/debt split, unchanged for decades, is the archetype.
3. If the ratio is far from the target → use firm valuation. The same applies to a firm that is recapitalizing, levering up for an acquisition, or deleveraging out of distress. Let the cost of capital drift toward the target-leverage WACC over the forecast horizon.
4. If interest expense, debt maturity or lease data are missing or unreliable, so you cannot build a credible net-debt-issuance line → use firm valuation.
5. If you use firm valuation, complete the bridge to equity: add cash and non-operating assets, subtract the market value of debt and other claims, subtract the value of employee options, divide by actual shares.
6. Cross-check: if leverage really is constant at market value, rebuild the model the other way; the equity values must match to the penny. A mismatch means your debt schedule and your WACC disagree.

**Worked example (from the FCFF-vs-FCFE reconciliation model):** Inputs: EBIT₀ = 100; growth 10% for 5 years, then 5% forever; tax rate 40%; market-value debt ratio 20%. Rates: cost of equity 12%, pre-tax cost of debt 7%. Returns: ROC 12% in high growth, 10% in stable growth.
- Firm route: reinvestment rate = g/ROC = 10%/12% = 83.33% in high growth, 5%/10% = 50% stable. After-tax k_d = 7%(1−0.4) = 4.2%; `WACC = 0.8(12%) + 0.2(4.2%) = 10.44%`. Terminal FCFF = 50.731; `TV₅ = 50.731/(0.1044 − 0.05) = 932.556`; Value of firm = **617.006**; equity = 617.006 × (1 − 0.20) = **493.605**; debt = 123.401.
- Equity route: each year's debt = 20% × that year's firm value; interest = 7% × beginning debt; new debt issued = change in debt. Year 1: net income = (110 − 8.638)(1 − 0.4) = 60.817; FCFE = 60.817 − 55 + 10.683 = 16.500. Discounting the FCFE stream plus a terminal equity value of 746.045 at 12% gives **493.605** — identical.

**Determinism:**
- DETERMINISTIC: both valuation routes given the inputs; the debt schedule when the rule "debt = debt ratio × firm value" is imposed; the equality check between the two routes.
- JUDGMENT: classifying leverage as "stable" or "changing" and choosing the target debt ratio and the speed of convergence to it. That needs the firm's stated financing policy, sector norms, credit-rating constraints and any covenant or regulatory limits.

**Pitfalls:**
- Using equity valuation on a firm whose debt ratio is drifting, and then holding the cost of equity constant — the changing leverage should have raised or lowered beta.
- Subtracting *book* debt from a DCF firm value (see [[debt-and-other-claims-in-the-bridge]]).
- Forgetting that firm valuation's FCFF is before debt cash flows: adding an interest expense line to FCFF double-counts the cost of debt already in the WACC.
- Assuming the two routes must agree even when leverage changes over time — they agree only under the constant-market-value-debt-ratio construction.

**Sources:**
- valpacket1spr21 p.213
- valpacket1spr20 p.209
- valpacket1spr21 p.279 (Con Ed: "why equity" test — stable 70/30 capital structure)
- reconciliation (fcffvsfcfe.xls)

**Related:** [[dcf-model-choice-framework]], [[dividends-versus-fcfe]], [[fcff-fcfe-reconciliation]], [[equity-value-bridge]], [[defining-debt-for-cost-of-capital]], [[cost-of-capital]], [[levered-beta]]
