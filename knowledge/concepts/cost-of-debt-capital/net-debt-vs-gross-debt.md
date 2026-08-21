# Net debt versus gross debt

**Core idea:** Analysts in Europe and Latin America often subtract cash from debt before computing debt ratios. That is the net-debt convention. It produces very different levered betas and very different cost-of-capital weights from the gross-debt convention. Neither is wrong. What IS wrong is mixing them. If you lever the beta with a net debt ratio, you must weight the cost of capital with the net debt ratio too. Done consistently, the two conventions give roughly the same cost of capital even though they give quite different costs of equity — the lower net-debt cost of equity is offset by a lower (or negative) debt weight.

**Formulas:**
- Gross debt ratio: D/E = Total debt / Market value of equity.
- Net debt: Net debt = Total debt − Cash and marketable securities.
- Net debt ratio: (D − Cash) / Market value of equity. It can be negative when cash exceeds debt.
- Levered beta, gross: β_L = β_u × [1 + (1 − t) × (D/E)].
- Levered beta, net: β_L = β_u × [1 + (1 − t) × ((D − Cash)/E)].
- Cost of capital under the net convention: the debt weight must be Net debt / (Net debt + E), and the value you get is the value of the OPERATING business excluding cash, so cash is not added back separately.

**Procedure:**
1. Pick a convention up front and write it down.
2. Gross-debt route (Damodaran's default in the corporate finance packet):
   - Unlever comparable betas with gross D/E and strip cash out of the unlevered beta separately, using Business unlevered beta = Company unlevered beta / (1 − Cash/Firm value).
   - Relever at the firm's gross market D/E.
   - Weight the cost of capital with gross debt and full equity.
   - Value the operating business, then ADD cash back at the end.
3. Net-debt route:
   - Unlever and relever with net D/E.
   - Weight the cost of capital with net debt.
   - The resulting value is already net of cash; do not add cash back.
4. Check that the D/E used in the beta and the D/(D+E) used in the weights are the same convention and the same number.
5. Watch for a negative net debt ratio. It produces a levered beta BELOW the unlevered beta and a negative debt weight. That is arithmetically fine but easy to mis-handle downstream.

**Reference data:** Embraer, from the valuation packets (millions of Brazilian reais): debt 1,953; cash 2,320; market value of equity 11,042; unlevered beta 0.95; marginal tax rate 34%.

| Convention | Debt measure | D/E ratio | Levered beta |
|---|---|---|---|
| Gross | 1,953 | 1,953 / 11,042 = 18.95% | 0.95 × [1 + 0.66 × 0.1895] = 1.07 |
| Net | 1,953 − 2,320 = −367 | −367 / 11,042 = −3.32% | 0.95 × [1 + 0.66 × (−0.0332)] = 0.93 |

Related cash-adjustment mechanics from the same material (gross-debt route): a comparable firm's unlevered beta is a portfolio of its operating business and its cash, and cash has a beta of zero. So Company unlevered beta = (Cash/Value) × 0 + (1 − Cash/Value) × Business beta, which rearranges to Business beta = Company unlevered beta / (1 − Cash/Value). For US movie firms with a median unlevered beta of 1.0668 and median cash/firm value of 2.96%, the pure movie-business beta is 1.0668 / (1 − 0.0296) = 1.0993. The net-debt shortcut on the same firms gives 1.24 / [1 + 0.6 × 0.2330] = 1.0879 — close, but not identical.

**Worked example:** Embraer's cost of equity under both conventions, with a 4.29% riskfree rate and a 4% mature-market premium (ignoring the country premium for clarity).
- Gross: cost of equity = 4.29% + 1.07 × 4% = 8.57%. Debt weight = 1,953 / (1,953 + 11,042) = 15.03%.
- Net: cost of equity = 4.29% + 0.93 × 4% = 8.01%. Net debt weight = −367 / (−367 + 11,042) = −3.44%.
- With a 9.29% pre-tax cost of debt and a 34% tax rate: gross gives 8.57% × 0.8497 + 6.13% × 0.1503 = 8.20%. Net gives 8.01% × 1.0344 + 6.13% × (−0.0344) = 8.07%. The two land close, as they should — and the residual gap reflects how the cash is being treated, not a difference in business risk.

**Determinism:**
- DETERMINISTIC: debt, cash, market equity, unlevered beta and the tax rate → both D/E ratios, both levered betas, both sets of weights, both costs of capital.
- JUDGMENT: which convention to adopt. The choice needs the analyst's downstream valuation structure (does the model add cash back at the end?), the audience's conventions, and whether the firm's cash is genuinely excess or is operating cash.
- JUDGMENT: how much of the cash balance counts as cash. Trapped foreign cash, minimum operating cash, and cash pledged as collateral all complicate the subtraction.

**Pitfalls:**
- Levering the beta with net debt and weighting the cost of capital with gross debt. This is the error the whole concept exists to prevent, and it produces a cost of capital that is too low.
- Using the net convention and then also adding cash back to the value of operations. That double counts cash.
- Assuming the net-debt cost of equity is "better" because it is lower. It is lower because the risk of the cash has been removed from the equity; the value implication is offset elsewhere.
- Netting cash against debt when the cash cannot actually be used to repay debt.
- Mishandling a negative debt weight in code that assumes weights are non-negative.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.98
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.96
- corporate_finance--lecture_slides--cfpacket1spr20 p.168, p.170-171 (cash adjustment to unlevered betas under the gross convention)
- corporate_finance--lecture_slides--cfpacket1spr20 p.195 (market-value weights)

**Related:** [[market-value-weights]], [[what-counts-as-debt]], [[cost-of-capital-assembly]], [[bottom-up-beta]], [[levered-beta]], [[cash-and-valuation]]
