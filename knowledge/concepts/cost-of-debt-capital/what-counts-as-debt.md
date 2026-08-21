# What counts as debt

**Core idea:** Before you can compute a cost of debt or a debt weight, you must decide what "debt" is. Damodaran defines debt by three characteristics, not by where an item sits on the balance sheet. First, it commits the firm to fixed future payments. Second, those payments are tax deductible. Third, missing them can cause default and hand control of the firm to the party owed. Anything meeting all three is debt, whether or not the accountant calls it debt. So debt = all interest-bearing liabilities, short-term and long-term, PLUS all lease obligations, operating as well as capital. It excludes non-interest-bearing liabilities such as accounts payable. The same three-part test applied to the income statement is the "financial expense" test. Operating-lease rent passes that test, which is why it is a financial expense misclassified as an operating expense.

**Formulas:**
- Total debt for cost of capital = Market value of interest-bearing debt (short-term + long-term) + Debt value of operating leases + Straight-debt component of any convertible/hybrid debt.
- Debt for the D/(D+E) weight is measured at MARKET value, never book value.
- Net debt (an alternative convention) = Total debt − Cash and marketable securities. If you use net debt anywhere (levering beta), you must use it everywhere (cost-of-capital weights).

Symbols: "interest-bearing" = any liability on which the firm accrues and pays interest, including commercial paper, revolvers, notes payable, bank loans, bonds, and the current portion of long-term debt.

**Procedure:**
1. Take the balance sheet and list every liability line item.
2. For each item, apply the three tests: fixed contractual payment? tax deductible? non-payment triggers default/loss of control?
   - All three yes → debt.
   - Accounts payable, accrued expenses, deferred taxes, pension underfunding treated as an operating item, minority interest → NOT debt under this test (though deferred taxes and unfunded pensions may be handled as separate value adjustments elsewhere).
3. Include short-term interest-bearing debt. Do not exclude it because it is "temporary" — it is a real claim.
4. Read the lease footnote. Capitalize operating-lease commitments (see [[operating-leases-as-debt]]) and add the resulting debt value to both book and market debt.
5. If the firm has convertible debt, split it (see [[convertible-debt-decomposition]]) and put only the straight-debt component in debt.
6. Decide preferred stock's treatment (see [[preferred-stock-cost]]): it is a separate third component of capital, or lumpable with debt if it is < 5% of the firm's market value.
7. Convert the resulting book debt to market value (see [[market-value-of-debt]]) before computing weights.
8. Consistency check: the interest expense you use for the interest coverage ratio must correspond to the debt you counted. If you capitalize leases, add the imputed lease interest to interest expense.

**Reference data:** No lookup table. Classification checklist:

| Item | Debt for cost of capital? | Why |
|---|---|---|
| Bank loans, notes payable, bonds, commercial paper | Yes | Fixed, deductible, default-triggering |
| Current portion of long-term debt / short-term debt | Yes | Same three tests |
| Capital (finance) leases | Yes | Already on balance sheet as debt |
| Operating leases | Yes — capitalize them | Fixed, deductible, non-payment costs you the asset/business |
| Convertible bond — straight-debt component | Yes | Bond half of the hybrid |
| Convertible bond — conversion option | No — equity | Option value, no fixed claim |
| Preferred stock | Separate component (or with debt if < 5% of firm value) | Fixed dividend but NOT tax deductible |
| Accounts payable, accruals | No | Non-interest-bearing supplier credit |
| Deferred taxes, minority interest | No | Not a contractual fixed payment to a lender |

**Worked example:** Disney, 2013 (fiscal year data used throughout the corporate finance packet). Book interest-bearing debt was $14,288 million. Treated as one coupon bond with coupon = $349m interest expense, 7.92-year weighted-average maturity, discounted at Disney's 3.75% pre-tax cost of debt, its market value is $13,028 million. Disney's operating-lease commitments capitalized at 3.75% add $2,933 million. Total debt used in the cost of capital = $13,028 + $2,933 = $15,961 million, against a market value of equity of $121,878 million, giving debt and equity weights of 11.58% and 88.42%.

**Determinism:**
- DETERMINISTIC: once each liability is classified, summing debt, capitalizing leases (commitments + pre-tax cost of debt → lease debt), and converting book to market debt (book debt, interest expense, maturity, cost of debt → market debt) are pure arithmetic a script computes.
- JUDGMENT: the classification itself for ambiguous items (unfunded pension obligations, securitized receivables, guarantees, take-or-pay contracts, underfunded healthcare obligations). The judgment needs: the footnote text describing whether the payment is contractual and unavoidable, whether it is tax deductible, and what happens on non-payment.
- JUDGMENT: whether to work in gross or net debt terms — and the resulting requirement to be consistent between the beta relevering and the cost-of-capital weights.

**Pitfalls:**
- Leaving operating leases out of debt. Pre-2019 statements hid them entirely; leaving them out understates debt, overstates the equity weight, overstates operating income's quality and inflates return on capital.
- Counting accounts payable as debt because it is a "liability". It carries no interest and no default trigger of this kind.
- Excluding short-term debt as "not permanent capital".
- Using book debt in the weights. See [[market-value-weights]].
- Mixing conventions: levering the beta with net debt but weighting the cost of capital with gross debt.
- Treating a convertible bond wholly as debt (overstates debt, understates equity and the cost of capital's equity weight).

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.184-185
- corporate_finance--lecture_slides--cfpacket1spr20 p.196-197, p.199
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.120
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.113
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls, Cost of Capital worksheet debt block (straight debt, convertible, leases, preferred)

**Related:** [[operating-leases-as-debt]], [[market-value-of-debt]], [[market-value-weights]], [[convertible-debt-decomposition]], [[preferred-stock-cost]], [[cost-of-capital-assembly]], [[net-debt-vs-gross-debt]]
