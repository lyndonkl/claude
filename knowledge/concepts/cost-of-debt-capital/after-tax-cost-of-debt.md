# After-tax cost of debt

**Core idea:** Interest on debt is tax deductible, so the firm's real cost of borrowing is the pre-tax rate net of the tax saving. That saving is the entire tax advantage of debt in the cost-of-capital framework, and it enters the WACC through the (1 − t) factor on the cost of debt. It does NOT enter the cash flows. Free cash flow to the firm is built from EBIT × (1 − tax rate), with no interest tax shield added, precisely because the shield is already in the discount rate. Putting it in both places double counts. The tax rate used is the MARGINAL rate, not the effective rate.

**Formulas:**
- After-tax cost of debt = Pre-tax cost of debt × (1 − marginal tax rate).
  - Pre-tax cost of debt = Riskfree rate + Default spread (see [[cost-of-debt-estimation-routes]]).
  - Marginal tax rate = the rate on the next dollar of income in the jurisdiction whose deduction the firm actually gets.
- Tax benefit per year = Interest expense × Marginal tax rate.
- In the WACC: Cost of capital = Cost of equity × E/(D+E) + Pre-tax cost of debt × (1 − t) × D/(D+E).
- FCFF = EBIT × (1 − t) − (CapEx − Depreciation) − Change in non-cash working capital. No interest tax shield term.

**Procedure:**
1. Compute the pre-tax cost of debt.
2. Choose the marginal tax rate.
   - Use the statutory marginal rate of the country where the interest is deducted. Country marginal rates are tabulated in [[country-risk-in-cost-of-debt]].
   - Do not use the effective tax rate (taxes paid / taxable income) here. The effective rate reflects deferrals and one-off items; the marginal rate is what the next dollar of interest saves.
   - Where the firm's taxable income is negative or too small to absorb the deduction, the marginal rate on the next dollar of interest is effectively zero until the shelter is used up. Model that explicitly if it matters.
3. Multiply: after-tax cost of debt = pre-tax × (1 − t).
4. Use the SAME t in the WACC as in the levering of the beta. Consistency across the model matters more than precision in the rate.
5. Keep the tax shield out of the cash flows.

**Reference data:** After-tax costs of debt for the corporate finance packet's running companies (2013/14):

| Company | Pre-tax cost of debt | Marginal tax rate | After-tax cost of debt |
|---|---|---|---|
| Disney | 3.75% (US$) | 36.10% | 2.40% |
| Deutsche Bank | 2.75% (Euro) | 29.48% | 1.94% |
| Vale | 4.05% (US$) | 34.00% | 2.67% |
| Bookscape | 4.05% (US$) | 40.00% | 2.43% |
| Tata Motors | 9.62% (Rupee) | 32.45% | 6.50% |
| Baidu | ~4.60% (RMB) | 25.00% | 3.45% |

Selected marginal tax rates (wacccalc.xls `Country risk and taxes`, January 2020 vintage): United States 40.00%; United Kingdom 21.00%; Germany 29.58%; France 33.33%; Japan 35.64%; China 25.00%; India 33.99%; Brazil 25.00%; Canada 26.50%; Australia 30.00%; Ireland 12.50%; Singapore 17.00%; Switzerland 17.92%; Mexico 30.00%; Russia 20.00%; South Africa 28.00%; Korea 30.00%; Italy 31.40%; Spain 30.00%; Netherlands 25.00%.

**Worked example:** Disney, 2013. Actual S&P rating A → default spread 1.00%. Riskfree rate 2.75% in US dollars → pre-tax cost of debt = 3.75%. Marginal tax rate 36.1% → after-tax cost of debt = 3.75% × (1 − 0.361) = 2.40%. In Disney's cost of capital, that 2.40% carries an 11.58% weight: 8.52% × 0.8842 + 2.40% × 0.1158 = 7.81%.

Contrast with Embraer, 2004: pre-tax cost of debt 9.29%, Brazil marginal rate 34% → the WACC term is 9.29% × (1 − 0.34) × 0.16 = 0.98 percentage points of the 9.97% total.

**Determinism:**
- DETERMINISTIC: pre-tax cost of debt and marginal tax rate → after-tax cost of debt. Interest expense and tax rate → annual tax benefit.
- JUDGMENT: which marginal tax rate applies. That needs the firm's jurisdiction of borrowing, its jurisdictional income mix, whether it has current taxable income to absorb the deduction, and whether any interest-deductibility cap applies. Damodaran's own note in the accounting-return spreadsheet is that the marginal rate is more robust than the effective rate, even though it produces lower measured returns.
- JUDGMENT: whether to model a tax rate that changes over time (e.g. an effective rate today converging to a marginal rate later). If so, the after-tax cost of debt changes over time too.

**Pitfalls:**
- Using the effective tax rate. It is backward-looking and distorted by deferrals.
- Applying the tax shield twice — once in the discount rate and again as an add-back in the cash flows.
- Giving a loss-making firm a full tax shield when it has no taxable income to shelter.
- Using different tax rates in the levered beta formula and the WACC.
- Using a US rate against a foreign cost of debt, or vice versa.
- Forgetting that preferred dividends are NOT tax deductible, so no (1 − t) factor applies to the cost of preferred stock ([[preferred-stock-cost]]).

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.191, p.200-202
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.111, p.115, p.119
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.108, p.112, p.116
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls tax-rate block (B38/B39/B40), after-tax cost of debt C64, and `Country risk and taxes` marginal tax rates
- spreadsheet doc `corpfin-ratings-risk` — returncalculator.xls note that the marginal rate is more robust than the effective rate

**Related:** [[cost-of-debt-estimation-routes]], [[cost-of-capital-assembly]], [[country-risk-in-cost-of-debt]], [[preferred-stock-cost]], [[fcff]], [[marginal-vs-effective-tax-rate]]
