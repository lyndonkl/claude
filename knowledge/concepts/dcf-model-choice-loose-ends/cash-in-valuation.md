# Treating cash in a DCF (keep it out, then add it back)

**Core idea:** The cleanest way to handle cash and marketable securities is to keep them out of the operating valuation entirely, then add the balance back at the end. That means two disciplines. Cash flows must be measured *before* interest income from cash. The discount rate must use the beta of the operating assets alone, uncontaminated by the near-zero risk of the cash pile. The alternative — folding interest income into the cash flows and weighting the beta down for cash — only works if cash stays a fixed percentage of value forever. It rarely does, so those valuations break down over time. A related choice, gross debt versus net debt, is not cosmetic: it changes the assumed funding of cash and therefore the equity value.

**Formulas:**
- Preferred structure: `Value of Firm = PV(FCFF excluding interest income, discounted at operating-asset WACC) + Cash`.
- Operating-asset beta: unlever and relever using the operating business only. If a reported beta is cash-contaminated: `Beta_operating = (Beta_reported − Beta_cash × cash weight) / (1 − cash weight)`, with `Beta_cash ≈ 0`.
- Cash as a stand-alone asset: `Value of cash = Cash Earnings / Riskfree Rate` (a riskless perpetuity). Equivalently, cash trades at `PE = 1/riskfree rate` and `P/BV = 1`.
- Gross debt approach: cash is assumed funded with the firm's overall debt/equity mix.
  `k_d,gross = (Interest Expense − rf × Cash × D/V) / (Debt − Cash × D/V)`;
  `Levered Beta = Unlevered Beta × (1 + (1 − t) D/E)`;
  `Firm Value = Operating Assets + Cash`; `Equity = Firm Value − Gross Debt`.
- Net debt approach: cash is assumed funded entirely with riskless debt.
  `Net Debt = Gross Debt − Cash`; `k_d,net = (Interest Expense − rf × Cash)/(Debt − Cash)`;
  `Levered Beta = Unlevered Beta × (1 + (1 − t) × Net Debt/Equity)`; `Equity = Operating Assets − Net Debt`.

**Reference data — how holding cash distorts blended multiples:**

| Component | Capital Invested | After-tax Earnings | Value | PE | P/BV |
|---|---|---|---|---|---|
| Operating assets | 1,000 | 125 | 1,250 | 10.0 | 1.25 |
| Cash | 250 | 10 | 250 | 25.0 | 1.00 |
| Firm (blended) | 1,250 | 135 | 1,500 | 11.1 | 1.20 |

Cash is valued at a 4% riskfree rate (10/0.04 = 250), so it carries a PE of 25. Blending it with an operating business on a PE of 10 lifts the reported firm PE to 11.1. Gross multiples of cash-rich firms are inflated for this reason alone.

**Procedure:**
1. Split the balance sheet: operating assets versus cash and marketable securities.
2. Strip interest income on cash out of the earnings you forecast.
3. Estimate beta from the operating business (bottom-up, from comparable operating firms), not from a regression that mixes in the cash.
4. Value the operating assets with that discount rate.
5. Add cash back, adjusted if you can defend a discount or premium ([[marginal-value-of-cash]]).
6. Choose gross or net debt consistently, and adjust the cost of debt accordingly. The firm's stated blended borrowing rate can never be used directly in either WACC.
7. Decide how much cash is *operating* cash (needed for day-to-day liquidity). Operating cash belongs inside working capital; only the excess is added back as a separate asset.

**Worked example (gross versus net debt, `GrossvsNet.xls`):** Balance sheet: gross debt 500, cash 250. Earnings: after-tax operating earnings 125 in perpetuity, cash earnings 10. Rates: tax 40%, riskfree 4%, ERP 5%, unlevered beta 1.42, stated cost of debt 5.9% (so total interest = 29.5). The system is circular and must be solved iteratively.
- **Gross debt:** debt allocated to cash = 250 × (500/1,491.246) = 83.82, assumed riskless. `k_d,gross = (29.5 − 0.04 × 83.82)/416.18 = 6.283%`. Levered beta = 1.42(1 + 0.6 × 500/991.246) = 1.8498; `k_e = 13.249%`; WACC = 10.0705%. Operating assets = 125/0.100705 = 1,241.25. Firm = 1,491.25. Equity = **991.25**.
- **Net debt:** cash is funded with riskless debt, so `k_d,net = (29.5 − 0.04 × 250)/250 = 7.8%`. Levered beta = 1.42(1 + 0.6 × 250/924.775) = 1.6503; `k_e = 12.252%`; WACC = 10.6403%. Operating assets = 125/0.106403 = 1,174.78. Equity = 1,174.78 − 250 = **924.78**.
- The two agree only at a 0% tax rate. As the tax rate rises they diverge, and the net debt approach gives the **lower** value, because it assumes the tax benefit of debt funding cash is fully offset by tax on the cash's interest income.

**Determinism:**
- DETERMINISTIC: the split of value into operating assets plus cash; the multiples distortion table; both gross- and net-debt equity values, given the inputs (solved as a fixed point, converging in well under 50 iterations).
- JUDGMENT: how much cash is operating rather than excess; whether to use the gross or net debt frame; the unlevered beta of the operating business. Judgment needs the firm's liquidity needs, working-capital seasonality, and comparable-company betas.

**Pitfalls:**
- Leaving interest income in the cash flows *and* adding cash back — a straight double count.
- Using a regression beta for a cash-rich firm, which understates operating risk.
- Using the stated firm-wide cost of debt inside either WACC without the cash adjustment.
- Comparing a cash-rich firm's PE to a peer's without noticing that cash alone inflates it.
- Switching between gross and net debt part way through a valuation, or netting cash against debt while also adding cash back.

**Sources:**
- valpacket1spr21 p.220
- valpacket1spr20 p.216
- reconciliation (GrossvsNet.xls — both sheets)

**Related:** [[marginal-value-of-cash]], [[equity-value-bridge]], [[defining-debt-for-cost-of-capital]], [[bottom-up-beta]], [[cost-of-capital]], [[ddm-fcfe-reconciliation]]
