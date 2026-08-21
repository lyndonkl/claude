# Qualitative debt trade-off assessment

**Core idea:** Part V of the corporate finance project asks whether *this* firm should use debt, before any spreadsheet computes an optimum. It is a three-lens argument. Debt's main benefit is the tax shield, which is worth more when operating cash flow is large relative to firm value. Debt's second benefit is discipline over managers, which matters less when diversified institutions already own the firm. Debt's main cost is expected bankruptcy cost, which rises with earnings volatility and falls with credit quality. The section also asks where each existing financing instrument sits on the debt-equity continuum. Done well, this part *predicts* the mechanical optimum computed in Part VI, and disagreement between the two is a signal to re-examine both.

**Formulas:**
- Tax-benefit proxy: EBITDA / Firm value. Higher ratio → more operating cash flow per dollar of value → greater debt capacity.
- Revenue volatility = standard deviation of revenue growth.
- EBIT volatility = standard deviation of EBIT growth. This is the bankruptcy-cost driver that matters, not revenue volatility.
- Discipline proxy: % of shares held by institutional investors, compared against the industry average.

**Procedure:**
1. **Inventory the financing.** List every instrument used to raise funds and place it on the continuum between pure debt and pure equity — straight debt, leases, convertibles, preferred, equity.
2. **Tax benefit.** Compute EBITDA/Firm value and compare it to the industry average. Rank the firms in the peer set: the highest ratio should have the highest optimal debt ratio, the lowest the lowest.
3. **Discipline.** Compute institutional holdings and compare to the industry average. High diversified-institutional ownership means the disciplinary role of debt is less needed. See [[stockholder-analysis-marginal-investor]].
4. **Bankruptcy cost.** Gauge it two ways: volatility of operations and current credit rating. Compute the standard deviation of revenue growth *and* of EBIT growth. Stable revenue with volatile EBIT is still risky — operating leverage transmits small revenue moves into large earnings moves.
5. **Form the qualitative verdict.** Too much or too little debt, and roughly where the optimum should sit relative to peers.
6. **Check for pending events.** An in-flight acquisition raises earnings uncertainty and argues for holding debt below the mechanical optimum.
7. **Check rating-agency behaviour.** Agencies apply qualitative criteria and penalise fast moves toward the optimum, which is a reason to move gradually even when the capacity exists.
8. Carry the ranking into Part VI and check it against the computed optimum. See [[optimal-debt-ratio-wacc-schedule]].

**Reference data:** Spring 2015 debt-capacity indicators.

| Item | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Marginal tax rate | 35% | 35% | 35% | 35% |
| EBITDA ($m) | 3,791 | 9,612 | 829 | 1,897 |
| Firm value ($m, market) | 58,147 | 92,392 | 21,220 | 12,387 |
| EBITDA / value | 6.52% | 10.40% | 3.90% | 15.31% |
| EBITDA / value, industry avg | 7.88% | 8.21% | 8.21% | 8.36% |
| Institutional holdings | 78.09% | 68.91% | 92.00% | 98.48% |
| Institutional holdings, industry avg | 48.46% | 58.06% | 58.06% | 50.80% |
| Revenue volatility (sd of revenue growth) | 1.75% | 5.45% | 4.36% | 2.38% |
| Credit rating | A− | A− | BBB | BBB |

Prediction from the table: Tyson (EBITDA/value 15.31%, the highest) should carry the most debt; Chipotle (3.90%, the lowest) the least. Part VI confirmed it — computed optima of 60% for Tyson and 30% for Chipotle.

Published data sets for this part: debt ratios by industry; trade-off variables by industry.

**Worked example:** Tyson Foods, 2015. Tax benefit: EBITDA/value of 15.31% is nearly double the 8.36% industry average, so Tyson has the most debt capacity in the group. Discipline: institutional holdings of 98.48% against a 50.80% industry average mean debt is not needed to discipline management. Bankruptcy cost: revenue growth volatility is a mild 2.38%, but EBIT growth volatility is 16.16% — operating leverage makes earnings far less stable than sales. Tyson had just bought Hillshire Brands (August 2014, $63.00/share cash, ~$300m of claimed synergies from operational efficiency, purchasing, distribution, supply chain, raw materials, combined sales and marketing, and shared services). It funded the deal with roughly $5.7bn of debt plus roughly $2.1bn of equity specifically to preserve its investment-grade rating. Verdict: the debt raised sits well within capacity (optimum around 60% versus an actual 35.5%), but three factors argue against moving fast — EBIT volatility, acquisition uncertainty, and rating-agency penalties for rapid moves.

**Determinism:** DETERMINISTIC — EBITDA/value, both volatility measures, institutional holdings, and the comparison of each against its industry average. The peer ranking implied by EBITDA/value is mechanical. JUDGMENT — the whole trade-off verdict. It needs the instrument inventory, the identity of the marginal investor, the credit rating and rating-agency criteria, knowledge of pending strategic events, and a view on how much operating volatility the business can absorb.

**Pitfalls:**
- Judging stability from revenue volatility alone. Tyson's revenue was stable at 2.38% while its EBIT swung at 16.16%.
- Assuming a high EBITDA/value ratio automatically justifies moving to the mechanical optimum immediately. Capacity and timing are separate questions.
- Ignoring the discipline lens when ownership is concentrated in insiders, where debt's disciplinary benefit is largest.
- Doing Part V *after* Part VI and reverse-engineering the qualitative story to match the spreadsheet. The prediction has value only if made first.

**Sources:**
- corporate_finance--project--cfproj p.8
- corporate_finance--project--food2015 p.10

**Related:** [[optimal-debt-ratio-wacc-schedule]], [[recapitalization-value-and-stress-test]], [[debt-design-deliverable]], [[stockholder-analysis-marginal-investor]], [[corporate-finance-project-blueprint]]
