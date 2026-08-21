# Total beta for undiversified owners

**Core idea:** Beta measures only the risk an investment adds to a **diversified** portfolio. Owners of most private businesses are not diversified — their wealth is concentrated in the one firm — so they bear total risk, not just market risk. Using a market beta for such an owner understates the required return and therefore overstates the value of the business. Total beta scales the market beta up by dividing by the correlation between the business and the market. Since the R² of a beta regression is the share of risk that is market risk, the square root of R² is that correlation. Dividing by a correlation below 1 always raises the beta, and for a typical private-firm comparable set the increase is roughly a doubling.

**Formulas:**
- **Total Beta = Market Beta / Correlation of the business with the market = Market Beta / sqrt(R²)**.
- **Total Cost of Equity = Riskfree rate + Total Beta × ERP**.
- Because R² = (systematic variance)/(total variance) and correlation = sqrt(R²), total beta ≥ market beta always, with equality only when the business is perfectly correlated with the market.
- Underlying decomposition: Systematic variance = β² × Var(market); Unsystematic variance = Var(stock) − Systematic variance; R² = Systematic / Total.

**Procedure:**
1. Establish that the marginal investor in this asset is **not** diversified. Typical cases: a family-owned private firm, a founder selling to an individual buyer, an owner whose entire net worth is the business.
2. Estimate the market beta first, by the comparable-firm route in [[non-traded-asset-betas]] — unlever the comparables' median beta, correct for cash, relever at the assumed D/E.
3. Get the **median R²** of the comparable firms' own beta regressions. Take its square root to get the correlation of the sector with the market.
4. Total beta = market beta / correlation.
5. Cost of equity = riskfree rate + total beta × ERP.
6. Use the total-beta cost of equity when valuing the business **from the undiversified owner's perspective** (a fair value to that owner, or a divorce/estate/tax valuation). Use the market-beta cost of equity when the buyer is a diversified public acquirer or a financial buyer with a diversified portfolio. The gap between the two values is the diversification benefit the buyer brings, and it is negotiable.
7. If the owner is partially diversified, the correlation to divide by can be adjusted upward toward 1 to reflect the fraction of wealth in the business.

**Reference data:**

Bookscape comparables (eleven publishing and book-retail firms): median levered beta 0.8130, median gross D/E 21.41%, median cash/firm value 5.00%, **median R² = 26.00%** → correlation = sqrt(0.26) = **0.5099**.

Effect of the adjustment for Bookscape:

| Measure | Market beta | Total beta |
|---|---|---|
| Beta | 0.8558 | 1.6783 |
| Cost of equity (Rf 2.75%, ERP 5.5%) | 7.46% | 11.98% |

The correlation of a typical sector with the market is around 0.5, so total betas run near twice market betas, and costs of equity rise by half or more.

The related concept check: for a diversified investor choosing between Disney (beta 1.25, R² 73%) and Amgen (beta 1.25, R² 25%), the correct answer is indifference — same beta, same expected return, and the firm-specific portion diversifies away. An **undiversified** investor, who bears total risk, prefers the higher-R² stock, because less of its risk is firm-specific.

**Worked example (Bookscape):** Bookscape's market beta from comparables is 0.8558 and the median R² of those comparables is 26.00%.

- Correlation with the market = sqrt(0.26) = 0.5099.
- Total beta = 0.8558 / 0.5099 = **1.6783**.
- Total cost of equity = 2.75% + 1.6783 × 5.5% = **11.98%**, against 7.46% on the market beta.

At a perpetual cash flow of $1 a year, the owner's value is $1/0.1198 = $8.35 while a diversified buyer's value is $1/0.0746 = $13.40. The 60% gap is exactly the value of diversification, and it is why private businesses are usually worth more to public acquirers than to their founders.

**Determinism:**
- DETERMINISTIC: (market beta, R²) → total beta; (Rf, total beta, ERP) → total cost of equity; (comparable R² values) → median R².
- JUDGMENT: whether the marginal investor is undiversified; whether the comparables' median R² represents this business's correlation with the market; how to handle partial diversification; whether a valuation should be done from the owner's or the buyer's perspective (often both, to frame the negotiation).

**Pitfalls:**
- Applying total beta when the buyer is diversified. It understates value for no reason.
- Using the *firm's own* R² when the firm is not traded. You must borrow the comparables' median R².
- Confusing total beta with an adjusted beta or a small-cap premium. It is a different correction, and stacking them double-counts.
- Assuming a private-firm owner's undiversification is permanent. An owner planning an IPO in two years is closer to the diversified case.
- Forgetting that a very low R² produces an enormous total beta. A sector R² of 0.05 gives a correlation of 0.224 and quadruples the beta, which should prompt a check of whether the comparables are right.
- Using total beta and *also* adding an illiquidity discount to the value without checking whether the two overlap.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.141-142, p.179, p.181-182
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.87-88
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.85-86

**Related:** [[non-traded-asset-betas]], [[bottom-up-beta]], [[alternative-relative-risk-measures]], [[capm-cost-of-equity]], [[private-company-valuation]], [[illiquidity-discount]]
