# Cash returned = dividends plus buybacks

**Core idea:** Any assessment of payout policy that looks only at dividends is wrong for a modern US firm. Buybacks now account for roughly 60% of cash returned by US companies, and they behave differently from dividends: they are flexible, one-time, and carry no expectation of repetition. The correct measure of what a firm gives back to stockholders is **augmented dividends** — dividends plus stock buybacks. Using this measure changes the ranking of firms dramatically, and it is the number that must be compared with FCFE. The choice between the two forms is a separate question, driven by stockholder preferences, the permanence of the cash surplus, and tax treatment.

**Formulas:**
- Cash returned to stockholders = Dividends + Stock Buybacks. Also called **Augmented Dividends** in valuation contexts.
- Cash payout ratio = (Dividends + Buybacks) / Net Income.
- Buyback share of payout = Buybacks / (Dividends + Buybacks).
- Cash returned as % of FCFE = (Dividends + Buybacks) / FCFE. Compute this for each FCFE variant (pre-debt, actual-debt, target-debt-ratio); see [[fcfe-potential-dividends]].
- Effective total yield = (Dividends + Net Buybacks) / Market Capitalization. Use *net* buybacks (repurchases minus new share issuance) if the firm issues stock to employees, or the gross figure overstates the return.

**Procedure:**
1. Pull dividends paid on common stock and stock repurchases from the financing section of the cash flow statement, for each of the last 5 years.
2. Net the buyback figure against equity issuance if the firm has a large stock-compensation program. Gross repurchases at such a firm partly offset dilution rather than returning cash.
3. Sum both series over the period. Report dividends, buybacks, and the total separately — the split is as informative as the total.
4. Compute the cash payout ratio and the buyback share. A high buyback share means the firm has deliberately retained flexibility.
5. Compare the total with FCFE over the same period, using all three FCFE variants ([[fcfe-potential-dividends]]), and classify the firm as an accumulator or an overpayer.
6. Recommend the *form* of any change in payout on these rules:
   - One-time or uncertain cash surplus → buyback (or special dividend). No stickiness commitment.
   - Recurring, predictable surplus at a mature firm → dividend increase, which the market reads as a commitment.
   - Investor base is income-seeking (see [[clientele-effect]]) → dividends.
   - Investor base is taxable and prefers deferral, or management believes the stock is undervalued → buybacks.
7. When comparing against peers or against a regression prediction, either add buybacks on both sides or explicitly flag that the dividend-only comparison understates payout. This is the single most common error in peer analysis ([[peer-group-payout-analysis]], [[market-regression-payout-prediction]]).

**Reference data:**

*Cash returned by the five case companies, 2008–2012 (millions; Disney and Vale in $, Tata Motors in ₹, Baidu in RMB, Deutsche Bank in €):*

| Year | Disney Div | Disney Buybacks | Vale Div | Vale Buybacks | Tata Div | Tata Buybacks | Baidu Div | Baidu Buybacks | DB Div | DB Buybacks |
|---|---|---|---|---|---|---|---|---|---|---|
| 2008 | 648 | 648 | 2,993 | 741 | 7,595 | 0 | 0 | 0 | 2,274 | 0 |
| 2009 | 653 | 2,669 | 2,771 | 9 | 3,496 | 0 | 0 | 0 | 309 | 0 |
| 2010 | 756 | 4,993 | 3,037 | 1,930 | 10,195 | 0 | 0 | 0 | 465 | 0 |
| 2011 | 1,076 | 3,015 | 9,062 | 3,051 | 15,031 | 0 | 0 | 0 | 691 | 0 |
| 2012 | 1,324 | 4,087 | 6,006 | 0 | 15,088 | 970 | 0 | 0 | 689 | 0 |
| **2008–12** | **4,457** | **15,412** | **23,869** | **5,731** | **51,405** | **970** | **0** | **0** | **4,428** | **0** |

Disney returned more than three times as much through buybacks as through dividends. Vale and Tata Motors used mainly dividends. Baidu returned nothing. Deutsche Bank used dividends only.

*Regional buyback intensity (January 2020):* the US returned 60.13% of its cash via buybacks and Canada 48.21%, while China (5.40%), Africa/Middle East (5.45%) and Small Asia (9.70%) remain almost pure dividend markets. Japan sits in between at 37.64%. Both the US and Canada returned more than 100% of net income (111.49% and 111.79%).

*Trend (S&P 500, 1988–2019):* buybacks were about a third of cash returned in 1988, dropped below 20% around 1991, exceeded dividends from the late 1990s, and reached about 60–72% through the 2000s and 2010s. In 2019, buybacks ≈ $770bn against dividends ≈ $480bn.

**Worked example — Disney 2008–2012:** Dividends $4,457M, buybacks $15,412M, so cash returned = **$19,869M**. Net income over the period was $23,895M, so the cash payout ratio = 19,869 / 23,895 = **83.2%**, against a dividend payout ratio of 4,457 / 23,895 = **18.7%**. Buyback share = 15,412 / 19,869 = **77.6%**. Now compare with FCFE: cash returned is 114.8% of pre-debt FCFE ($17,301M), 73.2% of actual-debt FCFE ($27,126M), and 110.0% of target-debt-ratio FCFE ($18,065M). Anyone looking only at the 18.7% dividend payout would call Disney a cash hoarder; the full picture shows it returned essentially everything it could afford.

**Determinism:**
- DETERMINISTIC: cash returned, cash payout ratio, buyback share, total yield, and cash-returned-to-FCFE ratios — all from cash flow statement line items, net income, and market cap.
- JUDGMENT: whether to net buybacks against issuance, and by how much. Whether a given buyback is a genuine return of cash or an offset to stock compensation dilution. Which form of payout suits the investor base. Whether the historical mix of dividends and buybacks will persist.

**Pitfalls:**
- Using dividends alone. It is the defining error in payout analysis and it mis-ranks US firms by a factor of two or more.
- Using gross repurchases at a firm that issues large amounts of stock to employees. Net buybacks are the cash actually returned.
- Treating buybacks as a permanent policy. They are deliberately discretionary, which is their main advantage over dividends.
- Assuming buybacks create value per share by shrinking the count. They do not by themselves; see [[buyback-value-and-eps-effect]].
- Comparing a US firm's payout with an Asian peer group without adjusting for the buyback gap.
- Adding buybacks to dividends but forgetting to add them on the FCFE side of the comparison. FCFE is the capacity for *both*.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.156-157
- corporate_finance--lecture_slides--cfpacket2spr20 p.192
- corporate_finance--lecture_slides--cfpacket2spr20 p.233
- corpfin-payout-projects — dividends.xls, sheet `Analysis of past dividends` (row 13, rows 35–37)

**Related:** [[fcfe-potential-dividends]], [[buyback-value-and-eps-effect]], [[dividend-empirical-facts]], [[cash-trust-assessment]], [[clientele-effect]], [[dividend-payout-and-yield-measures]]
